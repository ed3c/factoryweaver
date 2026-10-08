"""Prove the FactoryWeaver skill is consumable without this source checkout."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_skill_bundle as builder


class PortableBundleTests(unittest.TestCase):
    def test_can_execute_in_foreign_project_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "other-project" / ".agents" / "skills" / "factoryweaver"
            first = builder.build(bundle)
            self.assertEqual(first["status"], "CREATED")
            self.assertGreater(first["files"], 9)
            self.assertEqual(builder.build(bundle)["status"], "NOOP")
            entry = (bundle / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(entry.startswith("---\nname: factoryweaver\n"))
            self.assertIn("references/compiler.md", entry)
            self.assertIn("references/verifier.md", entry)
            self.assertNotIn("../../", entry)
            self.assertTrue((bundle / "references/compiler.md").is_file())
            self.assertTrue((bundle / "contracts/v1/knowledge-record.schema.json").is_file())
            self.assertTrue((bundle / "scripts/factoryweaver.py").is_file())

            root = Path(tmp) / "other-project"
            script = str(bundle / "scripts/factoryweaver.py")
            grilling = str(bundle / "examples/matt-grilling/project.json")
            sample = str(bundle / "examples/openai-plugin-platform/project.json")
            registry = str(bundle / "examples/host-registry.example.json")
            for args in (["validate", grilling], ["project", grilling],
                         ["route", sample, "--registry", registry], ["cards", sample]):
                result = subprocess.run([sys.executable, script, *args],
                                        cwd=root, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            projected = subprocess.run([sys.executable, script, "project", grilling],
                                       cwd=root, capture_output=True, text=True)
            self.assertEqual(json.loads(projected.stdout)["projection"][0]["state"], "WAIT_FOR_HUMAN")

    def test_manifest_content_hashes_and_no_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "factoryweaver"
            builder.build(folder)
            manifest = json.loads((folder / "bundle-manifest.json").read_text())
            self.assertEqual(manifest["protocol"], "factoryweaver/portable-bundle-v1")
            self.assertFalse(manifest["effect_authority"])
            for item in manifest["files"]:
                file = folder / item["path"]
                self.assertTrue(file.is_file())
                self.assertFalse(file.is_symlink())
                self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), item["sha256"])
            self.assertFalse(any(path.name in ("soodles.py", "provider_credential.py")
                                 for path in folder.rglob("*")))

    def test_content_drift_or_unregistered_file_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "factoryweaver"
            builder.build(bundle)
            (bundle / "SKILL.md").write_text("tampered skill", encoding="utf-8")
            with self.assertRaisesRegex(builder.BundleError, "existing_bundle_content_drift"):
                builder.build(bundle)
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "factoryweaver"
            builder.build(bundle)
            (bundle / "new-unregistered.txt").write_text("stale file")
            with self.assertRaisesRegex(builder.BundleError, "existing_bundle_file_set_changed"):
                builder.build(bundle)

    def test_generated_bundle_checks_itself_without_source_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "foreign" / "factoryweaver"
            builder.build(bundle)
            checker = str(bundle / "scripts/check_bundle.py")
            def run():
                return subprocess.run([sys.executable, checker, str(bundle)],
                                      cwd=Path(tmp), text=True, capture_output=True)
            result = run()
            self.assertEqual(result.returncode, 0, result.stderr)
            status = json.loads(result.stdout)
            self.assertEqual(status["status"], "SELF_CONSISTENT")
            self.assertFalse(status["external_publisher_authenticated"])
            self.assertFalse(status["effect_authority"])
            (bundle / "SKILL.md").write_text("tampered entry", encoding="utf-8")
            result = run()
            self.assertEqual(result.returncode, 2)
            self.assertIn("content_digest_mismatch", result.stderr)

    def test_extra_bundle_file_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "factoryweaver"
            builder.build(folder)
            checker = folder / "scripts/check_bundle.py"
            subprocess_args = [sys.executable, str(checker), str(folder)]
            (folder / "unregistered.sh").write_text("echo unauthorized")
            p = subprocess.run(subprocess_args, capture_output=True, text=True)
            self.assertEqual(p.returncode, 2)
            self.assertIn("untracked_or_missing_bundle_file", p.stderr)

    def test_missing_canonical_source_is_a_hard_refusal(self):
        old = builder.FILES["references/compatibility.md"]
        try:
            builder.FILES["references/compatibility.md"] = "docs/nonexistent-missing-source.md"
            with self.assertRaisesRegex(builder.BundleError, "missing_or_symlink_source"):
                builder.generate()
        finally:
            builder.FILES["references/compatibility.md"] = old

    def test_deterministic_rebuild_from_frozen_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a" / "factoryweaver", Path(tmp) / "b" / "factoryweaver"
            first, second = builder.build(a), builder.build(b)
            self.assertEqual(first["manifest_sha256"], second["manifest_sha256"])
            self.assertEqual((a / "bundle-manifest.json").read_bytes(),
                             (b / "bundle-manifest.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
