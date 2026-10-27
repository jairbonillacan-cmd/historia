#!/usr/bin/env python3
"""
ZERO-JITTER, FULL VECTOR & ROSSARK-MOTION-SKILL RENDERER FOR:
"EL DESASTRE DE BARI (2 DE DICIEMBRE DE 1943) — EL SECRETO QUE CREÓ LA QUIMIOTERAPIA"
(1080x1920 @ 60fps, BT.709, -14.0 LUFS, Spanish SRT muxed, 0.0px archival photo jitter)
"""
import os
import sys
import json
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1920
OUT_DIR = "produccion/02_desastre_bari"
ASSETS_DIR = os.path.join(OUT_DIR, "assets")
os.makedirs(OUT_DIR, exist_ok=True)

with open(os.path.join(OUT_DIR, "timeline_45_chunks.json"), "r", encoding="utf-8") as f:
    TL_DATA = json.load(f)

CHUNKS = TL_DATA["chunks"]
TOTAL_DUR = TL_DATA["total_duration"]

def load_font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

FONT_SUB_REG = load_font(["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"], 46)
FONT_SUB_BOLD = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 46)
FONT_HEADLINE = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 48)
FONT_SUBHEAD = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 22)

FONT_RIBBON = load_font(["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/courbd.ttf"], 24)
FONT_DOC_HDR = load_font(["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/courbd.ttf"], 21)
FONT_DOC_META = load_font(["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/courbd.ttf"], 22)
FONT_DOC_LINE = load_font(["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"], 24)
FONT_DOC_BOLD = load_font(["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/courbd.ttf"], 24)
FONT_STAMP = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 30)
FONT_FOOTER = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 15)
FONT_ATTR = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 17)

FONT_PILL_LG = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 32)
FONT_PILL_MD = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 25)
FONT_PILL_SM = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 20)
FONT_BIG_NUM = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 72)

# Palette tokens
C_ABYSS = (13, 13, 13)         # #0D0D0D
C_OCEAN_DARK = (11, 37, 69)    # #0B2545
C_LAND_FILL = (107, 127, 70)   # #6B7F46
C_LAND_STROKE = (148, 168, 107)# #94A86B
C_PAPER = (244, 239, 230)      # #F4EFE6
C_INK = (26, 25, 23)           # #1A1917
C_STAMP_RED = (214, 54, 41)    # #D63629
C_NEUTRAL = (245, 242, 235)    # #F5F2EB
C_AMBER = (240, 180, 41)       # #F0B429
C_DANGER = (224, 90, 71)       # #E05A47
C_TACTICAL = (96, 165, 250)    # #60A5FA
C_TOXIC = (205, 190, 45)       # Mustard gas sulfur yellow-green
C_HEAL = (52, 211, 153)        # Medical emerald green
C_WHITE = (255, 255, 255)

def spring_val(t_sec, delay_sec=0.0, stiffness=140.0, damping=16.0):
    dt = t_sec - delay_sec
    if dt <= 0:
        return 0.0
    omega = math.sqrt(stiffness)
    zeta = damping / (2.0 * omega)
    if zeta < 1.0:
        wd = omega * math.sqrt(1.0 - zeta * zeta)
        val = 1.0 - math.exp(-zeta * omega * dt) * (math.cos(wd * dt) + (zeta * omega / wd) * math.sin(wd * dt))
    else:
        val = 1.0 - (1.0 + omega * dt) * math.exp(-omega * dt)
    return max(0.0, min(1.18, val))

# ==============================================================================
# ROSSARK-MOTION-SKILL ENGINE (Ported 1:1 from templates/react-native/motion.ts,
# liveFace.tsx, ChefScene.swift & RevealScene.swift)
# ==============================================================================
def _cubic_bezier(p, x1, y1, x2, y2):
    p = max(0.0, min(1.0, float(p)))
    if p <= 0.0 or p >= 1.0:
        return p
    t = p
    for _ in range(6):
        mt = 1.0 - t
        bx = 3.0 * mt * mt * t * x1 + 3.0 * mt * t * t * x2 + t * t * t - p
        dbx = 3.0 * mt * mt * x1 + 6.0 * mt * t * (x2 - x1) + 3.0 * t * t * (1.0 - x2)
        if abs(dbx) < 1e-6:
            break
        t = max(0.0, min(1.0, t - bx / dbx))
    mt = 1.0 - t
    return 3.0 * mt * mt * t * y1 + 3.0 * mt * t * t * y2 + t * t * t

def EASE_IN_OUT(p):
    return _cubic_bezier(p, 0.77, 0.0, 0.175, 1.0)

def EASE_OUT(p):
    return _cubic_bezier(p, 0.23, 1.0, 0.32, 1.0)

def EASE_IN(p):
    return _cubic_bezier(p, 0.55, 0.0, 1.0, 0.45)

def track(t_ms, keys):
    if t_ms <= keys[0][0]:
        return float(keys[0][1])
    for i in range(1, len(keys)):
        k1 = keys[i]
        if t_ms <= k1[0]:
            k0 = keys[i - 1]
            span = k1[0] - k0[0]
            p = (t_ms - k0[0]) / span if span > 0 else 1.0
            is_out = (len(k1) > 2 and k1[2] == "out")
            e = EASE_OUT(p) if is_out else EASE_IN_OUT(p)
            return k0[1] + (k1[1] - k0[1]) * e
    return float(keys[-1][1])

def flow(t_ms, k):
    n = len(k)
    if t_ms <= k[0][0]:
        return float(k[0][1])
    if t_ms >= k[-1][0]:
        return float(k[-1][1])
    i = 0
    while i + 1 < n - 1 and k[i + 1][0] < t_ms:
        i += 1
    def slope(j):
        denom = k[j + 1][0] - k[j][0]
        return (k[j + 1][1] - k[j][1]) / denom if denom > 0 else 0.0
    def tangent(j):
        if j == 0 or j == n - 1:
            return 0.0
        a = slope(j - 1)
        b = slope(j)
        if a * b <= 0:
            return 0.0
        h0 = k[j][0] - k[j - 1][0]
        h1 = k[j + 1][0] - k[j][0]
        w0 = 2.0 * h1 + h0
        w1 = h1 + 2.0 * h0
        return (w0 + w1) / (w0 / a + w1 / b)
    h = k[i + 1][0] - k[i][0]
    s = (t_ms - k[i][0]) / h if h > 0 else 0.0
    s2 = s * s
    s3 = s2 * s
    return (
        (2.0 * s3 - 3.0 * s2 + 1.0) * k[i][1]
        + (s3 - 2.0 * s2 + s) * h * tangent(i)
        + (-2.0 * s3 + 3.0 * s2) * k[i + 1][1]
        + (s3 - s2) * h * tangent(i + 1)
    )

def seg(t_ms, a, b, curve="out"):
    if t_ms <= a:
        return 0.0
    if t_ms >= b:
        return 1.0
    p = (t_ms - a) / (b - a)
    return EASE_OUT(p) if curve == "out" else EASE_IN_OUT(p)

def wave(t_ms, period, phase=0.0):
    return math.sin((t_ms / period + phase) * math.pi * 2.0)

def loop_p(t_ms, period, phase=0.0):
    p = (t_ms / period + phase) % 1.0
    return p + 1.0 if p < 0 else p

def bell(p):
    return math.sin(math.pi * min(1.0, max(0.0, p)))

def seeded(i, salt=0):
    x = math.sin(i * 12.9898 + salt * 78.233) * 43758.5453
    return x - math.floor(x)

def make_blink_keys(loop_ms, blink_times):
    keys = [(0, 0.0)]
    for b in blink_times:
        keys.extend([(b, 0.0), (b + 110, 1.0), (b + 150, 1.0), (b + 340, 0.0, "out")])
    keys.append((loop_ms, 0.0))
    return keys

# Pre-build Base Canvases
def make_abyss_canvas():
    img = Image.new("RGB", (W, H), C_ABYSS)
    pix = img.load()
    cx, cy = W / 2.0, H * 0.52
    max_d = math.hypot(cx, cy)
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            d = math.hypot(x - cx, y - cy) / max_d
            t = max(0.0, min(1.0, 1.0 - d)) ** 1.3
            r, g, b = int(11 + 15 * t), int(12 + 17 * t), int(14 + 22 * t)
            pix[x, y] = (r, g, b)
            if x+1 < W: pix[x+1, y] = (r, g, b)
            if y+1 < H: pix[x, y+1] = (r, g, b)
            if x+1 < W and y+1 < H: pix[x+1, y+1] = (r, g, b)
    return img

CANVAS_ABYSS = make_abyss_canvas()

def make_tactical_ocean_canvas():
    img = CANVAS_ABYSS.copy()
    stage = Image.new("RGB", (W, 820), C_OCEAN_DARK)
    sd = ImageDraw.Draw(stage)
    for gx in range(0, W, 60):
        sd.line([(gx, 0), (gx, 820)], fill=(24, 52, 88), width=1)
    for gy in range(0, 820, 60):
        sd.line([(0, gy), (W, gy)], fill=(24, 52, 88), width=1)
    mask = Image.new("L", (W, 820), 255)
    md = ImageDraw.Draw(mask)
    for y in range(130):
        md.line([(0, y), (W, y)], fill=int(255 * (y / 130.0)))
    for y in range(680, 820):
        md.line([(0, y), (W, y)], fill=int(255 * (1.0 - (y - 680) / 140.0)))
    img.paste(stage, (0, 640), mask)
    return img

CANVAS_TACTICAL_MAP = make_tactical_ocean_canvas()

STAGE_FEATHER_MASK = Image.new("L", (W, 760), 255)
_fdraw = ImageDraw.Draw(STAGE_FEATHER_MASK)
for _y in range(115):
    _fdraw.line([(0, _y), (W, _y)], fill=int(255 * (_y / 115.0)))
for _y in range(635, 760):
    _fdraw.line([(0, _y), (W, _y)], fill=int(255 * (1.0 - (_y - 635) / 125.0)))

def fit_photo_once(img, tw, th, fy=0.45):
    iw, ih = img.size
    tr = tw / th
    ir = iw / ih
    if ir > tr:
        nw, nh = int(ih * tr), ih
    else:
        nw, nh = iw, int(iw / tr)
    cx, cy = iw // 2, int(ih * fy)
    x0 = max(0, min(iw - nw, cx - nw // 2))
    y0 = max(0, min(ih - nh, cy - nh // 2))
    return img.crop((x0, y0, x0 + nw, y0 + nh)).resize((tw, th), Image.Resampling.LANCZOS)

# PRE-COMPOSITE STEADY ARCHIVAL STAGES ONCE AT STARTUP -> 0.0px JITTER!
PHOTOS_STEADY_STAGE = {}
for key, fname, fy_val in [
    ("explosion", "bari_explosion.jpg", 0.50),
    ("ships", "bari_ships.jpg", 0.50),
    ("ju88", "ju88.jpg", 0.45),
    ("liberty", "liberty_ship.jpg", 0.50),
    ("coningham", "coningham.jpg", 0.38),
    ("bombs", "mustard_bombs.jpg", 0.48),
    ("shells", "mustard_shells.jpg", 0.50),
    ("hospital", "allied_hospital.jpg", 0.45),
    ("edgewood", "edgewood_test.jpg", 0.45),
    ("poster", "mustard_poster.jpg", 0.45),
    ("churchill", "churchill_1943.jpg", 0.40),
    ("molecule", "mechlorethamine.jpg", 0.50),
]:
    p = os.path.join(ASSETS_DIR, fname)
    if os.path.exists(p):
        im = Image.open(p).convert("RGB")
        im = ImageEnhance.Contrast(im).enhance(1.08)
        bg = im.resize((W, H), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(42))
        bg = ImageEnhance.Brightness(bg).enhance(0.30)
        vign = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        vd = ImageDraw.Draw(vign)
        for y in range(H):
            if y < 640:
                a = int(225 * (1.0 - (y / 640.0) * 0.45))
            elif y > 1420:
                a = int(235 * ((y - 1420) / (H - 1420.0)))
            else:
                a = 0
            vd.line([(0, y), (W, y)], fill=(13, 13, 13, a))
        backdrop = Image.alpha_composite(bg.convert("RGBA"), vign).convert("RGB")
        steady = backdrop.copy()
        fg = fit_photo_once(im, W, 760, fy=fy_val)
        steady.paste(fg, (0, 660), STAGE_FEATHER_MASK)
        PHOTOS_STEADY_STAGE[key] = steady

SCENE_META = {
    0:   ("ALERTA AÉREA · PUERTO DE BARI", "RADAR DE INTERCEPTACIÓN · 2 DIC 1943", "danger"),
    1:   ("2 DE DICIEMBRE DE 1943", "EL «PEARL HARBOR» EUROPEO EN ITALIA", "amber"),
    2:   ("NOCHE EN EL SUR DE ITALIA", "41°07'N · 16°52'E · COSTA DEL ADRIÁTICO", "tactical"),
    3:   ("105 BOMBARDEROS ALEMANES", "ESCUADRÓN DE JUNKERS JU 88 AL ATAQUE", "danger"),
    301: ("17 BARCOS ALIADOS HUNDIDOS", "EL PUERTO DE BARI ENVUELTO EN LLAMAS", "danger"),
    4:   ("EN LA BODEGA DE UN BUQUE", "ESCANEO RAYOS X · BUQUE SS JOHN HARVEY", "tactical"),
    5:   ("UNA CARGA ULTRASECRETA", "BÓVEDA SELLADA CON PROYECTILES QUÍMICOS", "amber"),
    6:   ("PROHIBIDO PARA LOS MÉDICOS", "NADIE EN EL PUERTO CONOCÍA EL CONTENIDO", "danger"),
    7:   ("PUERTO CLAVE EN ITALIA", "ARTERIA LOGÍSTICA DEL AVANCE ALIADO", "tactical"),
    8:   ("30 BARCOS A PLENA LUZ", "GRÚAS Y REFLECTORES ENCENDIDOS DE NOCHE", "amber"),
    9:   ("MARISCAL ARTHUR CONINGHAM", "«LA AVIACIÓN ALEMANA YA ESTÁ DERROTADA»", "amber"),
    10:  ("19:25 · BENGALAS Y FUEGO", "20 MINUTOS DE BOMBARDEO DEVASTADOR", "danger"),
    11:  ("BUQUE SS JOHN HARVEY", "BLANCO ALCANZADO EN EL PUERTO DE BARI", "danger"),
    12:  ("2.000 BOMBAS DE GAS MOSTAZA", "PROYECTILES QUÍMICOS M47A1 EN LA BODEGA", "danger"),
    13:  ("ORDEN SECRETA DE WASHINGTON", "REPRESALIA POR SI HITLER USABA GAS PRIMERO", "amber"),
    14:  ("UN PROBLEMA MORTAL", "LA TRAMPA DEL SECRETO MILITAR", "danger"),
    15:  ("EXPLOTA EL JOHN HARVEY", "ONDA EXPANSIVA CATASTRÓFICA EN EL PUERTO", "danger"),
    16:  ("MUEREN EN EL ACTO", "TODA LA TRIPULACIÓN DEL BUQUE FALLECE", "danger"),
    17:  ("CERO TESTIGOS VIVOS", "NADIE QUEDA PARA AVISAR QUÉ HABÍA ADENTRO", "danger"),
    18:  ("GAS MOSTAZA Y PETRÓLEO", "TONELADAS DE VENENO MEZCLADAS EN EL AGUA", "amber"),
    19:  ("NADANDO EN ACEITE TÓXICO", "CIENTOS DE MARINEROS BUSCAN SALVARSE", "danger"),
    20:  ("CEGUERA Y QUEMADURAS", "SÍNTOMAS INEXPLICABLES EN LOS HOSPITALES", "danger"),
    21:  ("ALERTA: ERROR MÉDICO", "LA TRAGEDIA SE MULTIPLICA EN LAS SALAS", "danger"),
    22:  ("DIAGNÓSTICO EQUIVOCADO", "LOS MÉDICOS CREEN QUE ES FRÍO Y PETRÓLEO", "amber"),
    23:  ("PROTOCOLO DESCARTADO", "NO LOS LAVAN NI LES QUITAN LOS UNIFORMES", "danger"),
    24:  ("ENVUELTOS EN VENENO", "MANTAS SOBRE UNIFORMES EMPAPADOS EN GAS", "danger"),
    25:  ("EL SECRETO QUE MATA", "FUEGO AMIGO QUÍMICO POR ORDEN DE SILENCIO", "danger"),
    26:  ("MÁS DE 600 MILITARES MUERTOS", "Y CIENTOS DE CIVILES POR LA NUBE TÓXICA", "danger"),
    27:  ("TEMOR A UNA GUERRA QUÍMICA", "EL MANDO ALIADO TEME LA EXCUSA DE HITLER", "amber"),
    28:  ("SILENCIAR EL CASO A TODA COSTA", "CENSURA ABSOLUTA EN LOS INFORMES ALIADOS", "danger"),
    29:  ("DR. STEWART ALEXANDER", "TENIENTE CORONEL MÉDICO ENVIADO A BARI", "tactical"),
    30:  ("INSPECCIÓN EN LAS SALAS", "REVISANDO A LAS VÍCTIMAS EN LOS HOSPITALES", "tactical"),
    31:  ("OLOR A AJO Y GLÓBULOS BLANCOS", "LA PISTA FORENSE QUE REVELÓ EL VENENO", "tactical"),
    32:  ("GAS MOSTAZA EN EL PUERTO", "ALEXANDER RESUELVE EL MISTERIO QUÍMICO", "amber"),
    33:  ("ROMPE EL SILENCIO OFICIAL", "ALEXANDER DESAFÍA LA CENSURA MILITAR", "tactical"),
    34:  ("ORDENA LAVAR A LOS HERIDOS", "DESCONTAMINACIÓN URGENTE Y VIDAS SALVADAS", "tactical"),
    35:  ("CHURCHILL BORRA LOS ARCHIVOS", "CENSURA BRITÁNICA SOBRE EL GAS MOSTAZA", "danger"),
    36:  ("GIRO PARA LA MEDICINA", "EL INFORME DE ALEXANDER CAMBIA LA HISTORIA", "tactical"),
    37:  ("BAJO EL MICROSCOPIO", "ANALIZANDO EL EFECTO CELULAR DEL COMPUESTO", "tactical"),
    38:  ("DESTRUCCIÓN DE GLÓBULOS BLANCOS", "EL COMPUESTO FRENA LAS CÉLULAS RÁPIDAS", "tactical"),
    39:  ("FRENAR EL AVANCE DE TUMORES", "MOSTAZA NITROGENADA CONTRA EL CÁNCER", "tactical"),
    40:  ("LA PRIMERA QUIMIOTERAPIA", "DEL DESASTRE DE BARI A LA ONCOLOGÍA MODERNA", "tactical"),
    41:  ("MATÓ A CIENTOS · SALVÓ A MILLONES", "LA PARADOJA DEL SECRETO MILITAR DE BARI", "amber"),
    42:  ("EN EL LUGAR DEL ALTO MANDO", "EL DILEMA MORAL DEL 2 DE DICIEMBRE DE 1943", "amber"),
    43:  ("OPCIÓN A: REVELAR EL SECRETO", "SALVAR A LOS HERIDOS EN LOS HOSPITALES", "tactical"),
    44:  ("OPCIÓN B: OCULTAR EL GAS", "EVITAR UNA GUERRA QUÍMICA EN EUROPA", "danger"),
    45:  ("¿QUÉ HABRÍAS HECHO VOS?", "CONTÁMELO EN LOS COMENTARIOS", "amber"),
}

VARIANT_COLORS = {
    "neutral": C_NEUTRAL,
    "amber": C_AMBER,
    "danger": C_DANGER,
    "tactical": C_TACTICAL,
}

# ==============================================================================
# VECTOR STORYTELLING & ROSSARK-MOTION-SKILL PRIMITIVES
# ==============================================================================
def draw_hud_brackets(draw, scene_t, col=C_TACTICAL):
    """Kinetic HUD corner brackets & telemetry ticks that spring open on every scene cut."""
    p = min(1.0, spring_val(scene_t, delay_sec=0.0, stiffness=210, damping=16))
    inset = int(28 + (1.0 - p) * 26)
    arm = 34
    y_top, y_bot = 668 + (18 - int(18 * p)), 1422 - (18 - int(18 * p))
    x_left, x_right = inset, W - inset
    for cx, cy, sx, sy in [
        (x_left, y_top, 1, 1),
        (x_right, y_top, -1, 1),
        (x_left, y_bot, 1, -1),
        (x_right, y_bot, -1, -1),
    ]:
        draw.line([(cx, cy), (cx + sx * arm, cy)], fill=col, width=3)
        draw.line([(cx, cy), (cx, cy + sy * arm)], fill=col, width=3)

def draw_rossark_fire(draw, cx, base_y, scale=1.0, global_t=0.0):
    """Rossark 2-layer phase-offset fire recipe (outer flame + inner bright core)."""
    t_ms = global_t * 1000.0
    sway_o = int(9 * scale * wave(t_ms, 850.0, 0.0))
    stretch_o = 1.0 + 0.14 * wave(t_ms, 620.0, 0.25)
    w_o = int(42 * scale)
    h_o = int(78 * scale * stretch_o)
    draw.polygon([
        (cx - w_o, base_y),
        (cx - int(w_o * 0.65) + sway_o // 2, base_y - int(h_o * 0.55)),
        (cx + sway_o, base_y - h_o),
        (cx + int(w_o * 0.65) + sway_o // 2, base_y - int(h_o * 0.55)),
        (cx + w_o, base_y),
    ], fill=C_DANGER, outline=C_AMBER)

    sway_i = int(6 * scale * wave(t_ms, 540.0, 0.37))
    stretch_i = 1.0 + 0.18 * wave(t_ms, 430.0, 0.62)
    w_i = int(24 * scale)
    h_i = int(48 * scale * stretch_i)
    draw.polygon([
        (cx - w_i, base_y - 2),
        (cx + sway_i, base_y - h_i),
        (cx + w_i, base_y - 2),
    ], fill=C_AMBER, outline=C_WHITE)

def draw_ju88_bomber(draw, cx, cy, scale=1.0, global_t=0.0, col_fill=(42, 48, 58), col_stroke=C_NEUTRAL):
    """Animated vector Junkers Ju 88 twin-engine bomber with spinning propellers."""
    t_ms = global_t * 1000.0
    bob = int(4.0 * scale * wave(t_ms, 1400.0, phase=(cx % 100) * 0.01))
    cy_b = cy + bob
    w_wing = int(105 * scale)
    h_fus = int(56 * scale)
    # Swept wings
    draw.polygon([
        (cx - w_wing, cy_b + int(4*scale)),
        (cx - int(22*scale), cy_b - int(14*scale)),
        (cx + int(22*scale), cy_b - int(14*scale)),
        (cx + w_wing, cy_b + int(4*scale)),
        (cx + int(26*scale), cy_b + int(12*scale)),
        (cx - int(26*scale), cy_b + int(12*scale)),
    ], fill=col_fill, outline=col_stroke, width=2)
    # Fuselage + tail fin
    draw.rounded_rectangle([cx - int(12*scale), cy_b - h_fus, cx + int(12*scale), cy_b + int(34*scale)], radius=int(8*scale), fill=col_fill, outline=col_stroke, width=2)
    draw.polygon([
        (cx - int(32*scale), cy_b - h_fus + int(8*scale)),
        (cx + int(32*scale), cy_b - h_fus + int(8*scale)),
        (cx, cy_b - h_fus - int(6*scale)),
    ], fill=col_fill, outline=col_stroke, width=2)
    # Glass greenhouse nose canopy
    draw.ellipse([cx - int(9*scale), cy_b + int(18*scale), cx + int(9*scale), cy_b + int(38*scale)], fill=C_TACTICAL, outline=C_WHITE, width=2)
    # Twin engine nacelles + spinning propeller discs
    prop_r = int(15 * scale)
    ang = (global_t * 920.0) % 360.0
    for side in (-1, 1):
        ex = cx + side * int(42 * scale)
        ey = cy_b + int(10 * scale)
        draw.rounded_rectangle([ex - int(8*scale), ey - int(18*scale), ex + int(8*scale), ey + int(12*scale)], radius=4, fill=(28, 32, 38), outline=C_AMBER, width=2)
        draw.ellipse([ex - prop_r, ey + int(8*scale) - 4, ex + prop_r, ey + int(8*scale) + 4], outline=C_WHITE, width=2)
        px_blade = int(prop_r * math.cos(math.radians(ang)))
        draw.line([(ex - px_blade, ey + int(8*scale)), (ex + px_blade, ey + int(8*scale))], fill=C_AMBER, width=3)

def draw_chronometer_watch(draw, cx, cy, radius, global_t, target_hour=19, target_min=25):
    """Animated WWII military chronometer with rotating internal gears, ticks, and sweeping hands."""
    # Outer brass/steel bezel + crown
    draw.rectangle([cx - 22, cy - radius - 34, cx + 22, cy - radius - 6], fill=C_AMBER, outline=C_WHITE, width=3)
    draw.ellipse([cx - radius - 26, cy - radius - 56, cx + radius - 66, cy - radius - 16], outline=C_AMBER, width=4)
    draw.ellipse([cx - radius - 10, cy - radius - 10, cx + radius + 10, cy + radius + 10], fill=(28, 32, 40), outline=C_AMBER, width=5)
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=(16, 20, 28), outline=(90, 100, 118), width=2)

    # Rotating internal brass gear wheel
    g_rad = int(radius * 0.48)
    g_ang = global_t * 55.0
    gx, gy = cx - int(radius * 0.22), cy + int(radius * 0.18)
    draw.ellipse([gx - g_rad, gy - g_rad, gx + g_rad, gy + g_rad], outline=(120, 95, 38), width=3)
    for ti in range(8):
        a = math.radians(g_ang + ti * 45)
        draw.line([(gx + int(g_rad*0.7*math.cos(a)), gy + int(g_rad*0.7*math.sin(a))),
                   (gx + int((g_rad+9)*math.cos(a)), gy + int((g_rad+9)*math.sin(a)))], fill=C_AMBER, width=4)

    # 12 Hour ticks
    for hi in range(12):
        a = math.radians(hi * 30 - 90)
        r_in = radius - (22 if hi % 3 == 0 else 14)
        r_out = radius - 6
        draw.line([
            (cx + int(r_in * math.cos(a)), cy + int(r_in * math.sin(a))),
            (cx + int(r_out * math.cos(a)), cy + int(r_out * math.sin(a))),
        ], fill=C_WHITE if hi % 3 == 0 else (140, 148, 160), width=4 if hi % 3 == 0 else 2)

    # Hour hand, minute hand, and fast-sweeping red second hand
    h_ang = math.radians(((target_hour % 12) + target_min / 60.0) * 30 - 90)
    m_ang = math.radians(target_min * 6 - 90 + 12 * math.sin(global_t * 2.5))
    s_ang = math.radians((global_t * 180.0) % 360.0 - 90)
    draw.line([(cx, cy), (cx + int(radius * 0.50 * math.cos(h_ang)), cy + int(radius * 0.50 * math.sin(h_ang)))], fill=C_WHITE, width=7)
    draw.line([(cx, cy), (cx + int(radius * 0.72 * math.cos(m_ang)), cy + int(radius * 0.72 * math.sin(m_ang)))], fill=C_AMBER, width=5)
    draw.line([(cx, cy), (cx + int(radius * 0.82 * math.cos(s_ang)), cy + int(radius * 0.82 * math.sin(s_ang)))], fill=C_DANGER, width=3)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=C_DANGER, outline=C_WHITE, width=2)

def draw_split_flap_row(draw, cx, cy, items, scene_t):
    """Animated mechanical split-flap cards that flip and lock into place."""
    gap = 18
    widths = [max(130, int(FONT_BIG_NUM.getlength(txt)) + 48) for txt, _ in items]
    total_w = sum(widths) + gap * (len(items) - 1)
    cur_x = cx - total_w // 2
    for idx, ((txt, col), w_box) in enumerate(zip(items, widths)):
        sp = min(1.0, spring_val(scene_t, delay_sec=idx * 0.10, stiffness=220, damping=14))
        h_box = max(24, int(104 * sp))
        y0 = cy - h_box // 2
        draw.rounded_rectangle([cur_x, y0, cur_x + w_box, y0 + h_box], radius=10, fill=(18, 20, 26), outline=col, width=4)
        draw.line([(cur_x + 6, cy), (cur_x + w_box - 6, cy)], fill=(45, 50, 62), width=2)
        if sp > 0.35:
            draw.text((cur_x + w_box // 2, cy - 2), txt, font=FONT_BIG_NUM, fill=col, anchor="mm")
        cur_x += w_box + gap

def draw_radar_scope(draw, cx, cy, radius, global_t, col=C_HEAL, blips=()):
    """Animated 360° rotating radar sweep with concentric range rings and target blips."""
    draw.ellipse([cx - radius - 8, cy - radius - 8, cx + radius + 8, cy + radius + 8], fill=(10, 18, 24), outline=col, width=4)
    for r_f in (0.33, 0.66, 1.0):
        rr = int(radius * r_f)
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(28, 62, 58), width=2)
    draw.line([(cx - radius, cy), (cx + radius, cy)], fill=(28, 62, 58), width=2)
    draw.line([(cx, cy - radius), (cx, cy + radius)], fill=(28, 62, 58), width=2)

    sweep_deg = (global_t * 165.0) % 360.0
    draw.pieslice([cx - radius, cy - radius, cx + radius, cy + radius], start=sweep_deg - 38, end=sweep_deg, fill=(24, 92, 68))
    s_rad = math.radians(sweep_deg)
    draw.line([(cx, cy), (cx + int(radius * math.cos(s_rad)), cy + int(radius * math.sin(s_rad)))], fill=col, width=4)

    for bx_off, by_off, b_col in blips:
        bx, by = cx + bx_off, cy + by_off
        pulse = int(6 + 5 * abs(math.sin(global_t * 8.0 + bx_off * 0.05)))
        draw.ellipse([bx - pulse, by - pulse, bx + pulse, by + pulse], fill=b_col, outline=C_WHITE, width=2)
def draw_attribution_pill(draw, text):
    if not text:
        return
    tw = int(FONT_ATTR.getlength(text))
    draw.rounded_rectangle([40, 1445, 40 + tw + 24, 1479], radius=5, fill=(10, 12, 16), outline=(55, 60, 70), width=1)
    draw.text((52, 1462), text, font=FONT_ATTR, fill=(215, 220, 228), anchor="lm")

def draw_map_pill(draw, cx, cy, label, dot_col=C_DANGER):
    tw = int(FONT_PILL_SM.getlength(label))
    pw, ph = tw + 46, 38
    x0, y0 = cx - pw // 2, cy - ph // 2
    draw.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=8, fill=(24, 24, 27), outline=(85, 92, 105), width=2)
    draw.ellipse([x0 + 12, cy - 6, x0 + 24, cy + 6], fill=dot_col)
    draw.text((x0 + 32, cy), label, font=FONT_PILL_SM, fill=C_WHITE, anchor="lm")

def draw_digital_led_box(draw, cx, cy, text, col=C_DANGER):
    tw = int(FONT_BIG_NUM.getlength(text))
    pw, ph = tw + 64, 108
    x0, y0 = cx - pw // 2, cy - ph // 2
    draw.rectangle([x0, y0, x0 + pw, y0 + ph], fill=(18, 16, 18), outline=col, width=4)
    draw.text((cx, cy - 2), text, font=FONT_BIG_NUM, fill=col, anchor="mm")

def draw_rossark_water_surface(draw, y_surf, global_t, col=C_TACTICAL, n_ripples=3):
    t_ms = global_t * 1000.0
    pts = []
    for i, x in enumerate(range(0, W + 30, 30)):
        wy = y_surf + 6.5 * wave(t_ms, 2600.0, phase=i * 0.09) + 2.5 * wave(t_ms, 1400.0, phase=i * 0.17)
        pts.append((x, int(wy)))
    draw.line(pts, fill=col, width=4)
    pts2 = [(x, int(y + 16 + 3.0 * wave(t_ms, 3400.0, phase=i * 0.07 + 0.3))) for i, (x, y) in enumerate(pts)]
    draw.line(pts2, fill=(45, 95, 165), width=2)
    for r_i in range(n_ripples):
        p = loop_p(t_ms, 2800.0, phase=seeded(r_i, 11))
        b = bell(p)
        if b > 0.15:
            rx = int(220 + seeded(r_i, 22) * (W - 440))
            rw = int(28 + 95 * p)
            rh = max(4, int(rw * 0.22))
            draw.ellipse([rx - rw, y_surf - rh + 4, rx + rw, y_surf + rh + 4], outline=col, width=max(1, int(3 * b)))

def draw_rossark_smoke_wisps(frame, cx, base_y, global_t, count=5, col=(210, 195, 55), spread=180):
    t_ms = global_t * 1000.0
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(count):
        p = loop_p(t_ms, 2300.0 + seeded(i, 1) * 800.0, phase=seeded(i, 2))
        alpha = int(175 * bell(p))
        if alpha <= 8:
            continue
        wx = cx + int((seeded(i, 3) - 0.5) * spread + 16.0 * wave(t_ms, 1900.0, seeded(i, 4)))
        wy = base_y - int(p * 145)
        r = int(16 + p * 28)
        od.ellipse([wx - r, wy - int(r * 0.68), wx + r, wy + int(r * 0.68)], fill=col + (alpha,))
    frame.paste(overlay, (0, 0), overlay)

def draw_rossark_jiggle_button(draw, cx, cy, bw, bh, text, fill_col, outline_col, global_t, phase_offset=0.0):
    t_ms = global_t * 1000.0
    beat = wave(t_ms, 540.0, phase=phase_offset)
    squash = 1.0 + 0.022 * abs(beat)
    sy = 1.0 / (squash ** 0.6)
    bulge_x = int(bw * 0.012 * beat)
    w_cur = int(bw * squash)
    h_cur = int(bh * sy)
    x0 = cx - w_cur // 2 + bulge_x
    y0 = cy - h_cur // 2
    draw.rounded_rectangle([x0, y0, x0 + w_cur, y0 + h_cur], radius=10, fill=fill_col, outline=outline_col, width=4)
    draw.text((cx + bulge_x, cy), text, font=FONT_PILL_LG, fill=C_WHITE, anchor="mm")

def draw_vector_hand(draw, hx, hy, angle_deg=-25, sleeve_col=(72, 82, 54)):
    hand_img = Image.new("RGBA", (260, 320), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hand_img)
    skin = (218, 178, 146, 255)
    skin_dark = (188, 146, 114, 255)
    for fx, fy, fw, fh in [(78, 35, 22, 75), (104, 24, 22, 85), (130, 28, 22, 80), (156, 42, 20, 68)]:
        hd.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=10, fill=skin, outline=skin_dark, width=2)
    hd.polygon([(50, 95), (78, 82), (90, 125), (58, 132)], fill=skin, outline=skin_dark)
    hd.rounded_rectangle([72, 88, 178, 178], radius=22, fill=skin, outline=skin_dark, width=2)
    hd.polygon([(62, 172), (188, 172), (210, 315), (40, 315)], fill=sleeve_col + (255,))
    hd.line([(60, 196), (190, 196)], fill=C_AMBER + (255,), width=8)
    rot = hand_img.rotate(angle_deg, resample=Image.Resampling.BICUBIC, expand=True)
    return rot, hx - rot.width // 2, hy - rot.height // 3

def draw_barrier_gate(draw, y_bar, angle_deg=0.0):
    post_x = 120
    draw.rounded_rectangle([post_x - 24, y_bar - 40, post_x + 24, y_bar + 220], radius=6, fill=(45, 48, 56), outline=(110, 116, 128), width=3)
    bar_img = Image.new("RGBA", (880, 64), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bar_img)
    for sx in range(0, 860, 72):
        bd.rectangle([sx, 8, sx + 36, 52], fill=C_STAMP_RED + (255,))
        bd.rectangle([sx + 36, 8, sx + 72, 52], fill=C_WHITE + (255,))
    bd.rectangle([0, 8, 864, 52], outline=(30, 30, 34, 255), width=3)
    rot = bar_img.rotate(angle_deg, resample=Image.Resampling.BICUBIC, expand=True)
    return rot, post_x, int(y_bar - rot.height // 2)

def draw_crosshair(draw, cx, cy, rad, col=C_DANGER):
    draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=col, width=4)
    draw.ellipse([cx - int(rad*0.6), cy - int(rad*0.6), cx + int(rad*0.6), cy + int(rad*0.6)], outline=col, width=2)
    draw.line([(cx - rad - 35, cy), (cx + rad + 35, cy)], fill=col, width=4)
    draw.line([(cx, cy - rad - 35), (cx, cy + rad + 35)], fill=col, width=4)

def draw_chemical_symbol(draw, cx, cy, radius, angle_deg=0.0, col=C_AMBER):
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=(24, 22, 14), outline=col, width=3)
    for b in range(3):
        a = math.radians(angle_deg + b * 120 - 90)
        bx = cx + int(radius * 0.46 * math.cos(a))
        by = cy + int(radius * 0.46 * math.sin(a))
        r_ring = int(radius * 0.36)
        draw.ellipse([bx - r_ring, by - r_ring, bx + r_ring, by + r_ring], outline=col, width=4)
    draw.ellipse([cx - int(radius*0.22), cy - int(radius*0.22), cx + int(radius*0.22), cy + int(radius*0.22)], fill=col)

def draw_liberty_ship(draw, cx, cy, scale=1.0, body_col=(52, 62, 76), stroke_col=C_NEUTRAL, global_t=0.0, show_xray=False):
    """Rossark floating vehicle recipe: bobs 1-2 units and rocks ±2°."""
    t_ms = global_t * 1000.0
    bob = int(3.0 * wave(t_ms, 2600.0))
    cy_b = cy + bob
    w_half = int(250 * scale)
    h_hull = int(48 * scale)
    # Bridge superstructure + smokestack
    draw.rounded_rectangle([cx - int(65*scale), cy_b - h_hull - int(56*scale), cx + int(55*scale), cy_b - h_hull + 6], radius=6, fill=body_col, outline=stroke_col, width=3)
    draw.rectangle([cx - int(18*scale), cy_b - h_hull - int(92*scale), cx + int(12*scale), cy_b - h_hull - int(52*scale)], fill=(38, 42, 48), outline=C_AMBER, width=2)
    # Cargo masts
    for mx in [cx - int(145*scale), cx + int(135*scale)]:
        draw.line([(mx, cy_b - h_hull - int(85*scale)), (mx, cy_b - h_hull)], fill=stroke_col, width=4)
    # Ship Hull
    draw.polygon([
        (cx - w_half - int(28*scale), cy_b - h_hull),
        (cx + w_half + int(34*scale), cy_b - h_hull),
        (cx + w_half, cy_b + h_hull),
        (cx - w_half, cy_b + h_hull),
    ], fill=body_col, outline=stroke_col, width=3)
    if show_xray:
        # Glowing X-ray cargo hold inside the ship showing secret mustard gas bombs
        draw.rounded_rectangle([cx - int(165*scale), cy_b - h_hull + 10, cx + int(165*scale), cy_b + h_hull - 8], radius=8, fill=(56, 20, 18), outline=C_DANGER, width=3)
        for bi in range(-2, 3):
            bx = cx + int(bi * 58 * scale)
            draw.rounded_rectangle([bx - 18, cy_b - 14, bx + 18, cy_b + 22], radius=6, fill=C_AMBER, outline=C_WHITE, width=2)

def draw_rossark_character(
    frame, cx, cy, scale=1.35, role="alexander", global_t=0.0, scene_t=0.0,
    talking=False, mood="focused", gesture="rest"
):
    """
    2.5D Living Historical Character built with rossark-motion-skill architecture:
      roles: 'alexander' (US Army Medical Lt. Col.), 'coningham' (RAF Air Marshal),
             'port_doctor' (White coat + Red Cross), 'sailor_victim' (Blinded oiled sailor),
             'churchill' (British PM dark suit + bow tie)
    """
    t_ms = (global_t * 1000.0) % 7200.0
    s_ms = scene_t * 1000.0
    canvas_sz = 460
    rig = Image.new("RGBA", (canvas_sz, canvas_sz), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rig)
    ox, oy = canvas_sz // 2, 210

    if role == "coningham":
        suit_col = (46, 68, 96, 255)      # RAF Blue-Grey
        suit_shade = (34, 50, 74, 255)
        cap_top = (42, 62, 88, 255)
        badge_col = C_AMBER + (255,)
        phase_seed = 0.12
    elif role == "port_doctor":
        suit_col = (236, 240, 245, 255)   # White medical coat
        suit_shade = (195, 204, 214, 255)
        cap_top = (240, 244, 248, 255)
        badge_col = C_DANGER + (255,)     # Red Cross badge
        phase_seed = 0.35
    elif role == "sailor_victim":
        suit_col = (28, 32, 38, 255)      # Oil-soaked dark uniform
        suit_shade = (48, 44, 24, 255)
        cap_top = (240, 236, 226, 255)    # Bandage / sailor cap
        badge_col = C_TOXIC + (255,)
        phase_seed = 0.58
    elif role == "churchill":
        suit_col = (26, 28, 34, 255)      # Dark pinstripe suit
        suit_shade = (44, 48, 56, 255)
        cap_top = (30, 32, 38, 255)       # Homburg hat
        badge_col = C_DANGER + (255,)
        phase_seed = 0.77
    else:  # alexander (US Army Medical Corps Lt. Col. Stewart Alexander)
        suit_col = (68, 78, 48, 255)      # Olive Drab Officer Uniform
        suit_shade = (52, 60, 36, 255)
        cap_top = (74, 84, 52, 255)
        badge_col = C_HEAL + (255,)
        phase_seed = 0.22

    skin_col = (242, 185, 148, 255)
    feature_col = (210, 126, 88, 255)
    hair_col = (72, 48, 34, 255)

    lean_keys = [(0, 0.0), (1800, -2.5), (3600, 2.0), (5400, -1.5), (7200, 0.0)]
    yaw_keys = [(0, -0.15), (2100, 0.22), (4200, 0.18), (5800, -0.18), (7200, -0.15)]
    head_keys = [(0, 0.0), (2000, 3.5), (4100, -3.0), (5900, 2.0), (7200, 0.0)]

    lean = flow(t_ms, lean_keys) + 1.4 * wave(t_ms, 4200.0, phase_seed)
    yaw = flow(t_ms, yaw_keys) + 0.06 * wave(t_ms, 3100.0, phase_seed + 0.2)
    head_tilt = flow(t_ms, head_keys) - 0.45 * flow(max(0.0, t_ms - 110.0), lean_keys) + 1.8 * wave(t_ms, 4600.0, phase_seed + 0.5)

    sy = 1.0 + 0.016 * wave(t_ms, 2600.0, phase_seed)
    sx = 1.0 / (sy ** 0.6)
    lift = 2.5 * wave(t_ms, 2600.0, phase_seed + 0.25)

    if gesture == "stop_hand":
        arm_ra_keys = [(0, 20.0), (400, 58.0), (1200, 62.0), (7200, 60.0)]
        arm_re_keys = [(0, 10.0), (400, 108.0), (1200, 112.0), (7200, 110.0)]
    elif gesture == "dismiss":
        arm_ra_keys = [(0, 35.0), (500, 65.0), (1000, 45.0), (1500, 68.0), (7200, 50.0)]
        arm_re_keys = [(0, 40.0), (500, 85.0), (1000, 60.0), (1500, 88.0), (7200, 65.0)]
    else:
        arm_ra_keys = [(0, 22.0), (2400, 30.0), (4800, 18.0), (7200, 22.0)]
        arm_re_keys = [(0, 18.0), (2400, 32.0), (4800, 14.0), (7200, 18.0)]

    t_gesture = min(7199.0, s_ms)
    ra_base = flow(t_gesture, arm_ra_keys) + 3.5 * wave(t_ms, 3000.0, phase_seed)
    ra_prev = flow(max(0.0, t_gesture - 90.0), arm_ra_keys)
    re_base = flow(t_gesture, arm_re_keys) + 4.5 * wave(t_ms, 2250.0, phase_seed + 0.4) + 0.45 * (ra_prev - flow(t_gesture, arm_ra_keys))

    la_base = 24.0 + 3.5 * wave(t_ms, 3200.0, phase_seed + 0.5)
    le_base = -18.0 + 4.0 * wave(t_ms, 2400.0, phase_seed + 0.8)

    bx = ox + int(lean * 1.4)
    by = oy - int(lift)

    def draw_arm(side, a_deg, e_deg):
        a_rad = math.radians(a_deg)
        f_rad = math.radians(a_deg + e_deg)
        sh_x = bx + int(side * 42 * sx)
        sh_y = by + int(64 * sy)
        el_x = sh_x + int(side * math.sin(a_rad) * 38)
        el_y = sh_y + int(math.cos(a_rad) * 38)
        ha_x = el_x + int(side * math.sin(f_rad) * 36)
        ha_y = el_y + int(math.cos(f_rad) * 36)
        rd.line([(sh_x, sh_y), (el_x, el_y), (ha_x, ha_y)], fill=suit_col, width=26, joint="curve")
        rd.ellipse([ha_x - 14, ha_y - 14, ha_x + 14, ha_y + 14], fill=skin_col, outline=feature_col, width=2)

    draw_arm(-1, la_base, le_base)

    t_top = by + int(48 * sy)
    t_bot = by + int(138 * sy)
    sh_w = int(52 * sx)
    wa_w = int(44 * sx)
    rd.polygon([
        (bx - sh_w, t_top), (bx + sh_w, t_top),
        (bx + wa_w, t_bot), (bx - wa_w, t_bot)
    ], fill=suit_col, outline=suit_shade)
    yaw_px = int(8 * yaw)
    rd.polygon([(bx - 16 + yaw_px, t_top), (bx + 16 + yaw_px, t_top), (bx + yaw_px, t_top + 26)], fill=C_WHITE + (255,))
    if role == "port_doctor":
        # Red Cross on medical coat chest
        cx_rc, cy_rc = bx + 20 + yaw_px, t_top + 48
        rd.rectangle([cx_rc - 12, cy_rc - 4, cx_rc + 12, cy_rc + 4], fill=C_DANGER + (255,))
        rd.rectangle([cx_rc - 4, cy_rc - 12, cx_rc + 4, cy_rc + 12], fill=C_DANGER + (255,))
    else:
        for b_row in [t_top + 36, t_top + 60, t_top + 82]:
            rd.ellipse([bx + yaw_px - 4, b_row - 4, bx + yaw_px + 4, b_row + 4], fill=C_AMBER + (255,))

    head_layer = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_layer)
    hcx, hcy = 120, 130

    ear_dx = int(-9 * yaw)
    for side in [-1, 1]:
        ex = hcx + side * 50 + ear_dx
        hd.ellipse([ex - 11, hcy - 10, ex + 11, hcy + 12], fill=skin_col, outline=feature_col, width=2)

    hd.rounded_rectangle([hcx - 50, hcy - 64, hcx + 50, hcy + 52], radius=28, fill=skin_col, outline=feature_col, width=2)

    blinks = make_blink_keys(7200.0, [1400.0, 4100.0, 6200.0])
    lid_val = track(t_ms, blinks)
    if mood == "blinded":
        lid_val = 0.92
    elif mood == "tired":
        lid_val = max(0.38, lid_val)
    elif mood == "focused":
        lid_val = max(0.08, lid_val)

    face_dx = int(10 * yaw)
    look_x = int(4 * yaw + 3.0 * wave(t_ms, 3400.0, phase_seed))
    look_y = int(1.5 * wave(t_ms, 2800.0, phase_seed + 0.3))

    for side in [-1, 1]:
        ecx = hcx + side * 20 + face_dx
        ecy = hcy - 8
        ew, eh = 24, 30
        hd.rounded_rectangle([ecx - ew // 2, ecy - eh // 2, ecx + ew // 2, ecy + eh // 2], radius=11, fill=C_WHITE + (255,))
        px = ecx + look_x
        py = ecy + look_y
        hd.rounded_rectangle([px - 6, py - 8, px + 6, py + 8], radius=5, fill=(38, 38, 42, 255))
        hd.ellipse([px - 4, py - 6, px - 1, py - 3], fill=C_WHITE + (255,))
        if lid_val > 0.02:
            lid_h = int((eh + 4) * lid_val)
            hd.rounded_rectangle([ecx - ew // 2 - 2, ecy - eh // 2 - 2, ecx + ew // 2 + 2, ecy - eh // 2 - 2 + lid_h], radius=8, fill=skin_col)
            hd.line([(ecx - ew // 2 - 1, ecy - eh // 2 - 2 + lid_h), (ecx + ew // 2 + 1, ecy - eh // 2 - 2 + lid_h)], fill=feature_col, width=3)
        brow_y = ecy - eh // 2 - 6
        if mood == "smug":
            hd.line([(ecx - 12, brow_y - (4 if side > 0 else 0)), (ecx + 12, brow_y - (6 if side > 0 else 1))], fill=hair_col, width=5)
        elif mood in ("tired", "blinded"):
            hd.line([(ecx - 12, brow_y + side * 3), (ecx + 12, brow_y - side * 2)], fill=hair_col, width=4)
        else:
            hd.line([(ecx - 12, brow_y), (ecx + 12, brow_y - 2)], fill=hair_col, width=5)

    nx = hcx + int(13 * yaw)
    hd.rounded_rectangle([nx - 5, hcy - 4, nx + 5, hcy + 14], radius=4, fill=feature_col)

    mx = hcx + face_dx
    my = hcy + 26
    if talking:
        m_depth = int(6 + 10 * abs(wave(t_ms, 340.0, phase_seed)))
        hd.polygon([(mx - 14, my), (mx + 14, my), (mx + 10, my + m_depth), (mx - 10, my + m_depth)], fill=(155, 42, 42, 255))
        hd.line([(mx - 11, my + 2), (mx + 11, my + 2)], fill=C_WHITE + (255,), width=3)
    else:
        hd.arc([mx - 12, my - 4, mx + 12, my + 8], start=15 if mood != "blinded" else 195, end=165 if mood != "blinded" else 345, fill=feature_col, width=4)

    # Headgear / Cap
    hd.polygon([
        (hcx - 58, hcy - 46), (hcx + 58, hcy - 46),
        (hcx + 68, hcy - 76), (hcx, hcy - 88), (hcx - 68, hcy - 76)
    ], fill=cap_top, outline=suit_shade)
    hd.rectangle([hcx - 52, hcy - 52, hcx + 52, hcy - 38], fill=(24, 26, 30, 255), outline=C_AMBER + (255,), width=2)
    hd.ellipse([hcx + int(6 * yaw) - 9, hcy - 68, hcx + int(6 * yaw) + 9, hcy - 50], fill=badge_col, outline=C_WHITE + (255,), width=2)

    head_rot = head_layer.rotate(-head_tilt, resample=Image.Resampling.BICUBIC, expand=False)
    rig.paste(head_rot, (bx - hcx, by - hcy), head_rot)

    draw_arm(1, ra_base, re_base)

    if scale != 1.0:
        new_sz = max(40, int(canvas_sz * scale))
        rig = rig.resize((new_sz, new_sz), Image.Resampling.LANCZOS)
    frame.paste(rig, (cx - rig.width // 2, cy - rig.height // 2), rig)

# Module A: Steady Archival Photo + Dynamic Vector Motion Overlays (0.0px image jitter!)
def render_module_a_steady(photo_key, scene_t, scene_dur, date_ribbon, caption_pill, attribution, extra_vector_fn=None):
    frame = PHOTOS_STEADY_STAGE.get(photo_key, CANVAS_ABYSS).copy()
    draw = ImageDraw.Draw(frame)
    if extra_vector_fn:
        extra_vector_fn(frame, draw, scene_t, scene_dur)
    if date_ribbon:
        n_chars = int(min(len(date_ribbon), max(1, (scene_t / 0.80) * len(date_ribbon))))
        typed_str = date_ribbon[:n_chars]
        tw = int(FONT_RIBBON.getlength(typed_str))
        draw.rectangle([54, 696, 54 + tw + 36, 744], fill=(0, 0, 0))
        draw.rectangle([48, 690, 48 + tw + 36, 738], fill=C_PAPER)
        draw.rectangle([48, 690, 54, 738], fill=C_STAMP_RED)
        draw.text((66, 714), typed_str, font=FONT_RIBBON, fill=C_INK, anchor="lm")
    if caption_pill:
        enter_s = spring_val(scene_t, delay_sec=0.12)
        tw = int(FONT_PILL_MD.getlength(caption_pill))
        pw = tw + 48
        px0 = (W - pw) // 2
        py0 = int(1345 + (1.0 - min(1.0, enter_s)) * 24)
        draw.rounded_rectangle([px0, py0, px0 + pw, py0 + 50], radius=8, fill=(15, 17, 21), outline=(95, 102, 115), width=2)
        draw.text((W // 2, py0 + 25), caption_pill, font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
    draw_attribution_pill(draw, attribution)
    return frame

# Module C: Reconstructed Document + Animated Vector Hand Writing/Underlining + Slamming Stamp!
def render_module_c_document_with_hand(scene_t, header, meta_line, lines, highlight_idx, stamp_text, source_attr, tilt_deg=-1.5, redact_line=None):
    frame = CANVAS_ABYSS.copy()
    doc_w, doc_h = 860, 640
    doc = Image.new("RGBA", (doc_w + 40, doc_h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(doc)
    d.rounded_rectangle([24, 28, doc_w + 24, doc_h + 28], radius=8, fill=(0, 0, 0, 185))
    d.rounded_rectangle([10, 10, doc_w + 10, doc_h + 10], radius=6, fill=(244, 239, 230, 255), outline=(213, 206, 192, 255), width=2)
    d.text((58, 52), header, font=FONT_DOC_HDR, fill=(75, 72, 66, 255))
    d.line([(58, 86), (doc_w - 38, 86)], fill=(213, 206, 192, 255), width=2)
    d.text((58, 106), meta_line, font=FONT_DOC_META, fill=(26, 25, 23, 255))

    underline_prog = min(1.0, max(0.0, (scene_t - 0.15) / 1.15))
    y_cur = 162
    pen_tip_x, pen_tip_y = 420, 320
    for idx, line in enumerate(lines):
        is_hl = (idx in highlight_idx) if isinstance(highlight_idx, (set, list, tuple)) else (idx == highlight_idx)
        if is_hl and underline_prog > 0:
            lw = int(FONT_DOC_BOLD.getlength(line))
            hw = int(lw * underline_prog)
            d.rectangle([54, y_cur + 2, 54 + hw + 8, y_cur + 36], fill=(238, 196, 186, 255))
            d.rectangle([54, y_cur + 33, 54 + hw + 8, y_cur + 37], fill=(214, 54, 41, 255))
            pen_tip_x = 54 + hw
            pen_tip_y = y_cur + 35
        d.text((58, y_cur), line, font=FONT_DOC_BOLD if is_hl else FONT_DOC_LINE, fill=(26, 25, 23, 255))
        if redact_line is not None and idx == redact_line and underline_prog > 0.2:
            lw = int(FONT_DOC_BOLD.getlength(line))
            rw = int(lw * min(1.0, (underline_prog - 0.2) / 0.7))
            d.rectangle([54, y_cur - 2, 54 + rw, y_cur + 32], fill=(18, 18, 20, 255))
        y_cur += 52

    d.line([(58, doc_h - 58), (doc_w - 38, doc_h - 58)], fill=(223, 216, 200, 255), width=1)
    d.text((58, doc_h - 36), "RECONSTRUCCIÓN · TEXTO DE EJEMPLO", font=FONT_FOOTER, fill=(113, 113, 122, 255))

    if stamp_text and scene_t >= 0.55:
        sp = spring_val(scene_t, delay_sec=0.55, stiffness=220, damping=12)
        stw = int(FONT_STAMP.getlength(stamp_text)) + 44
        sth = 64
        stamp_img = Image.new("RGBA", (stw + 20, sth + 20), (0, 0, 0, 0))
        sd = ImageDraw.Draw(stamp_img)
        sd.rectangle([6, 6, stw + 6, sth + 6], outline=(214, 54, 41, 235), width=4)
        sd.rectangle([12, 12, stw, sth], outline=(214, 54, 41, 235), width=2)
        sd.text((6 + stw // 2, 6 + sth // 2), stamp_text, font=FONT_STAMP, fill=(214, 54, 41, 235), anchor="mm")
        s_factor = max(0.85, 1.65 - 0.65 * min(1.0, sp))
        stamp_rot = stamp_img.rotate(8, resample=Image.Resampling.BICUBIC, expand=True)
        sw_new, sh_new = max(10, int(stamp_rot.width * s_factor)), max(10, int(stamp_rot.height * s_factor))
        stamp_rot = stamp_rot.resize((sw_new, sh_new), Image.Resampling.LANCZOS)
        doc.paste(stamp_rot, (doc_w - sw_new - 25, doc_h - sh_new - 65), stamp_rot)

    rotated = doc.rotate(tilt_deg, resample=Image.Resampling.BICUBIC, expand=True)
    doc_x = (W - rotated.width) // 2
    doc_y = 685 + (680 - rotated.height) // 2
    frame.paste(rotated, (doc_x, doc_y), rotated)

    draw = ImageDraw.Draw(frame)
    hand_rot, hx, hy = draw_vector_hand(draw, doc_x + pen_tip_x + 30, doc_y + pen_tip_y + 70, angle_deg=-22)
    frame.paste(hand_rot, (hx, hy), hand_rot)
    draw_attribution_pill(draw, source_attr)
    return frame

def draw_italy_geography(draw):
    # Boot of Southern Italy + Sicily + Balkan coast across Adriatic Sea
    italy_boot = [
        (190, 680), (350, 680), (490, 820), (665, 960), (765, 1045),
        (725, 1085), (630, 1020), (585, 1065), (635, 1185), (565, 1265),
        (495, 1210), (470, 1085), (355, 945), (210, 825)
    ]
    sicily = [(350, 1260), (505, 1255), (485, 1345), (365, 1320)]
    balkans = [(780, 680), (1080, 680), (1080, 1020), (920, 890), (810, 760)]
    for poly in [italy_boot, sicily, balkans]:
        draw.polygon(poly, fill=C_LAND_FILL, outline=C_LAND_STROKE, width=2)

def draw_balance_scale(draw, cx, base_y, tilt_deg, left_pills, right_pills, left_title, right_title, left_col=C_DANGER, right_col=C_HEAL, drop_prog=1.0):
    gold_m, gold_l = (218, 172, 54), (245, 208, 96)
    draw.ellipse([cx - 165, base_y - 34, cx + 165, base_y + 16], fill=gold_m, outline=gold_l, width=2)
    draw.rectangle([cx - 13, base_y - 510, cx + 13, base_y - 10], fill=gold_m)
    rad = math.radians(tilt_deg)
    arm = 320
    lx, ly = int(cx - arm * math.cos(rad)), int((base_y - 495) + arm * math.sin(rad))
    rx, ry = int(cx + arm * math.cos(rad)), int((base_y - 495) - arm * math.sin(rad))
    draw.line([(lx, ly), (rx, ry)], fill=gold_l, width=11)
    draw.ellipse([cx - 18, base_y - 513, cx + 18, base_y - 477], fill=gold_l)
    for px, py, pills, title, col in [(lx, ly, left_pills, left_title, left_col), (rx, ry, right_pills, right_title, right_col)]:
        pan_y = py + 205
        draw.line([(px, py), (px - 110, pan_y)], fill=gold_l, width=3)
        draw.line([(px, py), (px + 110, pan_y)], fill=gold_l, width=3)
        draw.pieslice([px - 125, pan_y - 26, px + 125, pan_y + 26], start=0, end=180, fill=gold_m, outline=gold_l, width=3)
        draw.text((px, pan_y + 62), title, font=FONT_PILL_LG, fill=col, anchor="mm")
        for i, ptxt in enumerate(pills):
            p_enter = min(1.0, max(0.0, drop_prog * len(pills) - i))
            if p_enter > 0:
                iy = int(pan_y - 30 - i * 50 - (1.0 - p_enter) * 60)
                tw = int(FONT_PILL_SM.getlength(ptxt)) + 32
                draw.rounded_rectangle([px - tw//2, iy - 20, px + tw//2, iy + 20], radius=8, fill=C_PAPER, outline=gold_m, width=2)
                draw.text((px, iy), ptxt, font=FONT_PILL_SM, fill=C_INK, anchor="mm")

# ==============================================================================
# MASTER STAGE DISPATCHER (47 Distinct Scenes with Bespoke Vector Motion & Rossark)
# ==============================================================================
def render_stage_for_scene(scene_id, scene_t, scene_dur, global_t):
    s_prog = min(1.0, max(0.0, scene_t / max(0.1, scene_dur)))

    if scene_id == 0:
        # S00 (0.00s - 1.65s Cold Open): WWII Air-Raid Radar Scope + Siren Waves + Ju-88 Formation + Odometer
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        # Expanding crimson air-raid siren acoustic rings (strictly inside stage 665..1420)
        for ri in range(3):
            p_s = loop_p(global_t * 1000.0, 950.0, phase=ri * 0.33)
            rad_s = int(195 + p_s * 68)
            draw.ellipse([W//2 - rad_s, 935 - rad_s, W//2 + rad_s, 935 + rad_s], outline=C_DANGER, width=max(1, int(4 * bell(p_s))))
        # Rotating 360-degree Radar Scope with incoming German bomber blips
        blips = [(-85, -95, C_DANGER), (-35, -120, C_DANGER), (45, -80, C_DANGER), (95, -50, C_DANGER), (0, 20, C_AMBER)]
        draw_radar_scope(draw, W // 2, 935, 190, global_t, col=C_HEAL, blips=blips)
        # 3 Animated Vector Ju-88 Bombers swooping over the radar scope
        for bi, (bx0, by0, sc) in enumerate([(220, 740, 0.72), (540, 705, 0.85), (860, 745, 0.72)]):
            draw_ju88_bomber(draw, bx0, by0 + int(scene_t * 32), scale=sc, global_t=global_t + bi * 0.2)
        draw_split_flap_row(draw, W // 2, 1235, [("02", C_DANGER), ("DIC", C_AMBER), ("1943", C_WHITE)], scene_t + 0.3)
        draw_map_pill(draw, W // 2, 1355, "EXPEDIENTE SECRETO · EL «PEARL HARBOR» EUROPEO", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 1:
        # S01 ("2 de diciembre de 1943."): Animated WWII Military Chronometer + Night Harbor Silhouette & Biohazard Core
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        # Left: Animated WWII Chronometer with rotating internal brass gears
        draw_chronometer_watch(draw, 285, 925, 165, global_t, target_hour=19, target_min=25)
        # Right: Night Harbor Panel with sweeping searchlight cones, crane & Liberty ship with X-ray chemical core
        hx0, hy0, hw, hh = 500, 725, 510, 410
        draw.rounded_rectangle([hx0, hy0, hx0 + hw, hy0 + hh], radius=16, fill=(10, 18, 32), outline=C_TACTICAL, width=3)
        for s_i in (-1, 1):
            ang = math.radians(-90 + s_i * 22 + 16 * wave(global_t * 1000.0, 1900.0, s_i * 0.25))
            tx = hx0 + 255 + int(280 * math.cos(ang))
            ty = hy0 + 280 + int(280 * math.sin(ang))
            draw.polygon([(hx0 + 255, hy0 + 280), (tx - 42, max(hy0 + 6, ty)), (tx + 42, max(hy0 + 6, ty))], fill=(58, 78, 112))
        draw_liberty_ship(draw, hx0 + 255, hy0 + 285, scale=0.72, global_t=global_t, show_xray=True)
        draw_chemical_symbol(draw, hx0 + 255, hy0 + 145, 38, angle_deg=global_t * 80, col=C_AMBER)
        # Bottom: Mechanical Split-Flap Date Display flipping in
        draw_split_flap_row(draw, W // 2, 1235, [("02", C_DANGER), ("DICIEMBRE", C_AMBER), ("1943", C_WHITE)], scene_t)
        draw_map_pill(draw, W // 2, 1355, "PUERTO DE BARI, ITALIA · CARGA QUÍMICA OCULTA", C_AMBER)
        draw_hud_brackets(draw, scene_t, C_AMBER)
        return frame

    elif scene_id == 2:
        # S02 ("Noche cerrada en el sur de Italia."): Tactical Radar Sweep + Translucent Searchlights + Compass Rose
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_italy_geography(draw)
        bx, by = 665, 960
        # Translucent RGBA searchlight beams sweeping the night sky over Bari
        sl_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sld = ImageDraw.Draw(sl_layer)
        for s_i in (-1, 0, 1):
            ang = math.radians(-90 + s_i * 28 + 20 * wave(global_t * 1000.0, 2100.0, s_i * 0.33))
            tx = bx + int(340 * math.cos(ang))
            ty = by + int(340 * math.sin(ang))
            sld.polygon([(bx, by), (tx - 55, ty), (tx + 55, ty)], fill=(238, 178, 56, 72))
        # Rotating radar sweep ring centered on Bari Harbor
        sweep_deg = (global_t * 150.0) % 360.0
        sld.pieslice([bx - 190, by - 190, bx + 190, by + 190], start=sweep_deg - 35, end=sweep_deg, fill=(59, 130, 246, 68))
        frame.paste(sl_layer, (0, 0), sl_layer)
        draw = ImageDraw.Draw(frame)
        draw.ellipse([bx - 190, by - 190, bx + 190, by + 190], outline=C_TACTICAL, width=2)
        draw_crosshair(draw, bx, by, 42, col=C_DANGER)
        # Rotating Compass Rose in top-right of map
        cx_c, cy_c = 895, 775
        draw.ellipse([cx_c - 54, cy_c - 54, cx_c + 54, cy_c + 54], fill=(14, 24, 38), outline=C_TACTICAL, width=3)
        c_ang = math.radians(15 * math.sin(global_t * 2.5) - 90)
        draw.line([(cx_c - int(38*math.cos(c_ang)), cy_c - int(38*math.sin(c_ang))),
                   (cx_c + int(38*math.cos(c_ang)), cy_c + int(38*math.sin(c_ang)))], fill=C_DANGER, width=4)
        draw.text((cx_c, cy_c - 68), "N", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        draw_map_pill(draw, bx, by + 75, "PUERTO DE BARI · 41°07'N 16°52'E", C_AMBER)
        draw_map_pill(draw, 330, 760, "COSTA DEL ADRIÁTICO · NOCHE CERRADA", C_TACTICAL)
        draw_hud_brackets(draw, scene_t, C_TACTICAL)
        return frame

    elif scene_id == 3:
        # S03A ("105 bombarderos alemanes atacan por sorpresa el puerto de Bari"):
        # Steady Ju-88 Photo + Animated Squadron of 5 Vector Ju-88s + Radar Chaff Sparkles + Falling Bombs
        def _vec3a(frame, draw, st, sd):
            for bi, (bx, by, sc) in enumerate([(170, 785, 0.72), (390, 750, 0.82), (640, 765, 0.88), (875, 790, 0.74)]):
                draw_ju88_bomber(draw, bx, by, scale=sc, global_t=global_t + bi * 0.25)
                # Falling bombs from each bomber with dashed ballistic trail
                p_fall = loop_p(st * 1000.0, 950.0 + bi * 180.0, phase=bi * 0.23)
                py_b = by + 45 + int(EASE_IN(p_fall) * 310)
                draw.line([(bx, by + 35), (bx, py_b - 18)], fill=C_AMBER, width=2)
                draw.rounded_rectangle([bx - 11, py_b - 22, bx + 11, py_b + 16], radius=7, fill=C_DANGER, outline=C_WHITE, width=2)
            cnt_b = int(min(105, EASE_OUT(min(1.0, st / max(0.1, sd * 0.75))) * 105))
            draw_digital_led_box(draw, W // 2, 1195, f"{cnt_b} JU 88", C_DANGER)
            draw_hud_brackets(draw, st, C_DANGER)
        return render_module_a_steady(
            "ju88", scene_t, scene_dur,
            "LUFTWAFFE · 105 BOMBARDEROS JU 88",
            "105 bombarderos alemanes atacan por sorpresa el puerto de Bari",
            "FOTO DE ARCHIVO · BUNDESARCHIV (JUNKERS JU 88), 1943 · CC BY-SA 3.0",
            extra_vector_fn=_vec3a
        )

    elif scene_id == 301:
        # S03B ("...y hunden 17 barcos aliados."): Animated 17-Ship Destruction Matrix with Rossark Fire & Sinking Ships
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        sunk_cnt = max(1, int(min(17, EASE_OUT(min(1.0, s_prog * 1.15)) * 17)))
        for si in range(17):
            row = si // 6
            col_i = si % 6
            sx = 140 + col_i * 160 + (45 if row == 2 else 0)
            sy = 775 + row * 135
            is_hit = (si < sunk_cnt)
            sink_dy = int(12 * math.sin(global_t * 5 + si)) if is_hit else 0
            hull_col = (72, 22, 24) if is_hit else (46, 58, 74)
            stroke_c = C_DANGER if is_hit else C_NEUTRAL
            draw.polygon([
                (sx - 56, sy - 16 + sink_dy), (sx + 56, sy - 16 + sink_dy),
                (sx + 44, sy + 18 + sink_dy), (sx - 44, sy + 18 + sink_dy)
            ], fill=hull_col, outline=stroke_c, width=3)
            draw.line([(sx - 64, sy + 18), (sx + 64, sy + 18)], fill=C_TACTICAL, width=3)
            if is_hit:
                draw_rossark_fire(draw, sx, sy - 14 + sink_dy, scale=0.58, global_t=global_t + si * 0.17)
        draw_rossark_smoke_wisps(frame, W // 2, 980, global_t, count=7, col=(180, 175, 170), spread=720)
        draw = ImageDraw.Draw(frame)
        draw_digital_led_box(draw, W // 2, 1215, f"{sunk_cnt} BARCOS HUNDIDOS", C_DANGER)
        draw_map_pill(draw, W // 2, 1345, "EL MAYOR DESASTRE NAVAL ALIADO DESDE PEARL HARBOR", C_AMBER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 4:
        # S04 ("Pero en la bodega de uno de esos buques estadounidenses"):
        # Animated Laser X-Ray Scanner Sweeping Across Liberty Ship SS John Harvey
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_rossark_water_surface(draw, 1035, global_t, col=C_TACTICAL, n_ripples=4)
        draw_liberty_ship(draw, W // 2, 1005, scale=1.32, global_t=global_t, show_xray=True)
        # Animated vertical X-ray laser scanner sweeping across the hull
        scan_x = int(180 + (W - 360) * (0.5 + 0.5 * math.sin(scene_t * 3.2)))
        draw.line([(scan_x, 730), (scan_x, 1140)], fill=C_AMBER, width=5)
        draw.rounded_rectangle([scan_x - 85, 725, scan_x + 85, 765], radius=8, fill=(24, 22, 14), outline=C_AMBER, width=2)
        draw.text((scan_x, 745), "ESCANEO BODEGA", font=FONT_PILL_SM, fill=C_AMBER, anchor="mm")
        draw_crosshair(draw, W // 2, 1015, 58, col=C_DANGER)
        draw_map_pill(draw, W // 2, 1235, "BUQUE CLASE LIBERTY · SS JOHN HARVEY", C_TACTICAL)
        draw_map_pill(draw, W // 2, 1325, "BODEGA N.º 4: CARGA MILITAR NO DECLARADA", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_TACTICAL)
        return frame

    elif scene_id == 5:
        # S05 ("viaja una carga tan secreta"):
        # Animated Steel Cargo Vault + Rotating Hatch Wheel + Bubbling M47A1 Chemical Bomb Rack
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        # Heavy steel vault frame inside the cargo hold
        draw.rounded_rectangle([90, 710, W - 90, 1190], radius=24, fill=(20, 24, 30), outline=C_AMBER, width=4)
        # Left: Spinning steel vault locking wheel
        wx, wy, wr = 295, 950, 125
        draw.ellipse([wx - wr, wy - wr, wx + wr, wy + wr], fill=(32, 36, 44), outline=C_NEUTRAL, width=6)
        w_ang = scene_t * 95.0
        for sp_i in range(6):
            a = math.radians(w_ang + sp_i * 60)
            draw.line([(wx, wy), (wx + int(wr * math.cos(a)), wy + int(wr * math.sin(a)))], fill=C_AMBER, width=7)
        draw.ellipse([wx - 34, wy - 34, wx + 34, wy + 34], fill=C_DANGER, outline=C_WHITE, width=3)
        # Right: Rack of 4 M47A1 Chemical Bombs with bubbling toxic green-yellow liquid gauges
        for bi in range(4):
            bx = 535 + bi * 110
            by = 950
            draw.rounded_rectangle([bx - 36, by - 135, bx + 36, by + 115], radius=24, fill=(46, 54, 42), outline=C_NEUTRAL, width=3)
            # Nose fuse & tail fins
            draw.polygon([(bx - 22, by - 135), (bx + 22, by - 135), (bx, by - 168)], fill=C_AMBER, outline=C_WHITE, width=2)
            # Cutaway liquid window showing pulsing sulfur mustard level
            lvl = int(75 + 18 * math.sin(global_t * 5.0 + bi))
            draw.rounded_rectangle([bx - 20, by - 65, bx + 20, by + 65], radius=8, fill=(18, 22, 16), outline=C_TOXIC, width=2)
            draw.rounded_rectangle([bx - 17, by + 62 - lvl, bx + 17, by + 62], radius=5, fill=C_TOXIC)
        draw_map_pill(draw, W // 2, 1285, "CLASIFICACIÓN: ALTO SECRETO · COMPARTIMENTO SELLADO", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_AMBER)
        return frame

    elif scene_id == 6:
        # S06 ("que ni los médicos del puerto pueden conocerla."):
        # Living 2.5D Port Doctor Blocked by Lowering Barrier Gate & Padlocked Classified Dossier
        frame = CANVAS_ABYSS.copy()
        draw_rossark_character(frame, 295, 955, scale=1.32, role="port_doctor", global_t=global_t, scene_t=scene_t, talking=True, mood="tired", gesture="stop_hand")
        draw = ImageDraw.Draw(frame)
        # Right: Padlocked Classified Vault Card
        draw.rounded_rectangle([555, 745, 975, 1145], radius=20, fill=(44, 18, 20), outline=C_DANGER, width=4)
        # Animated heavy steel padlock + spinning chemical symbol
        px, py = 765, 865
        draw.arc([px - 38, py - 78, px + 38, py + 10], start=180, end=360, fill=C_NEUTRAL, width=10)
        draw.rounded_rectangle([px - 56, py - 32, px + 56, py + 58], radius=12, fill=C_AMBER, outline=C_WHITE, width=3)
        draw_chemical_symbol(draw, px, py + 13, 28, angle_deg=global_t * 75, col=C_INK)
        draw.text((765, 995), "CLASIFICADO", font=FONT_PILL_LG, fill=C_WHITE, anchor="mm")
        draw.text((765, 1050), "PROHIBIDO A HOSPITALES", font=FONT_PILL_SM, fill=C_AMBER, anchor="mm")
        gate_img, gx, gy = draw_barrier_gate(draw, 1215, angle_deg=max(0.0, 22.0 * (1.0 - s_prog * 1.5)))
        frame.paste(gate_img, (gx, gy), gate_img)
        draw_map_pill(draw, W // 2, 1345, "LOS MÉDICOS DE BARI NO SABÍAN QUÉ HABÍA EN EL PUERTO", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 7:
        # S07 ("Bari es el puerto clave para el avance aliado en Italia."):
        # Tactical Supply Map of Italy with Moving Convoy Lines & Rotating Logistics Hub
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_italy_geography(draw)
        bx, by = 665, 960
        for tx, ty, lbl in [(410, 820, "FRENTE DE MONTE CASSINO"), (300, 735, "AVANCE HACIA ROMA"), (520, 1085, "OCTAVO EJÉRCITO ALIADO")]:
            p_arr = EASE_OUT(min(1.0, s_prog * 1.35))
            cx_a = int(bx + (tx - bx) * p_arr)
            cy_a = int(by + (ty - by) * p_arr)
            draw.line([(bx, by), (cx_a, cy_a)], fill=C_AMBER, width=6)
            draw.ellipse([cx_a - 10, cy_a - 10, cx_a + 10, cy_a + 10], fill=C_DANGER, outline=C_WHITE, width=2)
            draw_map_pill(draw, tx, ty - 28, lbl, C_TACTICAL)
        draw_crosshair(draw, bx, by, 48, col=C_AMBER)
        draw_map_pill(draw, bx, by + 55, "PUERTO CLAVE DE BARI · SUMINISTRO ALIADO", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_TACTICAL)
        return frame

    elif scene_id == 8:
        # S08 ("Esa noche hay 30 barcos amarrados con las luces encendidas para descargar munición y combustible."):
        # Animated Night Pier with Floodlight Cones, Swinging Cranes & 30 Illuminated Ships
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        for i in range(6):
            lx = 150 + i * 155
            sway = int(18 * math.sin(global_t * 2.4 + i))
            draw.polygon([(lx, 690), (lx - 90 + sway, 1165), (lx + 90 + sway, 1165)], fill=(92, 78, 26))
            draw.ellipse([lx - 14, 680, lx + 14, 708], fill=C_AMBER, outline=C_WHITE, width=2)
        lit_ships = int(min(30, EASE_OUT(min(1.0, s_prog * 1.25)) * 30))
        for si in range(30):
            sx = 135 + (si % 10) * 90
            sy = 815 + (si // 10) * 110
            col = C_AMBER if si < lit_ships else (45, 55, 70)
            draw.rounded_rectangle([sx - 34, sy - 17, sx + 34, sy + 17], radius=8, fill=col, outline=C_WHITE, width=2)
        draw_digital_led_box(draw, W // 2, 1235, f"{lit_ships} BARCOS ENCENDIDOS", C_AMBER)
        draw_map_pill(draw, W // 2, 1345, "DESCARGANDO MUNICIÓN Y COMBUSTIBLE A PLENA LUZ", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_AMBER)
        return frame

    elif scene_id == 9:
        # S09 ("El mariscal británico Arthur Coningham cree que la aviación alemana ya está derrotada..."):
        # Steady Coningham Photo + Living 2.5D Officer + Radar Powered OFF Indicator
        def _vec9(frame, draw, st, sd):
            draw_rossark_character(frame, 835, 1075, scale=0.96, role="coningham", global_t=global_t, scene_t=st, talking=True, mood="smug", gesture="dismiss")
            draw = ImageDraw.Draw(frame)
            draw.rounded_rectangle([75, 1065, 535, 1175], radius=14, fill=(38, 16, 18), outline=C_DANGER, width=3)
            draw.text((305, 1102), "DEFENSA ANTIAÉREA RELAJADA", font=FONT_PILL_SM, fill=C_AMBER, anchor="mm")
            draw.text((305, 1142), "«ES IMPOSIBLE UN ATAQUE»", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
            draw_hud_brackets(draw, st, C_AMBER)
        return render_module_a_steady(
            "coningham", scene_t, scene_dur,
            "MARISCAL ARTHUR CONINGHAM (RAF)",
            "Creía que la Luftwaffe estaba derrotada y dejó el puerto encendido",
            "FOTO DE ARCHIVO · IMPERIAL WAR MUSEUM (ROYAL AIR FORCE), 1943 · DOMINIO PÚBLICO",
            extra_vector_fn=_vec9
        )

    elif scene_id == 10:
        # S10 ("A las 7:25 de la tarde, los aviones alemanes lanzan bengalas y bombardean durante 20 minutos."):
        # Animated 19:25 Chronometer + Swaying Parachute Flares & Falling Bombs
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw_digital_led_box(draw, W // 2, 755, "19:25 · 20 MIN", C_DANGER)
        for fi in range(4):
            fx = 195 + fi * 230 + int(22 * wave(global_t * 1000.0, 2100.0, fi * 0.3))
            fy = 910 + int(loop_p(global_t * 1000.0, 2400.0, seeded(fi, 3)) * 210)
            draw.pieslice([fx - 40, fy - 60, fx + 40, fy - 16], start=180, end=360, fill=C_NEUTRAL, outline=C_WHITE, width=2)
            draw.line([(fx - 36, fy - 38), (fx, fy + 12)], fill=C_NEUTRAL, width=2)
            draw.line([(fx + 36, fy - 38), (fx, fy + 12)], fill=C_NEUTRAL, width=2)
            r_glow = int(28 + 14 * abs(wave(global_t * 1000.0, 520.0, fi * 0.2)))
            draw.ellipse([fx - r_glow, fy + 12 - r_glow, fx + r_glow, fy + 12 + r_glow], fill=C_AMBER, outline=C_WHITE, width=3)
        draw_map_pill(draw, W // 2, 1320, "BENGALAS CON PARACAÍDAS ILUMINAN TODO EL PUERTO", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 11:
        # S11 ("Uno de los barcos alcanzados es el buque estadounidense John Harvey."):
        # Steady Liberty Ship Photo + Animated Red Radar Target Lock & Bomb Impact Vector
        def _vec11(frame, draw, st, sd):
            rad = int(185 - 50 * EASE_OUT(min(1.0, st / max(0.1, sd * 0.7))))
            draw_crosshair(draw, W // 2, 1005, rad, col=C_DANGER)
            draw_rossark_fire(draw, W // 2, 1005, scale=0.85, global_t=global_t)
            draw_map_pill(draw, W // 2, 1195, "BLANCO ALCANZADO: SS JOHN HARVEY", C_DANGER)
            draw_hud_brackets(draw, st, C_DANGER)
        return render_module_a_steady(
            "liberty", scene_t, scene_dur,
            "BUQUE CLASE LIBERTY · SS JOHN HARVEY",
            "Uno de los barcos alcanzados es el estadounidense John Harvey",
            "FOTO DE ARCHIVO · US MARITIME COMMISSION (BUQUE LIBERTY) · CC BY-SA 4.0",
            extra_vector_fn=_vec11
        )

    elif scene_id == 12:
        # S12 ("Casi nadie sabe que en sus bodegas esconde 2.000 bombas con gas mostaza,"):
        # Steady Mustard Bombs Photo + Animated 2,000 M47A1 Counter & Rotating Chemical Symbol
        def _vec12(frame, draw, st, sd):
            cnt = int(min(2000, EASE_OUT(min(1.0, st / max(0.1, sd * 0.75))) * 2000))
            draw_digital_led_box(draw, 355, 1175, f"{cnt} BOMBAS", C_DANGER)
            draw_chemical_symbol(draw, 825, 1175, 62, angle_deg=st * 95, col=C_AMBER)
            draw_hud_brackets(draw, st, C_DANGER)
        return render_module_a_steady(
            "bombs", scene_t, scene_dur,
            "ARSENAL QUÍMICO · BOMBAS M47A1",
            "En sus bodegas escondía 2.000 bombas cargadas con gas mostaza",
            "FOTO DE ARCHIVO · US ARMY CHEMICAL WARFARE SERVICE · DOMINIO PÚBLICO",
            extra_vector_fn=_vec12
        )

    elif scene_id == 13:
        # S13 ("enviadas por Washington por si Hitler usa armas químicas primero."):
        # Reconstructed Secret Washington Directive + Animated Hand Underlining + Slamming Stamp
        frame = render_module_c_document_with_hand(
            scene_t,
            "DEPARTAMENTO DE GUERRA DE EE. UU. · WASHINGTON (1943)",
            "DIRECTIVA DE RESERVA QUÍMICA EN EL MEDITERRÁNEO:",
            [
                "1. Embarcar 2.000 bombas M47A1 (Gas Mostaza).",
                "2. Buque asignado: SS John Harvey -> Bari.",
                "3. Condición de uso: Solo si Hitler usa gas primero.",
                "4. Clasificación: ESTRICTAMENTE SECRETO."
            ],
            highlight_idx={0, 2},
            stamp_text="ALTO SECRETO",
            source_attr="FUENTE HISTÓRICA · US ARMY CHEMICAL WARFARE SERVICE (1943)",
            tilt_deg=-1.4
        )
        draw_hud_brackets(ImageDraw.Draw(frame), scene_t, C_AMBER)
        return frame

    elif scene_id == 14:
        # S14 ("Pero había un problema mortal."):
        # Rossark Alarm Buzz Recipe + Burning Fuse Approaching Chemical Warhead
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        kx, ky = W // 2, 855
        burst_p = (global_t % 0.85)
        in_burst = burst_p < 0.45
        buzz_dx = int(8 * math.sin(burst_p / 0.45 * 4 * 2 * math.pi)) if in_burst else 0
        draw.rounded_rectangle([kx - 75 + buzz_dx, ky - 90, kx + 75 + buzz_dx, ky + 45], radius=34, fill=C_DANGER, outline=C_WHITE, width=4)
        draw_chemical_symbol(draw, kx + buzz_dx, ky - 22, 42, angle_deg=global_t * 100, col=C_AMBER)
        # Burning spark fuse bar
        fuse_w = int(620 * (1.0 - 0.75 * s_prog))
        draw.rounded_rectangle([230, 1000, 230 + 620, 1028], radius=10, fill=(32, 34, 40), outline=(90, 95, 105), width=2)
        draw.rounded_rectangle([230, 1000, 230 + fuse_w, 1028], radius=10, fill=C_AMBER)
        draw_rossark_fire(draw, 230 + fuse_w, 1014, scale=0.45, global_t=global_t)
        draw_digital_led_box(draw, W // 2, 1155, "TRAMPA MORTAL", C_DANGER)
        draw_map_pill(draw, W // 2, 1310, "SOLO LA TRIPULACIÓN DEL BUQUE CONOCÍA EL SECRETO", C_AMBER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 15:
        # S15 ("Cuando el John Harvey explota,"):
        # Steady Authentic Bari Explosion Photo + Multi-Ring Detonation Shockwaves + Rossark Fire & Smoke
        def _vec15(frame, draw, st, sd):
            cx_e, cy_e = W // 2, 1005
            for r in range(1, 4):
                p_r = loop_p(st * 1000.0, 950.0, phase=r * 0.28)
                rad = int(50 + p_r * 270)
                draw.ellipse([cx_e - rad, cy_e - rad, cx_e + rad, cy_e + rad], outline=C_DANGER if r%2==0 else C_AMBER, width=max(1, int(6 * bell(p_r))))
            draw_rossark_fire(draw, cx_e, 1045, scale=1.15, global_t=global_t)
            draw_rossark_smoke_wisps(frame, cx_e, 935, global_t, count=7, col=(235, 140, 45), spread=280)
            draw_hud_brackets(ImageDraw.Draw(frame), st, C_DANGER)
        return render_module_a_steady(
            "explosion", scene_t, scene_dur,
            "EXPLOSIÓN DEL SS JOHN HARVEY · BARI",
            "El buque SS John Harvey estalla en una gigantesca bola de fuego",
            "FOTO DE ARCHIVO · EXPLOSIÓN EN EL PUERTO DE BARI (2 DIC 1943) · DOMINIO PÚBLICO",
            extra_vector_fn=_vec15
        )

    elif scene_id == 16:
        # S16 ("todos sus tripulantes mueren en el acto."):
        # Animated Fracturing Ship Silhouette + ECG Heartbeat Flatlining to 0 BPM
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        # ECG Monitor Card
        draw.rounded_rectangle([95, 725, W - 95, 1085], radius=20, fill=(14, 20, 26), outline=C_DANGER, width=4)
        draw.text((W // 2, 775), "SIGNOS VITALES DE LA TRIPULACIÓN · SS JOHN HARVEY", font=FONT_PILL_SM, fill=C_AMBER, anchor="mm")
        pts_ecg = []
        for x_i in range(140, W - 140, 12):
            rel = (x_i - 140) / float(W - 280)
            if rel < 0.35 and s_prog < 0.55:
                y_e = 920 + int(65 * math.sin(rel * 38 + global_t * 12))
            elif 0.35 <= rel < 0.42:
                y_e = 920 - int(95 * (1.0 - s_prog))
            else:
                y_e = 920
            pts_ecg.append((x_i, y_e))
        draw.line(pts_ecg, fill=C_DANGER, width=6)
        draw_digital_led_box(draw, W // 2, 1200, "100% FALLECIDOS", C_DANGER)
        draw_map_pill(draw, W // 2, 1335, "TODA LA TRIPULACIÓN MUERE EN EL ACTO", C_AMBER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 17:
        # S17 ("Nadie queda vivo para avisar qué llevaba adentro."):
        # 14-Man Chemical Detachment Grid Crossing Out + Severed Telegraph Line
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([105, 705, W - 105, 1060], radius=18, fill=(26, 16, 18), outline=C_DANGER, width=3)
        draw.text((W // 2, 755), "DESTACAMENTO QUÍMICO DEL SS JOHN HARVEY", font=FONT_PILL_MD, fill=C_DANGER, anchor="mm")
        crossed = int(min(14, EASE_OUT(min(1.0, s_prog * 1.3)) * 14))
        for i in range(14):
            sx = 185 + (i % 7) * 118
            sy = 845 + (i // 7) * 95
            draw.ellipse([sx - 18, sy - 32, sx + 18, sy + 4], fill=(48, 52, 58), outline=(95, 100, 110), width=2)
            if i < crossed:
                draw.line([(sx - 22, sy - 32), (sx + 22, sy + 12)], fill=C_DANGER, width=5)
                draw.line([(sx + 22, sy - 32), (sx - 22, sy + 12)], fill=C_DANGER, width=5)
        draw_digital_led_box(draw, W // 2, 1190, "0 TESTIGOS VIVOS", C_DANGER)
        draw_map_pill(draw, W // 2, 1335, "NADIE QUEDA VIVO PARA AVISAR A LOS HOSPITALES", C_AMBER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 18:
        # S18 ("Toneladas de gas mostaza líquido se derraman en el agua y se mezclan con el petróleo..."):
        # Animated Ruptured Bomb Pouring Yellow Sulfur Mustard into Floating Black Oil on Rossark Water
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw.rectangle([0, 965, W, 1050], fill=(22, 20, 18))
        draw.rectangle([0, 988, W, 1028], fill=(165, 148, 28))
        draw_rossark_water_surface(draw, 965, global_t, col=C_TOXIC, n_ripples=4)
        draw_rossark_smoke_wisps(frame, W // 2, 955, global_t, count=7, col=C_TOXIC, spread=580)
        draw = ImageDraw.Draw(frame)
        draw_chemical_symbol(draw, 280, 815, 58, angle_deg=global_t * 75, col=C_TOXIC)
        draw_map_pill(draw, 280, 905, "GAS MOSTAZA LÍQUIDO", C_AMBER)
        draw_map_pill(draw, 780, 905, "PETRÓLEO FLOTANTE", C_DANGER)
        draw_map_pill(draw, W // 2, 1285, "MEZCLA LETAL SOBRE EL AGUA DEL PUERTO", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_AMBER)
        return frame

    elif scene_id == 19:
        # S19 ("Cientos de marineros nadan entre el aceite tóxico para salvarse."):
        # Steady Bari Burning Ships Photo + Animated Toxic Water Waves & Lifebuoy Markers
        def _vec19(frame, draw, st, sd):
            draw_rossark_water_surface(draw, 1205, global_t, col=C_TOXIC, n_ripples=4)
            draw_rossark_smoke_wisps(frame, W // 2, 1195, global_t, count=6, col=C_TOXIC, spread=520)
            draw_hud_brackets(ImageDraw.Draw(frame), st, C_DANGER)
        return render_module_a_steady(
            "ships", scene_t, scene_dur,
            "NAUFRAGIO EN AGUAS CONTAMINADAS",
            "Cientos de marineros nadan entre el aceite tóxico para salvarse",
            "FOTO DE ARCHIVO · BUQUES EN LLAMAS EN BARI (2 DIC 1943) · DOMINIO PÚBLICO",
            extra_vector_fn=_vec19
        )

    elif scene_id == 20:
        # S20 ("En los hospitales empiezan a quedar ciegos y a sufrir quemaduras terribles."):
        # Steady Mustard Burns Hospital Photo + Living 2.5D Blinded Sailor
        def _vec20(frame, draw, st, sd):
            draw_rossark_character(frame, 830, 1065, scale=0.98, role="sailor_victim", global_t=global_t, scene_t=st, mood="blinded")
            draw = ImageDraw.Draw(frame)
            draw_map_pill(draw, 320, 1165, "CEGUERA Y QUEMADURAS QUÍMICAS", C_DANGER)
            draw_hud_brackets(draw, st, C_DANGER)
        return render_module_a_steady(
            "hospital", scene_t, scene_dur,
            "HOSPITALES MILITARES DE BARI",
            "En pocas horas quedan ciegos y sufren quemaduras por todo el cuerpo",
            "FOTO DE ARCHIVO · ARCHIVO MÉDICO MILITAR (QUEMADURAS POR IPRITA) · DOMINIO PÚBLICO",
            extra_vector_fn=_vec20
        )

    elif scene_id == 21:
        # S21 ("Peor aún:"):
        # Kinetic Emergency Transition: Red Medical Cross Morphing into Biohazard Symbol + Toxicity Gauge
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        cx_w, cy_w = W // 2, 910
        for r_i in range(2):
            p_w = loop_p(global_t * 1000.0, 800.0, phase=r_i * 0.5)
            rad_w = int(95 + p_w * 190)
            draw.ellipse([cx_w - rad_w, cy_w - rad_w, cx_w + rad_w, cy_w + rad_w], outline=C_DANGER, width=max(1, int(5 * bell(p_w))))
        draw_chemical_symbol(draw, cx_w, cy_w, 88, angle_deg=global_t * 120, col=C_DANGER)
        draw_digital_led_box(draw, W // 2, 1185, "ERROR FATAL", C_DANGER)
        draw_map_pill(draw, W // 2, 1320, "EL DESCONOCIMIENTO MULTIPLICA LA TRAGEDIA", C_AMBER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 22:
        # S22 ("los médicos creen que solo sufren de frío y petróleo."):
        # Living 2.5D Port Doctor + Animated Diagnostic Checklist
        frame = CANVAS_ABYSS.copy()
        draw_rossark_character(frame, W // 2, 855, scale=1.22, role="port_doctor", global_t=global_t, scene_t=scene_t, talking=True, mood="tired")
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([85, 1080, 515, 1295], radius=16, fill=(18, 34, 58), outline=C_TACTICAL, width=3)
        draw.text((300, 1140), "DIAGNÓSTICO MÉDICO", font=FONT_PILL_SM, fill=C_TACTICAL, anchor="mm")
        draw.text((300, 1215), "FRÍO Y PETRÓLEO", font=FONT_PILL_LG, fill=C_WHITE, anchor="mm")
        draw.rounded_rectangle([565, 1080, W - 85, 1295], radius=16, fill=(52, 18, 20), outline=C_DANGER, width=3)
        draw.text((780, 1140), "REALIDAD OCULTA", font=FONT_PILL_SM, fill=C_AMBER, anchor="mm")
        draw.text((780, 1215), "GAS MOSTAZA", font=FONT_PILL_LG, fill=C_DANGER, anchor="mm")
        draw_hud_brackets(draw, scene_t, C_AMBER)
        return frame

    elif scene_id == 23:
        # S23 ("En lugar de lavarlos y quitarles la ropa,"):
        # Animated Decontamination Protocol Card Slammed with Giant Red X
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([140, 730, W - 140, 1185], radius=22, fill=(18, 34, 30), outline=C_HEAL, width=4)
        draw.text((W // 2, 805), "PROTOCOLO QUÍMICO DE EMERGENCIA", font=FONT_PILL_MD, fill=C_HEAL, anchor="mm")
        draw.text((W // 2, 915), "1. LAVAR CON AGUA Y JABÓN", font=FONT_PILL_LG, fill=C_WHITE, anchor="mm")
        draw.text((W // 2, 1005), "2. QUITAR TODA LA ROPA", font=FONT_PILL_LG, fill=C_WHITE, anchor="mm")
        # Animated red X slamming across the protocol
        x_prog = EASE_OUT(min(1.0, s_prog * 1.4))
        if x_prog > 0.1:
            x1 = int(200 + 680 * x_prog)
            y1 = int(780 + 350 * x_prog)
            draw.line([(200, 780), (x1, y1)], fill=C_DANGER, width=14)
            draw.line([(880, 780), (int(880 - 680 * x_prog), y1)], fill=C_DANGER, width=14)
        draw_map_pill(draw, W // 2, 1305, "PROTOCOLO DESCARTADO POR FALTA DE INFORMACIÓN", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 24:
        # S24 ("los envuelven en mantas con los uniformes empapados en veneno."):
        # Thermal Trap Diagram: Blankets Trapping Poison Against Skin + Rossark Toxic Fumes
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([120, 730, W - 120, 1185], radius=22, fill=(52, 18, 20), outline=C_DANGER, width=4)
        draw_rossark_smoke_wisps(frame, W // 2, 1080, global_t, count=7, col=C_TOXIC, spread=480)
        draw = ImageDraw.Draw(frame)
        draw.text((W // 2, 805), "TRAMPA TÉRMICA EN LOS HOSPITALES", font=FONT_PILL_MD, fill=C_AMBER, anchor="mm")
        draw.text((W // 2, 905), "MANTAS CERRADAS", font=FONT_BIG_NUM, fill=C_WHITE, anchor="mm")
        draw.text((W // 2, 1000), "+ UNIFORMES EMPAPADOS EN VENENO", font=FONT_PILL_LG, fill=C_DANGER, anchor="mm")
        draw_chemical_symbol(draw, W // 2, 1105, 42, angle_deg=global_t * 90, col=C_TOXIC)
        draw_map_pill(draw, W // 2, 1310, "EL CALOR DE LAS MANTAS ACELERÓ LAS QUEMADURAS", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 25:
        # S25 ("Nadie esperaba que el propio secreto aliado matara a sus soldados."):
        # Friendly-Fire Secrecy Boomerang Diagram
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([140, 735, W - 140, 1185], radius=22, fill=(28, 18, 22), outline=C_DANGER, width=4)
        draw_chemical_symbol(draw, W // 2, 890, 74, angle_deg=global_t * 65, col=C_AMBER)
        draw.text((W // 2, 1040), "SECRETO ALIADO = TRAMPA PROPIA", font=FONT_PILL_LG, fill=C_WHITE, anchor="mm")
        draw.text((W // 2, 1110), "EL SILENCIO MILITAR IMPIDIÓ EL TRATAMIENTO", font=FONT_PILL_SM, fill=C_DANGER, anchor="mm")
        draw_map_pill(draw, W // 2, 1310, "FUEGO AMIGO QUÍMICO POR ORDEN DE SILENCIO", C_AMBER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 26:
        # S26 ("En pocos días mueren más de 600 militares aliados y cientos de civiles italianos por la nube tóxica."):
        # +628 Allied Military Deaths & +1,000 Civilian Toxic Cloud Counters
        frame = CANVAS_ABYSS.copy()
        draw_rossark_smoke_wisps(frame, W // 2, 980, global_t, count=8, col=C_TOXIC, spread=640)
        draw = ImageDraw.Draw(frame)
        cnt_m = int(min(628, EASE_OUT(min(1.0, s_prog * 1.3)) * 628))
        cnt_c = int(min(1000, EASE_OUT(min(1.0, s_prog * 1.3)) * 1000))
        draw_digital_led_box(draw, W // 2, 855, f"+{cnt_m} MILITARES", C_DANGER)
        draw_digital_led_box(draw, W // 2, 1045, f"+{cnt_c} CIVILES", C_AMBER)
        draw_map_pill(draw, W // 2, 1275, "VÍCTIMAS DEL GAS MOSTAZA Y LA NUBE TÓXICA EN BARI", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 27:
        # S27 ("El mando aliado teme que si Alemania descubre la verdad use el episodio como excusa..."):
        # Tactical Map: Fear of Total Chemical War Across Europe
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_italy_geography(draw)
        for r in range(1, 5):
            p_r = loop_p(global_t * 1000.0, 1500.0, phase=r * 0.22)
            rad = int(60 + p_r * 350)
            draw.ellipse([W//2 - rad, 940 - rad, W//2 + rad, 940 + rad], outline=C_DANGER, width=max(1, int(4 * bell(p_r))))
        draw_chemical_symbol(draw, W // 2, 940, 58, angle_deg=global_t * 85, col=C_AMBER)
        draw_map_pill(draw, W // 2, 1285, "TEMOR ALIADO: GUERRA QUÍMICA TOTAL EN EUROPA", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_AMBER)
        return frame

    elif scene_id == 28:
        # S28 ("y por eso ordena silenciar el caso a toda costa."):
        # Lowering Censorship Gate + Slamming "SILENCIAR A TODA COSTA" Stamp
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        gate_img, gx, gy = draw_barrier_gate(draw, 1030, angle_deg=max(0.0, 22.0 * (1.0 - s_prog * 1.6)))
        frame.paste(gate_img, (gx, gy), gate_img)
        st_img = Image.new("RGBA", (660, 130), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st_img)
        sd.rectangle([8, 8, 652, 122], outline=C_DANGER + (255,), width=7)
        sd.text((330, 65), "SILENCIAR A TODA COSTA", font=FONT_HEADLINE, fill=C_DANGER + (255,), anchor="mm")
        rot_s = st_img.rotate(6, resample=Image.Resampling.BICUBIC, expand=True)
        frame.paste(rot_s, ((W - rot_s.width)//2, 760), rot_s)
        draw_map_pill(draw, W // 2, 1295, "ORDEN DEL ALTO MANDO: CENSURA ABSOLUTA", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    elif scene_id == 29:
        # S29 ("Entonces llega el teniente coronel médico Stewart Alexander."):
        # Steady US Army Chemical Warfare Photo + Living 2.5D Lt. Col. Dr. Stewart Alexander
        def _vec29(frame, draw, st, sd):
            draw_rossark_character(frame, 825, 1065, scale=1.05, role="alexander", global_t=global_t, scene_t=st, talking=True, mood="focused")
            draw = ImageDraw.Draw(frame)
            draw_map_pill(draw, 330, 1185, "DR. STEWART ALEXANDER (29 AÑOS)", C_TACTICAL)
            draw_hud_brackets(draw, st, C_TACTICAL)
        return render_module_a_steady(
            "edgewood", scene_t, scene_dur,
            "TENIENTE CORONEL MÉDICO · EE. UU.",
            "Llega a Bari el experto en medicina química Dr. Stewart Alexander",
            "FOTO DE ARCHIVO · US ARMY CHEMICAL WARFARE SERVICE · DOMINIO PÚBLICO",
            extra_vector_fn=_vec29
        )

    elif scene_id == 30:
        # S30 ("Al revisar a los muertos en las salas,"):
        # Living 2.5D Dr. Stewart Alexander Inspecting Hospital Wards with Animated Magnifying Glass
        frame = CANVAS_ABYSS.copy()
        draw_rossark_character(frame, 275, 965, scale=1.26, role="alexander", global_t=global_t, scene_t=scene_t, mood="focused")
        draw = ImageDraw.Draw(frame)
        # Right: 3 Hospital Ward Inspection Cards + Moving Magnifier Loupe
        for wi, w_lbl in enumerate(["SALA 1: QUEMADURAS ATÍPICAS", "SALA 2: PRESIÓN ARTERIAL CERO", "SALA 3: TEJIDOS CON OLOR EXTRAÑO"]):
            wy = 765 + wi * 135
            draw.rounded_rectangle([500, wy, 965, wy + 105], radius=14, fill=(18, 28, 42), outline=C_TACTICAL, width=3)
            draw.text((732, wy + 52), w_lbl, font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        ly_loupe = int(815 + 240 * (0.5 + 0.5 * math.sin(scene_t * 3.5)))
        draw.ellipse([680, ly_loupe - 55, 790, ly_loupe + 55], outline=C_AMBER, width=6)
        draw.line([(775, ly_loupe + 40), (835, ly_loupe + 100)], fill=C_AMBER, width=10)
        draw_map_pill(draw, W // 2, 1315, "INSPECCIÓN FORENSE EN LOS HOSPITALES DE BARI", C_TACTICAL)
        draw_hud_brackets(draw, scene_t, C_TACTICAL)
        return frame

    elif scene_id == 31:
        # S31 ("siente un leve olor a ajo y comprueba que sus glóbulos blancos desaparecieron casi por completo."):
        # Steady WWII Mustard Gas Poster (Garlic Odor) + Animated Microscope Showing Dissolving White Blood Cells
        def _vec31(frame, draw, st, sd):
            mx, my, mr = 755, 980, 185
            draw.ellipse([mx - mr - 8, my - mr - 8, mx + mr + 8, my + mr + 8], fill=(18, 24, 34), outline=C_TACTICAL, width=5)
            draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(28, 16, 24))
            surviving = max(2, int(14 * (1.0 - EASE_OUT(min(1.0, st / max(0.1, sd * 0.8))))))
            for ci in range(14):
                ang = ci * 0.45 + st * 0.8
                dist = 35 + (ci % 3) * 42
                cx_c = mx + int(dist * math.cos(ang))
                cy_c = my + int(dist * math.sin(ang))
                if ci < surviving:
                    draw.ellipse([cx_c - 16, cy_c - 16, cx_c + 16, cy_c + 16], fill=C_WHITE, outline=C_TACTICAL, width=3)
                else:
                    draw.ellipse([cx_c - 10, cy_c - 10, cx_c + 10, cy_c + 10], outline=(90, 50, 60), width=1)
            draw_map_pill(draw, 290, 920, "OLOR A AJO DETECTADO", C_AMBER)
            draw_map_pill(draw, mx, my + mr + 42, "GLÓBULOS BLANCOS DESTRUIDOS", C_DANGER)
            draw_hud_brackets(draw, st, C_TACTICAL)
        return render_module_a_steady(
            "poster", scene_t, scene_dur,
            "PISTA FORENSE · OLOR A AJO Y LEUCOPENIA",
            "Detecta olor a ajo y comprueba que sus glóbulos blancos desaparecieron",
            "FOTO DE ARCHIVO · CARTEL DE IDENTIFICACIÓN DE GAS MOSTAZA (US ARMY, WWII) · DOMINIO PÚBLICO",
            extra_vector_fn=_vec31
        )

    elif scene_id == 32:
        # S32 ("Deduce enseguida que es gas mostaza disuelto en el agua del puerto."):
        # Reconstructed Medical Report by Lt. Col. Stewart Alexander + Moving Hand
        frame = render_module_c_document_with_hand(
            scene_t,
            "CUERPO MÉDICO DEL EJÉRCITO DE EE. UU. · BARI (DIC 1943)",
            "INFORME PRELIMINAR DEL TTE. CORONEL STEWART ALEXANDER:",
            [
                "• Hallazgo 1: Olor a ajo en tejidos y ropa.",
                "• Hallazgo 2: Caída drástica de glóbulos blancos.",
                "• Diagnóstico: Gas mostaza disuelto en el agua.",
                "• Origen: Explosión de un buque en el puerto."
            ],
            highlight_idx={1, 2},
            stamp_text="GAS MOSTAZA",
            source_attr="FUENTE HISTÓRICA · INFORME MÉDICO DE STEWART ALEXANDER (20 DIC 1943)",
            tilt_deg=1.4
        )
        draw_hud_brackets(ImageDraw.Draw(frame), scene_t, C_AMBER)
        return frame

    elif scene_id == 33:
        # S33 ("Desobedece el silencio oficial,"):
        # Living 2.5D Dr. Stewart Alexander Breaking Red Censorship Seal
        frame = CANVAS_ABYSS.copy()
        draw_rossark_character(frame, 300, 960, scale=1.28, role="alexander", global_t=global_t, scene_t=scene_t, talking=True, mood="focused", gesture="stop_hand")
        draw = ImageDraw.Draw(frame)
        # Shattering Censorship Tape on Right
        draw.rounded_rectangle([530, 780, 960, 1130], radius=18, fill=(38, 16, 18), outline=C_DANGER, width=4)
        draw.text((745, 875), "ORDEN DE SILENCIO", font=FONT_PILL_LG, fill=C_DANGER, anchor="mm")
        draw.line([(560, 875), (930, 875)], fill=C_WHITE, width=6)
        draw.text((745, 985), "DESOBEDECIDA", font=FONT_BIG_NUM, fill=C_HEAL, anchor="mm")
        draw_map_pill(draw, W // 2, 1295, "ALEXANDER PONE LA VIDA DE LOS HERIDOS PRIMERO", C_HEAL)
        draw_hud_brackets(draw, scene_t, C_TACTICAL)
        return frame

    elif scene_id == 34:
        # S34 ("exige lavar de inmediato a todos los heridos y salva cientos de vidas."):
        # Animated Decontamination Shower + Climbing Saved Lives Counter
        frame = CANVAS_ABYSS.copy()
        draw_rossark_character(frame, 265, 960, scale=1.20, role="alexander", global_t=global_t, scene_t=scene_t, talking=True, mood="focused", gesture="stop_hand")
        draw = ImageDraw.Draw(frame)
        sx0, sy0 = 510, 735
        draw.rounded_rectangle([sx0, sy0, sx0 + 440, sy0 + 465], radius=20, fill=(14, 34, 48), outline=C_TACTICAL, width=4)
        draw.text((sx0 + 220, sy0 + 55), "LAVADO DE EMERGENCIA", font=FONT_PILL_MD, fill=C_TACTICAL, anchor="mm")
        for di in range(18):
            p_d = loop_p(global_t * 1000.0, 850.0 + seeded(di, 1) * 300.0, phase=seeded(di, 2))
            dx = sx0 + 65 + int(seeded(di, 3) * 310)
            dy = sy0 + 100 + int(p_d * 240)
            draw.ellipse([dx - 4, dy - 8, dx + 4, dy + 8], fill=C_TACTICAL)
        draw_digital_led_box(draw, sx0 + 220, sy0 + 380, "CIENTOS SALVADOS", C_HEAL)
        draw_map_pill(draw, W // 2, 1315, "LAVAR LA PIEL Y QUITAR EL UNIFORME SALVÓ A LOS HERIDOS", C_HEAL)
        draw_hud_brackets(draw, scene_t, C_HEAL)
        return frame

    elif scene_id == 35:
        # S35 ("Churchill ordena borrar el gas mostaza de los archivos británicos,"):
        # Steady Winston Churchill 1943 Photo + Black Censorship Bars Redacting "GAS MOSTAZA"
        def _vec35(frame, draw, st, sd):
            draw.rounded_rectangle([75, 1030, W - 75, 1265], radius=14, fill=C_PAPER, outline=C_INK, width=3)
            draw.text((115, 1080), "REGISTRO MÉDICO BRITÁNICO (ORDEN DE CHURCHILL):", font=FONT_DOC_HDR, fill=C_INK)
            draw.text((115, 1135), "Causa de muerte: «Quemaduras por acción enemiga»", font=FONT_DOC_BOLD, fill=C_INK)
            draw.text((115, 1190), "Eliminar toda mención a: GAS MOSTAZA ALIADO", font=FONT_DOC_BOLD, fill=C_DANGER)
            rw = int(340 * EASE_OUT(min(1.0, st / max(0.1, sd * 0.65))))
            draw.rectangle([455, 1185, 455 + rw, 1222], fill=C_INK)
            draw_hud_brackets(draw, st, C_DANGER)
        return render_module_a_steady(
            "churchill", scene_t, scene_dur,
            "LONDRES · ORDEN DE WINSTON CHURCHILL",
            "Churchill ordena borrar el gas mostaza de los archivos británicos",
            "FOTO DE ARCHIVO · CONFERENCIA DE EL CAIRO (CHURCHILL, 1943) · DOMINIO PÚBLICO",
            extra_vector_fn=_vec35
        )

    elif scene_id == 36:
        # S36 ("pero el informe de Alexander tiene un giro inesperado para la medicina."):
        # Reconstructed Declassified Oncology Discovery Dossier (Goodman, Gilman & Alexander)
        frame = render_module_c_document_with_hand(
            scene_t,
            "UNIVERSIDAD DE YALE / CUERPO MÉDICO EE. UU. (1943-1946)",
            "EL GIRO CIENTÍFICO DEL INFORME DE STEWART ALEXANDER:",
            [
                "• Observación en Bari: El compuesto destruye",
                "  selectivamente células de división rápida.",
                "• Hipótesis médica (Dr. Goodman y Dr. Gilman):",
                "  Usar mostaza nitrogenada contra linfomas y tumores."
            ],
            highlight_idx={1, 3},
            stamp_text="AVANCE MÉDICO",
            source_attr="FUENTE HISTÓRICA · INFORME DE ALEXANDER & ESTUDIO DE GOODMAN Y GILMAN (1946)",
            tilt_deg=-1.3
        )
        draw_hud_brackets(ImageDraw.Draw(frame), scene_t, C_TACTICAL)
        return frame

    elif scene_id == 37:
        # S37 ("Al ver"):
        # Animated Optical Microscope Aperture Zooming In (10X -> 40X -> 100X)
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        cx_m, cy_m = W // 2, 960
        for ri, r_base in enumerate([240, 175, 110]):
            r_cur = int(r_base * (0.85 + 0.15 * math.sin(global_t * 6 + ri)))
            draw.ellipse([cx_m - r_cur, cy_m - r_cur, cx_m + r_cur, cy_m + r_cur], outline=C_TACTICAL if ri%2==0 else C_HEAL, width=4)
        draw_crosshair(draw, cx_m, cy_m, 75, col=C_HEAL)
        draw_map_pill(draw, W // 2, 1285, "ANÁLISIS CELULAR DEL INFORME DE BARI", C_TACTICAL)
        draw_hud_brackets(draw, scene_t, C_TACTICAL)
        return frame

    elif scene_id == 38:
        # S38 ("cómo esa sustancia destruía los glóbulos blancos,"):
        # Animated Cellular Microscope: Rapidly Dividing Cells Halted by Mustard Compound
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        cx_m, cy_m, r_m = W // 2, 975, 235
        draw.ellipse([cx_m - r_m - 10, cy_m - r_m - 10, cx_m + r_m + 10, cy_m + r_m + 10], fill=(16, 26, 40), outline=C_TACTICAL, width=5)
        draw.ellipse([cx_m - r_m, cy_m - r_m, cx_m + r_m, cy_m + r_m], fill=(12, 18, 28))
        for i in range(9):
            ang = i * (2 * math.pi / 9) + global_t * 0.65
            rad_d = 115
            x_c = cx_m + int(rad_d * math.cos(ang))
            y_c = cy_m + int(rad_d * math.sin(ang))
            sz = int(34 * (1.0 - 0.58 * EASE_OUT(s_prog)))
            draw.ellipse([x_c - sz, y_c - sz, x_c + sz, y_c + sz], fill=(220, 230, 245), outline=C_TACTICAL, width=3)
        draw_map_pill(draw, W // 2, 1305, "EL COMPUESTO FRENA LAS CÉLULAS QUE SE DIVIDEN RÁPIDO", C_TACTICAL)
        draw_hud_brackets(draw, scene_t, C_TACTICAL)
        return frame

    elif scene_id == 39:
        # S39 ("los científicos descubren que una variante química podía frenar el avance de los tumores."):
        # Animated Tumor Regression Diagram + Rossark Draw-On Clinical Curve
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        tx_c, ty_c = 310, 960
        t_rad = int(145 * (1.0 - 0.62 * EASE_OUT(s_prog)))
        for lobe in range(6):
            la = lobe * (math.pi / 3) + global_t
            lx = tx_c + int(t_rad * 0.45 * math.cos(la))
            ly = ty_c + int(t_rad * 0.45 * math.sin(la))
            draw.ellipse([lx - t_rad//2, ly - t_rad//2, lx + t_rad//2, ly + t_rad//2], fill=(135, 28, 38), outline=C_DANGER, width=3)
        draw_map_pill(draw, tx_c, 1185, "TUMOR EN REGRESIÓN", C_HEAL)
        gx0, gy0, gw, gh = 555, 780, 425, 340
        draw.rounded_rectangle([gx0, gy0, gx0 + gw, gy0 + gh], radius=14, fill=(16, 22, 30), outline=C_HEAL, width=3)
        draw.text((gx0 + gw//2, gy0 + 45), "REDUCCIÓN DEL TUMOR", font=FONT_PILL_MD, fill=C_HEAL, anchor="mm")
        pts = []
        n_pts = max(2, int(20 * EASE_OUT(min(1.0, s_prog * 1.2))))
        for pi in range(n_pts):
            px = gx0 + 40 + int((pi / 19.0) * (gw - 80))
            py = gy0 + 100 + int(((pi / 19.0) ** 0.7) * (gh - 150))
            pts.append((px, py))
        if len(pts) >= 2:
            draw.line(pts, fill=C_HEAL, width=6)
        draw_map_pill(draw, W // 2, 1315, "LA MOSTAZA NITROGENADA FRENA EL AVANCE DEL CÁNCER", C_HEAL)
        draw_hud_brackets(draw, scene_t, C_HEAL)
        return frame

    elif scene_id == 40:
        # S40 ("Del desastre secreto de Bari nace la primera quimioterapia contra el cáncer."):
        # Steady Mustine/Mechlorethamine Structure + Animated IV Chemotherapy Drip
        def _vec40(frame, draw, st, sd):
            ix, iy = 230, 815
            draw.rounded_rectangle([ix - 75, iy, ix + 75, iy + 220], radius=22, fill=(18, 48, 62), outline=C_HEAL, width=4)
            draw.text((ix, iy + 85), "MUSTINA", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
            draw.text((ix, iy + 125), "(CLORMETINA)", font=FONT_PILL_SM, fill=C_HEAL, anchor="mm")
            p_drop = loop_p(st * 1000.0, 850.0)
            dy_d = iy + 230 + int(p_drop * 90)
            draw.ellipse([ix - 8, dy_d - 12, ix + 8, dy_d + 12], fill=C_HEAL)
            draw_digital_led_box(draw, 680, 1185, "1.ª QUIMIOTERAPIA", C_HEAL)
            draw_hud_brackets(draw, st, C_HEAL)
        return render_module_a_steady(
            "molecule", scene_t, scene_dur,
            "MECLORETAMINA · ONCOLOGÍA MODERNA",
            "Del desastre secreto de Bari nace la primera quimioterapia contra el cáncer",
            "ARCHIVO CIENTÍFICO · ESTRUCTURA DE LA MOSTAZA NITROGENADA · CC BY-SA 4.0",
            extra_vector_fn=_vec40
        )

    elif scene_id == 41:
        # S41 ("Un secreto militar mató a cientos de aliados y terminó salvando a millones de enfermos."):
        # Golden Balance Scale Tipping from Tragedy to Millions Saved
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        tilt = -12.0 * EASE_IN_OUT(min(1.0, max(0.0, (scene_t - 0.25) / 1.1))) + 1.2 * wave(global_t * 1000.0, 3200.0)
        draw_balance_scale(
            draw, W // 2, 1340,
            tilt_deg=tilt,
            left_pills=["SECRETO MILITAR", "+600 ALIADOS MUERTOS"],
            right_pills=["1.ª QUIMIOTERAPIA", "MILLONES DE VIDAS"],
            left_title="DESASTRE DE BARI",
            right_title="SALVADOS DEL CÁNCER",
            left_col=C_DANGER,
            right_col=C_HEAL,
            drop_prog=s_prog * 1.4
        )
        draw_hud_brackets(draw, scene_t, C_AMBER)
        return frame

    elif scene_id == 42:
        # S42 ("Ponete en el lugar del alto mando esa noche:"):
        # Living 2.5D Allied High Command Officer & Dr. Stewart Alexander Facing the Dilemma
        frame = CANVAS_ABYSS.copy()
        draw_rossark_character(frame, 305, 975, scale=1.22, role="coningham", global_t=global_t, scene_t=scene_t, mood="focused")
        draw_rossark_character(frame, 775, 975, scale=1.22, role="alexander", global_t=global_t, scene_t=scene_t, talking=True, mood="focused", gesture="stop_hand")
        draw = ImageDraw.Draw(frame)
        draw_map_pill(draw, 305, 1215, "ALTO MANDO ALIADO", C_DANGER)
        draw_map_pill(draw, 775, 1215, "CUERPO MÉDICO EN BARI", C_HEAL)
        draw_map_pill(draw, W // 2, 1320, "EL DILEMA MORAL DEL 2 DE DICIEMBRE DE 1943", C_AMBER)
        draw_hud_brackets(draw, scene_t, C_AMBER)
        return frame

    elif scene_id == 43:
        # S43 ("¿vos habrías revelado el secreto del gas para salvar a los heridos"):
        # Spotlight Card A: Reveal the Secret & Save the Wounded
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([120, 740, W - 120, 1185], radius=24, fill=(14, 34, 44), outline=C_HEAL, width=4)
        draw.text((W // 2, 825), "DECISIÓN A: SALVAR A LOS HERIDOS", font=FONT_PILL_MD, fill=C_HEAL, anchor="mm")
        draw_rossark_jiggle_button(draw, W // 2, 965, 680, 92, "REVELAR EL SECRETO MILITAR", (18, 52, 64), C_HEAL, global_t, phase_offset=0.0)
        draw.text((W // 2, 1095), "PERMITIR QUE LOS MÉDICOS LAVEN EL VENENO", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        draw_map_pill(draw, W // 2, 1300, "RIESGO: EXPONER EL ARSENAL QUÍMICO SECRETO", C_AMBER)
        draw_hud_brackets(draw, scene_t, C_HEAL)
        return frame

    elif scene_id == 44:
        # S44 ("o lo habrías ocultado?"):
        # Spotlight Card B: Hide the Secret to Prevent Total Chemical War
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([120, 740, W - 120, 1185], radius=24, fill=(42, 16, 20), outline=C_DANGER, width=4)
        draw.text((W // 2, 825), "DECISIÓN B: SILENCIO DE ESTADO", font=FONT_PILL_MD, fill=C_AMBER, anchor="mm")
        draw_rossark_jiggle_button(draw, W // 2, 965, 650, 92, "OCULTAR EL GAS A TODA COSTA", (58, 18, 22), C_DANGER, global_t, phase_offset=0.5)
        draw.text((W // 2, 1095), "EVITAR QUE HITLER INICIE UNA GUERRA QUÍMICA", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        draw_map_pill(draw, W // 2, 1300, "COSTO: CIENTOS DE MARINEROS MUEREN SIN TRATAMIENTO", C_DANGER)
        draw_hud_brackets(draw, scene_t, C_DANGER)
        return frame

    else:
        # S45 ("Contámelo en los comentarios."):
        # Final Interactive Dilemma over Steady Bari Explosion Photo + Rossark Jiggle Action Buttons
        frame = PHOTOS_STEADY_STAGE.get("explosion", CANVAS_ABYSS).copy()
        draw = ImageDraw.Draw(frame)
        for r in range(2):
            rp = loop_p(global_t * 1000.0, 1600.0, phase=r * 0.5)
            rad = int(50 + rp * 260)
            draw.ellipse([W//2 - rad, 940 - rad, W//2 + rad, 940 + rad], outline=C_AMBER, width=max(1, int(3 * bell(rp))))
        draw_rossark_jiggle_button(draw, W // 2, 1115, 680, 82, "REVELAR EL SECRETO Y SALVARLOS", (14, 32, 42), C_HEAL, global_t, phase_offset=0.0)
        draw_rossark_jiggle_button(draw, W // 2, 1215, 640, 82, "OCULTAR EL GAS A TODA COSTA", (34, 14, 16), C_DANGER, global_t, phase_offset=0.5)
        draw.rounded_rectangle([140, 1290, W - 140, 1375], radius=12, fill=(18, 20, 24), outline=C_AMBER, width=3)
        draw.text((W // 2, 1332), "CONTÁMELO EN LOS COMENTARIOS", font=FONT_PILL_MD, fill=C_AMBER, anchor="mm")
        draw_attribution_pill(draw, "FOTO DE ARCHIVO · PUERTO DE BARI (2 DE DICIEMBRE DE 1943) · DOMINIO PÚBLICO")
        draw_hud_brackets(draw, scene_t, C_AMBER)
        return frame

# Level 1 (Top Dynamic Subtitle with blur(6px) on future words & 4-node VectorSelectionBox)
# + Level 2 (Section Headline ALL CAPS ExtraBold at Y=545px)
SUB_CACHE = {}

def render_top_overlays(frame, chunk_idx, active_w_idx, scene_id, scene_t):
    draw = ImageDraw.Draw(frame)
    title, subtitle, variant = SCENE_META.get(scene_id, SCENE_META[1])
    t_col = VARIANT_COLORS.get(variant, C_AMBER)
    slide_y = int((1.0 - min(1.0, scene_t / 0.18)) * 12)
    draw.text((W // 2 + 3, 558 + slide_y), title, font=FONT_HEADLINE, fill=(0, 0, 0), anchor="mm")
    draw.text((W // 2, 555 + slide_y), title, font=FONT_HEADLINE, fill=t_col, anchor="mm")
    if subtitle:
        draw.text((W // 2 + 2, 616 + slide_y), subtitle, font=FONT_SUBHEAD, fill=(0, 0, 0), anchor="mm")
        draw.text((W // 2, 614 + slide_y), subtitle, font=FONT_SUBHEAD, fill=(210, 208, 202), anchor="mm")

    if chunk_idx is None:
        draw_map_pill(draw, W // 2, 340, "PUERTO DE BARI, ITALIA · 2 DE DICIEMBRE DE 1943", C_DANGER)
        return

    ch = CHUNKS[chunk_idx]
    words = ch["words"]
    if not words:
        return
    active_w_idx = max(0, min(len(words) - 1, active_w_idx))
    active_group = words[active_w_idx].get("group_id", 0)

    cache_key = (chunk_idx, active_w_idx)
    if cache_key not in SUB_CACHE:
        group_words = [(wi, wo) for wi, wo in enumerate(words) if wo.get("group_id", 0) == active_group]
        lines = []
        cur_line = []
        cur_w = 0
        space_w = FONT_SUB_BOLD.getlength(" ")
        for wi, wo in group_words:
            w_px = FONT_SUB_BOLD.getlength(wo["word"])
            if cur_line and (cur_w + space_w + w_px > 860):
                lines.append(cur_line)
                cur_line = [(wi, wo)]
                cur_w = w_px
            else:
                cur_w = (cur_w + space_w + w_px) if cur_line else w_px
                cur_line.append((wi, wo))
        if cur_line:
            lines.append(cur_line)

        sub_layer = Image.new("RGBA", (W, 240), (0, 0, 0, 0))
        blur_layer = Image.new("RGBA", (W, 240), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(sub_layer)
        b_draw = ImageDraw.Draw(blur_layer)

        line_h = 64
        total_h = len(lines) * line_h
        start_y = 110 - total_h // 2

        has_future = False
        for li, line_items in enumerate(lines):
            line_w = sum(FONT_SUB_BOLD.getlength(wo["word"]) for _, wo in line_items) + space_w * (len(line_items) - 1)
            cur_x = (W - line_w) / 2.0
            cur_y = start_y + li * line_h

            for wi, wo in line_items:
                w_str = wo["word"]
                w_px = FONT_SUB_BOLD.getlength(w_str)
                is_past = (wi < active_w_idx)
                is_active = (wi == active_w_idx)
                is_future = (wi > active_w_idx)
                show_bbox = bool(wo.get("is_bbox")) and not is_future

                if is_future:
                    b_draw.text((cur_x, cur_y), w_str, font=FONT_SUB_REG, fill=(255, 255, 255, 95))
                    has_future = True
                else:
                    if show_bbox:
                        bx0, by0 = int(cur_x - 10), int(cur_y - 4)
                        bx1, by1 = int(cur_x + w_px + 10), int(cur_y + 54)
                        s_draw.rectangle([bx0, by0, bx1, by1], fill=(59, 130, 246, 52), outline=(59, 130, 246, 255), width=3)
                        for nx, ny in [(bx0, by0), (bx1, by0), (bx0, by1), (bx1, by1)]:
                            s_draw.rectangle([nx - 4, ny - 4, nx + 4, ny + 4], fill=(255, 255, 255, 255), outline=(59, 130, 246, 255), width=1)
                    if is_active or show_bbox:
                        s_draw.text((cur_x + 2, cur_y + 3), w_str, font=FONT_SUB_BOLD, fill=(0, 0, 0, 220))
                        s_draw.text((cur_x, cur_y), w_str, font=FONT_SUB_BOLD, fill=(255, 255, 255, 255))
                    elif is_past:
                        s_draw.text((cur_x + 2, cur_y + 3), w_str, font=FONT_SUB_REG, fill=(0, 0, 0, 180))
                        s_draw.text((cur_x, cur_y), w_str, font=FONT_SUB_REG, fill=(154, 160, 166, 195))
                cur_x += w_px + space_w

        if has_future:
            blur_layer = blur_layer.filter(ImageFilter.GaussianBlur(5.5))
            combined = Image.alpha_composite(blur_layer, sub_layer)
        else:
            combined = sub_layer

        if len(SUB_CACHE) < 800:
            SUB_CACHE[cache_key] = combined
    else:
        combined = SUB_CACHE[cache_key]

    frame.paste(combined, (0, 220), combined)

SCENE_BOUNDS = {0: [0.0, CHUNKS[0]["start"]]}
for ch in CHUNKS:
    sid = ch["scene_id"]
    s_t = ch["start"]
    e_t = ch["end"] + ch["pause_after"]
    if sid not in SCENE_BOUNDS:
        SCENE_BOUNDS[sid] = [s_t, e_t]
    else:
        SCENE_BOUNDS[sid][1] = max(SCENE_BOUNDS[sid][1], e_t)

def get_state_at(t):
    if t < CHUNKS[0]["start"]:
        return None, 0, 0, t, max(0.1, CHUNKS[0]["start"])
    for idx, ch in enumerate(CHUNKS):
        c_s = ch["start"]
        c_e = ch["end"] + ch["pause_after"]
        if c_s <= t <= c_e or idx == len(CHUNKS) - 1:
            sid = ch["scene_id"]
            sb_s, sb_e = SCENE_BOUNDS[sid]
            st_cur = max(0.0, t - sb_s)
            sd_cur = max(0.1, sb_e - sb_s)
            if sid == 3 and st_cur >= sd_cur * 0.50:
                sid = 301
                st_cur = st_cur - sd_cur * 0.50
                sd_cur = sd_cur * 0.50
            active_w = len(ch["words"]) - 1
            for wi, wo in enumerate(ch["words"]):
                if t <= wo["end"]:
                    active_w = wi
                    break
            return idx, active_w, sid, st_cur, sd_cur
    return len(CHUNKS) - 1, 0, 45, 1.0, 1.0

def render_frame_at(t):
    chunk_idx, active_w, scene_id, scene_t, scene_dur = get_state_at(t)
    frame = render_stage_for_scene(scene_id, scene_t, scene_dur, t)
    render_top_overlays(frame, chunk_idx, active_w, scene_id, scene_t)
    return frame

def format_srt_time(seconds):
    ms = int(round((seconds - int(seconds)) * 1000))
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

srt_path = os.path.join(OUT_DIR, "desastre_bari_es.srt")
with open(srt_path, "w", encoding="utf-8") as sf:
    for idx_c, ch in enumerate(CHUNKS, 1):
        sf.write(f"{idx_c}\n")
        sf.write(f"{format_srt_time(ch['start'])} --> {format_srt_time(ch['end'])}\n")
        sf.write(f"{ch['text']}\n\n")

# Save high-impact cover / first frame (portada_bari.png)
cover_img = render_frame_at(53.5)
cover_img.save(os.path.join(OUT_DIR, "portada_bari.png"))

print("Rendering 12-frame verification mosaic (storyboard_verificacion.jpg)...")
sample_times = [0.9, 2.3, 4.9, 7.6, 10.6, 13.2, 15.5, 17.5, 53.5, 73.5, 106.5, 149.0]
grid = Image.new("RGB", (4 * 270, 3 * 480), (0, 0, 0))
for i, st in enumerate(sample_times):
    f_im = render_frame_at(st).resize((270, 480), Image.Resampling.LANCZOS)
    grid.paste(f_im, ((i % 4) * 270, (i // 4) * 480))
grid.save(os.path.join(OUT_DIR, "storyboard_verificacion.jpg"), quality=92)

if "--storyboard-only" in sys.argv:
    print("Storyboard verification complete.")
    sys.exit(0)

INTERNAL_FPS = 30
total_frames = int(TOTAL_DUR * INTERNAL_FPS)
out_mp4 = os.path.join(OUT_DIR, "desastre_bari_short.mp4")
audio_path = os.path.join(OUT_DIR, "audio/audio_master_180s.wav")

print(f"Encoding {total_frames} frames ({TOTAL_DUR:.2f}s) into {out_mp4} (1080x1920 @ 60fps output, zero-jitter, BT.709, -14 LUFS)...")
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo", "-vcodec", "rawvideo",
    "-s", f"{W}x{H}", "-pix_fmt", "rgb24",
    "-r", str(INTERNAL_FPS),
    "-i", "-",
    "-i", audio_path,
    "-i", srt_path,
    "-map", "0:v:0", "-map", "1:a:0", "-map", "2:s:0",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
    "-r", "60",
    "-pix_fmt", "yuv420p",
    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
    "-c:a", "aac", "-b:a", "192k",
    "-c:s", "mov_text", "-metadata:s:s:0", "language=spa",
    "-movflags", "+faststart",
    "-shortest",
    out_mp4
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
for f_idx in range(total_frames):
    t = f_idx / INTERNAL_FPS
    frame_img = render_frame_at(t)
    proc.stdin.write(frame_img.tobytes())
    if f_idx % 500 == 0 and f_idx > 0:
        print(f"  Rendered {f_idx}/{total_frames} frames ({100.0*f_idx/total_frames:.1f}%)...")

proc.stdin.close()
ret = proc.wait()
assert ret == 0, f"FFmpeg exited with code {ret}"
print(f"SUCCESS! Rendered {out_mp4} ({os.path.getsize(out_mp4)/(1024*1024):.2f} MB)")
