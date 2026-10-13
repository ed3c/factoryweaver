# Manager Needs

Project source-backed Test and Hook needs without triggering a Manager, selecting a full suite or scheduling a Cron job.

## Sub-features

- Changed QA behavior requests only original Test Manager selection.
- Uninspected native Stop remains NEEDS_NATIVE_SOURCE_OBSERVATION.
- Unchanged scope yields NO_TEST_SELECTION_REQUESTED and NO_NATIVE_HOOK_REQUIRED.
- Source: scripts/card_semantic.py
- Source: examples/card-semantic/qa-test-needs.json
- Source: examples/card-semantic/native-stop-needs.json
- Source: docs/hook-purpose-and-review-boundaries.md
- Source: .cursor/skills/verify-factoryweaver/fixtures/hook-purpose-boundaries.json
- PR/MR source needs require no Stage/session/token metadata and no native Hook request.
- Extra runtime/effect fields refuse. A freeform event declaration still cannot certify its purpose or invocation.

## How to get to it (user POV)

From the repository root, run the named public CLI feature through the project-local verification helper; no server or browser is involved.

## Driving it with the CLI harness

Preconditions: Doctor returned ready and Python 3.12 plus jsonschema are installed.

- Command: python .cursor/skills/verify-factoryweaver/scripts/verify.py drive manager-needs
- Positive CLI manager projections return original-owner need statuses and no actions performed.
- Negative NOOP case does not select tests, invoke native Hook or create additional authorization.
- Proof: capture actual subprocess commands, stdout/stderr, exit codes, and result.json in external evidence after scratch cleanup.

## Gotchas

- This is advisory projection; no actual Manager is launched.
- Native Hook requires an original real event; Cron requires the original authorized heartbeat.
