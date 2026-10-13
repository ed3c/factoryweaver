#!/usr/bin/env python3
"""Repeatable project-local CLI verification, with an honest native proof ceiling."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parents[1]
FEATURES = ('knowledge-contract', 'semantic-cards', 'scope-handoff', 'manager-needs', 'typed-links', 'soodles-reader', 'source-fidelity', 'goal-scope', 'prompt-delta', 'pclass-consumer', 'outer-admission', 'inner-poteto', 'test-manager', 'schema-feedback', 'native-hook', 'native-cron', 'delivery-closure', 'prompt-carriers', 'portable-bundle', 'requirement-coverage', 'factory-profile', 'source-lock', 'semantic-golden', 'blind-packet')
LOCAL_FEATURES = {'typed-links', 'factory-profile', 'requirement-coverage', 'manager-needs', 'knowledge-contract', 'scope-handoff', 'semantic-golden', 'prompt-carriers', 'source-lock', 'blind-packet', 'semantic-cards', 'portable-bundle'}
EXTERNAL_PROOF = {
    "source-fidelity": "Independent review of actual inspected source units and source coverage, not a field-only fixture",
    "goal-scope": "Fresh original Issue and Source/REQ Goal-Measurement-Acceptance readback",
    "prompt-delta": "Actual admitted Noodle writer capture that consumed the changed Prompt Delta",
    "pclass-consumer": "Fresh native Agent consumer report/raw trace reviewed by original schema pclass-feedback",
    "outer-admission": "Original Soodles Issue Contract/Admission provider readback",
    "inner-poteto": "Admitted Noodle execute stage, selected Poteto playbook and real writer readback",
    "test-manager": "Original Test Manager selected controls, run and result readback",
    "schema-feedback": "Original Schema feedback and observable consumption of returned next",
    "native-hook": "Original native Hook event/effect readback or complete relevant nontrigger capture",
    "native-cron": "Previously authorized native heartbeat, current original owner continuation",
    "delivery-closure": "Original provider exact-head/merge/closure and complete parent Goal evidence",
}
HEADINGS = ("Sub-features", "How to get to it (user POV)",
            "Driving it with the CLI harness", "Gotchas")


class Gap(Exception):
    pass


def ensure(ok, message):
    if not ok:
        raise Gap(message)


def save(folder, name, data):
    path = folder / name
    text = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")


def invoke(args, evidence, label, expected=0, cwd=ROOT):
    result = subprocess.run(args, cwd=cwd, text=True, encoding="utf-8",
                            errors="replace", capture_output=True, timeout=30,
                            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    save(evidence, label + ".stdout.txt", result.stdout)
    save(evidence, label + ".stderr.txt", result.stderr)
    save(evidence, label + ".invocation.json",
         {"argv": args, "exit": result.returncode, "expected": expected})
    ensure(result.returncode == expected, label + ": unexpected CLI exit")
    return result.stdout if expected == 0 else result.stderr


def call(script, *args):
    return [sys.executable, str(ROOT / "scripts" / script), *map(str, args)]


def obj(args, evidence, label, expected=0, cwd=ROOT):
    value = json.loads(invoke(args, evidence, label, expected, cwd))
    ensure(isinstance(value, dict), label + ": expected JSON object")
    return value


def doctor():
    issues = []
    for p in ("scripts/factoryweaver.py", "scripts/card_semantic.py",
              "scripts/soodles_handoff.py", "docs/evals/cs329z-hw1/drill.json",
              "examples/card-semantic/hw1-email-qa.json"):
        if not (ROOT / p).is_file():
            issues.append("missing:" + p)
    try:
        import jsonschema
    except ImportError:
        issues.append("jsonschema_dependency_missing")
    try:
        index = (HERE / "features" / "README.md").read_text(encoding="utf-8")
        linked = re.findall(r"\]\(\./([a-z][a-z0-9-]+)\.md\)", index)
        actual = [p.stem for p in (HERE / "features").glob("*.md") if p.name != "README.md"]
        ensure(len(linked) == len(set(linked)) and set(linked) == set(actual) == set(FEATURES),
               "feature_map_index_drift")
    except (Gap, OSError) as err:
        issues.append(str(err))
    return {"status": "ready" if not issues else "blocked",
            "surface": "FactoryWeaver public Python CLI", "issues": issues}


def source_wave(feature):
    """Concurrent read-only source location check; semantic source review is separate."""
    doc = (HERE / "features" / (feature + ".md")).read_text(encoding="utf-8")
    headings = re.findall(r"^## (.*)$", doc, re.MULTILINE)
    sources = re.findall(r"^- Source: ([^\n]+)", doc, re.MULTILINE)
    missing = [s for s in sources if not (ROOT / s).is_file() or
               not (ROOT / s).resolve().is_relative_to(ROOT)]
    return {"feature": feature, "status": "indexed" if tuple(headings) == HEADINGS and
            sources and not missing else "map_drift", "sources": sources, "missing": missing,
            "proof_ceiling": "SOURCE_PATH_EXISTENCE_NOT_SOURCE_MEANING"}


def drive(feature, evidence, scratch):
    name = feature.replace("-", "_")
    if feature == "source-lock":
        repository = scratch / "source-fixture"
        repository.mkdir()
        source = repository / "SOURCE.md"
        raw = (ROOT / "docs/bootstrap-boundary.md").read_bytes()
        source.write_bytes(raw)
        invoke(["git", "init", "-q", "-b", "main", str(repository)], evidence, name + "_init")
        invoke(["git", "-C", str(repository), "add", "SOURCE.md"], evidence, name + "_add")
        invoke(["git", "-C", str(repository), "-c", "user.name=Fixture",
                "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Synthetic source snapshot"],
               evidence, name + "_snapshot")
        revision = invoke(["git", "-C", str(repository), "rev-parse", "HEAD"], evidence, name + "_head").strip()
        manifest = {"protocol": "factoryweaver/source-lock-v1", "repository": "example/synthetic-source",
                    "revision": revision, "path": "SOURCE.md",
                    "git_blob_sha1": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest(),
                    "sha256": hashlib.sha256(raw).hexdigest(), "source_dependency_key": "synthetic-source-fixture",
                    "anchors": [{"id": "title", "text_match": raw.decode("utf-8").splitlines()[0]}]}
        pinned = scratch / "manifest.json"
        pinned.write_text(json.dumps(manifest), encoding="utf-8")
        matched = obj(call("source_lock.py", pinned, source), evidence, name + "_match")
        ensure(matched["status"] == "SUPPLIED_BYTES_MATCH_FROZEN_MANIFEST" and
               not matched["external_origin_authenticated"], "source_lock_overclaim")
        altered = scratch / "altered.txt"
        altered.write_bytes(raw + b"altered")
        refused = obj(call("source_lock.py", pinned, altered), evidence, name + "_altered", expected=2)
        ensure("mismatch" in refused["error"], "changed_source_accepted")
    elif feature == "semantic-golden":
        fixture = ROOT / "tests/fixtures/semantic-golden.json"
        valid = obj(call("semantic_golden.py", fixture), evidence, name + "_fixture")
        ensure(valid["status"] == "STRUCTURAL_GOLDEN_PASS" and not valid["semantic_quality_proven"],
               "structural_golden_overclaim")
        data = json.loads(fixture.read_text())
        data["human_review"] = "APPROVED"
        bad = scratch / "forged-review.json"
        bad.write_text(json.dumps(data))
        refused = obj(call("semantic_golden.py", bad), evidence, name + "_forged", expected=2)
        ensure("forged_human_review" in refused["error"], "false_semantic_approval")
    elif feature == "blind-packet":
        case = {"protocol": "factoryweaver/blind-comparison-v1", "case_id": "synthetic-paired-outputs",
                "source_manifest_sha256": hashlib.sha256(b"synthetic source").hexdigest(),
                "task": "Compare two synthetic outputs under identical declared conditions.",
                "frozen_conditions": {"source": "synthetic fixture only"},
                "baseline_output": "The first illustrative output states a mechanism without its failure boundary.",
                "candidate_output": "The second illustrative output preserves a mechanism and its explicit failure boundary."}
        path = scratch / "case.json"
        path.write_text(json.dumps(case))
        seed = scratch / "seed.bin"
        seed.write_bytes(os.urandom(32))
        packet = obj(call("blind_review.py", "packet", path, "--seed-file", seed), evidence, name + "_packet")
        ensure(packet["review_status"] == "NOT_RUN" and "baseline_output" not in packet,
               "blind_packet_overclaim")
        case["candidate_output"] += " v7.2"
        path.write_text(json.dumps(case))
        refused = obj(call("blind_review.py", "packet", path, "--seed-file", seed),
                      evidence, name + "_unblinded", expected=2)
        ensure("unredacted_version_label" in refused["error"], "unblinded_output_accepted")
    elif feature == "factory-profile":
        root = ROOT / "examples/factory-profiles"
        profile = root / "pstack-synthetic.json"
        binding = root / "pstack-binding-synthetic.json"
        catalog = root / "pstack-catalog-synthetic.json"
        valid = obj(call("factory_profile.py", "validate", profile), evidence, name + "_profile")
        ensure(valid["status"] == "PROFILE_SHAPE_VALID", "profile_contract_drift")
        matching = obj(call("factory_profile.py", "audit-catalog", profile, binding, catalog),
                       evidence, name + "_catalog")
        ensure(matching["status"] == "EFFECTIVE_CATALOG_CLAIM_MATCHES" and
               not matching["actual_worker_skill_discovery_verified"], "catalog_claim_promoted")
        raw = catalog.read_bytes()
        pinned = hashlib.sha256(raw).hexdigest()
        obj(call("factory_profile.py", "audit-catalog-pinned", profile, binding, catalog,
                 "--catalog-sha256", pinned), evidence, name + "_pinned")
        duplicate = scratch / "duplicate-catalog.json"
        duplicate.write_bytes(b'{"producer_claim":"OWNER_VERIFIED",' + raw[1:])
        refused = obj(call("factory_profile.py", "audit-catalog-pinned", profile, binding, duplicate,
                           "--catalog-sha256", hashlib.sha256(duplicate.read_bytes()).hexdigest()),
                      evidence, name + "_duplicate", expected=2)
        ensure("duplicate_json_key" in refused["error"], "ambiguous_catalog_accepted")
        bad = json.loads(raw)
        bad["skills"][0]["scope"] = "global"
        duplicate.write_text(json.dumps(bad), encoding="utf-8")
        refused = obj(call("factory_profile.py", "audit-catalog", profile, binding, duplicate),
                      evidence, name + "_global", expected=2)
        ensure("catalog_nonworktree_inheritance" in refused["error"], "global_skill_claim_accepted")
    elif feature == "requirement-coverage":
        root = ROOT / "examples/openai-plugin-platform"
        base = obj(call("requirement_coverage.py", root / "project.json",
                        root / "job-clause-inventory.json"), evidence, name + "_baseline")
        proposal = obj(call("requirement_coverage.py", root / "proposed-six-requirements.json",
                            root / "proposed-six-clause-inventory.json"), evidence, name + "_proposal")
        ensure(base["declared_link_count"] == 1 and proposal["declared_link_count"] == 6
               and not proposal["semantic_mapping_verified"], "coverage_claim_drift")
        invalid = scratch / "bad-record.json"
        invalid.write_text("{}", encoding="utf-8")
        refused = obj(call("requirement_coverage.py", invalid, root / "job-clause-inventory.json"),
                      evidence, name + "_invalid", expected=2)
        ensure(not refused["valid"], "schema_invalid_coverage_accepted")
        inventory = json.loads((root / "job-clause-inventory.json").read_text())
        inventory["source_id"] = "SRC-unknown"
        bad = scratch / "bad-inventory.json"
        bad.write_text(json.dumps(inventory), encoding="utf-8")
        refused = obj(call("requirement_coverage.py", root / "project.json", bad),
                      evidence, name + "_source", expected=2)
        ensure("coverage_unknown_source" in refused["error"], "unbound_coverage_source")
    elif feature == "portable-bundle":
        folder = scratch / "distribution"
        first = obj(call("build_skill_bundle.py", folder), evidence, name + "_build")
        repeated = obj(call("build_skill_bundle.py", folder), evidence, name + "_repeat")
        ensure(first["status"] == "CREATED" and repeated["status"] == "NOOP",
               "bundle_replay_drift")
        observed = obj(call("verify_installed_skill.py", folder), evidence, name + "_installed")
        ensure(observed["status"] == "INSTALLED_SKILL_REFERENCE_CLI_PASS" and
               not observed["actual_agent_invocation"], "bundle_claims_native_agent")
        entry = folder / "skills/factoryweaver/SKILL.md"
        entry.write_text("tampered", encoding="utf-8")
        refused = obj(call("check_bundle.py", folder), evidence, name + "_tampered", expected=2)
        ensure("content_digest_mismatch" in refused["error"], "tampered_bundle_accepted")
    elif feature == "knowledge-contract":
        record = ROOT / "docs/evals/cs329z-hw1/drill.json"
        result = obj(call("factoryweaver.py", "validate", record), evidence, name + "_valid")
        ensure(result["valid"] and result["proof_ceiling"] == "SCHEMA_FIXTURE_ONLY",
               "fixture_wrongly_reported_semantics")
        cards = invoke(call("factoryweaver.py", "cards", record), evidence, name + "_cards")
        ensure("SPEC-email-qa" in cards and "REQ-email-qa" in cards,
               "rendered_knowledge_missing")
        bad = scratch / "bad.json"
        bad.write_text("{}", encoding="utf-8")
        ensure(obj(call("factoryweaver.py", "validate", bad), evidence,
                   name + "_invalid", expected=2)["valid"] is False, "malformed_record_accepted")
    elif feature == "semantic-cards":
        selected = obj(call("card_semantic.py", "select", "C", "SPEC", "V"),
                       evidence, name + "_select")
        ensure([x["series"] for x in selected["prompts"]] == ["C", "SPEC", "V"],
               "wrong_selected_types")
        all_series = ("N", "Q", "C", "D", "S", "P", "T", "R", "G",
                      "E", "V", "X", "K", "REQ", "SPEC")
        exhaustive = obj(call("card_semantic.py", "select", *all_series),
                         evidence, name + "_all_15_series")
        ensure([item["series"] for item in exhaustive["prompts"]] == list(all_series),
               "original_card_series_registry_incomplete")
        fixture = ROOT / "examples/card-semantic/hw1-email-qa.json"
        result = obj(call("card_semantic.py", "inspect", fixture), evidence, name + "_inspect")
        ensure(result["status"] == "SHAPE_VALID_SEMANTICS_UNVERIFIED",
               "shape_result_mislabeled_as_semantic_pass")
        bad = json.loads(fixture.read_text(encoding="utf-8"))
        next(c for c in bad["cards"] if c["series"] == "SPEC")["source_status"] = "UNREAD"
        target = scratch / "unread.json"
        target.write_text(json.dumps(bad), encoding="utf-8")
        result = obj(call("card_semantic.py", "inspect", target),
                     evidence, name + "_unread", expected=2)
        ensure("source_not_inspected" in result["error"], "unread_source_not_refused")
    elif feature == "scope-handoff":
        record = ROOT / "docs/evals/cs329z-hw1/drill.json"
        selection = ROOT / "examples/soodles-scope/hw1-email-qa-selection.json"
        target = scratch / "bundle.json"
        cmd = call("soodles_handoff.py", record, selection, "--output", target)
        first = obj(cmd, evidence, name + "_first")
        second = obj(cmd, evidence, name + "_repeat")
        ensure(first == second and target.exists(), "bundle_not_idempotent")
        ensure(hashlib.sha256(target.read_bytes()).hexdigest() == first["bundle"]["sha256"],
               "bundle_not_host_bound")
        payload = json.loads(target.read_text(encoding="utf-8"))
        ensure(len(payload["knowledge_record"]["requirements"]) == 13 and
               not first["authorizes_landing"], "full_requirements_or_authority_drift")
        different = json.loads(selection.read_text(encoding="utf-8"))
        different["causal_change"] = "Conflicting scope at same output path"
        next_path = scratch / "different.json"
        next_path.write_text(json.dumps(different), encoding="utf-8")
        failure = obj(call("soodles_handoff.py", record, next_path, "--output", target),
                      evidence, name + "_conflict", expected=2)
        ensure(failure["valid"] is False, "conflicting_bundle_overwritten")
    elif feature == "manager-needs":
        root = ROOT / "examples/card-semantic"
        a = obj(call("card_semantic.py", "managers", root / "qa-test-needs.json"),
                evidence, name + "_test")
        b = obj(call("card_semantic.py", "managers", root / "native-stop-needs.json"),
                evidence, name + "_hook")
        ensure(a["test_manager"]["status"] == "NEEDS_ORIGINAL_TEST_MANAGER_SELECTION" and
               b["hook_manager"]["status"] == "NEEDS_NATIVE_SOURCE_OBSERVATION" and
               not a["manager_actions_performed"] and not b["manager_actions_performed"],
               "manager_request_promoted_to_execution")
        none = scratch / "none.json"
        none.write_text(json.dumps({"schema": "factoryweaver/manager-needs/v1",
                                    "subject": "Unchanged scope", "test_need": None, "hook_need": None}))
        noop = obj(call("card_semantic.py", "managers", none), evidence, name + "_noop")
        ensure(noop["test_manager"]["status"] == "NO_TEST_SELECTION_REQUESTED" and
               noop["hook_manager"]["status"] == "NO_NATIVE_HOOK_REQUIRED",
               "no_change_triggered_manager")
    elif feature == "prompt-carriers":
        # CLI proof of data-carrier preservation, NOT independent Agent reasoning.
        source = ROOT / "docs/evals/cs329z-hw1/drill.json"
        selection_path = ROOT / "examples/soodles-scope/hw1-email-qa-selection.json"
        scope = json.loads(selection_path.read_text(encoding="utf-8"))
        selected = obj(call("card_semantic.py", "select", "C", "REQ", "SPEC", "V"),
                       evidence, name + "_prompt_contracts")
        ensure([item["series"] for item in selected["prompts"]] == ["C", "REQ", "SPEC", "V"],
               "selected_role_contracts_changed")
        target = scratch / "prompt-chain-bundle.json"
        materialized = obj(call("soodles_handoff.py", source, selection_path,
                                "--output", target), evidence, name + "_bundle")
        packet = json.loads(target.read_text(encoding="utf-8"))
        record = json.loads(source.read_text(encoding="utf-8"))
        ensure(packet["kind"] == "SOURCE_BOUND_PROPOSAL" and
               packet["knowledge_record"] == record and
               packet["selection"] == scope and
               not materialized["authorizes_landing"], "prompt_scope_or_parent_goal_truncated")
        ensure(isinstance(scope["prompt_delta"], list) and
               all(isinstance(v, str) for v in scope["prompt_delta"]),
               "semantic_delta_missing")
        altered = dict(scope)
        altered["goal"] = "A conflicting task target not confirmed by current original Issue."
        conflicting = scratch / "conflicting-goal.json"
        conflicting.write_text(json.dumps(altered), encoding="utf-8")
        second = scratch / "different-goal-bundle.json"
        proposed = obj(call("soodles_handoff.py", source, conflicting,
                            "--output", second), evidence, name + "_unverified_goal")
        actual = json.loads(second.read_text(encoding="utf-8"))
        ensure(actual["selection"]["goal"] == altered["goal"] and
               actual["kind"] == "SOURCE_BOUND_PROPOSAL" and
               not proposed["authorizes_landing"],
               "syntactic_goal_duplicate_promoted_to_authorization")
        wrong = dict(scope)
        wrong["card_ids"] = ["SPEC-FORGED-IDENTITY"]
        malformed = scratch / "wrong-card.json"
        malformed.write_text(json.dumps(wrong), encoding="utf-8")
        refused = obj(call("soodles_handoff.py", source, malformed),
                      evidence, name + "_wrong_card", expected=2)
        ensure(refused["valid"] is False, "unknown_card_identity_did_not_refuse")
        return {"feature": feature, "status": "cli-verified",
                "proof_ceiling": "PROMPT_DATA_CARRIERS_ONLY",
                "source_to_card_semantics": "UNVERIFIED",
                "selection_goal_equality_to_original_issue": "NOT_OBSERVED",
                "delta_consumed_by_writer": "NOT_RUN",
                "next": None, "original_manager_effects": []}
    elif feature == "typed-links":
        target = ROOT / "examples/card-semantic/hw1-email-qa.json"
        fixture = json.loads(target.read_text(encoding="utf-8"))
        positive = obj(call("card_semantic.py", "inspect", target),
                       evidence, name + "_valid")
        ensure(positive["status"] == "SHAPE_VALID_SEMANTICS_UNVERIFIED",
               "link_shape_is_not_semantic_truth")
        links = next(card for card in fixture["cards"] if card["series"] == "SPEC")["links"]
        ensure(bool(links), "missing_selected_link_control")
        links[0]["relation"] = "unsupported_relation"
        altered = scratch / "unsupported-link.json"
        altered.write_text(json.dumps(fixture), encoding="utf-8")
        denied = obj(call("card_semantic.py", "inspect", altered),
                     evidence, name + "_refused", expected=2)
        ensure("invalid_link_kind" in denied["error"], "unsupported_link_not_refused")
    elif feature == "soodles-reader":
        checkout = os.environ.get("SOODLES_CHECKOUT")
        if not checkout or not (Path(checkout).resolve() / "soodles.py").is_file():
            return {"feature": feature, "status": "verified-unreachable",
                    "prerequisite": "original Host must provide a compatible SOODLES_CHECKOUT",
                    "attempted": "real Soodles knowledge inspect CLI"}
        record = ROOT / "docs/evals/cs329z-hw1/drill.json"
        selection = ROOT / "examples/soodles-scope/hw1-email-qa-selection.json"
        target = scratch / "reader-bundle.json"
        materialized = obj(call("soodles_handoff.py", record, selection, "--output", target),
                           evidence, name + "_bundle")
        result = obj([sys.executable, str(Path(checkout).resolve() / "soodles.py"),
                      "knowledge", "inspect", *materialized["reader_arguments"]],
                     evidence, name + "_inspect", cwd=Path(checkout).resolve())
        ensure(result["status"] == "source_bound_proposal" and result["next"] is None
               and result["effects"] == [] and not result["authorizes_landing"] and
               "boundary_findings" in result and "verification_targets" in result,
               "reader_claimed_unobserved_effects")
        return {"feature": feature, "status": "cli-verified-native-not-run",
                "proof_ceiling": "READER_TRANSPORT_ONLY"}
    elif feature in EXTERNAL_PROOF:
        return {"feature": feature, "status": "verified-unreachable",
                "attempted": "Source-map inspection only; no matching original runtime evidence",
                "prerequisite": EXTERNAL_PROOF[feature],
                "proof_ceiling": "UNVERIFIED_ORIGINAL_OWNER",
                "original_effects_performed": []}
    else:
        raise Gap("unknown_feature")
    return {"feature": feature, "status": "cli-verified",
            "proof_ceiling": "LOCAL_CLI_BEHAVIOR_ONLY"}


def maintain(scope, evidence):
    report = {"outcome": "blocked", "scope": scope, "doctor": doctor(),
              "proof_ceiling": "NO_FRESH_AGENT_OR_PROVIDER_EVIDENCE", "features": []}
    if report["doctor"]["status"] != "ready":
        save(evidence, "run.json", report)
        return report
    with ThreadPoolExecutor(max_workers=len(FEATURES)) as pool:
        sources = list(pool.map(source_wave, FEATURES))
    report["source_wave"] = sources
    save(evidence, "source-wave.json", sources)
    if any(x["status"] != "indexed" for x in sources):
        report["reason"] = "feature_map_or_source_drift"
    else:
        with tempfile.TemporaryDirectory(prefix="fw-drive-") as tmp:
            for name in FEATURES:
                if name not in LOCAL_FEATURES and scope == "local":
                    report["features"].append({"feature": name, "status": "excluded",
                                               "reason": "outside local CLI proof; original native/source semantic evidence NOT_RUN"})
                    continue
                try:
                    report["features"].append(drive(name, evidence, Path(tmp)))
                except (Gap, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as err:
                    report["features"].append({"feature": name, "status": "product_or_harness_gap",
                                               "reason": str(err)})
        bad = [x for x in report["features"] if x["status"] not in
               ("cli-verified", "cli-verified-native-not-run", "excluded")]
        if bad:
            report["gaps"] = bad
        elif scope == "local":
            report["outcome"] = "clean"
            report["limits"] = "LOCAL_CLI_ONLY; P-class native and original Owner E2E are NOT_RUN"
        else:
            report["reason"] = "native_issue_admission_and_fresh_consumer_not_observed"
    report["feature_status"] = {item["feature"]: item["status"] for item in report["features"]}
    report["coverage"] = {"mapped": len(FEATURES), "cli_verified": sum(
        item["status"] == "cli-verified" for item in report["features"]),
        "unverified": sum(item["status"] == "verified-unreachable" for item in report["features"])}
    report["cleanup"] = "scratch removed; evidence retained"
    save(evidence, "run.json", report)
    return report


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    sub.add_parser("doctor")
    a = sub.add_parser("drive")
    a.add_argument("feature", choices=FEATURES)
    a.add_argument("--evidence-dir")
    m = sub.add_parser("maintain")
    m.add_argument("--scope", choices=("local", "full"), default="full")
    m.add_argument("--evidence-dir")
    args = parser.parse_args()
    if args.mode == "doctor":
        result = doctor()
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "ready" else 2
    evidence = Path(args.evidence_dir).resolve() if args.evidence_dir else Path(
        tempfile.mkdtemp(prefix="factoryweaver-verify-"))
    evidence.mkdir(parents=True, exist_ok=True)
    if args.mode == "maintain":
        result = maintain(args.scope, evidence)
        success = result["outcome"] == "clean"
    else:
        try:
            ensure(doctor()["status"] == "ready", "doctor_failed")
            with tempfile.TemporaryDirectory(prefix="fw-drive-") as tmp:
                result = drive(args.feature, evidence, Path(tmp))
        except (Gap, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as e:
            result = {"feature": args.feature, "status": "blocked", "reason": str(e)}
        success = result["status"].startswith("cli-verified")
    result["evidence_dir"] = str(evidence)
    save(evidence, "result.json", result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if success else 2


if __name__ == "__main__":
    sys.exit(main())
