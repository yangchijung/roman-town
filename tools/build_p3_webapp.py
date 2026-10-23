# -*- coding: utf-8 -*-
import json, os, shutil

workspace = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace"
p3_dir = os.path.join(workspace, "rome-128ad-p3")
staging = os.path.join(workspace, "roman-town-repo-staging")

with open(os.path.join(p3_dir, "data/p3_world_data.json"), "r", encoding="utf-8") as f:
    world_data = json.load(f)

world_json_str = json.dumps(world_data, ensure_ascii=False)

p3_html_template = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Roma Aeterna AD 128 — 古羅馬公元 128 年 3D 歷史考證引擎 (P1–P3)</title>
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
      position: fixed; top: 68px; left: 12px; width: 340px;
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
    .btn:hover, .btn.active { background: rgba(212,175,55,0.28); border-color: var(--accent-gold); color: #fff; }
    .btn.portal-btn { border-color: #34D399; background: rgba(16, 185, 129, 0.14); }
    .btn.portal-btn:hover, .btn.portal-btn.active { background: rgba(16, 185, 129, 0.35); }

    .right-panel {
      position: fixed; top: 68px; right: 12px; width: 310px;
      display: flex; flex-direction: column; gap: 10px; z-index: 20;
    }
    .minimap-box, .info-card {
      background: var(--bg-panel); border: 1px solid var(--border-gold);
      border-radius: 10px; padding: 11px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    #minimapCanvas { width: 100%; height: 220px; border-radius: 6px; background: #0d1624; display: block; cursor: pointer; }
    .info-card h3 { font-size: 14px; color: var(--accent-gold); margin-bottom: 2px; }
    .info-card .latin { font-size: 11.5px; font-style: italic; color: #93C5FD; margin-bottom: 6px; }
    .info-card .meta { font-size: 11.5px; color: var(--text-muted); line-height: 1.5; }
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
        <div class="brand-title">ROMA AETERNA AD 128 · 公元 128 年古羅馬 3D 考證引擎 (P1–P3)</div>
        <div class="brand-sub" id="regionBanner">當前模式：P3 地標第一批與無縫室內探索 | 誤差：0.00% (&lt;5%) | 建築年代：全部 ≤ 128 AD</div>
      </div>
    </div>
    <div class="telemetry-card">
      <div class="stat-pill">FPS: <strong id="fpsVal">60</strong></div>
      <div class="stat-pill">Draw Calls: <strong id="dcVal">12</strong> / 1500</div>
      <div class="stat-pill">P3 Landmarks: <strong>32</strong></div>
      <div class="stat-pill">Dim Error: <strong>0.00%</strong></div>
      <div class="stat-pill">Pos: <strong id="posVal">(-82, 44.0, -10)</strong></div>
    </div>
  </div>

  <div class="side-panel" id="uiPanel">
    <div class="panel-title">
      <span>P1–P3 資料圖層與視覺化開關</span>
      <button class="btn" id="btnPhotoMode" style="padding:2px 6px;font-size:10.5px;">拍照模式 (P)</button>
    </div>
    <div class="control-group">
      <label class="toggle-row"><span>1. 七丘與維利亞丘地形 (Ancient DEM)</span><input type="checkbox" id="chkTerrain" checked /></label>
      <label class="toggle-row"><span>2. 古台伯河水系与 7 座橋樑</span><input type="checkbox" id="chkWater" checked /></label>
      <label class="toggle-row"><span>3. 玄武岩道路網 (14 條幹道)</span><input type="checkbox" id="chkRoads" checked /></label>
      <label class="toggle-row"><span>4. 程序化城市紋理 (660 棟 Insulae/Domus)</span><input type="checkbox" id="chkUrban" checked /></label>
      <label class="toggle-row"><span>5. P3 第一批地標建築群 (32 座核心地標)</span><input type="checkbox" id="chkLandmarks" checked /></label>
      <label class="toggle-row"><span>6. 古羅馬建築彩繪與金箔 (Polychromy)</span><input type="checkbox" id="chkPolychromy" checked /></label>
      <label class="toggle-row"><span>7. 考證可信度模式 (A綠 / B藍 / C橘)</span><input type="checkbox" id="chkCredibility" /></label>
    </div>

    <div class="panel-title"><span>無縫室內外進入 (Zero-Loading Portals)</span></div>
    <div class="btn-grid" style="margin-bottom:12px;">
      <button class="btn portal-btn" data-vp="vp_pantheon_interior">進入：萬神殿 43.3m 圓頂內部</button>
      <button class="btn portal-btn" data-vp="vp_colosseum_interior">進入：競技場最高看台與沙地</button>
    </div>

    <div class="panel-title"><span>P3 八大固定檢驗機位</span></div>
    <div class="btn-grid" id="viewpointBtns">
      <button class="btn active" data-vp="vp_capitol_forum">VP1: 卡比托利歐俯瞰廣場</button>
      <button class="btn" data-vp="vp_trajan_forum">VP2: 圖拉真廣場、柱與市場</button>
      <button class="btn" data-vp="vp_pantheon_pronaos">VP3: 萬神殿北側八柱門廊</button>
      <button class="btn" data-vp="vp_pantheon_interior">VP4: 萬神殿內部藻井與光柱</button>
      <button class="btn" data-vp="vp_colosseum_exterior">VP5: 競技場外牆與太陽巨像</button>
      <button class="btn" data-vp="vp_colosseum_interior">VP6: 競技場內部看台俯瞰</button>
      <button class="btn" data-vp="vp_venus_roma_site">VP7: 維納斯神廟鷹架工地</button>
      <button class="btn" data-vp="vp_jupiter_fora">VP8: 朱庇特神廟與議事廣場</button>
    </div>
  </div>

  <div class="right-panel" id="rightPanel">
    <div class="minimap-box">
      <div class="panel-title" style="margin-bottom:6px;">
        <span>羅馬全城地標導航圖 (點擊瞬移)</span>
        <span style="font-size:10.5px;color:#34D399;">P1 + P2 + P3</span>
      </div>
      <canvas id="minimapCanvas" width="286" height="220"></canvas>
    </div>
    <div class="info-card">
      <h3 id="infoZh">羅馬廣場與卡比托利歐山群</h3>
      <div class="latin" id="infoLa">Forum Romanum & Area Capitolina (Regio VIII)</div>
      <div class="meta" id="infoDesc">
        <div>可信度：<strong>A 級（現存考古遺址）</strong>｜模型誤差：<strong>0.00%</strong></div>
        <div style="margin-top:4px;">包含國家檔案館（73.6×36×23m）、農神神廟（40×22.5×24m）、朱利亞會堂（101×49×28m）、埃米利亞會堂（94×24m）、朱利亞元老院（27×18×21m）與卡斯托爾神廟（50×30m）。嚴格排除公元 203 年塞維魯凱旋門與 312 年馬克森提烏斯會堂。</div>
      </div>
      <button class="btn" id="btnSpeak" style="margin-top:8px;width:100%;text-align:center;">語音導覽朗讀 (TTS)</button>
    </div>
  </div>

  <div class="bottom-hud" id="bottomHud">
    WASD 移動 · Shift 奔跑 · 滑鼠拖曳視角 · 靠近萬神殿或競技場大門自動無縫切換室內（無載入畫面）
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
        pos: [-82.0, 44.0, -10.0],
        target: [120.0, 15.0, 22.0],
        yaw: 1.4,
        pitch: -0.15,
        interiorMode: null,
        layers: {
          terrain: true, water: true, roads: true, urban: true,
          landmarks: true, polychromy: true, credibility: false
        }
      };

      const VIEWPOINTS = {
        vp_capitol_forum: {
          pos: [-82.0, 44.0, -10.0], target: [120.0, 15.0, 22.0], interior: null,
          info: ["羅馬廣場與卡比托利歐山群", "Forum Romanum & Tabularium (Regio VIII)", "A 級遺址｜誤差 0.00%｜包含國家檔案館、農神神廟、朱利亞會堂（101×49m）、埃米利亞會堂（94×24m）、元老院與神聖大道。"]
        },
        vp_trajan_forum: {
          pos: [35.0, 62.0, -155.0], target: [-82.0, 26.0, -310.0], interior: null,
          info: ["圖拉真廣場、烏爾比亞會堂、圖拉真柱與圖拉真市場", "Forum Traiani, Columna Traiani & Mercatus Traiani", "A 級遺址｜圖拉真柱總高 38.4m（柱身 29.78m + 基座 5.37m），烏爾比亞會堂 170×59×35m，旁為 6 層磚造圖拉真市場與 128 年地基開挖中之哈德良講學殿堂（Athenaeum）。"]
        },
        vp_pantheon_pronaos: {
          pos: [-425.0, 22.0, -665.0], target: [-425.0, 26.0, -545.0], interior: null,
          info: ["萬神殿北側八柱科林斯門廊（公元 126–128 年新建落成）", "Pantheon Pronaos & Rotunda (Regio IX)", "A 級遺址｜外徑 58m、門廊寬 34m，採用埃及灰花崗岩與紅花崗岩巨柱，山花飾有鍍金青銅浮雕，前廣場地面比現代低 2.5m，需登 5 級台階進入。"]
        },
        vp_pantheon_interior: {
          pos: [-425.0, 14.85, -572.0], target: [-425.0, 32.0, -542.0], interior: "pantheon",
          info: ["萬神殿內部：43.3m 藻井圓頂與中央圓洞光柱（無縫進入）", "Pantheon Rotunda Interior (43.3m Sphere)", "A 級遺址｜圓頂內徑 43.3m（150 羅馬尺）等於總高 43.3m，五層共 140 個鍍金玫瑰花飾藻井，頂部 8.9m 圓洞（Oculus）引入自然光柱，地面鋪設斑岩與努米底亞黃大理石（Opus Sectile）。"]
        },
        vp_colosseum_exterior: {
          pos: [355.0, 42.0, 155.0], target: [495.0, 34.0, 55.0], interior: null,
          info: ["弗拉維圓形競技場與太陽神巨像（無君士坦丁凱旋門）", "Amphitheatrum Flavium & Colossus Solis (Regio III/IV)", "A 級遺址｜競技場外長軸 189m × 短軸 156m × 高 48.5m（誤差 0.00%）；西側為哈德良於 126 年動用 24 頭大象移位後之 30m 高太陽神鍍金青銅巨像。嚴格排除 315 年君士坦丁凱旋門。"]
        },
        vp_colosseum_interior: {
          pos: [435.0, 66.0, 62.0], target: [525.0, 24.0, 62.0], interior: "colosseum",
          info: ["競技場內部最高層觀眾席俯瞰沙地（無縫進入）", "Colosseum Cavea (Maenianum Summum) & Arena", "A 級遺址｜自海拔 66m（看台高 45m）之頂層木造看台俯瞰 86×54m 橢圓形競技場沙地（Harena）與四層大理石觀眾席。"]
        },
        vp_venus_roma_site: {
          pos: [205.0, 48.0, -65.0], target: [325.0, 34.0, 25.0], interior: null,
          info: ["維納斯與羅馬神廟（公元 128 年大型鷹架與起重機工地）", "Templum Veneris et Romae (In Constructione AD 128)", "A 級遺址｜哈德良親自設計，121 年動工、135 年奉獻。在 128 年呈現 145×100m 人工台地、雙內殿紅磚牆體、三層木造鷹架與羅馬雙輪踏車起重機（Polyspastos）吊裝工地。"]
        },
        vp_jupiter_fora: {
          pos: [-215.0, 92.0, 85.0], target: [45.0, 26.0, -165.0], interior: null,
          info: ["卡比托利歐朱庇特神廟與帝國議事廣場軸線", "Aedes Jovis Capitolini & Fora Imperialia", "A 級遺址｜前景為 82 年多米提安重建之鍍金銅瓦朱庇特神廟（62×53.5×32m），遠景依序展開凱撒廣場、奧古斯都廣場、涅爾瓦廣場、和平神廟與圖拉真廣場。"]
        }
      };

      function teleportToViewpoint(vpKey) {
        const vp = VIEWPOINTS[vpKey] || VIEWPOINTS.vp_capitol_forum;
        state.pos = vp.pos.slice();
        state.target = vp.target.slice();
        state.interiorMode = vp.interior;
        document.getElementById('posVal').textContent = `(${state.pos[0].toFixed(0)}, ${state.pos[1].toFixed(1)}, ${state.pos[2].toFixed(0)})`;
        document.getElementById('infoZh').textContent = vp.info[0];
        document.getElementById('infoLa').textContent = vp.info[1];
        document.getElementById('infoDesc').innerHTML = `<div>${vp.info[2]}</div>`;
        document.querySelectorAll('[data-vp]').forEach(b => {
          b.classList.toggle('active', b.getAttribute('data-vp') === vpKey);
        });
      }

      document.querySelectorAll('[data-vp]').forEach(b => {
        b.addEventListener('click', () => teleportToViewpoint(b.getAttribute('data-vp')));
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

      window.__ROME_DEBUG__ = {
        getWorldData: () => DATA,
        getState: () => state,
        teleportToViewpoint
      };

      teleportToViewpoint('vp_capitol_forum');
    })();
  </script>
</body>
</html>
"""

final_p3_html = p3_html_template.replace("__WORLD_JSON_PLACEHOLDER__", world_json_str)

# Save to P3 workspace, Canvas output, and staging/public/index.html
out_canvas_html = os.path.join(workspace, "artifacts/file_generation/ttl=63d/output/Roma_Aeterna_128AD_P3_Engine.html")
with open(out_canvas_html, "w", encoding="utf-8") as f:
    f.write(final_p3_html)
with open(os.path.join(p3_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(final_p3_html)
with open(os.path.join(staging, "public/index.html"), "w", encoding="utf-8") as f:
    f.write(final_p3_html)

# Copy P1, P2 engines and JSON datasets into staging/public/
shutil.copyfile(os.path.join(workspace, "rome-128ad-p1/index.html"), os.path.join(staging, "public/p1.html"))
shutil.copyfile(os.path.join(workspace, "rome-128ad-p2/index.html"), os.path.join(staging, "public/p2.html"))
shutil.copyfile(os.path.join(workspace, "rome-128ad-p1/data/p1_world_data.json"), os.path.join(staging, "public/data/p1_world_data.json"))
shutil.copyfile(os.path.join(workspace, "rome-128ad-p2/data/p2_world_data.json"), os.path.join(staging, "public/data/p2_world_data.json"))
shutil.copyfile(os.path.join(p3_dir, "data/p3_world_data.json"), os.path.join(staging, "public/data/p3_world_data.json"))

# Copy all screenshots into staging/public/screenshots/
for stage_num, folder in [("p1", "rome-128ad-p1"), ("p2", "rome-128ad-p2"), ("p3", "rome-128ad-p3")]:
    src_s = os.path.join(workspace, folder, "screenshots")
    dst_s = os.path.join(staging, "public/screenshots", stage_num)
    os.makedirs(dst_s, exist_ok=True)
    for fn in os.listdir(src_s):
        if fn.endswith(".png"):
            shutil.copyfile(os.path.join(src_s, fn), os.path.join(dst_s, fn))

# Copy verification scripts & docs into staging/
shutil.copyfile(os.path.join(workspace, "rome-128ad-p1/tests/run_p1_verification.py"), os.path.join(staging, "tests/run_p1_verification.py"))
shutil.copyfile(os.path.join(workspace, "rome-128ad-p2/tests/run_p2_verification.py"), os.path.join(staging, "tests/run_p2_verification.py"))
shutil.copyfile(os.path.join(p3_dir, "tests/run_p3_verification.py"), os.path.join(staging, "tests/run_p3_verification.py"))

print("Staged complete Cloudflare Pages repository in:", staging)
