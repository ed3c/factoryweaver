#!/usr/bin/env python3
"""FactoryWeaver -> Soodles: read-only, lossless selected Scope export.

The bundle is a proposal containing the original full knowledge record.
Soodles independently checks transport shape and exact bytes; its original
Session/Issue owner alone reconciles provider readback and admission.
"""
from __future__ import annotations

import argparse
import json
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
    if any(r["knowledge_status"] in ("UNKNOWN", "CONFLICTED") for r in selected_requirements):
        # Unknowns are valid *knowledge*, but cannot silently enter an atom as
        # verified requirements. Preserve them in the original full inventory.
        raise ContractError("scope_selection_unresolved_requirement")
    return {
        "protocol": PROTOCOL,
        "kind": "SOURCE_BOUND_PROPOSAL",
        "knowledge_record": record,
        "selection": selection,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Export a read-only Soodles scope proposal.")
    parser.add_argument("record", help="FactoryWeaver knowledge-record JSON, read-only")
    parser.add_argument("selection", help="Selected semantic scope, no physical metadata")
    args = parser.parse_args(argv)
    try:
        value = export(load(args.record), load(args.selection))
        print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"valid": False, "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
