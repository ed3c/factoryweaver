# v7.2 閉環規格交接

這份規格讓下一個原 Noodle Poteto execute writer 能按完整需求接續工作。它包含 30 個 REQ、30 個 SPEC、68 張卡、14 個来源片語分組，以及七類事件和五個 task-unit 提案。原要求對照與 runtime 驗收仍由原 owner 負責。

先讀 [卡片盒](cards.md) 與 [交接程序](handoff.md)。[閉環附錄](profile.md) 說明 Soodles 外迴圈、Noodle Poteto 內迴圈、Thinking Router、Ponytail 和四個 Manager 的職責。[eval 審計](eval-audit.md) 記錄調整理由、五案有限觀察與證據限制。

機讀資料使用 [project.json](project.json)、[specifications.json](specifications.json)、[loop-profile.json](loop-profile.json) 和 [coverage.json](coverage.json)。project 保持原 v7.2 exchange 形狀。loop-profile 使用独立的提案 schema，不把新欄位塞入舊契約。卡片原句來自 [來源分解](source-clauses.md)，完整原文由 supervising Session 保留於私有 evidence。

閉環要求由事件推進必要 Manager，原 owner 消費 next，取得實際效果讀回，再更新同一需求。局部綠、資料合法或指引 consumer_report PASS 都不能直接宣布整份 runtime 完成。

本次交付是規格及有限 eval。全部 runtime REQ 保持 engineering=UNASSESSED、delivery=NOT_STARTED；adapter 為 UNBOUND、task unit 為 NOT_RUN。文件 PR 的 merge 只驗收筆記交付，不啟用 native Hook／Cron 或啟動 Noodle。

PR #15 的規格交付時尚未包含 reference compiler CLI。現在的純讀取 CLI 可驗證與投影這份規格，不能據此宣稱原 Noodle、四個 Manager 或 native Hook／Cron 已完成 runtime 驗收。

## Current FCL supplement — Intent-to-Acceptance Closure (2026-10-23)

This newer specification increment preserves the **historical** original 30 REQ / 68 stable Card IDs and all original NOT_RUN states. It adds CL-15…CL-19 to [source clauses](source-clauses.md) / [coverage](coverage.json), updates exactly four preexisting Card revisions (SPEC-outer-loop, SPEC-inner-loop, SPEC-stable-update, V-runtime-gap), and aligns their [structured SPECs](specifications.json). The [source-bound ScopeManifest / SkillRoute / PromptDelta / Continuation](intent-to-acceptance-scope.json) is proposal-only.

[Complete Harness² × NeoWeaver × pstack INT/HOF and A01–A20 coverage](intent-to-acceptance-coverage.md) stays linked to its **original cross-repo Owners**, not duplicated as another FactoryWeaver registry. [Positive/negative verification contract](intent-to-acceptance-verification.md) declares real native tests that are still NOT_RUN until the original Noodle/Soodles/Provider executors return observations.

**Scope:** accepted FCL-01 A / FCL-02 A / FCL-03 A — card/coverage/specification documents and PR only. No Harness² runtime, Noodle admission, card-to-native auto-dispatch, formal proof, paid API key, provider landing or main merge authorized by this supplement.

## MGP System Prompt semantic-parity amendment (FCL source-compatible)

Follow-up to FCL-01 A / FCL-02 A / FCL-03 A and MGP-01 A / MGP-02 B / MGP-03 B: the [portable v7.2 System Prompt](../../references/zettelkasten-v7.2.md) now selects **conditional** source-to-Consumer Semantic Parity / reuse-before-rewrite when an actually material transformation exists. [Existing r3 Cards](project.json), [CL-20/CL-21](coverage.json) and [MGP review/Evals protocol](../evals/v72-migrate-semantic-parity.md) preserve all 30 REQ / 68 stable Card IDs and historical failed/unknown results. The original [migrate-class](https://github.com/ed3c/soodles/blob/c45d566e69bb074da33b63a89060022c893ff7de/.agents/skills/migrate-class/SKILL.md) is an unmerged method reference, not an automatically installed Skill. A source-only PR/CI PASS cannot certify live FactoryWeaver Agent behavior or native Soodles/Noodle effects.
