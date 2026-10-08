"""Bounded mutation/negative controls for the public, no-effect card compiler."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from card_delta import compile_delta
from factoryweaver import ContractError

SAMPLE = ROOT / "examples/openai-plugin-platform/project.json"


def base_record():
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


def new_card(number):
    return {
        "stable_id": f"C-fixture-{number}",
        "canonical_key": f"C|fixture-{number}|demonstrates|case|portable|v1",
        "series": "C", "revision": 1, "status": "ACTIVE",
        "title": f"Independent case {number}",
        "payload": f"One intentionally distinct fixture case number {number}.",
        "evidence_ids": ["SRC-OPENAI-JD"], "typed_links": []
    }


class CardDeltaTests(unittest.TestCase):
    def test_exact_replay_is_noop(self):
        before = base_record()
        result = compile_delta(before, copy.deepcopy(before))
        self.assertEqual(result["status"], "NOOP")
        self.assertEqual(result["patch"], [])
        self.assertIsNone(result["next_cursor"])
        self.assertFalse(result["effect_authority"])

    def test_compatible_evidence_increment_preserves_identity(self):
        before, after = base_record(), base_record()
        original = before["cards"][0]
        after["cards"][0]["payload"] += " Additional independently proposed context."
        after["cards"][0]["revision"] += 1
        result = compile_delta(before, after)
        self.assertEqual(result["patch"][0]["operation"], "UPDATE")
        self.assertEqual(result["patch"][0]["card"]["stable_id"], original["stable_id"])
        self.assertEqual(result["patch"][0]["previous_revision"], original["revision"])
        self.assertEqual(result["status"], "DONE")

    def test_spurious_and_missing_revisions_refused(self):
        a, b = base_record(), base_record()
        b["cards"][0]["revision"] += 1
        with self.assertRaisesRegex(ContractError, "spurious_revision"):
            compile_delta(a, b)
        b = base_record()
        b["cards"][0]["payload"] += " Material new evidence."
        with self.assertRaisesRegex(ContractError, "revision_not_incremented"):
            compile_delta(a, b)

    def test_identity_change_or_history_deletion_refused(self):
        a, b = base_record(), base_record()
        b["cards"][0]["stable_id"] = "SPEC-replaced"
        with self.assertRaisesRegex(ContractError, "stable_id_changed"):
            compile_delta(a, b)
        b = base_record()
        b["cards"].clear()
        with self.assertRaisesRegex(ContractError, "card_history_removed"):
            compile_delta(a, b)

    def test_supersession_requires_retained_old_card(self):
        a, b = base_record(), base_record()
        previous = b["cards"][0]
        previous["status"] = "SUPERSEDED"
        previous["revision"] += 1
        replacement = new_card(90)
        replacement["typed_links"] = [{"relation": "supersedes", "target": previous["stable_id"]}]
        b["cards"].append(replacement)
        diff = compile_delta(a, b)
        self.assertEqual([x["operation"] for x in diff["patch"]], ["UPDATE", "CREATE"])
        self.assertIn(previous["stable_id"], diff["affected_nodes"])
        previous["status"] = "ACTIVE"
        previous["revision"] -= 1  # Isolate the supersession gate from spurious revision.
        with self.assertRaisesRegex(ContractError, "supersession_history_not_closed"):
            compile_delta(a, b)

    def test_twelve_card_lossless_batch_cursor(self):
        a, b = base_record(), base_record()
        b["cards"].extend(new_card(n) for n in range(13))
        one = compile_delta(a, b)
        self.assertEqual(one["status"], "CONTINUE")
        self.assertEqual(len(one["patch"]), 12)
        self.assertIsNotNone(one["next_cursor"])
        two = compile_delta(a, b, cursor=one["next_cursor"])
        self.assertEqual(two["status"], "DONE")
        self.assertEqual(len(two["patch"]), 1)
        keys = [x["card"]["canonical_key"] for x in one["patch"] + two["patch"]]
        self.assertEqual(len(keys), 13)
        self.assertEqual(len(set(keys)), 13)

    def test_stale_cursor_rejected_after_source_mutation(self):
        a, b = base_record(), base_record()
        b["cards"].extend(new_card(n) for n in range(13))
        cursor = compile_delta(a, b)["next_cursor"]
        b["sources"][0]["locator"] += " / changed"
        with self.assertRaisesRegex(ContractError, "stale_or_malformed_cursor"):
            compile_delta(a, b, cursor=cursor)

    def test_source_change_invalidates_only_dependent_nodes(self):
        a, b = base_record(), base_record()
        independent = new_card(50)
        # Existing source is referenced by existing cards; a second source
        # remains unchanged and is the only source for the independent card.
        second = copy.deepcopy(b["sources"][0])
        second["source_id"] = "SRC-independent"
        second["source_dependency_key"] = "independent-origin"
        second["locator"] = "Frozen separate reference"
        a["sources"].append(copy.deepcopy(second))
        b["sources"].append(second)
        independent["evidence_ids"] = ["SRC-independent"]
        a["cards"].append(copy.deepcopy(independent))
        b["cards"].append(independent)
        b["sources"][0]["locator"] = "Materially changed source anchor"
        outcome = compile_delta(a, b)
        self.assertIn("SRC-OPENAI-JD", outcome["source_metadata_changed"])
        self.assertIn("REQ-api-sdk", outcome["affected_nodes"])
        self.assertIn(a["cards"][0]["stable_id"], outcome["affected_nodes"])
        self.assertNotIn("C-fixture-50", outcome["affected_nodes"])
        self.assertFalse(outcome["source_integrity_proven"])
        self.assertEqual(outcome["status"], "BLOCKED")
        self.assertIn("original_source_owner_readback_required", outcome["remaining_work"])

    def test_two_attributions_from_one_origin_are_one_group(self):
        before, after = base_record(), base_record()
        duplicate = copy.deepcopy(after["sources"][0])
        duplicate["source_id"] = "SRC-SECOND-ATTRIBUTION"
        duplicate["locator"] = "A different paragraph from the same article"
        after["sources"].append(duplicate)
        result = compile_delta(before, after)
        self.assertEqual(len(result["origin_groups"]), 1)
        self.assertEqual(result["origin_groups"][0]["source_ids"],
                         ["SRC-OPENAI-JD", "SRC-SECOND-ATTRIBUTION"])
        self.assertFalse(result["source_independence_proven"])
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("original_source_owner_readback_required", result["remaining_work"])

    def test_noncard_record_change_never_false_done(self):
        a, b = base_record(), base_record()
        b["progress"]["knowledge"]["state"] = "SPECIFIED"
        result = compile_delta(a, b)
        self.assertEqual(result["patch"], [])
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("noncard_change_requires_reconciliation", result["remaining_work"])

    def test_batch_limit_or_forged_offset_refused(self):
        a, b = base_record(), base_record()
        b["cards"].extend(new_card(n) for n in range(13))
        with self.assertRaisesRegex(ContractError, "batch_size_out_of_range"):
            compile_delta(a, b, batch_size=13)
        cursor = compile_delta(a, b)["next_cursor"]
        with self.assertRaisesRegex(ContractError, "invalid_cursor_offset"):
            compile_delta(a, b, cursor=cursor.split(":")[0] + ":1")


if __name__ == "__main__":
    unittest.main()
