# 給 Gemini：Roman Town 存放與部署

## 任務

在此儲存庫製作可進去逛的古羅馬城鎮地圖。GitHub 位址：https://github.com/yangchijung/roman-town 。目前只有部署準備頁，尚未有地圖成品。

## 目前接入方式

1. 以完整可執行網站替換 `public/index.html`。
2. JavaScript、CSS、模型、貼圖與音效放在 `public/` 內；大型資源可歸在 `public/assets/`。
3. 網站檔案使用相對或網站根目錄路徑，不使用電腦本機路徑。不要把 Markdown 程式碼框當成檔案內容。
4. 目前 Pages 不執行編譯：preset None、build `exit 0`、output `public`、正式分支 `main`。Git 連接和網址見 DEPLOYMENT.md。
5. 若需要 Vite／npm，先建立完整可重現的建置專案並同步調整 Pages 設定，再提交；不要留下只有 import 裸套件名稱、瀏覽器無法執行的程式。
6. 如果 Gemini 目前沒有 GitHub 寫入能力，請交付完整檔案 ZIP，由使用者或已授權的工程工具上傳；不要宣稱僅貼程式碼就已自動上傳。
7. 不需要新增登入、付費、API key 或後端即可完成第一版城鎮瀏覽。

## 交付證據

- 電腦可以進入並移動，手機／平板有可用的觸控操作。
- 模型與貼圖實際載入；缺少資源、WebGL 不支援時有可理解的提示。
- 提供操作方式、實際截圖、目前已做與未做的範圍。
- 歷史考據與想像重建分別說明；不要把想像建築標成已證實的復原。
- 地圖、模型、貼圖、字體與音效列出來源與授權，不放私密資料。
- 網站可用後再移除準備頁的 noindex 設定。
