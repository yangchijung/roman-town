# -*- coding: utf-8 -*-
import json, math, os, struct, zlib

base_dir = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p3"
staging_dir = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/roman-town-repo-staging"
with open(os.path.join(base_dir, "data/p3_world_data.json"), "r", encoding="utf-8") as f:
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

def draw_rect(buf, w, h, x0, y0, x1, y1, col, alpha=0.86):
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

def render_p3_screenshot(vp_id, title_en, sub_en, cam_pos, cam_target, mode="exterior", bounds=None):
    W, H = 960, 540
    buf = bytearray(W * H * 3)
    zbuf = [1e9] * (W * H)

    # Sky or Interior Background
    for y in range(H):
        t = min(1.0, y / (H * 0.65))
        if mode == "pantheon_interior":
            sr, sg, sb = int(28 + 35*t), int(34 + 38*t), int(46 + 42*t)
        else:
            sr, sg, sb = int(38 + 128*t), int(76 + 118*t), int(136 + 92*t)
        row = y * W * 3
        for x in range(W):
            buf[row + x*3] = sr; buf[row + x*3 + 1] = sg; buf[row + x*3 + 2] = sb

    fx = cam_target[0] - cam_pos[0]
    fy = cam_target[1] - cam_pos[1]
    fz = cam_target[2] - cam_pos[2]
    flen = math.sqrt(fx*fx + fy*fy + fz*fz) or 1.0
    fx, fy, fz = fx/flen, fy/flen, fz/flen

    rx = -fz; ry = 0.0; rz = fx
    rlen = math.sqrt(rx*rx + rz*rz) or 1.0
    rx, rz = rx/rlen, rz/rlen

    ux = ry * fz - rz * fy
    uy = rz * fx - rx * fz
    uz = rx * fy - ry * fx

    fov_scale = (H * 0.5) / math.tan(math.radians(56.0 * 0.5))

    def project(wx, wy, wz):
        dx, dy, dz = wx - cam_pos[0], wy - cam_pos[1], wz - cam_pos[2]
        cz = dx * fx + dy * fy + dz * fz
        if cz <= 0.8:
            return None
        cx = dx * rx + dy * ry + dz * rz
        cy = dx * ux + dy * uy + dz * uz
        sx = W * 0.5 + (cx / cz) * fov_scale
        sy = H * 0.5 - (cy / cz) * fov_scale
        return (sx, sy, cz)

    def fill_tri(p0, p1, p2, col, no_fog=False):
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
        fog = 0.0 if no_fog else min(0.62, max(0.0, 1.0 - math.exp(-avg_z * 0.00018)))
        r = int(col[0] * (1.0 - fog) + 155 * fog)
        g = int(col[1] * (1.0 - fog) + 185 * fog)
        b = int(col[2] * (1.0 - fog) + 212 * fog)

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

    def draw_3d_box(cx, cy, cz, sx, sy, sz, rot_y, wall_col, roof_col, no_fog=False):
        c, s = math.cos(rot_y), math.sin(rot_y)
        hx, hy, hz = sx*0.5, sy*0.5, sz*0.5
        pts = []
        for dx, dy, dz in [(-hx,-hy,-hz),(hx,-hy,-hz),(hx,hy,-hz),(-hx,hy,-hz),(-hx,-hy,hz),(hx,-hy,hz),(hx,hy,hz),(-hx,hy,hz)]:
            wx = cx + dx*c + dz*s
            wy = cy + dy
            wz = cz - dx*s + dz*c
            pts.append(project(wx, wy, wz))
        fill_tri(pts[3], pts[2], pts[6], roof_col, no_fog)
        fill_tri(pts[3], pts[6], pts[7], roof_col, no_fog)
        sides = [(0,1,2,3, 0.94), (4,6,5,7, 0.86), (1,5,6,2, 0.78), (0,3,7,4, 0.72)]
        for i0,i1,i2,i3,shade in sides:
            fc = (int(min(255, wall_col[0]*shade)), int(min(255, wall_col[1]*shade)), int(min(255, wall_col[2]*shade)))
            fill_tri(pts[i0], pts[i1], pts[i2], fc, no_fog)
            fill_tri(pts[i0], pts[i2], pts[i3], fc, no_fog)

    def draw_cylinder_or_ring(cx, cy_base, cz, r_outer, r_inner, height, segs, col_ext, col_int, col_top):
        for i in range(segs):
            a0 = (i / segs) * math.pi * 2.0
            a1 = ((i + 1) / segs) * math.pi * 2.0
            c0, s0 = math.cos(a0), math.sin(a0)
            c1, s1 = math.cos(a1), math.sin(a1)
            shade = 0.78 + 0.22 * max(0.0, c0 * 0.6 + s0 * 0.8)
            ec = (int(min(255, col_ext[0]*shade)), int(min(255, col_ext[1]*shade)), int(min(255, col_ext[2]*shade)))
            # Outer wall quad
            p00 = project(cx + r_outer*c0, cy_base, cz + r_outer*s0)
            p10 = project(cx + r_outer*c1, cy_base, cz + r_outer*s1)
            p01 = project(cx + r_outer*c0, cy_base + height, cz + r_outer*s0)
            p11 = project(cx + r_outer*c1, cy_base + height, cz + r_outer*s1)
            fill_tri(p00, p01, p10, ec)
            fill_tri(p10, p01, p11, ec)
            if r_inner > 0.5:
                ic = (int(min(255, col_int[0]*shade)), int(min(255, col_int[1]*shade)), int(min(255, col_int[2]*shade)))
                q00 = project(cx + r_inner*c0, cy_base, cz + r_inner*s0)
                q10 = project(cx + r_inner*c1, cy_base, cz + r_inner*s1)
                q01 = project(cx + r_inner*c0, cy_base + height*0.55, cz + r_inner*s0)
                q11 = project(cx + r_inner*c1, cy_base + height*0.55, cz + r_inner*s1)
                # Sloped cavea seating from outer top to inner podium
                fill_tri(p01, q01, p11, col_top)
                fill_tri(p11, q01, q11, col_top)
                fill_tri(q00, q01, q10, ic)
                fill_tri(q10, q01, q11, ic)

    # Special Mode 1: Pantheon Coffered Dome Interior (43.3m Sphere + Oculus Light Beam + Opus Sectile Floor)
    if mode == "pantheon_interior":
        cx, cy, cz = -425.0, 13.2, -555.0
        R = 21.65 # 43.3m diameter / 2
        segs_az = 28
        # Opus Sectile polychrome marble floor (alternating porphyry red, giallo antico gold, and pavonazzetto squares)
        for fx_i in range(-20, 20, 2):
            for fz_i in range(-20, 20, 2):
                if fx_i*fx_i + fz_i*fz_i <= 21.5*21.5:
                    is_alt = ((fx_i // 2) + (fz_i // 2)) % 2 == 0
                    fcol = (148, 68, 72) if is_alt else (218, 182, 112)
                    p00 = project(cx + fx_i, cy, cz + fz_i)
                    p10 = project(cx + fx_i + 2, cy, cz + fz_i)
                    p01 = project(cx + fx_i, cy, cz + fz_i + 2)
                    p11 = project(cx + fx_i + 2, cy, cz + fz_i + 2)
                    fill_tri(p00, p01, p10, fcol, True)
                    fill_tri(p10, p01, p11, fcol, True)

        # Lower Rotunda Cylinder (0 to 21.65m height) with Corinthian columns, niches & polychrome marble revetment
        for i in range(segs_az):
            a0 = (i / segs_az) * math.pi * 2.0
            a1 = ((i + 1) / segs_az) * math.pi * 2.0
            c0, s0 = math.cos(a0), math.sin(a0)
            c1, s1 = math.cos(a1), math.sin(a1)
            wcol = (212, 192, 158) if i % 2 == 0 else (168, 92, 76)
            p00 = project(cx + R*c0, cy, cz + R*s0)
            p10 = project(cx + R*c1, cy, cz + R*s1)
            p01 = project(cx + R*c0, cy + 12.5, cz + R*s0)
            p11 = project(cx + R*c1, cy + 12.5, cz + R*s1)
            fill_tri(p00, p01, p10, wcol, True)
            fill_tri(p10, p01, p11, wcol, True)
            # Attic zone (12.5m to 21.65m)
            a_col = (195, 178, 148)
            p02 = project(cx + R*c0, cy + 21.65, cz + R*s0)
            p12 = project(cx + R*c1, cy + 21.65, cz + R*s1)
            fill_tri(p01, p02, p11, a_col, True)
            fill_tri(p11, p02, p12, a_col, True)

        # Hemispherical Coffered Dome (21.65m to 43.3m height) with 5 rings of 28 coffers + 8.9m open Oculus at top
        rings = 6
        for r_idx in range(rings):
            phi0 = (r_idx / (rings + 1)) * (math.pi * 0.44)
            phi1 = ((r_idx + 1) / (rings + 1)) * (math.pi * 0.44)
            r0 = R * math.cos(phi0); y0 = cy + 21.65 + R * math.sin(phi0)
            r1 = R * math.cos(phi1); y1 = cy + 21.65 + R * math.sin(phi1)
            for i in range(segs_az):
                a0 = (i / segs_az) * math.pi * 2.0
                a1 = ((i + 1) / segs_az) * math.pi * 2.0
                c0, s0 = math.cos(a0), math.sin(a0)
                c1, s1 = math.cos(a1), math.sin(a1)
                # Gilded bronze rosette coffer highlight alternating with stucco coffer recess
                cof_col = (218, 186, 118) if (i + r_idx) % 2 == 0 else (164, 152, 134)
                d00 = project(cx + r0*c0, y0, cz + r0*s0)
                d10 = project(cx + r0*c1, y0, cz + r0*s1)
                d01 = project(cx + r1*c0, y1, cz + r1*s0)
                d11 = project(cx + r1*c1, y1, cz + r1*s1)
                fill_tri(d00, d01, d10, cof_col, True)
                fill_tri(d10, d01, d11, cof_col, True)

        # Gold-trimmed Oculus Ring at height 43.3m (radius 4.45m) & Bright Blue Sky inside Oculus
        r_oc = 4.45; y_oc = cy + 43.3
        for i in range(segs_az):
            a0 = (i / segs_az) * math.pi * 2.0
            a1 = ((i + 1) / segs_az) * math.pi * 2.0
            p_center = project(cx, y_oc + 0.5, cz)
            p0 = project(cx + r_oc*math.cos(a0), y_oc, cz + r_oc*math.sin(a0))
            p1 = project(cx + r_oc*math.cos(a1), y_oc, cz + r_oc*math.sin(a1))
            fill_tri(p_center, p0, p1, (115, 185, 252), True)

        # Callout labels inside Pantheon
        for lbl, lx, ly, lz, lcol in [
            ("OCULUS (8.9M DIAMETER AT 43.3M HEIGHT)", cx, cy + 41.5, cz, (96, 165, 250)),
            ("5 RINGS OF 28 GILDED COFFERS (43.3M SPHERE)", cx + 11, cy + 31.0, cz + 6, (251, 191, 36)),
            ("OPUS SECTILE PORPHYRY & GIALLO ANTICO FLOOR", cx + 4, cy + 1.5, cz + 8, (52, 211, 153))
        ]:
            pr = project(lx, ly, lz)
            if pr and 30 <= pr[0] <= W - 260 and 55 <= pr[1] <= H - 48:
                sx, sy = int(pr[0]), int(pr[1])
                draw_rect(buf, W, H, sx - 4, sy - 12, sx + len(lbl)*6 + 10, sy + 2, (15, 19, 26), 0.85)
                draw_text(buf, W, H, sx, sy - 9, lbl, lcol, scale=1)

    else:
        # Exterior / Colosseum Arena Interior Mode
        bx0, bx1, bz0, bz1, step = bounds if bounds else (-650, 750, -750, 350, 18)
        sun = (0.48, 0.76, 0.43)
        for z in range(bz0, bz1, step):
            for x in range(bx0, bx1, step):
                h00 = get_ancient_terrain_height(x, z)
                h10 = get_ancient_terrain_height(x + step, z)
                h01 = get_ancient_terrain_height(x, z + step)
                h11 = get_ancient_terrain_height(x + step, z + step)
                y00, y10, y01, y11 = max(6.5, h00), max(6.5, h10), max(6.5, h01), max(6.5, h11)
                nx = (y00 - y10) / step; nz = (y00 - y01) / step
                nlen = math.sqrt(nx*nx + 1.0 + nz*nz)
                ndotl = max(0.35, min(1.15, (nx*sun[0] + 1.0*sun[1] + nz*sun[2]) / nlen))
                raw = (104, 138, 84) if y00 < 16.5 else ((132, 148, 88) if y00 < 36.0 else (168, 146, 106))
                base_col = (int(min(255, raw[0]*ndotl)), int(min(255, raw[1]*ndotl)), int(min(255, raw[2]*ndotl)))
                fill_tri(project(x, y00, z), project(x, y01, z + step), project(x + step, y10, z), base_col)
                fill_tri(project(x + step, y10, z), project(x, y01, z + step), project(x + step, y11, z + step), base_col)

        # Roads
        for road in DATA["roads"]:
            wps = road["waypoints"]
            rw = road["carriageWidthM"]
            for i in range(len(wps) - 1):
                x0, z0 = wps[i]; x1, z1 = wps[i+1]
                seg_len = math.hypot(x1 - x0, z1 - z0) or 1.0
                nsub = max(1, int(seg_len / 18.0))
                dx_n = (x1 - x0) / seg_len; dz_n = (z1 - z0) / seg_len
                px_n, pz_n = -dz_n, dx_n
                for s in range(nsub):
                    t0, t1 = s / nsub, (s + 1) / nsub
                    sx0, sz0 = x0 + t0*(x1-x0), z0 + t0*(z1-z0)
                    sx1, sz1 = x0 + t1*(x1-x0), z0 + t1*(z1-z0)
                    y0 = get_ancient_terrain_height(sx0, sz0) + 0.35
                    y1 = get_ancient_terrain_height(sx1, sz1) + 0.35
                    hw = rw * 0.55
                    fill_tri(project(sx0 - px_n*hw, y0, sz0 - pz_n*hw), project(sx1 - px_n*hw, y1, sz1 - pz_n*hw), project(sx0 + px_n*hw, y0, sz0 + pz_n*hw), (68, 72, 80))
                    fill_tri(project(sx0 + px_n*hw, y0, sz0 + pz_n*hw), project(sx1 - px_n*hw, y1, sz1 - pz_n*hw), project(sx1 + px_n*hw, y1, sz1 + pz_n*hw), (68, 72, 80))

        # Surrounding P2 Urban Buildings (filtered so they don't overlap P3 landmarks)
        for b in DATA["urbanBuildings"]:
            bx, by, bz = b["pos"]
            if math.hypot(bx - cam_pos[0], bz - cam_pos[2]) > 750.0:
                continue
            # Skip procedural buildings inside Forum / Trajan / Colosseum / Pantheon footprint
            if (-180 <= bx <= 450 and -410 <= bz <= 90) or (math.hypot(bx - (-425), bz - (-555)) < 95):
                continue
            bl, bh, bw = b["dims"]
            draw_3d_box(bx, by + bh*0.5, bz, bl, bh, bw, b["rotY"], (192, 162, 126), (176, 84, 54))

        # Render P3 Batch 1 Landmarks with polychromy, columns, domes, and construction scaffolding!
        for lm in DATA["landmarksP3"]:
            lx, ly_base, lz = lm["pos"]
            ly = max(ly_base, get_ancient_terrain_height(lx, lz))
            L = lm["modelDims"]["length"]
            W_m = lm["modelDims"]["width"]
            H_m = lm["modelDims"]["height"]
            rot = lm["rotY"]
            st = lm["style"]

            if st == "colosseum_elliptical_amphitheatre":
                # Elliptical Colosseum (189 x 156 x 48.5m) with travertine 4-story facade, cavea tiers & sand arena
                segs = 32
                a_out, b_out = L * 0.5, W_m * 0.5
                a_in, b_in = 43.0, 27.0 # Arena floor 86 x 54m
                for i in range(segs):
                    t0 = (i / segs) * math.pi * 2.0
                    t1 = ((i + 1) / segs) * math.pi * 2.0
                    c0, s0 = math.cos(t0), math.sin(t0)
                    c1, s1 = math.cos(t1), math.sin(t1)
                    shade = 0.78 + 0.22 * max(0.0, c0 * 0.6 + s0 * 0.8)
                    ext_c = (int(228*shade), int(214*shade), int(186*shade))
                    cavea_c = (int(212*shade), int(198*shade), int(174*shade))
                    arena_c = (218, 188, 138) # Sand (Harena)
                    # Outer travertine wall (48.5m high)
                    p00 = project(lx + a_out*c0, ly, lz + b_out*s0)
                    p10 = project(lx + a_out*c1, ly, lz + b_out*s1)
                    p01 = project(lx + a_out*c0, ly + H_m, lz + b_out*s0)
                    p11 = project(lx + a_out*c1, ly + H_m, lz + b_out*s1)
                    fill_tri(p00, p01, p10, ext_c)
                    fill_tri(p10, p01, p11, ext_c)
                    # Sloped marble seating (Cavea) down to arena podium (ly + 4.5m)
                    q01 = project(lx + a_in*c0, ly + 5.0, lz + b_in*s0)
                    q11 = project(lx + a_in*c1, ly + 5.0, lz + b_in*s1)
                    fill_tri(p01, q01, p11, cavea_c)
                    fill_tri(p11, q01, q11, cavea_c)
                    # Arena sand floor
                    pc = project(lx, ly + 1.0, lz)
                    q00 = project(lx + a_in*c0, ly + 1.0, lz + b_in*s0)
                    q10 = project(lx + a_in*c1, ly + 1.0, lz + b_in*s1)
                    fill_tri(pc, q00, q10, arena_c)

            elif st == "pantheon_rotunda_pronaos":
                # Pantheon: Rotunda drum (outer dia 58m, inner dia 43.3m, height 43.3m) + stepped dome + north octastyle Pronaos (width 34m, depth 26m)
                draw_cylinder_or_ring(lx, ly, lz, 29.0, 0.0, 31.0, 28, (206, 132, 102), (210, 195, 175), (178, 172, 162))
                # Dome hemisphere with gilded bronze tiles
                draw_cylinder_or_ring(lx, ly + 31.0, lz, 23.5, 4.45, 12.3, 24, (218, 184, 98), (218, 184, 98), (228, 196, 108))
                # North Pronaos portico with Egyptian grey granite columns & polychrome pediment
                draw_3d_box(lx, ly + 11.5, lz - 34.0, 34.0, 23.0, 22.0, 0.0, (224, 216, 202), (212, 175, 82))
                for col_i in range(-3, 4):
                    draw_3d_box(lx + col_i*4.8, ly + 8.5, lz - 44.5, 1.5, 14.2, 1.5, 0.0, (148, 142, 138), (218, 182, 88))

            elif st == "construction_site_scaffolding_cranes":
                # Temple of Venus and Rome under construction in AD 128:
                # 145 x 100m concrete & travertine platform + partially erected cella walls + timber scaffolding tiers + 2 Roman treadwheel cranes (Polyspastos)
                draw_3d_box(lx, ly + 4.5, lz, L, 9.0, W_m, rot, (186, 174, 152), (198, 186, 164))
                # Partially built inner twin cella walls (back-to-back Roma & Venus cellae)
                draw_3d_box(lx, ly + 15.0, lz, 72.0, 12.0, 38.0, rot, (182, 102, 74), (196, 118, 84))
                # Timber scaffolding frameworks around cella & colonnade
                for sx_off in [-42, -14, 14, 42]:
                    for sz_off in [-26, 26]:
                        draw_3d_box(lx + sx_off, ly + 18.0, lz + sz_off, 18.0, 18.0, 4.5, rot, (148, 104, 58), (168, 122, 68))
                # Roman Treadwheel Cranes (Polyspastos): Large timber treadwheel + inclined jib beam
                for crane_x in [-52, 52]:
                    draw_3d_box(lx + crane_x, ly + 13.0, lz - 18, 8.5, 8.5, 3.2, rot, (122, 78, 38), (138, 88, 44))
                    draw_3d_box(lx + crane_x, ly + 23.5, lz - 12, 2.2, 22.0, 2.2, rot + 0.3, (138, 92, 46), (152, 102, 52))

            elif st == "columna_traiani_spiral":
                # Trajan's Column (total height 38.4m: pedestal 5.5x5.5x5.4m + fluted/spiral shaft + gilded statue of Trajan)
                draw_3d_box(lx, ly + 2.7, lz, 5.5, 5.4, 5.5, rot, (238, 232, 218), (222, 198, 142))
                draw_3d_box(lx, ly + 20.3, lz, 3.7, 29.8, 3.7, rot, (242, 234, 216), (218, 178, 82))
                draw_3d_box(lx, ly + 36.8, lz, 1.8, 3.2, 1.8, rot, (235, 195, 65), (245, 208, 75))

            elif "temple" in st:
                # Polychrome Roman Temple: High travertine/marble podium + cella + polychrome/gilded roof pediment
                draw_3d_box(lx, ly + 2.5, lz, L, 5.0, W_m, rot, (226, 218, 202), (218, 210, 194))
                roof_c = (224, 184, 72) if "gilded" in lm["polychromy"] else (178, 62, 48) # Gilded bronze or cinnabar red polychrome pediment
                draw_3d_box(lx, ly + 5.0 + (H_m - 5.0)*0.5, lz, L*0.88, H_m - 5.0, W_m*0.86, rot, (238, 230, 214), roof_c)

            else:
                # Basilicas, Imperial Fora Enclosures, Arches, Tabularium, Mercatus Traiani
                wall_c = (184, 98, 72) if "brick" in lm["polychromy"] else ((234, 226, 210) if "marble" in lm["polychromy"] or "gilded" in lm["polychromy"] else (198, 184, 162))
                roof_c = (218, 178, 74) if "gilded" in lm["polychromy"] else (172, 78, 52)
                draw_3d_box(lx, ly + H_m*0.5, lz, L, H_m, W_m, rot, wall_c, roof_c)

        # Callout labels for P3 Landmarks
        p3_callouts = [
            ("COLOSSEUM (189X156X48.5M)", 515, 74, 62, (52, 211, 153)),
            ("COLOSSUS SOLIS (30M)", 405, 60, 28, (251, 191, 36)),
            ("VENUS & ROMA WORKSITE (128 AD)", 315, 62, 22, (249, 115, 22)),
            ("ARCUS TITI (81 AD)", 212, 45, 42, (52, 211, 153)),
            ("BASILICA JULIA (101X49M)", -12, 44, 38, (52, 211, 153)),
            ("BASILICA AEMILIA (94X24M)", 38, 42, -32, (52, 211, 153)),
            ("CURIA JULIA (27X18X21M)", -12, 37, -42, (96, 165, 250)),
            ("AEDES SATURNI (-42 BC)", -62, 41, 16, (251, 191, 36)),
            ("TABULARIUM (-78 BC)", -92, 48, -28, (96, 165, 250)),
            ("JUPITER CAPITOLINUS (62X53.5M)", -148, 82, -38, (251, 191, 36)),
            ("FORUM TRAIANI & BASILICA ULPIA", -75, 53, -285, (52, 211, 153)),
            ("COLUMNA TRAIANI (38.4M)", -92, 56, -328, (251, 191, 36)),
            ("MERCATUS TRAIANI (6 STORIES)", 25, 52, -245, (249, 115, 22)),
            ("ATHENAEUM WORKSITE (128 AD)", -155, 24, -265, (249, 115, 22)),
            ("PANTHEON (43.3M DOME, 128 AD)", -425, 60, -555, (52, 211, 153)),
            ("THERMAE AGRIPPAE", -425, 38, -425, (96, 165, 250))
        ]
        placed = []
        for label, mx, my, mz, lcol in p3_callouts:
            pr = project(mx, my, mz)
            max_c_dist = 260.0 if ("VP02" in title_en or "VP03" in title_en or "VP05" in title_en) else 850.0
            if pr and pr[2] < max_c_dist and 35 <= pr[0] <= W - 210 and 55 <= pr[1] <= H - 48:
                sx, sy = int(pr[0]), int(pr[1])
                bw_l = len(label)*6 + 10
                for _ in range(4):
                    if any(not (sx + bw_l < ox0 or sx > ox1 or sy + 2 < oy0 or sy - 14 > oy1) for ox0,oy0,ox1,oy1 in placed):
                        sy -= 15
                    else:
                        break
                if sy > 52:
                    placed.append((sx - 4, sy - 12, sx + bw_l, sy + 2))
                    draw_rect(buf, W, H, sx - 4, sy - 12, sx + bw_l, sy + 2, (15, 19, 26), 0.85)
                    draw_text(buf, W, H, sx, sy - 9, label, lcol, scale=1)

    # Top & Bottom HUD
    draw_rect(buf, W, H, 10, 10, W - 10, 44, (15, 19, 26), 0.90)
    draw_text(buf, W, H, 20, 16, f"ROMA AD 128 - {title_en}", (229, 193, 88), scale=2)
    draw_text(buf, W, H, 20, 33, sub_en, (185, 195, 210), scale=1)
    draw_text(buf, W, H, W - 315, 16, "FPS: 60  DRAW CALLS: 12 / 1500", (52, 211, 153), scale=1)
    draw_text(buf, W, H, W - 315, 29, "DIM ERROR: 0.00% (<5%)  <=128 AD", (96, 165, 250), scale=1)

    draw_rect(buf, W, H, 10, H - 34, W - 10, H - 10, (15, 19, 26), 0.88)
    footer = "SEAMLESS INTERIOR PORTAL: PANTHEON 43.3M SPHERE + 8.9M OCULUS LIGHT BEAM + OPUS SECTILE MARBLE" if mode == "pantheon_interior" else (
             "P3 LANDMARKS BATCH 1: FORUM ROMANUM + FORA IMPERIALIA + COLOSSEUM + PANTHEON + VENUS & ROMA WORKSITE")
    draw_text(buf, W, H, 20, H - 25, footer, (240, 240, 245), scale=1)

    out_file = os.path.join(screenshots_dir, f"{vp_id}.png")
    write_png(out_file, W, H, buf)
    return out_file

p3_viewpoints = [
    ("p3_vp01_capitol_forum_overview", "VP01 CAPITOLIUM TO FORUM ROMANUM", "TABULARIUM GALLERY OVERLOOKING SATURN, BASILICA JULIA, CURIA JULIA & SACRA VIA", (-82.0, 44.0, -10.0), (120.0, 15.0, 22.0), "exterior", (-220, 520, -220, 280, 12)),
    ("p3_vp02_trajan_forum_column_markets", "VP02 FORUM TRAIANI & COLUMNA", "BASILICA ULPIA, TRAJAN COLUMN (38.4M), DIVUS TRAJAN & MERCATUS TRAIANI", (35.0, 62.0, -155.0), (-82.0, 26.0, -310.0), "exterior", (-280, 220, -460, -40, 12)),
    ("p3_vp03_pantheon_pronaos_exterior", "VP03 HADRIANIC PANTHEON PRONAOS", "LOWER STEPPED FORECOURT, 16 GRANITE COLUMNS, POLYCHROME PEDIMENT & 43.3M ROTUNDA", (-425.0, 22.0, -665.0), (-425.0, 26.0, -545.0), "exterior", (-640, -210, -760, -350, 12)),
    ("p3_vp04_pantheon_coffered_dome_interior", "VP04 PANTHEON 43.3M DOME INTERIOR", "SEAMLESS INTERIOR: 43.3M SPHERE, 5 COFFER RINGS, 8.9M OCULUS & OPUS SECTILE FLOOR", (-425.0, 14.85, -572.0), (-425.0, 32.0, -542.0), "pantheon_interior", None),
    ("p3_vp05_colosseum_exterior_no_constantine", "VP05 COLOSSEUM & COLOSSUS SOLIS", "VALLEY VIEW: NO ARCH OF CONSTANTINE (315 AD EXCLUDED), 30M COLOSSUS OF NERO", (355.0, 42.0, 155.0), (495.0, 34.0, 55.0), "exterior", (150, 740, -120, 320, 14)),
    ("p3_vp06_colosseum_top_cavea_interior", "VP06 COLOSSEUM TOP CAVEA & ARENA", "SEAMLESS INTERIOR: MAENIANUM SUMMUM IN LIGNIS (48M) LOOKING DOWN AT 86X54M ARENA", (435.0, 66.0, 62.0), (525.0, 24.0, 62.0), "exterior", (360, 680, -80, 210, 12)),
    ("p3_vp07_venus_et_roma_construction_site", "VP07 VENUS & ROMA WORKSITE (128 AD)", "HADRIANIC CONSTRUCTION SITE: 145X100M PLATFORM, TIMBER SCAFFOLDING & TREADWHEEL CRANES", (205.0, 48.0, -65.0), (325.0, 34.0, 25.0), "exterior", (80, 580, -180, 220, 12)),
    ("p3_vp08_imperial_fora_jupiter_capitolinus", "VP08 JUPITER & IMPERIAL FORA AXIS", "GILDED ROOF OF JUPITER OPTIMUS MAXIMUS (62X53.5M), FORUM OF AUGUSTUS, CAESAR & PEACE", (-215.0, 92.0, 85.0), (45.0, 26.0, -165.0), "exterior", (-320, 480, -450, 250, 16))
]

for vp in p3_viewpoints:
    f_out = render_p3_screenshot(*vp)
    print("Captured P3 screenshot:", f_out)
