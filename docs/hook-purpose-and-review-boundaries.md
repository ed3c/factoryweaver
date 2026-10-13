# Hook 用途與 PR／MR check 邊界

FactoryWeaver 與 NeoWeaver 使用原 Soodles Hook Manager，沒有各自新增的 Manager。兩個 repository 的差別是 Goal 與受審資料。原 task owner 先判斷用途，再選既有 Consumer。Card 類型、PR 標題或 `INSPECTED` 都不能證明已發生原生事件。

| 用途與時機 | Producer → Consumer | 必要資料 | 不要求的資料 | 驗收上限 |
| --- | --- | --- | --- | --- |
| 普通 task-review；需求或 observation 改變後 | Task owner → `schema task-review` → 原工程 next | 固定 requirements／observations／FileRefs | Native Session、Stage、generation tokens | 申報覆蓋與 next，沒有 native 事件 |
| 原生 Stop task-review；專用任務首次符合的 Stop | Codex Host → Hook Manager Stop → task-review → 同任務 consumer | Trusted definition、actual event、Session／cwd binding、固定 requirements／selection、`stop_hook_active` | 不相關 token lineage／training rights | 原生呼叫與一次 continuation；另觀察 exact next 消費 |
| PR／MR source check；具體 candidate 與 material diff 已可讀 | Provider／source owner → `outer-review` → Waza `check` → findings validation | Repository、精確 base／head、原 task／acceptance、diff／source、必要 CI／review evidence | 歷史 Noodle custody、Stage IDs、Stop／Session、training／transfer receipts | 所選來源與風險審查，沒有 effect authority |
| Native Hook behavior check；定義或接線改變後 | Config／Host owner → Hook inspect／event → 原觀察者 | Definition／handler bytes、trust、load、event、invocation、必要 consumption／effect readback | 其他任務的 runtime metadata | 所選 native 行為；Installed 不等於 Invoked |
| Merge／delivery check；來源審查及必要 checks 完成後 | Task／provider owner → 現有 landing route → provider readback | 當前授權、最新 head、必要 CI／review、expected-head 保護與 merge readback | 未選 Noodle carrier 的歷史 reconciliation、未實作 training／transfer metadata | Repository 交付，沒有父 Goal closure |

修改 native Hook 的候選可以先做來源 check。要宣稱接線已啟動，仍需該用途的 native evidence。缺少這些證據只限制相應 claim，不把来源審查卡在無關的 Stage／token 欄位。Provider head 與 source digest 是來源用途的必要身分，不能當「非必要 runtime metadata」刪除。

## Repository applicability

FactoryWeaver 的 `card_semantic.py managers` 只交付 semantic needs。Compiler 可以提出 control 或 Hook 問題，不能選 actual tests、註冊定義或將投影當 invocation。其 PR check 審視 source fidelity、Card／Scope Consumer 邊界與 portable CLI。Full native maintenance 是另一個 proof scope，不是來源 PR 的通用前置條件。

NeoWeaver 首 atom 的 PR check 審視 raw parser／refusal、fixed references、protected／stale targets、正反測試和十項原需求保存。Parser 不啟動 Hook。工程任務的 Stop task-review 不等於 learned patch transfer。未來候選真的修改 native Hook 時，才核對該 surface 的原 capability、授權、trust 與 consumption。

## 觸發與交接

Codex Stop 使用 Host 寫入 stdin 的 actual event JSON。PR／MR check 使用 provider candidate/event readback 與 source-bound review selection。GitHub `pull_request` 或其他 provider `merge_request` 不等於 Codex native event。沒有已註冊且授權的 adapter 時，保留 trigger bridge 未觀察；當前授權 Session 仍可執行來源 check。

原 `schema outer-review` 接受 task／diff FileRefs、repository／head、source-backed signals 與 reports，不要求 native runtime custody。它不會啟動 reviewer。`pending_capture` 是缺 reviewer capture，`reported_unverified` 是 supplied evidence 已綁定，兩者都不是 findings ACCEPT。原 Session 檢查真正的 reviewer 輸出與 source／caller／acceptance。若聲稱事件自動啟動 check，另保留 event → adapter invocation → exact candidate request → reviewer capture → findings consumption 的觀察。

Host／provider 產生及讀回必要 identities、digests 與 argv。Consumer 不從文字重建它們。Head 改變後重新讀取受影響 evidence；相同 source-bound 合法 next 保留，不因 unchanged event 重播未知 write。

## 逐步推論斷點

| 交接步驟 | 不成立的推論 | 正反驗收與修正 Owner |
| --- | --- | --- |
| Goal → purpose | PR 要 check，所以一定需要 native Hook | PR request 的 `hook_need=null` 正常投影；Task owner 分開來源與 native 用途 |
| Purpose → need | `native_event` 非空且 `INSPECTED`，所以事件已發生／適用 | 任意宣告仍只回 `native_execution=UNKNOWN`；Compiler／Session 核對原用途與 event，形狀不當語義驗收 |
| Candidate → request | 沒有 Stage／Session／tokens 就不能 check | Metadata-free 原 `outer-review` 接受固定 task／diff／head；缺原 source quote 會拒絕 |
| Request → invocation | 選到 `check` 就代表 reviewer 已啟動 | `pending_capture` 不當 PASS；Host／Session 保存 actual reviewer capture |
| Evidence → verdict | 有 report／CI／後續 tool 就支持所有 acceptance | Session 逐 finding 驗 source／caller／acceptance；next 消費與 exact request 關聯，CI 只覆蓋實際 controls |
| Verdict → delivery／Goal | Scoped ACCEPT 等於 merge／transfer／父 Goal 完成 | Provider 回讀 exact-head merge；未覆蓋需求與 native／whole Goal receipts 保留 |

這是用途與來源審查契約，沒有新增 event adapter、CLI 狀態機或效果權限。既有 `manager-needs` drive 只驗 metadata-free advisory、extra fields refusal 與 UNKNOWN ceiling；`native-hook` 保留原 native prerequisites。Agent guidance compliance 另走原 P-class feedback。

來源是原 Soodles `outer-review/references/selection.md`、`hook_manager.py` 與 `cron-job-manager/references/native-stop.md`。已讀 checkout `c2f1c3afa81fef06fc439ccee67df32104ad5218` 的這些 selected sources 與 fetched main `1fbae801fda7590a6e6fe728a8a2fc0e5f63e409` 無差異。Codex 原生事件與 trust 依 [官方 Hooks 文件](https://learn.chatgpt.com/docs/hooks)。
