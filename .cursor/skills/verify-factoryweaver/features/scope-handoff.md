# Scope Handoff

Export a selected HW1 behavior into immutable Host-bound source bytes while preserving full parent Requirement inventory.

## Sub-features

- Materialization uses only the original Host-selected output directory.
- Same selected source reuses exact bytes and computed SHA.
- Conflicting contents refuse rather than overwriting unknown writes.
- Source: scripts/soodles_handoff.py
- Source: docs/evals/cs329z-hw1/drill.json
- Source: examples/soodles-scope/hw1-email-qa-selection.json

## How to get to it (user POV)

From the repository root, run the named public CLI feature through the project-local verification helper; no server or browser is involved.

## Driving it with the CLI harness

Preconditions: Doctor returned ready and Python 3.12 plus jsonschema are installed.

- Command: python .cursor/skills/verify-factoryweaver/scripts/verify.py drive scope-handoff
- Actual exporter CLI creates a Bundle with 13 original REQs and authorizes_landing=false.
- Exact input repeated on the same path returns the same result.
- Different causal change at the same path must exit 2 without destroying original evidence.
- Proof: capture actual subprocess commands, stdout/stderr, exit codes, and result.json in external evidence after scratch cleanup.

## Gotchas

- Materialization does not create a Soodles Issue or enable the Reader.
- The digest is calculated by CLI, not filled by the Agent.
