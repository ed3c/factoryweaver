# Semantic Cards

Select specific card generation contracts and reject an unread mechanism claim without conflating field correctness with source truth.

## Sub-features

- Only selected C/SPEC/V prompts are returned.
- Card proposal inspection returns SHAPE_VALID_SEMANTICS_UNVERIFIED.
- An unread SPEC must not be claimed as an inspected source mechanism.
- Source: scripts/card_semantic.py
- Source: references/card-prompts/registry.json
- Source: examples/card-semantic/hw1-email-qa.json
- Source: .cursor/skills/verify-factoryweaver/fixtures/parser-consumer-boundary.json

## How to get to it (user POV)

From the repository root, run the named public CLI feature through the project-local verification helper; no server or browser is involved.

## Driving it with the CLI harness

Preconditions: Doctor returned ready and Python 3.12 plus jsonschema are installed.

- Command: python .cursor/skills/verify-factoryweaver/scripts/verify.py drive semantic-cards
- Positive select returns exactly C, SPEC, V in order.
- Positive inspect reports shape valid with semantics explicitly UNVERIFIED.
- Negative change to SPEC source_status UNREAD must refuse.
- Drive parser-claims-replay, v-copies-result-without-input and parser-refusal-local-exit. All remain structurally valid with semantics UNVERIFIED; the CLI must not award semantic ACCEPT to any of them.
- Proof: capture actual subprocess commands, stdout/stderr, exit codes, and result.json in external evidence after scratch cleanup.

## One-Shot / Roadmap deterministic controls

The same existing Card Semantic CLI also supports `roadmap RECORD` as a
read-only index. Run it against `docs/closed-loop-v72/project.json` and
observe existing registered cards and Roadmap typed links, with no Scope,
Prompt, next or effects. A forged Roadmap target must receive the original
v1 verification refusal. This verifies index/reference behavior, **not** that
Session chose an optimal Scope. The independent reviewer must test omission
of an applicable G, copied parent acceptance as local exit, and unchanged
prompt-delta NOOP; source review and native P-class remain separate.

## Gotchas

- Reading a title or PDF link alone is not inspecting the actual source.
- Independent source/semantic review is still required.
- Independent reviewer: compare fixed parser inputs and output against then; reject the first fixture's downstream replay claim and the second fixture's input-free V control. Review the corrected local exit while preserving the original parent replay requirement. These expected review criteria are not fresh native behavior observations.

All 15 N/Q/C/D/S/P/T/R/G/E/V/X/K/REQ/SPEC prompts are selected in a real CLI call during this journey. The grounded C/SPEC/V fixture and its negative unread-source control remain distinct. Every one of the fifteen types has existing per-type field tests; none is assumed semantically complete without reading the original source.

See [Prompt Carriers](prompt-carriers.md) for the actual data transformation after type selection; a Scope Selection with conflicting Goal text stays a proposal, not a semantic PASS.
