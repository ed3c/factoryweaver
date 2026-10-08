# FactoryWeaver Card Delta — bounded knowledge compilation

This is a **read-only** reference compiler for Issue #4. It does not execute upstream Skills, query sources, run Noodle, create PRs, validate whether provided SHA-256 metadata matches external bytes, or promote human/owner attestations.

## Entry

```bash
python3 scripts/card_delta.py BEFORE.json AFTER.json --batch-size 12
python3 scripts/card_delta.py BEFORE.json AFTER.json --cursor '<exact next_cursor>'
```

The calling owner supplies two JSON records under `contracts/v1/knowledge-record.schema.json`. The compiler calls the existing `verify` function first. Inputs must have identical protocol and subject scope.

## Invariants / known limits

- Canonical keys identify cards. The same key must keep its `stable_id`. No content change permits a revision increase; material content change requires **exactly one** revision increment.
- The old card cannot silently disappear. A supersession must keep it with `SUPERSEDED` status and updated revision, plus an `ACTIVE` new card linked via `supersedes`.
- New cards begin at revision 1; a reused stable ID is rejected.
- Source metadata changes yield `source_metadata_changed` and **advisory** `affected_nodes` via the exact `source_ids/evidence_ids/depends_on/typed_links` graph. This does **not** invalidate original owner receipts or authenticate source bytes.
- Source attributions with the **same** `source_dependency_key` appear in one `origin_groups` entry, even if their `source_id`s differ. This prevents structural overcounting. It is not cryptographic proof of independent origins; `source_independence_proven` is always false in this reference CLI.
- Output patches use deterministic after-record order. At most 12 card changes per batch. `next_cursor` binds **both record contents** with SHA-256 plus an offset. Never treat a cursor as authorization or independent source integrity.
- Identical records return `NOOP`. `DONE` means the current bounded **patch compilation** is complete. `BLOCKED` with `original_source_owner_readback_required` means input Source metadata changed but no trusted producer validated the new bytes; `BLOCKED` with `noncard_change_requires_reconciliation` prevents silently treating changed project-only fields as verified card output. Neither status means software, tests, product delivery, or original v7.1 semantic parity are complete.
- This module implements **only** stable revision, supersession, dependency metadata and lossless batching. It does not implement semantic contradiction resolution, time-anchor fidelity, anti-fragmentation judging, narrative-richness judging, full I-01–I-16 / QG-01–QG-34 or actual original source retrieval. These stay open in Issue #4.

## Verification

```bash
python3 -m unittest discover -s tests -v
```

Expected negative controls: spurious revision, identity rewrite, card deletion, incomplete supersession, out-of-range batching and stale cursor. This is local fixture verification only; use the exact-head GitHub Actions result to establish hosted scope. Candidate PR remains a stack behind Bootstrap PR #3, and cannot be treated as an accepted release before its base is independently accepted.
