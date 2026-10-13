"""Physical local worktree skill file allowlist controls (not an Agent discovery proof)."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from factory_profile import (
    ProfileError, profile_digest, observe_local_skill_view, skill_tree_sha256,
)

def git(*parts):
    result = subprocess.run(["git", *parts], text=True, capture_output=True)
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout.strip()

class LocalSkillViewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        top = Path(self.tmp.name)
        self.root, self.a, self.b = top / "repo", top / "lane-a", top / "lane-b"
        git("init", "-q", "-b", "main", str(self.root))
        git("-C", str(self.root), "config", "user.name", "Fixture")
        git("-C", str(self.root), "config", "user.email", "fixture@example.invalid")
        (self.root / "README.md").write_text("disposable\n", encoding="utf-8")
        git("-C", str(self.root), "add", "README.md")
        git("-C", str(self.root), "commit", "-qm", "base")
        self.origin_url = "https://github.com/fictional/target.git"
        git("-C", str(self.root), "remote", "add", "origin", self.origin_url)
        git("-C", str(self.root), "worktree", "add", "-q", "-b", "lane-a", str(self.a))
        git("-C", str(self.root), "worktree", "add", "-q", "-b", "lane-b", str(self.b))
        self.p = []
        self.bindings = []
        for index, (kind, folder) in enumerate((("pstack", self.a), ("builder", self.b))):
            record = json.loads(
                (ROOT / "examples/factory-profiles" / (kind + "-synthetic.json")).read_text()
            )
            for skill in record["skills"]:
                path = folder / ".agents" / "skills" / skill["name"]
                path.mkdir(parents=True)
                (path / "SKILL.md").write_text(
                    "---\nname: " + skill["name"] + "\n---\n# Synthetic\n",
                    encoding="utf-8")
                skill["tree_sha256"] = skill_tree_sha256(path)
            self.p.append(record)
            self.bindings.append({
                "protocol": "factoryweaver/factory-binding-v1",
                "profile_sha256": profile_digest(record),
                "work_order": {"id": f"fictional/target#{index+1}",
                               "repository": "fictional/target",
                               "base_sha": git("-C", str(folder), "rev-parse", "HEAD"),
                               "origin_url": self.origin_url},
                "carrier": {"id": "noodle" if index == 0 else "alternate",
                            "capabilities": record["carrier_capabilities"]},
                "session": {"id": "session-" + str(index), "worktree_id": "tree-" + str(index),
                            "worktree_path": str(folder),
                            "head_sha": git("-C", str(folder), "rev-parse", "HEAD"),
                            "repository": "fictional/target",
                            "entry_skill": record["workflow_entry"],
                            "profile_sha256": profile_digest(record),
                            "skill_view": [{"name": s["name"], "tree_sha256": s["tree_sha256"]}
                                           for s in record["skills"]]},
                "effect_authority": False,
            })

    def tearDown(self):
        self.tmp.cleanup()

    def test_two_real_worktrees_have_distinct_local_skill_views(self):
        a = observe_local_skill_view(self.p[0], self.bindings[0])
        b = observe_local_skill_view(self.p[1], self.bindings[1])
        self.assertEqual(a["status"], "LOCAL_WORKTREE_SKILL_FILES_MATCH")
        self.assertEqual(b["status"], "LOCAL_WORKTREE_SKILL_FILES_MATCH")
        self.assertIn("poteto-mode", a["local_skill_names"])
        self.assertNotIn("builder-bug-factory", a["local_skill_names"])
        self.assertIn("builder-bug-factory", b["local_skill_names"])
        self.assertNotIn("poteto-mode", b["local_skill_names"])
        self.assertFalse(a["agent_effective_skill_catalog_verified"])
        self.assertFalse(b["global_skill_inheritance_excluded"])

    def test_registered_worktree_with_special_path_is_observed(self):
        for name in ("技能工作樹", 'quoted"worktree', "tab\tworktree", "line\nworktree"):
            with self.subTest(name=name):
                moved = Path(self.tmp.name) / name
                git("-C", str(self.root), "worktree", "move", str(self.a), str(moved))
                self.a = moved
                self.bindings[0]["session"]["worktree_path"] = str(moved)
                result = observe_local_skill_view(self.p[0], self.bindings[0])
                self.assertEqual(result["status"], "LOCAL_WORKTREE_SKILL_FILES_MATCH")
                self.assertFalse(result["worker_session_observed"])

    def test_worktree_absent_from_git_registration_is_refused(self):
        real_run = subprocess.run

        def without_registration(argv, **kwargs):
            if argv[3:5] == ["worktree", "list"]:
                return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")
            return real_run(argv, **kwargs)

        with patch("factory_profile.subprocess.run", side_effect=without_registration):
            with self.assertRaisesRegex(ProfileError, "worktree_not_registered"):
                observe_local_skill_view(self.p[0], self.bindings[0])

    def test_registered_worktree_with_trailing_whitespace_is_observed(self):
        for name in ("trailing-space ", "trailing-tab\t", "trailing-newline\n"):
            with self.subTest(name=name):
                moved = Path(self.tmp.name) / name
                git("-C", str(self.root), "worktree", "move", str(self.a), str(moved))
                self.a = moved
                self.bindings[0]["session"]["worktree_path"] = str(moved)
                result = observe_local_skill_view(self.p[0], self.bindings[0])
                self.assertEqual(result["status"], "LOCAL_WORKTREE_SKILL_FILES_MATCH")
                self.assertEqual(result["observed_worktree_head_sha"],
                                 self.bindings[0]["session"]["head_sha"])
                self.assertFalse(result["worker_session_observed"])
                self.assertFalse(result["effect_authority"])

    def test_wrong_head_on_trailing_whitespace_worktree_is_refused(self):
        for name in ("trailing-space ", "trailing-tab\t", "trailing-newline\n"):
            with self.subTest(name=name):
                moved = Path(self.tmp.name) / name
                git("-C", str(self.root), "worktree", "move", str(self.a), str(moved))
                self.a = moved
                self.bindings[0]["session"]["worktree_path"] = str(moved)
                self.bindings[0]["session"]["head_sha"] = "e" * 40
                with self.assertRaisesRegex(ProfileError, "worktree_head_changed"):
                    observe_local_skill_view(self.p[0], self.bindings[0])

    def test_inject_foreign_factory_skill_fails_closed(self):
        path = self.a / ".agents" / "skills" / "builder-bug-factory"
        path.mkdir()
        (path / "SKILL.md").write_text("---\nname: builder-bug-factory\n---\n")
        with self.assertRaisesRegex(ProfileError, "unlisted_worktree_skill"):
            observe_local_skill_view(self.p[0], self.bindings[0])

    def test_source_content_tamper_fails_closed(self):
        path = self.a / ".agents" / "skills" / "poteto-mode" / "SKILL.md"
        path.write_text(path.read_text() + "\nUnexpected override\n")
        with self.assertRaisesRegex(ProfileError, "worktree_skill_content_drift"):
            observe_local_skill_view(self.p[0], self.bindings[0])

    def test_missing_skill_fails_closed(self):
        path = self.b / ".agents" / "skills" / "factoryweaver" / "SKILL.md"
        path.unlink()
        with self.assertRaisesRegex(ProfileError, "local_skill_entry_missing"):
            observe_local_skill_view(self.p[1], self.bindings[1])

    def test_symlink_skill_is_refused(self):
        other = self.root / "untrusted-source"
        other.mkdir()
        (self.a / ".agents" / "skills" / "link-from-home").symlink_to(other, target_is_directory=True)
        with self.assertRaisesRegex(ProfileError, "unexpected_worktree_skill_surface"):
            observe_local_skill_view(self.p[0], self.bindings[0])

    def test_symlinked_agents_parent_is_refused(self):
        # Replacing .agents by a link must not let a worker inspect outside the
        # selected worktree even if the ultimate skills/ subtree exists.
        agents = self.a / ".agents"
        outside = Path(self.tmp.name) / "outside-agents"
        agents.rename(outside)
        agents.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ProfileError, "worktree_skill_parent_symlink"):
            observe_local_skill_view(self.p[0], self.bindings[0])

    def test_selected_git_remote_matches_local_config_only(self):
        result = observe_local_skill_view(self.p[0], self.bindings[0])
        self.assertTrue(result["local_skill_files_verified"])
        self.assertTrue(result["selected_origin_config_matched"])
        self.assertFalse(result["remote_provider_identity_authenticated"])
        self.assertFalse(result["original_owner_readback_verified"])

    def test_changed_origin_before_worktree_readback_is_refused(self):
        git("-C", str(self.root), "remote", "set-url", "origin",
            "https://github.com/attacker/wrong-target.git")
        with self.assertRaisesRegex(ProfileError, "worktree_origin_changed"):
            observe_local_skill_view(self.p[0], self.bindings[0])

    def test_origin_with_added_trailing_space_is_refused(self):
        changed_origin = self.origin_url + " "
        git("-C", str(self.root), "remote", "set-url", "origin", changed_origin)
        readback = subprocess.run(
            ["git", "-C", str(self.a), "remote", "get-url", "origin"],
            text=True, capture_output=True, check=True)
        self.assertEqual(readback.stdout, changed_origin + "\n")
        with self.assertRaisesRegex(ProfileError, "worktree_origin_changed"):
            observe_local_skill_view(self.p[0], self.bindings[0])

    def test_unbound_origin_refuses_physical_checkout_claim(self):
        self.bindings[0]["work_order"].pop("origin_url")
        with self.assertRaisesRegex(ProfileError, "worktree_origin_pin_required"):
            observe_local_skill_view(self.p[0], self.bindings[0])

    def test_owner_selected_origin_for_different_repository_is_refused(self):
        self.bindings[0]["work_order"]["origin_url"] = (
            "https://github.com/another/example.git")
        with self.assertRaisesRegex(ProfileError, "selected_origin_repository_mismatch"):
            observe_local_skill_view(self.p[0], self.bindings[0])

    def test_wrong_admission_base_does_not_get_git_identity_pass(self):
        self.bindings[0]["work_order"]["base_sha"] = "e" * 40
        with self.assertRaisesRegex(ProfileError, "work_order_base_not_ancestor"):
            observe_local_skill_view(self.p[0], self.bindings[0])

    def test_candidate_commit_descended_from_base_remains_valid(self):
        folder = self.a
        (folder / "candidate.txt").write_text("one bounded candidate change\n")
        git("-C", str(folder), "add", "candidate.txt")
        git("-C", str(folder), "commit", "-qm", "candidate")
        newer_head = git("-C", str(folder), "rev-parse", "HEAD")
        self.assertNotEqual(newer_head, self.bindings[0]["work_order"]["base_sha"])
        self.bindings[0]["session"]["head_sha"] = newer_head
        result = observe_local_skill_view(self.p[0], self.bindings[0])
        self.assertEqual(result["observed_worktree_head_sha"], newer_head)
        self.assertTrue(result["local_skill_files_verified"])
        self.assertFalse(result["worker_session_observed"])

    def test_wrong_linked_git_head_fails_before_skill_check(self):
        self.bindings[0]["session"]["head_sha"] = "e" * 40
        with self.assertRaisesRegex(ProfileError, "worktree_head_changed"):
            observe_local_skill_view(self.p[0], self.bindings[0])

if __name__ == "__main__":
    unittest.main()
