---
name: verify-factoryweaver
description: Exercise real FactoryWeaver CLI spec/card behavior and source-bound Soodles Reader via an isolated harness with repeatable verification evidence.
---

# Verify FactoryWeaver — project-local verification skill

Adapted for the real repository surface through upstream pstack create-verification-skill, with repeated maintenance governed by upstream maintain-verification-skill. The upstream copies and MIT license are pinned in .cursor/UPSTREAM-PSTACK.md.

The primary user surface is the Python CLI. There is no server, browser, port, database or credentials. Validation alone does not prove semantic Card truth, fresh P-class Agent behavior or actual Soodles admission.

## Launch

In a checkout with Python 3.12 and jsonschema installed:

    python .cursor/skills/verify-factoryweaver/scripts/verify.py doctor

Each drive uses the existing CLI in a disposable scratch directory. No persistent service starts; the helper uses one isolated short-lived process per drive command.

## Doctor

The doctor command above checks required source files, dependencies, feature-map index and selected surface. Re-run Doctor after any unexpected failure or newly selected native session. Doctor checks readiness, not product correctness.

## Drive

Use the feature map at features/README.md. Available commands:

    python .cursor/skills/verify-factoryweaver/scripts/verify.py drive knowledge-contract
    python .cursor/skills/verify-factoryweaver/scripts/verify.py drive semantic-cards
    python .cursor/skills/verify-factoryweaver/scripts/verify.py drive scope-handoff
    python .cursor/skills/verify-factoryweaver/scripts/verify.py drive manager-needs
    python .cursor/skills/verify-factoryweaver/scripts/verify.py drive portable-bundle
    python .cursor/skills/verify-factoryweaver/scripts/verify.py drive requirement-coverage
    python .cursor/skills/verify-factoryweaver/scripts/verify.py drive factory-profile

The native Soodles read-only feature can be attempted only when the original Host provides SOODLES_CHECKOUT with the actual compatible Soodles checkout:

    python .cursor/skills/verify-factoryweaver/scripts/verify.py drive soodles-reader

No selected Soodles checkout is NOT_RUN, not a passed native verification. Even a successful read-only Soodles CLI does not prove issue admission or a Noodle Writer.

## Evidence

The helper records each actual command, stdout, stderr and exit code in a Host-created external evidence directory. Its output names the actual evidence path; optional --evidence-dir is supported for an existing Host-selected path. It returns status and a precise proof ceiling, never a fabricated source-to-Card semantic PASS.

Card meaning requires original inspected sources and independent semantic review. Upstream source review should use independent read-only feature analysis where a carrier supports subagents. Native P-class proof requires original Soodles review-writing, fresh consumer captures and schema pclass-feedback. Actual outer/inner/Manager/provider effects need the original owners.

The existing semantic-cards and typed-links drives retain parser-boundary
review subjects and declared dependency/scoped-gap controls. Shape-valid
contradictory content remains semantics UNVERIFIED. Use the taxonomy
contract's Consumer boundary and partial parent acceptance check for the
separate source review; no harness result scores Agent compliance.

## Roadmap / One-Shot discriminating cases

In the existing `semantic-cards` feature, test `card_semantic.py roadmap`
on a real v1 fixture: known R/Card references are indexed; forged links refuse;
returned `next`, effects and prompt composition stay absent. Independent
source review—not this CLI—checks chosen minimal Card applicability, missing
G constraints, local-versus-parent acceptance and the difference between
Card generation feedback and the worker `PromptDelta`. A valid owner next
implies no duplicate route. Changed saved P-class instructions still need
fresh native Consumer and original schema feedback, not fixture PASS.

## Cleanup

Every drive uses an isolated TemporaryDirectory, cleaned even after failures. No process is killed by name and no user's running instance is affected. Evidence logs remain at the printed path; check run.json and result.json after cleanup. The helper does not mutate product files, register hooks, schedule Cron, create Issues or PRs, publish or run a new model.

## Helpers

The only helper is scripts/verify.py, and every invocation is shown above. It invokes supported CLI commands as actual subprocesses, not direct internal setters.

## Maintain repeatedly

For every relevant source/feature change, explicitly follow the installed upstream maintain-verification-skill and run the source-wave and live drive of every feature:

    python .cursor/skills/verify-factoryweaver/scripts/verify.py maintain

This attempts the whole feature map. Without the original native Soodles Host and admission it returns blocked, not clean. Use the following as an explicit **local CLI-only** CI control:

    python .cursor/skills/verify-factoryweaver/scripts/verify.py maintain --scope local

That can return clean only for the selected registered local CLI features. It cannot certify source semantics, native P-class adherence, Hook/Cron nontriggers, or parent Goal completion. Do not disguise a full blocked run as local clean.

Maintenance must reconcile the feature index, perform a concurrent read-only source-path wave, then serially drive each feature and capture positive/negative cases. Independent Agent source reasoning is separate from path existence. After a surprising failure, Doctor and retry only a proven harness drift once. Maintain may edit ONLY this verification skill directory, not product code. Doc drift or harness gap can be corrected and driven again before shipping at most one PR; a product regression must be reported to its original owner. For clean/blocked, no new PR.

The authoritative E2E evidence boundary is docs/evals/factoryweaver-e2e-card-verification.md. Original Soodles Test Manager, P-class feedback and owner next remain the single decision producers.

## Complete E2E feature maintenance

The [Feature Map](features/README.md) now covers the registered source-to-Reader-to-original-owner boundaries, including content fidelity, Goal Scope, Typed Links, Prompt Delta, fresh P-class consumer, Outer admission, Noodle Poteto, Test/Schema Manager, native Hook/Cron and Provider closure. A full pass attempts every mapped feature and returns named `verified-unreachable` prerequisites rather than dropping untested paths. Local mode covers the registered CLI features. Actual original Host / Soodles / Provider evidence is required to upgrade native status. No new Runtime Metadata or duplicate runner is authorized.

Offline evidence drives use source-lock, semantic-golden and blind-packet.
The source-lock drive requires Git for its disposable fixture snapshot.
