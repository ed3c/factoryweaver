# FactoryWeaver → Soodles dedicated read-only knowledge-card bundle

## Purpose

A FactoryWeaver v7.2 Compiler turns actual source data into cards, accepted requirements and a Goal-oriented Behavior Scope. Soodles must consume these **without re-parsing prose** and without inferring effect authority, current Issue identity or a new independent Scheduler.

**Producer:** `scripts/soodles_handoff.py` imports existing `factoryweaver.verify`, verifies the original `factoryweaver/v1` record and checks one semantic selection referencing **existing** REQ/card identities.

**Transport:** `factoryweaver/soodles-scope/v1` Bundle contains exactly `protocol`, `kind=SOURCE_BOUND_PROPOSAL`, `knowledge_record` (complete original record) and `selection`. This preserves whole-task Source→REQ history and all unrelated knowledge; only the selected IDs become the proposed Scope.

**Consumer:** Soodles [`./soodles knowledge inspect`](https://github.com/ed3c/soodles/blob/feat/factoryweaver-scope-readback/contracts/factoryweaver-scope-v1.md), backed by its own read-only `factoryweaver_scope.py`. It checks **Host-computed exact bundle bytes** and selected references, projects only selected Card/REQ and their semantic properties, and lists other full-inventory requirement IDs as incomplete work.

## Selection semantics (no model-generated machine metadata)

The selection has exactly these fields:

| Field | Meaning |
| --- | --- |
| `requirement_ids` | Selected existing original REQ IDs; not newly generated |
| `card_ids` | Selected existing active Card IDs, often C/REQ/SPEC/G/V |
| `goal` | Observable user outcome retained from original requirement |
| `measurement` | Actual expected independent oracle/metric owner |
| `persistence` | Evidence-driven continuation obligation and known effort policy |
| `stop_and_escalation` | Success, bounded blocker and reassessment condition |
| `causal_change` | One bounded Issue Atom's needed behavior change |
| `acceptance` | Observable accepted/rejected behavior, nonempty |
| `constraints` | Reused applicable G plus task-local exclusions |
| `prompt_delta` | Only new semantic required changes, or empty for NOOP |

The exact file reference and SHA are computed by the real Host/CLI. Do not put a fake digest, checkout path, new execution ID, guessed `next.argv` or model-generated operation ID into a Card, Scope selection or Prompt Delta.

## Minimal use

1. Compile and validate `factoryweaver/v1` knowledge using the existing FactoryWeaver Skill/CLI.
2. Select one existing bounded Goal/REQ with relevant accepted cards. The included [HW1 example selection](../examples/soodles-scope/hw1-email-qa-selection.json) is a structural demonstration, not an authorized Issue.
3. Prefer the original Producer's materialization interface with a **Host-selected** absolute output: `python3 scripts/soodles_handoff.py RECORD_JSON SELECTION_JSON --output HOST_DESTINATION`. It validates the full knowledge record, writes exclusive bytes and returns a computed FileRef plus fixed `reader_arguments`. Identical re-entry reuses exact bytes; conflicting/changed output refuses and requires original Host readback. Without a supported destination, the legacy stdout-only output remains a read-only proposal and the necessary Host materialization is a named gap. The Skill does not ask the model to choose the destination or calculate SHA.
4. In the authorized Soodles Session, use the dedicated [`factoryweaver-read` Skill](https://github.com/ed3c/soodles/blob/feat/factoryweaver-scope-readback/.agents/skills/factoryweaver-read/SKILL.md) and `./soodles knowledge inspect BUNDLE_FILE HOST_COMPUTED_SHA256`.
5. Use its source-bound selected REQ/card projection to compare the fresh original Issue Body, covered callers, acceptance, source priority and provider state; only then follow the existing Soodles `issue-atom` preparation/admission route.
6. Outer Loop selects Test Manager controls, conditional Thinking/Evals or original Hook readback only on observed triggers; original `execute` / Poteto receives selected semantics after actual admission. Soodles must not copy the text into new permission fields.

## Negative cases

- An unknown/repeated REQ/Card identity, retired card, missing Goal/Measurement/Stop or author-authored mechanical binding refuses at producer. Selected existing UNKNOWN/CONFLICTED REQ or K/X Card is **retained**, so Soodles can return `needs_source_readback` rather than hiding the original source gap.
- Changed bundle bytes, unknown references or invented effect claims refuse at Soodles consumer. A valid digest proves byte selection, **not source truth or human approval**.
- Original Issue readback is `NOT_READ` after this reader. An actual Issue/PR may be created **only** by the original authorized Soodles lifecycle.
- The full original 13-REQ HW1 inventory remains available even if one selected QA atom uses three cards; no silent loss from four-slot Boot/Drill.
- Tests and Hooks are not selected/run by either exporter or reader. No new Test/Hook/Cron manager, global hooks or separate Scheduler.

## Verification boundary

FactoryWeaver tests validate full v1 source record plus selection and CLI emission; Soodles tests check actual portable HW1 record consumption, exact-byte binding, schema/refusal cases and `next=null`. Cross-repository CI green establishes only this read-only transport seam. It does **not** establish native Skill behavior, Issue admission, fresh Noodle writer, real Test Manager choice, merged PR or terminal owner readback. Such states require independent original Host evidence.

## P-class and CLI correctness boundaries

The model's P-class instructions identify **semantic** conditions (Goal ambiguity, real Scope value, observed failure). The original CLI fixes **mechanical** outcomes (v1 validation, exact Bundle bytes, content reuse/refusal, source/Owner continuation, admissible operations). The returned `reader_arguments` belong to the original Producer and are consumed with Soodles' fixed CLI entry. They do not grant permissions.

The Selection still contains Goal/Measurement/Acceptance prose because the v1 REQ data does not independently encode the entire Goal Contract. A matching REQ ID **does not prove** that these copied sentences are semantically equivalent to the original requirement; the Soodles Session and original Issue Contract Owner must reconcile that before Admission. A later migration may remove duplicated fields only after an actual canonical Goal Producer exists. Do not fabricate another one.

Soodles Reader status `source_bound_proposal` is **not** a legal execution transition and its `next=null` is intentionally not an invitation to guess `issue-atom` arguments. The original Session uses existing Issue/provider readbacks and current Owner next first. If a structured Issue Contract is missing, return that named prerequisite rather than forge it. Test/Hook/Cron Managers receive only applicable, source-backed needs; they do not fire as a consequence of cards.
