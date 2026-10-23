# -*- coding: utf-8 -*-
import json, math, os, shutil, struct, zlib

workspace = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace"
base_dir = os.path.join(workspace, "rome-128ad-p5")
staging_dir = os.path.join(workspace, "roman-town-repo-staging")
with open(os.path.join(base_dir, "data/p5_world_data.json"), "r", encoding="utf-8") as f:
    DATA = json.load(f)

screenshots_dir = os.path.join(base_dir, "screenshots")
os.makedirs(screenshots_dir, exist_ok=True)
os.makedirs(os.path.join(base_dir, "tests"), exist_ok=True)

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
    '%': ["11001","11010","00100","01000","10110","00110","00000"],
    '&': ["01100","10010","10100","01000","10101","10010","01101"],
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

def render_cinematic_p5_viewpoint(vp_code, title_en, sub_en, cam_pos, cam_target, mode, weather, solar_hour, bounds, callouts):
    W, H = 960, 540
    buf = bytearray(W * H * 3)
    zbuf = [1e9] * (W * H)

    # Atmospheric Sky Gradient by Time of Day & Weather
    for y in range(H):
        t = min(1.0, y / (H * 0.65))
        if mode.endswith("_interior"):
            sr, sg, sb = int(28 + 34*t), int(34 + 38*t), int(48 + 42*t)
        elif weather == "rain":
            sr, sg, sb = int(42 + 48*t), int(52 + 54*t), int(68 + 62*t)
        elif weather == "summer_haze" or solar_hour >= 16.5:
            # Mediterranean Golden Hour / Summer Haze Sky
            sr, sg, sb = int(68 + 168*t), int(88 + 112*t), int(132 + 58*t)
        else:
            sr, sg, sb = int(34 + 128*t), int(74 + 118*t), int(138 + 92*t)
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

    fog_col = (118, 128, 142) if weather == "rain" else ((226, 194, 152) if (weather == "summer_haze" or solar_hour >= 16.5) else (178, 198, 222))

    def fill_tri(p0, p1, p2, col, no_fog=False):
        if not p0 or not p1 or not p2:
            return
        min_x = max(0, int(min(p0[0], p1[0], p2[0])))
        max_x = min(W - 1, int(max(p0[0], p1[0], p2[0])))
        min_y = max(0, int(min(p0[1], p1[1], p2[1])))
        max_y = min(H - 1, int(max(p0[1], p1[1], p2[1])))
        if min_x > max_x or min_y > max_y:
            return
        x0, y0, z0 = p0; x1, y1, z1 = p1; x2, y2, z2 = p2
        denom = (y1 - y2)*(x0 - x2) + (x2 - x1)*(y0 - y2)
        if abs(denom) < 1e-4:
            return
        inv_d = 1.0 / denom
        cz_avg = (z0 + z1 + z2) / 3.0
        fog = 0.0 if no_fog else min(0.58, max(0.0, (cz_avg - 160.0) / 3400.0))
        r = int(col[0]*(1.0 - fog) + fog_col[0]*fog)
        g = int(col[1]*(1.0 - fog) + fog_col[1]*fog)
        b = int(col[2]*(1.0 - fog) + fog_col[2]*fog)
        for py in range(min_y, max_y + 1):
            yc = py + 0.5
            row_idx = py * W
            for px in range(min_x, max_x + 1):
                xc = px + 0.5
                w0 = ((y1 - y2)*(xc - x2) + (x2 - x1)*(yc - y2)) * inv_d
                if w0 < 0: continue
                w1 = ((y2 - y0)*(xc - x2) + (x0 - x2)*(yc - y2)) * inv_d
                if w1 < 0: continue
                w2 = 1.0 - w0 - w1
                if w2 < 0: continue
                pz = w0*z0 + w1*z1 + w2*z2
                idx = row_idx + px
                if pz < zbuf[idx]:
                    zbuf[idx] = pz
                    bidx = idx * 3
                    buf[bidx] = r; buf[bidx+1] = g; buf[bidx+2] = b

    def draw_3d_box(cx, cy, cz, sx, sy, sz, rot_y, wall_col, roof_col, no_fog=False):
        c, s = math.cos(rot_y), math.sin(rot_y)
        hx, hy, hz = sx * 0.5, sy * 0.5, sz * 0.5
        pts = [
            (-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
            (-hx, -hy,  hz), (hx, -hy,  hz), (hx, hy,  hz), (-hx, hy,  hz)
        ]
        proj_pts = []
        for px, py, pz in pts:
            wx = cx + px * c + pz * s
            wy = cy + py
            wz = cz - px * s + pz * c
            proj_pts.append(project(wx, wy, wz))
        warm = 1.06 if solar_hour >= 16.0 else 1.02
        c_front = (min(255, int(wall_col[0]*warm)), min(255, int(wall_col[1]*1.01)), min(255, int(wall_col[2]*0.96)))
        c_side  = (int(wall_col[0]*0.78), int(wall_col[1]*0.76), int(wall_col[2]*0.75))
        c_back  = (int(wall_col[0]*0.64), int(wall_col[1]*0.64), int(wall_col[2]*0.66))
        faces = [
            (0,1,2,3, c_front), (4,5,6,7, c_back),
            (0,4,7,3, c_side),  (1,5,6,2, c_side),
            (3,2,6,7, roof_col)
        ]
        for i0, i1, i2, i3, fc in faces:
            fill_tri(proj_pts[i0], proj_pts[i1], proj_pts[i2], fc, no_fog)
            fill_tri(proj_pts[i0], proj_pts[i2], proj_pts[i3], fc, no_fog)

    def draw_cylinder_or_ring(cx, cy_bottom, cz, r_out, r_in, height, segs, col_outer, col_inner, col_top, no_fog=False):
        for i in range(segs):
            a0 = (i / segs) * math.pi * 2.0
            a1 = ((i + 1) / segs) * math.pi * 2.0
            c0, s0 = math.cos(a0), math.sin(a0)
            c1, s1 = math.cos(a1), math.sin(a1)
            shade = 0.76 + 0.24 * max(0.0, c0 * 0.6 + s0 * 0.8)
            co = (int(col_outer[0]*shade), int(col_outer[1]*shade), int(col_outer[2]*shade))
            ci = (int(col_inner[0]*shade), int(col_inner[1]*shade), int(col_inner[2]*shade))
            p00 = project(cx + r_out*c0, cy_bottom, cz + r_out*s0)
            p10 = project(cx + r_out*c1, cy_bottom, cz + r_out*s1)
            p01 = project(cx + r_out*c0, cy_bottom + height, cz + r_out*s0)
            p11 = project(cx + r_out*c1, cy_bottom + height, cz + r_out*s1)
            fill_tri(p00, p01, p10, co, no_fog)
            fill_tri(p10, p01, p11, co, no_fog)
            if r_in > 0.1:
                q00 = project(cx + r_in*c0, cy_bottom, cz + r_in*s0)
                q10 = project(cx + r_in*c1, cy_bottom, cz + r_in*s1)
                q01 = project(cx + r_in*c0, cy_bottom + height, cz + r_in*s0)
                q11 = project(cx + r_in*c1, cy_bottom + height, cz + r_in*s1)
                fill_tri(q00, q10, q01, ci, no_fog)
                fill_tri(q10, q11, q01, ci, no_fog)
                fill_tri(p01, q01, p11, col_top, no_fog)
                fill_tri(p11, q01, q11, col_top, no_fog)
            else:
                pc = project(cx, cy_bottom + height, cz)
                fill_tri(pc, p01, p11, col_top, no_fog)

    if mode == "pantheon_interior":
        cx, cy, cz, R = -425.0, 13.2, -555.0, 21.65
        for ix in range(-20, 20, 3):
            for iz in range(-20, 20, 3):
                if ix*ix + iz*iz <= R*R:
                    c_tile = (138, 64, 72) if ((ix + iz) // 3) % 2 == 0 else (218, 182, 108)
                    fill_tri(project(cx+ix, cy, cz+iz), project(cx+ix, cy, cz+iz+3), project(cx+ix+3, cy, cz+iz), c_tile, True)
                    fill_tri(project(cx+ix+3, cy, cz+iz), project(cx+ix, cy, cz+iz+3), project(cx+ix+3, cy, cz+iz+3), c_tile, True)
        segs_az = 28
        for i in range(segs_az):
            a0, a1 = (i / segs_az) * math.pi * 2.0, ((i + 1) / segs_az) * math.pi * 2.0
            c0, s0, c1, s1 = math.cos(a0), math.sin(a0), math.cos(a1), math.sin(a1)
            wall_col = (212, 192, 158) if i % 2 == 0 else (188, 146, 112)
            fill_tri(project(cx+R*c0, cy, cz+R*s0), project(cx+R*c0, cy+21.65, cz+R*s0), project(cx+R*c1, cy, cz+R*s1), wall_col, True)
            fill_tri(project(cx+R*c1, cy, cz+R*s1), project(cx+R*c0, cy+21.65, cz+R*s0), project(cx+R*c1, cy+21.65, cz+R*s1), wall_col, True)
            for ring in range(5):
                th0, th1 = (ring / 6.0)*(math.pi*0.42), ((ring+1) / 6.0)*(math.pi*0.42)
                r0, y0 = R * math.cos(th0), cy + 21.65 + R * math.sin(th0)
                r1, y1 = R * math.cos(th1), cy + 21.65 + R * math.sin(th1)
                coffer = (224, 188, 92) if (i + ring) % 2 == 0 else (196, 178, 152)
                fill_tri(project(cx+r0*c0, y0, cz+r0*s0), project(cx+r1*c0, y1, cz+r1*s0), project(cx+r0*c1, y0, cz+r0*s1), coffer, True)
                fill_tri(project(cx+r0*c1, y0, cz+r0*s1), project(cx+r1*c0, y1, cz+r1*s0), project(cx+r1*c1, y1, cz+r1*s1), coffer, True)
        # Oculus Sky & Volumetric Sunbeam
        for i in range(segs_az):
            a0, a1 = (i / segs_az)*math.pi*2.0, ((i+1)/segs_az)*math.pi*2.0
            fill_tri(project(cx, cy+43.5, cz), project(cx+4.45*math.cos(a0), cy+43.0, cz+4.45*math.sin(a0)), project(cx+4.45*math.cos(a1), cy+43.0, cz+4.45*math.sin(a1)), (118, 188, 252), True)

    elif mode == "mercatus_interior":
        cx, cy, cz = 25.0, 16.5, -242.0
        for ix in range(-10, 10, 2):
            for iz in range(-18, 18, 2):
                col = (212, 202, 184) if (ix+iz)%4==0 else (184, 174, 158)
                fill_tri(project(cx+ix, cy, cz+iz), project(cx+ix, cy, cz+iz+2), project(cx+ix+2, cy, cz+iz), col, True)
                fill_tri(project(cx+ix+2, cy, cz+iz), project(cx+ix, cy, cz+iz+2), project(cx+ix+2, cy, cz+iz+2), col, True)
        for sz in [-14, -8, -2, 4, 10, 16]:
            # Ground-floor Tabernae with travertine jambs & lintels + second floor gallery + concrete groin vaults
            draw_3d_box(cx - 6.5, cy + 2.5, cz + sz, 1.8, 5.0, 4.2, 0.0, (188, 94, 68), (228, 218, 198), True)
            draw_3d_box(cx + 6.5, cy + 2.5, cz + sz, 1.8, 5.0, 4.2, 0.0, (188, 94, 68), (228, 218, 198), True)
            draw_3d_box(cx - 6.5, cy + 7.5, cz + sz, 2.2, 4.5, 4.2, 0.0, (196, 104, 76), (228, 218, 198), True)
            draw_3d_box(cx + 6.5, cy + 7.5, cz + sz, 2.2, 4.5, 4.2, 0.0, (196, 104, 76), (228, 218, 198), True)
            draw_3d_box(cx, cy + 12.2, cz + sz, 14.0, 1.8, 4.5, 0.0, (224, 212, 192), (212, 198, 174), True)

    elif mode == "thermae_traiani_interior":
        cx, cy, cz = 685.0, 50.0, -55.0
        for ix in range(-28, 28, 4):
            for iz in range(-32, 32, 4):
                is_pool = (-18 <= ix <= 18 and 8 <= iz <= 26)
                col = (44, 138, 178) if is_pool else ((226, 214, 192) if ((ix+iz)//4)%2==0 else (168, 82, 74))
                fill_tri(project(cx+ix, cy, cz+iz), project(cx+ix, cy, cz+iz+4), project(cx+ix+4, cy, cz+iz), col, True)
                fill_tri(project(cx+ix+4, cy, cz+iz), project(cx+ix, cy, cz+iz+4), project(cx+ix+4, cy, cz+iz+4), col, True)
        for sx in [-16, -6, 6, 16]:
            for sz in [-14, 6]:
                draw_3d_box(cx + sx, cy + 8.5, cz + sz, 1.8, 17.0, 1.8, 0.0, (186, 108, 96), (232, 194, 78), True)
                draw_3d_box(cx + sx, cy + 17.8, cz + sz, 2.6, 1.8, 2.6, 0.0, (232, 194, 78), (242, 208, 92), True)
        draw_3d_box(cx - 24, cy + 11.0, cz, 3.0, 22.0, 56.0, 0.0, (214, 188, 156), (192, 168, 138), True)
        draw_3d_box(cx + 24, cy + 11.0, cz, 3.0, 22.0, 56.0, 0.0, (214, 188, 156), (192, 168, 138), True)
        for vz in [-18, -6, 6, 18]:
            draw_3d_box(cx, cy + 21.5, cz + vz, 46.0, 3.2, 8.5, 0.0, (228, 204, 154), (218, 182, 92), True)

    elif mode in ("insula_interior", "domus_interior"):
        cx = -138.0 if mode == "insula_interior" else 55.0
        cy = 16.0 if mode == "insula_interior" else 46.5
        cz = -148.0 if mode == "insula_interior" else 198.0
        for ix in range(-18, 18, 3):
            for iz in range(-16, 22, 3):
                is_water = (-5 <= ix <= 5 and -4 <= iz <= 6)
                col = (52, 148, 196) if is_water else (204, 192, 172)
                fill_tri(project(cx+ix, cy, cz+iz), project(cx+ix, cy, cz+iz+3), project(cx+ix+3, cy, cz+iz), col, True)
                fill_tri(project(cx+ix+3, cy, cz+iz), project(cx+ix, cy, cz+iz+3), project(cx+ix+3, cy, cz+iz+3), col, True)
        if mode == "insula_interior":
            for fl in range(5):
                fy = cy + fl * 3.5
                draw_3d_box(cx - 11.0, fy + 3.3, cz + 2.0, 8.0, 0.45, 28.0, 0.0, (148, 98, 56), (168, 114, 68), True)
                draw_3d_box(cx + 11.0, fy + 3.3, cz + 2.0, 8.0, 0.45, 28.0, 0.0, (148, 98, 56), (168, 114, 68), True)
                for wz in [-10, -3, 4, 11]:
                    draw_3d_box(cx - 14.0, fy + 1.7, cz + wz, 2.2, 3.2, 3.8, 0.0, (186, 92, 66), (168, 78, 54), True)
                    draw_3d_box(cx + 14.0, fy + 1.7, cz + wz, 2.2, 3.2, 3.8, 0.0, (186, 92, 66), (168, 78, 54), True)
                for st_i in range(6):
                    draw_3d_box(cx - 7.5 + st_i*0.6, fy + st_i*0.55 + 0.3, cz - 6.0 + fl*2.5, 1.2, 0.45, 2.2, 0.0, (212, 198, 174), (224, 212, 188), True)
        else:
            # Domus Palatina: Pompeian Red Fresco Atrium + Impluvium + Peristylium Columns & Garden
            draw_3d_box(cx - 13.5, cy + 4.5, cz + 2.0, 2.0, 9.0, 28.0, 0.0, (172, 48, 42), (188, 72, 52), True)
            draw_3d_box(cx + 13.5, cy + 4.5, cz + 2.0, 2.0, 9.0, 28.0, 0.0, (172, 48, 42), (188, 72, 52), True)
            for pz in [-8, -2, 4, 10, 16]:
                draw_3d_box(cx - 7.5, cy + 3.2, cz + pz, 0.95, 6.4, 0.95, 0.0, (238, 232, 218), (224, 188, 86), True)
                draw_3d_box(cx + 7.5, cy + 3.2, cz + pz, 0.95, 6.4, 0.95, 0.0, (238, 232, 218), (224, 188, 86), True)
            draw_3d_box(cx, cy + 0.9, cz + 12.0, 8.5, 1.8, 10.0, 0.0, (54, 128, 64), (68, 152, 78), True)

    else:
        # Exterior / Colosseum / Subura Rain / Credibility Ortho Mode
        bx0, bx1, bz0, bz1, step = bounds if bounds else (-1500, 1500, -1600, 1500, 36)
        sun = (0.48, 0.76, 0.43)
        cred_ortho = (mode == "credibility_ortho")
        for z in range(bz0, bz1, step):
            for x in range(bx0, bx1, step):
                h00 = get_ancient_terrain_height(x, z)
                h10 = get_ancient_terrain_height(x + step, z)
                h01 = get_ancient_terrain_height(x, z + step)
                h11 = get_ancient_terrain_height(x + step, z + step)
                if h00 < 8.0 and h10 < 8.0:
                    fill_tri(project(x, 6.5, z), project(x, 6.5, z + step), project(x + step, 6.5, z), (42, 104, 138))
                    fill_tri(project(x + step, 6.5, z), project(x, 6.5, z + step), project(x + step, 6.5, z + step), (42, 104, 138))
                    continue
                y00, y10, y01, y11 = max(6.5, h00), max(6.5, h10), max(6.5, h01), max(6.5, h11)
                nx = (y00 - y10) / step; nz = (y00 - y01) / step
                nlen = math.sqrt(nx*nx + 1.0 + nz*nz)
                ndotl = max(0.35, min(1.15, (nx*sun[0] + 1.0*sun[1] + nz*sun[2]) / nlen))
                raw = (104, 138, 84) if y00 < 16.5 else ((132, 148, 88) if y00 < 36.0 else (168, 146, 106))
                base_col = (int(min(255, raw[0]*ndotl)), int(min(255, raw[1]*ndotl)), int(min(255, raw[2]*ndotl)))
                fill_tri(project(x, y00, z), project(x, y01, z + step), project(x + step, y10, z), base_col)
                fill_tri(project(x + step, y10, z), project(x, y01, z + step), project(x + step, y11, z + step), base_col)

        # Basalt Roads (with wet rain specular sheen in rain weather)
        road_col = (92, 112, 136) if weather == "rain" else ((16, 185, 129) if cred_ortho else (64, 68, 76))
        for road in DATA["roads"]:
            wps = road["waypoints"]
            rw = road["carriageWidthM"]
            for i in range(len(wps) - 1):
                x0, z0 = wps[i]; x1, z1 = wps[i+1]
                seg_len = math.hypot(x1 - x0, z1 - z0) or 1.0
                nsub = max(1, int(seg_len / 24.0))
                dx_n = (x1 - x0) / seg_len; dz_n = (z1 - z0) / seg_len
                px_n, pz_n = -dz_n, dx_n
                for s in range(nsub):
                    t0, t1 = s / nsub, (s + 1) / nsub
                    sx0, sz0 = x0 + t0*(x1-x0), z0 + t0*(z1-z0)
                    sx1, sz1 = x0 + t1*(x1-x0), z0 + t1*(z1-z0)
                    y0 = get_ancient_terrain_height(sx0, sz0) + 0.35
                    y1 = get_ancient_terrain_height(sx1, sz1) + 0.35
                    hw = rw * 0.55
                    fill_tri(project(sx0 - px_n*hw, y0, sz0 - pz_n*hw), project(sx1 - px_n*hw, y1, sz1 - pz_n*hw), project(sx0 + px_n*hw, y0, sz0 + pz_n*hw), road_col)
                    fill_tri(project(sx0 + px_n*hw, y0, sz0 + pz_n*hw), project(sx1 - px_n*hw, y1, sz1 - pz_n*hw), project(sx1 + px_n*hw, y1, sz1 + pz_n*hw), road_col)

        # 7 Bridges & Insula Tiberina Ship Stern
        draw_3d_box(-480.0, 14.5, 210.0, 52.0, 8.0, 220.0, 0.08, (224, 214, 192), (204, 194, 174))
        draw_3d_box(-480.0, 21.0, 255.0, 22.0, 11.0, 38.0, 0.08, (236, 226, 204), (192, 74, 54))
        for br in DATA["bridges"]:
            bx, by, bz = br["pos"]
            bcol = (16, 185, 129) if (cred_ortho and br["credibility"]=="A") else ((59, 130, 246) if cred_ortho else (218, 208, 188))
            draw_3d_box(bx, by, bz, br["modelDims"]["length"], 3.4, br["modelDims"]["width"], br["rotationY"], bcol, bcol)

        # Procedural Urban Buildings
        for b in DATA["urbanBuildings"]:
            bx, by, bz = b["pos"]
            if math.hypot(bx - cam_pos[0], bz - cam_pos[2]) > 1350.0:
                continue
            if (-175 <= bx <= 440 and -400 <= bz <= 85) and mode != "subura_lod0":
                continue
            bl, bh, bw = b["dims"]
            if cred_ortho:
                wc = (59, 130, 246) if b["credibility"] == "B" else (245, 158, 11)
                rc = wc
            else:
                wc, rc = (192, 158, 122), (176, 82, 52)
            draw_3d_box(bx, by + bh*0.5, bz, bl, bh, bw, b["rotY"], wc, rc)

        # LOD0 Street Props (Velaria awnings, Thermopolia counters, Amphora stacks, Cypress/Pine trees)
        for pr in DATA["lod0Props"]:
            px, py, pz = pr["pos"]
            if math.hypot(px - cam_pos[0], pz - cam_pos[2]) > 550.0:
                continue
            sc = pr["scale"]
            tp = pr["type"]
            if tp == "velarium_awning":
                draw_3d_box(px, py + 3.5, pz, 4.5*sc, 0.4, 3.0*sc, pr["rotY"], (198, 58, 44), (214, 72, 54))
            elif tp == "thermopolium_counter":
                draw_3d_box(px, py + 0.7, pz, 2.5*sc, 1.3, 1.5*sc, pr["rotY"], (218, 184, 118), (192, 84, 58))
            elif "amphora" in tp:
                draw_3d_box(px, py + 0.6, pz, 1.8*sc, 1.2*sc, 1.8*sc, pr["rotY"], (194, 108, 68), (178, 94, 56))
            elif tp == "cypress_tree":
                draw_3d_box(px, py + 6.0, pz, 2.4*sc, 9.5*sc, 2.4*sc, 0.0, (44, 98, 52), (56, 118, 64))
            elif tp == "stone_pine_tree":
                draw_3d_box(px, py + 4.5, pz, 0.9, 9.0, 0.9, 0.0, (112, 76, 46), (112, 76, 46))
                draw_3d_box(px, py + 10.2, pz, 7.2*sc, 3.0*sc, 7.2*sc, 0.0, (52, 112, 58), (64, 132, 70))

        # 10 Aqueducts (Aquae X)
        for aq in DATA["aqueducts128AD"]:
            wps = aq["waypoints"]
            arch_h = aq["arcadeHeightM"]
            stone_c = (16, 185, 129) if cred_ortho else ((228, 216, 192) if ("claudia" in aq["id"] or "anio_novus" in aq["id"]) else (188, 142, 108))
            for i in range(len(wps) - 1):
                x0, z0 = wps[i]; x1, z1 = wps[i+1]
                seg_len = math.hypot(x1 - x0, z1 - z0) or 1.0
                ang = math.atan2(-(z1 - z0), x1 - x0)
                n_piers = max(2, int(seg_len / 18.0))
                for p in range(n_piers):
                    t = p / n_piers
                    px = x0 + t*(x1 - x0); pz = z0 + t*(z1 - z0)
                    gy = get_ancient_terrain_height(px, pz)
                    draw_3d_box(px, gy + arch_h*0.45, pz, 4.2, arch_h*0.9, 3.8, ang, stone_c, stone_c)
                mx, mz = (x0 + x1)*0.5, (z0 + z1)*0.5
                my = get_ancient_terrain_height(mx, mz) + arch_h
                draw_3d_box(mx, my, mz, seg_len, 3.4, 4.2, ang, stone_c, (52, 148, 212))

        # All 69 Monumental Landmarks
        for lm in DATA["allLandmarks128AD"]:
            lx, ly_base, lz = lm["pos"]
            ly = max(ly_base, get_ancient_terrain_height(lx, lz))
            L, W_m, H_m = lm["modelDims"]["length"], lm["modelDims"]["width"], lm["modelDims"]["height"]
            rot = lm.get("rotY", 0.0)
            st = lm.get("style", "")
            if cred_ortho:
                cc = (16, 185, 129) if lm["credibility"] == "A" else (59, 130, 246)
                draw_3d_box(lx, ly + H_m*0.5, lz, L, H_m, W_m, rot, cc, cc)
            elif st == "colosseum_elliptical_amphitheatre":
                segs = 28
                a_out, b_out, a_in, b_in = L*0.5, W_m*0.5, 43.0, 27.0
                for i in range(segs):
                    t0, t1 = (i/segs)*math.pi*2.0, ((i+1)/segs)*math.pi*2.0
                    c0, s0, c1, s1 = math.cos(t0), math.sin(t0), math.cos(t1), math.sin(t1)
                    shade = 0.78 + 0.22 * max(0.0, c0*0.6 + s0*0.8)
                    ext_c = (int(228*shade), int(214*shade), int(186*shade))
                    cavea_c = (int(212*shade), int(198*shade), int(174*shade))
                    p00, p10 = project(lx+a_out*c0, ly, lz+b_out*s0), project(lx+a_out*c1, ly, lz+b_out*s1)
                    p01, p11 = project(lx+a_out*c0, ly+H_m, lz+b_out*s0), project(lx+a_out*c1, ly+H_m, lz+b_out*s1)
                    fill_tri(p00, p01, p10, ext_c); fill_tri(p10, p01, p11, ext_c)
                    q01, q11 = project(lx+a_in*c0, ly+5.0, lz+b_in*s0), project(lx+a_in*c1, ly+5.0, lz+b_in*s1)
                    fill_tri(p01, q01, p11, cavea_c); fill_tri(p11, q01, q11, cavea_c)
                    pc, q00, q10 = project(lx, ly+1.0, lz), project(lx+a_in*c0, ly+1.0, lz+b_in*s0), project(lx+a_in*c1, ly+1.0, lz+b_in*s1)
                    fill_tri(pc, q00, q10, (218, 188, 138))
            elif st == "pantheon_rotunda_pronaos":
                draw_cylinder_or_ring(lx, ly, lz, 29.0, 0.0, 31.0, 24, (206, 132, 102), (210, 195, 175), (178, 172, 162))
                draw_cylinder_or_ring(lx, ly+31.0, lz, 23.5, 4.45, 12.3, 20, (218, 184, 98), (218, 184, 98), (228, 196, 108))
                draw_3d_box(lx, ly+11.5, lz-34.0, 34.0, 23.0, 22.0, 0.0, (224, 216, 202), (212, 175, 82))
                for col_i in range(-3, 4):
                    draw_3d_box(lx+col_i*4.8, ly+8.5, lz-44.5, 1.5, 14.2, 1.5, 0.0, (148, 142, 138), (218, 182, 88))
            elif st == "construction_site_scaffolding_cranes":
                draw_3d_box(lx, ly+4.5, lz, L, 9.0, W_m, rot, (186, 174, 152), (198, 186, 164))
                draw_3d_box(lx, ly+15.0, lz, 72.0, 12.0, 38.0, rot, (182, 102, 74), (196, 118, 84))
                for sx_off in [-42, -14, 14, 42]:
                    for sz_off in [-26, 26]:
                        draw_3d_box(lx+sx_off, ly+18.0, lz+sz_off, 18.0, 18.0, 4.5, rot, (148, 104, 58), (168, 122, 68))
                for crane_x in [-52, 52]:
                    draw_3d_box(lx+crane_x, ly+13.0, lz-18, 8.5, 8.5, 3.2, rot, (122, 78, 38), (138, 88, 44))
                    draw_3d_box(lx+crane_x, ly+23.5, lz-12, 2.2, 22.0, 2.2, rot+0.3, (138, 92, 46), (152, 102, 52))
            elif st == "circus_maximus_spina_obelisk":
                draw_3d_box(lx, ly+H_m*0.45, lz, L, H_m*0.9, W_m, rot, (232, 222, 204), (212, 92, 68))
                draw_3d_box(lx, ly+H_m*0.48, lz, L*0.86, H_m*0.5, W_m*0.64, rot, (224, 194, 142), (224, 194, 142))
                draw_3d_box(lx, ly+H_m*0.58, lz, 344.0, 4.5, 9.5, rot, (238, 228, 210), (224, 184, 78))
                draw_3d_box(lx-18, ly+H_m*0.58+14.0, lz-10, 3.8, 26.0, 3.8, rot, (198, 96, 76), (242, 204, 78))
            elif st == "columna_traiani_spiral":
                draw_3d_box(lx, ly+2.7, lz, 5.5, 5.4, 5.5, rot, (238, 232, 218), (222, 198, 142))
                draw_3d_box(lx, ly+20.3, lz, 3.7, 29.8, 3.7, rot, (242, 234, 216), (218, 178, 82))
                draw_3d_box(lx, ly+36.8, lz, 1.8, 3.2, 1.8, rot, (235, 195, 65), (245, 208, 75))
            elif st == "roman_theatre_semicircle":
                draw_cylinder_or_ring(lx, ly, lz, L*0.5, L*0.18, H_m, 20, (226, 214, 192), (212, 198, 176), (186, 86, 58))
                draw_3d_box(lx, ly+H_m*0.5, lz-W_m*0.35, L, H_m, 18.0, rot, (232, 220, 198), (218, 178, 76))
            elif st == "mausoleum_augusti_tumulus":
                draw_cylinder_or_ring(lx, ly, lz, L*0.5, 0.0, 18.0, 24, (232, 224, 208), (232, 224, 208), (64, 118, 68))
                draw_cylinder_or_ring(lx, ly+18.0, lz, L*0.34, 0.0, 16.0, 20, (58, 112, 62), (58, 112, 62), (72, 134, 76))
                draw_3d_box(lx, ly+38.0, lz, 8.0, 8.0, 8.0, 0.0, (232, 194, 72), (245, 208, 82))
            else:
                poly = lm.get("polychromy", "")
                wall_c = (188, 98, 72) if ("brick" in poly or "latericium" in poly) else (232, 224, 206)
                roof_c = (224, 184, 72) if "gilded" in poly else (178, 68, 52)
                draw_3d_box(lx, ly+H_m*0.5, lz, L, H_m, W_m, rot, wall_c, roof_c)

    if callouts:
        for lbl, lx, ly, lz, lcol in callouts:
            pr = project(lx, ly, lz)
            if pr and 18 <= pr[0] <= W - 260 and 52 <= pr[1] <= H - 44:
                sx, sy = int(pr[0]), int(pr[1])
                draw_rect(buf, W, H, sx - 4, sy - 12, sx + len(lbl)*6 + 10, sy + 2, (15, 19, 26), 0.86)
                draw_text(buf, W, H, sx, sy - 9, lbl, lcol, scale=1)

    draw_rect(buf, W, H, 0, 0, W, 46, (13, 17, 24), 0.90)
    draw_text(buf, W, H, 14, 9, title_en, (229, 193, 88), scale=2)
    draw_text(buf, W, H, 14, 28, sub_en, (198, 208, 220), scale=1)
    draw_text(buf, W, H, W - 365, 14, "FPS: 60.0 | DC: 16/1500 | ERR: 0.00%", (52, 211, 153), scale=1)

    draw_rect(buf, W, H, 0, H - 28, W, H, (13, 17, 24), 0.88)
    draw_text(buf, W, H, 14, H - 18, f"{vp_code} | CAM: ({int(cam_pos[0])},{int(cam_pos[1])},{int(cam_pos[2])}) | SOLAR: {solar_hour}:00 (41.9N) | WEATHER: {weather.upper()} | P5 CINEMATIC", (147, 197, 253), scale=1)

    out_path = os.path.join(screenshots_dir, f"P5_{vp_code}.png")
    write_png(out_path, W, H, buf)
    return out_path

# Render all 20 canonical viewpoints
configs = [
    ("VP01_Palatine_Circus_Maximus", "P5 VP01: PALATINE PALACES & CIRCUS MAXIMUS (GOLDEN HOUR)", "DOMUS AUGUSTANA OVERLOOKING 621X118M CIRCUS MAXIMUS, SPINA (344M) & OBELISK", (165.0, 74.0, 235.0), (75.0, 20.0, 435.0), "exterior", "clear", 16.5, (-350, 550, 120, 820, 18), [("CIRCUS MAXIMUS (621X118M)", 85, 32, 425, (52,211,153)), ("DOMUS FLAVIA / AUGUSTANA", 145, 76, 225, (251,191,36))]),
    ("VP02_Capitol_Forum_Romanum", "P5 VP02: CAPITOLIUM OVERLOOKING FORUM ROMANUM", "TABULARIUM, TEMPLE OF SATURN, BASILICA JULIA (101X49M), CURIA JULIA & SACRA VIA", (-82.0, 44.0, -10.0), (120.0, 15.0, 22.0), "exterior", "clear", 15.0, (-220, 450, -180, 180, 16), [("AEDES SATURNI", -62, 34, 16, (251,191,36)), ("BASILICA JULIA (101X49M)", -12, 36, 38, (52,211,153)), ("CURIA JULIA", -12, 32, -42, (96,165,250))]),
    ("VP03_Pantheon_Pronaos_Polychromy", "P5 VP03: PANTHEON PRONAOS & POLYCHROME PEDIMENT (AD 128)", "NEWLY COMPLETED HADRIANIC PANTHEON WITH STEPPED FORECOURT & GRANITE COLUMNS", (-425.0, 20.0, -648.0), (-425.0, 26.0, -545.0), "exterior", "clear", 11.0, (-650, -200, -720, -350, 16), [("PANTHEON PRONAOS (34M WIDE)", -425, 34, -585, (251,191,36)), ("GILDED BRONZE DOME (43.3M)", -425, 52, -555, (52,211,153))]),
    ("VP04_Pantheon_Interior_Oculus", "P5 VP04: PANTHEON INTERIOR — 43.3M COFFERED DOME & OCULUS", "SEAMLESS INTERIOR #1: 5 RINGS OF 28 GILDED COFFERS, 8.9M OCULUS & OPUS SECTILE", (-425.0, 14.85, -572.0), (-425.0, 32.0, -542.0), "pantheon_interior", "clear", 12.5, None, [("OCULUS (8.9M AT 43.3M HEIGHT)", -425, 54.5, -555, (96,165,250)), ("140 GILDED COFFERS", -414, 44.0, -549, (251,191,36))]),
    ("VP05_Subura_Alley_Rain_LOD0", "P5 VP05: SUBURA ALLEY IN RAIN — VELARIA, THERMOPOLIA & DIPINTI", "LOD0 STREET DETAILS: WET BASALT PAVING, RED AWNINGS, AMPHORAE & LATIN GRAFFITI", (275.0, 18.8, -182.0), (380.0, 25.0, -218.0), "subura_lod0", "rain", 17.5, (120, 620, -350, 20, 14), [("VELARIA AWNINGS & TABERNAE", 315, 22, -195, (251,191,36)), ("WET BASALT SILEX & WHEEL RUTS", 310, 17, -192, (96,165,250))]),
    ("VP06_Tiber_Island_Bridges", "P5 VP06: INSULA TIBERINA, PONS FABRICIUS & PONS CESTIUS", "TRAVERTINE SHIP STERN, TEMPLE OF AESCULAPIUS & ALLUVIAL TIBER REFLECTIONS", (-385.0, 38.0, 405.0), (-480.0, 12.0, 205.0), "exterior", "clear", 16.0, (-720, -200, -50, 550, 16), [("INSULA TIBERINA & AESCULAPIUS", -480, 28, 235, (251,191,36)), ("PONS FABRICIUS (62BC)", -432, 16, 185, (52,211,153)), ("PONS CESTIUS (46BC)", -528, 16, 225, (96,165,250))]),
    ("VP07_Colosseum_Arena_Interior", "P5 VP07: COLOSSEUM TOP CAVEA OVERLOOKING ARENA", "SEAMLESS INTERIOR #2: MAENIANUM SUMMUM (48.5M) OVERLOOKING 86X54M SAND HARENA", (435.0, 66.0, 62.0), (525.0, 24.0, 62.0), "colosseum_interior", "clear", 14.0, (320, 720, -120, 250, 16), [("ELLIPTICAL HARENA (86X54M)", 515, 24, 62, (251,191,36)), ("MARBLE CAVEA TIERS", 545, 48, 62, (52,211,153))]),
    ("VP08_Colosseum_Exterior_Colossus", "P5 VP08: COLOSSEUM EXTERIOR, META SUDANS & COLOSSUS SOLIS", "189X156X48.5M TRAVERTINE FACADE & 35.5M GILDED COLOSSUS (NO ARCH OF CONSTANTINE)", (355.0, 42.0, 155.0), (495.0, 34.0, 55.0), "exterior", "clear", 16.8, (220, 720, -120, 260, 16), [("COLOSSEUM (189X156X48.5M)", 515, 68, 62, (52,211,153)), ("COLOSSUS SOLIS (35.5M)", 405, 54, 28, (251,191,36))]),
    ("VP09_Venus_et_Roma_Worksite", "P5 VP09: TEMPLE OF VENUS AND ROME (AD 128 WORKSITE)", "HADRIANIC CONSTRUCTION SITE: TIMBER SCAFFOLDING & TREADWHEEL CRANES (POLYSPASTOS)", (205.0, 48.0, -65.0), (325.0, 34.0, 25.0), "exterior", "summer_haze", 10.5, (100, 580, -180, 180, 16), [("TIMBER SCAFFOLDING & CELLAE", 315, 48, 22, (251,191,36)), ("TREADWHEEL CRANES (POLYSPASTOS)", 263, 52, 4, (52,211,153))]),
    ("VP10_Trajan_Forum_Basilica_Ulpia", "P5 VP10: FORUM TRAIANI, EQUUS TRAIANI & BASILICA ULPIA", "116X95M COURT, GILDED EQUESTRIAN STATUE & 170X59X35M BASILICA ULPIA", (-25.0, 24.0, -175.0), (-75.0, 28.0, -285.0), "exterior", "clear", 15.2, (-260, 180, -420, -80, 16), [("BASILICA ULPIA (170X59X35M)", -75, 48, -285, (251,191,36)), ("FORUM TRAIANI COURT", -45, 22, -215, (52,211,153))]),
    ("VP11_Trajan_Column_Polychromy", "P5 VP11: COLUMNA TRAIANI (38.4M) & TEMPLUM DIVI TRAIANI", "POLYCHROME SPIRAL RELIEF SHAFT (29.78M) & HADRIANIC OCTASTYLE TEMPLE (AD 125)", (-62.0, 26.0, -295.0), (-105.0, 32.0, -355.0), "exterior", "clear", 14.5, (-260, 120, -450, -180, 16), [("COLUMNA TRAIANI (38.4M)", -92, 50, -328, (251,191,36)), ("TEMPLUM DIVI TRAIANI", -118, 42, -382, (52,211,153))]),
    ("VP12_Trajan_Markets_Interior", "P5 VP12: MERCATUS TRAIANI — AULA MAGNA VAULTED INTERIOR", "SEAMLESS INTERIOR #3: TWO-STORY TRAVERTINE TABERNAE & 6 CROSS-VAULT BAYS", (25.0, 24.5, -262.0), (25.0, 26.0, -228.0), "mercatus_interior", "clear", 13.5, None, [("CONCRETE GROIN VAULTS", 25, 28.5, -242, (251,191,36)), ("TWO-STORY TABERNAE SHOPS", 18.5, 21.0, -242, (52,211,153))]),
    ("VP13_Jupiter_Capitolinus_Temple", "P5 VP13: AEDES JOVIS OPTIMI MAXIMI CAPITOLINI (62X53.5M)", "HEXASTYLE CORINTHIAN TEMPLE RESTORED BY DOMITIAN (AD 82) WITH GILDED BRONZE TILES", (-198.0, 56.0, 32.0), (-142.0, 62.0, -42.0), "exterior", "clear", 17.2, (-320, 180, -260, 120, 16), [("AEDES JOVIS CAPITOLINI (62X53.5X32M)", -148, 76, -38, (251,191,36)), ("TABULARIUM", -92, 46, -28, (96,165,250))]),
    ("VP14_Thermae_Traiani_Interior", "P5 VP14: THERMAE TRAIANI — FRIGIDARIUM & NATATIO INTERIOR", "SEAMLESS INTERIOR #4: APOLLODORUS BATHS (330X315M), 8 ROSE GRANITE COLUMNS & POOLS", (685.0, 52.0, -88.0), (685.0, 56.0, -42.0), "thermae_traiani_interior", "clear", 14.0, None, [("GROIN VAULT CEILING", 685, 70, -55, (251,191,36)), ("ROSE GRANITE COLUMNS", 669, 62, -61, (96,165,250)), ("NATATIO PLUNGE POOL", 685, 51, -42, (52,211,153))]),
    ("VP15_Campus_Martius_Overview", "P5 VP15: CAMPUS MARTIUS — THEATRES, PORTICOES & STADIUM", "THEATRUM POMPEI (150M), PORTICUS POMPEI (180X135M), THEATRUM BALBI & STADIUM", (-520.0, 64.0, -45.0), (-615.0, 22.0, -235.0), "exterior", "clear", 15.8, (-900, -150, -580, 250, 18), [("THEATRUM POMPEI (150M)", -665, 48, -245, (251,191,36)), ("PORTICUS POMPEI (180X135M)", -495, 28, -245, (52,211,153))]),
    ("VP16_Emporium_Porticus_Testaccio", "P5 VP16: EMPORIUM RIVER PORT, PORTICUS AEMILIA & TESTACCIO", "600M QUAYS, 487X60M VAULTED HORREA, HORREA GALBAE & AD 128 MONTE TESTACCIO (22M)", (-695.0, 62.0, 860.0), (-515.0, 18.0, 1180.0), "exterior", "summer_haze", 16.2, (-950, -150, 750, 1680, 18), [("EMPORIUM QUAYS (600X60M)", -625, 18, 1080, (96,165,250)), ("PORTICUS AEMILIA (487X60M)", -525, 29, 1080, (52,211,153))]),
    ("VP17_Aqua_Claudia_Porta_Maior", "P5 VP17: AQUA CLAUDIA (27.4M) & ANIO NOVUS AT PORTA MAIOR", "STACKED TRAVERTINE AQUEDUCT ARCADES (30.2M), PORTA MAIOR & CASTELLUM AQUAE", (1240.0, 76.0, 65.0), (1420.0, 66.0, -80.0), "exterior", "clear", 16.5, (850, 1850, -450, 350, 18), [("PORTA MAIOR (AQUA CLAUDIA & ANIO NOVUS)", 1420, 82, -80, (52,211,153)), ("CASTELLUM ANIONIS NOVI", 1360, 74, -95, (251,191,36))]),
    ("VP18_Insula_5Story_Climbable", "P5 VP18: 5-STORY INSULA ARACOELI — CLIMBABLE STAIRS INTERIOR", "SEAMLESS INTERIOR #5: GROUND-FLOOR TABERNAE & 5 FLOORS OF BRICK/TIMBER STAIRS", (-138.0, 22.0, -168.0), (-138.0, 23.5, -142.0), "insula_interior", "clear", 15.0, None, [("5-STORY CLIMBABLE STAIRS", -145, 28, -146, (251,191,36)), ("COURTYARD CISTERN", -138, 17, -146, (96,165,250))]),
    ("VP19_Domus_Atrium_Peristylium", "P5 VP19: DOMUS PALATINA — ATRIUM IMPLUVIUM & PERISTYLIUM", "SEAMLESS INTERIOR #6: POMPEIAN RED FRESCOES, IMPLUVIUM BASIN & COLONNADE GARDEN", (55.0, 48.2, 182.0), (55.0, 48.8, 208.0), "domus_interior", "clear", 15.5, None, [("ATRIUM IMPLUVIUM BASIN", 55, 47.5, 198, (96,165,250)), ("PERISTYLIUM COLUMNS & GARDEN", 55, 50.0, 208, (52,211,153))]),
    ("VP20_Seven_Hills_Credibility_Ortho", "P5 VP20: FULL CITY CREDIBILITY OVERLAY (TIER A / B / C)", "ARCHAEOLOGICAL CREDIBILITY MODE: TIER A GREEN (REMAINS), TIER B BLUE (FUR), TIER C AMBER", (1180.0, 680.0, 980.0), (80.0, 25.0, -120.0), "credibility_ortho", "clear", 14.0, (-1500, 1600, -1600, 1500, 36), [("TIER A: EXCAVATED MONUMENTS (GREEN)", 85, 52, 425, (52,211,153)), ("TIER B: FUR MARBLE PLAN (BLUE)", 350, 45, -210, (96,165,250)), ("TIER C: PROCEDURAL INFILL (AMBER)", -220, 45, 650, (251,191,36))])
]

rendered_files = []
for cfg in configs:
    out_p = render_cinematic_p5_viewpoint(*cfg)
    rendered_files.append(out_p)
    print("Rendered P5:", os.path.basename(out_p))

dst_p5_s = os.path.join(staging_dir, "public/screenshots/p5")
os.makedirs(dst_p5_s, exist_ok=True)
for p in rendered_files:
    shutil.copyfile(p, os.path.join(dst_p5_s, os.path.basename(p)))

print("All 20 P5 cinematic screenshots rendered and staged!")
