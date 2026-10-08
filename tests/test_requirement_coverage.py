"""Positive and planted falsifiers for declared JD-clause trace coverage."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "scripts/requirement_coverage.py"
RECORD = ROOT / "examples/openai-plugin-platform/project.json"
INVENTORY = ROOT / "examples/openai-plugin-platform/job-clause-inventory.json"
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("coverage_auditor", FILE)
coverage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coverage)
sys.path.insert(0, str(ROOT / "scripts"))
from factoryweaver import ContractError


def inputs():
    return json.loads(RECORD.read_text()), json.loads(INVENTORY.read_text())


class RequirementCoverageTests(unittest.TestCase):
    def test_current_real_jd_inventory_surfaces_five_missing(self):
        record, inventory = inputs()
        result = coverage.trace(record, inventory)
        self.assertEqual(result["inventory_clause_count"], 6)
        self.assertEqual(result["declared_link_count"], 1)
        self.assertEqual(len(result["unmapped_clause_ids"]), 5)
        self.assertEqual(result["rows"][0]["requirement_ids"], ["REQ-api-sdk"])
        self.assertEqual(result["rows"][0]["spec_card_ids"], ["SPEC-api-contract"])
        self.assertEqual(result["rows"][1]["trace_status"], "UNMAPPED")
        for key in ("source_exhaustiveness_proven", "source_origin_authenticated",
                    "semantic_mapping_verified", "engineering_verified",
                    "delivery_verified", "effect_authority"):
            self.assertFalse(result[key], key)

    def test_mappings_deterministic_with_repeated_input(self):
        record, inventory = inputs()
        self.assertEqual(coverage.trace(record, inventory),
                         coverage.trace(copy.deepcopy(record), copy.deepcopy(inventory)))

    def test_all_links_are_only_declared_not_semantically_proven(self):
        record, inventory = inputs()
        for clause in inventory["clauses"]:
            clause["requirement_ids"] = ["REQ-api-sdk"]
        result = coverage.trace(record, inventory)
        self.assertEqual(result["declared_link_count"], 6)
        self.assertEqual(result["unmapped_clause_ids"], [])
        self.assertFalse(result["semantic_mapping_verified"])
        self.assertFalse(result["source_exhaustiveness_proven"])

    def test_unknown_requirement_refuses(self):
        record, inventory = inputs()
        inventory["clauses"][1]["requirement_ids"] = ["REQ-does-not-exist"]
        with self.assertRaisesRegex(ContractError, "coverage_unknown_requirement"):
            coverage.trace(record, inventory)

    def test_requirement_source_cannot_be_swapped(self):
        record, inventory = inputs()
        record["sources"].append({
            "source_id": "SRC-other", "source_type": "official_doc",
            "source_dependency_key": "unrelated-origin", "locator": "unrelated",
            "uri": "https://example.org/unrelated", "integrity": "UNPINNED"})
        record["requirements"][0]["source_ids"] = ["SRC-other"]
        with self.assertRaisesRegex(ContractError, "coverage_requirement_source_mismatch"):
            coverage.trace(record, inventory)

    def test_unknown_or_changed_source_identity_refuses(self):
        record, inventory = inputs()
        inventory["source_id"] = "SRC-nobody"
        with self.assertRaisesRegex(ContractError, "coverage_unknown_source"):
            coverage.trace(record, inventory)
        _, inventory = inputs()
        inventory["source_dependency_key"] = "another-document"
        with self.assertRaisesRegex(ContractError, "coverage_source_dependency_mismatch"):
            coverage.trace(record, inventory)

    def test_subject_mismatch_refuses(self):
        record, inventory = inputs()
        inventory["subject_id"] = "someone-elses-project"
        with self.assertRaisesRegex(ContractError, "coverage_subject_mismatch"):
            coverage.trace(record, inventory)

    def test_duplicate_clauses_refuse_not_silently_overcount(self):
        record, inventory = inputs()
        inventory["clauses"][1]["clause_id"] = inventory["clauses"][0]["clause_id"]
        with self.assertRaisesRegex(ContractError, "coverage_duplicate_clause_id"):
            coverage.trace(record, inventory)

    def test_provenance_metadata_cannot_fake_pinned_source(self):
        record, inventory = inputs()
        inventory["source_state"] = "PINNED_SHA256"
        with self.assertRaisesRegex(ContractError, "coverage_source_pin_mismatch"):
            coverage.trace(record, inventory)

    def test_claim_kind_cannot_promote_unsupported_fact(self):
        record, inventory = inputs()
        inventory["clauses"][1]["claim_kind"] = "VERIFIED_TRUE"
        with self.assertRaisesRegex(ContractError, "coverage_claim_kind_unverified"):
            coverage.trace(record, inventory)

    def test_empty_inventory_or_hidden_key_refused(self):
        record, inventory = inputs()
        inventory["clauses"] = []
        with self.assertRaisesRegex(ContractError, "coverage_clauses_missing"):
            coverage.trace(record, inventory)
        record, inventory = inputs()
        inventory["complete"] = True
        with self.assertRaisesRegex(ContractError, "coverage_inventory_shape"):
            coverage.trace(record, inventory)

    def test_cli_exit_and_counts(self):
        result = subprocess.run(
            [sys.executable, str(FILE), str(RECORD), str(INVENTORY)],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["inventory_clause_count"], 6)
        self.assertEqual(payload["declared_link_count"], 1)
        self.assertEqual(len(payload["unmapped_clause_ids"]), 5)
        self.assertEqual(payload["coverage_kind"], "STRUCTURAL_TRACE_ONLY")


if __name__ == "__main__":
    unittest.main()
