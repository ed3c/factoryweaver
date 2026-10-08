#!/usr/bin/env python3
"""Read-only, content-bound incremental card patches for FactoryWeaver records.

This is a reference knowledge compiler, not an evidence owner, test runner,
provider adapter, independent source verifier, or PR execution authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from factoryweaver import ContractError, load, verify


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def fingerprint(before, after):
    return hashlib.sha256(canonical([before, after]).encode("utf-8")).hexdigest()


def index(items, key):
    return {item[key]: item for item in items}


def compile_delta(before, after, *, batch_size=12, cursor=None):
    verify(before)
    verify(after)
    if before["schema_version"] != after["schema_version"] or before["subject"] != after["subject"]:
        raise ContractError("subject_or_protocol_changed")
    if type(batch_size) is not int or not 1 <= batch_size <= 12:
        raise ContractError("batch_size_out_of_range")
    old_cards = index(before["cards"], "canonical_key")
    new_cards = index(after["cards"], "canonical_key")
    if set(old_cards) - set(new_cards):
        raise ContractError("card_history_removed")
    old_id_map = index(before["cards"], "stable_id")
    new_id_map = index(after["cards"], "stable_id")
    changes = []
    for card in after["cards"]:
        previous = old_cards.get(card["canonical_key"])
        if previous is None:
            if card["stable_id"] in old_id_map:
                raise ContractError("stable_id_reused:" + card["stable_id"])
            if card["revision"] != 1:
                raise ContractError("new_card_revision_must_be_one:" + card["stable_id"])
            changes.append({"operation": "CREATE", "card": card})
            continue
        if card["stable_id"] != previous["stable_id"]:
            raise ContractError("stable_id_changed:" + card["canonical_key"])
        old_payload = {k: v for k, v in previous.items() if k != "revision"}
        new_payload = {k: v for k, v in card.items() if k != "revision"}
        if old_payload == new_payload:
            if card["revision"] != previous["revision"]:
                raise ContractError("spurious_revision:" + card["stable_id"])
        else:
            if card["revision"] != previous["revision"] + 1:
                raise ContractError("revision_not_incremented:" + card["stable_id"])
            changes.append({"operation": "UPDATE", "previous_revision": previous["revision"], "card": card})
    # No silent deletion or rewriting of an old canonical key: supersession
    # retains the old card as SUPERSEDED and adds a linked new canonical key.
    for card in after["cards"]:
        for link in card["typed_links"]:
            if link["relation"] != "supersedes":
                continue
            prior = old_id_map.get(link["target"])
            if prior is None or prior["stable_id"] == card["stable_id"]:
                raise ContractError("unbound_supersedes:" + card["stable_id"])
            retained = new_id_map[prior["stable_id"]]
            if retained["status"] != "SUPERSEDED" or card["status"] != "ACTIVE":
                raise ContractError("supersession_history_not_closed:" + card["stable_id"])

    old_sources = index(before["sources"], "source_id")
    new_sources = index(after["sources"], "source_id")
    changed_sources = sorted(k for k in old_sources.keys() | new_sources.keys()
                             if old_sources.get(k) != new_sources.get(k))
    old_req = index(before["requirements"], "id")
    new_req = index(after["requirements"], "id")
    if set(old_req) - set(new_req):
        raise ContractError("requirement_history_removed")
    # The compiler can identify changed metadata, not certify remote bytes.
    changed_requirements = set(
        key for key, req in new_req.items()
        if old_req.get(key) != req
    )
    affected = set(changed_requirements)
    for req in after["requirements"]:
        if set(req["source_ids"]) & set(changed_sources):
            affected.add(req["id"])
    changed_card_ids = {change["card"]["stable_id"] for change in changes}
    affected |= changed_card_ids
    for card in after["cards"]:
        if set(card["evidence_ids"]) & set(changed_sources):
            affected.add(card["stable_id"])
    # Propagate only through actual typed dependency edges; no full global
    # invalidation and no claim that independent owner receipts are stale.
    changed = True
    while changed:
        old_affected = set(affected)
        for req in after["requirements"]:
            if set(req.get("depends_on", [])) & affected:
                affected.add(req["id"])
        for card in after["cards"]:
            if {edge["target"] for edge in card["typed_links"]} & affected:
                affected.add(card["stable_id"])
        changed = old_affected != affected

    stamp = fingerprint(before, after)
    offset = 0
    if cursor is not None:
        match = re.fullmatch(r"([0-9a-f]{64}):([0-9]+)", cursor)
        if match is None or match.group(1) != stamp:
            raise ContractError("stale_or_malformed_cursor")
        offset = int(match.group(2))
        if str(offset) != match.group(2) or offset > len(changes) or offset % batch_size != 0:
            raise ContractError("invalid_cursor_offset")
        if offset and offset == len(changes):
            raise ContractError("cursor_after_terminal_batch")
    selected = changes[offset:offset + batch_size]
    next_offset = offset + len(selected)
    next_cursor = f"{stamp}:{next_offset}" if next_offset < len(changes) else None
    noop = before == after
    # A modified source record is merely metadata; this compiler cannot
    # independently verify its real bytes or clear downstream test receipts.
    remaining_work = []
    if changed_sources:
        remaining_work.append("original_source_owner_readback_required")
    if not changes and not noop and not changed_sources:
        remaining_work.append("noncard_change_requires_reconciliation")
    status = ("NOOP" if noop else "CONTINUE" if next_cursor else
              "BLOCKED" if remaining_work else "DONE")
    return {
        "protocol": "factoryweaver/card-delta-v1",
        "subject": after["subject"]["id"],
        "status": status,
        "remaining_work": remaining_work,
        "patch": selected,
        "next_cursor": next_cursor,
        "source_metadata_changed": changed_sources,
        "affected_nodes": sorted(affected),
        "change_count": len(changes),
        "unmapped_changes": [] if noop or changes or affected else ["noncard_record_change"],
        "proof_ceiling": "SCHEMA_FIXTURE_ONLY",
        "source_integrity_proven": False,
        "effect_authority": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Pure FactoryWeaver card patch compiler")
    parser.add_argument("before")
    parser.add_argument("after")
    parser.add_argument("--batch-size", type=int, default=12)
    parser.add_argument("--cursor")
    args = parser.parse_args(argv)
    try:
        result = compile_delta(load(args.before), load(args.after),
                               batch_size=args.batch_size, cursor=args.cursor)
        print(canonical(result))
        return 0
    except (OSError, ValueError) as error:
        print(canonical({"valid": False, "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
