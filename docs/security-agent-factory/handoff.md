# Security Agent Factory — Soodles Session Handoff

**Purpose:** Zero-context continuation for the **specification-only**, canonical FactoryWeaver v7.2 Security Agent Factory work, now including the accepted **FW-MIG-01 A / FW-MIG-02 A / FW-MIG-03 A** Migrate Class Source→Card→Consumer semantic-parity review and cross-PR continuation. Coverage uses both the [33-REQ decision ledger](source-coverage.md) **and** the [whole-conversation source inventory](source-inventory.md); decision completeness is not proof of full raw-source parity.  
**Date:** 2026-10-23. **HOF-01 A:** update this existing file on FactoryWeaver Draft PR #33; no second handoff owner or Soodles root handoff overwrite.  
**Status:** HUMAN SCOPE DECISION-COMPLETE; SEMANTIC CARD PROPOSALS WRITTEN; NATIVE COMPILATION / READ-ONLY CONSUMER NOT RUN; SECURITY RUNTIME NOT RUN.  
**Execution authority:** none conferred by this document; do not execute a Red/Blue attack task, modify security policies, create a Security Lab runtime, deploy, merge, or dispatch a worker from this handoff.

## 1. Start here — exact sources, not copied specifications

Repository: https://github.com/ed3c/factoryweaver  
Draft PR: https://github.com/ed3c/factoryweaver/pull/33  
PR branch: spec/security-agent-factory-v1-20261023 → main. Before this handoff update, the PR HEAD readback was a571d216ce059e2dc5b0f651667e2eb4b44f4b3d, with draft=true, state=open, merged=false. **This is historical pre-handoff provenance; retrieve the fresh PR HEAD and CI before taking further action.**

The five Markdown files under docs/security-agent-factory/ have distinct owners of meaning (the adjacent source-only test is not another specification):

| Artifact | Authoritative purpose |
|---|---|
| [README.md](README.md) | Decision-complete SEC-01–16 architecture, revised SEC-10R/SEC-13R, trust boundaries, licensing and source links |
| [source-coverage.md](source-coverage.md) | 33 **decision-derived** REQ mappings, owner, acceptance, negative falsifier and named gaps; not complete original-source ingestion |
| [source-inventory.md](source-inventory.md) | Original named research/security tools, proposed defenses, selected/deferred/rejected alternatives, hypothesis and evidence-level dispositions |
| [cards.md](cards.md) | 41 FactoryWeaver v7.2 **semantic Card proposals** with typed-link proposals, including an initial four-slot BOOT preview |
| [handoff.md](handoff.md) | **This** next-session continuation, original owner actions, evidence ledger and stopping rules; does not duplicate the cards |

Additional original contracts:

- FactoryWeaver compiler: references/zettelkasten-v7.2.md; classification: references/card-classification-and-scope-assembly.md; entry: skills/factoryweaver/SKILL.md; official preparation: docs/record-preparation.md; exporter: scripts/soodles_handoff.py; transport: docs/factoryweaver-soodles-readback.md.
- Soodles Thinking Router: https://github.com/ed3c/soodles/blob/main/.agents/skills/thinking-router/SKILL.md; Ambitious Route: https://github.com/ed3c/soodles/blob/main/.agents/skills/ambitious-route/SKILL.md; original Outer/Inner: https://github.com/ed3c/soodles/blob/main/.agents/skills/thinking-router/references/loop-execution.md; source-bound Reader: https://github.com/ed3c/soodles/blob/main/contracts/factoryweaver-scope-v1.md.
- Soodles handoff source: https://github.com/ed3c/soodles/blob/main/.agents/skills/handoff/SKILL.md. This upstream skill is **manual-only** (disable-model-invocation: true); it calls for a temporary-OS-directory copy, suggested skills, secrecy redaction and links to existing artifacts. This Git-committed copy is **separately and explicitly requested by the user** under HOF-01 A. Do not claim the Skill tool was natively invoked merely because this document follows its instructions.
- Migrate Class source: Soodles original [PR #444](https://github.com/ed3c/soodles/pull/444), branch `codex/migrate-class-source-bound-parity`, exact reviewed head `c45d566e69bb074da33b63a89060022c893ff7de`; method [SKILL.md](https://github.com/ed3c/soodles/blob/codex/migrate-class-source-bound-parity/.agents/skills/migrate-class/SKILL.md) and [method.md](https://github.com/ed3c/soodles/blob/codex/migrate-class-source-bound-parity/.agents/skills/migrate-class/references/method.md). Use Soodles [state-machine change contract](https://github.com/ed3c/soodles/blob/main/contracts/state-machine-change.md) through the original FactoryWeaver `docs/state-machine-change.md` application, never as permission to create a second Owner.
- v7.2 original Compiler changes: FactoryWeaver [Draft PR #36](https://github.com/ed3c/factoryweaver/pull/36), branch `codex/v72-migrate-class-parity-tests-20261023`, reviewed pre-handoff head `1bf03b944e737a43708c8b27281927285ff0e48b`; references/zettelkasten-v7.2.md, docs/soodles-scope-routing.md, tests/test_migrate_semantic_parity.py and [evidence contract](https://github.com/ed3c/factoryweaver/blob/codex/v72-migrate-class-parity-tests-20261023/docs/evals/migrate-class-semantic-parity.md). The Source/CLI CI for this read HEAD passed; semantic/native proof is separate.
- External dependencies: https://github.com/ed3c/rea-environments ; https://github.com/NVIDIA/OpenShell/tree/main/crates/openshell-driver-vm ; https://openbao.org/ ; https://developers.cloudflare.com/workers/ .

## 2. Human intent and accepted decisions — do not re-ask

**Parent Goal:** an open-source, commercially usable, independently verifiable Red / Blue / White AI Security Factory. Measure actual attack prevention, legal-task completion, remediation evidence and cost per verified outcome, not scans/agent counts. Preserve later expansion to general Security Platform and Self-play/Agent RL, but **do not implement those in this task**.

**Current concrete Goal:** compile the entire accepted conversation into authentic FactoryWeaver v7.2 source-backed cards and a read-only, exact-byte-bound Soodles selection, with independent semantic/source review. No security runtime is authorized. The user's explicit HOF-01 A chooses the existing FactoryWeaver PR handoff path.

Decision anchor map (full semantics and per-REQ acceptance remain in README.md and source-coverage.md):

| Decisions | Fixed meaning |
|---|---|
| SEC-01 D, SEC-02 A | Self-owned factory first; Red tests, Blue detects/fixes, White reviews independently. White LLM output is not the ground-truth oracle. |
| SEC-03 B, SEC-04 B | Synthetic isolated lab first; staging needs its own authorization; Red limited lab testing and Blue repair PR allowed only under future proper admission; original Owner keeps merge/deploy. |
| SEC-05 A, SEC-06 A, SEC-07 B | Agent security threats first; REA L1 Replay and AgentEnv L2 Stateful; bounded resettable mutation; live L3 Strix/garak deferred. |
| SEC-08 B, SEC-09 | Gitea + Vault-compatible Secret API + Target Agent. OpenShell owns real sandbox/policy boundary. Historical VaultEnv-REA remains recorded evidence; OpenBao live service is a candidate subject to compatibility/license checks. |
| SEC-10 → SEC-10R | **Later MacBook-first revision prevails over native-Linux/Docker-first.** Apple Silicon OpenShell MicroVM/libkrun first candidate; Podman Machine fallback; both require the same native security controls. Experimental VM driver not production qualified on its name alone. |
| SEC-11 A, SEC-12 A | Fixed Run authorization/policy; scope increases require new original Owner Admission. New independent Security Lab runtime repo eventual consumer, not canonical Card owner. |
| SEC-13R A | Cloudflare receives open-source app / sanitized results presentation, **not** an assumed full OpenShell host. |
| SEC-14 A, SEC-15 A, SEC-16 A | Canonical record belongs in FactoryWeaver; **specification, validation, source-bound handoff only** this phase; Cloudflare Workers Dashboard/Results API read-only, **no remote dispatch**. |
| HOF-01 A and HOF-MIG-01 A | Canonical handoff stays **only** at PR #33 `docs/security-agent-factory/handoff.md`; PR #36 is the separate v7.2 Producer/Parity owner, PR #444 the original Soodles method owner. Do not overwrite Soodles `docs/handoff.md`; keep all PRs Draft and unmerged. |
| FW-MIG-01 A | Portable v7.2 adopts Host-independent Source→Semantic Parity rules; Soodles Host conditionally uses original installed Migrate Class, not a mandatory route. |
| FW-MIG-02 A | v7.2 Producer changes and regression tests belong to separate FactoryWeaver PR #36; Security Factory source omissions/case controls belong to PR #33. No cross-repo write expansion. |
| FW-MIG-03 A | Source/Semantic Differential and existing CLI positive/negative controls only for this phase; Native Agent Evals `NOT_RUN`. |

**Non-overridable hard gates:** accurate source/decision fidelity; open-source/commercial-use review of each code/image/model/dataset (hosted Cloudflare is not itself open source); explicit authorized asset scope; real OpenShell supervisor/host/network/secret isolation; independent oracle and Positive/Negative/Unknown/Replay controls; scoped immutable versions/receipts; unknown effect → original owner readback; frozen Stage never rewritten.

## 3. Original actors and evidence-trust boundaries

| Owner | Sole responsibility | Cannot infer from a handoff |
|---|---|---|
| Human + Supervising Session | Goal, Scope tradeoffs, real unresolved semantic decisions, selected source-backed atom | Extra security permissions, model consent from markdown |
| FactoryWeaver v7.2 Registry / original prepare & exporter | Full REQ/card/source record, generated IDs/revisions/digests and source-bound Bundle | Native Issue admission or actual security outcome |
| Soodles original Issue/Admission/Provider | Authorized write/effect boundary, actual Owner next, reviewed HEAD, landing decisions | Executable argv or policy grant from Card/Reader |
| Noodle Poteto inner, selected Test Manager | Future admitted worktree/Stage changes, selected tests and native worker results | Parent Goal completion from worker completed |
| OpenShell Policy/Host Owner | Future real network/process/filesystem/credential enforcement | Security qualification from official-support text |
| AgentEnv / REA owners | L2 synthetic state/reset and L1 recorded replay respectively | True live exploit from replay or simulator |
| White Oracle / evidence owner | Independent state, policy, effect and authorized-completion observations | PASS from White Agent self-report |
| Cloudflare deployment owner | Later read-only sanitized app publication | Any scanning/dispatch/merging right |

Thinking V2 uses original Goal/Measurement/Effort Horizon and the *first evidenced causal breakpoint*. Conditional V3 is only used for a falsifiable design counterexample that changes Scope, Owner or Verification. Ambitious Route primarily contributes **Depth**, measuring real improvement under the same acceptance contract. One Session fuses findings into a minimal **source-bound Prompt Delta**, or NOOP. Original owner continuation takes priority over repeated reasoning.

Outer Thinking → original admission → Inner Poteto → native readback/independent oracle → *only material* FactoryWeaver delta and Outer reconsideration. No new manager, parallel decision ledger, made-up `next.argv`, guessed hashes, or extra schedule. Known code defects remain inner; new source facts go to original reader; real semantic conflict alone returns to Thinking. New instructions reach only the next legal unfrozen Stage.

## 4. What actually exists vs what remains unproved

**Observed in GitHub at updated handoff preparation:** PR #33 open/draft/not merged, five Markdown documents (including a preserved named Source Inventory) and one scoped source-only test; 33 decision-derived requirement rows and 41 unique semantic card proposal sections. FactoryWeaver PR #36 and Soodles PR #444 remain distinct open/draft/unmerged original Producers. Source ledger names SEC-01–16 plus SEC-10R/13R; all are normative design items, **not runtime PASS**. Previous author checked static coverage and card-link name references; no claim of fresh independent semantic review or installed Skill-tool execution.

**NOT_RUN / UNKNOWN (must not be greenwashed):**
- Full original conversation exact-byte Source snapshot and verified Host source ownership; record and Card IDs/revisions/source SHA via actual FactoryWeaver `prepare` + original validator; source semantics acceptance.
- Original exporter materialization and exact-byte/refusal controls; Soodles `knowledge inspect` actual `source_bound_proposal` / `needs_source_readback` and fresh original Owner `next`.
- Native Poteto consumption / Test Manager selection / Schema feedback / genuine Red/Blue/White White Oracle.
- MacBook OpenShell VM and Podman runtime readiness, security and speed/memory baselines; exact images and licensing; Vault Replay ↔ OpenBao API compatibility.
- L1/L2 E2E, L3, Cloudflare deployment and Cloudflare read-only write-denial tests; CI status at future exact head; any provider effects or merge.

Known documentary limitations: `cards.md` contains **41 proposals**, not a `factoryweaver/v1` machine-validated canonical record. The historical recorded L1 exchange cannot prove real host authorization, mutation or exploit success. OpenShell MicroVM driver is experimental. OpenBao may differ from recorded Vault API behavior. No measured latency or cost improvement should be asserted.

## 5. First legal next actions for a fresh Session

This is a **source-bound specification/reader** continuation, not an attack task.

1. **Read fresh original owners:** FactoryWeaver PR #33 *and* PR #36 and Soodles PR #444 metadata/HEAD, this handoff and all four sibling Markdown artifacts, the two source-only test files, relevant original Skills/contracts and available Host/Provider state. If the branch changed, reconcile original source/accepted scope before edits. Never retry an uncertain write; read back first.
2. **Verify full source inventory and card meaning:** reconcile original SEC-01–16 human decisions, later MacBook SEC-10R and Cloudflare SEC-13R, HOF-01 A, HOF-MIG-01 A and FW-MIG-01–03 A; distinguish the 33 accepted-decision REQ from all original named source alternatives, and check 41 semantic proposal headers. Check actual mechanism, owner, positive/negative falsifier, typed-link direction and whether the first bounded proposed atom is still needed. Preserve 15-series taxonomy, the 4-slot BOOT display, full requirements and all deferred work without fake cards.
3. **Close missing source binding, if the original Host can:** obtain actual source bytes through the proper Source Reader and create a separate accepted source snapshot; use FactoryWeaver's real prepare/validation and selected registered type prompts. **The Registry/CLI computes** ID, revision, digests, timestamps, and cursor; do not handwrite them. If source bytes or Host permission are unavailable, keep K/source-binding as UNKNOWN and do not fabricate machine validation.
4. **Produce/verify read-only Bundle, if available:** original scripts/soodles_handoff.py generates one selected `factoryweaver/soodles-scope/v1` from the complete v1 record; original Host materializes exact bytes/reader_arguments, original Soodles `knowledge inspect` must return only source-bound proposal or named needs_source_readback, `effects=[]`, `next=null`, `authorizes_landing=false`; reject changed bytes, unknown IDs, duplicate/invalid references. Preserve parent inventory.
5. **Review and report:** use the separate original PR #36 v7.2 Prompt/Profile and matched source-only parity fixture as a *bounded* regression source; check PR #33 full inventory and invalid link correction without merging, replaying or rewriting PR #36. Source/semantic review and focused non-effect validation first; check all three current Draft PR heads and actual CI; leave PR unmerged and do not convert it into security runtime authorization. If the current spec-only task is complete, explicitly report which of authoring, source, machine, native-consumer and Provider gates are PASS vs NOT_RUN.

Do **not** invent a new Issue/Task/Worker because a read-only Reader has `next=null`. If a native Soodles original Issue Contract is missing, name the actual prerequisite. Existing Soodles `docs/handoff.md` belongs to a different task and must remain untouched.

## 6. Acceptance / source-claim ladder

| Gate | Required evidence | Status at handoff |
|---|---|---|
| A1 DECISION + SOURCE COVERAGE | SEC-01–16/10R/13R mapped; original semantic meaning and later overrides reviewed | STATIC WRITTEN; INDEPENDENT SEMANTIC REVIEW NOT_RUN |
| A2 CARD QUALITY | Complete v7.2 type prompts; evidence-backed SPEC implements REQ / SPEC validated_by V; negative falsifiers | SEMANTIC PROPOSALS; NATIVE REVIEW NOT_RUN |
| A3 v1 RECORD | Original prepare/validate, Registry-generated IDs and actual pinned Source | NOT_RUN |
| A4 EXPORT | Original immutable Bundle and same-byte/conflict-refusal controls | NOT_RUN |
| A5 SOODLES READ | Real knowledge inspect receipt, all original REQ, no effects/next | NOT_RUN |
| A6 ORIGINAL AUTHORITY | No false Issue admission, changed Frozen Stage, invented Provider write/next | DESIGN LIMIT; NATIVE NOT_RUN |
| A7 OPEN SHELL MAC | VM/Podman full allow/deny controls incl. host, credentials, mounts, network | DEFERRED / NOT_RUN |
| A8 L1/L2 | Recorded exact replay versus synthetic mutating/reset evidence | DEFERRED / NOT_RUN |
| A9 CLOUDFLARE | Sanitized GET; all write/dispatch/gateway routes denied | DEFERRED / NOT_RUN |
| A10 RED/BLUE/WHITE | Authorized task succeeds; forbidden secret read denied; independent truth protected | DEFERRED / NOT_RUN |
| A11 LICENSE | Per transitive code/image/model/data intended-commercial-use review | NOT_RUN |
| A12 EFFICIENCY | Qualified safety first, then matched cold/warm p50/p95/memory/cost | DEFERRED / NOT_RUN |

**Do not infer that green documentation/CI proves Runtime or user Goal complete.** Negative cases, missing native readback and provider-specific effects remain explicit. The new conversation should preserve these evidence ceilings.

## 7. Suggested Skills — ask the original Host Skill tool where available

- **factoryweaver** (canonical v7.2 compiler; load full source/classification contract and only selected type-specific leaf prompts); **verify-factoryweaver** for genuinely supported targeted checks.
- **thinking-router** (V2 default, bounded V3 only for a genuine causal conflict); **ambitious-route** (Depth; one fused minimum Prompt Delta, not standalone rewrite).
- **migrate-class** from **original Soodles PR #444**, only if the selected Soodles Host really has the matching installed version and a source-to-Consumer migration needs it (not automatic on every Card); **factoryweaver-read** from Soodles (only after a real materialized v1 Scope Bundle, read-only); **review-writing** for actual engineering guidance; **test-manager** and **verify-soodles** only for selected real checks.
- **handoff** from Soodles is manual-only and requires a Host-supported Skill invocation; this committed handoff follows its redaction, deduplication and suggested-skill content contract, but **is not evidence of native invocation**.
- **outer-review / check / ponytail-review** only for concrete current diff/over-design questions; no mandatory multi-review cascade. **Noodle Poteto** only after separately authorized original admission.

## 8. One minimal Source-bound Prompt Delta for the successor

Goal: continue the **existing** Security Factory spec-only Goal, retaining all user decisions and 33 REQ / 41 proposals; preserve the Parent Goal and deferred runtime obligations.  
Measurement: complete Source→REQ fidelity, actual original v1 semantic/machine validation and source-bound Soodles read-only consumer evidence, each with negative refusals.  
Effort Horizon: stay within current spec/handoff authorization; no automatic future runs, Red/Blue activity, merging or Cloudflare deployment.  
First Causal Breakpoint: B1's observed decision-coverage versus full-source-inventory conflation was corrected in PR #33 source-only artifacts, while authentic raw-conversation Source pin/Registry/Reader evidence and real B2–B5 Consumer parity are not yet independently observed.  
Method: Thinking V2 plus Ambitious Depth; V3 only if a new falsifiable source/ownership inconsistency appears.  
Constraints: HOF-01 A same branch/path, original Actor/Owner permissions, no duplicate canonical card file, no fabricated FileRef/IDs, no Frozen Stage rewrite, preserve distinct L1/L2/L3 evidence levels and OpenShell MacBook requirement.  
Verification: exact original Source/record/export/reader receipts and negative controls, not AI self-attestation.  
Stop: no new semantic decision → NOOP and consume valid original owner next; missing source/unknown effect → named BLOCKED/UNKNOWN and readback; native proof absent → NOT_RUN.

**Current handoff outcome:** zero-context successor instructions committed as a document-only handoff. This document must not claim that the subsequent source snapshot, real v1 compilation or Soodles reader execution have happened.

---
**Security note:** No secrets, access tokens, customer records, precise local file paths or private credentials are needed or provided in this file.


## 9. FW-MIG cross-PR continuation — **2026-10-23, HOF-MIG-01 A**

**Accepted and final adversarial review:** Thinking Router V2 (first evidenced Producer→Consumer breakpoint) × conditional V3 (planted counterexample) × Ambitious Route **Depth** found **no new user-owned Scope, write-owner, acceptance or handoff-location decision**. Stop questioning. One fused Prompt Delta only when the next permitted Consumer genuinely needs new instructions, otherwise NOOP. The existence of this new document section does not create another executable `next`.

### Exact reviewed PR and CI snapshots — re-read heads on next Session

| Original owner / repository | PR & reviewed HEAD (pre this handoff commit) | Actual GitHub CI readback | Authorization and acceptance ceiling |
|---|---|---|---|
| Security Factory source/case Owner, FactoryWeaver | [#33](https://github.com/ed3c/factoryweaver/pull/33) `de8954730598a6d7baa98641c19ace179a164126` | Run [39826251837](https://github.com/ed3c/factoryweaver/actions/runs/39826251837) **SUCCESS** at that exact HEAD | Documentation and source-only tests. Handoff update changes this HEAD; its new CI must be read again. |
| v7.2 Portable System Prompt, Soodles Host Profile + semantic-parity fixture Owner, FactoryWeaver | [#36](https://github.com/ed3c/factoryweaver/pull/36) `1bf03b944e737a43708c8b27281927285ff0e48b` | Run [39826396042](https://github.com/ed3c/factoryweaver/actions/runs/39826396042) **SUCCESS** | Matched **synthetic** source/consumer differential + original CLI refusals only; not universal Natural Language Parity. |
| Original Soodles engineering-method Owner | [#444](https://github.com/ed3c/soodles/pull/444) `c45d566e69bb074da33b63a89060022c893ff7de` | Run [39590124507](https://github.com/ed3c/soodles/actions/runs/39590124507) **SUCCESS** | Migrate Class source/methodology and source-only controls; not native Noodle Agent Evals. |

All three snapshots were **Open / Draft / Not Merged** when reviewed. Historical heads and CI are *immutable provenance*, not forecasts or authority for any future HEAD. This file update is authorized **only on PR #33**. Do not independently mutate #36 or #444.

### B1–B5 first inference breakpoints — original Producer and verification ceiling

| Boundary | Actual observation / earliest Producer | Source-bound repair and negative control | Remaining honest proof |
|---|---|---|---|
| **B1** Original discussion → Source Coverage | PR #33 original 33 REQ retained SEC decisions but omitted named tools and defensive sources. **Producer: original Security Factory Source Inventory** | PR #33 [source-inventory.md](source-inventory.md) lists ScopeSentry, PentAGI, CyberStrikeAI, ARTEX, promptfoo, REA, garak, Strix, Ghidra/Hopper, defense and selected/deferred/rejected status. `tests/test_security_factory_source_coverage.py` plants deleted-source cases. | **Source-only CI PASS**. Exact full conversation source bytes / independent 100% completeness **UNKNOWN**; do not say full raw-source parity proven. |
| **B2** Source → REQ/SPEC/Card/One-Shot Prompt | Form-valid rewrite might erase secret-access refusal or required Parent Goal. **Producer: v7.2 System Prompt / selected Card authoring; Consumer: chosen Scope/Prompt** | PR #36 `references/zettelkasten-v7.2.md` adds Reuse Before Rewrite, frozen matched before/after, legitimate neighbor and planted refusal/side-effect/ordered-event differences. See `tests/test_migrate_semantic_parity.py`. | Synthetic matched **source-only fixture/CI PASS**; independent whole-conversation semantic reviewer and actual Native Consumer behavior **NOT_RUN**. |
| **B3** Evidence document → Typed Card Link | Security Factory proposed `based_on:source-coverage` document path as if canonical Card identity. **Producer: PR #33 Card author; machine validator: original FactoryWeaver Registry** | PR #33 [cards.md](cards.md) reclassifies it as source locator; PR #36 tests original `factoryweaver.verify` refusal for an unregistered document path, not a second graph validator. | Source/CLI refusal controls PASS in their current exact-head CI; semantic graph completeness and real Registry materialization still **NOT_RUN**. |
| **B4** Card/Scope → admitted Noodle Stage | Printed One-Shot Prompt can exist without actual Writer consumption. **Owner: original Soodles Admission/Stage** | Preserve `factoryweaver/soodles-scope/v1` read-only Bundle and `knowledge inspect next=null, effects=[]`; no prompt projection can prove Stage instructions consumed or alter Frozen stage. | True `factoryweaver/v1` host prepare/export and Soodles knowledge reader on this Security Factory case **NOT_RUN**; fresh Native Stage/Schema/Owner receipt **NOT_RUN**. |
| **B5** local pass → verified Outcome | CLI valid, fake happy-path parity or White Agent report cannot prove permissions, independent correct outcome, or provider effect. **Owner: original Test Manager/independent Oracle/Provider** | PR #36 explicitly separates Source Identity, Consumer-observable Parity, Independent Semantic Correctness and Native Consumer/Provider Effect; PR #33 retains Red/Blue/White and L1/L2/L3 evidence ceilings. | Source-only Evals PASS at the stated fixtures only. Actual Security Factory Runtime / Cloudflare / OpenShell / Noodle / Provider tests **DEFERRED or NOT_RUN**. |

**Remaining genuine Unknowns:** complete raw conversation Source pin and revision/locator; original v1 Registry `prepare` + valid IDs/digest/cursors; semantic reviewer independently linking Source→Card→Consumer; Security Factory-specific read-only Soodles Reader receipt; original host/attempt and effect owner; MacBook OpenShell VM/Podman native isolation and memory/latency; OpenBao/Vault API/rights; Cloudflare real read-only deployment. These become K/source/owner observations, not forced questions to the user, new Product Requirements or false PASS.

### Migrate Class parity policy for the new Session

- **Portable v7.2** applies generic, Host-independent Source→Semantic Parity. The **Soodles Host Profile** may *conditionally* invoke original `migrate-class` only when available/version-pinned and material to an actual migration; it never creates a second executor or source-of-truth.
- Prefer existing target reuse → byte-preserving vendor → supported codemod → thin adapter → necessary semantic rewrite, but **do not migrate application code in this specification-only task**.
- Compare identical fixture inputs/version/seed and explicitly approved normalization; planted unchanged-happy-path wrong-refusal, wrong-side-effect, wrong-event-order, missing-parent and wrong-evidence-level controls must fail. Real semantic correctness is not established by a machine shape PASS.
- Adopt original [Soodles State Machine Change Contract](https://github.com/ed3c/soodles/blob/main/contracts/state-machine-change.md): locate first actual Producer→Consumer error; repair that original Owner, then re-drive only affected consumers. Do not rewrite every layer or alter `contracts/v1/knowledge-record.schema.json` to carry prose proposals. Soodles P-class guides decisions; CLI proves only its mechanical checks; Native Provider owns actual effects.
- **No implicit dependency or merge order** from PR numbers: #36 v7.2 code owner is separate from #33 Security Factory regression owner and #444 Soodles method owner. Their statuses must be checked before any later integration decision. Do not cherry-pick blindly or collapse two PRs into one.

### Minimal next-session contract after this handoff

**Read** PR #33's updated canonical handoff and five source documents; PR #36's v7.2 System Prompt/Profile, actual test and eval contract; Soodles PR #444 original method, and real fresh GitHub HEAD/CI. **Decide** only a *new* source-backed, falsifiable B1–B5 mismatch that changes original Owner, Scope or Verification; otherwise `PromptDelta=NOOP` and follow the original legal read-only spec workflow. **Verify** source completeness claims against genuinely available raw source, selected real Card/REQ references and original CLI/Reader refusals. **Stop** with named K/`NOT_RUN` if authentic Host data, semantic reviewer or Native Observer is unavailable. This handoff is not permission for Noodle/OpenShell execution, PR Merge, Cloudflare deployment, real-world pentesting or more repositories.

**Suggested skills specific to this continuation:** the original installed `factoryweaver` entry and `verify-factoryweaver`, Soodles `thinking-router`, `ambitious-route`, conditional original `migrate-class`, `factoryweaver-read` only for real Host-bound Bundle, `review-writing`, selected `test-manager`, and `handoff` only when natively exposed (its SKILL.md is manual-only). Refer to §7 for applicability; names in repository documentation are not proof that an active Host loaded or executed these skills.

**Exit of this handoff task:** exactly one committed modified file in the previously approved PR #33 branch, matching original GitHub Blob readback, fresh PR Draft/open/unmerged; no other effects. Do not claim this documentation update has itself completed a v1 compile, native Source/Consumer Parity or any Security Runtime.
