#!/usr/bin/env python3
"""Inspect a real, externally installed FactoryWeaver Skill directory."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path


def inspect(root: Path):
    if root.is_symlink():
        raise ValueError("symlink_install_root")
    root = root.resolve()
    candidates = sorted(p.parent for p in root.rglob("SKILL.md")
                        if p.parent.name == "factoryweaver" and p.parent.parent.name == "skills"
                        and p.is_file() and p.read_text(encoding="utf-8").startswith(
                            "---\nname: factoryweaver\n"))
    candidates = [p for p in candidates if not any(p in other.parents for other in candidates if p != other)]
    if len(candidates) != 1:
        raise ValueError("factoryweaver_install_not_uniquely_found:" + str(len(candidates)))
    directory = candidates[0].parents[1]
    if candidates[0].relative_to(directory).as_posix() != "skills/factoryweaver":
        raise ValueError("partial_install_missing_virtual_root")
    script = directory / "scripts/factoryweaver.py"
    example = directory / "examples/matt-grilling/project.json"
    manifest = directory / "bundle-manifest.json"
    checker = directory / "scripts/check_bundle.py"
    if not all(p.is_file() for p in (script, example, manifest, checker)):
        raise ValueError("partial_install_missing_cli_or_contract")
    for command in ([sys.executable, str(checker), str(directory)],
                    [sys.executable, str(script), "project", str(example)]):
        result = subprocess.run(command, cwd=root, capture_output=True, text=True)
        if result.returncode:
            raise ValueError("installed_skill_command_failed:" + result.stderr)
        data = json.loads(result.stdout)
        if "projection" in data:
            if data["projection"][0]["state"] != "WAIT_FOR_HUMAN":
                raise ValueError("installed_skill_bypassed_grilling_human")
        elif data.get("status") != "SELF_CONSISTENT":
            raise ValueError("installed_bundle_inconsistent")
    return {"status": "INSTALLED_SKILL_REFERENCE_CLI_PASS",
            "installed_layout_observed": True, "installer_behavior_observed": False, "actual_agent_invocation": False,
            "external_owner_authenticated": False, "effect_authority": False}


if __name__ == "__main__":
    try:
        print(json.dumps(inspect(Path(sys.argv[1])), sort_keys=True))
    except (IndexError, ValueError, OSError) as error:
        print(json.dumps({"valid": False, "error": str(error)}), file=sys.stderr)
        raise SystemExit(2)
