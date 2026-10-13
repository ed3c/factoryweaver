# Soodles Test Manager and Native Hook Manager — FactoryWeaver advisory handoff

This document describes **real original owners**, not new FactoryWeaver managers.

Classify task-review, PR/MR source check, native Hook behavior verification and delivery before preparing needs. Their triggers and necessary inputs differ; see [Hook purposes and review boundaries](hook-purpose-and-review-boundaries.md). A source check does not require historical Stage, Stop/session or training metadata. Native Stop still needs its actual Host binding.

## Grounded upstream authorities

- [Soodles Test Manager Skill](https://github.com/ed3c/soodles/blob/main/.agents/skills/test-manager/SKILL.md) and `test_manager.py`: **single P-class test scope owner**. Its selected `ready`, `needs_scope` and `not_required` are not test PASS. A selected exact-head success covers only chosen controls. Only a matching owner/provider readback establishes a real result. Missing scope may not be replaced with Full Suite.
- [Soodles Hook Manager code](https://github.com/ed3c/soodles/blob/main/hook_manager.py), [hook tests](https://github.com/ed3c/soodles/blob/main/tests/test_hook_manager.py), [Stop tests](https://github.com/ed3c/soodles/blob/main/tests/test_hook_stop.py). This original implementation inspects installed native configurations and safely adapts a selected Stop event into existing Schema Manager task review. **No installed `.agents/skills/hook-manager/SKILL.md` was present at the inspected revision**; do not model a fictitious Skill.
- [Soodles Schema Manager](https://github.com/ed3c/soodles/blob/main/schema_manager.py) returns bounded projections and retains the original Owner continuation. A digest checks source identity, not independent Agent behavior. Hook observation and a later command do not prove the command consumed a specified `next`.
- [Soodles review-writing](https://github.com/ed3c/soodles/blob/main/.agents/skills/review-writing/SKILL.md) separates N-class prose reviews from P-class behavior feedback. It does not substitute tests or actual Hook execution.

## Data flow (does not create a second scheduler)

```text
Source → Card(s) → one Goal-oriented Behavior Scope
      → SPEC+V focused verification question / negative control
         → FactoryWeaver manager-need projection (read-only)
            → Original Soodles Test Manager selects actual tests
              → original CI/runtime execution + source/owner readback
      → Only if observed native Hook event is required:
         → FactoryWeaver proposed Hook need (event + source condition)
            → original Soodles Session / native Host checks config and capabilities
              → hook_manager.py inspect / Stop
                 → Schema Manager task-review + original owner next
      → Original Soodles Session reconciles requirements and results.
```

This handoff **never** executes tests/hooks, adds a `test_argv`, fabricates a Hook configuration/registration, installs a skill, runs Cron, or grants effect authority. It cannot update the original owner `next`.

## Projection contract

The optional **read-only** `scripts/card_semantic.py managers REQUEST` input has the following *semantic* form, constructed from **actual observed requirements**:

- `subject`: real behavioral Scope topic.
- `test_need`: `null` if no selected change requires new test control, otherwise `changed_behavior`, `verification_question`, and `negative_case`.
- `hook_need`: `null` when no actual native event is needed; otherwise `native_event`, `observed_requirement`, `source_state` (INSPECTED / UNREAD).
- No physical IDs, digest, computed metrics, selected test cases, actual `next`, commands, event payloads, installed Hook declarations or effect receipts. Host/Owner supplies actual native bindings independently.

Output status:
- No test need → `NO_TEST_SELECTION_REQUESTED`; otherwise `NEEDS_ORIGINAL_TEST_MANAGER_SELECTION` with `selected_controls=UNKNOWN`, `test_execution=NOT_RUN`.
- No Hook need → `NO_NATIVE_HOOK_REQUIRED`; a source-unread event → `NEEDS_NATIVE_SOURCE_OBSERVATION`; a source-inspected event → `NEEDS_ORIGINAL_HOOK_OWNER_READBACK`, **never** native PASS.
- `effect_authority=false`, `authorizes_landing=false`, `manager_actions_performed=[]`.

The actual Session reads Soodles Test Manager's selected scope or Hook Manager's native receipts and consumes their original next. FactoryWeaver cannot derive Soodles commands from a textual operation name.

## Hard negative controls

| Scenario | Correct scope result |
| --- | --- |
| Only source catalog / N-class writing change | No test execution just because a Card changed; review prose, route `NOT_RUN` for behavior. |
| A SPEC changes returned IDs or response shape | Propose a verification question, let original Test Manager select matching positive/negative cases. Never demand `--full`. |
| Test Manager returns `needs_scope` | Preserve owner selection refusal and request named affected caller/controls, not an invented module or PASS. |
| P-class Agent behavior guidance changed | `review-writing` + scoped fresh-consumer feedback and Schema Manager consumption, separate from selected software controls. |
| A card mentions safety or Stop but no native Hook behavior is required | `NO_NATIVE_HOOK_REQUIRED`; do not create any registration. |
| Soodles native Stop input matches source but handler result is unknown | Request native Host/Hook owner readback; preserve `stop_hook_active` recursion behavior, do not force Stop continuation. |
| Native Hook completed and subsequent tool call exists | Do not infer the subsequent call consumed the exact original `next`; require appropriate observation. |
| Original owner next already fixed | Preserve it; a suggested manager need adds no new authorization or route. |
| FactoryWeaver schema/fixture is green | Knowledge-record structural validity only; not a Soodles native effect, Goal success, merge or landing. |

**No additional Test Manager or Hook Manager class exists in FactoryWeaver.** The projection is an optional owner-neutral handoff; original native Soodles units remain the only authority.
