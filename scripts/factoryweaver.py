#!/usr/bin/env python3
"""FactoryWeaver reference-only CLI: no shell, network, host write, or PR authority."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts/v1/knowledge-record.schema.json"
REGISTRY = ROOT / "contracts/v1/adapter-registry.schema.json"

class ContractError(ValueError):
    pass

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def _check_unique(name, items):
    if len(items) != len(set(items)):
        raise ContractError("duplicate_" + name)

def verify(record):
    Draft202012Validator(load(SCHEMA)).validate(record)
    sources = {s["source_id"]: s for s in record["sources"]}
    _check_unique("sources", [s["source_id"] for s in record["sources"]])
    _check_unique("requirements", [r["id"] for r in record["requirements"]])
    _check_unique("decisions", [d["id"] for d in record.get("decisions", [])])
    _check_unique("cards", [c["stable_id"] for c in record["cards"]])
    _check_unique("canonical_keys", [c["canonical_key"] for c in record["cards"]])
    _check_unique("action_requests", [a["request_id"] for a in record["action_requests"]])
    targets = {r["id"] for r in record["requirements"]}
    targets |= {c["stable_id"] for c in record["cards"]}
    targets |= {d["id"] for d in record.get("decisions", [])}
    for s in record["sources"]:
        pinned = s.get("integrity") == "PINNED_SHA256"
        if pinned != bool(s.get("sha256")):
            raise ContractError("invalid_source_pin:" + s["source_id"])
    def sources_exist(refs, label):
        if not set(refs).issubset(sources):
            raise ContractError("unknown_source:" + label)
    for r in record["requirements"]:
        sources_exist(r["source_ids"], r["id"])
        if not set(r.get("depends_on", [])).issubset(targets):
            raise ContractError("unknown_requirement_dependency:" + r["id"])
        if r["engineering_status"] in ("TESTED_SCOPED", "ACTIVATED"):
            raise ContractError("untrusted_test_claim:" + r["id"])
        if r["delivery_status"] == "RELEASE_CONFIRMED":
            raise ContractError("untrusted_delivery_claim:" + r["id"])
    # A typed dependency graph may be consulted by other hosts. Refuse
    # cyclic requirement prerequisites instead of projecting an apparent READY.
    requirements_by_id = {r["id"]: r for r in record["requirements"]}
    visiting, visited = set(), set()
    def visit_requirement(key):
        if key in visiting:
            raise ContractError("requirement_dependency_cycle:" + key)
        if key in visited:
            return
        visiting.add(key)
        for dep in requirements_by_id[key].get("depends_on", []):
            if dep in requirements_by_id:
                visit_requirement(dep)
        visiting.remove(key)
        visited.add(key)
    for key in requirements_by_id:
        visit_requirement(key)
    for c in record["cards"]:
        sources_exist(c["evidence_ids"], c["stable_id"])
        if any(edge["target"] not in targets for edge in c["typed_links"]):
            raise ContractError("unknown_typed_link:" + c["stable_id"])
    for d in record.get("decisions", []):
        sources_exist(d["source_ids"], d["id"])
        if d["human_confirmed"]:
            # A record-controlled SHA-256 field proves no human identity or consent.
            # This reference CLI has no independently trusted human-input owner.
            # A future host adapter must verify the raw decision outside this
            # untrusted exchange before issuing any confirmation projection.
            raise ContractError("human_confirmation_owner_required:" + d["id"])
        elif d.get("decision") is not None or d.get("confirmation_ref"):
            raise ContractError("unconfirmed_decision:" + d["id"])
    for a in record["action_requests"]:
        if a["effect_authority"] or a["registered"] or a["status"] in ("READY", "RUNNING", "OBSERVED") or a.get("observed") is not None:
            raise ContractError("untrusted_action_claim:" + a["request_id"])
    # Progress is an untrusted author-supplied summary, not a host receipt.
    # The public reference validator must not accept completion or invented
    # states that it has no independently verified owner evidence for.
    allowed_progress_states = {
        "knowledge": {"UNKNOWN", "ANCHORED", "CONFLICTED", "SPECIFIED", "HUMAN_ANSWER_MISSING"},
        "engineering": {"NOT_STARTED", "UNASSESSED", "CODE_OBSERVED", "CONTRACT_DEFINED"},
        "delivery": {"NOT_STARTED", "BLOCKED", "OWNER_WAIT"},
    }
    for axis, allowed in allowed_progress_states.items():
        if record["progress"][axis]["state"] not in allowed:
            raise ContractError("unsupported_progress_state:" + axis)
        sources_exist(record["progress"][axis]["evidence_refs"], axis)
    return {"valid": True, "requirements": len(record["requirements"]), "cards": len(record["cards"]), "proof_ceiling": "SCHEMA_FIXTURE_ONLY", "effect_authority": False}

def project(record):
    verify(record)
    decisions = {d["id"]: d for d in record.get("decisions", [])}
    requirements_by_id = {r["id"]: r for r in record["requirements"]}
    cards_by_id = {c["stable_id"]: c for c in record["cards"]}
    sources_by_id = {source["source_id"]: source for source in record["sources"]}
    evaluated = {}

    def evaluate(req_id):
        # Verification already rejects cyclic requirement dependencies.
        if req_id in evaluated:
            return evaluated[req_id]
        req = requirements_by_id[req_id]
        dependencies = req.get("depends_on", [])
        unresolved = [ref for ref in dependencies
                      if ref in decisions and not decisions[ref]["human_confirmed"]]
        unpinned = [ref for ref in req["source_ids"]
                    if sources_by_id[ref].get("integrity") != "PINNED_SHA256"]
        # Knowledge claims do not override missing prerequisites. Walk the
        # actual dependency DAG, including decisions buried in another REQ.
        prerequisites = [ref for ref in dependencies
                         if (ref in requirements_by_id and
                             evaluate(ref)[0] not in ("READY_FOR_OWNER_REVIEW", "SPECIFICATION_ONLY")) or
                            (ref in cards_by_id and
                             cards_by_id[ref]["series"] in ("K", "X") and
                             cards_by_id[ref]["status"] == "ACTIVE")]
        if unresolved:
            status, missing = "WAIT_FOR_HUMAN", unresolved
        elif prerequisites:
            status, missing = "WAIT_FOR_PREREQUISITE", prerequisites
        elif req["knowledge_status"] == "CONFLICTED":
            status, missing = "CONTESTED", []
        elif req["knowledge_status"] == "UNKNOWN":
            status, missing = "WAIT_FOR_EVIDENCE", []
        elif unpinned:
            status, missing = "WAIT_FOR_SOURCE_PIN", unpinned
        elif req["engineering_status"] == "UNASSESSED":
            status, missing = "READY_FOR_OWNER_REVIEW", []
        else:
            status, missing = "SPECIFICATION_ONLY", []
        evaluated[req_id] = (status, missing)
        return evaluated[req_id]

    result = []
    for req in record["requirements"]:
        status, missing = evaluate(req["id"])
        result.append({"requirement": req["id"], "state": status, "missing": missing,
                       "knowledge": req["knowledge_status"],
                       "engineering": req["engineering_status"],
                       "delivery": req["delivery_status"], "authorizes_effects": False})
    return {"protocol": "factoryweaver/v1", "subject": record["subject"]["id"],
            "projection": result, "operation_scope": "READ_ONLY_NO_EXECUTION",
            "completion": "COMPILED_ONLY"}

def route(record, registry=None):
    verify(record)
    # Bind readiness to the named requirement for validation/readback. A
    # registered-looking capability cannot bypass unresolved human decisions.
    projections = {row["requirement"]: row for row in project(record)["projection"]}
    operations = {}
    if registry:
        Draft202012Validator(load(REGISTRY)).validate(registry)
        for entry in registry["operations"]:
            op = entry["operation_id"]
            if op in operations:
                raise ContractError("duplicate_registry_operation:" + op)
            operations[op] = entry
    results = []
    for a in record["action_requests"]:
        entry = operations.get(a["operation_id"])
        status = "HOST_REGISTRY_REQUIRED"
        owner = entry["owner"] if entry else None
        requirement_id = a["target"].get("requirement_id")
        requirement_state = projections.get(requirement_id, {}).get("state")
        if entry:
            if not entry["enabled"]:
                status = "CAPABILITY_DISABLED"
            elif a["mode"] not in entry["allowed_modes"] or a["target"].get("kind") not in entry["target_kinds"]:
                status = "REGISTRY_SCOPE_MISMATCH"
            elif a["intent"] != "resolve_unknown" and not requirement_id:
                status = "REQUIREMENT_BINDING_REQUIRED"
            elif requirement_id is not None and requirement_id not in projections:
                status = "UNKNOWN_REQUIREMENT"
            elif a["intent"] != "resolve_unknown" and requirement_state not in ("READY_FOR_OWNER_REVIEW", "SPECIFICATION_ONLY"):
                status = "REQUIREMENT_BLOCKED"
            elif entry.get("requires_pinned_source", False) and any(s.get("integrity") != "PINNED_SHA256" for s in record["sources"]):
                status = "WAIT_FOR_SOURCE_PIN"
            else:
                status = "REGISTERED_CANDIDATE_ONLY"
        results.append({"request_id": a["request_id"], "operation_id": a["operation_id"],
                        "route": status, "owner": owner,
                        "requirement_state": requirement_state, "can_execute": False})
    return {"requests": results, "effects": 0, "authority": "NONE"}

def cards(record):
    verify(record)
    out = ["# FactoryWeaver — Knowledge / Engineering / Delivery", "", "| REQ | Knowledge | Engineering | Delivery |", "|---|---|---|---|"]
    for r in record["requirements"]:
        out.append(f"| {r['id']} | {r['knowledge_status']} | {r['engineering_status']} | {r['delivery_status']} |")
    for c in record["cards"]:
        out.extend(["", f"## {c['stable_id']} | {c['title']}", "", c["payload"], "", "**Evidence:** " + (", ".join(c["evidence_ids"]) or "NONE"), "**Typed Links:** " + (", ".join(f"{e['relation']} → {e['target']}" for e in c["typed_links"]) or "NONE")])
    return "\n".join(out) + "\n"

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("validate", "project", "route", "cards"))
    parser.add_argument("input")
    parser.add_argument("--registry", help="Optional host capability registry for advisory routing only")
    args = parser.parse_args(argv)
    try:
        record = load(args.input)
        output = {
            "validate": lambda: verify(record),
            "project": lambda: project(record),
            "route": lambda: route(record, load(args.registry) if args.registry else None),
            "cards": lambda: cards(record),
        }[args.command]()
        print(json.dumps(output, ensure_ascii=False, sort_keys=True) if not isinstance(output, str) else output, end="\n" if not isinstance(output, str) else "")
        return 0
    except (OSError, ValueError, ValidationError, ContractError) as e:
        print(json.dumps({"valid": False, "error": str(e)}), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
