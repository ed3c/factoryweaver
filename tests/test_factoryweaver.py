import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
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

    def test_target_known_fields_refuse_invalid_types(self):
        for field in ("requirement_id", "kind"):
            for value in ([], {}, None, True, 0):
                with self.subTest(field=field, value=value):
                    record, registry = self.pinned_route_fixture()
                    record["action_requests"][0]["target"][field] = value
                    result = self.invoke_raw("route", json.dumps(record), json.dumps(registry))
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertEqual(result.stdout, "")
                    refusal = json.loads(result.stderr)
                    self.assertFalse(refusal["valid"])
                    self.assertIn(field, refusal["error"])

    def test_explicit_invalid_registry_is_not_absent(self):
        record, _ = self.pinned_route_fixture()
        for registry in ({}, [], None, "", 0, False):
            with self.subTest(registry=registry):
                result = self.invoke_raw("route", json.dumps(record), json.dumps(registry))
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertFalse(json.loads(result.stderr)["valid"])

    def test_library_registry_omission_and_null_are_distinct(self):
        record, _ = self.pinned_route_fixture()
        self.assertEqual(fw.route(record)["requests"][0]["route"], "HOST_REGISTRY_REQUIRED")
        with self.assertRaises(fw.ValidationError):
            fw.route(record, None)

    def test_empty_target_strings_keep_existing_advisory_results(self):
        expected = {"kind": "REGISTRY_SCOPE_MISMATCH", "requirement_id": "REQUIREMENT_BINDING_REQUIRED"}
        for field, state in expected.items():
            with self.subTest(field=field):
                record, registry = self.pinned_route_fixture()
                record["action_requests"][0]["target"][field] = ""
                result = self.invoke_raw("route", json.dumps(record), json.dumps(registry))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["requests"][0]["route"], state)

    def invoke_raw(self, action, record_text, registry_text=None):
        with tempfile.TemporaryDirectory() as directory:
            record_path = Path(directory) / "record.json"
            record_path.write_text(record_text, encoding="utf-8")
            args = ()
            if registry_text is not None:
                registry_path = Path(directory) / "registry.json"
                registry_path.write_text(registry_text, encoding="utf-8")
                args = ("--registry", str(registry_path))
            return self.invoke(action, record_path, args)

    def assert_duplicate_refused(self, action, record_text, key, registry_text=None):
        result = self.invoke_raw(action, record_text, registry_text)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "")
        refusal = json.loads(result.stderr)
        self.assertFalse(refusal["valid"])
        self.assertEqual(refusal["error"], "duplicate_json_key:" + key)

    def test_duplicate_requirement_dependency_fields_refuse(self):
        record = json.loads(EXAMPLE.read_text())
        selected = json.dumps(record)
        token = '"depends_on": ' + json.dumps(record["requirements"][0]["depends_on"])
        for key, value in (("depends_on", []),
                           ("depends_on", ["DEC-auth-owner"]),
                           (r"depends\u005fon", [])):
            with self.subTest(key=key, value=value):
                text = selected.replace(token, token + ', "' + key + '": '
                                        + json.dumps(value), 1)
                self.assert_duplicate_refused("project", text, "depends_on")

    def test_duplicate_top_level_requirement_arrays_refuse(self):
        record = json.loads(EXAMPLE.read_text())
        changed = copy.deepcopy(record["requirements"])
        changed[0]["depends_on"] = []
        selected = json.dumps(record)
        token = '"requirements": ' + json.dumps(record["requirements"])
        for key, value in (("requirements", changed),
                           ("requirements", record["requirements"]),
                           (r"requirem\u0065nts", changed)):
            with self.subTest(key=key, value=value):
                text = selected.replace(token, token + ', "' + key + '": '
                                        + json.dumps(value), 1)
                self.assert_duplicate_refused("project", text, "requirements")

    def test_duplicate_registry_enabled_fields_refuse(self):
        record, registry = self.pinned_route_fixture()
        registry["operations"][0]["enabled"] = False
        selected = json.dumps(registry)
        token = '"enabled": false'
        for key, value in (("enabled", True), ("enabled", False),
                           (r"enabl\u0065d", True)):
            with self.subTest(key=key, value=value):
                text = selected.replace(token, token + ', "' + key + '": '
                                        + json.dumps(value), 1)
                self.assert_duplicate_refused("route", json.dumps(record), "enabled", text)

    def test_duplicate_top_level_registry_operations_refuse(self):
        record, registry = self.pinned_route_fixture()
        registry["operations"][0]["enabled"] = False
        changed = copy.deepcopy(registry["operations"])
        changed[0]["enabled"] = True
        selected = json.dumps(registry)
        token = '"operations": ' + json.dumps(registry["operations"])
        for key, value in (("operations", changed),
                           ("operations", registry["operations"]),
                           (r"operat\u0069ons", changed)):
            with self.subTest(key=key, value=value):
                text = selected.replace(token, token + ', "' + key + '": '
                                        + json.dumps(value), 1)
                self.assert_duplicate_refused("route", json.dumps(record), "operations", text)

    def test_dependency_keys_in_distinct_objects_and_strings_remain_valid(self):
        record = json.loads(EXAMPLE.read_text())
        child = copy.deepcopy(record["requirements"][0])
        child["id"] = "REQ-second-human"
        child["statement"] = 'Literal "depends_on": [] text is not a JSON field.'
        record["requirements"].append(child)
        result = self.invoke_raw("project", json.dumps(record))
        self.assertEqual(result.returncode, 0, result.stderr)
        projection = json.loads(result.stdout)
        self.assertEqual(len(projection["projection"]), 2)
        for row in projection["projection"]:
            self.assertEqual((row["state"], row["missing"]),
                             ("WAIT_FOR_HUMAN", ["DEC-auth-owner"]))
            self.assertFalse(row["authorizes_effects"])
        self.assertEqual(projection["completion"], "COMPILED_ONLY")

    def test_registry_keys_in_distinct_objects_and_strings_remain_valid(self):
        record, registry = self.pinned_route_fixture()
        other = copy.deepcopy(registry["operations"][0])
        other["operation_id"] = "schema.inspect"
        other["owner"] = 'Literal "enabled": false text is not a JSON field.'
        registry["operations"].append(other)
        result = self.invoke_raw("route", json.dumps(record), json.dumps(registry))
        self.assertEqual(result.returncode, 0, result.stderr)
        routed = json.loads(result.stdout)
        self.assertEqual(routed["requests"][0]["route"], "REGISTERED_CANDIDATE_ONLY")
        self.assertFalse(routed["requests"][0]["can_execute"])
        self.assertEqual((routed["effects"], routed["authority"]), (0, "NONE"))

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
    def test_spec_validation_route_cannot_skip_human_frontier(self):
        record = json.loads(EXAMPLE.read_text())
        request = {
            "request_id": "AR-validation",
            "operation_id": "schema.validate",
            "target": {"kind": "requirement", "requirement_id": "REQ-human-auth"},
            "intent": "validate_specification",
            "mode": "READ_ONLY",
            "registered": False,
            "effect_authority": False,
            "status": "PROPOSED",
            "requires": [],
            "expect": {"result": "schema"},
            "observed": None,
        }
        record["action_requests"].append(request)
        registry = {"protocol": "factoryweaver/registry-v1", "operations": [{
            "operation_id": "schema.validate", "owner": "example-checker",
            "allowed_modes": ["READ_ONLY"], "target_kinds": ["requirement"],
            "enabled": True,
        }]}
        row = fw.route(record, registry)["requests"][0]
        self.assertEqual((row["route"], row["requirement_state"]),
                         ("REQUIREMENT_BLOCKED", "WAIT_FOR_HUMAN"))
        self.assertFalse(row["can_execute"])
        del request["target"]["requirement_id"]
        self.assertEqual(fw.route(record, registry)["requests"][0]["route"],
                         "REQUIREMENT_BINDING_REQUIRED")
        request["target"]["requirement_id"] = "REQ-not-found"
        self.assertEqual(fw.route(record, registry)["requests"][0]["route"],
                         "UNKNOWN_REQUIREMENT")

    def test_spec_validation_candidate_still_has_no_effect_authority(self):
        record = json.loads(SAMPLE.read_text())
        record["requirements"][0]["knowledge_status"] = "SPECIFIED"
        record["requirements"][0]["depends_on"] = []
        # Preview metadata, not an independent source-authenticity proof.
        record["sources"][0]["integrity"] = "PINNED_SHA256"
        record["sources"][0]["sha256"] = "a" * 64
        record["action_requests"][0].update(
            operation_id="schema.validate",
            target={"kind": "requirement", "requirement_id": "REQ-api-sdk"},
            intent="validate_specification")
        registry = {"protocol": "factoryweaver/registry-v1", "operations": [{
            "operation_id": "schema.validate", "owner": "example-checker",
            "allowed_modes": ["READ_ONLY"], "target_kinds": ["requirement"],
            "enabled": True,
        }]}
        projected = fw.project(record)["projection"][0]
        routed = fw.route(record, registry)["requests"][0]
        self.assertEqual(projected["state"], "READY_FOR_OWNER_REVIEW")
        self.assertEqual(routed["route"], "REGISTERED_CANDIDATE_ONLY")
        self.assertFalse(routed["can_execute"])

    def pinned_route_fixture(self):
        record = json.loads(SAMPLE.read_text())
        record["requirements"][0].update(knowledge_status="SPECIFIED", depends_on=[])
        record["sources"][0].update(integrity="PINNED_SHA256", sha256="a" * 64)
        record["action_requests"][0].update(
            operation_id="schema.validate", intent="validate_specification",
            target={"kind": "requirement", "requirement_id": "REQ-api-sdk"})
        registry = {"protocol": "factoryweaver/registry-v1", "operations": [{
            "operation_id": "schema.validate", "owner": "example-checker",
            "allowed_modes": ["READ_ONLY"], "target_kinds": ["requirement"],
            "enabled": True, "requires_pinned_source": True,
        }]}
        return record, registry

    def add_route_source(self, record):
        source = copy.deepcopy(record["sources"][0])
        source.update(source_id="SRC-OTHER", source_dependency_key="other-source",
                      integrity="UNPINNED")
        source.pop("sha256", None)
        record["sources"].append(source)

    def test_pinned_route_ignores_independent_unknown_requirement(self):
        for has_requirement in (False, True):
            with self.subTest(has_requirement=has_requirement):
                record, registry = self.pinned_route_fixture()
                self.add_route_source(record)
                if has_requirement:
                    other = copy.deepcopy(record["requirements"][0])
                    other.update(id="REQ-independent", knowledge_status="UNKNOWN",
                                 source_ids=["SRC-OTHER"])
                    record["requirements"].append(other)
                result = fw.route(record, registry)
                self.assertEqual(result, {"requests": [{
                    "request_id": "AR-docs", "operation_id": "schema.validate",
                    "route": "REGISTERED_CANDIDATE_ONLY", "owner": "example-checker",
                    "requirement_state": "READY_FOR_OWNER_REVIEW", "can_execute": False,
                }], "effects": 0, "authority": "NONE"})

    def test_pinned_transitive_route_ignores_unrelated_source(self):
        record, registry = self.pinned_route_fixture()
        self.add_route_source(record)
        parent = copy.deepcopy(record["requirements"][0])
        parent.update(id="REQ-parent", depends_on=["SPEC-api-contract", "DEC-auth-owner"])
        grandparent = copy.deepcopy(record["requirements"][0])
        grandparent.update(id="REQ-grandparent")
        parent["depends_on"].append("REQ-grandparent")
        record["requirements"].extend([parent, grandparent])
        record["requirements"][0]["depends_on"] = ["REQ-parent"]
        record["action_requests"][0]["intent"] = "resolve_unknown"
        result = fw.route(record, registry)
        row = result["requests"][0]
        self.assertEqual((row["route"], row["requirement_state"]),
                         ("REGISTERED_CANDIDATE_ONLY", "WAIT_FOR_PREREQUISITE"))
        self.assertEqual((row["can_execute"], result["effects"], result["authority"]),
                         (False, 0, "NONE"))

    def test_route_requires_pins_for_explicit_dependency_sources(self):
        for contributor in ("direct", "requirement", "card", "decision"):
            with self.subTest(contributor=contributor):
                record, registry = self.pinned_route_fixture()
                self.add_route_source(record)
                record["action_requests"][0]["intent"] = "resolve_unknown"
                if contributor == "direct":
                    record["requirements"][0]["source_ids"] = ["SRC-OTHER"]
                elif contributor == "requirement":
                    parent = copy.deepcopy(record["requirements"][0])
                    parent.update(id="REQ-parent", source_ids=["SRC-OTHER"])
                    child = copy.deepcopy(record["requirements"][0])
                    child.update(id="REQ-child", depends_on=["REQ-parent"])
                    record["requirements"].extend([parent, child])
                    record["requirements"][0]["depends_on"] = ["REQ-child"]
                elif contributor == "card":
                    record["cards"][0]["evidence_ids"] = ["SRC-OTHER"]
                    record["requirements"][0]["depends_on"] = ["SPEC-api-contract"]
                else:
                    record["decisions"][0]["source_ids"] = ["SRC-OTHER"]
                    record["requirements"][0]["depends_on"] = ["DEC-auth-owner"]
                row = fw.route(record, registry)["requests"][0]
                self.assertEqual(row["route"], "WAIT_FOR_SOURCE_PIN")
                self.assertFalse(row["can_execute"])

    def test_typed_card_links_do_not_become_route_prerequisites(self):
        record, registry = self.pinned_route_fixture()
        self.add_route_source(record)
        record["requirements"][0]["depends_on"] = ["SPEC-api-contract"]
        other = copy.deepcopy(record["requirements"][0])
        other.update(id="REQ-independent", knowledge_status="UNKNOWN",
                     source_ids=["SRC-OTHER"], depends_on=[])
        record["requirements"].append(other)
        record["cards"][0]["typed_links"] = [
            {"relation": "implements", "target": "REQ-independent"}]
        row = fw.route(record, registry)["requests"][0]
        self.assertEqual((row["route"], row["requirement_state"]),
                         ("REGISTERED_CANDIDATE_ONLY", "READY_FOR_OWNER_REVIEW"))
        self.assertFalse(row["can_execute"])

    def test_colliding_requirement_and_card_ids_keep_both_source_contributors(self):
        for unpinned_contributor in ("requirement", "card"):
            with self.subTest(unpinned_contributor=unpinned_contributor):
                record, registry = self.pinned_route_fixture()
                self.add_route_source(record)
                record["cards"][0]["stable_id"] = "REQ-api-sdk"
                if unpinned_contributor == "requirement":
                    record["requirements"][0]["source_ids"] = ["SRC-OTHER"]
                else:
                    record["cards"][0]["evidence_ids"] = ["SRC-OTHER"]
                record["action_requests"][0]["intent"] = "resolve_unknown"
                row = fw.route(record, registry)["requests"][0]
                self.assertEqual(row["route"], "WAIT_FOR_SOURCE_PIN")
                self.assertFalse(row["can_execute"])

    def test_unbound_unknown_resolution_remains_conservative(self):
        record, registry = self.pinned_route_fixture()
        self.add_route_source(record)
        request = record["action_requests"][0]
        request["intent"] = "resolve_unknown"
        del request["target"]["requirement_id"]
        self.assertEqual(fw.route(record, registry)["requests"][0]["route"],
                         "WAIT_FOR_SOURCE_PIN")
        registry["operations"][0]["requires_pinned_source"] = False
        self.assertEqual(fw.route(record, registry)["requests"][0]["route"],
                         "REGISTERED_CANDIDATE_ONLY")

    def test_route_precedence_still_refuses_invalid_bindings_and_scope(self):
        for mutation, expected in (("unbound", "REQUIREMENT_BINDING_REQUIRED"),
                                   ("unknown", "UNKNOWN_REQUIREMENT"),
                                   ("disabled", "CAPABILITY_DISABLED"),
                                   ("scope", "REGISTRY_SCOPE_MISMATCH"),
                                   ("human", "REQUIREMENT_BLOCKED")):
            with self.subTest(mutation=mutation):
                record, registry = self.pinned_route_fixture()
                self.add_route_source(record)
                request = record["action_requests"][0]
                entry = registry["operations"][0]
                if mutation == "unbound":
                    del request["target"]["requirement_id"]
                elif mutation == "unknown":
                    request["target"]["requirement_id"] = "REQ-not-found"
                elif mutation == "disabled":
                    entry["enabled"] = False
                elif mutation == "scope":
                    entry["target_kinds"] = ["official_doc"]
                else:
                    record["requirements"][0]["depends_on"] = ["DEC-auth-owner"]
                row = fw.route(record, registry)["requests"][0]
                self.assertEqual(row["route"], expected)
                self.assertFalse(row["can_execute"])

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
