"""AG-15 · Cielo de Bremen (1943). Música ambiental y efectos de sonido sintetizados acá mismo.

Todo sale de osciladores y ruido generados con numpy: no hay grabaciones ni pistas de terceros,
así que no hay nada que pueda reclamar Content ID y el video se puede monetizar.

Entrada:  audio/audio_master_censurado.wav (voz ya censurada, npm run mute:bremen) + timeline_chunks.json
Salida:   audio/musica.wav, audio/sfx.wav y audio/audio_master_final.wav (voz + música con ducking + efectos, -14 LUFS)

Uso (desde la raíz del repo): python produccion/06_cielo_bremen/build_music_and_sfx_bremen.py
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("produccion/06_cielo_bremen")
VOICE = BASE / "audio/audio_master_censurado.wav"
MUSIC_OUT = BASE / "audio/musica.wav"
SFX_OUT = BASE / "audio/sfx.wav"
MIX_PRE = BASE / "audio/_mezcla_sin_normalizar.wav"
FINAL = BASE / "audio/audio_master_final.wav"
SR = 48000
TAIL = 0.6  # misma cola que la composición de Remotion

# Niveles relativos a la voz hablada (dB RMS).
MUSIC_UNDER_VOICE = -24
MUSIC_IN_GAPS = -15
SFX_LEVEL = -13
SFX_DUCK = 0.4  # los efectos también bajan ~4 dB mientras se habla

rng = np.random.default_rng(15)
timeline = json.loads((BASE / "timeline_chunks.json").read_text(encoding="utf-8"))
chunk = {c["index"]: c for c in timeline["chunks"]}


def at(i: int, field: str = "start") -> float:
    return chunk[i][field]


# ───────────────────────── utilidades ─────────────────────────

def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path)) as w:
        assert w.getframerate() == SR and w.getsampwidth() == 2
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels())


def write_wav(path: Path, x: np.ndarray) -> None:
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def tvec(dur: float) -> np.ndarray:
    return np.arange(int(dur * SR)) / SR


def band(x: np.ndarray, lo: float = 0, hi: float = SR / 2) -> np.ndarray:
    """Filtro pasabanda por FFT con bordes suaves."""
    n = len(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    X = np.fft.rfft(x)
    m = np.ones_like(f)
    if lo > 0:
        m *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** 4)
    if hi < SR / 2:
        m *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, n).astype(np.float32)


def noise(dur: float) -> np.ndarray:
    return rng.standard_normal(int(dur * SR)).astype(np.float32)


def env_ar(n: int, attack: float, release: float) -> np.ndarray:
    t = np.arange(n) / SR
    return np.minimum(1, t / max(attack, 1e-4)) * np.exp(-t / release)


def fade(n: int, fin: float, fout: float) -> np.ndarray:
    t = np.arange(n) / SR
    d = n / SR
    return np.clip(t / max(fin, 1e-4), 0, 1) * np.clip((d - t) / max(fout, 1e-4), 0, 1)


def room(x: np.ndarray, size: float = 0.35, mix: float = 0.35) -> np.ndarray:
    """Reverb liviana: ecos múltiples con decaimiento (sin dependencias)."""
    out = x.copy()
    for k, d in enumerate([0.029, 0.047, 0.071, 0.103, 0.149, 0.211, 0.297]):
        s = int(d * SR * size / 0.35)
        g = mix * 0.72 ** k
        out[s:] += g * x[: len(x) - s]
    return out


def norm_rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(x ** 2)) + 1e-9)


# ───────────────────────── música ─────────────────────────

NOTE = {n: i for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}


def hz(name: str) -> float:
    pitch, octave = name[:-1], int(name[-1])
    return 440 * 2 ** ((NOTE[pitch] + 12 * (octave + 1) - 69) / 12)


CHORDS = {
    "Dm": ["D2", "A2", "D3", "F3", "A3"],
    "Bb": ["A#1", "F2", "A#2", "D3", "F3"],
    "Gm": ["G1", "D2", "G2", "A#2", "D3"],
    "A": ["A1", "E2", "A2", "C#3", "E3"],
    "Dsus": ["D2", "A2", "D3", "E3", "A3"],
    "Dm9": ["D3", "A3", "E4", "F4", "C5"],
    "F": ["F1", "C2", "F2", "A2", "C3"],
    "C": ["C2", "G2", "C3", "E3", "G3"],
    "Fmaj7": ["F2", "C3", "E3", "A3", "C4"],
}

# (desde, acorde, brillo): la armonía sigue el arco del guion.
SECTIONS_START = [
    (0.0, ["Dm", "Bb", "Gm", "A"], 0.55),              # el dilema y el B-17 destrozado
    (at(15), ["Dsus", "Dm", "Dsus", "Bb"], 0.45),       # aparece Stigler: suspenso
    (at(26), ["Dm9", "Bb", "Dm9", "Gm"], 0.7),          # ve a los jóvenes / el recuerdo de África
    (at(33), ["Bb", "F", "C", "Dm"], 0.65),             # la escolta
    (at(36), ["Gm", "Dm", "A", "Dm"], 0.5),             # la muralla de cañones
    (at(40), ["Bb", "F", "C", "F"], 0.75),              # el saludo y el aterrizaje
    (at(42), ["Fmaj7", "C", "Dm", "Bb"], 0.85),         # hermanos
    (at(43), ["Dm", "Bb", "Dsus"], 0.6),                # el dilema final
]
CHORD_LEN = 6.0


def chord_plan(total: float) -> list[tuple[float, float, str, float]]:
    plan = []
    for k, (s, prog, bright) in enumerate(SECTIONS_START):
        e = SECTIONS_START[k + 1][0] if k + 1 < len(SECTIONS_START) else total
        t, i = s, 0
        while t < e - 0.5:
            plan.append((t, min(e, t + CHORD_LEN), prog[i % len(prog)], bright))
            t += CHORD_LEN
            i += 1
    return plan


def pad_note(f: float, dur: float, bright: float, pan: float) -> np.ndarray:
    t = tvec(dur)
    out = np.zeros((len(t), 2), np.float32)
    for det, side in [(-0.0018, 0), (0.0018, 1), (0.0, None)]:
        ph = rng.uniform(0, 2 * np.pi)
        ff = f * (1 + det)
        tone = np.sin(2 * np.pi * ff * t + ph) + bright * 0.35 * np.sin(4 * np.pi * ff * t + ph) + bright * 0.12 * np.sin(6 * np.pi * ff * t)
        trem = 0.85 + 0.15 * np.sin(2 * np.pi * rng.uniform(0.08, 0.2) * t + ph)
        v = (tone * trem).astype(np.float32)
        if side is None:
            out[:, 0] += v * (1 - pan) * 0.7
            out[:, 1] += v * pan * 0.7
        else:
            out[:, side] += v * 0.6
    return out


def felt_piano(f: float, dur: float = 3.2) -> np.ndarray:
    t = tvec(dur)
    e = env_ar(len(t), 0.006, 0.9) * fade(len(t), 0.001, 0.4)
    tone = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 3) + 0.08 * np.sin(6 * np.pi * f * t) * np.exp(-t * 6)
    return band((tone * e).astype(np.float32), 0, 2400)


def build_music(total: float) -> np.ndarray:
    n = int(total * SR)
    mus = np.zeros((n, 2), np.float32)
    xf = 2.0  # crossfade entre acordes
    for s, e, name, bright in chord_plan(total):
        dur = e - s + xf
        block = np.zeros((int(dur * SR), 2), np.float32)
        for k, note in enumerate(CHORDS[name]):
            block += pad_note(hz(note), dur, bright, pan=0.3 + 0.1 * k) * (0.8 if k == 0 else 0.5)
        block *= fade(len(block), xf, xf)[:, None]
        i = int(s * SR)
        j = min(n, i + len(block))
        mus[i:j] += block[: j - i]
    # cuerpo cálido: recorte de agudos para que no compita con la voz
    for ch in range(2):
        mus[:, ch] = band(mus[:, ch], 40, 1800)

    # Piano suave en las partes humanas (recuerdo, escolta, hermanos).
    piano = np.zeros(n, np.float32)
    for s, e, name, _ in chord_plan(total):
        if s < at(26) - 0.1:
            continue
        notes = [hz(x) * 2 for x in CHORDS[name][2:]]
        for k, tt in enumerate(np.arange(s, e - 0.5, 1.5)):
            p = felt_piano(notes[[0, 1, 2, 1][k % 4]])
            i = int(tt * SR)
            j = min(n, i + len(p))
            piano[i:j] += p[: j - i] * 0.22
    piano = room(piano, 0.5, 0.45)
    mus[:, 0] += piano * 0.9
    mus[:, 1] += piano * 1.1

    # Pulso grave muy suave en el suspenso (Stigler se acerca, frena en seco).
    pulse_from, pulse_to = at(22), at(26)
    for tt in np.arange(pulse_from, pulse_to, 1.0):
        p = band(noise(0.5), 30, 120) * env_ar(int(0.5 * SR), 0.01, 0.12) * 0.5
        p += np.sin(2 * np.pi * 52 * tvec(0.5)) * env_ar(int(0.5 * SR), 0.004, 0.14)
        i = int(tt * SR)
        mus[i:i + len(p)] += p[:, None] * 0.35

    # Entrada y salida.
    g = np.ones(n, np.float32)
    g[: int(1.5 * SR)] = np.linspace(0.3, 1, int(1.5 * SR))
    g[-int(3 * SR):] *= np.linspace(1, 0, int(3 * SR))
    return mus * g[:, None]


# ───────────────────────── efectos ─────────────────────────

def boom(dur: float = 1.6, f0: float = 55, crack: float = 0.4) -> np.ndarray:
    t = tvec(dur)
    body = band(noise(dur), 20, 180) * env_ar(len(t), 0.004, 0.35)
    thump = np.sin(2 * np.pi * (f0 * t - 18 * t ** 2)) * env_ar(len(t), 0.002, 0.18)
    hi = band(noise(dur), 900, 5000) * env_ar(len(t), 0.001, 0.03) * crack
    return room(body * 1.4 + thump + hi, 0.6, 0.4)


def flak(dist: float = 1.0) -> np.ndarray:
    """Estallido antiaéreo: chasquido seco + golpe sordo, más apagado cuanto más lejos."""
    dur = 1.4
    t = tvec(dur)
    crack = band(noise(dur), 600, 4500 / dist) * env_ar(len(t), 0.0008, 0.025)
    body = band(noise(dur), 30, 260) * env_ar(len(t), 0.003, 0.22)
    return room((crack * 0.8 + body * 1.3) / dist, 0.9, 0.5)


def engine_b17(dur: float, rough: float = 0.0) -> np.ndarray:
    """Cuatro motores radiales: zumbido grave con batido de hélice. `rough` = motores que tosen."""
    t = tvec(dur)
    f = 41 + 0.6 * np.sin(2 * np.pi * 0.07 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = sum(a * np.sin(h * ph + k) for k, (h, a) in enumerate([(1, 1), (2, 0.6), (3, 0.35), (4.02, 0.2), (6, 0.1)]))
    beat = 0.75 + 0.25 * np.sin(2 * np.pi * 3.1 * t)
    rumble = band(noise(dur), 40, 400) * 0.6
    x = (tone * 0.5 + rumble) * beat
    if rough:
        # cortes irregulares: un motor que falla
        cut = np.ones(len(t), np.float32)
        for s in rng.uniform(0, dur, int(dur * 1.2)):
            i = int(s * SR)
            cut[i:i + int(rng.uniform(0.06, 0.2) * SR)] = 1 - rough
        k = int(0.02 * SR)
        cut = np.convolve(cut, np.ones(k) / k, "same")
        x *= cut
    return band(x.astype(np.float32), 30, 900) * fade(len(t), 1.2, 1.5)


def flyby(dur: float, f_start: float = 118, f_end: float = 84, pan_from: float = 0.15, pan_to: float = 0.85) -> np.ndarray:
    """Caza de motor en línea que pasa: doppler de agudo a grave, sube y baja, cruza de lado."""
    t = tvec(dur)
    p = t / dur
    f = f_start + (f_end - f_start) / (1 + np.exp(-(p - 0.5) * 12))
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.7 * np.sin(2 * ph) + 0.45 * np.sin(3 * ph) + 0.25 * np.sin(5 * ph)
    hiss = band(noise(dur), 300, 2500) * 0.35
    loud = np.exp(-((p - 0.5) / 0.22) ** 2)
    mono = band(((tone * 0.5 + hiss) * loud).astype(np.float32), 50, 3000)
    pan = pan_from + (pan_to - pan_from) * p
    return np.stack([mono * np.sqrt(1 - pan), mono * np.sqrt(pan)], 1)


def wind(dur: float, strength: float = 1.0) -> np.ndarray:
    t = tvec(dur)
    a = band(noise(dur), 200, 900)
    b = band(noise(dur), 700, 3000)
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.18 * t + 1) * np.sin(2 * np.pi * 0.07 * t)
    x = a * (0.6 + 0.4 * lfo) + b * 0.45 * lfo
    return (x * strength * fade(len(t), 1.5, 2.0)).astype(np.float32)


def heartbeat(dur: float, bpm: float = 62) -> np.ndarray:
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    beat = 60 / bpm
    for s in np.arange(0, dur - 0.4, beat):
        for off, g in [(0, 1.0), (0.24, 0.7)]:
            th = tvec(0.25)
            h = np.sin(2 * np.pi * (48 * th - 20 * th ** 2)) * env_ar(len(th), 0.006, 0.06) * g
            i = int((s + off) * SR)
            out[i:i + len(h)] += h[: n - i]
    return out * fade(n, 0.8, 0.8)


def whoosh(dur: float = 0.9) -> np.ndarray:
    t = tvec(dur)
    x = band(noise(dur), 250, 2600) * np.exp(-((t / dur - 0.6) / 0.25) ** 2)
    return x.astype(np.float32)


def touchdown() -> np.ndarray:
    dur = 1.5
    t = tvec(dur)
    thump = np.sin(2 * np.pi * 60 * t) * env_ar(len(t), 0.003, 0.12)
    chirp = band(noise(dur), 1200, 3500) * env_ar(len(t), 0.002, 0.08) * 0.5
    roll = band(noise(dur), 60, 400) * fade(len(t), 0.05, 0.9) * 0.4
    x = np.zeros(len(t), np.float32)
    for off in [0.0, 0.35]:
        i = int(off * SR)
        x[i:] += (thump + chirp)[: len(t) - i] * (1 if off == 0 else 0.6)
    return x + roll


def frost() -> np.ndarray:
    """Crujido de escarcha: microchasquidos agudos (la morfina se congela)."""
    dur = 1.6
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    for s in rng.uniform(0, dur - 0.05, 70):
        i = int(s * SR)
        k = int(0.004 * SR)
        out[i:i + k] += rng.standard_normal(k).astype(np.float32) * rng.uniform(0.1, 0.5)
    return band(out, 3000, 12000) * fade(n, 0.2, 0.6)


def salute_bell() -> np.ndarray:
    """Campana suave y lejana para el saludo militar (transición emotiva, no un efecto literal)."""
    t = tvec(3.0)
    x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in [(587.3, 1, 1.2), (880, 0.4, 1.8), (1174.7, 0.25, 2.5)])
    return room(x.astype(np.float32), 0.8, 0.5)


def build_sfx(total: float) -> np.ndarray:
    n = int(total * SR)
    sfx = np.zeros((n, 2), np.float32)

    def put(x: np.ndarray, t0: float, gain: float = 1.0, pan: float = 0.5) -> None:
        if x.ndim == 1:
            x = np.stack([x * np.sqrt(1 - pan), x * np.sqrt(pan)], 1)
        i = int(t0 * SR)
        if i >= n:
            return
        j = min(n, i + len(x))
        sfx[i:j] += x[: j - i] * gain

    # Gancho: golpe de apertura en t=0 y un golpe seco en cada corte.
    put(boom(2.2, 50, 0.6), 0.0, 1.0)
    put(engine_b17(at(5) + 1.0), 0.0, 0.55)
    for i in (2, 3, 4):
        put(boom(1.0, 70, 0.3), at(i) - 0.04, 0.45)
    put(heartbeat(at(5) - at(4) + 0.4, 70), at(4), 0.5)

    # Mapa y la misión: whoosh de transición, motores y fuego antiaéreo sobre Bremen.
    put(whoosh(), at(5) - 0.5, 0.5)
    put(engine_b17(at(15) - at(6)), at(6), 0.5)
    put(whoosh(), at(8) - 0.5, 0.4)
    for k, s in enumerate(np.arange(at(8), at(10), 0.55)):
        put(flak(rng.uniform(1.0, 2.6)), s + rng.uniform(-0.15, 0.15), 0.7, rng.uniform(0.15, 0.85))
    put(boom(1.4, 60, 0.8), at(9) + 0.9, 0.6, 0.4)  # impacto directo
    put(boom(1.4, 60, 0.8), at(10), 0.55, 0.6)      # «un colador»

    # Nariz destrozada: viento helado; motores que tosen; escarcha.
    put(wind(at(15) - at(11) + 1.5), at(11), 0.55)
    put(engine_b17(at(15) - at(11), rough=0.85), at(11), 0.4)
    put(frost(), at(13) + 1.2, 0.5, 0.65)

    # El B-17 pasa bajo sobre el aeródromo, lejano.
    put(engine_b17(at(22) - at(16) + 1), at(16), 0.3)

    # Stigler: despegue y pasada del Bf 109, después se pone detrás de la cola.
    put(whoosh(), at(17) - 0.5, 0.35)
    put(flyby(5.5, 92, 120, 0.8, 0.4), at(22) - 0.2, 0.75)
    put(engine_b17(at(26) - at(22)), at(22), 0.35)
    put(flyby(4.0, 110, 100, 0.35, 0.5), at(23), 0.4)
    put(heartbeat(at(26) - at(24) + 0.6, 66), at(24), 0.55)

    # El recuerdo de África: solo viento muy lejano.
    put(wind(at(33) - at(26), 0.35), at(26), 0.5)

    # La escolta: dos motores juntos, ala con ala.
    put(engine_b17(at(36) - at(33) + 1), at(33), 0.45)
    put(flyby(at(36) - at(33) + 1, 100, 98, 0.65, 0.6), at(33), 0.45)

    # La muralla antiaérea de la costa: estallidos más cercanos.
    for s in np.arange(at(36) + 0.6, at(37), 0.45):
        put(flak(rng.uniform(1.0, 1.8)), s + rng.uniform(-0.1, 0.1), 0.6, rng.uniform(0.2, 0.8))
    put(heartbeat(at(39) - at(37) + 0.5, 72), at(37), 0.6)
    put(engine_b17(at(40) - at(39) + 1), at(39), 0.45)

    # El saludo y la vuelta de Stigler; mar abierto.
    put(wind(at(41) - at(40) + 1, 0.4), at(40), 0.5)
    put(salute_bell(), at(40) + 1.2, 0.25)
    put(flyby(4.5, 104, 80, 0.5, 0.05), at(40) + 2.5, 0.6)

    # Aterrizaje en Inglaterra.
    put(touchdown(), at(41) + 0.9, 0.55)

    # Cierre: un último golpe grave para la pregunta.
    put(boom(2.5, 45, 0.0), at(44) - 0.1, 0.4)
    return sfx


# ───────────────────────── mezcla ─────────────────────────

def voice_envelope(v: np.ndarray) -> np.ndarray:
    """1 donde hay voz, 0 en los silencios; con ataque rápido y salida lenta para que la música respire."""
    mono = np.abs(v.mean(1))
    hop = int(0.01 * SR)
    frames = mono[: len(mono) // hop * hop].reshape(-1, hop).max(1)
    active = (frames > 0.02).astype(np.float32)
    env = np.zeros_like(active)
    a, r = 0.5, 0.04  # por cuadro de 10 ms: ataque ~20 ms, salida ~250 ms
    for i, x in enumerate(active):
        prev = env[i - 1] if i else 0
        env[i] = prev + (x - prev) * (a if x > prev else r)
    return np.repeat(env, hop)[: len(mono)]


def main() -> None:
    voice = read_wav(VOICE)
    if voice.shape[1] == 1:
        voice = np.repeat(voice, 2, 1)
    total = len(voice) / SR + TAIL
    n = int(total * SR)
    voice = np.vstack([voice, np.zeros((n - len(voice), 2), np.float32)])

    print("Música…")
    music = build_music(total)
    print("Efectos…")
    sfx = build_sfx(total)

    env = np.concatenate([voice_envelope(voice), np.zeros(n)])[:n]
    speech = voice[env > 0.5]
    v_rms = norm_rms(speech)
    music *= v_rms / norm_rms(music)
    sfx *= v_rms * 10 ** (SFX_LEVEL / 20) / norm_rms(sfx[np.abs(sfx).max(1) > 1e-3])
    under, gaps = 10 ** (MUSIC_UNDER_VOICE / 20), 10 ** (MUSIC_IN_GAPS / 20)
    music_gain = gaps + (under - gaps) * env
    music *= music_gain[:, None]
    sfx *= (1 - SFX_DUCK * env)[:, None]

    write_wav(MUSIC_OUT, music)
    write_wav(SFX_OUT, sfx)
    mix = voice + music + sfx
    write_wav(MIX_PRE, mix / max(1.0, np.abs(mix).max() * 1.05))

    # -14 LUFS sin tocar la dinámica (loudnorm lineal en dos pasadas), pico verdadero -1.5 dBTP.
    probe = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(MIX_PRE), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    ).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    af = (
        "loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:"
        f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
        f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(MIX_PRE), "-af", af, "-ar", str(SR), "-c:a", "pcm_s16le", str(FINAL)], check=True)
    MIX_PRE.unlink()
    print(f"{total:.2f} s → {FINAL}")


if __name__ == "__main__":
    main()
