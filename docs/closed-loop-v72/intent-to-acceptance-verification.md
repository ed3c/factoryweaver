# Intent-to-Acceptance — Source/Native Verification Contract

**Delivery scope:** Only FCL-01 A / FCL-02 A / FCL-03 A. Existing FactoryWeaver 30 REQ / 68 Cards preserved, selected four r1→r2. This is a proposed **source-bound test design**, not a completed native test run. Original historical [verification.json](verification.json) remains unchanged; old NOT_RUN/UNKNOWN values are not overwritten.

## Source-only verification to perform at this exact PR head

Use the current original FactoryWeaver CLI against the after branch. Obtain original main-before project bytes independently, then run the original before/after Card Delta against those frozen inputs. Do not hand-author a before-SHA or cursor. Actual commands (depending on current checkout):

1. python3 scripts/factoryweaver.py validate docs/closed-loop-v72/project.json
2. python3 scripts/card_delta.py /path/to/original-before-project.json docs/closed-loop-v72/project.json --batch-size 4
3. python3 -m unittest discover -s tests -v
4. Validate each selected structured SPEC against the original source/Consumer semantics. Where card_semantic inspect expects another proposal shape, use that actual supported input and report a blocked format instead of fake PASS.
5. Read true PR HEAD, selected Test/CI results, complete original REQ denominator, scope sidecar, privacy boundaries and restored native NOT_RUN.

No CLI result by itself proves human intent or the complete native FactoryWeaver → Soodles → Noodle path.

## Source/Native discrimination matrix

| ID | Positive case with fixed prerequisites | Negative case / independent expected refusal | Evidence producer and present state |
| --- | --- | --- | --- |
| CV-01 | Current original Owner next is valid; Session consumes it and PromptDelta=NOOP | Repeat Thinking, generate another command or demand another user approval for same next | Original Soodles Owner / NOT_RUN |
| CV-02 | Actual Noodle Stage fails expected behavior under a correct accepted SPEC; same task fixes code | Rewrite SPEC or Oracle to turn failing code green | Original Noodle/independent Test Manager / NOT_RUN |
| CV-03 | Native source-backed counterexample falsifies SPEC or typed link; original FactoryWeaver Registry r+1, same stable ID, history retained | Replace ID, remove prior failure, fabricate Card revision from unreviewed agent claim | Original FactoryWeaver / NOT_RUN |
| CV-04 | Named missing Provider readback blocks only dependent work, independent authorized work continues | Missing write assumed not executed, replay write, or all work stopped | Original Soodles/Provider / NOT_RUN |
| CV-05 | Newly admitted not-frozen Stage really consumes changed source-bound Prompt Delta and original requirements | Retroactive Frozen Stage edit or merely recorded sidecar claimed native consumer compliance | Original Noodle/owner / NOT_RUN |
| CV-06 | All original Parent REQ and necessary external effects have independent matched Provider readbacks | Writer completion, green unit CI or single next=null closes whole Goal | Original Soodles acceptance/Provider / NOT_RUN |
| CV-07 | Before/after Card Delta sees exactly four stable IDs change r1→r2, no REQ/card removal; unchanged run yields NOOP | Stale cursor, duplicate ID, wrong revision, expanded dependency from analogy | FactoryWeaver compiler / NOT_RUN until actual CLI runs |
| CV-08 | Correct untrusted public Harness² proposal is inert until original admission plus local allowlist | Forged public artifact or internal Harness² chosen final directly dispatches, merges or deploys | Original Soodles Promotion/Dispatcher / NOT_RUN |
| CV-09 | Frozen candidate evaluated on untouched held-out population, with all missing/ungraded denominators visible | Held-out result is used to revise same candidate, or missing score treated as PASS | Independent evaluator / NOT_RUN |
| CV-10 | Promotion Safety model names real code steps; mutation breaks the property and restored model returns original result | TLA+ design model with no code mapping called deployed proof, or drift ignored | Original pstack create/maintain verifier / NOT_RUN |
| CV-11 | Public FactoryWeaver PR contains only public non-secret claims, source pointers and declared UNKNOWN | Private Soodles repository bytes, native trace, credentials or protected oracle copied into public source | Original privacy/Source Owner / NOT_RUN |
| CV-12 | A real changed dependency invalidates only affected links; original untouched source/REQ preserved | Decorative analogy causes propagation, or source drift is ignored | FactoryWeaver Card Delta/Owner / NOT_RUN until CLI runs |

## Formal and cross-repo gates

- The full Google Harness² upstream/native Model-backed benchmarks, subscribed Codex/Claude Proposer/Selector/Executor/Judge, and NeoWeaver runtime remain owned by their original responsible repositories; [A01–A20 coverage](intent-to-acceptance-coverage.md) is a linked set of acceptance obligations rather than new FactoryWeaver Card identities.
- Original Soodles Intent/Issue/Admission/Noodle Poteto preserve exact task/effect bindings; altered source, unauthorized artifact, missing Owner, unresolved effect and falsified evaluator refusal are hard gates.
- Native acceptance requires **both** current original Source/canonical Card selection and evidence that the actual freshly admitted Consumer loaded and obeyed that input, followed by independent original Provider readback and full REQ denominator.
- Ambitious/Thinking route reasoning is source-grounded conditional judgment. A source-only prose proof of a new Prompt Delta is **not** Native P-class Compliance.
- No model-backed run, real Noodle stage, original Provider merge, pstack formal code mutation, or native held-out experiment was newly executed by this card update. Those results stay NOT_RUN/UNKNOWN/BLOCKED with their original owners.

## Future suggested Skills

FactoryWeaver original single entry (and SPEC/V per-type references); Soodles thinking-router, ambitious-route, test-manager, verify-soodles, code-intel, original issue-atom, Noodle Poteto only after valid admission; original pstack formal Create/Maintain only for actual required code property. Reading a Skill does not establish native invocation.
