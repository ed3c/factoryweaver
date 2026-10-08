---
name: factoryweaver-verify
description: Verify FactoryWeaver JSON contract validity, evidence references, human-decision boundaries, skill routing honesty and completion claims. Use before passing a specification to a software factory or reporting test, PR or delivery status.
license: MIT
---
# FactoryWeaver verification

1. Load `../../contracts/v1/knowledge-record.schema.json` and run the read-only CLI `validate`.
2. Check Source ID uniqueness, dependency and typed link reachability, and stable card IDs. For enumerated JD clause coverage, run `python3 scripts/requirement_coverage.py RECORD.json CLAUSES.json` on an explicit source inventory and read `../../docs/requirement-coverage.md`. Declared IDs do not establish source exhaustiveness or semantic validity.
3. Require provenance before SUPPORTED, raw test evidence before TESTED, and named original owner readback before RELEASE_CONFIRMED.
4. `READY` is only a proposal. Never launch an adapter from this skill; host must check registry, identity, permission, source pins and effect boundaries.
5. Negative cases: hallucinated operation, unconfirmed human answer, invalid link, duplicate key, empty delivery receipt, unknown effect and source drift.
6. Report machine-checked proof boundary and remaining unknowns. A local fixture never proves upstream model performance or PR delivery.