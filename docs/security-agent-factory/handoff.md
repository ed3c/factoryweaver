# Security Agent Factory — Soodles Session Handoff

**Purpose:** Zero-context continuation for the **specification-only**, canonical FactoryWeaver v7.2 Security Agent Factory work. Coverage uses both the [33-REQ decision ledger](source-coverage.md) **and** the [whole-conversation source inventory](source-inventory.md); decision completeness is not proof of full raw-source parity.  
**Date:** 2026-10-23. **HOF-01 A:** update this existing file on FactoryWeaver Draft PR #33; no second handoff owner or Soodles root handoff overwrite.  
**Status:** HUMAN SCOPE DECISION-COMPLETE; SEMANTIC CARD PROPOSALS WRITTEN; NATIVE COMPILATION / READ-ONLY CONSUMER NOT RUN; SECURITY RUNTIME NOT RUN.  
**Execution authority:** none conferred by this document; do not execute a Red/Blue attack task, modify security policies, create a Security Lab runtime, deploy, merge, or dispatch a worker from this handoff.

## 1. Start here — exact sources, not copied specifications

Repository: https://github.com/ed3c/factoryweaver  
Draft PR: https://github.com/ed3c/factoryweaver/pull/33  
PR branch: spec/security-agent-factory-v1-20261023 → main. Before this handoff update, the PR HEAD readback was a571d216ce059e2dc5b0f651667e2eb4b44f4b3d, with draft=true, state=open, merged=false. **This is historical pre-handoff provenance; retrieve the fresh PR HEAD and CI before taking further action.**

The four files under docs/security-agent-factory/ have distinct owners of meaning:

| Artifact | Authoritative purpose |
|---|---|
| [README.md](README.md) | Decision-complete SEC-01–16 architecture, revised SEC-10R/SEC-13R, trust boundaries, licensing and source links |
| [source-coverage.md](source-coverage.md) | 33 source/decision-to-REQ mappings, owner, positive acceptance, negative falsifier and named gaps |
| [cards.md](cards.md) | 41 FactoryWeaver v7.2 **semantic Card proposals** with typed-link proposals, including an initial four-slot BOOT preview |
| [handoff.md](handoff.md) | **This** next-session continuation, original owner actions, evidence ledger and stopping rules; does not duplicate the cards |

Additional original contracts:

- FactoryWeaver compiler: references/zettelkasten-v7.2.md; classification: references/card-classification-and-scope-assembly.md; entry: skills/factoryweaver/SKILL.md; official preparation: docs/record-preparation.md; exporter: scripts/soodles_handoff.py; transport: docs/factoryweaver-soodles-readback.md.
- Soodles Thinking Router: https://github.com/ed3c/soodles/blob/main/.agents/skills/thinking-router/SKILL.md; Ambitious Route: https://github.com/ed3c/soodles/blob/main/.agents/skills/ambitious-route/SKILL.md; original Outer/Inner: https://github.com/ed3c/soodles/blob/main/.agents/skills/thinking-router/references/loop-execution.md; source-bound Reader: https://github.com/ed3c/soodles/blob/main/contracts/factoryweaver-scope-v1.md.
- Soodles handoff source: https://github.com/ed3c/soodles/blob/main/.agents/skills/handoff/SKILL.md. This upstream skill is **manual-only** (disable-model-invocation: true); it calls for a temporary-OS-directory copy, suggested skills, secrecy redaction and links to existing artifacts. This Git-committed copy is **separately and explicitly requested by the user** under HOF-01 A. Do not claim the Skill tool was natively invoked merely because this document follows its instructions.
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
| HOF-01 A | Modify **only** docs/security-agent-factory/handoff.md in existing FactoryWeaver PR #33; commit there; leave PR Draft; no merge. |

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

**Observed in GitHub at handoff preparation:** PR #33 open/draft/not merged, four documents and 33 requirement rows, 41 unique semantic card sections. Source ledger names SEC-01–16 plus SEC-10R/13R; all are normative design items, **not runtime PASS**. Previous author checked static coverage and card-link name references; no claim of fresh independent semantic review or installed Skill-tool execution.

**NOT_RUN / UNKNOWN (must not be greenwashed):**
- Full original conversation exact-byte Source snapshot and verified Host source ownership; record and Card IDs/revisions/source SHA via actual FactoryWeaver `prepare` + original validator; source semantics acceptance.
- Original exporter materialization and exact-byte/refusal controls; Soodles `knowledge inspect` actual `source_bound_proposal` / `needs_source_readback` and fresh original Owner `next`.
- Native Poteto consumption / Test Manager selection / Schema feedback / genuine Red/Blue/White White Oracle.
- MacBook OpenShell VM and Podman runtime readiness, security and speed/memory baselines; exact images and licensing; Vault Replay ↔ OpenBao API compatibility.
- L1/L2 E2E, L3, Cloudflare deployment and Cloudflare read-only write-denial tests; CI status at future exact head; any provider effects or merge.

Known documentary limitations: `cards.md` contains **41 proposals**, not a `factoryweaver/v1` machine-validated canonical record. The historical recorded L1 exchange cannot prove real host authorization, mutation or exploit success. OpenShell MicroVM driver is experimental. OpenBao may differ from recorded Vault API behavior. No measured latency or cost improvement should be asserted.

## 5. First legal next actions for a fresh Session

This is a **source-bound specification/reader** continuation, not an attack task.

1. **Read fresh original owners:** PR #33 metadata/HEAD, this handoff and all three sibling artifacts, relevant Soodles/FactoryWeaver Skills/contracts and available Host/Provider state. If the branch changed, reconcile original source/accepted scope before edits. Never retry an uncertain write; read back first.
2. **Verify source coverage and card meaning:** reconcile original SEC-01–16 human decisions, later MacBook SEC-10R and Cloudflare SEC-13R, HOF-01 A, 33 REQ and 41 semantic proposal headers. Check actual mechanism, owner, positive/negative falsifier, typed-link direction and whether the first bounded proposed atom is still needed. Preserve 15-series taxonomy, the 4-slot BOOT display, full requirements and all deferred work without fake cards.
3. **Close missing source binding, if the original Host can:** obtain actual source bytes through the proper Source Reader and create a separate accepted source snapshot; use FactoryWeaver's real prepare/validation and selected registered type prompts. **The Registry/CLI computes** ID, revision, digests, timestamps, and cursor; do not handwrite them. If source bytes or Host permission are unavailable, keep K/source-binding as UNKNOWN and do not fabricate machine validation.
4. **Produce/verify read-only Bundle, if available:** original scripts/soodles_handoff.py generates one selected `factoryweaver/soodles-scope/v1` from the complete v1 record; original Host materializes exact bytes/reader_arguments, original Soodles `knowledge inspect` must return only source-bound proposal or named needs_source_readback, `effects=[]`, `next=null`, `authorizes_landing=false`; reject changed bytes, unknown IDs, duplicate/invalid references. Preserve parent inventory.
5. **Review and report:** source/semantic review and focused non-effect validation first; check current Draft PR head and actual CI; leave PR unmerged and do not convert it into security runtime authorization. If the current spec-only task is complete, explicitly report which of authoring, source, machine, native-consumer and Provider gates are PASS vs NOT_RUN.

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
- **factoryweaver-read** from Soodles (only after a real materialized v1 Scope Bundle, read-only); **review-writing** for actual engineering guidance; **test-manager** and **verify-soodles** only for selected real checks.
- **handoff** from Soodles is manual-only and requires a Host-supported Skill invocation; this committed handoff follows its redaction, deduplication and suggested-skill content contract, but **is not evidence of native invocation**.
- **outer-review / check / ponytail-review** only for concrete current diff/over-design questions; no mandatory multi-review cascade. **Noodle Poteto** only after separately authorized original admission.

## 8. One minimal Source-bound Prompt Delta for the successor

Goal: continue the **existing** Security Factory spec-only Goal, retaining all user decisions and 33 REQ / 41 proposals; preserve the Parent Goal and deferred runtime obligations.  
Measurement: complete Source→REQ fidelity, actual original v1 semantic/machine validation and source-bound Soodles read-only consumer evidence, each with negative refusals.  
Effort Horizon: stay within current spec/handoff authorization; no automatic future runs, Red/Blue activity, merging or Cloudflare deployment.  
First Causal Breakpoint: authentic source snapshot and original FactoryWeaver Registry/Reader native evidence are not yet observed.  
Method: Thinking V2 plus Ambitious Depth; V3 only if a new falsifiable source/ownership inconsistency appears.  
Constraints: HOF-01 A same branch/path, original Actor/Owner permissions, no duplicate canonical card file, no fabricated FileRef/IDs, no Frozen Stage rewrite, preserve distinct L1/L2/L3 evidence levels and OpenShell MacBook requirement.  
Verification: exact original Source/record/export/reader receipts and negative controls, not AI self-attestation.  
Stop: no new semantic decision → NOOP and consume valid original owner next; missing source/unknown effect → named BLOCKED/UNKNOWN and readback; native proof absent → NOT_RUN.

**Current handoff outcome:** zero-context successor instructions committed as a document-only handoff. This document must not claim that the subsequent source snapshot, real v1 compilation or Soodles reader execution have happened.

---
**Security note:** No secrets, access tokens, customer records, precise local file paths or private credentials are needed or provided in this file.
