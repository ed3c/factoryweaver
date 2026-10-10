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
