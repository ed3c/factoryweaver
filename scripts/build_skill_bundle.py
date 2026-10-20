#!/usr/bin/env python3
"""Build self-contained read-only Agent Skill from canonical FactoryWeaver sources."""
from __future__ import annotations
import argparse
import hashlib
import json
import posixpath
import re
from urllib.parse import unquote, urlsplit
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "LICENSE": "LICENSE",
    "scripts/build_skill_bundle.py": "scripts/build_skill_bundle.py",
    "scripts/verify_installed_skill.py": "scripts/verify_installed_skill.py",
    ".cursor/skills/verify-factoryweaver/scripts/verify.py": ".cursor/skills/verify-factoryweaver/scripts/verify.py",
    ".cursor/pstack-LICENSE": ".cursor/pstack-LICENSE",
    "scripts/factoryweaver.py": "scripts/factoryweaver.py",
    "scripts/record_prepare.py": "scripts/record_prepare.py",
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
    "docs/compatibility.md": "docs/compatibility.md",
    "docs/record-preparation.md": "docs/record-preparation.md",
    "docs/bootstrap-boundary.md": "docs/bootstrap-boundary.md",
    "docs/soodles-scope-routing.md": "docs/soodles-scope-routing.md",
    "docs/soodles-manager-consumption.md": "docs/soodles-manager-consumption.md",
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
    if not p.is_file() or any(q.is_symlink() for q in (p, *p.parents) if q != ROOT and ROOT in q.parents):
        raise BundleError("missing_or_symlink_source:" + path)
    return p.read_bytes()

def local_links(path, raw):
    if not path.endswith(".md"):
        return []
    links = re.findall(r"^- Source: (\S+)$", raw.decode("utf-8"), re.MULTILINE)
    for href in re.findall(r"\[[^\]]*\]\(([^)]+)\)", raw.decode("utf-8")):
        uri = urlsplit(href)
        if uri.scheme or uri.netloc or not uri.path:
            continue
        target = posixpath.normpath(posixpath.join(posixpath.dirname(path), unquote(uri.path)))
        if target.startswith("../") or target.startswith("/"):
            raise BundleError("reference_outside_bundle:" + path + ":" + href)
        links.append(target)
    return links

def generate():
    files = {target: read_source(source) for target, source in FILES.items()}
    files["skills/factoryweaver/SKILL.md"] = read_source("skills/factoryweaver/SKILL.md")
    files["skills/factoryweaver-compile/SKILL.md"] = read_source("skills/factoryweaver-compile/SKILL.md")
    files["skills/factoryweaver-verify/SKILL.md"] = read_source("skills/factoryweaver-verify/SKILL.md")
    entry = files["skills/factoryweaver/SKILL.md"].decode("utf-8")
    header = entry.split("---", 2)[1]
    files["SKILL.md"] = ("---" + header + "---\n# FactoryWeaver portable entry\n\n"
        "Read [the canonical v7.2 entry](skills/factoryweaver/SKILL.md) before compiling or verifying.\n"
        "Keep this whole directory. The canonical entry owns prompt selection and proof boundaries.\n").encode("utf-8")
    pending = list(files)
    while pending:
        name = pending.pop()
        for target in local_links(name, files[name]):
            if target not in files:
                source = ROOT / target
                if source.is_dir() and not source.is_symlink():
                    targets = sorted(p.relative_to(ROOT).as_posix() for p in source.rglob("*")
                                     if p.is_file() or p.is_symlink())
                else:
                    targets = [target]
                for dependency in targets:
                    if dependency not in files:
                        files[dependency] = read_source(dependency)
                        pending.append(dependency)
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
    if destination.is_symlink():
        raise BundleError("symlink_destination")
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
