# v7.2 與內外迴圈的 eval 審計

審計日期為 2026-10-11。方法使用 eval-audit，並依 review-writing 核對保存文字、條件與來源。結論是保留 v7.2 核心，加入 [閉環 sidecar profile](profile.md)。這是來源支持的設計建議。有限 consumer 觀察支持指定判斷，沒有證明附錄比 baseline 提高成功率，也沒有證明原生自動閉環已完成。

已讀來源包括本 repository 的 v7.2 portable reference、knowledge-record schema、既有 reference compiler，及經授權可讀的 Host main／候選架構資料。三個相似路徑為 source-bound intent handoff、whole-task review、Manager feedback 回到原需求。私有實作、source tree、原始 session 與 test traces 留在私有任務 evidence；此處只記設計結論和限制。

Host main 已有部分 Schema／Test／Hook／Cron 入口與 feedback 資料路徑。Thinking Router／Ponytail 的指定整合來源仍是候選，不能混稱 main 已安裝或已啟用。因此使用者的「沒有功能」不足以支持重建全部 Managers。已支持的需求是讓整条事件、判定、原 owner 接續及驗收讀回可追蹤並實際接線。

## 優先問題

### 1. 資料契約無法單獨表示整條閉環

Status 為問題存在，限於已讀 portable exchange schema。

REQ／SPEC 的來源、依賴與三軸狀態已有設計，但原 exchange 沒有明確的 LoopEvent、Manager 結果到原 REQ 的映射、OwnerConsumption 及整份 ClosureClaim。卡片 payload 可以描述它們，不能證明 consumer 有保存或採用它們。ActionRequest 仍只是提案。

Fix 是加入相容 sidecar，沿原事件與效果 owner 接線。以精確版本、producer、事件去重和 owner readback 驗收。原 v7.2 不需要變成四 Manager 的 executor。

### 2. 局部證據容易被誤當整份完成

Status 為存在設計風險；本次沒有 production defect rate。

原文已區分 compile DONE、knowledge、engineering、delivery，但若 handoff 沒保留完整需求分母及停止條件，consumer 仍可能停在局部測試或報告。風險不能冒稱已觀察的真實 Noodle 故障。

Fix 是保留原句 inventory、全部 REQ IDs、剩餘可做項目和逐項 closure obligations。外迴圈接受實際結果，小迴圈只切工作，不縮小完成範圍。

### 3. 架構與安裝狀態未對齊

Status 為本次 runtime 整合未知。

候選 Thinking Router／Ponytail 資料、main 的 Manager 入口、原生 carrier 和此 public compiler 是不同驗收對象。來源相似不證明已在同一 task 接線。

Fix 是由原 owner 固定 selected refs、實際 schema、execution envelope、carrier 與 input binding。能建立的工程輸入由本 Session 完成；不可取得的身分或效果只阻塞相依分支。

## 六個診斷區域

| 區域 | 查得的狀態 | 必要下一步 |
| --- | --- | --- |
| Error analysis | 沒有本次 compiler 到真實 inner／outer runtime 的代表性 traces。五個指定反例不是 taxonomy 飽和取樣。 | 實際接線後，先檢查正常 logs 與 readback。若仍有未知 Agent 行為，依 error-discovery 分析該批 traces。 |
| Evaluator design | 格式、IDs、digest、scope 和欄位真假可做確定性檢查。原 preview 拒絕自述 runtime 完成。 | 保留原信任邊界。語義漏項另審，不用 schema PASS 或 style 分數替代。 |
| Judge validation | 本次沒有語義 LLM judge，也沒有人的 Pass／Fail labels 可計算 TPR／TNR。 | 不報 judge 已校準。真的需要語義 judge 時，再用 write-judge-prompt 及 validate-evaluator。 |
| Human review | 本次條件由 supervising Agent 對原要求自審；consumer 是無聊天繼承的獨立 native subagent。 | 不稱人標或獨立條件審查。保留原 output 與可用 capture，人工審查可後續補充。 |
| Labeled data | 五案、12 個指定輸出欄位；未經人類代表性確認。 | 只支持這些反例。沒有 production rate、統計泛化或 100-trace 飽和證明。 |
| Pipeline hygiene | 保存指引、輸入、protocol、report、capture 與 Schema response 的摘要綁定。真實 adapter／native execution 未接入。 | 來源或指引改變後只失效依賴證據。禁止舊 PASS 蓋過目前 FAIL，亦不可把新檔名當新任務身分。 |

目前缺的是整條自動接續與效果證據。建立更多泛用 judge 或 dashboard 不能代替此接線。這次未建立新 scheduler、runtime gate 或持續 eval pipeline。

## 實際有限觀察

本次 fresh consumer 只讀保存的 profile.md、handoff.md 與五個指定案例。它沒有繼承本對話，沒有看到 supervisor 的 expected。它輸出實際報告和輸入、判斷、理由的 capture。capture 不含完整模型或工具 transcript。此限制保留，不能冒稱原生 Noodle session。

| 案例 | 已觀察判斷 | 範圍 |
| --- | --- | --- |
| partial-green | R2 可做，不能標 blocked，整體未完成 | 防止局部 PASS 提前停止 |
| unknown-write | 不重播原寫入，獨立 R2 可繼續；capture 說明先 owner readback | 未知效果及局部阻塞 |
| changed-bytes | 舊 SPEC PASS 不能作目前驗收；native activation 未證明 | 身分失效及證據分級 |
| manager-result | 閉環未完成，不需新方法或第二 scheduler | 尚未消費的 next |
| budget | 喚醒不重設次數，不做第四次不變重試；capture 說明重審前提或縮小問題 | 原修正失敗 budget |

第一個 supervisor protocol 錯把「重審根因」固定成單一英文 action label，產生一個欄位 FAIL。原要求只規定行為，沒有規定英文拼字。這是判準缺陷，不能當 candidate 行為故障。

已保留原 protocol、FAIL response 和 consumer 輸出。修正後移除兩個沒有原文固定拼字的 action-label 判準，保留原始回答與 capture，沒有把 consumer 答案抄成 expected。對原要求支持的 12 個欄位，用 schema-2 條件審查再提交相同實際 observations。

Schema Manager 讀回 evidence_validity=VALID、criteria=SUPPORTED、behavior=PASS，五案共 12 個欄位通過。task owner 已消費 consume_verified_behavior，保存 response digest、返回 next、實際採用動作及上述限制。條件仍是 Agent 自審，不是外部真值。

此 PASS 的 observation_scope 是 consumer_report。它不證明 wording 因果改善、完整 transcript、真實 Noodle execute、四 Manager 自動執行、原生 Hook／Cron、PR runtime acceptance 或全部未知錯誤的修復。效果權限仍為 false。

## 保留、增加與待驗

保留 evidence-first、stable IDs、typed links、lossless batching、source dependency、unknown scheduling、三軸狀態、原 owner 效果邊界及確定性失效。新增 event／result／consumption／closure 的資料提案，以及小迴圈與整份要求的對照。

Thinking Router 保留原意與方法來源。Noodle Poteto 保留原 execute 工程入口。Ponytail 在外迴圈審查最小完整解。兩者都不能替代 Schema 證據、Test scope、native activation 或原 owner delivery。

真實閉環 traces、原生載入與喚醒、原效果 consumption/readback、代表性人標，以及完整 v7.1 來源仍待驗。按照 [handoff](handoff.md) 沿原 owner 完成具名工程與觀察。文件 PR 合併只能完成本次規格交付。
