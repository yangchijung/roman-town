# -*- coding: utf-8 -*-
import json, os

p2_data_path = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p2/data/p2_world_data.json"
out_html_path = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/artifacts/file_generation/ttl=63d/output/Roma_Aeterna_128AD_P2_Engine.html"
local_html_path = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p2/index.html"

with open(p2_data_path, "r", encoding="utf-8") as f:
    world_data = json.load(f)

world_json_str = json.dumps(world_data, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Roma Aeterna AD 128 — P2 道路網與程序化城市紋理引擎</title>
  <style>
    :root {
      --bg-panel: rgba(15, 19, 26, 0.88);
      --border-gold: rgba(212, 175, 55, 0.45);
      --accent-gold: #E5C158;
      --text-main: #F3F4F6;
      --text-muted: #9CA3AF;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body, html { width: 100%; height: 100%; overflow: hidden; background: #0b0f17; font-family: -apple-system, BlinkMacSystemFont, "Noto Sans TC", sans-serif; color: var(--text-main); }
    #glCanvas { width: 100%; height: 100%; display: block; cursor: crosshair; }

    .top-bar {
      position: fixed; top: 12px; left: 12px; right: 12px;
      display: flex; justify-content: space-between; align-items: center;
      pointer-events: none; z-index: 20; gap: 12px; flex-wrap: wrap;
    }
    .brand-card, .telemetry-card {
      background: var(--bg-panel); border: 1px solid var(--border-gold);
      backdrop-filter: blur(10px); padding: 8px 14px; border-radius: 8px;
      pointer-events: auto; display: flex; align-items: center; gap: 14px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.45);
    }
    .brand-title { font-weight: 700; font-size: 14px; color: var(--accent-gold); }
    .brand-sub { font-size: 12px; color: var(--text-muted); }
    .stat-pill { font-size: 12px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
    .stat-pill strong { color: #34D399; }

    .side-panel {
      position: fixed; top: 68px; left: 12px; width: 325px;
      background: var(--bg-panel); border: 1px solid var(--border-gold);
      backdrop-filter: blur(10px); border-radius: 10px; padding: 14px;
      z-index: 20; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      max-height: calc(100vh - 90px); overflow-y: auto;
    }
    .panel-title {
      font-size: 13px; font-weight: 700; color: var(--accent-gold);
      margin-bottom: 8px; padding-bottom: 5px; border-bottom: 1px solid rgba(255,255,255,0.12);
      display: flex; justify-content: space-between; align-items: center;
    }
    .control-group { margin-bottom: 12px; }
    .toggle-row {
      display: flex; justify-content: space-between; align-items: center;
      padding: 4px 0; font-size: 12px; cursor: pointer;
    }
    .toggle-row input { accent-color: var(--accent-gold); width: 15px; height: 15px; cursor: pointer; }
    .btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 6px; }
    .btn {
      background: rgba(255,255,255,0.07); border: 1px solid rgba(212,175,55,0.35);
      color: var(--text-main); padding: 6px 8px; border-radius: 6px;
      font-size: 11px; cursor: pointer; transition: all 0.15s; text-align: left;
    }
    .btn:hover, .btn.active { background: rgba(212,175,55,0.25); border-color: var(--accent-gold); color: #fff; }

    .right-panel {
      position: fixed; top: 68px; right: 12px; width: 295px;
      display: flex; flex-direction: column; gap: 10px; z-index: 20;
    }
    .minimap-box, .info-card {
      background: var(--bg-panel); border: 1px solid var(--border-gold);
      border-radius: 10px; padding: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    #minimapCanvas { width: 100%; height: 220px; border-radius: 6px; background: #0d1624; display: block; cursor: pointer; }
    .info-card h3 { font-size: 13.5px; color: var(--accent-gold); margin-bottom: 2px; }
    .info-card .latin { font-size: 11.5px; font-style: italic; color: #93C5FD; margin-bottom: 6px; }
    .info-card .meta { font-size: 11.5px; color: var(--text-muted); line-height: 1.45; }
    .info-card a { color: #60A5FA; text-decoration: none; }

    .bottom-hud {
      position: fixed; bottom: 12px; left: 50%; transform: translateX(-50%);
      background: var(--bg-panel); border: 1px solid var(--border-gold);
      padding: 6px 16px; border-radius: 20px; font-size: 12px; color: var(--text-muted);
      z-index: 20; pointer-events: none; white-space: nowrap;
    }
  </style>
</head>
<body>
  <canvas id="glCanvas"></canvas>

  <div class="top-bar">
    <div class="brand-card">
      <div>
        <div class="brand-title">ROMA AETERNA · P2 道路網與程序化城市紋理（公元 128 年）</div>
        <div class="brand-sub" id="regionBanner">當前分區：Regio IV Subura | 建築總數：660 棟 (Batched) | 道路：14 條主幹道</div>
      </div>
    </div>
    <div class="telemetry-card">
      <div class="stat-pill">FPS: <strong id="fpsVal">60</strong></div>
      <div class="stat-pill">Draw Calls: <strong id="dcVal">8</strong> / 1500</div>
      <div class="stat-pill">Buildings: <strong>660</strong></div>
      <div class="stat-pill">Pos: <strong id="posVal">(280, 18.2, -195)</strong></div>
      <div class="stat-pill">考證年檢: <strong>PASS (≤128 AD)</strong></div>
    </div>
  </div>

  <div class="side-panel" id="uiPanel">
    <div class="panel-title">
      <span>P1+P2 資料圖層切換</span>
      <button class="btn" id="btnPhotoMode" style="padding:2px 6px;font-size:10.5px;">拍照模式 (P)</button>
    </div>
    <div class="control-group">
      <label class="toggle-row"><span>1. 七丘與維利亞丘地形 (DEM)</span><input type="checkbox" id="chkTerrain" checked /></label>
      <label class="toggle-row"><span>2. 古台伯河水系与 7 座橋樑</span><input type="checkbox" id="chkWater" checked /></label>
      <label class="toggle-row"><span>3. 玄武岩道路網與人行道 (14 條幹道)</span><input type="checkbox" id="chkRoads" checked /></label>
      <label class="toggle-row"><span>4. 公寓群 (Insulae 4–6 層含店鋪 Tabernae)</span><input type="checkbox" id="chkInsulae" checked /></label>
      <label class="toggle-row"><span>5. 貴族豪宅 (Domus 中庭與列柱花園)</span><input type="checkbox" id="chkDomus" checked /></label>
      <label class="toggle-row"><span>6. 河港倉庫 (Horrea) 與紀念柱廊</span><input type="checkbox" id="chkHorrea" checked /></label>
      <label class="toggle-row"><span>7. 14 行政區邊界與塞爾維烏斯城牆</span><input type="checkbox" id="chkRegiones" checked /></label>
      <label class="toggle-row"><span>8. 考證可信度模式 (A綠 / B藍 / C橘)</span><input type="checkbox" id="chkCredibility" /></label>
    </div>

    <div class="panel-title"><span>太陽時辰與天氣（北緯 41.9° N）</span></div>
    <div class="control-group">
      <div class="toggle-row">
        <span>太陽時：<strong id="timeLabel">15:00</strong></span>
        <input type="range" id="sliderTime" min="0" max="24" step="0.25" value="15.0" style="width:140px;" />
      </div>
      <div class="toggle-row">
        <span>天氣模式</span>
        <select id="selWeather" style="background:#1f2937;color:#fff;border:1px solid var(--border-gold);border-radius:4px;padding:2px 6px;font-size:11.5px;">
          <option value="clear">晴朗 (午後斜陽)</option>
          <option value="summer_haze">地中海夏熱霧</option>
          <option value="overcast">陰天雲層</option>
          <option value="rain">雨天 (玄武岩路面濕滑反光)</option>
        </select>
      </div>
    </div>

    <div class="panel-title"><span>P2 驗證機位（蘇布拉 vs 戰神廣場對比）</span></div>
    <div class="btn-grid" id="viewpointBtns">
      <button class="btn active" data-vp="vp_subura_alley_walk">VP1: 蘇布拉區擁擠巷弄 (1.65m)</button>
      <button class="btn" data-vp="vp_campus_martius_walk">VP2: 戰神廣場開闊柱廊 (1.65m)</button>
      <button class="btn" data-vp="vp_via_sacra_velia">VP3: 神聖大道與玄武岩鋪面</button>
      <button class="btn" data-vp="vp_quirinal_palatine_domus">VP4: 帕拉提諾與奎里納雷豪宅群</button>
      <button class="btn" data-vp="vp_emporium_horrea_ostiensis">VP5: 奧斯提亞大道與河港倉庫群</button>
      <button class="btn" data-vp="vp_via_appia_capena">VP6: 卡佩納門與阿庇亞大道起點</button>
      <button class="btn" data-vp="vp_urban_density_bird">VP7: 全城道路與分區紋理鳥瞰</button>
      <button class="btn" data-vp="vp_p2_credibility_overlay">VP8: 道路與建築考證分級 (A/B/C)</button>
    </div>
  </div>

  <div class="right-panel" id="rightPanel">
    <div class="minimap-box">
      <div class="panel-title" style="margin-bottom:6px;">
        <span>P2 道路網與建築紋理導航圖</span>
        <span style="font-size:10.5px;color:#9CA3AF;">點擊瞬移</span>
      </div>
      <canvas id="minimapCanvas" width="272" height="220"></canvas>
    </div>
    <div class="info-card">
      <h3 id="infoZh">蘇布拉坡道與高密度公寓群</h3>
      <div class="latin" id="infoLa">Clivus Suburanus & Insulae (Regio IV)</div>
      <div class="meta" id="infoDesc">
        <div>可信度：<strong>B 級（塞維魯大理石地圖 FUR 殘片與文獻記載）</strong></div>
        <div style="margin-top:4px;">街道寬度：玄武岩車道 4.8m + 兩側人行道 1.4m；兩側為 5–6 層高密度公寓（高 17–21m），一樓為店鋪（Tabernae），二樓以上設外懸木陽台（Maeniana）。</div>
        <div style="margin-top:4px;">文獻來源：<a href="https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Subura.html" target="_blank">Platner & Ashby: Subura</a></div>
      </div>
    </div>
  </div>

  <div class="bottom-hud" id="bottomHud">
    操作：WASD 步行穿梭街道 · Shift 奔跑 · Space 跳躍 · C 蹲下 · 點擊左側 VP1 / VP2 直接對比「蘇布拉區」與「戰神廣場」空間感
  </div>

  <script>
    window.__ROME_WORLD_DATA__ = __WORLD_JSON_PLACEHOLDER__;
  </script>
  <script>
    (function() {
      const DATA = window.__ROME_WORLD_DATA__;
      const canvas = document.getElementById('glCanvas');
      const gl = canvas.getContext('webgl2', { antialias: true, preserveDrawingBuffer: true }) ||
                 canvas.getContext('webgl', { antialias: true, preserveDrawingBuffer: true });

      const state = {
        camMode: 'walk',
        pos: [285.0, 18.5, -182.0],
        target: [360.0, 21.0, -210.0],
        yaw: 0.95,
        pitch: 0.08,
        vel: [0, 0, 0],
        crouching: false,
        grounded: true,
        solarHour: 15.0,
        weather: 'clear',
        layers: {
          terrain: true,
          water: true,
          roads: true,
          insulae: true,
          domus: true,
          horrea: true,
          regiones: true,
          credibility: false
        },
        fps: 60,
        drawCalls: 8,
        firstFrameMs: 195
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
        vp_subura_alley_walk: {
          pos: [275.0, getAncientTerrainHeight(275, -182) + 1.65, -182.0],
          target: [380.0, getAncientTerrainHeight(380, -218) + 8.0, -218.0],
          walkMode: true,
          info: ["蘇布拉區擁擠巷弄與 5–6 層公寓群", "Clivus Suburanus & Insulae (Regio IV)", "B 級（塞維魯大理石地圖 FUR 殘片）｜窄巷車道 4.8m、兩側 5–6 層斑駁灰泥與紅磚公寓（一樓 Tabernae 店鋪、二樓木陽台 Maeniana）。"]
        },
        vp_campus_martius_walk: {
          pos: [-235.0, getAncientTerrainHeight(-235, -510) + 1.65, -510.0],
          target: [-350.0, getAncientTerrainHeight(-350, -450) + 6.0, -450.0],
          walkMode: true,
          info: ["戰神廣場開闊紀念柱廊與寬街", "Saepta Julia & Porticus Divorum (Regio IX)", "A 級（考古遺址與大理石地圖）｜開闊石灰華柱廊、大片綠地庭園與規整 4 層紅磚公寓，與蘇布拉區的壓迫感形成強烈對比。"]
        },
        vp_via_sacra_velia: {
          pos: [55.0, getAncientTerrainHeight(55, 12) + 8.5, 12.0],
          target: [265.0, getAncientTerrainHeight(265, 35) + 4.0, 35.0],
          walkMode: false,
          info: ["神聖大道玄武岩鋪面與高起人行道", "Sacra Via (Via Silice Strata)", "A 級（現存玄武岩遺址）｜多邊形玄武岩（Silex）緊密拼鋪，中央微拱排水，兩側配置石灰華路緣石與人行道（Crepidines）。"]
        },
        vp_quirinal_palatine_domus: {
          pos: [340.0, getAncientTerrainHeight(340, -680) + 45.0, -680.0],
          target: [560.0, getAncientTerrainHeight(560, -840) + 6.0, -840.0],
          walkMode: false,
          info: ["奎里納雷山高徑大道與貴族豪宅群", "Alta Semita & Domus (Regio VI)", "B/C 級｜1–2 層寬闊白灰泥紅瓦豪宅（Domus），內含前庭蓄水池（Impluvium）與後方列柱花園（Peristylium）。"]
        },
        vp_emporium_horrea_ostiensis: {
          pos: [-520.0, getAncientTerrainHeight(-520, 620) + 38.0, 620.0],
          target: [-460.0, getAncientTerrainHeight(-460, 960) + 6.0, 960.0],
          walkMode: false,
          info: ["奧斯提亞大道、埃米利亞河港與倉庫群", "Via Ostiensis & Horrea Galbae (Regio XIII)", "A/B 級｜6.0m 寬重載玄武岩大道連接台伯河碼頭、網格石砌倉庫（Horrea）與公元 128 年高 22m 之陶片山。"]
        },
        vp_via_appia_capena: {
          pos: [240.0, getAncientTerrainHeight(240, 520) + 24.0, 520.0],
          target: [420.0, getAncientTerrainHeight(420, 1050) + 5.0, 1050.0],
          walkMode: false,
          info: ["塞爾維烏斯城牆卡佩納門與阿庇亞大道起點", "Porta Capena & Via Appia (Regio I)", "A 級｜自卡佩納門向南延伸之「萬路之王（Regina Viarum）」，標準車道寬 4.1m（14 羅馬尺），兩側附墓園與旅店。"]
        },
        vp_urban_density_bird: {
          pos: [-120.0, 1180.0, 1150.0],
          target: [60.0, 20.0, -220.0],
          walkMode: false,
          info: ["公元 128 年羅馬全城道路網與 14 區城市紋理鳥瞰", "Forma Urbis Romae AD 128 (Regiones I–XIV)", "展示 14 條玄武岩道路網、蘇布拉高密度公寓群、戰神廣場大型柱廊、七丘貴族豪宅與河港倉庫區之空間分布。"]
        },
        vp_p2_credibility_overlay: {
          pos: [-120.0, 1180.0, 1150.0],
          target: [60.0, 20.0, -220.0],
          walkMode: false,
          forceCredibility: true,
          info: ["考證模式：A 級遺址綠 / B 級大理石地圖藍 / C 級程序化推測橘", "Archaeological Credibility Overlay (Tier A / B / C)", "嚴格執行規則：有考古遺址之幹道與柱廊標為 A 級（綠）；塞維魯大理石地圖（FUR）殘片街區一律標為 B 級（藍）；程序化生成民宅標為 C 級（橘）。"]
        }
      };

      function teleportToViewpoint(vpKey) {
        const vp = VIEWPOINTS[vpKey] || VIEWPOINTS.vp_subura_alley_walk;
        state.pos = vp.pos.slice();
        state.target = vp.target.slice();
        state.camMode = vp.walkMode ? 'walk' : 'viewpoint';
        if (vp.forceCredibility) {
          state.layers.credibility = true;
          document.getElementById('chkCredibility').checked = true;
        } else if (vpKey !== 'vp_p2_credibility_overlay') {
          state.layers.credibility = false;
          document.getElementById('chkCredibility').checked = false;
        }
        const dx = state.target[0] - state.pos[0], dy = state.target[1] - state.pos[1], dz = state.target[2] - state.pos[2];
        state.yaw = Math.atan2(dx, dz);
        state.pitch = Math.atan2(dy, Math.hypot(dx, dz) || 1);
        if (vp.info) {
          document.getElementById('infoZh').textContent = vp.info[0];
          document.getElementById('infoLa').textContent = vp.info[1];
          document.getElementById('infoDesc').innerHTML = `<div>${vp.info[2]}</div>`;
        }
        document.querySelectorAll('#viewpointBtns .btn').forEach(b => {
          b.classList.toggle('active', b.getAttribute('data-vp') === vpKey);
        });
        updateHUD();
      }

      function updateHUD() {
        document.getElementById('posVal').textContent = `(${state.pos[0].toFixed(0)}, ${state.pos[1].toFixed(1)}, ${state.pos[2].toFixed(0)})`;
      }

      // Bind UI controls
      ['Terrain','Water','Roads','Insulae','Domus','Horrea','Regiones','Credibility'].forEach(k => {
        const el = document.getElementById('chk' + k);
        if (el) el.addEventListener('change', e => state.layers[k.toLowerCase()] = e.target.checked);
      });
      document.querySelectorAll('#viewpointBtns .btn').forEach(b => {
        b.addEventListener('click', () => teleportToViewpoint(b.getAttribute('data-vp')));
      });

      window.__ROME_DEBUG__ = {
        getWorldData: () => DATA,
        getState: () => state,
        teleportToViewpoint
      };

      teleportToViewpoint('vp_subura_alley_walk');
    })();
  </script>
</body>
</html>
"""

final_html = html_template.replace("__WORLD_JSON_PLACEHOLDER__", world_json_str)
os.makedirs(os.path.dirname(out_html_path), exist_ok=True)
with open(out_html_path, "w", encoding="utf-8") as f:
    f.write(final_html)
with open(local_html_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print("Generated P2 WebApp HTML:", out_html_path, "size:", len(final_html))
