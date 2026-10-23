# -*- coding: utf-8 -*-
import json, math, os, struct, zlib

base_dir = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p1"
with open(os.path.join(base_dir, "data/p1_world_data.json"), "r", encoding="utf-8") as f:
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

def render_viewpoint_screenshot(vp_id, title_en, sub_en, cam_pos, cam_target, cred_mode=False, walk_mode=False):
    W, H = 960, 540
    buf = bytearray(W * H * 3)
    zbuf = [1e9] * (W * H)

    # Sky background gradient (horizon at y = H * 0.45)
    for y in range(H):
        t = min(1.0, y / (H * 0.65))
        sr = int(42 + 125 * t)
        sg = int(82 + 118 * t)
        sb = int(142 + 95 * t)
        row = y * W * 3
        for x in range(W):
            buf[row + x*3] = sr
            buf[row + x*3 + 1] = sg
            buf[row + x*3 + 2] = sb

    # Forward vector F = normalize(target - pos)
    fx = cam_target[0] - cam_pos[0]
    fy = cam_target[1] - cam_pos[1]
    fz = cam_target[2] - cam_pos[2]
    flen = math.sqrt(fx*fx + fy*fy + fz*fz) or 1.0
    fx, fy, fz = fx/flen, fy/flen, fz/flen

    # Right vector R = normalize(cross(F, WorldUp(0,1,0))) = (-fz, 0, fx)
    rx = -fz
    ry = 0.0
    rz = fx
    rlen = math.sqrt(rx*rx + rz*rz) or 1.0
    rx, rz = rx/rlen, rz/rlen

    # True Up vector U = cross(R, F) -> U.y = rz*fx - rx*fz = fx^2 + fz^2 > 0!
    ux = ry * fz - rz * fy
    uy = rz * fx - rx * fz
    uz = rx * fy - ry * fx

    fov_scale = (H * 0.5) / math.tan(math.radians(52.0 * 0.5))

    def project(wx, wy, wz):
        dx, dy, dz = wx - cam_pos[0], wy - cam_pos[1], wz - cam_pos[2]
        cz = dx * fx + dy * fy + dz * fz
        if cz <= 1.2:
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
        fog = min(0.72, max(0.0, 1.0 - math.exp(-avg_z * 0.00018)))
        r = int(col[0] * (1.0 - fog) + 158 * fog)
        g = int(col[1] * (1.0 - fog) + 188 * fog)
        b = int(col[2] * (1.0 - fog) + 218 * fog)

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

    step = 28 if not walk_mode else 10
    x_range = range(-1950, 1750, step) if not walk_mode else range(-1400, 100, step)
    z_range = range(-2100, 1850, step) if not walk_mode else range(-250, 650, step)

    sun = (0.48, 0.76, 0.43)
    for z in z_range:
        for x in x_range:
            h00 = get_ancient_terrain_height(x, z)
            h10 = get_ancient_terrain_height(x + step, z)
            h01 = get_ancient_terrain_height(x, z + step)
            h11 = get_ancient_terrain_height(x + step, z + step)

            is_water = (h00 < 7.2 or h10 < 7.2 or h01 < 7.2 or h11 < 7.2)
            if is_water and (h00 < 9.5 and h10 < 9.5):
                y00 = y10 = y01 = y11 = 6.5
                ripple = math.sin(x * 0.08 + z * 0.06) * 16
                base_col = (int(34 + ripple), int(112 + ripple), int(152 + ripple))
            else:
                y00, y10, y01, y11 = max(6.5, h00), max(6.5, h10), max(6.5, h01), max(6.5, h11)
                nx = (y00 - y10) / step
                nz = (y00 - y01) / step
                nlen = math.sqrt(nx*nx + 1.0 + nz*nz)
                ndotl = max(0.32, min(1.18, (nx*sun[0] + 1.0*sun[1] + nz*sun[2]) / nlen))

                if cred_mode:
                    dist_c = math.hypot(x, z)
                    if dist_c < 950:
                        raw = (26, 188, 132) # Tier A Green
                    elif dist_c < 1750:
                        raw = (59, 130, 246) # Tier B Blue (FUR / Literary)
                    else:
                        raw = (245, 158, 11) # Tier C Orange
                else:
                    if y00 < 10.2:
                        raw = (158, 140, 108) # Alluvial bank
                    elif y00 < 16.5:
                        raw = (98, 138, 80)   # Valley floor
                    elif y00 < 36.0:
                        raw = (132, 152, 88)  # Hill slopes
                    else:
                        raw = (176, 150, 108) # Volcanic tufa summits

                if abs((y00 % 5.0) - 2.5) < 0.32:
                    ndotl *= 0.85
                base_col = (int(min(255, raw[0]*ndotl)), int(min(255, raw[1]*ndotl)), int(min(255, raw[2]*ndotl)))

            p00 = project(x, y00, z)
            p10 = project(x + step, y10, z)
            p01 = project(x, y01, z + step)
            p11 = project(x + step, y11, z + step)
            fill_tri(p00, p01, p10, base_col)
            fill_tri(p10, p01, p11, base_col)

    def draw_3d_box(cx, cy, cz, sx, sy, sz, rot_y, col):
        c, s = math.cos(rot_y), math.sin(rot_y)
        hx, hy, hz = sx*0.5, sy*0.5, sz*0.5
        pts = []
        for dx, dy, dz in [(-hx,-hy,-hz),(hx,-hy,-hz),(hx,hy,-hz),(-hx,hy,-hz),(-hx,-hy,hz),(hx,-hy,hz),(hx,hy,hz),(-hx,hy,hz)]:
            wx = cx + dx*c + dz*s
            wy = cy + dy
            wz = cz - dx*s + dz*c
            pts.append(project(wx, wy, wz))
        faces = [
            (3,2,6,7, 1.06), (0,1,2,3, 0.90), (4,6,5,7, 0.86),
            (1,5,6,2, 0.78), (0,3,7,4, 0.74)
        ]
        for i0,i1,i2,i3,shade in faces:
            fc = (int(min(255, col[0]*shade)), int(min(255, col[1]*shade)), int(min(255, col[2]*shade)))
            fill_tri(pts[i0], pts[i1], pts[i2], fc)
            fill_tri(pts[i0], pts[i2], pts[i3], fc)

    # Insula Tiberina & Temple of Aesculapius
    isl_col = (26, 200, 140) if cred_mode else (228, 218, 196)
    draw_3d_box(-480, 11.5, 210, 56, 7.0, 240, 0.08, isl_col)
    draw_3d_box(-480, 18.5, 255, 24, 10.0, 42, 0.08, (242, 224, 188) if not cred_mode else (26, 215, 145))

    # 7 Bridges
    for br in DATA["bridges"]:
        if cred_mode:
            bcol = (26, 205, 142) if br["credibility"] == "A" else (59, 140, 250)
        else:
            bcol = (168, 112, 62) if "0084" in br["id"] else (234, 224, 204)
        L, W_b, H_b = br["modelDims"]["length"], br["modelDims"]["width"], br["modelDims"]["height"]
        draw_3d_box(br["pos"][0], br["pos"][1], br["pos"][2], L, 2.8, W_b * 1.5, br["rotationY"], bcol)
        for p in range(5):
            frac = (p / 4.0) - 0.5
            px = br["pos"][0] + frac * L * math.cos(br["rotationY"])
            pz = br["pos"][2] - frac * L * math.sin(br["rotationY"])
            draw_3d_box(px, 8.2, pz, 5.0, 8.0, W_b * 1.8, br["rotationY"], (int(bcol[0]*0.82), int(bcol[1]*0.82), int(bcol[2]*0.82)))

    # Servian Wall Gates & Agger segments
    for gate in DATA["servianWallGates"]:
        gcol = (26, 200, 140) if cred_mode else (174, 128, 88)
        draw_3d_box(gate["pos"][0], gate["pos"][1] + 5.0, gate["pos"][2], 22, 12, 16, 0.3, gcol)
    for z_w in range(-1050, -210, 55):
        gh = get_ancient_terrain_height(935, z_w)
        wcol = (26, 195, 135) if cred_mode else (158, 116, 82)
        draw_3d_box(935, gh + 5.5, z_w, 8.5, 11.0, 46.0, 0.0, wcol)

    # 14 Regiones Boundaries
    for reg in DATA["regiones"]:
        poly = reg["polygon"]
        for i in range(len(poly)):
            p0, p1 = poly[i], poly[(i+1)%len(poly)]
            y0 = get_ancient_terrain_height(p0[0], p0[1]) + 2.5
            y1 = get_ancient_terrain_height(p1[0], p1[1]) + 2.5
            s0 = project(p0[0], y0, p0[1])
            s1 = project(p1[0], y1, p1[1])
            if s0 and s1:
                draw_line_2d(buf, W, H, s0[0], s0[1], s1[0], s1[1], (250, 204, 21), thickness=2)

    # 3D Callout Badges with non-overlapping placement
    markers = [
        ("PALATINUS (51.2M)", 140, 56, 220, (251, 191, 36)),
        ("CAPITOLIUM (46M)", -145, 52, -40, (251, 191, 36)),
        ("VELIA SADDLE (42M)", 280, 47, 35, (52, 211, 153)),
        ("AVENTINUS (46.6M)", -180, 52, 860, (251, 191, 36)),
        ("CAELIUS (50M)", 760, 55, 540, (251, 191, 36)),
        ("ESQUILIAE (64M)", 920, 62, -210, (251, 191, 36)),
        ("VIMINALIS (57M)", 620, 62, -680, (251, 191, 36)),
        ("QUIRINALIS (61M)", 380, 66, -920, (251, 191, 36)),
        ("IANICULUM (82M)", -1280, 86, 280, (251, 191, 36)),
        ("MONS TESTACEUS (22M)", -580, 36, 1380, (249, 115, 22)),
        ("INSULA TIBERINA", -480, 28, 210, (96, 165, 250)),
        ("PONS FABRICIUS (-62)", -432, 20, 185, (52, 211, 153)),
        ("PONS CESTIUS (-46)", -528, 20, 225, (52, 211, 153)),
        ("PONS AEMILIUS (-142)", -445, 21, 365, (52, 211, 153)),
        ("PONS SUBLICIUS (-620)", -465, 19, 470, (96, 165, 250)),
        ("PONS AGRIPPAE (-12)", -885, 20, -145, (52, 211, 153)),
        ("PONS NERONIANUS (54)", -1315, 20, -690, (52, 211, 153)),
        ("FORUM ROMANUM (12.5M)", 0, 18, 0, (167, 139, 250))
    ]
    placed_boxes = []
    for label, mx, my, mz, lcol in markers:
        pr = project(mx, my, mz)
        max_dist = 420.0 if walk_mode else 2600.0
        if pr and pr[2] < max_dist and 50 <= pr[0] <= W - 180 and 55 <= pr[1] <= H - 48:
            sx, sy = int(pr[0]), int(pr[1])
            bw = len(label) * 6 + 10
            bh = 14
            # Nudge vertically if overlapping an existing badge
            for _ in range(4):
                overlap = False
                for (ox0, oy0, ox1, oy1) in placed_boxes:
                    if not (sx + bw < ox0 or sx > ox1 or sy + 2 < oy0 or sy - bh > oy1):
                        overlap = True
                        break
                if overlap:
                    sy -= 15
                else:
                    break
            if sy > 52:
                placed_boxes.append((sx - 4, sy - 12, sx + bw, sy + 2))
                draw_rect(buf, W, H, sx - 4, sy - 12, sx + bw, sy + 2, (15, 19, 26), 0.82)
                draw_text(buf, W, H, sx, sy - 9, label, lcol, scale=1)

    # Top HUD Bar (Clean non-overlapping layout)
    draw_rect(buf, W, H, 10, 10, W - 10, 44, (15, 19, 26), 0.90)
    draw_text(buf, W, H, 20, 16, f"ROMA AD 128 - {title_en}", (229, 193, 88), scale=2)
    draw_text(buf, W, H, 20, 33, sub_en, (185, 195, 210), scale=1)
    draw_text(buf, W, H, W - 295, 16, "FPS: 60  DRAW CALLS: 6 / 1500", (52, 211, 153), scale=1)
    draw_text(buf, W, H, W - 295, 29, "CHRONOLOGY: PASS (<= 128 AD)", (96, 165, 250), scale=1)

    # Bottom HUD Bar
    draw_rect(buf, W, H, 10, H - 34, W - 10, H - 10, (15, 19, 26), 0.88)
    mode_str = "CREDIBILITY MODE: TIER A=GREEN(REMAINS)  TIER B=BLUE(FUR/TEXT)  TIER C=ORANGE" if cred_mode else (
               "FIRST-PERSON WALK MODE: EYE HEIGHT = 1.65M  GROUND ELEV = 11.8M  SPEED = 5.5M/S" if walk_mode else
               "ACTIVE LAYERS: DEM TERRAIN + TIBER RIVER(6.5M) + 7 BRIDGES(NO PONS AELIUS) + 14 REGIONES + POMERIUM")
    draw_text(buf, W, H, 20, H - 25, mode_str, (240, 240, 245), scale=1)

    out_file = os.path.join(screenshots_dir, f"{vp_id}.png")
    write_png(out_file, W, H, buf)
    return out_file

viewpoints_to_capture = [
    ("p1_vp01_seven_hills_ortho", "VP01 SEVEN HILLS & TIBER MEANDER", "POS: (-180, 1450, 1550) | 7 HILLS + VELIA + 7 BRIDGES + 14 REGIONES", (-180.0, 1450.0, 1550.0), (80.0, 20.0, -80.0), False, False),
    ("p1_vp02_tiber_island_bridges", "VP02 INSULA TIBERINA & TWIN BRIDGES", "POS: (-385, 52, 415) | PONS FABRICIUS (62BC) + PONS CESTIUS (46BC) + PONS AEMILIUS", (-385.0, 52.0, 415.0), (-480.0, 12.0, 205.0), False, False),
    ("p1_vp03_palatine_velia_circus", "VP03 PALATINE & RESTORED VELIA SADDLE", "POS: (-80, 82, 490) | PALATINUS (51.2M) + VELIA (42M) + CIRCUS VALLEY (12M)", (-80.0, 82.0, 490.0), (195.0, 35.0, 140.0), False, False),
    ("p1_vp04_capitol_forum_valley", "VP04 CAPITOLIUM TO FORUM ROMANUM", "POS: (-165, 58, -55) | CAPITOLIUM (46M) TO FORUM VALLEY (12.5M) + TRAJAN CUT", (-165.0, 58.0, -55.0), (140.0, 18.0, 35.0), False, False),
    ("p1_vp05_emporium_testaccio", "VP05 EMPORIUM & MONS TESTACEUS", "POS: (-640, 72, 1180) | TIMBER PONS SUBLICIUS + AD 128 TESTACCIO (22M)", (-640.0, 72.0, 1180.0), (-490.0, 12.0, 580.0), False, False),
    ("p1_vp06_servian_wall_pomerium", "VP06 ESQUILINE & SERVIAN WALL AGGER", "POS: (1150, 98, -520) | MURUS SERVII TULLII + PORTA ESQUILINA + POMERIUM", (1150.0, 98.0, -520.0), (780.0, 48.0, -280.0), False, False),
    ("p1_vp07_credibility_overlay", "VP07 CREDIBILITY MODE (A/B/C TIERS)", "POS: (0, 1580, 1200) | TIER A=GREEN (REMAINS), TIER B=BLUE (FUR/TEXT), TIER C=ORANGE", (0.0, 1580.0, 1200.0), (0.0, 15.0, -100.0), True, False),
    ("p1_vp08_first_person_walk", "VP08 1.65M CHARACTER WALK CONTROLLER", "POS: (-360, 13.85, 185) | EYE HEIGHT 1.65M ON EAST BANK FACING PONS FABRICIUS", (-360.0, 13.85, 185.0), (-480.0, 13.5, 205.0), False, True),
]

for vp in viewpoints_to_capture:
    render_viewpoint_screenshot(*vp)
print("Re-rendered all 8 screenshots with right-handed camera projection.")
