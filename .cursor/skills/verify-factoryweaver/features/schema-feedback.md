# Schema Manager evidence and next consumption

This feature is a source/Owner proof boundary. The FactoryWeaver CLI can name missing evidence but cannot execute native Soodles effects.

## Sub-features

- Required evidence: Original feedback result and evidence that same Owner next was actually consumed
- Keep missing original evidence as `verified-unreachable`, never a false PASS.
- Source: docs/evals/factoryweaver-e2e-card-verification.md

## How to get to it (user POV)

Start from the FactoryWeaver feature map; invoke the project-local verification helper. Original Soodles Session/Host is the owner of any native continuation.

## Driving it with the CLI harness

Preconditions: Doctor ready and original Source/Owner capability available when native behavior is required.

- Run `python .cursor/skills/verify-factoryweaver/scripts/verify.py drive schema-feedback` from repository root.
- The helper returns the concrete unmet original Owner prerequisite without making effectful calls.
- Real verification follows the existing E2E contract and saves actual original receipts. Do not replace the Host with synthetic metadata.
- Proof: recorded CLI response, command, exit code and the retained result.json.

## Gotchas

- Later command output alone does not prove next consumption.
- The source wave checks entrypoint presence, not semantic truth or model execution.
- A product bug belongs to the original product Owner; maintain-verification-skill cannot silently fix it.
