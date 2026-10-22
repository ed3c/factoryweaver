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
        self.assertEqual(result["requirements"], 22)
        self.assertEqual(result["cards"], 74)

    def test_all_locked_human_decisions_preserved_without_forged_confirmation(self):
        decisions = {item["id"]: item["choice"] for item in self.coverage["decisions"]}
        self.assertEqual(len(decisions), 16)
        for i in range(1, 11):
            self.assertEqual(decisions[f"MRL-{i:02d}"], "B" if i == 9 else "A")
        for decision_id in ("HOF-01", "FWC-01", "FWC-02", "FWP-01", "FWP-02", "FWP-03"):
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

    def test_source_clause_mapping_and_first_false_dependency(self):
        ids = {c["stable_id"] for c in self.record["cards"]}
        self.assertEqual(len(self.coverage["source_clauses"]), 25)
        self.assertTrue(all(c["card"] in ids for c in self.coverage["source_clauses"]))
        rr = {r["id"]: r for r in self.record["requirements"]}
        self.assertNotIn("REQ-mrl-closure", rr["REQ-mrl-spec-record"].get("depends_on", []))
        self.assertNotIn("REQ-mrl-cards", rr["REQ-mrl-session"].get("depends_on", []))
        self.assertIn("REQ-mrl-migration-method", rr)

    def test_specific_consumer_spec_and_verification(self):
        cards = {c["stable_id"]: c for c in self.record["cards"]}
        for slug in ("retrieval", "math", "interfaces", "session", "ui-effects"):
            self.assertIn("Producer:", cards["SPEC-"+slug]["payload"])
            self.assertIn("Consumer:", cards["SPEC-"+slug]["payload"])
            self.assertIn("Inputs and conditions:", cards["SPEC-"+slug]["payload"])
            self.assertIn("Positive input/control:", cards["V-"+slug]["payload"])
            self.assertIn("Negative mutation:", cards["V-"+slug]["payload"])

    def test_original_card_delta_preserves_revision_history(self):
        from card_delta import compile_delta
        original = json.loads((SPEC/"history"/"project-before-fwp.json").read_text(encoding="utf-8"))
        receipt = compile_delta(original, self.record, batch_size=4)
        self.assertEqual(len(receipt["patch"]), 4)
        self.assertFalse(receipt["effect_authority"])
        before = {c["stable_id"]: c for c in original["cards"]}
        for c in self.record["cards"]:
            if c["stable_id"] not in before:
                self.assertEqual(c["revision"], 1)
            else:
                old = before[c["stable_id"]]
                self.assertEqual(c["revision"], old["revision"]+int(
                    {k:v for k,v in old.items() if k!="revision"} !=
                    {k:v for k,v in c.items() if k!="revision"}))

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
