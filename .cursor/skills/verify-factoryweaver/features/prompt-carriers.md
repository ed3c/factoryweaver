# Prompt Carriers — source intent to Reader-proposed Scope

This journey verifies that the *same existing source-backed content* moves through selected Card Contract → accepted Knowledge Record → semantic Scope/Prompt Delta → immutable Soodles Bundle. It does **not** prove native P-class Skill loading or writer consumption.

## Sub-features

- Source: references/zettelkasten-v7.2.md
- Source: references/prompt-carrier-and-ownership.md
- Source: docs/hook-purpose-and-review-boundaries.md
- Source check consumes exact task/candidate/diff and actual review evidence without unrelated Stage, native Session, token or transfer metadata. Native-effect proof stays separately applicable.
- Source: scripts/card_semantic.py
- Source: scripts/soodles_handoff.py
- Source: docs/evals/cs329z-hw1/drill.json
- Source: examples/soodles-scope/hw1-email-qa-selection.json
- Selected C/REQ/SPEC/V prompt references are returned by the original CLI.
- The entire original Requirement/Card inventory is preserved exactly in the transport.
- Prompt Delta remains plain semantic requirements, without invented permission or next.
- NOOP `prompt_delta=[]` keeps full Goal, Acceptance, selected Card IDs and full
  Knowledge Record. NOOP is not task deletion.
- A syntactically valid but parent-overreaching acceptance remains a low-trust
  proposal; only independent Source Review can reject the semantic error.
- A deliberately contradictory copied Goal can still pass **transport syntax** but remains UNVERIFIED until the original Issue/Session reconciles it.
- Forged Card identity receives a deterministic producer refusal.

## How to get to it (user POV)

From the original FactoryWeaver source/REQ/card interface, prepare the accepted v1 record and one selected bounded Soodles Scope. No new agent manager or schema field.

## Driving it with the CLI harness

Preconditions: original required test sources exist; Doctor succeeds; each drive owns an isolated scratch directory.

- Run `python .cursor/skills/verify-factoryweaver/scripts/verify.py drive prompt-carriers` from repository root.
- The harness invokes actual `card_semantic.py select` and `soodles_handoff.py --output`, then reads back the original Bundle and compares data to the selected source file.
- Negative control 1: different nonempty Goal is still a low-trust source-bound proposal; it **must not** be called Issue Goal equivalence.
- Negative control 2: forged selected Card ID is rejected with the original CLI's nonzero exit.
- Proof: original commands/stdout/stderr/exit, output source preservation and result.json retained after cleanup.

## Gotchas

- Source text vs v1 Card fidelity still needs an independent semantic reviewer.
- Soodles `factoryweaver-read` plus current Issue/provider/actual Noodle Stage is a separate native boundary; local `clean` proves no such effect.
- If the supplied Goal differs from current Issue, Session/Issue Contract owner must resolve it. Do **not** relax acceptance or invent a new machine identity to hide it.
