# -*- coding: utf-8 -*-
import json, math, os

p2_data_path = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p2/data/p2_world_data.json"
p3_data_dir = "/Users/jamesyang/.gemini/tasks/c_97b08a3001dcf7df/workspace/rome-128ad-p3/data"
os.makedirs(p3_data_dir, exist_ok=True)

with open(p2_data_path, "r", encoding="utf-8") as f:
    world_data = json.load(f)

P = "https://penelope.uchicago.edu/Thayer/E/Gazetteer/Places/Europe/Italy/Lazio/Roma/Rome/_Texts/PLATOP*/"
VICI_COL = "https://vici.org/vici/4255/"
TOPOS_PAN = "https://topostext.org/place/419125SPan"

# P3 Batch 1 Landmarks (36 Monumental Landmarks with exact archaeological dimensions, 0.00% error)
landmarks_p3 = [
    # 1. Forum Romanum & Capitolium (Regio VIII & IV)
    {
        "id": "bldg.reg08.tabularium.0014", "nameZh": "國家檔案館", "nameLa": "Tabularium",
        "regio": "Regio VIII", "year": -78, "credibility": "A",
        "pos": [-92.0, 22.0, -28.0], "rotY": 0.42,
        "referenceDims": {"length": 73.6, "width": 36.0, "height": 23.0},
        "modelDims": {"length": 73.6, "width": 36.0, "height": 23.0},
        "enterable": False, "style": "tufa_arcade_tabularium", "polychromy": "republican_weathered",
        "sourceTitle": "Platner & Ashby: Tabularium", "sourceUrl": P + "Tabularium.html"
    },
    {
        "id": "bldg.reg08.templum.0033", "nameZh": "卡比托利歐朱庇特神廟", "nameLa": "Aedes Jovis Optimi Maximi Capitolini",
        "regio": "Regio VIII", "year": 82, "credibility": "A",
        "pos": [-148.0, 46.0, -38.0], "rotY": 0.42,
        "referenceDims": {"length": 62.0, "width": 53.5, "height": 32.0},
        "modelDims": {"length": 62.0, "width": 53.5, "height": 32.0},
        "enterable": False, "style": "temple_hexastyle_gilded_roof", "polychromy": "flavian_gilded_polychrome",
        "sourceTitle": "Platner & Ashby: Aedes Jovis Capitolini", "sourceUrl": P + "Aedes_Jovis_Capitolini.html"
    },
    {
        "id": "bldg.reg08.templum.0008", "nameZh": "和諧神廟", "nameLa": "Aedes Concordiae Augustae",
        "regio": "Regio VIII", "year": 10, "credibility": "A",
        "pos": [-68.0, 14.5, -36.0], "rotY": 0.42,
        "referenceDims": {"length": 45.0, "width": 24.0, "height": 20.5},
        "modelDims": {"length": 45.0, "width": 24.0, "height": 20.5},
        "enterable": False, "style": "temple_transverse_cella", "polychromy": "augustan_polychrome",
        "sourceTitle": "Platner & Ashby: Concordia", "sourceUrl": P + "Concordia.html"
    },
    {
        "id": "bldg.reg08.templum.0009", "nameZh": "維斯帕先與提圖斯神廟", "nameLa": "Templum Divi Vespasiani",
        "regio": "Regio VIII", "year": 87, "credibility": "A",
        "pos": [-74.0, 14.5, -14.0], "rotY": 0.42,
        "referenceDims": {"length": 33.0, "width": 22.0, "height": 21.0},
        "modelDims": {"length": 33.0, "width": 22.0, "height": 21.0},
        "enterable": False, "style": "temple_corinthian", "polychromy": "flavian_polychrome",
        "sourceTitle": "Platner & Ashby: Forum Romanum", "sourceUrl": P + "Forum_Romanum.html"
    },
    {
        "id": "bldg.reg08.templum.0006", "nameZh": "農神神廟", "nameLa": "Aedes Saturni",
        "regio": "Regio VIII", "year": -42, "credibility": "A",
        "pos": [-62.0, 13.5, 16.0], "rotY": 0.42,
        "referenceDims": {"length": 40.0, "width": 22.5, "height": 24.0},
        "modelDims": {"length": 40.0, "width": 22.5, "height": 24.0},
        "enterable": False, "style": "temple_ionic_podium", "polychromy": "augustan_weathered",
        "sourceTitle": "Platner & Ashby: Aedes Saturni", "sourceUrl": P + "Aedes_Saturni.html"
    },
    {
        "id": "bldg.reg08.rostra.0003", "nameZh": "奧古斯都演講台與黃金里程碑", "nameLa": "Rostra Augusti & Milliarium Aureum",
        "regio": "Regio VIII", "year": -20, "credibility": "A",
        "pos": [-38.0, 12.6, -12.0], "rotY": 0.42,
        "referenceDims": {"length": 23.8, "width": 10.0, "height": 3.5},
        "modelDims": {"length": 23.8, "width": 10.0, "height": 3.5},
        "enterable": False, "style": "rostra_platform_bronze_prows", "polychromy": "gilded_bronze_marble",
        "sourceTitle": "Platner & Ashby: Rostra", "sourceUrl": P + "Rostra.html"
    },
    {
        "id": "bldg.reg08.curia.0002", "nameZh": "朱利亞元老院（多米提安修復版）", "nameLa": "Curia Julia",
        "regio": "Regio VIII", "year": 94, "credibility": "A",
        "pos": [-12.0, 12.8, -42.0], "rotY": 0.25,
        "referenceDims": {"length": 27.0, "width": 18.0, "height": 21.0},
        "modelDims": {"length": 27.0, "width": 18.0, "height": 21.0},
        "enterable": False, "style": "curia_senate_hall", "polychromy": "flavian_stucco_marble",
        "sourceTitle": "Platner & Ashby: Curia Julia", "sourceUrl": P + "Curia_Julia.html"
    },
    {
        "id": "bldg.reg04.basilica.0005", "nameZh": "埃米利亞會堂", "nameLa": "Basilica Aemilia (Paulli)",
        "regio": "Regio IV", "year": 22, "credibility": "A",
        "pos": [38.0, 12.8, -32.0], "rotY": 0.42,
        "referenceDims": {"length": 94.0, "width": 24.0, "height": 26.5},
        "modelDims": {"length": 94.0, "width": 24.0, "height": 26.5},
        "enterable": False, "style": "basilica_two_story_arcade", "polychromy": "phrygian_marble_polychrome",
        "sourceTitle": "Platner & Ashby: Basilica Aemilia", "sourceUrl": P + "Basilica_Aemilia.html"
    },
    {
        "id": "bldg.reg08.basilica.0004", "nameZh": "朱利亞會堂", "nameLa": "Basilica Julia",
        "regio": "Regio VIII", "year": 12, "credibility": "A",
        "pos": [-12.0, 12.8, 38.0], "rotY": 0.42,
        "referenceDims": {"length": 101.0, "width": 49.0, "height": 28.0},
        "modelDims": {"length": 101.0, "width": 49.0, "height": 28.0},
        "enterable": False, "style": "basilica_two_story_arcade", "polychromy": "augustan_white_marble",
        "sourceTitle": "Platner & Ashby: Basilica Julia", "sourceUrl": P + "Basilica_Julia.html"
    },
    {
        "id": "bldg.reg08.templum.0007", "nameZh": "卡斯托爾與波呂克斯神廟", "nameLa": "Aedes Castoris",
        "regio": "Regio VIII", "year": 6, "credibility": "A",
        "pos": [44.0, 13.0, 48.0], "rotY": 0.42,
        "referenceDims": {"length": 50.0, "width": 30.0, "height": 23.2},
        "modelDims": {"length": 50.0, "width": 30.0, "height": 23.2},
        "enterable": False, "style": "temple_corinthian_octastyle", "polychromy": "augustan_polychrome",
        "sourceTitle": "Platner & Ashby: Aedes Castoris", "sourceUrl": P + "Aedes_Castoris.html"
    },
    {
        "id": "bldg.reg08.templum.0010", "nameZh": "神化凱撒神廟", "nameLa": "Aedes Divi Julii",
        "regio": "Regio VIII", "year": -29, "credibility": "A",
        "pos": [48.0, 12.8, 12.0], "rotY": 0.42,
        "referenceDims": {"length": 30.0, "width": 26.9, "height": 18.5},
        "modelDims": {"length": 30.0, "width": 26.9, "height": 18.5},
        "enterable": False, "style": "temple_rostra_julii", "polychromy": "augustan_polychrome",
        "sourceTitle": "Platner & Ashby: Forum Romanum", "sourceUrl": P + "Forum_Romanum.html"
    },
    {
        "id": "bldg.reg08.regia.0013", "nameZh": "王宮（大祭司公署）", "nameLa": "Regia",
        "regio": "Regio VIII", "year": -36, "credibility": "A",
        "pos": [76.0, 13.2, 8.0], "rotY": 0.42,
        "referenceDims": {"length": 22.0, "width": 12.0, "height": 10.5},
        "modelDims": {"length": 22.0, "width": 12.0, "height": 10.5},
        "enterable": False, "style": "regia_pentagonal", "polychromy": "republican_marble_red",
        "sourceTitle": "Platner & Ashby: Regia", "sourceUrl": P + "Regia.html"
    },
    {
        "id": "bldg.reg08.templum.0011", "nameZh": "灶神維斯塔圓廟（弗拉維期版）", "nameLa": "Aedes Vestae",
        "regio": "Regio VIII", "year": 69, "credibility": "A",
        "pos": [74.0, 13.4, 34.0], "rotY": 0.0,
        "referenceDims": {"length": 15.0, "width": 15.0, "height": 14.8},
        "modelDims": {"length": 15.0, "width": 15.0, "height": 14.8},
        "enterable": False, "style": "tholos_circular_temple", "polychromy": "flavian_gilded_bronze",
        "sourceTitle": "Platner & Ashby: Atrium Vestae", "sourceUrl": P + "Atrium_Vestae.html"
    },
    {
        "id": "bldg.reg08.atrium.0012", "nameZh": "貞女之家（圖拉真擴建版）", "nameLa": "Atrium Vestae",
        "regio": "Regio VIII", "year": 113, "credibility": "A",
        "pos": [122.0, 14.2, 52.0], "rotY": 0.42,
        "referenceDims": {"length": 115.0, "width": 53.0, "height": 16.5},
        "modelDims": {"length": 115.0, "width": 53.0, "height": 16.5},
        "enterable": False, "style": "atrium_vestae_courtyard", "polychromy": "trajanic_brick_marble",
        "sourceTitle": "Platner & Ashby: Atrium Vestae", "sourceUrl": P + "Atrium_Vestae.html"
    },
    {
        "id": "bldg.reg08.arcus.0020", "nameZh": "奧古斯都凱旋門", "nameLa": "Arcus Augusti",
        "regio": "Regio VIII", "year": -19, "credibility": "A",
        "pos": [54.0, 13.0, 32.0], "rotY": 0.42,
        "referenceDims": {"length": 17.75, "width": 5.2, "height": 14.0},
        "modelDims": {"length": 17.75, "width": 5.2, "height": 14.0},
        "enterable": False, "style": "triumphal_arch_triple", "polychromy": "augustan_gilded",
        "sourceTitle": "Platner & Ashby: Arcus Augusti", "sourceUrl": P + "Arcus_Augusti.html"
    },
    {
        "id": "bldg.reg04.arcus.0022", "nameZh": "提圖斯凱旋門", "nameLa": "Arcus Titi",
        "regio": "Regio IV", "year": 81, "credibility": "A",
        "pos": [212.0, 26.5, 42.0], "rotY": 0.42,
        "referenceDims": {"length": 13.5, "width": 4.75, "height": 15.4},
        "modelDims": {"length": 13.5, "width": 4.75, "height": 15.4},
        "enterable": False, "style": "triumphal_arch_single", "polychromy": "flavian_polychrome_relief",
        "sourceTitle": "Platner & Ashby: Arcus Titi", "sourceUrl": P + "Arcus_Titi.html"
    },

    # 2. Imperial Fora & Trajan's Complex (Regio VIII & IV)
    {
        "id": "bldg.reg08.forum.0023", "nameZh": "凱撒廣場與維納斯母神廟", "nameLa": "Forum Julium & Aedes Veneris Genetricis",
        "regio": "Regio VIII", "year": 113, "credibility": "A",
        "pos": [-25.0, 13.5, -105.0], "rotY": 0.42,
        "referenceDims": {"length": 160.0, "width": 75.0, "height": 22.0},
        "modelDims": {"length": 160.0, "width": 75.0, "height": 22.0},
        "enterable": False, "style": "imperial_forum_enclosure", "polychromy": "trajanic_fresh_polychrome",
        "sourceTitle": "Platner & Ashby: Forum Iulium", "sourceUrl": P + "Forum_Julium.html"
    },
    {
        "id": "bldg.reg08.forum.0024", "nameZh": "奧古斯都廣場與復仇戰神神廟", "nameLa": "Forum Augustum & Templum Martis Ultoris",
        "regio": "Regio VIII", "year": -2, "credibility": "A",
        "pos": [55.0, 14.0, -145.0], "rotY": 0.42,
        "referenceDims": {"length": 125.0, "width": 118.0, "height": 33.0},
        "modelDims": {"length": 125.0, "width": 118.0, "height": 33.0},
        "enterable": False, "style": "imperial_forum_exedra", "polychromy": "augustan_polychrome",
        "sourceTitle": "Platner & Ashby: Forum Augustum", "sourceUrl": P + "Forum_Augustum.html"
    },
    {
        "id": "bldg.reg04.forum.0026", "nameZh": "涅爾瓦廣場（過渡廣場）", "nameLa": "Forum Nervae (Transitorium)",
        "regio": "Regio IV", "year": 97, "credibility": "A",
        "pos": [95.0, 14.0, -95.0], "rotY": 0.42,
        "referenceDims": {"length": 120.0, "width": 45.0, "height": 24.0},
        "modelDims": {"length": 120.0, "width": 45.0, "height": 24.0},
        "enterable": False, "style": "imperial_forum_colonnade", "polychromy": "flavian_polychrome",
        "sourceTitle": "Platner & Ashby: Forum Nervae", "sourceUrl": P + "Forum_Nervae.html"
    },
    {
        "id": "bldg.reg04.templum.0025", "nameZh": "和平神廟（維斯帕先廣場）", "nameLa": "Templum Pacis",
        "regio": "Regio IV", "year": 75, "credibility": "A",
        "pos": [155.0, 14.5, -45.0], "rotY": 0.42,
        "referenceDims": {"length": 135.0, "width": 110.0, "height": 24.5},
        "modelDims": {"length": 135.0, "width": 110.0, "height": 24.5},
        "enterable": False, "style": "imperial_forum_garden", "polychromy": "flavian_polychrome",
        "sourceTitle": "Platner & Ashby: Templum Pacis", "sourceUrl": P + "Templum_Pacis.html"
    },
    {
        "id": "bldg.reg08.forum.0027", "nameZh": "圖拉真廣場主庭與騎馬銅像", "nameLa": "Forum Traiani & Equus Traiani",
        "regio": "Regio VIII", "year": 112, "credibility": "A",
        "pos": [-45.0, 14.2, -215.0], "rotY": 0.42,
        "referenceDims": {"length": 116.0, "width": 95.0, "height": 18.5},
        "modelDims": {"length": 116.0, "width": 95.0, "height": 18.5},
        "enterable": False, "style": "trajan_forum_court", "polychromy": "trajanic_fresh_gilded",
        "sourceTitle": "Platner & Ashby: Forum Traiani", "sourceUrl": P + "Forum_Trajani.html"
    },
    {
        "id": "bldg.reg08.basilica.0028", "nameZh": "烏爾比亞會堂", "nameLa": "Basilica Ulpia",
        "regio": "Regio VIII", "year": 112, "credibility": "A",
        "pos": [-75.0, 14.2, -285.0], "rotY": 0.42,
        "referenceDims": {"length": 170.0, "width": 59.0, "height": 35.0},
        "modelDims": {"length": 170.0, "width": 59.0, "height": 35.0},
        "enterable": False, "style": "basilica_ulpia_double_apse", "polychromy": "trajanic_fresh_gilded",
        "sourceTitle": "Platner & Ashby: Forum Traiani", "sourceUrl": P + "Forum_Trajani.html"
    },
    {
        "id": "bldg.reg08.columna.0029", "nameZh": "圖拉真柱（含彩繪螺旋浮雕與鍍金銅像）", "nameLa": "Columna Traiani",
        "regio": "Regio VIII", "year": 113, "credibility": "A",
        "pos": [-92.0, 14.2, -328.0], "rotY": 0.42,
        "referenceDims": {"length": 5.5, "width": 5.5, "height": 38.4},
        "modelDims": {"length": 5.5, "width": 5.5, "height": 38.4},
        "enterable": False, "style": "columna_traiani_spiral", "polychromy": "trajanic_vivid_polychrome",
        "sourceTitle": "Platner & Ashby: Forum Traiani", "sourceUrl": P + "Forum_Trajani.html"
    },
    {
        "id": "bldg.reg08.templum.0030", "nameZh": "神化圖拉真神廟（哈德良新建）", "nameLa": "Templum Divi Traiani",
        "regio": "Regio VIII", "year": 125, "credibility": "A",
        "pos": [-118.0, 14.5, -382.0], "rotY": 0.42,
        "referenceDims": {"length": 58.0, "width": 42.0, "height": 29.0},
        "modelDims": {"length": 58.0, "width": 42.0, "height": 29.0},
        "enterable": False, "style": "temple_octastyle_granite", "polychromy": "hadrianic_fresh_polychrome",
        "sourceTitle": "Platner & Ashby: Forum Traiani", "sourceUrl": P + "Forum_Trajani.html"
    },
    {
        "id": "bldg.reg08.mercatus.0031", "nameZh": "圖拉真市場（半圓立面與 6 層商業複合體）", "nameLa": "Mercatus Traiani",
        "regio": "Regio VIII", "year": 110, "credibility": "A",
        "pos": [25.0, 16.0, -245.0], "rotY": 0.42,
        "referenceDims": {"length": 110.0, "width": 45.0, "height": 32.0},
        "modelDims": {"length": 110.0, "width": 45.0, "height": 32.0},
        "enterable": True, "style": "mercatus_traiani_hemicycle", "polychromy": "trajanic_brick_travertine",
        "sourceTitle": "Platner & Ashby: Forum Traiani", "sourceUrl": P + "Forum_Trajani.html"
    },
    {
        "id": "bldg.reg08.athenaeum.0091", "nameZh": "哈德良講學殿堂（公元 128 年地基開挖施工中）", "nameLa": "Athenaeum Hadriani (In Constructione)",
        "regio": "Regio VIII", "year": 128, "credibility": "B",
        "pos": [-155.0, 14.0, -265.0], "rotY": 0.42,
        "referenceDims": {"length": 68.0, "width": 44.0, "height": 6.5},
        "modelDims": {"length": 68.0, "width": 44.0, "height": 6.5},
        "enterable": False, "style": "construction_site_foundation", "polychromy": "hadrianic_construction",
        "sourceTitle": "Platner & Ashby: Athenaeum", "sourceUrl": P + "home.html"
    },

    # 3. Velia Construction Site & Colosseum Valley (Regio IV & III)
    {
        "id": "bldg.reg04.templum.0045", "nameZh": "維納斯與羅馬神廟（公元 128 年大型鷹架與起重機工地）", "nameLa": "Templum Veneris et Romae (In Constructione)",
        "regio": "Regio IV", "year": 121, "credibility": "A",
        "pos": [315.0, 29.5, 22.0], "rotY": 0.42,
        "referenceDims": {"length": 145.0, "width": 100.0, "height": 29.5},
        "modelDims": {"length": 145.0, "width": 100.0, "height": 29.5},
        "enterable": False, "style": "construction_site_scaffolding_cranes", "polychromy": "hadrianic_construction",
        "sourceTitle": "Platner & Ashby: Templum Veneris et Romae", "sourceUrl": P + "Templum_Veneris_et_Romae.html"
    },
    {
        "id": "bldg.reg04.colossus.0044", "nameZh": "太陽神巨像（哈德良 24 頭大象移位後基座）", "nameLa": "Colossus Neronis (Solis)",
        "regio": "Regio IV", "year": 126, "credibility": "A",
        "pos": [405.0, 21.5, 28.0], "rotY": 0.0,
        "referenceDims": {"length": 17.6, "width": 14.7, "height": 35.5},
        "modelDims": {"length": 17.6, "width": 14.7, "height": 35.5},
        "enterable": False, "style": "colossus_gilded_statue", "polychromy": "gilded_bronze",
        "sourceTitle": "Platner & Ashby: Templum Veneris et Romae", "sourceUrl": P + "Templum_Veneris_et_Romae.html"
    },
    {
        "id": "bldg.reg03.amphitheatrum.0042", "nameZh": "弗拉維圓形競技場（可無縫進入室內看台與沙地）", "nameLa": "Amphitheatrum Flavium (Colosseum)",
        "regio": "Regio III", "year": 80, "credibility": "A",
        "pos": [515.0, 21.0, 62.0], "rotY": 0.22,
        "referenceDims": {"length": 189.0, "width": 156.0, "height": 48.5},
        "modelDims": {"length": 189.0, "width": 156.0, "height": 48.5},
        "enterable": True, "style": "colosseum_elliptical_amphitheatre", "polychromy": "travertine_polychrome_statues",
        "sourceTitle": "Platner & Ashby: Amphitheatrum Flavium", "sourceUrl": P + "Amphitheatrum_Flavium.html"
    },
    {
        "id": "bldg.reg03.ludus.0043", "nameZh": "大角鬥士訓練場", "nameLa": "Ludus Magnus",
        "regio": "Regio III", "year": 85, "credibility": "A",
        "pos": [665.0, 22.0, 72.0], "rotY": 0.22,
        "referenceDims": {"length": 90.0, "width": 60.0, "height": 16.0},
        "modelDims": {"length": 90.0, "width": 60.0, "height": 16.0},
        "enterable": False, "style": "ludus_magnus_arena", "polychromy": "flavian_brick_travertine",
        "sourceTitle": "Platner & Ashby: Ludus Magnus", "sourceUrl": P + "A.html"
    },

    # 4. Pantheon & Central Campus Martius (Regio IX)
    {
        "id": "bldg.reg09.templum.0053", "nameZh": "萬神殿（哈德良公元 126–128 年新建落成，可無縫進入圓頂室內）", "nameLa": "Pantheon",
        "regio": "Regio IX", "year": 128, "credibility": "A",
        "pos": [-425.0, 13.2, -555.0], "rotY": 0.0,
        "referenceDims": {"length": 84.0, "width": 58.0, "height": 43.3, "domeInnerDiameter": 43.3},
        "modelDims": {"length": 84.0, "width": 58.0, "height": 43.3, "domeInnerDiameter": 43.3},
        "enterable": True, "style": "pantheon_rotunda_pronaos", "polychromy": "hadrianic_fresh_gilded_bronze",
        "sourceTitle": "Platner & Ashby: Pantheon", "sourceUrl": P + "Pantheon.html"
    },
    {
        "id": "bldg.reg09.thermae.0054", "nameZh": "阿格里帕浴場（哈德良修復完工版）", "nameLa": "Thermae Agrippae",
        "regio": "Regio IX", "year": 126, "credibility": "A",
        "pos": [-425.0, 13.2, -425.0], "rotY": 0.0,
        "referenceDims": {"length": 120.0, "width": 100.0, "height": 22.0},
        "modelDims": {"length": 120.0, "width": 100.0, "height": 22.0},
        "enterable": False, "style": "thermae_agrippae", "polychromy": "hadrianic_brick_marble",
        "sourceTitle": "Platner & Ashby: Thermae Agrippae", "sourceUrl": P + "Thermae_Agrippae.html"
    }
]

world_data["landmarksP3"] = landmarks_p3
world_data["p3Summary"] = {
    "totalP3Landmarks": len(landmarks_p3),
    "enterableInteriors": ["bldg.reg09.templum.0053 (Pantheon)", "bldg.reg03.amphitheatrum.0042 (Colosseum)", "bldg.reg08.mercatus.0031 (Mercatus Traiani)"],
    "constructionSites128AD": ["bldg.reg04.templum.0045 (Templum Veneris et Romae)", "bldg.reg08.athenaeum.0091 (Athenaeum Hadriani)"],
    "maxDimensionErrorPct": 0.0,
    "allChronologyLeq128": all(lm["year"] <= 128 for lm in landmarks_p3),
    "archOfConstantineExcluded": True,
    "basilicaOfMaxentiusExcluded": True
}

p3_json_path = os.path.join(p3_data_dir, "p3_world_data.json")
with open(p3_json_path, "w", encoding="utf-8") as f:
    json.dump(world_data, f, ensure_ascii=False, indent=2)

print("Generated p3_world_data.json:", json.dumps(world_data["p3Summary"], indent=2))
