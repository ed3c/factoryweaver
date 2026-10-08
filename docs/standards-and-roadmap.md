# FactoryWeaver — Engineering coverage and standard boundaries

## Purpose
Turn an external requirement (job description, user story, issue, bug or document) into evidence-anchored REQ/SPEC cards, a human-readable Zettelkasten view and a machine contract. The consumer host owns all actual tool/CI/PR effects. FactoryWeaver is **not** a generic PR runner or replacement host Schema Manager.

## Normative / optional official references

| Contract | Reference | Status |
|---|---|---|
| Agent Skills SKILL.md | https://agentskills.io/specification | structural format only |
| JSON Schema 2020-12 | https://json-schema.org/draft/2020-12 | reference data validator |
| OpenAPI 3.2.1 | https://spec.openapis.org/oas/v3.2.1.html | optional external HTTP/SDK |
| MCP protocol | https://modelcontextprotocol.io/specification/2026-07-28 | optional remote tool adapter |
| GitHub Actions | https://docs.github.com/en/actions | actual workflow runs must be checked by exact head |

Source dates, package installations and host capabilities must be verified independently; nothing here claims upstream/runtime compatibility.

## User-facing end-to-end layers

| Layer | Known from current PR | Unknown / required owner evidence |
|---|---|---|
| Job description / request | synthetic, source-linked example | source capture and original bytes for genuine new input |
| Zettelkasten narrative/cards | v7.2 reference Prompt, sample cards | complete v7.1 semantic richness, lossless cursor, registry replay |
| Machine REQ/SPEC data | JSON Schema 2020-12 | real source change invalidation, attachment digest readback |
| Skill entry | three public SKILL.md with frontmatter | real upstream skill execution under an installed host |
| CLI routing | read-only deterministic candidate projection | host registry provenance and actual permissible capability |
| API/SDK | schema only | versioned SDK contract + external consumer |
| MCP/Plugins | optional documentation | real tool transport/authentication/negative cases |
| Noodle / Soodles | external owner boundary documented | independent admission / Noodle writer / runtime / landing |
| Test / CI | public focused tests and PR workflow | host production-equivalent verification and live use |
| Observability | evidence fields | source-pinned trace, cost, latency, failure telemetry |
| Delivery / release | evidence status cannot claim release | merge/release/activation receipt from original authority |

## Work DAG with explicit evidence ceilings

```text
1. Bootstrap #2: SKILL + JSON schema + read-only CLI + fixtures
   └─ PR #3 exact-head CI (structural/runtime-local only; merge separate)
2. Zettelkasten semantic regression: full v7.1 contract / card revision / source cursor
3. Real Matt grilling interview -> human confirmation, no self-answer
4. Private Soodles/Noodle independent owner binding (not part of public runtime)
5. A second Auto-PR host, paired frozen task, negative controls, independent receipt
6. Release/naming/license/security review and external-user onboarding
```

## Data-driven loop contract
`source → assertions → decision/REQ/SPEC → dependency DAG → candidate operation → host-owned act/readback → evidence revision → only-affected-node projection`.

The reference CLI currently handles **candidate selection** and never operates a tool. No valid JSON or successful local test may set `effect_authority=true`. Progress axes (knowledge, engineering and delivery) are separate. Absence of evidence must remain unknown or blocked, not PASS. No model can award its own TESTED / RELEASE_CONFIRMED.

## Disallowed promotion
- passing JSON validation ≠ upstream skill behavior;
- GitHub Actions green ≠ production runtime success;
- public PR merged ≠ Soodles issue complete;
- fixture-only owner metadata ≠ a physical provider readback;
- Source hash written in JSON ≠ independently compared source bytes;
- a proposed operation ID ≠ executable command or authority.

## Rollback
Each public candidate remains a draft PR until exact-head CI and human/owner acceptance. The private consumer gets separate authorization, exact release/source pin and rollback. Public skill updates never silently rewrite private Soodles admitted task envelopes.
