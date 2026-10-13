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
    def test_source_only_skill_copy_is_incomplete_baseline(self):
        # Frozen causal baseline: a loader which copies only this source folder
        # lacks root-owned dependencies. The generated bundle is the treatment.
        source = ROOT / "skills/factoryweaver"
        with tempfile.TemporaryDirectory() as tmp:
            foreign = Path(tmp) / "unrelated-project" / ".agents" / "skills" / "factoryweaver"
            foreign.mkdir(parents=True)
            (foreign / "SKILL.md").write_bytes((source / "SKILL.md").read_bytes())
            original = (foreign / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("../../docs/compatibility.md", original)
            self.assertFalse((foreign / "../../docs/compatibility.md").resolve().is_file())
            self.assertFalse((foreign / "scripts/factoryweaver.py").is_file())
            installed = Path(tmp) / "complete-skill"
            builder.build(installed)
            self.assertIn("../../docs/compatibility.md",
                          (installed / "skills/factoryweaver/SKILL.md").read_text(encoding="utf-8"))
            self.assertTrue((installed / "docs/compatibility.md").is_file())
            self.assertTrue((installed / "scripts/factoryweaver.py").is_file())

    def test_can_execute_in_foreign_project_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "other-project" / ".agents" / "skills" / "factoryweaver"
            first = builder.build(bundle)
            self.assertEqual(first["status"], "CREATED")
            self.assertGreater(first["files"], 9)
            self.assertEqual(builder.build(bundle)["status"], "NOOP")
            entry = (bundle / "skills/factoryweaver/SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(entry.startswith("---\nname: factoryweaver\n"))
            self.assertIn("../factoryweaver-compile/SKILL.md", entry)
            self.assertIn("../factoryweaver-verify/SKILL.md", entry)
            self.assertIn("../../references/zettelkasten-v7.2.md", entry)
            self.assertTrue((bundle / "skills/factoryweaver-compile/SKILL.md").is_file())
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
            (bundle / "skills/factoryweaver/SKILL.md").write_text("tampered skill", encoding="utf-8")
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
            (bundle / "skills/factoryweaver/SKILL.md").write_text("tampered entry", encoding="utf-8")
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
        old = builder.FILES["docs/compatibility.md"]
        try:
            builder.FILES["docs/compatibility.md"] = "docs/nonexistent-missing-source.md"
            with self.assertRaisesRegex(builder.BundleError, "missing_or_symlink_source"):
                builder.generate()
        finally:
            builder.FILES["docs/compatibility.md"] = old

    def test_importing_clis_leave_distribution_replayable(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "distribution"
            builder.build(bundle)
            fixture = bundle / "examples/matt-grilling/project.json"
            env = dict(os.environ)
            env.pop("PYTHONDONTWRITEBYTECODE", None)
            result = subprocess.run([sys.executable, str(bundle / "scripts/card_delta.py"),
                                     str(fixture), str(fixture)], env=env,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "NOOP")
            self.assertEqual(builder.build(bundle)["status"], "NOOP")
            harness = bundle / ".cursor/skills/verify-factoryweaver/scripts/verify.py"
            result = subprocess.run([sys.executable, str(harness), "maintain", "--scope", "local"],
                                    capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_all_local_markdown_dependencies_preserve_canonical_paths(self):
        files = builder.generate()
        for name, raw in files.items():
            for target in builder.local_links(name, raw):
                self.assertTrue(target in files or any(p.startswith(target + "/") for p in files),
                                (name, target))
        self.assertIn("docs/soodles-manager-consumption.md", files)
        self.assertIn("references/card-prompts/README.md", files)
        self.assertEqual(files["skills/factoryweaver/SKILL.md"],
                         (ROOT / "skills/factoryweaver/SKILL.md").read_bytes())

    def test_installed_verifier_uses_virtual_root_and_refuses_partial_copy(self):
        verifier = ROOT / "scripts/verify_installed_skill.py"
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "installed"
            builder.build(bundle)
            result = subprocess.run([sys.executable, str(verifier), str(bundle)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            relative = subprocess.run([sys.executable, str(verifier), "installed"],
                                      cwd=Path(tmp), capture_output=True, text=True)
            self.assertEqual(relative.returncode, 0, relative.stderr)
            observed = json.loads(result.stdout)
            self.assertEqual(observed["status"], "INSTALLED_SKILL_REFERENCE_CLI_PASS")
            self.assertFalse(observed["actual_agent_invocation"])
            self.assertFalse(observed["installer_behavior_observed"])
            (bundle / "bundle-manifest.json").unlink()
            result = subprocess.run([sys.executable, str(verifier), str(bundle)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("partial_install", result.stderr)

    def test_tampered_installed_checker_is_not_executed(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "bundle"
            builder.build(bundle)
            marker = Path(tmp) / "executed"
            (bundle / "scripts/check_bundle.py").write_text(
                "from pathlib import Path\nPath(" + repr(str(marker)) + ").touch()\n"
                "print('{\"status\":\"SELF_CONSISTENT\"}')\n")
            result = subprocess.run([sys.executable, str(ROOT / "scripts/verify_installed_skill.py"),
                                     str(bundle)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("content_digest_mismatch", result.stderr)
            self.assertFalse(marker.exists())

    def test_symlink_roots_and_nested_paths_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "bundle"
            builder.build(bundle)
            alias = Path(tmp) / "alias"
            alias.symlink_to(bundle, target_is_directory=True)
            with self.assertRaisesRegex(builder.BundleError, "symlink_destination"):
                builder.build(alias)
            checker = ROOT / "scripts/check_bundle.py"
            result = subprocess.run([sys.executable, str(checker), str(alias)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("symlink_bundle_root", result.stderr)
            (bundle / "linked-directory").symlink_to(bundle / "docs", target_is_directory=True)
            result = subprocess.run([sys.executable, str(checker), str(bundle)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("symlink_bundle_path", result.stderr)

    def test_deterministic_rebuild_from_frozen_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a" / "factoryweaver", Path(tmp) / "b" / "factoryweaver"
            first, second = builder.build(a), builder.build(b)
            self.assertEqual(first["manifest_sha256"], second["manifest_sha256"])
            self.assertEqual((a / "bundle-manifest.json").read_bytes(),
                             (b / "bundle-manifest.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
