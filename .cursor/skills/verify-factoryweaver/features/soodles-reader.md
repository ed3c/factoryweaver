# Soodles Reader

Read a Host-bound FactoryWeaver Bundle with the original Soodles CLI, retaining unverified Runtime targets and never granting admission.

## Sub-features

- An actual original SOODLES_CHECKOUT is required for the native reader CLI.
- Reader emits boundary_findings and verification_targets from the selected Scope.
- Actual Issue/Agent/Manager/Provider effects remain separate original owner readbacks.
- Source: scripts/soodles_handoff.py
- Source: docs/factoryweaver-soodles-readback.md
- Source: docs/evals/factoryweaver-e2e-card-verification.md

## How to get to it (user POV)

From the repository root, run the named public CLI feature through the project-local verification helper; no server or browser is involved.

## Driving it with the CLI harness

Preconditions: Doctor returned ready and Python 3.12 plus jsonschema are installed.

- Command: python .cursor/skills/verify-factoryweaver/scripts/verify.py drive soodles-reader
- Precondition: original Host supplied SOODLES_CHECKOUT; do not silently clone/assume it.
- Actual CLI knowledge inspect verifies source-bound Bundle and returns next=null, effects=[], authorizes_landing=false.
- Without checkout, declare verified-unreachable and retain full maintain outcome blocked.
- Proof: capture actual subprocess commands, stdout/stderr, exit codes, and result.json in external evidence after scratch cleanup.

## Gotchas

Reuse the returned Reader arguments after changing only the disposable Bundle
bytes. The negative drive requires exit 2, selected_bytes_changed and unchanged
null next/empty effects/no landing authority. Exact-byte transport is not admission.

- A compatible read-only Reader does not prove legal admission, selected Poteto playbook or fresh native Agent behavior.
- The repository's original Issue #300 is still a separate admission gate.
