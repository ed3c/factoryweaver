# factoryweaver

[Zettelkasten v7.2 閉環規格卡片盒](docs/closed-loop-v72/README.md)包含完整需求交接、Soodles／Noodle 內外迴圈、Thinking Router／Ponytail、四個 Manager 的資料觸發提案，以及有限 eval 審計。

目前交付是規格。資料合法和文件合併不代表 runtime 自動閉環已啟用。

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
