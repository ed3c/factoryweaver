# 從語義草稿準備 v1 record

`factoryweaver.py prepare DRAFT --output ABSOLUTE_DIRECTORY [--previous RECORD]`
保存來源快照及可供原 Validator、Exporter 消費的 v1 record。
這個入口只寫指定輸出目錄，不授權 worker、Issue、發布或整合。

原 CLI 能驗證 v1 身分，但原先沒有從語義草稿產生身分的入口。
若要求 Session 填寫 digest、Card ID 與 revision，會讓 Session 重建程式可決定的資料。
`prepare` 在同一 CLI 補上這段 producer；沿用原 v1 Validator 與 Card Delta，
沒有增加 Registry、另一份知識 schema 或執行狀態機。

草稿包含 `subject`、`sources`、`requirements`、`cards`、`progress`。
`subject` 接受原 v1 的 `scope` 與可選 `consumer`。
`sources` 以語義名稱索引來源；每筆包含絕對 `path`、`source_type`、`locator`，
以及可選的 `source_role`。程式讀取原 bytes、保存快照並計算摘要。
`requirements` 以語義名稱索引原 v1 requirement 欄位，省略 `id`。
`cards` 使用原 v1 Card 欄位，省略 `stable_id` 與 `revision`。
Card 的 `canonical_key` 是 Session 選定的語義身分，不是內容 hash。

Requirement 的 `source_ids`、Card 的 `evidence_ids` 與 progress 的 `evidence_refs`
引用草稿來源名稱。`depends_on` 和 `typed_links.target` 引用 requirement 名稱或 Card
的 `canonical_key`。程式解析引用；未找到的引用拒絕，不推測依賴。
其餘欄位由原 v1 Validator 檢查。規格合法不能證明來源詮釋或因果關係正確。

同一 subject、語義名稱與內容會產生相同身分。傳入 `--previous` 時，
未改 Card 保留 revision；同一 canonical key 的修改保留 stable ID 並增加 revision。
此入口只續編同一語義 subject 所產生的 record。其他 Host 配發的 subject ID
或既有語義名稱映射仍須由原 Host 提供；此入口拒絕代為遷移或猜測。
原 Delta 拒絕刪除既有 Card。前版來源、record 與第一頁 Delta 保存在輸出中；
後續頁仍由原 `card_delta.py` 消費它產生的 cursor。
草稿及輸入前版保存於 `input.json`。原始失敗證據仍由原任務保管，不能用新版覆寫。
`input.json` 同時綁定本次已讀來源所產生的完整 record 摘要。
中斷後若來源 bytes 改變，原目錄拒絕重送；來源路徑相同不足以視為同一輸入。
舊 producer 未保存這項綁定的目錄也不覆寫。已完成 record 仍可由原 Reader 消費。
已有 decision 或 action request 的 record 必須回原 owner；此入口拒絕代管或丟棄它們。

程式先驗證整份結果，再逐檔原子發布。相同請求重送或並行重送讀回相同 bytes。
不同輸入使用相同目的目錄時拒絕。中斷後可以用完全相同輸入續寫尚缺快照，
但不能替換已有檔案。程式只在所有輸出保存後返回 `PREPARED_SPECIFICATION`。
回應中的 `record` 是原程式計算的 FileRef，`references` 提供可供語義選取的真實 ID。
其 `completion=COMPILED_ONLY` 不等於獨立語義審查或工程驗收通過。

下游沿原 `soodles_handoff.py` 產生 Bundle，再交原 Soodles Reader。
每個執行綁定固定版本；修改草稿不會更新已派發任務的輸入。
規格更正與任務修訂仍須原 owner 接受，並保留原 Goal、版本與失敗歷史。
