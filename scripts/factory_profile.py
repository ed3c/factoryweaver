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
    parser.add_argument("command", choices=("validate", "bind-check", "compare"))
    parser.add_argument("files", nargs="+")
    args = parser.parse_args(argv)
    expected = {"validate": 1, "bind-check": 2, "compare": 4}[args.command]
    if len(args.files) != expected:
        parser.error(args.command + " requires " + str(expected) + " file(s)")
    try:
        records = [load(path) for path in args.files]
        output = {"validate": lambda: validate_profile(records[0]),
                  "bind-check": lambda: validate_binding(*records),
                  "compare": lambda: compare(*records)}[args.command]()
        print(json.dumps(output, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, ValidationError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
