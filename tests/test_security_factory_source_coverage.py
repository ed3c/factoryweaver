"""Source-only regression for the Security Agent Factory conversation inventory.

The 33 decision requirements and 41 Markdown cards are still PROPOSALS.
This does not certify full unseen conversation bytes, source truth, native
FactoryWeaver/v1 preparation, Soodles admission or Security Runtime effects.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/security-agent-factory"

DECISIONS = tuple(
    [f"SEC-{n:02d}" for n in range(1, 17)] + ["SEC-10R", "SEC-13R"]
)
ORIGINAL_RESEARCH = (
    "ScopeSentry", "REA", "Strix", "PentAGI", "CyberStrikeAI",
    "ARTEX", "garak", "promptfoo", "Ghidra", "Hopper",
)
DEFENSIVE_REFERENCES = ("Asset", "patch", "Secret", "least privilege",
                        "audit", "OIDC", "API key")
UNAUTHORIZED_EXPANSIONS = (
    "Cloudflare results endpoint starts scan",
    "Blue self-merges after its own test",
    "L1 PASS reported live exploit",
)


def missing_required(text, items):
    return tuple(item for item in items if item.casefold() not in text.casefold())


class SecurityFactorySourceCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = (BASE / "source-coverage.md").read_text(encoding="utf-8")
        cls.inventory = (BASE / "source-inventory.md").read_text(encoding="utf-8")
        cls.cards = (BASE / "cards.md").read_text(encoding="utf-8")
        cls.scope = (BASE / "README.md").read_text(encoding="utf-8")
        cls.handoff = (BASE / "handoff.md").read_text(encoding="utf-8")

    def test_decision_ledger_is_not_misreported_as_full_source_parity(self):
        self.assertFalse(missing_required(self.ledger, DECISIONS))
        self.assertEqual(len(re.findall(r"^\| REQ-\d{3} \|", self.ledger, re.M)), 33)
        self.assertIn("decision ledger", self.ledger.lower())
        self.assertIn("source-inventory.md", self.ledger)
        self.assertIn("whole-conversation", self.scope.lower())

    def test_all_originally_named_reference_tools_are_retained(self):
        self.assertEqual(missing_required(self.inventory, ORIGINAL_RESEARCH), ())
        self.assertEqual(missing_required(self.inventory, DEFENSIVE_REFERENCES), ())
        for status in ("DEFERRED", "HISTORICAL SOURCE", "NOT MEASURED", "SELECTED"):
            with self.subTest(status=status):
                self.assertIn(status, self.inventory)

    def test_planted_missing_source_fails_independently_of_selected_scope(self):
        before = self.inventory
        # The selected first Behavior Scope may remain intact despite this loss.
        planted = before.replace("[ScopeSentry]", "[missing-origin]")
        planted = planted.replace("ScopeSentry or promptfoo", "one reference or promptfoo")
        self.assertNotEqual(before, planted)
        self.assertTrue(missing_required(planted, ("ScopeSentry",)))
        self.assertEqual(missing_required(before, ORIGINAL_RESEARCH), ())

    def test_no_fake_typed_link_to_document_locator(self):
        self.assertNotIn("based_on:source-coverage", self.cards)
        self.assertIn("document/evidence locator", self.cards)
        self.assertIn("Registry Card ID", self.cards)
        self.assertEqual(len(re.findall(r"^### (?:REQ|SPEC|C|G|V|K|X|S|R) ·",
                                         self.cards, re.M)), 41)

    def test_planted_false_security_equivalence_rejected(self):
        for explicit_negative in UNAUTHORIZED_EXPANSIONS:
            with self.subTest(case=explicit_negative):
                self.assertIn(explicit_negative, self.ledger)
                altered = self.ledger.replace(explicit_negative, "silently omitted")
                self.assertTrue(missing_required(altered, (explicit_negative,)))
        self.assertIn("FAIL_SEMANTIC_PARITY", self.inventory)
        self.assertIn("FAIL_EVIDENCE_CLAIM", self.inventory)
        self.assertIn("FAIL_AUTHORITY", self.inventory)

    def test_handoff_keeps_native_evidence_and_effect_ceiling_unverified(self):
        self.assertIn("source-inventory.md", self.handoff)
        for term in ("NOT_RUN", "effects=[]", "next=null", "OpenShell", "Podman",
                     "MacBook", "Cloudflare", "L3", "SEC-16"):
            with self.subTest(term=term):
                self.assertIn(term, self.handoff)
        self.assertIn("no remote dispatch", self.handoff.lower())


if __name__ == "__main__":
    unittest.main()
