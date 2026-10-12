"""Static semantic-policy routing tests, not an LLM content-quality evaluation."""
import re
import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
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
            "C, C, G, SPEC",
            "SPEC-email-qa validated_by V-email-qa",
        ]:
            with self.subTest(bad=bad):
                self.assertIn(bad, d)
        for good in ["three search calls","returned by search in that request",
                     "actually inspected", "NOOP", "NOT_RUN"]:
            self.assertIn(good, d)

    def test_host_metadata_not_promoted_to_card_content(self):
        d = REF.read_text(encoding="utf-8")
        self.assertIn("HOST_OWNED_METADATA", d)

    def test_every_card_kind_has_explicit_scope_outer_and_inner_skill_consumers(self):
        document = REF.read_text(encoding="utf-8")
        section = document.split("## 7. Per-series consumers", 1)[1].split("## 8. Universal", 1)[0]
        card_rows = [line for line in section.splitlines() if line.startswith("| **") and line.count("|") >= 6]
        expected = {"N", "C", "D", "T", "E", "Q", "S", "R", "REQ", "SPEC", "G", "P", "V", "X", "K"}
        observed = {}
        for row in card_rows:
            columns = [column.strip() for column in row.strip().strip("|").split("|")]
            label = columns[0].removeprefix("**").split()[0]
            self.assertEqual(len(columns), 5, f"Expected 5 semantic columns for {label}")
            for item in columns[1:]:
                self.assertGreater(len(item), 35, f"Missing meaningful mapping for {label}")
            self.assertNotIn(label, observed)
            observed[label] = columns
        self.assertEqual(set(observed), expected)
        self.assertIn("issue-atom", section)
        self.assertIn("poteto-mode", section)

    def test_modality_agnostic_coverage_and_review_writing(self):
        doc = REF.read_text(encoding="utf-8")
        for medium in [
            "Plain text", "PDF, slide deck", "Image, chart", "Video/audio",
            "Tables, CSV", "Code, Git diffs", "Logs, agent traces",
        ]:
            with self.subTest(medium=medium):
                self.assertIn(medium, doc)
        for condition in [
            "source-coverage ledger", "never its media format", "P-class instruction",
            "review-writing", "Actor / subject", "Condition first",
            "Acceptance, rejection and unknown", "NOOP",
        ]:
            self.assertIn(condition, doc)
        self.assertIn("many Scopes", doc)

    def test_original_test_and_hook_manager_contracts_are_explicit(self):
        source = read("docs/soodles-manager-consumption.md")
        for item in ("test-manager/SKILL.md", "hook_manager.py", "tests/test_hook_stop.py",
                     "needs_scope", "NO_NATIVE_HOOK_REQUIRED", "stop_hook_active",
                     "preserve", "native", "NOT_RUN"):
            self.assertIn(item.lower(), source.lower())
        self.assertNotIn("This FactoryWeaver Hook Manager executes", source)
        import card_semantic
        no_need = {"schema": "factoryweaver/manager-needs/v1",
                   "subject": "Only classify an existing Concept",
                   "test_need": None, "hook_need": None}
        result = card_semantic.project_managers(no_need)
        self.assertEqual(result["test_manager"]["status"], "NO_TEST_SELECTION_REQUESTED")
        self.assertEqual(result["hook_manager"]["status"], "NO_NATIVE_HOOK_REQUIRED")
        self.assertEqual(result["manager_actions_performed"], [])
        self.assertFalse(result["effect_authority"])

    def test_each_selected_card_has_a_real_prompt(self):
        import card_semantic
        for series in card_semantic.registry()["cards"]:
            with self.subTest(series=series):
                selected = card_semantic.select([series])
                path = ROOT / selected["prompts"][0]["prompt"]
                content = path.read_text(encoding="utf-8")
                for required in ("**Trigger:**", "**Required semantic slots", "**Scope contribution:**",
                                 "**Rejection/non-case:**", "**Review-writing:**", "**Output:**"):
                    self.assertIn(required, content)
        overall = read("references/zettelkasten-v7.2.md")
        self.assertIn("registry.json", overall)
        self.assertIn("SELECTED TYPES ONLY", overall)
        self.assertNotIn("先產生 D/V/X/K", overall)

if __name__ == "__main__": unittest.main()
