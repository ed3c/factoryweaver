---
name: factoryweaver-compile
description: Convert job descriptions, project requests, existing specs and confirmed human decisions into evidence-anchored Zettelkasten v7.2 REQ and SPEC records. Use before coding when requirements, ownership, acceptance or unknowns need explicit machine-readable contracts.
license: MIT
---
# Zettelkasten Specification Compiler v7.2

1. Read `../../references/zettelkasten-v7.2.md` for compiler invariants and human-readable card forms.
2. Keep sources, provenance, evidence and decisions separate from the resulting cards.
3. For each meaningful requirement map actor, capability, outcome, non-case, precondition, falsifier, owner, acceptance and source locator.
4. Classify source assertions by epistemic role across all fifteen Card Series. Select only required per-type prompts from `../../references/card-prompts/registry.json`; read their complete `types/` instructions. Do not force REQ/SPEC/K/X/V or any other type into each batch.
5. For unresolved human questions, keep `decision=null`, `human_confirmed=false`, and `WAIT_FOR_HUMAN`.
6. Write a `contracts/v1/knowledge-record.schema.json`-conforming data record. Verify using `python3 scripts/factoryweaver.py validate FILE` from repository root.
7. Run `project` to read the deterministic requirements status; submit any proposed capability request to host's adapter registry for independent authorization.
8. On repeated unchanged sources emit NOOP; preserve stable IDs, valid links and unresolved blockers.
9. Render selected readable cards only when material source-backed gain exists; reuse accepted cards and named evidence/unknown. Read-only `scripts/card_semantic.py select` exposes type contracts, `inspect` checks structured semantic-field shape with proof ceiling, and `managers` projects Test/Hook requests without executing them. The original `cards` command only renders materialized v1 records and never proves semantic quality.

## Two different feedback boundaries

While generating/revising a Card, the Session supplies source-bound
**card-generation feedback** about missing premises, false causal edges,
consumer-specific outputs and discriminating cases. Resolve the earliest
incorrect Card producer before accepting the record. This is not the
Soodles `PromptDelta` sidecar and does not mutate an accepted history without
its ordinary revision/source review. REUSE/NOOP when evidence brings no change.

When several causal atoms are actually needed, an R card indexes their semantic
prerequisites and already registered Card references. The read-only
`python scripts/card_semantic.py roadmap RECORD` supplies the existing
references; it neither infers membership nor selects execution order. The
current Session uses actual owner next and current evidence to choose a
minimal sufficient Scope, then composes a consumer-specific One-Shot Prompt.
Only the changed required behavior enters the existing `prompt_delta` selection;
reused constraints are referenced, not repeated as new requirements. Do not
make a new Prompt schema, author runtime metadata or reduce Worker autonomy.

## Classification and graph composition (all Hosts)

After the v7.2 System Prompt, **read [the authoritative taxonomy and Scope Assembly contract](../../references/card-classification-and-scope-assembly.md)**, including **all 15 per-series Soodles/Poteto-pstack Skill Consumers, modality-agnostic source coverage, and review-writing expectations**. All 15 card series remain available; the core seven C/REQ/G/SPEC/V/X/K are not mandatory per case. Choose series by source-supported knowledge function, not chapter position or a C,C,G,SPEC template. Reuse existing G/C across Scopes, update only after a distinct semantic gain, and leave unread PDFs as K/source catalogs.

Before emitting a card CREATE/UPDATE, use its own type-specific fields and state mechanism, condition, observable consequence, discriminating falsifier, actually inspected source and change from accepted knowledge. First preserve modality-specific source assertions (slide figure, image region, transcript turn, table population, code symbol, runtime trace as applicable) through the Host. A source/title listing is not the underlying content. Use `review-writing` semantic Source Fidelity for every engineering-facing card, but **do not invoke all mapped Skills just because cards exist**. Reject generic 'select a mechanism' payloads. Before emitting each material typed link, state relation direction, applicability and what dependent requirement or test is affected if the target changes; reject mere week-order links, false causes and reversed SPEC/verification edges. The four proposed runtime contracts (ScopeManifest, SkillRoute, PromptDelta, Continuation) are not cards. An exact valid next or already enforced CLI contract yields PromptDelta=NOOP, not a repetitive worker checklist.
## Test Manager and Hook Manager boundary

Classify the Consumer purpose before projecting needs. PR/MR source review uses the original exact candidate, task/diff and scoped check evidence; do not require unrelated Stage, Session, token or transfer metadata. Native Stop task-review still needs its original event and binding. Follow [the purpose and handoff contract](../../docs/hook-purpose-and-review-boundaries.md); a nonempty `native_event` declaration is not observed native behavior.

Before materializing, apply the taxonomy contract's
[Consumer boundary and partial parent acceptance](../../references/card-classification-and-scope-assembly.md#consumer-boundary-and-partial-parent-acceptance)
check. Do not mechanically expand each source row to REQ/SPEC/V by copying
one acceptance string. Review the selected per-type meaning and the atom's
covered/remaining clauses before exporting.

For a selected behavior, propose source-bound control inputs and expected outcomes with a **verification question and distinct negative case**. The Soodles Test Manager owns the unique actual control selection/execution and any valid `needs_scope` correction. A FactoryWeaver proposal cannot replace that selection, require full tests or reuse stale PASS.

For a real **native Hook** need, cite the original event and source-observed requirement. Soodles uses `hook_manager.py` and the native Host/Schema Manager readbacks; **there is no installed `.agents/skills/hook-manager/SKILL.md` in the inspected Soodles tree**. Do not invent one, register a handler, create a scheduler, or report execution from document text. Reuse original owner next, unknown-effect readback and native Stop recursion guard. See [Manager Consumption](../../docs/soodles-manager-consumption.md).

## Preserve prompt carrier semantics at every transform

Read [the Prompt Carrier and Original Owner Contract](../../references/prompt-carrier-and-ownership.md) when preparing a Soodles Scope. A `Card.payload` is evidence-bearing data, not a new instruction. A `PromptDelta` is a bounded semantic change to be delivered through the accepted Stage, **not** a free-standing System Prompt or Tool invocation. The selected REQ/Goal/Measurement/Stop remains a proposal until the original Soodles Issue owner reconciles current provider facts. Preserve NOOP when nothing changed. The original Host/CLI owns all machine identities and returned `next`; do not reselect fixed methods, tests, Hooks or Cron from card labels.

## Soodles Host Profile: four-slot Boot → Drill-down and goal-oriented scopes

When the selected Host is Soodles, read `../../docs/soodles-scope-routing.md` and the original task. Apply the profile **without replacing** the portable compiler, legacy v1 schema, Soodles original owners or installed skill instructions.

10. BOOT: extract the complete user-intent→REQ coverage inventory into the Host's existing record, even if far more than four obligations exist. Render exactly four visual slots with up to four truly meaningful CREATE/UPDATE cards. Empty end slots are display-only `UNUSED`, never fabricated cards.
11. DRILL: consume the last **accepted** card state and its remaining named gaps. Prefer UPDATE that strengthens behavior/goal/measurement/constraints/typed-links/Prompt Delta/Oracle/continuity. A new card needs an independently useful new concept or case. Require an explicit account of what changed since the last batch.
12. Each Behavior Scope assembles multiple reused cards into **one proposed Issue Atom causal change**. Include outcome, work kind, **Goal + Measurement + Persistence + Stop/Escalation**, entry/exit, callers, consumers, test fixtures, rollback and later owner delivery. Whole-task goals may require multiple bounded atoms; do not equate one passing atom with goal attainment.
13. Produce a **Scope Skill Trigger Plan** with observed trigger, chosen installed outer-loop skill, expected evidence, non-trigger and return/stop conditions. Always use the original `issue-atom` owner for selected atom preparation. Route goal ambiguity through Thinking Router and supported `grilling`, architecture through `think`, evaluator ambiguity through **actually installed** Evals skills only, and objective results through original metric provider/Test Manager. No automatic two-brain, unnecessary `think`, Ponytail/Waza, native Hook or Cron.
14. Produce the Noodle Poteto inner worker's **bullet-only semantic Prompt Delta requirements**. Include required outcome, constraints, forbidden behavior, measurable acceptance and writer stopping point; leave code design, implementation approach and valid playbook execution to the admitted inner worker. Do not send outer skill calls as inner work instructions.
15. Treat metadata and machine bindings as Host-owned. Model-authored prompts/cards contain no calculated digests, timestamps, IDs, cursors, paths, argv, HEADs or made-up measurement results. Materialize actual validated records only through the Host/CLI; never relax schema because the model cannot supply mechanical fields.
16. For a frozen Before/After record, the original `card_delta.py` can page with `batch_size=4` and its Host-returned cursor. **A new DRILL edit starts a new delta cycle** rather than reusing that cursor. Preserve meaningful `CONTINUE / DONE / BLOCKED / NOOP` conditions: compile DONE is not delivery DONE. Do not force four real cards when fewer changes exist.

When a real Soodles consumer requests an Issue Atom from accepted cards, produce a semantic selection over **existing** requirement/card references. Pass it to the original [FactoryWeaver → Soodles Bundle exporter](../../scripts/soodles_handoff.py) after normal knowledge-record verification. The full source record travels in one read-only bundle, so partial four-slot display does not truncate the whole-task REQ inventory. The Host supplies actual file/digest references; Soodles `knowledge inspect` reads but does **not** admit or authorize the Issue. See [consumer seam](../../docs/factoryweaver-soodles-readback.md).

Compilation is not live execution. Do not add `TESTED` or `RELEASE_CONFIRMED` without external artifacts and the original owner's readback.
**Do not re-select technical handoff identity:** When the Host requests a read-only Scope transfer, choose only existing REQ/Card references from the accepted v1 Registry and bounded behavioral changes. The original `soodles_handoff.py` with Host-selected `--output` owns exact Bundle bytes, FileRef, conflict refusal and reader arguments. No card or Skill manufactures these. Soodles still reconciles original Issue/Goal and may reject the proposal before Admission.

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

## Declared source-clause coverage

For an enumerated source, preserve its complete inspected clause inventory and run
`python3 scripts/requirement_coverage.py RECORD.json CLAUSES.json` from the repository root.
Read [the coverage contract](../../docs/requirement-coverage.md). Unmapped clauses stay
visible. Declared links do not establish source exhaustiveness or semantic fidelity.
