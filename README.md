# Roman Town｜古羅馬城鎮

可步行探索的古羅馬城鎮地圖。地圖由 Gemini 製作；目前先建立儲存庫、靜態網站目錄與部署準備頁，城鎮內容尚未交付。

## 專案位置

- GitHub：https://github.com/yangchijung/roman-town
- 正式網站：https://roman-town.pages.dev
- 部署紀錄：[DEPLOYMENT.md](DEPLOYMENT.md)
- 給 Gemini：[GEMINI_HANDOFF.md](GEMINI_HANDOFF.md)

## 目前結構

```text
public/
  index.html       網站入口；以可玩的城鎮取代準備頁
  assets/
    .gitkeep       放模型、貼圖、音效等靜態資源
GEMINI_HANDOFF.md   開發接入說明
DEPLOYMENT.md       Pages 設定與驗證紀錄
```

目前採不需建置的 HTML／CSS／JavaScript 靜態網站，沒有指定 3D 引擎；Gemini 可依地圖設計選擇合適的瀏覽器技術。

## 本機預覽

在儲存庫根目錄執行 `python3 -m http.server 8000 --directory public`，開啟 http://localhost:8000 。

## Cloudflare Pages 設定

| 項目 | 值 |
|---|---|
| Git 儲存庫 | yangchijung/roman-town |
| 正式分支 | main |
| Framework preset | None |
| Build command | exit 0 |
| Build output directory | public |
| Root directory | 儲存庫根目錄 |

設定依據：[Cloudflare 靜態 HTML 文件](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/)。
已連接 Cloudflare Pages，正式分支為 main，自動部署已啟用。main 更新後會觸發正式部署；預覽與正式部署紀錄可在 Pages 控制台查看。

若改用 Vite／npm，請同時提交 package.json、lockfile、實際可成功的 build script，並把 Pages 建置命令與輸出目錄改成對應值；不要只提交原始 TypeScript 而沿用 exit 0。

## 資源與公開資料

這是公開儲存庫。只提交專案可公開的檔案，不提交 API key、密碼、.env、node_modules 或個人檔案。模型／貼圖／音效須記錄來源與授權。網站不需要 Gemini API key 即可瀏覽。
