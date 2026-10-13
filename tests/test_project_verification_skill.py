"""Project-local pstack verification skill: actual public CLI and repeatable maintenance."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".cursor/skills/verify-factoryweaver/scripts/verify.py"
FEATURE_DIR = ROOT / ".cursor/skills/verify-factoryweaver/features"
SPEC = importlib.util.spec_from_file_location("fw_project_verify", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ProjectLocalVerificationTests(unittest.TestCase):
    def test_upstream_skills_are_complete_and_manually_selected(self):
        pstack = ROOT / ".cursor/skills"
        for name in ("create-verification-skill", "maintain-verification-skill"):
            text = (pstack / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("disable-model-invocation: true", text)
        self.assertTrue((pstack / "create-verification-skill/references/feature-map-example/create-note.md").exists())
        self.assertTrue((pstack / "create-verification-skill/references/feature-map-example/search.md").exists())
        self.assertIn("MIT License", (ROOT / ".cursor/pstack-LICENSE").read_text())
        skill = (pstack / "verify-factoryweaver/SKILL.md").read_text()
        for section in ("## Launch", "## Doctor", "## Drive", "## Evidence",
                        "## Cleanup", "## Helpers", "## Maintain repeatedly"):
            self.assertIn(section, skill)

    def test_factoryweaver_guidance_routes_to_pstack_maintenance_not_auto_manager(self):
        for rel in ("AGENTS.md", "skills/factoryweaver/SKILL.md",
                    "skills/factoryweaver-verify/SKILL.md",
                    "docs/evals/factoryweaver-e2e-card-verification.md", "README.md"):
            with self.subTest(path=rel):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn("maintain-verification-skill", text)
                self.assertIn("verify-factoryweaver", text)
        guide = (ROOT / ".cursor/skills/verify-factoryweaver/SKILL.md").read_text()
        self.assertIn("blocked", guide)
        self.assertIn("source", guide.lower())

    def test_map_index_and_source_wave_cover_each_declared_feature(self):
        self.assertEqual(MODULE.doctor()["status"], "ready")
        source = [MODULE.source_wave(x) for x in MODULE.FEATURES]
        self.assertEqual(len(source), 5)
        self.assertTrue(all(item["status"] == "indexed" for item in source), source)
        for item in source:
            self.assertGreaterEqual(len(item["sources"]), 1)
            self.assertEqual(item["proof_ceiling"], "SOURCE_PATH_EXISTENCE_NOT_SOURCE_MEANING")

    def test_two_repeated_local_maintain_passes_keep_real_cli_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            product = (ROOT / "scripts/factoryweaver.py").read_bytes()
            for i in range(2):
                folder = root / f"pass-{i}"
                out = subprocess.run(
                    [sys.executable, str(SCRIPT), "maintain", "--scope", "local",
                     "--evidence-dir", str(folder)],
                    cwd=ROOT, capture_output=True, text=True, timeout=90)
                self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
                result = json.loads(out.stdout)
                self.assertEqual(result["outcome"], "clean")
                self.assertEqual(result["scope"], "local")
                statuses = {x["feature"]: x["status"] for x in result["features"]}
                self.assertEqual({key for key, value in statuses.items() if value == "cli-verified"},
                                 set(MODULE.FEATURES) - {"soodles-reader"})
                self.assertEqual(statuses["soodles-reader"], "excluded")
                self.assertIn("NOT_RUN", result["limits"])
                self.assertEqual(result["cleanup"], "scratch removed; evidence retained")
                self.assertTrue((folder / "source-wave.json").is_file())
                self.assertTrue((folder / "run.json").is_file())
                self.assertTrue((folder / "result.json").is_file())
                self.assertTrue((folder / "scope_handoff_conflict.invocation.json").is_file())
            self.assertEqual((ROOT / "scripts/factoryweaver.py").read_bytes(), product)

    def test_full_maintenance_reports_unreachable_native_not_a_clean_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            # A deliberately unbound checkout cannot become an unearned native PASS.
            absent = MODULE.drive("soodles-reader", Path(temp), Path(temp))
            if "SOODLES_CHECKOUT" not in __import__("os").environ:
                self.assertEqual(absent["status"], "verified-unreachable")
                self.assertIn("original Host", absent["prerequisite"])
            self.assertNotEqual(absent["status"], "native-e2e-passed")


if __name__ == "__main__":
    unittest.main()
