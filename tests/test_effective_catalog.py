"""Carrier-supplied effective Skill catalog is *untrusted* until owner readback."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from factory_profile import (
    ProfileError, profile_digest, audit_effective_catalog
)


def inputs():
    profile = json.loads(
        (ROOT / "examples/factory-profiles/pstack-synthetic.json").read_text()
    )
    digest = profile_digest(profile)
    binding = {
        "protocol": "factoryweaver/factory-binding-v1",
        "profile_sha256": digest,
        "work_order": {"id": "fictional/target#10", "repository": "fictional/target",
                       "base_sha": "a" * 40},
        "carrier": {"id": "noodle", "capabilities": profile["carrier_capabilities"]},
        "session": {
            "id": "session-a", "worktree_id": "worktree-a",
            "worktree_path": "/disposable/worktrees/a",
            "repository": "fictional/target",
            "entry_skill": profile["workflow_entry"],
            "profile_sha256": digest,
            "skill_view": [
                {"name": skill["name"], "tree_sha256": skill["tree_sha256"]}
                for skill in profile["skills"]
            ],
        },
        "effect_authority": False,
    }
    catalog = {
        "protocol": "factoryweaver/effective-skill-catalog-v1",
        "producer_claim": "UNVERIFIED_CARRIER_OUTPUT",
        "profile_sha256": digest,
        "work_order_id": binding["work_order"]["id"],
        "carrier_id": binding["carrier"]["id"],
        "session_id": "session-a", "worktree_id": "worktree-a",
        "entry_skill": profile["workflow_entry"],
        "skills": [
            {"name": skill["name"], "tree_sha256": skill["tree_sha256"],
             "scope": "worktree"} for skill in profile["skills"]
        ],
    }
    return profile, binding, catalog


class EffectiveCatalogTests(unittest.TestCase):
    def test_good_declared_catalog_is_never_owner_receipt(self):
        profile, binding, catalog = inputs()
        result = audit_effective_catalog(profile, binding, catalog)
        self.assertEqual(result["status"], "EFFECTIVE_CATALOG_CLAIM_MATCHES")
        self.assertFalse(result["original_owner_capture_verified"])
        self.assertFalse(result["actual_worker_skill_discovery_verified"])
        self.assertFalse(result["global_skill_exclusion_verified"])
        self.assertFalse(result["effect_authority"])

    def test_global_skill_injection_refuses(self):
        profile, binding, catalog = inputs()
        catalog["skills"].append({
            "name": "builder-bug-factory", "tree_sha256": "f" * 64,
            "scope": "global"
        })
        with self.assertRaisesRegex(ProfileError, "catalog_unlisted_skill"):
            audit_effective_catalog(profile, binding, catalog)

    def test_allowed_skill_inherited_globally_refuses(self):
        profile, binding, catalog = inputs()
        catalog["skills"][0]["scope"] = "user"
        with self.assertRaisesRegex(ProfileError, "catalog_nonworktree_inheritance"):
            audit_effective_catalog(profile, binding, catalog)

    def test_wrong_worker_session_and_carrier_refuse(self):
        profile, binding, catalog = inputs()
        catalog["session_id"] = "another-session"
        with self.assertRaisesRegex(ProfileError, "catalog_identity_mismatch:session_id"):
            audit_effective_catalog(profile, binding, catalog)
        profile, binding, catalog = inputs()
        catalog["carrier_id"] = "another-carrier"
        with self.assertRaisesRegex(ProfileError, "catalog_identity_mismatch:carrier_id"):
            audit_effective_catalog(profile, binding, catalog)

    def test_profile_revision_drift_refuses(self):
        profile, binding, catalog = inputs()
        catalog["profile_sha256"] = "0" * 64
        with self.assertRaisesRegex(ProfileError, "catalog_identity_mismatch:profile_sha256"):
            audit_effective_catalog(profile, binding, catalog)

    def test_missing_and_duplicate_skills_refuse(self):
        profile, binding, catalog = inputs()
        catalog["skills"].pop()
        with self.assertRaisesRegex(ProfileError, "catalog_missing_skill"):
            audit_effective_catalog(profile, binding, catalog)
        profile, binding, catalog = inputs()
        catalog["skills"].append(dict(catalog["skills"][0]))
        with self.assertRaisesRegex(ProfileError, "catalog_duplicate_skill"):
            audit_effective_catalog(profile, binding, catalog)

    def test_claimed_skill_digest_drift_refuses(self):
        profile, binding, catalog = inputs()
        catalog["skills"][0]["tree_sha256"] = "0" * 64
        with self.assertRaisesRegex(ProfileError, "catalog_skill_digest_drift"):
            audit_effective_catalog(profile, binding, catalog)

    def test_claimed_trusted_source_refuses(self):
        profile, binding, catalog = inputs()
        catalog["producer_claim"] = "OWNER_VERIFIED"
        with self.assertRaisesRegex(ProfileError, "catalog_producer_claim_invalid"):
            audit_effective_catalog(profile, binding, catalog)
        profile, binding, catalog = inputs()
        catalog["owner_approved"] = True
        with self.assertRaisesRegex(ProfileError, "catalog_shape"):
            audit_effective_catalog(profile, binding, catalog)

if __name__ == "__main__":
    unittest.main()
