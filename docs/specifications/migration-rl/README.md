# Migration-RL — FactoryWeaver v7.2 Canonical Specification Cards

**FWC-01 A:** new canonical Knowledge Record in `ed3c/factoryweaver`, independent branch. **FWC-02 A:** deliver **only** machine-checkable cards/coverage and source review; no Soodles runtime/P-class modifications, native Migration-RL environment, real RL Evals, training, cross-repo write, PR merge or deployment.

## Artifact inventory

| File | Purpose / truth ceiling |
|---|---|
| `project.json` | Original `factoryweaver/v1` closed-schema Knowledge Record: 22 REQs, 74 distinct active REQ/SPEC/V/C/G/K/R cards, source registry and source-grounded links |
| `cards.md` | Human-readable full Card projection from the canonical record, not a second source of truth |
| `coverage.json` | MRL-01–10, MRA-01–18, FWC-01 A, FWC-02 A, HOF-01 A, source-to-REQ/card mapping |
| `scope.md` | Goal, Measurement, Persistence, Stop and four advisory sidecars for a future authorized Soodles Consumer |
| `verification.md` | Original FactoryWeaver read-only CLI commands and strict proof ceilings |
| `tests/test_migration_rl_spec_artifacts.py` | Spec-only original `verify()` contract and mapped-source coverage tests, discovered by the existing PR workflow |

## Human decisions and schema trust boundaries

MRL-01–08 A, **MRL-09 B**, MRL-10 A, FWC-01 A, FWC-02 A and HOF-01 A were confirmed in this conversation and recorded in `coverage.json`. The public FactoryWeaver `scripts/factoryweaver.py` **deliberately refuses any model-authored `human_confirmed=true`** in untrusted v1 records. Therefore `project.json` does **not** forge such a decision or an Owner authorization. The original Session/Requirement Owner can reconcile these existing human answers without re-asking the user.

Source URI paths can pin Git commits, but this card author has **not calculated raw Source SHA-256 bytes**; `integrity=UNPINNED` remains explicit. Host/Producer binding is necessary when actually exporting a selected Scope. A card's `source_ids` do not certify a native runtime claim.

## Existing source and original authorities

- [Migration-RL Soodles Issue #446](https://github.com/ed3c/soodles/issues/446)
- [Source-bound handoff with all accepted decisions](https://github.com/ed3c/soodles/blob/7feb3e9510611b229e2e370d00ec9d11812e115c/docs/handoffs/migration-rl/handoff.md)
- [Soodles migrate-class PR #444](https://github.com/ed3c/soodles/pull/444): open Draft when inspected; not in Soodles main
- [medium-compiler PR #72](https://github.com/ed3c/medium-compiler/pull/72): historical selected Chromium source-only coverage, not Native Agent behavior
- [FactoryWeaver v7.2 Card Classifications](https://github.com/ed3c/factoryweaver/blob/main/references/card-classification-and-scope-assembly.md), [Card Delta](https://github.com/ed3c/factoryweaver/blob/main/docs/card-delta-contract.md), original `contracts/v1/knowledge-record.schema.json`

## Explicit exclusions

This record does not reimplement the original Soodles/FactoryWeaver managers, assert AST/SCIP measured Precision ≥99%, produce Native source/target state, perform an independent RL Reward run, create a trainer checkpoint, or approve any cross-repository write. `knowledge=SPECIFIED`, `engineering=UNASSESSED`, `delivery=NOT_STARTED` are separate. Completion of the card compilation **does not mean the Migration-RL parent Goal is complete**.

## FWP Source-to-Consumer correction

FWP-01/02/03 A update v7.2 portable invariant, conditional Soodles source profile, SPEC/V semantic contents, source clause coverage and the first false dependency edge. Original prior state is retained under history/project-before-fwp.json; no Native improvement or Merge claimed.
