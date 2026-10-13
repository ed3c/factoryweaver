# FactoryWeaver verification feature map

This is the feature map maintained by create-verification-skill and maintain-verification-skill. A user interacts with the actual Python CLI; each feature file names source entry points, a CLI drive and its observable end state.

## Preconditions

- Python 3.12 and jsonschema; no server.
- A clean isolated scratch directory per drive, retained external evidence.
- Doctor before the first drive or after unexpected failure.
- SOODLES_CHECKOUT only if provided by original Host, not auto-cloned.
- No original Issue admission, Hook/Cron event or native model invocation is implied by a passing public CLI fixture.

## Map and proof

The source wave checks all declared Source paths from these feature files concurrently; it is a path-based preflight, not a semantic source review. The coordinator drives all local features serially, records stdout/stderr/exit codes and cleans scratch. Every feature must be examined even if another fails. Full maintain remains blocked without actual native admission and fresh consumer evidence.

## Complete end-to-end Feature Map and current verification states

The status reported by each real maintain run is authoritative. Local CLI PASS does not prove native/semantic E2E.

| Feature | Known proof | Still required |
| --- | --- | --- |
| [knowledge-contract](./knowledge-contract.md) | Real CLI positive/negative controls | Source truth and native effects excluded |
| [semantic-cards](./semantic-cards.md) | Real CLI positive/negative controls | Source truth and native effects excluded |
| [scope-handoff](./scope-handoff.md) | Real CLI positive/negative controls | Source truth and native effects excluded |
| [manager-needs](./manager-needs.md) | Real CLI positive/negative controls | Source truth and native effects excluded |
| [typed-links](./typed-links.md) | Real CLI positive/negative controls | Source truth and native effects excluded |
| [soodles-reader](./soodles-reader.md) | Original Owner not verified | Actual source/Session/Provider readback |
| [source-fidelity](./source-fidelity.md) | Original Owner not verified | Actual source/Session/Provider readback |
| [goal-scope](./goal-scope.md) | Original Owner not verified | Actual source/Session/Provider readback |
| [prompt-delta](./prompt-delta.md) | Original Owner not verified | Actual source/Session/Provider readback |
| [pclass-consumer](./pclass-consumer.md) | Original Owner not verified | Actual source/Session/Provider readback |
| [outer-admission](./outer-admission.md) | Original Owner not verified | Actual source/Session/Provider readback |
| [inner-poteto](./inner-poteto.md) | Original Owner not verified | Actual source/Session/Provider readback |
| [test-manager](./test-manager.md) | Original Owner not verified | Actual source/Session/Provider readback |
| [schema-feedback](./schema-feedback.md) | Original Owner not verified | Actual source/Session/Provider readback |
| [native-hook](./native-hook.md) | Original Owner not verified | Actual source/Session/Provider readback |
| [native-cron](./native-cron.md) | Original Owner not verified | Actual source/Session/Provider readback |
| [delivery-closure](./delivery-closure.md) | Original Owner not verified | Actual source/Session/Provider readback |

Three levels: (1) Card schema/type verification is not source semantics; (2) Reader/CLI transport is not Issue admission; (3) P-class, Outer, Inner, Test/Schema/Hook/Cron and Provider effects each need original native capture.

Local maintain drives five CLI features and marks twelve `excluded`. Full maintain source-indexes and attempts all 17, reports individual `verified-unreachable` prerequisites, and remains `blocked` without original native evidence. `clean` in local mode never means full E2E.
## Features

- [Knowledge Contract](./knowledge-contract.md): validate and render original HW1 specification records.
- [Semantic Cards](./semantic-cards.md): selected card prompts and unread-source refusal.
- [Scope Handoff](./scope-handoff.md): original Host-bound Bundle and replay/conflict cases.
- [Manager Needs](./manager-needs.md): focused verification needs without unauthorized manager invocation.
- [Soodles Reader](./soodles-reader.md): consume actual external Reader where Host supports it; native admission remains separately unverified.

- [Typed links](./typed-links.md) — actual CLI registered relation and refused invalid relation.
- [source-fidelity](./source-fidelity.md) — original-owner E2E proof target, not a local PASS.
- [goal-scope](./goal-scope.md) — original-owner E2E proof target, not a local PASS.
- [prompt-delta](./prompt-delta.md) — original-owner E2E proof target, not a local PASS.
- [pclass-consumer](./pclass-consumer.md) — original-owner E2E proof target, not a local PASS.
- [outer-admission](./outer-admission.md) — original-owner E2E proof target, not a local PASS.
- [inner-poteto](./inner-poteto.md) — original-owner E2E proof target, not a local PASS.
- [test-manager](./test-manager.md) — original-owner E2E proof target, not a local PASS.
- [schema-feedback](./schema-feedback.md) — original-owner E2E proof target, not a local PASS.
- [native-hook](./native-hook.md) — original-owner E2E proof target, not a local PASS.
- [native-cron](./native-cron.md) — original-owner E2E proof target, not a local PASS.
- [delivery-closure](./delivery-closure.md) — original-owner E2E proof target, not a local PASS.
