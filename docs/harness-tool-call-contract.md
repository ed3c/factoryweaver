# FactoryWeaver → Codex MCP: original CLI tool-call boundary

Status: **design and existing-CLI wiring**, not proof that a Host installed a Plugin or that a Noodle Writer consumed a generated Scope. The current FactoryWeaver v7.2 CLI already implements read-only validation, projection and advisory routing. Do not duplicate it inside a second MCP-specific rules engine.

## First incorrect inference and repair owner

FactoryWeaver Cards are source-grounded **knowledge data**, not executable instructions. The Session chooses an unresolved semantic Goal, REQ/SPEC/V coverage and one minimal Behavior Scope. The original `factoryweaver.py` Validator/Registry already decides record shape, registered identities, pinned-source status and non-authorizing route status; the original `card_semantic.py` chooses only registered Card references. If the Session would reselect these from prose, consume the existing deterministic CLI output instead.

The candidate Codex plugin is in [NeoWeaver PR #18](https://github.com/ed3c/NeoWeaver/pull/18). `factoryweaver_project({record_path, operation})` calls one original `python scripts/factoryweaver.py validate|project|route <record>`; operations are a closed enum. `record_path` stays inside the exact-head configured FactoryWeaver checkout. Its output is `OWNER_RESULT` or `OWNER_REFUSAL` plus unchanged original CLI data; it cannot produce a Noodle admission, true Host system-role prompt, real Issue next, tests, or effect permission.

`soodles_knowledge_inspect({bundle_ref})` belongs to **Soodles** and consumes the original Host-exported Bundle FileRef; FactoryWeaver does not issue its own substitute Soodles admission or derive missing Bundle SHA in model prose. The file may live in an authorized evidence area outside the FactoryWeaver checkout. The original Host/Producer supplies the path and computed SHA.

## State, tool call and refusal

| Input | Original CLI | MCP wrapper behavior | Proof ceiling |
| --- | --- | --- | --- |
| v1 knowledge record at source-pinned path | `validate` | Return exact original validation or named refusal | Schema/declared source shape only |
| Same record, current source pins | `project` | Return original knowledge/engineering/delivery projection | Does not mean current Agent followed cards |
| Registered action request | `route` | Return original advisory `HOST_REGISTRY_REQUIRED / REGISTERED_CANDIDATE_ONLY / WAIT_FOR_SOURCE_PIN` | `can_execute=false` even with registered-looking metadata |
| Scope Bundle with original FileRef | Soodles `knowledge inspect` | Use Soodles MCP tool, never FactoryWeaver local imitation | `next=null` means no effect |
| Missing/changed source, outside-root path, malformed JSON, oversize result | Original owner or bounded adapter | Typed refusal, preserve original source and no fallback | Never silent success |

Do not automatically run every Boot/Drill leaf Skill because a Card mentions it. Do not use an MCP call to reclassify a Card or replace the Session's causal judgement. A response marked `source_bound_proposal` is only evidence for the original Soodles Issue/Admission decision.

## Idempotence limits and paired validation

Read-only queries are repeatable only while **source commit, original record bytes and host conditions** match; the MCP wrapper verifies the configured source HEAD, and the original CLI verifies its own declared source integrity. This is not a guarantee of full semantic content correctness. Action Fusion, compaction, log reduction and Tool Result interception are **separate Host capabilities**; Codex MCP alone cannot intercept all native tools, perform atomic edit+test, or grant actor rights.

For real tests use the original FactoryWeaver fixture-positive + source/registry-refusal controls, followed by **fresh Codex native Tool Call consumption** on a held-out selected Scope, and the original Soodles Test/Schema/Provider readbacks where a downstream effect is due. Source tests are not native evidence. See Soodles [single-owner Harness Tool Call contract](https://github.com/ed3c/soodles/blob/main/docs/harness-tool-call-contract.md) (link valid only after corresponding merge).

## P-class implication

P-class asks Session to (a) identify unresolved Goal/causal semantics and (b) choose the minimum applicable Scope. It no longer asks the model to recompute registered CLI routes, digests, Card identities, Bundle argv, Manager tests or owner next. Any still-required uncertainty becomes a named source/Owner input; if no new behavior change exists, `PromptDelta=NOOP` without dropping the original parent Goal. Preserve the full source evidence, type-links, and three independent proof levels.
