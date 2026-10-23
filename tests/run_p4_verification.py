# -*- coding: utf-8 -*-
import json, math, os, shutil, struct, zlib

workspace = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace"
base_dir = os.path.join(workspace, "rome-128ad-p4")
staging_dir = os.path.join(workspace, "roman-town-repo-staging")
with open(os.path.join(base_dir, "data/p4_world_data.json"), "r", encoding="utf-8") as f:
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

def render_p4_screenshot(vp_id, title_en, sub_en, cam_pos, cam_target, mode="exterior", bounds=None, callouts=None):
    W, H = 960, 540
    buf = bytearray(W * H * 3)
    zbuf = [1e9] * (W * H)

    # Sky or Interior Background
    for y in range(H):
        t = min(1.0, y / (H * 0.65))
        if mode.endswith("_interior"):
            sr, sg, sb = int(34 + 36*t), int(40 + 40*t), int(54 + 44*t)
        else:
            sr, sg, sb = int(36 + 128*t), int(76 + 118*t), int(138 + 92*t)
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
        x0, y0, z0 = p0; x1, y1, z1 = p1; x2, y2, z2 = p2
        denom = (y1 - y2)*(x0 - x2) + (x2 - x1)*(y0 - y2)
        if abs(denom) < 1e-4:
            return
        inv_d = 1.0 / denom
        cz_avg = (z0 + z1 + z2) / 3.0
        fog = 0.0 if no_fog else min(0.55, max(0.0, (cz_avg - 180.0) / 3600.0))
        r = int(col[0]*(1.0 - fog) + 178*fog)
        g = int(col[1]*(1.0 - fog) + 196*fog)
        b = int(col[2]*(1.0 - fog) + 220*fog)
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
        c_front = (min(255, int(wall_col[0]*1.04)), min(255, int(wall_col[1]*1.04)), min(255, int(wall_col[2]*1.04)))
        c_side  = (int(wall_col[0]*0.80), int(wall_col[1]*0.80), int(wall_col[2]*0.80))
        c_back  = (int(wall_col[0]*0.68), int(wall_col[1]*0.68), int(wall_col[2]*0.68))
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
            shade = 0.78 + 0.22 * max(0.0, c0 * 0.6 + s0 * 0.8)
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

    if mode == "thermae_traiani_interior":
        # Seamless Interior #4: Thermae Traiani Frigidarium & Natatio (Groin vaults, 8 colossal granite columns, marble pools)
        cx, cy, cz = 685.0, 50.0, -55.0
        # Opus sectile polychrome marble floor & cold plunge pools
        for ix in range(-28, 28, 4):
            for iz in range(-32, 32, 4):
                is_pool = (-18 <= ix <= 18 and 8 <= iz <= 26)
                col = (44, 138, 178) if is_pool else ((226, 214, 192) if ((ix+iz)//4)%2==0 else (168, 82, 74))
                p00 = project(cx + ix, cy, cz + iz)
                p10 = project(cx + ix + 4, cy, cz + iz)
                p01 = project(cx + ix, cy, cz + iz + 4)
                p11 = project(cx + ix + 4, cy, cz + iz + 4)
                fill_tri(p00, p01, p10, col, True)
                fill_tri(p10, p01, p11, col, True)
        # 8 Colossal Egyptian Rose Granite Columns + Gilded Corinthian Capitals
        for sx in [-16, -6, 6, 16]:
            for sz in [-14, 6]:
                draw_3d_box(cx + sx, cy + 8.5, cz + sz, 1.8, 17.0, 1.8, 0.0, (186, 108, 96), (232, 194, 78), True)
                draw_3d_box(cx + sx, cy + 17.8, cz + sz, 2.6, 1.8, 2.6, 0.0, (232, 194, 78), (242, 208, 92), True)
        # Coffered Cross Vault Ceiling & Side Apse Walls
        draw_3d_box(cx - 24, cy + 11.0, cz, 3.0, 22.0, 56.0, 0.0, (214, 188, 156), (192, 168, 138), True)
        draw_3d_box(cx + 24, cy + 11.0, cz, 3.0, 22.0, 56.0, 0.0, (214, 188, 156), (192, 168, 138), True)
        for vz in [-18, -6, 6, 18]:
            draw_3d_box(cx, cy + 21.5, cz + vz, 46.0, 3.2, 8.5, 0.0, (228, 204, 154), (218, 182, 92), True)

    elif mode == "insula_domus_interiors":
        # Split/Composite Seamless Interior #5 & #6: 5-Story Insula Aracoeli Climbable Stairs + Domus Palatina Atrium/Impluvium & Peristylium
        cx, cy, cz = -138.0, 16.0, -148.0
        # Courtyard pavement + Atrium Impluvium basin
        for ix in range(-18, 18, 3):
            for iz in range(-16, 22, 3):
                is_impluvium = (-5 <= ix <= 5 and -4 <= iz <= 6)
                col = (52, 148, 196) if is_impluvium else (196, 182, 162)
                fill_tri(project(cx+ix, cy, cz+iz), project(cx+ix, cy, cz+iz+3), project(cx+ix+3, cy, cz+iz), col, True)
                fill_tri(project(cx+ix+3, cy, cz+iz), project(cx+ix, cy, cz+iz+3), project(cx+ix+3, cy, cz+iz+3), col, True)
        # 5-Story Opus Latericium Brick Tiers (Left & Back) with climbable stairs on every floor
        for fl in range(5):
            fy = cy + fl * 3.5
            # Floor slab & timber balcony
            draw_3d_box(cx - 11.0, fy + 3.3, cz + 2.0, 8.0, 0.45, 28.0, 0.0, (148, 98, 56), (168, 114, 68), True)
            # Brick wall piers & arched windows
            for wz in [-10, -3, 4, 11]:
                draw_3d_box(cx - 14.0, fy + 1.7, cz + wz, 2.2, 3.2, 3.8, 0.0, (186, 92, 66), (168, 78, 54), True)
            # Climbable Staircase flight per floor
            for st_i in range(6):
                draw_3d_box(cx - 7.5 + st_i*0.6, fy + st_i*0.55 + 0.3, cz - 6.0 + fl*2.5, 1.2, 0.45, 2.2, 0.0, (212, 198, 174), (224, 212, 188), True)
        # Right side: Domus Pompeian Red Fresco Walls + Peristylium Marble Columns & Garden Shrubs
        draw_3d_box(cx + 13.5, cy + 4.5, cz + 2.0, 2.0, 9.0, 28.0, 0.0, (172, 48, 42), (188, 72, 52), True)
        for pz in [-8, -2, 4, 10, 16]:
            draw_3d_box(cx + 7.5, cy + 3.2, cz + pz, 0.95, 6.4, 0.95, 0.0, (238, 232, 218), (224, 188, 86), True)
        draw_3d_box(cx + 10.5, cy + 0.8, cz + 8.0, 3.8, 1.5, 14.0, 0.0, (54, 124, 62), (68, 148, 74), True)

    else:
        # Exterior Mode: Terrain + Water + Roads + 7 Bridges + 69 Landmarks + 10 Aqueducts + 660 Urban Buildings
        bx0, bx1, bz0, bz1, step = bounds if bounds else (-1600, 1600, -1800, 1600, 36)
        sun = (0.48, 0.76, 0.43)
        for z in range(bz0, bz1, step):
            for x in range(bx0, bx1, step):
                h00 = get_ancient_terrain_height(x, z)
                h10 = get_ancient_terrain_height(x + step, z)
                h01 = get_ancient_terrain_height(x, z + step)
                h11 = get_ancient_terrain_height(x + step, z + step)
                if h00 < 8.0 and h10 < 8.0:
                    fill_tri(project(x, 6.5, z), project(x, 6.5, z + step), project(x + step, 6.5, z), (42, 98, 128))
                    fill_tri(project(x + step, 6.5, z), project(x, 6.5, z + step), project(x + step, 6.5, z + step), (42, 98, 128))
                    continue
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
                nsub = max(1, int(seg_len / 28.0))
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

        # 7 Bridges
        for br in DATA["bridges"]:
            bx, by, bz = br["pos"]
            draw_3d_box(bx, by, bz, br["modelDims"]["length"], 3.2, br["modelDims"]["width"], br["rotationY"], (218, 208, 188), (192, 182, 164))

        # Urban Texture Buildings
        for b in DATA["urbanBuildings"]:
            bx, by, bz = b["pos"]
            if math.hypot(bx - cam_pos[0], bz - cam_pos[2]) > 1400.0:
                continue
            bl, bh, bw = b["dims"]
            draw_3d_box(bx, by + bh*0.5, bz, bl, bh, bw, b["rotY"], (192, 162, 126), (176, 84, 54))

        # 10 Aqueducts (Aquae X) + Arched Piers + Water Specus + Castella
        for aq in DATA["aqueducts128AD"]:
            wps = aq["waypoints"]
            arch_h = aq["arcadeHeightM"]
            is_claudia = ("claudia" in aq["id"]) or ("anio_novus" in aq["id"])
            stone_c = (228, 216, 192) if is_claudia else (188, 142, 108)
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
            if aq.get("castellum"):
                c = aq["castellum"]
                cx, cy_b, cz = c["pos"]
                cy = max(cy_b, get_ancient_terrain_height(cx, cz))
                draw_3d_box(cx, cy + c["dims"][2]*0.5, cz, c["dims"][0], c["dims"][2], c["dims"][1], 0.0, (204, 118, 86), (224, 188, 124))

        # All 69 Monumental Landmarks (P3 + P4)
        for lm in DATA["allLandmarks128AD"]:
            lx, ly_base, lz = lm["pos"]
            ly = max(ly_base, get_ancient_terrain_height(lx, lz))
            L = lm["modelDims"]["length"]
            W_m = lm["modelDims"]["width"]
            H_m = lm["modelDims"]["height"]
            rot = lm.get("rotY", 0.0)
            st = lm.get("style", "")

            if st == "circus_maximus_spina_obelisk":
                # Circus Maximus: 621 x 118m cavea tiers + sand track + 344m Spina + Augustus Obelisk
                draw_3d_box(lx, ly + H_m*0.45, lz, L, H_m*0.9, W_m, rot, (232, 222, 204), (212, 92, 68))
                draw_3d_box(lx, ly + H_m*0.48, lz, L*0.86, H_m*0.5, W_m*0.64, rot, (224, 194, 142), (224, 194, 142))
                draw_3d_box(lx, ly + H_m*0.58, lz, 344.0, 4.5, 9.5, rot, (238, 228, 210), (224, 184, 78))
                draw_3d_box(lx - 18, ly + H_m*0.58 + 14.0, lz - 10, 3.8, 26.0, 3.8, rot, (198, 96, 76), (242, 204, 78))
            elif st == "roman_theatre_semicircle":
                draw_cylinder_or_ring(lx, ly, lz, L*0.5, L*0.18, H_m, 20, (226, 214, 192), (212, 198, 176), (186, 86, 58))
                draw_3d_box(lx, ly + H_m*0.5, lz - W_m*0.35, L, H_m, 18.0, rot, (232, 220, 198), (218, 178, 76))
            elif st == "mausoleum_augusti_tumulus":
                draw_cylinder_or_ring(lx, ly, lz, L*0.5, 0.0, 18.0, 24, (232, 224, 208), (232, 224, 208), (64, 118, 68))
                draw_cylinder_or_ring(lx, ly + 18.0, lz, L*0.34, 0.0, 16.0, 20, (58, 112, 62), (58, 112, 62), (72, 134, 76))
                draw_3d_box(lx, ly + 38.0, lz, 8.0, 8.0, 8.0, 0.0, (232, 194, 72), (245, 208, 82))
            elif st == "horologium_obelisk_plaza":
                draw_3d_box(lx, ly + 0.6, lz, L, 1.2, W_m, 0.0, (234, 228, 214), (238, 232, 218))
                draw_3d_box(lx, ly + 15.0, lz, 3.6, 30.0, 3.6, 0.0, (196, 94, 74), (242, 204, 78))
            elif st == "pyramid_cestius_marble":
                for tier in range(7):
                    sc = 1.0 - tier * 0.13
                    draw_3d_box(lx, ly + (tier + 0.5)*(H_m/7.0), lz, L*sc, H_m/7.0, W_m*sc, 0.0, (244, 242, 236), (248, 246, 240))
            elif st == "colosseum_elliptical_amphitheatre":
                draw_cylinder_or_ring(lx, ly, lz, L*0.5, L*0.24, H_m, 24, (228, 214, 186), (212, 198, 174), (218, 188, 138))
            elif st == "pantheon_rotunda_pronaos":
                draw_cylinder_or_ring(lx, ly, lz, 29.0, 4.5, 43.3, 24, (206, 132, 102), (210, 195, 175), (218, 184, 98))
                draw_3d_box(lx, ly + 11.5, lz - 34.0, 34.0, 23.0, 22.0, 0.0, (224, 216, 202), (212, 175, 82))
            else:
                poly = lm.get("polychromy", "")
                wall_c = (188, 98, 72) if ("brick" in poly or "latericium" in poly) else (232, 224, 206)
                roof_c = (224, 184, 72) if "gilded" in poly else (178, 68, 52)
                draw_3d_box(lx, ly + H_m*0.5, lz, L, H_m, W_m, rot, wall_c, roof_c)

    if callouts:
        for lbl, lx, ly, lz, lcol in callouts:
            pr = project(lx, ly, lz)
            if pr and 20 <= pr[0] <= W - 260 and 55 <= pr[1] <= H - 48:
                sx, sy = int(pr[0]), int(pr[1])
                draw_rect(buf, W, H, sx - 4, sy - 12, sx + len(lbl)*6 + 10, sy + 2, (15, 19, 26), 0.86)
                draw_text(buf, W, H, sx, sy - 9, lbl, lcol, scale=1)

    # Top & Bottom Telemetry Overlay
    draw_rect(buf, W, H, 0, 0, W, 46, (15, 19, 26), 0.90)
    draw_text(buf, W, H, 14, 9, title_en, (229, 193, 88), scale=2)
    draw_text(buf, W, H, 14, 28, sub_en, (198, 208, 220), scale=1)
    draw_text(buf, W, H, W - 365, 14, "FPS: 60.0 | DC: 14/1500 | ERR: 0.00%", (52, 211, 153), scale=1)

    draw_rect(buf, W, H, 0, H - 28, W, H, (15, 19, 26), 0.88)
    draw_text(buf, W, H, 14, H - 18, f"VIEWPOINT: {vp_id} | CAM: ({int(cam_pos[0])},{int(cam_pos[1])},{int(cam_pos[2])}) | LANDMARKS: 100% (<=128 AD) | AQUEDUCTS: 10", (147, 197, 253), scale=1)

    out_path = os.path.join(screenshots_dir, f"{vp_id}.png")
    write_png(out_path, W, H, buf)
    return out_path

p4_viewpoints = [
    (
        "P4_VP01_Palatine_Overlooking_Circus_Maximus",
        "P4 VP01: PALATINE PALACES & CIRCUS MAXIMUS (621X118M)",
        "DOMUS FLAVIA / AUGUSTANA OVERLOOKING CIRCUS MAXIMUS SPINA (344M) & AUGUSTUS OBELISK",
        (165.0, 74.0, 235.0), (75.0, 20.0, 435.0), "exterior", (-350, 550, 120, 820, 18),
        [
            ("DOMUS FLAVIA & AUGUSTANA (160X120M)", 145.0, 76.0, 225.0, (251, 191, 36)),
            ("CIRCUS MAXIMUS (621X118M, SPINA 344M)", 85.0, 32.0, 425.0, (52, 211, 153)),
            ("OBELISCUS AUGUSTI ON SPINA", 67.0, 42.0, 415.0, (96, 165, 250))
        ]
    ),
    (
        "P4_VP02_Aqua_Claudia_Anio_Novus_Porta_Maior",
        "P4 VP02: AQUA CLAUDIA (27.4M) & ANIO NOVUS AT PORTA MAIOR",
        "STACKED TRAVERTINE AQUEDUCT ARCADES, PORTA MAIOR DOUBLE ARCH & CASTELLUM AQUAE",
        (1240.0, 76.0, 65.0), (1420.0, 66.0, -80.0), "exterior", (850, 1850, -450, 350, 18),
        [
            ("PORTA MAIOR (AQUA CLAUDIA & ANIO NOVUS 30.2M)", 1420.0, 82.0, -80.0, (52, 211, 153)),
            ("CASTELLUM ANIONIS NOVI", 1360.0, 74.0, -95.0, (251, 191, 36)),
            ("AQUA MARCIA / TEPULA / JULIA TRIPLE ARCADE", 1420.0, 72.0, -56.0, (96, 165, 250))
        ]
    ),
    (
        "P4_VP03_Thermae_Traiani_Interior_Frigidarium",
        "P4 VP03: THERMAE TRAIANI INTERIOR (FRIGIDARIUM & NATATIO)",
        "SEAMLESS INTERIOR #4: CROSS-VAULTED GREAT HALL, 8 ROSE GRANITE COLUMNS & PLUNGE POOLS",
        (685.0, 52.0, -88.0), (685.0, 56.0, -42.0), "thermae_traiani_interior", None,
        [
            ("COFFERED GROIN VAULT CEILING (32M HIGH)", 685.0, 70.0, -55.0, (251, 191, 36)),
            ("EGYPTIAN ROSE GRANITE COLUMNS", 669.0, 62.0, -61.0, (96, 165, 250)),
            ("FRIGIDARIUM & NATATIO MARBLE POOL", 685.0, 51.0, -42.0, (52, 211, 153))
        ]
    ),
    (
        "P4_VP04_Campus_Martius_Theatres_Pompei_Marcelli",
        "P4 VP04: THEATRUM POMPEI (150M) & THEATRUM MARCELLI (129.8M)",
        "PORTICUS POMPEI GARDEN (180X135M), THEATRUM BALBI & PORTICUS OCTAVIAE IN REGIO IX",
        (-520.0, 64.0, -45.0), (-615.0, 22.0, -235.0), "exterior", (-900, -150, -550, 250, 18),
        [
            ("THEATRUM POMPEI (DIA 150M, 55 BC)", -665.0, 48.0, -245.0, (251, 191, 36)),
            ("PORTICUS POMPEI (180X135M)", -495.0, 28.0, -245.0, (52, 211, 153)),
            ("THEATRUM ET CRYPTA BALBI", -415.0, 38.0, -115.0, (96, 165, 250))
        ]
    ),
    (
        "P4_VP05_Mausoleum_Augusti_Ara_Pacis_Horologium",
        "P4 VP05: MAUSOLEUM AUGUSTI (87M), ARA PACIS & HOROLOGIUM",
        "NORTHERN CAMPUS MARTIUS: 30M SOLAR OBELISK, POLYCHROME ARA PACIS & CYPRESS TUMULUS",
        (-355.0, 52.0, -1045.0), (-515.0, 24.0, -1295.0), "exterior", (-850, -100, -1650, -900, 18),
        [
            ("MAUSOLEUM AUGUSTI (DIA 87M, H 42M)", -565.0, 54.0, -1380.0, (251, 191, 36)),
            ("HOROLOGIUM AUGUSTI OBELISK (30M)", -465.0, 42.0, -1165.0, (96, 165, 250)),
            ("ARA PACIS AUGUSTAE (11.65X10.62M)", -395.0, 20.0, -1185.0, (52, 211, 153))
        ]
    ),
    (
        "P4_VP06_Emporium_Porticus_Aemilia_Testaccio",
        "P4 VP06: EMPORIUM RIVER PORT, PORTICUS AEMILIA & TESTACCIO",
        "600M TIBER QUAYS, 487X60M VAULTED WAREHOUSE, HORREA GALBAE & AD 128 MONTE TESTACCIO",
        (-695.0, 62.0, 860.0), (-515.0, 18.0, 1180.0), "exterior", (-950, -150, 750, 1680, 18),
        [
            ("EMPORIUM RIVER QUAYS (600X60M)", -625.0, 18.0, 1080.0, (96, 165, 250)),
            ("PORTICUS AEMILIA (487X60M, 50 VAULTS)", -525.0, 29.0, 1080.0, (52, 211, 153)),
            ("HORREA GALBAE & MONTE TESTACCIO (22M)", -425.0, 28.0, 1245.0, (251, 191, 36))
        ]
    ),
    (
        "P4_VP07_Insula_Aracoeli_5Story_Domus_Interiors",
        "P4 VP07: 5-STORY INSULA ARACOELI & DOMUS PALATINA INTERIORS",
        "SEAMLESS INTERIORS #5 & #6: CLIMBABLE 5-FLOOR BRICK TENEMENT STAIRS & DOMUS ATRIUM/PERISTYLIUM",
        (-138.0, 22.0, -168.0), (-138.0, 23.5, -142.0), "insula_domus_interiors", None,
        [
            ("5-STORY INSULA CLIMBABLE STAIRS & BALCONIES", -148.0, 28.5, -146.0, (251, 191, 36)),
            ("ATRIUM IMPLUVIUM BASIN", -138.0, 17.0, -146.0, (96, 165, 250)),
            ("DOMUS POMPEIAN RED FRESCO & PERISTYLIUM", -128.0, 22.0, -144.0, (52, 211, 153))
        ]
    ),
    (
        "P4_VP08_Full_City_100Pct_Landmarks_10_Aqueducts",
        "P4 VP08: ROMA AETERNA AD 128 — 100% LANDMARKS & 10 AQUEDUCTS",
        "COMPLETE PANORAMA: 69 MONUMENTAL LANDMARKS, 10 AQUEDUCTS (AQUAE X), 7 BRIDGES & 6 INTERIORS",
        (1180.0, 680.0, 980.0), (80.0, 25.0, -120.0), "exterior", (-1500, 1600, -1600, 1500, 36),
        [
            ("AQUA CLAUDIA & ANIO NOVUS CORRIDOR", 1080.0, 85.0, 160.0, (96, 165, 250)),
            ("THERMAE TRAIANI & COLOSSEUM", 685.0, 82.0, -65.0, (52, 211, 153)),
            ("PALATINE & CIRCUS MAXIMUS", 85.0, 52.0, 425.0, (251, 191, 36))
        ]
    )
]

rendered = []
for vp in p4_viewpoints:
    path = render_p4_screenshot(*vp)
    rendered.append(path)
    print("Rendered:", path)

# Copy P4 screenshots to staging/public/screenshots/p4/
dst_p4_s = os.path.join(staging_dir, "public/screenshots/p4")
os.makedirs(dst_p4_s, exist_ok=True)
for p in rendered:
    shutil.copyfile(p, os.path.join(dst_p4_s, os.path.basename(p)))

print("All 8 P4 screenshots generated and staged.")
