# 閉環資料流卡片盒

此筆記使用 Zettelkasten Specification Compiler v7.2 portable profile。這次交付規格與 eval 審計。30 個 REQ 描述待實作或待驗的結果，不能因筆記合併便稱系統已完成。

卡片內容以 [project.json](project.json) 為交換資料。[specifications.json](specifications.json) 補完整 SPEC 欄位。[coverage.json](coverage.json) 保留 14 個原句分組、逐項映射及每批最多 12 卡的 cursor。原句分組仍須對照原要求，映射齊全不證明語義無漏項。

Knowledge 為 SPECIFIED。Engineering 為 UNASSESSED。Runtime delivery 為 NOT_STARTED。文件 PR 的交付記錄獨立保存。

## 需求索引

| ID | 結果 | Owner | 前置需求 |
| --- | --- | --- | --- |
| REQ-intent | 保留原始意圖及約束 | Session／Thinking Router | 無 |
| REQ-coverage | 原句到需求逐項覆蓋 | 需求 compiler／task owner | REQ-intent |
| REQ-dependencies | 只阻塞真正相依的工作 | compiler／Schema Manager | REQ-coverage |
| REQ-spec-data | 規格與 schema data 共用契約 | compiler／契約 owner | REQ-coverage |
| REQ-stable-update | 卡片可增修但保留歷史 | compiler／卡片 owner | REQ-spec-data |
| REQ-correction | 直接修正錯誤推論 | Session／原 owner | REQ-stable-update |
| REQ-identity | 所有資料綁定同一驗收對象 | Schema Manager／證據 producer | REQ-spec-data |
| REQ-events | 資料事件自動進入既有 owner | 既有事件／lifecycle owner | REQ-identity, REQ-dependencies |
| REQ-schema | Schema Manager 重算受影響投影 | Schema Manager | REQ-events |
| REQ-test | Test Manager 按差異選必要驗證 | Test Manager | REQ-schema |
| REQ-hook | Hook Manager 驗證原生載入與效果 | Hook Manager／原生設定 owner | REQ-schema |
| REQ-cron | Cron Manager 用等待資料決定喚醒 | Cron Manager／既有 scheduler owner | REQ-schema |
| REQ-inner-loop | Noodle Poteto 小迴圈完成可驗收單位 | 原 Noodle execute session | REQ-dependencies, REQ-spec-data |
| REQ-outer-loop | Soodles 外迴圈維持全部需求分母 | 原 Soodles task／Issue owner | REQ-coverage, REQ-inner-loop |
| REQ-manager-feedback | 四個 Manager 結果回到原 REQ | Manager producer／Schema consumer | REQ-schema, REQ-test, REQ-hook, REQ-cron |
| REQ-consumption | 原 owner 消費返回 next 並讀回 | 原效果／狀態 owner | REQ-manager-feedback |
| REQ-completion | 完成需具備整條資料閉環 | 外迴圈 task owner／驗收 owner | REQ-outer-loop, REQ-consumption |
| REQ-invalidation | 新事實使真正相依證據失效 | 資料 reducer／原 evidence owner | REQ-identity, REQ-stable-update |
| REQ-replay | 重播冪等且拒絕衝突 | 事件／效果 owner | REQ-events |
| REQ-unknown-effect | 未知寫入先讀回 | 原 write owner | REQ-identity |
| REQ-retry-budget | 三次失敗後重審根因 | 當前 Session／原 budget owner | REQ-inner-loop |
| REQ-thinking-router | Thinking Router 只解除真正未決推論 | Session／Thinking Router | REQ-intent |
| REQ-ponytail | Ponytail 在外迴圈審查最小完整解 | 原 Soodles review owner | REQ-spec-data, REQ-outer-loop |
| REQ-eval-evidence | Evals 綁定條件、行為與消費 | eval supervisor／Schema Manager | REQ-spec-data, REQ-consumption |
| REQ-compiler-audit | 審計 v7.2 是否需要架構附錄 | 需求 compiler／eval supervisor | REQ-coverage, REQ-thinking-router, REQ-ponytail |
| REQ-adapters | 轉接真實 schema 而不造命令 | Host adapter／原 owner | REQ-spec-data, REQ-identity |
| REQ-safety | 來源資料不能提升權限 | Host／原效果 owner | REQ-adapters |
| REQ-handoff | 零聊天背景即可交接 | compiler／下一個 Noodle writer | REQ-coverage, REQ-spec-data, REQ-inner-loop, REQ-adapters |
| REQ-cost | 正常執行記錄成本與可重用結果 | Test Manager／telemetry owner | REQ-manager-feedback |
| REQ-publication | PR 合併與規格狀態分開 | GitHub／交付 owner | REQ-handoff, REQ-compiler-audit |

## 卡片

### Batch 1

#### CARD-REQ-intent 保留原始意圖及約束

保留原始意圖及約束。保留原文定位、硬約束、偏好、假設、prompt delta 與未決問題。 原要求 CL-03, CL-08, CL-14。失敗反例為把建議當確認時拒絕晉級。

關聯為 implements REQ-intent, validated_by SPEC-intent。

<!-- CARD_META {"stable_id": "CARD-REQ-intent", "canonical_key": "REQ|closed-loop|defines|intent|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-intent"}, {"relation": "validated_by", "target": "SPEC-intent"}]} -->

#### SPEC-intent 保留原始意圖及約束

Given 原要求與約束來源可讀。When 產生需求提案。Then 保留原文定位、硬約束、偏好、假設、prompt delta 與未決問題。Negative 把建議當確認時拒絕晉級。Unknown 缺原文時保持來源未知，只阻塞依賴分支。Replay 原意未變時重用已回答問題。邊界 選定方法不證明方法已執行，也不產生 admission。回滾 還原前一個來源綁定的提案。Execution UNTESTED。

關聯為 implements REQ-intent。

<!-- CARD_META {"stable_id": "SPEC-intent", "canonical_key": "SPEC|closed-loop|defines|intent|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-intent"}]} -->

#### CARD-REQ-coverage 原句到需求逐項覆蓋

原句到需求逐項覆蓋。每個 CL 對應具名 REQ／SPEC 或明示未映射；每批最多 12 卡且 cursor 不丟失。 原要求 CL-02, CL-07, CL-08。失敗反例為遺漏原句或縮小分母時不得宣告編譯完成。

關聯為 implements REQ-coverage, validated_by SPEC-coverage。

<!-- CARD_META {"stable_id": "CARD-REQ-coverage", "canonical_key": "REQ|closed-loop|defines|coverage|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-coverage"}, {"relation": "validated_by", "target": "SPEC-coverage"}]} -->

#### SPEC-coverage 原句到需求逐項覆蓋

Given 已固定整份原要求。When 拆解需求並分批輸出。Then 每個 CL 對應具名 REQ／SPEC 或明示未映射；每批最多 12 卡且 cursor 不丟失。Negative 遺漏原句或縮小分母時不得宣告編譯完成。Unknown 語義完整性未審時保留 unknown，不能靠連結數證明。Replay 同一 canonical key 保留 ID，不重新生成。邊界 結構映射不是語義無遺漏的證明。回滾 還原 inventory，保留差異與未映射清單。Execution UNTESTED。

關聯為 implements REQ-coverage, depends_on REQ-intent。

<!-- CARD_META {"stable_id": "SPEC-coverage", "canonical_key": "SPEC|closed-loop|defines|coverage|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-coverage"}, {"relation": "depends_on", "target": "REQ-intent"}]} -->

#### CARD-REQ-dependencies 只阻塞真正相依的工作

只阻塞真正相依的工作。僅相依 REQ 等待，獨立且授權內的已知需求繼續。 原要求 CL-08, CL-09, CL-13。失敗反例為循環、懸空 ID 與未審矛盾拒絕 ready。

關聯為 implements REQ-dependencies, validated_by SPEC-dependencies。

<!-- CARD_META {"stable_id": "CARD-REQ-dependencies", "canonical_key": "REQ|closed-loop|defines|dependencies|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-dependencies"}, {"relation": "validated_by", "target": "SPEC-dependencies"}]} -->

#### SPEC-dependencies 只阻塞真正相依的工作

Given 需求與 K／X 的依賴已列明。When 一項必要輸入未知或矛盾。Then 僅相依 REQ 等待，獨立且授權內的已知需求繼續。Negative 循環、懸空 ID 與未審矛盾拒絕 ready。Unknown 未查 producer 的缺件標待查，不直接稱外部阻塞。Replay 相同缺件不重跑，但新輸入到齊可接續。邊界 需求 DAG 不是第二個 scheduler。回滾 撤回受影響 ready 與其下游證據。Execution UNTESTED。

關聯為 implements REQ-dependencies, depends_on REQ-coverage。

<!-- CARD_META {"stable_id": "SPEC-dependencies", "canonical_key": "SPEC|closed-loop|defines|dependencies|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-dependencies"}, {"relation": "depends_on", "target": "REQ-coverage"}]} -->

#### CARD-REQ-spec-data 規格與 schema data 共用契約

規格與 schema data 共用契約。每個規格有 actor、前置、結果、non-case、oracle、回滾及型別；用同一契約產生人讀和機讀輸出。 原要求 CL-02, CL-11。失敗反例為資料與 Given/When/Then 矛盾時拒絕升級。

關聯為 implements REQ-spec-data, validated_by SPEC-spec-data。

<!-- CARD_META {"stable_id": "CARD-REQ-spec-data", "canonical_key": "REQ|closed-loop|defines|spec-data|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-spec-data"}, {"relation": "validated_by", "target": "SPEC-spec-data"}]} -->

#### SPEC-spec-data 規格與 schema data 共用契約

Given 原要求已映射為具名 SPEC。When 定義輸入輸出及資料欄位。Then 每個規格有 actor、前置、結果、non-case、oracle、回滾及型別；用同一契約產生人讀和機讀輸出。Negative 資料與 Given/When/Then 矛盾時拒絕升級。Unknown 無法表示必要語義時新增 K，不靜默丟欄位。Replay 資料不變時輸出 NOOP。邊界 本附錄是提案，不是任意 Host 已支援的 schema。回滾 保留上一契約版本與兼容性差異。Execution UNTESTED。

關聯為 implements REQ-spec-data, depends_on REQ-coverage。

<!-- CARD_META {"stable_id": "SPEC-spec-data", "canonical_key": "SPEC|closed-loop|defines|spec-data|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-spec-data"}, {"relation": "depends_on", "target": "REQ-coverage"}]} -->

#### CARD-REQ-stable-update 卡片可增修但保留歷史

卡片可增修但保留歷史。就地更新現行 revision；保留原版、差異、理由及 supersedes；必要新問題新增 K／X。 原要求 CL-07, CL-09, CL-10。失敗反例為不得刪原要求以消除 FAIL。

關聯為 implements REQ-stable-update, validated_by SPEC-stable-update。

<!-- CARD_META {"stable_id": "CARD-REQ-stable-update", "canonical_key": "REQ|closed-loop|defines|stable-update|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-stable-update"}, {"relation": "validated_by", "target": "SPEC-stable-update"}]} -->

#### SPEC-stable-update 卡片可增修但保留歷史

Given 已有 stable ID 與 canonical key。When 新事實或必要未知出現。Then 就地更新現行 revision；保留原版、差異、理由及 supersedes；必要新問題新增 K／X。Negative 不得刪原要求以消除 FAIL。Unknown 無新證據的現況主張保持假設。Replay 相同新證據重送不增加 revision。邊界 重寫現行文字不改原始 logs／receipts。回滾 切回上一 revision，保持 superseded 關係。Execution UNTESTED。

關聯為 implements REQ-stable-update, depends_on REQ-spec-data。

<!-- CARD_META {"stable_id": "SPEC-stable-update", "canonical_key": "SPEC|closed-loop|defines|stable-update|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-stable-update"}, {"relation": "depends_on", "target": "REQ-spec-data"}]} -->

#### CARD-REQ-correction 直接修正錯誤推論

直接修正錯誤推論。記錄原主張、前提、證據、失效點、支持結論及對下一步的影響。 原要求 CL-10。失敗反例為不能只調整驗收文字使候選變綠。

關聯為 implements REQ-correction, validated_by SPEC-correction。

<!-- CARD_META {"stable_id": "CARD-REQ-correction", "canonical_key": "REQ|closed-loop|defines|correction|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-correction"}, {"relation": "validated_by", "target": "SPEC-correction"}]} -->

#### SPEC-correction 直接修正錯誤推論

Given 主張、前提與來源可定位。When 新觀察推翻推論或事實。Then 記錄原主張、前提、證據、失效點、支持結論及對下一步的影響。Negative 不能只調整驗收文字使候選變綠。Unknown 尚不能判定的因果保持 hypothesis。Replay 未變的已修事實不重做調查。邊界 修正事實不授權未知外部效果。回滾 還原候選資料，保留已證偽的主張與原因。Execution UNTESTED。

關聯為 implements REQ-correction, depends_on REQ-stable-update。

<!-- CARD_META {"stable_id": "SPEC-correction", "canonical_key": "SPEC|closed-loop|defines|correction|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-correction"}, {"relation": "depends_on", "target": "REQ-stable-update"}]} -->

### Batch 2

#### CARD-REQ-identity 所有資料綁定同一驗收對象

所有資料綁定同一驗收對象。核對 task、owner、session 或 N/A、head、需求與規格摘要、plan、環境、producer、sequence 及 artifact identity。 原要求 CL-04, CL-06, CL-11。失敗反例為跨任務／版本／producer 的 PASS 不得重用。

關聯為 implements REQ-identity, validated_by SPEC-identity。

<!-- CARD_META {"stable_id": "CARD-REQ-identity", "canonical_key": "REQ|closed-loop|defines|identity|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-identity"}, {"relation": "validated_by", "target": "SPEC-identity"}]} -->

#### SPEC-identity 所有資料綁定同一驗收對象

Given 選定 task、REQ、SPEC、來源與候選版本。When 接收事件或驗收產物。Then 核對 task、owner、session 或 N/A、head、需求與規格摘要、plan、環境、producer、sequence 及 artifact identity。Negative 跨任務／版本／producer 的 PASS 不得重用。Unknown 缺身分時要求原 owner 讀回，只停相依操作。Replay 重送同一事件識別回原結果；衝突拒絕。邊界 hash 證明 bytes，不能證明可信 producer 或授權。回滾 撤回錯配投影，不改原始產物。Execution UNTESTED。

關聯為 implements REQ-identity, depends_on REQ-spec-data。

<!-- CARD_META {"stable_id": "SPEC-identity", "canonical_key": "SPEC|closed-loop|defines|identity|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-identity"}, {"relation": "depends_on", "target": "REQ-spec-data"}]} -->

#### CARD-REQ-events 資料事件自動進入既有 owner

資料事件自動進入既有 owner。以驗證後事件觸發必要 Manager；owner 持續接續，不等新使用者提示；保存 request/result/consumption 關係。 原要求 CL-04, CL-06。失敗反例為未註冊事件或任意 argv 不得執行。

關聯為 implements REQ-events, validated_by SPEC-events。

<!-- CARD_META {"stable_id": "CARD-REQ-events", "canonical_key": "REQ|closed-loop|defines|events|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-events"}, {"relation": "validated_by", "target": "SPEC-events"}]} -->

#### SPEC-events 資料事件自動進入既有 owner

Given Host 已獨立登錄事件 adapter 與授權。When 需求、來源、結果、hook 設定或等待條件改變。Then 以驗證後事件觸發必要 Manager；owner 持續接續，不等新使用者提示；保存 request/result/consumption 關係。Negative 未註冊事件或任意 argv 不得執行。Unknown 投遞結果未知先讀回；缺 adapter 回具名工程工作。Replay duplicate 不再產生效果；out-of-order 不覆蓋新結果。邊界 自動觸發沿原 owner，不新增排程器或 compiler 執行權。回滾 停用本次新增 binding，由原設定 owner 恢復上一版本。Execution UNTESTED。

關聯為 implements REQ-events, depends_on REQ-identity, depends_on REQ-dependencies。

<!-- CARD_META {"stable_id": "SPEC-events", "canonical_key": "SPEC|closed-loop|defines|events|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-events"}, {"relation": "depends_on", "target": "REQ-identity"}, {"relation": "depends_on", "target": "REQ-dependencies"}]} -->

#### CARD-REQ-schema Schema Manager 重算受影響投影

Schema Manager 重算受影響投影。回傳 current state、前提證據、known/unknown、影響 REQ 及唯一支持的 next 或工程缺口。 原要求 CL-03, CL-04, CL-06, CL-11。失敗反例為無證據不能把 projected success 當實際成功。

關聯為 implements REQ-schema, validated_by SPEC-schema。

<!-- CARD_META {"stable_id": "CARD-REQ-schema", "canonical_key": "REQ|closed-loop|defines|schema|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-schema"}, {"relation": "validated_by", "target": "SPEC-schema"}]} -->

#### SPEC-schema Schema Manager 重算受影響投影

Given 事件身分與依賴有效。When 原 owner 提交已驗證的新資料。Then 回傳 current state、前提證據、known/unknown、影響 REQ 及唯一支持的 next 或工程缺口。Negative 無證據不能把 projected success 當實際成功。Unknown missing 欄位指明 producer 與下一個必要輸入。Replay 同一資料得同一投影；未消費 next 仍須接續。邊界 Schema 投影不授予 Test／Hook／Cron／landing 效果。回滾 撤回受影響快取投影，以保存 facts 重算。Execution UNTESTED。

關聯為 implements REQ-schema, depends_on REQ-events。

<!-- CARD_META {"stable_id": "SPEC-schema", "canonical_key": "SPEC|closed-loop|defines|schema|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-schema"}, {"relation": "depends_on", "target": "REQ-events"}]} -->

#### CARD-REQ-test Test Manager 按差異選必要驗證

Test Manager 按差異選必要驗證。選 focused controls／必要 consumer observations；保存 exact selection、實際執行及原始產物，再回 Schema。 原要求 CL-05, CL-06, CL-11。失敗反例為格式檢查或 scope plan 不得算行為 PASS；不得推定 full suite。

關聯為 implements REQ-test, validated_by SPEC-test。

<!-- CARD_META {"stable_id": "CARD-REQ-test", "canonical_key": "REQ|closed-loop|defines|test|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-test"}, {"relation": "validated_by", "target": "SPEC-test"}]} -->

#### SPEC-test Test Manager 按差異選必要驗證

Given 有變更範圍及原 oracle。When 新規格或結果需要判別行為。Then 選 focused controls／必要 consumer observations；保存 exact selection、實際執行及原始產物，再回 Schema。Negative 格式檢查或 scope plan 不得算行為 PASS；不得推定 full suite。Unknown known deterministic fault 用既有 control；缺憑證不觸發 eval。Replay 相同 bytes／inputs／claim 重用已涵蓋結果。邊界 scope owner 不兼任外部驗收 owner。回滾 回復候選，重驗受到影響的有限邊界。Execution UNTESTED。

關聯為 implements REQ-test, depends_on REQ-schema。

<!-- CARD_META {"stable_id": "SPEC-test", "canonical_key": "SPEC|closed-loop|defines|test|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-test"}, {"relation": "depends_on", "target": "REQ-schema"}]} -->

#### CARD-REQ-hook Hook Manager 驗證原生載入與效果

Hook Manager 驗證原生載入與效果。記錄 native trust、loaded、matched、invoked、completed、delivered 及原 owner effect readback。 原要求 CL-04, CL-06。失敗反例為設定檔存在或 fixture 綠不能算原生 hook 已啟用。

關聯為 implements REQ-hook, validated_by SPEC-hook。

<!-- CARD_META {"stable_id": "CARD-REQ-hook", "canonical_key": "REQ|closed-loop|defines|hook|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-hook"}, {"relation": "validated_by", "target": "SPEC-hook"}]} -->

#### SPEC-hook Hook Manager 驗證原生載入與效果

Given carrier 與精確 hook 定義已選定。When 定義或事件接線改變。Then 記錄 native trust、loaded、matched、invoked、completed、delivered 及原 owner effect readback。Negative 設定檔存在或 fixture 綠不能算原生 hook 已啟用。Unknown carrier 不支持 hook 時 K 保持未知，獨立工作繼續。Replay 同一事件不反覆要求續作；取消或終態不復活。邊界 不同 carrier 需各自證據；Codex App 無此能力不能冒稱 CLI hook。回滾 由原設定 owner 撤 binding 並讀回停用結果。Execution UNTESTED。

關聯為 implements REQ-hook, depends_on REQ-schema。

<!-- CARD_META {"stable_id": "SPEC-hook", "canonical_key": "SPEC|closed-loop|defines|hook|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-hook"}, {"relation": "depends_on", "target": "REQ-schema"}]} -->

#### CARD-REQ-cron Cron Manager 用等待資料決定喚醒

Cron Manager 用等待資料決定喚醒。以原 scheduler 建立／更新／取消具名 wakeup；醒來重查身分與 prerequisites，消費原 next。 原要求 CL-04, CL-06。失敗反例為無可做事項且阻塞未變不得重跑寫入；不得醒後重設预算。

關聯為 implements REQ-cron, validated_by SPEC-cron。

<!-- CARD_META {"stable_id": "CARD-REQ-cron", "canonical_key": "REQ|closed-loop|defines|cron|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-cron"}, {"relation": "validated_by", "target": "SPEC-cron"}]} -->

#### SPEC-cron Cron Manager 用等待資料決定喚醒

Given 同一任務仍有效且存在必要等待或接續。When 等待條件、deadline、授權或終態改變。Then 以原 scheduler 建立／更新／取消具名 wakeup；醒來重查身分與 prerequisites，消費原 next。Negative 無可做事項且阻塞未變不得重跑寫入；不得醒後重設预算。Unknown 缺平台能力或設定讀回時保留 K。Replay 重送同一排程 identity 不建第二份；終態與取消停止喚醒。邊界 Cron 只喚醒 owner，不決定需求或驗收。回滾 取消本次具名排程並取得原 scheduler 讀回。Execution UNTESTED。

關聯為 implements REQ-cron, depends_on REQ-schema。

<!-- CARD_META {"stable_id": "SPEC-cron", "canonical_key": "SPEC|closed-loop|defines|cron|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-cron"}, {"relation": "depends_on", "target": "REQ-schema"}]} -->

### Batch 3

#### CARD-REQ-inner-loop Noodle Poteto 小迴圈完成可驗收單位

Noodle Poteto 小迴圈完成可驗收單位。選原 Poteto playbook，讀相似實作，小步修改、必要驗證、自審 diff，回填本單位結果後继续其他可做需求。 原要求 CL-05, CL-08, CL-13。失敗反例為局部 commit／PASS 不能作整份任務 stopping point。

關聯為 implements REQ-inner-loop, validated_by SPEC-inner-loop。

<!-- CARD_META {"stable_id": "CARD-REQ-inner-loop", "canonical_key": "REQ|closed-loop|defines|inner-loop|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-inner-loop"}, {"relation": "validated_by", "target": "SPEC-inner-loop"}]} -->

#### SPEC-inner-loop Noodle Poteto 小迴圈完成可驗收單位

Given 原 admission／execution envelope 固定且工作授權有效。When 已有可執行 task unit。Then 選原 Poteto playbook，讀相似實作，小步修改、必要驗證、自審 diff，回填本單位結果後继续其他可做需求。Negative 局部 commit／PASS 不能作整份任務 stopping point。Unknown 缺原 session 身分只停需要該身分的效果。Replay 原終態 session 不自行重啟；重送結果回原紀錄。邊界 本次交接不啟動 Noodle、不製造 admission。回滾 由原 owner 回滾該單位，保留失敗歷史。Execution UNTESTED。

關聯為 implements REQ-inner-loop, depends_on REQ-dependencies, depends_on REQ-spec-data。

<!-- CARD_META {"stable_id": "SPEC-inner-loop", "canonical_key": "SPEC|closed-loop|defines|inner-loop|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-inner-loop"}, {"relation": "depends_on", "target": "REQ-dependencies"}, {"relation": "depends_on", "target": "REQ-spec-data"}]} -->

#### CARD-REQ-outer-loop Soodles 外迴圈維持全部需求分母

Soodles 外迴圈維持全部需求分母。核對全部 REQ、未映射原句、缺件與下一步；可做項目继续，只有全要求具證據才整體完成。 原要求 CL-05, CL-08, CL-13。失敗反例為單一 owner next=null 或無新 bug 不能結束整份能力工作。

關聯為 implements REQ-outer-loop, validated_by SPEC-outer-loop。

<!-- CARD_META {"stable_id": "CARD-REQ-outer-loop", "canonical_key": "REQ|closed-loop|defines|outer-loop|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-outer-loop"}, {"relation": "validated_by", "target": "SPEC-outer-loop"}]} -->

#### SPEC-outer-loop Soodles 外迴圈維持全部需求分母

Given 整份需求及全部局部結果仍可讀。When 一個小迴圈返回結果。Then 核對全部 REQ、未映射原句、缺件與下一步；可做項目继续，只有全要求具證據才整體完成。Negative 單一 owner next=null 或無新 bug 不能結束整份能力工作。Unknown 沒有原身份的歷史欠帳保留在原任務，不阻塞獨立新工作。Replay 終態新證據按原任務邊界處理，不重開生命週期。邊界 外迴圈不把 runtime 確認責任塞回 compiler。回滾 撤回錯誤 whole-task complete，回到剩餘需求。Execution UNTESTED。

關聯為 implements REQ-outer-loop, depends_on REQ-coverage, depends_on REQ-inner-loop。

<!-- CARD_META {"stable_id": "SPEC-outer-loop", "canonical_key": "SPEC|closed-loop|defines|outer-loop|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-outer-loop"}, {"relation": "depends_on", "target": "REQ-coverage"}, {"relation": "depends_on", "target": "REQ-inner-loop"}]} -->

#### CARD-REQ-manager-feedback 四個 Manager 結果回到原 REQ

四個 Manager 結果回到原 REQ。引用原 requirements digest 與 REQ ID，保存 Manager request/result、範圍、缺口和返回 next；再更新同一 handoff。 原要求 CL-04, CL-06, CL-11。失敗反例為分類 PASS、清冊或新檔名不能當原需求完成。

關聯為 implements REQ-manager-feedback, validated_by SPEC-manager-feedback。

<!-- CARD_META {"stable_id": "CARD-REQ-manager-feedback", "canonical_key": "REQ|closed-loop|defines|manager-feedback|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-manager-feedback"}, {"relation": "validated_by", "target": "SPEC-manager-feedback"}]} -->

#### SPEC-manager-feedback 四個 Manager 結果回到原 REQ

Given 已取得 selected Manager 的实际輸出。When 原 producer 發出結果事件。Then 引用原 requirements digest 與 REQ ID，保存 Manager request/result、範圍、缺口和返回 next；再更新同一 handoff。Negative 分類 PASS、清冊或新檔名不能當原需求完成。Unknown result 尚未到齊保持 pending，不填 expected。Replay 同一 result identity 不產生第二份 state store。邊界 資料按原 owner schema 轉換，不能假造互操作已成立。回滾 撤回錯誤映射，保留 producer 原結果。Execution UNTESTED。

關聯為 implements REQ-manager-feedback, depends_on REQ-schema, depends_on REQ-test, depends_on REQ-hook, depends_on REQ-cron。

<!-- CARD_META {"stable_id": "SPEC-manager-feedback", "canonical_key": "SPEC|closed-loop|defines|manager-feedback|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-manager-feedback"}, {"relation": "depends_on", "target": "REQ-schema"}, {"relation": "depends_on", "target": "REQ-test"}, {"relation": "depends_on", "target": "REQ-hook"}, {"relation": "depends_on", "target": "REQ-cron"}]} -->

#### CARD-REQ-consumption 原 owner 消費返回 next 並讀回

原 owner 消費返回 next 並讀回。保存原 returned_next、實際 actor、合法輸入、執行結果及 owner readback；結果再回 Schema。 原要求 CL-04, CL-05, CL-06。失敗反例為只寫 consumed=true 或摘要不能算效果完成。

關聯為 implements REQ-consumption, validated_by SPEC-consumption。

<!-- CARD_META {"stable_id": "CARD-REQ-consumption", "canonical_key": "REQ|closed-loop|defines|consumption|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-consumption"}, {"relation": "validated_by", "target": "SPEC-consumption"}]} -->

#### SPEC-consumption 原 owner 消費返回 next 並讀回

Given Manager 返回具名 next。When 原 Session 有合法接續且前提到齊。Then 保存原 returned_next、實際 actor、合法輸入、執行結果及 owner readback；結果再回 Schema。Negative 只寫 consumed=true 或摘要不能算效果完成。Unknown next 無 argv 時处理具名工程工作；寫入未知先讀回。Replay 未消費 next 即使無新 bytes 仍可做；已完成的效果不重播。邊界 owner 是職責來源，不必是另一帳號或另一 chat。回滾 由原效果 owner 撤回並讀回殘留效果。Execution UNTESTED。

關聯為 implements REQ-consumption, depends_on REQ-manager-feedback。

<!-- CARD_META {"stable_id": "SPEC-consumption", "canonical_key": "SPEC|closed-loop|defines|consumption|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-consumption"}, {"relation": "depends_on", "target": "REQ-manager-feedback"}]} -->

#### CARD-REQ-completion 完成需具備整條資料閉環

完成需具備整條資料閉環。逐 REQ 核對來源、SPEC、必要 Manager 結果、owner consumption、效果及交付 readback；保留 knowledge/engineering/delivery 三軸。 原要求 CL-04, CL-05, CL-08, CL-13。失敗反例為schema 合法、CI 綠、report 自述或編譯 DONE 不能代替整體完成。

關聯為 implements REQ-completion, validated_by SPEC-completion。

<!-- CARD_META {"stable_id": "CARD-REQ-completion", "canonical_key": "REQ|closed-loop|defines|completion|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-completion"}, {"relation": "validated_by", "target": "SPEC-completion"}]} -->

#### SPEC-completion 完成需具備整條資料閉環

Given 整份要求無未映射項且必要結果存在。When 申報 whole-task complete。Then 逐 REQ 核對來源、SPEC、必要 Manager 結果、owner consumption、效果及交付 readback；保留 knowledge/engineering/delivery 三軸。Negative schema 合法、CI 綠、report 自述或編譯 DONE 不能代替整體完成。Unknown 全部剩餘項不可取得且有 producer 查證才申報 scoped blocked。Replay 已驗範圍與原始 failure history 保留。邊界 有限案例閉環不證明所有未知錯誤都可自動修復。回滾 撤回不符範圍的完成宣告，保留局部驗證。Execution UNTESTED。

關聯為 implements REQ-completion, depends_on REQ-outer-loop, depends_on REQ-consumption。

<!-- CARD_META {"stable_id": "SPEC-completion", "canonical_key": "SPEC|closed-loop|defines|completion|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-completion"}, {"relation": "depends_on", "target": "REQ-outer-loop"}, {"relation": "depends_on", "target": "REQ-consumption"}]} -->

#### CARD-REQ-invalidation 新事實使真正相依證據失效

新事實使真正相依證據失效。只失效其傳遞依賴的證據、confirmation 與 ready；保留不相依成果及舊版來源。 原要求 CL-10, CL-11。失敗反例為舊 PASS 不得覆蓋目前 FAIL。

關聯為 implements REQ-invalidation, validated_by SPEC-invalidation。

<!-- CARD_META {"stable_id": "CARD-REQ-invalidation", "canonical_key": "REQ|closed-loop|defines|invalidation|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-invalidation"}, {"relation": "validated_by", "target": "SPEC-invalidation"}]} -->

#### SPEC-invalidation 新事實使真正相依證據失效

Given 有具名 evidence dependency edges。When source／head／plan／SPEC／環境／readback 改變。Then 只失效其傳遞依賴的證據、confirmation 與 ready；保留不相依成果及舊版來源。Negative 舊 PASS 不得覆蓋目前 FAIL。Unknown 未知依賴須先查 owner，不猜全部通過。Replay 相同身份重送不失效；相同時間不代表無可做 next。邊界 保留歷史，不把 hash 當外部確認。回滾 從保留的事實與依賴重新投影。Execution UNTESTED。

關聯為 implements REQ-invalidation, depends_on REQ-identity, depends_on REQ-stable-update。

<!-- CARD_META {"stable_id": "SPEC-invalidation", "canonical_key": "SPEC|closed-loop|defines|invalidation|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-invalidation"}, {"relation": "depends_on", "target": "REQ-identity"}, {"relation": "depends_on", "target": "REQ-stable-update"}]} -->

### Batch 4

#### CARD-REQ-replay 重播冪等且拒絕衝突

重播冪等且拒絕衝突。精確 duplicate 返回原 receipt；同 ID 不同 payload 拒絕；舊 sequence 不覆蓋新狀態。 原要求 CL-04, CL-06。失敗反例為不得靠新檔名／新 request ID 繞去重。

關聯為 implements REQ-replay, validated_by SPEC-replay。

<!-- CARD_META {"stable_id": "CARD-REQ-replay", "canonical_key": "REQ|closed-loop|defines|replay|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-replay"}, {"relation": "validated_by", "target": "SPEC-replay"}]} -->

#### SPEC-replay 重播冪等且拒絕衝突

Given 同一 task、producer、event identity 與 payload digest。When 重送或亂序到達。Then 精確 duplicate 返回原 receipt；同 ID 不同 payload 拒絕；舊 sequence 不覆蓋新狀態。Negative 不得靠新檔名／新 request ID 繞去重。Unknown 先前 effects unknown 時沿原 owner 讀回，不執行同一寫入。Replay duplicate 本身不產生新 effects 或 retry attempt。邊界 以原事件 writer 保留歷史，不新增重試 engine。回滾 停止本次投遞，查明原 event writer。Execution UNTESTED。

關聯為 implements REQ-replay, depends_on REQ-events。

<!-- CARD_META {"stable_id": "SPEC-replay", "canonical_key": "SPEC|closed-loop|defines|replay|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-replay"}, {"relation": "depends_on", "target": "REQ-events"}]} -->

#### CARD-REQ-unknown-effect 未知寫入先讀回

未知寫入先讀回。停止同一效果重送，沿原 owner 查 readback；其他已知需求继续。 原要求 CL-04, CL-06, CL-13。失敗反例為改 identity、credentials 或換 session 重寫不合法。

關聯為 implements REQ-unknown-effect, validated_by SPEC-unknown-effect。

<!-- CARD_META {"stable_id": "CARD-REQ-unknown-effect", "canonical_key": "REQ|closed-loop|defines|unknown-effect|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-unknown-effect"}, {"relation": "validated_by", "target": "SPEC-unknown-effect"}]} -->

#### SPEC-unknown-effect 未知寫入先讀回

Given 已尝試写入且結果未明。When 沒有確定 receipt 或 transport 中斷。Then 停止同一效果重送，沿原 owner 查 readback；其他已知需求继续。Negative 改 identity、credentials 或換 session 重寫不合法。Unknown 尚未嘗試的可產生輸入不叫 unknown write。Replay 重複 missing readback 不消耗修正次數。邊界 不能把正確拒絕叫恢復成功。回滾 取得原 owner 的補償／撤回讀回。Execution UNTESTED。

關聯為 implements REQ-unknown-effect, depends_on REQ-identity。

<!-- CARD_META {"stable_id": "SPEC-unknown-effect", "canonical_key": "SPEC|closed-loop|defines|unknown-effect|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-unknown-effect"}, {"relation": "depends_on", "target": "REQ-identity"}]} -->

#### CARD-REQ-retry-budget 三次失敗後重審根因

三次失敗後重審根因。停止不變重試，記錄嘗試／錯誤／原因，質疑抽象並改採更小路徑；保留任務與预算。 原要求 CL-08, CL-10, CL-13。失敗反例為新 chat／新名稱／cron wakeup 不重設次數。

關聯為 implements REQ-retry-budget, validated_by SPEC-retry-budget。

<!-- CARD_META {"stable_id": "CARD-REQ-retry-budget", "canonical_key": "REQ|closed-loop|defines|retry-budget|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-retry-budget"}, {"relation": "validated_by", "target": "SPEC-retry-budget"}]} -->

#### SPEC-retry-budget 三次失敗後重審根因

Given 已有可診斷的修正失敗歷史。When 同一問題第三次修正失敗。Then 停止不變重試，記錄嘗試／錯誤／原因，質疑抽象並改採更小路徑；保留任務與预算。Negative 新 chat／新名稱／cron wakeup 不重設次數。Unknown 缺證據與同一讀回不冒充修正失敗。Replay 再次讀回相同結果不新增失敗。邊界 重審根因不取消已知独立需求。回滾 回復最近可驗證候選，保存失敗三筆。Execution UNTESTED。

關聯為 implements REQ-retry-budget, depends_on REQ-inner-loop。

<!-- CARD_META {"stable_id": "SPEC-retry-budget", "canonical_key": "SPEC|closed-loop|defines|retry-budget|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-retry-budget"}, {"relation": "depends_on", "target": "REQ-inner-loop"}]} -->

#### CARD-REQ-thinking-router Thinking Router 只解除真正未決推論

Thinking Router 只解除真正未決推論。選最小必要方法或 none，保存 trigger、reason、prompt delta 與未決輸入；事實先查來源。 原要求 CL-03, CL-14。失敗反例為不得把五種方法作固定 checklist，或替代 Poteto execute。

關聯為 implements REQ-thinking-router, validated_by SPEC-thinking-router。

<!-- CARD_META {"stable_id": "CARD-REQ-thinking-router", "canonical_key": "REQ|closed-loop|defines|thinking-router|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-thinking-router"}, {"relation": "validated_by", "target": "SPEC-thinking-router"}]} -->

#### SPEC-thinking-router Thinking Router 只解除真正未決推論

Given 同一任務來源與有效 continuation 已知。When 出現實質未決意圖、前提或職責問題。Then 選最小必要方法或 none，保存 trigger、reason、prompt delta 與未決輸入；事實先查來源。Negative 不得把五種方法作固定 checklist，或替代 Poteto execute。Unknown 工具或上游 wrapper 未可用時不稱已執行。Replay 已回答且前提未變不重新問；現有 next 有效則沿用。邊界 方法是 P-class 提案；不創造 Issue contract 或 effect authority。回滾 撤回不受證據支持的方法及附加約束。Execution UNTESTED。

關聯為 implements REQ-thinking-router, depends_on REQ-intent。

<!-- CARD_META {"stable_id": "SPEC-thinking-router", "canonical_key": "SPEC|closed-loop|defines|thinking-router|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-thinking-router"}, {"relation": "depends_on", "target": "REQ-intent"}]} -->

#### CARD-REQ-ponytail Ponytail 在外迴圈審查最小完整解

Ponytail 在外迴圈審查最小完整解。選用可用的 Ponytail review，檢查所有必要呼叫者、測試、設定、失敗邊界與漏項，findings 回原 owner。 原要求 CL-13, CL-14。失敗反例為更短 diff 但漏需求、讀回或安全邊界不合格。

關聯為 implements REQ-ponytail, validated_by SPEC-ponytail。

<!-- CARD_META {"stable_id": "CARD-REQ-ponytail", "canonical_key": "REQ|closed-loop|defines|ponytail|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-ponytail"}, {"relation": "validated_by", "target": "SPEC-ponytail"}]} -->

#### SPEC-ponytail Ponytail 在外迴圈審查最小完整解

Given 具名候選 diff 與全部需求可讀。When 需要檢查多餘機制或交付 readiness。Then 選用可用的 Ponytail review，檢查所有必要呼叫者、測試、設定、失敗邊界與漏項，findings 回原 owner。Negative 更短 diff 但漏需求、讀回或安全邊界不合格。Unknown 尚無獨立 review／安裝證據時保持候選能力未知。Replay 相同候選與已涵蓋 scope 可重用 review。邊界 Ponytail 不另建 inner loop，不授予 merge。回滾 撤回多餘改動，仍完成原要求。Execution UNTESTED。

關聯為 implements REQ-ponytail, depends_on REQ-spec-data, depends_on REQ-outer-loop。

<!-- CARD_META {"stable_id": "SPEC-ponytail", "canonical_key": "SPEC|closed-loop|defines|ponytail|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-ponytail"}, {"relation": "depends_on", "target": "REQ-spec-data"}, {"relation": "depends_on", "target": "REQ-outer-loop"}]} -->

#### CARD-REQ-eval-evidence Evals 綁定條件、行為與消費

Evals 綁定條件、行為與消費。先 error analysis；客觀條件用程式或 receipts，語義 judge 須人標校準；保存真實 input／instructions／trace／report 與已消費 next。 原要求 CL-05, CL-12。失敗反例為自己填 expected、用 style 分數或 fixture 冒充實際 consumer 不合格。

關聯為 implements REQ-eval-evidence, validated_by SPEC-eval-evidence。

<!-- CARD_META {"stable_id": "CARD-REQ-eval-evidence", "canonical_key": "REQ|closed-loop|defines|eval-evidence|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-eval-evidence"}, {"relation": "validated_by", "target": "SPEC-eval-evidence"}]} -->

#### SPEC-eval-evidence Evals 綁定條件、行為與消費

Given 要驗的行為與原要求已固定。When 來源與正常 logs 不能回答 Agent 行為問題。Then 先 error analysis；客觀條件用程式或 receipts，語義 judge 須人標校準；保存真實 input／instructions／trace／report 與已消費 next。Negative 自己填 expected、用 style 分數或 fixture 冒充實際 consumer 不合格。Unknown 缺 human labels、完整 capture 或原生執行時只保留該證據缺口。Replay 未變 instructions、inputs、claim 可重用綁定觀察。邊界 來源審閱、模型觀察與原生 runtime 三者分開。回滾 保留失敗 protocol，修正有根據條件後重驗受影響決策。Execution UNTESTED。

關聯為 implements REQ-eval-evidence, depends_on REQ-spec-data, depends_on REQ-consumption。

<!-- CARD_META {"stable_id": "SPEC-eval-evidence", "canonical_key": "SPEC|closed-loop|defines|eval-evidence|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-eval-evidence"}, {"relation": "depends_on", "target": "REQ-spec-data"}, {"relation": "depends_on", "target": "REQ-consumption"}]} -->

### Batch 5

#### CARD-REQ-compiler-audit 審計 v7.2 是否需要架構附錄

審計 v7.2 是否需要架構附錄。指出六個診斷區域的有據缺口，提出相容附錄，有限 consumer 檢查不宣稱因果改善或普遍可靠。 原要求 CL-02, CL-12, CL-13, CL-14。失敗反例為v7.1 未提供不能聲稱全部 inherited gates 已驗。

關聯為 implements REQ-compiler-audit, validated_by SPEC-compiler-audit。

<!-- CARD_META {"stable_id": "CARD-REQ-compiler-audit", "canonical_key": "REQ|closed-loop|defines|compiler-audit|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-compiler-audit"}, {"relation": "validated_by", "target": "SPEC-compiler-audit"}]} -->

#### SPEC-compiler-audit 審計 v7.2 是否需要架構附錄

Given v7.2 portable profile 與候選／main 架構分開可查。When 依 eval-audit 審閱交接資料及現有驗收邊界。Then 指出六個診斷區域的有據缺口，提出相容附錄，有限 consumer 檢查不宣稱因果改善或普遍可靠。Negative v7.1 未提供不能聲稱全部 inherited gates 已驗。Unknown 缺真實閉環 traces 時不可量化缺陷率或稱 runtime 已修。Replay 既有審計只在來源或行為改變時更新。邊界 v7.2 原文保留；本 profile 不冒稱官方 v7.3。回滾 撤回附錄，不改既有 compiler 信任邊界。Execution UNTESTED。

關聯為 implements REQ-compiler-audit, depends_on REQ-coverage, depends_on REQ-thinking-router, depends_on REQ-ponytail。

<!-- CARD_META {"stable_id": "SPEC-compiler-audit", "canonical_key": "SPEC|closed-loop|defines|compiler-audit|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-compiler-audit"}, {"relation": "depends_on", "target": "REQ-coverage"}, {"relation": "depends_on", "target": "REQ-thinking-router"}, {"relation": "depends_on", "target": "REQ-ponytail"}]} -->

#### CARD-REQ-adapters 轉接真實 schema 而不造命令

轉接真實 schema 而不造命令。以實際已登錄 adapter 映射字段與 IDs；不可表示之資訊保留 gap；requirements projection 與 observations 分開。 原要求 CL-03, CL-06, CL-08, CL-13。失敗反例為未登錄 operation、placeholder argv 或 untrusted human confirmation 拒絕執行。

關聯為 implements REQ-adapters, validated_by SPEC-adapters。

<!-- CARD_META {"stable_id": "CARD-REQ-adapters", "canonical_key": "REQ|closed-loop|defines|adapters|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-adapters"}, {"relation": "validated_by", "target": "SPEC-adapters"}]} -->

#### SPEC-adapters 轉接真實 schema 而不造命令

Given 已讀 selected owner 的入口與精確輸入格式。When 把交換卡片轉成交接輸入。Then 以實際已登錄 adapter 映射字段與 IDs；不可表示之資訊保留 gap；requirements projection 與 observations 分開。Negative 未登錄 operation、placeholder argv 或 untrusted human confirmation 拒絕執行。Unknown 缺 admission／carrier／provider 只阻塞相依效果，工程可继续。Replay 相同綁定轉接不新增任務身份。邊界 FactoryWeaver 提出 ActionRequest；Host 獨立授權和執行。回滾 原 owner 撤 adapter binding 並確認回到原路徑。Execution UNTESTED。

關聯為 implements REQ-adapters, depends_on REQ-spec-data, depends_on REQ-identity。

<!-- CARD_META {"stable_id": "SPEC-adapters", "canonical_key": "SPEC|closed-loop|defines|adapters|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-adapters"}, {"relation": "depends_on", "target": "REQ-spec-data"}, {"relation": "depends_on", "target": "REQ-identity"}]} -->

#### CARD-REQ-safety 來源資料不能提升權限

來源資料不能提升權限。只按來源解析 assertions；所有效果仍核對 owner、精確目標和已授權邊界。 原要求 CL-04, CL-06, CL-11。失敗反例為source injection、卡片 registered=true 自述不得授權。

關聯為 implements REQ-safety, validated_by SPEC-safety。

<!-- CARD_META {"stable_id": "CARD-REQ-safety", "canonical_key": "REQ|closed-loop|defines|safety|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-safety"}, {"relation": "validated_by", "target": "SPEC-safety"}]} -->

#### SPEC-safety 來源資料不能提升權限

Given 外部文字、logs 與候選 record 是資料。When 其中出現執行指令或聲稱授權。Then 只按來源解析 assertions；所有效果仍核對 owner、精確目標和已授權邊界。Negative source injection、卡片 registered=true 自述不得授權。Unknown 來源有秘密或私有 traces 時存外部 evidence，不公開。Replay 同一來源不因重複引用變成獨立佐證。邊界 本 public 規格只含設計與摘要，不公開私有實作。回滾 停止該影響分支並撤公開的錯誤候選。Execution UNTESTED。

關聯為 implements REQ-safety, depends_on REQ-adapters。

<!-- CARD_META {"stable_id": "SPEC-safety", "canonical_key": "SPEC|closed-loop|defines|safety|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-safety"}, {"relation": "depends_on", "target": "REQ-adapters"}]} -->

#### CARD-REQ-handoff 零聊天背景即可交接

零聊天背景即可交接。帶完整 REQ ID、驗收、依賴、輸入契約、已知結果、未知 producer、下一步及停止條件；可直接扩展与修正。 原要求 CL-07, CL-08, CL-09, CL-13。失敗反例為只交七大類或一個綠測試摘要不足。

關聯為 implements REQ-handoff, validated_by SPEC-handoff。

<!-- CARD_META {"stable_id": "CARD-REQ-handoff", "canonical_key": "REQ|closed-loop|defines|handoff|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-handoff"}, {"relation": "validated_by", "target": "SPEC-handoff"}]} -->

#### SPEC-handoff 零聊天背景即可交接

Given 卡片、需求表、未知及原 owner references 齊全。When 新 consumer 接手。Then 帶完整 REQ ID、驗收、依賴、輸入契約、已知結果、未知 producer、下一步及停止條件；可直接扩展与修正。Negative 只交七大類或一個綠測試摘要不足。Unknown 缺 selected execution envelope 時維持交接提案，不啟動替代 session。Replay 保留 stable IDs，交接不消耗或重設修正 budget。邊界 prompt 交接不是 session 隔離／admission 的證據。回滾 退回上版 handoff，不覆寫原 execution envelope。Execution UNTESTED。

關聯為 implements REQ-handoff, depends_on REQ-coverage, depends_on REQ-spec-data, depends_on REQ-inner-loop, depends_on REQ-adapters。

<!-- CARD_META {"stable_id": "SPEC-handoff", "canonical_key": "SPEC|closed-loop|defines|handoff|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-handoff"}, {"relation": "depends_on", "target": "REQ-coverage"}, {"relation": "depends_on", "target": "REQ-spec-data"}, {"relation": "depends_on", "target": "REQ-inner-loop"}, {"relation": "depends_on", "target": "REQ-adapters"}]} -->

#### CARD-REQ-cost 正常執行記錄成本與可重用結果

正常執行記錄成本與可重用結果。分開 runtime、projection、模型、網路、測試、等待及人工決策；缺值 unknown，不重複加巢狀時間。 原要求 CL-04, CL-05, CL-06, CL-13。失敗反例為文件長度／tool call／duration 不能推導決策減少或效益。

關聯為 implements REQ-cost, validated_by SPEC-cost。

<!-- CARD_META {"stable_id": "CARD-REQ-cost", "canonical_key": "REQ|closed-loop|defines|cost|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-cost"}, {"relation": "validated_by", "target": "SPEC-cost"}]} -->

#### SPEC-cost 正常執行記錄成本與可重用結果

Given 正常事件有來源和可用量測。When 收集一個小迴圈的结果。Then 分開 runtime、projection、模型、網路、測試、等待及人工決策；缺值 unknown，不重複加巢狀時間。Negative 文件長度／tool call／duration 不能推導決策減少或效益。Unknown 無量測本身不觸發 benchmark／修復。Replay 同一 log 重用，不為填報重跑原工作。邊界 成本 review 不替代行為／交付验收。回滾 修正錯算摘要，保留原 logs。Execution UNTESTED。

關聯為 implements REQ-cost, depends_on REQ-manager-feedback。

<!-- CARD_META {"stable_id": "SPEC-cost", "canonical_key": "SPEC|closed-loop|defines|cost|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-cost"}, {"relation": "depends_on", "target": "REQ-manager-feedback"}]} -->

#### CARD-REQ-publication PR 合併與規格狀態分開

PR 合併與規格狀態分開。建立具體 PR、綁 exact head、確認必要 checks、merge main 並讀回 provider main；只完成規格交付。 原要求 CL-01。失敗反例為新規格 merge 不把 runtime requirements 標 RELEASE_CONFIRMED。

關聯為 implements REQ-publication, validated_by SPEC-publication。

<!-- CARD_META {"stable_id": "CARD-REQ-publication", "canonical_key": "REQ|closed-loop|defines|publication|portable|v1", "series": "REQ", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-publication"}, {"relation": "validated_by", "target": "SPEC-publication"}]} -->

#### SPEC-publication PR 合併與規格狀態分開

Given 本次 artifact 已讀回、自審與有限檢查完成。When 使用者已授權此次 PR 合併。Then 建立具體 PR、綁 exact head、確認必要 checks、merge main 並讀回 provider main；只完成規格交付。Negative 新規格 merge 不把 runtime requirements 標 RELEASE_CONFIRMED。Unknown 舊 Draft scope 未指明時保留，不替其驗收缺口簽名。Replay merge outcome unknown 先 provider readback，不重複寫入。邊界 此需求只交付本次筆記與評估，不實作所有 Managers。回滾 如需回滾，以新 PR revert 規格提交。Execution UNTESTED。

關聯為 implements REQ-publication, depends_on REQ-handoff, depends_on REQ-compiler-audit。

<!-- CARD_META {"stable_id": "SPEC-publication", "canonical_key": "SPEC|closed-loop|defines|publication|portable|v1", "series": "SPEC", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "implements", "target": "REQ-publication"}, {"relation": "depends_on", "target": "REQ-handoff"}, {"relation": "depends_on", "target": "REQ-compiler-audit"}]} -->

### Batch 6

#### N-whole-task 小步成功後還有整份要求

小迴圈得到綠測試時，原 owner 只能更新該 REQ。外迴圈仍保留全部原要求。閉環要看下一個 consumer 是否採用結果及效果讀回，不能停在文字報告。

關聯為 based_on REQ-outer-loop, based_on REQ-completion。

<!-- CARD_META {"stable_id": "N-whole-task", "canonical_key": "N|closed-loop|explains|n-whole-task|portable|v1", "series": "N", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "based_on", "target": "REQ-outer-loop"}, {"relation": "based_on", "target": "REQ-completion"}]} -->

#### C-data-loop 資料閉環的定義

閉環由版本綁定事件開始，經必要 Manager 判定與原 owner 執行，再以實際讀回改變同一需求狀態。Schema 驗證只支持資料形狀。沒有事件接線、消費紀錄或效果證據，就缺一段閉環。

關聯為 based_on REQ-events, based_on REQ-consumption。

<!-- CARD_META {"stable_id": "C-data-loop", "canonical_key": "C|closed-loop|explains|c-data-loop|portable|v1", "series": "C", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "based_on", "target": "REQ-events"}, {"relation": "based_on", "target": "REQ-consumption"}]} -->

#### R-delivery-order 逐步實作順序

先固定意圖、完整需求與 SPEC，再補 adapter 字段能力。第二步接 event 到 Schema／Test。第三步證明 Hook／Cron 的 native binding。最後驗收 Manager feedback、owner consumption 與整份 stopping point。每步只聲稱所驗範圍。

關聯為 based_on REQ-handoff, based_on REQ-completion。

<!-- CARD_META {"stable_id": "R-delivery-order", "canonical_key": "R|closed-loop|explains|r-delivery-order|portable|v1", "series": "R", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "based_on", "target": "REQ-handoff"}, {"relation": "based_on", "target": "REQ-completion"}]} -->

#### T-architecture-choice 三個調整方案

維持 v7.2 原文只補 prose 能交接人讀資訊，不能約束事件資料。改成 compiler 執行所有 Manager 會新增第二個 scheduler 並改權限。選相容 sidecar profile，保存 typed contracts 與觸發規則，效果仍由原 owner。這是設計判斷，沒有行為因果優勢的比較證據。

關聯為 based_on REQ-compiler-audit, based_on REQ-adapters。

<!-- CARD_META {"stable_id": "T-architecture-choice", "canonical_key": "T|closed-loop|explains|t-architecture-choice|portable|v1", "series": "T", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "based_on", "target": "REQ-compiler-audit"}, {"relation": "based_on", "target": "REQ-adapters"}]} -->

#### V-runtime-gap 目前 runtime 驗收仍未執行

本次驗證卡片資料及有限指引消費。真實 Noodle admission／execute、原生 Hook／Cron、四 Manager 自動触發與 whole-task effect readback 均 NOT_RUN。候選說明或 schema 合法不能解除這些缺口。

關聯為 based_on REQ-eval-evidence, based_on REQ-completion。

<!-- CARD_META {"stable_id": "V-runtime-gap", "canonical_key": "V|closed-loop|explains|v-runtime-gap|portable|v1", "series": "V", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "based_on", "target": "REQ-eval-evidence"}, {"relation": "based_on", "target": "REQ-completion"}]} -->

#### X-no-managers 「没有功能」需要縮限

原主張是 Data 驅動沒有自動觸發四 Manager。前提可能把未驗收當成未實作。來源審閱顯示部分入口與 feedback 已存在，但沒有本次 exact-task 的 native execution 證據。支持結論是整條自動接續未證明；先查 producer 與接線，不能重建全部 Managers。

關聯為 based_on REQ-events, based_on REQ-manager-feedback。

<!-- CARD_META {"stable_id": "X-no-managers", "canonical_key": "X|closed-loop|explains|x-no-managers|portable|v1", "series": "X", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "based_on", "target": "REQ-events"}, {"relation": "based_on", "target": "REQ-manager-feedback"}]} -->

#### K-native-bindings 查明原生接線與選定身份

缺 selected execution envelope、native hook／cron binding、四 Manager input adapters 及效果 owner readback。先由原 producer 查 source／normal logs，只有來源不能回答的行为才取 fresh observation。已知規格工作可繼續。

關聯為 based_on REQ-hook, based_on REQ-cron, based_on REQ-adapters。

<!-- CARD_META {"stable_id": "K-native-bindings", "canonical_key": "K|closed-loop|explains|k-native-bindings|portable|v1", "series": "K", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "based_on", "target": "REQ-hook"}, {"relation": "based_on", "target": "REQ-cron"}, {"relation": "based_on", "target": "REQ-adapters"}]} -->

#### K-legacy-v71 v7.1 全文未提供

可讀 v7.2 是 portable profile。其宣稱繼承的完整 v7.1 不在本來源。只按 annex 所列不變量審閱，不宣稱 I-01..16 與 QG-01..34 全部語義已機械驗證。必要時由 compiler owner 供給原文。

關聯為 based_on REQ-compiler-audit。

<!-- CARD_META {"stable_id": "K-legacy-v71", "canonical_key": "K|closed-loop|explains|k-legacy-v71|portable|v1", "series": "K", "revision": 1, "status": "ACTIVE", "evidence_ids": ["SRC-TASK", "SRC-V72"], "typed_links": [{"relation": "based_on", "target": "REQ-compiler-audit"}]} -->
