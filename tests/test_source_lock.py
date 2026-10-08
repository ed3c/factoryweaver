"""Source-lock is an offline byte check, never an independent origin attestation."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from source_lock import git_blob_sha1, verify_source
from factoryweaver import ContractError

RAW = b"""---
name: synthetic-grilling
---
Work the frontier in rounds and record confirmed decisions.
Wait for the human answer before continuing execution.
The suggested answer is not an authorization or owner readback.
"""


def manifest(raw=RAW):
    return {
        "protocol": "factoryweaver/source-lock-v1",
        "repository": "example/synthetic-upstream",
        "revision": "a" * 40,
        "path": "skills/grilling/SKILL.md",
        "git_blob_sha1": git_blob_sha1(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "source_dependency_key": "single-synthetic-origin",
        "anchors": [
            {"id": "human-frontier", "text_match": "Wait for the human answer before continuing execution."},
            {"id": "permission-boundary", "text_match": "The suggested answer is not an authorization or owner readback."},
        ],
    }


class SourceLockTests(unittest.TestCase):
    def test_valid_bytes_and_anchor_fixture(self):
        result = verify_source(manifest(), RAW)
        self.assertEqual(result["status"], "SUPPLIED_BYTES_MATCH_FROZEN_MANIFEST")
        self.assertEqual(result["anchors_verified"], 2)
        self.assertFalse(result["external_origin_authenticated"])
        self.assertFalse(result["provider_readback_verified"])
        self.assertFalse(result["effect_authority"])

    def test_mutated_bytes_fail_even_if_locator_remains(self):
        with self.assertRaisesRegex(ContractError, "git_blob_sha1_mismatch"):
            verify_source(manifest(), RAW + b"unauthorized injected footer\n")

    def test_false_github_blob_does_not_pass_with_correct_sha256(self):
        fake = manifest()
        fake["git_blob_sha1"] = "b" * 40
        with self.assertRaisesRegex(ContractError, "git_blob_sha1_mismatch"):
            verify_source(fake, RAW)

    def test_wrong_sha256_also_refuses(self):
        fake = manifest()
        fake["sha256"] = "b" * 64
        with self.assertRaisesRegex(ContractError, "source_sha256_mismatch"):
            verify_source(fake, RAW)

    def test_missing_anchor_or_quote_substitution_refuses(self):
        bad = manifest()
        bad["anchors"][0]["text_match"] = "human said yes and confirmed the choice"
        with self.assertRaisesRegex(ContractError, "missing_or_ambiguous_text_match"):
            verify_source(bad, RAW)

    def test_repeated_quote_is_not_unique_locator(self):
        repeated = RAW + b"Wait for the human answer before continuing execution.\n"
        with self.assertRaisesRegex(ContractError, "missing_or_ambiguous_text_match"):
            verify_source(manifest(repeated), repeated)

    def test_unpinned_revision_and_traversal_refuse(self):
        fake = manifest()
        fake["revision"] = "main"
        with self.assertRaisesRegex(ContractError, "source_revision_unpinned"):
            verify_source(fake, RAW)
        fake = manifest()
        fake["path"] = "../private/control.json"
        with self.assertRaisesRegex(ContractError, "source_path_invalid"):
            verify_source(fake, RAW)

    def test_claim_of_independent_owner_is_rejected_by_shape(self):
        fake = manifest()
        fake["original_owner_authenticated"] = True
        with self.assertRaisesRegex(ContractError, "source_manifest_shape"):
            verify_source(fake, RAW)

    def test_cli_exercises_raw_bytes_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            raw_file = base / "source.txt"
            manifest_file = base / "manifest.json"
            raw_file.write_bytes(RAW)
            manifest_file.write_text(json.dumps(manifest()), encoding="utf-8")
            p = subprocess.run([sys.executable, str(ROOT / "scripts/source_lock.py"),
                                str(manifest_file), str(raw_file)], text=True, capture_output=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(json.loads(p.stdout)["anchors_verified"], 2)


if __name__ == "__main__":
    unittest.main()
