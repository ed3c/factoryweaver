#!/usr/bin/env python3
"""Build self-contained read-only Agent Skill from canonical FactoryWeaver sources."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "LICENSE": "LICENSE",
    "scripts/factoryweaver.py": "scripts/factoryweaver.py",
    "scripts/card_semantic.py": "scripts/card_semantic.py",
    "scripts/card_delta.py": "scripts/card_delta.py",
    "scripts/soodles_handoff.py": "scripts/soodles_handoff.py",
    "scripts/check_bundle.py": "scripts/check_bundle.py",
    "contracts/v1/knowledge-record.schema.json": "contracts/v1/knowledge-record.schema.json",
    "contracts/v1/adapter-registry.schema.json": "contracts/v1/adapter-registry.schema.json",
    "references/zettelkasten-v7.2.md": "references/zettelkasten-v7.2.md",
    "references/card-classification-and-scope-assembly.md": "references/card-classification-and-scope-assembly.md",
    "references/prompt-carrier-and-ownership.md": "references/prompt-carrier-and-ownership.md",
    "references/card-prompts/registry.json": "references/card-prompts/registry.json",
    "references/compatibility.md": "docs/compatibility.md",
    "references/bootstrap-boundary.md": "docs/bootstrap-boundary.md",
    "references/soodles-scope-routing.md": "docs/soodles-scope-routing.md",
    "references/soodles-manager-consumption.md": "docs/soodles-manager-consumption.md",
    "examples/matt-grilling/project.json": "examples/matt-grilling/project.json",
    "examples/openai-plugin-platform/project.json": "examples/openai-plugin-platform/project.json",
    "examples/host-registry.example.json": "examples/host-registry.example.json",
}
FILES.update({f"references/card-prompts/types/{kind}.md": f"references/card-prompts/types/{kind}.md"
              for kind in ("N", "Q", "C", "D", "S", "P", "T", "R", "G", "E", "V", "X", "K", "REQ", "SPEC")})

class BundleError(ValueError):
    pass

def read_source(path):
    p = ROOT / path
    if not p.is_file() or p.is_symlink():
        raise BundleError("missing_or_symlink_source:" + path)
    return p.read_bytes()

def body_of_skill(path):
    text = read_source(path).decode("utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0] != "":
        raise BundleError("invalid_skill_frontmatter:" + path)
    return parts[2].lstrip("\r\n")

def generate():
    files = {target: read_source(source) for target, source in FILES.items()}
    files["skills/factoryweaver/SKILL.md"] = read_source("skills/factoryweaver/SKILL.md")
    files["skills/factoryweaver-compile/SKILL.md"] = read_source("skills/factoryweaver-compile/SKILL.md")
    files["skills/factoryweaver-verify/SKILL.md"] = read_source("skills/factoryweaver-verify/SKILL.md")
    # Preserve canonical relative references under a portable virtual repository root.
    # Installers must use this directory as the repository root, not copy SKILL.md alone.
    for name, raw in files.items():
        if Path(name).is_absolute() or ".." in Path(name).parts:
            raise BundleError("unsafe_generated_path:" + name)
    rows = [{"path": p, "sha256": hashlib.sha256(content).hexdigest()}
            for p, content in sorted(files.items())]
    files["bundle-manifest.json"] = (
        json.dumps({"protocol": "factoryweaver/portable-bundle-v1",
                    "scope": "read-only-reference", "effect_authority": False,
                    "files": rows}, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return files

def build(destination):
    destination = destination.resolve()
    if destination in (ROOT, ROOT / "skills", ROOT / "contracts"):
        raise BundleError("cannot_overwrite_canonical_sources")
    files = generate()
    if destination.exists():
        if not destination.is_dir() or destination.is_symlink():
            raise BundleError("existing_destination_not_directory")
        existing = {p.relative_to(destination).as_posix(): p for p in destination.rglob("*")
                    if p.is_file() or p.is_symlink()}
        if set(existing) != set(files):
            raise BundleError("existing_bundle_file_set_changed")
        if any(path.is_symlink() or path.read_bytes() != files[name]
               for name, path in existing.items()):
            raise BundleError("existing_bundle_content_drift")
        status = "NOOP"
    else:
        destination.mkdir(parents=True, exist_ok=False)
        for name, data in files.items():
            output = destination / name
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
        status = "CREATED"
    return {"status": status, "files": len(files),
            "manifest_sha256": hashlib.sha256(files["bundle-manifest.json"]).hexdigest(),
            "effect_authority": False}

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("destination")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(build(Path(args.destination)), sort_keys=True))
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps({"valid": False, "error": str(error)}, sort_keys=True), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
