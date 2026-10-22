# FactoryWeaver v7.2 — Migrate Class semantic parity evaluation contract

**Scope and authority:** source-only evaluation of the existing v7.2 System Prompt and Soodles-specific Host Profile. Derived from [Soodles migrate-class](https://github.com/ed3c/soodles/tree/codex/migrate-class-source-bound-parity/.agents/skills/migrate-class), which remains a separate **method**, not a FactoryWeaver validator, Agent, scheduler or permission source. Apply the pinned original [Soodles state-machine-change contract](../state-machine-change.md) only at its original producer/consumer boundary.

## Causal claim and first correction site

The Security Factory example originally had 33 confirmed-decision REQs and 41 Markdown Card proposals, but its evidence ledger omitted named background candidates such as ScopeSentry/PentAGI/CyberStrikeAI/promptfoo. It also proposed `based_on:source-coverage` as if a document were a registered Card ID. Thus:

- **Observed**: Decision coverage was not complete whole-conversation source inventory, and source/document locators risked promotion to Card identities.
- **Proposed correction**: Before a narrower REQ/Behavior Scope is selected, preserve complete actually available source units, approved decisions, deferred/rejected candidates, unknown evidence, and each unit's disposition; reuse the original Registry's real Card IDs and typed-link direction only.
- **Not established**: exact original conversation bytes, universal semantic equivalence, Native Noodle behavior, security effectiveness, Cloudflare/OpenShell deployment.

## Matched Source → Card → Consumer fixture and falsifiers

The bounded synthetic fixture in `tests/test_migrate_semantic_parity.py` freezes a Gitea Issue / restricted secret test. Before and After use the same input, Source clauses and Consumer. The original allowed outcome is issue read and legal completion. Forbidden outcome is secret read. The independent test oracle enumerates denied operations, denied side effects, exceptions, event order, original parent obligations and claim level.

| Comparison | Planted alteration | Expected discrimination |
|---|---|---|
| Same source/consumer | unchanged clone | No differences |
| Legitimate neighbor | permitted metadata read added | Explicit changed allowed behavior; do not silently normalize |
| False security equivalence | forbidden secret operation removed from deny set | Fail / mismatch even if happy path identical |
| Side-effect change | restricted secret export appears | Fail |
| Error and event behavior | AccessDenied becomes ValueError, or policy event order changes | Fail |
| Parent goal loss | unauthorized-secret obligation dropped | Fail |
| Evidence level | L2 synthetic declared L3 live | Fail |
| Source omission/wrong quote | a source clause deleted or replaced with its opposite | Fail |
| Link identity | original v1 record typed-link target changed to a Markdown pathname | Original Registry validator must reject `unknown_typed_link` |
| Card shape only | two conflicting SPEC cards each pass field-shape | Independent semantic review remains `NOT_RUN`, never PASS |

All cases are **synthetic source-only tests**. Their verdict does not certify genuine transformation equivalence of arbitrary natural language, real prompt loading, model/Host usage, or release acceptance. The original CLI still owns source/Card identity and action refusal; a human or independent semantic reviewer owns intent meaning.

## Expected verification and non-claims

Run the existing Python unittest discovery if its original Host/CI is available; do not claim it ran from this documentation alone. Reuse original FactoryWeaver `factoryweaver.verify` and `card_semantic.inspect` to show that structural validation accepts both plausible and corrupted prose while a distinct bounded oracle detects the corrupted claim. No new runtime validator or second Registry was introduced.

The Soodles Host Profile may select `migrate-class` *only* for genuine source-bound Semantic Migration with an installed, version-confirmed original skill. Routine source preserving card compilation does not run Migrate Class. Native Noodle/Provider parity remains `NOT_RUN` without fresh admitted Session/Attempt/independent Observer/Owner readback.

## Acceptance states to report separately

1. **Source identity and coverage:** observed/declared raw source units; unknown full conversation bytes remain `K`, not automatically COMPLETE.
2. **Matched synthetic consumer parity:** focused test fixtures and planted divergences; `PASS` only on those frozen fields and input cases.
3. **Independent semantic correctness:** reviewer confirms actual original intent, exceptions, role/authority and parent Goal; `NOT_RUN` if not performed.
4. **Native Consumer/Provider effect:** fresh Noodle Stage and external owner readback; `NOT_RUN` for this change.

Do not turn a source-only test or GitHub CI PASS into whole-product completion.
