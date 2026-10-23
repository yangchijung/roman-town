# Roma Aeterna AD 128 — 公元 128 年古羅馬 1:1 3D 歷史考證引擎

- **正式線上網址 (Cloudflare Pages)**：<https://roman-town.pages.dev>
- **GitHub 儲存庫**：<https://github.com/yangchijung/roman-town>
- **歷史斷代**：嚴格鎖定於**公元 128 年（哈德良皇帝時期）**，所有建築年代均 `≤ 128 AD`，模型與考古參考尺寸誤差 `0.00% (≤ 5%)`。

## 專案結構與直接執行入口

本儲存庫採用零建置依賴（`Framework preset: None`、`Build command: exit 0`、`Build output directory: public`）之標準靜態部署架構，更新 `main` 分支後由 Cloudflare Pages 自動部署：

- `public/index.html`：**主程式入口（P1–P4 完整整合版）**，涵蓋七丘與維利亞丘古代 DEM 地形、古台伯河與 7 座橋樑、14 行政區與聖界、玄武岩道路網、660 棟程序化城市紋理、**100% 歷史地標建築群（69 座核心複合體）**、**10 條輸水道與配水塔/公共噴泉**，以及 **6 座無縫室內外進入傳送門**（萬神殿、競技場、圖拉真市場、圖拉真浴場、卡比托利歐 5 層公寓、帕拉提諾豪宅）。
- `public/p1.html`：P1 地形、水系、7 座橋樑與 14 行政區獨立檢視器。
- `public/p2.html`：P2 玄武岩道路網與 660 棟程序化城市紋理獨立檢視器。
- `public/p3.html`：P3 地標第一批（羅馬廣場、帝國議事廣場、圖拉真廣場、競技場、萬神殿、維納斯與羅馬神廟工地）檢視器。
- `public/p4.html`：P4 地標第二批與 10 條輸水道完整版檢視器。
- `public/data/`：`p1_world_data.json` 至 `p4_world_data.json` 結構化考證資料庫。
- `public/screenshots/`：`p1/`、`p2/`、`p3/`、`p4/` 各階段固定檢驗機位渲染截圖（共 32 張 PNG）。
- `docs/P0_Ancient_Rome_128AD_Master_Plan.md`：P0 完整考證規劃書與 101 項地標尺寸對照表。
- `tools/` 與 `tests/`：P1–P4 資料建置腳本與自動化驗證腳本。
