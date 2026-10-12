# FactoryWeaver v7.2 — Card Classification, Link Semantics and Scope Assembly

> **Authoritative classification extension**, read after `references/zettelkasten-v7.2.md`. This is a semantic compiler contract. It does not grant execution authority, add a card type or change `contracts/v1/knowledge-record.schema.json`. The machine validator proves structural conformance, **not** source truth, causal link validity or full semantic coverage.

## 1. Cardinality: 15 card series, 5 functional groups, 7 core series

Every card is one independently meaningful **decision-relevant concept, case, requirement or contradiction**, not one sentence, lecture, week or code file. The series follows the **kind of knowledge** being preserved, never a fixed presentation position.

| Functional group | Series | Use only when | Minimum discriminating content |
| --- | --- | --- | --- |
| Knowledge | `N` Narrative | Actual actor/event sequence changes a technical decision | Actors, tension, turning point, outcome, source |
| Knowledge | **`C` Concept (core)** | Understanding a mechanism is necessary for a scope | Mechanism, inputs/outputs, invariant/conditions, limitations, failure mode, decision it changes |
| Knowledge | `D` Detail | A particular source-backed case adds non-duplicative evidence | Specific case, condition, outcome, countercase, source |
| Knowledge | `T` Comparison | Alternatives differ along matched dimensions | Comparable choices, tradeoffs, evidence and decision boundary |
| Knowledge | `E` Essential Law | An evidence-supported generalizable derivation exists | Premises, derivation, scope of validity and counterexample; never extrapolate universally |
| Decision | `Q` Question | A genuine unresolved choice can change scope, measurement or acceptance | Exact open question, decision owner, competing answers, impact, next evidence |
| Decision | `S` Strategy | A justified intervention/hypothesis needs controlled action | Causal hypothesis, alternative, constraints, effort, measurement and stop condition |
| Decision | `R` Roadmap | Several **distinct bounded causal** atoms must be ordered | Prerequisite order and exit per atom; not a new scheduler |
| Specification | **`REQ` Requirement (core)** | A source requires an observable user/owner outcome | Actor, outcome, measurable acceptance, non-case, exact source role |
| Specification | **`SPEC` Specification (core)** | An implementation/verification boundary can be tested | Given/When/Then, typed interface, allowed/forbidden behavior, actor/owner, positive/negative/unknown/replay cases |
| Specification | **`G` Governance (core)** | A reusable, source-backed constraint has a concrete consumer | Invariant, applicability, original policy/effect owner, refusal, consequence, exception |
| Implementation | `P` Practice | A durable method/procedure is genuinely reusable | Preconditions, operations, verification and rollback; **not** Soodles `P-class` |
| Verification | **`V` Verification (core)** | A test, independent oracle or real measurement can discriminate a claim | Claim/subject, positive and negative control, evidence producer, status; `NOT_RUN` if missing |
| Verification | **`X` Conflict (core)** | Two applicable source-bound claims cannot both hold | Each exact claim and version/authority, discriminating evidence, unresolved outcome |
| Verification | **`K` Knowledge Gap (core)** | A named missing prerequisite can change a necessary decision | Missing input, why required, producer/route, dependent scopes, status |

**Core seven:** C, REQ, G, SPEC, V, X, K. They are a **coverage vocabulary**, not seven mandatory cards per Scope. For a straightforward bug fix, existing C/G may be reused and no new X/K is needed. The remaining eight series preserve depth, tradeoffs, contextual explanations and multi-atom planning.

**Fixed four-slot rendering:** the 4-slot Soodles Boot / Drill presentation is **not a 2C+1G+1SPEC recipe**. Select the four most valuable *real changes* by source-backed improvement. A batch may legitimately hold four C updates, one SPEC and three V updates, or fewer real patches and `UNUSED` terminal slots; unchanged `G` cards are linked, not recreated.

## 2. Anti-template quality gate: decision gain or NOOP

Every nontrivial CREATE/UPDATE needs a **domain-specific semantic delta**. The writer must be able to answer, in words:

1. **Mechanism:** What technical behavior/mechanism makes this claim true? Not just "Tool schema and validation".
2. **Condition:** Under what specific input, actor, state, or constraint does it apply?
3. **Consequence:** What observable runtime behavior, architectural choice, refusal or test differs because this card exists?
4. **Falsifier:** Which concrete negative case would overturn the claim?
5. **Origin:** What *actually inspected* source supports the assertion, as distinct from a linked unread title/slide?
6. **Incremental value:** What new error boundary, knowledge relation or useful question does this add beyond accepted cards?

**Reject as content-ready:**
- `Concept: Tool schema and validation. Why it matters: select a mechanism only when it changes an observable outcome.`
- `Concept: Grounding & retrieval. Connection: apply to Slides and Readings.`
- `Implement required behavior; keep tests; choose code autonomously.` (generic inner worker instructions masquerading as a Prompt Delta)
- Twelve copied Governance cards for different chapters with the same source/consumer/condition.

If a source provides only a lecture title, the honest output is a **catalog/Q/K question**, not an asserted page-grounded C. If no new knowledge exists, reuse a C/G and return `NOOP`. Content depth is proportional to the real available source, not output token budget alone.

## 3. Typed-link selection (declared meaning vs actual dependency)

Use only the relations already permitted by `contracts/v1/knowledge-record.schema.json`:

`based_on`, `derived_from`, `leads_to`, `causes`, `enables`, `contradicts`, `competes_with`, `analogous_to`, `instance_of`, `implements`, `validated_by`, `supersedes`, `depends_on`, `mitigates`.

| Relation | Source → Target must mean | Require this negative check |
| --- | --- | --- |
| `based_on` / `derived_from` | Claim demonstrably grounded in a read source/earlier premise | A bibliography listing or unread PDF is **not** content evidence |
| `depends_on` | Source **cannot satisfy its specified behavior** without target's prerequisite | Chronological or same chapter is insufficient; target failure must affect source |
| `enables` | Target capability becomes feasible because source capability exists | "Week 9 coding agents enables Week 10 vacation" is false |
| `implements` | Source specification/realization implements target REQ/interface | A concept explains a REQ but does not thereby implement it |
| `validated_by` | Source claim/behavior is evaluated by a target **V / test oracle** | `V validated_by SPEC` reverses direction; fixture does not equal live PASS |
| `contradicts` | Two relevant assertions cannot both hold under same applicability | Different versions or contexts may resolve apparent conflict |
| `mitigates` | Source control reduces a target risk/failure mode under stated condition | Mere policy mention has no proven effect |
| `supersedes` | New accepted record replaces a previous preserved record with history | No deletion/reuse of old identity |
| `competes_with` / `analogous_to` | Matched alternatives or analogy, **not prerequisite** | Do not trigger dependency invalidation from analogy |
| `leads_to` / `causes` | Evidence-supported directional consequence or causal mechanism | A lecture sequence or simple correlation does not prove causation |
| `instance_of` | One particular case belongs to target concept | Never label unrelated section headings as instances |

For **every material Scope edge**, supply a concise justification: source topic → relation → target topic; applicability; *what decision/test fails if the target changes*. If this cannot be answered, remove the edge or mark the relation as **PROPOSED / K**, not as validated fact.

The existing `card_delta.py` propagates *advisory invalidation* only through `depends_on`, `based_on`, `derived_from`, `implements`, `validated_by`. It does **not** derive semantic truth or automatically invalidate through analogy/contradiction/enabling. Do not silently change that machine contract. Scoped dependency walking must distinguish: "context useful to read" from "prerequisite invalidating acceptance".

## 4. Minimal sufficient Scope Assembly (not a Card Type)

**Four Runtime Contracts are semantic proposals, never new `series`:**

- **`ScopeManifest`** — selected outcome/REQ, relevant card closure and applicability, one causal Issue Atom, external producer/consumer and acceptance boundaries.
- **`SkillRoute`** — trigger evidence, installed capability check, *one selected* outer-loop method/skill, expected output, non-trigger, original owner continuation.
- **`PromptDelta`** — a minimal task-local change to attention/constraint/behavior **only where warranted**, otherwise explicit `NOOP`. No technical IDs/digests/cursors.
- **`Continuation`** — original whole-task REQ inventory, accepted card state, fixed batch phase, changed scopes and genuinely unfinished obligations; actual cursor from original CLI/Host only.

These contracts are **Sidecar proposals** until a consumer/schema exists; do not insert unknown keys into the closed `knowledge-record.schema.json`.

### Deterministic-first assembly algorithm

1. **Preserve original REQ inventory** independently of visible cards, assigned weeks or token budget.
2. Anchor by ONE meaningful user-visible Goal, actual measurement producer and selected REQ/SPEC acceptance. If goal/measurement ambiguous, classify the unresolved decision; do not forge metric truth.
3. Add **only relevant** C/D/T/S/P explanations necessary to make the decision or engineering interface intelligible.
4. Add existing applicable G with explicit condition and original authority. Avoid duplicate shared G; keep narrow restrictions local to SPEC.
5. Add V for the outcome and consumer, showing true producer and `NOT_RUN` until executed. Include X/K only for real material contradiction / missing prerequisite.
6. Evaluate typed links by **semantic counterfactual**: if target card were removed/changed, what required behavior or selected test actually changes? Reject decorative chronological edges.
7. Select a **single bounded causal Issue Atom** (actual callers, fixtures, tests, consumer, original owner/effect/rollback/landing responsibilities). Multi-atom parent goal stays in whole-task inventory.
8. If the original owner's returned valid next already selects the route, use **no thinking and PromptDelta=NOOP**. Otherwise Soodles Thinking Router resolves a genuine architectural/goal/causal question; only selected installed skills are eligible.
9. Outer Loop selects skills and owns lifecycle; Inner Noodle Poteto receives **bullet-list semantic Prompt Delta requirements** and is free to choose implementation within admitted scope. Do not encode an algorithm unless it is genuinely a required acceptance or a previously fixed method.
10. Source/evidence change: request targeted invalidation by real dependencies and a new `card_delta` Before/After cycle. Do not reconstruct or reuse a stale Host cursor.

### Four Scope Profiles (semantic lenses, not Card Series)

| `work_kind` | Minimum applicable knowledge | When extra decision method is justified |
| --- | --- | --- |
| Implementation | REQ + SPEC + V; reuse C/G | Unexplained failure/premise; otherwise direct `issue-atom` / selected tests |
| Architecture | C/T/S + REQ/G/SPEC/V where applicable | `think`, `high-cohesion-low-coupling` or `occams-razor` for actual tradeoff |
| Decision | Q/T/X/K only as applicable, plus affected REQ | `grilling` for real user-owned choice; never ask for inspectable facts |
| Evaluation / Optimization / Security | S/SPEC/V/G + observed D and relevant X/K | Error-discovery/audit only with installed Evals and appropriate traces; ablation for confounding; objective Code/Provider truth first |

Profiles can overlap; do not force a card family or a new Skill merely because the profile exists. Extend future scopes via **namespaced semantic sidecar fields**, not an unregistered new card series.

## 5. Positive exemplar: one HW1 Email QA Scope, four different knowledge responsibilities

**C — Grounded Retrieval**: a search tool returns inspectable candidate email IDs. A generated support citation is valid only when it refers to an ID returned in that same request; a remembered or imagined ID cannot become evidence.

**REQ — Grounded Email QA**: given a question over email archives, answer correctly enough for the course's actual test criteria without inventing a supporting email. Goal persists across separate producer and consumer atoms.

**SPEC — Answer/Support Contract**:
- Given a question, allowed search function and plain `LMCallable`;
- When the system searches, reasons and produces an answer/support;
- Then the `support` array refers exclusively to **IDs returned by search in that request**; the deterministic homework tests allow at most **three search calls**.
- Negative: malformed response, unknown support ID, zero search results or a model insisting on repeated search.
- Producer: search/BM25 adapter. Consumer: email-QA adapter. They are distinct boundaries; do not replace required BM25 scoring with Dense RAG from an illustrative reading.
- Unknown live accuracy remains `NOT_RUN` until the live evaluator actually runs.

**V — Email QA Deterministic Controls**: `tests/test_email_qa.py` checks returned support IDs, shape, zero result and bounded searches. Source-backed test expectation is **not** a recorded test PASS.

**Reusable G (linked, not re-created per batch)**: untrusted model output cannot authorize unsupported citations or tools. Applies only to relevant consumers and does not add permissions.

**Correct links (described, to be bound by registry):** `SPEC-email-qa implements REQ-email-qa`; `SPEC-email-qa based_on C-grounding`; `SPEC-email-qa validated_by V-email-qa`. On actual data, Host resolves IDs and verifies link direction/reachability. An uninspected lecture PDF does **not** become `based_on` evidence.

**Soodles Outer Loop:** `issue-atom` for contract preparation, Test Manager for exact available QA tests, `thinking-router` → adversarial-review only if a genuine unsupported-citation inference remains, optional `outer-review` after a concrete candidate. **Noodle Poteto Inner Prompt Delta**:
- Return the exact `answer` / `support` contract using only seen IDs.
- Respect the existing search-hop bound; handle empty/malformed model responses without forged support.
- Preserve provided adapter signatures and original effect boundary.
- Choose parsing/loop design within admitted scope; report actual selected tests, unresolved effects and later-owner obligations.

## 6. Explicit negative fixtures from CS329Z course pilot

- **Template failure:** `Concept: Agent-computer interface. Why it matters: select a mechanism only when it changes an observable outcome.` → **REJECT_CONTENT**: no mechanism, condition, falsifier, or decision gain.
- **Decorative link:** `W9 Coding Agents enables W10 Thanksgiving Recess` → **REJECT_EDGE**: chronology isn't capability.
- **False source claim:** assigning a figure or mechanism to Lecture 03 PDF before page inspection → **SOURCE_NOT_READ / K**.
- **Forced type recipe:** every week's 4 slots always `C, C, G, SPEC` → **REJECT_IF_NO_INDEPENDENT_CASE**: reuse G and choose actual substantive patches.
- **Forced route:** select `think` and `adversarial-review` for a known deterministic failing toy BM25 test → **ROUTING_NOOP**: use the present owner/Test Manager.
- **False closure:** `SPEC` valid JSON or writer completed means HW1 graded → **REJECT_COMPLETION**.
- **Duplication:** re-create same G constraint every week with no new applicability → **REUSE_EXISTING_CARD**.
- **Metadata fabrication:** request model-filled digest, Git HEAD, times, operation IDs or cursor → **HOST_OWNED_METADATA**, never place in generated cards or Prompt Delta.

## 7. Quality gate and evidence boundary

The compiler and `factoryweaver-verify` must produce a **scoped semantic audit** separate from the original JSON validator:
- Per proposed card: `ACCEPT | REVISE | REUSE | K_SOURCE_MISSING`, with explicit failure reason.
- Per material edge: `SUPPORTED | REJECT | UNKNOWN`, with direction and counterfactual.
- Per selected Behavior Scope: `GOAL_BOUND | NEEDS_MEASUREMENT | NEEDS_ACCEPTANCE | NEEDS_OWNER | READY_FOR_ORIGINAL_OWNER_PROPOSAL`.
- Per Prompt Delta: `ADD | REPLACE | NOOP`, with source-backed cause; generic template repeat → NOOP.
- Per completion: knowledge/pass, scoped test, native effect, provider delivery tracked independently.

These are **review vocabulary**, not extra accepted legacy JSON enums or live Evals outcomes. Require actual sources or an independent reviewer for semantic verdicts. The machine contract alone cannot prove them. Preserve corrected/rejected draft history when the original Host provides it.
