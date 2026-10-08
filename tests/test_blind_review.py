"""Blind review packet only: transport separation and negative controls."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from blind_review import pair
from factoryweaver import ContractError


def sample():
    return {
        "protocol": "factoryweaver/blind-comparison-v1",
        "case_id": "plugin-work-order-golden",
        "source_manifest_sha256": "a" * 64,
        "task": "Explain an evidence-preserving plugin work order from the identical source.",
        "frozen_conditions": {"source": "synthetic fixture only", "budget": "same"},
        "baseline_output": "An illustrative first output describes the feature without verification evidence.",
        "candidate_output": "A second illustrative output separates source claims, unknowns, a falsifier and an original owner readback.",
    }


class BlindComparisonTests(unittest.TestCase):
    def test_packet_contains_no_answer_key_or_success_claim(self):
        packet, key = pair(sample(), b"x" * 32)
        self.assertEqual(set(["A", "B"]), {k for k in packet if k in ("A", "B")})
        self.assertTrue({"v7.1", "v7.2"} == {key["A"], key["B"]})
        self.assertNotIn("baseline_output", packet)
        self.assertNotIn("candidate_output", packet)
        self.assertNotIn("separate_owner_custody_required", packet)
        self.assertEqual(packet["review_status"], "NOT_RUN")
        self.assertFalse(packet["independent_reviewer_verified"])
        self.assertFalse(packet["source_origin_verified"])
        self.assertFalse(packet["effect_authority"])
        self.assertEqual(packet["case_sha256"], key["case_sha256"])

    def test_repeat_with_same_seed_is_byte_stable(self):
        first, key1 = pair(sample(), b"x" * 32)
        second, key2 = pair(copy.deepcopy(sample()), b"x" * 32)
        self.assertEqual(first, second)
        self.assertEqual(key1, key2)

    def test_host_seed_changes_assignment_without_changing_candidate_bytes(self):
        outputs = set()
        for val in range(1, 64):
            packet, key = pair(sample(), bytes([val]) * 32)
            outputs.add(key["A"])
            self.assertEqual({packet["A"], packet["B"]},
                             {sample()["baseline_output"], sample()["candidate_output"]})
        self.assertEqual(outputs, {"v7.1", "v7.2"})

    def test_missing_or_weak_seed_refuses(self):
        for secret in (b"", b"0" * 31, b"\x00" * 32):
            with self.assertRaisesRegex(ContractError, "blind_seed_invalid"):
                pair(sample(), secret)

    def test_self_identifying_output_refuses_without_rewriting_original(self):
        record = sample()
        record["candidate_output"] += " The author says v7.2."
        with self.assertRaisesRegex(ContractError, "unredacted_version_label"):
            pair(record, b"x" * 32)

    def test_identical_outputs_and_missing_frozen_conditions_refuse(self):
        record = sample()
        record["baseline_output"] = record["candidate_output"]
        with self.assertRaisesRegex(ContractError, "identical_comparison_outputs"):
            pair(record, b"x" * 32)
        record = sample()
        record["frozen_conditions"] = {}
        with self.assertRaisesRegex(ContractError, "frozen_conditions_missing"):
            pair(record, b"x" * 32)

    def test_pair_input_changes_invalidate_packet_digest(self):
        first, _ = pair(sample(), b"x" * 32)
        revised = sample()
        revised["candidate_output"] += " More user-facing detail."
        second, _ = pair(revised, b"x" * 32)
        self.assertNotEqual(first["case_sha256"], second["case_sha256"])

    def test_cli_packet_and_key_are_separate_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            case_file, seed_file = directory / "case.json", directory / "seed.bin"
            case_file.write_text(json.dumps(sample()), encoding="utf-8")
            seed_file.write_bytes(b"x" * 32)
            base = [sys.executable, str(ROOT / "scripts/blind_review.py")]
            packet_result = subprocess.run(base + ["packet", str(case_file), "--seed-file",
                                                    str(seed_file)], capture_output=True, text=True)
            key_result = subprocess.run(base + ["key", str(case_file), "--seed-file",
                                                 str(seed_file)], capture_output=True, text=True)
            self.assertEqual(packet_result.returncode, 0, packet_result.stderr)
            self.assertEqual(key_result.returncode, 0, key_result.stderr)
            packet, key = json.loads(packet_result.stdout), json.loads(key_result.stdout)
            self.assertNotIn("separate_owner_custody_required", packet)
            self.assertTrue(key["separate_owner_custody_required"])
            self.assertEqual(packet["case_sha256"], key["case_sha256"])


if __name__ == "__main__":
    unittest.main()
