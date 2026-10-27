import os
import json
import math
import wave
import struct
import subprocess

os.makedirs("produccion/05_isla_kiska/audio", exist_ok=True)

raw_mp3 = "produccion/05_isla_kiska/audio/voz_raw.mp3"
clean_wav = "produccion/05_isla_kiska/audio/voz_clean.wav"

# Convert raw_mp3 to 48kHz mono WAV (1.0x natural pitch & speed, highpass + gentle afftdn to clean any rumble)
subprocess.run([
    "ffmpeg", "-y", "-i", raw_mp3,
    "-af", "highpass=f=85,afftdn=nf=-28",
    "-ar", "48000", "-ac", "1", clean_wav
], capture_output=True, check=True)

# 58 exact acoustic segments (raw_start, raw_end, text, bbox_word, pause_after, scene_id)
# Rapid 1-to-1 scene cuts on the first 6 segments (Scenes 1..6) starting at t=0.00s for an explosive, high-retention opening hook!
SEGMENTS = [
    # EXPLOSIVE HOOK (Scenes 1..6) — 6 rapid cuts in 12.8s!
    (0.04, 2.78, "¿Cómo hacés para perder más de 300 hombres,", "300", 0.08, 1),
    (2.79, 4.02, "entre muertos y heridos,", "muertos", 0.14, 2),
    (4.24, 5.15, "asaltando una isla", "isla", 0.05, 3),
    (5.15, 7.56, "donde no hay ni un solo soldado enemigo?", "enemigo?", 0.22, 4),
    (8.18, 9.89, "Aunque parezca un absurdo imposible,", "imposible,", 0.16, 5),
    (10.08, 12.57, "le pasó a Estados Unidos y Canadá en Alaska.", "Alaska.", 0.78, 6),

    # CONTEXT: ALEUTIANS, ATTU CARNAGE & KISKA BUILDUP (Scenes 7..13)
    (14.22, 15.66, "En 1942,", "1942,", 0.14, 7),
    (15.81, 20.08, "Japón había ocupado dos islas estadounidenses en el archipiélago de las Aleutianas:", "Aleutianas:", 0.18, 7),
    (20.43, 21.46, "Attu y Kiska.", "Kiska.", 0.24, 8),
    (21.93, 26.00, "Es el único territorio norteamericano invadido en toda la Segunda Guerra Mundial.", "único", 0.34, 8),
    (26.70, 27.88, "En mayo del 43,", "43,", 0.14, 9),
    (28.07, 30.58, "Estados Unidos recupera primero la isla de Attu.", "Attu.", 0.24, 9),
    (30.93, 32.68, "La batalla es una carnicería:", "carnicería:", 0.18, 10),
    (32.99, 37.94, "casi todos los 2.500 defensores japoneses pelean hasta la muerte en cargas suicidas.", "2.500", 0.30, 10),
    (38.40, 39.83, "El siguiente objetivo es Kiska,", "Kiska,", 0.18, 11),
    (40.08, 45.36, "donde los aviones espía calculan que esperan más de 5.000 japoneses metidos en túneles bajo la roca.", "5.000", 0.28, 11),
    (45.80, 47.13, "Para no repetir el desastre,", "desastre,", 0.16, 12),
    (47.35, 49.54, "el Pentágono organiza una fuerza gigantesca", "gigantesca", 0.10, 12),
    (49.56, 53.37, "con 34.400 soldados y 100 barcos de guerra.", "34.400", 0.65, 13),

    # BATTLE OF THE PIPS & ADMIRAL KIMURA'S 55-MINUTE EVACUATION (Scenes 14..23)
    (54.91, 56.14, "Lo que Washington ignora", "ignora", 0.12, 14),
    (56.29, 58.26, "es lo que acaba de ocurrir bajo la niebla.", "niebla.", 0.28, 14),
    (58.81, 60.48, "Tres semanas antes del desembarco,", "semanas", 0.14, 15),
    (60.52, 65.51, "dos acorazados estadounidenses detectan siete ecos en su pantalla de radar cerca de la isla", "siete", 0.18, 15),
    (65.75, 68.84, "y disparan más de mil proyectiles pesados contra el mar vacío.", "mil", 0.28, 16),
    (69.33, 70.72, "Creen que fue un fallo del radar,", "fallo", 0.16, 17),
    (70.96, 73.18, "la llamada batalla de los puntos fantasma,", "fantasma,", 0.18, 17),
    (73.44, 74.88, "y se retiran a cargar munición.", "retiran", 0.32, 18),
    (75.49, 77.53, "Mientras los barcos estadounidenses se alejan,", "alejan,", 0.16, 18),
    (77.74, 83.03, "el contraalmirante japonés Masatomi Kimura hace algo contrario al código militar de su país.", "Kimura", 0.28, 19),
    (83.48, 87.10, "Decide que la vida de sus hombres vale más que un sacrificio inútil.", "vida", 0.32, 20),
    (87.68, 89.42, "Aprovecha un banco de niebla espesa,", "niebla", 0.16, 21),
    (89.66, 91.47, "entra a toda máquina con sus buques", "máquina", 0.14, 21),
    (91.66, 95.01, "y embarca a los 5.183 soldados japoneses", "5.183", 0.12, 22),
    (95.05, 97.22, "en solo 55 minutos.", "55", 0.24, 22),
    (97.64, 100.12, "Toda la guarnición escapa sin dejar rastro.", "escapa", 0.40, 23),

    # BOMBING AN EMPTY ISLAND (Scenes 24..25)
    (101.49, 103.18, "Durante las dos semanas siguientes,", "semanas", 0.14, 24),
    (103.22, 108.18, "los bombarderos estadounidenses siguen lanzando toneladas de bombas sobre campamentos vacíos.", "vacíos.", 0.26, 24),
    (108.64, 111.43, "Los pilotos juran que ven disparos antiaéreos desde abajo,", "antiaéreos", 0.16, 25),
    (111.68, 112.47, "cuando en realidad", "realidad", 0.12, 25),
    (112.66, 114.91, "son las explosiones de sus propias bombas.", "propias", 0.72, 25),

    # OPERATION COTTAGE LANDING, FRIENDLY FIRE, ABNER READ & 4 DOGS (Scenes 26..34)
    (116.47, 122.13, "El 15 de agosto desembarcan por fin los 34.000 soldados aliados en medio de una niebla cerrada.", "34.000", 0.26, 26),
    (122.59, 124.61, "El verdadero enemigo es el miedo.", "miedo.", 0.28, 27),
    (125.15, 127.95, "Convencidas de que los japoneses están ocultos en las colinas,", "colinas,", 0.16, 28),
    (128.18, 132.75, "las patrullas estadounidenses y canadienses empiezan a tirotearse entre sí en la oscuridad.", "tirotearse", 0.26, 28),
    (133.23, 134.56, "Otros pisan minas.", "minas.", 0.22, 29),
    (134.93, 136.41, "Y el destructor Abner Read", "Read", 0.14, 30),
    (136.59, 139.30, "choca contra una mina flotante que le arranca la popa.", "popa.", 0.28, 30),
    (139.62, 141.86, "Cuando llegan a los búnkeres principales,", "búnkeres", 0.20, 31),
    (142.22, 145.98, "solo encuentran raciones frías y cuatro perros abandonados.", "perros", 0.34, 31),
    (146.55, 148.08, "En un combate contra nada,", "nada,", 0.16, 32),
    (148.32, 151.10, "los Aliados sufren más de 90 muertos en tierra,", "90", 0.18, 32),
    (151.38, 152.77, "70 en el destructor", "70", 0.16, 33),
    (153.00, 154.29, "y 200 heridos.", "200", 0.28, 33),
    (154.75, 159.72, "34.000 hombres disparándole a la niebla mientras el enemigo ya estaba a salvo en casa.", "niebla", 0.60, 34),

    # CLOSURE & ETHICAL DILEMMA (Scenes 35..36)
    (160.36, 162.62, "Decime qué pesa más para vos en una guerra:", "guerra:", 0.22, 35),
    (162.98, 165.31, "¿quedarte a resistir hasta el último hombre por honor,", "honor,", 0.18, 36),
    (165.59, 167.74, "o retirar tus tropas a tiempo para que vivan?", "vivan?", 0.28, 36),
    (168.20, 169.09, "Dejame tu respuesta.", None, 1.80, 36),
]

with wave.open(clean_wav, "rb") as wf:
    sr = wf.getframerate()
    raw_bytes = wf.readframes(wf.getnframes())
    samples = list(struct.unpack(f"<{len(raw_bytes)//2}h", raw_bytes))

def make_hook_naval_impact(duration_sec=0.88, sr=48000, vol=0.24):
    """Explosive naval artillery boom + high-tension radar/sonar ping at t=0.00s."""
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        # Deep naval 16-inch cannon impact at t=0.00s
        sub_env = math.exp(-4.6 * t) * (1.0 - math.exp(-170.0 * t))
        sub = 0.88 * sub_env * (math.sin(2 * math.pi * 50.0 * t) + 0.55 * math.sin(2 * math.pi * 104.0 * t))
        # Sharp radar/sonar ping at t=0.08s
        ping = 0.0
        if t >= 0.08:
            tp = t - 0.08
            ping = 0.34 * math.exp(-6.5 * tp) * math.sin(2 * math.pi * 1320.0 * tp)
        val = vol * (sub + ping)
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

def make_radar_ping(duration_sec=0.55, sr=48000, vol=0.17):
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        env = math.exp(-6.0 * t) * (1.0 - math.exp(-220.0 * t))
        val = vol * env * math.sin(2 * math.pi * 1280.0 * t)
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

def make_naval_salvo(duration_sec=0.75, sr=48000, vol=0.20):
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        env = math.exp(-4.2 * t) * (1.0 - math.exp(-120.0 * t))
        val = vol * env * (math.sin(2 * math.pi * 46.0 * t) + 0.55 * math.sin(2 * math.pi * 98.0 * t) * math.exp(-8 * t))
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

def make_rifle_crossfire(duration_sec=0.65, sr=48000, vol=0.17):
    n = int(duration_sec * sr)
    out = [0.0] * n
    for bt in [0.03, 0.15, 0.27]:
        s_i = int(bt * sr)
        for j in range(int(0.09 * sr)):
            idx = s_i + j
            if idx >= n:
                break
            tj = j / sr
            env = math.exp(-32.0 * tj) * (1.0 - math.exp(-260.0 * tj))
            shot = math.sin(2 * math.pi * 118.0 * tj) + 0.65 * math.sin(2 * math.pi * 285.0 * tj) * math.exp(-18 * tj)
            out[idx] += vol * env * shot
    return [int(max(-32767, min(32767, x * 32767))) for x in out]

def make_stamp_thud(duration_sec=0.30, sr=48000, vol=0.16):
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        env = math.exp(-20.0 * t) * (1.0 - math.exp(-220.0 * t))
        val = vol * env * (math.sin(2 * math.pi * 140.0 * t) + 0.5 * math.sin(2 * math.pi * 360.0 * t))
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

def make_aleutian_fog_tail(duration_sec, sr=48000, vol=0.22):
    """Circular acoustic tail: Arctic wind + ocean swell + radar ping + distant rifle shots looping into 00:00."""
    n = int(duration_sec * sr)
    out = [0.0] * n
    for i in range(n):
        t = i / sr
        fade = min(1.0, t / 0.15) * min(1.0, (duration_sec - t) / 0.25)
        swell = 0.65 + 0.35 * math.sin(2 * math.pi * 1.8 * t)
        wind = 0.08 * fade * swell * (math.sin(2 * math.pi * 62.0 * t) + 0.5 * math.sin(2 * math.pi * 128.0 * t + 0.5))
        out[i] += wind
        if 0.35 <= t <= 1.15:
            tp = t - 0.35
            out[i] += 0.14 * fade * math.exp(-5.5 * tp) * math.sin(2 * math.pi * 1320.0 * tp)
    for bt in [0.18, 0.72, 1.18]:
        s_i = int(bt * sr)
        for j in range(int(0.11 * sr)):
            idx = s_i + j
            if idx >= n:
                break
            tj = j / sr
            env = math.exp(-26.0 * tj) * (1.0 - math.exp(-240.0 * tj))
            shot = math.sin(2 * math.pi * 96.0 * tj) + 0.6 * math.sin(2 * math.pi * 220.0 * tj) * math.exp(-15 * tj)
            out[idx] += vol * env * shot
    return [int(max(-32767, min(32767, x * 32767))) for x in out]

final_samples = []
timeline = []
cur_time = 0.0

for idx, (r_start, r_end, text, bbox_word, pause_after, scene_id) in enumerate(SEGMENTS):
    s_idx = max(0, int(r_start * sr))
    e_idx = min(len(samples), int(r_end * sr))
    chunk_samps = samples[s_idx:e_idx]

    fade_len = min(int(0.008 * sr), len(chunk_samps) // 4)
    for fi in range(fade_len):
        chunk_samps[fi] = int(chunk_samps[fi] * (fi / fade_len))
        chunk_samps[-(fi + 1)] = int(chunk_samps[-(fi + 1)] * (fi / fade_len))

    # Diegetic foley accents
    if idx == 0:  # Opening hook impact at t=0.00s
        sfx = make_hook_naval_impact(min(0.85, len(chunk_samps) / sr), sr, vol=0.24)
        for ti in range(len(sfx)):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + sfx[ti]))
    elif idx in (1, 13, 43):  # Dead & wounded / Banzai charges in Attu / Friendly fire in darkness
        sfx = make_rifle_crossfire(min(0.65, len(chunk_samps) / sr), sr, vol=0.16)
        for ti in range(len(sfx)):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + sfx[ti]))
    elif idx in (3, 15, 22):  # 0 enemy soldiers / 5,000 in tunnels / 7 radar pips
        sfx = make_radar_ping(min(0.55, len(chunk_samps) / sr), sr, vol=0.16)
        for ti in range(len(sfx)):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + sfx[ti]))
    elif idx in (23, 36, 46):  # 1,000 heavy shells / Tons of bombs / Destroyer Abner Read hits mine
        sfx = make_naval_salvo(min(0.75, len(chunk_samps) / sr), sr, vol=0.19)
        for ti in range(len(sfx)):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + sfx[ti]))
    elif idx in (4, 18, 29):  # Document stamps
        sfx = make_stamp_thud(0.28, sr, vol=0.15)
        for ti in range(min(len(sfx), len(chunk_samps))):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + sfx[ti]))

    chunk_dur = len(chunk_samps) / sr
    start_sec = cur_time
    end_sec = cur_time + chunk_dur

    words = text.split()
    total_chars = sum(max(2, len(w)) for w in words)

    groups = []
    cur_g = []
    cur_len = 0
    for w in words:
        if cur_g and (len(cur_g) >= 5 or cur_len + 1 + len(w) > 30):
            groups.append(cur_g)
            cur_g = [w]
            cur_len = len(w)
        else:
            cur_g.append(w)
            cur_len += (1 + len(w)) if cur_len > 0 else len(w)
    if cur_g:
        groups.append(cur_g)

    w_list = []
    w_cur = start_sec
    g_idx = 0
    w_in_g = 0
    for w in words:
        if w_in_g >= len(groups[g_idx]):
            g_idx += 1
            w_in_g = 0
        w_dur = chunk_dur * (max(2, len(w)) / total_chars)
        w_list.append({
            "word": w,
            "start": round(w_cur, 3),
            "end": round(w_cur + w_dur, 3),
            "is_bbox": (bbox_word is not None and w == bbox_word),
            "group_id": g_idx
        })
        w_cur += w_dur
        w_in_g += 1

    timeline.append({
        "index": idx + 1,
        "scene_id": scene_id,
        "start": round(start_sec, 3),
        "end": round(end_sec, 3),
        "pause_after": pause_after,
        "text": text,
        "bbox_word": bbox_word,
        "words": w_list
    })

    final_samples.extend(chunk_samps)
    cur_time = end_sec

    if idx == len(SEGMENTS) - 1:
        final_samples.extend(make_aleutian_fog_tail(pause_after, sr, vol=0.22))
    else:
        final_samples.extend([0] * int(pause_after * sr))
    cur_time += pause_after

print(f"Total assembled video/audio duration (instant hook start): {cur_time:.2f}s ({int(cur_time//60)}m {cur_time%60:.2f}s)")

assembled_wav = "produccion/05_isla_kiska/audio/assembled_pre_lufs.wav"
with wave.open(assembled_wav, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(struct.pack(f"<{len(final_samples)}h", *final_samples))

timeline_path = "produccion/05_isla_kiska/timeline_chunks.json"
with open(timeline_path, "w", encoding="utf-8") as f:
    json.dump({"total_duration": round(cur_time, 3), "chunks": timeline}, f, ensure_ascii=False, indent=2)

master_wav = "produccion/05_isla_kiska/audio/audio_master_180s.wav"
subprocess.run([
    "python", ".agents/skills/historical-shorts-audio-sync/scripts/master_and_align.py",
    "--input", assembled_wav,
    "--output", master_wav,
    "--timeline", timeline_path
], check=True)
