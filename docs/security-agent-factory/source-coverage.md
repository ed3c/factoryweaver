# Complete Requirement & Source Coverage Ledger

**Scope:** Security Agent Factory decisions SEC-01..16 and the later MacBook-first SEC-10R refinement. This ledger enumerates **confirmed decision-derived requirements only**; [source-inventory.md](source-inventory.md) separately preserves earlier named security tools, defenses, alternatives and hypotheses that were not selected as Phase-1 requirements. Do not call the 33-row decision ledger whole-conversation source completeness. Sources are of two distinct types: **HUMAN_DECISION** (explicitly supplied in the supervising conversation) and **OFFICIAL_DOC / REPO_SOURCE** (read for capability/contract facts). This file preserves semantic excerpts and all decisions; it is *not* a cryptographically bound original conversation transcript.

## Decision-to-requirement trace

| ID | Requirement / expected behavior | Source anchors | Canonical owner | Acceptance / observable discriminator | Negative case |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | 保留全部人類 SEC-01～16 與 SEC-10R 後續修訂，維持 Parent Goal | SEC-01/SEC-10R/SEC-13R/SEC-14/SEC-15/SEC-16 | Supervising Session | Full ledger retained; older overridden rule labelled | 同時宣稱 Docker-first 與 MicroVM-first 為優先 |
| REQ-002 | Red/Blue/White 三方分權，White Oracle 與 Agent 裁判分離 | SEC-02 | Security policy owner | Red/Blue cannot modify oracle data or credentials | Red can replace ground truth and still obtain PASS |
| REQ-003 | 只在擁有或明確授權的隔離 Lab 操作，Staging 額外授權 | SEC-03 | Asset/Admission owner | Unallowlisted target/refused; staging request not auto-admitted | Unknown public host reached by same run |
| REQ-004 | Red 可在隔離 Lab 測試、Blue 可提修復 PR；Merge/Deploy 原 Owner 才能做 | SEC-04 | Soodles/Provider | No automatic merge/deploy effect from card or agent verdict | Blue self-merges after its own test |
| REQ-005 | 第一階段優先 Agent Prompt Injection/Tool Misuse/Privilege Boundary | SEC-05 | Security scope owner | Negative prompt injection and authorized completion separate | Only runs conventional port scan and claims goal |
| REQ-006 | L1 採 REA captured read-only replay，保存來源與 exact-match | SEC-06/REA | REA producer | Known retrieval can replay; no write or live exploit claim | Nearest replay response used as exploit evidence |
| REQ-007 | L2 採 AgentEnv Stateful，包含 RBAC、mutation、reset、clock | SEC-06/SEC-07 | AgentEnv environment owner | Observed state transition and reset match fixed oracle | Role header alone treated as real host authority |
| REQ-008 | L3 Strix/garak 真實隔離測試延後，另需授權 | SEC-06 | Staging/L3 owner | L1/L2 green cannot change L3 status NOT_RUN | Synthetic proof marked real vulnerability |
| REQ-009 | 紅隊有限合成狀態變更且每次任務能完整重設 | SEC-07 | Lab environment owner | Mutation limited to resettable synthetic objects | Unrecoverable external effect in lab |
| REQ-010 | 參考環境使用 Gitea+Vault-compatible API+Target Agent | SEC-08 | Environment owner | Three component identities and data boundaries traceable | Target agent shares oracle admin identity |
| REQ-011 | 歷史 VaultEnv-REA 與 Live OpenBao 分別處理，API 相容須實測 | SEC-08/licensing | Replay/Live provider owner | No replay-to-live equivalence without contract checks | Vault BUSL treated as OSI-open source |
| REQ-012 | OpenShell 為唯一指定 Agent Sandbox Policy Boundary | SEC-09 | OpenShell Policy owner | Supervisor/runtime refusal and allow controls read back | Agent-env RBAC substituted for OS isolation |
| REQ-013 | MacBook Apple Silicon 優先；OpenShell VM/libkrun 第一驗證候選 | SEC-10R | Host runtime owner | Actual Apple Hypervisor VM execution plus policy tests required | Experimental driver named production qualified |
| REQ-014 | Podman Machine 保留備援且必須通過相同測試 | SEC-10R | Host runtime owner | Same workload and controls distinguish candidate runtimes | Docker-compatible socket assumed equivalent |
| REQ-015 | 隔離校驗優先於速度、資源與成本優化 | SEC-09/SEC-10R | Independent Security Test owner | Unsafe runtime rejected regardless of latency | Faster forbidden egress accepted |
| REQ-016 | 同一 Run 權限固定，Policy 擴張要新 Admission | SEC-11 | Admission/Policy owner | Prior run cannot use a broader policy without authority | Agent hot reload grants itself privileges |
| REQ-017 | 新獨立 Security Lab Repo 擁有 Runtime，不接管 FactoryWeaver Registry | SEC-12/14 | Repository owner | Single canonical cards, chosen source-bound consumption | Duplicate conflicting card registries |
| REQ-018 | Cloudflare 控制面只提供 read-only sanitized dashboard/results API | SEC-13R/SEC-16 | Cloudflare app owner | No public write/dispatch route to OpenShell Gateway | Cloudflare results endpoint starts scan |
| REQ-019 | Cloudflare 不能作為尚未驗證的 OpenShell Container Host | SEC-13R | Deployment owner | Unsupported cloud runtime remains not qualified | Cloudflare nested Docker marked fully supported |
| REQ-020 | 核心元件/模型/映像/資料全部依使用情境核對開源商用授權 | SEC-10/13R/license | Licensing owner | License inventory per artifact; unresolved exclusions blocked | One repo Apache license inferred for every dependency |
| REQ-021 | 同一 Supervising Session 路由 Thinking V2／條件式 V3 × Ambitious | Session request | Session owner | V3 only with new falsifiable engineering distinction | Every inner test triggers V3 |
| REQ-022 | 以 Goal/Measurement/Effort Horizon 選第一因果斷點，已知事項不重問 | Session request | Session owner | Original owner next takes precedence; unknown explicitly named | Repeats already decided SEC question |
| REQ-023 | Noodle Poteto 在原授權 worktree/Stage 運作並回送真實 evidence | Session request | Noodle Host/Stage owner | Actual native Stage consumed admitted delta and produced readback | Card text described as native agent invocation |
| REQ-024 | FactoryWeaver v7.2 保存完整 REQ/卡片/Typed Links/Source Fidelity | SEC-14 + FactoryWeaver | FactoryWeaver producer | Full inventory not lost by Boot four visual slots | Unselected parent requirements discarded |
| REQ-025 | 卡片改動僅沿 source-backed Delta；Frozen inputs 不逆向修改 | Session/FactoryWeaver | Original Registry + Stage owner | Material change updates only affected cards and next unfrozen consumer | Old stage rewritten to claim it read new delta |
| REQ-026 | FactoryWeaver Soodles 交接僅是 SOURCE_BOUND_PROPOSAL、無效果權 | SEC-14/SEC-15 | Original exporter/reader | Exact bytes bound; next=null; effects=[] | Reader output treated as issue admission |
| REQ-027 | 本階段只作規格/驗證/唯讀 Handoff，不執行 Runtime 或 Merge | SEC-15 | User / Original Provider | No running security agent, PR merge, staging effects | Creating doc causes unauthorized scan |
| REQ-028 | 白隊 Oracle 使用獨立 Positive/Negative/Unknown/Replay Controls | SEC-02/Measurement | Independent Oracle owner | Authorized work succeeds and denied work remains denied | Blocked-all policy earns pass |
| REQ-029 | 結果分清 L1 recorded、L2 synthetic、L3 live claim levels | SEC-06 + evidence | White Oracle owner | Report includes environment/build/policy/trace provenance | L1 PASS reported live exploit |
| REQ-030 | 指標包括 verified success、unauthorized actions、cost/remediation、false positives | Goal/Measurement | Metric producer/Test Manager | Baseline measured from equivalent tested tasks; no invented targets | Unmeasured % improvement reported |
| REQ-031 | Unknown effect 先 Owner readback，不重新投遞；Known error 回 Poteto | Session contract | Soodles owner | Readback before retry; semantic ambiguity only then Thinking | Uncertain write executed twice |
| REQ-032 | Self-play/RL 和多 App Platform 是未來能力，不在本期調度 | SEC-01 | Product owner | Deferred REQs preserved without implementation claims | Future platform capability passed |
| REQ-033 | Runtime 完整驗收前保留 OpenShell policy, VM bind mounts, host socket threats 為 K | SEC-09/SEC-10R | Host+Independent Oracle | Missing capability probe blocks qualification, not source-only work | Host bind mount ignored in security verdict |

## Source role and capture boundary

- **SRC-HUMAN-SEC:** explicit user-confirmed SEC-01..16 responses and the revised MacBook-first OpenShell directive from this conversation. Authority: PRODUCT SCOPE, not measured security evidence. Exact conversation bytes are not mounted to the original FactoryWeaver Host; `integrity=UNPINNED` until a Host-owned source snapshot is prepared.
- **SRC-SOODLES-ROUTER:** [thinking-router/SKILL.md](https://github.com/ed3c/soodles/blob/main/.agents/skills/thinking-router/SKILL.md), **SRC-SOODLES-LOOP:** [loop-execution.md](https://github.com/ed3c/soodles/blob/main/.agents/skills/thinking-router/references/loop-execution.md). Authority: conditional routing / original owner responsibilities, not proof of native usage.
- **SRC-FW-COMPILER:** [v7.2 compiler](../../references/zettelkasten-v7.2.md), **SRC-FW-CLASS:** [classification](../../references/card-classification-and-scope-assembly.md), **SRC-FW-HANDOFF:** [readback contract](../../docs/factoryweaver-soodles-readback.md). Authority: knowledge-record / proposal format, not admission.
- **SRC-REA:** [ed3c fork](https://github.com/ed3c/rea-environments). Captured exchanges read-only, fixed evidence; dataset/individual app licenses differ.
- **SRC-OPEN-SHELL:** [official VM driver source](https://github.com/NVIDIA/OpenShell/blob/main/crates/openshell-driver-vm/README.md) and [runtime support documentation](https://docs.nvidia.com/openshell/latest/how-it-works/sandboxes/runtimes). VM driver explicitly Experimental; facts about docs are not runtime evidence.
- **SRC-CLOUD:** [Cloudflare Workers](https://developers.cloudflare.com/workers/). Platform is hosted; Workers first-phase proposal read-only.
- **SRC-OPENBAO:** [OpenBao](https://openbao.org/) (MPL-2.0 candidate). Contract compatibility against historical Vault Replay is not tested.

## Provenance / status invariants

Each row records a **normative requirement**, not a verified implementation. Design maturity: `knowledge=SPECIFIED_PROPOSAL`; native `engineering=UNASSESSED`, `delivery=NOT_STARTED` for all 33 requirements. A source document citation is not a security PASS. Unknown user source bytes, provider behavior, speed/cost baselines and MacBook policy proofs remain UNVERIFIED. Retain all numbered requirements across Boot four-slot display and all later Drill batches.

## Genuinely unresolved K obligations (not new product choices)

1. Exact-byte Host capture of conversation decision sources and canonical v1 record preparation / source digests.
2. Named MacBook machine/OS, available OpenShell release, VM Entitlement, CPU/memory constraints, and actual VM/Podman capability/performance baselines.
3. Exact real L2 simulator role, state, reset and independent evidence interfaces; Vault historical recording vs OpenBao compatibility.
4. Per-component open-source/commercial license matrix including transitive OCI artifacts and dataset redistribution terms.
5. First real original Soodles Issue/Task admission and fresh native Consumer/White Oracle/Cloudflare results; all NOT_RUN.

No missing runtime input blocks writing source-faithful specification cards. It blocks only the claims/operations depending on it.
