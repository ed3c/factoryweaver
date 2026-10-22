# Security Agent Factory — Whole-Conversation Source & Alternative Inventory

**Scope:** Supplemental **source-role catalogue**, not new accepted security execution requirements, and not a raw verbatim conversation transcript. The user's SEC-01..16, SEC-10R/13R and HOF-01 decisions remain the authoritative selected Scope in [README.md](README.md) and the [33-REQ ledger](source-coverage.md).

**Why this file exists:** Earlier 33 REQ cover major user-confirmed decisions but omit several *named starting sources* and defensive practices. A four-slot Boot or a deliberately narrow Behavior Scope may exclude a source from implementation **without deleting it from the knowledge inventory**. Neither source mention nor advisor recommendation grants test/scan authority.

## Source classification — beginning of this conversation

| Mentioned source / proposal | Original role and source locator | Selection / fidelity boundary | Next requirement or disposition |
| --- | --- | --- | --- |
| [ScopeSentry](https://github.com/Autumn-27/ScopeSentry) | Candidate Asset Discovery / subdomain/port/asset inventory cited in original message; current upstream details not freshly verified | **REFERENCE / DEFERRED**: useful for future asset inventory; first Goal prioritizes Agent Security and isolated synthetic assets | Source candidate, not Phase-1 scanner and not approved real-world reconnaissance |
| [REA](https://github.com/morluto/rea) | REA reverse engineering / capture ecosystem, including Ghidra/Hopper discussion | **REUSED CONCEPTUALLY**: distinct REA tool framework vs actual `ed3c/rea-environments` replay bundles | Keep reverse engineering and replay export separate; REA binary analysis is not an L1 test |
| [ed3c/rea-environments](https://github.com/ed3c/rea-environments) | 44 environment source-reported recordings and generated bundles; recorded retrieval/replay | **SELECTED L1**: read-only replay, source-reported counts, no real writes or live vulnerability proof | REQ-006, REQ-029; exact-match/nearest ambiguity; no security PASS from replay |
| [Strix](https://github.com/usestrix/strix) | Multi-agent offensive testing candidate | **DEFERRED L3**: only authorized isolated live lab after later explicit permission | REQ-008; no Phase-1 execution |
| [PentAGI](https://github.com/vxcontrol/pentagi) | Sandboxed multi-agent pentesting candidate, memory/tools | **REFERENCE / DEFERRED**: evaluate security/isolation and license prior to any future adoption | No automatic combined super-agent or sandbox replacement |
| [CyberStrikeAI](https://github.com/AIPentest/CyberStrikeAI) | Agent/tool orchestration and policy/control-plane candidate | **REFERENCE / DEFERRED**: Soodles/OpenShell original owners take precedence; no second scheduler or automatic attack-chain driver | Future comparison only, not a present dependency |
| [ARTEX](https://github.com/Hinln/ARTEX) | Asset graph / Human-in-the-loop architecture reference; originally discussed integration with ScopeSentry | **HISTORICAL SOURCE**: backup/maintenance provenance and abuse concerns must be verified before reuse | Do not rely on it as maintained production prerequisite; no rights to external targets |
| [garak](https://github.com/NVIDIA/garak) | LLM-focused vulnerability test candidate | **DEFERRED L3** for native security-testing claims; possible future focused model eval after separate approval | REQ-008; no live model scan authorized |
| [promptfoo](https://github.com/promptfoo/promptfoo) | Prompt / agent red-team evaluation and CI regression candidate | **EVAL TOOL REFERENCE / DEFERRED**: do not execute untrusted script hooks on privileged CI runner | Distinguish evaluation candidate from Soodles existing Test Manager owner |
| Traditional patch and exposure practices | Version/asset inventory, patching, disable unused ports, uploads and debug interfaces, least exposure | **DEFENSIVE PRINCIPLES / CONTEXT**, not a blanket new Phase-1 implementation mandate | Map to original G/Scope/Policy if a later selected threat scenario needs them |
| Identity and secrets hygiene | API key lifecycle, secret scanning, OIDC/short-lived credentials, least privilege, bulk export alerts / audit logging | **DEFENSIVE PRINCIPLES / CONTEXT**: some original claims (e.g. exact PingCAP entry path) were not independently proven | Existing REQ-002, REQ-012, REQ-016, REQ-028 and future differentiated SPEC; do not assert confirmed incident root cause |
| Security economics assertion | Claims that offensive cycle drops from months to days and team cost to single operator | **HYPOTHESIS / NOT MEASURED**: no direct comparable baseline in current source | Future K/experiment only, never used as actual recorded gain |

## Decisions and later platform candidates

| Candidate / design element | User-originated selection | Disposition |
| --- | --- | --- |
| [AgentEnv](https://www.agentenvframework.com/) | L2 Stateful Environment + synthetic RBAC, mutations and reset | SELECTED L2. Simulated Role headers are not trusted OpenShell host authorization. |
| Red / Blue / White independent roles | SEC-02 A plus later Oracle separation | SELECTED. Red tests, Blue repairs/PR proposals, White reviews; programmatic/owned independent ground truth. |
| NVIDIA [OpenShell](https://github.com/NVIDIA/OpenShell) | SEC-09 and SEC-10R MacBook-first refinement | SELECTED policy boundary; **MicroVM/libkrun first capability candidate, Podman Machine fallback**; neither native qualified yet. |
| Docker Desktop / OrbStack / Colima / Linux Docker / Cloudflare Containers | Explored alternatives across earlier questions | DO NOT REVIVE stale Docker-first requirement. The accepted priority is MacBook-first official OpenShell support, full safety proof before speed, open-source commercial licensing; unqualified Cloudflare nested Docker not accepted. |
| [Cloudflare Workers](https://developers.cloudflare.com/workers/) / [workerd](https://github.com/cloudflare/workerd) | SEC-13R A and SEC-16 A | SELECTED **read-only** cloud results UI/API. Hosted Cloudflare is not itself fully open-source infrastructure. No remote test dispatch or public Gateway. |
| HashiCorp Vault replay vs [OpenBao](https://openbao.org/) | SEC-08 B and licensing clarification | Keep historical `VaultEnv-REA` unchanged; OpenBao is proposed open-source live implementation; parity and licensing still untested. |
| Soodles Thinking V2 / conditional V3 × Ambitious Depth / Noodle Poteto | User explicitly required the cognitive/engineering interaction | SELECTED method split; one Session, original Owner continuation, independent measurements, never new effect permission. |
| [Soodles migrate-class](https://github.com/ed3c/soodles/tree/codex/migrate-class-source-bound-parity/.agents/skills/migrate-class) | Later conversation asks to use its **methodology** to review FactoryWeaver | METHOD REFERENCE: Reuse Before Rewrite, structural source selection, matched Consumer-visible parity, differential/planted negative controls; not a new runtime gate or a replacement compiler. |
| FactoryWeaver v7.2, 15 card series, fixed four-slot presentation | SEC-14 A, SEC-15 A, HOF-01 A | CANONICAL SPEC OWNER and presentation constraints; 33 REQ/41 **proposals** are not `factoryweaver/v1` native validated cards. |
| Agent RL / Self-play, general multi-application security platform | SEC-01 D | DEFERRED PRODUCT GOAL, preserve source/decision references; no authorized RL training or broad security scanning. |

## Source-to-Consumer discrimination

This is a *source inventory* of explicit discussion subjects, not independently inspected bytes of every upstream repo nor of the original conversation. Fresh Host capture of user decisions remains `UNKNOWN` and **cannot** be replaced by this prose.

Matched negative controls for any proposed `Source → REQ → SPEC/V → Scope → One-Shot Prompt` transfer:

1. **Omitted non-selected reference:** a 4-slot BOOT retains selected core cards but removes ScopeSentry or promptfoo from full Source Inventory. Expected **FAIL_SOURCE_COVERAGE** even if the first selected Scope still works.
2. **Dropped prohibition:** source prohibits unauthorized secret read; transformed SPEC/Prompt omits denial but keeps legal happy-path task. Expected **FAIL_SEMANTIC_PARITY** despite shape-valid JSON.
3. **Wrong level of proof:** Source L1 read-only replay reported as successful L3 live exploit. Expected **FAIL_EVIDENCE_CLAIM**.
4. **Wrong origin:** `based_on:source-coverage` is treated as an accepted typed `Card ID` rather than a document citation. Expected **FAIL_LINK_TARGET** until original Registry resolves a legitimate card target.
5. **Unapproved expansion:** Phase-1 read-only Cloudflare page turns into POST-based remote attack dispatcher or merges Blue PR. Expected **FAIL_AUTHORITY**.
6. **Stale host selection:** older Linux Docker-first candidate overrides the later MacBook OpenShell MicroVM-first decision. Expected **FAIL_DECISION_PRECEDENCE**.
7. **Unknown writes:** effect readback missing; transformation infers re-run safe, or frozen Noodle Stage can be retroactively edited. Expected **FAIL_OWNER_CONTINUATION**.

## Evidence and closure

- **Observed in documentation:** these mentioned sources are catalogued with selected/deferred/rejected/unknown distinctions. No further source-specific runtime behavior is claimed.
- **Not performed:** original conversation exact-byte ingestion; FactoryWeaver official v1 prepare/validate/Registry source binding; independent semantic reviewer; Soodles knowledge inspect; native agent/Host tests; production/cloud security work.
- **One-atom handoff:** [existing handoff](handoff.md) is the only proposed source-bound specification continuation. Unselected source references remain in this inventory; they do not create new runtime Issue Atoms.
