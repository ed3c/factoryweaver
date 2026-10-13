# Declared requirement coverage

## Sub-features

- Baseline reports five unmapped clauses; proposal traces six distinct REQ/SPEC pairs.
- Schema-invalid records and swapped sources return JSON refusal with exit 2.
- Source: scripts/requirement_coverage.py
- Source: examples/openai-plugin-platform/project.json
- Source: examples/openai-plugin-platform/job-clause-inventory.json
- Source: examples/openai-plugin-platform/proposed-six-requirements.json
- Source: examples/openai-plugin-platform/proposed-six-clause-inventory.json

## How to get to it (user POV)

Provide the knowledge record and declared source-clause inventory to requirement_coverage.py.

## Driving it with the CLI harness

Run `python .cursor/skills/verify-factoryweaver/scripts/verify.py drive requirement-coverage`.
The coordinator captures both positive traces and schema/source refusals in isolated scratch.

## Gotchas

A declared inventory can omit source clauses. Structural links do not prove source
exhaustiveness, semantic correspondence, implementation or delivery.
