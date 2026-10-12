"""Static entry-skill contract and existing read-only 4-card delta pagination.

These tests do NOT claim Agent Skill invocation, source semantics, P-class
behavior, native owner consumption, or actual Soodles admission.
"""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from card_delta import compile_delta


class FactoryWeaverEntrySkillTests(unittest.TestCase):
    def read(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_one_entry_references_real_authoritative_prompt_and_profiles(self):
        entry = ROOT / "skills/factoryweaver/SKILL.md"
        text = entry.read_text(encoding="utf-8")
        for ref in (
            "../../references/zettelkasten-v7.2.md",
            "../../docs/compatibility.md",
            "../../docs/soodles-scope-routing.md",
            "../factoryweaver-compile/SKILL.md",
            "../factoryweaver-verify/SKILL.md",
        ):
            with self.subTest(ref=ref):
                self.assertTrue((entry.parent / ref).is_file())
                self.assertIn(ref, text)
        self.assertIn("name: factoryweaver", text)
        self.assertIn("before compiling", text)

    def test_entry_is_a_router_not_an_effect_owner(self):
        content = self.read("skills/factoryweaver/SKILL.md")
        self.assertIn("New requirement / no accepted inventory", content)
        self.assertIn("Previously accepted inventory", content)
        self.assertIn("factoryweaver-verify", content)
        self.assertIn("Original authorized Host", content)
        self.assertIn("no computed digests", content)
        self.assertIn("Noodle Poteto Inner Loop", content)
        self.assertIn("no extra", self.read("docs/soodles-scope-routing.md").lower())

    def test_soodles_profile_keeps_batching_and_goal_boundary(self):
        entry = self.read("skills/factoryweaver/SKILL.md")
        ref = self.read("references/zettelkasten-v7.2.md")
        profile = self.read("docs/soodles-scope-routing.md")
        self.assertIn("## SOODLES PROFILE", ref)
        self.assertIn("MAX_CARDS_PER_BATCH: 12", ref)
        self.assertIn("SOODLES_BATCH_RENDER_SLOTS: 4", ref)
        self.assertIn("four-slot", entry.lower())
        self.assertIn("Measurement / Persistence / Stop-Escalation", entry)
        self.assertIn("Issue Atom", profile)
        self.assertIn("p95 CI duration below 10 minutes", profile)
        self.assertIn("**not** evidence of an installed live Evals capability", profile)

    def test_documentation_points_to_one_entry(self):
        self.assertIn("skills/factoryweaver/SKILL.md", self.read("README.md"))
        self.assertIn("skills/factoryweaver/SKILL.md", self.read("AGENTS.md"))
        self.assertIn("references/zettelkasten-v7.2.md",
                      self.read("skills/factoryweaver-compile/SKILL.md"))

    def test_handoff_diagnosis_is_read_only_and_original_owner_selected(self):
        entry = self.read("skills/factoryweaver/SKILL.md")
        agents = self.read("AGENTS.md")
        contract = self.read("docs/factoryweaver-soodles-readback.md")
        for source in (entry, agents, contract):
            self.assertIn("boundary_findings", source)
            self.assertIn("original", source.lower())
            self.assertIn("Poteto", source)
        self.assertIn("NOT_OBSERVED", contract)
        self.assertIn("UNVERIFIED", contract)
        self.assertIn("no Card automatically", contract)
        self.assertIn("Host-selected", entry)
        self.assertIn("next=null", agents)

    def test_four_changed_cards_per_frozen_cli_page(self):
        project = json.loads(
            self.read("examples/openai-plugin-platform/project.json")
        )
        updated = copy.deepcopy(project)
        for n in range(9):
            updated["cards"].append({
                "stable_id": f"C-entry-fixture-{n}",
                "canonical_key": f"C|entry-fixture-{n}|demonstrates|case|portable|v1",
                "series": "C", "revision": 1, "status": "ACTIVE",
                "title": f"Independent entry fixture {n}",
                "payload": f"A distinct input case to test four-card pages, number {n}.",
                "evidence_ids": [project["sources"][0]["source_id"]],
                "typed_links": [],
            })
        statuses, lengths = [], []
        cursor = None
        while True:
            result = compile_delta(project, updated, batch_size=4, cursor=cursor)
            statuses.append(result["status"])
            lengths.append(len(result["patch"]))
            cursor = result["next_cursor"]
            if cursor is None:
                break
        self.assertEqual(lengths, [4, 4, 1])
        self.assertEqual(statuses, ["CONTINUE", "CONTINUE", "DONE"])
        self.assertEqual(compile_delta(project, project, batch_size=4)["status"],
                         "NOOP")


if __name__ == "__main__":
    unittest.main()
