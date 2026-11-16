"""AG-22 · Operación Bernhard (1942). Música ambiental y efectos de sonido sintetizados acá mismo.

Todo sale de osciladores y ruido generados con numpy: no hay grabaciones ni pistas de terceros,
así que no hay nada que pueda reclamar Content ID y el video se puede monetizar.

Entrada:  audio/audio_master_censurado.wav (voz ya censurada, npm run mute:bernhard) + timeline_chunks.json
Salida:   audio/musica.wav, audio/sfx.wav y audio/audio_master_final.wav (voz + música con ducking + efectos, -14 LUFS)

Uso (desde la raíz del repo): python produccion/14_operacion_bernhard/build_music_and_sfx_bernhard.py
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("produccion/14_operacion_bernhard")
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

rng = np.random.default_rng(22)
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
    "Cm": ["C2", "G2", "C3", "D#3", "G3"],
    "Ab": ["G#1", "D#2", "G#2", "C3", "D#3"],
    "Fm": ["F1", "C2", "F2", "G#2", "C3"],
    "G": ["G1", "D2", "G2", "B2", "D3"],
    "Gsus": ["G1", "D2", "G2", "C3", "D3"],
    "Db": ["C#2", "G#2", "C#3", "F3", "G#3"],
    "Csus": ["C2", "G2", "C3", "F3", "G3"],
    "Eb": ["D#2", "A#2", "D#3", "G3", "A#3"],
    "Bb": ["A#1", "F2", "A#2", "D3", "F3"],
    "Cm9": ["C3", "G3", "D4", "D#4", "A#4"],
    "Abmaj7": ["G#2", "D#3", "G3", "C4", "D#4"],
}

# (desde, acorde, brillo): la armonía sigue el arco del guion.
SECTIONS_START = [
    (0.0, ["Cm", "Ab", "Fm", "G"], 0.5),                # el billete perfecto: intriga
    (at(7), ["Cm", "Ab", "Db", "G"], 0.45),             # el plan del régimen: oscuro
    (at(11), ["Fm", "Cm", "Db", "Gsus"], 0.4),          # los prisioneros y Sachsenhausen
    (at(16), ["Csus", "Cm", "Csus", "Db"], 0.35),       # el equilibrio aterrador: suspenso
    (at(20), ["Cm9", "Ab", "Eb", "Bb"], 0.6),           # descifran los secretos: método
    (at(26), ["Ab", "Eb", "Bb", "Cm"], 0.7),            # el resultado perfecto, el dinero circula
    (at(31), ["Cm", "Db", "Gsus", "G"], 0.4),           # el dólar y el sabotaje
    (at(34), ["Ab", "Eb", "Bb", "Eb"], 0.75),           # la liberación
    (at(35), ["Abmaj7", "Eb", "Cm9", "Bb"], 0.8),       # epílogo y dilema
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

    # Piano suave desde que descifran los secretos (el trabajo paciente), salvo en el sabotaje.
    piano = np.zeros(n, np.float32)
    for s, e, name, _ in chord_plan(total):
        if s < at(20) - 0.1 or at(31) - 0.1 <= s < at(34) - 0.1:
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

    # Pulso grave muy suave en el suspenso (vivos mientras tarden; el sabotaje).
    for tt in [*np.arange(at(16), at(20), 1.0), *np.arange(at(32), at(34), 1.0)]:
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


def paper(dur: float = 0.7, crisp: float = 1.0) -> np.ndarray:
    """Billete que se manosea: ráfagas cortas de ruido agudo con crujidos."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    for s in rng.uniform(0, max(0.01, dur - 0.06), int(30 * dur * crisp)):
        k = int(rng.uniform(0.008, 0.04) * SR)
        i = int(s * SR)
        burst = band(rng.standard_normal(k).astype(np.float32), 1800, 9000) * env_ar(k, 0.001, 0.012) * rng.uniform(0.3, 1)
        out[i:i + k] += burst[: n - i]
    return out * fade(n, 0.05, 0.2)


def snap() -> np.ndarray:
    """Billete tensado de golpe entre las manos: chasquido seco con cuerpo."""
    t = tvec(0.35)
    x = band(noise(0.35), 900, 7000) * env_ar(len(t), 0.0008, 0.02) + band(noise(0.35), 150, 900) * env_ar(len(t), 0.002, 0.05) * 0.6
    return room(x.astype(np.float32), 0.3, 0.25)


def shimmer(dur: float = 2.2) -> np.ndarray:
    """Destello de luz al trasluz: campanitas agudas que se apagan."""
    t = tvec(dur)
    x = np.zeros(len(t), np.float32)
    for k, f in enumerate([1568, 2093, 2637, 3136]):
        tt = np.clip(t - k * 0.08, 0, None)
        x += (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 2.5) * (t >= k * 0.08)).astype(np.float32) * 0.3
    return room(x, 0.7, 0.5)


def pin() -> np.ndarray:
    """Pinchazo de alfiler en el papel: clic diminuto y agudo."""
    t = tvec(0.12)
    x = band(noise(0.12), 3000, 12000) * env_ar(len(t), 0.0004, 0.006) + np.sin(2 * np.pi * 4200 * t) * env_ar(len(t), 0.0005, 0.01) * 0.3
    return x.astype(np.float32)


def stamp() -> np.ndarray:
    """Sello de goma sobre un escritorio de madera."""
    t = tvec(0.6)
    x = np.sin(2 * np.pi * (140 * t - 60 * t ** 2)) * env_ar(len(t), 0.001, 0.04) + band(noise(0.6), 200, 2500) * env_ar(len(t), 0.0008, 0.03) * 0.8
    return room(x.astype(np.float32), 0.4, 0.3)


def clang(dur: float = 2.6) -> np.ndarray:
    """Puerta de hierro que se cierra: golpe metálico con resonancias inarmónicas."""
    t = tvec(dur)
    x = band(noise(dur), 80, 3000) * env_ar(len(t), 0.001, 0.05)
    for f, a, d in [(196, 0.6, 1.6), (311, 0.45, 2.2), (523, 0.3, 3.0), (877, 0.2, 4.0)]:
        x += a * np.sin(2 * np.pi * f * t) * np.exp(-t * d)
    return room(x.astype(np.float32), 0.9, 0.55)


def tick(dur: float, bpm: float = 60) -> np.ndarray:
    """Reloj: tic-tac seco, alternando dos intensidades."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    for k, s in enumerate(np.arange(0, dur - 0.05, 60 / bpm)):
        c = band(pin(), 1500, 6000) * (0.9 if k % 2 else 0.6)
        i = int(s * SR)
        out[i:i + len(c)] += c[: n - i]
    return out


def press(dur: float, rate: float = 1.6, failing: bool = False) -> np.ndarray:
    """Imprenta: golpe de la platina y chirrido del rodillo. `failing` = se traba a destiempo."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    th = tvec(0.5)
    for s in np.arange(0, dur - 0.3, 1 / rate):
        if failing and rng.random() < 0.35:
            s += rng.uniform(0.05, 0.25)
        hit = np.sin(2 * np.pi * (90 * th - 40 * th ** 2)) * env_ar(len(th), 0.001, 0.05)
        hit += band(noise(0.5), 300, 3000) * env_ar(len(th), 0.0008, 0.02) * 0.7
        roll = band(noise(0.5), 1200, 4000) * np.exp(-((th - 0.25) / 0.08) ** 2) * 0.25
        x = (hit + roll).astype(np.float32)
        i = int(s * SR)
        out[i:i + len(x)] += x[: n - i]
    return room(out, 0.5, 0.35) * fade(n, 0.3, 0.6)


def marching(dur: float, bpm: float = 112) -> np.ndarray:
    """Botas sobre grava a lo lejos."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    th = tvec(0.18)
    for k, s in enumerate(np.arange(0, dur - 0.2, 60 / bpm)):
        x = band(noise(0.18), 120, 1800) * env_ar(len(th), 0.002, 0.03) * (1 if k % 2 else 0.75)
        i = max(0, int((s + rng.uniform(-0.01, 0.01)) * SR))
        out[i:i + len(x)] += x[: n - i]
    return room(out, 0.8, 0.4) * fade(n, 0.6, 0.8)


def drone(dur: float, f0: float = 58) -> np.ndarray:
    """Bimotor lejano (los aviones que tirarían los billetes, el rescate de Mussolini)."""
    t = tvec(dur)
    f = f0 + 0.8 * np.sin(2 * np.pi * 0.09 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.6 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph)
    beat = 0.8 + 0.2 * np.sin(2 * np.pi * 2.3 * t)
    x = (tone * 0.5 + band(noise(dur), 40, 500) * 0.5) * beat
    return band(x.astype(np.float32), 30, 1000) * fade(len(t), 1.0, 1.5)


def flutter(dur: float = 3.0) -> np.ndarray:
    """Lluvia de billetes: muchos papeles que caen y aletean."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    for _ in range(6):
        out += paper(dur, 0.8) * (0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(1.5, 4) * tvec(dur)[:n] + rng.uniform(0, 6))).astype(np.float32)
    return band(out, 900, 7000) * fade(n, 0.4, 1.0)


def bell() -> np.ndarray:
    """Campana lejana para la liberación (emotiva, no literal)."""
    t = tvec(3.5)
    x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in [(392, 1, 1.0), (622.3, 0.4, 1.6), (784, 0.3, 2.2)])
    return room(x.astype(np.float32), 0.9, 0.5)


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

    def w(i: int, k: int) -> float:
        """Inicio de la palabra k de la cláusula i."""
        return chunk[i]["words"][k]["start"]

    # Gancho: golpe de apertura, el billete en la mano, y un golpe en cada corte.
    put(boom(2.2, 50, 0.6), 0.0, 1.0)
    put(paper(1.2), 0.25, 0.6, 0.45)
    put(snap(), w(2, 4) - 0.05, 0.7)                 # «suena exacto»
    put(shimmer(), w(3, 4) - 0.05, 0.35, 0.6)         # la marca de agua brilla
    put(pin(), w(3, 14), 0.9, 0.55)                  # agujero de alfiler
    for i in (2, 3, 4, 5, 6):
        put(boom(1.0, 70, 0.3), at(i) - 0.04, 0.4)
    put(heartbeat(at(7) - at(5) + 0.3, 70), at(5), 0.45)
    put(wind(at(7) - at(6) + 1, 0.5), at(6), 0.5)     # barracones y alambre de púas

    # El plan del régimen: sellos, aviones que tiran billetes.
    put(boom(1.6, 55, 0.5), at(7) - 0.05, 0.6)
    put(stamp(), w(8, 1), 0.7)                       # «la Operación Bernhard»
    put(stamp(), w(8, 10), 0.6)                      # Krüger
    put(whoosh(), at(10) - 0.5, 0.4)
    put(drone(6.0), w(10, 7) - 0.5, 0.55)            # «tirarlas desde aviones»
    put(flutter(3.5), w(10, 9), 0.55)
    put(boom(1.4, 60, 0.6), w(10, 27), 0.5)          # «colapse»

    # Los prisioneros: marcha lejana, un sello por oficio, la puerta de hierro de los bloques.
    put(marching(at(13) - at(12) + 1.0), at(12), 0.45)
    for k in range(5):
        put(stamp(), w(13, k), 0.35, 0.3 + 0.1 * k)
    put(clang(), w(15, 1), 0.6)                      # «los encierran»
    put(wind(at(16) - at(15), 0.3), at(15) + 1.0, 0.4)

    # Vivos mientras tarden: reloj y latidos, golpe seco en la amenaza.
    put(tick(at(20) - at(16) + 0.5, 60), at(16), 0.5)
    put(heartbeat(at(20) - at(17), 74), at(17), 0.55)
    put(boom(1.8, 48, 0.4), w(19, 3) - 0.05, 0.65)

    # Descifran los secretos: papel, marca de agua, la numeración, los alfileres.
    put(whoosh(), at(20) - 0.5, 0.35)
    put(paper(1.5, 0.7), w(21, 7), 0.4)              # trapos de lino
    put(shimmer(1.6), w(22, 4), 0.25, 0.4)           # la marca de agua
    put(tick(at(23) - w(22, 15), 120), w(22, 15), 0.3)  # el algoritmo numera las series
    put(paper(at(24) - w(23, 10), 1.3), w(23, 10), 0.45)  # los frotan entre las manos
    for k, s in enumerate(np.arange(w(24, 4), at(25) + 0.6, 0.32)):
        put(pin(), s, 0.6, 0.35 + 0.3 * (k % 2))     # los pinchan con alfileres

    # El resultado: golpe de revelación, la imprenta a pleno, billetes que vuelan.
    put(boom(2.0, 50, 0.5), at(26) - 0.05, 0.6)
    put(press(at(29) - at(27), 2.2), at(27), 0.55)
    put(flutter(3.0), w(28, 2), 0.45)
    put(drone(at(31) - w(30, 3) + 0.5, 62), w(30, 3), 0.45)  # el rescate de Mussolini

    # El dólar y el sabotaje: la imprenta se traba.
    put(stamp(), w(31, 3), 0.7)
    put(boom(1.4, 60, 0.4), w(31, 9), 0.5)
    put(heartbeat(at(34) - at(32), 68), at(32), 0.5)
    put(press(at(34) - at(33), 1.2, failing=True), at(33), 0.45)
    put(clang(1.8), w(33, 7), 0.35, 0.6)             # las planchas estropeadas

    # La liberación.
    put(wind(at(35) - w(34, 7) + 1, 0.4), w(34, 7), 0.45)
    put(bell(), w(34, 7), 0.3)

    # Epílogo: los billetes retirados y el golpe grave para la pregunta.
    put(paper(1.0), w(35, 10), 0.35)
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
