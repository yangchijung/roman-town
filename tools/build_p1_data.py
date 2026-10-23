# -*- coding: utf-8 -*-
import json, math, os

base_dir = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p1/data"
os.makedirs(base_dir, exist_ok=True)

P = "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/"
FUR = "https://formaurbis.stanford.edu/docs/FURmap.html"

# 1. Seven Hills + Velia + Janiculum + Vatican + Pincian + Testaccio DEM Gaussian/Plateau definitions
# Coordinates in meters relative to Milliarium Aureum (0, 0, 0), +X = East, -Z = North, +Z = South
hills_dem = [
    {"id": "mons.palatinus", "nameLa": "Mons Palatinus", "nameZh": "帕拉提諾山", "x": 140.0, "z": 220.0, "rx": 240.0, "rz": 220.0, "peakElevationM": 51.2, "plateauFactor": 0.65, "credibility": "A", "sourceUrl": P + "Palatinus.html"},
    {"id": "mons.capitolinus.capitolium", "nameLa": "Mons Capitolinus (Capitolium)", "nameZh": "卡比托利歐山（南峰）", "x": -145.0, "z": -40.0, "rx": 130.0, "rz": 150.0, "peakElevationM": 46.0, "plateauFactor": 0.60, "credibility": "A", "sourceUrl": P + "Aedes_Jovis_Capitolini.html"},
    {"id": "mons.capitolinus.arx", "nameLa": "Mons Capitolinus (Arx)", "nameZh": "卡比托利歐山（北峰衛城）", "x": -95.0, "z": -195.0, "rx": 115.0, "rz": 120.0, "peakElevationM": 49.2, "plateauFactor": 0.58, "credibility": "A", "sourceUrl": P + "M.html"},
    {"id": "mons.velia", "nameLa": "Collis Velia", "nameZh": "維利亞丘（1930年代剷平前原始鞍部）", "x": 280.0, "z": 35.0, "rx": 165.0, "rz": 125.0, "peakElevationM": 42.0, "plateauFactor": 0.50, "credibility": "A", "sourceUrl": P + "Templum_Veneris_et_Romae.html"},
    {"id": "mons.aventinus.major", "nameLa": "Mons Aventinus", "nameZh": "阿文提諾山", "x": -180.0, "z": 860.0, "rx": 360.0, "rz": 340.0, "peakElevationM": 46.6, "plateauFactor": 0.68, "credibility": "A", "sourceUrl": P + "Thermae_Suranae.html"},
    {"id": "mons.aventinus.minor", "nameLa": "Aventinus Minor", "nameZh": "小阿文提諾山", "x": 210.0, "z": 1120.0, "rx": 260.0, "rz": 240.0, "peakElevationM": 41.5, "plateauFactor": 0.55, "credibility": "A", "sourceUrl": P + "home.html"},
    {"id": "mons.caelius", "nameLa": "Mons Caelius", "nameZh": "西利歐山", "x": 760.0, "z": 540.0, "rx": 480.0, "rz": 260.0, "peakElevationM": 50.0, "plateauFactor": 0.62, "credibility": "A", "sourceUrl": P + "home.html"},
    {"id": "mons.oppius", "nameLa": "Mons Oppius (Esquiliae)", "nameZh": "奧比烏斯山（埃スクイリーノ南峰）", "x": 740.0, "z": -40.0, "rx": 420.0, "rz": 280.0, "peakElevationM": 53.0, "plateauFactor": 0.64, "credibility": "A", "sourceUrl": P + "Thermae_Trajani.html"},
    {"id": "mons.cispius", "nameLa": "Mons Cispius (Esquiliae)", "nameZh": "키斯皮烏斯山（埃スクイリーノ北峰）", "x": 780.0, "z": -420.0, "rx": 380.0, "rz": 220.0, "peakElevationM": 54.0, "plateauFactor": 0.58, "credibility": "A", "sourceUrl": P + "home.html"},
    {"id": "mons.esquilinus.plateau", "nameLa": "Mons Esquilinus", "nameZh": "埃スクイリーノ高地", "x": 1280.0, "z": -220.0, "rx": 650.0, "rz": 520.0, "peakElevationM": 64.0, "plateauFactor": 0.72, "credibility": "A", "sourceUrl": P + "Aqua_Claudia.html"},
    {"id": "collis.viminalis", "nameLa": "Collis Viminalis", "nameZh": "維米納萊山", "x": 620.0, "z": -680.0, "rx": 420.0, "rz": 190.0, "peakElevationM": 57.0, "plateauFactor": 0.60, "credibility": "A", "sourceUrl": P + "home.html"},
    {"id": "collis.quirinalis", "nameLa": "Collis Quirinalis", "nameZh": "奎里納雷山", "x": 380.0, "z": -920.0, "rx": 580.0, "rz": 310.0, "peakElevationM": 61.0, "plateauFactor": 0.65, "credibility": "A", "sourceUrl": P + "home.html"},
    {"id": "mons.pincius", "nameLa": "Mons Pincius (Collis Hortulorum)", "nameZh": "平키歐山（花園山）", "x": -180.0, "z": -1680.0, "rx": 480.0, "rz": 420.0, "peakElevationM": 54.0, "plateauFactor": 0.65, "credibility": "A", "sourceUrl": P + "Aqua_Virgo.html"},
    {"id": "mons.ianiculum", "nameLa": "Mons Ianiculum", "nameZh": "賈尼科洛山（台伯河右岸）", "x": -1280.0, "z": 280.0, "rx": 380.0, "rz": 980.0, "peakElevationM": 82.0, "plateauFactor": 0.52, "credibility": "A", "sourceUrl": P + "Aqua_Alsietina.html"},
    {"id": "mons.vaticanus", "nameLa": "Mons Vaticanus", "nameZh": "梵蒂岡丘", "x": -1850.0, "z": -980.0, "rx": 450.0, "rz": 450.0, "peakElevationM": 60.0, "plateauFactor": 0.50, "credibility": "A", "sourceUrl": P + "home.html"},
    {"id": "mons.testaceus", "nameLa": "Mons Testaceus (AD 128 State)", "nameZh": "陶片山（公元128年高度 22m）", "x": -580.0, "z": 1380.0, "rx": 110.0, "rz": 95.0, "peakElevationM": 30.5, "plateauFactor": 0.45, "credibility": "A", "sourceUrl": P + "Testaceus_Mons.html"}
]

# 2. Tiber River Ancient Channel Centerline & Widths (from North Pons Milvius z=-2800 to South Emporium z=+2200)
tiber_channel = [
    {"z": -2800, "x": -620, "width": 98, "bankElev": 11.5},
    {"z": -2200, "x": -680, "width": 96, "bankElev": 11.2},
    {"z": -1600, "x": -750, "width": 92, "bankElev": 11.0},
    {"z": -1150, "x": -890, "width": 90, "bankElev": 10.8},
    {"z": -850,  "x": -1280, "width": 94, "bankElev": 10.6},
    {"z": -520,  "x": -1360, "width": 92, "bankElev": 10.5},
    {"z": -220,  "x": -980, "width": 88, "bankElev": 10.5},
    {"z": 40,    "x": -620, "width": 92, "bankElev": 10.4},
    {"z": 210,   "x": -480, "width": 138, "bankElev": 10.2, "note": "Insula Tiberina (台伯島分流段)"},
    {"z": 390,   "x": -440, "width": 90, "bankElev": 10.2},
    {"z": 680,   "x": -520, "width": 94, "bankElev": 10.0},
    {"z": 1150,  "x": -690, "width": 98, "bankElev": 9.8, "note": "Emporium (埃米利亞河港段)"},
    {"z": 1680,  "x": -820, "width": 102, "bankElev": 9.6},
    {"z": 2400,  "x": -920, "width": 106, "bankElev": 9.5}
]

# 3. Exactly 7 Bridges existing in AD 128 (Strictly excluding Pons Aelius per User Decision #3)
bridges_128ad = [
    {
        "id": "bridge.tiber.0084",
        "nameLa": "Pons Sublicius",
        "nameZh": "蘇布利키烏斯木橋（神聖木橋）",
        "year": -620,
        "region": "Regio XI – XIV",
        "pos": [-465.0, 11.2, 470.0],
        "rotationY": 0.18,
        "referenceDims": {"length": 95.0, "width": 6.5, "height": 9.5},
        "modelDims": {"length": 95.0, "width": 6.5, "height": 9.5},
        "materialType": "timber_sublicae_no_iron",
        "arches": 0,
        "credibility": "B",
        "sourceTitle": "Platner & Ashby (1929), Pons Sublicius",
        "sourceUrl": P + "Pons_Sublicius.html"
    },
    {
        "id": "bridge.tiber.0085",
        "nameLa": "Pons Aemilius",
        "nameZh": "埃米利烏斯石橋",
        "year": -142,
        "region": "Regio XI – XIV",
        "pos": [-445.0, 12.8, 365.0],
        "rotationY": 0.12,
        "referenceDims": {"length": 135.0, "width": 9.0, "height": 12.5},
        "modelDims": {"length": 135.0, "width": 9.0, "height": 12.5},
        "materialType": "travertine_tufa_stone_arches",
        "arches": 6,
        "credibility": "A",
        "sourceTitle": "Platner & Ashby (1929), Pons Aemilius",
        "sourceUrl": P + "Pons_Aemilius.html"
    },
    {
        "id": "bridge.tiber.0086",
        "nameLa": "Pons Fabricius",
        "nameZh": "法布里키烏斯橋（台伯島東橋）",
        "year": -62,
        "region": "Regio IX – XIV (Insula)",
        "pos": [-432.0, 12.2, 185.0],
        "rotationY": 0.42,
        "referenceDims": {"length": 62.0, "width": 5.5, "height": 11.0},
        "modelDims": {"length": 62.0, "width": 5.5, "height": 11.0},
        "materialType": "travertine_faced_tufa_2arches",
        "arches": 2,
        "credibility": "A",
        "sourceTitle": "Platner & Ashby (1929), Pons Fabricius",
        "sourceUrl": P + "Pons_Fabricius.html"
    },
    {
        "id": "bridge.tiber.0087",
        "nameLa": "Pons Cestius",
        "nameZh": "塞斯提烏斯橋（台伯島西橋）",
        "year": -46,
        "region": "Regio XIV (Insula – Transtiberim)",
        "pos": [-528.0, 12.0, 225.0],
        "rotationY": -0.35,
        "referenceDims": {"length": 48.0, "width": 8.2, "height": 10.8},
        "modelDims": {"length": 48.0, "width": 8.2, "height": 10.8},
        "materialType": "republican_travertine_tufa",
        "arches": 3,
        "credibility": "A",
        "sourceTitle": "Platner & Ashby (1929), Pons Cestius",
        "sourceUrl": P + "Pons_Cestius.html"
    },
    {
        "id": "bridge.tiber.0088",
        "nameLa": "Pons Agrippae",
        "nameZh": "阿格里帕橋",
        "year": -12,
        "region": "Regio IX – XIV",
        "pos": [-885.0, 12.4, -145.0],
        "rotationY": 0.55,
        "referenceDims": {"length": 105.0, "width": 7.5, "height": 11.5},
        "modelDims": {"length": 105.0, "width": 7.5, "height": 11.5},
        "materialType": "travertine_piers_4",
        "arches": 5,
        "credibility": "A",
        "sourceTitle": "Platner & Ashby (1929), Pons Agrippae",
        "sourceUrl": P + "Pons_Agrippae.html"
    },
    {
        "id": "bridge.tiber.0089",
        "nameLa": "Pons Neronianus",
        "nameZh": "尼祿橋（勝利大道橋）",
        "year": 54,
        "region": "Regio IX – XIV (Vaticanus)",
        "pos": [-1315.0, 12.5, -690.0],
        "rotationY": 0.25,
        "referenceDims": {"length": 108.0, "width": 8.0, "height": 11.8},
        "modelDims": {"length": 108.0, "width": 8.0, "height": 11.8},
        "materialType": "travertine_piers_4",
        "arches": 5,
        "credibility": "A",
        "sourceTitle": "Platner & Ashby (1929), Pons Neronianus",
        "sourceUrl": P + "Pons_Neronianus.html"
    },
    {
        "id": "bridge.tiber.0090",
        "nameLa": "Pons Milvius",
        "nameZh": "米爾維烏斯橋（北郊弗拉米尼亞大道）",
        "year": -109,
        "region": "Via Flaminia (North)",
        "pos": [-630.0, 13.5, -2650.0],
        "rotationY": 0.08,
        "referenceDims": {"length": 136.0, "width": 8.75, "height": 13.0},
        "modelDims": {"length": 136.0, "width": 8.75, "height": 13.0},
        "materialType": "travertine_tufa_6arches",
        "arches": 6,
        "credibility": "A",
        "sourceTitle": "Platner & Ashby (1929), Bridges of Rome",
        "sourceUrl": P + "home.html"
    }
]

# 4. 14 Augustan Regions (Regiones Quattuordecim) polygons & metadata
regiones_14 = [
    {"regio": 1, "code": "Regio I", "nameLa": "Porta Capena", "nameZh": "第 1 區：卡佩納門區", "color": "#E11D48", "credibility": "B", "center": [480, 1180], "polygon": [[220, 680], [650, 720], [820, 1650], [310, 1720]], "sourceUrl": P + "R.html"},
    {"regio": 2, "code": "Regio II", "nameLa": "Caelimontium", "nameZh": "第 2 區：西利歐山區", "color": "#F97316", "credibility": "B", "center": [760, 540], "polygon": [[380, 260], [1180, 280], [1150, 820], [350, 720]], "sourceUrl": P + "R.html"},
    {"regio": 3, "code": "Regio III", "nameLa": "Isis et Serapis", "nameZh": "第 3 區：伊西斯與塞拉皮斯區（含競技場與圖拉真浴場）", "color": "#EAB308", "credibility": "A", "center": [680, -20], "polygon": [[360, -260], [1080, -280], [1060, 260], [360, 260]], "sourceUrl": P + "R.html"},
    {"regio": 4, "code": "Regio IV", "nameLa": "Templum Pacis (Subura)", "nameZh": "第 4 區：和平神廟與蘇布拉區", "color": "#84CC16", "credibility": "A", "center": [290, -180], "polygon": [[60, -450], [560, -450], [520, 110], [80, 110]], "sourceUrl": P + "Subura.html"},
    {"regio": 5, "code": "Regio V", "nameLa": "Esquiliae", "nameZh": "第 5 區：埃スクイリーノ山區", "color": "#10B981", "credibility": "B", "center": [1280, -260], "polygon": [[820, -780], [1850, -750], [1820, 280], [1080, 260]], "sourceUrl": P + "R.html"},
    {"regio": 6, "code": "Regio VI", "nameLa": "Alta Semita", "nameZh": "第 6 區：高徑區（奎里納雷山與禁衛軍營）", "color": "#06B6D4", "credibility": "A", "center": [580, -960], "polygon": [[80, -1550], [1480, -1520], [1380, -480], [120, -460]], "sourceUrl": P + "Castra_Praetoria.html"},
    {"regio": 7, "code": "Regio VII", "nameLa": "Via Lata", "nameZh": "第 7 區：寬街區（弗拉米尼亞大道東側）", "color": "#3B82F6", "credibility": "B", "center": [-120, -920], "polygon": [[-320, -1680], [80, -1550], [60, -280], [-280, -280]], "sourceUrl": P + "R.html"},
    {"regio": 8, "code": "Regio VIII", "nameLa": "Forum Romanum", "nameZh": "第 8 區：羅馬廣場與卡比托利歐山區", "color": "#6366F1", "credibility": "A", "center": [-20, -40], "polygon": [[-280, -280], [120, -280], [110, 180], [-290, 180]], "sourceUrl": P + "Forum_Romanum.html"},
    {"regio": 9, "code": "Regio IX", "nameLa": "Circus Flaminius (Campus Martius)", "nameZh": "第 9 區：戰神廣場區", "color": "#8B5CF6", "credibility": "A", "center": [-680, -580], "polygon": [[-1320, -1680], [-320, -1680], [-280, 140], [-880, 120]], "sourceUrl": P + "Pantheon.html"},
    {"regio": 10, "code": "Regio X", "nameLa": "Palatium", "nameZh": "第 10 區：帕拉提諾皇家山區", "color": "#EC4899", "credibility": "A", "center": [140, 220], "polygon": [[-60, 80], [350, 90], [340, 420], [-70, 390]], "sourceUrl": P + "Palatinus.html"},
    {"regio": 11, "code": "Regio XI", "nameLa": "Circus Maximus", "nameZh": "第 11 區：大競技場與屠牛廣場區", "color": "#F43F5E", "credibility": "A", "center": [40, 480], "polygon": [[-420, 180], [340, 420], [310, 720], [-440, 560]], "sourceUrl": P + "Circus_Maximus.html"},
    {"regio": 12, "code": "Regio XII", "nameLa": "Piscina Publica", "nameZh": "第 12 區：公共浴池區（東阿文提諾）", "color": "#14B8A6", "credibility": "B", "center": [180, 1080], "polygon": [[-20, 680], [360, 720], [380, 1480], [-60, 1420]], "sourceUrl": P + "R.html"},
    {"regio": 13, "code": "Regio XIII", "nameLa": "Aventinus & Emporium", "nameZh": "第 13 區：阿文提諾山、河港與陶片山區", "color": "#F59E0B", "credibility": "A", "center": [-320, 1020], "polygon": [[-780, 560], [-20, 680], [-60, 1580], [-820, 1560]], "sourceUrl": P + "Emporium.html"},
    {"regio": 14, "code": "Regio XIV", "nameLa": "Transtiberim & Insula Tiberina", "nameZh": "第 14 區：台伯河右岸與台伯島區", "color": "#A855F7", "credibility": "B", "center": [-1050, 320], "polygon": [[-1780, -820], [-420, 160], [-680, 1420], [-1820, 1280]], "sourceUrl": P + "Insula_Tiberina.html"}
]

# 5. Servian Wall Segments & Gates (Murus Servii Tullii) + Pomerium Cippi
servian_wall_gates = [
    {"id": "gate.servian.capena", "nameLa": "Porta Capena", "nameZh": "卡佩納門（阿庇亞大道起點）", "pos": [295.0, 19.5, 620.0], "credibility": "A", "sourceUrl": P + "Murus_Servii_Tullii.html"},
    {"id": "gate.servian.caelimontana", "nameLa": "Porta Caelimontana", "nameZh": "西利歐山門", "pos": [780.0, 48.0, 480.0], "credibility": "A", "sourceUrl": P + "Murus_Servii_Tullii.html"},
    {"id": "gate.servian.esquilina", "nameLa": "Porta Esquilina (Arcus Gallieni)", "nameZh": "埃スクイリーノ門", "pos": [920.0, 52.0, -210.0], "credibility": "A", "sourceUrl": P + "Murus_Servii_Tullii.html"},
    {"id": "gate.servian.viminalis", "nameLa": "Porta Viminalis", "nameZh": "維米納萊門（含高地防禦土壘 Agger）", "pos": [960.0, 58.0, -680.0], "credibility": "A", "sourceUrl": P + "Murus_Servii_Tullii.html"},
    {"id": "gate.servian.collina", "nameLa": "Porta Collina", "nameZh": "科利納門", "pos": [860.0, 59.0, -1120.0], "credibility": "A", "sourceUrl": P + "Murus_Servii_Tullii.html"},
    {"id": "gate.servian.fontinalis", "nameLa": "Porta Fontinalis", "nameZh": "泉門（弗拉米尼亞大道起點）", "pos": [-65.0, 26.0, -215.0], "credibility": "A", "sourceUrl": P + "Murus_Servii_Tullii.html"},
    {"id": "gate.servian.carmentalis", "nameLa": "Porta Carmentalis", "nameZh": "卡爾門塔利斯門", "pos": [-285.0, 13.5, 110.0], "credibility": "A", "sourceUrl": P + "Murus_Servii_Tullii.html"},
    {"id": "gate.servian.trigemina", "nameLa": "Porta Trigemina", "nameZh": "三拱門（河港入口）", "pos": [-385.0, 12.5, 520.0], "credibility": "A", "sourceUrl": P + "Murus_Servii_Tullii.html"},
    {"id": "gate.servian.raudusculana", "nameLa": "Porta Raudusculana", "nameZh": "青銅門（阿文提諾南側）", "pos": [-95.0, 38.0, 1080.0], "credibility": "A", "sourceUrl": P + "Murus_Servii_Tullii.html"},
    {"id": "gate.servian.naevia", "nameLa": "Porta Naevia", "nameZh": "奈維亞門", "pos": [125.0, 39.5, 1060.0], "credibility": "A", "sourceUrl": P + "Murus_Servii_Tullii.html"}
]

# 6. Update Landmarks JSON with user's 10 confirmed rules:
# - Remove Pons Aelius (bridge.tiber.0091) completely
# - Add Hadrian's Athenaeum (bldg.reg08.athenaeum.0091) as second construction site (foundation excavation)
# - Mark FUR-only inferred items as Tier B (Decision #4)
with open("/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p1/data/p1_world_data.json", "w", encoding="utf-8") as f:
    json.dump({
        "metadata": {
            "project": "Roma Aeterna AD 128",
            "lockedYear": 128,
            "emperor": "Hadrianus (AD 117–138)",
            "scale": "1:1 (1 unit = 1 meter)",
            "origin": "Milliarium Aureum (Forum Romanum)",
            "chunkGrid": "48x48 chunks of 128x128m (6144x6144m core)",
            "waterLevelElevationM": 6.5,
            "characterEyeHeightM": 1.65,
            "furCredibilityRule": "Tier B (per User Decision #4)",
            "ponsAeliusExcluded": True
        },
        "hills": hills_dem,
        "tiberChannel": tiber_channel,
        "bridges": bridges_128ad,
        "regiones": regiones_14,
        "servianWallGates": servian_wall_gates
    }, f, ensure_ascii=False, indent=2)

print("Saved p1_world_data.json successfully.")
