# FactoryWeaver v7.2 — P0→P1 Prioritized Acceptance and Remaining Owner Proof

**Scope:** existing FactoryWeaver PR #21 source change only. **Proof:** typed prompt selection, schema/field/link preflight, manager-needs read-only projection, Soodles original owner/source comparison, and GitHub reference CI. No native Soodles Writer, Hook, Test Manager, Schema Manager or Evals agent consumer has been launched from these documents.

## Original requirements and ordered completion readback

| Priority | Requested deliverable | What changed | What the present tests establish | What is still unknown |
| --- | --- | --- | --- | --- |
| P0-1 | 15 distinct Card Generation Contracts | `references/card-prompts/types/` contains one prompt for each of N/C/D/T/E/Q/S/R/REQ/SPEC/G/P/V/X/K; a single `registry.json` defines required semantic fields and selected file | `card_semantic.select()` returns only requested types, refuses unknown/duplicate types, verifies installed reference file for each of 15; missing fields fail | Fresh Agent generation quality, independent depth/fidelity review |
| P0-2 | Overall Prompt vs per-Card Prompt | `zettelkasten-v7.2.md` keeps global Source/I-01/Authority/Completion; selected prompt files supply type-specific semantics | tests check one entry + source of prompt contracts, CLI source resolves selected files | Actual host model honors read instructions under native Skill loading |
| P0-3 | Clear legacy forced sequencing | Replaced old D/V/X/K-first and N/C/T/SPEC/P/V output order, removed fixed JD-specific user task and invented ActionRequest example. Only source-relevant types and optional host-registered actions | static assertions check old forced D/V/X/K wording removed; no synthetic operation/ID from card prompts | No Agent runtime capture of false-extra-card rate |
| P0-4 | Per-type semantic verification | `scripts/card_semantic.py inspect` rejects missing/blank type-specific fields, title-only placeholders, unknown/unread assertive source roles, reversed validated_by, invalid link vocab/field shape and unbound declared coverage | local/CI tests exercise 15 types, negative controls and named source gaps. Output explicitly `SHAPE_VALID_SEMANTICS_UNVERIFIED` | Textual mechanism truth, semantic omissions, full source coverage, human semantic acceptance |
| P1-1 | review-writing source fidelity | The entry, per-type prompts and Verify Skill refer to Soodles review-writing (N-class prose vs actual P-class instruction feedback), with Actor/Condition/Causality/State/Acceptance separation | static prompt references and a grounded fixture are checked; no spurious rule that Practice Card means P-class | Actual installed review-writing run and its review evidence; changed P-class requires fresh behavior feedback |
| P1-2 | Scope-level SkillRoute | One original Soodles Session selects Issue Atom, conditional Thinking Router, Test Manager and original owners; non-card sidecars stay proposed. Model-generated Digest/argv/IDs remain forbidden | manager-needs tests ensure no test selected, no fake Hook run/Owner next, no effect authority | Soodles native Skills installation/readback and original Issue admission |
| P1-3 | Multimodal source coverage | Source-type rules preserve slide/page, image/figure, video/time, table/row, code/symbol and log/event distinctions; `card_semantic.inspect` consumes declared coverage, retains a K for unread material | tests refuse unbound/duplicate declared units and assert `source_completeness=NOT_VERIFIED` | A real reader has not exhausted a complete multimodal corpus; no general lossless proof |
| P1-4 | Soodles → Poteto native closed loop | [Manager consumption contract](../soodles-manager-consumption.md) maps Test Manager, Hook native code, Schema and original owner; Soodles Outer/Noodle Inner authority is preserved | FactoryWeaver tests and PR CI establish **reference-only** sidecars; no external effect claimed | **BLOCKED_BY_NATIVE_EVIDENCE**: actual installed carrier, Issue admission, selected Poteto playbook, fresh writer capture, Test Manager scope and results, native Hook/Stop/Schema/Owner readback, provider landing |

The P0/P1 order does not grant a later stage a false PASS because an earlier fixture test passed. A knowledge compilation may be DONE while runtime, delivery, model behavior or material ingestion remain unknown.

## Real manager source contracts reused

The original [Soodles test-manager Skill](https://github.com/ed3c/soodles/blob/main/.agents/skills/test-manager/SKILL.md) is the only test-selection owner. Its `ready` result is not a PASS; `needs_scope` requests a named source/consumer correction; no full-suite selection is inferred. Existing test logs/receipts, cost and CI scope belong to this owner.

[Soodles hook_manager.py](https://github.com/ed3c/soodles/blob/main/hook_manager.py) is native implementation, **not a presently installed `hook-manager/SKILL.md`** in the checked Soodles skills tree. An inspected handler artifact does not establish native execution, tool-message delivery or consumed next. Native Stop requires appropriate original binding/readback and retains Stop recursion semantics. FactoryWeaver never installs or triggers a Hook.

Soodles Schema Manager consumes **original** manager evidence; FactoryWeaver cannot replace its `next` or create a new task scheduler.

## Fresh native behavior comparison required for completion

An authorized original Soodles Session and actual Noodle carrier must independently run controlled baseline and changed Skill tasks on the **same source/requirements and compatible environment**. Select the smallest cases that separate intended differences:

1. **Card classification:** a chapter heading alone should lead to K/Q/source catalog, not content-rich C by hallucination. With actual mechanism source, generate a genuine C including behavior and falsifier.
2. **Typed link:** Week 9 Coding Agents → Week 10 Vacation should not become `enables`; for real SPEC QA claim, `validated_by` should point to actual V.
3. **Card-local semantics:** a K with absent slide PDF must name the missing source/producer without pretending to know the unknown mechanism.
4. **Original test scope:** changing Email QA support citations should produce a verification **need**, Test Manager selects discriminating cases, and a `needs_scope` refusal must remain unresolved until original owner repairs scope; no forced full suite.
5. **Native Hook non-trigger:** a schema/card/prose edit with no real native event must not register or run a Hook.
6. **Stop readback:** if native Stop is actually selected, capture original event, handler and Schema Manager response; differentiate native execution, actual next consumption, terminal task review and provider delivery. An identical later tool call alone is insufficient.
7. **Inner Worker autonomy:** Noodle Poteto receives only the precise semantic Prompt Delta, chooses actual implementation within admission, returns observed outcomes. Outer loop handles review/landing, not a second writer.
8. **Unmodified input / NOOP:** no new Card, no prompt change, no duplicate tests, and no native Hook activation when evidence and original next remain unchanged.

For each case retain real source, baseline/treatment instruction identity via **Host-computed** bindings, raw consumer capture, independent error analysis, discriminating controls and stop rule. Use Soodles `review-writing` and its scoped P-class behavior feedback for actual instruction changes; one JSON/CLI fixture PASS is not a native Agent behavior result.

**Exit:** only the original runtime/effect owner may upgrade native effect or provider delivery states after corresponding readback; otherwise report `NOT_RUN` / `BLOCKED_BY_NATIVE_EVIDENCE`. Do not add schedulers, uninstalled Hook skills, or a second Test Manager.

## Source-level example fixtures

- [Grounded HW1 Card proposal](../../examples/card-semantic/hw1-email-qa.json) — SPEC + V + K (real HW1 tester source, unread lecture gap); field/link preflight does not prove classroom completion.
- [QA Test Manager need](../../examples/card-semantic/qa-test-needs.json) — original Test Manager must select controls.
- [Uninspected Stop Hook need](../../examples/card-semantic/native-stop-needs.json) — requires source readback rather than new Hook execution.

## E2E P-class evidence update — 2026-10-13

Added the [source-to-native E2E verification protocol](factoryweaver-e2e-card-verification.md). It separates Card content, changed Prompt Delta, Reader, real fresh P-class consumer, actual Outer/Inner activation, original Test/Schema owners, conditional Hook/Cron and provider closure. Soodles Reader now exposes these as `verification_targets` in the same read; none is a fabricated runtime PASS. Original Issue #300 admission is still the native prerequisite. Changed P-class behavior is `NOT_RUN` until a fresh consumer report/raw trace and actual Schema Owner continuation exist.
