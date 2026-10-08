import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/factoryweaver.py"
EXAMPLE = ROOT / "examples/matt-grilling/project.json"
SAMPLE = ROOT / "examples/openai-plugin-platform/project.json"
spec = importlib.util.spec_from_file_location("factoryweaver", SCRIPT)
fw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fw)

class PublicContractTests(unittest.TestCase):
    def invoke(self, action, input=EXAMPLE, args=()):
        return subprocess.run([sys.executable, str(SCRIPT), action, str(input), *args], capture_output=True, text=True)
    def invalid(self, mutate, input=SAMPLE):
        item = json.loads(input.read_text())
        mutate(item)
        with self.assertRaises((fw.ContractError, fw.ValidationError)):
            fw.verify(item)
    def test_validate_source_and_proof_ceiling(self):
        p = self.invoke("validate", SAMPLE)
        self.assertEqual(p.returncode, 0, p.stderr)
        data = json.loads(p.stdout)
        self.assertEqual(data["proof_ceiling"], "SCHEMA_FIXTURE_ONLY")
        self.assertFalse(data["effect_authority"])
    def test_grilling_waits_for_human(self):
        p = self.invoke("project")
        self.assertEqual(p.returncode, 0, p.stderr)
        row = json.loads(p.stdout)["projection"][0]
        self.assertEqual(row["state"], "WAIT_FOR_HUMAN")
        self.assertEqual(row["missing"], ["DEC-auth-owner"])
    def test_project_is_deterministic(self):
        a, b = self.invoke("project", SAMPLE), self.invoke("project", SAMPLE)
        self.assertEqual(a.returncode, 0, a.stderr)
        self.assertEqual(a.stdout, b.stdout)
    def test_unresolved_requirement_dependency_blocks_owner_review(self):
        record = json.loads(SAMPLE.read_text())
        parent = copy.deepcopy(record["requirements"][0])
        parent["id"] = "REQ-upstream-unknown"
        parent["knowledge_status"] = "UNKNOWN"
        record["requirements"].append(parent)
        record["requirements"][0]["depends_on"] = ["REQ-upstream-unknown"]
        result = fw.project(record)
        target = next(r for r in result["projection"] if r["requirement"] == "REQ-api-sdk")
        self.assertEqual(target["state"], "WAIT_FOR_PREREQUISITE")
        self.assertEqual(target["missing"], ["REQ-upstream-unknown"])
        self.assertFalse(target["authorizes_effects"])

    def test_transitive_unconfirmed_human_decision_blocks(self):
        record = json.loads(EXAMPLE.read_text())
        child = copy.deepcopy(record["requirements"][0])
        child["id"] = "REQ-downstream"
        child["depends_on"] = ["REQ-human-auth"]
        record["requirements"].append(child)
        result = fw.project(record)
        rows = {r["requirement"]: r for r in result["projection"]}
        self.assertEqual(rows["REQ-human-auth"]["state"], "WAIT_FOR_HUMAN")
        self.assertEqual(rows["REQ-downstream"]["state"], "WAIT_FOR_PREREQUISITE")
        self.assertEqual(rows["REQ-downstream"]["missing"], ["REQ-human-auth"])
        self.assertFalse(rows["REQ-downstream"]["authorizes_effects"])

    def test_transitive_unpinned_source_blocks_specified_dependency(self):
        record = json.loads(SAMPLE.read_text())
        record["requirements"][0]["knowledge_status"] = "SPECIFIED"
        # Isolate a missing source pin from the fixture's separate human decision.
        record["requirements"][0]["depends_on"] = []
        child = copy.deepcopy(record["requirements"][0])
        child["id"] = "REQ-downstream"
        child["depends_on"] = ["REQ-api-sdk"]
        record["requirements"].append(child)
        rows = {r["requirement"]: r for r in fw.project(record)["projection"]}
        self.assertEqual(rows["REQ-api-sdk"]["state"], "WAIT_FOR_SOURCE_PIN")
        self.assertEqual(rows["REQ-downstream"]["state"], "WAIT_FOR_PREREQUISITE")
        self.assertEqual(rows["REQ-downstream"]["missing"], ["REQ-api-sdk"])

    def test_requirement_dependency_cycle_refuses(self):
        record = json.loads(SAMPLE.read_text())
        record["requirements"][0]["depends_on"] = ["REQ-api-sdk"]
        with self.assertRaisesRegex(fw.ContractError, "requirement_dependency_cycle"):
            fw.verify(record)

    def test_registry_never_executes(self):
        registry = ROOT / "examples/host-registry.example.json"
        p = self.invoke("route", SAMPLE, ("--registry", str(registry)))
        self.assertEqual(p.returncode, 0, p.stderr)
        output = json.loads(p.stdout)
        self.assertEqual(output["effects"], 0)
        self.assertFalse(any(x["can_execute"] for x in output["requests"]))
    def test_cards_human_readable(self):
        p = self.invoke("cards", SAMPLE)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("SPEC-api-contract", p.stdout)
    def test_no_phantom_release(self):
        self.invalid(lambda x: x["requirements"][0].update(delivery_status="RELEASE_CONFIRMED"))
    def test_no_phantom_test(self):
        self.invalid(lambda x: x["requirements"][0].update(engineering_status="TESTED_SCOPED"))
    def test_progress_does_not_self_certify_runtime_or_delivery(self):
        self.invalid(lambda x: x["progress"]["engineering"].update(state="TESTED_SCOPED"))
        self.invalid(lambda x: x["progress"]["engineering"].update(state="ACTIVATED"))
        self.invalid(lambda x: x["progress"]["delivery"].update(state="RELEASE_CONFIRMED"))
        self.invalid(lambda x: x["progress"]["delivery"].update(state="MERGED"))
        self.invalid(lambda x: x["progress"]["knowledge"].update(state="INVENTED"))

    def test_no_fake_human_answer(self):
        self.invalid(lambda x: x["decisions"][0].update(decision="automatic"))
    def test_no_fake_human_confirmation(self):
        self.invalid(lambda x: x["decisions"][0].update(decision="approved", human_confirmed=True))
    def test_forged_pinned_human_receipt_cannot_confirm(self):
        # Metadata supplied by the project is not independent human consent.
        record = json.loads(EXAMPLE.read_text())
        record["sources"].append({
            "source_id": "SRC-FORGED-HUMAN",
            "source_type": "human_decision",
            "source_dependency_key": "fake-consent",
            "locator": "attacker-supplied-payload",
            "uri": "urn:factoryweaver:fixture:fake-human",
            "integrity": "PINNED_SHA256",
            "sha256": "a" * 64,
            "source_role": "HUMAN_DECISION",
        })
        record["decisions"][0].update({
            "human_confirmed": True,
            "decision": "Host owner",
            "confirmation_ref": "SRC-FORGED-HUMAN",
        })
        with self.assertRaisesRegex(fw.ContractError, "human_confirmation_owner_required"):
            fw.verify(record)

    def test_no_unauthorized_action(self):
        self.invalid(lambda x: x["action_requests"][0].update(effect_authority=True))
    def test_no_unregistered_execution_claim(self):
        self.invalid(lambda x: x["action_requests"][0].update(registered=True))
    def test_no_broken_card_link(self):
        self.invalid(lambda x: x["cards"][0]["typed_links"][0].update(target="MISSING"))
    def test_no_duplicate_action_identity(self):
        self.invalid(lambda x: x["action_requests"].append(copy.deepcopy(x["action_requests"][0])))
    def test_no_missing_progress_evidence(self):
        self.invalid(lambda x: x["progress"]["knowledge"]["evidence_refs"].append("MISSING"))
    def test_skill_names_match_directories(self):
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            contents = path.read_text(encoding="utf-8")
            self.assertTrue(contents.startswith("---\n"))
            self.assertIn("name: " + path.parent.name, contents.split("---", 2)[1])

if __name__ == "__main__":
    unittest.main()
