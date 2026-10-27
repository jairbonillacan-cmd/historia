import os
import re
import json
import math
import wave
import struct
import subprocess

os.makedirs('produccion/01_submarino_b59/audio', exist_ok=True)

# 1. Convert voz_raw.mp3 to 48kHz mono wav with 1.13x tempo (preserving pitch, ~169 WPM like @cdmauro2010) so total duration is ~179.2s (<180s Shorts limit)
TEMPO_FACTOR = 1.13
raw_mp3 = "produccion/01_submarino_b59/audio/voz_raw.mp3"
tempo_wav = "produccion/01_submarino_b59/audio/voz_tempo.wav"
subprocess.run([
    'ffmpeg', '-y', '-i', raw_mp3,
    '-af', f'atempo={TEMPO_FACTOR},highpass=f=80',
    '-ar', '48000', '-ac', '1', tempo_wav
], capture_output=True, check=True)

# Detect silences on raw_mp3 (verified to yield exact 84 speech chunks) and scale timestamps by 1/TEMPO_FACTOR
res = subprocess.run([
    'ffmpeg', '-i', raw_mp3, '-af', 'silencedetect=noise=-35dB:d=0.18', '-f', 'null', '-'
], capture_output=True, text=True, encoding='utf-8', errors='replace')

silences = []
cur_start = None
for line in res.stderr.splitlines():
    if 'silence_start:' in line:
        m = re.search(r'silence_start:\s*([0-9.]+)', line)
        if m: cur_start = float(m.group(1))
    elif 'silence_end:' in line and cur_start is not None:
        m_e = re.search(r'silence_end:\s*([0-9.]+)', line)
        m_d = re.search(r'silence_duration:\s*([0-9.]+)', line)
        if m_e and m_d:
            silences.append((cur_start, float(m_e.group(1)), float(m_d.group(1))))
            cur_start = None

m_dur = re.search(r'Duration:\s*(\d+):(\d+):([0-9.]+)', res.stderr)
total_dur = int(m_dur.group(1))*3600 + int(m_dur.group(2))*60 + float(m_dur.group(3))

raw_chunks = []
prev_end = 0.0
for s_start, s_end, s_dur in silences:
    if s_start > prev_end + 0.05:
        raw_chunks.append((prev_end / TEMPO_FACTOR, s_start / TEMPO_FACTOR, s_dur / TEMPO_FACTOR))
    prev_end = s_end
if total_dur > prev_end + 0.05:
    raw_chunks.append((prev_end / TEMPO_FACTOR, total_dur / TEMPO_FACTOR, 0.0))

print(f"Detected {len(raw_chunks)} chunks (scaled total_dur={total_dur/TEMPO_FACTOR:.2f}s)")

# Ground-truth 84 clauses matching the 84 chunks in exact order
CLAUSES = [
    ("27 de octubre de 1962.", "1962.", 0.35, 1),
    ("A 90 metros bajo el mar Caribe,", "90", 0.14, 2),
    ("el capitán de un submarino soviético ordena armar un torpedo nuclear.", "nuclear.", 0.32, 3),
    ("Tiene la misma potencia que la bomba de Hiroshima.", "Hiroshima.", 0.28, 4),
    ("Y para dispararlo,", None, 0.22, 4),
    ("solo hacen falta tres palabras.", "tres", 0.72, 4),
    ("Un mes antes,", None, 0.14, 5),
    ("cuatro submarinos diésel soviéticos habían salido en secreto desde el Ártico hacia Cuba.", "secreto", 0.28, 5),
    ("Uno de ellos es el B-59.", "B-59.", 0.28, 6),
    ("Adentro viajan 78 hombres", "78", 0.14, 6),
    ("y un arma que Washington no sabe que existe.", "arma", 0.30, 6),
    ("Pero cuando llegan cerca de la isla,", None, 0.14, 7),
    ("el mundo ya cambió.", None, 0.32, 7),
    ("Kennedy acaba de ordenar la cuarentena naval.", "cuarentena", 0.28, 7),
    ("Arriba los busca el portaaviones estadounidense Randolph y 11 destructores.", "11", 0.26, 8),
    ("Para no ser detectado,", None, 0.14, 8),
    ("el B-59 se sumerge.", "sumerge.", 0.55, 8),
    ("Y ahí", None, 0.15, 9),
    ("empieza el infierno.", "infierno.", 0.52, 9),
    ("Es un submarino diésel:", None, 0.18, 9),
    ("bajo el agua no puede recargar sus baterías ni renovar el aire.", "aire.", 0.26, 9),
    ("Llevan días sin contacto por radio con Moscú.", "Moscú.", 0.24, 10),
    ("No saben si la Tercera Guerra Mundial ya empezó arriba.", "Mundial", 0.30, 10),
    ("Adentro, el aire acondicionado se apaga.", None, 0.22, 11),
    ("La temperatura pasa de los 50 grados.", "50", 0.22, 11),
    ("Los marineros se desmayan en sus puestos.", "desmayan", 0.50, 11),
    ("Entonces,", None, 0.14, 12),
    ("los destructores estadounidenses empiezan a tirar pequeñas cargas de profundidad.", "cargas", 0.28, 12),
    ("Para ellos son solo señales de práctica,", "práctica,", 0.15, 12),
    ("para obligar al submarino a subir.", None, 0.28, 12),
    ("Pero adentro del casco de acero,", None, 0.15, 13),
    ("cada explosión suena como un martillazo gigante.", "martillazo", 0.28, 13),
    ("Las luces parpadean en la oscuridad.", "oscuridad.", 0.26, 13),
    ("El capitán, Valentín Savitsky, lleva días sin dormir.", "dormir.", 0.25, 14),
    ("Cree que la guerra ya estalló.", "estalló.", 0.26, 14),
    ("Y grita la orden que nadie quería escuchar:", None, 0.45, 14),
    ("«¡Los vamos a volar ahora mismo!", "volar", 0.18, 15),
    ("¡Moriremos, pero los hundiremos a todos!", "hundiremos", 0.18, 15),
    ("¡No seremos la vergüenza de la flota!»", "vergüenza", 0.65, 15),
    ("En cualquier submarino soviético normal, para lanzar el torpedo nuclear solo hacían falta dos firmas:", "dos", 0.20, 16),
    ("la del capitán", None, 0.14, 16),
    ("y la del oficial político.", None, 0.28, 16),
    ("El oficial político, Iván Maslénnikov, está de acuerdo.", None, 0.24, 17),
    ("Las dos llaves están listas.", "llaves", 0.22, 17),
    ("Si disparan,", None, 0.14, 17),
    ("el portaaviones desaparece.", "desaparece.", 0.32, 17),
    ("Y en minutos,", None, 0.14, 17),
    ("Estados Unidos respondería contra Moscú.", "Moscú.", 0.62, 17),
    ("Pero ese día,", None, 0.18, 18),
    ("en ese submarino,", None, 0.18, 18),
    ("había un tercer hombre.", "tercer", 0.45, 18),
    ("Se llamaba Vasili Arkhipov.", "Arkhipov.", 0.26, 19),
    ("Tenía 36 años y el mismo rango que el capitán,", None, 0.18, 19),
    ("pero era el jefe de Estado Mayor de toda la flotilla.", "flotilla.", 0.24, 19),
    ("Por puro azar estaba viajando en el B-59. Y por estar él a bordo,", "azar", 0.15, 20),
    ("el reglamento exigía que los tres votaran que sí.", "tres", 0.42, 20),
    ("Además,", None, 0.14, 21),
    ("Arkhipov tenía algo que el capitán no tenía:", None, 0.28, 21),
    ("un año antes había sobrevivido a una fuga radiactiva en el submarino K-19.", "radiactiva", 0.30, 21),
    ("Había visto morir a sus propios marineros por radiación.", "radiación.", 0.28, 21),
    ("Sabía exactamente lo que significaba abrir esa puerta.", "puerta.", 0.68, 21),
    ("Así que dijo que no.", "no.", 0.85, 22),
    ("En el puente de mando estalló una discusión feroz.", "feroz.", 0.28, 23),
    ("Arkhipov le señaló un detalle clave al capitán:", None, 0.25, 23),
    ("las cargas explotaban a los costados, no encima del casco.", "costados,", 0.28, 23),
    ("Si Estados Unidos quisiera hundirlos,", None, 0.14, 24),
    ("ya los habría partido al medio.", "medio.", 0.25, 24),
    ("Eran señales para que salieran.", "señales", 0.28, 24),
    ("Lo convenció de desarmar el torpedo y subir a la superficie.", "superficie.", 0.55, 24),
    ("Cuando regresaron a la Unión Soviética,", None, 0.18, 25),
    ("nadie los recibió como héroes.", "héroes.", 0.28, 25),
    ("El ministro de Defensa les dijo que habría sido mejor que se hundieran con su barco.", "hundieran", 0.35, 25),
    ("El mundo no supo lo que había pasado en ese submarino hasta 40 años después,", "40", 0.16, 26),
    ("cuando se desclasificaron los archivos en el año 2002.", "2002.", 0.62, 26),
    ("90 metros bajo el agua,", None, 0.18, 27),
    ("50 grados de calor y tres llaves.", "llaves.", 0.28, 27),
    ("Dos hombres votaron por el fin del mundo.", "mundo.", 0.26, 27),
    ("Uno solo", None, 0.14, 27),
    ("pidió esperar.", "esperar.", 0.58, 27),
    ("Sin radio,", None, 0.14, 28),
    ("bajo fuego y a punto de quedarte sin oxígeno,", "oxígeno,", 0.32, 28),
    ("¿vos habrías girado la llave", "llave", 0.16, 28),
    ("o habrías salido a la superficie?", "superficie?", 0.36, 28),
    ("Contámelo en los comentarios.", None, 1.85, 28)
]

assert len(raw_chunks) == len(CLAUSES), f"Expected 84 chunks, got {len(raw_chunks)}"

with wave.open(tempo_wav, 'rb') as wf:
    sr = wf.getframerate()
    raw_bytes = wf.readframes(wf.getnframes())
    samples = list(struct.unpack(f"<{len(raw_bytes)//2}h", raw_bytes))

def make_sonar_ping(duration_sec, sr=48000, freq=1320.0, vol=0.26, with_rumble=True):
    n = int(duration_sec * sr)
    out = [0.0] * n
    ping_times = [0.12, 1.05] if duration_sec >= 1.5 else [0.20]
    for pt in ping_times:
        start_idx = int(pt * sr)
        for i in range(int(0.75 * sr)):
            idx = start_idx + i
            if idx >= n: break
            t = i / sr
            env = math.exp(-5.5 * t) * (1.0 - math.exp(-120.0 * t))
            sig = math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(2 * math.pi * (freq * 1.5) * t) * math.exp(-10 * t)
            out[idx] += vol * env * sig
    if with_rumble:
        for i in range(n):
            t = i / sr
            fade = min(1.0, t / 0.2) * min(1.0, (duration_sec - t) / 0.3)
            rumble = 0.065 * fade * (math.sin(2 * math.pi * 52.0 * t) + 0.6 * math.sin(2 * math.pi * 78.0 * t + 0.5))
            out[i] += rumble
    return [int(max(-32767, min(32767, x * 32767))) for x in out]

def make_depth_charge_thud(duration_sec, sr=48000, vol=0.22):
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        env = math.exp(-4.2 * t) * (1.0 - math.exp(-90.0 * t))
        val = vol * env * (math.sin(2 * math.pi * 44.0 * t) + 0.45 * math.sin(2 * math.pi * 108.0 * t) * math.exp(-7 * t))
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

def make_metallic_lock(duration_sec=0.35, sr=48000, vol=0.14):
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        env = math.exp(-18.0 * t) * (1.0 - math.exp(-200.0 * t))
        val = vol * env * (math.sin(2 * math.pi * 420.0 * t) + 0.6 * math.sin(2 * math.pi * 880.0 * t))
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

final_samples = []
timeline = []

# Pre-Hook (0.00s -> 1.85s)
pre_hook_dur = 1.85
final_samples.extend(make_sonar_ping(pre_hook_dur, sr, vol=0.28, with_rumble=True))
cur_time = pre_hook_dur

for idx, ((c_start, c_end, _), (text, bbox_word, pause_after, scene_id)) in enumerate(zip(raw_chunks, CLAUSES)):
    s_idx = max(0, int(c_start * sr))
    e_idx = min(len(samples), int(c_end * sr))
    chunk_samps = samples[s_idx:e_idx]
    
    fade_len = min(int(0.008 * sr), len(chunk_samps) // 4)
    for fi in range(fade_len):
        chunk_samps[fi] = int(chunk_samps[fi] * (fi / fade_len))
        chunk_samps[-(fi+1)] = int(chunk_samps[-(fi+1)] * (fi / fade_len))
        
    # Subtle diegetic SFX on key moments
    if idx in (27, 31, 32): # Depth charges & hull blows
        thud = make_depth_charge_thud(min(0.85, len(chunk_samps)/sr), sr, vol=0.20 if idx==31 else 0.13)
        for ti in range(len(thud)):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + thud[ti]))
    elif idx in (2, 43, 61): # Torpedo arming / 2 keys ready / Arkhipov says NO
        lock_sfx = make_metallic_lock(0.30, sr, vol=0.14)
        offset = max(0, len(chunk_samps) - len(lock_sfx)) if idx == 61 else 0
        for ti in range(min(len(lock_sfx), len(chunk_samps) - offset)):
            chunk_samps[offset + ti] = max(-32767, min(32767, chunk_samps[offset + ti] + lock_sfx[ti]))

    chunk_dur = len(chunk_samps) / sr
    start_sec = cur_time
    end_sec = cur_time + chunk_dur
    
    # Split long clauses into short 2-to-5 word display groups (@cdmauro2010 progressive short subtitles)
    words = text.split()
    total_chars = sum(max(2, len(w)) for w in words)
    
    # Group words into sub-phrases of max ~4-5 words (or max 26 chars per line, max 2 short lines)
    groups = []
    cur_g = []
    cur_len = 0
    for w in words:
        if cur_g and (len(cur_g) >= 5 or cur_len + 1 + len(w) > 32):
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
    
    if idx == len(CLAUSES) - 1:
        final_samples.extend(make_sonar_ping(pause_after, sr, vol=0.28, with_rumble=True))
    else:
        final_samples.extend([0] * int(pause_after * sr))
    cur_time += pause_after

print(f"Total assembled video/audio duration: {cur_time:.2f}s ({int(cur_time//60)}m {cur_time%60:.2f}s)")

assembled_wav = "produccion/01_submarino_b59/audio/assembled_pre_lufs.wav"
with wave.open(assembled_wav, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(struct.pack(f"<{len(final_samples)}h", *final_samples))

master_wav = "produccion/01_submarino_b59/audio/audio_master_180s.wav"
subprocess.run([
    'ffmpeg', '-y', '-i', assembled_wav,
    '-af', 'acompressor=threshold=-18dB:ratio=3:attack=5:release=60:makeup=3dB,loudnorm=I=-21.0:TP=-3.0:LRA=3.0',
    '-ar', '48000', '-ac', '2', master_wav
], capture_output=True, check=True)

with open("produccion/01_submarino_b59/timeline_84_chunks.json", "w", encoding="utf-8") as f:
    json.dump({"total_duration": round(cur_time, 3), "chunks": timeline}, f, ensure_ascii=False, indent=2)

print("Updated audio_master_180s.wav and timeline_84_chunks.json with short progressive subtitle groups!")
