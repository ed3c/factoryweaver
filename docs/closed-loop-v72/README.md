# v7.2 閉環規格交接

這份規格讓下一個原 Noodle Poteto execute writer 能按完整需求接續工作。它包含 30 個 REQ、30 個 SPEC、68 張卡、14 個来源片語分組，以及七類事件和五個 task-unit 提案。原要求對照與 runtime 驗收仍由原 owner 負責。

先讀 [卡片盒](cards.md) 與 [交接程序](handoff.md)。[閉環附錄](profile.md) 說明 Soodles 外迴圈、Noodle Poteto 內迴圈、Thinking Router、Ponytail 和四個 Manager 的職責。[eval 審計](eval-audit.md) 記錄調整理由、五案有限觀察與證據限制。

機讀資料使用 [project.json](project.json)、[specifications.json](specifications.json)、[loop-profile.json](loop-profile.json) 和 [coverage.json](coverage.json)。project 保持原 v7.2 exchange 形狀。loop-profile 使用独立的提案 schema，不把新欄位塞入舊契約。卡片原句來自 [來源分解](source-clauses.md)，完整原文由 supervising Session 保留於私有 evidence。

閉環要求由事件推進必要 Manager，原 owner 消費 next，取得實際效果讀回，再更新同一需求。局部綠、資料合法或指引 consumer_report PASS 都不能直接宣布整份 runtime 完成。

本次交付是規格及有限 eval。全部 runtime REQ 保持 engineering=UNASSESSED、delivery=NOT_STARTED；adapter 為 UNBOUND、task unit 為 NOT_RUN。文件 PR 的 merge 只驗收筆記交付，不啟用 native Hook／Cron 或啟動 Noodle。

PR #15 的規格交付時尚未包含 reference compiler CLI。現在的純讀取 CLI 可驗證與投影這份規格，不能據此宣稱原 Noodle、四個 Manager 或 native Hook／Cron 已完成 runtime 驗收。
