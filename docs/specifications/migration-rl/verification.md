# Migration-RL Specification — Verification Contract

## Canonical inputs and direct CLI

The original FactoryWeaver public Python CLI validates **shape, identities, permitted source/progress states, source refs and typed links**, not the truth of Human Intent, actual Runtime equivalence or RL training improvements.

```bash
python3 scripts/factoryweaver.py validate docs/specifications/migration-rl/project.json
python3 scripts/factoryweaver.py project docs/specifications/migration-rl/project.json
python3 -m unittest tests.test_migration_rl_spec_artifacts -v
```

On a PR, the repository's existing `verify-public-contract` workflow discovers `tests/test_migration_rl_spec_artifacts.py` without creating a parallel Test Manager. This record may be machine-validated by that workflow; actual native execution and Provider acceptance must be checked separately.

## Input completeness / semantic evidence

- User-confirmed FWC-01 A and FWC-02 A determine official producer and current authorization: cards-only.
- MRL-01–10 / MRA-01–18 / HOF-01 A fully enumerated in `coverage.json`. Formal public v1 validator disallows untrusted model-authored `human_confirmed=true`; retain raw human choice in the bound coverage/Owner readback, not forged record authority.
- Each MRA item has an original REQ ID plus a SPEC and a V card, with legal typed `implements`, `validated_by` and `depends_on` targets. Actual semantics require original source-based independent reviewer; schema-valid is not semantic acceptance.
- Each SPEC `Given/When/Then`, real Producer/Consumer boundary, negative, Unknown, Replay, selected independent Oracle and original Owner must be judged against the same original MRA requirement, not against an implementation invented by the Agent.
- Source URI can pin Git commit while source byte SHA256 is not computed; `UNPINNED` is deliberate. No cross-repository worktree is authorized by this record.

## Required discriminatory negatives

1. Fake `human_confirmed=true` cannot pass public original FactoryWeaver verifier.
2. Untrusted `TESTED_SCOPED` claim cannot pass with only card text.
3. Wrong typed target or fake `PINNED_SHA256` must be refused.
4. Source-only Chromium/browser PASS must not be promoted to a new Dual Native Agent execution.
5. Local PASS with outstanding original Human REQ must not close the Parent Goal.
6. An actual Runtime failure challenging a card assumption must generate a source-bound proposal to the original FactoryWeaver Producer, never rewrite Golden in place.
7. Unknown external write must use original Owner readback before retry.
8. AST/SCIP Precision≥99% must report independently labeled TP/FP/FN, Recall, query coverage and critical missing dynamic edges; none are measured in this specification phase.

## Current acceptance ceiling

- Knowledge: `SPECIFIED` (normative source-bound record).
- Engineering: `UNASSESSED`; source/prompt links have not been proven consumed by Native Noodle.
- Delivery: `NOT_STARTED` for Migration-RL; a documentation PR is separate.
- Migration-RL Native dual Runtime, Reward, policy/weights training, FactoryWeaver→Soodles card revision consumption, and whole-human-goal closure: `NOT_RUN`.
- The first actual source and target project remains AIFS/SeeCode → medium-compiler only as **future** original admission, not selected here for execution.

**Never treat this verification document or source-only CI result as legal admission, launch approval, native Actor evidence, PR merge or deployment.**
