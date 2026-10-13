# Original Goal and REQ-to-Issue alignment

This feature is a source/Owner proof boundary. The FactoryWeaver CLI can name missing evidence but cannot execute native Soodles effects.

## Sub-features

- Required evidence: Original Issue owner compares Goal, Measurement, Persistence, Stop and Acceptance with selected REQ
- Keep missing original evidence as `verified-unreachable`, never a false PASS.
- Source: docs/factoryweaver-soodles-readback.md
- Source: references/card-classification-and-scope-assembly.md
- Source: .cursor/skills/verify-factoryweaver/fixtures/parser-consumer-boundary.json

## How to get to it (user POV)

Start from the FactoryWeaver feature map; invoke the project-local verification helper. Original Soodles Session/Host is the owner of any native continuation.

## Driving it with the CLI harness

Preconditions: Doctor ready and original Source/Owner capability available when native behavior is required.

- Run `python .cursor/skills/verify-factoryweaver/scripts/verify.py drive goal-scope` from repository root.
- The helper returns the concrete unmet original Owner prerequisite without making effectful calls.
- Real verification follows the existing E2E contract and saves actual original receipts. Do not replace the Host with synthetic metadata.
- Source review must distinguish the atom's covered parent clauses/local exit, inherited constraints and deferred obligations. For the parser review fixture, ParsedProposal/refusal is local; original TaskSnapshot replay and native lifecycle remain parent obligations.
- Proof: recorded CLI response, command, exit code and the retained result.json.

## Gotchas

- Matching REQ ID does not establish semantic equivalence.
- The source wave checks entrypoint presence, not semantic truth or model execution.
- A product bug belongs to the original product Owner; maintain-verification-skill cannot silently fix it.
- A parent native prerequisite cannot block unrelated authorized local work. Neither a card ID nor fixture shape proves original Goal alignment; the helper still reports the missing actual Issue/Owner readback.
