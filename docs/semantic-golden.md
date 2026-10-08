# Semantic Golden Fixtures — declared-case structural gate

This is the first **bounded** v7.1 → v7.2 regression specimen for [Issue #4](https://github.com/ed3c/factoryweaver/issues/4). It is **not** an autonomous semantic judge, an authenticated retrieval system, or a full proof that v7.2 preserves the readability of v6.6.

## Why this fixture exists

A schema can accept a card that lists fields but explains nothing. It can also split one decision-relevant case across several thin cards, or collapse two different falsifiers into one card. The user-authored v7.1 specification requires:

- One *decision-relevant case* per card, with compatible evidence.
- Narrative (N): tension → observed situation → decision/turn → outcome → unknown.
- Concept (C): definition + causal mechanism + explicit non-goals, boundaries and counterexample.
- Practice (P): executable steps with validation/failure signals, independent evidence and rollback.

This fixture uses **synthetic normative scenarios**, not verified claims about external systems. Each case is explicitly annotated by a curator with `entity`, `event`, `scope`, `decision_use`, `falsifier`, `evidence_compatibility` and `card_id`. The comparator **does not derive** this identity from unrestricted prose.

## Executable probe

```bash
python3 scripts/semantic_golden.py tests/fixtures/semantic-golden.json
python3 -m unittest discover -s tests -p 'test_semantic_golden.py' -v
```

The fixture has four observations mapping to three decision-relevant cases and three cards. Two observations of the same interview episode belong to one N card; Source Drift and Delivery Readback have different falsifiers and therefore map to distinct C/P cards.

Planted negatives test:
- same signature mapped into different cards (**fragmentation**);
- different signatures mapped into the same card (**hidden compression**);
- missing Narrative turn / Concept mechanism / P rollback or step oracle;
- `TESTED` declared in an unexecuted P card;
- faked reviewer approval, orphan cards, duplicate identity.

## Evidence ceiling

`STRUCTURAL_GOLDEN_PASS` only proves the **fixture's declared partition and required field presence** passed deterministic checks. A malicious author can populate fields with impressive but false prose; a text-length check cannot establish semantic yield, citation integrity or independent evidence. Consequently `human_review=REQUIRED_NOT_RUN`, `semantic_quality_proven=false`, `source_veracity_proven=false` and `effect_authority=false` are fixed outputs, never promoted by the fixture itself.

Independent blind-pairwise v7.1/v7.2 narrative review, authentic source excerpts and an end-to-end real Skill/Host evaluation remain required. No external provider writes or automatic PR activity occur here.

## Related identity invariants

The [Card Delta contract](card-delta-contract.md) owns exact stable-ID changes, strict revisions, source-linked invalidation and batch cursor binding. Its `noncard_sections_changed` result records updates to Sources, Decisions, Requirements, ActionRequests and Progress *even when a Card Patch also exists*, blocking `DONE` until the original owner reconciles those noncard differences. Source history may not silently disappear.
