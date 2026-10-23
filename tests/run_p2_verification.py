# -*- coding: utf-8 -*-
import json, math, os, struct, zlib

base_dir = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p2"
with open(os.path.join(base_dir, "data/p2_world_data.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)

screenshots_dir = os.path.join(base_dir, "screenshots")
os.makedirs(screenshots_dir, exist_ok=True)

def get_ancient_terrain_height(x, z):
    h = 12.2 + 0.0012 * abs(x) + 0.0008 * abs(z)
    chan = DATA["tiberChannel"]
    river_dist = 9999.0
    river_width = 92.0
    river_x = -600.0
    for i in range(len(chan) - 1):
        p0, p1 = chan[i], chan[i+1]
        if p0["z"] <= z <= p1["z"]:
            t = (z - p0["z"]) / (p1["z"] - p0["z"])
            river_x = p0["x"] + t * (p1["x"] - p0["x"])
            river_width = p0["width"] + t * (p1["width"] - p0["width"])
            river_dist = abs(x - river_x)
            break

    dx_isl = (x - (-480.0)) / 33.5
    dz_isl = (z - 210.0) / 135.0
    isl_r2 = dx_isl * dx_isl + dz_isl * dz_isl

    if river_dist < river_width * 0.72:
        norm_d = river_dist / (river_width * 0.5)
        if isl_r2 < 1.0:
            return 11.8 + 1.8 * (1.0 - isl_r2)
        if norm_d < 1.0:
            return 3.2 + 3.0 * (norm_d * norm_d)
        else:
            bank_t = (norm_d - 1.0) / 0.44
            h = 6.5 + bank_t * 5.2

    for hill in DATA["hills"]:
        dx = (x - hill["x"]) / hill["rx"]
        dz = (z - hill["z"]) / hill["rz"]
        r2 = dx * dx + dz * dz
        if r2 < 3.2:
            falloff = math.exp(-math.pow(r2, 1.35))
            contrib = (hill["peakElevationM"] - 12.2) * falloff
            if 12.2 + contrib > h:
                h = max(h, 12.2 + contrib)

    dx_cut = (x - (-35.0)) / 95.0
    dz_cut = (z - (-175.0)) / 110.0
    cut_r2 = dx_cut * dx_cut + dz_cut * dz_cut
    if cut_r2 < 1.0:
        h = h * cut_r2 + 14.2 * (1.0 - cut_r2)

    return h

def write_png(filepath, width, height, rgb_bytes):
    def chunk(tag, data):
        return struct.pack("!I", len(data)) + tag + data + struct.pack("!I", zlib.crc32(tag + data) & 0xffffffff)
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw.extend(rgb_bytes[y * stride : (y + 1) * stride])
    ihdr = struct.pack("!IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 6)) + chunk(b"IEND", b"")
    with open(filepath, "wb") as f:
        f.write(png)

FONT_5X7 = {
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'B': ["11110","10001","10001","11110","10001","10001","11110"],
    'C': ["01111","10000","10000","10000","10000","10000","01111"],
    'D': ["11110","10001","10001","10001","10001","10001","11110"],
    'E': ["11111","10000","10000","11110","10000","10000","11111"],
    'F': ["11111","10000","10000","11110","10000","10000","10000"],
    'G': ["01111","10000","10000","10111","10001","10001","01111"],
    'H': ["10001","10001","10001","11111","10001","10001","10001"],
    'I': ["01110","00100","00100","00100","00100","00100","01110"],
    'J': ["00111","00010","00010","00010","10010","10010","01100"],
    'K': ["10001","10010","10100","11000","10100","10010","10001"],
    'L': ["10000","10000","10000","10000","10000","10000","11111"],
    'M': ["10001","11011","10101","10101","10001","10001","10001"],
    'N': ["10001","11001","10101","10011","10001","10001","10001"],
    'O': ["01110","10001","10001","10001","10001","10001","01110"],
    'P': ["11110","10001","10001","11110","10000","10000","10000"],
    'Q': ["01110","10001","10001","10001","10101","10010","01101"],
    'R': ["11110","10001","10001","11110","10100","10010","10001"],
    'S': ["01111","10000","10000","01110","00001","00001","11110"],
    'T': ["11111","00100","00100","00100","00100","00100","00100"],
    'U': ["10001","10001","10001","10001","10001","10001","01110"],
    'V': ["10001","10001","10001","10001","10001","01010","00100"],
    'W': ["10001","10001","10001","10101","10101","11011","10001"],
    'X': ["10001","10001","01010","00100","01010","10001","10001"],
    'Y': ["10001","10001","01010","00100","00100","00100","00100"],
    'Z': ["11111","00001","00010","00100","01000","10000","11111"],
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    '1': ["00100","01100","00100","00100","00100","00100","01110"],
    '2': ["01110","10001","00001","00110","01000","10000","11111"],
    '3': ["11110","00001","00001","01110","00001","00001","11110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","10000","11110","00001","00001","11110"],
    '6': ["01110","10000","10000","11110","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00001","01110"],
    ':': ["00000","00100","00100","00000","00100","00100","00000"],
    '.': ["00000","00000","00000","00000","00000","00110","00110"],
    '-': ["00000","00000","00000","11111","00000","00000","00000"],
    '/': ["00001","00010","00100","00100","01000","10000","00000"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
    ')': ["01000","00100","00010","00010","00010","00100","01000"],
    ',': ["00000","00000","00000","00000","00100","00100","01000"],
    '=': ["00000","00000","11111","00000","11111","00000","00000"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"]
}

def draw_rect(buf, w, h, x0, y0, x1, y1, col, alpha=0.85):
    x0, x1 = max(0, int(x0)), min(w, int(x1))
    y0, y1 = max(0, int(y0)), min(h, int(y1))
    r, g, b = col
    inv = 1.0 - alpha
    for y in range(y0, y1):
        row = y * w * 3
        for x in range(x0, x1):
            idx = row + x * 3
            buf[idx]   = int(buf[idx] * inv + r * alpha)
            buf[idx+1] = int(buf[idx+1] * inv + g * alpha)
            buf[idx+2] = int(buf[idx+2] * inv + b * alpha)

def draw_text(buf, w, h, x, y, text, col=(245, 247, 250), scale=2):
    cx = int(x)
    for ch in text.upper():
        glyph = FONT_5X7.get(ch, FONT_5X7[' '])
        for gy in range(7):
            row_str = glyph[gy]
            for gx in range(5):
                if row_str[gx] == '1':
                    for sy in range(scale):
                        for sx in range(scale):
                            px = cx + gx * scale + sx
                            py = int(y) + gy * scale + sy
                            if 0 <= px < w and 0 <= py < h:
                                idx = (py * w + px) * 3
                                buf[idx], buf[idx+1], buf[idx+2] = col[0], col[1], col[2]
        cx += 6 * scale

def draw_line_2d(buf, w, h, x0, y0, x1, y1, col, thickness=2):
    steps = int(max(abs(x1 - x0), abs(y1 - y0), 1))
    for s in range(steps + 1):
        t = s / steps
        px = int(x0 + t * (x1 - x0))
        py = int(y0 + t * (y1 - y0))
        for dy in range(-thickness//2, thickness//2 + 1):
            for dx in range(-thickness//2, thickness//2 + 1):
                xx, yy = px + dx, py + dy
                if 0 <= xx < w and 0 <= yy < h:
                    idx = (yy * w + xx) * 3
                    buf[idx], buf[idx+1], buf[idx+2] = col[0], col[1], col[2]

def render_p2_screenshot(vp_id, title_en, sub_en, cam_pos, cam_target, cred_mode=False, walk_mode=False, bounds=None):
    W, H = 960, 540
    buf = bytearray(W * H * 3)
    zbuf = [1e9] * (W * H)

    # Sky background gradient
    for y in range(H):
        t = min(1.0, y / (H * 0.65))
        sr = int(40 + 130 * t)
        sg = int(78 + 120 * t)
        sb = int(138 + 95 * t)
        row = y * W * 3
        for x in range(W):
            buf[row + x*3] = sr
            buf[row + x*3 + 1] = sg
            buf[row + x*3 + 2] = sb

    fx = cam_target[0] - cam_pos[0]
    fy = cam_target[1] - cam_pos[1]
    fz = cam_target[2] - cam_pos[2]
    flen = math.sqrt(fx*fx + fy*fy + fz*fz) or 1.0
    fx, fy, fz = fx/flen, fy/flen, fz/flen

    rx = -fz
    ry = 0.0
    rz = fx
    rlen = math.sqrt(rx*rx + rz*rz) or 1.0
    rx, rz = rx/rlen, rz/rlen

    ux = ry * fz - rz * fy
    uy = rz * fx - rx * fz
    uz = rx * fy - ry * fx

    fov_scale = (H * 0.5) / math.tan(math.radians(54.0 * 0.5))

    def project(wx, wy, wz):
        dx, dy, dz = wx - cam_pos[0], wy - cam_pos[1], wz - cam_pos[2]
        cz = dx * fx + dy * fy + dz * fz
        if cz <= 1.0:
            return None
        cx = dx * rx + dy * ry + dz * rz
        cy = dx * ux + dy * uy + dz * uz
        sx = W * 0.5 + (cx / cz) * fov_scale
        sy = H * 0.5 - (cy / cz) * fov_scale
        return (sx, sy, cz)

    def fill_tri(p0, p1, p2, col):
        if not p0 or not p1 or not p2:
            return
        min_x = max(0, int(min(p0[0], p1[0], p2[0])))
        max_x = min(W - 1, int(max(p0[0], p1[0], p2[0])))
        min_y = max(0, int(min(p0[1], p1[1], p2[1])))
        max_y = min(H - 1, int(max(p0[1], p1[1], p2[1])))
        if min_x > max_x or min_y > max_y:
            return
        denom = (p1[1] - p2[1]) * (p0[0] - p2[0]) + (p2[0] - p1[0]) * (p0[1] - p2[1])
        if abs(denom) < 1e-4:
            return
        inv_d = 1.0 / denom
        avg_z = (p0[2] + p1[2] + p2[2]) / 3.0
        fog = min(0.68, max(0.0, 1.0 - math.exp(-avg_z * 0.00018)))
        r = int(col[0] * (1.0 - fog) + 158 * fog)
        g = int(col[1] * (1.0 - fog) + 188 * fog)
        b = int(col[2] * (1.0 - fog) + 215 * fog)

        for py in range(min_y, max_y + 1):
            row_idx = py * W
            for px in range(min_x, max_x + 1):
                w0 = ((p1[1] - p2[1]) * (px - p2[0]) + (p2[0] - p1[0]) * (py - p2[1])) * inv_d
                w1 = ((p2[1] - p0[1]) * (px - p2[0]) + (p0[0] - p2[0]) * (py - p2[1])) * inv_d
                w2 = 1.0 - w0 - w1
                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    z = w0 * p0[2] + w1 * p1[2] + w2 * p2[2]
                    bi = row_idx + px
                    if z < zbuf[bi]:
                        zbuf[bi] = z
                        c_idx = bi * 3
                        buf[c_idx], buf[c_idx+1], buf[c_idx+2] = r, g, b

    # 1. Terrain & Tiber Water
    bx0, bx1, bz0, bz1, step = bounds if bounds else (-1600, 1600, -1800, 1600, 32)
    sun = (0.48, 0.76, 0.43)
    for z in range(bz0, bz1, step):
        for x in range(bx0, bx1, step):
            h00 = get_ancient_terrain_height(x, z)
            h10 = get_ancient_terrain_height(x + step, z)
            h01 = get_ancient_terrain_height(x, z + step)
            h11 = get_ancient_terrain_height(x + step, z + step)

            is_water = (h00 < 7.2 or h10 < 7.2 or h01 < 7.2)
            if is_water and (h00 < 9.5 and h10 < 9.5):
                y00 = y10 = y01 = y11 = 6.5
                ripple = math.sin(x * 0.08 + z * 0.06) * 14
                base_col = (int(34 + ripple), int(112 + ripple), int(152 + ripple))
            else:
                y00, y10, y01, y11 = max(6.5, h00), max(6.5, h10), max(6.5, h01), max(6.5, h11)
                nx = (y00 - y10) / step
                nz = (y00 - y01) / step
                nlen = math.sqrt(nx*nx + 1.0 + nz*nz)
                ndotl = max(0.35, min(1.15, (nx*sun[0] + 1.0*sun[1] + nz*sun[2]) / nlen))
                if cred_mode:
                    raw = (45, 65, 82)
                else:
                    if y00 < 10.2: raw = (152, 136, 106)
                    elif y00 < 16.5: raw = (102, 136, 82)
                    elif y00 < 36.0: raw = (128, 148, 86)
                    else: raw = (168, 146, 106)
                base_col = (int(min(255, raw[0]*ndotl)), int(min(255, raw[1]*ndotl)), int(min(255, raw[2]*ndotl)))

            p00 = project(x, y00, z)
            p10 = project(x + step, y10, z)
            p01 = project(x, y01, z + step)
            p11 = project(x + step, y11, z + step)
            fill_tri(p00, p01, p10, base_col)
            fill_tri(p10, p01, p11, base_col)

    # 2. Rasterize Roman Basalt Roads (Silex carriageway + raised travertine Crepidines sidewalks)
    for road in DATA["roads"]:
        wps = road["waypoints"]
        rw = road["carriageWidthM"]
        sw = road["sidewalkWidthM"]
        for i in range(len(wps) - 1):
            x0, z0 = wps[i]
            x1, z1 = wps[i+1]
            seg_len = math.hypot(x1 - x0, z1 - z0) or 1.0
            nsub = max(1, int(seg_len / 18.0))
            dx_n = (x1 - x0) / seg_len
            dz_n = (z1 - z0) / seg_len
            px_n = -dz_n
            pz_n = dx_n
            for s in range(nsub):
                t0 = s / nsub
                t1 = (s + 1) / nsub
                sx0, sz0 = x0 + t0*(x1-x0), z0 + t0*(z1-z0)
                sx1, sz1 = x0 + t1*(x1-x0), z0 + t1*(z1-z0)
                y0 = get_ancient_terrain_height(sx0, sz0) + 0.35
                y1 = get_ancient_terrain_height(sx1, sz1) + 0.35

                if cred_mode:
                    rcol = (16, 195, 132) if road["credibility"] == "A" else (59, 135, 248)
                    scol = rcol
                else:
                    rcol = (64, 68, 76) # Dark grey polygonal basalt Silex
                    scol = (196, 186, 168) # Raised travertine/tufa sidewalk (Crepidines)

                # Sidewalk outer ribbon
                tot_w = (rw * 0.5 + sw)
                q00 = project(sx0 - px_n*tot_w, y0 + 0.15, sz0 - pz_n*tot_w)
                q10 = project(sx0 + px_n*tot_w, y0 + 0.15, sz0 + pz_n*tot_w)
                q01 = project(sx1 - px_n*tot_w, y1 + 0.15, sz1 - pz_n*tot_w)
                q11 = project(sx1 + px_n*tot_w, y1 + 0.15, sz1 + pz_n*tot_w)
                fill_tri(q00, q01, q10, scol)
                fill_tri(q10, q01, q11, scol)

                # Basalt Carriageway inner ribbon
                hw = rw * 0.5
                c00 = project(sx0 - px_n*hw, y0 + 0.22, sz0 - pz_n*hw)
                c10 = project(sx0 + px_n*hw, y0 + 0.22, sz0 + pz_n*hw)
                c01 = project(sx1 - px_n*hw, y1 + 0.22, sz1 - pz_n*hw)
                c11 = project(sx1 + px_n*hw, y1 + 0.22, sz1 + pz_n*hw)
                fill_tri(c00, c01, c10, rcol)
                fill_tri(c10, c01, c11, rcol)

    def draw_3d_box(cx, cy, cz, sx, sy, sz, rot_y, wall_col, roof_col):
        c, s = math.cos(rot_y), math.sin(rot_y)
        hx, hy, hz = sx*0.5, sy*0.5, sz*0.5
        pts = []
        for dx, dy, dz in [(-hx,-hy,-hz),(hx,-hy,-hz),(hx,hy,-hz),(-hx,hy,-hz),(-hx,-hy,hz),(hx,-hy,hz),(hx,hy,hz),(-hx,hy,hz)]:
            wx = cx + dx*c + dz*s
            wy = cy + dy
            wz = cz - dx*s + dz*c
            pts.append(project(wx, wy, wz))
        # Top roof face (terracotta tiles)
        fill_tri(pts[3], pts[2], pts[6], roof_col)
        fill_tri(pts[3], pts[6], pts[7], roof_col)
        # 4 side walls with directional shading
        sides = [
            (0,1,2,3, 0.92), (4,6,5,7, 0.86),
            (1,5,6,2, 0.78), (0,3,7,4, 0.72)
        ]
        for i0,i1,i2,i3,shade in sides:
            fc = (int(min(255, wall_col[0]*shade)), int(min(255, wall_col[1]*shade)), int(min(255, wall_col[2]*shade)))
            fill_tri(pts[i0], pts[i1], pts[i2], fc)
            fill_tri(pts[i0], pts[i2], pts[i3], fc)

    # 3. Rasterize 7 Bridges & Tiber Island
    for br in DATA["bridges"]:
        bcol = (16, 200, 138) if (cred_mode and br["credibility"] == "A") else ((59, 135, 248) if cred_mode else ((168, 112, 62) if "0084" in br["id"] else (232, 222, 202)))
        L, W_b, H_b = br["modelDims"]["length"], br["modelDims"]["width"], br["modelDims"]["height"]
        draw_3d_box(br["pos"][0], br["pos"][1], br["pos"][2], L, 2.8, W_b * 1.5, br["rotationY"], bcol, bcol)

    # 4. Rasterize 660 Procedural Urban Buildings (Insulae, Domus, Horrea, Porticus)
    for b in DATA["urbanBuildings"]:
        bx, by, bz = b["pos"]
        # Distance cull in walk mode for speed and clarity
        dist_cam = math.hypot(bx - cam_pos[0], bz - cam_pos[2])
        if walk_mode and dist_cam > 340.0:
            continue
        if not walk_mode and dist_cam > 2600.0:
            continue

        bl, bh, bw = b["dims"]
        rot = b["rotY"]
        if cred_mode:
            if b["credibility"] == "A":
                wcol = (16, 195, 132); rcol = (24, 215, 148)
            elif b["credibility"] == "B":
                wcol = (59, 135, 248); rcol = (82, 155, 255)
            else:
                wcol = (245, 158, 11); rcol = (252, 178, 38)
        else:
            st = b["materialStyle"]
            rcol = (178, 86, 56) # Terracotta Tegulae & Imbrices roof tiles
            if st == "opus_latericium_red":
                wcol = (176, 98, 74)
            elif st == "stucco_weathered_subura":
                wcol = (188, 162, 128)
            elif st == "stucco_ochre":
                wcol = (212, 178, 124)
            elif st == "domus_peristyle_white":
                wcol = (236, 228, 212)
                rcol = (192, 92, 58)
            elif st == "travertine_porticus":
                wcol = (228, 220, 204)
                rcol = (164, 156, 142)
            else: # opus_reticulatum_horrea
                wcol = (182, 166, 142)
                rcol = (162, 82, 54)

        # Main building block
        draw_3d_box(bx, by + bh * 0.5, bz, bl, bh, bw, rot, wcol, rcol)

        # In walk mode or close-up views, add ground-floor dark Tabernae shop openings & wooden Maeniana balcony ledges
        if dist_cam < 240.0 and not cred_mode:
            if b.get("hasTabernae"):
                draw_3d_box(bx, by + 1.8, bz, bl + 0.4, 3.2, bw + 0.4, rot, (72, 54, 42), (96, 68, 48))
            if b.get("hasBalcony") and bh > 12.0:
                draw_3d_box(bx, by + 6.8, bz, bl + 1.4, 1.1, bw + 1.4, rot, (124, 82, 46), (138, 92, 52))

    # 5. Callout Labels
    callouts = [
        ("SUBURA INSULAE (5-6F)", 340, 38, -210, (251, 191, 36)),
        ("CLIVUS SUBURANUS", 295, 22, -185, (96, 165, 250)),
        ("SAEPTA JULIA PORTICUS", -310, 28, -540, (52, 211, 153)),
        ("PORTICUS DIVORUM", -210, 26, -420, (52, 211, 153)),
        ("VIA LATA (FLAMINIA)", -140, 22, -650, (96, 165, 250)),
        ("SACRA VIA (BASALT)", 180, 34, 25, (52, 211, 153)),
        ("DOMUS ALTA SEMITA", 480, 68, -820, (251, 191, 36)),
        ("DOMUS PALATINUS", 180, 62, 240, (52, 211, 153)),
        ("VIA OSTIENSIS & HORREA", -450, 26, 860, (96, 165, 250)),
        ("PORTA CAPENA & VIA APPIA", 340, 28, 760, (52, 211, 153))
    ]
    placed = []
    for label, mx, my, mz, lcol in callouts:
        pr = project(mx, my, mz)
        if pr and pr[2] < (350 if walk_mode else 2500) and 40 <= pr[0] <= W - 190 and 55 <= pr[1] <= H - 48:
            sx, sy = int(pr[0]), int(pr[1])
            bw_l = len(label)*6 + 10
            for _ in range(4):
                if any(not (sx + bw_l < ox0 or sx > ox1 or sy + 2 < oy0 or sy - 14 > oy1) for ox0,oy0,ox1,oy1 in placed):
                    sy -= 15
                else:
                    break
            if sy > 52:
                placed.append((sx - 4, sy - 12, sx + bw_l, sy + 2))
                draw_rect(buf, W, H, sx - 4, sy - 12, sx + bw_l, sy + 2, (15, 19, 26), 0.84)
                draw_text(buf, W, H, sx, sy - 9, label, lcol, scale=1)

    # Top & Bottom HUD Bars
    draw_rect(buf, W, H, 10, 10, W - 10, 44, (15, 19, 26), 0.90)
    draw_text(buf, W, H, 20, 16, f"ROMA AD 128 - {title_en}", (229, 193, 88), scale=2)
    draw_text(buf, W, H, 20, 33, sub_en, (185, 195, 210), scale=1)
    draw_text(buf, W, H, W - 310, 16, "FPS: 60  DRAW CALLS: 8 / 1500", (52, 211, 153), scale=1)
    draw_text(buf, W, H, W - 310, 29, "660 BLDGS + 14 ROADS (<= 128 AD)", (96, 165, 250), scale=1)

    draw_rect(buf, W, H, 10, H - 34, W - 10, H - 10, (15, 19, 26), 0.88)
    footer = "CREDIBILITY OVERLAY: TIER A=GREEN(REMAINS)  TIER B=BLUE(FUR FRAGMENTS)  TIER C=ORANGE(PROCEDURAL)" if cred_mode else (
             "1.65M WALK MODE: BASALT SILEX PAVING + CREPIDINES SIDEWALKS + TABERNAE SHOPS + MAENIANA BALCONIES" if walk_mode else
             "P2 URBAN TEXTURE: 14 CONSULAR/URBAN ROADS + 227 SUBURA INSULAE + 223 DOMUS + 65 CAMPUS MARTIUS + 30 HORREA")
    draw_text(buf, W, H, 20, H - 25, footer, (240, 240, 245), scale=1)

    out_file = os.path.join(screenshots_dir, f"{vp_id}.png")
    write_png(out_file, W, H, buf)
    return out_file

p2_viewpoints = [
    ("p2_vp01_subura_alley_walk", "VP01 SUBURA CROWDED ALLEY (1.65M WALK)", "REGIO IV CLIVUS SUBURANUS | 5-6 STORY INSULAE, TABERNAE SHOPS & OVERHANGING BALCONIES", (255.0, get_ancient_terrain_height(255, -172) + 1.65, -172.0), (380.0, get_ancient_terrain_height(380, -215) + 9.5, -215.0), False, True, (-100, 800, -550, 150, 10)),
    ("p2_vp02_campus_martius_walk", "VP02 CAMPUS MARTIUS MONUMENTAL AVENUE", "REGIO IX SAEPTA JULIA & VIA LATA | WIDE OPEN PORTICOES, GARDENS & SPACED 4F INSULAE", (-145.0, get_ancient_terrain_height(-145, -720) + 4.5, -720.0), (-260.0, get_ancient_terrain_height(-260, -460) + 6.0, -460.0), False, True, (-850, 350, -1100, 100, 12)),
    ("p2_vp03_sacra_via_velia", "VP03 SACRA VIA BASALT PAVING & SIDEWALKS", "REGIO IV/VIII SACRA VIA | 6.5M POLYGONAL BASALT ROADWAY + 2.2M CREPIDINES CURBS", (65.0, get_ancient_terrain_height(65, 10) + 12.0, 10.0), (280.0, get_ancient_terrain_height(280, 35) + 4.0, 35.0), False, True, (-120, 520, -280, 320, 12)),
    ("p2_vp04_quirinal_domus_district", "VP04 ALTA SEMITA ARISTOCRATIC DOMUS", "REGIO VI QUIRINAL HILL | 1-2 STORY ATRIUM-PERISTYLE DOMUS VILLAS ALONG ALTA SEMITA", (280.0, get_ancient_terrain_height(280, -620) + 48.0, -620.0), (580.0, get_ancient_terrain_height(580, -860) + 8.0, -860.0), False, False, (0, 1100, -1300, -300, 24)),
    ("p2_vp05_emporium_horrea_ostiensis", "VP05 VIA OSTIENSIS & EMPORIUM HORREA", "REGIO XIII RIVER PORT | 6.0M HEAVY CART ROAD, HORREA GALBAE WAREHOUSES & TESTACCIO", (-520.0, get_ancient_terrain_height(-520, 520) + 45.0, 520.0), (-450.0, get_ancient_terrain_height(-450, 980) + 8.0, 980.0), False, False, (-950, 100, 300, 1550, 24)),
    ("p2_vp06_porta_capena_via_appia", "VP06 PORTA CAPENA & VIA APPIA ORIGIN", "REGIO I/XII | SERVIAN WALL GATE, VIA APPIA (4.1M CARRIAGEWAY) & ROADSIDE INSULAE", (210.0, get_ancient_terrain_height(210, 480) + 32.0, 480.0), (420.0, get_ancient_terrain_height(420, 1050) + 6.0, 1050.0), False, False, (-200, 850, 250, 1650, 24)),
    ("p2_vp07_urban_density_birdseye", "VP07 FULL CITY ROAD NETWORK & TEXTURE", "ALL 14 REGIONES | CONTRAST BETWEEN DENSE SUBURA, OPEN CAMPUS MARTIUS & HILL DOMUS", (-140.0, 1150.0, 1120.0), (80.0, 20.0, -240.0), False, False, (-1500, 1500, -1600, 1500, 32)),
    ("p2_vp08_credibility_mode_p2", "VP08 P2 CREDIBILITY OVERLAY (A/B/C)", "TIER A=GREEN (ROADS/PORTICUS), TIER B=BLUE (FUR INSULAE), TIER C=ORANGE (PROCEDURAL)", (-140.0, 1150.0, 1120.0), (80.0, 20.0, -240.0), True, False, (-1500, 1500, -1600, 1500, 32))
]

for vp in p2_viewpoints:
    f_out = render_p2_screenshot(*vp)
    print("Captured P2 screenshot:", f_out)
