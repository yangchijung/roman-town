# -*- coding: utf-8 -*-
import json, math, os, random

p1_data_path = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p1/data/p1_world_data.json"
p2_data_dir = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p2/data"
os.makedirs(p2_data_dir, exist_ok=True)

with open(p1_data_path, "r", encoding="utf-8") as f:
    world_data = json.load(f)

P = "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/"
FUR = "https://formaurbis.stanford.edu/docs/FURmap.html"

# Ancient Terrain height function for placing roads and buildings accurately on slopes
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

# 1. Major Roman Roads, Streets (Vici), Clivi & Consular Roads (18 routes)
roads_128ad = [
    {
        "id": "road.rome.sacra_via",
        "nameLa": "Sacra Via (Via Sacra)",
        "nameZh": "神聖大道（羅馬廣場至維利亞丘頂）",
        "year": -500,
        "type": "via_sacra",
        "carriageWidthM": 6.5,
        "sidewalkWidthM": 2.2,
        "referenceWidthM": 6.5,
        "modelWidthM": 6.5,
        "paving": "basalt_silex_polygonal",
        "credibility": "A",
        "sourceUrl": P + "Forum_Romanum.html",
        "waypoints": [[-95, -25], [0, 0], [120, 15], [265, 35], [420, 45]]
    },
    {
        "id": "road.rome.via_lata_flaminia",
        "nameLa": "Via Lata / Via Flaminia",
        "nameZh": "寬街／弗拉米尼亞大道（戰神廣場東界北向幹道）",
        "year": -220,
        "type": "via_consularis",
        "carriageWidthM": 8.5,
        "sidewalkWidthM": 3.0,
        "referenceWidthM": 8.5,
        "modelWidthM": 8.5,
        "paving": "basalt_silex_with_porticus",
        "credibility": "A",
        "sourceUrl": P + "home.html",
        "waypoints": [[-65, -215], [-140, -650], [-240, -1250], [-380, -1850], [-580, -2620]]
    },
    {
        "id": "road.rome.via_appia",
        "nameLa": "Via Appia (Intra et Extra Portam Capenam)",
        "nameZh": "阿庇亞大道（卡佩納門起點南向執政官大道）",
        "year": -312,
        "type": "via_consularis",
        "carriageWidthM": 4.1,
        "sidewalkWidthM": 3.1,
        "referenceWidthM": 4.1,
        "modelWidthM": 4.1,
        "paving": "basalt_silex_crepidines",
        "credibility": "A",
        "sourceUrl": P + "Via_Appia.html",
        "waypoints": [[240, 480], [295, 620], [420, 1050], [580, 1580], [740, 2050]]
    },
    {
        "id": "road.rome.via_latina",
        "nameLa": "Via Latina",
        "nameZh": "拉丁大道（自阿庇亞大道分岔東南向）",
        "year": -334,
        "type": "via_consularis",
        "carriageWidthM": 4.1,
        "sidewalkWidthM": 2.0,
        "referenceWidthM": 4.1,
        "modelWidthM": 4.1,
        "paving": "basalt_silex",
        "credibility": "A",
        "sourceUrl": P + "home.html",
        "waypoints": [[420, 1050], [680, 1380], [980, 1780]]
    },
    {
        "id": "road.rome.via_ostiensis",
        "nameLa": "Via Ostiensis",
        "nameZh": "奧斯提亞大道（通往河港、陶片山與塞斯提烏斯金字塔）",
        "year": -300,
        "type": "via_consularis",
        "carriageWidthM": 6.0,
        "sidewalkWidthM": 2.0,
        "referenceWidthM": 6.0,
        "modelWidthM": 6.0,
        "paving": "basalt_silex_heavy_wheel_ruts",
        "credibility": "A",
        "sourceUrl": P + "Emporium.html",
        "waypoints": [[-385, 520], [-450, 920], [-420, 1380], [-360, 1850]]
    },
    {
        "id": "road.rome.via_aurelia",
        "nameLa": "Via Aurelia",
        "nameZh": "奧ウレ利亞大道（自埃米利烏斯橋跨越賈尼科洛山西向）",
        "year": -241,
        "type": "via_consularis",
        "carriageWidthM": 4.2,
        "sidewalkWidthM": 1.8,
        "referenceWidthM": 4.2,
        "modelWidthM": 4.2,
        "paving": "basalt_silex",
        "credibility": "A",
        "sourceUrl": P + "Pons_Aemilius.html",
        "waypoints": [[-445, 365], [-780, 340], [-1280, 280], [-1820, 220]]
    },
    {
        "id": "road.rome.via_tiburtina_labicana",
        "nameLa": "Via Labicana et Praenestina",
        "nameZh": "拉比卡納與普萊內斯蒂納大道（自埃スクイリーノ門東向）",
        "year": -300,
        "type": "via_consularis",
        "carriageWidthM": 5.5,
        "sidewalkWidthM": 2.0,
        "referenceWidthM": 5.5,
        "modelWidthM": 5.5,
        "paving": "basalt_silex",
        "credibility": "A",
        "sourceUrl": P + "Aqua_Claudia.html",
        "waypoints": [[920, -210], [1350, -140], [1820, -60]]
    },
    {
        "id": "road.rome.via_nomentana_salaria",
        "nameLa": "Alta Semita / Via Nomentana",
        "nameZh": "高徑大道／諾門塔納大道（縱貫奎里納雷山脊至禁衛軍營）",
        "year": -300,
        "type": "via_urbana_major",
        "carriageWidthM": 6.5,
        "sidewalkWidthM": 2.2,
        "referenceWidthM": 6.5,
        "modelWidthM": 6.5,
        "paving": "basalt_silex",
        "credibility": "A",
        "sourceUrl": P + "Castra_Praetoria.html",
        "waypoints": [[180, -520], [480, -820], [860, -1120], [1280, -1380]]
    },
    {
        "id": "road.rome.argiletum_subura",
        "nameLa": "Argiletum & Clivus Suburanus",
        "nameZh": "阿吉萊圖姆街與蘇布拉坡道（連接議事廣場與擁擠蘇布拉谷地）",
        "year": -200,
        "type": "clivus_subura",
        "carriageWidthM": 4.8,
        "sidewalkWidthM": 1.4,
        "referenceWidthM": 4.8,
        "modelWidthM": 4.8,
        "paving": "basalt_silex_wet_drain",
        "credibility": "A",
        "sourceUrl": P + "Subura.html",
        "waypoints": [[90, -60], [240, -160], [420, -240], [680, -230], [920, -210]]
    },
    {
        "id": "road.rome.vicus_patricius",
        "nameLa": "Vicus Patricius",
        "nameZh": "貴族街（自蘇布拉向東北延伸至維米納萊門）",
        "year": -150,
        "type": "vicus",
        "carriageWidthM": 4.2,
        "sidewalkWidthM": 1.2,
        "referenceWidthM": 4.2,
        "modelWidthM": 4.2,
        "paving": "basalt_silex",
        "credibility": "A",
        "sourceUrl": P + "Subura.html",
        "waypoints": [[360, -210], [580, -420], [820, -580], [960, -680]]
    },
    {
        "id": "road.rome.vicus_tuscus",
        "nameLa": "Vicus Tuscus",
        "nameZh": "伊特魯里亞街（羅馬廣場經維拉布魯姆至屠牛廣場）",
        "year": -400,
        "type": "vicus",
        "carriageWidthM": 4.5,
        "sidewalkWidthM": 1.5,
        "referenceWidthM": 4.5,
        "modelWidthM": 4.5,
        "paving": "basalt_silex",
        "credibility": "A",
        "sourceUrl": P + "Forum_Romanum.html",
        "waypoints": [[-20, 35], [-120, 160], [-240, 290], [-340, 360]]
    },
    {
        "id": "road.rome.vicus_jugarius",
        "nameLa": "Vicus Jugarius",
        "nameZh": "軛街（沿卡比托利歐山南麓至河岸卡爾門塔利斯門）",
        "year": -400,
        "type": "vicus",
        "carriageWidthM": 4.5,
        "sidewalkWidthM": 1.5,
        "referenceWidthM": 4.5,
        "modelWidthM": 4.5,
        "paving": "basalt_silex",
        "credibility": "A",
        "sourceUrl": P + "Forum_Romanum.html",
        "waypoints": [[-65, 20], [-185, 75], [-285, 110], [-380, 210]]
    },
    {
        "id": "road.rome.clivus_capitolinus",
        "nameLa": "Clivus Capitolinus",
        "nameZh": "卡比托利歐凱旋坡道（農神神廟登頂至朱庇特神廟）",
        "year": -174,
        "type": "clivus",
        "carriageWidthM": 4.8,
        "sidewalkWidthM": 1.2,
        "referenceWidthM": 4.8,
        "modelWidthM": 4.8,
        "paving": "basalt_silex",
        "credibility": "A",
        "sourceUrl": P + "Aedes_Saturni.html",
        "waypoints": [[-70, 5], [-135, -15], [-165, -45], [-145, -55]]
    },
    {
        "id": "road.rome.via_tecta_recta",
        "nameLa": "Via Recta / Via Tecta (Campus Martius)",
        "nameZh": "戰神廣場直街（橫貫戰神廣場柱廊群至尼祿橋）",
        "year": -20,
        "type": "via_porticus",
        "carriageWidthM": 7.5,
        "sidewalkWidthM": 3.5,
        "referenceWidthM": 7.5,
        "modelWidthM": 7.5,
        "paving": "travertine_and_basalt_avenue",
        "credibility": "B",
        "sourceUrl": P + "home.html",
        "waypoints": [[-160, -650], [-520, -660], [-920, -675], [-1315, -690]]
    }
]

# 2. Procedural Generation of Urban Texture (Insulae, Domus, Horrea, Campus Martius Porticoes, Subura Alleys)
random.seed(128) # Deterministic seed locked to AD 128

buildings_p2 = []
street_props_p2 = [] # Fountains (Lacus), Compita shrines, Stepping stones, Market stalls

def add_building(b_id, category, regio, x, z, length, width, height, stories, rot_y, cred, mat_style, has_tabernae=True, has_balcony=False):
    y_ground = max(6.8, get_ancient_terrain_height(x, z))
    buildings_p2.append({
        "id": b_id,
        "category": category, # 'insula', 'domus', 'horrea', 'porticus'
        "regio": regio,
        "year": random.choice([-45, -15, 14, 35, 68, 82, 98, 108, 118, 125]),
        "pos": [round(x, 1), round(y_ground, 2), round(z, 1)],
        "dims": [round(length, 1), round(height, 1), round(width, 1)],
        "stories": stories,
        "rotY": round(rot_y, 3),
        "credibility": cred,
        "materialStyle": mat_style, # 'opus_latericium_red', 'stucco_ochre', 'stucco_weathered_subura', 'domus_peristyle_white', 'travertine_porticus', 'opus_reticulatum_horrea'
        "hasTabernae": has_tabernae,
        "hasBalcony": has_balcony
    })

# A. Generate Subura (Regio IV & North Regio III) — Ultra-high density 5-6 story Insulae, narrow alleys (3.2m), overhanging balconies, stepping stones & street fountains
subura_idx = 1
for gx in range(130, 680, 32):
    for gz in range(-420, -70, 28):
        # Leave slight narrow winding channels for Clivus Suburanus and Vicus Patricius
        dist_clivus = abs(gz - (-160 - (gx - 240) * 0.25))
        if dist_clivus < 5.5:
            # Place a Subura street fountain (Lacus) or stepping stones along the main alley
            if subura_idx % 5 == 0:
                yg = get_ancient_terrain_height(gx, gz)
                street_props_p2.append({
                    "id": f"prop.reg04.lacus.{subura_idx:04d}",
                    "type": "lacus_fountain",
                    "pos": [round(gx, 1), round(yg, 2), round(gz, 1)],
                    "credibility": "B"
                })
            continue
        jx = gx + random.uniform(-3.5, 3.5)
        jz = gz + random.uniform(-3.0, 3.0)
        stories = random.choice([5, 5, 6, 6]) # 5-6 stories (17.5m - 20.6m per Lex Iulia / Nero limit + timber cenacula)
        height = stories * 3.35 + random.uniform(-0.3, 0.4)
        length = random.uniform(18.0, 25.0)
        width = random.uniform(15.0, 21.0)
        rot = random.uniform(-0.18, 0.18)
        # FUR fragment coverage in Subura -> Tier B per User Decision #4, outer procedural -> Tier C
        cred = "B" if (200 <= gx <= 520 and -320 <= gz <= -120) else "C"
        mat = random.choice(["stucco_weathered_subura", "opus_latericium_red", "stucco_ochre"])
        add_building(
            f"bldg.reg04.insula.{subura_idx:04d}", "insula", "Regio IV (Subura)",
            jx, jz, length, width, height, stories, rot, cred, mat,
            has_tabernae=True, has_balcony=True
        )
        subura_idx += 1

# B. Generate Campus Martius (Regio IX & Regio VII) — Wide orthogonal avenues, monumental porticoes (Porticus), gardens, and spaced 4-story Hadrianic brick insulae along Via Lata
cm_idx = 1
# Monumental Porticoes & Colonnade Enclosures in Central Campus Martius (Tier A/B)
campus_porticoes = [
    ("bldg.reg09.porticus.saepta", "Regio IX", -310, -540, 120.0, 310.0, 14.5, 1, 0.0, "A", "travertine_porticus"),
    ("bldg.reg09.porticus.pompei", "Regio IX", -520, -240, 180.0, 135.0, 13.0, 1, 0.0, "A", "travertine_porticus"),
    ("bldg.reg09.porticus.divorum", "Regio IX", -210, -420, 77.0, 194.0, 12.5, 1, 0.0, "A", "travertine_porticus"),
    ("bldg.reg09.porticus.minucia", "Regio IX", -380, -260, 165.0, 130.0, 13.5, 1, 0.0, "A", "travertine_porticus"),
    ("bldg.reg09.porticus.octaviae", "Regio IX", -310, 45, 119.0, 132.0, 14.0, 1, 0.15, "A", "travertine_porticus")
]
for pid, preg, px, pz, pl, pw, ph, pst, prot, pcred, pmat in campus_porticoes:
    add_building(pid, "porticus", preg, px, pz, pl, pw, ph, pst, prot, pcred, pmat, has_tabernae=False, has_balcony=False)

# Planned Hadrianic brick Insulae along Via Lata (Regio VII & East Regio IX)
for gz in range(-1450, -320, 78):
    for gx in [-220, -90, 20, 110]:
        stories = 4
        height = 14.8
        cred = "B" if gz > -950 else "C"
        add_building(
            f"bldg.reg07.insula.{cm_idx:04d}", "insula", "Regio VII (Via Lata)",
            gx + random.uniform(-4, 4), gz + random.uniform(-4, 4),
            34.0, 26.0, height, stories, 0.0, cred, "opus_latericium_red",
            has_tabernae=True, has_balcony=False
        )
        cm_idx += 1

# C. Generate Aristocratic Domus (Atrium + Peristyle Garden Villas) on Palatine Slopes (Regio X), Quirinal (Regio VI), Caelian (Regio II), and Aventine (Regio XII/XIII)
domus_idx = 1
domus_zones = [
    ("Regio VI (Alta Semita)", 260, 880, -1080, -560, 68, "C"),
    ("Regio II (Caelimontium)", 440, 980, 320, 720, 72, "C"),
    ("Regio XII (Piscina Publica)", 40, 340, 760, 1280, 70, "C"),
    ("Regio XIII (Aventinus)", -360, -40, 680, 1120, 68, "B"),
    ("Regio X (Palatinus Slopes)", 40, 310, 120, 360, 64, "A")
]
for reg_name, x0, x1, z0, z1, step, base_cred in domus_zones:
    for gx in range(x0, x1, step):
        for gz in range(z0, z1, step):
            jx = gx + random.uniform(-8, 8)
            jz = gz + random.uniform(-8, 8)
            stories = random.choice([1, 2])
            height = 6.5 if stories == 1 else 9.8
            add_building(
                f"bldg.domus.{domus_idx:04d}", "domus", reg_name,
                jx, jz, random.uniform(28, 42), random.uniform(24, 36),
                height, stories, random.uniform(-0.1, 0.1), base_cred,
                "domus_peristyle_white", has_tabernae=False, has_balcony=False
            )
            domus_idx += 1

# D. Generate River Port Warehouses (Horrea) in Emporium / Regio XIII & Transtiberim (Regio XIV)
horrea_idx = 1
for gz in range(580, 1320, 76):
    for gx in range(-640, -380, 68):
        if get_ancient_terrain_height(gx, gz) < 8.5:
            continue
        cred = "B" if gz < 1050 else "C"
        add_building(
            f"bldg.reg13.horrea.{horrea_idx:04d}", "horrea", "Regio XIII (Emporium)",
            gx, gz, 52.0, 38.0, 11.5, 2, 0.12, cred,
            "opus_reticulatum_horrea", has_tabernae=True, has_balcony=False
        )
        horrea_idx += 1

# Transtiberim (Regio XIV) mixed riverfront Insulae
trans_idx = 1
for gz in range(-180, 580, 48):
    for gx in range(-920, -580, 46):
        if get_ancient_terrain_height(gx, gz) < 9.2:
            continue
        stories = random.choice([3, 4, 5])
        add_building(
            f"bldg.reg14.insula.{trans_idx:04d}", "insula", "Regio XIV (Transtiberim)",
            gx + random.uniform(-5, 5), gz + random.uniform(-5, 5),
            22.0, 18.0, stories * 3.4, stories, random.uniform(-0.2, 0.2), "B",
            "stucco_ochre", has_tabernae=True, has_balcony=True
        )
        trans_idx += 1

world_data["roads"] = roads_128ad
world_data["urbanBuildings"] = buildings_p2
world_data["streetProps"] = street_props_p2
world_data["p2Summary"] = {
    "totalRoads": len(roads_128ad),
    "totalProceduralBuildings": len(buildings_p2),
    "suburaInsulaeCount": subura_idx - 1,
    "campusMartiusStructures": cm_idx - 1 + len(campus_porticoes),
    "aristocraticDomusCount": domus_idx - 1,
    "emporiumHorreaCount": horrea_idx - 1,
    "transtiberimInsulaeCount": trans_idx - 1,
    "streetPropsCount": len(street_props_p2)
}

p2_json_path = os.path.join(p2_data_dir, "p2_world_data.json")
with open(p2_json_path, "w", encoding="utf-8") as f:
    json.dump(world_data, f, ensure_ascii=False, indent=2)

print("Generated p2_world_data.json:", json.dumps(world_data["p2Summary"], indent=2))
