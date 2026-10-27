import os
import json
import math
import wave
import struct
import subprocess

os.makedirs("produccion/03_operacion_tigre/audio", exist_ok=True)

raw_mp3 = "produccion/03_operacion_tigre/audio/voz_raw.mp3"
clean_wav = "produccion/03_operacion_tigre/audio/voz_clean.wav"

# Convert raw_mp3 to 48kHz mono WAV (1.0x natural pitch & speed)
subprocess.run([
    "ffmpeg", "-y", "-i", raw_mp3,
    "-af", "highpass=f=80",
    "-ar", "48000", "-ac", "1", clean_wav
], capture_output=True, check=True)

# 53 exact acoustic segments (raw_start, raw_end, text, bbox_word, pause_after, scene_id)
# Note: First 6 segments have rapid 1-to-1 scene cuts (Scenes 1..6) for maximum hook retention!
SEGMENTS = [
    (0.04, 2.80, "28 de abril de 1944.", "1944.", 0.24, 1),
    (3.22, 5.97, "Faltan cinco semanas para el desembarco de Normandía.", "cinco", 0.22, 2),
    (6.37, 8.04, "En una playa del sur de Inglaterra,", "Inglaterra,", 0.12, 3),
    (8.21, 12.28, "casi 750 soldados estadounidenses mueren en cuestión de horas.", "750", 0.28, 4),
    (12.71, 13.62, "No están en Francia.", "Francia.", 0.22, 5),
    (14.00, 15.99, "Están en un simple ensayo secreto.", "secreto.", 0.75, 6),

    (17.63, 22.55, "El general Dwight Eisenhower quiere que el ensayo del Día D sea igual al combate verdadero.", "Eisenhower", 0.26, 7),
    (22.87, 27.77, "Eligen la playa inglesa de Slapton Sands porque es idéntica a la playa de Utah, en Normandía.", "idéntica", 0.26, 8),
    (28.07, 31.77, "Evacuan a 3.000 vecinos y reúnen a 30.000 soldados.", "30.000", 0.24, 9),
    (32.01, 37.20, "El plan incluye que un crucero dispare munición real sobre la arena minutos antes del desembarco,", "real", 0.14, 10),
    (37.32, 40.45, "para que los reclutas se acostumbren al ruido de las explosiones.", "explosiones.", 0.60, 11),

    (41.39, 43.27, "Pero había un problema tras otro.", "problema", 0.30, 12),
    (43.65, 48.61, "El 27 de abril, el almirante que dirige la maniobra retrasa el horario 60 minutos,", "60", 0.22, 13),
    (48.88, 54.11, "pero parte de las lanchas no recibe el aviso y desembarca a la hora original bajo el fuego aliado.", "aliado.", 0.35, 14),
    (54.50, 57.21, "Peor aún es lo que ocurre esa madrugada en el mar.", "madrugada", 0.28, 15),
    (57.51, 60.89, "Un convoy de ocho grandes buques cargados de soldados y tanques", "ocho", 0.14, 16),
    (61.08, 62.55, "navega por la bahía de Lyme.", "Lyme.", 0.24, 16),
    (62.80, 65.44, "Deberían ir protegidos por dos escoltas británicos,", "dos", 0.16, 17),
    (65.65, 67.60, "pero uno volvió a puerto por avería.", "avería.", 0.26, 17),
    (67.90, 71.32, "En la oscuridad aparecen nueve lanchas torpederas alemanas.", "nueve", 0.26, 18),
    (71.60, 74.14, "El barco británico las detecta y avisa por radio.", "radio.", 0.24, 19),
    (74.39, 79.31, "Nadie esperaba que en las órdenes estadounidenses hubiera un error de imprenta en la frecuencia:", "error", 0.26, 20),
    (79.63, 81.29, "nunca escuchan la alerta.", "alerta.", 0.48, 21),

    (81.84, 84.09, "Durante dos largas horas en la oscuridad,", "dos", 0.18, 22),
    (84.33, 88.11, "las lanchas rápidas alemanas atacan el convoy casi sin oposición.", "atacan", 0.26, 22),
    (88.41, 91.40, "Dos transportes gigantes llenos de tropas se incendian", "incendian", 0.16, 23),
    (91.58, 93.72, "y un tercero queda gravemente averiado.", "averiado.", 0.24, 23),
    (93.97, 98.61, "Cientos de soldados saltan al agua helada del canal cargados con mochilas pesadas", "helada", 0.14, 24),
    (98.69, 101.63, "y con los cinturones salvavidas mal colocados en la cintura,", "cintura,", 0.18, 25),
    (101.85, 104.02, "lo que los hunde de cabeza bajo las olas.", "hunde", 0.72, 25),

    (105.22, 105.91, "Al amanecer,", None, 0.16, 26),
    (106.16, 107.31, "el saldo es devastador:", "devastador:", 0.24, 26),
    (107.70, 111.88, "749 soldados y marineros estadounidenses muertos.", "749", 0.30, 26),
    (112.21, 116.77, "Es casi cuatro veces más que los 197 que morirán semanas más tarde", "197", 0.16, 27),
    (116.91, 119.09, "en el desembarco real de la playa de Utah.", "Utah.", 0.30, 28),
    (119.38, 122.37, "Pero para Eisenhower hay una pesadilla todavía mayor.", "pesadilla", 0.44, 29),
    (122.93, 124.71, "Entre los desaparecidos en el mar", "desaparecidos", 0.18, 30),
    (124.93, 127.66, "hay 10 oficiales con nivel de acceso BIGOT:", "BIGOT:", 0.26, 30),
    (128.00, 131.70, "hombres que conocen la fecha exacta y las playas secretas del Día D.", "secretas", 0.30, 31),
    (132.08, 134.91, "Si los alemanes capturaron vivo a uno solo de ellos,", "vivo", 0.22, 32),
    (135.19, 136.36, "Hitler ya conoce", "Hitler", 0.16, 32),
    (136.54, 137.87, "todo el plan de Normandía.", "Normandía.", 0.24, 32),
    (138.05, 141.75, "Eisenhower está a punto de cancelar la invasión", "cancelar", 0.14, 33),
    (141.80, 144.43, "hasta que los buzos recuperan e identifican los 10 cadáveres en el agua.", "10", 0.28, 33),
    (144.71, 145.89, "Para proteger el secreto,", "secreto,", 0.18, 34),
    (146.11, 150.26, "prohíben a los sobrevivientes hablar del desastre bajo amenaza de consejo de guerra.", "guerra.", 0.28, 34),

    (150.57, 152.83, "Murieron más hombres practicando en Inglaterra", "Inglaterra", 0.16, 35),
    (153.02, 154.81, "que tomando la playa real en Francia.", "Francia.", 0.55, 35),
    (155.41, 157.40, "Ponete en el lugar de Eisenhower esa mañana.", "Eisenhower", 0.24, 36),
    (157.75, 159.99, "Si faltaba uno solo de esos 10 cuerpos,", "10", 0.28, 36),
    (160.36, 162.02, "¿vos habrías cancelado el Día D", "cancelado", 0.16, 37),
    (162.17, 163.40, "o habrías atacado igual?", "atacado", 0.32, 37),
    (163.86, 165.25, "Contámelo en los comentarios.", None, 1.45, 37),
]

with wave.open(clean_wav, "rb") as wf:
    sr = wf.getframerate()
    raw_bytes = wf.readframes(wf.getnframes())
    samples = list(struct.unpack(f"<{len(raw_bytes)//2}h", raw_bytes))

def make_hook_impact_and_sonar(duration_sec=1.20, sr=48000, vol=0.22):
    """High-impact opening sonar ping + deep naval torpedo thud layered underneath t=0.00s narration."""
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        # Crisp naval sonar ping at t=0.02s (1320 Hz resonant decay)
        ping = 0.0
        if t >= 0.01:
            tp = t - 0.01
            ping = 0.45 * math.exp(-7.5 * tp) * math.sin(2 * math.pi * 1320.0 * tp)
        # Deep cinematic sub-bass naval impact at t=0.00s
        sub_env = math.exp(-4.2 * t) * (1.0 - math.exp(-140.0 * t))
        sub = 0.85 * sub_env * (math.sin(2 * math.pi * 48.0 * t) + 0.5 * math.sin(2 * math.pi * 98.0 * t))
        val = vol * (ping + sub)
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

def make_naval_engine_and_bursts(duration_sec, sr=48000, vol=0.24, with_bursts=True):
    n = int(duration_sec * sr)
    out = [0.0] * n
    for i in range(n):
        t = i / sr
        fade = min(1.0, t / 0.15) * min(1.0, (duration_sec - t) / 0.25)
        chug = 0.65 + 0.35 * math.sin(2 * math.pi * 17.5 * t)
        rumble = 0.08 * fade * chug * (math.sin(2 * math.pi * 56.0 * t) + 0.55 * math.sin(2 * math.pi * 112.0 * t + 0.4))
        out[i] += rumble
    if with_bursts:
        burst_times = [0.20, 0.42, 0.64, 0.98] if duration_sec >= 1.2 else [0.22, 0.45]
        for bt in burst_times:
            s_i = int(bt * sr)
            for j in range(int(0.14 * sr)):
                idx = s_i + j
                if idx >= n:
                    break
                tj = j / sr
                env = math.exp(-26.0 * tj) * (1.0 - math.exp(-240.0 * tj))
                shot = math.sin(2 * math.pi * 92.0 * tj) + 0.6 * math.sin(2 * math.pi * 215.0 * tj) * math.exp(-15 * tj)
                out[idx] += vol * env * shot
    return [int(max(-32767, min(32767, x * 32767))) for x in out]

def make_cannon_salvo(duration_sec=0.75, sr=48000, vol=0.19):
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        env = math.exp(-4.5 * t) * (1.0 - math.exp(-100.0 * t))
        val = vol * env * (math.sin(2 * math.pi * 46.0 * t) + 0.5 * math.sin(2 * math.pi * 104.0 * t) * math.exp(-8 * t))
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

def make_stamp_thud(duration_sec=0.30, sr=48000, vol=0.16):
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        env = math.exp(-20.0 * t) * (1.0 - math.exp(-220.0 * t))
        val = vol * env * (math.sin(2 * math.pi * 140.0 * t) + 0.5 * math.sin(2 * math.pi * 360.0 * t))
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

final_samples = []
timeline = []

# IMMEDIATE NARRATION START AT t = 0.00s!
cur_time = 0.0

for idx, (r_start, r_end, text, bbox_word, pause_after, scene_id) in enumerate(SEGMENTS):
    s_idx = max(0, int(r_start * sr))
    e_idx = min(len(samples), int(r_end * sr))
    chunk_samps = samples[s_idx:e_idx]

    # Smooth 8ms micro-fade at edges of each vocal clause
    fade_len = min(int(0.008 * sr), len(chunk_samps) // 4)
    for fi in range(fade_len):
        chunk_samps[fi] = int(chunk_samps[fi] * (fi / fade_len))
        chunk_samps[-(fi + 1)] = int(chunk_samps[-(fi + 1)] * (fi / fade_len))

    # Immediate sonic impact on Clause 0 (t=0.00s) layered cleanly under the narrator's voice
    if idx == 0:
        hook_sfx = make_hook_impact_and_sonar(min(1.20, len(chunk_samps) / sr), sr, vol=0.20)
        for ti in range(len(hook_sfx)):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + hook_sfx[ti]))
    elif idx in (3, 9, 13, 24, 25):  # 750 deaths / HMS Hawkins live fire / friendly fire / S-Boot torpedo attack / burning LSTs
        salvo = make_cannon_salvo(min(0.80, len(chunk_samps) / sr), sr, vol=0.18 if idx in (3, 13, 25) else 0.14)
        for ti in range(len(salvo)):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + salvo[ti]))
    elif idx in (5, 21, 37, 45):  # Ensayo secreto stamp / Misprinted frequency / BIGOT stamp / Court-martial gag order
        st_sfx = make_stamp_thud(0.28, sr, vol=0.15)
        for ti in range(min(len(st_sfx), len(chunk_samps))):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + st_sfx[ti]))

    chunk_dur = len(chunk_samps) / sr
    start_sec = cur_time
    end_sec = cur_time + chunk_dur

    # Split clauses into short 3-to-5 word display groups for Top Dynamic Subtitle
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
        # Circular Acoustic Tail at end of video
        final_samples.extend(make_naval_engine_and_bursts(pause_after, sr, vol=0.24, with_bursts=True))
    else:
        # Surgical digital silence (-inf dB) between clauses
        final_samples.extend([0] * int(pause_after * sr))
    cur_time += pause_after

print(f"Total assembled video/audio duration (instant narration start): {cur_time:.2f}s ({int(cur_time//60)}m {cur_time%60:.2f}s)")

assembled_wav = "produccion/03_operacion_tigre/audio/assembled_pre_lufs.wav"
with wave.open(assembled_wav, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(struct.pack(f"<{len(final_samples)}h", *final_samples))

timeline_path = "produccion/03_operacion_tigre/timeline_chunks.json"
with open(timeline_path, "w", encoding="utf-8") as f:
    json.dump({"total_duration": round(cur_time, 3), "chunks": timeline}, f, ensure_ascii=False, indent=2)

master_wav = "produccion/03_operacion_tigre/audio/audio_master_180s.wav"
subprocess.run([
    "python", ".agents/skills/historical-shorts-audio-sync/scripts/master_and_align.py",
    "--input", assembled_wav,
    "--output", master_wav,
    "--timeline", timeline_path
], check=True)
