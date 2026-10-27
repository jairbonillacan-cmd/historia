import os
import re
import json
import math
import wave
import struct
import subprocess

os.makedirs("produccion/02_desastre_bari/audio", exist_ok=True)

TEMPO_FACTOR = 1.04
raw_mp3 = "produccion/02_desastre_bari/audio/voz_raw.mp3"
tempo_wav = "produccion/02_desastre_bari/audio/voz_tempo.wav"
subprocess.run([
    "ffmpeg", "-y", "-i", raw_mp3,
    "-af", f"atempo={TEMPO_FACTOR},highpass=f=80",
    "-ar", "48000", "-ac", "1", tempo_wav
], capture_output=True, check=True)

res = subprocess.run([
    "ffmpeg", "-i", raw_mp3, "-af", "silencedetect=noise=-35dB:d=0.18", "-f", "null", "-"
], capture_output=True, text=True, encoding="utf-8", errors="replace")

silences = []
cur_start = None
for line in res.stderr.splitlines():
    if "silence_start:" in line:
        m = re.search(r"silence_start:\s*([0-9.]+)", line)
        if m: cur_start = float(m.group(1))
    elif "silence_end:" in line and cur_start is not None:
        m_e = re.search(r"silence_end:\s*([0-9.]+)", line)
        m_d = re.search(r"silence_duration:\s*([0-9.]+)", line)
        if m_e and m_d:
            silences.append((cur_start, float(m_e.group(1)), float(m_d.group(1))))
            cur_start = None

m_dur = re.search(r"Duration:\s*(\d+):(\d+):([0-9.]+)", res.stderr)
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

# Ground-truth 45 spoken clauses mapped to 30 distinct visual scenes
CLAUSES = [
    ("2 de diciembre de 1943.", "1943.", 0.30, 1),
    ("Noche cerrada en el sur de Italia.", "Italia.", 0.22, 2),
    ("105 bombarderos alemanes atacan por sorpresa el puerto de Bari y hunden 17 barcos aliados.", "105", 0.28, 3),
    ("Pero en la bodega de uno de esos buques estadounidenses", "estadounidenses", 0.16, 4),
    ("viaja una carga tan secreta", "secreta", 0.18, 4),
    ("que ni los médicos del puerto pueden conocerla.", "médicos", 0.65, 5),
    ("Bari es el puerto clave para el avance aliado en Italia.", "clave", 0.24, 6),
    ("Esa noche hay 30 barcos amarrados con las luces encendidas para descargar munición y combustible.", "30", 0.24, 7),
    ("El mariscal británico Arthur Coningham cree que la aviación alemana ya está derrotada y que es imposible un ataque.", "imposible", 0.30, 8),
    ("A las 7:25 de la tarde, los aviones alemanes lanzan bengalas y bombardean durante 20 minutos.", "7:25", 0.26, 9),
    ("Uno de los barcos alcanzados es el buque estadounidense John Harvey.", "Harvey.", 0.24, 10),
    ("Casi nadie sabe que en sus bodegas esconde 2.000 bombas con gas mostaza,", "2.000", 0.16, 11),
    ("enviadas por Washington por si Hitler usa armas químicas primero.", "químicas", 0.58, 12),
    ("Pero había un problema mortal.", "mortal.", 0.26, 13),
    ("Cuando el John Harvey explota,", "explota,", 0.16, 14),
    ("todos sus tripulantes mueren en el acto.", "todos", 0.22, 14),
    ("Nadie queda vivo para avisar qué llevaba adentro.", "Nadie", 0.32, 15),
    ("Toneladas de gas mostaza líquido se derraman en el agua y se mezclan con el petróleo que flota en el puerto.", "petróleo", 0.24, 16),
    ("Cientos de marineros nadan entre el aceite tóxico para salvarse.", "tóxico", 0.24, 17),
    ("En los hospitales empiezan a quedar ciegos y a sufrir quemaduras terribles.", "ciegos", 0.20, 18),
    ("Peor aún:", None, 0.16, 19),
    ("los médicos creen que solo sufren de frío y petróleo.", "frío", 0.24, 19),
    ("En lugar de lavarlos y quitarles la ropa,", "lavarlos", 0.16, 20),
    ("los envuelven en mantas con los uniformes empapados en veneno.", "veneno.", 0.26, 20),
    ("Nadie esperaba que el propio secreto aliado matara a sus soldados.", "secreto", 0.45, 21),
    ("En pocos días mueren más de 600 militares aliados y cientos de civiles italianos por la nube tóxica.", "600", 0.26, 22),
    ("El mando aliado teme que si Alemania descubre la verdad use el episodio como excusa para desatar una guerra química total en Europa,", "química", 0.18, 23),
    ("y por eso ordena silenciar el caso a toda costa.", "silenciar", 0.65, 24),
    ("Entonces llega el teniente coronel médico Stewart Alexander.", "Alexander.", 0.24, 25),
    ("Al revisar a los muertos en las salas,", None, 0.15, 26),
    ("siente un leve olor a ajo y comprueba que sus glóbulos blancos desaparecieron casi por completo.", "ajo", 0.24, 26),
    ("Deduce enseguida que es gas mostaza disuelto en el agua del puerto.", "mostaza", 0.24, 27),
    ("Desobedece el silencio oficial,", "Desobedece", 0.16, 28),
    ("exige lavar de inmediato a todos los heridos y salva cientos de vidas.", "cientos", 0.28, 28),
    ("Churchill ordena borrar el gas mostaza de los archivos británicos,", "Churchill", 0.18, 29),
    ("pero el informe de Alexander tiene un giro inesperado para la medicina.", "medicina.", 0.20, 30),
    ("Al ver", None, 0.12, 31),
    ("cómo esa sustancia destruía los glóbulos blancos,", "glóbulos", 0.20, 31),
    ("los científicos descubren que una variante química podía frenar el avance de los tumores.", "tumores.", 0.26, 32),
    ("Del desastre secreto de Bari nace la primera quimioterapia contra el cáncer.", "quimioterapia", 0.30, 33),
    ("Un secreto militar mató a cientos de aliados y terminó salvando a millones de enfermos.", "millones", 0.55, 34),
    ("Ponete en el lugar del alto mando esa noche:", "mando", 0.24, 35),
    ("¿vos habrías revelado el secreto del gas para salvar a los heridos", "revelado", 0.15, 36),
    ("o lo habrías ocultado?", "ocultado?", 0.28, 36),
    ("Contámelo en los comentarios.", None, 1.65, 36),
]

assert len(raw_chunks) == len(CLAUSES), f"Expected 45 chunks, got {len(raw_chunks)}"

with wave.open(tempo_wav, "rb") as wf:
    sr = wf.getframerate()
    raw_bytes = wf.readframes(wf.getnframes())
    samples = list(struct.unpack(f"<{len(raw_bytes)//2}h", raw_bytes))

def make_air_raid_hook(duration_sec, sr=48000, vol=0.22):
    """Distant WWII air-raid siren swell + low harbor bomb rumble."""
    n = int(duration_sec * sr)
    out = [0.0] * n
    for i in range(n):
        t = i / sr
        fade = min(1.0, t / 0.25) * min(1.0, (duration_sec - t) / 0.35)
        # Rising and falling dual-tone air raid siren (380Hz -> 590Hz)
        f_siren = 380.0 + 210.0 * math.sin(math.pi * min(1.0, t / duration_sec))
        siren = 0.55 * math.sin(2 * math.pi * f_siren * t) + 0.25 * math.sin(2 * math.pi * (f_siren * 1.2) * t)
        rumble = 0.45 * (math.sin(2 * math.pi * 48.0 * t) + 0.5 * math.sin(2 * math.pi * 72.0 * t))
        out[i] = vol * fade * (0.45 * siren + 0.55 * rumble)
    return [int(max(-32767, min(32767, x * 32767))) for x in out]

def make_bomb_thud(duration_sec=0.75, sr=48000, vol=0.20):
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        env = math.exp(-4.0 * t) * (1.0 - math.exp(-95.0 * t))
        val = vol * env * (math.sin(2 * math.pi * 42.0 * t) + 0.5 * math.sin(2 * math.pi * 96.0 * t) * math.exp(-6 * t))
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

def make_stamp_hit(duration_sec=0.30, sr=48000, vol=0.14):
    n = int(duration_sec * sr)
    out = []
    for i in range(n):
        t = i / sr
        env = math.exp(-18.0 * t) * (1.0 - math.exp(-200.0 * t))
        val = vol * env * (math.sin(2 * math.pi * 380.0 * t) + 0.6 * math.sin(2 * math.pi * 760.0 * t))
        out.append(int(max(-32767, min(32767, val * 32767))))
    return out

final_samples = []
timeline = []

# Pre-Hook (0.00s -> 1.65s)
pre_hook_dur = 1.65
final_samples.extend(make_air_raid_hook(pre_hook_dur, sr, vol=0.24))
cur_time = pre_hook_dur

for idx, ((c_start, c_end, _), (text, bbox_word, pause_after, scene_id)) in enumerate(zip(raw_chunks, CLAUSES)):
    s_idx = max(0, int(c_start * sr))
    e_idx = min(len(samples), int(c_end * sr))
    chunk_samps = samples[s_idx:e_idx]

    fade_len = min(int(0.008 * sr), len(chunk_samps) // 4)
    for fi in range(fade_len):
        chunk_samps[fi] = int(chunk_samps[fi] * (fi / fade_len))
        chunk_samps[-(fi+1)] = int(chunk_samps[-(fi+1)] * (fi / fade_len))

    # Diegetic SFX
    if idx in (2, 9, 14):  # 105 bombers / 7:25 bombing / John Harvey explodes
        thud = make_bomb_thud(min(0.80, len(chunk_samps)/sr), sr, vol=0.18 if idx == 14 else 0.12)
        for ti in range(len(thud)):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + thud[ti]))
    elif idx in (11, 27, 34, 39):  # 2000 mustard bombs / silence case / Churchill erases / First chemotherapy
        st_sfx = make_stamp_hit(0.28, sr, vol=0.13)
        for ti in range(min(len(st_sfx), len(chunk_samps))):
            chunk_samps[ti] = max(-32767, min(32767, chunk_samps[ti] + st_sfx[ti]))

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

    if idx == len(CLAUSES) - 1:
        final_samples.extend(make_air_raid_hook(pause_after, sr, vol=0.22))
    else:
        final_samples.extend([0] * int(pause_after * sr))
    cur_time += pause_after

print(f"Total assembled video/audio duration: {cur_time:.2f}s ({int(cur_time//60)}m {cur_time%60:.2f}s)")

assembled_wav = "produccion/02_desastre_bari/audio/assembled_pre_lufs.wav"
with wave.open(assembled_wav, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(struct.pack(f"<{len(final_samples)}h", *final_samples))

master_wav = "produccion/02_desastre_bari/audio/audio_master_180s.wav"
subprocess.run([
    "ffmpeg", "-y", "-i", assembled_wav,
    "-af", "acompressor=threshold=-18dB:ratio=3:attack=5:release=60:makeup=3dB,loudnorm=I=-14.0:TP=-1.5:LRA=7.0",
    "-ar", "48000", "-ac", "2", master_wav
], capture_output=True, check=True)

with open("produccion/02_desastre_bari/timeline_45_chunks.json", "w", encoding="utf-8") as f:
    json.dump({"total_duration": round(cur_time, 3), "chunks": timeline}, f, ensure_ascii=False, indent=2)

print("Saved produccion/02_desastre_bari/audio/audio_master_180s.wav and timeline_45_chunks.json!")
