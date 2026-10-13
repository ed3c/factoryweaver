#!/usr/bin/env python3
"""Report explicitly declared source-clause to REQ/SPEC trace coverage.

Does not extract missing clauses, interpret job requirements, run a model,
authenticate an upstream document, or grant a host permission to execute.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

from factoryweaver import ContractError, load, verify

CLAUSE_KEYS = {"clause_id", "locator", "summary", "claim_kind", "requirement_ids"}
INVENTORY_KEYS = {"protocol", "subject_id", "source_id",
                  "source_dependency_key", "source_state", "clauses"}


def trace(record, inventory):
    verify(record)
    if not isinstance(inventory, dict) or set(inventory) != INVENTORY_KEYS:
        raise ContractError("coverage_inventory_shape")
    if inventory["protocol"] != "factoryweaver/requirement-coverage-v1":
        raise ContractError("coverage_protocol")
    if inventory["subject_id"] != record["subject"]["id"]:
        raise ContractError("coverage_subject_mismatch")
    sources = {s["source_id"]: s for s in record["sources"]}
    source = sources.get(inventory["source_id"])
    if source is None:
        raise ContractError("coverage_unknown_source")
    if inventory["source_dependency_key"] != source["source_dependency_key"]:
        raise ContractError("coverage_source_dependency_mismatch")
    if inventory["source_state"] not in ("UNPINNED", "PINNED_SHA256"):
        raise ContractError("coverage_source_state_invalid")
    if inventory["source_state"] != source.get("integrity", "UNPINNED"):
        raise ContractError("coverage_source_pin_mismatch")
    clauses = inventory["clauses"]
    if not isinstance(clauses, list) or not clauses:
        raise ContractError("coverage_clauses_missing")
    requirements = {r["id"]: r for r in record["requirements"]}
    cards = record["cards"]
    seen = set()
    rows = []
    for clause in clauses:
        if not isinstance(clause, dict) or set(clause) != CLAUSE_KEYS:
            raise ContractError("coverage_clause_shape")
        cid = clause["clause_id"]
        if not isinstance(cid, str) or not re.fullmatch(r"JD-[a-z0-9-]+", cid):
            raise ContractError("coverage_clause_id_invalid")
        if cid in seen:
            raise ContractError("coverage_duplicate_clause_id:" + cid)
        seen.add(cid)
        if not isinstance(clause["locator"], str) or len(clause["locator"].strip()) < 8:
            raise ContractError("coverage_locator_missing:" + cid)
        if not isinstance(clause["summary"], str) or len(clause["summary"].strip()) < 16:
            raise ContractError("coverage_summary_missing:" + cid)
        if clause["claim_kind"] != "SOURCE_PARAPHRASE":
            raise ContractError("coverage_claim_kind_unverified:" + cid)
        ids = clause["requirement_ids"]
        if not isinstance(ids, list) or len(ids) != len(set(ids)):
            raise ContractError("coverage_requirement_ids_invalid:" + cid)
        for req_id in ids:
            if req_id not in requirements:
                raise ContractError("coverage_unknown_requirement:" + str(req_id))
            if inventory["source_id"] not in requirements[req_id]["source_ids"]:
                raise ContractError("coverage_requirement_source_mismatch:" + req_id)
        # These are declared typed links, not proof of implementation or
        # whether a model mapped a natural-language source faithfully.
        spec_ids = sorted(c["stable_id"] for c in cards
                          if c["series"] == "SPEC" and c["status"] == "ACTIVE"
                          and any(edge["relation"] == "implements" and
                                  edge["target"] in ids for edge in c["typed_links"]))
        rows.append({"clause_id": cid,
                     "trace_status": "DECLARED_LINK_UNVERIFIED" if ids else "UNMAPPED",
                     "requirement_ids": ids, "spec_card_ids": spec_ids})
    missing = [r["clause_id"] for r in rows if r["trace_status"] == "UNMAPPED"]
    return {
        "protocol": "factoryweaver/requirement-coverage-v1",
        "subject": inventory["subject_id"],
        "source_id": inventory["source_id"],
        "inventory_clause_count": len(rows),
        "declared_link_count": len(rows) - len(missing),
        "unmapped_clause_ids": missing,
        "rows": rows,
        "coverage_kind": "STRUCTURAL_TRACE_ONLY",
        "source_exhaustiveness_proven": False,
        "source_origin_authenticated": False,
        "semantic_mapping_verified": False,
        "engineering_verified": False,
        "delivery_verified": False,
        "effect_authority": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only source-to-REQ trace audit")
    parser.add_argument("record")
    parser.add_argument("inventory")
    args = parser.parse_args(argv)
    try:
        result = trace(load(args.record), load(args.inventory))
        print(json.dumps(result, sort_keys=True, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({"valid": False, "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
