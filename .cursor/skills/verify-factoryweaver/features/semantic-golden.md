# semantic-golden

## Sub-features

- curated N/C/P shape is checked.
- forged human approval refuses.
- Source: scripts/semantic_golden.py
- Source: tests/fixtures/semantic-golden.json

## How to get to it (user POV)

Use the corresponding public offline CLI with original Owner-supplied inputs.

## Driving it with the CLI harness

Run `python .cursor/skills/verify-factoryweaver/scripts/verify.py drive semantic-golden`.
Positive and negative subprocess results are retained in the external evidence directory.

## Gotchas

These are byte/shape/packet controls. Real source authentication, model-quality
comparison and independent human review remain NOT_RUN.
