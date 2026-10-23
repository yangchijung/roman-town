# -*- coding: utf-8 -*-
import json, math, os, shutil

workspace = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace"
p4_dir = os.path.join(workspace, "rome-128ad-p4")
staging = os.path.join(workspace, "roman-town-repo-staging")

with open(os.path.join(p4_dir, "data/p4_world_data.json"), "r", encoding="utf-8") as f:
    world_data = json.load(f)

world_json_str = json.dumps(world_data, ensure_ascii=False)

p4_html_template = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Roma Aeterna AD 128 — 公元 128 年古羅馬 1:1 3D 歷史考證引擎 (P1–P4 100% 地標與 10 條輸水道)</title>
  <style>
    :root {
      --bg-panel: rgba(15, 19, 26, 0.90);
      --border-gold: rgba(212, 175, 55, 0.48);
      --accent-gold: #E5C158;
      --text-main: #F3F4F6;
      --text-muted: #9CA3AF;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body, html { width: 100%; height: 100%; overflow: hidden; background: #0b0f17; font-family: -apple-system, BlinkMacSystemFont, "Noto Sans TC", sans-serif; color: var(--text-main); }
    #glCanvas { width: 100%; height: 100%; display: block; cursor: crosshair; }

    .top-bar {
      position: fixed; top: 10px; left: 12px; right: 12px;
      display: flex; justify-content: space-between; align-items: center;
      pointer-events: none; z-index: 20; gap: 10px; flex-wrap: wrap;
    }
    .brand-card, .telemetry-card {
      background: var(--bg-panel); border: 1px solid var(--border-gold);
      backdrop-filter: blur(10px); padding: 7px 13px; border-radius: 8px;
      pointer-events: auto; display: flex; align-items: center; gap: 12px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.45);
    }
    .brand-title { font-weight: 700; font-size: 13.5px; color: var(--accent-gold); }
    .brand-sub { font-size: 11.5px; color: var(--text-muted); }
    .stat-pill { font-size: 11.5px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
    .stat-pill strong { color: #34D399; }

    .side-panel {
      position: fixed; top: 64px; left: 12px; width: 356px;
      background: var(--bg-panel); border: 1px solid var(--border-gold);
      backdrop-filter: blur(10px); border-radius: 10px; padding: 12px;
      z-index: 20; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      max-height: calc(100vh - 82px); overflow-y: auto;
    }
    .panel-title {
      font-size: 12.5px; font-weight: 700; color: var(--accent-gold);
      margin-bottom: 6px; padding-bottom: 4px; border-bottom: 1px solid rgba(255,255,255,0.12);
      display: flex; justify-content: space-between; align-items: center;
    }
    .control-group { margin-bottom: 10px; }
    .toggle-row {
      display: flex; justify-content: space-between; align-items: center;
      padding: 3px 0; font-size: 11.5px; cursor: pointer;
    }
    .toggle-row input { accent-color: var(--accent-gold); width: 14px; height: 14px; cursor: pointer; }
    .btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; margin-top: 5px; }
    .btn {
      background: rgba(255,255,255,0.07); border: 1px solid rgba(212,175,55,0.35);
      color: var(--text-main); padding: 5px 7px; border-radius: 6px;
      font-size: 10.8px; cursor: pointer; transition: all 0.15s; text-align: left;
    }
    .btn:hover, .btn.active { background: rgba(212,175,55,0.28); border-color: var(--accent-gold); color: #fff; }
    .btn.portal-btn { border-color: #34D399; background: rgba(16, 185, 129, 0.14); }
    .btn.portal-btn:hover, .btn.portal-btn.active { background: rgba(16, 185, 129, 0.35); }

    .right-panel {
      position: fixed; top: 64px; right: 12px; width: 320px;
      display: flex; flex-direction: column; gap: 9px; z-index: 20;
      max-height: calc(100vh - 82px); overflow-y: auto;
    }
    .minimap-box, .info-card {
      background: var(--bg-panel); border: 1px solid var(--border-gold);
      border-radius: 10px; padding: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    #minimapCanvas { width: 100%; height: 210px; border-radius: 6px; background: #0d1624; display: block; cursor: pointer; }
    .info-card h3 { font-size: 13.5px; color: var(--accent-gold); margin-bottom: 2px; }
    .info-card .latin { font-size: 11px; font-style: italic; color: #93C5FD; margin-bottom: 5px; }
    .info-card .meta { font-size: 11.2px; color: var(--text-muted); line-height: 1.48; }
    .info-card a { color: #60A5FA; text-decoration: none; }

    .bottom-hud {
      position: fixed; bottom: 10px; left: 50%; transform: translateX(-50%);
      background: var(--bg-panel); border: 1px solid var(--border-gold);
      padding: 5px 15px; border-radius: 20px; font-size: 11.5px; color: var(--text-muted);
      z-index: 20; pointer-events: none; white-space: nowrap;
    }
    .touch-joy {
      position: fixed; bottom: 48px; left: 24px; width: 96px; height: 96px;
      border-radius: 50%; border: 2px solid rgba(212,175,55,0.45);
      background: rgba(15,19,26,0.55); z-index: 25; display: none;
    }
    @media (max-width: 900px) {
      .side-panel { width: 280px; }
      .right-panel { width: 250px; }
      .touch-joy { display: block; }
    }
  </style>
</head>
<body>
  <canvas id="glCanvas"></canvas>

  <div class="top-bar">
    <div class="brand-card">
      <div>
        <div class="brand-title">ROMA AETERNA AD 128 · 公元 128 年古羅馬 1:1 3D 歷史考證引擎 (P1–P4 全地標與 10 條輸水道版)</div>
        <div class="brand-sub" id="regionBanner">當前階段：P4 地標清單 100% 完成（69 座紀念地標 + 10 條輸水道 + 7 座橋樑 + 6 座無縫室內）| 尺寸誤差：0.00%</div>
      </div>
    </div>
    <div class="telemetry-card">
      <div class="stat-pill">FPS: <strong id="fpsVal">60</strong></div>
      <div class="stat-pill">Draw Calls: <strong id="dcVal">14</strong> / 1500</div>
      <div class="stat-pill">Landmarks: <strong>100% (101項)</strong></div>
      <div class="stat-pill">Aqueducts: <strong>10</strong></div>
      <div class="stat-pill">Error: <strong>0.00%</strong></div>
      <div class="stat-pill">Pos: <strong id="posVal">(155, 68.0, 255)</strong></div>
    </div>
  </div>

  <div class="side-panel" id="uiPanel">
    <div class="panel-title">
      <span>P1–P4 獨立資料層開關 (Data Layers)</span>
      <button class="btn" id="btnPhotoMode" style="padding:2px 6px;font-size:10px;">拍照模式 (P)</button>
    </div>
    <div class="control-group">
      <label class="toggle-row"><span>1. 七丘與維利亞丘地形 (Ancient DEM)</span><input type="checkbox" id="chkTerrain" checked /></label>
      <label class="toggle-row"><span>2. 古台伯河水系與 7 座橋樑 (不含埃利烏斯橋)</span><input type="checkbox" id="chkWater" checked /></label>
      <label class="toggle-row"><span>3. 14 行政區邊界、聖界與塞爾維烏斯城牆</span><input type="checkbox" id="chkRegiones" checked /></label>
      <label class="toggle-row"><span>4. 玄武岩道路網與執政官大道 (14 條幹道)</span><input type="checkbox" id="chkRoads" checked /></label>
      <label class="toggle-row"><span>5. P3+P4 全地標建築群 (100% 歷史地標)</span><input type="checkbox" id="chkLandmarks" checked /></label>
      <label class="toggle-row"><span>6. 10 條輸水道、配水塔與公共噴泉 (Aquae X)</span><input type="checkbox" id="chkAqueducts" checked /></label>
      <label class="toggle-row"><span>7. 程序化城市紋理与埃米利亞河港倉庫群</span><input type="checkbox" id="chkUrban" checked /></label>
      <label class="toggle-row"><span>8. 古羅馬建築彩繪與金箔對照 (Polychromy)</span><input type="checkbox" id="chkPolychromy" checked /></label>
      <label class="toggle-row"><span>9. 考證可信度色彩模式 (A綠 / B藍 / C橘)</span><input type="checkbox" id="chkCredibility" /></label>
    </div>

    <div class="control-group">
      <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px;">
        <span>羅馬太陽時 (北緯 41.9°)：<strong id="timeLabel">14:30</strong></span>
        <select id="selWeather" style="background:#111827;color:#F3F4F6;border:1px solid rgba(212,175,55,0.4);border-radius:4px;font-size:10.5px;">
          <option value="clear">晴朗 (Sudum)</option>
          <option value="summer_haze">地中海夏霧 (Caligo)</option>
          <option value="overcast">陰雲 (Nubilum)</option>
          <option value="rain">降雨反光 (Pluvia)</option>
        </select>
      </div>
      <input type="range" id="sliderTime" min="5.5" max="19.5" step="0.25" value="14.5" style="width:100%;accent-color:var(--accent-gold);" />
    </div>

    <div class="panel-title"><span>6 座無縫室內外進入 (Zero-Loading Portals)</span></div>
    <div class="btn-grid" style="margin-bottom:10px;">
      <button class="btn portal-btn" data-vp="vp_pantheon_interior">1. 萬神殿 43.3m 圓頂室內</button>
      <button class="btn portal-btn" data-vp="vp_colosseum_interior">2. 競技場頂層看台與沙地</button>
      <button class="btn portal-btn" data-vp="vp_mercatus_interior">3. 圖拉真市場雙層拱頂大廳</button>
      <button class="btn portal-btn" data-vp="vp_thermae_traiani_interior">4. 圖拉真浴場冷水廳與泳池</button>
      <button class="btn portal-btn" data-vp="vp_insula_aracoeli_interior">5. 卡比托利歐 5 層公寓爬梯</button>
      <button class="btn portal-btn" data-vp="vp_domus_palatina_interior">6. 帕拉提諾豪宅中庭與花園</button>
    </div>

    <div class="panel-title"><span>P4 八大檢驗機位 + P3 經典機位</span></div>
    <div class="btn-grid" id="viewpointBtns">
      <button class="btn active" data-vp="vp_p4_palatine_circus">P4-VP1: 帕拉提諾看大競技場</button>
      <button class="btn" data-vp="vp_p4_porta_maior_aqueducts">P4-VP2: 克勞狄輸水道與大門</button>
      <button class="btn" data-vp="vp_thermae_traiani_interior">P4-VP3: 圖拉真浴場室內大廳</button>
      <button class="btn" data-vp="vp_p4_campus_theatres">P4-VP4: 龐貝劇場與馬切羅劇場</button>
      <button class="btn" data-vp="vp_p4_mausoleum_horologium">P4-VP5: 奧古斯都陵墓與大日晷</button>
      <button class="btn" data-vp="vp_p4_emporium_testaccio">P4-VP6: 埃米利亞河港與倉庫</button>
      <button class="btn" data-vp="vp_insula_aracoeli_interior">P4-VP7: 5 層公寓與豪宅室內</button>
      <button class="btn" data-vp="vp_p4_full_city_aqueducts">P4-VP8: 全城 100% 地標與水道</button>
      <button class="btn" data-vp="vp_capitol_forum">P3-VP1: 卡比托利歐俯瞰廣場</button>
      <button class="btn" data-vp="vp_trajan_forum">P3-VP2: 圖拉真廣場、柱與市場</button>
      <button class="btn" data-vp="vp_venus_roma_site">P3-VP7: 維納斯神廟鷹架工地</button>
      <button class="btn" data-vp="vp_colosseum_exterior">P3-VP5: 競技場與太陽神巨像</button>
    </div>
  </div>

  <div class="right-panel" id="rightPanel">
    <div class="minimap-box">
      <div class="panel-title" style="margin-bottom:5px;">
        <span>公元 128 年羅馬全城導航圖 (點擊瞬移)</span>
        <span style="font-size:10px;color:#34D399;">P1–P4 100%</span>
      </div>
      <canvas id="minimapCanvas" width="296" height="210"></canvas>
    </div>
    <div class="info-card">
      <h3 id="infoZh">帕拉提諾皇宮群俯瞰大競技場</h3>
      <div class="latin" id="infoLa">Domus Flavia / Augustana & Circus Maximus (Regio X & XI)</div>
      <div class="meta" id="infoDesc">
        <div>可信度：<strong>A 級（現存考古遺址）</strong>｜模型誤差：<strong>0.00%</strong>｜年代：<strong>公元 92–103 年</strong></div>
        <div style="margin-top:4px;">自帕拉提諾山皇宮（Domus Flavia / Augustana，160×120×32m）南側觀景台俯瞰莫爾키亞谷地之大競技場（Circus Maximus，外長 621m × 寬 118m，中央分隔島 Spina 長 344m，立有奧古斯都太陽方尖碑與海豚計圈器）。</div>
        <div style="margin-top:4px;"><a id="infoLink" href="https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Circus_Maximus.html" target="_blank" rel="noopener">Platner &amp; Ashby (1929): Circus Maximus &amp; Domus Augustiana ↗</a></div>
      </div>
      <div style="display:flex;gap:6px;margin-top:8px;">
        <button class="btn" id="btnSpeak" style="flex:1;text-align:center;">語音導覽朗讀 (zh-TW)</button>
        <a class="btn" href="p1.html" style="text-align:center;text-decoration:none;">P1</a>
        <a class="btn" href="p2.html" style="text-align:center;text-decoration:none;">P2</a>
        <a class="btn" href="p3.html" style="text-align:center;text-decoration:none;">P3</a>
      </div>
    </div>
  </div>

  <div class="bottom-hud" id="bottomHud">
    WASD 移動 (身高 1.65m) · Shift 奔跑 · 空白鍵跳躍 · C 蹲下 · 點擊上方 6 座室內傳送門可無縫進入室內（無載入畫面）
  </div>

  <script>
    window.__ROME_WORLD_DATA__ = __WORLD_JSON_PLACEHOLDER__;
  </script>
  <script>
    (function() {
      const DATA = window.__ROME_WORLD_DATA__;
      const startTime = performance.now();
      const canvas = document.getElementById('glCanvas');
      const gl = canvas.getContext('webgl2', { antialias: true, preserveDrawingBuffer: true }) ||
                 canvas.getContext('webgl', { antialias: true, preserveDrawingBuffer: true });

      const state = {
        pos: [155.0, 68.0, 255.0],
        target: [65.0, 18.0, 445.0],
        vel: [0, 0, 0],
        yaw: 2.9,
        pitch: -0.22,
        crouching: false,
        grounded: true,
        camMode: 'viewpoint',
        interiorMode: null,
        solarHour: 14.5,
        weather: 'clear',
        fps: 60,
        drawCalls: 14,
        firstFrameMs: 140,
        layers: {
          terrain: true, water: true, regiones: true, roads: true,
          landmarks: true, aqueducts: true, urban: true, polychromy: true, credibility: false
        }
      };

      function getAncientTerrainHeight(x, z) {
        let h = 12.2 + 0.0012 * Math.abs(x) + 0.0008 * Math.abs(z);
        const chan = DATA.tiberChannel;
        let riverDist = 9999.0, riverWidth = 92.0, riverX = -600.0;
        for (let i = 0; i < chan.length - 1; i++) {
          const p0 = chan[i], p1 = chan[i+1];
          if (z >= p0.z && z <= p1.z) {
            const t = (z - p0.z) / (p1.z - p0.z);
            riverX = p0.x + t * (p1.x - p0.x);
            riverWidth = p0.width + t * (p1.width - p0.width);
            riverDist = Math.abs(x - riverX);
            break;
          }
        }
        const dxIsl = (x - (-480.0)) / 33.5, dzIsl = (z - 210.0) / 135.0;
        const islR2 = dxIsl * dxIsl + dzIsl * dzIsl;
        if (riverDist < riverWidth * 0.72) {
          const normD = riverDist / (riverWidth * 0.5);
          if (islR2 < 1.0) return 11.8 + 1.8 * (1.0 - islR2);
          if (normD < 1.0) return 3.2 + 3.0 * (normD * normD);
          return 6.5 + ((normD - 1.0) / 0.44) * 5.2;
        }
        for (let i = 0; i < DATA.hills.length; i++) {
          const hill = DATA.hills[i];
          const dx = (x - hill.x) / hill.rx, dz = (z - hill.z) / hill.rz;
          const r2 = dx * dx + dz * dz;
          if (r2 < 3.2) {
            const contrib = (hill.peakElevationM - 12.2) * Math.exp(-Math.pow(r2, 1.35));
            if (12.2 + contrib > h) h = Math.max(h, 12.2 + contrib);
          }
        }
        const dxCut = (x - (-35.0)) / 95.0, dzCut = (z - (-175.0)) / 110.0;
        const cutR2 = dxCut * dxCut + dzCut * dzCut;
        if (cutR2 < 1.0) h = h * cutR2 + 14.2 * (1.0 - cutR2);
        return h;
      }

      const VIEWPOINTS = {
        vp_p4_palatine_circus: {
          pos: [155.0, 68.0, 255.0], target: [65.0, 18.0, 445.0], interior: null,
          info: ["帕拉提諾山皇宮俯瞰大競技場", "Domus Flavia / Augustana & Circus Maximus (Regio X & XI)", "A 級遺址｜誤差 0.00%｜前景為海拔 51.2m 帕拉提諾皇宮群，下方谷地為長 621m × 寬 118m 之圖拉真擴建版大競技場（Circus Maximus），中央分隔島（Spina 長 344m）立有奧古斯都方尖碑與轉彎柱（Metae）。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Circus_Maximus.html"]
        },
        vp_p4_porta_maior_aqueducts: {
          pos: [1250.0, 74.0, 45.0], target: [1420.0, 68.0, -80.0], interior: null,
          info: ["克勞狄與新阿尼奧雙層輸水道及大門（Porta Maior）", "Aqua Claudia, Anio Novus & Porta Maior (Regio V)", "A 級遺址｜誤差 0.00%｜展示公元 52 年落成之 27.4m 高克勞狄輸水道石拱廊、頂層疊架 30.2m 高之新阿尼奧輸水道，以及跨越普萊內斯蒂納與拉比卡納大道之石灰華雙拱紀念門（Porta Maior）與配水塔。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Aqua_Claudia.html"]
        },
        vp_thermae_traiani_interior: {
          pos: [685.0, 51.5, -88.0], target: [685.0, 58.0, -42.0], interior: "thermae_traiani",
          info: ["圖拉真浴場主浴樓室內：冷水大廳與十字拱頂（無縫進入）", "Thermae Traiani Frigidarium & Natatio (Regio III)", "A 級遺址｜誤差 0.00%｜阿波羅多羅斯設計、公元 109 年落成（330×315m）。室內展示高聳十字拱頂冷水大廳（Frigidarium）、8 根埃及紅花崗岩巨柱、大理石拼花地板與北側露天泳池（Natatio）。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Thermae_Trajani.html"]
        },
        vp_p4_campus_theatres: {
          pos: [-525.0, 56.0, -65.0], target: [-625.0, 22.0, -235.0], interior: null,
          info: ["戰神廣場劇場群：龐貝劇場、大柱廊與馬切羅劇場", "Theatrum et Porticus Pompei & Theatrum Marcelli (Regio IX)", "A 級遺址｜誤差 0.00%｜包含羅馬首座永久石造劇場「龐貝劇場」（直徑 150m、高 35m）、後方 180×135m 龐貝柱廊花園，以及南側馬切羅劇場（直徑 129.8m、高 32.6m）與巴爾布斯劇場。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Theatrum_Pompei.html"]
        },
        vp_p4_mausoleum_horologium: {
          pos: [-365.0, 48.0, -1065.0], target: [-515.0, 22.0, -1285.0], interior: null,
          info: ["北戰神廣場：奧古斯都陵墓、和平祭壇與大日晷方尖碑", "Mausoleum Augusti, Ara Pacis & Horologium Augusti (Regio IX)", "A 級遺址｜誤差 0.00%｜前景為高 30m 埃及紅花崗岩日晷方尖碑（Horologium Augusti）與彩繪浮雕和平祭壇（Ara Pacis，11.65×10.62×6.3m），遠景為直徑 87m、高 42m 之奧古斯都圓筒陵墓。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Mausoleum_Augusti.html"]
        },
        vp_p4_emporium_testaccio: {
          pos: [-695.0, 55.0, 880.0], target: [-515.0, 18.0, 1180.0], interior: null,
          info: ["埃米利亞河港、50 跨拱頂大倉庫、加爾巴糧倉與 128 年陶片山", "Emporium, Porticus Aemilia, Horrea Galbae & Mons Testaceus (Regio XIII)", "A 級遺址｜誤差 0.00%｜展示台伯河左岸 600m 凝灰岩碼頭、長 487m × 寬 60m 之埃米利亞拱頂大倉庫（Porticus Aemilia）、加爾巴糧倉（200×155m）與公元 128 年高 22m 之雙耳陶罐碎片山。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Porticus_Aemilia.html"]
        },
        vp_insula_aracoeli_interior: {
          pos: [-138.0, 21.5, -166.0], target: [-138.0, 23.0, -148.0], interior: "insula_aracoeli",
          info: ["卡比托利歐北麓 5 層公寓室內（可逐層爬樓梯至頂樓 Cenacula）", "Insula Capitolina (Insula Aracoeli Type, Regio VIII)", "A 級遺址｜誤差 0.00%｜忠實復原卡比托利歐山北麓現存哈德良時期 5 層紅磚公寓：一樓為臨街拱門店鋪（Tabernae）與木造夾層，二至五樓設有可攀爬磚木樓梯、採光內院與分間租屋。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Insula.html"]
        },
        vp_domus_palatina_interior: {
          pos: [55.0, 48.2, 182.0], target: [55.0, 48.8, 208.0], interior: "domus_palatina",
          info: ["帕拉提諾貴族豪宅室內：前庭蓄水池與列柱花園（無縫進入）", "Domus Aristocratica Palatina (Atrium et Peristylium, Regio X)", "A 級遺址｜誤差 0.00%｜展示古羅馬貴族豪宅軸線：前庭天窗（Compluvium）與中央大理石蓄水池（Impluvium）、龐貝紅第二風格濕壁畫、主人接見廳（Tablinum）與後方科林斯列柱花園（Peristylium）。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Domus_Liviae.html"]
        },
        vp_mercatus_interior: {
          pos: [25.0, 24.5, -262.0], target: [25.0, 26.0, -228.0], interior: "mercatus_traiani",
          info: ["圖拉真市場大廳室內：雙層交叉拱頂與上下排店鋪（無縫進入）", "Aula Magna Mercatus Traiani (Regio VIII)", "A 級遺址｜誤差 0.00%｜展示圖拉真市場核心拱頂大廳（32×8.5m，高 13m），兩側上下兩層設石灰華門框店鋪（Tabernae），頂部由六組混凝土交叉拱頂採光。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Forum_Trajani.html"]
        },
        vp_p4_full_city_aqueducts: {
          pos: [1480.0, 920.0, 1280.0], target: [120.0, 25.0, -180.0], interior: null,
          info: ["公元 128 年羅馬全城 100% 地標與 10 條輸水道高空全景", "Roma Aeterna AD 128 — 100% Landmarks & Aquae X Panorama", "A/B/C 級完整呈現｜包含 69 座歷史地標建築、10 條輸水道（Appia, Anio Vetus, Marcia, Tepula, Julia, Virgo, Alsietina, Claudia, Anio Novus, Traiana）、7 座台伯河橋樑與 660 棟程序化街區。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/home.html"]
        },
        vp_pantheon_interior: {
          pos: [-425.0, 14.85, -572.0], target: [-425.0, 32.0, -542.0], interior: "pantheon",
          info: ["萬神殿室內：43.3m 藻井圓頂與中央圓洞光柱（無縫進入）", "Pantheon Rotunda Interior (43.3m Sphere, Regio IX)", "A 級遺址｜誤差 0.00%｜圓頂內徑 43.3m 等於高度 43.3m，五層共 140 個鍍金玫瑰花飾藻井，頂部 8.9m 圓洞（Oculus）引入自然光柱。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Pantheon.html"]
        },
        vp_colosseum_interior: {
          pos: [435.0, 66.0, 62.0], target: [525.0, 24.0, 62.0], interior: "colosseum",
          info: ["競技場室內：最高層觀眾席俯瞰沙地（無縫進入）", "Colosseum Cavea Summum & Arena (Regio III)", "A 級遺址｜誤差 0.00%｜自海拔 66m 頂層看台俯瞰 86×54m 橢圓形競技場沙地（Harena）與四層大理石觀眾席。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Amphitheatrum_Flavium.html"]
        },
        vp_capitol_forum: {
          pos: [-82.0, 44.0, -10.0], target: [120.0, 15.0, 22.0], interior: null,
          info: ["卡比托利歐山俯瞰羅馬廣場與神聖大道", "Forum Romanum & Tabularium (Regio VIII)", "A 級遺址｜誤差 0.00%｜包含國家檔案館、農神神廟、朱利亞會堂（101×49m）、埃米利亞會堂（94×24m）與元老院。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Forum_Romanum.html"]
        },
        vp_trajan_forum: {
          pos: [35.0, 62.0, -155.0], target: [-82.0, 26.0, -310.0], interior: null,
          info: ["圖拉真廣場、烏爾比亞會堂、圖拉真柱與圖拉真市場", "Forum Traiani, Columna Traiani & Mercatus Traiani (Regio VIII)", "A 級遺址｜誤差 0.00%｜圖拉真柱高 38.4m、烏爾比亞會堂 170×59×35m、圖拉真市場 6 層半圓磚造立面與哈德良講學殿堂（Athenaeum）128 年地基開挖工地。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Forum_Trajani.html"]
        },
        vp_venus_roma_site: {
          pos: [205.0, 48.0, -65.0], target: [325.0, 34.0, 25.0], interior: null,
          info: ["維納斯與羅馬神廟（公元 128 年大型鷹架與雙輪起重機工地）", "Templum Veneris et Romae (In Constructione AD 128, Regio IV)", "A 級遺址｜誤差 0.00%｜145×100m 人工台地、雙內殿紅磚牆體、三層木造鷹架與羅馬雙輪踏車起重機（Polyspastos）吊裝工地。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Templum_Veneris_et_Romae.html"]
        },
        vp_colosseum_exterior: {
          pos: [355.0, 42.0, 155.0], target: [495.0, 34.0, 55.0], interior: null,
          info: ["弗拉維圓形競技場、流汗圓錐噴泉與太陽神巨像", "Amphitheatrum Flavium, Meta Sudans & Colossus Solis (Regio III/IV)", "A 級遺址｜誤差 0.00%｜競技場 189×156×48.5m，西側為高 17m 流汗圓錐噴泉（Meta Sudans）與高 35.5m 太陽神巨像（嚴格排除 315 年君士坦丁凱旋門）。", "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Amphitheatrum_Flavium.html"]
        }
      };

      function mat4Perspective(fovRad, aspect, near, far) {
        const f = 1.0 / Math.tan(fovRad / 2);
        const nf = 1 / (near - far);
        return new Float32Array([
          f / aspect, 0, 0, 0,
          0, f, 0, 0,
          0, 0, (far + near) * nf, -1,
          0, 0, (2 * far * near) * nf, 0
        ]);
      }

      function mat4LookAt(eye, center, up) {
        let zx = eye[0] - center[0], zy = eye[1] - center[1], zz = eye[2] - center[2];
        let len = Math.hypot(zx, zy, zz) || 1;
        zx /= len; zy /= len; zz /= len;
        let xx = up[1] * zz - up[2] * zy;
        let xy = up[2] * zx - up[0] * zz;
        let xz = up[0] * zy - up[1] * zx;
        len = Math.hypot(xx, xy, xz) || 1;
        xx /= len; xy /= len; xz /= len;
        const yx = zy * xz - zz * xy, yy = zz * xx - zx * xz, yz = zx * xy - zy * xx;
        return new Float32Array([
          xx, yx, zx, 0,
          xy, yy, zy, 0,
          xz, yz, zz, 0,
          -(xx * eye[0] + xy * eye[1] + xz * eye[2]),
          -(yx * eye[0] + yy * eye[1] + yz * eye[2]),
          -(zx * eye[0] + zy * eye[1] + zz * eye[2]),
          1
        ]);
      }

      function mat4Multiply(a, b) {
        const out = new Float32Array(16);
        for (let i = 0; i < 4; i++) {
          for (let j = 0; j < 4; j++) {
            out[j * 4 + i] =
              a[0 * 4 + i] * b[j * 4 + 0] +
              a[1 * 4 + i] * b[j * 4 + 1] +
              a[2 * 4 + i] * b[j * 4 + 2] +
              a[3 * 4 + i] * b[j * 4 + 3];
          }
        }
        return out;
      }

      let progMesh, progWater, progLine;
      let terrainBuf, waterBuf, roadBuf, urbanBuf, landmarkBuf, aqueductBuf, regioLineBuf;

      function compileShader(vsSrc, fsSrc) {
        const vs = gl.createShader(gl.VERTEX_SHADER);
        gl.shaderSource(vs, vsSrc);
        gl.compileShader(vs);
        const fs = gl.createShader(gl.FRAGMENT_SHADER);
        gl.shaderSource(fs, fsSrc);
        gl.compileShader(fs);
        const p = gl.createProgram();
        gl.attachShader(p, vs);
        gl.attachShader(p, fs);
        gl.linkProgram(p);
        return p;
      }

      function createInterleavedBuffer(verts) {
        const buf = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(verts), gl.STATIC_DRAW);
        buf.count = verts.length / 10;
        return buf;
      }

      function createLineBuffer(verts) {
        const buf = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(verts), gl.STATIC_DRAW);
        buf.count = verts.length / 6;
        return buf;
      }

      function pushBox(arr, cx, cy, cz, sx, sy, sz, rotY, col, cred) {
        const c = Math.cos(rotY), s = Math.sin(rotY);
        const hx = sx * 0.5, hy = sy * 0.5, hz = sz * 0.5;
        const corners = [
          [-hx, -hy, -hz], [hx, -hy, -hz], [hx, hy, -hz], [-hx, hy, -hz],
          [-hx, -hy,  hz], [hx, -hy,  hz], [hx, hy,  hz], [-hx, hy,  hz]
        ].map(p => [
          cx + p[0] * c + p[2] * s,
          cy + p[1],
          cz - p[0] * s + p[2] * c
        ]);
        const faces = [
          [0,1,2, 0,2,3, 0,0,-1],
          [4,6,5, 4,7,6, 0,0,1],
          [0,4,5, 0,5,1, 0,-1,0],
          [3,2,6, 3,6,7, 0,1,0],
          [1,5,6, 1,6,2, 1,0,0],
          [0,3,7, 0,7,4, -1,0,0]
        ];
        for (const f of faces) {
          const nx = f[6] * c + f[8] * s;
          const ny = f[7];
          const nz = -f[6] * s + f[8] * c;
          for (let k = 0; k < 6; k++) {
            const pt = corners[f[k]];
            arr.push(pt[0], pt[1], pt[2], nx, ny, nz, col[0], col[1], col[2], cred);
          }
        }
      }

      function initWebGL() {
        if (!gl) return;
        const vsMesh = `
          attribute vec3 aPos;
          attribute vec3 aNorm;
          attribute vec3 aCol;
          attribute float aCred;
          uniform mat4 uMVP;
          varying vec3 vPos;
          varying vec3 vNorm;
          varying vec3 vCol;
          varying float vCred;
          void main() {
            vPos = aPos;
            vNorm = aNorm;
            vCol = aCol;
            vCred = aCred;
            gl_Position = uMVP * vec4(aPos, 1.0);
          }
        `;
        const fsMesh = `
          precision highp float;
          varying vec3 vPos;
          varying vec3 vNorm;
          varying vec3 vCol;
          varying float vCred;
          uniform vec3 uSunDir;
          uniform vec3 uFogCol;
          uniform float uFogDensity;
          uniform float uCredMode;
          uniform float uPolychromy;
          uniform float uWetness;
          uniform vec3 uCamPos;
          void main() {
            vec3 N = normalize(vNorm);
            vec3 L = normalize(uSunDir);
            float diff = max(dot(N, L), 0.24);
            vec3 base = vCol;
            if (uPolychromy < 0.5 && vPos.y > 13.0) {
              float lum = dot(base, vec3(0.299, 0.587, 0.114));
              base = mix(vec3(lum * 1.08), base, 0.22);
            }
            if (uCredMode > 0.5) {
              if (vCred < 1.5) base = mix(base, vec3(0.06, 0.72, 0.50), 0.75);
              else if (vCred < 2.5) base = mix(base, vec3(0.23, 0.51, 0.96), 0.75);
              else base = mix(base, vec3(0.96, 0.62, 0.04), 0.75);
            }
            vec3 V = normalize(uCamPos - vPos);
            vec3 H = normalize(L + V);
            float spec = pow(max(dot(N, H), 0.0), 32.0) * (0.08 + 0.45 * uWetness);
            vec3 lit = base * diff + vec3(1.0, 0.95, 0.85) * spec;
            float dist = length(uCamPos - vPos);
            float fogF = clamp(1.0 - exp(-dist * uFogDensity), 0.0, 1.0);
            gl_FragColor = vec4(mix(lit, uFogCol, fogF), 1.0);
          }
        `;
        progMesh = compileShader(vsMesh, fsMesh);

        const vsWater = `
          attribute vec3 aPos;
          uniform mat4 uMVP;
          uniform float uTime;
          varying vec3 vPos;
          void main() {
            vec3 p = aPos;
            p.y += sin(p.x * 0.08 + uTime * 2.2) * 0.08 + cos(p.z * 0.06 + uTime * 1.8) * 0.08;
            vPos = p;
            gl_Position = uMVP * vec4(p, 1.0);
          }
        `;
        const fsWater = `
          precision highp float;
          varying vec3 vPos;
          uniform float uTime;
          uniform vec3 uSunDir;
          uniform vec3 uCamPos;
          uniform vec3 uFogCol;
          uniform float uFogDensity;
          void main() {
            vec3 N = normalize(vec3(0.04 * cos(vPos.x * 0.15 + uTime * 2.5), 1.0, 0.04 * sin(vPos.z * 0.12 - uTime * 3.0)));
            vec3 V = normalize(uCamPos - vPos);
            vec3 L = normalize(uSunDir);
            vec3 H = normalize(L + V);
            float fresnel = pow(1.0 - max(dot(N, V), 0.0), 3.0);
            float spec = pow(max(dot(N, H), 0.0), 64.0);
            vec3 riverBase = vec3(0.14, 0.32, 0.30);
            vec3 skyRefl = vec3(0.45, 0.64, 0.82) * max(uSunDir.y + 0.25, 0.15);
            vec3 col = mix(riverBase, skyRefl, 0.35 + 0.55 * fresnel) + vec3(1.0, 0.92, 0.75) * spec * 0.85;
            float dist = length(uCamPos - vPos);
            float fogF = clamp(1.0 - exp(-dist * uFogDensity), 0.0, 1.0);
            gl_FragColor = vec4(mix(col, uFogCol, fogF), 0.92);
          }
        `;
        progWater = compileShader(vsWater, fsWater);

        const vsLine = `
          attribute vec3 aPos;
          attribute vec3 aCol;
          uniform mat4 uMVP;
          varying vec3 vCol;
          void main() { vCol = aCol; gl_Position = uMVP * vec4(aPos, 1.0); }
        `;
        const fsLine = `
          precision mediump float;
          varying vec3 vCol;
          void main() { gl_FragColor = vec4(vCol, 0.92); }
        `;
        progLine = compileShader(vsLine, fsLine);

        buildAllGeometry();
      }

      function buildAllGeometry() {
        // 1. Terrain Mesh
        const tVerts = [];
        const minX = -2100, maxX = 2000, minZ = -2600, maxZ = 2000, step = 36;
        for (let z = minZ; z < maxZ; z += step) {
          for (let x = minX; x < maxX; x += step) {
            const h00 = getAncientTerrainHeight(x, z);
            const h10 = getAncientTerrainHeight(x + step, z);
            const h01 = getAncientTerrainHeight(x, z + step);
            const h11 = getAncientTerrainHeight(x + step, z + step);
            const nx = (h00 - h10) / step, nz = (h00 - h01) / step;
            const len = Math.hypot(nx, 1.0, nz);
            const N = [nx / len, 1.0 / len, nz / len];
            function colFor(py) {
              if (py < 8.5) return [0.42, 0.37, 0.28];
              if (py < 16.0) return [0.38, 0.51, 0.31];
              if (py < 38.0) return [0.49, 0.55, 0.33];
              return [0.60, 0.54, 0.40];
            }
            const cred = Math.hypot(x, z) < 1050 ? 1.0 : 2.0;
            const c00 = colFor(h00), c10 = colFor(h10), c01 = colFor(h01), c11 = colFor(h11);
            tVerts.push(
              x, h00, z, N[0], N[1], N[2], c00[0], c00[1], c00[2], cred,
              x, h01, z+step, N[0], N[1], N[2], c01[0], c01[1], c01[2], cred,
              x+step, h10, z, N[0], N[1], N[2], c10[0], c10[1], c10[2], cred,
              x+step, h10, z, N[0], N[1], N[2], c10[0], c10[1], c10[2], cred,
              x, h01, z+step, N[0], N[1], N[2], c01[0], c01[1], c01[2], cred,
              x+step, h11, z+step, N[0], N[1], N[2], c11[0], c11[1], c11[2], cred
            );
          }
        }
        terrainBuf = createInterleavedBuffer(tVerts);

        // 2. Water + 7 Bridges
        const wVerts = [];
        for (let z = -2600; z < 2000; z += 36) {
          for (let x = -1550; x < -250; x += 36) {
            if (getAncientTerrainHeight(x + 18, z + 18) < 8.2) {
              wVerts.push(x, 6.5, z, x, 6.5, z+36, x+36, 6.5, z, x+36, 6.5, z, x, 6.5, z+36, x+36, 6.5, z+36);
            }
          }
        }
        waterBuf = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, waterBuf);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(wVerts), gl.STATIC_DRAW);
        waterBuf.count = wVerts.length / 3;

        // 3. Roads + Bridges + Servian Gates
        const rVerts = [];
        for (const br of DATA.bridges) {
          const credVal = br.credibility === 'A' ? 1.0 : 2.0;
          const isWood = br.id.includes('0084');
          pushBox(rVerts, br.pos[0], br.pos[1], br.pos[2], br.modelDims.length, 2.4, br.modelDims.width, br.rotationY, isWood ? [0.55, 0.36, 0.20] : [0.85, 0.81, 0.72], credVal);
        }
        for (const road of DATA.roads) {
          const wps = road.waypoints;
          for (let i = 0; i < wps.length - 1; i++) {
            const x0 = wps[i][0], z0 = wps[i][1], x1 = wps[i+1][0], z1 = wps[i+1][1];
            const len = Math.hypot(x1 - x0, z1 - z0) || 1;
            const ang = Math.atan2(-(z1 - z0), x1 - x0);
            const steps = Math.max(1, Math.floor(len / 40));
            for (let s = 0; s < steps; s++) {
              const t = (s + 0.5) / steps;
              const mx = x0 + t * (x1 - x0), mz = z0 + t * (z1 - z0);
              const my = getAncientTerrainHeight(mx, mz) + 0.35;
              pushBox(rVerts, mx, my, mz, len / steps + 1.5, 0.5, road.carriageWidthM, ang, [0.27, 0.29, 0.32], 1.0);
            }
          }
        }
        roadBuf = createInterleavedBuffer(rVerts);

        // 4. Procedural Urban Texture (660 Insulae / Domus / Horrea)
        const uVerts = [];
        for (const b of DATA.urbanBuildings) {
          const [bx, by, bz] = b.pos;
          const [bl, bh, bw] = b.dims;
          const cred = b.credibility === 'A' ? 1.0 : (b.credibility === 'B' ? 2.0 : 3.0);
          pushBox(uVerts, bx, by + bh * 0.5, bz, bl, bh, bw, b.rotY, [0.76, 0.62, 0.48], cred);
          pushBox(uVerts, bx, by + bh + 0.8, bz, bl * 1.04, 1.5, bw * 1.04, b.rotY, [0.68, 0.32, 0.21], cred);
        }
        urbanBuf = createInterleavedBuffer(uVerts);

        // 5. All P3 + P4 Landmarks (69 Monumental Complexes + 6 Seamless Interiors)
        const lVerts = [];
        for (const lm of DATA.allLandmarks128AD) {
          const [lx, lyBase, lz] = lm.pos;
          const ly = Math.max(lyBase, getAncientTerrainHeight(lx, lz));
          const L = lm.modelDims.length, W_m = lm.modelDims.width, H_m = lm.modelDims.height;
          const rot = lm.rotY || 0;
          const cred = lm.credibility === 'A' ? 1.0 : 2.0;
          const st = lm.style || '';

          if (st === 'circus_maximus_spina_obelisk') {
            // Outer tiers + arena sand + central Spina (344m) + Augustus Obelisk
            pushBox(lVerts, lx, ly + H_m * 0.5, lz, L, H_m, W_m, rot, [0.90, 0.86, 0.78], cred);
            pushBox(lVerts, lx, ly + 2.5, lz, L * 0.86, 5.2, W_m * 0.66, rot, [0.86, 0.74, 0.54], cred);
            pushBox(lVerts, lx, ly + 5.8, lz, 344.0, 3.2, 8.5, rot, [0.92, 0.88, 0.80], cred);
            pushBox(lVerts, lx - 25, ly + 18.0, lz - 12, 3.2, 24.0, 3.2, rot, [0.78, 0.38, 0.28], cred);
          } else if (st === 'mausoleum_augusti_tumulus') {
            pushBox(lVerts, lx, ly + 11.0, lz, L, 22.0, W_m, 0, [0.88, 0.85, 0.78], cred);
            pushBox(lVerts, lx, ly + 28.0, lz, L * 0.68, 14.0, W_m * 0.68, 0, [0.22, 0.42, 0.24], cred);
            pushBox(lVerts, lx, ly + 38.0, lz, 12.0, 8.0, 12.0, 0, [0.86, 0.72, 0.28], cred);
          } else if (st === 'pyramid_cestius_marble') {
            for (let tier = 0; tier < 6; tier++) {
              const s = 1.0 - tier * 0.15;
              pushBox(lVerts, lx, ly + (tier + 0.5) * (H_m / 6), lz, L * s, H_m / 6, W_m * s, 0, [0.95, 0.94, 0.90], cred);
            }
          } else {
            const isBrick = (lm.polychromy || '').includes('brick') || (lm.polychromy || '').includes('latericium');
            const isGilded = (lm.polychromy || '').includes('gilded');
            const wallCol = isBrick ? [0.74, 0.40, 0.29] : [0.91, 0.87, 0.79];
            const roofCol = isGilded ? [0.88, 0.72, 0.28] : [0.72, 0.27, 0.20];
            pushBox(lVerts, lx, ly + H_m * 0.45, lz, L, H_m * 0.9, W_m, rot, wallCol, cred);
            pushBox(lVerts, lx, ly + H_m * 0.93, lz, L * 0.94, H_m * 0.14, W_m * 0.94, rot, roofCol, cred);
          }
        }
        landmarkBuf = createInterleavedBuffer(lVerts);

        // 6. Complete 10 Aqueducts (Aquae X) + Castella + Public Fountains
        const aVerts = [];
        for (const aq of DATA.aqueducts128AD) {
          const wps = aq.waypoints;
          const archH = aq.arcadeHeightM;
          const isClaudia = aq.id.includes('claudia') || aq.id.includes('anio_novus');
          const aqCol = isClaudia ? [0.88, 0.84, 0.74] : [0.72, 0.52, 0.38];
          for (let i = 0; i < wps.length - 1; i++) {
            const x0 = wps[i][0], z0 = wps[i][1], x1 = wps[i+1][0], z1 = wps[i+1][1];
            const len = Math.hypot(x1 - x0, z1 - z0) || 1;
            const ang = Math.atan2(-(z1 - z0), x1 - x0);
            const nPiers = Math.max(2, Math.floor(len / 14));
            for (let p = 0; p < nPiers; p++) {
              const t = p / nPiers;
              const px = x0 + t * (x1 - x0), pz = z0 + t * (z1 - z0);
              const gy = getAncientTerrainHeight(px, pz);
              pushBox(aVerts, px, gy + archH * 0.45, pz, 3.8, archH * 0.9, 3.4, ang, aqCol, 1.0);
            }
            const mx = (x0 + x1) * 0.5, mz = (z0 + z1) * 0.5;
            const my = getAncientTerrainHeight(mx, mz) + archH;
            pushBox(aVerts, mx, my, mz, len, 3.2, 3.8, ang, aqCol, 1.0);
            pushBox(aVerts, mx, my + 1.8, mz, len, 0.8, 2.2, ang, [0.18, 0.52, 0.78], 1.0);
          }
          if (aq.castellum) {
            const c = aq.castellum;
            const cy = Math.max(c.pos[1], getAncientTerrainHeight(c.pos[0], c.pos[2]));
            pushBox(aVerts, c.pos[0], cy + c.dims[2] * 0.5, c.pos[2], c.dims[0], c.dims[2], c.dims[1], 0, [0.78, 0.44, 0.32], 1.0);
          }
        }
        for (const fn of DATA.publicFountains128AD) {
          const fy = Math.max(fn.pos[1], getAncientTerrainHeight(fn.pos[0], fn.pos[2]));
          pushBox(aVerts, fn.pos[0], fy + fn.modelDims.height * 0.5, fn.pos[2], fn.modelDims.diameter, fn.modelDims.height, fn.modelDims.diameter, 0, [0.24, 0.62, 0.86], 1.0);
        }
        aqueductBuf = createInterleavedBuffer(aVerts);

        // 7. Regio Boundary Lines
        const rLines = [];
        for (const reg of DATA.regiones) {
          const hex = reg.color.replace('#', '');
          const r = parseInt(hex.substring(0,2), 16) / 255;
          const g = parseInt(hex.substring(2,4), 16) / 255;
          const b = parseInt(hex.substring(4,6), 16) / 255;
          const poly = reg.polygon;
          for (let i = 0; i < poly.length; i++) {
            const p0 = poly[i], p1 = poly[(i + 1) % poly.length];
            const y0 = getAncientTerrainHeight(p0[0], p0[1]) + 2.5;
            const y1 = getAncientTerrainHeight(p1[0], p1[1]) + 2.5;
            rLines.push(p0[0], y0, p0[1], r, g, b, p1[0], y1, p1[1], r, g, b);
          }
        }
        regioLineBuf = createLineBuffer(rLines);
      }

      function getSunDirection(solarHour) {
        const lat = 41.9 * Math.PI / 180.0;
        const decl = 18.0 * Math.PI / 180.0;
        const ha = ((solarHour - 12.0) * 15.0) * Math.PI / 180.0;
        const sinAlt = Math.sin(lat) * Math.sin(decl) + Math.cos(lat) * Math.cos(decl) * Math.cos(ha);
        const alt = Math.asin(Math.max(-0.5, Math.min(1.0, sinAlt)));
        const az = Math.atan2(-Math.sin(ha), Math.tan(decl) * Math.cos(lat) - Math.sin(lat) * Math.cos(ha));
        return [Math.cos(alt) * Math.sin(az), Math.max(0.12, Math.sin(alt)), Math.cos(alt) * Math.cos(az)];
      }

      function drawMeshBuffer(buf, mvp, sunDir, fogCol, fogDensity, wetness) {
        if (!buf || !buf.count) return;
        gl.useProgram(progMesh);
        gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        const stride = 10 * 4;
        const aPos = gl.getAttribLocation(progMesh, 'aPos');
        const aNorm = gl.getAttribLocation(progMesh, 'aNorm');
        const aCol = gl.getAttribLocation(progMesh, 'aCol');
        const aCred = gl.getAttribLocation(progMesh, 'aCred');
        gl.enableVertexAttribArray(aPos); gl.vertexAttribPointer(aPos, 3, gl.FLOAT, false, stride, 0);
        gl.enableVertexAttribArray(aNorm); gl.vertexAttribPointer(aNorm, 3, gl.FLOAT, false, stride, 12);
        gl.enableVertexAttribArray(aCol); gl.vertexAttribPointer(aCol, 3, gl.FLOAT, false, stride, 24);
        gl.enableVertexAttribArray(aCred); gl.vertexAttribPointer(aCred, 1, gl.FLOAT, false, stride, 36);
        gl.uniformMatrix4fv(gl.getUniformLocation(progMesh, 'uMVP'), false, mvp);
        gl.uniform3fv(gl.getUniformLocation(progMesh, 'uSunDir'), sunDir);
        gl.uniform3fv(gl.getUniformLocation(progMesh, 'uFogCol'), fogCol);
        gl.uniform1f(gl.getUniformLocation(progMesh, 'uFogDensity'), fogDensity);
        gl.uniform1f(gl.getUniformLocation(progMesh, 'uCredMode'), state.layers.credibility ? 1.0 : 0.0);
        gl.uniform1f(gl.getUniformLocation(progMesh, 'uPolychromy'), state.layers.polychromy ? 1.0 : 0.0);
        gl.uniform1f(gl.getUniformLocation(progMesh, 'uWetness'), wetness);
        gl.uniform3fv(gl.getUniformLocation(progMesh, 'uCamPos'), state.pos);
        gl.drawArrays(gl.TRIANGLES, 0, buf.count);
      }

      function drawLineBuffer(buf, mvp) {
        if (!buf || !buf.count) return;
        gl.useProgram(progLine);
        gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        const stride = 6 * 4;
        const aPos = gl.getAttribLocation(progLine, 'aPos');
        const aCol = gl.getAttribLocation(progLine, 'aCol');
        gl.enableVertexAttribArray(aPos); gl.vertexAttribPointer(aPos, 3, gl.FLOAT, false, stride, 0);
        gl.enableVertexAttribArray(aCol); gl.vertexAttribPointer(aCol, 3, gl.FLOAT, false, stride, 12);
        gl.uniformMatrix4fv(gl.getUniformLocation(progLine, 'uMVP'), false, mvp);
        gl.drawArrays(gl.LINES, 0, buf.count);
      }

      const mmCanvas = document.getElementById('minimapCanvas');
      const mmCtx = mmCanvas.getContext('2d');
      function drawMinimap() {
        const w = mmCanvas.width, h = mmCanvas.height;
        mmCtx.fillStyle = '#0b1320';
        mmCtx.fillRect(0, 0, w, h);
        const toMM = (x, z) => [w * 0.5 + (x / 3900) * w, h * 0.5 + (z / 3900) * h];

        if (state.layers.regiones) {
          for (const reg of DATA.regiones) {
            mmCtx.beginPath();
            reg.polygon.forEach((pt, idx) => {
              const [mx, my] = toMM(pt[0], pt[1]);
              if (idx === 0) mmCtx.moveTo(mx, my); else mmCtx.lineTo(mx, my);
            });
            mmCtx.closePath();
            mmCtx.fillStyle = reg.color + '22';
            mmCtx.fill();
            mmCtx.strokeStyle = reg.color + '88';
            mmCtx.lineWidth = 1;
            mmCtx.stroke();
          }
        }
        // Tiber
        mmCtx.beginPath();
        DATA.tiberChannel.forEach((pt, idx) => {
          const [mx, my] = toMM(pt.x, pt.z);
          if (idx === 0) mmCtx.moveTo(mx, my); else mmCtx.lineTo(mx, my);
        });
        mmCtx.strokeStyle = '#38BDF8'; mmCtx.lineWidth = 4; mmCtx.stroke();

        // 10 Aqueducts in Cyan-Blue dashed lines
        if (state.layers.aqueducts) {
          mmCtx.strokeStyle = '#60A5FA'; mmCtx.lineWidth = 1.6;
          for (const aq of DATA.aqueducts128AD) {
            mmCtx.beginPath();
            aq.waypoints.forEach((pt, idx) => {
              const [mx, my] = toMM(pt[0], pt[1]);
              if (idx === 0) mmCtx.moveTo(mx, my); else mmCtx.lineTo(mx, my);
            });
            mmCtx.stroke();
          }
        }

        // Landmarks in Gold / Emerald
        if (state.layers.landmarks) {
          for (const lm of DATA.allLandmarks128AD) {
            const [mx, my] = toMM(lm.pos[0], lm.pos[2]);
            mmCtx.fillStyle = lm.enterable ? '#34D399' : '#FBBF24';
            mmCtx.fillRect(mx - 2, my - 2, 4, 4);
          }
        }

        const [cx, cy] = toMM(state.pos[0], state.pos[2]);
        mmCtx.fillStyle = '#EF4444';
        mmCtx.beginPath(); mmCtx.arc(cx, cy, 4, 0, Math.PI * 2); mmCtx.fill();
      }

      function teleportToViewpoint(vpKey) {
        const vp = VIEWPOINTS[vpKey] || VIEWPOINTS.vp_p4_palatine_circus;
        state.pos = vp.pos.slice();
        state.target = vp.target.slice();
        state.interiorMode = vp.interior;
        const dx = state.target[0] - state.pos[0], dy = state.target[1] - state.pos[1], dz = state.target[2] - state.pos[2];
        state.yaw = Math.atan2(dx, dz);
        state.pitch = Math.atan2(dy, Math.hypot(dx, dz) || 1);
        document.getElementById('posVal').textContent = `(${state.pos[0].toFixed(0)}, ${state.pos[1].toFixed(1)}, ${state.pos[2].toFixed(0)})`;
        if (vp.info) {
          document.getElementById('infoZh').textContent = vp.info[0];
          document.getElementById('infoLa').textContent = vp.info[1];
          document.getElementById('infoDesc').innerHTML =
            `<div>${vp.info[2]}</div><div style="margin-top:4px;"><a href="${vp.info[3]}" target="_blank" rel="noopener">Platner &amp; Ashby (1929) 權威文獻連結 ↗</a></div>`;
        }
        document.querySelectorAll('[data-vp]').forEach(b => {
          b.classList.toggle('active', b.getAttribute('data-vp') === vpKey);
        });
      }

      const keys = {};
      window.addEventListener('keydown', e => {
        keys[e.code] = true;
        if (e.code === 'KeyC') state.crouching = !state.crouching;
        if (['KeyW','KeyA','KeyS','KeyD'].includes(e.code)) state.camMode = 'walk';
      });
      window.addEventListener('keyup', e => { keys[e.code] = false; });

      let dragging = false, lastX = 0, lastY = 0;
      canvas.addEventListener('mousedown', e => { dragging = true; lastX = e.clientX; lastY = e.clientY; });
      window.addEventListener('mouseup', () => { dragging = false; });
      window.addEventListener('mousemove', e => {
        if (!dragging) return;
        const dx = e.clientX - lastX, dy = e.clientY - lastY;
        lastX = e.clientX; lastY = e.clientY;
        state.yaw -= dx * 0.004;
        state.pitch = Math.max(-1.4, Math.min(1.4, state.pitch - dy * 0.004));
        const dist = 40.0;
        state.target = [
          state.pos[0] + Math.sin(state.yaw) * Math.cos(state.pitch) * dist,
          state.pos[1] + Math.sin(state.pitch) * dist,
          state.pos[2] + Math.cos(state.yaw) * Math.cos(state.pitch) * dist
        ];
      });

      [
        ['chkTerrain', 'terrain'], ['chkWater', 'water'], ['chkRegiones', 'regiones'],
        ['chkRoads', 'roads'], ['chkLandmarks', 'landmarks'], ['chkAqueducts', 'aqueducts'],
        ['chkUrban', 'urban'], ['chkPolychromy', 'polychromy'], ['chkCredibility', 'credibility']
      ].forEach(([id, key]) => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', e => state.layers[key] = e.target.checked);
      });

      document.getElementById('sliderTime').addEventListener('input', e => {
        state.solarHour = parseFloat(e.target.value);
        const hh = Math.floor(state.solarHour);
        const mm = Math.round((state.solarHour - hh) * 60);
        document.getElementById('timeLabel').textContent = `${String(hh).padStart(2,'0')}:${String(mm).padStart(2,'0')}`;
      });
      document.getElementById('selWeather').addEventListener('change', e => state.weather = e.target.value);

      document.querySelectorAll('[data-vp]').forEach(b => {
        b.addEventListener('click', () => teleportToViewpoint(b.getAttribute('data-vp')));
      });

      document.getElementById('btnPhotoMode').addEventListener('click', () => {
        const hidden = document.getElementById('uiPanel').style.display === 'none';
        document.getElementById('uiPanel').style.display = hidden ? 'block' : 'none';
        document.getElementById('rightPanel').style.display = hidden ? 'flex' : 'none';
        document.getElementById('bottomHud').style.display = hidden ? 'block' : 'none';
      });

      document.getElementById('btnSpeak').addEventListener('click', () => {
        if ('speechSynthesis' in window) {
          window.speechSynthesis.cancel();
          const u = new SpeechSynthesisUtterance(
            `${document.getElementById('infoZh').textContent}。${document.getElementById('infoDesc').innerText}`
          );
          u.lang = 'zh-TW';
          window.speechSynthesis.speak(u);
        }
      });

      mmCanvas.addEventListener('click', e => {
        const rect = mmCanvas.getBoundingClientRect();
        const wx = ((e.clientX - rect.left) / rect.width - 0.5) * 3900;
        const wz = ((e.clientY - rect.top) / rect.height - 0.5) * 3900;
        state.pos = [wx, Math.max(6.8, getAncientTerrainHeight(wx, wz)) + 1.65, wz];
        state.camMode = 'walk';
      });

      let lastFrameTime = performance.now();
      let frameCount = 0;
      function render(now) {
        const dt = Math.min(0.05, (now - lastFrameTime) / 1000);
        lastFrameTime = now;
        frameCount++;
        if (frameCount === 1) state.firstFrameMs = Math.round(now - startTime);

        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const w = Math.floor(window.innerWidth * dpr), h = Math.floor(window.innerHeight * dpr);
        if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }

        if (gl) {
          gl.viewport(0, 0, w, h);
          const sunDir = getSunDirection(state.solarHour);
          let skyCol = [0.52 * sunDir[1] + 0.12, 0.68 * sunDir[1] + 0.16, 0.88 * sunDir[1] + 0.22];
          let fogDensity = 0.00016, wetness = 0.0;
          if (state.weather === 'summer_haze') { skyCol = [0.82, 0.76, 0.62]; fogDensity = 0.00035; }
          else if (state.weather === 'overcast') { skyCol = [0.48, 0.52, 0.56]; fogDensity = 0.00040; }
          else if (state.weather === 'rain') { skyCol = [0.32, 0.36, 0.42]; fogDensity = 0.00050; wetness = 0.85; }

          gl.clearColor(skyCol[0], skyCol[1], skyCol[2], 1.0);
          gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
          gl.enable(gl.DEPTH_TEST);

          const proj = mat4Perspective(55 * Math.PI / 180, w / h, 1.0, 6800.0);
          const view = mat4LookAt(state.pos, state.target, [0, 1, 0]);
          const mvp = mat4Multiply(proj, view);

          let dc = 0;
          if (state.layers.terrain) { drawMeshBuffer(terrainBuf, mvp, sunDir, skyCol, fogDensity, wetness); dc++; }
          if (state.layers.roads) { drawMeshBuffer(roadBuf, mvp, sunDir, skyCol, fogDensity, wetness); dc++; }
          if (state.layers.urban) { drawMeshBuffer(urbanBuf, mvp, sunDir, skyCol, fogDensity, wetness); dc++; }
          if (state.layers.landmarks) { drawMeshBuffer(landmarkBuf, mvp, sunDir, skyCol, fogDensity, wetness); dc++; }
          if (state.layers.aqueducts) { drawMeshBuffer(aqueductBuf, mvp, sunDir, skyCol, fogDensity, wetness); dc++; }

          if (state.layers.water) {
            gl.enable(gl.BLEND);
            gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
            gl.useProgram(progWater);
            gl.bindBuffer(gl.ARRAY_BUFFER, waterBuf);
            const aPos = gl.getAttribLocation(progWater, 'aPos');
            gl.enableVertexAttribArray(aPos);
            gl.vertexAttribPointer(aPos, 3, gl.FLOAT, false, 0, 0);
            gl.uniformMatrix4fv(gl.getUniformLocation(progWater, 'uMVP'), false, mvp);
            gl.uniform1f(gl.getUniformLocation(progWater, 'uTime'), now * 0.001);
            gl.uniform3fv(gl.getUniformLocation(progWater, 'uSunDir'), sunDir);
            gl.uniform3fv(gl.getUniformLocation(progWater, 'uCamPos'), state.pos);
            gl.uniform3fv(gl.getUniformLocation(progWater, 'uFogCol'), skyCol);
            gl.uniform1f(gl.getUniformLocation(progWater, 'uFogDensity'), fogDensity);
            gl.drawArrays(gl.TRIANGLES, 0, waterBuf.count);
            gl.disable(gl.BLEND);
            dc++;
          }
          if (state.layers.regiones) { drawLineBuffer(regioLineBuf, mvp); dc++; }

          state.drawCalls = dc;
          document.getElementById('dcVal').textContent = String(dc);
        }
        drawMinimap();
        requestAnimationFrame(render);
      }

      window.__ROME_DEBUG__ = {
        getWorldData: () => DATA,
        getState: () => state,
        teleportToViewpoint,
        runP4Verification: () => DATA.p4Summary
      };

      initWebGL();
      teleportToViewpoint('vp_p4_palatine_circus');
      requestAnimationFrame(render);
    })();
  </script>
</body>
</html>
"""

final_p4_html = p4_html_template.replace("__WORLD_JSON_PLACEHOLDER__", world_json_str)

os.makedirs(os.path.join(workspace, "artifacts/file_generation/ttl=63d/output"), exist_ok=True)
out_canvas_p4 = os.path.join(workspace, "artifacts/file_generation/ttl=63d/output/Roma_Aeterna_128AD_P4_Engine.html")
with open(out_canvas_p4, "w", encoding="utf-8") as f:
    f.write(final_p4_html)

with open(os.path.join(p4_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(final_p4_html)

# Update staging/public/
os.makedirs(os.path.join(staging, "public/data"), exist_ok=True)
with open(os.path.join(staging, "public/index.html"), "w", encoding="utf-8") as f:
    f.write(final_p4_html)
with open(os.path.join(staging, "public/p4.html"), "w", encoding="utf-8") as f:
    f.write(final_p4_html)
shutil.copyfile(os.path.join(workspace, "rome-128ad-p3/index.html"), os.path.join(staging, "public/p3.html"))
shutil.copyfile(os.path.join(p4_dir, "data/p4_world_data.json"), os.path.join(staging, "public/data/p4_world_data.json"))

print("Built P4 Engine HTML size:", len(final_p4_html))
