# FactoryWeaver → Soodles: source-to-runtime P-class E2E proof

**Goal:** Establish that real, source-faithful specification Cards produce a bounded Prompt Delta and that the original Soodles Session, Issue Atom, Noodle Poteto stage and only **applicable** Managers actually consume the selected behavior. **Fixture PASS, Reader status and a self-reported run are not E2E PASS.**

## One owner for each fact

| Verification target | Actual required evidence | Original producer |
| --- | --- | --- |
| `card_content` | Inspected source units, missing-unit ledger, type-specific mechanism, conditions, counterexample and real technical source-to-claim correspondence | FactoryWeaver source reader and independent semantic reviewer |
| `prompt_delta` | Material change from original REQ/SPEC/G; for a changed instruction, actual admitted stage prompt and writer capture showing consumption | Original task/REQ owner and Noodle `execute` stage |
| `outer_loop` | Fresh provider Issue, accepted structured contract, original authorization and selected next | Soodles Session / `issue-atom` owner |
| `inner_loop` | Noodle session/stage capture showing selected Poteto playbook and Prompt Delta used by writer | Native Noodle `execute` carrier |
| `pclass_feedback` | Fresh native consumer, reviewed source-bound criteria, report and raw trace, original `schema pclass-feedback` response and consumed next | Soodles `review-writing` / Schema owner |
| `test_manager` | Actual smallest discriminating controls and readback when behavior requires verification; `needs_scope` remains unresolved | Original Soodles Test Manager |
| `schema_manager` | Original feedback result and proof that the returned next was consumed | Original Soodles Schema Manager, admitted stage/Task Review |
| `hook_manager` | Original native event and effect readback only if the task requires a Hook; otherwise conditional nontrigger, not a fake PASS | Original Hook Host/`hook_manager.py` |
| `cron_job_manager` | Existing authorized heartbeat and original owner continuation only if task requires Cron | Original Cron Job Manager/native heartbeat |
| `delivery` | Exact-head/Provider/Landing receipt plus the entire parent Goal's original closure | Original provider/landing owners |

## From Card verification to actual consumer

1. Source-check **every selected claim**: typed role, actual input/condition/mechanism, falsifier, necessary source coverage and link direction. Test a heading-only hallucination, reversed `validated_by`, wrong dependency and missing source against real evidence. `factoryweaver.py validate` and `card_semantic.py inspect` prove structural fields **only**; semantic acceptance still needs review of actually inspected source.
2. Verify `Prompt Delta`: the selected accepted REQ/SPEC/G must support the exact new required behavior. Generic instructions, repeated skill selection, model-authored digest/ID/argv and new unapproved Goal clauses are negative controls. No meaningful change → NOOP.
3. Use the original Host's `soodles_handoff.py --output` and fixed `reader_arguments`. The first Soodles `knowledge inspect` emits `boundary_findings` and `verification_targets`, with all native execution targets **unobserved**. This is a proof inventory, not a second state-machine runner.
4. For changed P-class Skill instructions, apply Soodles `.agents/skills/review-writing/features/pclass-feedback.md`. Select the affected cases; review each expected condition against the original requirement. In the existing authorized carrier, observe *fresh* native consumers without inherited conversation. Do not disclose expected answers to the consumer. Preserve raw reports/traces. Use original `./soodles schema pclass-feedback` and its returned `next.input`, `materialization.next.argv`, validation status, failure cases and feedback owner continuation. The Host computes existing FileRefs; the model does not fill hashes, metadata or command argv.
5. Confirm the **original** Outer Loop: a valid Issue Contract and actual admitted `issue-atom` continuation. A Reader's `next=null` is not admission. The original Noodle `execute` stage must separately show selected Poteto method and task-local delta consumption. A supervisor's statement that the playbook was chosen is insufficient.
6. Confirm Manager actions only when the original requirement and runtime trigger demand them: Test Manager selects/runs focused controls; Schema Manager returns and has its original next consumed; Hook requires native event; Cron requires previously authorized heartbeat. **Do not force every Manager to run.** An absence of Hook/Cron events is only proven when the original capture covers the relevant event window; otherwise remain UNKNOWN.
7. Reuse the **existing** Soodles `./soodles schema behavior-datasets` read-only Manager-evidence view, when the original selected Test/Hook/Cron/Schema packages exist. It separates actual source/input, observation, owner consumption, readback and missing/stale evidence. Do not duplicate its Manager state machine or convert a `partial`/self-reported record into native PASS.
8. Finally distinguish Writer Completed, Scoped Test PASS, P-class Consumer PASS, Original Owner Resolved, PR Merged/Provider Reconciled and Parent Goal Achieved; never rename the first into the last. Preserve actual unknown effects and full Requirement inventory.

## Discriminating P-class cases

B1: an actually read mechanism produces source-grounded C/SPEC; a syllabus title does not. B2: a duplicated but inconsistent Goal is not silently accepted. B3: a valid Bundle never implies Issue authorization or an executable next. B4: an unchanged Owner next results in NOOP rather than another Thinking/playbook selection. B5: missing Issue contract preserves original named refusal rather than invented admission. B6: actual Noodle writer capture, not prompt text alone, proves Prompt Delta consumption. B7: unchanged Scope must not trigger test full suite/Hook/Cron; true observed requirements use original Managers. B8: a reported P-class PASS does not assert provider or parent Goal closure.

Cases are **questions to verify through the original P-class feedback procedure**, not additional model-generated runtime fields or a new evaluator. Use objective native controls before any LLM judge; an independent judge needs error analysis, source context and calibration. Repeat only affected cases on changed instruction bytes. A causal improvement claim additionally needs comparable baseline/treatment native captures.

## Decision-state and metadata constraints

The **probabilistic** part is Session semantic interpretation of true Goal, causal scope, remaining ambiguity and necessary method. The **deterministic** part is existing CLI/owner validation, bound source/authorization, fixed method mapping, selected Test Manager controls and returned continuation. Count real decisions using the original Test Manager's observable workflow-decision calculator; incomplete capture yields unknown, not zero.

No new `SHA`, `operation_id`, `head`, `timestamp`, `case_fingerprint`, scheduler, test manager, hook registration, CLI completion state or hand-edited next. Original Host/Owner materializes identity and provides the continuation.

## Present proof ceiling

FactoryWeaver reference CI currently demonstrates its source-shape contract, not comprehensive Card semantics or P-class behavior. Soodles PR #371 native canonical runtime remains **REFUSED** before its selected controls at `issue.contract.count=0` for original pre-admission Issue #300. Without a legitimate Issue Contract, native fresh-consumer + Noodle/Manager/Provider proofs remain `NOT_RUN`, not E2E PASS. This original gate cannot be replaced by a new FactoryWeaver verifier.

## Repeated create/maintain verification skill loop (upstream pstack pinned)

The source-pinned pstack [create-verification-skill](../../.cursor/skills/create-verification-skill/SKILL.md) created one project-local [verify-factoryweaver](../../.cursor/skills/verify-factoryweaver/SKILL.md), with real public-CLI Launch/Doctor/Drive/Evidence/Cleanup and a five-feature map. The upstream [maintain-verification-skill](../../.cursor/skills/maintain-verification-skill/SKILL.md) is for **repeated** maintenance, not a separate source of acceptance authority.

Each maintenance pass indexes every feature, runs a concurrent read-only source wave, reconciles documented entry points against actual code, drives every feature (serially/isolated for CLI), and preserves output after cleanup. Real independent Agent source review is still required for domain-semantic drift; the objective helper verifies path existence and actual CLI behavior. If a proven doc/harness issue exists, edit only the verification skill directory, re-drive, and submit at most one change PR. Product regression is reported separately. `clean`, `changed` and `blocked` are maintenance outcomes, **not** native effect claims.

From the root: `python .cursor/skills/verify-factoryweaver/scripts/verify.py maintain` attempts the full scope and returns `blocked` when original Soodles/Agent capability is unavailable. `maintain --scope local` proves only the four local CLI paths. GitHub runs this local workflow twice through `tests/test_project_verification_skill.py` to ensure idempotent independent drives, retained evidence and no product mutation. To verify semantic Card completeness across all source modalities or actual Noodle/Manager activation, use the original source/Agent/Owner evidence conditions above. Do not label local pass E2E success or request a model-computed digest/argv.
