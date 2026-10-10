# v7.2 閉環附錄提案

v7.2 的原文保存在 [reference](../../references/zettelkasten-v7.2.md)。本附錄補交接契約，不替換其信任邊界，也不宣稱為官方 v7.3。完整 v7.1 未提供，其全部繼承條款仍有來源缺口。

規格驅動開發固定「應該發生什麼」。Schema data 驅動開發讓既有 owner 根據版本綁定資料決定「現在可以做什麼」。两者必須使用同一 REQ／SPEC、依賴與驗收對象。只更新文字或只驗 JSON 都不能完成資料闭環。

本 profile 的選擇理由是保留既有 compiler 及效果 owner。只補 prose 無法明確表示事件與消費資料。把四個 Manager 塞進 compiler 會新增排程責任和權限。本提案因此使用 sidecar 資料，由原 Host adapter 接入既有事件與 lifecycle 路徑。

## Compiler 的新增輸出

Compiler 仍產生 CARD_PATCH、PROJECT_STATUS、ACTION_REQUESTS、NEXT_STATE。它另產生以下 sidecar 提案。Host 尚未接入時，輸出保持 PROPOSED。

| 輸出 | 必須保存的資料 | 已交付位置 |
| --- | --- | --- |
| Whole-task inventory | 原句分組、全部 REQ IDs、未映射項、分批 cursor | coverage.json |
| Executable specification | actor、Given/When/Then、型別、四類案例、non-case、oracle、回滾 | specifications.json |
| Event plan | 事件來源、schema 版本、身分、依賴、consumer、去重及失效規則 | loop-profile.json |
| Task-unit proposal | 本單位覆蓋 REQ、輸入、預期結果、依賴、原 owner、驗收邊界 | loop-profile.json |
| Closure obligations | 必要 Manager 結果、原 owner consumption、效果與交付 readback | loop-profile.json |

這些輸出描述要求。它們不是 execution envelope、admission、原生 Hook 設定或 Cron 排程。以 [profile schema](../../contracts/v1/closed-loop-profile.schema.json) 驗證只能支持其資料形狀。

## 擬議事件流

原事件 owner 在已登錄 adapter 和授權內驗證輸入，選定相應 consumer。未知 adapter 回具名工程缺口。不得從下表的 operation 名稱拼 shell command。

| 事件 | 必要消費者 | 何時觸發 | 回到哪裡 |
| --- | --- | --- | --- |
| intent.changed | Thinking Router、需求 compiler、Schema Manager | 原意或必要約束實質改變 | 同一任務 prompt delta 與完整 REQ inventory |
| requirement.changed | Schema Manager、Test Manager | 規格、驗收或依賴改變 | 失效範圍、focused scope 與原 owner next |
| source.changed | Schema Manager、必要證據 producer | Source pin、head、plan 或環境失效 | 真正相依的 REQ／SPEC；不相依成果保留 |
| manager.result | Schema Manager、原 task owner | Test／Hook／Cron 回傳實際結果 | 同一 REQ 的觀察、next 與 consumption obligation |
| hook.definition.changed | Hook Manager、原設定 owner | 精確定義、carrier 或 event binding 改變 | 原生 trust／load／invoke／delivery／效果讀回 |
| wait.changed | Cron Manager、原 scheduler owner | 必要等待、deadline、取消或授權改變 | 原排程設定讀回；喚醒原 owner 後再查前提 |
| owner.readback | Schema Manager、外迴圈 owner | 原效果或交付取得讀回 | 同一版本的 REQ 狀態與剩餘要求 |

自動接續的目標是不用新使用者提示即可走完已有合法路徑。Schema readiness 仍不授予效果。Test scope 仍由 Test Manager 決定。Hook 與 Cron 仍由原 carrier／scheduler 執行。缺能力時，原 Session 可完成具名接線工程；不能把「沒有 argv」當作停止所有工程的理由。

事件 owner 保存原 task、producer、event ID、payload digest、sequence、requirements／SPEC／head／plan／environment 身分。精確 duplicate 返回原 receipt。同 ID 不同 payload 或 producer 拒絕。亂序不得覆蓋較新狀態。投遞結果未知時先原 owner readback。此契約不建立第二份可授權 event store。

## 內外迴圈

Thinking Router 先核對有效 continuation。只有真正未決的意圖、前提或職責問題才選方法。方法可為 none。原意、來源、約束、建議和未決選擇必須分開。候選方法不能自稱已執行。

Soodles 外迴圈固定整份需求、驗收、原 owner 和 stopping point。它可在具名候選需要審查時使用 Ponytail，檢查最小完整解。Ponytail findings 回原 owner；它不建立另一個 inner loop，也不簽署驗收或 merge 權限。

Noodle 保留 Worktree、Session、Process 與 event writer。原 execute session 以 Poteto Mode 選適用 playbook，逐 task unit 解決已知需求。工程 writer 在同一授權邊界完成修正、必要驗證、自審及回填。小步不縮小整份需求。

每次小迴圈結果回到必要 Manager，再回原 owner。原 owner 保存 returned_next、實際動作及讀回。外迴圈核對剩餘全部 REQ。新事實直接更新當前卡片 revision，保留旧版和修正理由。新增未知使用 K；實質來源矛盾使用 X。不得改原始 receipt 或刪原要求来讓驗收通過。

## 完成與未知

知識编譯 DONE、單元測試 PASS、consumer_report PASS、native activation、provider delivery 是不同結果。原 owner 逐項核對相符的來源、規格、實際執行、必要 Manager 結果、consumption、效果與交付讀回，才能完成該 REQ。只有全部原要求具相符證據且無未映射項，才能宣告整體完成。

有任何授權內可做工作就繼續。未知只阻塞其依賴。尚未生成且可由本 Session 產生的輸入是工程工作。只有查證過 producer 且目前無法取得的必要輸入，才是阻塞依據。未知寫入始終先讀回，不重播效果。

三次修正失敗後停止不變重試。保存嘗試、錯誤與原因，再重審前提或縮小問題。缺證據和重複讀回不算修正失敗。Cron 喚醒、新檔名或交接不重設歷史與预算。

## 最小實作順序與驗收

1. 原 compiler owner 核對 source clauses、REQ 分母與完整 SPEC。用 unchanged、漏原句、矛盾、未知四類輸入檢查保存結果。
2. Host owner 查明精確 adapter schema。實作 exchange 到原 owner input 的映射，拒絕無法表示或錯版資料。沒有 adapter 時保留 K，不輸出虛構命令。
3. 原 lifecycle owner 接 requirement／result 事件到 Schema 與 Test。以一個真正的同版本 task unit，讀回 request、selection、實際產物、next 及 consumption。
4. 選定 carrier 與 scheduler 後，補 Hook／Cron 必要接線。觀察原生載入、事件、喚醒、取消和效果。Fixture 只驗它自己的邊界。
5. 外迴圈接回全部 Manager 結果。用「局部綠但還有可做要求」及「unknown write」作反例。逐 REQ 取得驗收與交付讀回後才報整體完成。

上述步驟是待實作需求，不是本次已執行紀錄。本次範圍是筆記、資料契約、有限 eval 及文件 PR 交付。
