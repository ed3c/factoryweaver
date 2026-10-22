"""Focused migration-parity controls for the existing FactoryWeaver semantic producer.

These are source-only differential fixtures. They explicitly do NOT establish
full natural-language semantic equivalence or fresh Noodle/native Agent use.
"""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import card_semantic  # the existing semantic shape/coverage preflight
import factoryweaver  # original machine contract; only structure, not source truth

PROMPT = ROOT / "references/zettelkasten-v7.2.md"
PROFILE = ROOT / "docs/soodles-scope-routing.md"

# A matched, synthetic bounded consumer contract. Independent of the text of
# the v7.2 prompt, and intentionally narrow: do not infer universal meaning.
ORIGINAL = {
    "source_clauses": {
        "SRC-1": "Agent may read the selected issue",
        "SRC-2": "Agent must not read restricted secret",
        "SRC-3": "Denied access must leave state unchanged",
    },
    "consumer": "Gitea-issue-to-secret-API synthetic fixture",
    "allowed": ("issue_read",),
    "denied": ("restricted_secret_read",),
    "denied_effects": (),
    "exception": "AccessDenied",
    "event_order": ("issue_read", "policy_denied"),
    "parent_obligations": ("legal_issue_completion", "deny_restricted_secret"),
    "claim_level": "L2_SYNTHETIC",
}


def snapshot_parity(before, candidate, normalized=()):
    """Independent *fixture* oracle: compare bounded observable contract.

    Normalization is opt-in and restricted to enumerated fields; no caller may
    erase forbidden effects, parent obligations, source clauses or authority.
    """
    never_normalize = {
        "source_clauses", "consumer", "denied", "denied_effects",
        "exception", "event_order", "parent_obligations", "claim_level",
    }
    if set(normalized) & never_normalize:
        raise ValueError("unsafe_normalization")
    return {
        field: (before.get(field), candidate.get(field))
        for field in before.keys() | candidate.keys()
        if field not in normalized and before.get(field) != candidate.get(field)
    }


def structured_spec(forbidden):
    registry = card_semantic.registry()
    required = registry["cards"]["SPEC"]["required_semantics"]
    # All required semantics present; form validity deliberately cannot
    # distinguish a missing security constraint from a correct constraint.
    semantics = {
        key: "Independent source-backed " + key +
        " has an observable consumer result and a named failure."
        for key in required
    }
    semantics["forbidden"] = forbidden
    return {
        "schema": "factoryweaver/card-semantic-proposal/v1",
        "cards": [{
            "series": "SPEC",
            "title": "Gitea Issue Access Boundary",
            "source_status": "INSPECTED",
            "evidence_topics": [
                "Original synthetic user goal and explicit denied secret read"
            ],
            "semantics": semantics,
            "links": [],
        }],
        "coverage": [{
            "source_unit": "synthetic denied secret source",
            "status": "MAPPED",
            "disposition": "Gitea Issue Access Boundary",
        }],
    }


class MigrateSemanticParityTests(unittest.TestCase):
    def test_portable_compiler_keeps_conditional_four_level_parity(self):
        p = PROMPT.read_text(encoding="utf-8")
        s = PROFILE.read_text(encoding="utf-8")
        for term in (
            "Reuse", "Matched", "Source Identity", "Consumer-observable",
            "Independent Semantic Correctness", "Native Consumer/Provider",
            "NOT_RUN", "original Owner", "PromptDelta=NOOP",
        ):
            with self.subTest(term=term):
                self.assertIn(term.lower(), p.lower())
        self.assertIn("Conditional migrate-class", s)
        self.assertIn("not an executor", s.lower())
        self.assertIn("not", s.lower())

    def test_valid_shape_must_not_be_accepted_as_semantic_parity(self):
        good = structured_spec("Never read the restricted synthetic secret")
        wrong = structured_spec("Read the restricted synthetic secret")
        for draft in (good, wrong):
            result = card_semantic.inspect(draft)
            self.assertEqual(result["status"], "SHAPE_VALID_SEMANTICS_UNVERIFIED")
            self.assertEqual(result["independent_semantic_review"], "NOT_RUN")
        self.assertNotEqual(
            good["cards"][0]["semantics"]["forbidden"],
            wrong["cards"][0]["semantics"]["forbidden"],
            "A valid card shape must not erase changed denial semantics",
        )

    def test_matched_before_after_and_legitimate_neighbor(self):
        self.assertEqual(snapshot_parity(ORIGINAL, copy.deepcopy(ORIGINAL)), {})
        legal_neighbor = copy.deepcopy(ORIGINAL)
        legal_neighbor["allowed"] = ("issue_read", "issue_metadata_read")
        self.assertIn("allowed", snapshot_parity(ORIGINAL, legal_neighbor))

    def test_planted_false_equivalence_for_rejection_and_event_order(self):
        for key, changed in (
            ("denied", ()),
            ("denied_effects", ("secret_export",)),
            ("exception", "ValueError"),
            ("event_order", ("policy_denied", "issue_read")),
            ("parent_obligations", ("legal_issue_completion",)),
            ("claim_level", "L3_LIVE"),
        ):
            with self.subTest(key=key):
                candidate = copy.deepcopy(ORIGINAL)
                candidate[key] = changed
                self.assertIn(key, snapshot_parity(ORIGINAL, candidate))
        # The happy path remains unchanged: negative controls must still fail.
        self.assertEqual(ORIGINAL["allowed"], ("issue_read",))

    def test_source_clause_loss_and_wrong_source_are_not_equivalent(self):
        missing = copy.deepcopy(ORIGINAL)
        missing["source_clauses"].pop("SRC-2")
        self.assertIn("source_clauses", snapshot_parity(ORIGINAL, missing))
        forged = copy.deepcopy(ORIGINAL)
        forged["source_clauses"]["SRC-2"] = "Agent may export every secret"
        self.assertIn("source_clauses", snapshot_parity(ORIGINAL, forged))

    def test_original_v1_validator_rejects_document_locator_as_card_id(self):
        # Actual original FactoryWeaver machine validator is the only owner
        # for registered references; fixture correctness is not semantics.
        record = factoryweaver.load(ROOT / "docs/closed-loop-v72/project.json")
        factoryweaver.verify(record)
        wrong = copy.deepcopy(record)
        wrong["cards"][0]["typed_links"].append({
            "relation": "based_on", "target": "source-coverage.md",
        })
        with self.assertRaisesRegex(
            factoryweaver.ContractError, "unknown_typed_link"
        ):
            factoryweaver.verify(wrong)

    def test_disallowed_normalization_and_unobserved_native_status(self):
        for name in ("source_clauses", "denied", "event_order",
                     "parent_obligations", "claim_level"):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, "unsafe_normalization"):
                    snapshot_parity(ORIGINAL, ORIGINAL, (name,))
        # No native Noodle input, host/attempt receipt, or Provider result
        # enters this fixture. Do not infer them from a unittest PASS.
        native_consumer = "NOT_RUN"
        self.assertEqual(native_consumer, "NOT_RUN")


if __name__ == "__main__":
    unittest.main()
