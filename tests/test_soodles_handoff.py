"""End-to-end FactoryWeaver side: validated REQ/card inventory to Soodles proposal.

No effect, no Soodles Issue admission, and no producer-truth claim.
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
from soodles_handoff import export, materialize
from factoryweaver import ContractError

FIXTURE = ROOT / "docs/evals/cs329z-hw1/drill.json"
SCRIPT = ROOT / "scripts/soodles_handoff.py"


class ScopeHandoffTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.selection = {
            "requirement_ids": ["REQ-email-qa"],
            "card_ids": ["C-retrieval-grounding", "SPEC-email-qa", "V-email-qa"],
            "goal": "Email QA references only IDs actually returned for this question.",
            "measurement": "Official deterministic test_email_qa checks support and search budget.",
            "persistence": "Continue only on observed failure with original requirement preserved.",
            "stop_and_escalation": "Selected test oracle and original owner readback decide acceptance.",
            "causal_change": "Ground answer/support behavior in the search result for one request.",
            "acceptance": ["No unseen support IDs; finite search hops and valid response shape."],
            "constraints": ["Preserve original adapter signatures and original effect boundary."],
            "prompt_delta": [
                "Use only search-returned email IDs in the support list.",
                "Handle malformed replies and empty searches without invented evidence."
            ],
        }

    def test_export_is_lossless_proposal_not_execution(self):
        bundle = export(self.record, self.selection)
        self.assertEqual(set(bundle), {"protocol", "kind", "knowledge_record", "selection"})
        self.assertEqual(bundle["protocol"], "factoryweaver/soodles-scope/v1")
        self.assertEqual(bundle["kind"], "SOURCE_BOUND_PROPOSAL")
        self.assertEqual(bundle["knowledge_record"], self.record)
        self.assertEqual(bundle["selection"], self.selection)
        self.assertEqual(len(bundle["knowledge_record"]["requirements"]), 13)
        self.assertEqual(len(bundle["knowledge_record"]["cards"]), 6)
        self.assertNotIn("sha256", bundle)
        self.assertNotIn("argv", bundle)
        self.assertNotIn("effect_authority", bundle)

    def test_selection_rejects_unbound_or_unresolved_references(self):
        cases = [
            ("requirement_ids", ["REQ-missing"], "unknown_requirement"),
            ("card_ids", ["V-unregistered"], "unknown_card"),
            ("measurement", "", "invalid:measurement"),
            ("prompt_delta", [""], "invalid:prompt_delta"),
            ("acceptance", [], "invalid:acceptance"),
        ]
        for key, changed, reason in cases:
            with self.subTest(key=key), self.assertRaisesRegex(ContractError, reason):
                export(self.record, {**self.selection, key: changed})
        with self.assertRaisesRegex(ContractError, "exact_fields"):
            export(self.record, {**self.selection, "fake_digest": "123"})
        with self.assertRaisesRegex(ContractError, "scope_selection_unknown_card"):
            export(self.record, {**self.selection, "card_ids": ["SPEC-email-qa", "C-phantom"]})

    def test_reject_false_original_knowledge_and_reused_retired_card(self):
        record = copy.deepcopy(self.record)
        target = next(r for r in record["requirements"] if r["id"] == "REQ-email-qa")
        target["knowledge_status"] = "CONFLICTED"
        unknown = export(record, self.selection)
        self.assertEqual(
            next(r for r in unknown["knowledge_record"]["requirements"]
                 if r["id"] == "REQ-email-qa")["knowledge_status"], "CONFLICTED")
        record = copy.deepcopy(self.record)
        target = next(c for c in record["cards"] if c["stable_id"] == "SPEC-email-qa")
        target["status"] = "SUPERSEDED"
        with self.assertRaisesRegex(ContractError, "retired_or_superseded"):
            export(record, self.selection)
        record = copy.deepcopy(self.record)
        target = next(r for r in record["requirements"] if r["id"] == "REQ-email-qa")
        target["delivery_status"] = "RELEASE_CONFIRMED"
        with self.assertRaisesRegex(ContractError, "untrusted_delivery_claim"):
            export(record, self.selection)

    def test_cli_emits_a_portable_standalone_bundle_without_side_effect(self):
        with tempfile.TemporaryDirectory() as temp:
            selected = Path(temp) / "selection.json"
            selected.write_text(json.dumps(self.selection), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(FIXTURE), str(selected)],
                capture_output=True, text=True, timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), export(self.record, self.selection))
            self.assertEqual(list(Path(temp).iterdir()), [selected])

    def test_unrelated_reqs_and_knowledge_persist_with_no_truncation(self):
        bundle = export(self.record, self.selection)
        all_req = {r["id"] for r in bundle["knowledge_record"]["requirements"]}
        self.assertIn("REQ-guardrails", all_req)
        self.assertIn("REQ-memory", all_req)
        self.assertNotIn("REQ-guardrails", bundle["selection"]["requirement_ids"])
        self.assertEqual(set(self.selection["card_ids"]),
                         {c for c in bundle["selection"]["card_ids"]})


    def test_host_materializes_one_exact_reader_binding_and_reuses_it(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "bundle.json"
            first = materialize(self.record, self.selection, str(target))
            self.assertEqual(first["status"], "MATERIALIZED_PROPOSAL")
            self.assertEqual(first["consumer"], "soodles.knowledge.inspect")
            self.assertEqual(first["reader_arguments"],
                             [str(target), first["bundle"]["sha256"]])
            self.assertFalse(first["effect_authority"])
            self.assertFalse(first["authorizes_landing"])
            self.assertEqual(json.loads(target.read_text()), export(self.record, self.selection))
            self.assertEqual(materialize(self.record, self.selection, str(target)), first)
            self.assertEqual(list(Path(temp).iterdir()), [target])

    def test_host_binding_refuses_foreign_or_unknown_write(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "bundle.json"
            target.write_text('{"different":true}', encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "conflict_requires_original_readback"):
                materialize(self.record, self.selection, str(target))
            self.assertEqual(target.read_text(), '{"different":true}')
            target.unlink()
            first = materialize(self.record, self.selection, str(target))
            changed = {**self.selection, "causal_change": "An actually different scoped change."}
            with self.assertRaisesRegex(ContractError, "conflict_requires_original_readback"):
                materialize(self.record, changed, str(target))
            self.assertEqual(materialize(self.record, self.selection, str(target)), first)
            with self.assertRaisesRegex(ContractError, "absolute_path_required"):
                materialize(self.record, self.selection, "relative/bundle.json")

    def test_cli_host_output_is_an_exact_binding_not_model_generated_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            input_path = Path(temp) / "selection.json"
            target = Path(temp) / "bundle.json"
            input_path.write_text(json.dumps(self.selection), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(FIXTURE), str(input_path),
                 "--output", str(target)], capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            receipt = json.loads(result.stdout)
            self.assertEqual(receipt["bundle"]["path"], str(target))
            self.assertEqual(receipt["reader_arguments"][0], str(target))
            self.assertEqual(json.loads(target.read_text()), export(self.record, self.selection))
            second = subprocess.run(
                [sys.executable, str(SCRIPT), str(FIXTURE), str(input_path),
                 "--output", str(target)], capture_output=True, text=True, timeout=15)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(json.loads(second.stdout), receipt)


if __name__ == "__main__":
    unittest.main()
