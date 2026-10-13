# Knowledge Contract

Validate a complete REQ/Card Knowledge Record and render it through the public FactoryWeaver CLI.

## Sub-features

- Original v1 record returns structural validation with explicit proof_ceiling.
- Rendered output contains the selected Email QA REQ and SPEC.
- Malformed record gets a typed refusal, not a fabricated effect.
- Source: scripts/factoryweaver.py
- Source: docs/evals/cs329z-hw1/drill.json

## How to get to it (user POV)

From the repository root, run the named public CLI feature through the project-local verification helper; no server or browser is involved.

## Driving it with the CLI harness

Preconditions: Doctor returned ready and Python 3.12 plus jsonschema are installed.

- Command: python .cursor/skills/verify-factoryweaver/scripts/verify.py drive knowledge-contract
- Positive CLI validate must return valid:true, proof_ceiling SCHEMA_FIXTURE_ONLY.
- CLI cards must include REQ-email-qa and SPEC-email-qa.
- Negative CLI validate against an empty object must refuse with exit code 2.
- Proof: capture actual subprocess commands, stdout/stderr, exit codes, and result.json in external evidence after scratch cleanup.

## Gotchas

- Fixture validity cannot establish semantic completeness of the original lecture.
- The public CLI is not an external provider or Noodle Worker.
