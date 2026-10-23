# -*- coding: utf-8 -*-
import json, math, os, random

workspace = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace"
p4_data_path = os.path.join(workspace, "rome-128ad-p4/data/p4_world_data.json")
p5_dir = os.path.join(workspace, "rome-128ad-p5")
p5_data_dir = os.path.join(p5_dir, "data")
os.makedirs(p5_data_dir, exist_ok=True)

with open(p4_data_path, "r", encoding="utf-8") as f:
    world_data = json.load(f)

random.seed(12805)

def get_ancient_terrain_height(x, z):
    h = 12.2 + 0.0012 * abs(x) + 0.0008 * abs(z)
    chan = world_data["tiberChannel"]
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

    for hill in world_data["hills"]:
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

# 1. LOD0 Street-Level Micro-Props (Within 10m walking view: Velaria awnings, Thermopolia counters, Amphorae stacks,
#    Street Lararia shrines, Travertine stepping stones, Wheel ruts, Torch sconces, Cypress/Stone Pine trees, Dipinti graffiti)
lod0_props = []

# Generate rich street props along Subura (Clivus Suburanus), Sacra Via, Forum Boarium, Mercatus Traiani, and Emporium
street_corridors = [
    ("subura", 95, -65, 660, -230, 48, ["velarium_awning", "thermopolium_counter", "amphora_cluster", "dipinti_graffiti", "lararium_shrine", "stepping_stones"]),
    ("sacra_via", -85, -20, 390, 42, 36, ["rostral_column", "bronze_brazier", "marble_statue_plinth", "honorific_stele"]),
    ("via_lata", -70, -220, -240, -1180, 44, ["velarium_awning", "portico_bench", "amphora_cluster", "bronze_brazier"]),
    ("emporium", -620, 880, -430, 1340, 64, ["amphora_dressel20_stack", "wooden_cargo_crane", "olive_oil_dolium", "travertine_bollard"]),
    ("campus_martius", -650, -580, -280, -220, 52, ["cypress_tree", "stone_pine_tree", "marble_herm", "fountain_lacus_basin"]),
    ("palatine_gardens", 15, 135, 245, 290, 40, ["cypress_tree", "stone_pine_tree", "marble_nymphaeum_urn", "bronze_brazier"])
]

prop_idx = 1
for zone, x0, z0, x1, z1, count, types in street_corridors:
    for i in range(count):
        t = (i + 0.5) / count
        lateral = random.choice([-1, 1]) * random.uniform(3.2, 14.5)
        dx = x1 - x0; dz = z1 - z0
        dist = math.hypot(dx, dz) or 1.0
        px = x0 + t * dx + (-dz / dist) * lateral + random.uniform(-2.0, 2.0)
        pz = z0 + t * dz + (dx / dist) * lateral + random.uniform(-2.0, 2.0)
        py = get_ancient_terrain_height(px, pz)
        ptype = types[i % len(types)]
        lod0_props.append({
            "id": f"prop.lod0.{zone}.{prop_idx:04d}",
            "zone": zone,
            "type": ptype,
            "pos": [round(px, 2), round(py, 2), round(pz, 2)],
            "rotY": round(math.atan2(-dz, dx) + (0.0 if lateral > 0 else math.pi), 3),
            "scale": round(random.uniform(0.88, 1.18), 2),
            "credibility": "A" if zone in ("sacra_via", "emporium") else ("B" if zone == "subura" else "C")
        })
        prop_idx += 1

# 2. Latin Wall Graffiti & Shop Signs (Dipinti & Programmata) for LOD0 Immersion
latin_dipinti = [
    {"id": "dipinti.subura.01", "pos": [282.0, 17.8, -184.5], "textLa": "C·IVLIVM·POLYBIVM·AED·OVF · PANEM·BONVM·FERT", "textZh": "請投蓋烏斯·尤利烏斯·波利比烏斯任營造官，他帶來好麵包", "color": "#991B1B"},
    {"id": "dipinti.subura.02", "pos": [312.5, 19.2, -196.0], "textLa": "CAUPONA·SALVI · VINVM·FALERNVM·ASSIBVS·II", "textZh": "薩爾維烏斯酒館：上等法萊爾諾葡萄酒每杯 2 阿斯", "color": "#1E293B"},
    {"id": "dipinti.subura.03", "pos": [348.0, 21.0, -208.0], "textLa": "FVLLONES·VBIQVE·SALVETE · VESPASIANVS·PECUNIAM·NON·OLERE", "textZh": "向全城的漂洗工致敬！", "color": "#991B1B"},
    {"id": "dipinti.mercatus.04", "pos": [28.0, 19.5, -242.0], "textLa": "STATIONES·AROMATARIVM · PIPER·ET·CINNAMOMVM·EX·INDIA", "textZh": "東方香料商行：供應印度胡椒與肉桂", "color": "#7C2D12"},
    {"id": "dipinti.emporium.05", "pos": [-535.0, 14.5, 1085.0], "textLa": "OLEVM·BAETICVM·EX·HISPANIA · PONDO·CCXL·ANNONA·AVG", "textZh": "西班牙貝蒂卡行省橄欖油 · 帝國糧政署驗收", "color": "#991B1B"}
]

# 3. 4 Spatial Audio Zones (Zero-anachronism Web Audio Synthesizer profiles: strictly NO church bells!)
audio_zones_128ad = [
    {
        "id": "audio.zone.forum_temples",
        "nameZh": "羅馬廣場與神廟聖域音場",
        "nameLa": "Sonitus Fori et Templorum",
        "center": [0.0, 13.0, -50.0],
        "radiusM": 380.0,
        "layers": ["orator_echo_latin", "sacred_brazier_crackle", "tibia_flute_harmonic", "fountain_lacus_juturnae"],
        "excludedAnachronisms": ["church_bells", "modern_sirens", "motor_engines"]
    },
    {
        "id": "audio.zone.subura_markets",
        "nameZh": "蘇布拉街區與圖拉真市場喧囂音場",
        "nameLa": "Sonitus Suburae et Mercatus",
        "center": [280.0, 18.0, -210.0],
        "radiusM": 420.0,
        "layers": ["plebeian_market_chatter", "blacksmith_anvil_clink", "wooden_cart_wheels_on_basalt", "thermopolium_sizzle"],
        "excludedAnachronisms": ["church_bells"]
    },
    {
        "id": "audio.zone.circus_amphitheatre",
        "nameZh": "大競技場與弗拉維競技場群眾音場",
        "nameLa": "Sonitus Spectaculorum",
        "center": [310.0, 22.0, 240.0],
        "radiusM": 460.0,
        "layers": ["distant_crowd_roar", "cornu_brass_horn", "meta_sudans_cascade", "chariot_hooves_rumble"],
        "excludedAnachronisms": ["church_bells"]
    },
    {
        "id": "audio.zone.tiber_emporium_aqueducts",
        "nameZh": "古台伯河港與高架輸水道流水音場",
        "nameLa": "Sonitus Tiberis et Aquarum",
        "center": [-520.0, 10.0, 580.0],
        "radiusM": 680.0,
        "layers": ["tiber_river_rapids_around_piers", "castellum_aquae_pour", "wooden_hull_creak_oars", "amphora_terracotta_clatter"],
        "excludedAnachronisms": ["church_bells"]
    }
]

# 4. Canonical 20 Fixed Viewpoints (VP01 to VP20) matching PROMPT_rome_argon.md & P0 Master Plan
viewpoints_20 = [
    {
        "code": "VP01", "key": "vp01_palatine_circus",
        "titleZh": "VP01: 從帕拉提諾山皇宮俯瞰大競技場與阿文提諾山",
        "titleLa": "Despectus e Domo Augustana in Circum Maximum",
        "pos": [165.0, 74.0, 235.0], "target": [75.0, 20.0, 435.0],
        "mode": "exterior", "solarHour": 16.5, "season": "summer", "weather": "clear"
    },
    {
        "code": "VP02", "key": "vp02_capitol_forum",
        "titleZh": "VP02: 從卡比托利歐山國家檔案館俯瞰羅馬廣場全景",
        "titleLa": "Despectus e Tabulario in Forum Romanum",
        "pos": [-82.0, 44.0, -10.0], "target": [120.0, 15.0, 22.0],
        "mode": "exterior", "solarHour": 15.0, "season": "spring", "weather": "clear"
    },
    {
        "code": "VP03", "key": "vp03_pantheon_pronaos",
        "titleZh": "VP03: 萬神殿北側廣場看向八柱科林斯門廊與彩繪山花",
        "titleLa": "Pantheon Hadriani — Pronaos Octastylus",
        "pos": [-425.0, 20.0, -648.0], "target": [-425.0, 26.0, -545.0],
        "mode": "exterior", "solarHour": 11.0, "season": "summer", "weather": "clear"
    },
    {
        "code": "VP04", "key": "vp04_pantheon_interior",
        "titleZh": "VP04: 萬神殿圓廳內部仰望 43.3m 藻井圓頂與中央圓洞光柱",
        "titleLa": "Pantheon — Tholus Lacunatus (43.3m) et Lumen Oculi",
        "pos": [-425.0, 14.85, -572.0], "target": [-425.0, 32.0, -542.0],
        "mode": "pantheon_interior", "solarHour": 12.5, "season": "summer", "weather": "clear"
    },
    {
        "code": "VP05", "key": "vp05_subura_alley",
        "titleZh": "VP05: 蘇布拉區底層巷道仰視兩側 5–6 層公寓、遮陽棚與塗鴉",
        "titleLa": "Clivus Suburanus — Insulae, Tabernae, Velaria et Dipinti",
        "pos": [275.0, 18.8, -182.0], "target": [380.0, 25.0, -218.0],
        "mode": "subura_lod0", "solarHour": 17.5, "season": "autumn", "weather": "rain"
    },
    {
        "code": "VP06", "key": "vp06_tiber_island",
        "titleZh": "VP06: 台伯島石造船尾、醫神神廟、法布里키烏斯橋與塞斯提烏斯橋",
        "titleLa": "Insula Tiberina, Pons Fabricius et Pons Cestius",
        "pos": [-385.0, 38.0, 405.0], "target": [-480.0, 12.0, 205.0],
        "mode": "exterior", "solarHour": 16.0, "season": "spring", "weather": "clear"
    },
    {
        "code": "VP07", "key": "vp07_colosseum_arena",
        "titleZh": "VP07: 競技場內部最高層觀眾席俯瞰橢圓沙地與遮陽帆桅杆",
        "titleLa": "Amphitheatrum Flavium — Maenianum Summum et Harena",
        "pos": [435.0, 66.0, 62.0], "target": [525.0, 24.0, 62.0],
        "mode": "colosseum_interior", "solarHour": 14.0, "season": "summer", "weather": "clear"
    },
    {
        "code": "VP08", "key": "vp08_colosseum_exterior",
        "titleZh": "VP08: 競技場外牆、流汗圓錐噴泉與太陽神巨像（無君士坦丁凱旋門）",
        "titleLa": "Amphitheatrum Flavium, Meta Sudans et Colossus Solis",
        "pos": [355.0, 42.0, 155.0], "target": [495.0, 34.0, 55.0],
        "mode": "exterior", "solarHour": 16.8, "season": "summer", "weather": "clear"
    },
    {
        "code": "VP09", "key": "vp09_venus_roma_site",
        "titleZh": "VP09: 維利亞丘「維納斯與羅馬神廟」公元 128 年鷹架與雙輪起重機工地",
        "titleLa": "Templum Veneris et Romae — In Constructione (AD 128)",
        "pos": [205.0, 48.0, -65.0], "target": [325.0, 34.0, 25.0],
        "mode": "exterior", "solarHour": 10.5, "season": "spring", "weather": "summer_haze"
    },
    {
        "code": "VP10", "key": "vp10_trajan_forum",
        "titleZh": "VP10: 圖拉真廣場中央看向烏爾比亞會堂與圖拉真鍍金騎馬銅像",
        "titleLa": "Forum Traiani, Equus Traiani et Basilica Ulpia",
        "pos": [-25.0, 24.0, -175.0], "target": [-75.0, 28.0, -285.0],
        "mode": "exterior", "solarHour": 15.2, "season": "summer", "weather": "clear"
    },
    {
        "code": "VP11", "key": "vp11_trajan_column",
        "titleZh": "VP11: 圖拉真柱彩繪螺旋浮雕帶與哈德良新建之神化圖拉真神廟",
        "titleLa": "Columna Traiani (38.4m) et Templum Divi Traiani",
        "pos": [-62.0, 26.0, -295.0], "target": [-105.0, 32.0, -355.0],
        "mode": "exterior", "solarHour": 14.5, "season": "spring", "weather": "clear"
    },
    {
        "code": "VP12", "key": "vp12_trajan_markets",
        "titleZh": "VP12: 圖拉真市場半圓立面與內部雙層交叉拱頂大廳（Aula Traiana）",
        "titleLa": "Mercatus Traiani — Hemicyclium et Aula Magna",
        "pos": [25.0, 24.5, -262.0], "target": [25.0, 26.0, -228.0],
        "mode": "mercatus_interior", "solarHour": 13.5, "season": "summer", "weather": "clear"
    },
    {
        "code": "VP13", "key": "vp13_jupiter_capitolinus",
        "titleZh": "VP13: 卡比托利歐山廣場仰望鍍金銅瓦朱庇特神廟與山頂四馬戰車",
        "titleLa": "Aedes Jovis Optimi Maximi Capitolini (62×53.5×32m)",
        "pos": [-198.0, 56.0, 32.0], "target": [-142.0, 62.0, -42.0],
        "mode": "exterior", "solarHour": 17.2, "season": "summer", "weather": "clear"
    },
    {
        "code": "VP14", "key": "vp14_trajan_baths",
        "titleZh": "VP14: 奧比烏斯山圖拉真浴場冷水大廳十字拱頂與玫瑰花崗岩巨柱",
        "titleLa": "Thermae Traiani — Frigidarium et Natatio",
        "pos": [685.0, 52.0, -88.0], "target": [685.0, 56.0, -42.0],
        "mode": "thermae_traiani_interior", "solarHour": 14.0, "season": "summer", "weather": "clear"
    },
    {
        "code": "VP15", "key": "vp15_campus_martius_bird",
        "titleZh": "VP15: 戰神廣場俯瞰（龐貝劇場、大柱廊、多米提安競技場、萬神殿）",
        "titleLa": "Campus Martius — Theatra, Porticus, Stadium et Pantheon",
        "pos": [-520.0, 64.0, -45.0], "target": [-615.0, 22.0, -235.0],
        "mode": "exterior", "solarHour": 15.8, "season": "spring", "weather": "clear"
    },
    {
        "code": "VP16", "key": "vp16_emporium_testaccio",
        "titleZh": "VP16: 埃米利亞河港碼頭、50 跨拱頂大倉庫、加爾巴糧倉與 128 年陶片山",
        "titleLa": "Emporium, Porticus Aemilia, Horrea Galbae et Mons Testaceus",
        "pos": [-695.0, 62.0, 860.0], "target": [-515.0, 18.0, 1180.0],
        "mode": "exterior", "solarHour": 16.2, "season": "autumn", "weather": "summer_haze"
    },
    {
        "code": "VP17", "key": "vp17_aqua_claudia_porta",
        "titleZh": "VP17: 克勞狄輸水道（27.4m）與新阿尼奧輸水道雙層高架巨拱及大門",
        "titleLa": "Aqua Claudia, Anio Novus (30.2m) et Porta Maior",
        "pos": [1240.0, 76.0, 65.0], "target": [1420.0, 66.0, -80.0],
        "mode": "exterior", "solarHour": 16.5, "season": "summer", "weather": "clear"
    },
    {
        "code": "VP18", "key": "vp18_insula_interior",
        "titleZh": "VP18: 卡比托利歐北麓 5 層公寓內部：一樓店鋪與逐層可爬磚木樓梯",
        "titleLa": "Insula Capitolina (5 Tabulata) — Tabernae et Scalae",
        "pos": [-138.0, 22.0, -168.0], "target": [-138.0, 23.5, -142.0],
        "mode": "insula_interior", "solarHour": 15.0, "season": "spring", "weather": "clear"
    },
    {
        "code": "VP19", "key": "vp19_domus_peristyle",
        "titleZh": "VP19: 帕拉提諾貴族豪宅內部：前庭天窗蓄水池（Impluvium）與列柱花園",
        "titleLa": "Domus Palatina — Atrium, Impluvium et Peristylium",
        "pos": [55.0, 48.2, 182.0], "target": [55.0, 48.8, 208.0],
        "mode": "domus_interior", "solarHour": 15.5, "season": "spring", "weather": "clear"
    },
    {
        "code": "VP20", "key": "vp20_seven_hills_ortho",
        "titleZh": "VP20: 全城高空鳥瞰（切換考證模式 A綠/B藍/C橘 與 14 行政區邊界）",
        "titleLa": "Forma Urbis Romae AD 128 — Modus Fidei Archaeologicae (Tier A/B/C)",
        "pos": [1180.0, 680.0, 980.0], "target": [80.0, 25.0, -120.0],
        "mode": "credibility_ortho", "solarHour": 14.0, "season": "summer", "weather": "clear"
    }
]

world_data["lod0Props"] = lod0_props
world_data["latinDipinti"] = latin_dipinti
world_data["audioZones128AD"] = audio_zones_128ad
world_data["viewpoints20"] = viewpoints_20
world_data["p5Summary"] = {
    "stage": "P5",
    "lod0StreetPropsCount": len(lod0_props),
    "latinDipintiCount": len(latin_dipinti),
    "audioZonesCount": len(audio_zones_128ad),
    "canonicalViewpointsCount": len(viewpoints_20),
    "churchBellsStrictlyExcluded": True,
    "seasonsSupported": ["spring", "summer", "autumn", "winter"],
    "weatherModesSupported": ["clear", "summer_haze", "overcast", "rain"],
    "polychromyComparisonToggle": True
}

p5_json_path = os.path.join(p5_data_dir, "p5_world_data.json")
with open(p5_json_path, "w", encoding="utf-8") as f:
    json.dump(world_data, f, ensure_ascii=False, indent=2)

print("Generated p5_world_data.json:", json.dumps(world_data["p5Summary"], indent=2))
