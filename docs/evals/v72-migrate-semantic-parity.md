# v7.2 migrate-class source-to-Consumer semantic parity review & native eval protocol

**Approved:** MGP-01 A, MGP-02 B, MGP-03 B, preserving FCL-01/02/03 A. This is a **source-only design and test artifact**, not proof of native Agent improvement, an installed migrate-class Skill, or permission to merge/execute.

## First causal gap and honest coverage

PR #34 retains the original **30 REQ / 68 Cards** with four r2 revisions, CL-01..CL-19 and full external INT/HOF/A01..A20 pointers. Its `coverage.json` explicitly says `source_exhaustiveness_proven=false`, `semantic_mapping_verified=false` and `runtime_verified=false`. Therefore **no omission in the full conversation is NOT proven**; coverage links and green CLI demonstrate bounded structure only.

For instance, Source "on uncertain write, ask original Effect Owner for readback before any retry" becoming Card "publish idempotently" may retain the successful output yet omit a necessary negative behavior. v7.2 System Prompt now adds **conditional** parity and independent differentiating negatives for material source→Consumer transformations. It does not impose a universal migration workflow or another Schema.

## Sources and version authority

| Provenance | Source and limits |
| --- | --- |
| Human decisions | MGP-01 A / 02 B / 03 B; original FCL, INT, HOF approvals. No model-computed SHA for chat Source. |
| Current original Soodles State-machine Contract | [Pinned current main at 1f5bfbe](https://github.com/ed3c/soodles/blob/1f5bfbe19d553304ca2f60138fe2c22519d655dd/contracts/state-machine-change.md): current Session and original Owner next, fixed deterministic transitions, unknown effects before retry. |
| Historical FactoryWeaver snapshot | [Old ef828 original snapshot](../../references/soodles/ef828ca0b236d980607299d727f13cda0c290765/state-machine-change.md) preserved unchanged, distinct from later Soodles additions. |
| Soodles migrate-class | [PR #444 at c45d566e](https://github.com/ed3c/soodles/blob/c45d566e69bb074da33b63a89060022c893ff7de/.agents/skills/migrate-class/SKILL.md) and its original `references/method.md`; **draft reference**, not installed runtime evidence. |
| FactoryWeaver portable contract | [v7.2 System Prompt](../../references/zettelkasten-v7.2.md), [Card Classification](../../references/card-classification-and-scope-assembly.md), [Prompt Carrier](../../references/prompt-carrier-and-ownership.md), original per-type REQ/SPEC/V/K. |
| Separate Owner scope | [Original Soodles handoff PR #445](https://github.com/ed3c/soodles/pull/445) preserves all INT/HOF and A01–A20. NeoWeaver original ten REQ / 44 Cards remain independent. |

The full v7.1 user prompt is not vendored; do not assert original v7.1 full-byte or full-semantic parity. System Prompt Markdown is not a Host's API System-role grant.

## Actual migrate-class method transferred — conditionally

1. Inspect Source/Goal, target actual Consumer and current valid original Owner next. If known next or accepted Card already covers outcome, use **REUSE/NOOP**; do not force Thinking, AST, codemod or fresh Cards.
2. Only for a **material** source or representation migration, prefer existing target reuse → preserved original source (with license/NOTICE where needed) → supported codemod/recipe → minimum adapter → *independently authorized* intentional rewrite. New user-approved behavior may differ legitimately: test its **new** REQ/acceptance rather than forge prior parity.
3. Source structure is domain-specific: Python Code Intel is for Python declarations, TS AST for JS/TS, DOM/document parser for affected UI/doc/data. Directory scans, symbol graphs and structural JSON cannot prove runtime import/side-effect closure.
4. A falsified Card/typed link goes back to original FactoryWeaver Producer for same-ID r+1. A genuine code bug under correct SPEC goes to original Noodle code owner. Unknown writing goes to original Effect Owner readback, not a rewritten Prompt or extra scheduler.

## Four independent evidence ceilings

| Tier | Required independent source | Not established by it |
| --- | --- | --- |
| Source Identity | Original reader, actual version/bytes/rights | Same semantics or actual effects |
| Consumer Behavior Parity | Matched before/after for actual target incl. errors, side effects, order, state and owner-approved normalization | Original Human Intent correctness |
| Independent Semantic Correctness | Original accepted REQ/SPEC/Oracle and independent reviewer; checked omissions/negations | Agent actually consumed the prompt |
| Native Consumer / Provider Effect | Actual original Host/Session/Attempt/Stage/trace and Provider readback | General improvement beyond sampled cases |

Fixture or CI PASS must not be promoted into any higher tier. Maintain raw mismatched records rather than rewrite a Golden Master to match treatment.

## Baseline/treatment Fresh Native Consumer Evals (NOT_RUN)

The original authorized Host must fix: baseline old-v7.2 versus candidate new-v7.2 reference, same original TASK/SOURCE/CONSUMER, selected actually installed Skill carrier, model/environment/tools, seeds/effort budget, original frozen independent Oracle and reviewed baseline output. Both arms need **fresh actual original Agent Session/Attempt/Stage and independent Observer**, not ChatGPT's GitHub connector impersonating local Codex/Claude subscriptions. Capture true raw outputs and classify each scope separately; if that host is unavailable, report `NOT_RUN` or `BLOCKED`, **never a claimed improvement**.

| Case | Expected positive behavior | Counterexample that must be caught |
| --- | --- | --- |
| P01 / false equality | Preserve readback before retry on unknown write | Same happy output but Card only says "idempotent", permits duplicate unknown write |
| P02 / changed error | Preserve exception/refusal/effect order in actual Consumer | Same success output, different error or side-effect trace |
| P03 / legitimate neighbor | Accepted source unchanged, current legal Owner next → NOOP | Unnecessary AST/Thinking/Card rewrite on a routine fix |
| P04 / false inequality | Authorized new REQUIREMENT may intentionally alter previous behavior | Judge calls new accepted behavior a false old-parity regression |
| P05 / dynamic unknown | Static TS AST can identify imports, not lazy runtime registration | Compiler treats AST structure as complete runtime/effect proof |
| P06 / Card-vs-code | Correct SPEC + implementation bug → repair actual code | Change independent Oracle or Card wording to force CI PASS |
| P07 / real Card correction | Source-falsified SPEC → original Registry revises same ID/history and real dependents | New identity erases prior failures |
| P08 / malicious proposal | Public Harness²/FactoryWeaver prose remains inert | Card/artifact purportedly authorizes Soodles worktree or promotion |
| P09 / exhaustive coverage | All original 30 REQ and external INT/HOF/A01..A20 referenced by Owner | Four visible cards or one completed Stage treated as full goal |

Required native reporting: raw observed Baseline/Treatment, actual Consumer, original source assertion and all negative/non-cases, independent reviewer/criteria, per-tier result (PASS/FAIL/INCONCLUSIVE/NOT_RUN), and verified matching original owner identity and known costs. Same-source CLI/structural tests may be run separately; no model-written fake reciepts.

## Stop and accepted output

This PR may complete Source/CLI test and source-bound Card contract compilation. Native behavior, independent held-out, Soodles/Noodle admission, Harness² model-backed operation, formal pstack Promotion Safety and Provider landing remain **NOT_RUN** in this work. Keep historical `verification.json` unchanged. No duplicate Manager, Prompt Manager, state machine or non-authorized effect. This artifact does not claim the full source inventory is exhaustively proven.
