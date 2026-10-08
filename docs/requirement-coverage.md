# JD → REQ / SPEC trace coverage (read-only contract)

This is a **bounded requirement coverage auditor**, not an extractor, job-market classifier, coding agent, or verified software factory.

## Why

The live [OpenAI Software Engineer, Plugin Developer Platform JD](https://openai.com/careers/software-engineer-plugin-developer-platform-san-francisco/) has six editorial responsibility groups under **What You'll Do**. The existing FactoryWeaver bootstrap example contains one requirement `REQ-api-sdk`, leaving five groups unmapped. A JSON Schema-valid record by itself cannot prove full requirement coverage.

## Source-normalized input

`examples/openai-plugin-platform/job-clause-inventory.json` contains six human-authored, **paraphrased** groups; each has stable `clause_id`, source locator, `SOURCE_PARAPHRASE` classification and zero or more declared `requirement_ids`.

The source registry uses `SRC-OPENAI-JD` with `integrity=UNPINNED`. These identifiers and paraphrases are untrusted input until a trusted retrieval owner freezes original source bytes. An arbitrary author can omit JD clauses from the inventory, so **this CLI cannot prove inventory exhaustiveness**.

No verbatim upstream JD is vendored. The six groups are a demonstration subset of job responsibilities, not a promise to parse every job requirement automatically or to endorse any hard-coded language/framework requirement.

## Execute

```bash
python3 scripts/requirement_coverage.py \
  examples/openai-plugin-platform/project.json \
  examples/openai-plugin-platform/job-clause-inventory.json
```

Expected structural result: `inventory_clause_count=6`, `declared_link_count=1`, and five `unmapped_clause_ids`. Existing first clause has one declared REQ and linked SPEC card.

## Proposed target: six distinct REQ/SPEC links (NOT VERIFIED)

A second fixture models **how the same six JD groups might be represented as portfolio engineering proposals**, with six separate REQ and six SPEC cards:

```bash
python3 scripts/requirement_coverage.py \
  examples/openai-plugin-platform/proposed-six-requirements.json \
  examples/openai-plugin-platform/proposed-six-clause-inventory.json
```

Expected *declared trace* count is six of six, with no omitted inventory clauses. These are **proposed normative FactoryWeaver design decisions**, not claims that the official JD prescribes FactoryWeaver architecture. Their `knowledge_status=ANCHORED`, `engineering_status=UNASSESSED`, and `delivery_status=NOT_STARTED` intentionally prevent inflated completeness.

The baseline (1/6) is preserved as a separate fixture. The proposed 6/6 inventory can still be wrong or incomplete; it has no original-source authentication, no independently checked semantic mapping, and no verified hosted Software Factory behavior. Do not treat this second fixture as completion of Issue #1, #5 or Soodles #300.

## Fail-closed criteria

- Clause inventory subject must match the knowledge-record subject exactly.
- Inventory source ID, dependency key and claimed pin state must match the actual record source fields.
- Clause IDs must be unique and stable; each clause must retain an explicit locator and paraphrase.
- Any `requirement_id` must exist and its own `source_ids` must include the inventoried source.
- Unknown or duplicate IDs, fake source pin, fake `claim_kind`, malformed inventory, and invented `complete:true` are refused.
- A requirement mapping cannot be credited for an unrelated source; a SPEC link is only a typed `implements` edge, not an executed acceptance test.

Output always preserves `source_exhaustiveness_proven=false`, `semantic_mapping_verified=false`, `engineering_verified=false`, `delivery_verified=false`, and `effect_authority=false`. A six-of-six declared link count would be **declared structural trace coverage**, not six verified job duties or a deployable software system.

## Bounded next loops

The next independently owned steps are (1) source retrieval and anchor verification; (2) human/adversarial review of six paraphrases versus the raw official JD and the user-specified development outcomes; (3) append REQ/SPEC cards with real acceptance/falsifiers, preserving unique source dependencies; (4) test the Skill in an actual Agent host; (5) private Soodles/Noodle or other Auto-PR owner admission, then independent runtime/landing readback. Do not widen this read-only public auditor into host authority.

## Links

- [Agent Skills Specification](https://agentskills.io/specification)
- [FactoryWeaver parent outcome](https://github.com/ed3c/factoryweaver/issues/1)
- [FactoryWeaver read-only bootstrap](https://github.com/ed3c/factoryweaver/pull/3)
