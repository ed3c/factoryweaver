"""HW1 source-to-card golden fixture: structural, NOT a live compiler Agent eval."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from card_delta import compile_delta
from factoryweaver import verify

CASES = ROOT / "docs/evals/cs329z-hw1"


class CS329ZHW1PilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.boot = json.loads((CASES / "boot.json").read_text(encoding="utf-8"))
        cls.drill = json.loads((CASES / "drill.json").read_text(encoding="utf-8"))

    def test_records_conform_to_unmodified_v1_schema(self):
        for item in [self.boot, self.drill]:
            verify(item)
            self.assertEqual(len(item["requirements"]), 13)
            self.assertFalse(item["action_requests"])
            self.assertEqual(item["progress"]["engineering"]["state"], "UNASSESSED")
            self.assertEqual(item["progress"]["delivery"]["state"], "NOT_STARTED")

    def test_fixed_four_boot_and_four_real_drill_patches(self):
        self.assertEqual(len(self.boot["cards"]), 4)
        output = compile_delta(self.boot, self.drill, batch_size=4)
        self.assertEqual(output["status"], "DONE")
        self.assertEqual(output["change_count"], 4)
        self.assertEqual(len(output["patch"]), 4)
        self.assertEqual(sorted(item["operation"] for item in output["patch"]),
                         ["CREATE", "CREATE", "UPDATE", "UPDATE"])
        self.assertIsNone(output["next_cursor"])
        self.assertFalse(output["effect_authority"])

    def test_source_trace_and_deterministic_homework_truth(self):
        docs = {s["source_id"]: s for s in self.drill["sources"]}
        self.assertIn("SRC-qa", docs)
        self.assertIn("SRC-bm25", docs)
        self.assertIn("SRC-paper", docs)
        self.assertIn("SRC-lecture", docs)
        body = "\n".join(c["payload"] for c in self.drill["cards"])
        self.assertIn("at most three search calls", body)
        self.assertIn("not conflate", body)
        self.assertIn("NOT_RUN", body)
        for card in self.drill["cards"]:
            for ref in card["evidence_ids"]:
                self.assertIn(ref, docs)
        self.assertNotIn("PINNED_SHA256", {s.get("integrity") for s in docs.values()})

    def test_drill_keeps_initial_identity_and_whole_task_coverage(self):
        old = {c["stable_id"]: c for c in self.boot["cards"]}
        new = {c["stable_id"]: c for c in self.drill["cards"]}
        self.assertEqual(set(old), set(old) & set(new))
        self.assertEqual({r["id"] for r in self.boot["requirements"]},
                         {r["id"] for r in self.drill["requirements"]})
        self.assertEqual(compile_delta(self.boot, self.boot, batch_size=4)["status"], "NOOP")

    def test_no_generated_runtime_evidence_or_unauthorized_admission(self):
        for record in (self.boot, self.drill):
            self.assertEqual(record["subject"]["consumer"], "UNBOUND")
            self.assertEqual(record["progress"]["delivery"]["state"], "NOT_STARTED")
            for src in record["sources"]:
                self.assertNotIn("sha256", src)
            for card in record["cards"]:
                self.assertNotIn("sha256", card)


if __name__ == "__main__":
    unittest.main()
