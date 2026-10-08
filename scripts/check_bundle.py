#!/usr/bin/env python3
"""Offline integrity check for a generated FactoryWeaver bundle.

Self-consistency only. A manifest included in an untrusted bundle cannot
authenticate its publisher, GitHub commit or installer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


class BundleInvalid(ValueError):
    pass


def inspect(root: Path) -> dict:
    root = root.resolve()
    manifest_path = root / "bundle-manifest.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise BundleInvalid("manifest_missing_or_symlink")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or set(manifest) != {
        "protocol", "scope", "effect_authority", "files"
    } or manifest["protocol"] != "factoryweaver/portable-bundle-v1" or manifest["effect_authority"] is not False:
        raise BundleInvalid("manifest_contract")
    entries = manifest["files"]
    if not isinstance(entries, list) or not entries:
        raise BundleInvalid("manifest_file_inventory_empty")
    expected = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256"}:
            raise BundleInvalid("manifest_entry_shape")
        rel, digest = entry["path"], entry["sha256"]
        if (not isinstance(rel, str) or not rel or rel.startswith("/") or
            "\\" in rel or ".." in Path(rel).parts or
            not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)):
            raise BundleInvalid("manifest_entry_invalid")
        if rel in expected or rel == "bundle-manifest.json":
            raise BundleInvalid("manifest_duplicate_path")
        expected.add(rel)
        target = root / rel
        if not target.is_file() or target.is_symlink():
            raise BundleInvalid("missing_or_symlink_file:" + rel)
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise BundleInvalid("content_digest_mismatch:" + rel)
    observed = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*") if p.is_file() or p.is_symlink()
    }
    if observed != expected | {"bundle-manifest.json"}:
        raise BundleInvalid("untracked_or_missing_bundle_file")
    return {
        "status": "SELF_CONSISTENT",
        "checked_files": len(entries),
        "external_publisher_authenticated": False,
        "source_commit_authenticated": False,
        "effect_authority": False
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle_dir", type=Path)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(inspect(args.bundle_dir), sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError) as e:
        print(json.dumps({"valid": False, "error": str(e)}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
