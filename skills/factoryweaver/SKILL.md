---
name: factoryweaver
description: "Single entry for Zettelkasten Specification Compiler v7.2. Use to compile or resume requirements as lossless Boot/Drill-down card batches, assemble goal-oriented Behavior Scopes and Prompt Deltas, select host skills, and verify a specification before handing it to a software factory."
license: MIT
compatibility: Requires Python 3 and jsonschema for optional machine validation; does not require GitHub access.
---

# FactoryWeaver — v7.2 unified specification entry

**Invoke this skill as `factoryweaver` for the entire specification session.**
Do not ask the caller to invoke `factoryweaver-compile`, `factoryweaver-verify`, or
a separate router manually. Those are leaf skills owned by this entry, not
alternative default launchers. One entry invocation may contain multiple
lossless Boot / Drill-down content batches. Each content batch is a bounded
rendering step, not a new Issue, worker, scheduler, or authorization.

## Mandatory reference resolution (read, do not duplicate prompts)

1. **Always read [the v7.2 System Prompt](../../references/zettelkasten-v7.2.md)
   in full before compiling**. This is the authoritative portable compiler
   contract, including I-01..I-16, card families, QG-01..34, lossless batching,
   source trust, typed links, and Completion Contract. Do not rephrase or
   replace it with this routing skill.
2. Read [compatibility boundaries](../../docs/compatibility.md) and any provided
   original task / previously accepted card registry. Discover available skills
   through this Host; a repository mention is **not** proof of installation.
3. **Only for an explicitly selected Soodles Host:** read
   [the goal-oriented Soodles profile](../../docs/soodles-scope-routing.md).
   This adds the four-slot Boot/Drill policy, Skill Trigger Matrix, Goal /
   Measurement / Persistence / Stop-Escalation, and outer / inner boundaries.
   Other consumers retain the portable v7.2 policy. Never apply Soodles
   runtime assumptions to a generic consumer.

## One dispatch per real need

Consume an unchanged, valid original Owner continuation first. If an owner
already specifies the next operation, preserve it instead of inventing a new
thinking question. For authoring, select the **minimum** necessary route:

| Observed input and intention | Leaf / responsible route | Return to this entry |
| --- | --- | --- |
| New requirement / no accepted inventory | [`factoryweaver-compile`](../factoryweaver-compile/SKILL.md) → BOOT | Source→REQ coverage, foundational cards, named pending semantics |
| Previously accepted inventory and unresolved necessary depth | `factoryweaver-compile` → DRILL | Material UPDATE/CREATE, Prompt Delta, prior-gap continuity |
| Unchanged content / valid previous continuation | No new thinking or compilation | `NOOP` or the existing Owner next |
| Explicit request to validate knowledge, links, status or handoff | [`factoryweaver-verify`](../factoryweaver-verify/SKILL.md) | Bounded validation result, false-claim refusals, gaps |
| A real unresolved architecture, goal, causality or evaluator question | Soodles `thinking-router`, only if selected/installed | One selected method, supported conclusion or named K |
| A ready, source-bound Behavior Scope needs implementation | Soodles `issue-atom` and original admission Owner **outside this Compiler** | Proposed Scope, selected outer skill triggers and worker semantic delta |
| Actual execution, publication, merge, native Hook/Cron, scheduled improvement | Original authorized Host and Soodles owners, **not this skill** | Owner-produced observation/readback or named dependency |

**Do not treat route names as executable commands.** First inspect the actual
selected leaf skill instructions. If missing, return the named unavailable
capability and continue unaffected semantic compilation. Do not fabricate a
`Skill` tool call or a model/Evals execution. A user decision belongs to the
user; inspect evidence and previous answers before asking again.

### Conditional Soodles thinking route

- `think` is for unresolved architecture / viability / decision-complete
  planning, **not** every small change.
- `grilling` is for genuinely unsettled user-owned Goal/Measurement/tradeoff
  choices; use only when the installed Host supports that route. Do not ask
  the user for evidence that the available source/Provider can supply.
- For an unresolved causal hypothesis, choose only the relevant installed
  Thinking Method. A bounded Brain A claim / Brain B counterexample is useful
  only if it changes a decision; an independent Oracle, not model consensus,
  determines the conclusion.
- Objective measurements use the original data producer / Test Manager, not
  an LLM judge. Unclear LLM evaluation with real traces may select an actually
  installed Evals skill. Frozen Evals examples are not installed capability.
- Any selected method and Prompt Delta return to the **same** Scope and
  accepted card inventory. Never restart BOOT solely due to a thinking pass.

## Host profile: Boot → Drill-down → verify

**First Boot content batch:** Preserve the *entire* original source/requirement
inventory, including requirements not displayed. Select up to four real,
high-leverage CREATE/UPDATE cards for the Soodles four-slot display; missing
terminal content becomes `UNUSED` display only. Never synthesize a card or
constraint to fill a slot.

**Subsequent Drill-down batches:** Resume from the last *accepted* card state
and named unfulfilled semantic obligations. Prefer UPDATE of existing cards.
Patch only when it materially clarifies a Behavior Scope, Goal/Measurement,
constraints, causality, verified/negative cases, Typed Links or a necessary
Prompt Delta. Record what prior gap is now settled, what evidence justifies
the change, and the next outstanding obligation. No gain means `NOOP`.

**One Behavior Scope is one proposed causal Issue Atom, not one Card.** Assemble
as many relevant concept/governance/REQ/SPEC/verification cards as needed.
Each Scope specifies: Goal, authoritative Measurement, Persistence obligation,
Stop/Escalation, work kind, entry/exit, single causal change, affected callers,
fixtures/tests/consumers, owner/effect/rollback/landing boundary, applicable
constraints, card connections, evidence, and conditional **outer-loop Skill
Trigger Plan**. New card semantic fields may be proposed in a sidecar, never
injected into `knowledge-record.schema.json` (additional properties forbidden).

**Strict work separation:** Soodles Outer Loop / `issue-atom` owns all skill
selection, authorization, lifecycle, original Owner readback, and later
reconciliation. Noodle Poteto Inner Loop receives a **bulleted list** of
already compiled Prompt Delta requirements, accepted goal/outcome, constraints,
non-cases, measurement and writer exit. Within its admitted boundaries and
selected playbook it chooses the implementation approach and correction steps
freely. Do not prescribe code line-by-line or re-route outer skills inside the
inner worker. Its completed writer stage cannot close the parent Goal.

**The four-card display is not the CLI delta limit.** The existing
`scripts/card_delta.py` supports Host-selected batches of up to twelve
changes. For Soodles use four real patches per frozen Before/After page.
A **new semantic DRILL revision creates a new Before/After cycle**;
the original CLI cursor is only for continued paging of the same frozen pair.
The Host/CLI calculates and owns all mechanical revisions, cursors,
identifiers and exact input bindings.

## Invariants and result contract

- Model-authored prompts, cards, Scope proposals and Prompt Deltas contain
  **no computed digests, Git HEADs, timestamps, numeric measurements,
  generated IDs, cursors, absolute paths or executable arguments**. Reference
  existing logical requirements and semantic objects; the original Host/CLI
  resolves and validates any required machine metadata. Never weaken validators.
- A Prompt Delta may be `NOOP` when the selected Owner continuation and skills
  already cover the needed behavior. Only a real changed instruction surface
  requires `ADD`/`REPLACE`; review actual P-class instruction changes via
  `review-writing` and scoped behavior evidence, not prose checks alone.
- For every meaningful batch, return `PROJECT_STATUS`, a four-slot Soodles
  card display when applicable, `CARD_PATCH` proposals, the assembled Scope
  and its Skill Trigger Plan, semantic inner-worker Prompt Delta bullets,
  outstanding source/constraint links, and `NEXT_STATE`. The portable
  `ACTION_REQUESTS` remain **proposals**, never effect authorizations.
- Keep knowledge, engineering and delivery axes distinct:
  `CONTINUE` = justified semantic work / frozen delta pages remain;
  `NOOP` = unchanged; `BLOCKED` = named source/owner reconciliation missing;
  `DONE` = this knowledge-compile pass is exhausted, **not** that the goal
  was achieved or the PR was delivered.
- Before describing a specification as valid, load
  `factoryweaver-verify` and perform available original read-only checks.
  Report verification as `NOT_RUN` if not actually invoked. Preserve
  unsupported/contradictory requirements in K/X cards rather than guessing.

## Stop / resume handoff

The return from this entry is a **semantic continuation**, not a second
scheduler checkpoint. Carry forward the complete requirement inventory,
accepted card graph, most recent meaningful changes, active Scope/constraints,
remaining Source→REQ obligations and unverified Goal measurement, plus the
original owner's valid next when present. Continue through already-authorized
operations; preserve any unavailable dependency without requesting the user
to repeat an answered question. Host-provided continuation and integrity
references remain outside generated prompts and cards.
