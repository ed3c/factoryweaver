# Security Agent Factory — decision-complete specification (design-only)

**Status:** `SOURCE-BOUNDED SPECIFICATION DRAFT`; no runtime execution, no released security claims.  
**Date:** 2026-10-23  
**Authority:** user-confirmed Security Agent Factory decisions in the supervising conversation; source references below.  
**Canonical knowledge owner:** FactoryWeaver v7.2. **Consumer:** a *future*, separately authorized Security Lab repository, via the original Soodles read-only Source-bound Scope contract.

## Outcome

Build a commercially usable, open-source Red / Blue / White AI Security Factory whose results can distinguish recorded tool use from simulated state from independently proven live behavior. Preserve full human intent across FactoryWeaver cards, Soodles Outer Thinking × Ambitious Route, Noodle Poteto Inner execution, independent White Oracle evidence, and verified card feedback. Phase 1 is *specification and handoff only* (SEC-15 A). No attack workload, staging scan, rollout, production or merge authorization is conferred by these documents.

## Accepted decisions (no re-vote)

| Decision | User-confirmed outcome / controlling revision |
|---|---|
| SEC-01 D | Self-owned Security Testing Factory first; keep generic platform and agent RL as future directions |
| SEC-02 A | Red proposes/tests, Blue detects/repairs, White independently evaluates/oversees |
| SEC-03 B | Isolated synthetic lab first; staging only after separate asset/scope authorization |
| SEC-04 B | Red may run authorized lab tests; Blue may propose repair PR; merge/deploy remain original owners |
| SEC-05 A | AI Agent Security priority: prompt injection, tool misuse, privileges and secret boundaries |
| SEC-06 A | Phase-1 runtime trajectory: L1 REA Replay + L2 AgentEnv Stateful; L3 deferred |
| SEC-07 B | Bounded, resettable state mutation in isolated lab, never unbounded operations |
| SEC-08 B | Gitea + Vault-compatible secrets API + Target Agent reference environment |
| SEC-09 | NVIDIA OpenShell is the sandbox/policy runtime; independent security acceptance required |
| SEC-10R | MacBook Apple Silicon first; official OpenShell MicroVM/libkrun VM Driver first *candidate*; Podman Machine fallback; no runtime is qualified by naming it |
| SEC-11 A | One run has immutable authorized scope; policy expansion requires original owner re-admission |
| SEC-12 A | Independent Security Lab repository as eventual runtime target; FactoryWeaver retains card provenance |
| SEC-13R A | OpenShell execution on supported host; Cloudflare control plane only, no unproven Cloudflare sandbox |
| SEC-14 A | Canonical card source in FactoryWeaver; Security Lab consumes selected source-bound scopes |
| SEC-15 A | Finish specification/cards, validation and read-only handoff; application/runtime implementation separately authorized |
| SEC-16 A | Cloudflare Workers Phase 1 read-only dashboard/results API; no remote test dispatch |

**Overrides:** MacBook-first SEC-10R supersedes the older native-Linux/Docker-first *host selection* but not the OpenShell hard gate. SEC-13R A is preserved: Cloudflare does not host an unqualified OpenShell execution layer. Raw `VaultEnv-REA` historical replay remains unchanged as recorded evidence; a future *live* secrets service should prefer OpenBao (MPL-2.0), contingent on API compatibility tests. HashiCorp Vault BUSL-1.1 is not interchangeable with an OSI open-source implementation.

## Contract layers and permitted evidence claims

1. **L1 / REA**: recorded exchanges, read-only replay, source-backed tool-use / retrieval evaluations. No real mutation and no claims of vulnerability exploit success.
2. **L2 / AgentEnv**: synthetic RBAC, mutation, reset, virtual time and cross-tool state. Simulated authorization proves only the simulation contract. OpenShell owns *real* process/network/filesystem/credential policy.
3. **L3 / isolated live services**: deferred Strix / garak and real isolated-system checks. This phase cannot be passed or scheduled by an L1 or L2 green result.
4. **White Oracle**: independent evidence producer outside Red/Blue modification and credential boundaries. White Agent may interpret evidence; it cannot create the ground truth or authorize effects.
5. **Cloudflare**: sanitized, read-only presentation. No Gateway, credential or execution endpoint exposed to the public internet.

## Hard gates

- **Authorization:** explicit allowlisted target and tool scope; red/blue cannot alter owner policy or white oracle. Unknown side effects require original owner readback, *never* blind retry.
- **OpenShell:** specific MacBook + VM/Podman version must prove actual enforcement (negative egress, API, secret, bind-mount, host control and cross-sandbox tests). Official support is not actual native PASS; VM driver documentation currently calls it Experimental.
- **License:** license inventory for code, data, models, images and transitive runtime dependencies; commercial-use permissions and redistribution obligations separately verified. Hosted Cloudflare service is *not* itself an open-source runtime.
- **Verification:** same build, policy, image, environment, and source/digest are bound to traces and receipts; unknown/unrun is never converted to PASS.
- **Non-degradation:** positive controls demonstrate permitted work can complete; blocking everything is not a successful defense.
- **No authority by text:** cards, scope selection, PromptDelta, CLI input shape, reader `source_bound_proposal`, PR body and graph presentation never constitute admission or real effects.

## Behavior and architectural documents

- [Complete source/requirement coverage](source-coverage.md): accepted SEC decision anchors, clauses, owners, acceptance and unresolved premises.
- [Whole-conversation source/alternative inventory](source-inventory.md): original security tools, defensive principles, selected/deferred/rejected candidates and explicit fidelity gaps; **decision coverage is not complete source coverage**.
- [Specification cards](cards.md): semantic C / REQ / SPEC / G / V / K / X / R cards and directional typed-link proposals, with explicit evidence limits.
- [Read-only handoff and scoped acceptance](handoff.md): first proposed Issue Atom, original Soodles owner path, tests, negative controls and rollout boundary.

**No created or verified machine `factoryweaver/v1` record is claimed by these Markdown files.** Materialization requires original `factoryweaver prepare` (which owns IDs, revisions, source digests), original verifier, exporter and Soodles knowledge reader. Do not invent those computed fields or equate a document commit to native acceptance.

## Primary sources

- [FactoryWeaver v7.2 compiler](../../references/zettelkasten-v7.2.md), [Card classification](../../references/card-classification-and-scope-assembly.md), [dedicated Soodles handoff](../../docs/factoryweaver-soodles-readback.md)
- [Soodles Thinking Router](https://github.com/ed3c/soodles/blob/main/.agents/skills/thinking-router/SKILL.md), [Outer/Inner contract](https://github.com/ed3c/soodles/blob/main/.agents/skills/thinking-router/references/loop-execution.md), [Scope Reader](https://github.com/ed3c/soodles/blob/main/contracts/factoryweaver-scope-v1.md)
- [REA environments fork](https://github.com/ed3c/rea-environments), [OpenShell VM Driver](https://github.com/NVIDIA/OpenShell/blob/main/crates/openshell-driver-vm/README.md), [OpenShell runtime docs](https://docs.nvidia.com/openshell/latest/how-it-works/sandboxes/runtimes)
- [Cloudflare Workers](https://developers.cloudflare.com/workers/), [OpenBao](https://openbao.org/)

**Source fidelity:** SEC decisions above come from the user’s explicit conversation messages, not from the linked repositories. The conversation is not a public machine-readable source file; its exact-byte Host source binding remains a named handoff prerequisite. Source code URLs establish documented capabilities or limitations, not actual running deployments.
