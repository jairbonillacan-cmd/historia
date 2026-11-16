"""AG-20 · Operación Cartago (Copenhague, 1945). Música ambiental y efectos de sonido sintetizados acá mismo.

Todo sale de osciladores y ruido generados con numpy: no hay grabaciones ni pistas de terceros,
así que no hay nada que pueda reclamar Content ID y el video se puede monetizar.

Entrada:  audio/audio_master_censurado.wav (voz ya censurada, npm run mute:cartago) + timeline_chunks.json
Salida:   audio/musica.wav, audio/sfx.wav y audio/audio_master_final.wav (voz + música con ducking + efectos, -14 LUFS)

Uso (desde la raíz del repo): python produccion/12_operacion_cartago/build_music_and_sfx_cartago.py
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("produccion/12_operacion_cartago")
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

rng = np.random.default_rng(20)
timeline = json.loads((BASE / "timeline_chunks.json").read_text(encoding="utf-8"))
chunk = {c["index"]: c for c in timeline["chunks"]}


def at(i: int, field: str = "start") -> float:
    return chunk[i][field]


def atw(i: int, k: int) -> float:
    """Inicio de la palabra k de la cláusula i (para clavar un efecto en la palabra exacta)."""
    return chunk[i]["words"][k]["start"]


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
    (0.0, ["Dm", "Bb", "Gm", "A"], 0.55),               # el poste y la pesadilla
    (at(4), ["Dsus", "Dm", "Dsus", "Bb"], 0.45),        # Copenhague ocupada, la Gestapo y los ficheros
    (at(11), ["Gm", "Dm", "A", "Dm"], 0.5),             # la trampa: escudos humanos
    (at(16), ["Dm", "Bb", "F", "C"], 0.65),             # la Operación Cartago y el vuelo rasante
    (at(19), ["Dm", "C", "Bb", "A"], 0.7),              # el ataque quirúrgico
    (at(24), ["Dsus", "Gm"], 0.35),                     # el ala toca el poste y el avión cae
    (at(28), ["Gm", "Dm", "A", "Dm"], 0.4),             # la segunda oleada confunde el humo
    (at(32), ["Dm9", "Bb", "Gm", "Dm"], 0.6),           # el precio: el colegio
    (at(36), ["Dm", "Bb", "Dsus"], 0.6),                # el dilema final
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

    # Piano suave en el duelo por el colegio.
    piano = np.zeros(n, np.float32)
    for s, e, name, _ in chord_plan(total):
        if s < at(32) - 0.1 or s >= at(36):
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

    # Pulso grave muy suave mientras los Mosquito cruzan el mar y entran a Copenhague.
    pulse_from, pulse_to = at(17), at(23)
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


def engine_mosquito(dur: float) -> np.ndarray:
    """Dos Merlin V12: zumbido más agudo y liso que un radial, con batido lento entre los dos motores."""
    t = tvec(dur)
    f = 86 + 0.8 * np.sin(2 * np.pi * 0.05 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    ph2 = 2 * np.pi * np.cumsum(f * 1.012) / SR
    tone = sum(a * (np.sin(h * ph + k) + np.sin(h * ph2 + 2 * k)) for k, (h, a) in enumerate([(1, 1), (2, 0.55), (3, 0.3), (6, 0.12)]))
    rumble = band(noise(dur), 60, 700) * 0.5
    x = tone * 0.35 + rumble
    return band(x.astype(np.float32), 40, 1600) * fade(len(t), 1.0, 1.5)


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


def clang(f0: float = 180, dur: float = 2.6) -> np.ndarray:
    """Golpe metálico sobre un poste de hierro: parciales inarmónicos que vibran largo."""
    t = tvec(dur)
    x = sum(a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t * d) for r, a, d in [(1, 1, 1.4), (2.76, 0.6, 2.2), (5.4, 0.4, 3.5), (8.9, 0.25, 5), (13.3, 0.15, 7)])
    hit = band(noise(dur), 1500, 9000) * env_ar(len(t), 0.0005, 0.015)
    return room((x * 0.6 + hit).astype(np.float32), 0.7, 0.4)


def scrape(dur: float = 0.7) -> np.ndarray:
    """Chapa que roza metal: ruido agudo áspero que se corta en seco."""
    t = tvec(dur)
    grit = band(noise(dur), 1200, 7000) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 37 * t)))
    return (grit * fade(len(t), 0.02, 0.25)).astype(np.float32)


def typewriter(dur: float = 1.6) -> np.ndarray:
    """Teclas de máquina de escribir / fichero: chasquidos secos irregulares."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    t = 0.0
    while t < dur - 0.05:
        k = int(0.012 * SR)
        i = int(t * SR)
        out[i:i + k] += band(rng.standard_normal(k).astype(np.float32), 1500, 6000) * env_ar(k, 0.0005, 0.003) * rng.uniform(0.6, 1)
        t += rng.uniform(0.07, 0.16)
    return room(out, 0.25, 0.2)


def radar_ping() -> np.ndarray:
    t = tvec(1.8)
    return room((np.sin(2 * np.pi * 1320 * t) * np.exp(-t * 4)).astype(np.float32), 0.6, 0.35)


def tick(n: int = 4, every: float = 0.5) -> np.ndarray:
    out = np.zeros(int((n * every + 0.2) * SR), np.float32)
    for k in range(n):
        i = int(k * every * SR)
        c = band(noise(0.03), 2500, 8000) * env_ar(int(0.03 * SR), 0.0003, 0.004)
        out[i:i + len(c)] += c * (1 if k % 2 == 0 else 0.7)
    return out


def siren(dur: float) -> np.ndarray:
    """Sirena antiaérea lejana: sube, se sostiene y baja."""
    t = tvec(dur)
    p = t / dur
    f = 220 + 260 * np.clip(np.minimum(p / 0.3, (1 - p) / 0.3), 0, 1)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)
    return room(band(x.astype(np.float32), 150, 1500) * fade(len(t), 0.8, 1.2), 1.0, 0.6)


def crackle(dur: float) -> np.ndarray:
    """Incendio: rumor grave con chasquidos de madera."""
    n = int(dur * SR)
    out = band(noise(dur), 80, 600) * 0.35
    for s0 in rng.uniform(0, dur - 0.05, int(dur * 9)):
        i = int(s0 * SR)
        k = int(rng.uniform(0.002, 0.008) * SR)
        out[i:i + k] += rng.standard_normal(k).astype(np.float32) * rng.uniform(0.3, 1)
    return band(out, 60, 6000) * fade(n, 0.8, 1.5)


def waves(dur: float) -> np.ndarray:
    t = tvec(dur)
    swell = 0.55 + 0.45 * np.sin(2 * np.pi * 0.16 * t) ** 2
    return (band(noise(dur), 150, 2500) * swell * fade(len(t), 1.2, 1.5)).astype(np.float32)


def cell_door() -> np.ndarray:
    """Puerta de celda que se cierra: golpe metálico sordo y cerrojo."""
    t = tvec(1.6)
    thud = np.sin(2 * np.pi * 75 * t) * env_ar(len(t), 0.002, 0.15)
    ring = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * d) * a for f, a, d in [(310, 0.4, 5), (870, 0.2, 8)])
    bolt = np.zeros(len(t), np.float32)
    i = int(0.35 * SR)
    k = int(0.05 * SR)
    bolt[i:i + k] = band(noise(0.05), 1500, 6000)[:k] * env_ar(k, 0.001, 0.01)
    return room((thud + ring + bolt * 0.8).astype(np.float32), 0.5, 0.4)


def church_bell(f: float = 392.0) -> np.ndarray:
    t = tvec(5.0)
    x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for r, a, d in [(0.5, 0.6, 0.6), (1, 1, 0.9), (1.19, 0.5, 1.3), (1.5, 0.35, 1.6), (2, 0.25, 2.2)])
    return room(x.astype(np.float32), 1.0, 0.55)


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

    # Gancho: golpe en t=0, el poste de hierro que suena, el ala que lo roza y la pesadilla.
    put(boom(2.2, 50, 0.6), 0.0, 1.0)
    put(clang(170), atw(1, 1) - 0.05, 0.55, 0.6)
    put(wind(at(4), 0.4), 0.0, 0.4)
    put(boom(1.0, 70, 0.3), at(2) - 0.04, 0.45)
    put(flyby(3.0, 120, 92, 0.2, 0.8), atw(2, 3) - 1.2, 0.6)
    put(scrape(), atw(2, 11) - 0.05, 0.5, 0.65)
    put(clang(140, 1.8), atw(2, 11), 0.35, 0.65)
    put(boom(1.0, 70, 0.3), at(3) - 0.04, 0.45)
    put(boom(2.4, 45, 0.5), atw(3, 12) - 0.04, 0.8)

    # Copenhague ocupada: transición, ficheros de la Gestapo, latidos mientras la red está por caer.
    put(whoosh(), at(4) - 0.5, 0.5)
    put(boom(1.0, 70, 0.2), at(5) - 0.04, 0.35)
    put(boom(1.2, 60, 0.4), atw(6, 5) - 0.04, 0.5)
    put(typewriter(1.8), atw(7, 3), 0.45, 0.4)
    put(heartbeat(at(10) - at(8) + 0.4, 68), at(8), 0.5)
    put(boom(1.2, 60, 0.4), at(10) - 0.04, 0.5)
    put(crackle(2.8), atw(10, 9), 0.35)

    # La trampa: puerta de celda, latidos sobre los escudos humanos.
    put(boom(1.4, 55, 0.3), atw(11, 4) - 0.04, 0.5)
    put(cell_door(), atw(13, 9) - 0.05, 0.6, 0.4)
    put(heartbeat(at(16) - at(13) + 0.3, 72), at(13), 0.5)

    # La Operación Cartago: los Mosquito despegan y cruzan el mar pegados a las olas.
    put(whoosh(), at(16) - 0.5, 0.45)
    put(flyby(4.0, 100, 84, 0.3, 0.7), atw(16, 12) - 1.4, 0.55)
    put(engine_mosquito(at(19) - at(17) + 1.0), at(17), 0.5)
    put(waves(at(19) - at(17) + 0.5), at(17), 0.45)
    put(radar_ping(), atw(17, 14), 0.3, 0.7)
    for k, d in enumerate([0.0, 0.7, 1.4]):
        put(flyby(2.6, 110, 90, 0.2 + 0.25 * k, 0.8 - 0.2 * k), atw(18, 3) - 0.6 + d, 0.35)

    # 11:15: reloj, sirena lejana, la primera oleada pasa bajo las agujas y da de lleno.
    put(tick(4, 0.45), atw(20, 2) - 0.3, 0.45)
    put(siren(at(23) - atw(20, 5)), atw(20, 5), 0.25)
    put(engine_mosquito(at(23) - atw(20, 5) + 1), atw(20, 5), 0.4)
    put(flyby(3.0, 126, 86, 0.1, 0.9), atw(20, 12) - 1.0, 0.75)
    put(church_bell(330), atw(20, 17), 0.2, 0.35)
    put(boom(2.2, 48, 0.8), at(21) - 0.04, 0.9, 0.45)
    put(boom(1.6, 58, 0.6), atw(21, 5), 0.6, 0.6)
    put(crackle(at(24) - at(22) + 0.5), at(22), 0.45)
    put(whoosh(0.7), atw(23, 6) - 0.35, 0.35)

    # El ala toca el poste: chirrido, golpe metálico, motor que se descontrola y se estrella.
    put(flyby(3.5, 124, 96, 0.2, 0.75), at(24) - 0.3, 0.55)
    put(scrape(0.9), atw(24, 12) - 0.08, 0.75, 0.3)
    put(clang(150, 3.0), atw(24, 12), 0.65, 0.3)
    put(boom(1.0, 80, 0.4), atw(24, 12), 0.4, 0.3)
    put(flyby(2.0, 130, 70, 0.4, 0.6), atw(25, 2) - 0.3, 0.55)
    put(boom(3.0, 40, 0.9), atw(25, 7) - 0.04, 1.0)
    put(crackle(at(29) - at(26) + 1), at(26), 0.5)
    put(boom(2.5, 38, 0.1), atw(27, 3), 0.45)

    # La segunda y tercera oleada llegan al humo.
    put(whoosh(), at(28) - 0.5, 0.4)
    for k, w in enumerate([3, 7, 10]):
        put(flyby(2.8, 118, 88, 0.15 + 0.3 * k, 0.85 - 0.3 * k), atw(28, w) - 0.8, 0.45)
    put(wind(at(32) - at(29) + 1, 0.6), at(29), 0.45)
    put(heartbeat(atw(32, 5) - at(29) + 0.2, 76), at(29), 0.55)
    for k, w in enumerate([10, 12, 15]):
        put(boom(2.0, 45, 0.15), atw(31, w) + 0.1, 0.45 - 0.08 * k, 0.4 + 0.1 * k)

    # El precio: silencio y una campana.
    put(church_bell(294), at(33) + 0.4, 0.35)
    put(wind(at(36) - at(34), 0.3), at(34), 0.35)
    put(church_bell(294), at(35) + 1.0, 0.22)

    # Cierre: un último golpe grave para la pregunta.
    put(boom(2.5, 45, 0.0), at(37) - 0.1, 0.4)
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
