---
name: factoryweaver-verify
description: Verify FactoryWeaver JSON contract validity, evidence references, human-decision boundaries, skill routing honesty and completion claims. Use before passing a specification to a software factory or reporting test, PR or delivery status.
license: MIT
---
# FactoryWeaver verification

1. Load `../../contracts/v1/knowledge-record.schema.json` and run the read-only CLI `validate`.
2. Check Source ID uniqueness, dependency and typed link reachability, and stable card IDs. If raw source bytes plus an independently supplied pinned manifest exist, run `python3 scripts/source_lock.py MANIFEST.json SOURCE.txt`; it checks Git blob/SHA-256/text anchors but does **not** authenticate original retrieval or provider authority. See `../../docs/source-lock.md`.
3. Require provenance before SUPPORTED, raw test evidence before TESTED, and named original owner readback before RELEASE_CONFIRMED.
4. `READY` is only a proposal. Never launch an adapter from this skill; host must check registry, identity, permission, source pins and effect boundaries.
5. Negative cases: hallucinated operation, unconfirmed human answer, invalid link, duplicate key, empty delivery receipt, unknown effect and source drift.
6. For a prior/proposed card record pair run `python3 scripts/card_delta.py BEFORE.json AFTER.json`; refuse changed IDs, unbalanced revisions, stale cursors and a hidden non-card delta. Read `../../docs/card-delta-contract.md` for what it does not prove.
7. For v7.1/v7.2 N/C/P *curated structural* regressions run `python3 scripts/semantic_golden.py tests/fixtures/semantic-golden.json`. Read `../../docs/semantic-golden.md`. The result is never human semantic approval: it reports `semantic_quality_proven=false` and `human_review=REQUIRED_NOT_RUN`.
8. Report machine-checked proof boundary and remaining unknowns. A local fixture never proves source authenticity, upstream model performance or PR delivery.