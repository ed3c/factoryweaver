#!/usr/bin/env python3
"""Prepare a blinded v7.1/v7.2 comparison packet, without running or scoring models.

Original evaluator/host must keep the seed + answer key separate from the
independent reviewer. A packet cannot establish independent human evaluation.
"""
from __future__ import annotations
import argparse
import hashlib
import hmac
import json
import re
import sys
from pathlib import Path
from factoryweaver import ContractError

DIMENSIONS = ("source_fidelity", "narrative", "concept_mechanism",
              "actionability", "reader_efficiency")


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def validate_case(case):
    required = {"protocol", "case_id", "source_manifest_sha256", "task",
                "frozen_conditions", "baseline_output", "candidate_output"}
    if not isinstance(case, dict) or set(case) != required:
        raise ContractError("blind_case_shape")
    if case["protocol"] != "factoryweaver/blind-comparison-v1":
        raise ContractError("blind_case_protocol")
    if not isinstance(case["case_id"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{3,80}", case["case_id"]):
        raise ContractError("blind_case_id")
    if not isinstance(case["source_manifest_sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", case["source_manifest_sha256"]):
        raise ContractError("source_manifest_digest_required")
    if not isinstance(case["task"], str) or len(case["task"].strip()) < 20:
        raise ContractError("blind_task_missing")
    conditions = case["frozen_conditions"]
    if not isinstance(conditions, dict) or not conditions or any(
        not isinstance(k, str) or not isinstance(v, str) or not k or not v for k, v in conditions.items()
    ):
        raise ContractError("frozen_conditions_missing")
    for field in ("baseline_output", "candidate_output"):
        value = case[field]
        if not isinstance(value, str) or len(value.strip()) < 30:
            raise ContractError("blind_output_missing:" + field)
        # A human reviewer cannot be blinded if candidate text explicitly
        # carries version labels. Never auto-edit source outputs to hide them.
        if re.search(r"\bv7[.]1\b|\bv7[.]2\b", value, re.IGNORECASE):
            raise ContractError("unredacted_version_label:" + field)
    if case["baseline_output"] == case["candidate_output"]:
        raise ContractError("identical_comparison_outputs")


def pair(case, secret):
    validate_case(case)
    if not isinstance(secret, bytes) or len(secret) != 32 or secret == b"\x00" * 32:
        raise ContractError("blind_seed_invalid")
    flip = hmac.digest(secret, b"factoryweaver/blind-v1:" + case["case_id"].encode(), "sha256")[0] & 1
    names = (("baseline_output", "candidate_output") if flip == 0 else
             ("candidate_output", "baseline_output"))
    digest = hashlib.sha256(canonical(case)).hexdigest()
    shared = {"protocol": "factoryweaver/blind-comparison-v1",
              "case_id": case["case_id"], "case_sha256": digest,
              "source_manifest_sha256": case["source_manifest_sha256"]}
    packet = {
        **shared, "task": case["task"], "frozen_conditions": case["frozen_conditions"],
        "criterion_ids": list(DIMENSIONS),
        "A": case[names[0]], "B": case[names[1]],
        "review_status": "NOT_RUN",
        "independent_reviewer_verified": False,
        "source_origin_verified": False,
        "effect_authority": False
    }
    key = {**shared, "A": "v7.1" if names[0] == "baseline_output" else "v7.2",
           "B": "v7.2" if names[1] == "candidate_output" else "v7.1",
           "separate_owner_custody_required": True}
    return packet, key


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("packet", "key"))
    parser.add_argument("case_file")
    parser.add_argument("--seed-file", required=True, help="Private, host-controlled 32-byte seed")
    args = parser.parse_args(argv)
    try:
        case = json.loads(Path(args.case_file).read_text(encoding="utf-8"))
        secret = Path(args.seed_file).read_bytes()
        packet, key = pair(case, secret)
        print(json.dumps(packet if args.command == "packet" else key, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
