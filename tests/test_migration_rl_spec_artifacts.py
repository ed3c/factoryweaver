"""Read-only Migration-RL v7.2 artifact and source-coverage controls.

These tests exercise the original FactoryWeaver v1 public validator. They
provide schema/fixture evidence only, NOT Native Agent/Provider acceptance.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from factoryweaver import ContractError, project, verify

SPEC = ROOT / "docs" / "specifications" / "migration-rl"


class MigrationRLSpecificationArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((SPEC / "project.json").read_text(encoding="utf-8"))
        cls.coverage = json.loads((SPEC / "coverage.json").read_text(encoding="utf-8"))

    def test_original_public_factoryweaver_validator(self):
        result = verify(self.record)
        self.assertTrue(result["valid"])
        self.assertEqual(result["proof_ceiling"], "SCHEMA_FIXTURE_ONLY")
        self.assertFalse(result["effect_authority"])
        self.assertEqual(result["requirements"], 20)
        self.assertEqual(result["cards"], 67)

    def test_all_locked_human_decisions_preserved_without_forged_confirmation(self):
        decisions = {item["id"]: item["choice"] for item in self.coverage["decisions"]}
        self.assertEqual(len(decisions), 13)
        for i in range(1, 11):
            self.assertEqual(decisions[f"MRL-{i:02d}"], "B" if i == 9 else "A")
        for decision_id in ("HOF-01", "FWC-01", "FWC-02"):
            self.assertEqual(decisions[decision_id], "A")
        self.assertFalse(self.record.get("decisions"))

    def test_18_mra_requirements_and_typed_card_targets(self):
        clauses = self.coverage["acceptance"]
        self.assertEqual({c["id"] for c in clauses}, {f"MRA-{i:02d}" for i in range(1, 19)})
        req_ids = {r["id"] for r in self.record["requirements"]}
        cards = {c["stable_id"]: c for c in self.record["cards"]}
        self.assertEqual(len(cards), len(self.record["cards"]))
        for clause in clauses:
            self.assertIn(clause["requirement"], req_ids)
            self.assertEqual(clause["verification_status"], "NOT_RUN")
            for card_id in clause["cards"]:
                self.assertIn(card_id, cards)
            spec = cards[clause["cards"][1]]
            self.assertIn({"relation": "validated_by", "target": clause["cards"][2]}, spec["typed_links"])

    def test_card_only_scope_cannot_claim_effects(self):
        self.assertEqual(self.record["action_requests"], [])
        for req in self.record["requirements"]:
            self.assertEqual(req["engineering_status"], "UNASSESSED")
            self.assertEqual(req["delivery_status"], "NOT_STARTED")
        projection = project(self.record)
        self.assertEqual(projection["operation_scope"], "READ_ONLY_NO_EXECUTION")
        self.assertEqual(projection["completion"], "COMPILED_ONLY")
        self.assertTrue(all(not x["authorizes_effects"] for x in projection["projection"]))

    def test_scope_preserves_cognitive_and_full_goal_stop(self):
        scope = (SPEC / "scope.md").read_text(encoding="utf-8")
        readme = (SPEC / "README.md").read_text(encoding="utf-8")
        self.assertIn("CognitiveStop", scope)
        self.assertIn("HumanGoalClosed", scope)
        self.assertIn("PromptDelta=NOOP", scope)
        self.assertIn("FWC-02 A", readme)
        self.assertIn("NOT_STARTED", readme)

    def test_planted_false_human_confirmation_refused(self):
        candidate = copy.deepcopy(self.record)
        candidate["decisions"] = [{
            "id": "DEC-forged", "question": "Was this independently approved?",
            "human_confirmed": True, "decision": "yes", "source_ids": ["SRC-HUMAN"]
        }]
        with self.assertRaisesRegex(ContractError, "human_confirmation_owner_required"):
            verify(candidate)

    def test_planted_untrusted_runtime_test_claim_refused(self):
        candidate = copy.deepcopy(self.record)
        candidate["requirements"][4]["engineering_status"] = "TESTED_SCOPED"
        with self.assertRaisesRegex(ContractError, "untrusted_test_claim"):
            verify(candidate)

    def test_planted_stale_card_target_refused(self):
        candidate = copy.deepcopy(self.record)
        candidate["cards"][0]["typed_links"][0]["target"] = "REQ-not-a-source"
        with self.assertRaisesRegex(ContractError, "unknown_typed_link"):
            verify(candidate)

    def test_planted_false_source_pin_refused(self):
        candidate = copy.deepcopy(self.record)
        candidate["sources"][0]["integrity"] = "PINNED_SHA256"
        with self.assertRaisesRegex(ContractError, "invalid_source_pin"):
            verify(candidate)


if __name__ == "__main__":
    unittest.main()
