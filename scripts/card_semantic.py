#!/usr/bin/env python3
"""Read-only typed Card prompt selection, proposal preflight and manager-need projection.

This is NOT a generative model, semantic truth judge, Test Manager, Hook Manager,
or effect/admission authority. Source truth and independent review stay external.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CARD_PROMPTS = ROOT / "references" / "card-prompts"
REGISTRY = CARD_PROMPTS / "registry.json"
KNOWLEDGE_SCHEMA = ROOT / "contracts" / "v1" / "knowledge-record.schema.json"


class ProposalError(ValueError):
    pass


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _object(value, fields, kind):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ProposalError(f"{kind}:exact_fields_required:{','.join(fields)}")
    return value


def _load(text):
    def unique(pairs):
        result = {}
        for k, v in pairs:
            if k in result:
                raise ProposalError(f"duplicate_json_key:{k}")
            result[k] = v
        return result
    return json.loads(text, object_pairs_hook=unique)


def registry():
    return _load(REGISTRY.read_text(encoding="utf-8"))


def select(series):
    """Host resolves selected files; never make the model reconstruct paths."""
    config = registry()["cards"]
    if not series or len(series) != len(set(series)):
        raise ProposalError("series_selection_empty_or_duplicate")
    unknown = set(series) - set(config)
    if unknown:
        raise ProposalError("unknown_card_series:" + ",".join(sorted(unknown)))
    result = []
    for kind in series:
        item = config[kind]
        path = CARD_PROMPTS / item["file"]
        if not path.is_file():
            raise ProposalError("prompt_missing:" + kind)
        result.append({
            "series": kind, "group": item["group"],
            "prompt": str(path.relative_to(ROOT)),
            "required_semantics": item["required_semantics"]
        })
    return {"status": "SELECTED_ONLY", "prompts": result, "execution": False}


def inspect(data):
    _object(data, ("schema", "cards", "coverage"), "semantic_proposal")
    if data["schema"] != "factoryweaver/card-semantic-proposal/v1":
        raise ProposalError("unsupported_semantic_schema")
    if not isinstance(data["cards"], list) or not isinstance(data["coverage"], list):
        raise ProposalError("invalid_cards_or_coverage")
    prompts = registry()["cards"]
    relations = set(_load(KNOWLEDGE_SCHEMA.read_text(encoding="utf-8"))
                    ["$defs"]["link"]["properties"]["relation"]["enum"])
    titles = []
    for index, card in enumerate(data["cards"]):
        prefix = f"cards[{index}]"
        _object(card, ("series", "title", "source_status", "evidence_topics",
                       "semantics", "links"), prefix)
        series = card["series"]
        if series not in prompts or not _nonempty(card["title"]):
            raise ProposalError(prefix + ":unknown_series_or_title")
        if card["source_status"] not in ("INSPECTED", "UNREAD", "MISSING"):
            raise ProposalError(prefix + ":invalid_source_status")
        if card["source_status"] != "INSPECTED" and series not in ("K", "Q"):
            raise ProposalError(prefix + ":source_not_inspected_use_Q_or_K")
        evidence = card["evidence_topics"]
        if not isinstance(evidence, list) or not all(_nonempty(s) for s in evidence):
            raise ProposalError(prefix + ":invalid_evidence_topics")
        if card["source_status"] == "INSPECTED" and not evidence:
            raise ProposalError(prefix + ":inspected_source_without_anchor")
        fields = prompts[series]["required_semantics"]
        semantics = card["semantics"]
        if not isinstance(semantics, dict) or set(semantics) != set(fields):
            raise ProposalError(prefix + ":wrong_semantic_fields:" + ",".join(fields))
        if any(not _nonempty(semantics[field]) for field in fields):
            raise ProposalError(prefix + ":blank_type_specific_semantics")
        if any(semantics[field].strip().lower() in {
                "tbd", "todo", "unknown", "select a mechanism",
                "implement the required behavior", card["title"].strip().lower()
            } for field in fields):
            raise ProposalError(prefix + ":generic_or_self_repeated_semantics")
        links = card["links"]
        if not isinstance(links, list):
            raise ProposalError(prefix + ":invalid_links")
        for j, link in enumerate(links):
            _object(link, ("relation", "target_series", "target_topic",
                           "applicability", "counterfactual"), prefix + ":link")
            if link["relation"] not in relations or link["target_series"] not in prompts:
                raise ProposalError(prefix + ":invalid_link_kind")
            if not all(_nonempty(link[key]) for key in (
                    "target_topic", "applicability", "counterfactual")):
                raise ProposalError(prefix + ":unjustified_link")
            if link["relation"] == "validated_by" and link["target_series"] != "V":
                raise ProposalError(prefix + ":validated_by_requires_V_target")
            if link["relation"] == "implements" and link["target_series"] not in ("REQ", "SPEC"):
                raise ProposalError(prefix + ":implements_requires_requirement")
        titles.append(card["title"])
    if len(set(titles)) != len(titles):
        raise ProposalError("duplicate_semantic_title")
    seen_units = set()
    for entry in data["coverage"]:
        _object(entry, ("source_unit", "status", "disposition"), "coverage")
        if not _nonempty(entry["source_unit"]) or not _nonempty(entry["disposition"]):
            raise ProposalError("incomplete_source_coverage_entry")
        if entry["status"] not in ("MAPPED", "K", "EXCLUDED"):
            raise ProposalError("invalid_coverage_state")
        if entry["source_unit"] in seen_units:
            raise ProposalError("duplicate_source_coverage_unit")
        seen_units.add(entry["source_unit"])
        if entry["status"] == "MAPPED" and entry["disposition"] not in titles:
            raise ProposalError("unbound_coverage_card_topic")
    return {
        "status": "SHAPE_VALID_SEMANTICS_UNVERIFIED",
        "proof_ceiling": "FIELD_LINK_AND_DECLARED_COVERAGE_ONLY",
        "card_count": len(data["cards"]),
        "declared_source_units": len(seen_units),
        "source_completeness": "NOT_VERIFIED",
        "review_writing": "REQUIRED_NOT_EXECUTED",
        "independent_semantic_review": "NOT_RUN",
        "effect_authority": False
    }


def project_managers(data):
    """Project declared needs only. Soodles owners decide and execute anything real."""
    _object(data, ("schema", "subject", "test_need", "hook_need"), "manager_needs")
    if data["schema"] != "factoryweaver/manager-needs/v1" or not _nonempty(data["subject"]):
        raise ProposalError("unsupported_manager_needs")
    test = data["test_need"]
    hook = data["hook_need"]
    if test is not None:
        _object(test, ("changed_behavior", "verification_question", "negative_case"), "test_need")
        if not all(_nonempty(v) for v in test.values()):
            raise ProposalError("incomplete_test_need")
        test_result = {
            "status": "NEEDS_ORIGINAL_TEST_MANAGER_SELECTION",
            "owner": "Soodles test-manager",
            "verification_question": test["verification_question"],
            "changed_behavior": test["changed_behavior"],
            "negative_case": test["negative_case"],
            "selected_controls": "UNKNOWN",
            "test_execution": "NOT_RUN",
        }
    else:
        test_result = {"status": "NO_TEST_SELECTION_REQUESTED"}
    if hook is not None:
        _object(hook, ("native_event", "observed_requirement", "source_state"), "hook_need")
        if not _nonempty(hook["native_event"]) or not _nonempty(hook["observed_requirement"]):
            raise ProposalError("incomplete_hook_need")
        if hook["source_state"] not in ("INSPECTED", "UNREAD"):
            raise ProposalError("invalid_hook_source_state")
        status = ("NEEDS_ORIGINAL_HOOK_OWNER_READBACK" if hook["source_state"] == "INSPECTED"
                  else "NEEDS_NATIVE_SOURCE_OBSERVATION")
        hook_result = {
            "status": status,
            "owner": "Soodles hook_manager.py / native Hook Owner",
            "native_event": hook["native_event"],
            "native_execution": "UNKNOWN",
            "original_owner_next": "PRESERVE_ORIGINAL_UNMODIFIED",
        }
    else:
        hook_result = {"status": "NO_NATIVE_HOOK_REQUIRED"}
    return {
        "subject": data["subject"],
        "test_manager": test_result,
        "hook_manager": hook_result,
        "effect_authority": False,
        "authorizes_landing": False,
        "manager_actions_performed": [],
        "notes": "Advisory only: no tests, hooks, schedules, commands or owner transitions.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("select")
    s.add_argument("series", nargs="+")
    x = sub.add_parser("inspect")
    x.add_argument("json_file")
    m = sub.add_parser("managers")
    m.add_argument("json_file")
    args = parser.parse_args(argv)
    try:
        if args.mode == "select":
            result = select(args.series)
        else:
            data = _load(Path(args.json_file).read_text(encoding="utf-8"))
            result = inspect(data) if args.mode == "inspect" else project_managers(data)
        print(json.dumps(result, sort_keys=True, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as err:
        print(json.dumps({"valid": False, "error": str(err)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
