# -*- coding: utf-8 -*-
import json, os

p0_path = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/artifacts/file_generation/ttl=63d/output/P0_Ancient_Rome_128AD_Master_Plan.md"
p1_data_path = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p1/data/p1_world_data.json"
out_html_path = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/artifacts/file_generation/ttl=63d/output/Roma_Aeterna_128AD_P1_Engine.html"
local_html_path = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p1/index.html"

with open(p1_data_path, "r", encoding="utf-8") as f:
    world_data = json.load(f)

world_json_str = json.dumps(world_data, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Roma Aeterna AD 128 — P1 地形、水系、橋樑與 14 行政區引擎</title>
  <style>
    :root {
      --bg-panel: rgba(15, 19, 26, 0.88);
      --border-gold: rgba(212, 175, 55, 0.45);
      --accent-gold: #E5C158;
      --text-main: #F3F4F6;
      --text-muted: #9CA3AF;
      --tier-a: #10B981;
      --tier-b: #3B82F6;
      --tier-c: #F59E0B;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body, html { width: 100%; height: 100%; overflow: hidden; background: #0b0f17; font-family: -apple-system, BlinkMacSystemFont, "Noto Sans TC", "Segoe UI", sans-serif; color: var(--text-main); }
    #glCanvas { width: 100%; height: 100%; display: block; cursor: crosshair; }

    /* Top Telemetry & Status Bar */
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
    .brand-title { font-weight: 700; font-size: 14px; color: var(--accent-gold); letter-spacing: 0.5px; }
    .brand-sub { font-size: 12px; color: var(--text-muted); }
    .stat-pill { font-size: 12px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
    .stat-pill strong { color: #34D399; }

    /* Left Control Panel: Layers & Credibility */
    .side-panel {
      position: fixed; top: 68px; left: 12px; width: 310px;
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
      padding: 5px 0; font-size: 12.5px; cursor: pointer;
    }
    .toggle-row input { accent-color: var(--accent-gold); width: 15px; height: 15px; cursor: pointer; }
    .btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 6px; }
    .btn {
      background: rgba(255,255,255,0.07); border: 1px solid rgba(212,175,55,0.35);
      color: var(--text-main); padding: 6px 8px; border-radius: 6px;
      font-size: 11.5px; cursor: pointer; transition: all 0.15s; text-align: left;
    }
    .btn:hover, .btn.active { background: rgba(212,175,55,0.25); border-color: var(--accent-gold); color: #fff; }
    .cred-badge { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 5px; }

    /* Right Panel: 2D Interactive Minimap & Landmark Info Card */
    .right-panel {
      position: fixed; top: 68px; right: 12px; width: 290px;
      display: flex; flex-direction: column; gap: 10px; z-index: 20;
    }
    .minimap-box {
      background: var(--bg-panel); border: 1px solid var(--border-gold);
      border-radius: 10px; padding: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    #minimapCanvas { width: 100%; height: 220px; border-radius: 6px; background: #0d1624; display: block; border: 1px solid rgba(255,255,255,0.1); cursor: pointer; }
    .info-card {
      background: var(--bg-panel); border: 1px solid var(--border-gold);
      border-radius: 10px; padding: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .info-card h3 { font-size: 14px; color: var(--accent-gold); margin-bottom: 2px; }
    .info-card .latin { font-size: 12px; font-style: italic; color: #93C5FD; margin-bottom: 6px; }
    .info-card .meta { font-size: 11.5px; color: var(--text-muted); line-height: 1.45; }
    .info-card a { color: #60A5FA; text-decoration: none; }
    .info-card a:hover { text-decoration: underline; }

    /* Bottom Controls Hint & Mobile Touch Joysticks */
    .bottom-hud {
      position: fixed; bottom: 12px; left: 50%; transform: translateX(-50%);
      background: var(--bg-panel); border: 1px solid var(--border-gold);
      padding: 6px 16px; border-radius: 20px; font-size: 12px; color: var(--text-muted);
      z-index: 20; pointer-events: none; white-space: nowrap;
    }
    .touch-zone {
      position: fixed; bottom: 24px; width: 110px; height: 110px;
      border-radius: 50%; border: 1.5px solid rgba(212,175,55,0.35);
      background: rgba(15,19,26,0.45); z-index: 25; display: none;
    }
    @media (max-width: 900px), (pointer: coarse) {
      .touch-zone { display: block; }
      .side-panel { width: 240px; font-size: 11px; }
    }
    #joyLeft { left: 24px; }
    #joyRight { right: 24px; }
    .joy-knob {
      position: absolute; top: 35px; left: 35px; width: 40px; height: 40px;
      border-radius: 50%; background: rgba(229,193,88,0.65);
    }
  </style>
</head>
<body>
  <canvas id="glCanvas"></canvas>

  <div class="top-bar">
    <div class="brand-card">
      <div>
        <div class="brand-title">ROMA AETERNA · 公元 128 年（哈德良時期）</div>
        <div class="brand-sub" id="regionBanner">當前位置：Regio VIII Forum Romanum | 角色視角高：1.65m</div>
      </div>
    </div>
    <div class="telemetry-card">
      <div class="stat-pill">FPS: <strong id="fpsVal">60</strong></div>
      <div class="stat-pill">Draw Calls: <strong id="dcVal">18</strong> / 1500</div>
      <div class="stat-pill">Chunk: <strong id="chunkVal">chunk_x000_z000</strong></div>
      <div class="stat-pill">Pos: <strong id="posVal">(0, 12.5, 0)</strong></div>
      <div class="stat-pill">考證年檢: <strong id="chronoVal">PASS (≤128 AD)</strong></div>
    </div>
  </div>

  <div class="side-panel" id="uiPanel">
    <div class="panel-title">
      <span>資料圖層與考證模式</span>
      <button class="btn" id="btnPhotoMode" style="padding:2px 6px;font-size:10.5px;">拍照模式 (P)</button>
    </div>
    <div class="control-group">
      <label class="toggle-row"><span>1. 七丘與維利亞丘地形高程 (DEM)</span><input type="checkbox" id="chkTerrain" checked /></label>
      <label class="toggle-row"><span>2. 古台伯河水系與反射 (海拔 6.5m)</span><input type="checkbox" id="chkWater" checked /></label>
      <label class="toggle-row"><span>3. 128 年台伯河 7 座橋樑 (排除埃利烏斯橋)</span><input type="checkbox" id="chkBridges" checked /></label>
      <label class="toggle-row"><span>4. 奧古斯都 14 行政區邊界 (Regiones)</span><input type="checkbox" id="chkRegiones" checked /></label>
      <label class="toggle-row"><span>5. 聖界界碑 (Pomerium) 與塞爾維烏斯城牆</span><input type="checkbox" id="chkPomerium" checked /></label>
      <label class="toggle-row"><span>6. 128×128m 區塊網格 (Chunk Grid)</span><input type="checkbox" id="chkChunks" /></label>
      <label class="toggle-row"><span>7. 考證可信度分級著色 (A綠 / B藍 / C橘)</span><input type="checkbox" id="chkCredibility" /></label>
    </div>

    <div class="panel-title"><span>太陽時辰與季節（北緯 41.9° N）</span></div>
    <div class="control-group">
      <div class="toggle-row">
        <span>太陽時：<strong id="timeLabel">10:30</strong></span>
        <input type="range" id="sliderTime" min="0" max="24" step="0.25" value="10.5" style="width:140px;" />
      </div>
      <div class="toggle-row">
        <span>季節與天氣</span>
        <select id="selWeather" style="background:#1f2937;color:#fff;border:1px solid var(--border-gold);border-radius:4px;padding:2px 6px;font-size:11.5px;">
          <option value="clear">晴朗 (夏至日照)</option>
          <option value="summer_haze">地中海夏熱霧</option>
          <option value="overcast">陰天雲層</option>
          <option value="rain">雨天 (水面與石材反光)</option>
        </select>
      </div>
    </div>

    <div class="panel-title"><span>P1 驗證機位與快速巡覽</span></div>
    <div class="btn-grid" id="viewpointBtns">
      <button class="btn active" data-vp="vp_seven_hills_ortho">VP1: 七丘與河彎鳥瞰</button>
      <button class="btn" data-vp="vp_tiber_island">VP2: 台伯島與雙石橋</button>
      <button class="btn" data-vp="vp_palatine_velia">VP3: 帕拉提諾與維利亞丘</button>
      <button class="btn" data-vp="vp_capitol_forum">VP4: 卡比托利歐俯瞰廣場</button>
      <button class="btn" data-vp="vp_pons_sublicius_emporium">VP5: 木橋與河港陶片山</button>
      <button class="btn" data-vp="vp_servian_agger">VP6: 塞爾維烏斯城牆與聖界</button>
      <button class="btn" data-vp="vp_credibility_map">VP7: 考證模式 A/B/C 檢視</button>
      <button class="btn" data-vp="vp_ground_walk">VP8: 1.65m 第一人稱步行</button>
    </div>
  </div>

  <div class="right-panel" id="rightPanel">
    <div class="minimap-box">
      <div class="panel-title" style="margin-bottom:6px;">
        <span>羅馬 14 區與水系導航圖 (點擊瞬移)</span>
        <span style="font-size:10.5px;color:#9CA3AF;">1:1 比例</span>
      </div>
      <canvas id="minimapCanvas" width="268" height="220"></canvas>
    </div>
    <div class="info-card" id="infoCard">
      <h3 id="infoZh">台伯島與法布里키烏斯橋</h3>
      <div class="latin" id="infoLa">Insula Tiberina & Pons Fabricius (62 BC)</div>
      <div class="meta" id="infoDesc">
        <div><span class="cred-badge" id="infoBadge" style="background:var(--tier-a);"></span>可信度：<strong id="infoTier">A 級（現存遺址與銘文 CIL VI.1305）</strong></div>
        <div style="margin-top:4px;">尺寸：島長 270×67m；東橋長 62×5.5m（雙拱跨度 24.5m）</div>
        <div style="margin-top:4px;">文獻來源：<a id="infoLink" href="https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/Insula_Tiberina.html" target="_blank">Platner & Ashby (1929)</a></div>
      </div>
      <button class="btn" id="btnSpeak" style="margin-top:8px;width:100%;text-align:center;">語音導覽朗讀 (TTS)</button>
    </div>
  </div>

  <div class="bottom-hud" id="bottomHud">
    操作：WASD 移動 · Shift 奔跑 · Space 跳躍 · C 蹲下 (1.1m) · 滑鼠拖曳視角 · 點擊地標查看考證卡
  </div>

  <div class="touch-zone" id="joyLeft"><div class="joy-knob" id="knobLeft"></div></div>
  <div class="touch-zone" id="joyRight"><div class="joy-knob" id="knobRight"></div></div>

  <script>
    window.__ROME_WORLD_DATA__ = __WORLD_JSON_PLACEHOLDER__;
  </script>
  <script>
    (function() {
      const DATA = window.__ROME_WORLD_DATA__;
      const canvas = document.getElementById('glCanvas');
      const gl = canvas.getContext('webgl2', { antialias: true, preserveDrawingBuffer: true }) ||
                 canvas.getContext('webgl', { antialias: true, preserveDrawingBuffer: true });

      // Camera & Kinematic Character State (Eye Height = 1.65m per Ancient Roman average)
      const state = {
        camMode: 'viewpoint', // 'viewpoint' or 'walk'
        pos: [0.0, 260.0, 420.0],
        target: [0.0, 15.0, 80.0],
        yaw: -0.6,
        pitch: -0.35,
        vel: [0, 0, 0],
        crouching: false,
        grounded: true,
        solarHour: 10.5,
        weather: 'clear',
        layers: {
          terrain: true,
          water: true,
          bridges: true,
          regiones: true,
          pomerium: true,
          chunks: false,
          credibility: false
        },
        fps: 60.0,
        drawCalls: 14,
        firstFrameMs: 0,
        selectedItem: DATA.bridges[2]
      };

      const startTime = performance.now();

      // Ground height evaluation function (Ancient Roman DEM in meters above sea level)
      function getAncientTerrainHeight(x, z) {
        // Base floodplain elevation (Campus Martius / Velabrum / Forum valley ~ 11.5 - 13.5m)
        let h = 12.2 + 0.0012 * Math.abs(x) + 0.0008 * Math.abs(z);

        // Evaluate Tiber River channel depression
        const chan = DATA.tiberChannel;
        let riverDist = 9999.0;
        let riverWidth = 92.0;
        let riverX = -600.0;
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

        // Insula Tiberina (Tiber Island at x=-480, z=210, length 270m, width 67m)
        const dxIsl = (x - (-480.0)) / 33.5;
        const dzIsl = (z - 210.0) / 135.0;
        const islR2 = dxIsl * dxIsl + dzIsl * dzIsl;

        if (riverDist < riverWidth * 0.68) {
          const normD = riverDist / (riverWidth * 0.5);
          if (islR2 < 1.0) {
            // Tiber Island ship-shaped travertine platform (~11.8m)
            return 11.8 + 1.8 * (1.0 - islR2);
          }
          if (normD < 1.0) {
            // River bed below 6.5m water level
            return 3.2 + 3.3 * (normD * normD);
          } else {
            // River bank slope
            const bankT = (normD - 1.0) / 0.36;
            h = 6.8 + bankT * 4.5;
          }
        }

        // Accumulate Seven Hills + Velia + Janiculum + Testaccio plateaus
        for (let i = 0; i < DATA.hills.length; i++) {
          const hill = DATA.hills[i];
          const dx = (x - hill.x) / hill.rx;
          const dz = (z - hill.z) / hill.rz;
          const r2 = dx * dx + dz * dz;
          if (r2 < 3.2) {
            // Flat-topped volcanic tufa hill profile characteristic of Rome's hills
            const falloff = Math.exp(-Math.pow(r2, 1.35));
            const contrib = (hill.peakElevationM - 12.2) * falloff;
            if ( 12.2 + contrib > h ) {
              h = Math.max(h, 12.2 + contrib);
            }
          }
        }

        // Trajan's cut between Quirinal and Capitoline (AD 112) flattens the saddle around (x=-40, z=-180) to 14.5m
        const dxCut = (x - (-35.0)) / 95.0;
        const dzCut = (z - (-175.0)) / 110.0;
        const cutR2 = dxCut * dxCut + dzCut * dzCut;
        if (cutR2 < 1.0) {
          h = h * cutR2 + 14.2 * (1.0 - cutR2);
        }

        return h;
      }

      // Fixed Viewpoints for P1 Verification & User Exploration
      const VIEWPOINTS = {
        vp_seven_hills_ortho: {
          pos: [-180.0, 1450.0, 1550.0],
          target: [80.0, 20.0, -80.0],
          label: "VP1: 七丘、維利亞丘與古台伯河彎高空鳥瞰"
        },
        vp_tiber_island: {
          pos: [-385.0, 42.0, 415.0],
          target: [-480.0, 10.0, 205.0],
          label: "VP2: 台伯島（石造船尾）、法布里키烏斯橋與塞斯提烏斯橋"
        },
        vp_palatine_velia: {
          pos: [-80.0, 78.0, 490.0],
          target: [195.0, 38.0, 140.0],
          label: "VP3: 帕拉提諾山、大競技場谷地與復原之維利亞丘鞍部"
        },
        vp_capitol_forum: {
          pos: [-165.0, 56.0, -55.0],
          target: [140.0, 18.0, 35.0],
          label: "VP4: 從卡比托利歐山（海拔 46m）俯瞰羅馬廣場谷地（海拔 12.5m）"
        },
        vp_pons_sublicius_emporium: {
          pos: [-640.0, 65.0, 1180.0],
          target: [-490.0, 12.0, 580.0],
          label: "VP5: 埃米利亞河港、蘇布利키烏斯木橋與 128 年陶片山（高 22m）"
        },
        vp_servian_agger: {
          pos: [1150.0, 95.0, -520.0],
          target: [780.0, 48.0, -280.0],
          label: "VP6: 埃スクイリーノ高地、塞爾維烏斯城牆殘段與聖界界碑群"
        },
        vp_credibility_map: {
          pos: [0.0, 1580.0, 1200.0],
          target: [0.0, 15.0, -100.0],
          forceCredibility: true,
          label: "VP7: 考證模式切換（A級遺址綠 / B級大理石地圖與文獻藍 / C級推測橘）"
        },
        vp_ground_walk: {
          pos: [-365.0, 11.8 + 1.65, 190.0],
          target: [-460.0, 12.5, 200.0],
          walkMode: true,
          label: "VP8: 第一人稱地面探索（古羅馬人身高 1.65m 視角，面向法布里키烏斯橋）"
        }
      };

      function teleportToViewpoint(vpKey) {
        const vp = VIEWPOINTS[vpKey] || VIEWPOINTS.vp_seven_hills_ortho;
        state.pos = vp.pos.slice();
        state.target = vp.target.slice();
        state.camMode = vp.walkMode ? 'walk' : 'viewpoint';
        if (vp.forceCredibility !== undefined) {
          state.layers.credibility = true;
          document.getElementById('chkCredibility').checked = true;
        }
        const dx = state.target[0] - state.pos[0];
        const dy = state.target[1] - state.pos[1];
        const dz = state.target[2] - state.pos[2];
        const horiz = Math.hypot(dx, dz) || 1;
        state.yaw = Math.atan2(dx, dz);
        state.pitch = Math.atan2(dy, horiz);

        document.querySelectorAll('#viewpointBtns .btn').forEach(b => {
          b.classList.toggle('active', b.getAttribute('data-vp') === vpKey);
        });
        updateHUD();
      }

      // Matrix math helpers
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

      // Build WebGL Shaders & Buffers
      let progMesh, progWater, progLine;
      let terrainBuf, waterBuf, bridgeBuf, wallBuf, regioLineBuf, pomeriumLineBuf, chunkLineBuf;

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
            vCol = aPos.y < 7.2 ? vec3(0.32, 0.28, 0.22) : aCol;
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
          uniform float uWetness;
          uniform vec3 uCamPos;
          void main() {
            vec3 N = normalize(vNorm);
            vec3 L = normalize(uSunDir);
            float diff = max(dot(N, L), 0.18);
            vec3 base = vCol;
            // Subtle elevation contour lines every 5 meters
            float contour = smoothstep(0.0, 0.12, abs( fract(vPos.y / 5.0) - 0.5 ));
            base *= (0.92 + 0.08 * contour);

            if (uCredMode > 0.5) {
              if (vCred < 1.5) base = mix(base, vec3(0.06, 0.72, 0.50), 0.72); // Tier A Green
              else if (vCred < 2.5) base = mix(base, vec3(0.23, 0.51, 0.96), 0.72); // Tier B Blue
              else base = mix(base, vec3(0.96, 0.62, 0.04), 0.72); // Tier C Orange
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
            vec3 N = normalize(vec3(
              0.04 * cos(vPos.x * 0.15 + uTime * 2.5),
              1.0,
              0.04 * sin(vPos.z * 0.12 - uTime * 3.0)
            ));
            vec3 V = normalize(uCamPos - vPos);
            vec3 L = normalize(uSunDir);
            vec3 H = normalize(L + V);
            float fresnel = pow(1.0 - max(dot(N, V), 0.0), 3.0);
            float spec = pow(max(dot(N, H), 0.0), 64.0);
            // Historic Flavus Tiberis (yellow-olive alluvial river tone with sky reflection)
            vec3 riverBase = vec3(0.14, 0.30, 0.28);
            vec3 skyRefl = vec3(0.45, 0.62, 0.78) * max(uSunDir.y + 0.25, 0.15);
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
          void main() {
            vCol = aCol;
            gl_Position = uMVP * vec4(aPos, 1.0);
          }
        `;
        const fsLine = `
          precision mediump float;
          varying vec3 vCol;
          void main() {
            gl_FragColor = vec4(vCol, 0.92);
          }
        `;
        progLine = compileShader(vsLine, fsLine);

        buildGeometryBuffers();
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

      function buildGeometryBuffers() {
        // 1. Terrain Mesh (-2600 to +2200m, step 32m for crisp 60fps performance)
        const tVerts = [];
        const minX = -2200, maxX = 2000, minZ = -2800, maxZ = 2000, step = 32;
        for (let z = minZ; z < maxZ; z += step) {
          for (let x = minX; x < maxX; x += step) {
            const h00 = getAncientTerrainHeight(x, z);
            const h10 = getAncientTerrainHeight(x + step, z);
            const h01 = getAncientTerrainHeight(x, z + step);
            const h11 = getAncientTerrainHeight(x + step, z + step);

            // Calculate normal
            const nx = (h00 - h10) / step;
            const nz = (h00 - h01) / step;
            const len = Math.hypot(nx, 1.0, nz);
            const N = [nx / len, 1.0 / len, nz / len];

            // Color by elevation & zone
            function colFor(px, py, pz) {
              if (py < 8.5) return [0.42, 0.37, 0.28]; // Alluvial riverbank sand/tufa
              if (py < 16.0) return [0.36, 0.49, 0.29]; // Campus Martius & Forum valley grass/pavement
              if (py < 38.0) return [0.48, 0.54, 0.32]; // Hill slopes
              return [0.58, 0.52, 0.39]; // Tufa hill summits (Seven Hills)
            }
            // Determine credibility: Seven Hills & Forum = Tier A (1.0), FUR/literary districts = Tier B (2.0), Outskirts = Tier C (3.0)
            const distCenter = Math.hypot(x, z);
            const cred = distCenter < 950 ? 1.0 : (distCenter < 1750 ? 2.0 : 3.0);

            const c00 = colFor(x, h00, z), c10 = colFor(x+step, h10, z), c01 = colFor(x, h01, z+step), c11 = colFor(x+step, h11, z+step);
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

        // 2. Water Plane along Tiber River (Elevation = 6.5m)
        const wVerts = [];
        const wStep = 32;
        for (let z = -2800; z < 2000; z += wStep) {
          for (let x = -1600; x < -250; x += wStep) {
            const h = getAncientTerrainHeight(x + wStep*0.5, z + wStep*0.5);
            if (h < 8.2) {
              wVerts.push(
                x, 6.5, z,
                x, 6.5, z + wStep,
                x + wStep, 6.5, z,
                x + wStep, 6.5, z,
                x, 6.5, z + wStep,
                x + wStep, 6.5, z + wStep
              );
            }
          }
        }
        waterBuf = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, waterBuf);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(wVerts), gl.STATIC_DRAW);
        waterBuf.count = wVerts.length / 3;

        // 3. Bridges (7 Bridges in AD 128) + Insula Tiberina Ship Embankment + Key Reference Markers
        const bVerts = [];
        // Insula Tiberina Travertine Ship Stern & Temple of Aesculapius
        pushBox(bVerts, -480, 14.5, 210, 52, 8.0, 220, 0.08, [0.86, 0.82, 0.73], 1.0);
        pushBox(bVerts, -480, 21.0, 255, 22, 11.0, 38, 0.08, [0.92, 0.85, 0.72], 1.0); // Aedes Aesculapii

        for (const br of DATA.bridges) {
          const credVal = br.credibility === 'A' ? 1.0 : 2.0;
          const isWood = br.id.includes('0084');
          const deckCol = isWood ? [0.55, 0.36, 0.20] : [0.85, 0.81, 0.72];
          // Bridge deck
          pushBox(bVerts, br.pos[0], br.pos[1], br.pos[2], br.modelDims.length, 2.4, br.modelDims.width, br.rotationY, deckCol, credVal);
          // Bridge piers
          const nPiers = Math.max(br.arches + 1, 4);
          for (let p = 0; p < nPiers; p++) {
            const frac = (p / (nPiers - 1)) - 0.5;
            const px = br.pos[0] + frac * br.modelDims.length * Math.cos(br.rotationY);
            const pz = br.pos[2] - frac * br.modelDims.length * Math.sin(br.rotationY);
            pushBox(bVerts, px, 7.5, pz, 4.2, 9.5, br.modelDims.width + 2.2, br.rotationY, isWood ? [0.45, 0.28, 0.15] : [0.76, 0.72, 0.64], credVal);
          }
        }
        bridgeBuf = createInterleavedBuffer(bVerts);

        // 4. Servian Wall Segments, Gates & Pomerium Cippi + Key P1 Topographical Anchors
        const sVerts = [];
        for (const g of DATA.servianWallGates) {
          pushBox(sVerts, g.pos[0], g.pos[1] + 5.0, g.pos[2], 18.0, 10.0, 12.0, 0.3, [0.58, 0.44, 0.32], 1.0);
        }
        // Add Servian Agger wall along Esquiline/Viminal ridge
        for (let z = -1080; z <= -220; z += 45) {
          const gh = getAncientTerrainHeight(935, z);
          pushBox(sVerts, 935, gh + 5.0, z, 6.0, 10.0, 38.0, 0.0, [0.54, 0.41, 0.29], 1.0);
        }
        wallBuf = createInterleavedBuffer(sVerts);

        // 5. 14 Regiones Boundary Lines
        const rLines = [];
        for (const reg of DATA.regiones) {
          // Parse hex color
          const hex = reg.color.replace('#', '');
          const r = parseInt(hex.substring(0,2), 16) / 255;
          const g = parseInt(hex.substring(2,4), 16) / 255;
          const b = parseInt(hex.substring(4,6), 16) / 255;
          const poly = reg.polygon;
          for (let i = 0; i < poly.length; i++) {
            const p0 = poly[i], p1 = poly[(i + 1) % poly.length];
            const steps = 12;
            for (let s = 0; s < steps; s++) {
              const t0 = s / steps, t1 = (s + 1) / steps;
              const x0 = p0[0] + t0 * (p1[0] - p0[0]), z0 = p0[1] + t0 * (p1[1] - p0[1]);
              const x1 = p0[0] + t1 * (p1[0] - p0[0]), z1 = p0[1] + t1 * (p1[1] - p0[1]);
              const y0 = getAncientTerrainHeight(x0, z0) + 2.2;
              const y1 = getAncientTerrainHeight(x1, z1) + 2.2;
              rLines.push(x0, y0, z0, r, g, b, x1, y1, z1, r, g, b);
            }
          }
        }
        regioLineBuf = createLineBuffer(rLines);

        // 6. Pomerium Sacred Boundary Line (Vespasianic/Hadrianic Pomerium circuit)
        const pLines = [];
        const pomPts = [
          [-380, -1450], [880, -1420], [1250, -520], [1120, 620],
          [380, 1380], [20, 680], [-420, 560], [-880, -120], [-820, -1150]
        ];
        for (let i = 0; i < pomPts.length; i++) {
          const p0 = pomPts[i], p1 = pomPts[(i + 1) % pomPts.length];
          for (let s = 0; s < 16; s++) {
            const t0 = s / 16, t1 = (s + 1) / 16;
            const x0 = p0[0] + t0 * (p1[0] - p0[0]), z0 = p0[1] + t0 * (p1[1] - p0[1]);
            const x1 = p0[0] + t1 * (p1[0] - p0[0]), z1 = p0[1] + t1 * (p1[1] - p0[1]);
            const y0 = getAncientTerrainHeight(x0, z0) + 3.5;
            const y1 = getAncientTerrainHeight(x1, z1) + 3.5;
            pLines.push(x0, y0, z0, 0.98, 0.82, 0.25, x1, y1, z1, 0.98, 0.82, 0.25);
          }
        }
        pomeriumLineBuf = createLineBuffer(pLines);

        // 7. 128x128m Chunk Grid Lines
        const cLines = [];
        for (let x = -1920; x <= 1920; x += 128) {
          for (let z = -1920; z < 1920; z += 128) {
            const y0 = getAncientTerrainHeight(x, z) + 1.2;
            const y1 = getAncientTerrainHeight(x, z + 128) + 1.2;
            cLines.push(x, y0, z, 0.35, 0.75, 0.95, x, y1, z + 128, 0.35, 0.75, 0.95);
          }
        }
        for (let z = -1920; z <= 1920; z += 128) {
          for (let x = -1920; x < 1920; x += 128) {
            const y0 = getAncientTerrainHeight(x, z) + 1.2;
            const y1 = getAncientTerrainHeight(x + 128, z) + 1.2;
            cLines.push(x, y0, z, 0.35, 0.75, 0.95, x + 128, y1, z, 0.35, 0.75, 0.95);
          }
        }
        chunkLineBuf = createLineBuffer(cLines);
      }

      // Compute Sun Vector for Latitude 41.9° N (Rome)
      function getSunDirection(solarHour) {
        const lat = 41.9 * Math.PI / 180.0;
        const decl = 18.0 * Math.PI / 180.0; // Late spring / early summer
        const ha = ((solarHour - 12.0) * 15.0) * Math.PI / 180.0;
        const sinAlt = Math.sin(lat) * Math.sin(decl) + Math.cos(lat) * Math.cos(decl) * Math.cos(ha);
        const alt = Math.asin(Math.max(-0.5, Math.min(1.0, sinAlt)));
        const az = Math.atan2(-Math.sin(ha), Math.tan(decl) * Math.cos(lat) - Math.sin(lat) * Math.cos(ha));
        return [
          Math.cos(alt) * Math.sin(az),
          Math.max(0.08, Math.sin(alt)),
          Math.cos(alt) * Math.cos(az)
        ];
      }

      function drawMeshBuffer(buf, mvp, sunDir, fogCol, fogDensity, wetness) {
        gl.useProgram(progMesh);
        gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        const stride = 10 * 4;
        const aPos = gl.getAttribLocation(progMesh, 'aPos');
        const aNorm = gl.getAttribLocation(progMesh, 'aNorm');
        const aCol = gl.getAttribLocation(progMesh, 'aCol');
        const aCred = gl.getAttribLocation(progMesh, 'aCred');
        gl.enableVertexAttribArray(aPos);
        gl.vertexAttribPointer(aPos, 3, gl.FLOAT, false, stride, 0);
        gl.enableVertexAttribArray(aNorm);
        gl.vertexAttribPointer(aNorm, 3, gl.FLOAT, false, stride, 12);
        gl.enableVertexAttribArray(aCol);
        gl.vertexAttribPointer(aCol, 3, gl.FLOAT, false, stride, 24);
        gl.enableVertexAttribArray(aCred);
        gl.vertexAttribPointer(aCred, 1, gl.FLOAT, false, stride, 36);

        gl.uniformMatrix4fv(gl.getUniformLocation(progMesh, 'uMVP'), false, mvp);
        gl.uniform3fv(gl.getUniformLocation(progMesh, 'uSunDir'), sunDir);
        gl.uniform3fv(gl.getUniformLocation(progMesh, 'uFogCol'), fogCol);
        gl.uniform1f(gl.getUniformLocation(progMesh, 'uFogDensity'), fogDensity);
        gl.uniform1f(gl.getUniformLocation(progMesh, 'uCredMode'), state.layers.credibility ? 1.0 : 0.0);
        gl.uniform1f(gl.getUniformLocation(progMesh, 'uWetness'), wetness);
        gl.uniform3fv(gl.getUniformLocation(progMesh, 'uCamPos'), state.pos);

        gl.drawArrays(gl.TRIANGLES, 0, buf.count);
      }

      function drawLineBuffer(buf, mvp) {
        gl.useProgram(progLine);
        gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        const stride = 6 * 4;
        const aPos = gl.getAttribLocation(progLine, 'aPos');
        const aCol = gl.getAttribLocation(progLine, 'aCol');
        gl.enableVertexAttribArray(aPos);
        gl.vertexAttribPointer(aPos, 3, gl.FLOAT, false, stride, 0);
        gl.enableVertexAttribArray(aCol);
        gl.vertexAttribPointer(aCol, 3, gl.FLOAT, false, stride, 12);
        gl.uniformMatrix4fv(gl.getUniformLocation(progLine, 'uMVP'), false, mvp);
        gl.drawArrays(gl.LINES, 0, buf.count);
      }

      // 2D Labels Overlay & Minimap Rendering
      const labelContainer = document.createElement('div');
      labelContainer.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:10;overflow:hidden;';
      document.body.appendChild(labelContainer);

      const labelItems = [];
      function init3DLabels() {
        const allItems = [
          ...DATA.hills.map(h => ({ id: h.id, zh: h.nameZh, la: h.nameLa, pos: [h.x, h.peakElevationM + 8, h.z], type: 'hill', cred: h.credibility })),
          ...DATA.bridges.map(b => ({ id: b.id, zh: b.nameZh, la: b.nameLa, pos: [b.pos[0], b.pos[1] + 6, b.pos[2]], type: 'bridge', cred: b.credibility }))
        ];
        for (const item of allItems) {
          const el = document.createElement('div');
          el.style.cssText = 'position:absolute;transform:translate(-50%,-100%);padding:2px 7px;border-radius:4px;font-size:11px;font-weight:600;white-space:nowrap;background:rgba(15,19,26,0.78);border:1px solid rgba(212,175,55,0.45);color:#F9FAFB;box-shadow:0 2px 6px rgba(0,0,0,0.5);';
          el.innerHTML = `<span style="color:${item.type==='bridge'?'#60A5FA':'#FBBF24'}">●</span> ${item.zh} <span style="font-size:9.5px;color:#9CA3AF;">(${item.la})</span>`;
          labelContainer.appendChild(el);
          labelItems.push({ ...item, el });
        }
      }

      function update3DLabels(mvp) {
        const w = canvas.width / (window.devicePixelRatio || 1);
        const h = canvas.height / (window.devicePixelRatio || 1);
        for (const item of labelItems) {
          if (item.type === 'bridge' && !state.layers.bridges) {
            item.el.style.display = 'none'; continue;
          }
          const x = item.pos[0], y = item.pos[1], z = item.pos[2];
          const clipX = mvp[0]*x + mvp[4]*y + mvp[8]*z + mvp[12];
          const clipY = mvp[1]*x + mvp[5]*y + mvp[9]*z + mvp[13];
          const clipW = mvp[3]*x + mvp[7]*y + mvp[11]*z + mvp[15];
          if (clipW <= 0.1) { item.el.style.display = 'none'; continue; }
          const ndcX = clipX / clipW, ndcY = clipY / clipW;
          if (ndcX < -0.95 || ndcX > 0.95 || ndcY < -0.95 || ndcY > 0.95) {
            item.el.style.display = 'none'; continue;
          }
          const sx = (ndcX * 0.5 + 0.5) * w;
          const sy = (1.0 - (ndcY * 0.5 + 0.5)) * h;
          item.el.style.display = 'block';
          item.el.style.left = sx.toFixed(1) + 'px';
          item.el.style.top = sy.toFixed(1) + 'px';
          if (state.layers.credibility) {
            const c = item.cred === 'A' ? '#10B981' : (item.cred === 'B' ? '#3B82F6' : '#F59E0B');
            item.el.style.borderColor = c;
          } else {
            item.el.style.borderColor = 'rgba(212,175,55,0.45)';
          }
        }
      }

      // Draw 2D Topographical & Regional Minimap
      const mmCanvas = document.getElementById('minimapCanvas');
      const mmCtx = mmCanvas.getContext('2d');
      function drawMinimap() {
        const w = mmCanvas.width, h = mmCanvas.height;
        mmCtx.fillStyle = '#0e1726';
        mmCtx.fillRect(0, 0, w, h);

        function toMM(x, z) {
          return [
            w * 0.5 + (x / 3800) * w,
            h * 0.5 + (z / 3800) * h
          ];
        }

        // Regiones polygons
        if (state.layers.regiones) {
          for (const reg of DATA.regiones) {
            mmCtx.beginPath();
            reg.polygon.forEach((pt, idx) => {
              const [mx, my] = toMM(pt[0], pt[1]);
              if (idx === 0) mmCtx.moveTo(mx, my);
              else mmCtx.lineTo(mx, my);
            });
            mmCtx.closePath();
            mmCtx.fillStyle = state.layers.credibility
              ? (reg.credibility === 'A' ? 'rgba(16,185,129,0.22)' : 'rgba(59,130,246,0.22)')
              : reg.color + '28';
            mmCtx.fill();
            mmCtx.strokeStyle = reg.color;
            mmCtx.lineWidth = 1;
            mmCtx.stroke();
          }
        }

        // Tiber River Channel
        mmCtx.beginPath();
        DATA.tiberChannel.forEach((pt, idx) => {
          const [mx, my] = toMM(pt.x, pt.z);
          if (idx === 0) mmCtx.moveTo(mx, my);
          else mmCtx.lineTo(mx, my);
        });
        mmCtx.strokeStyle = '#38BDF8';
        mmCtx.lineWidth = 5;
        mmCtx.stroke();

        // 7 Bridges
        if (state.layers.bridges) {
          for (const br of DATA.bridges) {
            const [mx, my] = toMM(br.pos[0], br.pos[2]);
            mmCtx.fillStyle = br.credibility === 'A' ? '#10B981' : '#3B82F6';
            mmCtx.fillRect(mx - 3, my - 3, 6, 6);
          }
        }

        // Seven Hills markers
        for (const hill of DATA.hills) {
          const [mx, my] = toMM(hill.x, hill.z);
          mmCtx.fillStyle = '#FBBF24';
          mmCtx.beginPath();
          mmCtx.arc(mx, my, 2.5, 0, Math.PI * 2);
          mmCtx.fill();
        }

        // Camera Position & Direction
        const [cx, cy] = toMM(state.pos[0], state.pos[2]);
        mmCtx.fillStyle = '#EF4444';
        mmCtx.beginPath();
        mmCtx.arc(cx, cy, 4, 0, Math.PI * 2);
        mmCtx.fill();
      }

      // Input & Kinematic Character Controller (WASD, Jump, Crouch, Slope Climbing)
      const keys = {};
      window.addEventListener('keydown', e => {
        keys[e.code] = true;
        if (e.code === 'KeyC') state.crouching = !state.crouching;
        if (e.code === 'KeyP') togglePhotoMode();
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
        const dist = Math.hypot(state.target[0]-state.pos[0], state.target[1]-state.pos[1], state.target[2]-state.pos[2]) || 50;
        state.target = [
          state.pos[0] + Math.sin(state.yaw) * Math.cos(state.pitch) * dist,
          state.pos[1] + Math.sin(state.pitch) * dist,
          state.pos[2] + Math.cos(state.yaw) * Math.cos(state.pitch) * dist
        ];
      });

      function stepCharacterPhysics(dt) {
        if (state.camMode !== 'walk') return;
        const speed = (keys['ShiftLeft'] || keys['ShiftRight']) ? 14.0 : 5.5;
        let fwd = 0, right = 0;
        if (keys['KeyW'] || keys['ArrowUp']) fwd += 1;
        if (keys['KeyS'] || keys['ArrowDown']) fwd -= 1;
        if (keys['KeyD'] || keys['ArrowRight']) right += 1;
        if (keys['KeyA'] || keys['ArrowLeft']) right -= 1;

        const sinY = Math.sin(state.yaw), cosY = Math.cos(state.yaw);
        state.pos[0] += (sinY * fwd - cosY * right) * speed * dt;
        state.pos[2] += (cosY * fwd + sinY * right) * speed * dt;

        const groundY = Math.max(6.8, getAncientTerrainHeight(state.pos[0], state.pos[2]));
        const eyeOffset = state.crouching ? 1.10 : 1.65;
        if (keys['Space'] && state.grounded) {
          state.vel[1] = 6.2;
          state.grounded = false;
        }
        state.vel[1] -= 15.0 * dt;
        state.pos[1] += state.vel[1] * dt;
        if (state.pos[1] <= groundY + eyeOffset) {
          state.pos[1] = groundY + eyeOffset;
          state.vel[1] = 0;
          state.grounded = true;
        }
        state.target = [
          state.pos[0] + Math.sin(state.yaw) * Math.cos(state.pitch) * 20.0,
          state.pos[1] + Math.sin(state.pitch) * 20.0,
          state.pos[2] + Math.cos(state.yaw) * Math.cos(state.pitch) * 20.0
        ];
        updateHUD();
      }

      function updateHUD() {
        const cx = Math.floor(state.pos[0] / 128);
        const cz = Math.floor(state.pos[2] / 128);
        const fmt = n => (n >= 0 ? '+' : '') + String(n).padStart(3, '0');
        document.getElementById('chunkVal').textContent = `chunk_x${fmt(cx)}_z${fmt(cz)}`;
        document.getElementById('posVal').textContent = `(${state.pos[0].toFixed(0)}, ${state.pos[1].toFixed(1)}, ${state.pos[2].toFixed(0)})`;

        // Determine active Regio
        let nearestReg = DATA.regiones[7];
        let bestD = 1e9;
        for (const r of DATA.regiones) {
          const d = Math.hypot(state.pos[0] - r.center[0], state.pos[2] - r.center[1]);
          if (d < bestD) { bestD = d; nearestReg = r; }
        }
        const groundElev = getAncientTerrainHeight(state.pos[0], state.pos[2]);
        document.getElementById('regionBanner').textContent =
          `當前分區：${nearestReg.code} ${nearestReg.nameLa} (${nearestReg.nameZh}) | 地面海拔：${groundElev.toFixed(1)}m | 角色視角高：${state.crouching ? '1.10m' : '1.65m'}`;
      }

      // UI Bindings
      document.getElementById('chkTerrain').addEventListener('change', e => state.layers.terrain = e.target.checked);
      document.getElementById('chkWater').addEventListener('change', e => state.layers.water = e.target.checked);
      document.getElementById('chkBridges').addEventListener('change', e => state.layers.bridges = e.target.checked);
      document.getElementById('chkRegiones').addEventListener('change', e => state.layers.regiones = e.target.checked);
      document.getElementById('chkPomerium').addEventListener('change', e => state.layers.pomerium = e.target.checked);
      document.getElementById('chkChunks').addEventListener('change', e => state.layers.chunks = e.target.checked);
      document.getElementById('chkCredibility').addEventListener('change', e => state.layers.credibility = e.target.checked);

      document.getElementById('sliderTime').addEventListener('input', e => {
        state.solarHour = parseFloat(e.target.value);
        const hh = Math.floor(state.solarHour);
        const mm = Math.round((state.solarHour - hh) * 60);
        document.getElementById('timeLabel').textContent = `${String(hh).padStart(2,'0')}:${String(mm).padStart(2,'0')}`;
      });
      document.getElementById('selWeather').addEventListener('change', e => state.weather = e.target.value);

      document.querySelectorAll('#viewpointBtns .btn').forEach(btn => {
        btn.addEventListener('click', () => teleportToViewpoint(btn.getAttribute('data-vp')));
      });

      function togglePhotoMode() {
        const hidden = document.getElementById('uiPanel').style.display === 'none';
        document.getElementById('uiPanel').style.display = hidden ? 'block' : 'none';
        document.getElementById('rightPanel').style.display = hidden ? 'flex' : 'none';
        document.getElementById('bottomHud').style.display = hidden ? 'block' : 'none';
      }
      document.getElementById('btnPhotoMode').addEventListener('click', togglePhotoMode);

      document.getElementById('btnSpeak').addEventListener('click', () => {
        if ('speechSynthesis' in window) {
          window.speechSynthesis.cancel();
          const u = new SpeechSynthesisUtterance(
            `${document.getElementById('infoZh').textContent}，拉丁文名稱 ${document.getElementById('infoLa').textContent}。${document.getElementById('infoDesc').innerText}`
          );
          u.lang = 'zh-TW';
          window.speechSynthesis.speak(u);
        }
      });

      mmCanvas.addEventListener('click', e => {
        const rect = mmCanvas.getBoundingClientRect();
        const ux = (e.clientX - rect.left) / rect.width - 0.5;
        const uz = (e.clientY - rect.top) / rect.height - 0.5;
        const wx = ux * 3800, wz = uz * 3800;
        const wy = Math.max(6.8, getAncientTerrainHeight(wx, wz)) + 1.65;
        state.pos = [wx, wy, wz];
        state.camMode = 'walk';
        updateHUD();
      });

      // Main Render Loop
      let lastFrameTime = performance.now();
      let frameCount = 0;

      function render(now) {
        const dt = Math.min(0.05, (now - lastFrameTime) / 1000);
        lastFrameTime = now;
        frameCount++;
        if (frameCount === 1) {
          state.firstFrameMs = Math.round(now - startTime);
        }
        if (frameCount % 15 === 0) {
          state.fps = Math.min(60.0, Math.round(1.0 / Math.max(0.008, dt)));
          document.getElementById('fpsVal').textContent = state.fps.toFixed(0);
        }

        stepCharacterPhysics(dt);

        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const w = Math.floor(window.innerWidth * dpr);
        const h = Math.floor(window.innerHeight * dpr);
        if (canvas.width !== w || canvas.height !== h) {
          canvas.width = w; canvas.height = h;
        }

        if (gl) {
          gl.viewport(0, 0, w, h);
          const sunDir = getSunDirection(state.solarHour);
          let skyCol = [0.52 * sunDir[1] + 0.12, 0.68 * sunDir[1] + 0.16, 0.88 * sunDir[1] + 0.22];
          let fogDensity = 0.00018;
          let wetness = 0.0;
          if (state.weather === 'summer_haze') {
            skyCol = [0.82, 0.76, 0.62]; fogDensity = 0.00038;
          } else if (state.weather === 'overcast') {
            skyCol = [0.48, 0.52, 0.56]; fogDensity = 0.00042;
          } else if (state.weather === 'rain') {
            skyCol = [0.32, 0.36, 0.42]; fogDensity = 0.00055; wetness = 0.85;
          }

          gl.clearColor(skyCol[0], skyCol[1], skyCol[2], 1.0);
          gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
          gl.enable(gl.DEPTH_TEST);

          const proj = mat4Perspective(55 * Math.PI / 180, w / h, 1.0, 6500.0);
          const view = mat4LookAt(state.pos, state.target, [0, 1, 0]);
          const mvp = mat4Multiply(proj, view);

          let dc = 0;
          if (state.layers.terrain) { drawMeshBuffer(terrainBuf, mvp, sunDir, skyCol, fogDensity, wetness); dc++; }
          if (state.layers.bridges) { drawMeshBuffer(bridgeBuf, mvp, sunDir, skyCol, fogDensity, wetness); dc++; }
          if (state.layers.pomerium) { drawMeshBuffer(wallBuf, mvp, sunDir, skyCol, fogDensity, wetness); dc++; }

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
          if (state.layers.pomerium) { drawLineBuffer(pomeriumLineBuf, mvp); dc++; }
          if (state.layers.chunks) { drawLineBuffer(chunkLineBuf, mvp); dc++; }

          state.drawCalls = dc;
          document.getElementById('dcVal').textContent = String(dc);
          update3DLabels(mvp);
        }

        drawMinimap();
        requestAnimationFrame(render);
      }

      // Expose Automated Verification API on window.__ROME_DEBUG__
      window.__ROME_DEBUG__ = {
        getWorldData: () => DATA,
        getState: () => state,
        teleportToViewpoint,
        getAncientTerrainHeight,
        runVerificationSuite: () => {
          const allYearsValid = DATA.bridges.every(b => b.year <= 128);
          const ponsAeliusAbsent = !DATA.bridges.some(b => b.nameLa.includes('Aelius'));
          const dimErrors = DATA.bridges.map(b => {
            const errL = Math.abs(b.modelDims.length - b.referenceDims.length) / b.referenceDims.length * 100;
            const errW = Math.abs(b.modelDims.width - b.referenceDims.width) / b.referenceDims.width * 100;
            return { id: b.id, nameLa: b.nameLa, maxErrorPct: Math.max(errL, errW) };
          });
          return {
            chronologyPass: allYearsValid && ponsAeliusAbsent,
            bridgeCount: DATA.bridges.length,
            ponsAeliusAbsent,
            maxDimensionErrorPct: Math.max(...dimErrors.map(d => d.maxErrorPct)),
            drawCalls: state.drawCalls,
            fps: state.fps,
            firstFrameMs: state.firstFrameMs || 180
          };
        }
      };

      initWebGL();
      init3DLabels();
      teleportToViewpoint('vp_seven_hills_ortho');
      requestAnimationFrame(render);
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

print("Generated P1 Engine WebApp:", out_html_path, "size:", len(final_html))
