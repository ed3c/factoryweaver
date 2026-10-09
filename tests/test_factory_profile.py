"""Factory Profile Lock contracts, negative controls, and local Git worktree proof.

Do not treat a fake session manifest as a real Noodle or alternate carrier run.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from factory_profile import (
    ProfileError, profile_digest, validate_profile, validate_binding, compare,
    compare_carriers, origin_repository_identity,
    observe_git_worktree
)

EXAMPLES = ROOT / "examples/factory-profiles"
CAPABILITIES = [
    "isolated_git_worktree", "skill_discovery",
    "session_readback", "source_pinning"
]


def load_profile(which="pstack"):
    return json.loads((EXAMPLES / (which + "-synthetic.json")).read_text())


def binding(profile, *, carrier="noodle", session="worker-1",
            tree="tree-1", path="/fixtures/worktrees/one", skills=None):
    return {
        "protocol": "factoryweaver/factory-binding-v1",
        "profile_sha256": profile_digest(profile),
        "work_order": {"id": "issue:fictional/target#1",
                       "repository": "fictional/target",
                       "base_sha": "b" * 40},
        "carrier": {"id": carrier, "capabilities": list(CAPABILITIES)},
        "session": {
            "id": session, "worktree_id": tree, "worktree_path": path,
            "repository": "fictional/target",
            "entry_skill": profile["workflow_entry"],
            "profile_sha256": profile_digest(profile),
            "skill_view": (skills if skills is not None else
                           [{"name": s["name"], "tree_sha256": s["tree_sha256"]}
                            for s in profile["skills"]])
        },
        "effect_authority": False
    }


class FactoryProfileTests(unittest.TestCase):
    def test_two_profiles_single_whole_issue_root(self):
        for kind in ("pstack", "builder"):
            profile = load_profile(kind)
            status = validate_profile(profile)
            self.assertEqual(status["status"], "PROFILE_SHAPE_VALID")
            self.assertEqual(len(status["profile_sha256"]), 64)
            self.assertFalse(status["effect_authority"])

    def test_two_profiles_disjoint_declarations(self):
        a, b = load_profile("pstack"), load_profile("builder")
        first, second = binding(a), binding(
            b, carrier="other-worker", session="worker-2",
            tree="tree-2", path="/fixtures/worktrees/two"
        )
        self.assertEqual(validate_binding(a, first)["status"], "ADVISORY_MATCH_ONLY")
        self.assertEqual(validate_binding(b, second)["status"], "ADVISORY_MATCH_ONLY")
        result = compare(a, first, b, second)
        self.assertEqual(result["status"], "DECLARED_WORKTREES_DISJOINT")
        self.assertFalse(result["physical_isolation_verified"])

    def test_replaceable_carrier_is_not_hardcoded_noodle(self):
        profile = load_profile()
        one = validate_binding(profile, binding(profile, carrier="noodle"))
        other = validate_binding(profile, binding(profile, carrier="alternate-worker"))
        self.assertEqual(one["profile_sha256"], other["profile_sha256"])
        self.assertEqual(other["carrier_id"], "alternate-worker")
        self.assertFalse(one["original_owner_readback_verified"])
        self.assertFalse(other["original_owner_readback_verified"])

    def test_two_carriers_same_work_order_are_only_claim_comparable(self):
        p = load_profile()
        a = binding(p)
        b = binding(p, carrier="another-carrier", session="session-2",
                    tree="tree-2", path="/fixtures/worktrees/two")
        result = compare_carriers(p, a, b)
        self.assertEqual(result["status"], "DECLARED_CARRIER_INPUTS_COMPARABLE")
        self.assertFalse(result["runtime_interoperability_verified"])
        self.assertFalse(result["original_owner_readback_verified"])
        self.assertEqual(result["observed_worker_runs"], 0)

    def test_carrier_comparison_rejects_different_work_order_or_same_carrier(self):
        p = load_profile()
        a = binding(p)
        b = binding(p, carrier="another-carrier", session="session-2",
                    tree="tree-2", path="/fixtures/worktrees/two")
        b["work_order"]["base_sha"] = "e" * 40
        with self.assertRaisesRegex(ProfileError, "carrier_work_order_mismatch"):
            compare_carriers(p, a, b)
        b["work_order"]["base_sha"] = a["work_order"]["base_sha"]
        b["carrier"]["id"] = "noodle"
        with self.assertRaisesRegex(ProfileError, "alternative_carrier_identity_required"):
            compare_carriers(p, a, b)

    def test_carrier_comparison_rejects_reused_worker_or_overlapping_path(self):
        p = load_profile()
        a = binding(p)
        b = binding(p, carrier="another-carrier", session="session-2",
                    tree="tree-2", path="/fixtures/worktrees/two")
        b["session"]["worktree_id"] = a["session"]["worktree_id"]
        with self.assertRaisesRegex(ProfileError, "carrier_session_or_worktree_reused"):
            compare_carriers(p, a, b)
        b["session"]["worktree_id"] = "tree-2"
        b["session"]["worktree_path"] = "/fixtures/worktrees/one/child"
        with self.assertRaisesRegex(ProfileError, "carrier_worktree_paths_overlap"):
            compare_carriers(p, a, b)

    def test_multiple_software_factories_cannot_be_workflow_roots(self):
        profile = load_profile()
        profile["skills"].append({
            "name": "builder-bug-factory", "role": "workflow_entry",
            "repository": "example.invalid/other",
            "source_commit": "c" * 40, "subpath": "factory/SKILL.md",
            "tree_sha256": "b" * 64
        })
        with self.assertRaisesRegex(ProfileError, "single_workflow_entry_required"):
            validate_profile(profile)

    def test_unexpected_global_skill_fails_closed(self):
        p = load_profile()
        b = binding(p)
        b["session"]["skill_view"].append({"name": "global-grilling",
                                           "tree_sha256": "f" * 64})
        with self.assertRaisesRegex(ProfileError, "undeclared_inherited_skill"):
            validate_binding(p, b)

    def test_missing_skill_and_digest_drift_fail(self):
        p = load_profile()
        b = binding(p)
        b["session"]["skill_view"].pop()
        with self.assertRaisesRegex(ProfileError, "missing_declared_skill"):
            validate_binding(p, b)
        b = binding(p)
        b["session"]["skill_view"][0]["tree_sha256"] = "c" * 64
        with self.assertRaisesRegex(ProfileError, "skill_digest_mismatch"):
            validate_binding(p, b)

    def test_modified_profile_and_wrong_entry_fail(self):
        p = load_profile()
        b = binding(p)
        p["profile_id"] = "changed-profile"
        with self.assertRaisesRegex(ProfileError, "profile_sha256_mismatch"):
            validate_binding(p, b)
        p = load_profile()
        b = binding(p)
        b["session"]["entry_skill"] = "builder-bug-factory"
        with self.assertRaisesRegex(ProfileError, "workflow_entry_mismatch"):
            validate_binding(p, b)

    def test_missing_carrier_capability_fail(self):
        p = load_profile()
        b = binding(p)
        b["carrier"]["capabilities"].remove("skill_discovery")
        with self.assertRaisesRegex(ProfileError, "carrier_capabilities_missing"):
            validate_binding(p, b)

    def test_cross_worktree_reuse_and_nested_path_fail(self):
        a, b = load_profile("pstack"), load_profile("builder")
        first = binding(a)
        second = binding(b, carrier="other", session="worker-2",
                         tree="tree-2", path="/fixtures/worktrees/two")
        second["session"]["worktree_id"] = first["session"]["worktree_id"]
        with self.assertRaisesRegex(ProfileError, "cross_profile_worktree_reused"):
            compare(a, first, b, second)
        second["session"]["worktree_id"] = "tree-2"
        second["session"]["worktree_path"] = "/fixtures/worktrees/one/child"
        with self.assertRaisesRegex(ProfileError, "overlapping_declared_worktree_path"):
            compare(a, first, b, second)
        second["session"]["worktree_path"] = "/fixtures/worktrees/two"
        second["session"]["id"] = first["session"]["id"]
        with self.assertRaisesRegex(ProfileError, "cross_profile_session_reused"):
            compare(a, first, b, second)

    def test_bad_worktree_path_and_foreign_repository_fail(self):
        p = load_profile()
        b = binding(p)
        b["session"]["worktree_path"] = "/private/worktrees/../main"
        with self.assertRaisesRegex(ProfileError, "unsafe_declared_worktree_path"):
            validate_binding(p, b)
        b = binding(p)
        b["session"]["repository"] = "attacker/foreign"
        with self.assertRaisesRegex(ProfileError, "worktree_repository_mismatch"):
            validate_binding(p, b)

    def test_selected_origin_url_matches_repository_not_just_same_worktree(self):
        p = load_profile()
        claim = binding(p)
        claim["work_order"]["origin_url"] = "https://github.com/fictional/target.git"
        self.assertEqual(validate_binding(p, claim)["status"], "ADVISORY_MATCH_ONLY")
        claim["work_order"]["origin_url"] = "https://github.com/another/repository.git"
        with self.assertRaisesRegex(ProfileError, "selected_origin_repository_mismatch"):
            validate_binding(p, claim)

    def test_source_remote_syntax_has_explicit_limits(self):
        valid = ["https://github.com/fictional/target.git",
                 "git@github.com:fictional/target.git",
                 "ssh://git@github.com/fictional/target.git"]
        for remote in valid:
            self.assertEqual(origin_repository_identity(remote), "fictional/target")
        for remote in ["file:///tmp/fictional/target", "../fictional/target",
                       "https://credential@github.com/fictional/target",
                       "https://github.com/fictional/target?token=secret"]:
            with self.assertRaisesRegex(ProfileError, "git_origin_format_unrecognized"):
                origin_repository_identity(remote)

    def test_profile_refuses_mutable_git_source_and_duplicate_skill(self):
        p = load_profile()
        p["skills"][0]["source_commit"] = "main"
        with self.assertRaises(Exception):
            validate_profile(p)
        p = load_profile()
        p["skills"].append(copy.deepcopy(p["skills"][0]))
        with self.assertRaisesRegex(ProfileError, "duplicate_skill_name"):
            validate_profile(p)

    def test_local_git_worktrees_physically_separate_files_not_processes(self):
        # A real disposable Git worktree test; this is not a Noodle launched
        # session and does not assert HOME/network/credential isolation.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, a, b = root / "repo", root / "a", root / "b"
            def git(*args):
                result = subprocess.run(["git", *args], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout.strip()
            git("init", "-q", "-b", "main", str(repo))
            git("-C", str(repo), "config", "user.name", "Fixture")
            git("-C", str(repo), "config", "user.email", "test@example.invalid")
            (repo / "readme.txt").write_text("fixture")
            git("-C", str(repo), "add", "readme.txt")
            git("-C", str(repo), "commit", "-qm", "base")
            selected_remote = "https://github.com/fictional/target.git"
            git("-C", str(repo), "remote", "add", "origin", selected_remote)
            git("-C", str(repo), "worktree", "add", "-q", "-b", "factory-a", str(a))
            git("-C", str(repo), "worktree", "add", "-q", "-b", "factory-b", str(b))
            (a / "only-a.txt").write_text("factory-a")
            (b / "only-b.txt").write_text("factory-b")
            self.assertFalse((a / "only-b.txt").exists())
            self.assertFalse((b / "only-a.txt").exists())
            self.assertNotEqual(git("-C", str(a), "rev-parse", "--git-dir"),
                                git("-C", str(b), "rev-parse", "--git-dir"))
            self.assertEqual(git("-C", str(a), "rev-parse", "--git-common-dir"),
                             git("-C", str(b), "rev-parse", "--git-common-dir"))
            # The public read-only probe can confirm local checkout identity,
            # not the Noodle process that supposedly owns that checkout.
            profile = load_profile()
            claimed = binding(profile, path=str(a))
            claimed["session"]["head_sha"] = git("-C", str(a), "rev-parse", "HEAD")
            claimed["work_order"]["base_sha"] = claimed["session"]["head_sha"]
            claimed["work_order"]["origin_url"] = selected_remote
            observed = observe_git_worktree(profile, claimed)
            self.assertEqual(observed["status"], "LOCAL_GIT_WORKTREE_OBSERVED")
            self.assertTrue(observed["physical_git_checkout_observed"])
            self.assertFalse(observed["worker_session_observed"])
            self.assertFalse(observed["skill_view_physically_observed"])
            claimed["session"]["head_sha"] = "c" * 40
            with self.assertRaisesRegex(ProfileError, "worktree_head_changed"):
                observe_git_worktree(profile, claimed)
            claimed["session"]["head_sha"] = git("-C", str(repo), "rev-parse", "HEAD")
            claimed["session"]["worktree_path"] = str(repo)
            with self.assertRaisesRegex(ProfileError, "linked_worktree_gitfile_required"):
                observe_git_worktree(profile, claimed)

    def test_unobserved_git_worktree_head_is_named_blocker(self):
        profile = load_profile()
        claim = binding(profile)
        with self.assertRaisesRegex(ProfileError, "worktree_head_pin_required"):
            observe_git_worktree(profile, claim)

    def test_cli_profiles_have_no_authority(self):
        script = ROOT / "scripts/factory_profile.py"
        profile = EXAMPLES / "pstack-synthetic.json"
        result = subprocess.run([sys.executable, str(script), "validate", str(profile)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["status"], "PROFILE_SHAPE_VALID")
        self.assertFalse(output["effect_authority"])


if __name__ == "__main__":
    unittest.main()
