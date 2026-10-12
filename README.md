# factoryweaver

[Zettelkasten v7.2 閉環規格卡片盒](docs/closed-loop-v72/README.md)包含完整需求交接、Soodles／Noodle 內外迴圈、Thinking Router／Ponytail、四個 Manager 的資料觸發提案，以及有限 eval 審計。

目前交付是規格。資料合法和文件合併不代表 runtime 自動閉環已啟用。

## v7.2 統一入口：`factoryweaver` Skill

日常產生、更新或驗證規格時，只需呼叫 **[`factoryweaver` 入口 Skill](skills/factoryweaver/SKILL.md)**，不必自行選擇 `factoryweaver-compile`／`factoryweaver-verify`。

這個入口會**先讀 [v7.2 System Prompt](references/zettelkasten-v7.2.md)** 作為編譯規則；當任務選定 Soodles Host 時，再讀 [Goal-oriented Scope / Skill Trigger Profile](docs/soodles-scope-routing.md)。它統一管理 Boot、Drill-down、Thinking Router（按需）、規格驗證與語義續傳。它不新增 Agent、Scheduler 或 GitHub 執行權限。

可以對支援 Agent Skills 的 Host 提出這類需求：

> 使用 `factoryweaver` Skill，把這份需求編譯成 v7.2 規格卡片盒。先 Boot，之後用 Drill-down Patch 無損續傳；每批四個顯示槽位；每個 Behavior Scope 包含 Goal、Measurement、Persistence、Stop/Escalation，明確列出 Soodles Outer Loop Skills 與 Noodle Poteto Inner Loop 的條列式 Prompt Delta。

要延續先前任務：

> 使用 `factoryweaver` Skill，消費上一批**已接受**的卡片與剩餘義務，僅更新必要的 Scope／約束／知識連接／Prompt Delta；無有效變更就回 NOOP。

**入口分工：** `factoryweaver` 是唯一建議對話入口；`factoryweaver-compile`、`factoryweaver-verify` 是被它選用的 leaf skills。實際修改 Repository、Issue Contract admission、PR delivery、Runtime Measurement 依然由原 Host/Owner 執行。Prompt 與卡片只含語義，不手工產生 Hash、Digest、Cursor、Execution ID、Git HEAD 或命令參數。

## Stanford CS329Z full-course knowledge collection

[Stanford CS329Z Course Master Card Box](docs/courses/cs329z-fall-2026/MASTER-CARD-BOX.md) combines all 11 weekly chapters. [Each chapter's Slides, Readings, Homework and Integrated Cards](docs/courses/cs329z-fall-2026/README.md) are separately navigable and source-status aware. The syllabus catalog is not proof of full-slide/article ingestion.

## 可執行的規格驗證

純讀取 CLI 可驗證、投影、路由提案及渲染卡片。它不執行 Host actions。原 owner 仍負責 admission、執行與效果回讀。

```sh
python3 -m pip install 'jsonschema>=4.20,<5'
python3 scripts/factoryweaver.py validate docs/closed-loop-v72/project.json
python3 scripts/factoryweaver.py project docs/closed-loop-v72/project.json
python3 scripts/factoryweaver.py cards docs/closed-loop-v72/project.json
python3 -m unittest discover -s tests -v
```

[相容性與證據邊界](docs/compatibility.md)區分本地契約驗證與真實 Host integration。對外文章與工程規格使用 [AGENTS.md](AGENTS.md) 的既有寫作路由。

## 增量知識編譯

[Card delta 契約](docs/card-delta-contract.md)定義 stable ID／revision、history、最多 12 卡的分批輸出及綁定原始 bytes 的 cursor。

```sh
python3 scripts/card_delta.py docs/closed-loop-v72/project.json docs/closed-loop-v72/project.json
```

相同資料產生 `NOOP`。修改後輸入產生唯讀 patch 與依賴失效建議；`DONE` 僅表示本輪編譯完成。owner acceptance、runtime effect 和 publication／landing 仍由原 owner 驗收。[本單元 manifest](docs/closed-loop-v72/delta-unit.json)保存有限交付範圍；原 30 REQ 與尚缺的 native Manager readback 繼續保留。
