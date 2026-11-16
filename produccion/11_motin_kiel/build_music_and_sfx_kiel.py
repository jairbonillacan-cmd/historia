"""AG-19 · Motín de Kiel (1918). Música ambiental y efectos de sonido sintetizados acá mismo.

Todo sale de osciladores y ruido generados con numpy: no hay grabaciones ni pistas de terceros,
así que no hay nada que pueda reclamar Content ID y el video se puede monetizar.

Entrada:  audio/audio_master_censurado.wav (voz ya censurada, npm run mute:kiel) + timeline_chunks.json
Salida:   audio/musica.wav, audio/sfx.wav y audio/audio_master_final.wav (voz + música con ducking + efectos, -14 LUFS)

Uso (desde la raíz del repo): python produccion/11_motin_kiel/build_music_and_sfx_kiel.py
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("produccion/11_motin_kiel")
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

rng = np.random.default_rng(19)
timeline = json.loads((BASE / "timeline_chunks.json").read_text(encoding="utf-8"))
chunk = {c["index"]: c for c in timeline["chunks"]}


def at(i: int, word: int | None = None) -> float:
    """Inicio de la cláusula `i` o de su palabra `word`."""
    return chunk[i]["start"] if word is None else chunk[i]["words"][word]["start"]


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
    (0.0, ["Dm", "Bb", "Gm", "A"], 0.45),               # la pala cae, los fogoneros se cruzan de brazos
    (at(5), ["Dm", "F", "Gm", "A"], 0.6),               # la flota, orgullo del káiser; Jutlandia y el bloqueo
    (at(10), ["Gm", "Dm", "Bb", "A"], 0.45),            # la guerra está perdida
    (at(13), ["Dsus", "Dm", "Dsus", "Bb"], 0.4),        # los almirantes y la orden secreta: suspenso
    (at(21), ["Dm", "Bb", "Dsus", "A"], 0.5),           # la noche del 29 de octubre
    (at(26), ["Dsus", "Dm"], 0.3),                      # sin vapor: quietud
    (at(29), ["Gm", "Dm", "A", "Dm"], 0.6),             # enciende la mecha, la revuelta
    (at(34), ["Bb", "F", "C", "F"], 0.75),              # cae Berlín, abdica el káiser, fin de la guerra
    (at(37), ["Fmaj7", "C", "Dm", "Bb"], 0.8),          # reflexión
    (at(39), ["Dm", "Bb", "Dsus"], 0.55),               # el dilema final
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

    # Piano suave en el cierre (fin de la guerra y reflexión).
    piano = np.zeros(n, np.float32)
    for s, e, name, _ in chord_plan(total):
        if s < at(34) - 0.1:
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

    # Pulso grave muy suave en el suspenso (la orden de zarpar) y en la revuelta, más rápido.
    beats = list(np.arange(at(21), at(26), 1.0)) + list(np.arange(at(30), at(34), 0.5))
    for tt in beats:
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


def naval_gun(dist: float = 1.0) -> np.ndarray:
    """Cañonazo lejano en el mar: golpe grave largo y retumbo que rueda."""
    dur = 3.0
    t = tvec(dur)
    body = band(noise(dur), 18, 140 / dist) * env_ar(len(t), 0.01, 0.6)
    thump = np.sin(2 * np.pi * (38 * t - 8 * t ** 2)) * env_ar(len(t), 0.005, 0.3)
    return room((body * 1.6 + thump) / dist, 1.2, 0.55)


def clang(f: float = 420, dur: float = 1.4, gain: float = 1.0) -> np.ndarray:
    """Golpe metálico (pala contra el piso de chapa): parciales inarmónicos que decaen rápido."""
    t = tvec(dur)
    x = sum(a * np.sin(2 * np.pi * f * r * t + rng.uniform(0, 6)) * np.exp(-t * d) for r, a, d in [(1, 1, 6), (2.76, 0.6, 9), (5.4, 0.4, 14), (8.93, 0.25, 20)])
    hit = band(noise(dur), 1500, 8000) * env_ar(len(t), 0.0005, 0.01)
    return room(((x * 0.5 + hit) * gain).astype(np.float32), 0.5, 0.35)


def coal_spill(dur: float = 1.2) -> np.ndarray:
    """Carbón que cae y rueda: muchos chasquidos secos que se van espaciando."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    for s in np.sort(rng.exponential(0.25, 90)):
        if s > dur - 0.05:
            continue
        i = int(s * SR)
        k = int(rng.uniform(0.004, 0.012) * SR)
        click = band(rng.standard_normal(k).astype(np.float32), 400, 3500) * np.exp(-np.arange(k) / (k / 3))
        out[i:i + k] += click * rng.uniform(0.2, 0.9)
    return out * fade(n, 0.002, 0.3)


def furnace(dur: float) -> np.ndarray:
    """Rugido del hogar de las calderas: ruido grave que respira y chisporrotea."""
    t = tvec(dur)
    roar = band(noise(dur), 30, 260) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.4 * t))
    crackle = np.zeros(len(t), np.float32)
    for s in rng.uniform(0, dur - 0.01, int(dur * 6)):
        i = int(s * SR)
        k = int(0.006 * SR)
        crackle[i:i + k] += rng.standard_normal(len(crackle[i:i + k])).astype(np.float32) * 0.3
    return (roar + band(crackle, 1500, 6000)) * fade(len(t), 0.4, 1.2)


def steam_die(dur: float = 3.5) -> np.ndarray:
    """Vapor que se escapa y se apaga: siseo que baja de tono y de volumen hasta cero."""
    t = tvec(dur)
    p = t / dur
    a = band(noise(dur), 2500, 9000) * (1 - p) ** 2
    b = band(noise(dur), 600, 2500) * (1 - p) ** 3 * 0.6
    groan = np.sin(2 * np.pi * np.cumsum(90 - 50 * p) / SR) * (1 - p) * 0.25
    return ((a + b + groan) * fade(len(t), 0.05, 0.4)).astype(np.float32)


def ship_horn(dur: float = 3.0, f: float = 92) -> np.ndarray:
    """Sirena de barco: dos tonos graves desafinados con ataque lento."""
    t = tvec(dur)
    x = sum(a * np.sin(2 * np.pi * f * h * t) for h, a in [(1, 1), (2, 0.5), (3, 0.3), (4, 0.15)])
    x += sum(a * np.sin(2 * np.pi * f * 1.26 * h * t) for h, a in [(1, 0.7), (2, 0.35), (3, 0.2)])
    return room(band((x * fade(len(t), 0.35, 0.8)).astype(np.float32), 50, 1200), 1.3, 0.55)


def sea(dur: float, strength: float = 1.0) -> np.ndarray:
    """Agua contra el casco: olas lentas de ruido filtrado."""
    t = tvec(dur)
    swell = 0.55 + 0.45 * np.sin(2 * np.pi * 0.13 * t) ** 2
    x = band(noise(dur), 120, 1400) * swell + band(noise(dur), 1400, 4000) * 0.25 * swell ** 3
    return (x * strength * fade(len(t), 1.5, 2.0)).astype(np.float32)


def artillery_far(dur: float) -> np.ndarray:
    """Frente lejano: retumbos sordos al azar."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    for s in np.arange(0.2, max(0.3, dur - 1), 0.7):
        x = band(noise(1.5), 20, 90) * env_ar(int(1.5 * SR), 0.02, 0.4)
        i = max(0, int((s + rng.uniform(-0.2, 0.2)) * SR))
        j = min(n, i + len(x))
        out[i:j] += x[: j - i] * rng.uniform(0.4, 1.0)
    return out * fade(n, 0.5, 1.0)


def telegraph(dur: float) -> np.ndarray:
    """Morse de telégrafo: pitidos cortos y largos (el pedido de armisticio)."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    s = 0.0
    while s < dur - 0.3:
        L = 0.06 if rng.random() < 0.6 else 0.18
        k = int(L * SR)
        i = int(s * SR)
        out[i:i + k] += (np.sin(2 * np.pi * 760 * tvec(L)) * fade(k, 0.004, 0.004))[: n - i]
        s += L + (0.06 if rng.random() < 0.8 else 0.22)
    return out


def typewriter(dur: float) -> np.ndarray:
    """Máquina de escribir: golpes de tecla y, al final, la campanita del carro."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    s = 0.0
    while s < dur - 0.6:
        k = int(0.03 * SR)
        i = int(s * SR)
        key = band(noise(0.03), 900, 6000) * env_ar(k, 0.0005, 0.006) + np.sin(2 * np.pi * 180 * tvec(0.03)) * env_ar(k, 0.001, 0.008) * 0.5
        out[i:i + k] += key[: n - i] * rng.uniform(0.5, 1.0)
        s += rng.uniform(0.07, 0.16)
    bell = np.sin(2 * np.pi * 2100 * tvec(0.6)) * np.exp(-tvec(0.6) * 7) * 0.4
    i = int((dur - 0.55) * SR)
    out[i:i + len(bell)] += bell[: n - i]
    return out


def chain(dur: float = 2.2) -> np.ndarray:
    """Cadena del ancla que sube eslabón por eslabón."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    t = tvec(0.15)
    for s in np.arange(0, dur - 0.2, 0.11):
        x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * 40) for f, a in [(rng.uniform(1100, 1500), 1), (rng.uniform(2600, 3300), 0.5)])
        x += band(noise(0.15), 1500, 7000) * env_ar(len(t), 0.0005, 0.004)
        i = int(s * SR)
        out[i:i + len(x)] += x[: n - i] * rng.uniform(0.3, 0.6)
    return room(out * fade(n, 0.05, 0.4), 0.6, 0.3)


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


def door_slam() -> np.ndarray:
    """Puerta de calabozo de hierro: golpe seco + resonancia metálica corta."""
    dur = 1.6
    t = tvec(dur)
    hit = band(noise(dur), 60, 900) * env_ar(len(t), 0.001, 0.05) * 1.4
    ring = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in [(180, 0.5, 5), (497, 0.3, 9)])
    return room((hit + ring).astype(np.float32), 0.9, 0.5)


def fuse(dur: float = 1.2) -> np.ndarray:
    """Mecha encendida: chisporroteo agudo que avanza."""
    n = int(dur * SR)
    out = band(noise(dur), 3000, 10000) * (0.4 + 0.6 * (rng.random(n) > 0.7))
    return (out * fade(n, 0.05, 0.15)).astype(np.float32)


def march(dur: float, bpm: float = 112) -> np.ndarray:
    """Muchedumbre marchando: pisadas graves en tiempo, con desfasaje entre cientos de pies."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    beat = 60 / bpm
    k = int(0.08 * SR)
    for s in np.arange(0, dur - 0.3, beat):
        for _ in range(6):
            i = int((s + rng.normal(0, 0.025)) * SR)
            if i < 0 or i >= n:
                continue
            step = band(noise(0.08), 80, 1200) * env_ar(k, 0.002, 0.02) * rng.uniform(0.3, 0.7)
            out[i:i + k] += step[: n - i]
    crowd = band(noise(dur), 250, 1800) * 0.18
    return (out + crowd) * fade(n, 1.0, 1.0)


def rifle(dist: float = 1.0) -> np.ndarray:
    """Disparo de fusil: chasquido seco y eco corto."""
    dur = 1.0
    t = tvec(dur)
    crack = band(noise(dur), 800, 9000 / dist) * env_ar(len(t), 0.0003, 0.008)
    body = band(noise(dur), 100, 800) * env_ar(len(t), 0.001, 0.05)
    return room((crack + body * 0.8) / dist, 1.1, 0.5)


def train(dur: float) -> np.ndarray:
    """Locomotora a vapor: resoplidos rítmicos que aceleran, traqueteo y silbato al final."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    s, period = 0.0, 0.42
    k = int(0.2 * SR)
    while s < dur - 0.3:
        i = int(s * SR)
        puff = band(noise(0.2), 300, 3000) * env_ar(k, 0.01, 0.06)
        out[i:i + k] += puff[: n - i]
        s += period
        period = max(0.2, period * 0.97)
    k = int(0.05 * SR)
    for s in np.arange(0.3, dur - 0.2, 0.55):
        for off in (0, 0.12):
            i = int((s + off) * SR)
            out[i:i + k] += (band(noise(0.05), 200, 2500) * env_ar(k, 0.001, 0.01))[: n - i] * 0.6
    t = tvec(1.2)
    whistle = (np.sin(2 * np.pi * 740 * t) + 0.6 * np.sin(2 * np.pi * 932 * t) + 0.3 * np.sin(2 * np.pi * 1110 * t)) * fade(len(t), 0.1, 0.4) * 0.35
    i = int(max(0, dur - 1.4) * SR)
    out[i:i + len(whistle)] += whistle[: n - i]
    return out * fade(n, 0.3, 0.5)


def bell_toll(f: float = 196) -> np.ndarray:
    """Campana grave de iglesia (abdicación, fin de la guerra)."""
    t = tvec(5.0)
    x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for r, a, d in [(0.5, 0.6, 0.6), (1, 1, 0.8), (1.19, 0.5, 1.1), (1.5, 0.35, 1.4), (2.0, 0.3, 1.8), (2.66, 0.15, 2.5)])
    return room(x.astype(np.float32), 1.0, 0.45)


def engine_down(dur: float = 3.0) -> np.ndarray:
    """Máquina de vapor que se detiene: golpes de pistón cada vez más lentos."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    s, period = 0.0, 0.18
    k = int(0.12 * SR)
    while s < dur - 0.3:
        i = int(s * SR)
        out[i:i + k] += (np.sin(2 * np.pi * 55 * tvec(0.12)) * env_ar(k, 0.003, 0.04) + band(noise(0.12), 200, 1500) * env_ar(k, 0.002, 0.02) * 0.4)[: n - i]
        s += period
        period *= 1.18
    return out * fade(n, 0.05, 0.6)


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

    # Gancho: golpe de apertura, sala de máquinas con el hogar rugiendo, la pala cae en «cae al piso».
    put(boom(2.2, 50, 0.6), 0.0, 1.0)
    put(furnace(at(2, 9) + 0.6), 0.0, 0.7)
    put(clang(380, 1.6, 1.2), at(1, 5) + 0.15, 0.9, 0.4)
    put(coal_spill(1.4), at(1, 5) + 0.2, 0.7, 0.55)
    # «apagan el fuego»: el vapor se escapa y se apaga; golpes secos en cada corte.
    put(steam_die(3.0), at(2, 7), 0.6)
    for i in (2, 3, 4):
        put(boom(1.0, 70, 0.3), at(i) - 0.04, 0.45)
    put(heartbeat(at(5) - at(3) + 0.3, 66), at(3), 0.5)
    put(boom(2.4, 42, 0.5), at(4, 4), 0.85)  # «tumbar a un emperador»

    # La flota del káiser: mar, sirena; Jutlandia con cañonazos lejanos; el bloqueo.
    put(whoosh(), at(5) - 0.5, 0.5)
    put(sea(at(13) - at(5) + 1, 0.8), at(5), 0.55)
    put(ship_horn(3.2, 88), at(6, 1), 0.55)
    for s in np.arange(at(7, 5), at(8), 0.6):
        put(naval_gun(rng.uniform(1.0, 2.2)), s + rng.uniform(-0.1, 0.1), 0.65, rng.uniform(0.2, 0.8))
    put(ship_horn(2.6, 70), at(9) - 0.2, 0.35)
    # Francia: frente lejano. Berlín pide el armisticio por telégrafo.
    put(artillery_far(at(11) - at(10, 5) + 0.5), at(10, 5), 0.6)
    put(telegraph(at(12) - at(11, 2)), at(11, 2), 0.25, 0.6)

    # Los almirantes redactan la orden secreta: máquina de escribir; pulso de suspenso.
    put(whoosh(), at(13) - 0.5, 0.4)
    put(typewriter(at(17) - at(16, 2)), at(16, 2), 0.45, 0.55)
    put(boom(1.2, 60, 0.4), at(17), 0.45)
    put(sea(at(18) - at(17) + 1, 0.9), at(17), 0.5)
    put(ship_horn(3.0, 84), at(17, 3), 0.55)
    put(heartbeat(at(21) - at(18) + 0.4, 62), at(18), 0.45)
    put(typewriter(at(21) - at(20) - 0.2), at(20), 0.3, 0.45)

    # La noche del 29 de octubre: mar nocturno, la orden de levar anclas (cadena), corazón.
    put(sea(at(26) - at(21) + 1, 0.6), at(21), 0.5)
    put(chain(2.4), at(22, 9), 0.6, 0.6)
    put(heartbeat(at(25) - at(23) + 0.4, 72), at(23), 0.55)
    put(furnace(at(25, 6) - at(24) + 0.4), at(24), 0.55)
    # Bajan las palas (dos golpes de chapa) y la presión cae a cero: vapor que se apaga.
    put(clang(420, 1.4, 1.0), at(25, 2) + 0.15, 0.7, 0.35)
    put(clang(360, 1.4, 0.8), at(25, 4) + 0.1, 0.6, 0.65)
    put(steam_die(3.2), at(25, 6), 0.75)
    put(engine_down(2.8), at(26), 0.55)

    # Hipper cancela, arresta y manda fusilar: puerta de hierro, golpe grave. La mecha.
    put(boom(1.0, 70, 0.3), at(27) - 0.04, 0.4)
    put(door_slam(), at(28) + 0.05, 0.75, 0.45)
    put(boom(1.8, 48, 0.2), at(28, 14), 0.55)
    put(fuse(1.3), at(29, 2), 0.45, 0.55)
    put(boom(2.2, 45, 0.6), at(29, 4) + 0.4, 0.85)

    # 3 de noviembre: marcha en Kiel; la patrulla dispara; la flota se rebela.
    put(march(at(31, 2) - at(30, 4) + 0.4), at(30, 4), 0.7)
    put(rifle(1.0), at(31, 3), 0.8, 0.35)
    put(rifle(1.3), at(31, 3) + 0.28, 0.6, 0.6)
    put(rifle(1.6), at(31, 3) + 0.5, 0.45, 0.45)
    put(boom(1.6, 55, 0.4), at(31, 8), 0.6)
    put(march(at(33, 10) - at(32) + 0.4, 120), at(32), 0.45)
    # La revuelta viaja en tren y toma Berlín.
    put(train(at(35) - at(33, 9)), at(33, 9), 0.6, 0.55)
    put(boom(2.0, 50, 0.5), at(34, 5), 0.6)
    # Abdica el káiser; la guerra termina: campanas.
    put(bell_toll(196), at(35, 10), 0.4)
    put(bell_toll(262), at(36, 4), 0.35)
    put(bell_toll(196), at(36, 4) + 2.2, 0.25)

    # Reflexión: mar en calma; «les apagaron el motor».
    put(sea(at(39) - at(37) + 1.5, 0.45), at(37), 0.45)
    put(engine_down(2.6), at(38, 5), 0.45)

    # Cierre: un último golpe grave para la pregunta.
    put(boom(2.5, 45, 0.0), at(40) - 0.1, 0.4)
    put(heartbeat(total - at(40), 58), at(40), 0.35)
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
