# Migration-RL revised FactoryWeaver Cards

Canonical record: project.json. Original version preserved in history/project-before-fwp.json.

## REQ-intent | Migration-RL intent (revision 1)

Actor: Soodles supervising Session.
Goal: Human Intent Hypothesis is grounded in original requirement, preconditions and falsifier; wrong premise cannot become proven.
Measurement: Source-grounded falsification and original Owner; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Named Human Goal assumption + falsifier.
Non-case: Wrong premise promoted from text to PROVEN.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-intent, validated_by → V-intent

## SPEC-intent | Migration-RL intent executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected supervising Session consumes its actual input.
Then: Human Intent Hypothesis is grounded in original requirement, preconditions and falsifier; wrong premise cannot become proven.
Producer: Human Requirement Owner.
Consumer: supervising Session.
Inputs and conditions: original clause, source, condition and falsifier.
Outputs/refusals/effects: scoped hypothesis/unknown.
Positive: traced claim with counterexample.
Negative/falsifier: missing source but fluent conclusion.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from supervising Session; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-intent, validated_by → V-intent

## V-intent | Migration-RL intent independent verification (revision 2)

Subject: REQ-mrl-intent; not whole Human Goal.
Independent Oracle Producer: Human Requirement Owner to verify supervising Session.
Positive input/control: traced claim with counterexample; selected input original clause, source, condition and falsifier.
Negative mutation: missing source but fluent conclusion.
Expected discriminator: scoped hypothesis/unknown.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: depends_on → SPEC-intent

## REQ-rights | Migration-RL rights (revision 1)

Actor: Original Source/Admission Owner.
Goal: Source rights and identity admissible; unlicensed asset, wrong SHA or wrong target refused.
Measurement: Source license+NOTICE+Owner admission; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Explicit licensed source/asset and one admitted writable target.
Non-case: Incompatible asset/foreign worktree authorized.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-MIGRATE, SRC-ISSUE
Typed Links: implements → REQ-mrl-rights, validated_by → V-rights, depends_on → REQ-mrl-intent

## SPEC-rights | Migration-RL rights executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected migration source selector consumes its actual input.
Then: Source rights and identity admissible; unlicensed asset, wrong SHA or wrong target refused.
Producer: rights/admission owner.
Consumer: migration source selector.
Inputs and conditions: source revision, per-asset licenses, original Worktree scope.
Outputs/refusals/effects: admissible/refused/unknown.
Positive: legal Source and selected target.
Negative/falsifier: unlicensed sub-asset or foreign repo.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from migration source selector; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-MIGRATE, SRC-ISSUE
Typed Links: implements → REQ-mrl-rights, validated_by → V-rights, depends_on → REQ-mrl-intent

## V-rights | Migration-RL rights independent verification (revision 2)

Subject: REQ-mrl-rights; not whole Human Goal.
Independent Oracle Producer: rights/admission owner to verify migration source selector.
Positive input/control: legal Source and selected target; selected input source revision, per-asset licenses, original Worktree scope.
Negative mutation: unlicensed sub-asset or foreign repo.
Expected discriminator: admissible/refused/unknown.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-MIGRATE, SRC-ISSUE
Typed Links: depends_on → SPEC-rights

## REQ-retrieval | Migration-RL retrieval (revision 1)

Actor: Code-intel + independent evaluator.
Goal: Actual task-level AST/SCIP Migration Dependency Retrieval measures target Precision ≥99% against frozen ground truth and publishes Recall/Coverage/abstentions.
Measurement: Frozen TP/FP/FN, Precision/Recall/Coverage; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Task-relevant symbol and dependency retrieval on frozen JS/TS AST+SCIP.
Non-case: Only one easy correct hit and omitted critical deps.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-CODE
Typed Links: implements → REQ-mrl-retrieval, validated_by → V-retrieval, depends_on → REQ-mrl-rights

## SPEC-retrieval | Migration-RL retrieval executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected independent retrieval evaluator consumes its actual input.
Then: Actual task-level AST/SCIP Migration Dependency Retrieval measures target Precision ≥99% against frozen ground truth and publishes Recall/Coverage/abstentions.
Producer: actual JS/TS AST+SCIP Indexer.
Consumer: independent retrieval evaluator.
Inputs and conditions: compiler configuration, labeled symbol/consumer/asset population.
Outputs/refusals/effects: TP/FP/FN, precision/recall/coverage/abstention.
Positive: labeled definition and consumer reference.
Negative/falsifier: one easy hit hides missed dynamic edge.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from independent retrieval evaluator; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-CODE
Typed Links: implements → REQ-mrl-retrieval, validated_by → V-retrieval, depends_on → REQ-mrl-rights

## V-retrieval | Migration-RL retrieval independent verification (revision 2)

Subject: REQ-mrl-retrieval; not whole Human Goal.
Independent Oracle Producer: actual JS/TS AST+SCIP Indexer to verify independent retrieval evaluator.
Positive input/control: labeled definition and consumer reference; selected input compiler configuration, labeled symbol/consumer/asset population.
Negative mutation: one easy hit hides missed dynamic edge.
Expected discriminator: TP/FP/FN, precision/recall/coverage/abstention.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-CODE
Typed Links: depends_on → SPEC-retrieval

## REQ-deps | Migration-RL deps (revision 1)

Actor: Selected Consumer owner.
Goal: Dependency closure spans symbols, imports, registrations, assets and observed dynamic edges; missing critical edge blocks `CLOSED`.
Measurement: Static graph plus real runtime dynamic trace; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Imports, registrations, assets and runtime edges traced.
Non-case: Dynamic missing edge called CLOSED.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-CODE
Typed Links: implements → REQ-mrl-deps, validated_by → V-deps, depends_on → REQ-mrl-retrieval

## SPEC-deps | Migration-RL deps executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected dependency closure verifier consumes its actual input.
Then: Dependency closure spans symbols, imports, registrations, assets and observed dynamic edges; missing critical edge blocks `CLOSED`.
Producer: AST+SCIP structural producer and native dynamic trace.
Consumer: dependency closure verifier.
Inputs and conditions: imports, CSS/assets, dynamic registration and side-effect edges.
Outputs/refusals/effects: supported/unknown critical dependencies.
Positive: import and runtime handler both observed.
Negative/falsifier: critical handler omitted but closure called complete.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from dependency closure verifier; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-CODE
Typed Links: implements → REQ-mrl-deps, validated_by → V-deps, depends_on → REQ-mrl-retrieval

## V-deps | Migration-RL deps independent verification (revision 2)

Subject: REQ-mrl-deps; not whole Human Goal.
Independent Oracle Producer: AST+SCIP structural producer and native dynamic trace to verify dependency closure verifier.
Positive input/control: import and runtime handler both observed; selected input imports, CSS/assets, dynamic registration and side-effect edges.
Negative mutation: critical handler omitted but closure called complete.
Expected discriminator: supported/unknown critical dependencies.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-CODE
Typed Links: depends_on → SPEC-deps

## REQ-runtimes | Migration-RL runtimes (revision 1)

Actor: AgentEnv Environment Owner.
Goal: Original and target are separately executed native runtimes, not REA/HAR replay masquerading as execution.
Measurement: Native process traces under fixed images; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Separate original and target programs execute identical input.
Non-case: HAR Replay treated as actual process.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-AGENTENV, SRC-REA
Typed Links: implements → REQ-mrl-runtimes, validated_by → V-runtimes, depends_on → REQ-mrl-rights, depends_on → REQ-mrl-deps

## SPEC-runtimes | Migration-RL runtimes executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected independent paired runtime Consumer consumes its actual input.
Then: Original and target are separately executed native runtimes, not REA/HAR replay masquerading as execution.
Producer: original and target native process owners.
Consumer: independent paired runtime Consumer.
Inputs and conditions: matched math/UI fixture, pinned versions, real process launch.
Outputs/refusals/effects: separate output/error/DOM/event traces.
Positive: two actual programs run matched input.
Negative/falsifier: HAR Replay substitutes for source process.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from independent paired runtime Consumer; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-AGENTENV, SRC-REA
Typed Links: implements → REQ-mrl-runtimes, validated_by → V-runtimes, depends_on → REQ-mrl-rights, depends_on → REQ-mrl-deps

## V-runtimes | Migration-RL runtimes independent verification (revision 2)

Subject: REQ-mrl-runtimes; not whole Human Goal.
Independent Oracle Producer: original and target native process owners to verify independent paired runtime Consumer.
Positive input/control: two actual programs run matched input; selected input matched math/UI fixture, pinned versions, real process launch.
Negative mutation: HAR Replay substitutes for source process.
Expected discriminator: separate output/error/DOM/event traces.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-AGENTENV, SRC-REA
Typed Links: depends_on → SPEC-runtimes

## REQ-mutation | Migration-RL mutation (revision 1)

Actor: Original Noodle Worktree Owner.
Goal: Authorized action changes actual target worktree/program state; foreign/unauthorized mutation is refused.
Measurement: Worktree diff and original Owner effect receipt; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Authorized target modification changes actual file.
Non-case: Agent writes upstream or frozen target.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-MIGRATE, SRC-ISSUE
Typed Links: implements → REQ-mrl-mutation, validated_by → V-mutation, depends_on → REQ-mrl-rights

## SPEC-mutation | Migration-RL mutation executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected authorized target Worktree consumes its actual input.
Then: Authorized action changes actual target worktree/program state; foreign/unauthorized mutation is refused.
Producer: original admitted Noodle Stage.
Consumer: authorized target Worktree.
Inputs and conditions: allowed write path and Owner next.
Outputs/refusals/effects: actual diff/effect or refused/unknown.
Positive: authorized patch visible in target.
Negative/falsifier: foreign write or Frozen Stage mutation.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from authorized target Worktree; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-MIGRATE, SRC-ISSUE
Typed Links: implements → REQ-mrl-mutation, validated_by → V-mutation, depends_on → REQ-mrl-rights

## V-mutation | Migration-RL mutation independent verification (revision 2)

Subject: REQ-mrl-mutation; not whole Human Goal.
Independent Oracle Producer: original admitted Noodle Stage to verify authorized target Worktree.
Positive input/control: authorized patch visible in target; selected input allowed write path and Owner next.
Negative mutation: foreign write or Frozen Stage mutation.
Expected discriminator: actual diff/effect or refused/unknown.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-MIGRATE, SRC-ISSUE
Typed Links: depends_on → SPEC-mutation

## REQ-reset | Migration-RL reset (revision 1)

Actor: AgentEnv Sandbox Owner.
Goal: Mutation→Reset→readback restores clean worktree/process/browser/fixture state without cross-episode contamination.
Measurement: Before/after isolated state readbacks; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Mutate file/cookie/process; reset restores clean seed.
Non-case: Reset returns OK with stale process/cookie.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-AGENTENV, SRC-REA
Typed Links: implements → REQ-mrl-reset, validated_by → V-reset, depends_on → REQ-mrl-runtimes, depends_on → REQ-mrl-mutation

## SPEC-reset | Migration-RL reset executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected independent episode reset verifier consumes its actual input.
Then: Mutation→Reset→readback restores clean worktree/process/browser/fixture state without cross-episode contamination.
Producer: actual AgentEnv state/reset adapter.
Consumer: independent episode reset verifier.
Inputs and conditions: mutated file, cookie, process, seed.
Outputs/refusals/effects: clean snapshot or residual state.
Positive: mutate and compare clean restored state.
Negative/falsifier: reset OK while stale process remains.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from independent episode reset verifier; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-AGENTENV, SRC-REA
Typed Links: implements → REQ-mrl-reset, validated_by → V-reset, depends_on → REQ-mrl-runtimes, depends_on → REQ-mrl-mutation

## V-reset | Migration-RL reset independent verification (revision 2)

Subject: REQ-mrl-reset; not whole Human Goal.
Independent Oracle Producer: actual AgentEnv state/reset adapter to verify independent episode reset verifier.
Positive input/control: mutate and compare clean restored state; selected input mutated file, cookie, process, seed.
Negative mutation: reset OK while stale process remains.
Expected discriminator: clean snapshot or residual state.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-AGENTENV, SRC-REA
Typed Links: depends_on → SPEC-reset

## REQ-math | Migration-RL math (revision 1)

Actor: Independent mathematical Oracle.
Goal: Mathematical parity validates differential results, properties, metamorphic/boundary inputs and predeclared numeric error policy.
Measurement: Paired native math+properties/edge cases; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Matched input, epsilon fixed before result, property/metamorphic/boundaries.
Non-case: Error type differs or epsilon adjusted after candidate.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-PILOT
Typed Links: implements → REQ-mrl-math, validated_by → V-math, depends_on → REQ-mrl-runtimes

## SPEC-math | Migration-RL math executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected independent property Oracle consumes its actual input.
Then: Mathematical parity validates differential results, properties, metamorphic/boundary inputs and predeclared numeric error policy.
Producer: source and target AIFS engine.
Consumer: independent property Oracle.
Inputs and conditions: same slider domain and predeclared epsilon/boundary.
Outputs/refusals/effects: numbers/NaN/errors and property outcomes.
Positive: matched real computation satisfies invariant.
Negative/falsifier: epsilon changed after candidate fails.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from independent property Oracle; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-PILOT
Typed Links: implements → REQ-mrl-math, validated_by → V-math, depends_on → REQ-mrl-runtimes

## V-math | Migration-RL math independent verification (revision 2)

Subject: REQ-mrl-math; not whole Human Goal.
Independent Oracle Producer: source and target AIFS engine to verify independent property Oracle.
Positive input/control: matched real computation satisfies invariant; selected input same slider domain and predeclared epsilon/boundary.
Negative mutation: epsilon changed after candidate fails.
Expected discriminator: numbers/NaN/errors and property outcomes.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-PILOT
Typed Links: depends_on → SPEC-math

## REQ-interfaces | Migration-RL interfaces (revision 1)

Actor: Interface Contract Owner.
Goal: Producer→Consumer guarantees and Consumer→Producer prerequisites/feedback/exception obligations are both tested in scope.
Measurement: Typed interface and native return/error trace; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Producer guarantee satisfies consumer accepted domain and feedback/ack.
Non-case: Lost acknowledgment or required inverse hash.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-interfaces, validated_by → V-interfaces, depends_on → REQ-mrl-deps, depends_on → REQ-mrl-runtimes

## SPEC-interfaces | Migration-RL interfaces executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected two-sided interface Consumer consumes its actual input.
Then: Producer→Consumer guarantees and Consumer→Producer prerequisites/feedback/exception obligations are both tested in scope.
Producer: module Producer.
Consumer: two-sided interface Consumer.
Inputs and conditions: producer values, accepted domain and required ack/error.
Outputs/refusals/effects: forward acceptance and reverse feedback.
Positive: actual input accepted with ack.
Negative/falsifier: missing error ack with same forward value.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from two-sided interface Consumer; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-interfaces, validated_by → V-interfaces, depends_on → REQ-mrl-deps, depends_on → REQ-mrl-runtimes

## V-interfaces | Migration-RL interfaces independent verification (revision 2)

Subject: REQ-mrl-interfaces; not whole Human Goal.
Independent Oracle Producer: module Producer to verify two-sided interface Consumer.
Positive input/control: actual input accepted with ack; selected input producer values, accepted domain and required ack/error.
Negative mutation: missing error ack with same forward value.
Expected discriminator: forward acceptance and reverse feedback.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: depends_on → SPEC-interfaces

## REQ-ui-effects | Migration-RL ui-effects (revision 1)

Actor: Browser Consumer Owner.
Goal: Selected DOM/ARIA/focus/events/network/filesystem/persistence behavior and side-effect order remain contracted.
Measurement: Chromium native DOM+event+effect trace; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Selected DOM/ARIA/focus/event/side-effects contract equivalent.
Non-case: Removed SeeCode edge or event reorder hidden by image.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-PILOT
Typed Links: implements → REQ-mrl-ui-effects, validated_by → V-ui-effects, depends_on → REQ-mrl-interfaces, depends_on → REQ-mrl-runtimes

## SPEC-ui-effects | Migration-RL ui-effects executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected independent Browser differential consumes its actual input.
Then: Selected DOM/ARIA/focus/events/network/filesystem/persistence behavior and side-effect order remain contracted.
Producer: source SeeCode Renderer and migrated Browser.
Consumer: independent Browser differential.
Inputs and conditions: four nodes/three edges and step/focus actions.
Outputs/refusals/effects: DOM/ARIA/focus/ordered effects.
Positive: source and target preserve edge and focus.
Negative/falsifier: edge removed but screenshot matches.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from independent Browser differential; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-PILOT
Typed Links: implements → REQ-mrl-ui-effects, validated_by → V-ui-effects, depends_on → REQ-mrl-interfaces, depends_on → REQ-mrl-runtimes

## V-ui-effects | Migration-RL ui-effects independent verification (revision 2)

Subject: REQ-mrl-ui-effects; not whole Human Goal.
Independent Oracle Producer: source SeeCode Renderer and migrated Browser to verify independent Browser differential.
Positive input/control: source and target preserve edge and focus; selected input four nodes/three edges and step/focus actions.
Negative mutation: edge removed but screenshot matches.
Expected discriminator: DOM/ARIA/focus/ordered effects.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-PILOT
Typed Links: depends_on → SPEC-ui-effects

## REQ-false-inference | Migration-RL false-inference (revision 1)

Actor: Original Test Manager and independent Evals.
Goal: Plant false-equivalence, bad error, order and over-inference negatives; verifier rejects them.
Measurement: Selected discriminating negative controls; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Known good and planted false-equivalence negative controls.
Non-case: Same happy path excuses wrong exception/order.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-false-inference, validated_by → V-false-inference, depends_on → REQ-mrl-math, depends_on → REQ-mrl-ui-effects

## SPEC-false-inference | Migration-RL false-inference executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected Test Manager-selected independent verifier consumes its actual input.
Then: Plant false-equivalence, bad error, order and over-inference negatives; verifier rejects them.
Producer: original Source/Runtime Owner.
Consumer: Test Manager-selected independent verifier.
Inputs and conditions: normal case and planted exception/order mismatch.
Outputs/refusals/effects: honest scoped verdict.
Positive: scope-limited PASS with untested cases unknown.
Negative/falsifier: same output but changed effects accepted.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from Test Manager-selected independent verifier; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-false-inference, validated_by → V-false-inference, depends_on → REQ-mrl-math, depends_on → REQ-mrl-ui-effects

## V-false-inference | Migration-RL false-inference independent verification (revision 2)

Subject: REQ-mrl-false-inference; not whole Human Goal.
Independent Oracle Producer: original Source/Runtime Owner to verify Test Manager-selected independent verifier.
Positive input/control: scope-limited PASS with untested cases unknown; selected input normal case and planted exception/order mismatch.
Negative mutation: same output but changed effects accepted.
Expected discriminator: honest scoped verdict.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: depends_on → SPEC-false-inference

## REQ-reward | Migration-RL reward (revision 1)

Actor: AgentEnv Task Verifier and original outcome Owner.
Goal: Reward is independent and resists forged trace, agent self-score, changed Oracle and insufficient hard-gate evidence.
Measurement: Independent recomputed reward and receipts; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Independent hard gates all observed true.
Non-case: Self-report or changed Golden yields reward one.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-reward, validated_by → V-reward, depends_on → REQ-mrl-rights, depends_on → REQ-mrl-runtimes, depends_on → REQ-mrl-false-inference

## SPEC-reward | Migration-RL reward executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected AgentEnv outcome grader consumes its actual input.
Then: Reward is independent and resists forged trace, agent self-score, changed Oracle and insufficient hard-gate evidence.
Producer: independent rights/parity/Native Owners.
Consumer: AgentEnv outcome grader.
Inputs and conditions: all actually evaluated hard gate receipts.
Outputs/refusals/effects: success only for fully observed accepted migration.
Positive: independent reward recomputation matches.
Negative/falsifier: Candidate self-score or unknown gate yields 1.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from AgentEnv outcome grader; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-reward, validated_by → V-reward, depends_on → REQ-mrl-rights, depends_on → REQ-mrl-runtimes, depends_on → REQ-mrl-false-inference

## V-reward | Migration-RL reward independent verification (revision 2)

Subject: REQ-mrl-reward; not whole Human Goal.
Independent Oracle Producer: independent rights/parity/Native Owners to verify AgentEnv outcome grader.
Positive input/control: independent reward recomputation matches; selected input all actually evaluated hard gate receipts.
Negative mutation: Candidate self-score or unknown gate yields 1.
Expected discriminator: success only for fully observed accepted migration.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: depends_on → SPEC-reward

## REQ-cards | Migration-RL cards (revision 1)

Actor: FactoryWeaver original Card Producer.
Goal: Native Evals are source-bound to correct SPEC/V/G revisions via original FactoryWeaver producer; unsupported changes do not become truth.
Measurement: Original card producer/Owner revision and Evals; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Observed failure produces source-bound SPEC/V/G revision proposal.
Non-case: Candidate failure causes rewriting oracle.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-FW-CARDS
Typed Links: implements → REQ-mrl-cards, validated_by → V-cards, depends_on → REQ-mrl-intent, depends_on → REQ-mrl-false-inference

## SPEC-cards | Migration-RL cards executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected versioned SPEC/V/G/K/X consumes its actual input.
Then: Native Evals are source-bound to correct SPEC/V/G revisions via original FactoryWeaver producer; unsupported changes do not become truth.
Producer: independent Evals & FactoryWeaver producer.
Consumer: versioned SPEC/V/G/K/X.
Inputs and conditions: original REQ/Card, real trace and falsifier.
Outputs/refusals/effects: original revision proposal or NOOP.
Positive: actual falsifier suggests precise card correction.
Negative/falsifier: candidate fails and rewrites Golden.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from versioned SPEC/V/G/K/X; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-FW-CARDS
Typed Links: implements → REQ-mrl-cards, validated_by → V-cards, depends_on → REQ-mrl-intent, depends_on → REQ-mrl-false-inference

## V-cards | Migration-RL cards independent verification (revision 2)

Subject: REQ-mrl-cards; not whole Human Goal.
Independent Oracle Producer: independent Evals & FactoryWeaver producer to verify versioned SPEC/V/G/K/X.
Positive input/control: actual falsifier suggests precise card correction; selected input original REQ/Card, real trace and falsifier.
Negative mutation: candidate fails and rewrites Golden.
Expected discriminator: original revision proposal or NOOP.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-FW-CARDS
Typed Links: depends_on → SPEC-cards

## REQ-invalidation | Migration-RL invalidation (revision 1)

Actor: FactoryWeaver Card Producer.
Goal: Source revision change, stale evidence, wrong card version, missing link and dependency updates yield targeted invalidation/recovery.
Measurement: Original card_delta and dependent consumer check; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Changed SPEC invalidates dependent V while preserving history.
Non-case: Deletes/recycles card ID or analogue causes false invalidation.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-FW-CARDS
Typed Links: implements → REQ-mrl-invalidation, validated_by → V-invalidation, depends_on → REQ-mrl-cards

## SPEC-invalidation | Migration-RL invalidation executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected card_delta affected consumer consumes its actual input.
Then: Source revision change, stale evidence, wrong card version, missing link and dependency updates yield targeted invalidation/recovery.
Producer: actual original FactoryWeaver before/after.
Consumer: card_delta affected consumer.
Inputs and conditions: stable IDs, old/new content, directed links.
Outputs/refusals/effects: revision/history and affected_nodes.
Positive: SPEC change invalidates dependent V.
Negative/falsifier: old ID deleted or analogy treated as prerequisite.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from card_delta affected consumer; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-FW-CARDS
Typed Links: implements → REQ-mrl-invalidation, validated_by → V-invalidation, depends_on → REQ-mrl-cards

## V-invalidation | Migration-RL invalidation independent verification (revision 2)

Subject: REQ-mrl-invalidation; not whole Human Goal.
Independent Oracle Producer: actual original FactoryWeaver before/after to verify card_delta affected consumer.
Positive input/control: SPEC change invalidates dependent V; selected input stable IDs, old/new content, directed links.
Negative mutation: old ID deleted or analogy treated as prerequisite.
Expected discriminator: revision/history and affected_nodes.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-FW-CARDS
Typed Links: depends_on → SPEC-invalidation

## REQ-session | Migration-RL session (revision 2)

Actor: Soodles supervising Owner; Noodle Host.
Goal: In the same supervising Session, Source/Owner-bound Outer reasoning (or NOOP) is consumed by the next authorized unsealed Poteto Stage; real inner feedback changes only warranted subsequent decisions/cards. Fresh Native Consumer and original Owner readback prove the handoff, not documentation.
Measurement: Actual Stage inputs, result, original Owner next; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: One fused Delta/NOOP consumed in next legal unsealed Stage.
Non-case: Frozen Stage overwritten or local pass closes all.
Correction: an authorized Outer/Inner Session can start and later discover a required Card revision.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-session, validated_by → V-session, depends_on → REQ-mrl-intent, depends_on → REQ-mrl-mutation

## SPEC-session | Migration-RL session executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected admitted unsealed Poteto Stage consumes its actual input.
Then: In the same supervising Session, Source/Owner-bound Outer reasoning (or NOOP) is consumed by the next authorized unsealed Poteto Stage; real inner feedback changes only warranted subsequent decisions/cards. Fresh Native Consumer and original Owner readback prove the handoff, not documentation.
Producer: current Soodles Session and valid Owner next.
Consumer: admitted unsealed Poteto Stage.
Inputs and conditions: full original Goal and minimal Delta/NOOP.
Outputs/refusals/effects: native stage consumption and Owner readback.
Positive: NOOP valid next continues.
Negative/falsifier: Frozen Stage changed or card prerequisite invented.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from admitted unsealed Poteto Stage; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-session, validated_by → V-session, depends_on → REQ-mrl-intent, depends_on → REQ-mrl-mutation

## V-session | Migration-RL session independent verification (revision 2)

Subject: REQ-mrl-session; not whole Human Goal.
Independent Oracle Producer: current Soodles Session and valid Owner next to verify admitted unsealed Poteto Stage.
Positive input/control: NOOP valid next continues; selected input full original Goal and minimal Delta/NOOP.
Negative mutation: Frozen Stage changed or card prerequisite invented.
Expected discriminator: native stage consumption and Owner readback.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: depends_on → SPEC-session

## REQ-baseline | Migration-RL baseline (revision 1)

Actor: Test Manager + Evals Supervisor.
Goal: Evaluation-first reproducible baseline, proper held-out split, success/failure/cost/latency/refusal/coverage metrics.
Measurement: Real comparable episodes and denominators; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Matched deterministic/untuned runs and held-out family/cost.
Non-case: Different budget or zero successes cost=0.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-baseline, validated_by → V-baseline, depends_on → REQ-mrl-reset, depends_on → REQ-mrl-reward

## SPEC-baseline | Migration-RL baseline executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected independent held-out evaluator consumes its actual input.
Then: Evaluation-first reproducible baseline, proper held-out split, success/failure/cost/latency/refusal/coverage metrics.
Producer: native episodes and Test Manager costs.
Consumer: independent held-out evaluator.
Inputs and conditions: matched budget/model/task family and real cost.
Outputs/refusals/effects: comparable success/refusal/latency/cost.
Positive: same-budget baseline and treatment.
Negative/falsifier: different budget credited to RL.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from independent held-out evaluator; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-baseline, validated_by → V-baseline, depends_on → REQ-mrl-reset, depends_on → REQ-mrl-reward

## V-baseline | Migration-RL baseline independent verification (revision 2)

Subject: REQ-mrl-baseline; not whole Human Goal.
Independent Oracle Producer: native episodes and Test Manager costs to verify independent held-out evaluator.
Positive input/control: same-budget baseline and treatment; selected input matched budget/model/task family and real cost.
Negative mutation: different budget credited to RL.
Expected discriminator: comparable success/refusal/latency/cost.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: depends_on → SPEC-baseline

## REQ-training | Migration-RL training (revision 1)

Actor: Later Policy Training Owner.
Goal: RL-ready vs trained-policy outcomes remain separate; no training improvement claims without actual controlled weights/checkpoints/held-out comparison.
Measurement: Separate checkpoints and trained-heldout comparison; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: RL-ready verified episodes kept distinct from trained weights.
Non-case: Replay success labeled RL-trained.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-training, validated_by → V-training, depends_on → REQ-mrl-baseline

## SPEC-training | Migration-RL training executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected held-out trained policy evaluator consumes its actual input.
Then: RL-ready vs trained-policy outcomes remain separate; no training improvement claims without actual controlled weights/checkpoints/held-out comparison.
Producer: future training/checkpoint Owner.
Consumer: held-out trained policy evaluator.
Inputs and conditions: verified episodes, separate training grant.
Outputs/refusals/effects: RL-ready now, RL-trained only future.
Positive: no checkpoints -> NOT_RUN.
Negative/falsifier: Replay called trained checkpoint.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from held-out trained policy evaluator; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-training, validated_by → V-training, depends_on → REQ-mrl-baseline

## V-training | Migration-RL training independent verification (revision 2)

Subject: REQ-mrl-training; not whole Human Goal.
Independent Oracle Producer: future training/checkpoint Owner to verify held-out trained policy evaluator.
Positive input/control: no checkpoints -> NOT_RUN; selected input verified episodes, separate training grant.
Negative mutation: Replay called trained checkpoint.
Expected discriminator: RL-ready now, RL-trained only future.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: depends_on → SPEC-training

## REQ-closure | Migration-RL closure (revision 1)

Actor: Original Parent Goal/Delivery Owner.
Goal: Whole original Human Goal **and** applicable FactoryWeaver card obligations (revision/NOOP + native consumer uptake), remaining REQ inventory, real independent evidence and original Owner effect/readback converge; partial green, card DONE, unknown-write or cognitive NOOP cannot falsely close the parent goal.
Measurement: Owner reconciliation of all parent obligations; actual native metrics NOT_RUN.
Persistence: preserve this and all parent REQs across authorized bounded attempts.
Stop/Escalation: incomplete or unknown evidence blocks only dependent work, never claims whole completion.
Acceptance: Full REQ plus Cards obligations and original effects closed.
Non-case: Card DONE while human REQ open or unknown write.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-closure, validated_by → V-closure, depends_on → REQ-mrl-session, depends_on → REQ-mrl-invalidation, depends_on → REQ-mrl-baseline

## SPEC-closure | Migration-RL closure executable contract (revision 2)

Given: selected real source/Consumer, original Owner permission and applicable inputs; absent exact signature remains K.
When: the selected whole Human Goal reconciler consumes its actual input.
Then: Whole original Human Goal **and** applicable FactoryWeaver card obligations (revision/NOOP + native consumer uptake), remaining REQ inventory, real independent evidence and original Owner effect/readback converge; partial green, card DONE, unknown-write or cognitive NOOP cannot falsely close the parent goal.
Producer: original parent REQ/Card and Provider owner.
Consumer: whole Human Goal reconciler.
Inputs and conditions: all REQs, card revisions/NOOP, actual effect receipts.
Outputs/refusals/effects: closed or named blocked remainder.
Positive: local PASS but REQ open -> continue.
Negative/falsifier: Card DONE with missing original effect.
Unknown effect: original Owner readback before any retry; no guessed status.
Replay: previous source-only result may be retained as history, not native evidence.
Independent Oracle: actual observation from whole Human Goal reconciler; new native test NOT_RUN.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: implements → REQ-mrl-closure, validated_by → V-closure, depends_on → REQ-mrl-session, depends_on → REQ-mrl-invalidation, depends_on → REQ-mrl-baseline

## V-closure | Migration-RL closure independent verification (revision 2)

Subject: REQ-mrl-closure; not whole Human Goal.
Independent Oracle Producer: original parent REQ/Card and Provider owner to verify whole Human Goal reconciler.
Positive input/control: local PASS but REQ open -> continue; selected input all REQs, card revisions/NOOP, actual effect receipts.
Negative mutation: Card DONE with missing original effect.
Expected discriminator: closed or named blocked remainder.
Actual observation: NOT_RUN for new Migration-RL Native tests; source-only historical results remain narrower.
Unobserved signatures/effects are K or original Owner readback, never inferred PASS.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: depends_on → SPEC-closure

## REQ-spec-record | spec-record (revision 2)

Actor: original FactoryWeaver/Soodles Owner, per scope.
Goal: Create one canonical v7.2 FactoryWeaver Migration-RL record and complete MRL/MRA/HOF/FWC coverage.
Measurement: Source-supported record contains all MRL-01–10 and MRA-01–18 mapping with typed, valid cards.
Persistence: preserve pending implementation after cards complete.
Stop: original owner readback and stage-specific acceptance.
Non-case: Card compilation is promoted to RL implementation completion.
Correction: card compilation is a local goal and does not depend on full parent Goal closure.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-FW-CARDS
Typed Links: implements → REQ-mrl-spec-record, depends_on → REQ-mrl-intent

## REQ-design-docs | design-docs (revision 1)

Actor: original FactoryWeaver/Soodles Owner, per scope.
Goal: Future implementation shall create separate migration-rl-implementation-scope.md and first-principles.md, linked by migrate-class P-class.
Measurement: Each contract has the agreed twelve sections and independent source-bound verification when actually created.
Persistence: preserve pending implementation after cards complete.
Stop: original owner readback and stage-specific acceptance.
Non-case: Uncreated docs are claimed to be deployed or already consumed.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-FW-CARDS
Typed Links: implements → REQ-mrl-design-docs, depends_on → REQ-mrl-intent, depends_on → REQ-mrl-session

## C-native-truth | Native mathematical runtime differs from text/Replay (revision 1)

Mechanism: actual pinned original and migrated processes compute numerical or DOM/event outcomes under matched inputs; REA captures recorded evidence, not arbitrary stateful writes. Conditions: real images, fixture/seed, independent runtime trace. Failure: HAR expected JSON with no executed original process. Decision: Native Evals cannot be replaced by Replay.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-REA, SRC-AGENTENV
Typed Links: based_on → REQ-mrl-runtimes

## C-two-sided | Two-sided interface proof is not invertibility (revision 1)

Mechanism: within specified preconditions, Producer guarantees meet Consumer accepted domain; reverse error/acknowledgment obligations must independently match Producer expectations. Inputs: typed Producer values, Consumer events, acknowledgments. Failure: lost error ack or forcing inverse hash/aggregation. Decision: verify both contract directions while avoiding invalid universal inverse claim.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: based_on → REQ-mrl-interfaces

## C-goal-loop | One supervising Session converges human goal and cards (revision 1)

Mechanism: Outer Thinking V2/optional V3 × Ambitious finds actual causal breakpoint; admitted Poteto executes bounded work; independent Native results inform original FactoryWeaver card revisions/NOOP; original Owner next resumes. Conditions: real stage/owner and unsealed input. Failure: local PASS or card DONE closes unfinished REQs. Distinct exits: CognitiveStop != HumanGoalClosed.

Evidence: SRC-HUMAN, SRC-HANDOFF, SRC-FW-CARDS
Typed Links: based_on → REQ-mrl-session, based_on → REQ-mrl-closure

## G-license-owner | Legal source and original owner authority (revision 1)

Invariant: multi-source read != multi-target write; repo-level OSS license does not automatically license all assets. Applicability: legal vendor/codemod/adapter and website capture. Authority: original Source/Admission/Provider Owner. Refusal: missing asset rights, foreign write or unknown effect. Consequence: only dependent action blocked. Exception: separately authorized and rights-checked task.

Evidence: SRC-HUMAN, SRC-ISSUE, SRC-MIGRATE
Typed Links: based_on → REQ-mrl-rights

## G-evidence | Independent proof ceiling and untouched Golden (revision 1)

Invariant: Source Identity, behavior parity, math correctness, Native acceptance, card producer and human closure remain separate. Applicability: AST/SCIP, CI, replay, Native Reward and card status. Authority: original Test/Verifier/Owner. Refusal: Candidate self-score, fabricated report, oracle changed for green. Consequence: NOT_RUN/UNKNOWN stay honest. Exception: true oracle error corrected only by its original owner with historical evidence retained.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: based_on → REQ-mrl-false-inference, based_on → REQ-mrl-reward

## G-card-owner | Versioned FactoryWeaver cards cannot rewrite Human Intent (revision 1)

Invariant: original FactoryWeaver producer owns stable IDs, revisions, typed invalidation and historical cards; goal changes need original Human Owner. Applicability: Evals-driven SPEC/V/G/K/X revisions. Authority: FactoryWeaver original producer. Refusal: fabricated human_confirmed=true, replacing Golden or card as effect authority. Consequence: revised card must have fresh Consumer proof. Exception: material source-grounded original Owner-approved revision.

Evidence: SRC-HUMAN, SRC-FW-SCHEMA, SRC-FW-CARDS
Typed Links: based_on → REQ-mrl-cards

## K-native-missing | Missing dual Native and Noodle Owner receipts (revision 1)

Missing input: Missing: paired executable original/target trace, actual reset, native Noodle stage and independent oracle. Producer: original AgentEnv/Noodle/Test Manager/Provider. Why: old Chromium source-only results are not native acceptance. Affected: MRA-05–12 and MRA-15–18. Unaffected: this specification compilation.
Next evidence: real named producer receipts, never invented commands or SHA. Affected dependent requirement: REQ-mrl-runtimes.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: depends_on → REQ-mrl-runtimes

## K-scip-missing | Missing independently labeled AST/SCIP retrieval data (revision 1)

Missing input: Missing: real JS/TS indexer, frozen task ground truth and independent TP/FP/FN/critical dynamic edges. Producer: original Code-intel/indexer and retrieval evaluator. Why: current Soodles Python-only index cannot prove 99%. Affected: MRA-03–04. Unaffected: rights/design cards.
Next evidence: real named producer receipts, never invented commands or SHA. Affected dependent requirement: REQ-mrl-retrieval.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: depends_on → REQ-mrl-retrieval

## K-card-native-missing | Missing card Producer and fresh native card Consumer uptake (revision 1)

Missing input: Missing: real FactoryWeaver revision, Host-bound exact Scope bundle, fresh Noodle Consumer and original Owner readback. Producer: original FactoryWeaver and Soodles/Noodle Owner. Why: card_delta DONE is not implementation acceptance. Affected: MRA-13–15,18. Unaffected: proposed spec.
Next evidence: real named producer receipts, never invented commands or SHA. Affected dependent requirement: REQ-mrl-cards.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: depends_on → REQ-mrl-cards

## K-asset-license-missing | Missing dependency/asset commercial-license closure (revision 1)

Missing input: Missing: actual selected upstream asset/license dependency closure and intended redistribution policy. Producer: Source rights/admission Owner. Why: MIT top-level is not blanket file rights. Affected: real mutation and publication. Unaffected: source-only cards.
Next evidence: real named producer receipts, never invented commands or SHA. Affected dependent requirement: REQ-mrl-rights.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: depends_on → REQ-mrl-rights

## R-causal-atoms | Bounded Migration-RL causal atoms (advisory only) (revision 2)

Parent Goal: lawful, verified source/target native Migration-RL with Session Human Goal/Card closure. Units: 1) spec-only cards, 2) approved .md/P-class, 3) AST/SCIP benchmark, 4) real math/UI runtime+reset, 5) independent Reward/Evals, 6) card producer→native Consumer, 7) comparable held-out baseline. Stateful Full-stack and RL Training deferred. Prerequisites: rights/source and original Owner next; no guessed Tool authority. Exit gates: scoped MRA-01–18 and actual Owner receipts. This Roadmap does not schedule, select tests, or replace Session choices.

Evidence: SRC-HUMAN, SRC-HANDOFF
Typed Links: based_on → REQ-mrl-intent

