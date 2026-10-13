#!/usr/bin/env python3
"""FactoryWeaver -> Soodles: read-only, lossless selected Scope export.

The bundle is a proposal containing the original full knowledge record.
Soodles independently checks transport shape and exact bytes; its original
Session/Issue owner alone reconciles provider readback and admission.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

from factoryweaver import verify, load, ContractError

PROTOCOL = "factoryweaver/soodles-scope/v1"
SELECTION_KEYS = (
    "requirement_ids", "card_ids", "goal", "measurement", "persistence",
    "stop_and_escalation", "causal_change", "acceptance", "constraints",
    "prompt_delta",
)


def _text(item):
    return isinstance(item, str) and bool(item.strip())


def _strings(items, *, nonempty=False):
    return isinstance(items, list) and (bool(items) or not nonempty) and all(
        _text(v) for v in items) and len(set(items)) == len(items)


def export(record, selection):
    """Produce immutable-file *content*, never an effect or authorization."""
    verify(record)  # Reuse the one original producer's v1 verification result.
    if not isinstance(selection, dict) or set(selection) != set(SELECTION_KEYS):
        raise ContractError("scope_selection_exact_fields_required")
    for key in ("requirement_ids", "card_ids"):
        if not _strings(selection[key], nonempty=True):
            raise ContractError("scope_selection_invalid:" + key)
    for key in ("goal", "measurement", "persistence", "stop_and_escalation", "causal_change"):
        if not _text(selection[key]):
            raise ContractError("scope_selection_invalid:" + key)
    for key in ("acceptance", "constraints", "prompt_delta"):
        if not _strings(selection[key], nonempty=key == "acceptance"):
            raise ContractError("scope_selection_invalid:" + key)

    requirements = {r["id"]: r for r in record["requirements"]}
    cards = {c["stable_id"]: c for c in record["cards"]}
    if set(selection["requirement_ids"]) - requirements.keys():
        raise ContractError("scope_selection_unknown_requirement")
    if set(selection["card_ids"]) - cards.keys():
        raise ContractError("scope_selection_unknown_card")
    selected_requirements = [requirements[key] for key in selection["requirement_ids"]]
    selected_cards = [cards[key] for key in selection["card_ids"]]
    if any(c["status"] != "ACTIVE" for c in selected_cards):
        raise ContractError("scope_selection_retired_or_superseded_card")
    # Preserve UNKNOWN and CONFLICTED requirements for source-resolution scopes.
    # The Soodles reader reports them as unresolved, never actionable admission.
    return {
        "protocol": PROTOCOL,
        "kind": "SOURCE_BOUND_PROPOSAL",
        "knowledge_record": record,
        "selection": selection,
    }


def bundle_bytes(bundle):
    """Canonical UTF-8 content for one Host-bound file; no model-derived fields."""
    return (json.dumps(bundle, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def materialize(record, selection, output):
    """Host-selected output path; exact bytes reused, unknown/drifted writes refuse."""
    bundle = export(record, selection)
    path = Path(output)
    if not path.is_absolute():
        raise ContractError("bundle_output_absolute_path_required")
    raw = bundle_bytes(bundle)
    expected = hashlib.sha256(raw).hexdigest()
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
    except FileExistsError:
        # A prior exact write is reusable; foreign bytes are never overwritten.
        if not stat.S_ISREG(path.lstat().st_mode) or path.read_bytes() != raw:
            raise ContractError("bundle_output_conflict_requires_original_readback")
    else:
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
        except BaseException:
            path.unlink(missing_ok=True)
            raise
    return {
        "status": "MATERIALIZED_PROPOSAL",
        "bundle": {"path": str(path), "sha256": expected},
        "reader_arguments": [str(path), expected],
        "effect_authority": False,
        "authorizes_landing": False,
    }

def main(argv=None):
    parser = argparse.ArgumentParser(description="Export a read-only Soodles scope proposal.")
    parser.add_argument("record", help="FactoryWeaver knowledge-record JSON, read-only")
    parser.add_argument("selection", help="Selected semantic scope, no physical metadata")
    parser.add_argument("--output", help="Original Host-selected absolute Bundle path; existing exact bytes are reused")
    args = parser.parse_args(argv)
    try:
        record, selection = load(args.record), load(args.selection)
        value = materialize(record, selection, args.output) if args.output else export(record, selection)
        print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"valid": False, "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
