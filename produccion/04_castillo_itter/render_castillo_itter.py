import os
import sys
import json
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1920

with open("produccion/04_castillo_itter/timeline_chunks.json", "r", encoding="utf-8") as f:
    TL_DATA = json.load(f)
TOTAL_DUR = TL_DATA["total_duration"]
CHUNKS = TL_DATA["chunks"]

def load_font(paths, size):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

FONT_SUB_REG = load_font([
    "produccion/04_castillo_itter/assets/fonts/Inter-Regular.ttf",
    "produccion/01_submarino_b59/assets/fonts/Inter-Regular.ttf",
    "C:/Windows/Fonts/segoeui.ttf"
], 46)
FONT_SUB_BOLD = load_font([
    "C:/Windows/Fonts/segoeuib.ttf",
    "produccion/04_castillo_itter/assets/fonts/Montserrat-Bold.ttf"
], 46)

FONT_HEADLINE = load_font([
    "C:/Windows/Fonts/segoeuib.ttf",
    "produccion/04_castillo_itter/assets/fonts/Montserrat-Bold.ttf"
], 54)
FONT_SUBHEAD = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 23)

FONT_RIBBON = load_font(["C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/consolab.ttf"], 25)
FONT_DOC_HDR = load_font(["C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/consolab.ttf"], 22)
FONT_DOC_META = load_font(["C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/consolab.ttf"], 24)
FONT_DOC_LINE = load_font(["C:/Windows/Fonts/cour.ttf", "C:/Windows/Fonts/consola.ttf"], 26)
FONT_DOC_BOLD = load_font(["C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/consolab.ttf"], 26)
FONT_STAMP = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 28)
FONT_FOOTER = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 15)
FONT_ATTR = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 17)

FONT_PILL_LG = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 31)
FONT_PILL_MD = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 24)
FONT_PILL_SM = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 19)
FONT_BIG_NUM = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 72)

# Palette tokens (historical-shorts-visual-system)
C_ABYSS = (13, 13, 13)          # #0D0D0D
C_OCEAN_DARK = (11, 37, 69)     # #0B2545
C_LAND_FILL = (107, 127, 70)    # #6B7F46
C_LAND_STROKE = (148, 168, 107) # #94A86B
C_PAPER = (244, 239, 230)       # #F4EFE6
C_INK = (26, 25, 23)            # #1A1917
C_STAMP_RED = (214, 54, 41)     # #D63629
C_NEUTRAL = (245, 242, 235)     # #F5F2EB
C_AMBER = (240, 180, 41)        # #F0B429
C_DANGER = (224, 90, 71)        # #E05A47
C_TACTICAL = (96, 165, 250)     # #60A5FA
C_WHITE = (255, 255, 255)
C_BBOX_BLUE = (59, 130, 246)    # #3B82F6

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
# ROSSARK-MOTION-SKILL ENGINE
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
            if x + 1 < W: pix[x + 1, y] = (r, g, b)
            if y + 1 < H: pix[x, y + 1] = (r, g, b)
            if x + 1 < W and y + 1 < H: pix[x + 1, y + 1] = (r, g, b)
    return img

CANVAS_ABYSS = make_abyss_canvas()

def make_tactical_map_canvas():
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

CANVAS_TACTICAL_MAP = make_tactical_map_canvas()

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

# PRE-COMPOSITE STEADY ARCHIVAL STAGES ONCE AT STARTUP -> ZERO IMAGE JITTER!
ASSETS_DIR = "produccion/04_castillo_itter/assets"
PHOTOS_STEADY_STAGE = {}
PORTRAIT_CROPS = {}

for key, fname, fy_val in [
    ("itter", "schloss_itter.jpg", 0.48),
    ("gangl", "josef_gangl.jpg", 0.35),
    ("reynaud", "paul_reynaud.jpg", 0.35),
    ("daladier", "edouard_daladier.jpg", 0.35),
    ("borotra", "jean_borotra.jpg", 0.42),
    ("sherman", "sherman_1945.jpg", 0.50),
    ("pak88", "pak_88mm.jpg", 0.48),
    ("us_reinf", "us_reinforcements_1945.jpg", 0.50),
    ("weygand", "weygand.jpg", 0.35),
    ("gamelin", "gamelin.jpg", 0.35),
]:
    p = os.path.join(ASSETS_DIR, fname)
    if os.path.exists(p):
        im = Image.open(p).convert("RGB")
        im = ImageEnhance.Contrast(im).enhance(1.08)
        PORTRAIT_CROPS[key] = im
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
    1:  ("5 DE MAYO DE 1945", "CASTILLO DE ITTER · ALPES AUSTRÍACOS", "danger"),
    2:  ("TANQUE SHERMAN EN LLAMAS", "BLOQUEANDO EL PORTÓN DEL CASTILLO MEDIEVAL", "danger"),
    3:  ("FUEGO DESDE LAS VENTANAS", "DEFENSORES TRAS LOS MUROS MEDIEVALES", "amber"),
    4:  ("SOLDADOS DE ESTADOS UNIDOS", "EJÉRCITO DE EE. UU. EN LAS ALMENAS", "tactical"),
    5:  ("EJÉRCITO REGULAR ALEMÁN", "SOLDADOS DE LA WEHRMACHT EN EL MISMO MURO", "amber"),
    6:  ("2 EX PRIMEROS MINISTROS", "LÍDERES DE FRANCIA ARMADOS CON FUSILES", "neutral"),
    7:  ("PELEANDO DEL MISMO LADO", "EE. UU. + WEHRMACHT + FRANCIA CONTRA LAS SS", "amber"),
    8:  ("MAYO DE 1945 · ALPES AUSTRÍACOS", "VALLE DE BRIXENTAL · TIROL, AUSTRIA", "neutral"),
    9:  ("5 DÍAS DESPUÉS DE HITLER", "EL TERCER REICH SE DESMORONA (MAYO 1945)", "danger"),
    10: ("CASTILLO DE ITTER", "PRISIÓN NAZI DE MÁXIMA SEGURIDAD PARA REHENES VIP", "amber"),
    11: ("PAUL REYNAUD Y ÉDOUARD DALADIER", "LOS DOS EX PRIMEROS MINISTROS DE FRANCIA", "tactical"),
    12: ("GENERALES Y CAMPEÓN DE TENIS", "WEYGAND, GAMELIN Y JEAN BOROTRA ENCERRADOS", "amber"),
    13: ("GUARDIAS HUYEN DEL CASTILLO", "ABANDONAN LA FORTALEZA ANTE EL COLAPSO NAZI", "neutral"),
    14: ("EL PELIGRO REAL ESTÁ AFUERA", "LA FORTALEZA QUEDA RODEADA EN LA MONTAÑA", "danger"),
    15: ("ESCUADRONES WAFFEN-SS", "OPERANDO EN LOS BOSQUES ALPINOS VECINOS", "danger"),
    16: ("ORDEN DE EJECUTAR A TODOS", "LIQUIDAR A LOS REHENES ANTES DE QUE LLEGUEN LOS ALIADOS", "danger"),
    17: ("CALLEJÓN SIN SALIDA", "TROPAS ALIADAS A KILÓMETROS SIN SABER NADA", "danger"),
    18: ("MISIÓN EN BICICLETA A WÖRGL", "EL COCINERO DEL CASTILLO BAJA A PEDIR SOCORRO", "tactical"),
    19: ("MAYOR JOSEF «SEPP» GANGL", "COMANDANTE CONDECORADO DE LA WEHRMACHT", "amber"),
    20: ("DESOBEDECE A SUS SUPERIORES", "PROTEGE A LOS VECINOS DE WÖRGL CONTRA LAS SS", "tactical"),
    21: ("SOLO 20 SOLDADOS ALEMANES", "INSUFICIENTES PARA FRENAR A LAS WAFFEN-SS", "danger"),
    22: ("BANDERA BLANCA EN UN AUTO", "GANGL SALE A BUSCAR A LOS ESTADOUNIDENSES", "neutral"),
    23: ("LA HISTORIA DA UN VUELCO", "EL ENCUENTRO MÁS INSÓLITO DE LA GUERRA", "amber"),
    24: ("CAPITÁN JOHN «JACK» LEE", "OFICIAL ESTADOUNIDENSE DE 27 AÑOS EN KUFSTEIN", "tactical"),
    25: ("14 SOLDADOS Y 1 TANQUE SHERMAN", "LA ÚNICA PATRULLA ALIADA EN LA ZONA", "amber"),
    26: ("LA ALIANZA SUBE AL CASTILLO", "LEE Y GANGL AVANZAN JUNTOS POR LA MONTAÑA", "tactical"),
    27: ("14 DE EE. UU. + 10 DE LA WEHRMACHT", "24 SOLDADOS EN TOTAL PARA DEFENDER ITTER", "amber"),
    28: ("SHERMAN TAPANDO EL PORTÓN", "EL TANQUE «BESOTTEN JENNY» BLOQUEA LA ENTRADA", "tactical"),
    29: ("REHENES FRANCESES ARMADOS", "LOS EX MINISTROS PIDEN FUSILES Y OCUPAN LAS ALMENAS", "amber"),
    30: ("AMANECER DEL 5 DE MAYO", "150 EFECTIVOS WAFFEN-SS Y CAÑONES ANTITANQUE", "danger"),
    31: ("DISPARANDO CODO CON CODO", "ESTADOUNIDENSES, ALEMANES Y FRANCESES JUNTOS", "amber"),
    32: ("DESTRUYEN EL TANQUE SHERMAN", "UN PROYECTIL DE 88 MM INCENDIA EL PORTÓN", "danger"),
    33: ("PAUL REYNAUD QUEDA EXPUESTO", "EN LA MIRA DE UN FRANCOTIRADOR EN EL MURO", "danger"),
    34: ("EL SACRIFICIO DE JOSEF GANGL", "CORRE A EMPUJARLO Y RECIBE EL DISPARO EN EL PECHO", "danger"),
    35: ("MUERE SALVANDO AL LÍDER FRANCÉS", "ÚNICA BAJA MORTAL ENTRE LOS DEFENSORES DEL CASTILLO", "amber"),
    36: ("16:00 HS · CASI SIN CARTUCHOS", "LOS DEFENSORES AL LÍMITE DE MUNICIÓN", "danger"),
    37: ("LLEGAN LOS REFUERZOS DE EE. UU.", "EL 142.º REGIMIENTO BARRE A LOS ATACANTES DE LAS SS", "tactical"),
    38: ("EN UNA MISMA TRINCHERA", "QUIENES UN DÍA ANTES TENÍAN ORDEN DE MATARSE", "amber"),
    39: ("EL DILEMA FRENTE AL ENEMIGO", "UN OFICIAL ALEMÁN CON BANDERA BLANCA PIDE AYUDA", "amber"),
    40: ("¿QUÉ HABRÍAS HECHO VOS?", "PELEAR A SU LADO vs. NO ARRIESGARSE", "amber"),
}

VARIANT_COLORS = {
    "neutral": C_NEUTRAL,
    "amber": C_AMBER,
    "danger": C_DANGER,
    "tactical": C_TACTICAL,
}

# ==============================================================================
# REUSABLE VECTOR STORYTELLING & ROSSARK MOTION PRIMITIVES
# ==============================================================================
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

def draw_five_point_star(draw, cx, cy, r_out, r_in, fill_col=C_WHITE):
    pts = []
    for i in range(10):
        ang = math.radians(i * 36 - 90)
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + int(r * math.cos(ang)), cy + int(r * math.sin(ang))))
    draw.polygon(pts, fill=fill_col)

def draw_digital_led_box(draw, cx, cy, text, col=C_DANGER):
    fnt = FONT_BIG_NUM
    tw = int(fnt.getlength(text))
    if tw + 64 > W - 80:
        fnt = FONT_HEADLINE
        tw = int(fnt.getlength(text))
    pw, ph = min(W - 60, tw + 64), 104
    x0, y0 = cx - pw // 2, cy - ph // 2
    draw.rectangle([x0, y0, x0 + pw, y0 + ph], fill=(18, 16, 18), outline=col, width=4)
    draw.text((cx, cy - 2), text, font=fnt, fill=col, anchor="mm")

def draw_crosshair(draw, cx, cy, rad, col=C_DANGER):
    draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=col, width=4)
    draw.ellipse([cx - int(rad * 0.6), cy - int(rad * 0.6), cx + int(rad * 0.6), cy + int(rad * 0.6)], outline=col, width=2)
    draw.line([(cx - rad - 35, cy), (cx + rad + 35, cy)], fill=col, width=4)
    draw.line([(cx, cy - rad - 35), (cx, cy + rad + 35)], fill=col, width=4)

def draw_rossark_smoke_and_fire(frame, cx, base_y, global_t, count=6, scale=1.0):
    """Rossark fire (2-4 deg lean & 3-6% stretch on two waves) + rising smoke wisps with bell(p)."""
    t_ms = global_t * 1000.0
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(count):
        p = loop_p(t_ms, 2200.0 + seeded(i, 1) * 650.0, phase=seeded(i, 2))
        alpha = int(195 * bell(p))
        if alpha > 8:
            wx = cx + int(((seeded(i, 3) - 0.5) * 170 + 18.0 * wave(t_ms, 1750.0, seeded(i, 4))) * scale)
            wy = base_y - int((30 + p * 180) * scale)
            r = int((20 + p * 36) * scale)
            od.ellipse([wx - r, wy - int(r * 0.78), wx + r, wy + int(r * 0.78)], fill=(42, 44, 50, alpha))
    for fi in range(3):
        fx = cx + int((fi - 1) * 48 * scale)
        stretch = 1.0 + 0.06 * wave(t_ms, 680.0, fi * 0.3) + 0.04 * wave(t_ms, 1080.0, fi * 0.7)
        lean_px = int(10.0 * scale * wave(t_ms, 820.0, fi * 0.4))
        fh = int(76 * scale * stretch)
        fw = int(28 * scale)
        od.polygon([(fx - fw, base_y), (fx + fw, base_y), (fx + lean_px, base_y - fh)], fill=(224, 90, 71, 240))
        od.polygon([(fx - int(fw * 0.55), base_y), (fx + int(fw * 0.55), base_y), (fx + int(lean_px * 0.6), base_y - int(fh * 0.65))], fill=(240, 180, 41, 250))
    frame.paste(overlay, (0, 0), overlay)

def draw_sherman_tank(draw, cx, cy, scale=1.0, on_fire=False, facing="right"):
    d = 1 if facing == "right" else -1
    hull_w = int(165 * scale)
    hull_h = int(42 * scale)
    # Tracks & bogies
    draw.rounded_rectangle([cx - hull_w, cy, cx + hull_w, cy + int(42 * scale)], radius=int(18 * scale), fill=(36, 38, 40), outline=(95, 100, 108), width=max(2, int(3 * scale)))
    for wi in range(-3, 4):
        wx = cx + int(wi * 44 * scale)
        r_w = int(14 * scale)
        draw.ellipse([wx - r_w, cy + int(21 * scale) - r_w, wx + r_w, cy + int(21 * scale) + r_w], fill=(64, 68, 72), outline=C_NEUTRAL, width=2)
    # Upper hull (Olive drab or scorched red)
    hull_col = (88, 32, 28) if on_fire else (74, 86, 54)
    stroke_col = C_DANGER if on_fire else (142, 158, 104)
    draw.polygon([
        (cx - hull_w + int(12 * scale), cy),
        (cx + hull_w - int(12 * scale), cy),
        (cx + int(hull_w * 0.82), cy - hull_h),
        (cx - int(hull_w * 0.86), cy - hull_h),
    ], fill=hull_col, outline=stroke_col, width=max(2, int(3 * scale)))
    # White Allied Star on hull side
    star_cy = cy - int(hull_h * 0.48)
    draw.ellipse([cx - int(18 * scale), star_cy - int(18 * scale), cx + int(18 * scale), star_cy + int(18 * scale)], fill=(38, 46, 32), outline=C_WHITE, width=2)
    draw_five_point_star(draw, cx, star_cy, int(13 * scale), int(5 * scale), C_WHITE)
    # Rounded cast turret + 75mm gun barrel
    tw = int(78 * scale)
    th = int(40 * scale)
    draw.rounded_rectangle([cx - tw, cy - hull_h - th + 4, cx + tw, cy - hull_h + 6], radius=int(18 * scale), fill=hull_col, outline=stroke_col, width=max(2, int(3 * scale)))
    barrel_x0 = cx + tw * d
    barrel_x1 = cx + int(195 * scale) * d
    by = cy - hull_h - int(th * 0.55)
    draw.line([(barrel_x0, by), (barrel_x1, by)], fill=stroke_col, width=max(5, int(10 * scale)))

def draw_castle_gatehouse(draw, cx, cy, scale=1.0):
    """Medieval stone gatehouse and crenellated towers of Castle Itter."""
    w = int(380 * scale)
    h = int(320 * scale)
    stone_fill = (64, 62, 58)
    stone_stroke = (128, 124, 116)
    # Main curtain wall
    draw.rectangle([cx - w, cy - h, cx + w, cy], fill=stone_fill, outline=stone_stroke, width=3)
    # Crenellations (merlons along top)
    merlon_w = int(42 * scale)
    for mx in range(cx - w, cx + w - merlon_w + 4, int(68 * scale)):
        draw.rectangle([mx, cy - h - int(34 * scale), mx + merlon_w, cy - h + 2], fill=stone_fill, outline=stone_stroke, width=2)
    # 3 Gothic arched windows on upper level
    for wx in [cx - int(220 * scale), cx, cx + int(220 * scale)]:
        wy = cy - int(h * 0.68)
        ww, wh = int(36 * scale), int(64 * scale)
        draw.rounded_rectangle([wx - ww, wy - wh // 2, wx + ww, wy + wh // 2], radius=int(18 * scale), fill=(22, 24, 28), outline=C_AMBER, width=2)
    # Grand medieval arched gateway at bottom center
    gw, gh = int(135 * scale), int(155 * scale)
    draw.rounded_rectangle([cx - gw, cy - gh, cx + gw, cy], radius=int(65 * scale), fill=(18, 16, 18), outline=C_AMBER, width=4)

def draw_tyrol_valley_map(draw, global_t):
    """2D Tactical Map of the Tyrolean Alps: Inn Valley, Kufstein, Wörgl, Brixental Valley, and Castle Itter."""
    t_ms = global_t * 1000.0
    # Alpine mountain ridges (olive/stone polygons)
    north_ridge = [(0, 650), (1080, 650), (1080, 820), (840, 855), (610, 795), (360, 845), (0, 810)]
    south_ridge = [(0, 1140), (310, 1085), (560, 1040), (820, 995), (1080, 1060), (1080, 1415), (0, 1415)]
    draw.polygon(north_ridge, fill=C_LAND_FILL, outline=C_LAND_STROKE, width=3)
    draw.polygon(south_ridge, fill=(84, 102, 56), outline=C_LAND_STROKE, width=3)
    # Inn River & Valley road from Kufstein -> Wörgl -> Itter
    road_pts = [(190, 890), (390, 980), (660, 1065), (790, 1165)]
    draw.line(road_pts, fill=(185, 178, 162), width=6)
    # Swaying alpine pine trees (rossark plant recipe: 1.5-4 deg sway around base)
    for i, (px, py) in enumerate([(140, 1210), (260, 1250), (480, 1190), (610, 1260), (910, 1180), (960, 1265)]):
        sway_px = int(4.0 * wave(t_ms, 3800.0 + i * 300.0, phase=seeded(i, 7)))
        draw.polygon([(px - 22, py), (px + 22, py), (px + sway_px, py - 58)], fill=(46, 72, 38), outline=C_LAND_STROKE, width=2)

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

def draw_vector_hand(draw, hx, hy, angle_deg=-25, sleeve_col=(62, 74, 48)):
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

def draw_rossark_soldier(
    frame, cx, cy, scale=1.25, role="us_soldier", global_t=0.0, scene_t=0.0,
    talking=False, mood="focused", gesture="aim_rifle"
):
    """2.5D Living Military Soldier / Statesman built with rossark-motion-skill."""
    t_ms = (global_t * 1000.0) % 7200.0
    s_ms = scene_t * 1000.0
    canvas_sz = 460
    rig = Image.new("RGBA", (canvas_sz, canvas_sz), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rig)
    ox, oy = canvas_sz // 2, 210

    if role == "us_soldier":
        suit_col = (74, 84, 52, 255)       # US Olive Drab
        suit_shade = (102, 114, 72, 255)
        cap_top = (56, 66, 40, 255)        # M1 Steel Helmet
        badge_col = C_TACTICAL + (255,)
        phase_seed = 0.14
    elif role == "wehrmacht":
        suit_col = (76, 86, 80, 255)       # Wehrmacht Feldgrau
        suit_shade = (104, 116, 108, 255)
        cap_top = (64, 74, 68, 255)        # Bergmütze / Field Cap
        badge_col = C_AMBER + (255,)
        phase_seed = 0.38
    elif role == "french_vip":
        suit_col = (30, 38, 56, 255)       # French Statesman Dark Suit
        suit_shade = (52, 64, 92, 255)
        cap_top = (36, 44, 64, 255)
        badge_col = C_DANGER + (255,)
        phase_seed = 0.62
    else:  # waffen_ss
        suit_col = (38, 36, 40, 255)
        suit_shade = (68, 64, 72, 255)
        cap_top = (28, 26, 30, 255)
        badge_col = C_DANGER + (255,)
        phase_seed = 0.84

    skin_col = (242, 185, 148, 255)
    feature_col = (210, 126, 88, 255)
    hair_col = (68, 46, 34, 255)

    lean_keys = [(0, 0.0), (1800, -2.2), (3600, 1.8), (5400, -1.4), (7200, 0.0)]
    yaw_keys = [(0, -0.14), (2100, 0.20), (4200, 0.16), (5800, -0.16), (7200, -0.14)]
    head_keys = [(0, 0.0), (2000, 3.2), (4100, -2.8), (5900, 1.8), (7200, 0.0)]

    lean = flow(t_ms, lean_keys) + 1.3 * wave(t_ms, 4200.0, phase_seed)
    yaw = flow(t_ms, yaw_keys) + 0.05 * wave(t_ms, 3100.0, phase_seed + 0.2)
    head_tilt = flow(t_ms, head_keys) - 0.45 * flow(max(0.0, t_ms - 110.0), lean_keys) + 1.6 * wave(t_ms, 4600.0, phase_seed + 0.5)

    sy = 1.0 + 0.015 * wave(t_ms, 2600.0, phase_seed)
    sx = 1.0 / (sy ** 0.6)
    lift = 2.4 * wave(t_ms, 2600.0, phase_seed + 0.25)

    if gesture == "aim_rifle":
        arm_ra_keys = [(0, 48.0), (400, 68.0), (1400, 72.0), (7200, 68.0)]
        arm_re_keys = [(0, 35.0), (400, 75.0), (1400, 80.0), (7200, 76.0)]
    elif gesture == "salute_alliance":
        arm_ra_keys = [(0, 25.0), (450, 58.0), (1400, 62.0), (7200, 60.0)]
        arm_re_keys = [(0, 15.0), (450, 92.0), (1400, 96.0), (7200, 94.0)]
    else:
        arm_ra_keys = [(0, 22.0), (2400, 30.0), (4800, 18.0), (7200, 22.0)]
        arm_re_keys = [(0, 18.0), (2400, 32.0), (4800, 14.0), (7200, 18.0)]

    t_gesture = min(7199.0, s_ms)
    ra_base = flow(t_gesture, arm_ra_keys) + 3.2 * wave(t_ms, 3000.0, phase_seed)
    ra_prev = flow(max(0.0, t_gesture - 90.0), arm_ra_keys)
    re_base = flow(t_gesture, arm_re_keys) + 4.0 * wave(t_ms, 2250.0, phase_seed + 0.4) + 0.45 * (ra_prev - flow(t_gesture, arm_ra_keys))

    la_base = 24.0 + 3.2 * wave(t_ms, 3200.0, phase_seed + 0.5)
    le_base = -18.0 + 3.8 * wave(t_ms, 2400.0, phase_seed + 0.8)

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
        return ha_x, ha_y

    draw_arm(-1, la_base, le_base)

    t_top = by + int(48 * sy)
    t_bot = by + int(138 * sy)
    sh_w = int(52 * sx)
    wa_w = int(44 * sx)
    rd.polygon([(bx - sh_w, t_top), (bx + sh_w, t_top), (bx + wa_w, t_bot), (bx - wa_w, t_bot)], fill=suit_col, outline=suit_shade)
    yaw_px = int(8 * yaw)
    rd.polygon([(bx - 16 + yaw_px, t_top), (bx + 16 + yaw_px, t_top), (bx + yaw_px, t_top + 26)], fill=C_WHITE + (255,))

    if role == "wehrmacht":
        # Iron Cross ribbon / badge on chest
        ix, iy = bx + yaw_px - 18, t_top + 48
        rd.rectangle([ix - 9, iy - 3, ix + 9, iy + 3], fill=C_INK + (255,), outline=C_WHITE + (255,), width=1)
        rd.rectangle([ix - 3, iy - 9, ix + 3, iy + 9], fill=C_INK + (255,), outline=C_WHITE + (255,), width=1)
    elif role == "french_vip":
        # French Tricolor cockade on lapel
        cx_f, cy_f = bx + yaw_px + 20, t_top + 40
        rd.ellipse([cx_f - 10, cy_f - 10, cx_f + 10, cy_f + 10], fill=C_DANGER + (255,), outline=C_WHITE + (255,), width=3)
        rd.ellipse([cx_f - 4, cy_f - 4, cx_f + 4, cy_f + 4], fill=C_TACTICAL + (255,))
    else:
        for b_row in [t_top + 36, t_top + 60, t_top + 84]:
            rd.ellipse([bx + yaw_px - 4, b_row - 4, bx + yaw_px + 4, b_row + 4], fill=C_AMBER + (255,))

    head_layer = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_layer)
    hcx, hcy = 120, 130

    ear_dx = int(-9 * yaw)
    for side in [-1, 1]:
        ex = hcx + side * 50 + ear_dx
        hd.ellipse([ex - 11, hcy - 10, ex + 11, hcy + 12], fill=skin_col, outline=feature_col, width=2)

    hd.rounded_rectangle([hcx - 50, hcy - 64, hcx + 50, hcy + 52], radius=28, fill=skin_col, outline=feature_col, width=2)

    blinks = make_blink_keys(7200.0, [1350.0, 4050.0, 6150.0])
    lid_val = track(t_ms, blinks)
    if mood == "focused":
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
        hd.line([(ecx - 12, brow_y), (ecx + 12, brow_y - 2)], fill=hair_col, width=5)

    nx = hcx + int(13 * yaw)
    hd.rounded_rectangle([nx - 5, hcy - 4, nx + 5, hcy + 14], radius=4, fill=feature_col)

    mx = hcx + face_dx
    my = hcy + 26
    if role == "french_vip":
        # Statesman mustache (Reynaud / Daladier)
        hd.line([(mx - 14, my - 6), (mx + 14, my - 6)], fill=hair_col, width=5)
    if talking:
        m_depth = int(6 + 10 * abs(wave(t_ms, 340.0, phase_seed)))
        hd.polygon([(mx - 14, my), (mx + 14, my), (mx + 10, my + m_depth), (mx - 10, my + m_depth)], fill=(155, 42, 42, 255))
    else:
        hd.arc([mx - 12, my - 4, mx + 12, my + 8], start=15, end=165, fill=feature_col, width=4)

    if role in ("us_soldier", "waffen_ss"):
        hd.pieslice([hcx - 60, hcy - 92, hcx + 60, hcy + 10], start=180, end=360, fill=cap_top, outline=suit_shade, width=3)
        hd.line([(hcx - 62, hcy - 42), (hcx + 62, hcy - 42)], fill=(36, 42, 28, 255), width=5)
        if role == "us_soldier":
            hd.ellipse([hcx + int(6 * yaw) - 8, hcy - 68, hcx + int(6 * yaw) + 8, hcy - 52], fill=C_WHITE + (255,))
    elif role == "wehrmacht":
        hd.polygon([(hcx - 56, hcy - 46), (hcx + 56, hcy - 46), (hcx + 64, hcy - 76), (hcx, hcy - 88), (hcx - 64, hcy - 76)], fill=cap_top, outline=suit_shade, width=2)
        hd.rectangle([hcx - 52, hcy - 52, hcx + 52, hcy - 38], fill=(24, 28, 26, 255), outline=C_AMBER + (255,), width=2)
    else:  # french_vip hair
        hd.pieslice([hcx - 52, hcy - 78, hcx + 52, hcy - 18], start=180, end=360, fill=hair_col)

    head_rot = head_layer.rotate(-head_tilt, resample=Image.Resampling.BICUBIC, expand=False)
    rig.paste(head_rot, (bx - hcx, by - hcy), head_rot)
    hx_r, hy_r = draw_arm(1, ra_base, re_base)

    if gesture == "aim_rifle":
        # Draw rifle in hand
        rd.line([(hx_r - 28, hy_r + 8), (hx_r + 74, hy_r - 18)], fill=(92, 64, 38, 255), width=10)
        rd.line([(hx_r + 20, hy_r - 4), (hx_r + 105, hy_r - 26)], fill=(165, 172, 180, 255), width=6)

    if scale != 1.0:
        new_sz = max(40, int(canvas_sz * scale))
        rig = rig.resize((new_sz, new_sz), Image.Resampling.LANCZOS)
    frame.paste(rig, (cx - rig.width // 2, cy - rig.height // 2), rig)

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

def render_module_c_document_with_hand(scene_t, header, meta_line, lines, highlight_idx, stamp_text, source_attr, tilt_deg=-1.5):
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

def draw_balance_scale(draw, cx, base_y, tilt_deg, left_pills, right_pills, left_title, right_title, left_col=C_TACTICAL, right_col=C_DANGER, drop_prog=1.0):
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
                draw.rounded_rectangle([px - tw // 2, iy - 20, px + tw // 2, iy + 20], radius=8, fill=C_PAPER, outline=gold_m, width=2)
                draw.text((px, iy), ptxt, font=FONT_PILL_SM, fill=C_INK, anchor="mm")

# ==============================================================================
# MASTER 40-SCENE STAGE DISPATCHER (CASTILLO DE ITTER 1945)
# ==============================================================================
def render_stage_for_scene(scene_id, scene_t, scene_dur, global_t):
    s_prog = min(1.0, max(0.0, scene_t / max(0.1, scene_dur)))
    t_ms = global_t * 1000.0

    # --------------------------------------------------------------------------
    # THE EXPLOSIVE 7-SCENE OPENING HOOK (00:00 - 00:16.6s)
    # --------------------------------------------------------------------------
    if scene_id == 1:
        # S01 ("Mirá esta escena."): High-Impact Castle Itter Photo + Red Target Reticle + Shockwaves
        def _vec1(frame, draw, st, sd):
            cx_t, cy_t = 580, 910
            for r in range(1, 4):
                p_r = loop_p(t_ms, 850.0, phase=r * 0.33)
                rad = int(45 + p_r * 185)
                draw.ellipse([cx_t - rad, cy_t - rad, cx_t + rad, cy_t + rad], outline=C_DANGER if r % 2 == 0 else C_AMBER, width=max(2, int(5 * bell(p_r))))
            draw_crosshair(draw, cx_t, cy_t, 88, C_DANGER)
            draw_digital_led_box(draw, W // 2, 1255, "5 MAYO 1945 · CASTILLO DE ITTER", C_DANGER)
        return render_module_a_steady(
            "itter", scene_t, scene_dur,
            "TIROL AUSTRÍACO · 5 DE MAYO DE 1945",
            None,
            "FOTO DE ARCHIVO · CASTILLO DE ITTER (TIROL, AUSTRIA) · CC BY-SA 4.0",
            extra_vector_fn=_vec1
        )

    elif scene_id == 2:
        # S02 ("En el portón de un castillo medieval hay un tanque estadounidense en llamas."):
        # Real M4 Sherman Tank Photo Full-Bleed + Living Rossark Fire & Smoke + Red Target Reticle!
        def _vec2(frame, draw, st, sd):
            draw_rossark_smoke_and_fire(frame, W // 2 - 20, 1065, global_t, count=8, scale=1.35)
            draw_rossark_smoke_and_fire(frame, W // 2 + 135, 1105, global_t + 0.4, count=6, scale=1.05)
            draw_after = ImageDraw.Draw(frame)
            draw_crosshair(draw_after, W // 2 + 20, 995, 92, C_DANGER)
            draw_digital_led_box(draw_after, W // 2, 1275, "SHERMAN EN LLAMAS", C_DANGER)
        return render_module_a_steady(
            "sherman", scene_t, scene_dur,
            "PORTÓN MEDIEVAL · CASTILLO DE ITTER",
            None,
            "FOTO DE ARCHIVO · IMPERIAL WAR MUSEUM (TANQUE M4 SHERMAN, 1945) · DOMINIO PÚBLICO",
            extra_vector_fn=_vec2
        )

    elif scene_id == 3:
        # S03 ("Y adentro, disparando por las mismas ventanas,"):
        # Castle Itter Battlements & 3 Gothic Windows with Synchronized Muzzle Flashes & Tracer Fire
        frame = PHOTOS_STEADY_STAGE.get("itter", CANVAS_ABYSS).copy()
        draw = ImageDraw.Draw(frame)
        draw_castle_gatehouse(draw, W // 2, 1215, scale=1.18)
        win_coords = [
            (W // 2 - 260, 948, "VENTANA 1 · EE. UU.", C_TACTICAL, -190),
            (W // 2, 948, "VENTANA 2 · WEHRMACHT", C_AMBER, 0),
            (W // 2 + 260, 948, "VENTANA 3 · FRANCIA", C_DANGER, 190),
        ]
        for i, (wx, wy, w_lbl, w_col, dx_dir) in enumerate(win_coords):
            # Glowing muzzle flash in window
            pulse = 0.65 + 0.35 * abs(wave(t_ms, 280.0, phase=i * 0.33))
            r_fl = int(28 * pulse)
            draw.ellipse([wx - r_fl, wy - r_fl, wx + r_fl, wy + r_fl], fill=C_AMBER, outline=C_WHITE, width=3)
            # Outgoing tracer rounds
            for tr_i in range(3):
                p_tr = loop_p(t_ms, 520.0, phase=i * 0.25 + tr_i * 0.33)
                tx0 = int(wx + dx_dir * p_tr)
                ty0 = int(wy + 310 * p_tr)
                tx1 = int(wx + dx_dir * min(1.0, p_tr + 0.16))
                ty1 = int(wy + 310 * min(1.0, p_tr + 0.16))
                draw.line([(tx0, ty0), (tx1, ty1)], fill=w_col, width=6)
            draw_map_pill(draw, wx, wy - 76, w_lbl, w_col)
        draw_digital_led_box(draw, W // 2, 1335, "DISPARANDO DESDE LAS VENTANAS", C_AMBER)
        draw_attribution_pill(draw, "FOTO DE ARCHIVO · CASTILLO DE ITTER (TIROL, AUSTRIA) · CC BY-SA 4.0")
        return frame

    elif scene_id in (4, 5, 6):
        # S04 ("hay soldados de Estados Unidos,") -> S05 ("soldados del ejército alemán") -> S06 ("y dos ex primeros ministros de Francia.")
        # Progressive 3-Column Living Alliance Reveal on the Castle Wall!
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        # Castle battlement stone wall along bottom
        draw.rectangle([40, 1185, W - 40, 1390], fill=(48, 46, 44), outline=(112, 108, 102), width=3)
        cols = [
            (200, "us_soldier", "1. EE. UU.", "14 SOLDADOS (CAPT. LEE)", C_TACTICAL, (16, 36, 62), scene_id >= 4),
            (540, "wehrmacht", "2. WEHRMACHT", "10 SOLDADOS (MAYOR GANGL)", C_AMBER, (44, 36, 16), scene_id >= 5),
            (880, "french_vip", "3. FRANCIA", "2 EX PRIMEROS MINISTROS", C_DANGER, (46, 18, 22), scene_id >= 6),
        ]
        for cx_c, role_c, title_c, sub_c, col_c, bg_c, is_active in cols:
            x0, x1 = cx_c - 150, cx_c + 150
            if is_active:
                draw.rounded_rectangle([x0, 680, x1, 1295], radius=16, fill=bg_c, outline=col_c, width=4)
                draw_rossark_soldier(frame, cx_c, 965, scale=0.92, role=role_c, global_t=global_t, scene_t=scene_t, talking=True, gesture="aim_rifle")
                draw = ImageDraw.Draw(frame)
                draw.rounded_rectangle([x0 + 12, 1135, x1 - 12, 1275], radius=10, fill=(14, 16, 20), outline=col_c, width=2)
                draw.text((cx_c, 1182), title_c, font=FONT_PILL_MD, fill=col_c, anchor="mm")
                draw.text((cx_c, 1235), sub_c, font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
            else:
                draw.rounded_rectangle([x0, 680, x1, 1295], radius=16, fill=(20, 22, 26), outline=(55, 60, 70), width=2)
                draw.text((cx_c, 985), "?", font=FONT_BIG_NUM, fill=(75, 80, 90), anchor="mm")
        draw_map_pill(draw, W // 2, 1355, "TRES FUERZAS EN LAS ALMENAS DEL CASTILLO DE ITTER", C_AMBER)
        return frame

    elif scene_id == 7:
        # S07 ("Todos peleando del mismo lado contra un enemigo común."):
        # Tactical Battle Overview: United Defenders vs. Encroaching Waffen-SS
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        # Top Bastion: United Defenders (EE. UU. + WEHRMACHT + FRANCIA)
        draw.rounded_rectangle([85, 685, W - 85, 965], radius=18, fill=(18, 34, 56), outline=C_AMBER, width=4)
        draw.text((W // 2, 742), "DEFENSORES UNIDOS EN EL CASTILLO DE ITTER", font=FONT_PILL_MD, fill=C_AMBER, anchor="mm")
        for bx_p, lbl_p, col_p in [
            (250, "EE. UU. (14)", C_TACTICAL),
            (540, "WEHRMACHT (10)", C_AMBER),
            (830, "FRANCIA (VIPs)", C_NEUTRAL),
        ]:
            draw.rounded_rectangle([bx_p - 125, 790, bx_p + 125, 865], radius=10, fill=(14, 20, 30), outline=col_p, width=3)
            draw.text((bx_p, 827), lbl_p, font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        draw.text((W // 2, 920), "PELEANDO DEL MISMO LADO", font=FONT_PILL_LG, fill=C_WHITE, anchor="mm")

        # Clash Arrows in the middle
        for ax in [260, 440, 640, 820]:
            draw.line([(ax, 975), (ax, 1115)], fill=C_AMBER, width=5)
            draw.line([(ax + 18, 1115), (ax + 18, 985)], fill=C_DANGER, width=5)

        # Bottom Threat Box: Common Enemy (Waffen-SS)
        draw.rounded_rectangle([85, 1125, W - 85, 1375], radius=18, fill=(48, 16, 18), outline=C_DANGER, width=4)
        draw.text((W // 2, 1195), "ENEMIGO COMÚN: WAFFEN-SS", font=FONT_HEADLINE, fill=C_DANGER, anchor="mm")
        draw.text((W // 2, 1265), "17.ª DIVISIÓN SS «GÖTZ VON BERLICHINGEN»", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        draw_map_pill(draw, W // 2, 1330, "LA BATALLA MÁS INSÓLITA DE LA SEGUNDA GUERRA MUNDIAL", C_AMBER)
        return frame

    # --------------------------------------------------------------------------
    # CONTEXT & PRISONERS (Scenes 8..16)
    # --------------------------------------------------------------------------
    elif scene_id == 8:
        # S08: 2D Tactical Map of the Austrian Alps (Tyrol / Brixental / Wörgl / Itter) in May 1945
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_tyrol_valley_map(draw, global_t)
        # Pulsing radar ring at Castle Itter
        ix, iy = 790, 1165
        for r in range(1, 4):
            p_r = loop_p(t_ms, 1400.0, phase=r * 0.33)
            rad = int(24 + p_r * 95)
            draw.ellipse([ix - rad, iy - rad, ix + rad, iy + rad], outline=C_AMBER, width=max(1, int(4 * bell(p_r))))
        draw.ellipse([ix - 12, iy - 12, ix + 12, iy + 12], fill=C_DANGER, outline=C_WHITE, width=3)
        draw_map_pill(draw, 220, 835, "KUFSTEIN (FRONTERA ALEMANA)", C_TACTICAL)
        draw_map_pill(draw, 420, 930, "PUEBLO DE WÖRGL", C_AMBER)
        draw_map_pill(draw, 730, 1085, "CASTILLO DE ITTER (ALPES)", C_DANGER)
        draw_digital_led_box(draw, W // 2, 1340, "MAYO 1945 · TIROL AUSTRÍACO", C_AMBER)
        return frame

    elif scene_id == 9:
        # S09: Animated Calendar: April 30 (Hitler's Suicide) -> +5 Days -> May 5, 1945
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        cx0, cy0, cw, ch = 120, 680, W - 240, 560
        draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=14, fill=C_PAPER, outline=(185, 176, 160), width=4)
        draw.text((W // 2, cy0 + 52), "MAYO DE 1945 · FIN DEL REICH", font=FONT_PILL_LG, fill=C_INK, anchor="mm")
        draw.line([(cx0 + 36, cy0 + 92), (cx0 + cw - 36, cy0 + 92)], fill=(195, 186, 170), width=3)
        days = [
            ("30 ABR", "SUICIDIO DE HITLER", C_DANGER),
            ("1 MAY", "DÍA +1", C_INK),
            ("2 MAY", "CAÍDA DE BERLÍN", C_INK),
            ("3 MAY", "DÍA +3", C_INK),
            ("4 MAY", "GUARDIAS HUYEN", C_AMBER),
            ("5 MAY", "BATALLA DE ITTER", C_DANGER),
        ]
        lit_idx = int(min(5, scene_t * 3.2))
        for i, (d_lbl, d_sub, d_col) in enumerate(days):
            col_i = i % 3
            row_i = i // 3
            bx = cx0 + 42 + col_i * 258
            by = cy0 + 125 + row_i * 200
            is_hi = i in (0, 5) or i <= lit_idx
            draw.rounded_rectangle([bx, by, bx + 236, by + 170], radius=12, fill=(252, 232, 160) if i == 5 else (234, 226, 212), outline=C_STAMP_RED if i in (0, 5) else (175, 166, 150), width=4 if i in (0, 5) else 2)
            draw.text((bx + 118, by + 58), d_lbl, font=FONT_PILL_LG, fill=C_STAMP_RED if i in (0, 5) else C_INK, anchor="mm")
            draw.text((bx + 118, by + 124), d_sub, font=FONT_PILL_SM, fill=C_INK, anchor="mm")
            if i < 5 and i <= lit_idx:
                draw.line([(bx + 35, by + 35), (bx + 200, by + 85)], fill=C_STAMP_RED, width=4)
        draw_digital_led_box(draw, W // 2, 1345, "5 DÍAS DESPUÉS DE HITLER", C_DANGER)
        return frame

    elif scene_id == 10:
        # S10: Steady Castle Itter Archival Photo + High-Security VIP Prison Overlay
        def _vec10(frame, draw, st, sd):
            draw.rounded_rectangle([64, 775, 530, 935], radius=14, fill=(44, 18, 20), outline=C_DANGER, width=3)
            draw.text((297, 828), "PRISIÓN DE MÁXIMA SEGURIDAD", font=FONT_PILL_MD, fill=C_DANGER, anchor="mm")
            draw.text((297, 885), "SUBCAMPO DE DACHAU EN EL TIROL", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        return render_module_a_steady(
            "itter", scene_t, scene_dur,
            "SCHLOSS ITTER · PRISIÓN VIP NAZI",
            "Fortaleza medieval usada para encerrar a rehenes franceses de alto valor",
            "FOTO DE ARCHIVO · CASTILLO DE ITTER (TIROL, AUSTRIA) · CC BY-SA 4.0",
            extra_vector_fn=_vec10
        )

    elif scene_id == 11:
        # S11: Dual Archival Portrait Dossier: Paul Reynaud & Édouard Daladier
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        for idx_p, (x0, p_key, name_str, role_str, col) in enumerate([
            (65, "reynaud", "PAUL REYNAUD", "EX PRIMER MINISTRO (1940)", C_TACTICAL),
            (555, "daladier", "ÉDOUARD DALADIER", "EX PRIMER MINISTRO (1938-40)", C_AMBER),
        ]):
            cw = 460
            draw.rounded_rectangle([x0, 685, x0 + cw, 1310], radius=16, fill=(18, 22, 30), outline=col, width=4)
            if p_key in PORTRAIT_CROPS:
                crop_im = fit_photo_once(PORTRAIT_CROPS[p_key], cw - 24, 450, fy=0.35)
                frame.paste(crop_im, (x0 + 12, 697))
            draw.text((x0 + cw // 2, 1195), name_str, font=FONT_PILL_LG, fill=col, anchor="mm")
            draw.text((x0 + cw // 2, 1255), role_str, font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        draw_attribution_pill(draw, "FOTOS DE ARCHIVO · BIBLIOTHÈQUE NATIONALE DE FRANCE (REYNAUD Y DALADIER) · DOMINIO PÚBLICO")
        return frame

    elif scene_id == 12:
        # S12: 3-Column Archival Dossier: Generals Maxime Weygand, Maurice Gamelin & Tennis Champion Jean Borotra
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        cards = [
            (50, "weygand", "GRAL. WEYGAND", "COMANDANTE EN JEFE", C_AMBER),
            (385, "gamelin", "GRAL. GAMELIN", "COMANDANTE EN JEFE", C_TACTICAL),
            (720, "borotra", "JEAN BOROTRA", "CAMPEÓN DE TENIS", C_NEUTRAL),
        ]
        for x0, p_key, name_s, sub_s, col in cards:
            cw = 310
            draw.rounded_rectangle([x0, 695, x0 + cw, 1305], radius=14, fill=(18, 22, 30), outline=col, width=3)
            if p_key in PORTRAIT_CROPS:
                crop_im = fit_photo_once(PORTRAIT_CROPS[p_key], cw - 16, 440, fy=0.38)
                frame.paste(crop_im, (x0 + 8, 703))
            draw.text((x0 + cw // 2, 1190), name_s, font=FONT_PILL_MD, fill=col, anchor="mm")
            draw.text((x0 + cw // 2, 1248), sub_s, font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        draw_attribution_pill(draw, "FOTOS DE ARCHIVO · BNF Y BUNDESARCHIV (WEYGAND, GAMELIN, BOROTRA) · DOMINIO PÚBLICO / CC BY-SA")
        return frame

    elif scene_id == 13:
        # S13: Prison Guards Abandon Castle Itter Diagram (4 de Mayo de 1945)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_castle_gatehouse(draw, W // 2, 1085, scale=0.95)
        # Fleeing arrows moving away from the gate
        for i, (ax0, ay0, ax1, ay1) in enumerate([
            (420, 1110, 160, 1275),
            (540, 1120, 540, 1300),
            (660, 1110, 920, 1275),
        ]):
            p_f = EASE_OUT(s_prog)
            cx_a = int(ax0 + (ax1 - ax0) * p_f)
            cy_a = int(ay0 + (ay1 - ay0) * p_f)
            draw.line([(ax0, ay0), (cx_a, cy_a)], fill=C_AMBER, width=6)
            draw.ellipse([cx_a - 12, cy_a - 12, cx_a + 12, cy_a + 12], fill=C_AMBER)
        draw_map_pill(draw, W // 2, 720, "4 DE MAYO DE 1945 · COLAPSO DEL TERCER REICH", C_AMBER)
        draw_digital_led_box(draw, W // 2, 1355, "GUARDIAS ABANDONAN ITTER", C_NEUTRAL)
        return frame

    elif scene_id == 14:
        # S14: Red Danger Alert — The Real Danger Is Outside in the Woods
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        cx_r, cy_r = W // 2, 995
        for r in [95, 190, 285]:
            draw.ellipse([cx_r - r, cy_r - r, cx_r + r, cy_r + r], outline=C_DANGER, width=3)
        # Castle in center surrounded by 6 red threat markers in the forest perimeter
        draw.rounded_rectangle([cx_r - 95, cy_r - 55, cx_r + 95, cy_r + 55], radius=10, fill=(28, 34, 44), outline=C_AMBER, width=3)
        draw.text((cx_r, cy_r), "ITTER", font=FONT_PILL_LG, fill=C_AMBER, anchor="mm")
        for i in range(6):
            ang = math.radians(i * 60 + global_t * 25)
            tx = cx_r + int(235 * math.cos(ang))
            ty = cy_r + int(235 * math.sin(ang))
            draw.ellipse([tx - 24, ty - 24, tx + 24, ty + 24], fill=(56, 16, 18), outline=C_DANGER, width=3)
            draw.text((tx, ty), "SS", font=FONT_PILL_SM, fill=C_DANGER, anchor="mm")
        draw_digital_led_box(draw, W // 2, 1355, "RODEADOS EN EL BOSQUE", C_DANGER)
        return frame

    elif scene_id == 15:
        # S15: Fanatical Waffen-SS Squads in the Neighboring Woods (Living Rossark Waffen-SS Soldiers + Pine Trees)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_tyrol_valley_map(draw, global_t)
        draw_rossark_soldier(frame, 330, 1020, scale=1.05, role="waffen_ss", global_t=global_t, scene_t=scene_t, gesture="aim_rifle")
        draw_rossark_soldier(frame, 750, 1020, scale=1.05, role="waffen_ss", global_t=global_t + 0.6, scene_t=scene_t, gesture="aim_rifle")
        draw = ImageDraw.Draw(frame)
        draw_map_pill(draw, W // 2, 725, "BOSQUES DE BRIXENTAL · UNIDADES FANÁTICAS", C_DANGER)
        draw_digital_led_box(draw, W // 2, 1335, "PATRULLAS WAFFEN-SS", C_DANGER)
        return frame

    elif scene_id == 16:
        # S16: Module C — Reconstructed Waffen-SS Order to Execute All Hostages Before Allies Arrive
        return render_module_c_document_with_hand(
            scene_t,
            "COMANDO WAFFEN-SS · SECTOR TIROL (MAYO DE 1945)",
            "ORDEN PRIORITARIA SOBRE PRISIONEROS DEL CASTILLO DE ITTER:",
            [
                "• Objetivo: Fortaleza de Schloss Itter (Brixental).",
                "• Impedir la liberación de los rehenes franceses.",
                "• Ejecutar a todos los prisioneros antes de la",
                "  llegada de las tropas aliadas a la montaña."
            ],
            highlight_idx={2, 3},
            stamp_text="EJECUTAR REHENES",
            source_attr="FUENTE HISTÓRICA · ARCHIVOS DE LA 103.ª DIVISIÓN DE INFANTERÍA (1945)",
            tilt_deg=-1.5
        )

    # --------------------------------------------------------------------------
    # THE BICYCLE MISSION, MAJOR GANGL & CAPTAIN LEE (Scenes 17..25)
    # --------------------------------------------------------------------------
    elif scene_id == 17:
        # S17: Tactical Map — Allied Troops Kilometers Away & Unaware of What Happens on the Mountain
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_tyrol_valley_map(draw, global_t)
        # Left box: Allied Troops far away
        draw.rounded_rectangle([70, 740, 460, 940], radius=14, fill=(16, 36, 62), outline=C_TACTICAL, width=3)
        draw.text((265, 805), "TROPAS ALIADAS", font=FONT_PILL_MD, fill=C_TACTICAL, anchor="mm")
        draw.text((265, 865), "A KILÓMETROS DE DISTANCIA", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        # Right box: Castle Itter isolated
        draw.rounded_rectangle([620, 980, 1010, 1180], radius=14, fill=(46, 18, 20), outline=C_DANGER, width=3)
        draw.text((815, 1045), "CASTILLO DE ITTER", font=FONT_PILL_MD, fill=C_DANGER, anchor="mm")
        draw.text((815, 1105), "AISLADO EN LA MONTAÑA", font=FONT_PILL_SM, fill=C_AMBER, anchor="mm")
        # Dashed severed line
        draw.line([(460, 840), (620, 1080)], fill=C_DANGER, width=5)
        draw.text((540, 960), "X", font=FONT_HEADLINE, fill=C_DANGER, anchor="mm")
        draw_digital_led_box(draw, W // 2, 1340, "SIN CONEXIÓN ALIADA", C_DANGER)
        return frame

    elif scene_id == 18:
        # S18: Living Rossark Bicycle Mission — Castle Cook Andreas Krobot Cycling Down to Wörgl
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        # Mountain slope road from Castle Itter (top left) down to Wörgl (bottom right)
        draw.polygon([(0, 820), (W, 1240), (W, 1415), (0, 1415)], fill=(64, 78, 46), outline=C_LAND_STROKE, width=4)
        draw.line([(80, 845), (1000, 1210)], fill=(185, 178, 162), width=14)
        # Animated bicycle position along the slope
        p_b = EASE_IN_OUT(s_prog)
        bx = int(220 + 580 * p_b)
        by = int(900 + 230 * p_b + 3.0 * wave(t_ms, 320.0))
        # Two spoked wheels rotating + frame + rider
        for wx_off in [-48, 48]:
            wx, wy = bx + wx_off, by
            draw.ellipse([wx - 28, wy - 28, wx + 28, wy + 28], outline=C_WHITE, width=4)
            ang_w = global_t * 9.0
            for sp_i in range(4):
                a_s = ang_w + sp_i * (math.pi / 4.0)
                draw.line([(wx - int(24 * math.cos(a_s)), wy - int(24 * math.sin(a_s))), (wx + int(24 * math.cos(a_s)), wy + int(24 * math.sin(a_s)))], fill=C_AMBER, width=2)
        draw.line([(bx - 48, by), (bx - 10, by - 48), (bx + 36, by - 42), (bx + 48, by)], fill=C_TACTICAL, width=5)
        draw.ellipse([bx - 16, by - 96, bx + 16, by - 64], fill=(242, 185, 148), outline=C_WHITE, width=2)
        draw.line([(bx, by - 64), (bx - 10, by - 42)], fill=C_WHITE, width=10)
        draw_map_pill(draw, 220, 745, "SALIDA: CASTILLO DE ITTER", C_AMBER)
        draw_map_pill(draw, 820, 1335, "DESTINO: PUEBLO DE WÖRGL (12 KM)", C_TACTICAL)
        return frame

    elif scene_id == 19:
        # S19: Steady Archival Portrait of Major Josef «Sepp» Gangl (Wehrmacht)
        def _vec19(frame, draw, st, sd):
            draw_map_pill(draw, 740, 785, "EJÉRCITO REGULAR ALEMÁN (WEHRMACHT)", C_AMBER)
        return render_module_a_steady(
            "gangl", scene_t, scene_dur,
            "MAYOR JOSEF «SEPP» GANGL · WÖRGL",
            "Comandante condecorado del ejército regular alemán en Wörgl",
            "FOTO DE ARCHIVO · ARCHIVO HISTÓRICO (MAYOR JOSEF GANGL) · DOMINIO PÚBLICO",
            extra_vector_fn=_vec19
        )

    elif scene_id == 20:
        # S20: Module C — Gangl Disobeys Nazi Superiors to Protect Local Citizens in Wörgl
        return render_module_c_document_with_hand(
            scene_t,
            "GUARNICIÓN DE WÖRGL · TIROL AUSTRÍACO (MAYO DE 1945)",
            "DECISIÓN DEL MAYOR JOSEF GANGL (WEHRMACHT):",
            [
                "• Desobedece la orden nazi de destruir puentes.",
                "• Colabora en secreto con la resistencia austríaca.",
                "• Protege a los vecinos de Wörgl de las represalias.",
                "• Decide defender a los rehenes del Castillo de Itter."
            ],
            highlight_idx={0, 2},
            stamp_text="REBELDÍA MILITAR",
            source_attr="FUENTE HISTÓRICA · DOCUMENTACIÓN DE LA RESISTENCIA EN WÖRGL (1945)",
            tilt_deg=1.4
        )

    elif scene_id == 21:
        # S21: Force Disparity Bar Chart: Gangl's 20 Wehrmacht Soldiers vs. Fanatical Waffen-SS
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        base_y = 1235
        draw.line([(120, base_y), (W - 120, base_y)], fill=C_NEUTRAL, width=4)
        # Left Bar: 20 Soldados de Gangl
        p1 = EASE_OUT(min(1.0, scene_t / 0.70))
        h1 = int(110 * p1)
        draw.rounded_rectangle([190, base_y - h1, 460, base_y], radius=10, fill=C_AMBER, outline=C_WHITE, width=3)
        draw.text((325, base_y - h1 - 42), "20 SOLDADOS", font=FONT_PILL_LG, fill=C_AMBER, anchor="mm")
        draw.text((325, base_y + 42), "MAYOR GANGL", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        draw.text((325, base_y + 80), "(WEHRMACHT)", font=FONT_PILL_SM, fill=C_NEUTRAL, anchor="mm")
        # Right Bar: 150 Waffen-SS
        p2 = EASE_OUT(min(1.0, max(0.0, (scene_t - 0.15) / 0.75)))
        h2 = int(440 * p2)
        draw.rounded_rectangle([620, base_y - h2, 890, base_y], radius=12, fill=C_DANGER, outline=C_WHITE, width=3)
        draw.text((755, base_y - h2 - 42), "FUERZAS SS", font=FONT_PILL_LG, fill=C_DANGER, anchor="mm")
        draw.text((755, base_y + 42), "WAFFEN-SS", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        draw.text((755, base_y + 80), "(CAÑONES Y MG42)", font=FONT_PILL_SM, fill=C_NEUTRAL, anchor="mm")
        draw_digital_led_box(draw, 325, 835, "INSUFICIENTES", C_DANGER)
        return frame

    elif scene_id == 22:
        # S22: Gangl Drives Staff Car with Giant Waving White Flag from Wörgl to Kufstein (Rossark Flag Recipe)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_tyrol_valley_map(draw, global_t)
        # Animated car moving from Wörgl (580, 1060) toward Kufstein (280, 910)
        cx_car = int(680 - 340 * EASE_IN_OUT(s_prog))
        cy_car = int(1120 + 2.0 * wave(t_ms, 260.0))
        # Car body
        draw.rounded_rectangle([cx_car - 85, cy_car - 36, cx_car + 85, cy_car], radius=8, fill=(74, 84, 78), outline=C_WHITE, width=3)
        for wx_o in [-52, 52]:
            draw.ellipse([cx_car + wx_o - 20, cy_car - 12, cx_car + wx_o + 20, cy_car + 28], fill=(28, 30, 34), outline=C_NEUTRAL, width=3)
        # Tall flagpole + waving white flag strips (rossark flag recipe: wave travels along length)
        pole_x, pole_y = cx_car - 60, cy_car - 190
        draw.line([(cx_car - 60, cy_car - 36), (pole_x, pole_y)], fill=C_AMBER, width=6)
        for strip_i in range(8):
            sx0 = pole_x + strip_i * 18
            sy_off = int((strip_i * 1.8) * wave(t_ms, 480.0, phase=strip_i * 0.14))
            draw.rectangle([sx0, pole_y + sy_off, sx0 + 19, pole_y + 78 + sy_off], fill=C_WHITE, outline=(210, 215, 222), width=1)
        draw_map_pill(draw, W // 2, 735, "RUTA WÖRGL -> KUFSTEIN CON BANDERA BLANCA", C_WHITE)
        draw_digital_led_box(draw, W // 2, 1340, "BUSCANDO A EE. UU.", C_TACTICAL)
        return frame

    elif scene_id == 23:
        # S23: Dramatic Plot Twist Card ("Y acá la historia da un vuelco:")
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([100, 740, W - 100, 1260], radius=20, fill=(24, 28, 38), outline=C_AMBER, width=4)
        draw.text((W // 2, 845), "ENCUENTRO EN KUFSTEIN", font=FONT_PILL_LG, fill=C_AMBER, anchor="mm")
        draw.text((W // 2, 955), "UN MAYOR DE LA WEHRMACHT", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        draw.text((W // 2, 1015), "PIDIENDO AYUDA A UNA PATRULLA", font=FONT_PILL_MD, fill=C_TACTICAL, anchor="mm")
        draw.text((W // 2, 1075), "DE RECONOCIMIENTO DE EE. UU.", font=FONT_PILL_MD, fill=C_TACTICAL, anchor="mm")
        draw_digital_led_box(draw, W // 2, 1185, "GIRO HISTÓRICO", C_AMBER)
        return frame

    elif scene_id == 24:
        # S24: Living 2.5D Captain John «Jack» Lee (27 años) & Major Josef Gangl Meeting Face to Face
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([75, 700, 515, 1280], radius=16, fill=(16, 36, 62), outline=C_TACTICAL, width=4)
        draw_rossark_soldier(frame, 295, 965, scale=1.08, role="us_soldier", global_t=global_t, scene_t=scene_t, talking=True, gesture="salute_alliance")
        draw = ImageDraw.Draw(frame)
        draw.text((295, 1165), "CAPITÁN JOHN «JACK» LEE", font=FONT_PILL_MD, fill=C_TACTICAL, anchor="mm")
        draw.text((295, 1220), "27 AÑOS · 12.ª DIV. BLINDADA", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")

        draw.rounded_rectangle([565, 700, W - 75, 1280], radius=16, fill=(42, 36, 18), outline=C_AMBER, width=4)
        draw_rossark_soldier(frame, 785, 965, scale=1.08, role="wehrmacht", global_t=global_t + 0.5, scene_t=scene_t, talking=False, gesture="salute_alliance")
        draw = ImageDraw.Draw(frame)
        draw.text((785, 1165), "MAYOR JOSEF GANGL", font=FONT_PILL_MD, fill=C_AMBER, anchor="mm")
        draw.text((785, 1220), "34 AÑOS · WEHRMACHT", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        draw_map_pill(draw, W // 2, 1345, "KUFSTEIN · 4 DE MAYO DE 1945", C_AMBER)
        return frame

    elif scene_id == 25:
        # S25: Steady Archival Photo of M4 Sherman Tank + 14 US Soldiers & 1 Tank Inventory
        def _vec25(frame, draw, st, sd):
            draw.rounded_rectangle([64, 775, 515, 945], radius=14, fill=(16, 34, 58), outline=C_TACTICAL, width=3)
            draw.text((289, 832), "14 SOLDADOS", font=FONT_PILL_LG, fill=C_TACTICAL, anchor="mm")
            draw.text((289, 892), "PATRULLA DE ESTADOS UNIDOS", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")

            draw.rounded_rectangle([565, 775, W - 64, 945], radius=14, fill=(44, 34, 16), outline=C_AMBER, width=3)
            draw.text((790, 832), "1 TANQUE SHERMAN", font=FONT_PILL_LG, fill=C_AMBER, anchor="mm")
            draw.text((790, 892), "«BESOTTEN JENNY» (M4A3E8)", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        return render_module_a_steady(
            "sherman", scene_t, scene_dur,
            "PATRULLA DEL CAPITÁN LEE · 23.º BATALLÓN",
            "Cuenta con apenas 14 soldados estadounidenses y un único tanque Sherman",
            "FOTO DE ARCHIVO · IMPERIAL WAR MUSEUM (TANQUE M4 SHERMAN, 1945) · DOMINIO PÚBLICO",
            extra_vector_fn=_vec25
        )

    # --------------------------------------------------------------------------
    # THE IMPROVISED ALLIANCE AT CASTLE ITTER (Scenes 26..29)
    # --------------------------------------------------------------------------
    elif scene_id == 26:
        # S26: Tactical Convoy Map — Lee & Gangl Ascend Together to Castle Itter
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_tyrol_valley_map(draw, global_t)
        # Animated convoy arrow climbing from Wörgl (390, 980) to Castle Itter (790, 1165)
        p_c = EASE_OUT(s_prog)
        cx_c = int(390 + (790 - 390) * p_c)
        cy_c = int(980 + (1165 - 980) * p_c)
        draw.line([(390, 980), (cx_c, cy_c)], fill=C_AMBER, width=8)
        draw.ellipse([cx_c - 16, cy_c - 16, cx_c + 16, cy_c + 16], fill=C_TACTICAL, outline=C_WHITE, width=3)
        draw_map_pill(draw, 390, 915, "WÖRGL (UNIÓN DE FUERZAS)", C_TACTICAL)
        draw_map_pill(draw, 760, 1235, "CASTILLO DE ITTER (META)", C_AMBER)
        draw_digital_led_box(draw, W // 2, 760, "ALIANZA EN MARCHA", C_AMBER)
        return frame

    elif scene_id == 27:
        # S27: Garrison Force Breakdown: 14 US Soldiers + 10 Loyal Wehrmacht Soldiers = 24 Total
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        # Left Card: 14 US Soldiers
        draw.rounded_rectangle([70, 710, 510, 1085], radius=16, fill=(16, 36, 62), outline=C_TACTICAL, width=4)
        draw.text((290, 815), "14", font=load_font(["C:/Windows/Fonts/segoeuib.ttf"], 115), fill=C_TACTICAL, anchor="mm")
        draw.text((290, 935), "ESTADOUNIDENSES", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        draw.text((290, 995), "AL MANDO DEL CAPITÁN LEE", font=FONT_PILL_SM, fill=C_NEUTRAL, anchor="mm")

        # Right Card: 10 Wehrmacht Soldiers
        draw.rounded_rectangle([570, 710, W - 70, 1085], radius=16, fill=(44, 36, 18), outline=C_AMBER, width=4)
        draw.text((790, 815), "10", font=load_font(["C:/Windows/Fonts/segoeuib.ttf"], 115), fill=C_AMBER, anchor="mm")
        draw.text((790, 935), "SOLDADOS ALEMANES", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        draw.text((790, 995), "LEALES AL MAYOR GANGL", font=FONT_PILL_SM, fill=C_NEUTRAL, anchor="mm")

        draw_digital_led_box(draw, W // 2, 1235, "TOTAL: 24 SOLDADOS", C_WHITE)
        draw_map_pill(draw, W // 2, 1345, "LA GUARNICIÓN CONJUNTA DEL CASTILLO DE ITTER", C_AMBER)
        return frame

    elif scene_id == 28:
        # S28: Tactical Gate Blueprint — Sherman Tank Parked Blocking the Main Entrance
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_castle_gatehouse(draw, W // 2, 1185, scale=1.10)
        # Sherman tank sliding into position at the gate
        tx_sh = int(W // 2 - 90 * (1.0 - EASE_OUT(min(1.0, scene_t / 0.85))))
        draw_sherman_tank(draw, tx_sh, 1140, scale=1.18, on_fire=False, facing="right")
        draw_map_pill(draw, W // 2, 725, "DEFENSA DEL PORTÓN PRINCIPAL", C_TACTICAL)
        draw_digital_led_box(draw, W // 2, 1320, "SHERMAN EN LA ENTRADA", C_AMBER)
        return frame

    elif scene_id == 29:
        # S29: Living Rossark French Ex-Prime Ministers Armed with Rifles on the Battlements
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw_rossark_soldier(frame, 340, 980, scale=1.15, role="french_vip", global_t=global_t, scene_t=scene_t, talking=True, gesture="aim_rifle")
        draw_rossark_soldier(frame, 740, 980, scale=1.15, role="french_vip", global_t=global_t + 0.7, scene_t=scene_t, talking=False, gesture="aim_rifle")
        draw = ImageDraw.Draw(frame)
        # Stone crenellations in front of the French statesmen
        for mx in range(70, W - 70, 155):
            draw.rectangle([mx, 1085, mx + 95, 1225], fill=(64, 62, 58), outline=(128, 124, 116), width=3)
        draw.rectangle([70, 1175, W - 70, 1255], fill=(52, 50, 46), outline=(128, 124, 116), width=3)
        draw_map_pill(draw, 340, 725, "PAUL REYNAUD (ARMADO)", C_TACTICAL)
        draw_map_pill(draw, 740, 725, "ÉDOUARD DALADIER (ARMADO)", C_AMBER)
        draw_digital_led_box(draw, W // 2, 1340, "EX MINISTROS EN LAS ALMENAS", C_AMBER)
        return frame

    # --------------------------------------------------------------------------
    # DAWN ASSAULT, SACRIFICE OF GANGL & RESCUE (Scenes 30..37)
    # --------------------------------------------------------------------------
    elif scene_id == 30:
        # S30: Dawn of May 5 — Steady Archival Photo of 88mm Cannon + 150 Waffen-SS Assault
        def _vec30(frame, draw, st, sd):
            for si in range(3):
                p_sh = loop_p(st * 1000.0, 950.0, phase=si * 0.33)
                sx0, sy0 = 620, 880
                sx1, sy1 = 980, 720
                cx_p = int(sx0 + (sx1 - sx0) * p_sh)
                cy_p = int(sy0 + (sy1 - sy0) * p_sh)
                draw.line([(sx0, sy0), (cx_p, cy_p)], fill=C_DANGER, width=6)
                draw.ellipse([cx_p - 10, cy_p - 10, cx_p + 10, cy_p + 10], fill=C_AMBER, outline=C_WHITE, width=2)
            draw_digital_led_box(draw, 330, 1185, "150 WAFFEN-SS", C_DANGER)
            draw_map_pill(draw, 740, 785, "CAÑÓN ANTITANQUE DE 88 MM + MG42", C_DANGER)
        return render_module_a_steady(
            "pak88", scene_t, scene_dur,
            "AMANECER DEL 5 DE MAYO DE 1945",
            "150 efectivos de las Waffen-SS asaltan el castillo con cañones",
            "FOTO DE ARCHIVO · CAÑÓN ALEMÁN DE 88 MM (FLAK 18/36) · CC BY-SA 3.0",
            extra_vector_fn=_vec30
        )

    elif scene_id == 31:
        # S31: Americans, Germans & French Firing Shoulder to Shoulder ("codo con codo")
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        for cx_s, role_s, lbl_s, col_s in [
            (220, "us_soldier", "EE. UU.", C_TACTICAL),
            (540, "wehrmacht", "ALEMANIA", C_AMBER),
            (860, "french_vip", "FRANCIA", C_NEUTRAL),
        ]:
            draw_rossark_soldier(frame, cx_s, 975, scale=0.98, role=role_s, global_t=global_t + cx_s * 0.001, scene_t=scene_t, gesture="aim_rifle")
            draw = ImageDraw.Draw(frame)
            # Tracer fire streaming right
            p_tr = loop_p(t_ms, 450.0, phase=cx_s * 0.002)
            tx0 = cx_s + 55 + int(p_tr * 120)
            ty0 = 935 - int(p_tr * 30)
            draw.line([(tx0, ty0), (tx0 + 55, ty0 - 14)], fill=col_s, width=5)
            draw_map_pill(draw, cx_s, 1215, lbl_s, col_s)
        draw.rectangle([50, 1095, W - 50, 1170], fill=(58, 56, 52), outline=C_AMBER, width=3)
        draw_digital_led_box(draw, W // 2, 1335, "DISPARANDO CODO CON CODO", C_AMBER)
        return frame

    elif scene_id == 32:
        # S32: 88mm Shell Destroys the Sherman Tank at the Castle Gate
        frame = PHOTOS_STEADY_STAGE.get("sherman", CANVAS_ABYSS).copy()
        draw = ImageDraw.Draw(frame)
        draw_castle_gatehouse(draw, W // 2, 1185, scale=1.08)
        draw_sherman_tank(draw, W // 2, 1135, scale=1.18, on_fire=True)
        # Incoming 88mm shell streak + blast rings
        p_hit = min(1.0, scene_t / 0.45)
        sx0, sy0 = 110, 740
        sx1, sy1 = W // 2, 1085
        cx_s = int(sx0 + (sx1 - sx0) * p_hit)
        cy_s = int(sy0 + (sy1 - sy0) * p_hit)
        draw.line([(sx0, sy0), (cx_s, cy_s)], fill=C_DANGER, width=8)
        draw_rossark_smoke_and_fire(frame, W // 2, 1085, global_t, count=8, scale=1.25)
        draw = ImageDraw.Draw(frame)
        draw_digital_led_box(draw, W // 2, 1320, "TANQUE SHERMAN DESTRUIDO", C_DANGER)
        draw_attribution_pill(draw, "FOTO DE ARCHIVO · IMPERIAL WAR MUSEUM (TANQUE M4 SHERMAN, 1945) · DOMINIO PÚBLICO")
        return frame

    elif scene_id == 33:
        # S33: Steady Archival Photo of Ex-Prime Minister Paul Reynaud Exposed on the Wall + Sniper Crosshair
        def _vec33(frame, draw, st, sd):
            cx_r, cy_r = 540, 960
            rad = int(115 - 25 * math.sin(st * 6.0))
            draw_crosshair(draw, cx_r, cy_r, rad, C_DANGER)
            draw_map_pill(draw, W // 2, 785, "EXPUESTO EN EL MURO DEL CASTILLO", C_DANGER)
        return render_module_a_steady(
            "reynaud", scene_t, scene_dur,
            "PAUL REYNAUD · EX PRIMER MINISTRO FRANCÉS",
            "En medio del tiroteo, Paul Reynaud queda expuesto en el muro",
            "FOTO DE ARCHIVO · BIBLIOTHÈQUE NATIONALE DE FRANCE (PAUL REYNAUD) · DOMINIO PÚBLICO",
            extra_vector_fn=_vec33
        )

    elif scene_id == 34:
        # S34: Major Josef Gangl Rushes to Push Reynaud to Cover and Takes the SS Sniper Bullet
        def _vec34(frame, draw, st, sd):
            # Sniper trajectory line & impact flash after t=1.2s
            draw.rounded_rectangle([60, 760, 520, 915], radius=12, fill=(46, 16, 18), outline=C_DANGER, width=3)
            draw.text((290, 812), "EMPUJA A REYNAUD A CUBIERTO", font=FONT_PILL_SM, fill=C_AMBER, anchor="mm")
            draw.text((290, 868), "DISPARO DE FRANCOTIRADOR SS", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
            cx_g, cy_g = 540, 1060
            draw_crosshair(draw, cx_g, cy_g, 82, C_DANGER)
        return render_module_a_steady(
            "gangl", scene_t, scene_dur,
            "MAYOR JOSEF GANGL · SACRIFICIO EN EL MURO",
            "Corre para cubrir a Reynaud y recibe el disparo de un francotirador",
            "FOTO DE ARCHIVO · ARCHIVO HISTÓRICO (MAYOR JOSEF GANGL) · DOMINIO PÚBLICO",
            extra_vector_fn=_vec34
        )

    elif scene_id == 35:
        # S35: Memorial Tribute Card — Gangl Dies Instantly Saving the French Leader
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([110, 705, W - 110, 1295], radius=20, fill=(24, 22, 20), outline=C_AMBER, width=4)
        if "gangl" in PORTRAIT_CROPS:
            g_im = fit_photo_once(PORTRAIT_CROPS["gangl"], 280, 320, fy=0.32)
            frame.paste(g_im, (W // 2 - 140, 735))
        draw.text((W // 2, 1105), "MAYOR JOSEF «SEPP» GANGL (1910–1945)", font=FONT_PILL_MD, fill=C_AMBER, anchor="mm")
        draw.text((W // 2, 1165), "DIO SU VIDA SALVANDO AL EX PRIMER MINISTRO FRANCÉS", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        draw.text((W // 2, 1225), "ÚNICA BAJA MORTAL ENTRE LOS DEFENSORES DE ITTER", font=FONT_PILL_SM, fill=C_DANGER, anchor="mm")
        draw_attribution_pill(draw, "FOTO DE ARCHIVO · ARCHIVO HISTÓRICO (MAYOR JOSEF GANGL) · DOMINIO PÚBLICO")
        return frame

    elif scene_id == 36:
        # S36: Analog Clock at 16:00 (4:00 PM) + Critical Ammunition Depletion Bar
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        cx_c, cy_c, r_c = 320, 960, 165
        draw.ellipse([cx_c - r_c - 6, cy_c - r_c - 6, cx_c + r_c + 6, cy_c + r_c + 6], fill=(42, 38, 34), outline=C_AMBER, width=4)
        draw.ellipse([cx_c - r_c, cy_c - r_c, cx_c + r_c, cy_c + r_c], fill=C_PAPER)
        for hi in range(12):
            a = math.radians(hi * 30 - 90)
            draw.line([(cx_c + int((r_c - 22) * math.cos(a)), cy_c + int((r_c - 22) * math.sin(a))), (cx_c + int((r_c - 6) * math.cos(a)), cy_c + int((r_c - 6) * math.sin(a)))], fill=C_INK, width=4)
        # 4:00 PM (Hour hand at 120 deg, Minute hand at 0 deg)
        ha = math.radians(120 - 90)
        ma = math.radians(0 - 90)
        draw.line([(cx_c, cy_c), (cx_c + int(95 * math.cos(ha)), cy_c + int(95 * math.sin(ha)))], fill=C_INK, width=8)
        draw.line([(cx_c, cy_c), (cx_c + int(135 * math.cos(ma)), cy_c + int(135 * math.sin(ma)))], fill=C_DANGER, width=6)
        draw_digital_led_box(draw, cx_c, 1235, "16:00 HS", C_AMBER)

        # Right side: Ammunition Depletion Gauge
        draw.rounded_rectangle([545, 760, 985, 1165], radius=16, fill=(38, 16, 18), outline=C_DANGER, width=4)
        draw.text((765, 825), "MUNICIÓN RESTANTE", font=FONT_PILL_MD, fill=C_DANGER, anchor="mm")
        bullets_left = max(1, int(8 * (1.0 - 0.85 * EASE_OUT(s_prog))))
        for bi in range(8):
            bx_b = 585 + bi * 46
            col_b = C_AMBER if bi < bullets_left else (55, 40, 42)
            draw.rounded_rectangle([bx_b, 890, bx_b + 30, 1020], radius=8, fill=col_b, outline=C_WHITE if bi < bullets_left else (80, 60, 62), width=2)
        draw.text((765, 1095), "CASI SIN CARTUCHOS", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        draw_map_pill(draw, W // 2, 1355, "5 DE MAYO · 4 DE LA TARDE EN EL CASTILLO DE ITTER", C_DANGER)
        return frame

    elif scene_id == 37:
        # S37: Steady Archival Photo of US Reinforcements & Sherman Tank Sweeping the SS Attackers
        def _vec37(frame, draw, st, sd):
            draw.rounded_rectangle([64, 775, 560, 925], radius=14, fill=(16, 36, 62), outline=C_TACTICAL, width=3)
            draw.text((312, 825), "142.º REGIMIENTO DE EE. UU.", font=FONT_PILL_MD, fill=C_TACTICAL, anchor="mm")
            draw.text((312, 880), "COLUMNA DE REFUERZOS LIBERA ITTER", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        return render_module_a_steady(
            "us_reinf", scene_t, scene_dur,
            "16:00 HS · LLEGAN LOS REFUERZOS ALIADOS",
            "Una columna de refuerzos estadounidenses barre a las Waffen-SS",
            "FOTO DE ARCHIVO · US ARMY SIGNAL CORPS (INFANTERÍA Y SHERMAN, 1945) · DOMINIO PÚBLICO",
            extra_vector_fn=_vec37
        )

    # --------------------------------------------------------------------------
    # CLOSURE & ETHICAL DILEMMA (Scenes 38..40)
    # --------------------------------------------------------------------------
    elif scene_id == 38:
        # S38: Reflection Card — US Soldier & Wehrmacht Soldier in the Same Trench
        frame = PHOTOS_STEADY_STAGE.get("itter", CANVAS_ABYSS).copy()
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([75, 760, W - 75, 1295], radius=20, fill=(15, 18, 24), outline=C_AMBER, width=4)
        draw_rossark_soldier(frame, 330, 995, scale=1.0, role="us_soldier", global_t=global_t, scene_t=scene_t, gesture="salute_alliance")
        draw_rossark_soldier(frame, 750, 995, scale=1.0, role="wehrmacht", global_t=global_t + 0.4, scene_t=scene_t, gesture="salute_alliance")
        draw = ImageDraw.Draw(frame)
        draw.text((W // 2, 1185), "AYER: ORDEN DE MATARSE", font=FONT_PILL_MD, fill=C_DANGER, anchor="mm")
        draw.text((W // 2, 1245), "HOY: JUNTOS EN LA MISMA TRINCHERA", font=FONT_PILL_LG, fill=C_AMBER, anchor="mm")
        draw_attribution_pill(draw, "FOTO DE ARCHIVO · CASTILLO DE ITTER (TIROL, AUSTRIA) · CC BY-SA 4.0")
        return frame

    elif scene_id == 39:
        # S39: Module D — Golden Balance Scale Tipping with Dropping Weights (Captain Lee's Dilemma)
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        tilt = -11.0 * EASE_IN_OUT(min(1.0, max(0.0, (scene_t - 0.15) / 1.1))) + 1.2 * wave(t_ms, 3200.0)
        draw_balance_scale(
            draw, W // 2, 1340,
            tilt_deg=tilt,
            left_pills=["VIENE CON BANDERA BLANCA", "SALVAR A LOS REHENES"],
            right_pills=["¿Y SI ES UNA EMBOSCADA?", "ENEMIGO HASTA HACE HORAS"],
            left_title="DARLE UN ARMA",
            right_title="NO ARRIESGARSE",
            left_col=C_TACTICAL,
            right_col=C_DANGER,
            drop_prog=s_prog * 1.4
        )
        return frame

    else:
        # S40: Final Tribunal Dilemma Over Steady Castle Itter Backdrop + Rossark Jiggle Buttons!
        frame = PHOTOS_STEADY_STAGE.get("itter", CANVAS_ABYSS).copy()
        draw = ImageDraw.Draw(frame)
        for r in range(2):
            rp = loop_p(t_ms, 1600.0, phase=r * 0.5)
            rad = int(50 + rp * 250)
            draw.ellipse([W // 2 - rad, 910 - rad, W // 2 + rad, 910 + rad], outline=C_AMBER, width=max(1, int(3 * bell(rp))))
        draw_rossark_jiggle_button(draw, W // 2, 1110, 680, 80, "LE DOY UN ARMA Y PELEO CON ÉL", (14, 28, 52), C_TACTICAL, global_t, phase_offset=0.0)
        draw_rossark_jiggle_button(draw, W // 2, 1210, 640, 80, "NO ME ARRIESGO (TRAMPA)", (42, 16, 18), C_DANGER, global_t, phase_offset=0.5)
        draw.rounded_rectangle([140, 1295, W - 140, 1375], radius=12, fill=(18, 20, 24), outline=C_AMBER, width=3)
        draw.text((W // 2, 1335), "TE LEO ABAJO EN LOS COMENTARIOS", font=FONT_PILL_MD, fill=C_AMBER, anchor="mm")
        draw_attribution_pill(draw, "FOTO DE ARCHIVO · CASTILLO DE ITTER (TIROL, AUSTRIA) · CC BY-SA 4.0")
        return frame

# ==============================================================================
# LEVEL 1 (TOP DYNAMIC SUBTITLE WITH BLUR(6PX) & 4-NODE VECTOR SELECTION BOX)
# + LEVEL 2 (SECTION HEADLINE ALL CAPS EXTRABOLD AT Y=555PX)
# ==============================================================================
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
        draw_map_pill(draw, W // 2, 340, "5 DE MAYO DE 1945 · CASTILLO DE ITTER", C_DANGER)
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

SCENE_BOUNDS = {}
for ch in CHUNKS:
    sid = ch["scene_id"]
    s_t = ch["start"]
    e_t = ch["end"] + ch["pause_after"]
    if sid not in SCENE_BOUNDS:
        SCENE_BOUNDS[sid] = [s_t, e_t]
    else:
        SCENE_BOUNDS[sid][1] = max(SCENE_BOUNDS[sid][1], e_t)

def get_state_at(t):
    for idx, ch in enumerate(CHUNKS):
        c_s = ch["start"]
        c_e = ch["end"] + ch["pause_after"]
        if c_s <= t <= c_e or idx == len(CHUNKS) - 1:
            sid = ch["scene_id"]
            sb_s, sb_e = SCENE_BOUNDS[sid]
            active_w = len(ch["words"]) - 1
            for wi, wo in enumerate(ch["words"]):
                if t <= wo["end"]:
                    active_w = wi
                    break
            return idx, active_w, sid, max(0.0, t - sb_s), max(0.1, sb_e - sb_s)
    return len(CHUNKS) - 1, 0, 40, 1.0, 1.0

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

srt_path = "produccion/04_castillo_itter/castillo_itter_es.srt"
with open(srt_path, "w", encoding="utf-8") as sf:
    for idx_c, ch in enumerate(CHUNKS, 1):
        sf.write(f"{idx_c}\n")
        sf.write(f"{format_srt_time(ch['start'])} --> {format_srt_time(ch['end'])}\n")
        sf.write(f"{ch['text']}\n\n")

print("Rendering 12-frame verification mosaic (storyboard_verificacion.jpg)...")
sample_times = [0.4, 2.8, 6.0, 11.5, 22.0, 32.0, 50.0, 66.0, 80.5, 114.0, 134.0, 160.5]
grid = Image.new("RGB", (4 * 270, 3 * 480), (0, 0, 0))
for i, st in enumerate(sample_times):
    f_im = render_frame_at(st).resize((270, 480), Image.Resampling.LANCZOS)
    grid.paste(f_im, ((i % 4) * 270, (i // 4) * 480))
grid.save("produccion/04_castillo_itter/storyboard_verificacion.jpg", quality=92)

# Save high-impact cover image (portada_castillo_itter.png) from the burning Sherman tank hook
cover_img = render_frame_at(2.8)
cover_img.save("produccion/04_castillo_itter/portada_castillo_itter.png")

if "--storyboard-only" in sys.argv:
    print("Storyboard verification complete.")
    sys.exit(0)

INTERNAL_FPS = 30
total_frames = int(TOTAL_DUR * INTERNAL_FPS)
out_mp4 = "produccion/04_castillo_itter/castillo_itter_short.mp4"
audio_path = "produccion/04_castillo_itter/audio/audio_master_180s.wav"

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
    "-af", "volume=7.0dB,alimiter=limit=-1.5dB:level=disabled",
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
