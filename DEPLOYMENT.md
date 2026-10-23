# 部署紀錄

2026-10-23：公開儲存庫與 Cloudflare Pages Git 連接已完成，首次部署成功。網站目前為準備頁，古羅馬城鎮尚未交付。

## 位置

- GitHub：https://github.com/yangchijung/roman-town
- 正式網址：https://roman-town.pages.dev
- Cloudflare Pages 專案：roman-town
- 首次固定部署：https://4f1f5fad.roman-town.pages.dev
- 首次部署 ID：4f1f5fad-f59e-44bb-93a5-38c586c5ca6c
- 首次部署 commit：f419069344238b059c5199efa57bcccacc520878

## 已設定

| 項目 | 設定 |
|---|---|
| Git source | yangchijung/roman-town |
| Production branch | main |
| Automatic deployments | Enabled |
| Framework preset | None |
| Build command | exit 0 |
| Build output directory | public |
| Root directory | 儲存庫根目錄 |
| 自訂網域 | 尚未設定；先使用 pages.dev |
| 環境變數／API key | 不需要，未新增 |

## 實際驗證

- Cloudflare 顯示首次部署成功，來源 commit 與預期一致。
- 控制台顯示「Automatic deployments enabled」，Git source 為本儲存庫。
- 正式網址回傳 HTTP 200。
- 正式網址 HTML 與 public/index.html 的提交內容完全相同。
- 瀏覽器實際顯示「古羅馬城鎮／地圖準備中」，專案連結指向本儲存庫。

更新 public/ 後提交 main 即會觸發部署。若未來引入 Vite／npm 等建置工具，須同時調整 Pages build/output 設定。

依據：[Cloudflare 靜態 HTML 部署](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/)、[GitHub 自動部署整合](https://developers.cloudflare.com/pages/configuration/git-integration/github-integration/)。
