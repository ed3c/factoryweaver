#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from jsonschema import ValidationError

from factoryweaver import ContractError, _unique_json_fields, verify

PROTOCOL = "factoryweaver/card-delta-v1"
PREREQUISITE_RELATIONS = frozenset({
    "depends_on", "based_on", "derived_from", "implements", "validated_by",
})
NONCARD_SECTIONS = ("sources", "decisions", "requirements", "action_requests", "progress")


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def fingerprint(before_bytes, after_bytes, batch_size, domain):
    identity = [PROTOCOL, domain, batch_size,
                hashlib.sha256(before_bytes).hexdigest(),
                hashlib.sha256(after_bytes).hexdigest()]
    return hashlib.sha256(canonical(identity).encode("utf-8")).hexdigest()


def index(items, key):
    return {item[key]: item for item in items}


def compile_delta(before, after, *, batch_size=12, cursor=None):
    return _compile_delta(before, after, canonical(before).encode("utf-8"),
                          canonical(after).encode("utf-8"), "canonical-objects",
                          batch_size, cursor)


def compile_delta_bytes(before_bytes, after_bytes, *, batch_size=12, cursor=None):
    before = json.loads(before_bytes.decode("utf-8"), object_pairs_hook=_unique_json_fields)
    after = json.loads(after_bytes.decode("utf-8"), object_pairs_hook=_unique_json_fields)
    return _compile_delta(before, after, before_bytes, after_bytes, "raw-bytes",
                          batch_size, cursor)


def affected_records(before, after, changes, changed_sources):
    graph = {}
    seeds = {("source", key) for key in changed_sources}
    seeds.update(("card", change["card"]["stable_id"]) for change in changes)
    for section, kind in (("requirements", "requirement"), ("decisions", "decision")):
        old = index(before.get(section, []), "id")
        new = index(after.get(section, []), "id")
        seeds.update((kind, key) for key in old.keys() | new.keys()
                     if old.get(key) != new.get(key))
    for record in (before, after):
        targets = {}
        for section, kind, key in (("requirements", "requirement", "id"),
                                   ("cards", "card", "stable_id"),
                                   ("decisions", "decision", "id")):
            for item in record.get(section, []):
                targets.setdefault(item[key], set()).add((kind, item[key]))
        for section, kind, key, source_field in (
                ("requirements", "requirement", "id", "source_ids"),
                ("cards", "card", "stable_id", "evidence_ids"),
                ("decisions", "decision", "id", "source_ids")):
            for item in record.get(section, []):
                dependent = (kind, item[key])
                prerequisites = {("source", ref) for ref in item[source_field]}
                refs = item.get("depends_on", []) if kind == "requirement" else []
                if kind == "card":
                    refs = [edge["target"] for edge in item["typed_links"]
                            if edge["relation"] in PREREQUISITE_RELATIONS]
                for ref in refs:
                    prerequisites.update(targets[ref])
                for prerequisite in prerequisites:
                    graph.setdefault(prerequisite, set()).add(dependent)
    pending = list(seeds)
    while pending:
        for dependent in graph.get(pending.pop(), ()):
            if dependent not in seeds:
                seeds.add(dependent)
                pending.append(dependent)
    return sorted(seeds)


def _compile_delta(before, after, before_bytes, after_bytes, domain, batch_size, cursor):
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
            changes.append({"operation": "UPDATE", "previous_revision": previous["revision"],
                            "previous_card": previous, "card": card})
    for card in after["cards"]:
        for link in card["typed_links"]:
            if link["relation"] != "supersedes":
                continue
            prior = old_id_map.get(link["target"])
            if prior is None or prior["stable_id"] == card["stable_id"]:
                raise ContractError("unbound_supersedes:" + card["stable_id"])
            retained = new_id_map[prior["stable_id"]]
            previous = old_id_map.get(card["stable_id"])
            is_new_link = previous is None or link not in previous["typed_links"]
            if retained["status"] != "SUPERSEDED" or (is_new_link and card["status"] != "ACTIVE"):
                raise ContractError("supersession_history_not_closed:" + card["stable_id"])

    old_sources = index(before["sources"], "source_id")
    new_sources = index(after["sources"], "source_id")
    changed_sources = sorted(k for k in old_sources.keys() | new_sources.keys()
                             if old_sources.get(k) != new_sources.get(k))
    if set(old_sources) - set(new_sources):
        raise ContractError("source_history_removed")
    changed_sections = [name for name in NONCARD_SECTIONS
                        if (name in before) != (name in after) or before.get(name) != after.get(name)]
    noncard_changes = {
        name: {"before_present": name in before, "after_present": name in after,
               "before": before.get(name), "after": after.get(name)}
        for name in changed_sections
    }
    old_req = index(before["requirements"], "id")
    new_req = index(after["requirements"], "id")
    if set(old_req) - set(new_req):
        raise ContractError("requirement_history_removed")
    affected = affected_records(before, after, changes, changed_sources)

    origin_groups = {}
    for source in after["sources"]:
        origin_groups.setdefault(source["source_dependency_key"], []).append(source["source_id"])
    grouped_sources = [{"source_dependency_key": key, "source_ids": sorted(ids)}
                       for key, ids in sorted(origin_groups.items())]

    stamp = fingerprint(before_bytes, after_bytes, batch_size, domain)
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
    remaining_work = []
    if changed_sources:
        remaining_work.append("original_source_owner_readback_required")
    if any(name != "sources" for name in changed_sections):
        remaining_work.append("noncard_change_requires_reconciliation")
    if not changes and not noop and not changed_sections:
        remaining_work.append("unmapped_change_requires_reconciliation")
    status = ("NOOP" if noop else "CONTINUE" if next_cursor else
              "BLOCKED" if remaining_work else "DONE")
    return {
        "protocol": PROTOCOL,
        "cursor_domain": domain,
        "subject": after["subject"]["id"],
        "status": status,
        "remaining_work": remaining_work,
        "patch": selected,
        "next_cursor": next_cursor,
        "source_metadata_changed": changed_sources,
        "noncard_sections_changed": changed_sections,
        "noncard_changes": noncard_changes,
        "card_order": [card["stable_id"] for card in after["cards"]],
        "origin_groups": grouped_sources,
        "source_independence_proven": False,
        "affected_nodes": sorted({key for kind, key in affected}),
        "affected_records": [{"kind": kind, "id": key} for kind, key in affected],
        "change_count": len(changes),
        "unmapped_changes": [name for name in changed_sections if name != "sources"]
                            + (["other_record_change"] if not noop and not changes and
                               not changed_sections else []),
        "proof_ceiling": "SCHEMA_FIXTURE_ONLY",
        "source_integrity_proven": False,
        "effect_authority": False,
        "effects": [],
        "authorizes_landing": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Pure FactoryWeaver card patch compiler")
    parser.add_argument("before")
    parser.add_argument("after")
    parser.add_argument("--batch-size", type=int, default=12)
    parser.add_argument("--cursor")
    args = parser.parse_args(argv)
    try:
        result = compile_delta_bytes(Path(args.before).read_bytes(), Path(args.after).read_bytes(),
                               batch_size=args.batch_size, cursor=args.cursor)
        print(canonical(result))
        return 0
    except (OSError, ValueError, ValidationError) as error:
        print(canonical({"valid": False, "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
