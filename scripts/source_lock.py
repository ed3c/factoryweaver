#!/usr/bin/env python3
"""Verify supplied raw source bytes against a frozen GitHub blob and explicit anchors.

External source acquisition and trust in the asserted GitHub revision belong to
the original retrieval owner. This CLI never performs network requests or
issues any authorization/production attestation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from factoryweaver import ContractError


def git_blob_sha1(raw: bytes) -> str:
    header = b"blob " + str(len(raw)).encode("ascii") + b"\x00"
    return hashlib.sha1(header + raw).hexdigest()


def verify_source(manifest: dict, raw: bytes) -> dict:
    if not isinstance(manifest, dict) or set(manifest) != {
        "protocol", "repository", "revision", "path", "git_blob_sha1",
        "sha256", "source_dependency_key", "anchors",
    }:
        raise ContractError("source_manifest_shape")
    if manifest["protocol"] != "factoryweaver/source-lock-v1":
        raise ContractError("source_manifest_protocol")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", manifest["repository"]):
        raise ContractError("source_repository_identity")
    if not re.fullmatch(r"[0-9a-f]{40}", manifest["revision"]):
        raise ContractError("source_revision_unpinned")
    if not isinstance(manifest["path"], str) or not manifest["path"] or (
        manifest["path"].startswith("/") or ".." in manifest["path"].split("/")
    ):
        raise ContractError("source_path_invalid")
    if not isinstance(manifest["source_dependency_key"], str) or not manifest["source_dependency_key"].strip():
        raise ContractError("source_dependency_key_missing")
    if not re.fullmatch(r"[0-9a-f]{40}", manifest["git_blob_sha1"]) or (
        not re.fullmatch(r"[0-9a-f]{64}", manifest["sha256"])
    ):
        raise ContractError("source_digest_format")
    if git_blob_sha1(raw) != manifest["git_blob_sha1"]:
        raise ContractError("git_blob_sha1_mismatch")
    if hashlib.sha256(raw).hexdigest() != manifest["sha256"]:
        raise ContractError("source_sha256_mismatch")
    try:
        content = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ContractError("source_not_utf8") from exc
    anchors = manifest["anchors"]
    if not isinstance(anchors, list) or not anchors:
        raise ContractError("source_anchors_missing")
    seen = set()
    for anchor in anchors:
        if not isinstance(anchor, dict) or set(anchor) != {"id", "text_match"}:
            raise ContractError("source_anchor_shape")
        name, excerpt = anchor["id"], anchor["text_match"]
        if not isinstance(name, str) or not name or name in seen:
            raise ContractError("duplicate_source_anchor")
        if not isinstance(excerpt, str) or len(excerpt.strip()) < 8:
            raise ContractError("source_excerpt_missing")
        if content.count(excerpt) != 1:
            raise ContractError("missing_or_ambiguous_text_match:" + name)
        seen.add(name)
    return {
        "status": "SUPPLIED_BYTES_MATCH_FROZEN_MANIFEST",
        "repository": manifest["repository"],
        "revision": manifest["revision"],
        "path": manifest["path"],
        "anchors_verified": len(anchors),
        "source_dependency_key": manifest["source_dependency_key"],
        "content_sha256": manifest["sha256"],
        "external_origin_authenticated": False,
        "provider_readback_verified": False,
        "effect_authority": False,
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("manifest")
    p.add_argument("source_bytes")
    args = p.parse_args(argv)
    try:
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        result = verify_source(manifest, Path(args.source_bytes).read_bytes())
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
