import copy
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from factoryweaver import ContractError, load, verify
from record_prepare import prepare
import record_prepare


class RecordPreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "intent.txt"
        self.source.write_text("Keep the original line order.\n")
        self.draft = {
            "subject": {"scope": "Order-preserving line deduplication", "consumer": "local task"},
            "sources": {"intent": {"path": str(self.source), "source_type": "human_decision", "locator": "whole source"}},
            "requirements": {"order": {"statement": "Keep first-occurrence order.", "claim_kind": "NORMATIVE",
                "source_ids": ["intent"], "owner": "Session", "acceptance": ["b,a,b returns b,a"],
                "knowledge_status": "SPECIFIED", "engineering_status": "CONTRACT_DEFINED",
                "delivery_status": "NOT_STARTED", "falsifier": "Sorted output violates input order."}},
            "cards": [{"canonical_key": "local|SPEC|dedupe|order|text|contract", "series": "SPEC", "status": "ACTIVE",
                       "title": "Stable line order", "payload": "Return the first occurrence of each line in its original position.",
                       "evidence_ids": ["intent"], "typed_links": [{"relation": "implements", "target": "order"}]}],
            "progress": {axis: {"state": state, "evidence_refs": ["intent"]} for axis, state in
                         (("knowledge", "SPECIFIED"), ("engineering", "CONTRACT_DEFINED"), ("delivery", "NOT_STARTED"))}}
        self.path = self.root / "draft.json"
        self.save()

    def save(self):
        self.path.write_text(json.dumps(self.draft))

    def test_cli_binds_real_sources_and_reuses_identical_concurrent_requests(self):
        target = self.root / "v1"
        argv = [sys.executable, str(ROOT / "scripts/factoryweaver.py"), "prepare", str(self.path), "--output", str(target)]
        with ThreadPoolExecutor(2) as pool:
            results = list(pool.map(lambda _: subprocess.run(argv, capture_output=True, text=True), range(2)))
        self.assertTrue(all(run.returncode == 0 for run in results), [run.stderr for run in results])
        first, second = [json.loads(run.stdout) for run in results]
        self.assertEqual(first, second)
        record = load(first["record"]["path"])
        self.assertTrue(verify(record)["valid"])
        self.assertEqual(record["cards"][0]["typed_links"][0]["target"], record["requirements"][0]["id"])
        self.assertEqual((target / "sources" / record["sources"][0]["sha256"]).read_bytes(), self.source.read_bytes())
        self.assertFalse(first["effect_authority"])
        wrong = subprocess.run([sys.executable, str(ROOT / "scripts/factoryweaver.py"),
                                "validate", first["record"]["path"], "--previous", first["record"]["path"]],
                               text=True, capture_output=True)
        self.assertEqual(wrong.returncode, 2)
        self.assertIn("preparation_arguments_require_prepare", wrong.stderr)

    def test_publication_refuses_symlink_directories_without_writing_outside_output(self):
        outside = self.root / "outside"
        outside.mkdir()
        target = self.root / "prepared"
        target.mkdir()
        (target / "sources").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ContractError, "output_directory"):
            prepare(self.path, target)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((target / "record.json").exists())
        alias = self.root / "alias"
        alias.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ContractError, "output_directory"):
            prepare(self.path, alias / "nested")
        self.assertEqual(list(outside.iterdir()), [])

    def test_revision_keeps_identity_sources_and_old_failure(self):
        first = prepare(self.path, self.root / "v1")
        before = load(first["record"]["path"])
        self.source.write_text("Keep the original line order. Prior sorted output failed.\n")
        self.draft["cards"][0]["payload"] += " Reject sorted output; prior failure remains in source history."
        self.save()
        second = prepare(self.path, self.root / "v2", first["record"]["path"])
        after = load(second["record"]["path"])
        self.assertEqual(before["cards"][0]["stable_id"], after["cards"][0]["stable_id"])
        self.assertEqual(after["cards"][0]["revision"], 2)
        self.assertEqual(len(after["sources"]), 2)
        self.assertEqual(load(self.root / "v2/previous.json"), before)
        self.assertEqual(load(first["record"]["path"]), before)
        self.assertTrue((self.root / "v2/delta.json").is_file())

    def test_progress_only_cli_binds_evidence_without_changing_specification(self):
        first = prepare(self.path, self.root / "v1")
        before = load(first["record"]["path"])
        observation = self.root / "owner.txt"
        observation.write_text("Original owner is waiting; no execution completed.\n")
        self.draft["sources"]["owner"] = {"path": str(observation), "source_type": "other", "locator": "owner readback"}
        self.draft["progress"]["delivery"] = {"state": "OWNER_WAIT", "evidence_refs": ["owner"]}
        self.save()
        target = self.root / "progress"
        argv = [sys.executable, str(ROOT / "scripts/factoryweaver.py"), "prepare", str(self.path),
                "--output", str(target), "--previous", first["record"]["path"], "--progress-only"]
        with ThreadPoolExecutor(2) as pool:
            runs = list(pool.map(lambda _: subprocess.run(argv, capture_output=True, text=True), range(2)))
        self.assertEqual([run.returncode for run in runs], [0, 0], [run.stderr for run in runs])
        replies = [json.loads(run.stdout) for run in runs]
        self.assertEqual(replies[0], replies[1])
        after = load(replies[0]["record"]["path"])
        self.assertEqual(after["cards"], before["cards"])
        self.assertEqual(after["requirements"], before["requirements"])
        self.assertEqual(after["progress"]["delivery"]["state"], "OWNER_WAIT")
        evidence = after["progress"]["delivery"]["evidence_refs"]
        self.assertEqual(evidence, [replies[0]["references"]["sources"]["owner"]])
        self.assertEqual(replies[0]["change_scope"], "progress_only")
        self.assertFalse(replies[0]["effect_authority"])
        self.assertTrue(load(target / "input.json")["progress_only"])
        with self.assertRaisesRegex(ContractError, "output_conflict"):
            prepare(self.path, target, first["record"]["path"])

    def test_progress_only_rejects_specification_changes_before_publication(self):
        first = prepare(self.path, self.root / "v1")
        original = copy.deepcopy(self.draft)
        for field in ("cards", "requirements"):
            with self.subTest(field=field):
                self.draft = copy.deepcopy(original)
                if field == "cards":
                    self.draft[field][0]["payload"] = "Sorted output is now allowed."
                else:
                    self.draft[field]["order"]["acceptance"] = ["Sorted output is allowed."]
                self.save()
                target = self.root / field
                with self.assertRaisesRegex(ContractError, "progress_only_specification_changed"):
                    prepare(self.path, target, first["record"]["path"], progress_only=True)
                self.assertFalse(target.exists())
                allowed = prepare(self.path, target, first["record"]["path"])
                self.assertTrue(verify(load(allowed["record"]["path"]))["valid"])

    def test_progress_only_requires_previous_and_prepare_command(self):
        with self.assertRaisesRegex(ContractError, "progress_only_requires_previous"):
            prepare(self.path, self.root / "missing", progress_only=True)
        self.assertFalse((self.root / "missing").exists())
        first = prepare(self.path, self.root / "v1")
        run = subprocess.run([sys.executable, str(ROOT / "scripts/factoryweaver.py"),
                              "validate", first["record"]["path"], "--progress-only"],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertIn("preparation_arguments_require_prepare", run.stderr)

    def test_installed_bundle_prepares_without_source_checkout(self):
        import build_skill_bundle
        bundle = self.root / "portable"
        build_skill_bundle.build(bundle)
        run = subprocess.run([sys.executable, str(bundle / "scripts/factoryweaver.py"),
                              "prepare", str(self.path), "--output", str(self.root / "prepared")],
                             cwd=self.root, text=True, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["completion"], "COMPILED_ONLY")

    def test_unchanged_revision_is_noop_and_old_output_cannot_be_replaced(self):
        first = prepare(self.path, self.root / "v1")
        second = prepare(self.path, self.root / "v2", first["record"]["path"])
        self.assertEqual(load(first["record"]["path"]), load(second["record"]["path"]))
        self.draft["cards"][0]["payload"] = "This is a changed semantic contract."
        self.save()
        with self.assertRaisesRegex(ContractError, "output_conflict"):
            prepare(self.path, self.root / "v1")

    def test_interrupted_attempt_rejects_changed_source_and_resumes_original_bytes(self):
        target = self.root / "interrupted"
        original = self.source.read_bytes()
        publish = record_prepare.publish

        def interrupt(path, raw):
            result = publish(path, raw)
            if Path(path).name == "input.json":
                raise OSError("interrupted after attempt binding")
            return result

        with patch.object(record_prepare, "publish", side_effect=interrupt):
            with self.assertRaisesRegex(OSError, "interrupted"):
                prepare(self.path, target)
        self.source.write_text("Changed source after interruption.\n")
        with self.assertRaisesRegex(ContractError, "output_conflict"):
            prepare(self.path, target)
        self.assertFalse((target / "record.json").exists())
        self.source.write_bytes(original)
        resumed = prepare(self.path, target)
        self.assertTrue(verify(load(resumed["record"]["path"]))["valid"])

    def test_rejects_removed_history_and_unknown_links_before_output(self):
        first = prepare(self.path, self.root / "v1")
        self.draft["cards"] = []
        self.save()
        with self.assertRaisesRegex(ContractError, "card_history_removed"):
            prepare(self.path, self.root / "v2", first["record"]["path"])
        self.assertFalse((self.root / "v2").exists())
        self.draft["requirements"]["order"]["depends_on"] = ["not registered"]
        self.save()
        with self.assertRaisesRegex(ContractError, "unknown_semantic_reference"):
            prepare(self.path, self.root / "invalid")

    def test_rejects_model_id_and_unsupported_completion_claims(self):
        original = copy.deepcopy(self.draft)
        self.draft["cards"][0]["stable_id"] = "invented"
        self.save()
        with self.assertRaisesRegex(ContractError, "without_identity"):
            prepare(self.path, self.root / "invalid")
        self.draft = original
        self.draft["requirements"]["order"]["engineering_status"] = "TESTED_SCOPED"
        self.save()
        with self.assertRaisesRegex(ContractError, "untrusted_test_claim"):
            prepare(self.path, self.root / "invalid")
        self.assertFalse((self.root / "invalid").exists())


if __name__ == "__main__":
    unittest.main()
