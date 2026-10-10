# Card delta：有界、唯讀的增量知識編譯

Issue #17 沿用公開 `issue4/card-delta-v1` commit `efd02f9102e291824b43550e53cb4edf0fcd9f8a` 的 compiler、tests 與本契約，再修正 cursor、history 和失效傳遞。輸入仍使用既有 `contracts/v1/knowledge-record.schema.json`；legacy schema bytes 不變。

## 使用入口

```sh
python3 scripts/card_delta.py BEFORE.json AFTER.json --batch-size 12
python3 scripts/card_delta.py BEFORE.json AFTER.json --batch-size 12 --cursor '<exact next_cursor>'
```

呼叫者提供同一 protocol 與 subject 的兩份完整 project。CLI 先用既有 `verify()` 驗證兩份資料，單次讀取各檔案的原始 bytes。它不寫入輸入、不執行 Host actions，也不授予 landing authority。驗證失敗以 JSON error 寫入 stderr，exit code 為 2。

## Identity 與 history

相同 canonical key 必須保留 stable ID。card 內容未變時 revision 不變；內容修改時 revision 恰好加一。新 card 從 revision 1 開始，不能重用既有 stable ID。原 card、Source 或 REQ 不能被刪除；supersession 保留原 card，將它更新為 `SUPERSEDED`，並以新 `ACTIVE` card 的 `supersedes` link 指向原 card。

每個 UPDATE 保存完整 previous card 與 current card。非 card 欄位的變更保存 before／after section，包括 Source、REQ acceptance／dependencies、decisions、action requests 與 progress。這些 snapshots 是輸入歷史，不是原 owner 的實際 receipt。compiler 不改寫 receipt，也不自動把 engineering status 升為 tested。

## Batching、失效與完成邊界

card patch 依 after record 的 card 順序排列，每批最多 12 個變更。cursor 綁定 exact before bytes、after bytes、batch size 與 offset。即使只改 JSON 空白，原 cursor 也不能接續；cursor 不是授權或來源真實性證明。Python object API `compile_delta()` 保留 canonical object binding，bytes API `compile_delta_bytes()` 和 CLI 使用 raw bytes binding，兩種 cursor 不能互換。

Source、REQ 與 card 變更只沿明示的依賴產生 advisory `affected_nodes`。沒有依賴的項目保留；類比、競爭或矛盾 link 本身不構成依賴。本單元的依賴 relation 是 `depends_on`、`based_on`、`derived_from`、`implements` 和 `validated_by`。card A 指向 B 時，B 的變更使 A 待重查。REQ 的 `depends_on` 同樣從前置項目傳向 REQ。before／after 兩個依賴圖取聯集，避免移除 link 後丟失原依賴。其他 relations 保留為資料，不自動推定失效方向。REQ 與 card 同 ID 時保留兩種節點，型別資訊由 `affected_records` 表示。

Source grouping 使用 `source_dependency_key`，只避免結構重複計數，不能證明獨立來源或外部 bytes 真實性。

相同資料回傳 `NOOP`。還有 card patch 時回傳 `CONTINUE`。card patch 已取完但非 card 變更仍需原 owner reconciliation 時回傳 `BLOCKED`。`DONE` 只表示本輪 card compilation 完成，不能當作 owner acceptance、runtime effect 或全任務完成。

`effects` 保持空列表，`authorizes_landing` 和 `effect_authority` 都是 false。原 owner 仍負責 Source readback、Schema／Test／Hook／Cron 的原生效果、next consumption，以及 publication／exact-head CI／landing readback。

## 驗證範圍

```sh
python3 -m unittest discover -s tests -v
python3 scripts/factoryweaver.py validate docs/closed-loop-v72/project.json
```

controls 直接消費現有 30 REQ、30 SPEC、68 cards 的 project 與修改後輸入，驗證 NOOP、合法更新、history removal、stable-ID misuse、stale cursor、batch bound、局部失效及 deterministic replay。完整 REQ IDs、acceptance 與 dependencies 都保留。卡片數或映射數不證明語義完整性；本單元不驗收全部 30 REQ 的 runtime，也不取消尚缺的 native Manager effect readback。
