"""Adversarial fixtures for the curated v7.1/v7.2 semantic contract boundary."""
import copy
import json
import subprocess
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from semantic_golden import audit_fixture
from factoryweaver import ContractError

FIXTURE = ROOT / "tests/fixtures/semantic-golden.json"


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class SemanticGoldenTests(unittest.TestCase):
    def test_curated_fixture_has_distinct_decision_cases(self):
        value = audit_fixture(load_fixture())
        self.assertEqual(value["status"], "STRUCTURAL_GOLDEN_PASS")
        self.assertEqual(value["case_rows"], 4)
        self.assertEqual(value["decision_relevant_cases"], 3)
        self.assertEqual(value["cards"], 3)
        self.assertFalse(value["semantic_quality_proven"])
        self.assertEqual(value["human_review"], "REQUIRED_NOT_RUN")

    def test_same_case_split_across_cards_is_refused(self):
        data = load_fixture()
        data["cases"][1]["card_id"] = "C-source-invalidation"
        with self.assertRaisesRegex(ContractError, "same_case_fragmented"):
            audit_fixture(data)

    def test_independent_cases_collapsed_into_one_card_refused(self):
        data = load_fixture()
        data["cases"][2]["card_id"] = "N-unconfirmed-frontier"
        with self.assertRaisesRegex(ContractError, "independent_cases_collapsed"):
            audit_fixture(data)

    def test_narrative_turn_and_mechanism_are_required(self):
        data = load_fixture()
        data["cards"][0]["payload"]["turn"] = ""
        with self.assertRaisesRegex(ContractError, "missing_or_fragmentary_field"):
            audit_fixture(data)
        data = load_fixture()
        data["cards"][1]["payload"]["mechanism"] = "unknown"
        with self.assertRaisesRegex(ContractError, "missing_or_fragmentary_field"):
            audit_fixture(data)

    def test_action_card_requires_rollback_and_step_oracle(self):
        data = load_fixture()
        data["cards"][2]["payload"]["rollback"] = ""
        with self.assertRaisesRegex(ContractError, "missing_or_fragmentary_field"):
            audit_fixture(data)
        data = load_fixture()
        data["cards"][2]["payload"]["steps"][1]["failure_signal"] = ""
        with self.assertRaisesRegex(ContractError, "missing_or_fragmentary_field"):
            audit_fixture(data)

    def test_tested_claim_without_runtime_is_refused(self):
        data = load_fixture()
        data["cards"][2]["payload"]["execution_status"] = "TESTED"
        with self.assertRaisesRegex(ContractError, "unverified_practice_execution"):
            audit_fixture(data)

    def test_forged_reviewer_approval_refused(self):
        data = load_fixture()
        data["human_review"] = "APPROVED"
        with self.assertRaisesRegex(ContractError, "forged_human_review"):
            audit_fixture(data)

    def test_missing_case_and_duplicate_identity_refused(self):
        data = load_fixture()
        data["cases"][3]["card_id"] = "NONEXISTENT"
        with self.assertRaisesRegex(ContractError, "unbound_case_card"):
            audit_fixture(data)
        data = load_fixture()
        data["cases"][1]["id"] = data["cases"][0]["id"]
        with self.assertRaisesRegex(ContractError, "duplicate_case_identity"):
            audit_fixture(data)

    def test_skill_entries_reach_real_readonly_cli(self):
        compile_skill = (ROOT / "skills/factoryweaver-compile/SKILL.md").read_text()
        verify_skill = (ROOT / "skills/factoryweaver-verify/SKILL.md").read_text()
        self.assertIn("scripts/card_delta.py BEFORE.json AFTER.json", compile_skill)
        self.assertIn("scripts/card_delta.py BEFORE.json AFTER.json", verify_skill)
        self.assertIn("scripts/semantic_golden.py tests/fixtures/semantic-golden.json",
                      verify_skill)
        self.assertIn("scripts/source_lock.py MANIFEST.json SOURCE.txt", verify_skill)
        self.assertIn("scripts/blind_review.py packet CASE.json", verify_skill)
        for path in ("scripts/card_delta.py", "scripts/semantic_golden.py",
                     "scripts/source_lock.py", "scripts/blind_review.py",
                     "docs/card-delta-contract.md", "docs/semantic-golden.md",
                     "docs/source-lock.md", "docs/blind-pairwise.md"):
            self.assertTrue((ROOT / path).is_file(), path)
        example = ROOT / "examples/openai-plugin-platform/project.json"
        out = subprocess.run(
            [sys.executable, str(ROOT / "scripts/card_delta.py"),
             str(example), str(example)], capture_output=True, text=True
        )
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(json.loads(out.stdout)["status"], "NOOP")

    def test_card_without_case_never_counts_as_complete(self):
        data = load_fixture()
        card = copy.deepcopy(data["cards"][1])
        card["id"] = "C-unbound-orphan"
        data["cards"].append(card)
        with self.assertRaisesRegex(ContractError, "unmapped_golden_cards"):
            audit_fixture(data)


if __name__ == "__main__":
    unittest.main()
