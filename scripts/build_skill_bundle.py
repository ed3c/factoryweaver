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
    "contracts/v1/knowledge-record.schema.json": "contracts/v1/knowledge-record.schema.json",
    "contracts/v1/adapter-registry.schema.json": "contracts/v1/adapter-registry.schema.json",
    "references/zettelkasten-v7.2.md": "references/zettelkasten-v7.2.md",
    "references/compatibility.md": "docs/compatibility.md",
    "references/bootstrap-boundary.md": "docs/bootstrap-boundary.md",
    "examples/matt-grilling/project.json": "examples/matt-grilling/project.json",
    "examples/openai-plugin-platform/project.json": "examples/openai-plugin-platform/project.json",
    "examples/host-registry.example.json": "examples/host-registry.example.json",
}

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
    source_entry = read_source("skills/factoryweaver/SKILL.md").decode("utf-8")
    marker = chr(96)
    replacements = {
        "../../docs/compatibility.md": "references/compatibility.md",
        "use " + marker + "factoryweaver-compile" + marker: "read " + marker + "references/compiler.md" + marker,
        "use " + marker + "factoryweaver-verify" + marker: "read " + marker + "references/verifier.md" + marker,
    }
    for before, after in replacements.items():
        if before not in source_entry:
            raise BundleError("entry_seam_changed:" + before)
        source_entry = source_entry.replace(before, after)
    files["SKILL.md"] = source_entry.encode()
    mappings = {
        "../../references/zettelkasten-v7.2.md": "references/zettelkasten-v7.2.md",
        "../../contracts/v1/knowledge-record.schema.json": "contracts/v1/knowledge-record.schema.json",
    }
    for name, path in (("compiler", "skills/factoryweaver-compile/SKILL.md"),
                       ("verifier", "skills/factoryweaver-verify/SKILL.md")):
        text = body_of_skill(path)
        for before, after in mappings.items():
            text = text.replace(before, after)
        files["references/" + name + ".md"] = text.encode()
    for path, raw in files.items():
        if Path(path).is_absolute() or ".." in Path(path).parts:
            raise BundleError("unsafe_generated_path:" + path)
        if path.endswith(".md") and b"../../" in raw:
            raise BundleError("unbundled_parent_reference:" + path)
    rows = [{"path": p, "sha256": hashlib.sha256(content).hexdigest()}
            for p, content in sorted(files.items())]
    files["bundle-manifest.json"] = (
        json.dumps({"protocol": "factoryweaver/portable-bundle-v1",
                    "scope": "read-only-reference",
                    "effect_authority": False, "files": rows},
                   sort_keys=True, separators=(",", ":")) + "\n").encode()
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
