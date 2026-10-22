# 本次需求來源分解

本頁是原使用者要求的編輯分解，原文保存在私有任務 evidence。它保留來源片語及設計範圍，不證明語義無漏項，也不是獨立人類確認 receipt。CL-06 的「沒有功能」是待查現況主張；其要求的未來結果仍須保留。

## CL-01

來源片語「merge main」。

要求結果為合併本次可驗收成果。

## CL-02

來源片語「用 Zettelkasten Specification Compiler v7.2」。

要求結果為使用 v7.2 卡片契約。

## CL-03

來源片語「按照 soodles thinking router & schema manager 產生需求」。

要求結果為意圖路由與證據投影交接。

## CL-04

來源片語「閉環資料流」。

要求結果為資料必須回到原需求與 owner。

## CL-05

來源片語「小迴圈執行常常無法驗收到真的 data 驅動閉環」。

要求結果為區分局部 PASS 與整份完成。

## CL-06

來源片語「Data 驅動沒有自動觸發 schema, test, hook, cron job manager 的功能」。

要求結果為規定四個 Manager 的事件觸發與消費。

## CL-07

來源片語「生成規格的卡片盒筆記」。

要求結果為交付可讀與可交換筆記。

## CL-08

來源片語「必須能交接 noodle poteto mode 小迴圈按照不遺漏的需求條列並解決已知需求」。

要求結果為完整需求與小步執行交接。

## CL-09

來源片語「未知的部分可以直接擴展」。

要求結果為可增加未知與最小調查。

## CL-10

來源片語「錯誤推論或是需要更新事實也直接改」。

要求結果為直接修正與失效傳播。

## CL-11

來源片語「必須結合規格驅動開發與 schema data 驅動開發」。

要求結果為規格與資料雙向一致。

## CL-12

來源片語「用 evals skills 評估Zettelkasten Specification Compiler v7.2」。

要求結果為來源審計與有限行為評估。

## CL-13

來源片語「soodles outer loop + noodle poteto mode inner loop」。

要求結果為保留內外迴圈職責。

## CL-14

來源片語「需要考慮 thinking router & ponytail」。

要求結果為路由與最小完整解審查。

## CL-15 — Human Intent, one Session Outer ↔ Inner

本對話原始要求：「outer loop 的 thinking route 與 inner loop 的 poteto mode 在 Session 中交互完成工程判斷……並循環驅動來完成人類意圖與factoryweaver規格卡片」。

要求結果：同一 Soodles Supervising Session 保留原 Parent Goal，僅於原 Source／Owner 證據存在真正未決問題時選 Thinking V2／條件式 V3 × Ambitious。原合法 next 直接消費。Inner 已准入 Noodle Stage 自主實作、回填真實候選與失敗證據，原 Owner 核對後再決定下個合法工作單元。

## CL-16 — Known／Unknown and earliest causality

本對話原始要求：「已知未知的軟體架構設計」。

要求結果：將目前情形辨為合法已知續行、Implementation Defect、已被原 Source／Native Consumer 推翻的 Specification／Oracle、具名必要未知、未知外部效果或真正未決 Architecture；不同種類交由各自原 Producer，缺實際觀察時保留 UNKNOWN。

## CL-17 — FactoryWeaver v7.2 Card Revision boundary

本對話原始要求：「factoryweaver規格卡片」；延續同一對話確認的 Card-generation Feedback、最小 Prompt Delta、Typed Links、Source-bound Revision History。

要求結果：同一 Registry／stable ID 上增量修正真的錯誤卡片；Card-generation 回到原 FactoryWeaver Producer，Worker Prompt Delta 只作被授權的下一個未凍結 Stage 需要的增量。不能為了通過實作測試而改寫正確 SPEC。

## CL-18 — Full cross-repository obligations, separate owners

本對話已確定「完整 Google Harness² × NeoWeaver × pstack Formal Verification」，包含所有 INT／HOF 決策與 A01–A20 正反驗證要求。原始 Soodles Handoff 見 [PR #445](https://github.com/ed3c/soodles/pull/445)；詳細 Source Coverage 見 [本次附錄](intent-to-acceptance-coverage.md)。

要求結果：本次不重編 NeoWeaver 原 10 REQ／44 Cards，也不在公開 FactoryWeaver 保存私有 Native Trace；保留完整外部 Parent Obligation 並單獨讀回原 Owner 實際證據。

## CL-19 — Approved FCL delivery contract

本次使用者已確認：「FCL-01 A、FCL-02 A、FCL-03 A」。

要求結果：保留完整對話分層驗收；FactoryWeaver 原 Closed-loop v7.2 Registry 擁有本次 Card Revision；完成 Source Coverage、Typed Links、Scope／Prompt Delta、Acceptance 與文件 PR。產品 Runtime／Harness² Model-backed／正式 Promotion 不在本次授權內。

## CL-20 — MGP approved Source-to-Consumer parity scope

本次使用者已確認：「MGP-01 A、MGP-02 B」。

要求結果：Portable v7.2 System Prompt 引入條件式 Source-to-Consumer Semantic Parity 和 Reuse-before-Rewrite，不讓所有 Card 強制走 AST／Codemod／Browser／Noodle Migration；僅修改實際受影響的 per-type Card Prompt、Owner Reference、原 Registry Revision 與驗證。原 Soodles migrate-class 為具名專案方法，不是每次編譯的新 Router、CLI 狀態或效果權限。

## CL-21 — Fresh Native Consumer versus Source-only proof

本次使用者已確認：「MGP-03 B」。

要求結果：分別觀察 Source Identity、Matched Consumer Behavior Parity、Independent Semantic Correctness、Native Host/Agent/Provider Acceptance，設計舊版／新版 Prompt 正反案例。只在原 Host／訂閱登入與原 Owner 合法可用時執行真實 Native Consumer Evals；沒有實際 Session/Attempt/Observer/Provider 收據時保持 NOT_RUN 或 BLOCKED，不能用 GitHub CI、靜態 AST、金標 Fixture 或字句相似度冒充通用語義改善。
