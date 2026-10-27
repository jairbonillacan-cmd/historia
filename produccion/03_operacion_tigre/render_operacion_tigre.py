import os
import sys
import json
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1920

with open("produccion/03_operacion_tigre/timeline_chunks.json", "r", encoding="utf-8") as f:
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
    "produccion/03_operacion_tigre/assets/fonts/Inter-Regular.ttf",
    "produccion/01_submarino_b59/assets/fonts/Inter-Regular.ttf",
    "C:/Windows/Fonts/segoeui.ttf"
], 46)
FONT_SUB_BOLD = load_font([
    "C:/Windows/Fonts/segoeuib.ttf",
    "produccion/03_operacion_tigre/assets/fonts/Montserrat-Bold.ttf"
], 46)

FONT_HEADLINE = load_font(["C:/Windows/Fonts/segoeuib.ttf"], 54)
FONT_SUBHEAD = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 23)
FONT_HUD = load_font(["C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/courbd.ttf"], 18)
FONT_RIBBON = load_font(["C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/consolab.ttf"], 24)
FONT_DOC_HDR = load_font(["C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/consolab.ttf"], 22)
FONT_DOC_META = load_font(["C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/consolab.ttf"], 24)
FONT_DOC_LINE = load_font(["C:/Windows/Fonts/cour.ttf", "C:/Windows/Fonts/consola.ttf"], 25)
FONT_DOC_BOLD = load_font(["C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/consolab.ttf"], 25)
FONT_STAMP = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 28)
FONT_FOOTER = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 15)
FONT_ATTR = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 17)

FONT_PILL_LG = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 30)
FONT_PILL_MD = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 23)
FONT_PILL_SM = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 19)
FONT_LED_MD = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 46)
FONT_BIG_NUM = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 68)
FONT_GIANT = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 122)

# Palette tokens
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

def spring_val(t_sec, delay_sec=0.0, stiffness=150.0, damping=15.0):
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

def EASE_IN_OUT(p): return _cubic_bezier(p, 0.77, 0.0, 0.175, 1.0)
def EASE_OUT(p): return _cubic_bezier(p, 0.23, 1.0, 0.32, 1.0)
def EASE_IN(p): return _cubic_bezier(p, 0.55, 0.0, 1.0, 0.45)

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
    if t_ms <= k[0][0]: return float(k[0][1])
    if t_ms >= k[-1][0]: return float(k[-1][1])
    i = 0
    while i + 1 < n - 1 and k[i + 1][0] < t_ms:
        i += 1
    def slope(j):
        denom = k[j + 1][0] - k[j][0]
        return (k[j + 1][1] - k[j][1]) / denom if denom > 0 else 0.0
    def tangent(j):
        if j == 0 or j == n - 1: return 0.0
        a, b = slope(j - 1), slope(j)
        if a * b <= 0: return 0.0
        h0, h1 = k[j][0] - k[j - 1][0], k[j + 1][0] - k[j][0]
        w0, w1 = 2.0 * h1 + h0, h1 + 2.0 * h0
        return (w0 + w1) / (w0 / a + w1 / b)
    h = k[i + 1][0] - k[i][0]
    s = (t_ms - k[i][0]) / h if h > 0 else 0.0
    s2, s3 = s * s, s * s * s
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

# Base Canvases with Tactical Grid
def make_abyss_canvas():
    img = Image.new("RGB", (W, H), C_ABYSS)
    pix = img.load()
    cx, cy = W / 2.0, H * 0.52
    max_d = math.hypot(cx, cy)
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            d = math.hypot(x - cx, y - cy) / max_d
            t = max(0.0, min(1.0, 1.0 - d)) ** 1.3
            r, g, b = int(11 + 16 * t), int(13 + 20 * t), int(16 + 28 * t)
            pix[x, y] = (r, g, b)
            if x + 1 < W: pix[x + 1, y] = (r, g, b)
            if y + 1 < H: pix[x, y + 1] = (r, g, b)
            if x + 1 < W and y + 1 < H: pix[x + 1, y + 1] = (r, g, b)
    d = ImageDraw.Draw(img)
    for gx in range(60, W, 90):
        d.line([(gx, 650), (gx, 1430)], fill=(22, 28, 38), width=1)
    for gy in range(680, 1430, 90):
        d.line([(40, gy), (W - 40, gy)], fill=(22, 28, 38), width=1)
    return img

CANVAS_ABYSS = make_abyss_canvas()

def make_tactical_ocean_canvas():
    img = CANVAS_ABYSS.copy()
    stage = Image.new("RGB", (W, 820), C_OCEAN_DARK)
    sd = ImageDraw.Draw(stage)
    for gx in range(0, W, 60):
        sd.line([(gx, 0), (gx, 820)], fill=(24, 54, 92), width=1)
    for gy in range(0, 820, 60):
        sd.line([(0, gy), (W, gy)], fill=(24, 54, 92), width=1)
    mask = Image.new("L", (W, 820), 255)
    md = ImageDraw.Draw(mask)
    for y in range(110):
        md.line([(0, y), (W, y)], fill=int(255 * (y / 110.0)))
    for y in range(690, 820):
        md.line([(0, y), (W, y)], fill=int(255 * (1.0 - (y - 690) / 130.0)))
    img.paste(stage, (0, 640), mask)
    return img

CANVAS_TACTICAL_MAP = make_tactical_ocean_canvas()

STAGE_FEATHER_MASK = Image.new("L", (W, 760), 255)
_fdraw = ImageDraw.Draw(STAGE_FEATHER_MASK)
for _y in range(105):
    _fdraw.line([(0, _y), (W, _y)], fill=int(255 * (_y / 105.0)))
for _y in range(645, 760):
    _fdraw.line([(0, _y), (W, _y)], fill=int(255 * (1.0 - (_y - 645) / 115.0)))

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
ASSETS_DIR = "produccion/03_operacion_tigre/assets"
PHOTOS_STEADY_STAGE = {}
PHOTOS_RAW_CROP = {}

for key, fname, fy_val in [
    ("slapton", "slapton_sands.jpg", 0.50),
    ("eisenhower", "eisenhower_1944.jpg", 0.35),
    ("utah", "utah_beach_1944.jpg", 0.50),
    ("hawkins", "hms_hawkins.jpg", 0.50),
    ("lst_convoy", "lst_convoy_1944.jpg", 0.52),
    ("lst_burning", "lst_burning.jpg", 0.52),
    ("s_boot", "s_boot_1944.jpg", 0.48),
    ("sherman", "sherman_slapton.jpg", 0.50),
]:
    p = os.path.join(ASSETS_DIR, fname)
    if os.path.exists(p):
        im = Image.open(p).convert("RGB")
        im = ImageEnhance.Contrast(im).enhance(1.10)
        PHOTOS_RAW_CROP[key] = fit_photo_once(im, 480, 340, fy=fy_val)
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
    1:  ("28 DE ABRIL DE 1944 · ALERTA", "CANAL DE LA MANCHA · OPERACIÓN TIGRE", "danger"),
    2:  ("5 SEMANAS ANTES DEL DÍA D", "CUENTA REGRESIVA · OPERACIÓN OVERLORD", "amber"),
    3:  ("PLAYA DE SLAPTON SANDS", "OBJETIVO DE ENSAYO · SUR DE INGLATERRA", "tactical"),
    4:  ("750 SOLDADOS MUERTOS EN HORAS", "CATASTROFE EN EL CANAL DE LA MANCHA", "danger"),
    5:  ("NO ESTÁN EN FRANCIA", "LEJOS DEL FRENTE DE COMBATE REAL", "danger"),
    6:  ("UN SIMPLE ENSAYO SECRETO", "CLASIFICADO · PROHIBIDO DIFUNDIR", "amber"),
    7:  ("GENERAL DWIGHT EISENHOWER", "ORDEN DE SIMULACIÓN DE COMBATE AL 100%", "amber"),
    8:  ("SLAPTON SANDS = PLAYA UTAH", "ESCÁNER TOPOGRÁFICO · COSTAS IDÉNTICAS", "tactical"),
    9:  ("3.000 VECINOS · 30.000 SOLDADOS", "MOVILIZACIÓN MASIVA EN DEVON, INGLATERRA", "amber"),
    10: ("CRUCERO HMS HAWKINS", "ORDEN DE DISPARAR MUNICIÓN REAL (190 MM)", "danger"),
    11: ("ACOSTUMBRARSE A LAS EXPLOSIONES", "IMPACTO ACÚSTICO DE ARTILLERÍA REAL", "amber"),
    12: ("UN PROBLEMA TRAS OTRO", "CADENA DE TRES FALLOS CRÍTICOS", "danger"),
    13: ("HORARIO RETRASADO 60 MINUTOS", "ORDEN DEL ALMIRANTE: 07:30 -> 08:30 AM", "amber"),
    14: ("DESEMBARCO BAJO FUEGO ALIADO", "LANCHAS SIN AVISO EN LA PLAYA A LAS 07:30", "danger"),
    15: ("MADRUGADA EN EL MAR", "28 DE ABRIL · RADAR NOCTURNO EN LYME BAY", "danger"),
    16: ("CONVOY T-4: 8 GRANDES BUQUES", "CARGADOS DE SOLDADOS Y TANQUES SHERMAN", "tactical"),
    17: ("UN SOLO ESCOLTA EN EL MAR", "EL SEGUNDO BUQUE VOLVIÓ A PUERTO POR AVERÍA", "danger"),
    18: ("9 LANCHAS TORPEDERAS ALEMANAS", "MANADA DE SCHNELLBOOTE A 40 NUDOS", "danger"),
    19: ("ALERTA POR RADIO BRITÁNICA", "LA CORBETA HMS AZALEA TRANSMITE EN 2880 KHZ", "tactical"),
    20: ("ERROR DE IMPRENTA EN LA ORDEN", "FRECUENCIA DE RADIO MAL ESCRITA (3880 KHZ)", "danger"),
    21: ("NUNCA ESCUCHAN LA ALERTA", "SILENCIO TOTAL EN LOS BUQUES DE EE. UU.", "danger"),
    22: ("2 HORAS BAJO ATAQUE NOCTURNO", "TORPEDOS ALEMANES CONTRA EL CONVOY INDEFENSO", "danger"),
    23: ("2 TRANSPORTES EN LLAMAS", "LST-507 Y LST-531 HUNDIDOS · LST-289 AVERIADO", "danger"),
    24: ("AGUA HELADA DEL CANAL (7 °C)", "SOLDADOS SALTANDO CON MOCHILAS DE 30 KG", "tactical"),
    25: ("SALVAVIDAS EN LA CINTURA", "EL CENTRO DE FLOTACIÓN LOS HUNDE DE CABEZA", "danger"),
    26: ("SALDO AL AMANECER: 749 MUERTOS", "551 DEL EJÉRCITO Y 198 DE LA MARINA", "danger"),
    27: ("CASI 4 VECES MÁS BAJAS", "749 EN EL ENSAYO vs. 197 EN EL DÍA D REAL", "amber"),
    28: ("DESEMBARCO REAL EN PLAYA UTAH", "6 DE JUNIO DE 1944 · NORMANDÍA, FRANCIA", "tactical"),
    29: ("LA PESADILLA DE EISENHOWER", "ALERTA DE SEGURIDAD MÁXIMA EN SHAEF", "danger"),
    30: ("10 OFICIALES CON ACCESO «BIGOT»", "DESAPARECIDOS EN LAS AGUAS DE LYME BAY", "amber"),
    31: ("EL SECRETO DEL DÍA D", "CONOCÍAN LA FECHA EXACTA Y LAS 5 PLAYAS", "amber"),
    32: ("SI CAPTURARON VIVO A UNO SOLO...", "HITLER YA CONOCE TODO EL PLAN DE NORMANDÍA", "danger"),
    33: ("BÚSQUEDA DE LOS 10 CADÁVERES", "BUZOS RECUPERAN E IDENTIFICAN LOS 10 CUERPOS", "tactical"),
    34: ("ORDEN DE SILENCIO ABSOLUTO", "PROHIBIDO HABLAR BAJO CONSEJO DE GUERRA", "danger"),
    35: ("MÁS MUERTOS EN EL ENSAYO", "749 EN INGLATERRA vs. 197 EN PLAYA UTAH", "amber"),
    36: ("EL DILEMA DE EISENHOWER", "¿Y SI FALTABA UNO SOLO DE LOS 10 CUERPOS?", "amber"),
    37: ("¿QUÉ HABRÍAS HECHO VOS?", "CANCELAR EL DÍA D vs. ATACAR IGUAL", "amber"),
}

VARIANT_COLORS = {"neutral": C_NEUTRAL, "amber": C_AMBER, "danger": C_DANGER, "tactical": C_TACTICAL}

# ==============================================================================
# MOTION GRAPHICS HUD, PARTICLES, AND VECTOR PRIMITIVES
# ==============================================================================
def draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="SECTOR: LYME BAY 50°16'N 03°38'W", mode="danger"):
    """Live animated military telemetry bar, corner viewfinder brackets, and signal waveform."""
    col = VARIANT_COLORS.get(mode, C_TACTICAL)
    t_ms = global_t * 1000.0
    # Top telemetry bar at Y=652..684
    draw.rectangle([40, 650, W - 40, 682], fill=(12, 16, 22), outline=(45, 58, 78), width=1)
    # Blinking recording/radar dot
    if int(global_t * 4) % 2 == 0:
        draw.ellipse([54, 660, 66, 672], fill=col)
    draw.text((76, 666), sector_txt, font=FONT_HUD, fill=(195, 205, 220), anchor="lm")
    # Live mission chronometer on right
    mm = int(global_t // 60)
    ss = int(global_t % 60)
    ff = int((global_t * 60) % 60)
    draw.text((W - 54, 666), f"T+{mm:02d}:{ss:02d}:{ff:02d} [SHAEF-44]", font=FONT_HUD, fill=col, anchor="rm")
    # Live mini waveform in center-right of telemetry bar
    wx0 = 620
    pts = []
    for i in range(24):
        wy = 666 + int(8.0 * math.sin(global_t * 14.0 + i * 0.55) * math.sin(i * math.pi / 23.0))
        pts.append((wx0 + i * 6, wy))
    draw.line(pts, fill=col, width=2)

    # Animated Corner Brackets locking in with spring_val
    sp = min(1.0, spring_val(scene_t, 0.0, 180, 16))
    inset = int(42 + (1.0 - sp) * 28)
    blen = 34
    for cx, cy, dx, dy in [
        (inset, 694, 1, 1), (W - inset, 694, -1, 1),
        (inset, 1425, 1, -1), (W - inset, 1425, -1, -1)
    ]:
        draw.line([(cx, cy), (cx + dx * blen, cy)], fill=col, width=3)
        draw.line([(cx, cy), (cx, cy + dy * blen)], fill=col, width=3)

def draw_ember_particles(frame, global_t, count=18):
    """Glowing rising embers & ash particles for combat/fire scenes."""
    t_ms = global_t * 1000.0
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for i in range(count):
        p = loop_p(t_ms, 2200.0 + seeded(i, 10) * 1400.0, phase=seeded(i, 20))
        alpha = int(220 * bell(p))
        if alpha > 15:
            x = int(90 + seeded(i, 30) * (W - 180) + 32.0 * wave(t_ms, 1600.0, seeded(i, 40)))
            y = int(1390 - p * 660)
            r = max(2, int(3 + 4 * seeded(i, 50) * (1.0 - p * 0.5)))
            col = (240, 180, 41, alpha) if i % 2 == 0 else (224, 90, 71, alpha)
            od.ellipse([x - r, y - r, x + r, y + r], fill=col)
    frame.paste(ov, (0, 0), ov)

def draw_radar_overlay(draw, cx, cy, rad, global_t, col=C_TACTICAL, blips=()):
    """Animated 360-degree rotating radar scope with concentric rings and pulsing target blips."""
    for r in [rad // 3, (rad * 2) // 3, rad]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=2)
    draw.line([(cx - rad - 12, cy), (cx + rad + 12, cy)], fill=(45, 75, 110), width=1)
    draw.line([(cx, cy - rad - 12), (cx, cy + rad + 12)], fill=(45, 75, 110), width=1)
    ang = global_t * 3.6
    # Sweep cone rays
    for da in range(0, 28, 4):
        a_trail = ang - math.radians(da)
        c_val = max(20, int(180 * (1.0 - da / 28.0)))
        draw.line([(cx, cy), (cx + int(rad * math.cos(a_trail)), cy + int(rad * math.sin(a_trail)))], fill=(col[0] // 2, col[1] // 2, col[2] // 2), width=2)
    draw.line([(cx, cy), (cx + int(rad * math.cos(ang)), cy + int(rad * math.sin(ang)))], fill=C_AMBER, width=4)
    for bx, by, bcol in blips:
        pr = 6 + int(4 * abs(math.sin(global_t * 8.0)))
        draw.ellipse([bx - pr, by - pr, bx + pr, by + pr], fill=bcol, outline=C_WHITE, width=2)

def draw_attribution_pill(draw, text):
    if not text:
        return
    tw = int(FONT_ATTR.getlength(text))
    draw.rounded_rectangle([40, 1445, 40 + tw + 24, 1479], radius=5, fill=(10, 12, 16), outline=(55, 60, 70), width=1)
    draw.text((52, 1462), text, font=FONT_ATTR, fill=(215, 220, 228), anchor="lm")

def draw_map_pill(draw, cx, cy, label, dot_col=C_DANGER, enter_prog=1.0):
    if enter_prog <= 0.01:
        return
    tw = int(FONT_PILL_SM.getlength(label))
    pw, ph = tw + 46, 38
    dy = int((1.0 - min(1.0, enter_prog)) * 22)
    x0, y0 = cx - pw // 2, cy - ph // 2 + dy
    draw.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=8, fill=(20, 22, 28), outline=dot_col, width=2)
    draw.ellipse([x0 + 12, cy - 6 + dy, x0 + 24, cy + 6 + dy], fill=dot_col)
    draw.text((x0 + 32, cy + dy), label, font=FONT_PILL_SM, fill=C_WHITE, anchor="lm")

def draw_digital_led_box(draw, cx, cy, text, col=C_DANGER, scale=1.0):
    f_use = FONT_LED_MD if (scale < 0.88 or len(text) > 13) else FONT_BIG_NUM
    tw = int(f_use.getlength(text))
    pw = max(140, tw + 56)
    ph = 84 if f_use == FONT_LED_MD else 102
    x0 = max(44, min(W - 44 - pw, cx - pw // 2))
    y0 = cy - ph // 2
    cx_adj = x0 + pw // 2
    draw.rounded_rectangle([x0 - 4, y0 - 4, x0 + pw + 4, y0 + ph + 4], radius=12, outline=(col[0]//3, col[1]//3, col[2]//3), width=3)
    draw.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=10, fill=(16, 15, 20), outline=col, width=4)
    draw.text((cx_adj, cy - 2), text, font=f_use, fill=col, anchor="mm")

def draw_leader_callout(draw, tx, ty, bx, by, title_txt, sub_txt, col=C_AMBER, prog=1.0):
    """Animated callout line from target point (tx, ty) to a HUD data card at (bx, by)."""
    if prog <= 0.02:
        return
    p_line = min(1.0, prog * 1.6)
    mx = int(tx + (bx - tx) * p_line)
    my = int(ty + (by - ty) * p_line)
    r_t = 8 + int(4 * math.sin(prog * 12.0))
    draw.ellipse([tx - r_t, ty - r_t, tx + r_t, ty + r_t], outline=col, width=3)
    draw.ellipse([tx - 4, ty - 4, tx + 4, ty + 4], fill=C_WHITE)
    draw.line([(tx, ty), (mx, my)], fill=col, width=3)
    if prog > 0.35:
        w_card = max(int(FONT_PILL_MD.getlength(title_txt)), int(FONT_PILL_SM.getlength(sub_txt))) + 44
        h_card = 78
        x0, y0 = bx - w_card // 2, by - h_card // 2
        draw.rounded_rectangle([x0, y0, x0 + w_card, y0 + h_card], radius=10, fill=(14, 18, 26), outline=col, width=3)
        draw.text((bx, y0 + 26), title_txt, font=FONT_PILL_MD, fill=col, anchor="mm")
        draw.text((bx, y0 + 56), sub_txt, font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")

def draw_rossark_water_surface(draw, y_surf, global_t, col=C_TACTICAL, n_ripples=4):
    t_ms = global_t * 1000.0
    pts = []
    for i, x in enumerate(range(0, W + 30, 30)):
        wy = y_surf + 7.5 * wave(t_ms, 2200.0, phase=i * 0.09) + 3.0 * wave(t_ms, 1250.0, phase=i * 0.17)
        pts.append((x, int(wy)))
    draw.line(pts, fill=col, width=4)
    pts2 = [(x, int(y + 16 + 3.5 * wave(t_ms, 2900.0, phase=i * 0.07 + 0.3))) for i, (x, y) in enumerate(pts)]
    draw.line(pts2, fill=(45, 95, 165), width=2)
    for r_i in range(n_ripples):
        p = loop_p(t_ms, 2400.0, phase=seeded(r_i, 11))
        b = bell(p)
        if b > 0.15:
            rx = int(180 + seeded(r_i, 22) * (W - 360))
            rw = int(28 + 105 * p)
            rh = max(4, int(rw * 0.22))
            draw.ellipse([rx - rw, y_surf - rh + 4, rx + rw, y_surf + rh + 4], outline=col, width=max(1, int(3 * b)))

def draw_rossark_smoke_and_fire(frame, cx, base_y, global_t, count=6, scale=1.0):
    t_ms = global_t * 1000.0
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(count):
        p = loop_p(t_ms, 2100.0 + seeded(i, 1) * 700.0, phase=seeded(i, 2))
        alpha = int(195 * bell(p))
        if alpha > 8:
            wx = cx + int(((seeded(i, 3) - 0.5) * 170 + 18.0 * wave(t_ms, 1700.0, seeded(i, 4))) * scale)
            wy = base_y - int((35 + p * 185) * scale)
            r = int((20 + p * 36) * scale)
            od.ellipse([wx - r, wy - int(r * 0.75), wx + r, wy + int(r * 0.75)], fill=(45, 48, 54, alpha))
    for fi in range(3):
        fx = cx + int((fi - 1) * 46 * scale)
        stretch = 1.0 + 0.065 * wave(t_ms, 650.0, fi * 0.3) + 0.04 * wave(t_ms, 1050.0, fi * 0.7)
        lean_px = int(10.0 * wave(t_ms, 800.0, fi * 0.4) * scale)
        fh = int(76 * stretch * scale)
        bw = int(28 * scale)
        od.polygon([(fx - bw, base_y), (fx + bw, base_y), (fx + lean_px, base_y - fh)], fill=(224, 90, 71, 240))
        od.polygon([(fx - bw // 2, base_y), (fx + bw // 2, base_y), (fx + int(lean_px * 0.6), base_y - int(fh * 0.65))], fill=(240, 180, 41, 250))
    frame.paste(overlay, (0, 0), overlay)

def draw_rossark_jiggle_button(draw, cx, cy, bw, bh, text, fill_col, outline_col, global_t, phase_offset=0.0):
    t_ms = global_t * 1000.0
    beat = wave(t_ms, 520.0, phase=phase_offset)
    squash = 1.0 + 0.025 * abs(beat)
    sy = 1.0 / (squash ** 0.6)
    bulge_x = int(bw * 0.014 * beat)
    w_cur, h_cur = int(bw * squash), int(bh * sy)
    x0, y0 = cx - w_cur // 2 + bulge_x, cy - h_cur // 2
    draw.rounded_rectangle([x0, y0, x0 + w_cur, y0 + h_cur], radius=12, fill=fill_col, outline=outline_col, width=4)
    draw.text((cx + bulge_x, cy), text, font=FONT_PILL_LG, fill=C_WHITE, anchor="mm")

def draw_vector_hand(draw, hx, hy, angle_deg=-25, sleeve_col=(62, 74, 48)):
    hand_img = Image.new("RGBA", (260, 320), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hand_img)
    skin, skin_dark = (218, 178, 146, 255), (188, 146, 114, 255)
    for fx, fy, fw, fh in [(78, 35, 22, 75), (104, 24, 22, 85), (130, 28, 22, 80), (156, 42, 20, 68)]:
        hd.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=10, fill=skin, outline=skin_dark, width=2)
    hd.polygon([(50, 95), (78, 82), (90, 125), (58, 132)], fill=skin, outline=skin_dark)
    hd.rounded_rectangle([72, 88, 178, 178], radius=22, fill=skin, outline=skin_dark, width=2)
    hd.polygon([(62, 172), (188, 172), (210, 315), (40, 315)], fill=sleeve_col + (255,))
    hd.line([(60, 196), (190, 196)], fill=C_AMBER + (255,), width=8)
    rot = hand_img.rotate(angle_deg, resample=Image.Resampling.BICUBIC, expand=True)
    return rot, hx - rot.width // 2, hy - rot.height // 3

def draw_lst_ship(draw, cx, cy, scale=1.0, body_col=(58, 68, 78), stroke_col=C_NEUTRAL, on_fire=False, facing="right"):
    d = 1 if facing == "right" else -1
    w_h, h_h = int(175 * scale), int(28 * scale)
    st_x0, st_x1 = cx - int(145 * scale * d), cx - int(65 * scale * d)
    if st_x0 > st_x1: st_x0, st_x1 = st_x1, st_x0
    draw.rounded_rectangle([st_x0, cy - h_h - int(44 * scale), st_x1, cy - h_h + 4], radius=int(6 * scale), fill=body_col, outline=stroke_col, width=max(2, int(3 * scale)))
    mast_x = (st_x0 + st_x1) // 2
    draw.line([(mast_x, cy - h_h - int(84 * scale)), (mast_x, cy - h_h - int(44 * scale))], fill=stroke_col, width=max(2, int(3 * scale)))
    draw.polygon([
        (cx - w_h, cy - h_h), (cx + w_h, cy - h_h),
        (cx + int(w_h * 0.88), cy + h_h), (cx - int(w_h * 0.92), cy + h_h)
    ], fill=(82, 24, 24) if on_fire else body_col, outline=C_DANGER if on_fire else stroke_col, width=max(2, int(3 * scale)))

def draw_sboot(draw, cx, cy, scale=1.0, facing="left"):
    d = 1 if facing == "right" else -1
    w_h, h_h = int(95 * scale), int(16 * scale)
    draw.polygon([
        (cx - w_h * d, cy - h_h), (cx + w_h * d, cy - int(h_h * 0.6)),
        (cx + int(w_h * 0.78 * d), cy + h_h), (cx - int(w_h * 0.92 * d), cy + h_h),
    ], fill=(42, 22, 24), outline=C_DANGER, width=max(2, int(3 * scale)))
    draw.rounded_rectangle([cx - int(25 * scale), cy - h_h - int(18 * scale), cx + int(25 * scale), cy - h_h + 2], radius=4, fill=(65, 28, 30), outline=C_DANGER, width=2)

def draw_english_channel_map(draw):
    england_poly = [
        (0, 682), (1080, 682), (1080, 795), (920, 815), (760, 800),
        (610, 845), (465, 825), (345, 905), (210, 925), (95, 890), (0, 915)
    ]
    france_poly = [
        (160, 1420), (295, 1345), (395, 1145), (485, 1145), (520, 1245),
        (695, 1265), (860, 1215), (1080, 1175), (1080, 1420)
    ]
    draw.polygon(england_poly, fill=C_LAND_FILL, outline=C_LAND_STROKE, width=3)
    draw.polygon(france_poly, fill=C_LAND_FILL, outline=C_LAND_STROKE, width=3)

def draw_rossark_officer(frame, cx, cy, scale=1.35, role="eisenhower", global_t=0.0, scene_t=0.0, talking=False, mood="focused", gesture="rest"):
    t_ms = (global_t * 1000.0) % 7200.0
    s_ms = scene_t * 1000.0
    canvas_sz = 460
    rig = Image.new("RGBA", (canvas_sz, canvas_sz), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rig)
    ox, oy = canvas_sz // 2, 210

    if role == "eisenhower":
        suit_col, suit_shade, cap_top, badge_col, phase_seed = (68, 76, 48, 255), (92, 102, 66, 255), (74, 82, 52, 255), C_AMBER + (255,), 0.12
    elif role == "admiral":
        suit_col, suit_shade, cap_top, badge_col, phase_seed = (20, 34, 62, 255), (34, 54, 92, 255), (238, 242, 248, 255), C_AMBER + (255,), 0.35
    elif role == "british_officer":
        suit_col, suit_shade, cap_top, badge_col, phase_seed = (18, 30, 54, 255), (30, 48, 82, 255), (235, 240, 248, 255), C_TACTICAL + (255,), 0.52
    else:
        suit_col, suit_shade, cap_top, badge_col, phase_seed = (78, 84, 56, 255), (102, 108, 74, 255), (56, 64, 42, 255), C_NEUTRAL + (255,), 0.74

    skin_col, feature_col, hair_col = (242, 185, 148, 255), (210, 126, 88, 255), (72, 48, 34, 255)
    lean_keys = [(0, 0.0), (1800, -2.5), (3600, 2.0), (5400, -1.5), (7200, 0.0)]
    yaw_keys = [(0, -0.15), (2100, 0.22), (4200, 0.18), (5800, -0.18), (7200, -0.15)]
    head_keys = [(0, 0.0), (2000, 3.5), (4100, -3.0), (5900, 2.0), (7200, 0.0)]

    lean = flow(t_ms, lean_keys) + 1.4 * wave(t_ms, 4200.0, phase_seed)
    yaw = flow(t_ms, yaw_keys) + 0.06 * wave(t_ms, 3100.0, phase_seed + 0.2)
    head_tilt = flow(t_ms, head_keys) - 0.45 * flow(max(0.0, t_ms - 110.0), lean_keys) + 1.8 * wave(t_ms, 4600.0, phase_seed + 0.5)

    sy = 1.0 + 0.016 * wave(t_ms, 2600.0, phase_seed)
    sx = 1.0 / (sy ** 0.6)
    lift = 2.5 * wave(t_ms, 2600.0, phase_seed + 0.25)

    if gesture == "point_order":
        arm_ra_keys, arm_re_keys = [(0, 25.0), (450, 64.0), (1400, 70.0), (7200, 66.0)], [(0, 15.0), (450, 82.0), (1400, 92.0), (7200, 86.0)]
    elif gesture == "stop_hand":
        arm_ra_keys, arm_re_keys = [(0, 20.0), (400, 58.0), (1200, 62.0), (7200, 60.0)], [(0, 10.0), (400, 108.0), (1200, 112.0), (7200, 110.0)]
    else:
        arm_ra_keys, arm_re_keys = [(0, 22.0), (2400, 30.0), (4800, 18.0), (7200, 22.0)], [(0, 18.0), (2400, 32.0), (4800, 14.0), (7200, 18.0)]

    t_gesture = min(7199.0, s_ms)
    ra_base = flow(t_gesture, arm_ra_keys) + 3.5 * wave(t_ms, 3000.0, phase_seed)
    ra_prev = flow(max(0.0, t_gesture - 90.0), arm_ra_keys)
    re_base = flow(t_gesture, arm_re_keys) + 4.5 * wave(t_ms, 2250.0, phase_seed + 0.4) + 0.45 * (ra_prev - flow(t_gesture, arm_ra_keys))
    la_base = 24.0 + 3.5 * wave(t_ms, 3200.0, phase_seed + 0.5)
    le_base = -18.0 + 4.0 * wave(t_ms, 2400.0, phase_seed + 0.8)

    bx, by = ox + int(lean * 1.4), oy - int(lift)

    def draw_arm(side, a_deg, e_deg):
        a_rad, f_rad = math.radians(a_deg), math.radians(a_deg + e_deg)
        sh_x, sh_y = bx + int(side * 42 * sx), by + int(64 * sy)
        el_x, el_y = sh_x + int(side * math.sin(a_rad) * 38), sh_y + int(math.cos(a_rad) * 38)
        ha_x, ha_y = el_x + int(side * math.sin(f_rad) * 36), el_y + int(math.cos(f_rad) * 36)
        rd.line([(sh_x, sh_y), (el_x, el_y), (ha_x, ha_y)], fill=suit_col, width=26, joint="curve")
        rd.ellipse([ha_x - 14, ha_y - 14, ha_x + 14, ha_y + 14], fill=skin_col, outline=feature_col, width=2)

    draw_arm(-1, la_base, le_base)
    t_top, t_bot = by + int(48 * sy), by + int(138 * sy)
    sh_w, wa_w = int(52 * sx), int(44 * sx)
    rd.polygon([(bx - sh_w, t_top), (bx + sh_w, t_top), (bx + wa_w, t_bot), (bx - wa_w, t_bot)], fill=suit_col, outline=suit_shade)
    yaw_px = int(8 * yaw)
    rd.polygon([(bx - 16 + yaw_px, t_top), (bx + 16 + yaw_px, t_top), (bx + yaw_px, t_top + 26)], fill=C_WHITE + (255,))
    for b_row in [t_top + 34, t_top + 56, t_top + 78]:
        for b_col in [-16, 16]:
            rd.ellipse([bx + b_col + yaw_px - 4, b_row - 4, bx + b_col + yaw_px + 4, b_row + 4], fill=C_AMBER + (255,))

    head_layer = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_layer)
    hcx, hcy = 120, 130
    ear_dx = int(-9 * yaw)
    for side in [-1, 1]:
        ex = hcx + side * 50 + ear_dx
        hd.ellipse([ex - 11, hcy - 10, ex + 11, hcy + 12], fill=skin_col, outline=feature_col, width=2)
    hd.rounded_rectangle([hcx - 50, hcy - 64, hcx + 50, hcy + 52], radius=28, fill=skin_col, outline=feature_col, width=2)

    blinks = make_blink_keys(7200.0, [1400.0, 4100.0, 6200.0])
    lid_val = max(0.08 if mood == "focused" else 0.0, track(t_ms, blinks))
    face_dx = int(10 * yaw)
    look_x = int(4 * yaw + 3.0 * wave(t_ms, 3400.0, phase_seed))
    look_y = int(1.5 * wave(t_ms, 2800.0, phase_seed + 0.3))

    for side in [-1, 1]:
        ecx, ecy = hcx + side * 20 + face_dx, hcy - 8
        ew, eh = 24, 30
        hd.rounded_rectangle([ecx - ew // 2, ecy - eh // 2, ecx + ew // 2, ecy + eh // 2], radius=11, fill=C_WHITE + (255,))
        px, py = ecx + look_x, ecy + look_y
        hd.rounded_rectangle([px - 6, py - 8, px + 6, py + 8], radius=5, fill=(38, 38, 42, 255))
        hd.ellipse([px - 4, py - 6, px - 1, py - 3], fill=C_WHITE + (255,))
        if lid_val > 0.02:
            lid_h = int((eh + 4) * lid_val)
            hd.rounded_rectangle([ecx - ew // 2 - 2, ecy - eh // 2 - 2, ecx + ew // 2 + 2, ecy - eh // 2 - 2 + lid_h], radius=8, fill=skin_col)
            hd.line([(ecx - ew // 2 - 1, ecy - eh // 2 - 2 + lid_h), (ecx + ew // 2 + 1, ecy - eh // 2 - 2 + lid_h)], fill=feature_col, width=3)
        hd.line([(ecx - 12, ecy - eh // 2 - 6), (ecx + 12, ecy - eh // 2 - 8)], fill=hair_col, width=5)

    nx = hcx + int(13 * yaw)
    hd.rounded_rectangle([nx - 5, hcy - 4, nx + 5, hcy + 14], radius=4, fill=feature_col)
    mx, my = hcx + face_dx, hcy + 26
    if talking:
        m_depth = int(6 + 10 * abs(wave(t_ms, 340.0, phase_seed)))
        hd.polygon([(mx - 14, my), (mx + 14, my), (mx + 10, my + m_depth), (mx - 10, my + m_depth)], fill=(155, 42, 42, 255))
        hd.line([(mx - 11, my + 2), (mx + 11, my + 2)], fill=C_WHITE + (255,), width=3)
    else:
        hd.arc([mx - 12, my - 4, mx + 12, my + 8], start=15, end=165, fill=feature_col, width=4)

    if role == "us_recruit":
        hd.pieslice([hcx - 60, hcy - 92, hcx + 60, hcy + 10], start=180, end=360, fill=cap_top, outline=suit_shade, width=3)
        hd.line([(hcx - 62, hcy - 42), (hcx + 62, hcy - 42)], fill=(40, 46, 30, 255), width=5)
    else:
        hd.polygon([(hcx - 58, hcy - 46), (hcx + 58, hcy - 46), (hcx + 68, hcy - 76), (hcx, hcy - 88), (hcx - 68, hcy - 76)], fill=cap_top, outline=suit_col)
        hd.rectangle([hcx - 52, hcy - 52, hcx + 52, hcy - 38], fill=(20, 22, 26, 255), outline=C_AMBER + (255,), width=2)
        hd.ellipse([hcx + int(6 * yaw) - 9, hcy - 68, hcx + int(6 * yaw) + 9, hcy - 50], fill=badge_col, outline=C_WHITE + (255,), width=2)

    head_rot = head_layer.rotate(-head_tilt, resample=Image.Resampling.BICUBIC, expand=False)
    rig.paste(head_rot, (bx - hcx, by - hcy), head_rot)
    draw_arm(1, ra_base, re_base)

    if scale != 1.0:
        new_sz = max(40, int(canvas_sz * scale))
        rig = rig.resize((new_sz, new_sz), Image.Resampling.LANCZOS)
    frame.paste(rig, (cx - rig.width // 2, cy - rig.height // 2), rig)

def render_module_a_steady(photo_key, scene_t, scene_dur, global_t, date_ribbon, caption_pill, attribution, mode="tactical", extra_vector_fn=None):
    frame = PHOTOS_STEADY_STAGE.get(photo_key, CANVAS_ABYSS).copy()
    draw = ImageDraw.Draw(frame)
    draw_tactical_hud_frame(frame, draw, global_t, scene_t, mode=mode)
    if extra_vector_fn:
        extra_vector_fn(frame, draw, scene_t, scene_dur)
        draw = ImageDraw.Draw(frame)
    if date_ribbon:
        n_chars = int(min(len(date_ribbon), max(1, (scene_t / 0.65) * len(date_ribbon))))
        typed_str = date_ribbon[:n_chars]
        tw = int(FONT_RIBBON.getlength(typed_str))
        draw.rectangle([58, 704, 58 + tw + 36, 750], fill=(0, 0, 0))
        draw.rectangle([52, 698, 52 + tw + 36, 744], fill=C_PAPER)
        draw.rectangle([52, 698, 58, 744], fill=C_STAMP_RED)
        draw.text((70, 721), typed_str, font=FONT_RIBBON, fill=C_INK, anchor="lm")
    if caption_pill:
        enter_s = spring_val(scene_t, delay_sec=0.10)
        tw = int(FONT_PILL_MD.getlength(caption_pill))
        pw = tw + 48
        px0 = (W - pw) // 2
        py0 = int(1352 + (1.0 - min(1.0, enter_s)) * 24)
        draw.rounded_rectangle([px0, py0, px0 + pw, py0 + 48], radius=8, fill=(14, 17, 24), outline=VARIANT_COLORS.get(mode, C_AMBER), width=2)
        draw.text((W // 2, py0 + 24), caption_pill, font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
    draw_attribution_pill(draw, attribution)
    return frame

def render_module_c_document_with_hand(scene_t, global_t, header, meta_line, lines, highlight_idx, stamp_text, source_attr, tilt_deg=-1.5):
    frame = CANVAS_ABYSS.copy()
    draw_bg = ImageDraw.Draw(frame)
    draw_tactical_hud_frame(frame, draw_bg, global_t, scene_t, sector_txt="ARCHIVO CLASIFICADO SHAEF · MICROFICHA #44-B", mode="danger")
    # Animated red laser scanline sweeping vertically over the document stage
    scan_y = int(700 + 680 * ((global_t * 0.55) % 1.0))
    draw_bg.line([(45, scan_y), (W - 45, scan_y)], fill=(120, 28, 32), width=2)

    doc_w, doc_h = 860, 620
    doc = Image.new("RGBA", (doc_w + 40, doc_h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(doc)
    d.rounded_rectangle([24, 28, doc_w + 24, doc_h + 28], radius=8, fill=(0, 0, 0, 195))
    d.rounded_rectangle([10, 10, doc_w + 10, doc_h + 10], radius=6, fill=(244, 239, 230, 255), outline=(213, 206, 192, 255), width=2)
    d.text((54, 48), header, font=FONT_DOC_HDR, fill=(75, 72, 66, 255))
    d.line([(54, 82), (doc_w - 38, 82)], fill=(213, 206, 192, 255), width=2)
    d.text((54, 100), meta_line, font=FONT_DOC_META, fill=(26, 25, 23, 255))
    underline_prog = min(1.0, max(0.0, (scene_t - 0.12) / 1.05))
    y_cur = 156
    pen_tip_x, pen_tip_y = 420, 320
    for idx, line in enumerate(lines):
        is_hl = (idx in highlight_idx) if isinstance(highlight_idx, (set, list, tuple)) else (idx == highlight_idx)
        if is_hl and underline_prog > 0:
            lw = int(FONT_DOC_BOLD.getlength(line))
            hw = int(lw * underline_prog)
            d.rectangle([50, y_cur + 2, 50 + hw + 8, y_cur + 36], fill=(238, 196, 186, 255))
            d.rectangle([50, y_cur + 33, 50 + hw + 8, y_cur + 37], fill=(214, 54, 41, 255))
            pen_tip_x, pen_tip_y = 50 + hw, y_cur + 35
        d.text((54, y_cur), line, font=FONT_DOC_BOLD if is_hl else FONT_DOC_LINE, fill=(26, 25, 23, 255))
        y_cur += 52
    d.line([(54, doc_h - 56), (doc_w - 38, doc_h - 56)], fill=(223, 216, 200, 255), width=1)
    d.text((54, doc_h - 34), "RECONSTRUCCIÓN DOCUMENTAL · ARCHIVOS 1944", font=FONT_FOOTER, fill=(113, 113, 122, 255))
    if stamp_text and scene_t >= 0.55:
        sp = spring_val(scene_t, delay_sec=0.55, stiffness=240, damping=12)
        stw = int(FONT_STAMP.getlength(stamp_text)) + 44
        sth = 64
        stamp_img = Image.new("RGBA", (stw + 20, sth + 20), (0, 0, 0, 0))
        sd = ImageDraw.Draw(stamp_img)
        sd.rectangle([6, 6, stw + 6, sth + 6], outline=(214, 54, 41, 240), width=4)
        sd.rectangle([12, 12, stw, sth], outline=(214, 54, 41, 240), width=2)
        sd.text((6 + stw // 2, 6 + sth // 2), stamp_text, font=FONT_STAMP, fill=(214, 54, 41, 240), anchor="mm")
        s_factor = max(0.85, 1.65 - 0.65 * min(1.0, sp))
        stamp_rot = stamp_img.rotate(8, resample=Image.Resampling.BICUBIC, expand=True)
        sw_new, sh_new = max(10, int(stamp_rot.width * s_factor)), max(10, int(stamp_rot.height * s_factor))
        stamp_rot = stamp_rot.resize((sw_new, sh_new), Image.Resampling.LANCZOS)
        doc.paste(stamp_rot, (doc_w - sw_new - 25, doc_h - sh_new - 65), stamp_rot)
    rotated = doc.rotate(tilt_deg, resample=Image.Resampling.BICUBIC, expand=True)
    doc_x = (W - rotated.width) // 2
    doc_y = 700 + (670 - rotated.height) // 2
    frame.paste(rotated, (doc_x, doc_y), rotated)
    draw = ImageDraw.Draw(frame)
    hand_rot, hx, hy = draw_vector_hand(draw, doc_x + pen_tip_x + 30, doc_y + pen_tip_y + 70, angle_deg=-22)
    frame.paste(hand_rot, (hx, hy), hand_rot)
    draw_attribution_pill(draw, source_attr)
    return frame

def draw_balance_scale(draw, cx, base_y, tilt_deg, left_pills, right_pills, left_title, right_title, left_col=C_DANGER, right_col=C_TACTICAL, drop_prog=1.0):
    gold_m, gold_l = (218, 172, 54), (245, 208, 96)
    draw.ellipse([cx - 165, base_y - 34, cx + 165, base_y + 16], fill=gold_m, outline=gold_l, width=2)
    draw.rectangle([cx - 13, base_y - 490, cx + 13, base_y - 10], fill=gold_m)
    rad = math.radians(tilt_deg)
    arm = 320
    lx, ly = int(cx - arm * math.cos(rad)), int((base_y - 475) + arm * math.sin(rad))
    rx, ry = int(cx + arm * math.cos(rad)), int((base_y - 475) - arm * math.sin(rad))
    draw.line([(lx, ly), (rx, ry)], fill=gold_l, width=11)
    draw.ellipse([cx - 18, base_y - 493, cx + 18, base_y - 457], fill=gold_l)
    for px, py, pills, title, col in [(lx, ly, left_pills, left_title, left_col), (rx, ry, right_pills, right_title, right_col)]:
        pan_y = py + 195
        draw.line([(px, py), (px - 110, pan_y)], fill=gold_l, width=3)
        draw.line([(px, py), (px + 110, pan_y)], fill=gold_l, width=3)
        draw.pieslice([px - 125, pan_y - 26, px + 125, pan_y + 26], start=0, end=180, fill=gold_m, outline=gold_l, width=3)
        draw.text((px, pan_y + 58), title, font=FONT_PILL_LG, fill=col, anchor="mm")
        for i, ptxt in enumerate(pills):
            p_enter = min(1.0, max(0.0, drop_prog * len(pills) - i))
            if p_enter > 0:
                iy = int(pan_y - 30 - i * 48 - (1.0 - p_enter) * 55)
                tw = int(FONT_PILL_SM.getlength(ptxt)) + 32
                draw.rounded_rectangle([px - tw // 2, iy - 19, px + tw // 2, iy + 19], radius=8, fill=C_PAPER, outline=gold_m, width=2)
                draw.text((px, iy), ptxt, font=FONT_PILL_SM, fill=C_INK, anchor="mm")

# ==============================================================================
# MASTER 37-SCENE MOTION GRAPHICS DISPATCHER (PART 1: SCENES 1..18)
# ==============================================================================
def render_stage_for_scene(scene_id, scene_t, scene_dur, global_t):
    s_prog = min(1.0, max(0.0, scene_t / max(0.1, scene_dur)))
    t_ms = global_t * 1000.0

    if scene_id == 1:
        # S01 (0.00s - 3.00s): EXPLOSIVE HOOK — Burning LST + Radar Scope + Embers + Kinetic Date Slam!
        frame = PHOTOS_STEADY_STAGE.get("lst_burning", CANVAS_ABYSS).copy()
        draw_ember_particles(frame, global_t, count=24)
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="ALERTA ROJA · CANAL DE LA MANCHA · 50°16'N", mode="danger")
        # Live rotating tactical radar scope in top-right of stage
        draw_radar_overlay(draw, 865, 835, 110, global_t, col=C_DANGER, blips=[(830, 800, C_AMBER), (895, 865, C_DANGER), (850, 880, C_DANGER)])
        # Target lock crosshair on burning ship + leader callout
        rad_c = int(72 - 18 * min(1.0, spring_val(scene_t, 0.05)))
        tx_b, ty_b = 585, 1085
        draw.ellipse([tx_b - rad_c, ty_b - rad_c, tx_b + rad_c, ty_b + rad_c], outline=C_DANGER, width=4)
        draw.line([(tx_b - rad_c - 22, ty_b), (tx_b + rad_c + 22, ty_b)], fill=C_DANGER, width=3)
        draw.line([(tx_b, ty_b - rad_c - 22), (tx_b, ty_b + rad_c + 22)], fill=C_DANGER, width=3)
        draw_leader_callout(draw, tx_b, ty_b, 310, 825, "IMPACTO DE TORPEDO", "CONVOY ALIADO T-4 EN LLAMAS", C_DANGER, prog=spring_val(scene_t, 0.08))
        # Kinetic spring-loaded LED banner at bottom of stage
        sp = min(1.08, spring_val(scene_t, 0.02, stiffness=210, damping=13))
        draw_digital_led_box(draw, W // 2, int(1265 + (1.0 - sp) * 60), "28 ABRIL 1944", C_DANGER, scale=1.0)
        draw_map_pill(draw, W // 2, 1375, "EL DESASTRE OCULTO ANTES DEL DÍA D", C_AMBER, enter_prog=sp)
        draw_attribution_pill(draw, "FOTO DE ARCHIVO · US NAVY (BUQUE LST EN LLAMAS, 1944) · DOMINIO PÚBLICO")
        return frame

    elif scene_id == 2:
        # S02 (3.00s - 5.97s): Animated War-Room Map + Radar Sweep + Countdown Ring (Faltan 5 Semanas)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_english_channel_map(draw)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="SALA DE GUERRA SHAEF · OPERACIÓN OVERLORD", mode="amber")
        draw_radar_overlay(draw, 540, 1040, 290, global_t, col=C_TACTICAL, blips=[(360, 840, C_TACTICAL), (520, 1210, C_DANGER)])
        draw_map_pill(draw, 330, 745, "SUR DE INGLATERRA", C_TACTICAL, enter_prog=spring_val(scene_t, 0.05))
        draw_map_pill(draw, 610, 1345, "PLAYAS DE NORMANDÍA (FRANCIA)", C_DANGER, enter_prog=spring_val(scene_t, 0.15))
        # Animated invasion vectors shooting across the Channel
        for i, (ax, tx) in enumerate([(310, 430), (490, 560), (670, 710)]):
            p_arr = EASE_OUT(min(1.0, max(0.0, (scene_t - i * 0.10) / 0.85)))
            ay_end = int(850 + 290 * p_arr)
            mx = int(ax + (tx - ax) * p_arr)
            draw.line([(ax, 850), (mx, ay_end)], fill=C_AMBER, width=7)
            draw.ellipse([mx - 11, ay_end - 11, mx + 11, ay_end + 11], fill=C_DANGER, outline=C_WHITE, width=2)
        draw_digital_led_box(draw, W // 2, 1035, "D - 5 SEMANAS", C_AMBER)
        return frame

    elif scene_id == 3:
        # S03 (5.97s - 7.76s): Aerial Recon Lock-On over Slapton Sands (Sur de Inglaterra)
        def _vec3(frame, draw, st, sd):
            # Sweeping horizontal topographic laser scanline
            scan_y = int(720 + 620 * ((st / max(0.2, sd)) % 1.0))
            draw.line([(45, scan_y), (W - 45, scan_y)], fill=C_TACTICAL, width=4)
            draw_leader_callout(draw, 480, 1020, 660, 835, "SLAPTON SANDS · DEVON", "COSTA SUR DE INGLATERRA (50°16'N)", C_TACTICAL, prog=spring_val(st, 0.06))
        return render_module_a_steady(
            "slapton", scene_t, scene_dur, global_t,
            "RECONOCIMIENTO AÉREO · SUR DE INGLATERRA",
            "En una playa inglesa idéntica a la costa de Normandía...",
            "FOTO DE ARCHIVO · PLAYA DE SLAPTON SANDS (DEVON) · CC BY-SA 2.0",
            mode="tactical", extra_vector_fn=_vec3
        )

    elif scene_id == 4:
        # S04 (7.76s - 12.11s): KINETIC CASUALTY MATRIX (15x10 = 750 Soldiers) + Live ECG Shockwave!
        frame = CANVAS_ABYSS.copy()
        draw_ember_particles(frame, global_t, count=20)
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="REGISTRO DE BAJAS EN COMBATE · 28 ABR 1944", mode="danger")
        p_cnt = EASE_OUT(min(1.0, scene_t / max(0.5, scene_dur * 0.72)))
        cnt_val = int(750 * p_cnt)
        # Giant glowing casualty counter at top of stage
        draw.rounded_rectangle([75, 705, W - 75, 925], radius=18, fill=(38, 14, 18), outline=C_DANGER, width=4)
        draw.text((340, 815), f"~{cnt_val}", font=FONT_GIANT, fill=C_DANGER, anchor="mm")
        draw.text((735, 780), "SOLDADOS DE EE. UU.", font=FONT_PILL_LG, fill=C_WHITE, anchor="mm")
        draw.text((735, 835), "MUERTOS EN HORAS", font=FONT_PILL_MD, fill=C_AMBER, anchor="mm")
        # Live spiking ECG / shockwave line inside the card
        ecg_pts = []
        for ix in range(540, 940, 8):
            ang = (ix - 540) * 0.08 - global_t * 14.0
            spike = 26.0 * math.sin(ang) * (1.0 if (ix // 32) % 3 == 0 else 0.25)
            ecg_pts.append((ix, int(885 + spike)))
        draw.line(ecg_pts, fill=C_DANGER, width=3)

        # 15 columns x 10 rows = 150 squad blocks (each = 5 soldiers -> 750 men) lighting up in crimson!
        lit_units = int(150 * p_cnt)
        gx0, gy0 = 88, 955
        for idx_u in range(150):
            col_u = idx_u % 15
            row_u = idx_u // 15
            ux = gx0 + col_u * 61
            uy = gy0 + row_u * 34
            is_dead = idx_u < lit_units
            fill_c = C_DANGER if is_dead else (28, 36, 48)
            out_c = (255, 160, 150) if is_dead else (55, 68, 86)
            draw.rounded_rectangle([ux, uy, ux + 48, uy + 24], radius=4, fill=fill_c, outline=out_c, width=1)
        draw_map_pill(draw, W // 2, 1355, "CADA BLOQUE ROJO = 5 SOLDADOS ESTADOUNIDENSES CAÍDOS", C_DANGER)
        return frame

    elif scene_id == 5:
        # S05 (12.11s - 13.24s): Kinetic Map Rejection — "NO ESTÁN EN FRANCIA"
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_english_channel_map(draw)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="VERIFICACIÓN DE TEATRO DE OPERACIONES", mode="danger")
        sp = min(1.0, spring_val(scene_t, 0.02, 200, 14))
        draw.rounded_rectangle([120, 780, W - 120, 1220], radius=20, fill=(28, 16, 20), outline=C_DANGER, width=4)
        draw.text((W // 2, 910), "FRANCIA · NORMANDÍA", font=FONT_HEADLINE, fill=(170, 175, 185), anchor="mm")
        draw.text((W // 2, 985), "COMBATE REAL EN EL FRENTE", font=FONT_PILL_LG, fill=(140, 145, 155), anchor="mm")
        # Dual animated laser X-slashes striking out France!
        slash_p = EASE_OUT(min(1.0, scene_t / 0.38))
        x1_end = int(180 + (W - 360) * slash_p)
        y1_end = int(830 + 330 * slash_p)
        draw.line([(180, 830), (x1_end, y1_end)], fill=C_DANGER, width=14)
        draw.line([(W - 180, 830), (W - x1_end, y1_end)], fill=C_DANGER, width=14)
        draw_digital_led_box(draw, W // 2, 1140, "NO ESTÁN EN FRANCIA", C_DANGER)
        return frame

    elif scene_id == 6:
        # S06 (13.24s - 15.98s): Top-Secret Dossier Slam — "ESTÁN EN UN SIMPLE ENSAYO SECRETO"
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="EXPEDIENTE CLASIFICADO · EJERCICIO TIGRE", mode="amber")
        sp = min(1.05, spring_val(scene_t, 0.02, 180, 14))
        cw, ch = int(880 * sp), int(520 * sp)
        cx0, cy0 = (W - cw) // 2, 740
        draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=18, fill=(40, 22, 16), outline=C_AMBER, width=4)
        draw.rectangle([cx0, cy0, cx0 + cw, cy0 + 68], fill=C_DANGER)
        draw.text((W // 2, cy0 + 34), "TOP SECRET · OPERACIÓN TIGRE (INGLATERRA)", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        draw.text((W // 2, cy0 + 165), "UN SIMPLE ENSAYO", font=FONT_HEADLINE, fill=C_AMBER, anchor="mm")
        draw.text((W // 2, cy0 + 235), "MURIERON ENTRENANDO EN SU PROPIA BASE", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        # Spring-loaded stamp + expanding shock ring
        st_p = spring_val(scene_t, 0.28, 240, 11)
        if st_p > 0:
            rad_s = int(60 + 220 * min(1.0, (scene_t - 0.28) / 0.8))
            draw.ellipse([W // 2 - rad_s, cy0 + 380 - rad_s // 2, W // 2 + rad_s, cy0 + 380 + rad_s // 2], outline=C_DANGER, width=2)
            draw_digital_led_box(draw, W // 2, cy0 + 380, "SECRETO MILITAR", C_DANGER, scale=max(0.85, 1.35 - 0.35 * min(1.0, st_p)))
        return frame

    elif scene_id == 7:
        # S07: General Eisenhower Archival Portrait + Animated Combat Simulation Checklist HUD
        def _vec7(frame, draw, st, sd):
            items = [
                ("1. PLAYA IDÉNTICA A UTAH", C_TACTICAL),
                ("2. 30.000 SOLDADOS Y TANQUES", C_AMBER),
                ("3. FUEGO NAVAL REAL (190 MM)", C_DANGER),
            ]
            for i, (txt, col) in enumerate(items):
                ip = spring_val(st, 0.15 + i * 0.25)
                if ip > 0.05:
                    x0 = int(520 + (1.0 - min(1.0, ip)) * 120)
                    y0 = 755 + i * 86
                    draw.rounded_rectangle([x0, y0, W - 48, y0 + 68], radius=10, fill=(14, 20, 30), outline=col, width=3)
                    draw.text((x0 + 24, y0 + 34), f"[✓] {txt}", font=FONT_PILL_SM, fill=C_WHITE, anchor="lm")
            # Simulation realism bar at 100%
            p_bar = EASE_OUT(min(1.0, st / 1.4))
            draw.rounded_rectangle([520, 1030, W - 48, 1105], radius=10, fill=(28, 16, 20), outline=C_AMBER, width=3)
            draw.rectangle([532, 1072, 532 + int(484 * p_bar), 1092], fill=C_AMBER)
            draw.text((774, 1050), f"REALISMO EXIGIDO: {int(100 * p_bar)}%", font=FONT_PILL_SM, fill=C_AMBER, anchor="mm")
        return render_module_a_steady(
            "eisenhower", scene_t, scene_dur, global_t,
            "GENERAL DWIGHT D. EISENHOWER · SHAEF",
            "Exige que el ensayo general sea idéntico al Día D verdadero",
            "FOTO DE ARCHIVO · US ARMY SIGNAL CORPS / DPLA, 1944 · DOMINIO PÚBLICO",
            mode="amber", extra_vector_fn=_vec7
        )

    elif scene_id == 8:
        # S08: Dual Biometric/Topographic Scanner: SLAPTON SANDS vs PLAYA DE UTAH (98.4% Match)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="ANÁLISIS GEOLÓGICO COMPARATIVO · CANAL DE LA MANCHA", mode="tactical")
        scan_y = int(730 + 500 * (0.5 + 0.5 * math.sin(global_t * 3.8)))
        for idx_c, (x0, title, country, col) in enumerate([
            (52, "SLAPTON SANDS", "INGLATERRA (ENSAYO)", C_TACTICAL),
            (556, "PLAYA DE UTAH", "FRANCIA (DÍA D REAL)", C_AMBER)
        ]):
            cw = 472
            draw.rounded_rectangle([x0, 700, x0 + cw, 1255], radius=16, fill=(14, 28, 48), outline=col, width=3)
            draw.text((x0 + cw // 2, 748), title, font=FONT_PILL_LG, fill=col, anchor="mm")
            draw.text((x0 + cw // 2, 788), country, font=FONT_PILL_SM, fill=C_NEUTRAL, anchor="mm")
            draw.rounded_rectangle([x0 + 30, 835, x0 + cw - 30, 925], radius=10, fill=(24, 68, 108), outline=C_TACTICAL, width=2)
            draw.text((x0 + cw // 2, 880), "1. LAGUNA DULCE INTERIOR", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
            draw.rounded_rectangle([x0 + 30, 950, x0 + cw - 30, 1050], radius=10, fill=(168, 148, 108), outline=C_AMBER, width=3)
            draw.text((x0 + cw // 2, 1000), "2. BARRA DE GRAVA COSTERA", font=FONT_PILL_SM, fill=C_INK, anchor="mm")
            draw.rounded_rectangle([x0 + 30, 1075, x0 + cw - 30, 1205], radius=10, fill=(18, 46, 82), outline=col, width=2)
            draw.text((x0 + cw // 2, 1140), "3. AGUAS DEL CANAL", font=FONT_PILL_SM, fill=C_NEUTRAL, anchor="mm")
            # Synchronized laser scanner bar sweeping across both profiles
            draw.line([(x0 + 12, scan_y), (x0 + cw - 12, scan_y)], fill=C_DANGER, width=4)
        match_p = EASE_OUT(min(1.0, scene_t / 1.1))
        draw_digital_led_box(draw, W // 2, 1340, f"SIMILITUD: {98.4 * match_p:.1f}%", C_AMBER, scale=0.82)
        return frame

    elif scene_id == 9:
        # S09: Slapton Sands Photo + Animated Counter Bars (3.000 Vecinos Evacuados / 30.000 Soldados)
        def _vec9(frame, draw, st, sd):
            p = EASE_OUT(min(1.0, st / 1.2))
            draw.rounded_rectangle([58, 770, 515, 995], radius=14, fill=(16, 20, 28), outline=C_AMBER, width=3)
            draw.text((286, 825), f"{int(3000 * p):,}".replace(",", "."), font=FONT_BIG_NUM, fill=C_AMBER, anchor="mm")
            draw.text((286, 895), "VECINOS EVACUADOS", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
            draw.rectangle([90, 935, 90 + int(390 * p), 958], fill=C_AMBER)

            draw.rounded_rectangle([565, 770, W - 58, 995], radius=14, fill=(14, 26, 44), outline=C_TACTICAL, width=3)
            draw.text((793, 825), f"{int(30000 * p):,}".replace(",", "."), font=FONT_BIG_NUM, fill=C_TACTICAL, anchor="mm")
            draw.text((793, 895), "SOLDADOS REUNIDOS", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
            draw.rectangle([597, 935, 597 + int(390 * p), 958], fill=C_TACTICAL)
        return render_module_a_steady(
            "slapton", scene_t, scene_dur, global_t,
            "MOVILIZACIÓN TOTAL EN SLAPTON SANDS",
            "Vacían pueblos enteros y reúnen a 30.000 hombres para el asalto",
            "FOTO DE ARCHIVO · PLAYA DE SLAPTON SANDS (DEVON) · CC BY-SA 2.0",
            mode="amber", extra_vector_fn=_vec9
        )

    elif scene_id == 10:
        # S10: Cruiser HMS Hawkins + Ballistic Fire-Control HUD & Live Parabolic Shell Arcs
        def _vec10(frame, draw, st, sd):
            for si in range(3):
                p_sh = loop_p(st * 1000.0, 1100.0, phase=si * 0.33)
                sx0, sy0 = 410 + si * 65, 955
                sx1, sy1 = 945, 1185
                # Draw dotted trajectory curve
                for step in range(12):
                    ps = (step / 12.0) * p_sh
                    px = int(sx0 + (sx1 - sx0) * ps)
                    py = int(sy0 + (sy1 - sy0) * ps - 210 * math.sin(math.pi * ps))
                    draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=C_DANGER)
                cx_p = int(sx0 + (sx1 - sx0) * p_sh)
                cy_p = int(sy0 + (sy1 - sy0) * p_sh - 210 * math.sin(math.pi * p_sh))
                draw.ellipse([cx_p - 11, cy_p - 11, cx_p + 11, cy_p + 11], fill=C_AMBER, outline=C_WHITE, width=2)
                # Muzzle flash at turret
                if p_sh < 0.22:
                    r_m = int(28 * (1.0 - p_sh / 0.22))
                    draw.ellipse([sx0 - r_m, sy0 - r_m, sx0 + r_m, sy0 + r_m], fill=C_AMBER, outline=C_DANGER, width=3)
            draw_leader_callout(draw, 475, 955, 755, 785, "CAÑONES NAVALES DE 190 MM", "ORDEN: DISPARAR FUEGO REAL A LA PLAYA", C_DANGER, prog=spring_val(st, 0.08))
        return render_module_a_steady(
            "hawkins", scene_t, scene_dur, global_t,
            "CRUCERO PESADO BRITÁNICO HMS HAWKINS",
            "Bombardeo con munición real minutos antes del desembarco",
            "FOTO DE ARCHIVO · IMPERIAL WAR MUSEUM (HMS HAWKINS) · DOMINIO PÚBLICO",
            mode="danger", extra_vector_fn=_vec10
        )

    elif scene_id == 11:
        # S11: 2.5D Living US Recruits in Landing Craft + Live Decibel/Blast Shockwave Meter (138 dB)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw_ember_particles(frame, global_t, count=14)
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="SIMULACIÓN ACÚSTICA DE ARTILLERÍA · PLAYA DE SLAPTON", mode="amber")
        draw_rossark_water_surface(draw, 1185, global_t, col=C_TACTICAL, n_ripples=4)
        for bx_e in [205, 875]:
            for r in range(1, 4):
                p_r = loop_p(t_ms, 1050.0, phase=r * 0.28)
                rad = int(35 + p_r * 125)
                draw.ellipse([bx_e - rad, 835 - rad, bx_e + rad, 835 + rad], outline=C_DANGER if r % 2 == 0 else C_AMBER, width=max(1, int(4 * bell(p_r))))
        draw_rossark_officer(frame, 390, 990, scale=0.95, role="us_recruit", global_t=global_t, scene_t=scene_t, mood="focused")
        draw_rossark_officer(frame, 690, 990, scale=0.95, role="us_recruit", global_t=global_t + 0.8, scene_t=scene_t, mood="focused")
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([195, 1085, 885, 1215], radius=14, fill=(52, 60, 70), outline=C_NEUTRAL, width=4)
        draw.text((W // 2, 1125), "LANCHA LCVP · RECLUTAS SIN EXPERIENCIA", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        # Live Decibel Meter bar inside landing craft gunwale
        db_val = int(134 + 6 * abs(math.sin(global_t * 12.0)))
        draw.rectangle([250, 1162, 830, 1192], fill=(20, 24, 30), outline=C_AMBER, width=2)
        draw.rectangle([254, 1166, 254 + int(572 * (db_val / 145.0)), 1188], fill=C_DANGER)
        draw.text((W // 2, 1177), f"RUIDO DE EXPLOSIONES: {db_val} dB", font=FONT_HUD, fill=C_WHITE, anchor="mm")
        draw_map_pill(draw, W // 2, 1340, "OBJETIVO: ACOSTUMBRARLOS AL ESTRÉPITO DEL COMBATE", C_AMBER)
        return frame

    elif scene_id == 12:
        # S12: Animated Chain-of-Failure Cascade (Klaxon + 3 Spring-Animated Hazard Domino Cards)
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="ANÁLISIS DE FALLOS EN CADENA · 27-28 ABR 1944", mode="danger")
        kx, ky = W // 2, 760
        burst_p = (global_t % 0.85)
        buzz_dx = int(7 * math.sin(burst_p / 0.45 * 4 * 2 * math.pi)) if burst_p < 0.45 else 0
        # Animated light beams shooting left and right from klaxon
        if int(global_t * 6) % 2 == 0:
            draw.polygon([(kx, ky - 25), (kx - 360, ky - 95), (kx - 360, ky + 45)], fill=(95, 22, 24))
            draw.polygon([(kx, ky - 25), (kx + 360, ky - 95), (kx + 360, ky + 45)], fill=(95, 22, 24))
        draw.rounded_rectangle([kx - 48 + buzz_dx, ky - 60, kx + 48 + buzz_dx, ky + 18], radius=22, fill=C_DANGER, outline=C_WHITE, width=4)
        draw.rectangle([kx - 68 + buzz_dx, ky + 14, kx + 68 + buzz_dx, ky + 38], fill=(55, 60, 70), outline=C_NEUTRAL, width=3)
        cards = [
            ("FALLO 1 · HORA H DESINCRONIZADA", "Retraso de 60 min no llega a todas las lanchas", C_AMBER),
            ("FALLO 2 · ESCOLTA NAVAL CON AVERÍA", "1 de los 2 buques protectores vuelve a puerto", C_DANGER),
            ("FALLO 3 · ERROR DE IMPRENTA EN RADIO", "El convoy de EE. UU. sintoniza otra frecuencia", C_DANGER),
        ]
        for i, (t_str, sub_s, col) in enumerate(cards):
            sp = spring_val(scene_t, i * 0.22, 170, 14)
            if sp > 0.02:
                cy_c = int(855 + i * 172 + (1.0 - min(1.0, sp)) * 45)
                draw.rounded_rectangle([95, cy_c, W - 95, cy_c + 140], radius=14, fill=(38, 16, 20), outline=col, width=3)
                draw.text((W // 2, cy_c + 46), t_str, font=FONT_PILL_MD, fill=col, anchor="mm")
                draw.text((W // 2, cy_c + 98), sub_s, font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
                if i < 2:
                    draw.line([(W // 2, cy_c + 140), (W // 2, cy_c + 172)], fill=C_DANGER, width=5)
        return frame

    elif scene_id == 13:
        # S13: Animated Dual Naval Chronometers (07:30 Original vs Rotating +60 Min -> 08:30 AM)
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="CAMBIO DE HORA H · 27 DE ABRIL DE 1944", mode="amber")
        rot_p = EASE_IN_OUT(min(1.0, scene_t / max(0.6, scene_dur * 0.65)))
        for idx_c, (cx_c, lbl, time_str, h_ang, m_ang, col) in enumerate([
            (275, "LANCHAS (SIN AVISO)", "07:30", 225.0, 180.0, C_DANGER),
            (805, "ORDEN DEL ALMIRANTE", "08:30" if rot_p > 0.5 else "07:30", 225.0 + 30.0 * rot_p, 180.0 + 360.0 * rot_p, C_AMBER)
        ]):
            cy_c, r_c = 895, 155
            draw.ellipse([cx_c - r_c - 6, cy_c - r_c - 6, cx_c + r_c + 6, cy_c + r_c + 6], fill=(38, 34, 30), outline=col, width=4)
            draw.ellipse([cx_c - r_c, cy_c - r_c, cx_c + r_c, cy_c + r_c], fill=C_PAPER)
            if idx_c == 1 and rot_p > 0.05:
                draw.pieslice([cx_c - r_c + 18, cy_c - r_c + 18, cx_c + r_c - 18, cy_c + r_c - 18], start=90, end=90 + int(360 * rot_p), fill=(248, 224, 165))
            for hi in range(12):
                a = math.radians(hi * 30 - 90)
                draw.line([(cx_c + int((r_c - 20) * math.cos(a)), cy_c + int((r_c - 20) * math.sin(a))), (cx_c + int((r_c - 6) * math.cos(a)), cy_c + int((r_c - 6) * math.sin(a)))], fill=C_INK, width=4)
            ha, ma = math.radians(h_ang - 90), math.radians(m_ang - 90)
            draw.line([(cx_c, cy_c), (cx_c + int(90 * math.cos(ha)), cy_c + int(90 * math.sin(ha)))], fill=C_INK, width=8)
            draw.line([(cx_c, cy_c), (cx_c + int(130 * math.cos(ma)), cy_c + int(130 * math.sin(ma)))], fill=col, width=6)
            draw_digital_led_box(draw, cx_c, 1165, time_str, col)
            draw_map_pill(draw, cx_c, 1270, lbl, col)
        # Animated +60 MIN arrow between clocks
        draw.line([(455, 895), (625, 895)], fill=C_AMBER, width=6)
        draw.polygon([(635, 895), (610, 880), (610, 910)], fill=C_AMBER)
        draw.text((540, 860), "+60 MIN", font=FONT_PILL_MD, fill=C_AMBER, anchor="mm")
        draw_map_pill(draw, W // 2, 1365, "EL ALMIRANTE RETRASA LA HORA H UNA HORA COMPLETA", C_AMBER)
        return frame

    elif scene_id == 14:
        # S14: Friendly Fire on Beach at 07:30 AM (Landing Craft + Falling Shells + Blast Shockwaves)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw_ember_particles(frame, global_t, count=16)
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="ALERTA DE FUEGO AMIGO · PLAYA SLAPTON 07:30 AM", mode="danger")
        draw.polygon([(640, 682), (W, 682), (W, 1410), (575, 1410)], fill=(156, 138, 102), outline=C_AMBER, width=4)
        draw.rounded_rectangle([65, 875, 305, 950], radius=12, fill=(58, 68, 82), outline=C_NEUTRAL, width=3)
        draw.text((185, 912), "HMS HAWKINS", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        for i, ly in enumerate([825, 1015, 1195]):
            lx = int(435 + 150 * EASE_OUT(s_prog))
            draw.rounded_rectangle([lx, ly - 24, lx + 115, ly + 24], radius=6, fill=(48, 68, 52), outline=C_WHITE, width=3)
            draw.text((lx + 57, ly), f"LANCHA {i+1}", font=FONT_HUD, fill=C_WHITE, anchor="mm")
            # Animated shell projectile flying along arc
            p_sh = loop_p(t_ms, 950.0, phase=i * 0.33)
            sx = int(185 + (660 - 185) * p_sh)
            sy = int(912 + (ly - 912) * p_sh - 165 * math.sin(math.pi * p_sh))
            draw.arc([185, ly - 155, 665, ly + 40], start=180, end=360, fill=C_DANGER, width=3)
            draw.ellipse([sx - 9, sy - 9, sx + 9, sy + 9], fill=C_AMBER, outline=C_DANGER, width=2)
            rad = int(18 + p_sh * 80)
            draw.ellipse([660 - rad, ly - rad, 660 + rad, ly + rad], outline=C_DANGER, width=max(1, int(4 * bell(p_sh))))
        draw_map_pill(draw, 330, 740, "ARTILLERÍA REAL A LAS 07:30", C_DANGER)
        draw_map_pill(draw, W // 2, 1350, "DESEMBARCAN A LA HORA ORIGINAL BAJO FUEGO ALIADO", C_DANGER)
        return frame

    elif scene_id == 15:
        # S15: Night Radar Scope in Lyme Bay (Madrugada del 28 de Abril en el Mar)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_english_channel_map(draw)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="RADAR NOCTURNO · BAHÍA DE LYME · 01:30 AM", mode="danger")
        cx_r, cy_r = W // 2, 995
        blips = [(420, 940, C_TACTICAL), (490, 965, C_TACTICAL), (640, 1110, C_DANGER), (710, 1140, C_DANGER), (590, 1150, C_DANGER)]
        draw_radar_overlay(draw, cx_r, cy_r, 275, global_t, col=C_TACTICAL, blips=blips)
        draw_digital_led_box(draw, W // 2, 1345, "MADRUGADA · BAHÍA DE LYME", C_DANGER, scale=0.82)
        return frame

    elif scene_id == 16:
        # S16: Steady US Navy LST Photo + Animated 8-Ship Convoy T-4 Column & Cargo Telemetry
        def _vec16(frame, draw, st, sd):
            draw.rounded_rectangle([54, 755, W - 54, 965], radius=14, fill=(12, 24, 42), outline=C_TACTICAL, width=3)
            draw.text((W // 2, 798), "CONVOY T-4 · 8 GRANDES BUQUES ANFIBIOS EN FILA", font=FONT_PILL_MD, fill=C_TACTICAL, anchor="mm")
            lit = int(min(8, (st / max(0.1, sd * 0.65)) * 8 + 1))
            for i in range(8):
                bx = 98 + i * 112
                by = 868
                col = C_AMBER if i < lit else (55, 65, 80)
                draw.rounded_rectangle([bx, by - 22, bx + 92, by + 22], radius=6, fill=(28, 44, 68) if i < lit else (22, 26, 34), outline=col, width=3)
                draw.text((bx + 46, by), f"LST-{i+1}", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
            draw.text((W // 2, 932), "CARGA: MILES DE SOLDADOS + TANQUES SHERMAN + CAMIONES", font=FONT_HUD, fill=C_AMBER, anchor="mm")
        return render_module_a_steady(
            "lst_convoy", scene_t, scene_dur, global_t,
            "CONVOY T-4 · BAHÍA DE LYME",
            "8 buques LST navegan lentamente en fila por la oscuridad del canal",
            "FOTO DE ARCHIVO · US NAVY (BUQUE ANFIBIO LST, 1944) · DOMINIO PÚBLICO",
            mode="tactical", extra_vector_fn=_vec16
        )

    elif scene_id == 17:
        # S17: Animated Naval Escort Shield Breakdown (HMS Azalea Alone vs HMS Scimitar Retreating)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="DEFENSA DEL CONVOY T-4 · ESCOLTAS REALES", mode="danger")
        # 8 LST Convoy Column at bottom
        draw.rounded_rectangle([95, 1115, W - 95, 1245], radius=14, fill=(18, 36, 62), outline=C_TACTICAL, width=3)
        for i in range(8):
            lx = 135 + i * 104
            c_l = C_TACTICAL if i < 4 else C_DANGER
            draw.rounded_rectangle([lx, 1140, lx + 82, 1185], radius=5, fill=(26, 44, 72), outline=c_l, width=2)
        draw.text((310, 1215), "SECTOR CUBIERTO", font=FONT_HUD, fill=C_TACTICAL, anchor="mm")
        draw.text((770, 1215), "FLANCO EXPUESTO SIN ESCOLTA", font=FONT_HUD, fill=C_DANGER, anchor="mm")

        # Left Escort: HMS Azalea (Active Radar Shield)
        draw.rounded_rectangle([95, 760, 505, 1005], radius=16, fill=(14, 38, 64), outline=C_TACTICAL, width=4)
        draw.text((300, 820), "ESCOLTA 1 · HMS AZALEA", font=FONT_PILL_MD, fill=C_TACTICAL, anchor="mm")
        draw.text((300, 875), "CORBETA EN POSICIÓN", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        r_sh = int(35 + 45 * ((global_t * 1.4) % 1.0))
        draw.ellipse([300 - r_sh, 945 - r_sh // 2, 300 + r_sh, 945 + r_sh // 2], outline=C_TACTICAL, width=3)

        # Right Escort: HMS Scimitar (Broken / Retreating to Plymouth)
        draw.rounded_rectangle([555, 760, W - 95, 1005], radius=16, fill=(46, 18, 20), outline=C_DANGER, width=4)
        draw.text((770, 820), "ESCOLTA 2 · HMS SCIMITAR", font=FONT_PILL_MD, fill=C_DANGER, anchor="mm")
        draw.text((770, 875), "VOLVIÓ A PUERTO POR AVERÍA", font=FONT_PILL_SM, fill=C_AMBER, anchor="mm")
        p_x = EASE_OUT(min(1.0, scene_t / 0.6))
        draw.line([(610, 790), (610 + int(320 * p_x), 790 + int(185 * p_x))], fill=C_DANGER, width=7)
        draw.line([(930, 790), (930 - int(320 * p_x), 790 + int(185 * p_x))], fill=C_DANGER, width=7)
        draw_map_pill(draw, W // 2, 1340, "8 GRANDES TRANSPORTES PROTEGIDOS POR UN SOLO BARCO", C_DANGER)
        return frame

    elif scene_id == 18:
        # S18: German Schnellboot Archival Photo + 9 Animated Wolfpack Attack Chevrons
        def _vec18(frame, draw, st, sd):
            # 9 animated red attack vector chevrons locking in
            draw.rounded_rectangle([54, 755, W - 54, 895], radius=12, fill=(28, 12, 16), outline=C_DANGER, width=3)
            draw.text((W // 2, 790), "MANADA DE 9 TORPEDERAS ALEMANAS (SCHNELLBOOTE)", font=FONT_PILL_SM, fill=C_AMBER, anchor="mm")
            lit_s = int(min(9, (st / max(0.2, sd * 0.65)) * 9 + 1))
            for i in range(9):
                sx = 92 + i * 102
                sy = 848
                active = i < lit_s
                col = C_DANGER if active else (60, 40, 44)
                draw.polygon([(sx, sy - 16), (sx + 68, sy), (sx, sy + 16), (sx + 16, sy)], fill=col, outline=C_WHITE if active else col, width=2)
            draw_digital_led_box(draw, 310, 1205, "9 S-BOOTE · 40 KT", C_DANGER, scale=0.80)
        return render_module_a_steady(
            "s_boot", scene_t, scene_dur, global_t,
            "KRIEGSMARINE · 9 LANCHAS RÁPIDAS S-BOOT",
            "En la oscuridad aparecen 9 torpederas alemanas armadas hasta los dientes",
            "FOTO DE ARCHIVO · BUNDESARCHIV (SCHNELLBOOT S-BOOT) · CC BY-SA 3.0",
            mode="danger", extra_vector_fn=_vec18
        )

    elif scene_id == 19:
        # S19: 2.5D British Officer on HMS Azalea + Live Oscilloscope Radio Transmission (2880 kHz)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="TRANSMISIÓN DE EMERGENCIA · HMS AZALEA (2880 KHZ)", mode="tactical")
        draw_rossark_officer(frame, 285, 985, scale=1.05, role="british_officer", global_t=global_t, scene_t=scene_t, talking=True, mood="focused", gesture="point_order")
        draw = ImageDraw.Draw(frame)
        draw_map_pill(draw, 285, 1215, "CORBETA BRITÁNICA HMS AZALEA", C_TACTICAL)
        tx_a, ty_a = 640, 865
        draw.line([(tx_a, ty_a + 185), (tx_a, ty_a)], fill=C_NEUTRAL, width=8)
        draw.ellipse([tx_a - 14, ty_a - 14, tx_a + 14, ty_a + 14], fill=C_AMBER)
        for r in range(1, 5):
            p_w = loop_p(t_ms, 1150.0, phase=r * 0.25)
            rad = int(35 + p_w * 205)
            draw.ellipse([tx_a - rad, ty_a - rad, tx_a + rad, ty_a + rad], outline=C_TACTICAL, width=max(1, int(4 * bell(p_w))))
        # Live animated radio waveform box
        draw.rounded_rectangle([490, 1085, 975, 1215], radius=12, fill=(14, 24, 42), outline=C_AMBER, width=3)
        w_pts = [(x, int(1135 + 24 * math.sin((x - 510) * 0.09 - global_t * 18.0))) for x in range(515, 955, 8)]
        draw.line(w_pts, fill=C_AMBER, width=3)
        draw.text((732, 1190), "TX: 2880 KHZ · ¡ENEMIGO EN RADAR!", font=FONT_HUD, fill=C_WHITE, anchor="mm")
        draw_map_pill(draw, W // 2, 1340, "DETECTA LAS TORPEDERAS Y EMITE ALERTA POR RADIO", C_TACTICAL)
        return frame

    elif scene_id == 20:
        # S20: Module C — Reconstructed Communications Order with Misprinted Radio Frequency
        return render_module_c_document_with_hand(
            scene_t, global_t,
            "ORDEN DE COMUNICACIONES · EJERCICIO TIGRE (ABRIL 1944)",
            "ASIGNACIÓN DE FRECUENCIAS RADIALES DEL CONVOY T-4:",
            [
                "• Escolta Británica (HMS Azalea): 2880 kHz",
                "• Buques LST de EE. UU.: 3880 kHz [ERRATA]",
                "• Error de imprenta en las órdenes escritas.",
                "• Resultado: Incompatibilidad total de radio."
            ],
            highlight_idx={1, 2},
            stamp_text="ERROR DE IMPRENTA",
            source_attr="FUENTE HISTÓRICA · INFORME DEL ALMIRANTAZGO Y US NAVY (1944)",
            tilt_deg=-1.5
        )

    elif scene_id == 21:
        # S21: Dual Radio Frequency Tuner Mismatch (2880 kHz Active vs 3880 kHz Flatline Silence)
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="FALLO DE ENLACE RADIAL · RECEPTORES DESINCRONIZADOS", mode="danger")
        # Top Tuner: UK 2880 kHz (Live Waveform)
        draw.rounded_rectangle([85, 725, W - 85, 945], radius=16, fill=(14, 34, 58), outline=C_TACTICAL, width=3)
        draw.text((295, 775), "RADIO BRITÁNICA (UK)", font=FONT_PILL_MD, fill=C_TACTICAL, anchor="mm")
        draw.text((295, 835), "2880 kHz", font=FONT_BIG_NUM, fill=C_WHITE, anchor="mm")
        pts_uk = [(x, int(835 + 42 * math.sin((x - 520) * 0.08 - global_t * 16.0) * math.sin((x - 520) * math.pi / 410.0))) for x in range(520, 930, 8)]
        draw.line(pts_uk, fill=C_TACTICAL, width=4)

        # Severed Link Badge in Center
        draw.ellipse([W // 2 - 42, 995 - 42, W // 2 + 42, 995 + 42], fill=(42, 14, 18), outline=C_DANGER, width=4)
        draw.text((W // 2, 995), "X", font=FONT_HEADLINE, fill=C_DANGER, anchor="mm")

        # Bottom Tuner: US 3880 kHz (Flatline 0.0 dB!)
        draw.rounded_rectangle([85, 1045, W - 85, 1265], radius=16, fill=(42, 16, 20), outline=C_DANGER, width=4)
        draw.text((295, 1095), "CONVOY EE. UU. (LST)", font=FONT_PILL_MD, fill=C_DANGER, anchor="mm")
        draw.text((295, 1155), "3880 kHz", font=FONT_BIG_NUM, fill=C_AMBER, anchor="mm")
        draw.line([(520, 1155), (930, 1155)], fill=C_DANGER, width=4)
        draw.text((725, 1120), "SILENCIO TOTAL (0.0 dB)", font=FONT_HUD, fill=C_DANGER, anchor="mm")
        draw_map_pill(draw, W // 2, 1350, "NUNCA ESCUCHAN LA ALERTA DE ATAQUE ENEMIGO", C_DANGER)
        return frame

    elif scene_id == 22:
        # S22: 2D Tactical Night Battle Map of Lyme Bay (9 S-Boote Torpedoing the 8 US LSTs)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw_ember_particles(frame, global_t, count=18)
        draw = ImageDraw.Draw(frame)
        draw_english_channel_map(draw)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="COMBATE NOCTURNO EN BAHÍA DE LYME · 01:30 - 03:30 AM", mode="danger")
        lst_coords = [(260, 955), (395, 975), (535, 995), (675, 1015), (810, 1035)]
        for i, (lx, ly) in enumerate(lst_coords):
            is_hit = i in (1, 2, 3)
            draw_lst_ship(draw, lx, ly, scale=0.38, on_fire=is_hit)
            if is_hit:
                p_b = loop_p(t_ms, 950.0, phase=i * 0.3)
                rad = int(18 + p_b * 65)
                draw.ellipse([lx - rad, ly - rad, lx + rad, ly + rad], outline=C_DANGER, width=max(1, int(4 * bell(p_b))))
        for si, sx in enumerate([310, 520, 730]):
            sy = 1205
            draw_sboot(draw, sx, sy, scale=0.58, facing="left")
            p_torp = loop_p(t_ms, 1300.0, phase=si * 0.33)
            tx_cur = int(sx + 65 * p_torp)
            ty_cur = int(sy - 15 - (sy - 1010) * p_torp)
            draw.line([(sx, sy - 15), (tx_cur, ty_cur)], fill=C_AMBER, width=4)
            draw.ellipse([tx_cur - 7, ty_cur - 7, tx_cur + 7, ty_cur + 7], fill=C_DANGER, outline=C_WHITE, width=2)
        draw_digital_led_box(draw, 320, 775, "2 HORAS DE ATAQUE", C_DANGER, scale=0.72)
        draw_map_pill(draw, W // 2, 1345, "TORPEDOS ALEMANES CONTRA EL CONVOY CASI SIN OPOSICIÓN", C_DANGER)
        return frame

    elif scene_id == 23:
        # S23: Burning LST Archival Photo + Embers + Animated Hull Integrity Bars
        def _vec23(frame, draw, st, sd):
            draw_ember_particles(frame, global_t, count=20)
            draw = ImageDraw.Draw(frame)
            ships = [
                ("LST-507", "INCENDIADO Y ABANDONADO", 0.0, C_DANGER),
                ("LST-531", "2 TORPEDOS · HUNDIDO EN 6 MIN", 0.0, C_DANGER),
                ("LST-289", "GRAVEMENTE AVERIADO (POPA)", 0.38, C_AMBER),
            ]
            p_drop = EASE_OUT(min(1.0, st / 1.1))
            for i, (sh_id, st_txt, target_hp, col) in enumerate(ships):
                py = 760 + i * 82
                draw.rounded_rectangle([54, py, 615, py + 68], radius=10, fill=(16, 15, 22), outline=col, width=3)
                draw.text((74, py + 24), f"{sh_id}: {st_txt}", font=FONT_PILL_SM, fill=C_WHITE, anchor="lm")
                hp_cur = 1.0 - (1.0 - target_hp) * p_drop
                draw.rectangle([74, py + 46, 590, py + 58], fill=(35, 38, 46))
                draw.rectangle([74, py + 46, 74 + int(516 * hp_cur), py + 58], fill=col)
        return render_module_a_steady(
            "lst_burning", scene_t, scene_dur, global_t,
            "2 TRANSPORTES EN LLAMAS Y 1 AVERIADO",
            "Dos buques gigantes llenos de tropas arden en mitad de la noche",
            "FOTO DE ARCHIVO · US NAVY (BUQUE LST EN LLAMAS, 1944) · DOMINIO PÚBLICO",
            mode="danger", extra_vector_fn=_vec23
        )

    elif scene_id == 24:
        # S24: Freezing Channel Water (7 °C) + Animated Thermometer & Soldiers Sinking with 30 kg Packs
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="TEMPERATURA DEL AGUA: 7 °C · HIPOTERMIA AGUDA", mode="tactical")
        draw_rossark_water_surface(draw, 865, global_t, col=C_TACTICAL, n_ripples=4)
        draw_lst_ship(draw, 310, 825, scale=1.1, on_fire=True)
        draw_rossark_smoke_and_fire(frame, 310, 800, global_t, count=4, scale=0.75)
        draw = ImageDraw.Draw(frame)
        for i, sx in enumerate([240, 460, 680]):
            sy = int(935 + i * 48 + 110 * EASE_IN_OUT(s_prog))
            draw.ellipse([sx - 18, sy - 42, sx + 18, sy - 6], fill=C_NEUTRAL, outline=C_TACTICAL, width=2)
            draw.rounded_rectangle([sx - 24, sy, sx + 24, sy + 64], radius=8, fill=(68, 76, 48), outline=C_WHITE, width=2)
            draw.rectangle([sx + 20, sy + 6, sx + 64, sy + 54], fill=C_DANGER, outline=C_WHITE, width=2)
            draw.text((sx + 42, sy + 30), "30KG", font=FONT_HUD, fill=C_WHITE, anchor="mm")
            # Downward gravity vector arrow
            draw.line([(sx, sy + 72), (sx, sy + 125)], fill=C_DANGER, width=5)
            draw.polygon([(sx, sy + 135), (sx - 10, sy + 115), (sx + 10, sy + 115)], fill=C_DANGER)
        # Animated Thermometer on Right
        tx0, ty0 = 885, 760
        draw.rounded_rectangle([tx0 - 28, ty0, tx0 + 28, ty0 + 360], radius=24, fill=(16, 26, 44), outline=C_TACTICAL, width=3)
        merc_h = int(280 * (1.0 - 0.72 * EASE_OUT(s_prog)))
        draw.rectangle([tx0 - 14, ty0 + 330 - merc_h, tx0 + 14, ty0 + 330], fill=C_TACTICAL)
        draw.ellipse([tx0 - 38, ty0 + 310, tx0 + 38, ty0 + 386], fill=C_TACTICAL, outline=C_WHITE, width=3)
        draw.text((tx0, ty0 + 425), "7 °C", font=FONT_BIG_NUM, fill=C_TACTICAL, anchor="mm")
        draw_map_pill(draw, W // 2, 1345, "SALTAN AL AGUA HELADA CARGADOS CON EQUIPO PESADO", C_DANGER)
        return frame

    elif scene_id == 25:
        # S25: Animated Physics & Buoyancy Inversion Diagram (M1926 Lifebelt Worn at Waist)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="FÍSICA DE FLOTACIÓN · CINTURÓN SALVAVIDAS M1926", mode="danger")
        # Left Card: Correct Placement (Chest / Armpits)
        draw.rounded_rectangle([60, 715, 505, 1265], radius=16, fill=(14, 34, 58), outline=C_TACTICAL, width=3)
        draw.text((282, 765), "CORRECTO (EN AXILAS)", font=FONT_PILL_MD, fill=C_TACTICAL, anchor="mm")
        draw.line([(90, 985), (475, 985)], fill=C_TACTICAL, width=4)
        draw.ellipse([282 - 26, 865, 282 + 26, 917], fill=C_NEUTRAL, outline=C_WHITE, width=2)
        draw.rounded_rectangle([282 - 34, 922, 282 + 34, 1085], radius=12, fill=(68, 76, 48), outline=C_WHITE, width=2)
        draw.rounded_rectangle([282 - 50, 942, 282 + 50, 974], radius=10, fill=C_AMBER, outline=C_WHITE, width=3)
        draw.text((282, 1185), "CABEZA FUERA DEL AGUA", font=FONT_PILL_SM, fill=C_TACTICAL, anchor="mm")

        # Right Card: Dynamic 180-Degree Rotation Animation of Soldier Flipping Head-Down!
        draw.rounded_rectangle([555, 715, W - 60, 1265], radius=16, fill=(44, 16, 18), outline=C_DANGER, width=4)
        draw.text((787, 765), "ERROR FATAL (EN CINTURA)", font=FONT_PILL_MD, fill=C_DANGER, anchor="mm")
        draw.line([(585, 985), (990, 985)], fill=C_TACTICAL, width=4)
        fig = Image.new("RGBA", (240, 260), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fig)
        fd.ellipse([120 - 24, 20, 120 + 24, 68], fill=C_DANGER + (255,), outline=C_WHITE + (255,), width=2)
        fd.rounded_rectangle([120 - 32, 72, 120 + 32, 220], radius=12, fill=(68, 76, 48, 255), outline=C_WHITE + (255,), width=2)
        fd.rounded_rectangle([120 - 50, 130, 120 + 50, 162], radius=10, fill=C_AMBER + (255,), outline=C_WHITE + (255,), width=3)
        flip_deg = 180.0 * EASE_IN_OUT(min(1.0, scene_t / max(0.5, scene_dur * 0.55)))
        fig_rot = fig.rotate(flip_deg, resample=Image.Resampling.BICUBIC, expand=False)
        frame.paste(fig_rot, (787 - 120, 985 - 130), fig_rot)
        draw = ImageDraw.Draw(frame)
        draw.arc([695, 885, 879, 1085], start=20, end=160, fill=C_DANGER, width=5)
        draw.text((787, 1185), "LOS HUNDE DE CABEZA", font=FONT_PILL_SM, fill=C_DANGER, anchor="mm")
        draw_map_pill(draw, W // 2, 1345, "EL FLOTADOR EN LA CINTURA Y LA MOCHILA LOS VUELCAN", C_DANGER)
        return frame

    elif scene_id == 26:
        # S26: Dawn Over the Channel + Kinetic Casualty Counter: 749 MUERTOS (551 Army + 198 Navy)
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="BALANCE OFICIAL DE VÍCTIMAS · OPERACIÓN TIGRE", mode="danger")
        p_c = EASE_OUT(min(1.0, scene_t / max(0.4, scene_dur * 0.55)))
        cnt = int(749 * p_c)
        draw.rounded_rectangle([80, 705, W - 80, 1035], radius=20, fill=(38, 15, 18), outline=C_DANGER, width=4)
        draw.text((W // 2, 835), f"{cnt}", font=load_font(["C:/Windows/Fonts/segoeuib.ttf"], 142), fill=C_DANGER, anchor="mm")
        draw.text((W // 2, 965), "SOLDADOS Y MARINEROS ESTADOUNIDENSES MUERTOS", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        # Animated breakdown cards with progress bars
        draw.rounded_rectangle([80, 1075, 520, 1260], radius=14, fill=(24, 26, 34), outline=C_AMBER, width=3)
        draw.text((300, 1125), f"{int(551 * p_c)} DEL EJÉRCITO", font=FONT_PILL_LG, fill=C_AMBER, anchor="mm")
        draw.text((300, 1175), "INGENIEROS Y ARTILLERÍA", font=FONT_PILL_SM, fill=C_NEUTRAL, anchor="mm")
        draw.rectangle([115, 1212, 115 + int(370 * p_c), 1232], fill=C_AMBER)

        draw.rounded_rectangle([560, 1075, W - 80, 1260], radius=14, fill=(16, 28, 46), outline=C_TACTICAL, width=3)
        draw.text((780, 1125), f"{int(198 * p_c)} DE LA MARINA", font=FONT_PILL_LG, fill=C_TACTICAL, anchor="mm")
        draw.text((780, 1175), "TRIPULANTES DE LST", font=FONT_PILL_SM, fill=C_NEUTRAL, anchor="mm")
        draw.rectangle([595, 1212, 595 + int(370 * (198 / 551.0) * p_c), 1232], fill=C_TACTICAL)
        draw_map_pill(draw, W // 2, 1345, "EL ENSAYO MÁS MORTÍFERO DE LA SEGUNDA GUERRA MUNDIAL", C_DANGER)
        return frame

    elif scene_id == 27:
        # S27: Rossark One-Shot Draw-On Comparative Bar Chart: 749 (Ensayo) vs 197 (Playa Utah Real)
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="COMPARATIVA HISTÓRICA DE BAJAS · ENSAYO vs. DÍA D", mode="amber")
        base_y = 1235
        draw.line([(110, base_y), (W - 110, base_y)], fill=C_NEUTRAL, width=4)
        p1 = EASE_OUT(min(1.0, scene_t / 0.80))
        h1 = int(460 * p1)
        draw.rounded_rectangle([195, base_y - h1, 455, base_y], radius=12, fill=C_DANGER, outline=C_WHITE, width=3)
        draw.text((325, base_y - h1 - 42), f"{int(749 * p1)} MUERTOS", font=FONT_PILL_LG, fill=C_DANGER, anchor="mm")
        draw.text((325, base_y + 42), "ENSAYO TIGRE", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        draw.text((325, base_y + 80), "(INGLATERRA)", font=FONT_PILL_SM, fill=C_NEUTRAL, anchor="mm")

        p2 = EASE_OUT(min(1.0, max(0.0, (scene_t - 0.18) / 0.80)))
        h2 = int(121 * p2)
        draw.rounded_rectangle([625, base_y - h2, 885, base_y], radius=12, fill=C_TACTICAL, outline=C_WHITE, width=3)
        draw.text((755, base_y - h2 - 42), f"{int(197 * p2)} MUERTOS", font=FONT_PILL_LG, fill=C_TACTICAL, anchor="mm")
        draw.text((755, base_y + 42), "PLAYA DE UTAH", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        draw.text((755, base_y + 80), "(DÍA D REAL)", font=FONT_PILL_SM, fill=C_NEUTRAL, anchor="mm")
        draw_digital_led_box(draw, 755, 830, "CASI 4X MÁS", C_AMBER, scale=0.85)
        return frame

    elif scene_id == 28:
        # S28: Steady Archival Photo of Normandy D-Day Landing (Into the Jaws of Death, June 6, 1944)
        def _vec28(frame, draw, st, sd):
            draw_leader_callout(draw, 540, 1040, 740, 815, "PLAYA DE UTAH · 6 JUN 1944", "197 BAJAS EN EL ASALTO REAL", C_TACTICAL, prog=spring_val(st, 0.08))
        return render_module_a_steady(
            "utah", scene_t, scene_dur, global_t,
            "DESEMBARCO REAL EN NORMANDÍA · 6 JUN 1944",
            "En el desembarco real de Playa Utah murieron 197 soldados (vs. 749 en el ensayo)",
            "FOTO DE ARCHIVO · US COAST GUARD (ROBERT F. SARGENT), 1944 · DOMINIO PÚBLICO",
            mode="tactical", extra_vector_fn=_vec28
        )

    elif scene_id == 29:
        # S29: 2.5D Living Rossark General Eisenhower + Flashing Security Breach Radar HUD
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="CUARTEL GENERAL SHAEF · ALERTA DE CONTRESPIONAJE", mode="danger")
        cx_e, cy_e = W // 2, 965
        draw.polygon([(cx_e - 110, 682), (cx_e + 110, 682), (cx_e + 360, 1390), (cx_e - 360, 1390)], fill=(54, 18, 22))
        draw_radar_overlay(draw, cx_e, 920, 250, global_t, col=C_DANGER, blips=[(390, 860, C_AMBER), (690, 950, C_DANGER)])
        draw_rossark_officer(frame, cx_e, cy_e, scale=1.48, role="eisenhower", global_t=global_t, scene_t=scene_t, talking=True, mood="focused", gesture="stop_hand")
        draw = ImageDraw.Draw(frame)
        draw_digital_led_box(draw, cx_e, 1290, "RIESGO CRÍTICO: BIGOT", C_DANGER, scale=0.85)
        return frame

    elif scene_id == 30:
        # S30: Module C — Reconstructed Top-Secret BIGOT Dossier + Vector Hand + Stamp
        return render_module_c_document_with_hand(
            scene_t, global_t,
            "CUARTEL GENERAL SUPREMO (SHAEF) · EXPEDIENTE ULTRA SECRETO",
            "CLASIFICACIÓN DE MÁXIMA SEGURIDAD: NIVEL «BIGOT»",
            [
                "• 10 oficiales con acceso BIGOT desaparecidos.",
                "• Viajaban a bordo de los buques LST hundidos.",
                "• Poseían los planos exactos de la Operación Overlord.",
                "• Estado actual: PARADERO DESCONOCIDO EN EL MAR."
            ],
            highlight_idx={0, 2},
            stamp_text="ACCESO BIGOT",
            source_attr="FUENTE HISTÓRICA · ARCHIVOS SHAEF / OPERACIÓN OVERLORD (1944)",
            tilt_deg=-1.4
        )

    elif scene_id == 31:
        # S31: Secret Normandy Invasion Beaches Map Locked Behind BIGOT Clearance
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_english_channel_map(draw)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="PLANOS SECRETOS DE OVERLORD · NIVEL BIGOT", mode="amber")
        beaches = [(385, 1185, "UTAH"), (490, 1235, "OMAHA"), (615, 1250, "GOLD"), (745, 1240, "JUNO"), (875, 1215, "SWORD")]
        for i, (bx, by, bname) in enumerate(beaches):
            p_b = spring_val(scene_t, i * 0.12)
            r_p = int(14 + 8 * abs(math.sin(global_t * 6.0 + i)))
            draw.ellipse([bx - r_p, by - r_p, bx + r_p, by + r_p], outline=C_DANGER, width=3)
            draw.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=C_AMBER)
            draw_map_pill(draw, bx, by - 44, bname, C_AMBER, enter_prog=p_b)
        draw_digital_led_box(draw, W // 2, 835, "FECHA Y 5 PLAYAS SECRETAS", C_AMBER, scale=0.78)
        draw_map_pill(draw, W // 2, 955, "INFORMACIÓN QUE SOLO POSEÍAN LOS OFICIALES «BIGOT»", C_DANGER)
        return frame

    elif scene_id == 32:
        # S32: Animated 3-Stage Intelligence Breach Flow Diagram (If 1 Captured -> Hitler Knows All)
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="SIMULACIÓN DE FILTRACIÓN DE INTELIGENCIA", mode="danger")
        steps = [
            ("1. UN OFICIAL «BIGOT» CAPTURADO VIVO", "Rescatado del mar por una torpedera alemana S-Boot", C_AMBER),
            ("2. INTERROGATORIO DE LA INTELIGENCIA ALEMANA", "Descubren la fecha y las playas exactas (Utah / Omaha)", C_DANGER),
            ("3. HITLER CONOCE TODO EL PLAN DEL DÍA D", "Las divisiones Panzer esperan en la arena de Normandía", C_DANGER),
        ]
        for i, (title_s, sub_s, col) in enumerate(steps):
            sp = spring_val(scene_t, i * 0.25, 175, 14)
            if sp > 0.02:
                cy_s = int(720 + i * 208 + (1.0 - min(1.0, sp)) * 40)
                draw.rounded_rectangle([85, cy_s, W - 85, cy_s + 148], radius=16, fill=(42, 16, 20) if i > 0 else (36, 28, 16), outline=col, width=4)
                draw.text((W // 2, cy_s + 50), title_s, font=FONT_PILL_MD, fill=col, anchor="mm")
                draw.text((W // 2, cy_s + 104), sub_s, font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
                if i < 2:
                    draw.line([(W // 2, cy_s + 148), (W // 2, cy_s + 208)], fill=C_DANGER, width=6)
        draw_map_pill(draw, W // 2, 1365, "UN SOLO PRISIONERO VIVO DESTRUÍA LA OPERACIÓN OVERLORD", C_DANGER)
        return frame

    elif scene_id == 33:
        # S33: 10 BIGOT Officers Recovery Checklist Matrix + Sonar Sweep (10 / 10 Bodies Recovered)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="OPERACIÓN DE BÚSQUEDA SUBMARINA · BUZOS ALIADOS", mode="tactical")
        found_count = int(min(10, max(1, (scene_t / max(0.5, scene_dur * 0.72)) * 11)))
        for i in range(10):
            col_i, row_i = i % 2, i // 2
            cx0, cy0 = 85 + col_i * 470, 705 + row_i * 106
            is_found = i < found_count
            bg_c = (14, 48, 72) if is_found else (48, 18, 20)
            bd_c = C_TACTICAL if is_found else C_DANGER
            draw.rounded_rectangle([cx0, cy0, cx0 + 440, cy0 + 88], radius=12, fill=bg_c, outline=bd_c, width=3)
            st_lbl = "✓ CUERPO RECUPERADO" if is_found else "? BUSCANDO EN EL MAR"
            draw.text((cx0 + 220, cy0 + 44), f"BIGOT #{i+1:02d} · {st_lbl}", font=FONT_PILL_SM, fill=C_WHITE if is_found else C_AMBER, anchor="mm")
        draw_digital_led_box(draw, W // 2, 1315, f"{found_count} / 10 IDENTIFICADOS", C_TACTICAL if found_count == 10 else C_AMBER, scale=0.85)
        return frame

    elif scene_id == 34:
        # S34: Module C — Reconstructed SHAEF Gag Order under Threat of Court-Martial
        return render_module_c_document_with_hand(
            scene_t, global_t,
            "ORDEN GENERAL DE CENSURA · COMANDO SUPREMO ALIADO (1944)",
            "DIRECTIVA DE SECRETO ABSOLUTO SOBRE SLAPTON SANDS:",
            [
                "• Prohibido a todo sobreviviente hablar del ataque.",
                "• Médicos y enfermeras bajo juramento de silencio.",
                "• Las 749 bajas se registran sin revelar el lugar.",
                "• Infracción sujeta a CONSEJO DE GUERRA inmediato."
            ],
            highlight_idx={0, 3},
            stamp_text="CONSEJO DE GUERRA",
            source_attr="FUENTE HISTÓRICA · ORDEN DE CENSURA SHAEF (ABRIL DE 1944)",
            tilt_deg=1.4
        )

    elif scene_id == 35:
        # S35: Steady Archival Photo of Torcross Sherman DD Tank Memorial + Dual Casualty HUD
        def _vec35(frame, draw, st, sd):
            sp = spring_val(st, 0.08)
            draw.rounded_rectangle([58, 765, 515, 925], radius=14, fill=(44, 16, 20), outline=C_DANGER, width=3)
            draw.text((286, 820), "INGLATERRA: 749", font=FONT_PILL_LG, fill=C_DANGER, anchor="mm")
            draw.text((286, 880), "PRACTICANDO EN EL ENSAYO", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")

            draw.rounded_rectangle([565, 765, W - 58, 925], radius=14, fill=(14, 34, 58), outline=C_TACTICAL, width=3)
            draw.text((793, 820), "FRANCIA: 197", font=FONT_PILL_LG, fill=C_TACTICAL, anchor="mm")
            draw.text((793, 880), "TOMANDO LA PLAYA REAL", font=FONT_PILL_SM, fill=C_WHITE, anchor="mm")
        return render_module_a_steady(
            "sherman", scene_t, scene_dur, global_t,
            "MEMORIAL DE TORCROSS · TANQUE SHERMAN DD",
            "Murieron más hombres practicando en Inglaterra que tomando Playa Utah",
            "FOTO DE ARCHIVO · MEMORIAL OPERACIÓN TIGRE (TORCROSS) · CC BY-SA 2.0",
            mode="amber", extra_vector_fn=_vec35
        )

    elif scene_id == 36:
        # S36: Module D — Golden Balance Scale Tipping with Dropping Weights (Eisenhower's Dilemma)
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="DECISIÓN DEL COMANDANTE SUPREMO · SHAEF", mode="amber")
        tilt = 11.5 * EASE_IN_OUT(min(1.0, max(0.0, (scene_t - 0.15) / 1.0))) + 1.4 * wave(t_ms, 3000.0)
        draw_balance_scale(
            draw, W // 2, 1345,
            tilt_deg=tilt,
            left_pills=["FALTA 1 CUERPO BIGOT", "¿PLAN FILTRADO A HITLER?"],
            right_pills=["INVASIÓN EN MARCHA", "NO PERDER LA SORPRESA"],
            left_title="CANCELAR EL DÍA D",
            right_title="ATACAR IGUAL",
            left_col=C_DANGER,
            right_col=C_TACTICAL,
            drop_prog=s_prog * 1.4
        )
        return frame

    else:
        # S37: Final Tribunal Dilemma Over Steady LST Convoy Backdrop + Rossark Jiggle Buttons!
        frame = PHOTOS_STEADY_STAGE.get("lst_convoy", CANVAS_ABYSS).copy()
        draw = ImageDraw.Draw(frame)
        draw_tactical_hud_frame(frame, draw, global_t, scene_t, sector_txt="DECISIÓN FINAL · ¿QUÉ HABRÍAS HECHO VOS?", mode="amber")
        for r in range(2):
            rp = loop_p(t_ms, 1500.0, phase=r * 0.5)
            rad = int(50 + rp * 250)
            draw.ellipse([W // 2 - rad, 915 - rad, W // 2 + rad, 915 + rad], outline=C_AMBER, width=max(1, int(3 * bell(rp))))
        draw_rossark_jiggle_button(draw, W // 2, 1105, 630, 82, "CANCELAR EL DÍA D", (44, 16, 20), C_DANGER, global_t, phase_offset=0.0)
        draw_rossark_jiggle_button(draw, W // 2, 1210, 670, 82, "ATACAR NORMANDÍA IGUAL", (14, 30, 56), C_TACTICAL, global_t, phase_offset=0.5)
        draw.rounded_rectangle([130, 1295, W - 130, 1375], radius=12, fill=(16, 18, 24), outline=C_AMBER, width=3)
        draw.text((W // 2, 1335), "CONTÁMELO EN LOS COMENTARIOS", font=FONT_PILL_MD, fill=C_AMBER, anchor="mm")
        draw_attribution_pill(draw, "FOTO DE ARCHIVO · US NAVY (BUQUE ANFIBIO LST, 1944) · DOMINIO PÚBLICO")
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
    slide_y = int((1.0 - min(1.0, scene_t / 0.16)) * 14)
    draw.text((W // 2 + 3, 558 + slide_y), title, font=FONT_HEADLINE, fill=(0, 0, 0), anchor="mm")
    draw.text((W // 2, 555 + slide_y), title, font=FONT_HEADLINE, fill=t_col, anchor="mm")
    if subtitle:
        draw.text((W // 2 + 2, 614 + slide_y), subtitle, font=FONT_SUBHEAD, fill=(0, 0, 0), anchor="mm")
        draw.text((W // 2, 612 + slide_y), subtitle, font=FONT_SUBHEAD, fill=(215, 212, 205), anchor="mm")

    if chunk_idx is None:
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
        lines, cur_line, cur_w = [], [], 0
        space_w = FONT_SUB_BOLD.getlength(" ")
        for wi, wo in group_words:
            w_px = FONT_SUB_BOLD.getlength(wo["word"])
            if cur_line and (cur_w + space_w + w_px > 860):
                lines.append(cur_line)
                cur_line, cur_w = [(wi, wo)], w_px
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
                        s_draw.rectangle([bx0, by0, bx1, by1], fill=(59, 130, 246, 56), outline=(59, 130, 246, 255), width=3)
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
    return 0, 0, 1, 0.0, 2.5

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

srt_path = "produccion/03_operacion_tigre/operacion_tigre_es.srt"
with open(srt_path, "w", encoding="utf-8") as sf:
    for idx_c, ch in enumerate(CHUNKS, 1):
        sf.write(f"{idx_c}\n")
        sf.write(f"{format_srt_time(ch['start'])} --> {format_srt_time(ch['end'])}\n")
        sf.write(f"{ch['text']}\n\n")

print("Rendering 12-frame verification mosaic (storyboard_verificacion.jpg)...")
sample_times = [1.2, 4.2, 10.2, 14.5, 23.5, 33.5, 44.5, 62.5, 83.0, 99.5, 112.5, 159.5]
grid = Image.new("RGB", (4 * 270, 3 * 480), (0, 0, 0))
for i, st in enumerate(sample_times):
    f_im = render_frame_at(st).resize((270, 480), Image.Resampling.LANCZOS)
    grid.paste(f_im, ((i % 4) * 270, (i // 4) * 480))
grid.save("produccion/03_operacion_tigre/storyboard_verificacion.jpg", quality=92)

cover_img = render_frame_at(1.2)
cover_img.save("produccion/03_operacion_tigre/portada_operacion_tigre.png")

if "--storyboard-only" in sys.argv:
    print("Storyboard verification complete.")
    sys.exit(0)

INTERNAL_FPS = 30
total_frames = int(TOTAL_DUR * INTERNAL_FPS)
out_mp4 = "produccion/03_operacion_tigre/operacion_tigre_short.mp4"
audio_path = "produccion/03_operacion_tigre/audio/audio_master_180s.wav"

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
    "-af", "volume=7.1dB,alimiter=limit=-1.5dB:level=disabled",
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
