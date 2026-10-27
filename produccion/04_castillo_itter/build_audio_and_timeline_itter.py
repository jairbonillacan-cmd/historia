import os
import json
import math
import wave
import struct
import subprocess

os.makedirs("produccion/04_castillo_itter/audio", exist_ok=True)

raw_mp3 = "produccion/04_castillo_itter/audio/voz_raw.mp3"
clean_wav = "produccion/04_castillo_itter/audio/voz_clean.wav"

# Convert raw_mp3 to 48kHz mono WAV (1.0x natural pitch & speed)
subprocess.run([
    "ffmpeg", "-y", "-i", raw_mp3,
    "-af", "highpass=f=80",
    "-ar", "48000", "-ac", "1", clean_wav
], capture_output=True, check=True)

# 51 exact acoustic segments (raw_start, raw_end, text, bbox_word, pause_after, scene_id)
# Rapid 1-to-1 scene cuts on the first 7 segments (Scenes 1..7) for an explosive, high-retention opening hook!
SEGMENTS = [
    # HOOK (Scenes 1..7)
    (0.00, 0.87, "Mirá esta escena.", "escena.", 0.18, 1),
    (1.30, 4.91, "En el portón de un castillo medieval hay un tanque estadounidense en llamas.", "llamas.", 0.22, 2),
    (5.28, 7.61, "Y adentro, disparando por las mismas ventanas,", "ventanas,", 0.16, 3),
    (7.87, 9.34, "hay soldados de Estados Unidos,", "Unidos,", 0.14, 4),
    (9.50, 10.87, "soldados del ejército alemán", "alemán", 0.14, 5),
    (11.10, 13.17, "y dos ex primeros ministros de Francia.", "Francia.", 0.22, 6),
    (13.56, 16.63, "Todos peleando del mismo lado contra un enemigo común.", "común.", 0.78, 7),

    # CONTEXT & PRISONERS (Scenes 8..16)
    (18.19, 21.99, "Ocurre en los Alpes austríacos, en mayo de 1945,", "1945,", 0.18, 8),
    (22.17, 24.67, "apenas cinco días después del suicidio de Hitler.", "Hitler.", 0.28, 9),
    (25.20, 26.91, "El lugar es el castillo de Itter,", "Itter,", 0.14, 10),
    (27.04, 31.62, "que el régimen nazi usa como prisión de máxima seguridad para rehenes franceses de alto valor.", "rehenes", 0.26, 10),
    (31.97, 35.96, "Adentro están encerrados los ex primeros ministros Paul Reynaud y Édouard Daladier,", "Reynaud", 0.22, 11),
    (36.22, 39.60, "dos comandantes en jefe y hasta el campeón de tenis Jean Borotra.", "Borotra.", 0.28, 12),
    (40.05, 44.36, "Con Alemania derrumbándose, los guardias de la prisión huyen y abandonan la fortaleza.", "abandonan", 0.26, 13),
    (44.72, 46.52, "Pero el peligro real está afuera:", "peligro", 0.24, 14),
    (46.88, 50.23, "en los bosques vecinos operan grupos fanáticos de las Waffen-SS", "Waffen-SS", 0.18, 15),
    (50.48, 54.21, "con orden de ejecutar a todos los rehenes antes de que lleguen los Aliados.", "ejecutar", 0.62, 16),

    # THE BICYCLE MISSION, MAJOR GANGL & CAPTAIN LEE (Scenes 17..25)
    (55.55, 57.13, "El callejón parece sin salida.", "salida.", 0.22, 17),
    (57.53, 61.79, "Las tropas aliadas están a kilómetros de distancia y no saben qué pasa en la montaña.", "kilómetros", 0.28, 17),
    (62.20, 66.46, "Para pedir socorro, el cocinero del castillo baja en bicicleta hacia el pueblo de Wörgl.", "bicicleta", 0.26, 18),
    (66.81, 69.05, "Allí se topa con el mayor Josef Gangl,", "Gangl,", 0.18, 19),
    (69.27, 72.07, "un comandante condecorado del ejército regular alemán", "condecorado", 0.14, 19),
    (72.13, 75.83, "que acaba de desobedecer a sus superiores para proteger a los vecinos de la zona.", "desobedecer", 0.28, 20),
    (76.19, 80.43, "Gangl sabe que sus propios 20 soldados no alcanzan para frenar a las SS.", "20", 0.26, 21),
    (80.79, 85.30, "Entonces sube a un auto con una bandera blanca y sale a buscar a los estadounidenses.", "blanca", 0.28, 22),
    (85.72, 87.41, "Y acá la historia da un vuelco:", "vuelco:", 0.22, 23),
    (87.77, 92.71, "la unidad más cercana es solo una patrulla al mando del capitán John Lee, de 27 años,", "Lee,", 0.20, 24),
    (92.96, 97.05, "que cuenta con 14 soldados estadounidenses y un único tanque Sherman.", "Sherman.", 0.36, 25),

    # THE IMPROVISED ALLIANCE AT CASTLE ITTER (Scenes 26..29)
    (97.59, 99.40, "La alianza se arma sobre la marcha.", "alianza", 0.22, 26),
    (99.73, 102.21, "Lee y Gangl suben juntos al castillo", "juntos", 0.14, 26),
    (102.26, 105.59, "con 14 estadounidenses y 10 soldados alemanes leales a Gangl.", "14", 0.26, 27),
    (105.91, 108.21, "Estacionan el tanque Sherman tapando la entrada.", "entrada.", 0.24, 28),
    (108.57, 109.87, "Al ver que son tan pocos,", "pocos,", 0.16, 29),
    (110.08, 113.46, "los ex ministros franceses piden fusiles y ocupan las almenas.", "almenas.", 0.72, 29),

    # DAWN ASSAULT, SACRIFICE OF GANGL & RESCUE (Scenes 30..37)
    (114.88, 116.47, "Al amanecer del 5 de mayo,", "mayo,", 0.16, 30),
    (116.51, 122.29, "150 efectivos de las Waffen-SS asaltan el castillo con ametralladoras y cañones antitanque.", "150", 0.26, 30),
    (122.58, 127.25, "Durante horas, estadounidenses, alemanes y franceses disparan codo con codo.", "codo.", 0.26, 31),
    (127.61, 130.18, "Un proyectil destruye el tanque Sherman en el portón.", "destruye", 0.26, 32),
    (130.51, 135.10, "En medio del tiroteo, el ex primer ministro francés Paul Reynaud queda expuesto en el muro.", "expuesto", 0.26, 33),
    (135.41, 139.45, "El mayor alemán Josef Gangl corre para empujarlo a cubierto", "Gangl", 0.16, 34),
    (139.58, 143.10, "y recibe en el pecho el disparo de un francotirador de las SS.", "pecho", 0.32, 34),
    (143.51, 145.85, "Muere en el acto salvando al líder francés.", "salvando", 0.42, 35),
    (146.40, 149.43, "A las 4 de la tarde, cuando ya casi no quedan cartuchos,", "cartuchos,", 0.20, 36),
    (149.68, 153.47, "llega una columna de refuerzos estadounidenses y barre a los atacantes.", "refuerzos", 0.38, 37),

    # CLOSURE & ETHICAL DILEMMA (Scenes 38..40)
    (153.93, 158.92, "A veces la historia junta en una misma trinchera a quienes un día antes tenían orden de matarse.", "trinchera", 0.58, 38),
    (159.87, 163.82, "Si un oficial enemigo aparece frente a vos con una bandera blanca pidiendo ayuda,", "blanca", 0.26, 39),
    (164.16, 165.95, "¿le das un arma y peleás a su lado,", "arma", 0.16, 40),
    (166.13, 167.14, "o no te arriesgás?", "arriesgás?", 0.30, 40),
    (167.59, 168.23, "Te leo abajo.", None, 1.50, 40),
]

with wave.open(clean_wav, "rb") as wf:
    sr = wf.getframerate()
    raw_bytes = wf.readframes(wf.getnframes())
    samples = list(struct.unpack(f"<{len(raw_bytes)//2}h", raw_bytes))

def make_hook_battle_impact(duration_sec=0.85, sr=48000, vol=0.22):
    """Explosive tank cannon thud + metallic tread screech layered under Clause 0 ('Mirá esta escena.')."""
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        # Deep 88mm / Sherman cannon sub-bass impact at t=0.00s
        sub_env = math.exp(-4.8 * t) * (1.0 - math.exp(-160.0 * t))
        sub = 0.85 * sub_env * (math.sin(2 * math.pi * 52.0 * t) + 0.55 * math.sin(2 * math.pi * 108.0 * t))
        # Metallic tank tread clank at t=0.06s
        clank = 0.0
        if t >= 0.05:
            tc = t - 0.05
            clank = 0.38 * math.exp(-18.0 * tc) * (math.sin(2 * math.pi * 680.0 * tc) + 0.6 * math.sin(2 * math.pi * 1140.0 * tc))
        val = vol * (sub + clank)
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

def make_rifle_bursts(duration_sec=0.65, sr=48000, vol=0.17):
    """Crisp rifle/MG bursts for window combat & SS assault."""
    n = int(duration_sec * sr)
    out = [0.0] * n
    for bt in [0.04, 0.16, 0.28]:
        s_i = int(bt * sr)
        for j in range(int(0.09 * sr)):
            idx = s_i + j
            if idx >= n:
                break
            tj = j / sr
            env = math.exp(-32.0 * tj) * (1.0 - math.exp(-260.0 * tj))
            shot = math.sin(2 * math.pi * 115.0 * tj) + 0.65 * math.sin(2 * math.pi * 290.0 * tj) * math.exp(-18 * tj)
            out[idx] += vol * env * shot
    return [int(max(-32767, min(32767, x * 32767))) for x in out]

def make_cannon_salvo(duration_sec=0.75, sr=48000, vol=0.19):
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        env = math.exp(-4.5 * t) * (1.0 - math.exp(-110.0 * t))
        val = vol * env * (math.sin(2 * math.pi * 48.0 * t) + 0.5 * math.sin(2 * math.pi * 106.0 * t) * math.exp(-8 * t))
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

def make_sniper_shot(duration_sec=0.45, sr=48000, vol=0.20):
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        env = math.exp(-16.0 * t) * (1.0 - math.exp(-300.0 * t))
        val = vol * env * (math.sin(2 * math.pi * 145.0 * t) + 0.7 * math.sin(2 * math.pi * 420.0 * t) * math.exp(-22 * t))
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

def make_alpine_tail_and_treads(duration_sec, sr=48000, vol=0.22):
    """Circular acoustic tail: Sherman tank rumble + distant rifle echoes fading into 00:00."""
    n = int(duration_sec * sr)
    out = [0.0] * n
    for i in range(n):
        t = i / sr
        fade = min(1.0, t / 0.15) * min(1.0, (duration_sec - t) / 0.25)
        chug = 0.65 + 0.35 * math.sin(2 * math.pi * 19.0 * t)
        rumble = 0.09 * fade * chug * (math.sin(2 * math.pi * 58.0 * t) + 0.5 * math.sin(2 * math.pi * 116.0 * t + 0.4))
        out[i] += rumble
    for bt in [0.22, 0.48, 0.85]:
        s_i = int(bt * sr)
        for j in range(int(0.12 * sr)):
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
    if idx == 0:
        sfx = make_hook_battle_impact(min(0.82, len(chunk_samps) / sr), sr, vol=0.22)
        for ti in range(len(sfx)):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + sfx[ti]))
    elif idx in (1, 6, 35, 37):  # Burning tank / Common enemy / 150 SS assault / 88mm destroys Sherman
        sfx = make_cannon_salvo(min(0.75, len(chunk_samps) / sr), sr, vol=0.18)
        for ti in range(len(sfx)):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + sfx[ti]))
    elif idx in (2, 36):  # Firing from windows / Fighting side by side
        sfx = make_rifle_bursts(min(0.65, len(chunk_samps) / sr), sr, vol=0.16)
        for ti in range(len(sfx)):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + sfx[ti]))
    elif idx == 40:  # Sniper shot hits Josef Gangl in the chest
        sfx = make_sniper_shot(min(0.45, len(chunk_samps) / sr), sr, vol=0.19)
        for ti in range(len(sfx)):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + sfx[ti]))
    elif idx in (16, 22):  # Execution order stamp / Disobedience dossier stamp
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
        final_samples.extend(make_alpine_tail_and_treads(pause_after, sr, vol=0.22))
    else:
        final_samples.extend([0] * int(pause_after * sr))
    cur_time += pause_after

print(f"Total assembled video/audio duration (instant hook start): {cur_time:.2f}s ({int(cur_time//60)}m {cur_time%60:.2f}s)")

assembled_wav = "produccion/04_castillo_itter/audio/assembled_pre_lufs.wav"
with wave.open(assembled_wav, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(struct.pack(f"<{len(final_samples)}h", *final_samples))

timeline_path = "produccion/04_castillo_itter/timeline_chunks.json"
with open(timeline_path, "w", encoding="utf-8") as f:
    json.dump({"total_duration": round(cur_time, 3), "chunks": timeline}, f, ensure_ascii=False, indent=2)

master_wav = "produccion/04_castillo_itter/audio/audio_master_180s.wav"
subprocess.run([
    "python", ".agents/skills/historical-shorts-audio-sync/scripts/master_and_align.py",
    "--input", assembled_wav,
    "--output", master_wav,
    "--timeline", timeline_path
], check=True)
