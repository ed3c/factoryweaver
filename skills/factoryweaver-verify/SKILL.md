---
name: factoryweaver-verify
description: Verify FactoryWeaver JSON contract validity, evidence references, human-decision boundaries, skill routing honesty and completion claims. Use before passing a specification to a software factory or reporting test, PR or delivery status.
license: MIT
---
# FactoryWeaver verification

1. Load `../../contracts/v1/knowledge-record.schema.json` and run the read-only CLI `validate` **on Host-materialized v1 data**. Before reviewing drafted Card semantics, load each *selected* contract from `../../references/card-prompts/registry.json`; `scripts/card_semantic.py inspect` checks typed fields without claiming content truth.
2. Check Source ID uniqueness, dependency and typed link reachability, and stable card IDs.
3. Require provenance before SUPPORTED, raw test evidence before TESTED, and named original owner readback before RELEASE_CONFIRMED.
4. `READY` is only a proposal. Never launch an adapter from this skill; host must check registry, identity, permission, source pins and effect boundaries.
5. Negative cases: hallucinated operation, unconfirmed human answer, invalid link, duplicate key, empty delivery receipt, unknown effect and source drift.
6. Report machine-checked proof boundary and remaining unknowns. A local fixture never proves upstream model performance or PR delivery.
## Semantic card and link gates (all Hosts)

Read [Card Classification and Scope Assembly](../../references/card-classification-and-scope-assembly.md), including **all 15 per-series Outer/Inner Skill routes, multimodal source-coverage ledger and review-writing** semantics. Validate all 15 series are preserved; the five groups and seven core types are **organizing vocabulary**, not card quotas. Review each material CREATE/UPDATE **against its own series**: C requires mechanism and failure, Q requires unresolved decision and owner, K names missing prerequisite, N reconstructs observed sequence, V requires oracle and evidence state, SPEC requires behavioral I/O. Do not require an unknown K to explain an unavailable mechanism. `review-writing` then checks relevant actor/condition/causality/state/acceptance and source fidelity. Only actually inspected sources support assertive conclusions. Generic title paraphrases and copied boilerplate must receive REVISE/REUSE, not semantic ACCEPT.

Verify each material edge's type, source/target direction and counterfactual dependency; reject 'W9 Coding Agents enables W10 Thanksgiving Recess', reverse V validated_by SPEC, and based_on attribution to an unread slide. Reuse cross-scope G and preserve named K. Ensure one causal Issue Atom assembles minimal sufficient cards and four runtime contracts are non-card sidecars. Verify task-local Prompt Delta names a **new** required behavior/constraint; no change means NOOP.

For each new/updated card confirm its **type-specific Soodles Outer Loop Consumer**, the conditional original Poteto/pstack candidate method (without fabricating installation), and a real Behavior Scope purpose. Confirm the authoritative Host extracted any image/slide/graph/audio/video/table/code/trace content claimed and preserved its content/uncertainty. An unread source URL cannot justify a technical mechanism. Use `review-writing` to assess actor, condition, causality, state, acceptance, negative and unknown claims; use real P-class behavior evals only when instructions changed. The current JSON validator checks structure and registered targets only, **not semantic sufficiency**. Report SEMANTICS_NOT_VERIFIED when independent source-content review or actual evidence is absent; never convert schema/CI fixture green into Agent behavior PASS or native effect delivery.
## E2E proof of content and effects

When the user asks for end-to-end verification, follow [the E2E verification contract](../../docs/evals/factoryweaver-e2e-card-verification.md). Judge selected Card content against **actually inspected source units** and an independent counterexample. Check whether `Prompt Delta` truly modifies the original REQ/SPEC/G boundary and does not reselect CLI/Owner paths or create permissions. Reuse Soodles' original `schema behavior-datasets` reader for selected Test/Hook/Cron/Schema Manager evidence when available, rather than adding a FactoryWeaver Manager verifier. Require actual original Soodles fresh P-class consumer evidence plus `schema pclass-feedback` and source-bound `next` consumption before calling P-class behavior observed. The Reader's `verification_targets` are not effect receipts. Admit no claims that Outer Loop, Noodle Poteto, Test Manager, Schema Manager, native Hook/Cron or Provider have run without each relevant original receipt. Do not require all managers to run; unneeded triggers must remain unselected.

## Per-hop semantic and mechanical verification

Use [the Prompt Carrier Contract](../../references/prompt-carrier-and-ownership.md) to verify that `AGENTS.md`/v7.2 instructions → selected Card types → accepted knowledge → proposed Prompt Delta → bound Bundle → Soodles Reader/Stage/Manager keeps the original Goal and no invented authority. Evaluate each hop's earliest incorrect premise and one negative control. Machine validation proves only accepted shape and source bindings; actual P-class instruction **consumption** requires fresh native Consumer and original `schema pclass-feedback` evidence; actual Outer/Inner/Manager effects require original Owners.

## Owner Manager interaction (verification never executes)

Read [Test/Hook Manager Consumption](../../docs/soodles-manager-consumption.md). The FactoryWeaver `scripts/card_semantic.py managers` projection is **advisory**; it does not select a Soodles control or native Hook, and can never override original Soodles `next`. Verify a Test Manager request has changed behavior, focused verification question and discriminating negative; no speculative full suite. Verify a Hook need comes from actual native event evidence and remains `native_execution=UNKNOWN` until its original Hook/Host receipt is observed. If no native requirement, `NO_NATIVE_HOOK_REQUIRED`. Record `NOT_RUN` and keep the Soodles manager owner responsible for real actions, consumption and landing.

## Soodles Profile: semantic batch/Scope verification

When the selected Host is Soodles, read `../../docs/soodles-scope-routing.md` and check all of the following *without* claiming real Host execution:

7. The content-batch layout has exactly four visual Card Slots; only genuine CREATE/UPDATE items count. Empty tail slots are `UNUSED` presentation, not cards or revisions. No unchanged content is recopied to fill a batch. Source→REQ ledger coverage is independent of the four-slot display.
8. BOOT maps the whole-task requested outcomes and documents pending depth. Every subsequent DRILL cites a prior accepted card/semantic gap and delivers a measurable correction to behavior boundary, Goal/Measurement, applicable constraint, knowledge-link direction, Prompt Delta, verifier or remaining obligation. If nothing improves, the correct outcome is NOOP.
9. Every Behavior Scope is a proposed Issue Atom with **Goal, Measurement, Persistence, Stop/Escalation, work kind, causal boundary, impacted callers/consumers/tests, rollback and original owner**. For long-running objectives, verify each atom is a bounded experiment and the parent goal remains open until actual metric-owner readback.
10. Verify the outer-loop Skill Trigger Plan: installed `issue-atom` for atom preparation; conditional `thinking-router`/`think`/`grilling` for genuine unresolved design or goal choice; Evals skills only after the Host confirms live availability and a concrete evaluation need; `test-manager` for focused controls; `review-writing` and P-class feedback for actual instruction changes; `outer-review` only on an observed candidate; Hook/Cron only when selected native carrier requires them. No duplicate selection where valid owner next exists.
11. Verify the inner-loop handoff consists of **bullet-point semantic Prompt Delta requirements** and admitted outcome/scope/constraints/acceptance only. Noodle Poteto is free to choose method and implementation sequence within its admitted contract. The outer loop must not turn speculative coding steps into worker obligations.
12. Check reasoning extensibility: `decision_class`, `think_skill`, `thinking_method`, Brain A/B falsifier when valuable, independent oracle, NOOP Delta where applicable, and namespaced future semantic fields. Never inject unsupported keys into `knowledge-record.schema.json` (which rejects additional properties).
13. Check metadata hygiene: Model-authored card/prompt/sidecar content does not calculate, invent or manually populate digests, HEADs, timestamps, cursors, operation IDs, paths, argv or numeric measurements. Existing Host and CLI must continue generating and validating all required mechanical fields.
14. Verify semantic continuation versus immutable delta pagination are not confused: modified DRILL after-record starts a new before/after cycle; previous CLI cursor is never reused; actual `CONTINUE / BLOCKED / DONE / NOOP` control status is preserved. Compilation completion never stands for engineering, provider effect or whole-goal completion.
15. Apply discriminating negative cases: an invented fourth card; omitted fifth source clause; child writer claiming parent p95 goal; objective latency wrongly routed to LLM judge; unavailable Evals fixture treated as installed; no-need `think` forced on valid owner next; cross-Scope hard constraint silently promoted globally; altered After with stale cursor; and native receipt synthesized from text. Keep absent producer evidence as UNKNOWN/NOT_RUN.

## Reusable pstack feature verification

The current repository has a **project-local** [verify-factoryweaver](../../.cursor/skills/verify-factoryweaver/SKILL.md) built against the actual public CLI. Its [feature map](../../.cursor/skills/verify-factoryweaver/features/README.md) and isolated harness test both valid and refused journeys; source drift is checked before each live pass. The complete upstream create/maintain methods are pinned in [UPSTREAM-PSTACK](../../.cursor/UPSTREAM-PSTACK.md), preserving the original manual invocation policy.

A real feature change requires source review and pstack `maintain-verification-skill` to run the full affected map; never silently rewrite product code inside a maintenance pass. CLI maintenance of the local subset is **not** independent semantic Card review and cannot prove outer/inner activation. Without original native Soodles Issue admission and P-class consumers, full maintenance must explicitly report `blocked`, naming those original prerequisites. Do not coerce an unavailable feature into a passing mock. The original Soodles Test Manager selects necessary live controls, and its existing P-class feedback/behavior-datasets owners verify scoped native observations, not this verification helper.

## Incremental source and structural regression controls

For independently supplied raw source bytes and a pinned manifest, run
`python3 scripts/source_lock.py MANIFEST.json SOURCE.txt`; read [source lock](../../docs/source-lock.md).
This proves only supplied byte consistency. For an accepted Before/After pair,
run `python3 scripts/card_delta.py BEFORE.json AFTER.json`; read [delta](../../docs/card-delta-contract.md).
Keep the current raw-byte cursor domain, history and non-card changes.
Run `python3 scripts/semantic_golden.py tests/fixtures/semantic-golden.json` for
curated structural regressions; read [golden](../../docs/semantic-golden.md).
`STRUCTURAL_GOLDEN_PASS` does not establish human semantic approval.
For two frozen outputs, an original evaluator may prepare
`python3 scripts/blind_review.py packet CASE.json --seed-file HOST_SEED.bin`.
Keep its separate `key` and seed with the original evaluator, outside the reviewer input.
Read [blind packet](../../docs/blind-pairwise.md). The CLI never scores models or names a winner.

## Factory Profile and Carrier boundaries

For a selected multi-factory Work Order, read [the Profile contract](../../docs/factory-profile-lock.md).
Use `python3 scripts/factory_profile.py validate PROFILE.json` and `bind-check PROFILE.json BINDING.json`.
For an original Host-selected linked checkout, `observe-local-skills PROFILE.json BINDING.json`
checks only local files; read [the Skill-view contract](../../docs/worktree-skill-view.md).
Use `python3 scripts/factory_profile.py audit-catalog PROFILE.json BINDING.json CATALOG.json`
for claimed effective Skills. Prefer `audit-catalog-pinned` with the original Owner's supplied raw pin.
`EFFECTIVE_CATALOG_CLAIM_MATCHES` means declared input consistency, never authenticated Worker discovery.
`compare-carriers PROFILE.json BASELINE_BINDING.json ALTERNATIVE_BINDING.json` compares one Work Order's claims.
It does not prove a Carrier replacement ran. Unknown owner observations remain NOT_RUN.

## Declared source-clause coverage

For an enumerated source, preserve its complete inspected clause inventory and run
`python3 scripts/requirement_coverage.py RECORD.json CLAUSES.json` from the repository root.
Read [the coverage contract](../../docs/requirement-coverage.md). Unmapped clauses stay
visible. Declared links do not establish source exhaustiveness or semantic fidelity.
