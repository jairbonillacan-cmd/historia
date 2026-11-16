"""AG-17 · Messines (1917). Música ambiental y efectos de sonido sintetizados acá mismo.

Todo sale de osciladores y ruido generados con numpy: no hay grabaciones ni pistas de terceros,
así que no hay nada que pueda reclamar Content ID y el video se puede monetizar.

Entrada:  audio/audio_master_censurado.wav (voz ya censurada, npm run mute:messines) + timeline_chunks.json
Salida:   audio/musica.wav, audio/sfx.wav y audio/audio_master_final.wav (voz + música con ducking + efectos, -14 LUFS)

Uso (desde la raíz del repo): python produccion/08_messines/build_music_and_sfx_messines.py
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("produccion/08_messines")
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

rng = np.random.default_rng(17)
timeline = json.loads((BASE / "timeline_chunks.json").read_text(encoding="utf-8"))
chunk = {c["index"]: c for c in timeline["chunks"]}


def at(i: int, field: str = "start") -> float:
    return chunk[i][field]


def word(i: int, k: int) -> float:
    return chunk[i]["words"][k]["start"]


BLAST = at(29, "end") + 0.45  # la gran voladura cae en el silencio antes de «En 20 segundos»


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
    "Am": ["A1", "E2", "A2", "C3", "E3"],
    "Ebdim": ["D#2", "A2", "D#3", "F#3", "A3"],
}

# (desde, acorde, brillo): la armonía sigue el arco del guion.
SECTIONS_START = [
    (0.0, ["Dm", "Bb", "Gm", "A"], 0.55),              # la frase de Plumer y medio millón de kilos bajo tierra
    (at(5), ["Dm", "Dsus", "Bb", "A"], 0.45),           # Bélgica 1917: la colina imposible
    (at(12), ["Dm", "C", "Bb", "A"], 0.5),              # los mineros empiezan a cavar
    (at(15), ["Dsus", "Dm", "Dsus", "Bb"], 0.38),       # la guerra a ciegas bajo el barro
    (at(21), ["Gm", "Ebdim", "Dm", "A"], 0.5),          # descubren una cámara / quedan 20 intactas
    (at(27), ["Dsus", "Am"], 0.3),                      # 3:10, calma tensa
    (BLAST, ["Dm", "Bb", "Gm", "A"], 0.7),              # 19 volcanes
    (at(37), ["Fmaj7", "C", "Dm", "Bb"], 0.6),          # la mina olvidada
    (at(39), ["Dm", "Bb", "Dsus"], 0.6),                # el dilema final
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
        if s < at(37) - 0.1:
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

    # Pulso grave muy suave bajo tierra y en la cuenta regresiva de las cámaras.
    beats = list(np.arange(at(15), at(21), 1.1)) + list(np.arange(at(24), at(27), 0.85))
    for tt in beats:
        p = band(noise(0.5), 30, 120) * env_ar(int(0.5 * SR), 0.01, 0.12) * 0.5
        p += np.sin(2 * np.pi * 52 * tvec(0.5)) * env_ar(int(0.5 * SR), 0.004, 0.14)
        i = int(tt * SR)
        mus[i:i + len(p)] += p[:, None] * 0.35

    # Entrada y salida; la música casi desaparece justo antes de la voladura para que el golpe pegue.
    g = np.ones(n, np.float32)
    dip = np.interp(np.arange(n) / SR, [at(29, "end") - 0.8, BLAST - 0.05, BLAST + 0.6, BLAST + 2.5], [1, 0.08, 0.08, 1]).astype(np.float32)
    g *= dip
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


def muffled(dur: float = 1.4, f0: float = 48) -> np.ndarray:
    """Explosión bajo tierra: sin chasquido, todo grave y apagado por la arcilla."""
    t = tvec(dur)
    body = band(noise(dur), 18, 110) * env_ar(len(t), 0.02, 0.4)
    thump = np.sin(2 * np.pi * (f0 * t - 10 * t ** 2)) * env_ar(len(t), 0.01, 0.3)
    return room((body * 1.5 + thump).astype(np.float32), 0.7, 0.3)


def artillery(dist: float = 2.0) -> np.ndarray:
    """Cañonazo lejano: retumbo sordo con cola larga."""
    dur = 2.2
    t = tvec(dur)
    body = band(noise(dur), 25, 300 / dist) * env_ar(len(t), 0.01, 0.5)
    thump = np.sin(2 * np.pi * 50 * t) * env_ar(len(t), 0.005, 0.2)
    return room(((body * 1.2 + thump * 0.7) / dist).astype(np.float32), 1.0, 0.5)


def mega_blast(dur: float = 14.0) -> np.ndarray:
    """Las 19 minas: golpe subsónico enorme, crujido de tierra, retumbo que tarda en apagarse."""
    t = tvec(dur)
    sub = np.sin(2 * np.pi * (34 * t - 4 * t ** 2 / dur)) * env_ar(len(t), 0.01, 2.2)
    body = band(noise(dur), 18, 160) * env_ar(len(t), 0.03, 3.0) * 1.8
    crack = band(noise(dur), 700, 6000) * env_ar(len(t), 0.002, 0.12) * 0.7
    roar = band(noise(dur), 60, 900) * env_ar(len(t), 0.25, 1.6) * 0.8
    x = sub * 1.4 + body + crack + roar
    # réplicas: las otras minas, una tras otra en los primeros segundos
    for off in rng.uniform(0.15, 4.0, 9):
        i = int(off * SR)
        b = boom(1.8, 40 + rng.uniform(0, 20), 0.2) * rng.uniform(0.3, 0.7)
        x[i:i + len(b)] += b[: len(x) - i]
    return room(x.astype(np.float32), 1.2, 0.45) * fade(len(t), 0.001, 4.0)


def debris(dur: float = 5.0) -> np.ndarray:
    """Tierra y piedras que vuelven a caer."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    for s in np.sort(rng.uniform(0.3, dur - 0.2, 160)):
        k = int(rng.uniform(0.01, 0.04) * SR)
        i = int(s * SR)
        hit = band(rng.standard_normal(k).astype(np.float32), 200, 3000) * env_ar(k, 0.001, 0.01)
        out[i:i + k] += hit[: n - i] * rng.uniform(0.2, 1.0)
    return out * fade(n, 0.5, 1.5)


def pick(wet: float = 1.0) -> np.ndarray:
    """Golpe de pico contra la arcilla: clic seco + golpe blando."""
    dur = 0.5
    t = tvec(dur)
    click = band(noise(dur), 1500, 6000) * env_ar(len(t), 0.0005, 0.008) * 0.6
    thud = band(noise(dur), 80, 600) * env_ar(len(t), 0.001, 0.05)
    tone = np.sin(2 * np.pi * 180 * t) * env_ar(len(t), 0.001, 0.03) * 0.5
    return room((click + thud + tone).astype(np.float32), 0.25, 0.3 * wet)


def knock() -> np.ndarray:
    """Golpe del pico enemigo oído a través de la tierra: sordo, sin agudos."""
    return band(pick(0.5), 60, 350) * 1.6


def drip() -> np.ndarray:
    t = tvec(0.6)
    f = 1400 + 900 * np.exp(-t * 40)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ar(len(t), 0.001, 0.05)
    return room(x.astype(np.float32), 0.4, 0.5)


def tick() -> np.ndarray:
    t = tvec(0.12)
    return (band(noise(0.12), 2000, 8000) * env_ar(len(t), 0.0005, 0.006) + np.sin(2 * np.pi * 2400 * t) * env_ar(len(t), 0.0005, 0.01) * 0.4).astype(np.float32)


def lever() -> np.ndarray:
    """Palanca del detonador: chasquido metálico y traba."""
    dur = 0.8
    t = tvec(dur)
    x = np.zeros(len(t), np.float32)
    for off, g in [(0.0, 0.6), (0.09, 1.0)]:
        i = int(off * SR)
        k = len(t) - i
        tt = t[:k]
        ring = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * d) for f, d in [(820, 40), (1630, 55), (2410, 70)])
        x[i:] += (ring + band(noise(dur), 1000, 6000)[:k] * np.exp(-tt * 120)) * g
    return room(x, 0.3, 0.3)


def thunder(dur: float = 5.0) -> np.ndarray:
    t = tvec(dur)
    crack = band(noise(dur), 400, 7000) * env_ar(len(t), 0.001, 0.08)
    roll = band(noise(dur), 30, 400) * (env_ar(len(t), 0.15, 1.4) * (0.7 + 0.3 * np.sin(2 * np.pi * 2.3 * t)))
    return room((crack * 0.9 + roll * 1.5).astype(np.float32), 1.0, 0.5) * fade(len(t), 0.001, 1.5)


def rumble(dur: float) -> np.ndarray:
    """Vibración subterránea grave."""
    t = tvec(dur)
    x = band(noise(dur), 20, 90) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.3 * t)) + np.sin(2 * np.pi * 31 * t) * 0.3
    return (x * fade(len(t), 0.4, 1.0)).astype(np.float32)


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


def wind(dur: float, strength: float = 1.0) -> np.ndarray:
    t = tvec(dur)
    a = band(noise(dur), 200, 900)
    b = band(noise(dur), 700, 3000)
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.18 * t + 1) * np.sin(2 * np.pi * 0.07 * t)
    x = a * (0.6 + 0.4 * lfo) + b * 0.45 * lfo
    return (x * strength * fade(len(t), 1.5, 2.0)).astype(np.float32)


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

    # Gancho: latido subterráneo y golpe en t=0, golpes secos en cada corte.
    put(rumble(at(5)), 0.0, 0.6)
    put(muffled(2.4, 40), 0.0, 1.0)
    put(heartbeat(at(4) - 0.2, 64), 0.2, 0.45)
    for t0 in (at(2), word(2, 6), at(3), word(3, 4), at(4), word(4, 12)):
        put(boom(1.0, 70, 0.3), t0 - 0.04, 0.4)
    put(muffled(1.8, 44), word(4, 20), 0.7)  # «estallar»

    # Bélgica 1917: whoosh al mapa y cañoneo lejano desde la colina.
    put(whoosh(), at(5) - 0.5, 0.5)
    for s in np.arange(word(7, 8), at(9), 0.9):
        put(artillery(rng.uniform(1.5, 3.0)), s + rng.uniform(-0.2, 0.2), 0.7, rng.uniform(0.2, 0.8))
    put(boom(1.4, 60, 0.6), word(8, 12) - 0.1, 0.45)  # «suicidio»

    # La obra: golpes de pico, goteo y la tierra encima.
    put(whoosh(), at(11) - 0.4, 0.45)
    put(muffled(1.6, 46), word(11, 3), 0.6)  # «borrar»
    for s in np.arange(word(13, 6), at(15), 0.72):
        put(pick(), s + rng.uniform(-0.05, 0.05), 0.55, rng.uniform(0.35, 0.65))
    for s in rng.uniform(at(14), at(17, "end"), 9):
        put(drip(), s, 0.25, rng.uniform(0.2, 0.8))
    put(rumble(at(21) - at(14)), at(14), 0.35)

    # Guerra a ciegas: los picos alemanes se oyen a través de la pared.
    for s in np.arange(word(15, 3), at(18), 0.95):
        put(knock(), s + rng.uniform(-0.08, 0.08), 0.5, 0.75)
    put(heartbeat(at(18) - at(16), 70), at(16), 0.45)
    put(boom(1.0, 70, 0.3), at(18) - 0.04, 0.4)
    put(muffled(1.6, 50), word(20, 1), 0.75)       # «detonan cargas chicas»
    put(muffled(2.0, 42), word(22, 4), 0.9)        # «destruyen una de las cámaras»
    put(boom(1.2, 60, 0.4), at(24) - 0.04, 0.45)   # «el dato clave»
    put(heartbeat(at(27) - at(25), 78), at(25), 0.55)

    # 3:10: tic-tac en la calma, palanca del detonador y el silencio.
    for k, s in enumerate(np.arange(at(27), at(29, "end") + 0.4, 0.5)):
        put(tick(), s, 0.35 if k % 2 else 0.5, 0.45 if k % 2 else 0.55)
    put(wind(at(29, "end") - at(28) + 1, 0.35), at(28), 0.35)
    put(lever(), word(29, 10), 0.7, 0.6)

    # La voladura: 19 minas, tierra que cae y el retumbo largo.
    put(mega_blast(14.0), BLAST, 1.6)
    put(debris(6.0), BLAST + 1.0, 0.5)
    put(rumble(at(35) - BLAST), BLAST, 0.6)
    put(boom(1.4, 55, 0.5), at(31) - 0.04, 0.4)
    put(artillery(2.5), word(33, 2), 0.8, 0.3)      # «el rugido» llegando a Londres
    put(whoosh(), at(33) - 0.4, 0.4)
    put(boom(2.0, 45, 0.2), word(35, 3), 0.5)       # «la mayor explosión»

    # La mina olvidada: el rayo de 1955.
    put(wind(at(39) - at(37), 0.3), at(37), 0.35)
    put(thunder(), word(38, 3) - 0.05, 0.9)
    put(muffled(2.0, 44), word(38, 11), 0.7)        # «la hizo volar»

    # Cierre: un último golpe grave para la pregunta.
    put(rumble(total - at(40)), at(40), 0.35)
    put(boom(2.5, 45, 0.0), at(40) - 0.1, 0.45)
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
