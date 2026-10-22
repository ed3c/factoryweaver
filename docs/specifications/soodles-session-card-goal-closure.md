# FactoryWeaver v7.2 — Soodles Session Card-to-Goal Closure

**Status:** Decision-complete *semantic card proposals*, not registered v1 JSON, not a Host-computed Scope Bundle, and not evidence of Native E2E. Original Registry owns IDs; original Owner owns effects. No financial runtime implementation.

## Source coverage

- User decisions: FWC-01 A (Core + financial reference), 02 B (cards then proven Core fixes), 03 A (v7.2 canonical), 04 A (Native E2E + independent Observer), 05 A (fix original owner), 06 A (Parent Goal + bounded Scope DAG), 07 A (tiered evidence); HOF-01 A and 02 A (prior handoff-only scope); QWR-01 B, 02 A, 03 A, 04 A, 05 A, 06 A, 07 A, 08 A, 09 A, 10 A, 11 A, 12 A (all reference-only).
- FactoryWeaver canonical: `references/zettelkasten-v7.2.md`, `references/card-classification-and-scope-assembly.md`, `references/card-prompts/registry.json`, `skills/factoryweaver/SKILL.md`, `docs/soodles-scope-routing.md`, `docs/factoryweaver-soodles-readback.md`.
- Soodles original consumers: `AGENTS.md`, `contracts/loop-interface.md`, `contracts/factoryweaver-scope-v1.md`, `.agents/skills/thinking-router/SKILL.md`, `.agents/skills/thinking-router/references/loop-execution.md`, `.agents/skills/ambitious-route/SKILL.md`.
- Prior handoff (not assumed merged): `ed3c/soodles` branch `docs/qwr-recursive-session-handoff-20261022`, commit `70baa9595083168224fd10162faca34f03820f00`.
- Financial reference pointers only: https://github.com/shiyu-coder/Kronos , https://arxiv.org/abs/2508.02739 , https://github.com/ginlix-ai/langalpha , https://github.com/simonlin1212/global-stock-data , https://github.com/shy3130/tick-stock-panel .
- Not observed: accepted current card Registry IDs, original authorized Issue/Task continuation, native Noodle Stage, independent Observer, a failing Core caller/consumer. Do not invent these.

## Proposed cards — canonical type semantics, provisional titles only

### REQ — Preserve Parent Human Intent
**Actor:** Human requester and original Soodles Session/Issue owner.
**Goal:** Carry Parent Goal, Measurement, Effort Horizon, source, authorization and complete Acceptance through selected FactoryWeaver scopes and authorized Poteto execution until independently observed Goal-level closure.
**Measurement:** Original owner acceptance report, selected source/card versions, actual Stage input and independent Parent clause coverage; no invented numeric threshold.
**Persistence:** Continue only on legal original next and materially new observations, preserving remaining clauses.
**Stop/escalation:** Verified evidence → VERIFIED; failed hard gate → REJECTED; unavailable independent evidence → INCONCLUSIVE; missing authority/unknown effect → BLOCKED and readback.
**Acceptance:** Child PASS never implies Parent Goal VERIFIED. **Non-case:** One card = one task; all local tests PASS = goal complete.
**Owner/rollback:** Original Soodles owner; legal revision only.

### C — Evidence-triggered Outer/Inner recursive loop
**Mechanism:** Session uses Thinking V2/conditional V3 to find earliest causal blocker, Ambitious Route to challenge outcome, chooses smallest sufficient scope; original Noodle Poteto performs authorized atomic work; readback and independent evidence return to Session.
**Inputs/outputs:** Parent Goal + source/owner → proposed Scope/one fused Prompt Delta → original admission/Stage → native observation and original next.
**Condition:** Valid original owner next takes precedence; no material new instruction means NOOP.
**Failure:** New reasoning mutates frozen Stage, duplicates scheduler, retries unknown effect, or mistakes projection for native consumption.
**Decision effect:** Reuse existing owners and CLI, do not create second Financial Truth or new route state.

### SPEC — FactoryWeaver scope to legal Soodles Consumer
**Given:** Valid canonical v7.2 record, accepted active refs, full Parent REQ inventory, Host-selected source bytes.
**When:** FactoryWeaver selects one causal Issue Atom and materializes a source-bound proposal; Soodles `knowledge inspect` reads exact Host-computed bytes.
**Then:** Reader projects selected refs and remaining REQs with `next=null`; original Session reconciles actual Issue/Task owner before admission.
**I/O:** Existing `soodles_handoff.py` output and FileRef → Soodles `factoryweaver_scope.py`/knowledge reader → original owner admission, not direct worker execution.
**Forbidden:** Model-generated IDs/digests/argv, copied full cards as worker prompt, new authority, retroactive Frozen Stage edit.
**Negative:** Stale bytes/wrong ref/wrong owner refuses. **Unknown effect:** Owner readback, no replay. **Replay:** Identical immutable output reuse, conflicting output refuses.
**Oracle/owner:** Original producer and reader tests for shape/bytes; native Host/independent observer for actual consumption.

### SPEC — Parent Goal closure is separate from child acceptance
**Given:** Parent REQ and its clauses, selected bounded scopes, actual owner observations.
**When:** A child task reports PASS or Noodle reports completed.
**Then:** Parent remains not VERIFIED until all necessary clauses are independently evidenced and original owner confirms.
**I/O:** Original Parent REQ inventory + child acceptance + native trace + provider readback + independent goal receipt.
**Forbidden:** Forged terminal receipt, downgraded Acceptance, synthetic native PASS.
**Negative:** Child PASS with uncovered Parent clause blocks closure. **Unknown/replay:** Readback, never blindly re-run.
**Oracle/owner:** Independent Observer and original Soodles Parent Goal owner. Conceptual status names must be mapped to actual schema before code changes.

### V — Source transport and refusal
**Subject:** FactoryWeaver bundle → Soodles reader. **Oracle:** Existing focused producer/reader controls and Test Manager selection. **Producer:** Original test owners.
**Positive:** Exact bytes and registered selected refs preserve remaining Parent REQs, return read-only proposal. **Negative:** Changed digest, invented ref, forged effect metadata refuses.
**Observed:** NOT_RUN for this task; prior documented fixtures do not establish fresh execution.

### V — Native consumption and goal-level closure
**Subject:** Actual unfrozen Stage consumes selected semantics; parent and child closure remain distinct.
**Oracle:** Original admitted envelope, native Consumer input/trace, provider readback, independent Observer comparing Parent Goal clauses.
**Positive:** Valid authorized task with independently verified Parent outcome. **Negative:** Projection only, false resolution, wrong owner, frozen rewrite or missing Observer cannot claim Parent VERIFIED.
**Observed:** NOT_RUN.

### K — Current Registry and Native evidence gap
**Missing:** Canonical accepted card IDs/revisions, legal original Owner next, current native Noodle trace, independent Observer and concrete failing caller.
**Why:** Cannot register/export exact Scope, claim effects, or identify justified code change without them.
**Producer/next source:** FactoryWeaver Registry/Host, Soodles Issue/Task owner, Noodle Host, independent Observer.
**Affected:** Native E2E and any code fix. **Unaffected:** Semantic card compilation, source coverage, proposed tests.
**Status:** KNOWN UNKNOWN.

### R — Bounded roadmap, not scheduler
1. Re-read fresh repository heads, existing registered cards and original Owner continuation.
2. Reuse/update existing canonical REQ/SPEC/V; validate selected record and scope via original FactoryWeaver CLI.
3. Original Host materializes exact Scope Bundle; Soodles reader verifies and returns proposal, not authority.
4. Locate earliest real failing Producer/Consumer via source and targeted negative controls. If none, NOOP, no code changes.
5. Only for demonstrated defect, follow original state-machine-change contract and fix original owner with Test Manager focused controls.
6. If legal native Host/Observer available, verify actual Stage consumption, refusal controls, original provider readback and Parent closure; otherwise report NOT_RUN/INCONCLUSIVE.
**Dependencies:** Each next unit requires preceding owner/source evidence, never a guessed argv.

## Typed links — proposals, not registered IDs
- REQ ParentIntent **depends_on** SPEC ScopeConsumer (missing source binding invalidates child evidence).
- REQ ParentIntent **depends_on** SPEC GoalClosure (child PASS cannot close parent).
- SPEC ScopeConsumer **validated_by** V Transport (stale/forged bytes must refuse).
- SPEC GoalClosure **validated_by** V NativeClosure (projection is not native proof).
- SPEC GoalClosure **depends_on** SPEC ScopeConsumer (evidence must match selected source).
- R Roadmap **based_on** REQ ParentIntent (knowledge index, not execution authority).
Original Registry/CLI must reconcile link types, direction and canonical identities.

## Non-card Scope projections
**ScopeManifest:** One bounded causal atom: prove/disprove source-bound Card → legal Consumer → native Observation → Parent clause closure, preserving other Parent REQs. Goal: source-faithful closure; Measurement: exact source/owner/native trace and independent acceptance; Persistence: evidence-driven bounded continuation; Stop: verified goal or explicit blocker.
**SkillRoute:** Unified FactoryWeaver entry, Thinking V2/conditional V3 and Ambitious only for material issue, original Soodles factoryweaver-read/issue-atom/Test Manager, Noodle Poteto through legal admission. Skill mention != invocation.
**PromptDelta:** Only if original unfrozen Consumer lacks required behavior: “Preserve complete Parent REQ inventory and exact selected source refs; report child acceptance separately from independent Parent closure; read back unknown provider effects rather than replay.” If already present, **PromptDelta=NOOP**. Advisory only.
**Continuation:** Re-read original Owner next and current refs; consume valid unchanged next or name earliest missing readback. No invented commands or permission.

## Acceptance matrix

| ID | Discriminating control | Expected | Current |
|---|---|---|---|
| AC-01 | User decision and source inventory | FWC/HOF/QWR retained, finance reference-only | SOURCE REVIEWED |
| AC-02 | Valid v1 record, selected active refs, exact bundle | Source-bound proposal, remaining Parent REQs, next=null | NOT_RUN |
| AC-03 | Stale digest, wrong ref, changed bytes | Refusal without effect | NOT_RUN |
| AC-04 | Frozen Stage receives changed Prompt Delta | No retroactive mutation | NOT_RUN |
| AC-05 | Actual native worker consumes accepted Scope | Native input/trace and original owner readback | NOT_RUN |
| AC-06 | Child PASS but Parent clause unmet | Parent not VERIFIED | NOT_RUN |
| AC-07 | Wrong owner, forged receipt, false completion | Independent rejection | NOT_RUN |
| AC-08 | Unknown write/retry | Original owner readback; no duplicate effect | NOT_RUN |
| AC-09 | No material new causal issue | PromptDelta=NOOP, original next | NOT_RUN |
| AC-10 | New counterexample changes decision | Bounded V2/conditional V3 replan, same authority | NOT_RUN |
| AC-11 | Native Observer unavailable | INCONCLUSIVE/NOT_RUN, never PASS | NOT_RUN |
| AC-12 | Several scopes pass, Parent obligation remains | Keep remaining REQ, no closure | NOT_RUN |
| AC-13 | Kronos forecast improves but net decision utility worsens | No policy promotion; no financial implementation | DESIGN ONLY |

## Mathematical financial reference (not implemented)
QWR objective: feasibility-first constrained multi-objective, preregistered utility candidate `E[log(W_T/W_0)]` with positive wealth, drawdown/turnover/exposure/cash/execution hard gates; compare incremental net utility against identical-data Rules baseline with time-series-aware uncertainty. Kronos optional forecast provider; LangAlpha research-only pattern; BTCUSDT/ETHUSDT spot; nested walk-forward, one-shot frozen holdout, historical truth and synthetic stress; shared execution semantics, paper reconciliation; RL only after evidence gate. Thresholds, windows and actual provider evidence UNKNOWN.

## Implementation / delivery decision
Existing source documents already describe the v7.2 compiler, Scope Bundle producer, Soodles read-only consumer, legal Loop owner and child-versus-parent acceptance distinction. **No specific failing Core caller/consumer has been observed in this task.** FWC-05 A forbids speculative changes; therefore no Runtime, P-class, CLI or financial code change is justified yet. Native E2E is NOT_RUN; this is not a claim of full acceptance. Next action: original Registry/Owner readback and focused native proof when available. Evidence tiers remain separate: SOURCE_REVIEWED, CONTRACT_TESTED, NATIVE_OBSERVED, PROVIDER_CONFIRMED, GOAL_VERIFIED.

## Project status
CARD_PATCH: proposed REQ/C/SPEC/SPEC/V/V/K/R, canonical IDs UNASSIGNED.
ACTION_REQUESTS: none (no Host-registered effect request).
NEXT_STATE: compilation complete for current inspected sources; **delivery INCONCLUSIVE**, awaiting original Registry/Owner/Native evidence.
