"""Static semantic-policy routing tests, not an LLM content-quality evaluation."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references/card-classification-and-scope-assembly.md"

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

class CardClassificationContractTests(unittest.TestCase):
    def test_original_fifteen_card_families_in_five_groups(self):
        doc = REF.read_text(encoding="utf-8")
        expected = {
            "Knowledge": {"N","C","D","T","E"},
            "Decision": {"Q","S","R"},
            "Specification": {"REQ","SPEC","G"},
            "Implementation": {"P"},
            "Verification": {"V","X","K"},
        }
        actual = {group:set() for group in expected}
        for line in doc.splitlines():
            m = re.match(r"^\| (Knowledge|Decision|Specification|Implementation|Verification) \|.*?`([A-Z]+)`", line)
                         flags=re.I)
            if m:
                actual[m.group(1)].add(m.group(2))
        self.assertEqual(actual, expected)
        self.assertEqual(sum(map(len, actual.values())), 15)
        for kind in ("C","REQ","G","SPEC","V","X","K"):
            self.assertIn("`"+kind+"`", doc)

    def test_single_skill_entry_and_compile_verify_load_taxonomy(self):
        for path in [
            "skills/factoryweaver/SKILL.md",
            "skills/factoryweaver-compile/SKILL.md",
            "skills/factoryweaver-verify/SKILL.md",
            "references/zettelkasten-v7.2.md",
            "docs/soodles-scope-routing.md",
        ]:
            with self.subTest(path=path):
                self.assertIn("card-classification-and-scope-assembly.md", read(path))
        self.assertTrue(REF.is_file())

    def test_runtime_contracts_are_not_card_families(self):
        d = REF.read_text(encoding="utf-8")
        for name in ["ScopeManifest","SkillRoute","PromptDelta","Continuation"]:
            self.assertIn(name, d)
        self.assertIn("never new `series`", d)

    def test_bad_course_examples_are_identified_and_good_case_is_concrete(self):
        d = REF.read_text(encoding="utf-8")
        for bad in [
            "Thanksgiving Recess",
            "Concept: Tool schema and validation",
            "C,C,G,SPEC",
            "SPEC-email-qa validated_by V-email-qa",
        ]:
            with self.subTest(bad=bad):
                self.assertIn(bad, d)
        for good in ["three search calls","returned by search in that request",
                     "actually inspected", "NOOP", "NOT_RUN"]:
            self.assertIn(good, d) if good != "actual inspected" else None

    def test_host_metadata_not_promoted_to_card_content(self):
        d = REF.read_text(encoding="utf-8")
        self.assertIn("HOST_OWNED_METADATA", d)

if __name__ == "__main__": unittest.main()
