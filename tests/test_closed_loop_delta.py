import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "docs/closed-loop-v72/project.json"
CLI = ROOT / "scripts/card_delta.py"
REQUIREMENTS = [
    "REQ-intent", "REQ-coverage", "REQ-dependencies", "REQ-spec-data",
    "REQ-stable-update", "REQ-correction", "REQ-identity", "REQ-events",
    "REQ-schema", "REQ-test", "REQ-hook", "REQ-cron", "REQ-inner-loop",
    "REQ-outer-loop", "REQ-manager-feedback", "REQ-consumption",
    "REQ-completion", "REQ-invalidation", "REQ-replay", "REQ-unknown-effect",
    "REQ-retry-budget", "REQ-thinking-router", "REQ-ponytail",
    "REQ-eval-evidence", "REQ-compiler-audit", "REQ-adapters", "REQ-safety",
    "REQ-handoff", "REQ-cost", "REQ-publication",
]
CARD_IDS = [key for req in REQUIREMENTS for key in ("CARD-" + req, "SPEC-" + req[4:])] + [
    "N-whole-task", "C-data-loop", "R-delivery-order", "T-architecture-choice",
    "V-runtime-gap", "X-no-managers", "K-native-bindings", "K-legacy-v71",
]
HOOK_DEPENDENTS = {
    "REQ-hook", "REQ-manager-feedback", "REQ-consumption", "REQ-completion",
    "REQ-eval-evidence", "REQ-cost",
}


def record():
    return json.loads(PROJECT.read_bytes())


def encode(value):
    return json.dumps(value, ensure_ascii=False).encode("utf-8")


def card(value, key):
    return next(c for c in value["cards"] if c["stable_id"] == key)


class ClosedLoopDeltaTests(unittest.TestCase):
    def invoke(self, before, after, *args):
        before_bytes = before if isinstance(before, bytes) else encode(before)
        after_bytes = after if isinstance(after, bytes) else encode(after)
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory) / "before.json", Path(directory) / "after.json"
            a.write_bytes(before_bytes)
            b.write_bytes(after_bytes)
            result = subprocess.run([sys.executable, str(CLI), str(a), str(b), *args],
                                    capture_output=True)
            self.assertEqual(a.read_bytes(), before_bytes)
            self.assertEqual(b.read_bytes(), after_bytes)
            return result

    def success(self, before, after, *args):
        result = self.invoke(before, after, *args)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(result.stderr, b"")
        output = json.loads(result.stdout)
        self.assertEqual(output["effects"], [])
        self.assertFalse(output["effect_authority"])
        self.assertFalse(output["authorizes_landing"])
        self.assertFalse(output["source_integrity_proven"])
        return output

    def refusal(self, before, after, error, *args):
        result = self.invoke(before, after, *args)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(result.stdout, b"")
        output = json.loads(result.stderr)
        self.assertFalse(output["valid"])
        self.assertIn(error, output["error"])

    def test_main_noop_retains_entire_denominator_and_statuses(self):
        frozen = PROJECT.read_bytes()
        original = json.loads(frozen)
        self.assertEqual([r["id"] for r in original["requirements"]], REQUIREMENTS)
        self.assertEqual([c["stable_id"] for c in original["cards"]], CARD_IDS)
        result = self.success(frozen, frozen)
        self.assertEqual(result["status"], "NOOP")
        self.assertEqual(result["patch"], [])
        self.assertEqual(result["card_order"], CARD_IDS)
        self.assertEqual(result["affected_records"], [])
        self.assertEqual(result["noncard_changes"], {})
        self.assertIsNone(result["next_cursor"])
        self.assertTrue(all(r["engineering_status"] == "UNASSESSED"
                            and r["delivery_status"] == "NOT_STARTED"
                            for r in original["requirements"]))
        self.assertEqual(PROJECT.read_bytes(), frozen)

    def test_all_68_updates_are_lossless_bounded_and_replay_identical(self):
        before, after = record(), record()
        for c in after["cards"]:
            c["payload"] += " 有限編譯控制，不表示 runtime 驗收。"
            c["revision"] += 1
        before_bytes, after_bytes = PROJECT.read_bytes(), encode(after)
        patches, cursor, sizes = [], None, []
        while True:
            args = ("--cursor", cursor) if cursor else ()
            execution = self.invoke(before_bytes, after_bytes, *args)
            replay = self.invoke(before_bytes, after_bytes, *args)
            self.assertEqual(execution.returncode, 0, execution.stderr)
            self.assertEqual(replay.returncode, 0, replay.stderr)
            self.assertEqual(execution.stdout, replay.stdout)
            output = json.loads(execution.stdout)
            self.assertEqual(output["change_count"], 68)
            self.assertEqual(output["noncard_changes"], {})
            self.assertEqual(output["effects"], [])
            self.assertFalse(output["authorizes_landing"])
            patches.extend(output["patch"])
            sizes.append(len(output["patch"]))
            cursor = output["next_cursor"]
            self.assertEqual(output["status"], "CONTINUE" if cursor else "DONE")
            if cursor is None:
                break
        self.assertEqual(sizes, [12, 12, 12, 12, 12, 8])
        self.assertEqual([p["card"]["stable_id"] for p in patches], CARD_IDS)
        self.assertEqual([p["previous_card"] for p in patches], before["cards"])
        self.assertTrue(all(p["operation"] == "UPDATE" and p["previous_revision"] == 1
                            and p["card"]["revision"] == 2 for p in patches))
        reconstructed = copy.deepcopy(before)
        reconstructed["cards"] = [p["card"] for p in patches]
        self.assertEqual(reconstructed, after)
        self.assertEqual(reconstructed["requirements"], before["requirements"])
        self.assertEqual(reconstructed["sources"], before["sources"])

    def test_cursor_rejects_other_bytes_batch_or_object_domain(self):
        before_bytes, after = PROJECT.read_bytes(), record()
        for c in after["cards"][:13]:
            c["payload"] += " Cursor binding control."
            c["revision"] += 1
        after_bytes = encode(after)
        cursor = self.success(before_bytes, after_bytes)["next_cursor"]
        for a, b, args in (
                (before_bytes + b"\n", after_bytes, ()),
                (before_bytes, after_bytes + b"\n", ()),
                (encode(record()), after_bytes, ()),
                (before_bytes, json.dumps(after, sort_keys=True).encode(), ()),
                (before_bytes, after_bytes, ("--batch-size", "6"))):
            with self.subTest(args=args, a_changed=a != before_bytes, b_changed=b != after_bytes):
                self.refusal(a, b, "stale_or_malformed_cursor", "--cursor", cursor, *args)
        sys.path.insert(0, str(ROOT / "scripts"))
        from card_delta import compile_delta
        object_cursor = compile_delta(record(), after)["next_cursor"]
        self.refusal(before_bytes, after_bytes, "stale_or_malformed_cursor",
                     "--cursor", object_cursor)
        for bad in (cursor.split(":")[0] + ":1", cursor.split(":")[0] + ":012"):
            self.refusal(before_bytes, after_bytes, "invalid_cursor_offset", "--cursor", bad)
        self.refusal(before_bytes, after_bytes, "batch_size_out_of_range", "--batch-size", "13")

    def test_requirement_changes_invalidate_only_actual_downstream(self):
        before, after = record(), record()
        req = next(r for r in after["requirements"] if r["id"] == "REQ-hook")
        req["acceptance"].append("新增有限契約控制，不升級原生效果。")
        output = self.success(before, after)
        affected = output["affected_records"]
        self.assertEqual({n["id"] for n in affected if n["kind"] == "requirement"}, HOOK_DEPENDENTS)
        self.assertIn({"kind": "card", "id": "CARD-REQ-consumption"}, affected)
        self.assertNotIn("REQ-test", output["affected_nodes"])
        self.assertNotIn("REQ-cron", output["affected_nodes"])
        self.assertEqual(output["noncard_changes"]["requirements"], {
            "before_present": True, "after_present": True,
            "before": before["requirements"], "after": after["requirements"],
        })
        self.assertEqual(output["status"], "BLOCKED")
        self.assertEqual(output["patch"], [])

    def test_main_shared_source_hits_all_30_and_preserves_source_history(self):
        before, after = record(), record()
        after["sources"][0]["locator"] += " / new public anchor"
        output = self.success(before, after)
        self.assertEqual({n["id"] for n in output["affected_records"]
                          if n["kind"] == "requirement"}, set(REQUIREMENTS))
        self.assertEqual({n["id"] for n in output["affected_records"]
                          if n["kind"] == "card"}, set(CARD_IDS))
        self.assertEqual(output["noncard_changes"]["sources"]["before"], before["sources"])
        self.assertEqual(output["noncard_changes"]["sources"]["after"], after["sources"])
        self.assertEqual(output["remaining_work"], ["original_source_owner_readback_required"])
        self.assertEqual(output["status"], "BLOCKED")

    def test_local_source_and_removed_edges_retain_before_dependencies(self):
        before = record()
        source = copy.deepcopy(before["sources"][0])
        source["source_id"] = "SRC-hook-local"
        source["source_dependency_key"] = "hook-local-origin"
        before["sources"].append(source)
        req = next(r for r in before["requirements"] if r["id"] == "REQ-hook")
        req["source_ids"] = ["SRC-hook-local"]
        card(before, "SPEC-hook")["evidence_ids"] = ["SRC-hook-local"]
        after = copy.deepcopy(before)
        after["sources"][-1]["locator"] += " / correction"
        next(r for r in after["requirements"] if r["id"] == "REQ-hook")["source_ids"] = ["SRC-V72"]
        card(after, "SPEC-hook")["evidence_ids"] = ["SRC-V72"]
        card(after, "SPEC-hook")["revision"] += 1
        output = self.success(before, after)
        self.assertEqual({n["id"] for n in output["affected_records"]
                          if n["kind"] == "requirement"}, HOOK_DEPENDENTS)
        self.assertNotIn("REQ-test", output["affected_nodes"])
        self.assertNotIn("SPEC-cron", output["affected_nodes"])
        self.assertEqual(output["patch"][0]["previous_card"], card(before, "SPEC-hook"))
        self.assertEqual(output["noncard_changes"]["sources"]["before"], before["sources"])

    def test_removed_dependency_still_invalidates_its_retained_consumers(self):
        before, after = record(), record()
        next(r for r in after["requirements"] if r["id"] == "REQ-hook")["statement"] += " New condition."
        next(r for r in after["requirements"] if r["id"] == "REQ-manager-feedback")["depends_on"].remove("REQ-hook")
        changed = card(after, "K-native-bindings")
        changed["typed_links"] = [e for e in changed["typed_links"] if e["target"] != "REQ-hook"]
        changed["revision"] += 1
        output = self.success(before, after)
        self.assertIn("REQ-consumption", output["affected_nodes"])
        self.assertIn("K-native-bindings", output["affected_nodes"])
        self.assertEqual(output["patch"][0]["previous_card"], card(before, "K-native-bindings"))

    def test_card_change_does_not_backflow_or_follow_comparison_relations(self):
        before = record()
        observer = card(before, "C-data-loop")
        observer["typed_links"] = [
            {"relation": relation, "target": "SPEC-hook"}
            for relation in ("leads_to", "causes", "enables", "contradicts", "competes_with",
                             "analogous_to", "instance_of", "mitigates")
        ]
        after = copy.deepcopy(before)
        card(after, "SPEC-hook")["payload"] += " Scoped specification correction."
        card(after, "SPEC-hook")["revision"] += 1
        output = self.success(before, after)
        self.assertEqual(output["affected_records"], [
            {"kind": "card", "id": "CARD-REQ-hook"},
            {"kind": "card", "id": "SPEC-hook"},
        ])
        self.assertEqual(output["status"], "DONE")

    def test_cross_kind_id_collision_does_not_invent_source_dependency(self):
        before = record()
        collision = copy.deepcopy(card(before, "C-data-loop"))
        collision["stable_id"] = "SRC-TASK"
        collision["canonical_key"] = "C|collision|defines|identity|portable|v1"
        collision["evidence_ids"] = ["SRC-V72"]
        collision["typed_links"] = []
        before["cards"].append(collision)
        observer = card(before, "C-data-loop")
        observer["evidence_ids"] = ["SRC-V72"]
        observer["typed_links"] = [{"relation": "depends_on", "target": "SRC-TASK"}]
        after = copy.deepcopy(before)
        after["sources"][0]["locator"] += " Changed source, not same-named card."
        output = self.success(before, after)
        self.assertIn({"kind": "source", "id": "SRC-TASK"}, output["affected_records"])
        self.assertNotIn({"kind": "card", "id": "SRC-TASK"}, output["affected_records"])
        self.assertNotIn({"kind": "card", "id": "C-data-loop"}, output["affected_records"])

    def test_requirement_card_collision_preserves_both_target_contributors(self):
        before = record()
        collision = copy.deepcopy(card(before, "C-data-loop"))
        collision["stable_id"] = "REQ-hook"
        collision["canonical_key"] = "C|collision|defines|requirement|portable|v1"
        collision["typed_links"] = []
        before["cards"].append(collision)
        after = copy.deepcopy(before)
        card(after, "REQ-hook")["payload"] += " Only the same-named card changed."
        card(after, "REQ-hook")["revision"] += 1
        output = self.success(before, after)
        self.assertIn({"kind": "card", "id": "REQ-hook"}, output["affected_records"])
        self.assertNotIn({"kind": "requirement", "id": "REQ-hook"}, output["affected_records"])
        self.assertIn({"kind": "requirement", "id": "REQ-manager-feedback"}, output["affected_records"])
        self.assertIn({"kind": "card", "id": "SPEC-hook"}, output["affected_records"])

    def test_source_dependency_through_decision_and_requirement_is_preserved(self):
        before = record()
        source = copy.deepcopy(before["sources"][0])
        source["source_id"] = "SRC-decision-local"
        source["source_dependency_key"] = "decision-local-origin"
        before["sources"].append(source)
        before["decisions"] = [{
            "id": "DEC-hook-scope", "question": "What scope is authorized?",
            "human_confirmed": False, "decision": None,
            "source_ids": ["SRC-decision-local"],
        }]
        next(r for r in before["requirements"] if r["id"] == "REQ-hook")["depends_on"].append("DEC-hook-scope")
        after = copy.deepcopy(before)
        after["sources"][-1]["locator"] += " Public correction."
        output = self.success(before, after)
        self.assertIn({"kind": "decision", "id": "DEC-hook-scope"}, output["affected_records"])
        self.assertEqual({n["id"] for n in output["affected_records"]
                          if n["kind"] == "requirement"}, HOOK_DEPENDENTS)
        self.assertNotIn("REQ-test", output["affected_nodes"])
        after = copy.deepcopy(before)
        after["decisions"][0]["question"] += " Clarify the prerequisite."
        result = self.success(before, after)
        self.assertIn("REQ-consumption", result["affected_nodes"])
        self.assertEqual(result["noncard_changes"]["decisions"]["before"], before["decisions"])

    def test_all_noncard_sections_and_optional_presence_are_lossless(self):
        before, after = record(), record()
        after["decisions"] = []
        after["sources"][0]["locator"] += " Public correction."
        after["requirements"][0]["falsifier"] += " Explicit additional condition."
        after["action_requests"][0]["expect"]["scope"] = "bounded knowledge only"
        after["progress"]["knowledge"]["evidence_refs"] = ["SRC-TASK"]
        changed = card(after, "CARD-REQ-intent")
        changed["payload"] += " Additional context."
        changed["revision"] += 1
        output = self.success(before, after)
        self.assertEqual(set(output["noncard_changes"]), {
            "sources", "decisions", "requirements", "action_requests", "progress",
        })
        reconstructed = copy.deepcopy(before)
        for name, delta in output["noncard_changes"].items():
            self.assertEqual(delta["before_present"], name in before)
            self.assertEqual(delta["before"], before.get(name))
            if delta["after_present"]:
                reconstructed[name] = delta["after"]
            else:
                reconstructed.pop(name)
        reconstructed["cards"][0] = output["patch"][0]["card"]
        self.assertEqual(reconstructed, after)
        self.assertEqual(output["status"], "BLOCKED")
        reverse = self.success(after, {k: v for k, v in after.items() if k != "decisions"})
        self.assertEqual(reverse["noncard_changes"]["decisions"], {
            "before_present": True, "after_present": False, "before": [], "after": None,
        })

    def test_history_identity_revision_and_schema_refusals_are_structured(self):
        before = record()
        for section, error in (("sources", "source_history_removed"),
                               ("requirements", "requirement_history_removed"),
                               ("cards", "card_history_removed")):
            a, b = copy.deepcopy(before), copy.deepcopy(before)
            if section == "sources":
                extra = copy.deepcopy(a["sources"][0])
                extra["source_id"] = "SRC-unreferenced"
                a["sources"].append(extra)
            elif section == "requirements":
                b["requirements"] = [r for r in b["requirements"] if r["id"] != "REQ-publication"]
                for c in b["cards"]:
                    c["typed_links"] = [e for e in c["typed_links"] if e["target"] != "REQ-publication"]
                    if c["typed_links"] != card(a, c["stable_id"])["typed_links"]:
                        c["revision"] += 1
            else:
                b["cards"] = [c for c in b["cards"] if c["stable_id"] != "N-whole-task"]
            self.refusal(a, b, error)
        for field, value, error in (
                ("stable_id", "CARD-illegal-replacement", "stable_id_changed"),
                ("revision", 2, "spurious_revision"),
                ("payload", "Material change without revision", "revision_not_incremented"),
                ("revision", 0, "minimum")):
            after = copy.deepcopy(before)
            card(after, "N-whole-task")[field] = value
            self.refusal(before, after, error)
        self.refusal(PROJECT.read_bytes(), b'{"cards":[],"cards":[]}', "duplicate_json_key:cards")
        after = copy.deepcopy(before)
        after["requirements"][0]["engineering_status"] = "TESTED_SCOPED"
        self.refusal(before, after, "untrusted_test_claim")


if __name__ == "__main__":
    unittest.main()
