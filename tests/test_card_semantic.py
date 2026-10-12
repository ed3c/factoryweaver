"""Exercise real read-only card selection, per-series draft preflight and manager needs.

These are discriminating field/contract tests, not model semantic or native Host tests.
"""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import card_semantic as semantic


class CardSemanticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = semantic.registry()
        cls.series = tuple(cls.registry["cards"])

    def card(self, series="SPEC", source="INSPECTED"):
        fields = self.registry["cards"][series]["required_semantics"]
        return {
            "series": series,
            "title": "Grounded " + series + " behavior",
            "source_status": source,
            "evidence_topics": ["Actually inspected original contract and its failure path"] if source == "INSPECTED" else [],
            "semantics": {name: "Observed " + name.replace("_", " ") +
                          " and actual decision boundary for this behavior." for name in fields},
            "links": [],
        }

    def draft(self, card=None):
        c = card or self.card()
        return {
            "schema": "factoryweaver/card-semantic-proposal/v1",
            "cards": [c],
            "coverage": [{"source_unit": "the supplied behavior assertion",
                          "status": "MAPPED", "disposition": c["title"]}],
        }

    def need(self, test=None, hook=None):
        return {"schema": "factoryweaver/manager-needs/v1",
                "subject": "One grounded behavior scope",
                "test_need": test, "hook_need": hook}

    def test_select_only_requested_prompts_and_all_fifteen_distinct_contracts(self):
        result = semantic.select(list(self.series))
        self.assertEqual(len(result["prompts"]), 15)
        self.assertFalse(result["execution"])
        self.assertEqual({row["series"] for row in result["prompts"]}, set(self.series))
        for row in result["prompts"]:
            with self.subTest(series=row["series"]):
                self.assertTrue((ROOT / row["prompt"]).is_file())
                self.assertTrue(row["required_semantics"])
                self.assertNotIn("observed_result", row)
        sample = semantic.select(["K", "REQ"])
        self.assertEqual([i["series"] for i in sample["prompts"]], ["K", "REQ"])
        with self.assertRaisesRegex(semantic.ProposalError, "duplicate"):
            semantic.select(["C", "C"])
        with self.assertRaisesRegex(semantic.ProposalError, "unknown_card_series"):
            semantic.select(["NO_SUCH_TYPE"])

    def test_every_series_has_its_own_required_field_contract(self):
        for series in self.series:
            with self.subTest(series=series):
                card = self.card(series)
                result = semantic.inspect(self.draft(card))
                self.assertEqual(result["status"], "SHAPE_VALID_SEMANTICS_UNVERIFIED")
                self.assertEqual(result["independent_semantic_review"], "NOT_RUN")
                self.assertEqual(result["source_completeness"], "NOT_VERIFIED")
                self.assertFalse(result["effect_authority"])
                missing = copy.deepcopy(card)
                missing["semantics"].pop(next(iter(missing["semantics"])))
                with self.assertRaisesRegex(semantic.ProposalError, "wrong_semantic_fields"):
                    semantic.inspect(self.draft(missing))

    def test_k_and_q_may_name_missing_source_but_cannot_invent_concept(self):
        for series in ("K", "Q"):
            with self.subTest(series=series):
                self.assertEqual(
                    semantic.inspect(self.draft(self.card(series, "UNREAD")))["card_count"], 1
                )
        with self.assertRaisesRegex(semantic.ProposalError, "source_not_inspected"):
            semantic.inspect(self.draft(self.card("C", "UNREAD")))
        with self.assertRaisesRegex(semantic.ProposalError, "source_not_inspected"):
            semantic.inspect(self.draft(self.card("V", "MISSING")))

    def test_reject_generic_title_and_claim_to_know_unknown(self):
        card = self.card("C")
        card["semantics"]["mechanism"] = "Grounded C behavior"
        with self.assertRaisesRegex(semantic.ProposalError, "generic_or_self_repeated"):
            semantic.inspect(self.draft(card))
        card = self.card("SPEC")
        card["semantics"]["when"] = "TBD"
        with self.assertRaisesRegex(semantic.ProposalError, "generic_or_self_repeated"):
            semantic.inspect(self.draft(card))
        card = self.card("SPEC")
        card["execution_id"] = "model-invented-value"
        with self.assertRaisesRegex(semantic.ProposalError, "exact_fields"):
            semantic.inspect(self.draft(card))

    def test_link_target_direction_and_justification_have_discriminators(self):
        spec = self.card("SPEC")
        spec["links"] = [{
            "relation": "validated_by", "target_series": "V",
            "target_topic": "Email QA deterministic controls",
            "applicability": "When returned email support identifiers are checked",
            "counterfactual": "If verification changes, QA acceptance needs rechecking.",
        }]
        self.assertEqual(semantic.inspect(self.draft(spec))["card_count"], 1)
        reverse = self.card("V")
        reverse["links"] = [{**spec["links"][0], "target_series": "SPEC"}]
        with self.assertRaisesRegex(semantic.ProposalError, "validated_by_requires_V_target"):
            semantic.inspect(self.draft(reverse))
        bad = copy.deepcopy(spec)
        bad["links"][0]["counterfactual"] = ""
        with self.assertRaisesRegex(semantic.ProposalError, "unjustified_link"):
            semantic.inspect(self.draft(bad))
        unrelated = copy.deepcopy(spec)
        unrelated["links"][0]["relation"] = "not_registered"
        with self.assertRaisesRegex(semantic.ProposalError, "invalid_link_kind"):
            semantic.inspect(self.draft(unrelated))

    def test_coverage_must_account_for_declared_units_without_claiming_completeness(self):
        draft = self.draft()
        draft["coverage"].append({
            "source_unit": "unread Lecture 03 diagram", "status": "K",
            "disposition": "Source Reader must inspect this figure before a new C claim",
        })
        out = semantic.inspect(draft)
        self.assertEqual(out["declared_source_units"], 2)
        self.assertEqual(out["source_completeness"], "NOT_VERIFIED")
        draft["coverage"][-1]["status"] = "MAPPED"
        with self.assertRaisesRegex(semantic.ProposalError, "unbound_coverage"):
            semantic.inspect(draft)
        draft["coverage"][-1]["status"] = "K"
        draft["coverage"][-1]["source_unit"] = "the supplied behavior assertion"
        with self.assertRaisesRegex(semantic.ProposalError, "duplicate_source_coverage_unit"):
            semantic.inspect(draft)

    def test_no_test_or_hook_need_does_not_invent_a_manager_action(self):
        p = semantic.project_managers(self.need())
        self.assertEqual(p["test_manager"]["status"], "NO_TEST_SELECTION_REQUESTED")
        self.assertEqual(p["hook_manager"]["status"], "NO_NATIVE_HOOK_REQUIRED")
        self.assertEqual(p["manager_actions_performed"], [])
        self.assertFalse(p["effect_authority"])
        self.assertNotIn("next", p)
        self.assertNotIn("argv", p)

    def test_test_manager_is_single_original_control_owner_and_no_full_suite(self):
        need = {"changed_behavior": "Search support must contain only returned email IDs",
                "verification_question": "Are unseen support identifiers rejected?",
                "negative_case": "Unsupported citation from malformed model text"}
        projected = semantic.project_managers(self.need(test=need))
        plan = projected["test_manager"]
        self.assertEqual(plan["status"], "NEEDS_ORIGINAL_TEST_MANAGER_SELECTION")
        self.assertEqual(plan["owner"], "Soodles test-manager")
        self.assertEqual(plan["selected_controls"], "UNKNOWN")
        self.assertEqual(plan["test_execution"], "NOT_RUN")
        self.assertNotIn("commands", plan)
        self.assertEqual(projected["hook_manager"]["status"], "NO_NATIVE_HOOK_REQUIRED")
        self.assertFalse(projected["authorizes_landing"])

    def test_hook_manager_is_existing_native_owner_not_automatic_new_skill(self):
        native = {"native_event": "Stop",
                  "observed_requirement": "Original task-review decides whether to continue",
                  "source_state": "INSPECTED"}
        projection = semantic.project_managers(self.need(hook=native))
        hook = projection["hook_manager"]
        self.assertEqual(hook["owner"], "Soodles hook_manager.py / native Hook Owner")
        self.assertEqual(hook["status"], "NEEDS_ORIGINAL_HOOK_OWNER_READBACK")
        self.assertEqual(hook["native_execution"], "UNKNOWN")
        self.assertEqual(hook["original_owner_next"], "PRESERVE_ORIGINAL_UNMODIFIED")
        self.assertEqual(projection["manager_actions_performed"], [])
        missing = {**native, "source_state": "UNREAD"}
        self.assertEqual(semantic.project_managers(self.need(hook=missing))
                         ["hook_manager"]["status"], "NEEDS_NATIVE_SOURCE_OBSERVATION")
        forged = {**native, "next": {"argv": ["my-hook"]}}
        with self.assertRaisesRegex(semantic.ProposalError, "exact_fields"):
            semantic.project_managers(self.need(hook=forged))

    def test_cli_returns_non_authoritative_status_and_typed_refusal(self):
        script = ROOT / "scripts/card_semantic.py"
        okay = subprocess.run([sys.executable, str(script), "select", "REQ", "SPEC"],
                              capture_output=True, text=True)
        self.assertEqual(okay.returncode, 0, okay.stderr)
        self.assertFalse(json.loads(okay.stdout)["execution"])
        denied = subprocess.run([sys.executable, str(script), "select", "FAKE_CARD"],
                                capture_output=True, text=True)
        self.assertEqual(denied.returncode, 2)
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "semantic.json"
            source.write_text(json.dumps(self.draft()), encoding="utf-8")
            a = subprocess.run([sys.executable, str(script), "inspect", str(source)],
                               capture_output=True, text=True)
            self.assertEqual(a.returncode, 0, a.stderr)
            self.assertEqual(json.loads(a.stdout)["proof_ceiling"],
                             "FIELD_LINK_AND_DECLARED_COVERAGE_ONLY")


if __name__ == "__main__":
    unittest.main()
