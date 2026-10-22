"""Source-level controls for v7.2 conditional migrate-class semantic parity.

These tests cannot certify model behavior, complete natural-language semantics,
fresh Soodles/Noodle Stage consumption, or Provider effect.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "docs/closed-loop-v72/project.json"
COVERAGE = ROOT / "docs/closed-loop-v72/coverage.json"


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


def observations_differ(before, after, fields):
    """Fixture-only comparator; cannot infer equivalence from arbitrary prose."""
    return {k: (before.get(k), after.get(k)) for k in fields
            if before.get(k) != after.get(k)}


class MigrationParityContractTests(unittest.TestCase):
    def test_source_contract_keeps_four_evidence_levels_separate(self):
        doc = read("references/zettelkasten-v7.2.md")
        for expected in (
            "SOURCE-TO-CONSUMER SEMANTIC PARITY",
            "Source Identity",
            "Contract/Behavior Parity",
            "Independent Semantic Correctness",
            "Native Consumer/Provider Acceptance",
            "REUSE/NOOP", "not", "original Owner",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, doc)
        self.assertIn("conditional", doc.lower())

    def test_conditional_methods_are_not_new_runtime_authority(self):
        system = read("references/zettelkasten-v7.2.md")
        entry = read("skills/factoryweaver/SKILL.md")
        profile = read("docs/soodles-scope-routing.md")
        for literal in ("AST", "universal"):
            self.assertIn(literal, system)
        self.assertIn("no new", entry.lower())
        self.assertIn("migrate-class", profile)
        self.assertIn("not proof it is installed", profile)
        self.assertIn("Noodle Poteto", profile)

    def test_planted_false_equivalence_even_with_same_happy_path(self):
        before = {
            "happy": "published",
            "unknown_write": "original_owner_readback_before_retry",
            "exception": "REFUSE",
            "ordered_effects": ["readback", "if_safe_retry"],
        }
        after = dict(before, unknown_write="retry_immediately")
        # The happy path is not a sufficient oracle for this source contract.
        self.assertEqual(before["happy"], after["happy"])
        self.assertEqual(observations_differ(before, after, ("happy",)), {})
        self.assertEqual(set(observations_differ(
            before, after, ("happy", "unknown_write", "exception",
                            "ordered_effects"))), {"unknown_write"})

    def test_planted_side_effect_and_exception_require_independent_parity(self):
        before = {"output": 42, "error": "REFUSED", "effects": ["readback"]}
        after = {"output": 42, "error": "ACCEPTED", "effects": ["publish"]}
        self.assertEqual(before["output"], after["output"])
        self.assertEqual(set(observations_differ(
            before, after, ("output", "error", "effects"))), {"error", "effects"})

    def test_intentional_owner_change_must_not_be_reported_as_old_parity(self):
        before = {"behavior": "readback_required"}
        after = {"behavior": "owner_approved_new_behavior"}
        self.assertTrue(observations_differ(before, after, ("behavior",)))
        # A distinct, separately reviewed new requirement may justify this
        # change: the old parity verdict must not be silently rewritten.
        doc = read("docs/evals/v72-migrate-semantic-parity.md")
        self.assertIn("new", doc.lower())
        self.assertIn("P04 / false inequality", doc)

    def test_mgp_source_mapping_preserves_existing_requirements_and_cards(self):
        project = json.loads(PROJECT.read_text(encoding="utf-8"))
        cov = json.loads(COVERAGE.read_text(encoding="utf-8"))
        self.assertEqual(len(project["requirements"]), 30)
        self.assertEqual(len(project["cards"]), 68)
        self.assertEqual(len({r["id"] for r in project["requirements"]}), 30)
        self.assertEqual(len({c["stable_id"] for c in project["cards"]}), 68)
        clauses = {c["id"]: c for c in cov["clauses"]}
        self.assertTrue({"CL-20", "CL-21"} <= clauses.keys())
        reqs = {r["id"] for r in project["requirements"]}
        for clause in (clauses["CL-20"], clauses["CL-21"]):
            self.assertTrue(clause["requirements"])
            self.assertLessEqual(set(clause["requirements"]), reqs)
        self.assertFalse(cov["source_exhaustiveness_proven"])
        self.assertFalse(cov["semantic_mapping_verified"])
        self.assertFalse(cov["runtime_verified"])
        for id_ in ("SPEC-outer-loop", "SPEC-inner-loop",
                    "SPEC-stable-update", "V-runtime-gap"):
            card = next(c for c in project["cards"] if c["stable_id"] == id_)
            self.assertEqual(card["revision"], 3)
            self.assertIn("SRC-2026-MGP-DECISIONS", card["evidence_ids"])

    def test_native_evals_must_not_be_inferred_from_source_only_ci(self):
        doc = read("docs/evals/v72-migrate-semantic-parity.md")
        self.assertIn("NOT_RUN", doc)
        self.assertIn("independent Observer", doc)
        self.assertIn("original Host", doc)
        self.assertIn("false equality", doc)
        self.assertIn("Source Identity", doc)
        self.assertIn("Behavior Parity", doc)


if __name__ == "__main__":
    unittest.main()
