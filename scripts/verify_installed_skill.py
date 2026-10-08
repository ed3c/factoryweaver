#!/usr/bin/env python3
"""Inspect a real, externally installed FactoryWeaver Skill directory."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path


def inspect(root: Path):
    candidates = sorted(p.parent for p in root.rglob("SKILL.md")
                        if p.is_file() and p.read_text(encoding="utf-8").startswith(
                            "---\nname: factoryweaver\n"))
    if len(candidates) != 1:
        raise ValueError("factoryweaver_install_not_uniquely_found:" + str(len(candidates)))
    directory = candidates[0]
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
            "installer_behavior_observed": True, "actual_agent_invocation": False,
            "external_owner_authenticated": False, "effect_authority": False}


if __name__ == "__main__":
    try:
        print(json.dumps(inspect(Path(sys.argv[1]).resolve()), sort_keys=True))
    except (IndexError, ValueError, OSError) as error:
        print(json.dumps({"valid": False, "error": str(error)}), file=sys.stderr)
        raise SystemExit(2)
