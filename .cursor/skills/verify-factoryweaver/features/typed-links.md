# Typed Link Registry

Inspect actual registered Card links using the public CLI and distinguish structural direction from independently established causality.

## Sub-features

- Registered SPEC validated_by V is structurally accepted.
- Unsupported relation returns a typed refusal.
- Source: scripts/card_semantic.py
- Source: examples/card-semantic/hw1-email-qa.json

## How to get to it (user POV)

Use the existing FactoryWeaver Card semantic inspection CLI.

## Driving it with the CLI harness

Preconditions: Doctor ready and an isolated scratch path.

- Run `python .cursor/skills/verify-factoryweaver/scripts/verify.py drive typed-links`.
- Positive control runs actual inspect against the selected HW1 Card.
- Negative control changes the relation and requires nonzero exit and refused output.
- Proof includes actual argv, stdout, stderr, exit and retained result.json.

## Gotchas

- JSON Link validity is not proof of real source/target causality.
- Chronological syllabus order cannot justify enables or depends_on.
