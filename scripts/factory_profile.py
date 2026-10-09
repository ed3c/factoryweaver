#!/usr/bin/env python3
"""FactoryWeaver read-only Profile/Binding contracts.

This validates *untrusted declared metadata*. It neither installs Skills nor
observes a real Noodle session, isolates processes, authorizes effects, or
launches another software factory workflow.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
PROFILE_SCHEMA = ROOT / "contracts/v1/factory-profile.schema.json"
BINDING_SCHEMA = ROOT / "contracts/v1/factory-binding.schema.json"

ESSENTIAL = {
    "isolated_git_worktree", "skill_discovery",
    "session_readback", "source_pinning"
}

class ProfileError(ValueError):
    pass

def load(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")

def profile_digest(profile):
    return hashlib.sha256(canonical(profile)).hexdigest()

def validate_profile(profile):
    Draft202012Validator(load(PROFILE_SCHEMA)).validate(profile)
    names = [skill["name"] for skill in profile["skills"]]
    if len(names) != len(set(names)):
        raise ProfileError("duplicate_skill_name")
    roots = [skill["name"] for skill in profile["skills"]
             if skill["role"] == "workflow_entry"]
    if roots != [profile["workflow_entry"]]:
        raise ProfileError("single_workflow_entry_required")
    sources = [(s["repository"], s["subpath"]) for s in profile["skills"]]
    if len(sources) != len(set(sources)):
        raise ProfileError("duplicate_skill_source")
    for skill in profile["skills"]:
        subpath = skill["subpath"]
        if (subpath.startswith("/") or ".." in subpath.split("/") or
            "//" in subpath or "\\" in subpath):
            raise ProfileError("unsafe_source_subpath:" + skill["name"])
    if not ESSENTIAL.issubset(profile["carrier_capabilities"]):
        raise ProfileError("carrier_minimum_capabilities_missing")
    return {"status": "PROFILE_SHAPE_VALID",
            "profile_id": profile["profile_id"],
            "profile_sha256": profile_digest(profile),
            "skills": names,
            "effect_authority": False,
            "proof_ceiling": "DECLARED_PROFILE_CONTRACT_ONLY"}

def checked_path(value):
    if (not value.startswith("/") or value == "/" or
        ".." in value.split("/") or "\\" in value or "//" in value):
        raise ProfileError("unsafe_declared_worktree_path")
    return posixpath.normpath(value)

def validate_binding(profile, binding):
    info = validate_profile(profile)
    Draft202012Validator(load(BINDING_SCHEMA)).validate(binding)
    if binding["profile_sha256"] != info["profile_sha256"] or (
        binding["session"]["profile_sha256"] != info["profile_sha256"]
    ):
        raise ProfileError("profile_sha256_mismatch")
    if binding["session"]["repository"] != binding["work_order"]["repository"]:
        raise ProfileError("worktree_repository_mismatch")
    if binding["session"]["entry_skill"] != profile["workflow_entry"]:
        raise ProfileError("workflow_entry_mismatch")
    missing = set(profile["carrier_capabilities"]) - set(binding["carrier"]["capabilities"])
    if missing:
        raise ProfileError("carrier_capabilities_missing:" + ",".join(sorted(missing)))
    declared_skills = {s["name"]: s["tree_sha256"] for s in profile["skills"]}
    observed_view = {}
    for item in binding["session"]["skill_view"]:
        if item["name"] in observed_view:
            raise ProfileError("duplicate_discovered_skill")
        observed_view[item["name"]] = item["tree_sha256"]
    unexpected = sorted(set(observed_view) - set(declared_skills))
    if unexpected:
        raise ProfileError("undeclared_inherited_skill:" + ",".join(unexpected))
    absent = sorted(set(declared_skills) - set(observed_view))
    if absent:
        raise ProfileError("missing_declared_skill:" + ",".join(absent))
    mismatch = sorted(name for name in declared_skills
                      if declared_skills[name] != observed_view[name])
    if mismatch:
        raise ProfileError("skill_digest_mismatch:" + ",".join(mismatch))
    checked_path(binding["session"]["worktree_path"])
    return {"status": "ADVISORY_MATCH_ONLY",
            "profile_id": profile["profile_id"],
            "profile_sha256": info["profile_sha256"],
            "work_order": binding["work_order"]["id"],
            "carrier_id": binding["carrier"]["id"],
            "declared_worktree_id": binding["session"]["worktree_id"],
            "declared_session_id": binding["session"]["id"],
            "unlisted_skill_count": 0,
            "physical_worktree_verified": False,
            "process_and_secret_isolation_verified": False,
            "original_owner_readback_verified": False,
            "effect_authority": False,
            "proof_ceiling": "DECLARED_PROFILE_CONTRACT_ONLY"}

def observe_git_worktree(profile, binding):
    """Corroborate a supplied Git checkout with real local read-only commands.

    No information from this operation authenticates Noodle worker identity,
    installed Skills, secrets, provider permission or host admission.
    """
    validate_binding(profile, binding)
    session = binding["session"]
    expected_head = session.get("head_sha")
    if not expected_head:
        raise ProfileError("worktree_head_pin_required")
    root = Path(checked_path(session["worktree_path"]))
    if not root.is_dir() or root.is_symlink() or root.resolve() != root:
        raise ProfileError("worktree_path_missing_or_symlink")
    # A separate linked Git worktree has a .git *file*, unlike main checkout.
    if not (root / ".git").is_file() or (root / ".git").is_symlink():
        raise ProfileError("linked_worktree_gitfile_required")
    def git(*arguments):
        try:
            result = subprocess.run(
                ["git", "-C", str(root), *arguments],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=10, check=False)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise ProfileError("git_observation_unavailable") from error
        if result.returncode != 0:
            raise ProfileError("git_readback_failed:" + " ".join(arguments))
        return result.stdout.strip()
    if Path(git("rev-parse", "--show-toplevel")).resolve() != root:
        raise ProfileError("worktree_root_mismatch")
    actual_head = git("rev-parse", "HEAD")
    if actual_head != expected_head:
        raise ProfileError("worktree_head_changed")
    # Candidate HEAD may advance beyond the admitted base. It may NOT come
    # from an unrelated branch or an object absent from this Git repository.
    base = binding["work_order"]["base_sha"]
    if subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", base, actual_head],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10,
        check=False
    ).returncode != 0:
        raise ProfileError("work_order_base_not_ancestor")
    git_dir = Path(git("rev-parse", "--absolute-git-dir")).resolve()
    common = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir")).resolve()
    if git_dir == common:
        raise ProfileError("independent_linked_worktree_required")
    rows = git("worktree", "list", "--porcelain").splitlines()
    actual_roots = [line[9:] for line in rows if line.startswith("worktree ")]
    if str(root) not in actual_roots:
        raise ProfileError("worktree_not_registered")
    return {"status": "LOCAL_GIT_WORKTREE_OBSERVED",
            "observed_head_sha": actual_head,
            "worktree_path": str(root),
            "physical_git_checkout_observed": True,
            "worker_session_observed": False,
            "skill_view_physically_observed": False,
            "process_and_secret_isolation_verified": False,
            "original_owner_readback_verified": False,
            "effect_authority": False}



def skill_tree_sha256(directory):
    """Canonical sorted file manifest digest; no installer or model interaction."""
    if not directory.is_dir() or directory.is_symlink():
        raise ProfileError("local_skill_not_directory")
    manifest = []
    for p in sorted(directory.rglob("*")):
        if p.is_symlink():
            raise ProfileError("symlink_in_skill_tree")
        if p.is_dir():
            continue
        if not p.is_file() or p.stat().st_size > 2_000_000:
            raise ProfileError("unsupported_local_skill_file")
        manifest.append([p.relative_to(directory).as_posix(),
                         hashlib.sha256(p.read_bytes()).hexdigest()])
        if len(manifest) > 200:
            raise ProfileError("skill_tree_file_count_exceeded")
    if not manifest or not (directory / "SKILL.md").is_file():
        raise ProfileError("local_skill_entry_missing")
    return hashlib.sha256(canonical(manifest)).hexdigest()


def observe_local_skill_view(profile, binding):
    """Read only local worktree Skills; never claim the agent's effective catalog."""
    observed = observe_git_worktree(profile, binding)
    worktree = Path(observed["worktree_path"])
    agents_dir = worktree / ".agents"
    directory = agents_dir / "skills"
    if agents_dir.is_symlink() or directory.is_symlink():
        raise ProfileError("worktree_skill_parent_symlink")
    if not directory.is_dir() or directory.resolve() != directory:
        raise ProfileError("worktree_skill_directory_missing")
    candidates = sorted(directory.iterdir())
    if any(p.is_symlink() or not p.is_dir() for p in candidates):
        raise ProfileError("unexpected_worktree_skill_surface")
    actual = {p.name: skill_tree_sha256(p) for p in candidates}
    pinned = {s["name"]: s["tree_sha256"] for s in profile["skills"]}
    unlisted = sorted(set(actual) - set(pinned))
    missing = sorted(set(pinned) - set(actual))
    if unlisted:
        raise ProfileError("unlisted_worktree_skill:" + ",".join(unlisted))
    if missing:
        raise ProfileError("missing_worktree_skill:" + ",".join(missing))
    drifted = sorted(name for name in pinned if actual[name] != pinned[name])
    if drifted:
        raise ProfileError("worktree_skill_content_drift:" + ",".join(drifted))
    return {"status": "LOCAL_WORKTREE_SKILL_FILES_MATCH",
            "observed_worktree_head_sha": observed["observed_head_sha"],
            "local_skill_names": sorted(actual),
            "local_skill_files_verified": True,
            "agent_effective_skill_catalog_verified": False,
            "global_skill_inheritance_excluded": False,
            "worker_session_observed": False,
            "original_owner_readback_verified": False,
            "effect_authority": False}


def audit_effective_catalog(profile, binding, catalog):
    """Compare a carrier-supplied catalog claim, never trust its source."""
    validate_binding(profile, binding)
    required = {
        "protocol", "producer_claim", "profile_sha256", "work_order_id",
        "carrier_id", "session_id", "worktree_id", "entry_skill", "skills"
    }
    if not isinstance(catalog, dict) or set(catalog) != required:
        raise ProfileError("catalog_shape")
    if (catalog["protocol"] != "factoryweaver/effective-skill-catalog-v1" or
        catalog["producer_claim"] != "UNVERIFIED_CARRIER_OUTPUT"):
        raise ProfileError("catalog_producer_claim_invalid")
    session = binding["session"]
    matches = {
        "profile_sha256": profile_digest(profile),
        "work_order_id": binding["work_order"]["id"],
        "carrier_id": binding["carrier"]["id"],
        "session_id": session["id"],
        "worktree_id": session["worktree_id"],
        "entry_skill": profile["workflow_entry"],
    }
    for field, expected in matches.items():
        if catalog[field] != expected:
            raise ProfileError("catalog_identity_mismatch:" + field)
    skills = catalog["skills"]
    if not isinstance(skills, list) or not skills:
        raise ProfileError("catalog_skills_missing")
    actual = {}
    for item in skills:
        if not isinstance(item, dict) or set(item) != {"name", "tree_sha256", "scope"}:
            raise ProfileError("catalog_entry_shape")
        name = item["name"]
        if not isinstance(name, str) or name in actual:
            raise ProfileError("catalog_duplicate_skill")
        if item["scope"] not in ("worktree", "global", "user", "system"):
            raise ProfileError("catalog_scope_unknown")
        if not isinstance(item["tree_sha256"], str) or len(item["tree_sha256"]) != 64 or any(
            letter not in "0123456789abcdef" for letter in item["tree_sha256"]
        ):
            raise ProfileError("catalog_digest_invalid")
        actual[name] = item
    pinned = {s["name"]: s["tree_sha256"] for s in profile["skills"]}
    extras = sorted(set(actual) - set(pinned))
    if extras:
        raise ProfileError("catalog_unlisted_skill:" + ",".join(extras))
    missing = sorted(set(pinned) - set(actual))
    if missing:
        raise ProfileError("catalog_missing_skill:" + ",".join(missing))
    inherited = sorted(name for name in pinned if actual[name]["scope"] != "worktree")
    if inherited:
        raise ProfileError("catalog_nonworktree_inheritance:" + ",".join(inherited))
    drift = sorted(name for name in pinned if actual[name]["tree_sha256"] != pinned[name])
    if drift:
        raise ProfileError("catalog_skill_digest_drift:" + ",".join(drift))
    return {
        "status": "EFFECTIVE_CATALOG_CLAIM_MATCHES",
        "profile_sha256": matches["profile_sha256"],
        "declared_skill_count": len(pinned),
        "original_owner_capture_verified": False,
        "actual_worker_skill_discovery_verified": False,
        "global_skill_exclusion_verified": False,
        "effect_authority": False,
    }


def compare(profile_a, binding_a, profile_b, binding_b):
    a = validate_binding(profile_a, binding_a)
    b = validate_binding(profile_b, binding_b)
    one, two = binding_a["session"], binding_b["session"]
    if one["id"] == two["id"]:
        raise ProfileError("cross_profile_session_reused")
    if one["worktree_id"] == two["worktree_id"]:
        raise ProfileError("cross_profile_worktree_reused")
    p1 = checked_path(one["worktree_path"])
    p2 = checked_path(two["worktree_path"])
    if p1 == p2 or posixpath.commonpath((p1, p2)) in (p1, p2):
        raise ProfileError("overlapping_declared_worktree_path")
    return {"status": "DECLARED_WORKTREES_DISJOINT",
            "first_profile": a["profile_id"], "second_profile": b["profile_id"],
            "physical_isolation_verified": False,
            "original_owner_readback_verified": False,
            "effect_authority": False}

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("validate", "bind-check", "compare", "observe-worktree", "observe-local-skills", "audit-catalog"))
    parser.add_argument("files", nargs="+")
    args = parser.parse_args(argv)
    expected = {"validate": 1, "bind-check": 2, "compare": 4, "observe-worktree": 2, "observe-local-skills": 2, "audit-catalog": 3}[args.command]
    if len(args.files) != expected:
        parser.error(args.command + " requires " + str(expected) + " file(s)")
    try:
        records = [load(path) for path in args.files]
        output = {"validate": lambda: validate_profile(records[0]),
                  "bind-check": lambda: validate_binding(*records),
                  "compare": lambda: compare(*records),
                  "observe-worktree": lambda: observe_git_worktree(*records),
                  "observe-local-skills": lambda: observe_local_skill_view(*records),
                  "audit-catalog": lambda: audit_effective_catalog(*records)}[args.command]()
        print(json.dumps(output, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, ValidationError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
