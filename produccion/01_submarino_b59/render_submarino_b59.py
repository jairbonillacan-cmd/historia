import os
import sys
import json
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1920

# Load timeline
with open("produccion/01_submarino_b59/timeline_84_chunks.json", "r", encoding="utf-8") as f:
    TL_DATA = json.load(f)
TOTAL_DUR = TL_DATA["total_duration"]
CHUNKS = TL_DATA["chunks"]

# Map the 84 clauses to 37 rich vector-storytelling & hybrid archival-motion scenes
CHUNK_TO_SCENE = {
    1: 1,                  # S01: Animated Oct 1962 Calendar + Digital LED Date Box
    2: 2,                  # S02: Full-screen Ocean Dive of B-59 with spinning propeller & bubbles
    3: 3,                  # S03: Torpedo Room Cutaway: Mechanical arm loading T-5 Nuclear Torpedo
    4: 4,                  # S04: Steady Enola Gay Photo + Animated falling atomic bomb & 15 KT blast ring
    5: 5, 6: 5,            # S05: 3 Illustrated Vector Hands turning 3 Brass Nuclear Keys ("TRES PALABRAS")
    7: 6, 8: 6,            # S06: Full-screen Map: 4 Vector Submarines moving along Arctic -> Cuba route
    9: 7, 10: 7, 11: 7,    # S07: Steady B-59 Photo + Animated 78 Sailor Silhouettes Grid & Secret Warhead
    12: 8, 13: 8,          # S08: Lowering Red-White Blockade Barrier Gate + Slamming "BLOQUEO" Stamp
    14: 9,                 # S09: Steady JFK Photo + Animated Radar Quarantine Sweep around Cuba
    15: 10,                # S10: Top-Down Vector Carrier Deck (USS Randolph) + 11 Destroyers cutting wakes
    16: 11, 17: 11,        # S11: Surface Fleet sweeping green sonar cones downward while B-59 dives deeper
    18: 12, 19: 12,        # S12: Rotating Red Emergency Klaxon Lamp inside Submarine Cabin ("INFIERNO")
    20: 13, 21: 13,        # S13: Split-Screen Vector Diagram: Draining Battery (4%) vs Vanishing O2 / Rising CO2
    22: 14, 23: 14,        # S14: Spinning Analog Clock + Severed Radio Waves between Moscow Tower & B-59
    24: 15, 25: 15, 26: 15,# S15: Stopping A/C Fan Blades + Boiling +50°C Thermometer + Collapsing Sailors
    27: 16, 28: 16,        # S16: Steady USS Cony Photo + Animated Vector Depth Charges splashing & sinking
    29: 17, 30: 17,        # S17: Reconstructed US Navy Signaling Directive + Acoustic Wave Diagram
    31: 18, 32: 18, 33: 18,# S18: Giant Vector Hammer striking B-59 Hull + Shockwaves + Flickering Cabin Lights
    34: 19, 35: 19, 36: 19,# S19: Captain Savitsky at Periscope + Red Targeting Crosshair + Megaphone Waves
    37: 20, 38: 20, 39: 20,# S20: Open Logbook + Moving Vector Hand with Red Marker Underline + Stamp
    40: 21, 41: 21, 42: 21,# S21: 2 Vector Officers closing 2 Electrical Firing Switches in series
    43: 22, 44: 22,        # S22: Animated Brass Keys #1 & #2 rotating 90 deg into "ARMADO" (Red Circuit Live)
    45: 23, 46: 23,        # S23: Steady Crossroads Baker Photo + Top-Down Carrier engulfed by 15 KT Blast Ring
    47: 24, 48: 24,        # S24: Cold War Map with Animated Red ICBM Missile Arcs (US <-> Moscow) + DEFCON 1
    49: 25, 50: 25, 51: 25,# S25: 3 Officer Silhouettes & Dramatic Blue Spotlight Beam revealing The 3rd Man
    52: 26, 53: 26, 54: 26,# S26: Steady Vasili Arkhipov Portrait + Animated 3-Star Flotilla Shoulder Board
    55: 27, 56: 27,        # S27: Reconstructed Fleet Regulation + 3rd Blue Padlock dropping onto Firing Wire
    57: 28, 58: 28, 59: 28,# S28: Steady K-19 Photo + Spinning Radiation Trefoil & Geiger Counter Needle
    60: 29, 61: 29,        # S29: 8 Sailor Silhouettes + Glowing Red Nuclear Door held shut by Arkhipov's Hand
    62: 30,                # S30: Climax Veto: Giant Blue Shield & Barrier slamming down ("ASÍ QUE DIJO QUE NO")
    63: 31, 64: 31, 65: 31,# S31: Underwater Sonar Diagram: Lateral Signaling Waves vs Zero Top Hull Hits
    66: 32, 67: 32, 68: 32,# S32: Vector Torpedo T-5 retracting disarming & B-59 ascending toward sunlight
    69: 33,                # S33: Steady B-59 Surfaced Photo + Signal Lamp Pulses on the Caribbean Surface
    70: 34, 71: 34, 72: 34,# S34: Open Kremlin Dossier + Moving Vector Hand underlining Malinovsky's Reprimand
    73: 35, 74: 35,        # S35: Steady Arkhipov Photo + Spinning Year Counter (1962 -> 2002) & Declassified Stamp
    75: 36, 76: 36, 77: 36, 78: 36, 79: 36, # S36: Golden Balance Scale tipping with dropping weights (2 Votes vs 1)
    80: 37, 81: 37, 82: 37, 83: 37, 84: 37  # S37: Midway-style Final Dilemma over B-59 Photo + Stacked Action Buttons
}

for ch in CHUNKS:
    ch["scene_id"] = CHUNK_TO_SCENE.get(ch["index"], ch["scene_id"])

def load_font(paths, size):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

FONT_SUB_REG = load_font([
    "produccion/01_submarino_b59/assets/fonts/Inter-Regular.ttf",
    "C:/Windows/Fonts/segoeui.ttf"
], 46)
FONT_SUB_BOLD = load_font([
    "C:/Windows/Fonts/segoeuib.ttf",
    "produccion/01_submarino_b59/assets/fonts/Montserrat-Bold.ttf"
], 46)

FONT_HEADLINE = load_font([
    "C:/Windows/Fonts/segoeuib.ttf",
    "produccion/01_submarino_b59/assets/fonts/Montserrat-Bold.ttf"
], 58)
FONT_SUBHEAD = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 23)

FONT_RIBBON = load_font(["C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/consolab.ttf"], 25)
FONT_DOC_HDR = load_font(["C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/consolab.ttf"], 22)
FONT_DOC_META = load_font(["C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/consolab.ttf"], 24)
FONT_DOC_LINE = load_font(["C:/Windows/Fonts/cour.ttf", "C:/Windows/Fonts/consola.ttf"], 27)
FONT_DOC_BOLD = load_font(["C:/Windows/Fonts/courbd.ttf", "C:/Windows/Fonts/consolab.ttf"], 27)
FONT_STAMP = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 28)
FONT_FOOTER = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 15)
FONT_ATTR = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 17)

FONT_PILL_LG = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 32)
FONT_PILL_MD = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 25)
FONT_PILL_SM = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 20)
FONT_BIG_NUM = load_font(["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"], 76)

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
C_WHITE = (255, 255, 255)
C_BBOX_BLUE = (59, 130, 246)   # #3B82F6

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
    """Things that travel (gaze, sway, a head turning, a lid closing)."""
    return _cubic_bezier(p, 0.77, 0.0, 0.175, 1.0)

def EASE_OUT(p):
    """Things that open or arrive (a mouth, a lid reopening, a prop appearing)."""
    return _cubic_bezier(p, 0.23, 1.0, 0.32, 1.0)

def EASE_IN(p):
    """Only for things leaving or falling away."""
    return _cubic_bezier(p, 0.55, 0.0, 1.0, 0.45)

def track(t_ms, keys):
    """Discrete track [ms, value, 'out'?] from rossark-motion-skill."""
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
    """Monotone cubic Hermite spline for continuous acting poses without stopping at keys."""
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
    """Rossark blink recipe: close in 110 ms, hold 40 ms, reopen in 190 ms with 'out'."""
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

# Soft top/bottom gradient feather mask for Module A foreground image (Y=660..1420, height=760)
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

# PRE-COMPOSITE STEADY ARCHIVAL STAGES ONCE AT STARTUP -> ZERO IMAGE JITTER/TREMOR!
ASSETS_DIR = "produccion/01_submarino_b59/assets"
PHOTOS_STEADY_STAGE = {}
PHOTOS_BACKDROP = {}

for key, fname, fy_val in [
    ("b59", "b59_surface.jpg", 0.50),
    ("arkhipov", "arkhipov.jpg", 0.35),
    ("randolph", "uss_randolph.jpg", 0.50),
    ("kennedy", "kennedy_1962.jpg", 0.35),
    ("k19", "k19_sub.jpg", 0.50),
    ("foxtrot", "foxtrot_sub.jpg", 0.50),
    ("enola", "b29_enola.jpg", 0.48),
    ("cony", "uss_cony.jpg", 0.50),
    ("malinovsky", "malinovsky.jpg", 0.35),
    ("baker", "crossroads_baker.jpg", 0.65),
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
        PHOTOS_BACKDROP[key] = backdrop
        
        steady = backdrop.copy()
        fg = fit_photo_once(im, W, 760, fy=fy_val)
        steady.paste(fg, (0, 660), STAGE_FEATHER_MASK)
        PHOTOS_STEADY_STAGE[key] = steady

SCENE_META = {
    0:  ("27 DE OCTUBRE DE 1962", "MAR DE LOS SARGAZOS · LÍNEA DE CUARENTENA", "neutral"),
    1:  ("27 DE OCTUBRE DE 1962", "SÁBADO NEGRO · CRISIS DE LOS MISILES", "neutral"),
    2:  ("90 METROS BAJO EL MAR", "INMERSIÓN EN EL MAR CARIBE", "tactical"),
    3:  ("TORPEDO NUCLEAR T-5", "ORDEN DE ARMADO EN EL TUBO DE PROA N.º 1", "danger"),
    4:  ("POTENCIA DE HIROSHIMA", "15 KILOTONES DE DESTRUCCIÓN", "amber"),
    5:  ("SOLO TRES PALABRAS", "PROTOCOLO DE DISPARO EN EL PUENTE", "amber"),
    6:  ("OPERACIÓN KAMA · 1962", "4 SUBMARINOS DESDE EL ÁRTICO HACIA CUBA", "neutral"),
    7:  ("SUBMARINO SOVIÉTICO B-59", "78 TRIPULANTES Y UN ARMA SECRETA", "amber"),
    8:  ("EL MUNDO YA CAMBIÓ", "BLOQUEO MILITAR ALREDEDOR DE LA ISLA", "danger"),
    9:  ("CUARENTENA NAVAL", "ORDEN EJECUTIVA DE JOHN F. KENNEDY", "danger"),
    10: ("USS RANDOLPH + 11 DESTRUCTORES", "GRUPO DE CAZA ANTISUBMARINA DE EE. UU.", "danger"),
    11: ("INMERSIÓN DE EMERGENCIA", "OCULTO BAJO LA FLOTA ESTADOUNIDENSE", "tactical"),
    12: ("EMPIEZA EL INFIERNO", "AISLAMIENTO TOTAL A 90 METROS", "danger"),
    13: ("SUBMARINO DIÉSEL", "SIN RECARGA DE BATERÍAS NI OXÍGENO", "danger"),
    14: ("SIN CONTACTO CON MOSCÚ", "DÍAS DE SILENCIO RADIAL · ¿TERCERA GUERRA MUNDIAL?", "amber"),
    15: ("MÁS DE 50 °C DE CALOR", "AIRE ACONDICIONADO APAGADO · DESMAYOS EN GUARDIA", "danger"),
    16: ("CARGAS DE PROFUNDIDAD", "DESTRUCTOR USS CONY (DD-508) EN LA SUPERFICIE", "amber"),
    17: ("SEÑALES DE PRÁCTICA (PDC)", "GRANADAS ACÚSTICAS PARA OBLIGARLO A SUBIR", "amber"),
    18: ("MARTILLAZOS EN EL CASCO", "ONDAS DE CHOQUE Y LUCES PARPADEANDO", "danger"),
    19: ("CAPITÁN VALENTÍN SAVITSKY", "DÍAS SIN DORMIR · CREE QUE LA GUERRA ESTALLÓ", "danger"),
    20: ("«¡LOS HUNDIREMOS A TODOS!»", "DIARIO DEL OFICIAL VADIM ORLOV EN EL B-59", "danger"),
    21: ("PROTOCOLO NUCLEAR HABITUAL", "EN CUALQUIER SUBMARINO BASTABAN 2 FIRMAS", "amber"),
    22: ("LAS DOS LLAVES ESTÁN LISTAS", "SAVITSKY Y MASLÉNNIKOV AUTORIZAN EL FUEGO", "danger"),
    23: ("IMPACTO DE 15 KILOTONES", "EL PORTAAVIONES DESAPARECE EN SEGUNDOS", "danger"),
    24: ("REPRESALIA CONTRA MOSCÚ", "ESCALADA NUCLEAR INMEDIATA (DEFCON 1)", "danger"),
    25: ("HABÍA UN TERCER HOMBRE", "UNA ANOMALÍA EN LA CADENA DE MANDO", "tactical"),
    26: ("VASILI ARKHIPOV (36 AÑOS)", "JEFE DE ESTADO MAYOR DE TODA LA FLOTILLA", "tactical"),
    27: ("REGLA DE UNANIMIDAD: 3 VOTOS", "POR ESTAR ÉL A BORDO DEL B-59", "amber"),
    28: ("LA CICATRIZ DEL SUBMARINO K-19", "FUGA RADIACTIVA UN AÑO ANTES (1961)", "amber"),
    29: ("EL PRECIO DE LA RADIACIÓN", "VIO MORIR A SUS PROPIOS MARINEROS", "danger"),
    30: ("ASÍ QUE DIJO QUE NO", "VETO HISTÓRICO EN EL PUENTE DE MANDO", "tactical"),
    31: ("EL DETALLE ACÚSTICO CLAVE", "EXPLOSIONES A LOS COSTADOS, NO ENCIMA", "tactical"),
    32: ("SEÑALES PARA EMERGER", "ARKHIPOV CONVENCE AL CAPITÁN DE DESARMARLO", "tactical"),
    33: ("EMERSIÓN EN EL CARIBE", "EL B-59 SALE A LA SUPERFICIE ANTE EE. UU.", "tactical"),
    34: ("REGAÑO EN EL KREMLIN", "ACTA DEL MINISTERIO DE DEFENSA DE LA URSS", "danger"),
    35: ("OCULTO DURANTE 40 AÑOS", "ARCHIVOS DESCLASIFICADOS EN EL AÑO 2002", "neutral"),
    36: ("2 VOTOS CONTRA 1 BAJO EL MAR", "DOS VOTARON POR EL FIN DEL MUNDO · UNO PIDIÓ ESPERAR", "amber"),
    37: ("¿QUÉ HABRÍAS HECHO VOS?", "GIRAR LA LLAVE vs. SALIR A LA SUPERFICIE", "amber"),
}

VARIANT_COLORS = {
    "neutral": C_NEUTRAL,
    "amber": C_AMBER,
    "danger": C_DANGER,
    "tactical": C_TACTICAL,
}

# Reusable Vector Storytelling Primitives (SVG-style 2D Motion Graphics)
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
    # Like the [ 10:22 ] red-bordered digital box in @cdmauro2010's Midway Short (lYVMDblBX3Y)
    tw = int(FONT_BIG_NUM.getlength(text))
    pw, ph = tw + 64, 108
    x0, y0 = cx - pw // 2, cy - ph // 2
    draw.rectangle([x0, y0, x0 + pw, y0 + ph], fill=(18, 16, 18), outline=col, width=4)
    draw.text((cx, cy - 2), text, font=FONT_BIG_NUM, fill=col, anchor="mm")

def draw_vector_submarine(draw, cx, cy, scale=1.0, body_col=(42, 54, 72), stroke_col=C_TACTICAL, prop_angle=0.0, facing="right"):
    direction = 1 if facing == "right" else -1
    w_half = int(240 * scale)
    h_half = int(36 * scale)
    # Conning tower / sail + periscope
    tx0 = cx - int(40 * scale * direction)
    tx1 = cx + int(35 * scale * direction)
    if tx0 > tx1: tx0, tx1 = tx1, tx0
    draw.line([(cx, cy - h_half - int(72*scale)), (cx, cy - h_half - int(36*scale))], fill=stroke_col, width=max(2, int(4*scale)))
    draw.line([(cx, cy - h_half - int(72*scale)), (cx + int(18*scale*direction), cy - h_half - int(72*scale))], fill=stroke_col, width=max(2, int(4*scale)))
    draw.rounded_rectangle([tx0, cy - h_half - int(42*scale), tx1, cy - h_half + 6], radius=int(8*scale), fill=body_col, outline=stroke_col, width=max(2, int(3*scale)))
    # Hull
    draw.rounded_rectangle([cx - w_half, cy - h_half, cx + w_half, cy + h_half], radius=h_half, fill=body_col, outline=stroke_col, width=max(2, int(3*scale)))
    # Spinning propeller at stern
    stern_x = cx - w_half * direction
    blade_h = int(26 * scale * math.sin(prop_angle))
    draw.ellipse([stern_x - int(8*scale), cy - abs(blade_h) - 4, stern_x + int(8*scale), cy + abs(blade_h) + 4], fill=C_AMBER, outline=C_WHITE, width=1)

def draw_vector_hand(draw, hx, hy, angle_deg=-25, sleeve_col=(135, 34, 42)):
    # Illustrated geometric hand + uniform sleeve (like @cdmauro2010's Marcus Aurelius / Commodus hands!)
    hand_img = Image.new("RGBA", (260, 320), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hand_img)
    skin = (218, 178, 146, 255)
    skin_dark = (188, 146, 114, 255)
    # 4 Fingers + Thumb
    for fi, (fx, fy, fw, fh) in enumerate([
        (78, 35, 22, 75), (104, 24, 22, 85), (130, 28, 22, 80), (156, 42, 20, 68)
    ]):
        hd.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=10, fill=skin, outline=skin_dark, width=2)
    # Thumb
    hd.polygon([(50, 95), (78, 82), (90, 125), (58, 132)], fill=skin, outline=skin_dark)
    # Palm
    hd.rounded_rectangle([72, 88, 178, 178], radius=22, fill=skin, outline=skin_dark, width=2)
    # Uniform Sleeve + Gold Naval Cuff Stripe
    hd.polygon([(62, 172), (188, 172), (210, 315), (40, 315)], fill=sleeve_col + (255,))
    hd.line([(60, 196), (190, 196)], fill=C_AMBER + (255,), width=8)
    rot = hand_img.rotate(angle_deg, resample=Image.Resampling.BICUBIC, expand=True)
    return rot, hx - rot.width // 2, hy - rot.height // 3

def draw_radiation_symbol(draw, cx, cy, radius, angle_deg=0.0, col=C_AMBER):
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=(24, 20, 16), outline=col, width=3)
    for b in range(3):
        start_a = angle_deg + b * 120
        draw.pieslice([cx - radius + 10, cy - radius + 10, cx + radius - 10, cy + radius - 10], start=start_a, end=start_a + 60, fill=col)
    draw.ellipse([cx - int(radius*0.28), cy - int(radius*0.28), cx + int(radius*0.28), cy + int(radius*0.28)], fill=(24, 20, 16), outline=col, width=3)

def draw_crosshair(draw, cx, cy, rad, col=C_DANGER):
    # Like @cdmauro2010's Berlin Airlift red targeting crosshair!
    draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=col, width=4)
    draw.ellipse([cx - int(rad*0.6), cy - int(rad*0.6), cx + int(rad*0.6), cy + int(rad*0.6)], outline=col, width=2)
    draw.line([(cx - rad - 35, cy), (cx + rad + 35, cy)], fill=col, width=4)
    draw.line([(cx, cy - rad - 35), (cx, cy + rad + 35)], fill=col, width=4)

def draw_barrier_gate(draw, y_bar, angle_deg=0.0):
    # Like @cdmauro2010's Berlin Airlift red-and-white striped blockade barrier gate!
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

# ==============================================================================
# ROSSARK-MOTION-SKILL RECIPES: Living Water, Steam Wisps, Jiggle Buttons,
# and 2.5D Living Naval Officers (ChefScene / RevealScene / LiveFace architecture)
# ==============================================================================
def draw_rossark_water_surface(draw, y_surf, global_t, col=C_TACTICAL, n_ripples=3):
    """Rossark water recipe: surface waves whose points follow wave(t, period, phase=k*i) + bell(p) ripples."""
    t_ms = global_t * 1000.0
    pts = []
    for i, x in enumerate(range(0, W + 30, 30)):
        wy = y_surf + 6.5 * wave(t_ms, 2600.0, phase=i * 0.09) + 2.5 * wave(t_ms, 1400.0, phase=i * 0.17)
        pts.append((x, int(wy)))
    draw.line(pts, fill=col, width=4)
    # Secondary deeper parallax wave
    pts2 = [(x, int(y + 16 + 3.0 * wave(t_ms, 3400.0, phase=i * 0.07 + 0.3))) for i, (x, y) in enumerate(pts)]
    draw.line(pts2, fill=(45, 95, 165), width=2)
    # Ripples that grow 0 -> 1 and fade with bell(p)
    for r_i in range(n_ripples):
        p = loop_p(t_ms, 2800.0, phase=seeded(r_i, 11))
        b = bell(p)
        if b > 0.15:
            rx = int(220 + seeded(r_i, 22) * (W - 440))
            rw = int(28 + 95 * p)
            rh = max(4, int(rw * 0.22))
            draw.ellipse([rx - rw, y_surf - rh + 4, rx + rw, y_surf + rh + 4], outline=col, width=max(1, int(3 * b)))

def draw_rossark_steam_wisps(frame, cx, base_y, global_t, count=4, col=(235, 240, 248)):
    """Rossark smoke/steam recipe: wisps rise 8-14 units while bell(p) fades them in and out on seeded phases."""
    t_ms = global_t * 1000.0
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(count):
        p = loop_p(t_ms, 2400.0 + seeded(i, 1) * 700.0, phase=seeded(i, 2))
        alpha = int(175 * bell(p))
        if alpha <= 8:
            continue
        wx = cx + int((seeded(i, 3) - 0.5) * 140 + 14.0 * wave(t_ms, 1900.0, seeded(i, 4)))
        wy = base_y - int(p * 135)
        r = int(14 + p * 22)
        od.ellipse([wx - r, wy - int(r * 0.7), wx + r, wy + int(r * 0.7)], fill=col + (alpha,))
    frame.paste(overlay, (0, 0), overlay)

def draw_rossark_jiggle_button(draw, cx, cy, bw, bh, text, fill_col, outline_col, global_t, phase_offset=0.0):
    """Rossark 'Something waiting to be tapped' recipe: 2% squash-and-widen pulse on ~270ms beat with alternating side bulge."""
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

def draw_rossark_officer(
    frame, cx, cy, scale=1.35, role="arkhipov", global_t=0.0, scene_t=0.0,
    talking=False, mood="focused", gesture="rest"
):
    """
    2.5D Living Naval Officer built with the exact rossark-motion-skill architecture
    (ChefScene.swift / RevealScene.swift + liveFace.tsx):
      - 100-wide tombstone head with 2.5D yaw (ears -9*yaw, eyes/mouth +10*yaw, nose +13*yaw)
      - LiveEye with sliding pupil, shine dot, 110ms/40ms/190ms 'out' blink, and expressive brows
      - LiveMouth with syllable articulation
      - Body breathing (sy, sx = 1/sy^0.6), waist lean, and 110ms delayed head counter-motion
      - Two-segment articulated arms (upper + fore sharing a round elbow) with 90ms forearm follow-through
    """
    t_ms = (global_t * 1000.0) % 7200.0
    s_ms = scene_t * 1000.0
    canvas_sz = 460
    rig = Image.new("RGBA", (canvas_sz, canvas_sz), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rig)
    ox, oy = canvas_sz // 2, 210  # head anchor in rig space

    # Role palette & uniform colors
    if role == "savitsky":
        suit_col = (44, 20, 24, 255)
        suit_shade = (68, 28, 32, 255)
        cap_top = (36, 18, 22, 255)
        badge_col = C_AMBER + (255,)
        phase_seed = 0.0
    elif role == "maslennikov":
        suit_col = (38, 26, 32, 255)
        suit_shade = (58, 36, 44, 255)
        cap_top = (42, 24, 28, 255)
        badge_col = C_DANGER + (255,)
        phase_seed = 0.33
    elif role == "sailor":
        suit_col = (22, 34, 54, 255)
        suit_shade = (34, 52, 82, 255)
        cap_top = (18, 28, 46, 255)
        badge_col = C_AMBER + (255,)
        phase_seed = 0.66
    else:  # arkhipov
        suit_col = (18, 38, 68, 255)
        suit_shade = (28, 58, 102, 255)
        cap_top = (238, 242, 248, 255)  # Flotilla Chief white-topped naval cap
        badge_col = C_AMBER + (255,)
        phase_seed = 0.18

    skin_col = (242, 185, 148, 255)
    feature_col = (210, 126, 88, 255)
    hair_col = (72, 48, 34, 255)

    # Acting tracks via flow() + idle waves + follow-through
    lean_keys = [(0, 0.0), (1800, -2.5), (3600, 2.0), (5400, -1.5), (7200, 0.0)]
    yaw_keys = [(0, -0.15), (2100, 0.22), (4200, 0.18), (5800, -0.18), (7200, -0.15)]
    head_keys = [(0, 0.0), (2000, 3.5), (4100, -3.0), (5900, 2.0), (7200, 0.0)]

    lean = flow(t_ms, lean_keys) + 1.4 * wave(t_ms, 4200.0, phase_seed)
    yaw = flow(t_ms, yaw_keys) + 0.06 * wave(t_ms, 3100.0, phase_seed + 0.2)
    # Rossark Rule 5.4 Counter-motion: head(t) = own(t) - 0.45 * lean(t - 110ms)
    head_tilt = flow(t_ms, head_keys) - 0.45 * flow(max(0.0, t_ms - 110.0), lean_keys) + 1.8 * wave(t_ms, 4600.0, phase_seed + 0.5)

    # Breathing & volume-preserving squash/stretch: sx = 1 / sy^0.6
    sy = 1.0 + 0.016 * wave(t_ms, 2600.0, phase_seed)
    sx = 1.0 / (sy ** 0.6)
    lift = 2.5 * wave(t_ms, 2600.0, phase_seed + 0.25)

    # Articulated arms (Rule 5.5 & 5.10: never symmetric, forearm trails upper arm by 90ms)
    if gesture == "turn_key":
        arm_ra_keys = [(0, 25.0), (450, 62.0), (1400, 68.0), (7200, 65.0)]
        arm_re_keys = [(0, 15.0), (450, 75.0), (1400, 88.0), (7200, 84.0)]
    elif gesture == "stop_hand":
        arm_ra_keys = [(0, 20.0), (400, 58.0), (1200, 62.0), (7200, 60.0)]
        arm_re_keys = [(0, 10.0), (400, 108.0), (1200, 112.0), (7200, 110.0)]
    elif gesture == "fist_rage":
        arm_ra_keys = [(0, 45.0), (500, 72.0), (1000, 52.0), (1500, 75.0), (7200, 55.0)]
        arm_re_keys = [(0, 45.0), (500, 85.0), (1000, 55.0), (1500, 88.0), (7200, 60.0)]
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
        # Gold naval cuff stripe
        dx_f, dy_f = ha_x - el_x, ha_y - el_y
        l_f = max(1.0, math.hypot(dx_f, dy_f))
        cx1, cy1 = ha_x - int(dx_f / l_f * 12), ha_y - int(dy_f / l_f * 12)
        rd.ellipse([cx1 - 11, cy1 - 11, cx1 + 11, cy1 + 11], fill=C_AMBER + (255,))
        rd.ellipse([ha_x - 14, ha_y - 14, ha_x + 14, ha_y + 14], fill=skin_col, outline=feature_col, width=2)

    # Back arm first
    draw_arm(-1, la_base, le_base)

    # Torso (Naval jacket with double-breasted gold buttons & collar that slide with 2.5D yaw)
    t_top = by + int(48 * sy)
    t_bot = by + int(138 * sy)
    sh_w = int(52 * sx)
    wa_w = int(44 * sx)
    rd.polygon([
        (bx - sh_w, t_top), (bx + sh_w, t_top),
        (bx + wa_w, t_bot), (bx - wa_w, t_bot)
    ], fill=suit_col, outline=suit_shade)
    # Collar V-neck + tie
    yaw_px = int(8 * yaw)
    rd.polygon([(bx - 16 + yaw_px, t_top), (bx + 16 + yaw_px, t_top), (bx + yaw_px, t_top + 26)], fill=C_WHITE + (255,))
    # Double-breasted gold buttons sliding with 2.5D yaw
    for b_row in [t_top + 34, t_top + 56, t_top + 78]:
        for b_col in [-16, 16]:
            rd.ellipse([bx + b_col + yaw_px - 4, b_row - 4, bx + b_col + yaw_px + 4, b_row + 4], fill=C_AMBER + (255,))
    # Shoulder boards (epaulettes)
    rd.rounded_rectangle([bx - sh_w - 4, t_top - 6, bx - sh_w + 22, t_top + 8], radius=4, fill=C_AMBER + (255,))
    rd.rounded_rectangle([bx + sh_w - 22, t_top - 6, bx + sh_w + 4, t_top + 8], radius=4, fill=C_AMBER + (255,))

    # Head layer (rotates around neck pivot with counter-motion follow-through)
    head_layer = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_layer)
    hcx, hcy = 120, 130

    # Ears slide the opposite way (-9 * yaw) per Rossark Rule 5.6
    ear_dx = int(-9 * yaw)
    for side in [-1, 1]:
        ex = hcx + side * 50 + ear_dx
        hd.ellipse([ex - 11, hcy - 10, ex + 11, hcy + 12], fill=skin_col, outline=feature_col, width=2)

    # 100-wide Tombstone Head
    hd.rounded_rectangle([hcx - 50, hcy - 64, hcx + 50, hcy + 52], radius=28, fill=skin_col, outline=feature_col, width=2)

    # LiveEyes (Rossark Section 4: plain white pills, sliding pupil + shine, 110ms/40ms/190ms blink)
    blinks = make_blink_keys(7200.0, [1400.0, 4100.0, 6200.0])
    lid_val = track(t_ms, blinks)
    if mood == "tired":
        lid_val = max(0.35, lid_val)
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
        # Pupil + specular shine dot
        px = ecx + look_x
        py = ecy + look_y
        hd.rounded_rectangle([px - 6, py - 8, px + 6, py + 8], radius=5, fill=(38, 38, 42, 255))
        hd.ellipse([px - 4, py - 6, px - 1, py - 3], fill=C_WHITE + (255,))
        # Eyelid (clipped 2 units larger than eye white so no anti-aliased glasses ring leaks)
        if lid_val > 0.02:
            lid_h = int((eh + 4) * lid_val)
            hd.rounded_rectangle([ecx - ew // 2 - 2, ecy - eh // 2 - 2, ecx + ew // 2 + 2, ecy - eh // 2 - 2 + lid_h], radius=8, fill=skin_col)
            hd.line([(ecx - ew // 2 - 1, ecy - eh // 2 - 2 + lid_h), (ecx + ew // 2 + 1, ecy - eh // 2 - 2 + lid_h)], fill=feature_col, width=3)
        # Eyebrows
        brow_y = ecy - eh // 2 - 6
        if mood == "rage":
            hd.line([(ecx - 12, brow_y - side * 4), (ecx + 12, brow_y + side * 5)], fill=hair_col, width=5)
        elif mood == "tired":
            hd.line([(ecx - 12, brow_y + side * 3), (ecx + 12, brow_y - side * 2)], fill=hair_col, width=4)
        else:
            hd.line([(ecx - 12, brow_y), (ecx + 12, brow_y - 2)], fill=hair_col, width=5)

    # Nose (sticks out the most -> slides 13 * yaw per Rossark Rule 5.6)
    nx = hcx + int(13 * yaw)
    hd.rounded_rectangle([nx - 5, hcy - 4, nx + 5, hcy + 14], radius=4, fill=feature_col)

    # LiveMouth (opens and closes in ~180ms syllables when talking, calm smile/line otherwise)
    mx = hcx + face_dx
    my = hcy + 26
    if talking:
        m_depth = int(6 + 10 * abs(wave(t_ms, 340.0, phase_seed)))
        hd.polygon([(mx - 14, my), (mx + 14, my), (mx + 10, my + m_depth), (mx - 10, my + m_depth)], fill=(155, 42, 42, 255))
        hd.line([(mx - 11, my + 2), (mx + 11, my + 2)], fill=C_WHITE + (255,), width=3)
    else:
        hd.arc([mx - 12, my - 4, mx + 12, my + 8], start=15 if mood != "rage" else 195, end=165 if mood != "rage" else 345, fill=feature_col, width=4)

    # Naval Officer Peaked Cap (one clean silhouette above brow)
    hd.polygon([
        (hcx - 58, hcy - 46), (hcx + 58, hcy - 46),
        (hcx + 68, hcy - 76), (hcx, hcy - 88), (hcx - 68, hcy - 76)
    ], fill=cap_top, outline=suit_col)
    hd.rectangle([hcx - 52, hcy - 52, hcx + 52, hcy - 38], fill=(20, 22, 26, 255), outline=C_AMBER + (255,), width=2)
    hd.ellipse([hcx + int(6 * yaw) - 9, hcy - 68, hcx + int(6 * yaw) + 9, hcy - 50], fill=badge_col, outline=C_WHITE + (255,), width=2)

    head_rot = head_layer.rotate(-head_tilt, resample=Image.Resampling.BICUBIC, expand=False)
    rig.paste(head_rot, (bx - hcx, by - hcy), head_rot)

    # Front arm (drawn in front of torso)
    draw_arm(1, ra_base, re_base)

    if scale != 1.0:
        new_sz = max(40, int(canvas_sz * scale))
        rig = rig.resize((new_sz, new_sz), Image.Resampling.LANCZOS)
    frame.paste(rig, (cx - rig.width // 2, cy - rig.height // 2), rig)


# Module A: Rock-Steady Archival Photo + Dynamic Vector Motion Overlays (0.0px image jitter!)
def render_module_a_steady(photo_key, scene_t, scene_dur, date_ribbon, caption_pill, attribution, extra_vector_fn=None):
    frame = PHOTOS_STEADY_STAGE.get(photo_key, CANVAS_ABYSS).copy()
    draw = ImageDraw.Draw(frame)
    
    if extra_vector_fn:
        extra_vector_fn(frame, draw, scene_t, scene_dur)
        
    # Typewriter Context Tape (dateRibbon at X=48, Y=690)
    if date_ribbon:
        n_chars = int(min(len(date_ribbon), max(1, (scene_t / 0.80) * len(date_ribbon))))
        typed_str = date_ribbon[:n_chars]
        tw = int(FONT_RIBBON.getlength(typed_str))
        draw.rectangle([54, 696, 54 + tw + 36, 744], fill=(0, 0, 0))
        draw.rectangle([48, 690, 48 + tw + 36, 738], fill=C_PAPER)
        draw.rectangle([48, 690, 54, 738], fill=C_STAMP_RED)
        draw.text((66, 714), typed_str, font=FONT_RIBBON, fill=C_INK, anchor="lm")
        
    # Context Subject Pill at Y=1345
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
    
    # Animated Red Rubber Stamp slamming down
    if stamp_text and scene_t >= 0.65:
        sp = spring_val(scene_t, delay_sec=0.65, stiffness=220, damping=12)
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
    
    # Draw animated vector hand gliding across the document as it underlines!
    draw = ImageDraw.Draw(frame)
    hand_rot, hx, hy = draw_vector_hand(draw, doc_x + pen_tip_x + 30, doc_y + pen_tip_y + 70, angle_deg=-22)
    frame.paste(hand_rot, (hx, hy), hand_rot)
    
    draw_attribution_pill(draw, source_attr)
    return frame

def draw_caribbean_geography(draw):
    fl = [(210, 660), (295, 660), (335, 815), (315, 855), (275, 845), (245, 755)]
    cuba = [(185, 965), (265, 935), (390, 945), (535, 985), (675, 1035), (755, 1075), (685, 1095), (555, 1075), (435, 1015), (290, 995)]
    hisp = [(795, 1075), (925, 1065), (985, 1115), (895, 1145), (785, 1125)]
    yuc = [(0, 1040), (115, 1025), (145, 1120), (95, 1280), (0, 1280)]
    for poly in [fl, cuba, hisp, yuc]:
        draw.polygon(poly, fill=C_LAND_FILL, outline=C_LAND_STROKE, width=2)

def draw_balance_scale(draw, cx, base_y, tilt_deg, left_pills, right_pills, left_title, right_title, left_col=C_DANGER, right_col=C_TACTICAL, drop_prog=1.0):
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

# Master Stage Dispatcher (37 Vector-Backed Storytelling Scenes)
def render_stage_for_scene(scene_id, scene_t, scene_dur, global_t):
    s_prog = min(1.0, max(0.0, scene_t / max(0.1, scene_dur)))
    
    if scene_id in (0, 1):
        # S01: Animated October 1962 Calendar + Midway-style Digital LED Date Box
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        cx0, cy0, cw, ch = 150, 680, W - 300, 610
        draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=14, fill=C_PAPER, outline=(185, 176, 160), width=4)
        draw.text((W // 2, cy0 + 52), "OCTUBRE 1962", font=FONT_PILL_LG, fill=C_INK, anchor="mm")
        draw.line([(cx0 + 36, cy0 + 92), (cx0 + cw - 36, cy0 + 92)], fill=(195, 186, 170), width=3)
        days_crossed = int(min(26, global_t * 14))
        for d in range(1, 32):
            idx = d - 1
            dx = cx0 + 72 + (idx % 7) * 105
            dy = cy0 + 150 + (idx // 7) * 92
            if d == 27:
                rad = 38 + int(4 * math.sin(global_t * 9))
                draw.ellipse([dx - rad, dy - rad, dx + rad, dy + rad], fill=(252, 232, 160), outline=C_STAMP_RED, width=5)
                draw.text((dx, dy), "27", font=FONT_PILL_MD, fill=C_INK, anchor="mm")
            else:
                draw.text((dx, dy), str(d), font=FONT_PILL_MD, fill=(55, 52, 48), anchor="mm")
                if d <= days_crossed:
                    draw.line([(dx - 24, dy - 24), (dx + 24, dy + 24)], fill=C_STAMP_RED, width=4)
        draw_digital_led_box(draw, W // 2, 1365, "27 · 10 · 1962", C_DANGER)
        return frame

    elif scene_id == 2:
        # S02: Rossark Travelling Water Surface + Submarine Diving to -90m with Seeded Bubbles
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_rossark_water_surface(draw, 705, global_t, col=C_TACTICAL, n_ripples=3)
        for dm, dy in [("-30 m", 860), ("-60 m", 1040), ("-90 m", 1220)]:
            draw.line([(60, dy), (140, dy)], fill=C_TACTICAL if dm=="-90 m" else (110, 130, 155), width=3)
            draw.text((160, dy), dm, font=FONT_PILL_MD, fill=C_AMBER if dm=="-90 m" else C_NEUTRAL, anchor="lm")
        sub_y = int(800 + 420 * EASE_IN_OUT(min(1.0, s_prog * 1.15)) + 3.0 * wave(global_t * 1000.0, 2600.0))
        sx = W // 2 + 50
        for bi in range(11):
            p_b = loop_p(global_t * 1000.0, 1800.0 + seeded(bi, 1) * 600.0, phase=seeded(bi, 2))
            bx = sx - 190 + int(seeded(bi, 3) * 380 + 8.0 * wave(global_t * 1000.0, 1600.0, seeded(bi, 4)))
            by = sub_y - 45 - int(p_b * 230)
            r_b = int(4 + seeded(bi, 5) * 5)
            draw.ellipse([bx - r_b, by - r_b, bx + r_b, by + r_b], outline=C_TACTICAL, width=2)
        draw_vector_submarine(draw, sx, sub_y, scale=1.05, prop_angle=global_t * 18)
        draw.text((sx, sub_y), "SUBMARINO B-59", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        return frame

    elif scene_id == 3:
        # S03: Torpedo Room Cutaway + Mechanical Loading of T-5 Nuclear Torpedo + Spinning Radiation Symbol
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        ty = 980
        slide = int((1.0 - EASE_OUT(min(1.0, scene_t / 0.85))) * -210)
        draw.line([(90, ty - 110), (W - 90, ty - 110)], fill=(90, 100, 118), width=6)
        draw.line([(90, ty + 110), (W - 90, ty + 110)], fill=(90, 100, 118), width=6)
        draw.rounded_rectangle([140 + slide, ty - 78, 950 + slide, ty + 78], radius=72, fill=(36, 44, 56), outline=C_NEUTRAL, width=4)
        draw.rounded_rectangle([140 + slide, ty - 78, 430 + slide, ty + 78], radius=72, fill=C_DANGER, outline=C_WHITE, width=4)
        draw_radiation_symbol(draw, 250 + slide, ty, 44, angle_deg=global_t * 90, col=C_AMBER)
        draw.text((355 + slide, ty), "15 KT", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        draw.text((685 + slide, ty), "TORPEDO NUCLEAR T-5", font=FONT_PILL_MD, fill=C_NEUTRAL, anchor="mm")
        draw_map_pill(draw, W // 2, 1255, "ORDEN DEL CAPITÁN: ARMAR EL TORPEDO EN PROA", C_DANGER)
        return frame

    elif scene_id == 4:
        # S04: Steady B-29 Enola Gay Photo + Animated Falling Vector Bomb & Expanding 15 KT Blast Ring
        def _vec4(frame, draw, st, sd):
            by = int(730 + EASE_IN(min(1.0, st / 1.05)) * 340)
            bx = 790
            draw.rounded_rectangle([bx - 22, by - 55, bx + 22, by + 35], radius=20, fill=(40, 44, 52), outline=C_AMBER, width=3)
            draw.polygon([(bx - 28, by - 75), (bx + 28, by - 75), (bx + 16, by - 50), (bx - 16, by - 50)], fill=C_DANGER, outline=C_WHITE)
            if st > 0.7:
                for r in range(1, 4):
                    rad = int(((st - 0.7) * 140 + r * 55) % 220)
                    draw.ellipse([bx - rad, 1080 - rad, bx + rad, 1080 + rad], outline=C_AMBER if r%2==0 else C_DANGER, width=4)
            draw_digital_led_box(draw, 310, 1180, "15 KT", C_AMBER)
        return render_module_a_steady(
            "enola", scene_t, scene_dur,
            "HIROSHIMA · 6 AGO 1945",
            "El torpedo del B-59 tenía la misma potencia que Hiroshima",
            "FOTO DE ARCHIVO · USAAF (B-29 ENOLA GAY), 1945 · DOMINIO PÚBLICO",
            extra_vector_fn=_vec4
        )

    elif scene_id == 5:
        # S05: 3 Living 2.5D Rossark Naval Officers + 3 Launch Key Cards ("SOLO TRES PALABRAS")
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        officers_spec = [
            ("1. CAPITÁN", "«SÍ»", "savitsky", "rage", "turn_key"),
            ("2. POLÍTICO", "«SÍ»", "maslennikov", "focused", "turn_key"),
            ("3. FLOTILLA", "«SÍ»", "arkhipov", "focused", "stop_hand"),
        ]
        for i, (role_lbl, word, r_type, mood, gest) in enumerate(officers_spec):
            kx = 88 + i * 312
            ky = 960
            active = scene_t >= i * 0.28
            col = C_DANGER if i < 2 else C_TACTICAL
            # Draw living 2.5D officer above their station card
            draw_rossark_officer(frame, kx + 140, 795, scale=0.82, role=r_type, global_t=global_t, scene_t=scene_t, talking=active, mood=mood, gesture=gest)
            draw = ImageDraw.Draw(frame)
            draw.rounded_rectangle([kx, ky, kx + 280, ky + 320], radius=20, fill=(38, 18, 20) if i < 2 else (18, 34, 62), outline=col if active else (70, 75, 85), width=4)
            draw.text((kx + 140, ky + 55), role_lbl, font=FONT_PILL_SM, fill=C_NEUTRAL, anchor="mm")
            draw.text((kx + 140, ky + 145), word, font=FONT_BIG_NUM, fill=C_WHITE if active else (90, 95, 105), anchor="mm")
            draw.ellipse([kx + 114, ky + 225, kx + 166, ky + 277], fill=C_AMBER, outline=C_WHITE, width=3)
            if active:
                h_rot, hx, hy = draw_vector_hand(draw, kx + 140, ky + 400, angle_deg=-8 + int(10 * wave(global_t * 1000.0, 1200.0, i * 0.25)))
                frame.paste(h_rot, (hx, hy), h_rot)
        return frame

    elif scene_id == 6:
        # S06: Tactical Map: 4 Vector Submarines moving along Arctic -> Cuba trajectory
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_caribbean_geography(draw)
        draw.polygon([(780, 660), (1080, 660), (1080, 790), (830, 760)], fill=C_LAND_FILL, outline=C_LAND_STROKE, width=2)
        draw_map_pill(draw, 850, 705, "ÁRTICO SOVIÉTICO (KOLA)", C_DANGER)
        draw_map_pill(draw, 480, 1060, "CUBA", C_AMBER)
        # Moving submarine icons along the curve
        for i, sname in enumerate(["B-4", "B-36", "B-59 (NUCLEAR)", "B-130"]):
            t_sub = min(1.0, max(0.0, s_prog * 1.2 - i * 0.14))
            sx = int(840 - 340 * t_sub)
            sy = int(745 + 265 * t_sub)
            draw.line([(840, 745), (sx, sy)], fill=C_AMBER, width=5)
            draw_vector_submarine(draw, sx, sy, scale=0.28, body_col=C_DANGER if "B-59" in sname else (42, 54, 72), stroke_col=C_WHITE, prop_angle=global_t*20, facing="left")
            draw_map_pill(draw, 270 if i%2==0 else 770, 1185 + (i//2)*75, f"SUBMARINO {sname}", C_DANGER if "B-59" in sname else C_TACTICAL)
        return frame

    elif scene_id == 7:
        # S07: Steady B-59 Photo + Animated 78 Sailor Silhouettes Grid & Secret Warhead
        def _vec7(frame, draw, st, sd):
            # Panel showing 78 illuminated crew dots (13x6 grid) + warhead badge
            draw.rounded_rectangle([64, 765, 580, 995], radius=14, fill=(14, 20, 30), outline=C_TACTICAL, width=3)
            draw.text((322, 805), "78 HOMBRES A BORDO", font=FONT_PILL_MD, fill=C_TACTICAL, anchor="mm")
            lit = int(min(78, (st / max(0.1, sd * 0.7)) * 78))
            for ci in range(78):
                cx_d = 98 + (ci % 13) * 37
                cy_d = 850 + (ci // 13) * 22
                draw.ellipse([cx_d - 6, cy_d - 6, cx_d + 6, cy_d + 6], fill=C_TACTICAL if ci < lit else (45, 52, 64))
            if st > 0.8:
                draw.rounded_rectangle([64, 1020, 660, 1135], radius=14, fill=(44, 16, 18), outline=C_DANGER, width=3)
                draw_radiation_symbol(draw, 125, 1077, 32, angle_deg=st*80, col=C_AMBER)
                draw.text((405, 1077), "1 ARMA NUCLEAR SECRETA", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
        return render_module_a_steady(
            "b59", scene_t, scene_dur,
            "SUBMARINO B-59 · MAR CARIBE",
            "Washington no sabía que llevaba un torpedo nuclear T-5",
            "FOTO DE ARCHIVO · US NAVY / NATIONAL ARCHIVES, 1962 · DOMINIO PÚBLICO",
            extra_vector_fn=_vec7
        )

    elif scene_id == 8:
        # S08: Lowering Red-White Blockade Barrier Gate + Slamming "BLOQUEO" Stamp (like Berlin Airlift RT6my9-VxFI panel 1 & 2!)
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_caribbean_geography(draw)
        ang_gate = max(0.0, 26.0 * (1.0 - min(1.0, s_prog * 1.6)))
        gate_img, gx, gy = draw_barrier_gate(draw, 1010, angle_deg=ang_gate)
        frame.paste(gate_img, (gx, gy), gate_img)
        if s_prog > 0.38:
            # Red rubber stamp [ CUARENTENA / BLOQUEO ]
            sp = spring_val(scene_t, delay_sec=0.4, stiffness=200, damping=12)
            st_img = Image.new("RGBA", (540, 130), (0, 0, 0, 0))
            sd = ImageDraw.Draw(st_img)
            sd.rectangle([8, 8, 532, 122], outline=C_DANGER + (255,), width=7)
            sd.text((270, 65), "BLOQUEO NAVAL", font=FONT_HEADLINE, fill=C_DANGER + (255,), anchor="mm")
            rot_s = st_img.rotate(7, resample=Image.Resampling.BICUBIC, expand=True)
            frame.paste(rot_s, ((W - rot_s.width)//2, 740), rot_s)
        return frame

    elif scene_id == 9:
        # S09: Steady JFK Photo + Animated Radar Quarantine Sweep
        def _vec9(frame, draw, st, sd):
            cx_r, cy_r = 850, 860
            for r in [55, 105, 155]:
                draw.ellipse([cx_r - r, cy_r - r, cx_r + r, cy_r + r], outline=C_DANGER, width=2)
            a = st * 4.0
            draw.line([(cx_r, cy_r), (cx_r + int(155*math.cos(a)), cy_r + int(155*math.sin(a)))], fill=C_AMBER, width=4)
            draw_map_pill(draw, cx_r, cy_r + 190, "CERCO A CUBA", C_DANGER)
        return render_module_a_steady(
            "kennedy", scene_t, scene_dur,
            "CASA BLANCA · 22 OCT 1962",
            "John F. Kennedy ordena la cuarentena naval alrededor de Cuba",
            "FOTO DE ARCHIVO · WHITE HOUSE / CECIL STOUGHTON, 1962 · DOMINIO PÚBLICO",
            extra_vector_fn=_vec9
        )

    elif scene_id == 10:
        # S10: Top-Down Vector Aircraft Carrier Flight Deck (USS Randolph, like Midway panel 7!) + 11 Destroyers
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        cx_d, cy_d = W // 2, 1030
        # Wake lines behind carrier
        for wy_w in range(1260, 1410, 28):
            draw.line([(cx_d - 85, wy_w), (cx_d + 85, wy_w)], fill=(140, 195, 245), width=3)
        # Aircraft Carrier Flight Deck (Top-Down)
        draw.rounded_rectangle([cx_d - 125, 730, cx_d + 125, 1280], radius=22, fill=(72, 68, 62), outline=C_NEUTRAL, width=4)
        draw.line([(cx_d, 750), (cx_d, 1260)], fill=C_AMBER, width=4)
        # Parked planes on deck
        for py_p in [810, 910, 1010, 1110, 1200]:
            for px_p in [cx_d - 65, cx_d + 65]:
                draw.line([(px_p - 26, py_p), (px_p + 26, py_p)], fill=C_NEUTRAL, width=6)
                draw.line([(px_p, py_p - 22), (px_p, py_p + 22)], fill=C_NEUTRAL, width=6)
        # 11 Destroyers flanking on left and right
        for i in range(11):
            side = -1 if i < 6 else 1
            row_i = i if i < 6 else (i - 6)
            dx = cx_d + side * (250 + (row_i % 2) * 115)
            dy = 760 + row_i * 95 - int((scene_t * 35) % 45)
            draw.polygon([(dx, dy - 32), (dx + 16, dy + 28), (dx - 16, dy + 28)], fill=C_AMBER, outline=C_WHITE, width=2)
        draw_map_pill(draw, cx_d, 1345, "USS RANDOLPH + 11 DESTRUCTORES DE CAZA", C_DANGER)
        return frame

    elif scene_id == 11:
        # S11: Rossark Water Surface + Surface Fleet sweeping sonar cones downward while B-59 dives
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_rossark_water_surface(draw, 720, global_t, col=C_TACTICAL, n_ripples=2)
        for sx_d in [220, 540, 860]:
            sw_off = int(60 * wave(global_t * 1000.0, 2200.0, sx_d * 0.001))
            draw.polygon([(sx_d, 720), (sx_d - 140 + sw_off, 1260), (sx_d + 140 + sw_off, 1260)], fill=(18, 68, 112), outline=C_TACTICAL)
            draw.polygon([(sx_d - 65, 720), (sx_d + 65, 720), (sx_d + 80, 690), (sx_d - 55, 690)], fill=C_NEUTRAL)
        sub_y = int(960 + 240 * EASE_IN_OUT(s_prog))
        draw_vector_submarine(draw, W // 2, sub_y, scale=1.0, prop_angle=global_t * 16)
        draw_map_pill(draw, W // 2, sub_y + 78, "EL B-59 SE SUMERGE PARA NO SER DETECTADO", C_TACTICAL)
        return frame

    elif scene_id == 12:
        # S12: Rossark Alarm Buzz Recipe (±3° 4 cycles in 0.45s + vibration ticks) + Living 2.5D Sailor
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        kx, ky = W // 2, 790
        ang = global_t * 5.5
        for dir_sign in [-1, 1]:
            bx1 = kx + int(480 * math.cos(ang) * dir_sign)
            by1 = ky + 280
            draw.polygon([(kx, ky), (bx1 - 160, by1), (bx1 + 160, by1)], fill=(95, 22, 20))
        # Rossark buzz recipe: bursts of ±3° (4 cycles in 0.45s), then a pause
        burst_p = (global_t % 1.0)
        in_burst = burst_p < 0.45
        buzz_dx = int(6 * math.sin(burst_p / 0.45 * 4 * 2 * math.pi)) if in_burst else 0
        draw.rounded_rectangle([kx - 55 + buzz_dx, ky - 75, kx + 55 + buzz_dx, ky + 25], radius=28, fill=C_DANGER, outline=C_WHITE, width=4)
        draw.rectangle([kx - 75 + buzz_dx, ky + 15, kx + 75 + buzz_dx, ky + 45], fill=(55, 60, 70), outline=C_NEUTRAL, width=3)
        if in_burst:
            for side in [-1, 1]:
                draw.arc([kx + side * 85 - 20, ky - 55, kx + side * 85 + 20, ky + 5], start=-60 if side > 0 else 120, end=60 if side > 0 else 240, fill=C_AMBER, width=4)
        draw_rossark_officer(frame, 250, 1140, scale=0.95, role="sailor", global_t=global_t, scene_t=scene_t, mood="tired")
        draw = ImageDraw.Draw(frame)
        draw_digital_led_box(draw, 660, 1180, "ALARMA · -90 M", C_DANGER)
        return frame

    elif scene_id == 13:
        # S13: Steady Foxtrot Photo + Animated Draining Battery & Rising CO2 Gauges
        def _vec13(frame, draw, st, sd):
            pct = max(4, int(38 - 34 * (st / max(0.1, sd))))
            draw.rounded_rectangle([64, 1020, 520, 1280], radius=16, fill=(16, 20, 28), outline=C_DANGER, width=3)
            draw.text((292, 1075), f"BATERÍAS: {pct}%", font=FONT_PILL_LG, fill=C_DANGER, anchor="mm")
            for bi in range(5):
                bx = 105 + bi * 78
                is_on = (pct >= (bi + 1) * 8)
                draw.rectangle([bx, 1130, bx + 62, 1230], fill=C_DANGER if bi==0 else (C_AMBER if is_on else (35, 40, 48)), outline=C_WHITE, width=2)
            draw.rounded_rectangle([560, 1020, W - 64, 1280], radius=16, fill=(16, 20, 28), outline=C_AMBER, width=3)
            draw.text((788, 1075), "AIRE Y OXÍGENO", font=FONT_PILL_LG, fill=C_AMBER, anchor="mm")
            draw.text((788, 1155), "O2 AGOTÁNDOSE", font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
            draw.text((788, 1215), "CO2 EN NIVEL TÓXICO", font=FONT_PILL_SM, fill=C_DANGER, anchor="mm")
        return render_module_a_steady(
            "foxtrot", scene_t, scene_dur,
            "SUBMARINO DIÉSEL · PROYECTO 641",
            "Bajo el agua no puede recargar baterías ni renovar el oxígeno",
            "FOTO DE ARCHIVO · SUBMARINO CLASE FOXTROT · CC BY-SA 3.0",
            extra_vector_fn=_vec13
        )

    elif scene_id == 14:
        # S14: Rossark Step-Clock Recipe (steps once a second with EASE_OUT) + Severed Radio Waves to Moscow
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        cx_c, cy_c, r_c = W // 2, 885, 165
        draw.ellipse([cx_c - r_c - 8, cy_c - r_c - 8, cx_c + r_c + 8, cy_c + r_c + 8], fill=(95, 82, 62), outline=C_AMBER, width=4)
        draw.ellipse([cx_c - r_c, cy_c - r_c, cx_c + r_c, cy_c + r_c], fill=C_PAPER)
        for h_i in range(12):
            a = math.radians(h_i * 30 - 90)
            draw.line([(cx_c + int((r_c-22)*math.cos(a)), cy_c + int((r_c-22)*math.sin(a))), (cx_c + int((r_c-8)*math.cos(a)), cy_c + int((r_c-8)*math.sin(a)))], fill=C_INK, width=4)
        # Rossark clock hand recipe: steps once a second with ease-out
        sec_whole = math.floor(global_t * 2.0)
        sec_frac = EASE_OUT(min(1.0, ((global_t * 2.0) - sec_whole) / 0.35))
        ang_m = math.radians((sec_whole + sec_frac) * 30.0 - 90.0)
        ang_h = math.radians(global_t * 24.0 - 30.0)
        draw.line([(cx_c, cy_c), (cx_c + int(100*math.cos(ang_h)), cy_c + int(100*math.sin(ang_h)))], fill=C_INK, width=9)
        draw.line([(cx_c, cy_c), (cx_c + int(140*math.cos(ang_m)), cy_c + int(140*math.sin(ang_m)))], fill=C_DANGER, width=6)
        draw_map_pill(draw, 220, 1185, "B-59 (-90 M)", C_TACTICAL)
        draw_map_pill(draw, 860, 1185, "MOSCÚ", C_DANGER)
        draw.line([(360, 1185), (720, 1185)], fill=C_DANGER, width=5)
        draw.text((W // 2, 1185), "X", font=FONT_HEADLINE, fill=C_DANGER, anchor="mm")
        draw_map_pill(draw, W // 2, 1320, "¿YA EMPEZÓ LA TERCERA GUERRA MUNDIAL ARRIBA?", C_AMBER)
        return frame

    elif scene_id == 15:
        # S15: Stopping A/C Ventilation Fan + Boiling +50°C Thermometer + Rossark Steam Wisps & Exhausted Sailor
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        fx, fy = 230, 840
        draw.ellipse([fx - 105, fy - 105, fx + 105, fy + 105], fill=(22, 26, 34), outline=C_AMBER, width=4)
        fan_ang = global_t * max(0.15, 4.0 * (1.0 - s_prog))
        for b in range(4):
            ba = fan_ang + b * (math.pi / 2)
            draw.line([(fx, fy), (fx + int(84*math.cos(ba)), fy + int(84*math.sin(ba)))], fill=C_NEUTRAL, width=15)
        draw_map_pill(draw, fx, fy + 145, "A/C: APAGADO", C_AMBER)
        # Center: Boiling Mercury Thermometer + Rising Rossark Steam Wisps (bell(p))
        tx, ty0, ty1 = 520, 720, 1120
        draw_rossark_steam_wisps(frame, tx, ty0 + 40, global_t, count=5, col=(240, 180, 160))
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle([tx - 26, ty0, tx + 26, ty1], radius=26, fill=(24, 20, 22), outline=C_NEUTRAL, width=4)
        draw.ellipse([tx - 48, ty1 - 35, tx + 48, ty1 + 60], fill=C_DANGER, outline=C_NEUTRAL, width=4)
        temp_val = int(38 + 14 * EASE_OUT(s_prog))
        fill_y = int(ty1 - (ty1 - ty0 - 30) * EASE_OUT(s_prog))
        draw.rounded_rectangle([tx - 15, fill_y, tx + 15, ty1 + 15], radius=14, fill=C_DANGER)
        draw_digital_led_box(draw, 835, 820, f"+{temp_val} °C", C_DANGER)
        # Exhausted sailor with heavy eyelids (lid = 0.35 per Rossark Section 4 table)
        draw_rossark_officer(frame, 835, 1110, scale=0.88, role="sailor", global_t=global_t, scene_t=scene_t, mood="tired")
        draw = ImageDraw.Draw(frame)
        draw_map_pill(draw, W // 2, 1335, "LOS MARINEROS SE DESMAYAN EN SUS PUESTOS", C_DANGER)
        return frame

    elif scene_id == 16:
        # S16: Steady USS Cony Photo + Animated Falling Depth Charges (Seeded Rossark Phases)
        def _vec16(frame, draw, st, sd):
            for i in range(4):
                px = 240 + i * 200
                p_fall = loop_p(st * 1000.0, 1500.0 + seeded(i, 1) * 300.0, phase=seeded(i, 2))
                py = 940 + int(p_fall * 350)
                for bi in range(4):
                    draw.ellipse([px - 4, py - 35 - bi*18, px + 4, py - 27 - bi*18], outline=C_TACTICAL, width=2)
                draw.rounded_rectangle([px - 18, py - 24, px + 18, py + 24], radius=6, fill=C_AMBER, outline=C_WHITE, width=3)
        return render_module_a_steady(
            "cony", scene_t, scene_dur,
            "DESTRUCTOR USS CONY (DD-508)",
            "Lanzan pequeñas cargas de profundidad sobre el B-59",
            "FOTO DE ARCHIVO · US NAVY (USS CONY DD-508), 1962 · DOMINIO PÚBLICO",
            extra_vector_fn=_vec16
        )

    elif scene_id == 17:
        # S17: Reconstructed US Navy Signaling Directive + Moving Hand
        return render_module_c_document_with_hand(
            scene_t,
            "DIRECTIVA DE CUARENTENA NAVAL · US ATLANTIC FLEET",
            "PROCEDIMIENTO DE SEÑALIZACIÓN ACÚSTICA (PDC):",
            [
                "1. Lanzar granadas de práctica inofensivas.",
                "2. Objetivo: Indicar al submarino que suba.",
                "3. Obligar al B-59 a emerger e identificarse.",
                "4. ALERTA: Moscú desconoce este protocolo."
            ],
            highlight_idx={1, 2},
            stamp_text="SEÑAL DE PRÁCTICA",
            source_attr="FUENTE HISTÓRICA · DIRECTIVA NAVAL DE EE. UU. (OCTUBRE 1962)",
            tilt_deg=1.4
        )

    elif scene_id == 18:
        # S18: Rossark Rule 5.13 Strike: Hammer winds up, stops at top, hits at mid-swing fastest + Hull Volume Squash (sx = 1/sy^0.6)
        cycle_ms = (global_t * 1000.0) % 900.0
        # Strike track: wind up [0..350ms], fast swing through contact at 480ms, follow-through & recover [480..900ms]
        ham_y = int(track(cycle_ms, [(0, 740), (320, 680), (480, 965, "out"), (650, 820), (900, 740)]))
        in_contact = 460.0 <= cycle_ms <= 570.0
        squash_k = 1.0 - seg(cycle_ms, 460.0, 570.0) if in_contact else 0.0
        hull_sy = 1.0 - 0.14 * squash_k
        hull_sx = 1.0 / (hull_sy ** 0.6)

        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        cx_h, cy_h = W // 2, 1080
        for r in range(1, 5):
            p_ring = loop_p(global_t * 1000.0, 1100.0, phase=r * 0.22)
            rad = int(55 + p_ring * 240)
            draw.ellipse([cx_h - rad, cy_h - rad, cx_h + rad, cy_h + rad], outline=C_DANGER if r%2==0 else C_AMBER, width=max(1, int(5 * bell(p_ring))))
        # Giant vector hammer swinging down onto the hull
        draw.rectangle([cx_h - 14, ham_y - 130, cx_h + 14, ham_y], fill=C_AMBER, outline=C_WHITE, width=2)
        draw.rounded_rectangle([cx_h - 95, ham_y - 35, cx_h + 95, ham_y + 35], radius=10, fill=C_DANGER, outline=C_WHITE, width=4)
        # Submarine hull with Rossark volume-preserving squash at contact
        w_half = int(260 * hull_sx)
        h_half = int(40 * hull_sy)
        draw.rounded_rectangle([cx_h - 42, cy_h - h_half - int(44 * hull_sy), cx_h + 38, cy_h - h_half + 6], radius=8, fill=(55, 20, 22) if in_contact else (32, 44, 62), outline=C_WHITE, width=3)
        draw.rounded_rectangle([cx_h - w_half, cy_h - h_half, cx_h + w_half, cy_h + h_half], radius=h_half, fill=(55, 20, 22) if in_contact else (32, 44, 62), outline=C_WHITE, width=3)
        draw_map_pill(draw, W // 2, 1365, "LAS LUCES PARPADEAN EN LA OSCURIDAD", C_DANGER)
        return frame

    elif scene_id == 19:
        # S19: Living 2.5D Captain Valentin Savitsky (Rage + Fist Gesture) + Red Targeting Crosshair
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        cx_s, cy_s = W // 2, 980
        draw.polygon([(cx_s - 90, 650), (cx_s + 90, 650), (cx_s + 320, 1380), (cx_s - 320, 1380)], fill=(58, 20, 22))
        draw_rossark_officer(frame, cx_s, cy_s, scale=1.55, role="savitsky", global_t=global_t, scene_t=scene_t, talking=True, mood="rage", gesture="fist_rage")
        draw = ImageDraw.Draw(frame)
        ch_rad = int(175 - 35 * EASE_OUT(min(1.0, s_prog * 1.4)))
        draw_crosshair(draw, cx_s, cy_s + 35, ch_rad, col=C_DANGER)
        draw_map_pill(draw, cx_s, 1320, "CAPITÁN SAVITSKY: «LA GUERRA YA ESTALLÓ»", C_DANGER)
        return frame

    elif scene_id == 20:
        # S20: Reconstructed Vadim Orlov Diary + Moving Hand Underlining Savitsky's Quote
        return render_module_c_document_with_hand(
            scene_t,
            "DIARIO DEL CAPITÁN VADIM ORLOV · PUENTE DEL B-59",
            "ORDEN VERBAL DEL COMANDANTE VALENTÍN SAVITSKY:",
            [
                "«¡Los vamos a volar ahora mismo!",
                "¡Moriremos, pero los hundiremos",
                "a todos!",
                "¡No seremos la vergüenza de la flota!»"
            ],
            highlight_idx={0, 1, 3},
            stamp_text="ORDEN DE DISPARO",
            source_attr="FUENTE HISTÓRICA · MEMORIAS DE VADIM ORLOV / NATIONAL SECURITY ARCHIVE",
            tilt_deg=-1.6
        )

    elif scene_id == 21:
        # S21: 2 Living 2.5D Rossark Officers (Savitsky & Maslennikov) closing 2 Firing Switches in Series
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw.line([(120, 1140), (W - 120, 1140)], fill=C_AMBER, width=8)
        for i, (cx_o, role_lbl, r_type, mood) in enumerate([
            (330, "1. CAPITÁN", "savitsky", "rage"),
            (750, "2. OFICIAL POLÍTICO", "maslennikov", "focused")
        ]):
            draw_rossark_officer(frame, cx_o, 890, scale=1.12, role=r_type, global_t=global_t, scene_t=scene_t, talking=(i == 0), mood=mood, gesture="turn_key")
            draw = ImageDraw.Draw(frame)
            draw_map_pill(draw, cx_o, 1065, role_lbl, C_AMBER)
            draw.ellipse([cx_o - 22, 1118, cx_o + 22, 1162], fill=C_AMBER, outline=C_WHITE, width=3)
        draw_map_pill(draw, W // 2, 1285, "EN UN SUBMARINO NORMAL BASTABAN 2 FIRMAS", C_AMBER)
        return frame

    elif scene_id == 22:
        # S22: Both Brass Keys Rotating into "ARMADO" with Hands Turning Them
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        for i, (cx_k, name) in enumerate([(330, "1. SAVITSKY: SÍ"), (750, "2. MASLÉNNIKOV: SÍ")]):
            draw.rounded_rectangle([cx_k - 180, 740, cx_k + 180, 1120], radius=22, fill=(58, 18, 20), outline=C_DANGER, width=4)
            draw.text((cx_k, 815), name, font=FONT_PILL_MD, fill=C_WHITE, anchor="mm")
            draw.ellipse([cx_k - 65, 895, cx_k + 65, 1025], fill=(28, 14, 16), outline=C_AMBER, width=5)
            ang = math.radians(90 * EASE_IN_OUT(min(1.0, s_prog * 1.5)))
            draw.line([(cx_k - int(42*math.cos(ang)), 960 - int(42*math.sin(ang))), (cx_k + int(42*math.cos(ang)), 960 + int(42*math.sin(ang)))], fill=C_AMBER, width=10)
            h_rot, hx, hy = draw_vector_hand(draw, cx_k, 1185, angle_deg=-10)
            frame.paste(h_rot, (hx, hy), h_rot)
        return frame

    elif scene_id == 23:
        # S23: Steady Crossroads Baker Photo + Top-Down Carrier engulfed by 15 KT Blast Ring
        def _vec23(frame, draw, st, sd):
            cx_b, cy_b = W // 2, 1020
            for r in range(1, 4):
                rad = int((st * 130 + r * 65) % 260)
                draw.ellipse([cx_b - rad, cy_b - rad, cx_b + rad, cy_b + rad], outline=C_DANGER if r%2==0 else C_AMBER, width=4)
            draw_crosshair(draw, cx_b, cy_b, 95, col=C_DANGER)
        return render_module_a_steady(
            "baker", scene_t, scene_dur,
            "IMPACTO NUCLEAR DE 15 KILOTONES",
            "Si disparan, el portaaviones USS Randolph desaparece en el acto",
            "FOTO DE ARCHIVO · US DOD (OPERACIÓN CROSSROADS BAKER), 1946 · DOMINIO PÚBLICO",
            extra_vector_fn=_vec23
        )

    elif scene_id == 24:
        # S24: Cold War Map with Animated Red ICBM Missile Arcs (US <-> Moscow) + DEFCON 1 LED Box
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_caribbean_geography(draw)
        p_carib, p_usa, p_moscow = (520, 1020), (280, 740), (880, 710)
        draw.line([p_carib, p_usa], fill=C_DANGER, width=6)
        for arc_h in [0, 45, 90]:
            draw.arc([280, 650 - arc_h, 880, 920], start=180, end=180 + int(180 * EASE_OUT(min(1.0, s_prog * 1.4))), fill=C_DANGER, width=5)
        draw_map_pill(draw, 280, 740, "EE. UU.", C_AMBER)
        draw_map_pill(draw, 860, 710, "MOSCÚ", C_DANGER)
        draw_digital_led_box(draw, W // 2, 1265, "DEFCON 1 · GUERRA TOTAL", C_DANGER)
        return frame

    elif scene_id == 25:
        # S25: 3 Living 2.5D Rossark Officers & Dramatic Blue Spotlight Beam revealing The 3rd Man (Arkhipov)
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        draw.polygon([(700, 650), (860, 650), (1020, 1410), (540, 1410)], fill=(20, 44, 82))
        for cx_o, name, col, r_type, mood, gest, sc in [
            (235, "SAVITSKY", C_DANGER, "savitsky", "rage", "rest", 0.95),
            (510, "MASLÉNNIKOV", C_DANGER, "maslennikov", "focused", "rest", 0.95),
            (795, "3.er HOMBRE", C_TACTICAL, "arkhipov", "focused", "stop_hand", 1.18)
        ]:
            cy_o = 965 if r_type == "arkhipov" else 995
            draw_rossark_officer(frame, cx_o, cy_o, scale=sc, role=r_type, global_t=global_t, scene_t=scene_t, talking=(r_type == "arkhipov"), mood=mood, gesture=gest)
            draw = ImageDraw.Draw(frame)
            draw_map_pill(draw, cx_o, cy_o + int(195 * sc), name, col)
        return frame

    elif scene_id == 26:
        # S26: Steady Vasili Arkhipov Portrait + Animated Flotilla Command Star Badge
        def _vec26(frame, draw, st, sd):
            draw_map_pill(draw, 815, 720, "JEFE DE ESTADO MAYOR", C_TACTICAL)
        return render_module_a_steady(
            "arkhipov", scene_t, scene_dur,
            "VASILI ARKHIPOV · 36 AÑOS",
            "El mismo rango que el capitán, pero jefe de toda la flotilla",
            "FOTO DE ARCHIVO · ARCHIVO FAMILIAR ARKHIPOV, 1962 · CC BY-SA 4.0",
            extra_vector_fn=_vec26
        )

    elif scene_id == 27:
        # S27: Reconstructed Fleet Regulation + Moving Hand Underlining "Unanimidad de los TRES"
        return render_module_c_document_with_hand(
            scene_t,
            "REGLAMENTO DE COMBATE · FLOTA DEL NORTE (URSS)",
            "PROTOCOLO CON JEFE DE ESTADO MAYOR A BORDO:",
            [
                "• Voto 1: Comandante del B-59 (Savitsky) -> SÍ",
                "• Voto 2: Oficial Político (Maslénnikov) -> SÍ",
                "• Voto 3: Jefe de Flotilla (Arkhipov) -> OBLIGATORIO",
                "• REGLA: Exige que los TRES voten que sí."
            ],
            highlight_idx={2, 3},
            stamp_text="3 VOTOS EXIGIDOS",
            source_attr="FUENTE HISTÓRICA · ARCHIVOS DE LA FLOTA DEL NORTE (URSS)",
            tilt_deg=-1.3
        )

    elif scene_id == 28:
        # S28: Steady K-19 Photo + Spinning Radiation Symbol & Dosimeter Alert
        def _vec28(frame, draw, st, sd):
            draw_radiation_symbol(draw, 880, 775, 58, angle_deg=st * 75, col=C_AMBER)
            draw_map_pill(draw, 880, 865, "FUGA EN REACTOR", C_DANGER)
        return render_module_a_steady(
            "k19", scene_t, scene_dur,
            "SUBMARINO K-19 · JULIO DE 1961",
            "Un año antes sobrevivió a una fuga radiactiva en el submarino K-19",
            "FOTO DE ARCHIVO · US NAVY (SUBMARINO K-19), 1961 · DOMINIO PÚBLICO",
            extra_vector_fn=_vec28
        )

    elif scene_id == 29:
        # S29: 8 Fallen Sailors Silhouettes + Glowing Red Nuclear Door held shut by Arkhipov's Hand
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        for i in range(8):
            sx_m = 115 + (i % 4) * 95
            sy_m = 820 + (i // 4) * 195
            draw.ellipse([sx_m - 24, sy_m - 60, sx_m + 24, sy_m - 12], fill=(48, 22, 24), outline=C_DANGER, width=2)
            draw.rounded_rectangle([sx_m - 36, sy_m - 8, sx_m + 36, sy_m + 75], radius=12, fill=(48, 22, 24), outline=C_DANGER, width=2)
        draw_map_pill(draw, 260, 1185, "8 MUERTOS POR RADIACIÓN", C_DANGER)
        dx0, dy0 = 590, 730
        draw.rounded_rectangle([dx0, dy0, dx0 + 380, dy0 + 520], radius=18, fill=(52, 18, 20), outline=C_DANGER, width=5)
        draw_radiation_symbol(draw, dx0 + 190, dy0 + 200, 68, angle_deg=global_t * 60, col=C_AMBER)
        h_rot, hx, hy = draw_vector_hand(draw, dx0 + 190, dy0 + 390, angle_deg=0, sleeve_col=(24, 48, 86))
        frame.paste(h_rot, (hx, hy), h_rot)
        return frame

    elif scene_id == 30:
        # S30: Climax Veto: 3 Living 2.5D Officers + Giant Blue "NO" Card + Barrier Gate Blocking Launch
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        for i, (lbl, v_txt, col, is_no, r_type, mood, gest) in enumerate([
            ("CAPITÁN", "SÍ", C_DANGER, False, "savitsky", "rage", "fist_rage"),
            ("POLÍTICO", "SÍ", C_DANGER, False, "maslennikov", "focused", "rest"),
            ("ARKHIPOV", "«NO»", C_TACTICAL, True, "arkhipov", "focused", "stop_hand")
        ]):
            kx = 88 + i * 312
            ky = 920
            draw_rossark_officer(frame, kx + 140, 770, scale=0.80, role=r_type, global_t=global_t, scene_t=scene_t, talking=is_no, mood=mood, gesture=gest)
            draw = ImageDraw.Draw(frame)
            draw.rounded_rectangle([kx, ky, kx + 280, ky + 280], radius=22, fill=(18, 42, 86) if is_no else (48, 18, 20), outline=C_WHITE if is_no else col, width=5 if is_no else 3)
            draw.text((kx + 140, ky + 65), lbl, font=FONT_PILL_MD, fill=C_NEUTRAL, anchor="mm")
            draw.text((kx + 140, ky + 175), v_txt, font=FONT_BIG_NUM, fill=C_WHITE if is_no else col, anchor="mm")
        gate_img, gx, gy = draw_barrier_gate(draw, 1265, angle_deg=0.0)
        frame.paste(gate_img, (gx, gy), gate_img)
        return frame

    elif scene_id == 31:
        # S31: Underwater Sonar Diagram: Lateral Blasts vs Zero Top Hull Hits
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        cx_h, cy_h = W // 2, 1080 + int(3.0 * wave(global_t * 1000.0, 2800.0))
        draw.rounded_rectangle([cx_h - 260, 720, cx_h + 260, 865], radius=14, fill=(14, 30, 52), outline=C_TACTICAL, width=3)
        draw.text((cx_h, 765), "ENCIMA DEL CASCO (ATAQUE REAL)", font=FONT_PILL_SM, fill=C_NEUTRAL, anchor="mm")
        draw.text((cx_h, 818), "0 EXPLOSIONES DIRECTAS", font=FONT_PILL_LG, fill=C_TACTICAL, anchor="mm")
        for sx_b in [185, W - 185]:
            for r in range(1, 4):
                p_r = loop_p(global_t * 1000.0, 1400.0, phase=r * 0.28)
                rad = int(32 + p_r * 80)
                draw.ellipse([sx_b - rad, cy_h - rad, sx_b + rad, cy_h + rad], outline=C_AMBER, width=max(1, int(4 * bell(p_r))))
            draw_map_pill(draw, sx_b, cy_h + 135, "A LOS COSTADOS", C_AMBER)
        draw_vector_submarine(draw, cx_h, cy_h, scale=0.95, prop_angle=global_t*14)
        return frame

    elif scene_id == 32:
        # S32: Rossark Travelling Water Surface & B-59 Ascending to Surface with Buoyancy Bob
        frame = CANVAS_TACTICAL_MAP.copy()
        draw = ImageDraw.Draw(frame)
        draw_rossark_water_surface(draw, 715, global_t, col=C_TACTICAL, n_ripples=4)
        sub_y = int(1180 - 380 * EASE_IN_OUT(s_prog) + 3.5 * wave(global_t * 1000.0, 2400.0))
        draw_vector_submarine(draw, W // 2, sub_y, scale=1.05, prop_angle=global_t * 22)
        draw_map_pill(draw, W // 2, sub_y - 95, "TORPEDO DESARMADO · SUBIENDO A 0 m", C_TACTICAL)
        return frame

    elif scene_id == 33:
        # S33: Steady B-59 Surfaced Photo
        return render_module_a_steady(
            "b59", scene_t, scene_dur,
            "SUPERFICIE DEL CARIBE · 27 OCT 1962",
            "El B-59 desarma el torpedo nuclear y sale a la superficie",
            "FOTO DE ARCHIVO · US NAVY / NATIONAL ARCHIVES, 1962 · DOMINIO PÚBLICO"
        )

    elif scene_id == 34:
        # S34: Reconstructed Kremlin Dossier + Moving Hand Underlining Malinovsky's Reprimand
        return render_module_c_document_with_hand(
            scene_t,
            "MINISTERIO DE DEFENSA DE LA URSS · MOSCÚ (NOV 1962)",
            "REPROCHE OFICIAL DEL MARISCAL RODIÓN MALINOVSKY:",
            [
                "• Ningún recibimiento como héroes en Moscú.",
                "• Declaración oficial ante la tripulación:",
                "«Habría sido mejor que ustedes se hundieran",
                "con su propio barco antes que subir.»"
            ],
            highlight_idx={2, 3},
            stamp_text="SECRETO DE ESTADO",
            source_attr="FUENTE HISTÓRICA · ACTAS DEL MINISTERIO DE DEFENSA DE LA URSS (1962)",
            tilt_deg=1.4
        )

    elif scene_id == 35:
        # S35: Steady Arkhipov Portrait + Spinning Year Counter (1962 -> 2002)
        def _vec35(frame, draw, st, sd):
            yr = int(1962 + min(40, EASE_OUT(min(1.0, st / max(0.1, sd * 0.65))) * 40))
            draw_digital_led_box(draw, 820, 775, str(yr), C_AMBER if yr==2002 else C_TACTICAL)
        return render_module_a_steady(
            "arkhipov", scene_t, scene_dur,
            "DESCLASIFICADO EN EL AÑO 2002",
            "40 años oculto hasta la Conferencia de La Habana (2002)",
            "FOTO DE ARCHIVO · ARCHIVO ARKHIPOV / NATIONAL SECURITY ARCHIVE · CC BY-SA 4.0",
            extra_vector_fn=_vec35
        )

    elif scene_id == 36:
        # S36: Golden Balance Scale tipping with EASE_IN_OUT + dropping weights (2 Votes vs 1)
        frame = CANVAS_ABYSS.copy()
        draw = ImageDraw.Draw(frame)
        tilt = 12.0 * EASE_IN_OUT(min(1.0, max(0.0, (scene_t - 0.25) / 1.1))) + 1.2 * wave(global_t * 1000.0, 3200.0)
        draw_balance_scale(
            draw, W // 2, 1340,
            tilt_deg=tilt,
            left_pills=["CAPITÁN SAVITSKY", "OFICIAL MASLÉNNIKOV"],
            right_pills=["VASILI ARKHIPOV", "PIDIÓ ESPERAR"],
            left_title="2 VOTOS: DISPARAR",
            right_title="1 VOTO: ESPERAR",
            left_col=C_DANGER,
            right_col=C_TACTICAL,
            drop_prog=s_prog * 1.4
        )
        return frame

    else:
        # Scene 37: Final Dilemma over Rock-Steady B-59 Photo + Rossark Jiggle Action Buttons!
        frame = PHOTOS_STEADY_STAGE.get("b59", CANVAS_ABYSS).copy()
        draw = ImageDraw.Draw(frame)
        for r in range(2):
            rp = loop_p(global_t * 1000.0, 1600.0, phase=r * 0.5)
            rad = int(50 + rp * 260)
            draw.ellipse([W//2 - rad, 940 - rad, W//2 + rad, 940 + rad], outline=C_TACTICAL, width=max(1, int(3 * bell(rp))))
        draw_rossark_jiggle_button(draw, W // 2, 1125, 580, 80, "GIRAR LA LLAVE NUCLEAR", (24, 14, 16), C_DANGER, global_t, phase_offset=0.0)
        draw_rossark_jiggle_button(draw, W // 2, 1225, 660, 80, "SALIR A LA SUPERFICIE", (14, 24, 42), C_TACTICAL, global_t, phase_offset=0.5)
        draw.rounded_rectangle([140, 1295, W - 140, 1375], radius=12, fill=(18, 20, 24), outline=C_AMBER, width=3)
        draw.text((W // 2, 1335), "CONTÁMELO EN LOS COMENTARIOS", font=FONT_PILL_MD, fill=C_AMBER, anchor="mm")
        draw_attribution_pill(draw, "FOTO DE ARCHIVO · US NAVY / NATIONAL ARCHIVES, 1962 · DOMINIO PÚBLICO")
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
        draw_map_pill(draw, W // 2, 340, "SONAR HIDROFÓNICO · 27 DE OCTUBRE DE 1962", C_TACTICAL)
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
            active_w = len(ch["words"]) - 1
            for wi, wo in enumerate(ch["words"]):
                if t <= wo["end"]:
                    active_w = wi
                    break
            return idx, active_w, sid, max(0.0, t - sb_s), max(0.1, sb_e - sb_s)
    return len(CHUNKS) - 1, 0, 37, 1.0, 1.0

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

srt_path = "produccion/01_submarino_b59/submarino_b59_es.srt"
with open(srt_path, "w", encoding="utf-8") as sf:
    for idx_c, ch in enumerate(CHUNKS, 1):
        sf.write(f"{idx_c}\n")
        sf.write(f"{format_srt_time(ch['start'])} --> {format_srt_time(ch['end'])}\n")
        sf.write(f"{ch['text']}\n\n")

print("Rendering 12-frame verification mosaic (storyboard_verificacion.jpg)...")
sample_times = [2.8, 12.2, 23.5, 48.0, 56.5, 67.5, 74.5, 86.0, 102.5, 131.5, 162.5, 174.5]
grid = Image.new("RGB", (4 * 270, 3 * 480), (0, 0, 0))
for i, st in enumerate(sample_times):
    f_im = render_frame_at(st).resize((270, 480), Image.Resampling.LANCZOS)
    grid.paste(f_im, ((i % 4) * 270, (i // 4) * 480))
grid.save("produccion/01_submarino_b59/storyboard_verificacion.jpg", quality=92)

if "--storyboard-only" in sys.argv:
    print("Storyboard verification complete.")
    sys.exit(0)

# Render at native 30fps -> 60fps (exact 2:1 integer multiple, ZERO pulldown stutter & ZERO image tremor!)
INTERNAL_FPS = 30
total_frames = int(TOTAL_DUR * INTERNAL_FPS)
out_mp4 = "produccion/01_submarino_b59/submarino_b59_short.mp4"
audio_path = "produccion/01_submarino_b59/audio/audio_master_180s.wav"

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
