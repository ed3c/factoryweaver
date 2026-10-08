#!/usr/bin/env python3
"""Fixture-only structural regression for v7.1/v7.2 card semantics.

This checks declared case partitions and required narrative/mechanism/action
sections. It cannot judge truthfulness, prose quality or human comprehension.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from factoryweaver import ContractError

CASE_DIMENSIONS = (
    "entity", "event", "scope", "decision_use", "falsifier", "evidence_compatibility"
)
NARRATIVE = (
    "tension", "actors", "starting_state", "pressure",
    "decision", "turn", "outcome", "unresolved"
)
CONCEPT = (
    "definition", "mechanism", "non_goals", "boundary",
    "positive_example", "counterexample"
)
PRACTICE = (
    "scenario", "value", "prerequisites", "inputs", "steps",
    "expected_output", "rollback", "failure_handling", "security"
)


def _text(value, name):
    # Minimum is structural, not an independent semantic-quality measure.
    if not isinstance(value, str) or len(value.strip()) < 12:
        raise ContractError("missing_or_fragmentary_field:" + name)


def audit_fixture(data):
    if not isinstance(data, dict) or data.get("protocol") != "factoryweaver/semantic-golden-v1":
        raise ContractError("semantic_golden_protocol")
    if data.get("source_kind") != "SYNTHETIC_NORMATIVE_FIXTURE":
        raise ContractError("unverified_source_type")
    if data.get("human_review") != "REQUIRED_NOT_RUN":
        raise ContractError("forged_human_review")
    cases = data.get("cases")
    cards = data.get("cards")
    if not isinstance(cases, list) or not cases or not isinstance(cards, list) or not cards:
        raise ContractError("golden_cases_or_cards_missing")
    card_map = {}
    for card in cards:
        if not isinstance(card, dict) or card.get("series") not in ("N", "C", "P"):
            raise ContractError("unsupported_golden_card")
        card_id = card.get("id")
        if not isinstance(card_id, str) or not card_id or card_id in card_map:
            raise ContractError("duplicate_or_missing_golden_card")
        fields = {"N": NARRATIVE, "C": CONCEPT, "P": PRACTICE}[card["series"]]
        payload = card.get("payload")
        if not isinstance(payload, dict):
            raise ContractError("golden_payload_missing:" + card_id)
        for field in fields:
            if field == "steps":
                steps = payload.get("steps")
                if not isinstance(steps, list) or not steps:
                    raise ContractError("missing_practice_steps:" + card_id)
                for step in steps:
                    if not isinstance(step, dict):
                        raise ContractError("invalid_practice_step")
                    for part in ("action", "validation", "failure_signal"):
                        _text(step.get(part), card_id + "." + part)
            else:
                _text(payload.get(field), card_id + "." + field)
        if card["series"] == "P" and payload.get("execution_status") != "UNTESTED":
            raise ContractError("unverified_practice_execution")
        card_map[card_id] = card
    by_signature, by_card, case_ids = {}, {}, set()
    for case in cases:
        if not isinstance(case, dict):
            raise ContractError("invalid_case")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in case_ids:
            raise ContractError("duplicate_case_identity")
        case_ids.add(case_id)
        signature = []
        for dim in CASE_DIMENSIONS:
            value = case.get(dim)
            _text(value, case_id + "." + dim)
            signature.append(value.strip())
        signature = tuple(signature)
        card_id = case.get("card_id")
        if card_id not in card_map:
            raise ContractError("unbound_case_card:" + case_id)
        if signature in by_signature and by_signature[signature] != card_id:
            raise ContractError("same_case_fragmented:" + case_id)
        if card_id in by_card and by_card[card_id] != signature:
            raise ContractError("independent_cases_collapsed:" + case_id)
        by_signature[signature] = card_id
        by_card[card_id] = signature
    if set(card_map) != set(by_card):
        raise ContractError("unmapped_golden_cards")
    return {
        "status": "STRUCTURAL_GOLDEN_PASS",
        "case_rows": len(cases),
        "decision_relevant_cases": len(by_signature),
        "cards": len(card_map),
        "human_review": "REQUIRED_NOT_RUN",
        "semantic_quality_proven": False,
        "source_veracity_proven": False,
        "effect_authority": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture")
    args = parser.parse_args(argv)
    try:
        data = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
        print(json.dumps(audit_fixture(data), ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
