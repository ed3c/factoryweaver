# Typed Link Registry

Inspect actual registered Card links using the public CLI and distinguish structural direction from independently established causality.

## Sub-features

- Registered SPEC validated_by V is structurally accepted.
- Unsupported relation returns a typed refusal.
- Source: scripts/card_semantic.py
- Source: examples/card-semantic/hw1-email-qa.json
- Source: scripts/card_delta.py
- Source: scripts/factoryweaver.py
- Source: docs/evals/cs329z-hw1/drill.json

## How to get to it (user POV)

Use the existing FactoryWeaver Card semantic inspection CLI.

## Driving it with the CLI harness

Preconditions: Doctor ready and an isolated scratch path.

- Run `python .cursor/skills/verify-factoryweaver/scripts/verify.py drive typed-links`.
- Positive control runs actual inspect against the selected HW1 Card.
- Negative control changes the relation and requires nonzero exit and refused output.
- Change the existing grounding Concept and confirm its declared based_on edge affects SPEC-email-qa. Remove that edge from both frozen fixture records: the same change must not invent a missing dependency.
- Add one synthetic K dependency only to REQ-framework: project must report its named prerequisite while REQ-email-qa retains its original WAIT_FOR_SOURCE_PIN/SRC-qa and no effects. Do not invent source pins to make the unrelated fixture appear ready.
- Proof includes actual argv, stdout, stderr, exit and retained result.json.

## Gotchas

- After a card revision, read its typed-link explanations again against the *new* Consumer API, input/output, and local-versus-parent clauses. An unchanged `implements → REQ` target can remain structurally valid while its prose still claims TaskSnapshot is loaded by a parser that only consumes raw bytes and opaque fixed references. This is an independent **source-semantic REVISE**, not a new CLI semantic validator or a runtime prerequisite. See the stale/corrected link pair in the existing `semantic-cards` feature.
- JSON Link validity is not proof of real source/target causality.
- Chronological syllabus order cannot justify enables or depends_on.
- Missing material links are a compiler/review correction, not permission for the CLI to infer causal truth. Context-only cards require no invented edges.
