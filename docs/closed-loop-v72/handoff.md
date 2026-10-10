# 交給原 Noodle Poteto execute writer

先讀 [cards.md](cards.md)、[profile.md](profile.md) 與 [eval-audit.md](eval-audit.md)。使用 [project.json](project.json) 的 stable IDs，[specifications.json](specifications.json) 的完整案例和 [loop-profile.json](loop-profile.json) 的擬議事件契約。原使用者全文、private source pins 與 receipts 由 supervising Session 在既有 evidence 提供，不在 public repository。

本次交接包含 30 個 REQ、30 個 SPEC、68 張卡、14 個來源片語分組及六批輸出。coverage.json 只證明宣告連結。原 writer 必須對照原使用者要求，再確認有無遗漏。其需求分母不得縮成剛完成的小步或 Manager 類別。

這是工程需求交接，不是啟動 Noodle 的 execution envelope。取得原 supervisor 選定且有效的 envelope、Skill selection、target binding、admission、worktree／head、session 與 budget 後，在原 execute stage 使用 Poteto Mode。不可從別的歷史任務借身分。缺身份只停止相依效果；已授權的來源與契約工程仍可繼續。

## 小迴圈作業順序

1. 保留整份 REQ、原句、验收與依賴。先處理輸入齊備且已授權的單位。原 owner 已回傳有效 next 時，沿该路徑，不重選等價命令。
2. 找現有 producer、consumer 及兩至三個相似實作。使用既有 library、測試模式及原資料 schema。沒有真正未決推論時，Thinking Router 使用 none 或沿用原 continuation。
3. 為本單位固定 REQ IDs、SPEC revision、inputs、oracle、原 owner、head、測試 scope 和回滾。Test Manager 選必要 controls。整份 handoff 不因這個 scope 縮小。
4. 小步修改。任何新事实、错误推论或必要未知，直接更新卡片及同一 handoff。保存旧版、差異、支持來源、失效範圍和 K／X。原要求与原 receipt 不可偷偷改写。
5. 對所選邊界取得真正 observation。將原始產物及必要 Manager 結果回 Schema。讀 evidence validity 再讀 behavior。缺證據不能寫 PASS；條件錯誤先修條件；行為失敗查 capture，再修實際缺陷。
6. 原 owner 消費返回 next。保存 returned_next、actor、合法 inputs、實際 action、result 與 readback。operation 名稱不是可拼接的 shell 命令。next 無 argv 時完成具名工程缺口。
7. 重新核對全部原要求。尚有可做項目就接續。已查證且現在不可取得的 prerequisite 只阻塞相依工作。原 effect unknown 先 readback。第三次修正失敗後停止不變重試，重審根因且不重設预算。

Ponytail 是具名候選的可選外迴圈 review。檢查最小完整解與全部受影響呼叫者，不以短 diff 當充分驗收。它不替代 Poteto 的 execute playbook或原验收 owner。

## 必須保留的交接欄位

每個 REQ 保留原句與來源、actor、結果、驗收及反例、依賴、owner、SPEC、knowledge／engineering／delivery 三軸、目前 evidence 與未解輸入。每個未知保留 producer、已查來源、obtainable 與原因。每個已嘗試效果保留原身份、失敗歷史及 outcome，未知寫入不可重播。

Task unit 僅切工作。既有事件 log 和 owner receipt 保存實際 state；卡片不增加可授權 checkpoint。資料 consumer 採用新事實後才算該修正接線完成，不能每輪重做同一調查。

## 停止條件

全部原要求具相符驗收和必要 owner readback、且沒有未映射項，才可整體完成。局部 commit、測試綠、Schema next 已消費或一個 owner next=null 均不足。

若全部剩餘動作都缺少已查證且目前不可取得的必要輸入，保留逐項 producer、理由與 scope，報部分完成。尚未檢查 producer、仍可產生输入或仍有授權工程时，不可把 final 當下一輪入口。

文件合併只完成規格交付。本次沒有真實 Noodle execute、四 Manager 自動觸發、native Hook／Cron 或全任務 runtime 驗收；这些状态保持 NOT_RUN。
