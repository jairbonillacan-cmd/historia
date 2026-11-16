"""AG-18 · Operación Chariot, Saint-Nazaire (1942). Música ambiental y efectos de sonido sintetizados acá mismo.

Todo sale de osciladores y ruido generados con numpy: no hay grabaciones ni pistas de terceros,
así que no hay nada que pueda reclamar Content ID y el video se puede monetizar.

Entrada:  audio/audio_master_censurado.wav (voz ya censurada, npm run mute:nazaire) + timeline_chunks.json
Salida:   audio/musica.wav, audio/sfx.wav y audio/audio_master_final.wav (voz + música con ducking + efectos, -14 LUFS)

Uso (desde la raíz del repo): python produccion/06_cielo_bremen/build_music_and_sfx_saint_nazaire.py
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("produccion/09_saint_nazaire")
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

rng = np.random.default_rng(18)
timeline = json.loads((BASE / "timeline_chunks.json").read_text(encoding="utf-8"))
chunk = {c["index"]: c for c in timeline["chunks"]}


def at(i: int, field: str = "start") -> float:
    return chunk[i][field]


def word(i: int, k: int) -> float:
    """Inicio de la palabra k de la cláusula i (para clavar golpes en la palabra exacta)."""
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
    (0.0, ["Dm", "Bb", "Gm", "A"], 0.5),                # alemanes sobre la proa, el ácido
    (at(5), ["Dsus", "Dm", "Dsus", "Bb"], 0.45),        # el Tirpitz y el dique: suspenso
    (at(14), ["Gm", "Dm", "A", "Dm"], 0.55),            # Operación Chariot: el barco bomba
    (at(24), ["Dm", "Bb", "Gm", "A"], 0.4),             # reflectores, fuego, embestida
    (at(29), ["Dm9", "Bb", "Dm9", "Gm"], 0.7),          # prisioneros, la burla
    (at(34), ["Dsus", "Dsus", "Dm"], 0.35),             # el ácido llega al detonador
    (at(36), ["Gm", "Dm", "A", "Dm"], 0.55),            # la explosión y el dique roto
    (at(38), ["Fmaj7", "C", "Dm", "Bb"], 0.85),         # cinco Cruces Victoria
    (at(41), ["Dm", "Bb", "Dsus"], 0.6),                # el dilema final
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

    # Piano suave en las partes humanas (los prisioneros, el homenaje).
    piano = np.zeros(n, np.float32)
    for s, e, name, _ in chord_plan(total):
        if not (at(29) - 0.1 <= s < at(34) or s >= at(38) - 0.1):
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

    # Pulso grave en el suspenso: la entrada al río y la cuenta regresiva del ácido.
    beats = list(np.arange(at(22), at(28), 0.8)) + list(np.arange(at(32), word(35, 1), 0.7))
    for tt in beats:
        p = band(noise(0.5), 30, 120) * env_ar(int(0.5 * SR), 0.01, 0.12) * 0.5
        p += np.sin(2 * np.pi * 52 * tvec(0.5)) * env_ar(int(0.5 * SR), 0.004, 0.14)
        i = int(tt * SR)
        mus[i:i + len(p)] += p[:, None] * 0.35

    # Silencio de la música justo antes de la explosión; entrada y salida.
    g = np.ones(n, np.float32)
    g[int((word(35, 1) - 0.35) * SR):int((word(35, 3) + 1.2) * SR)] = 0.0
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




def tick(dur: float, bpm: float = 120, hard: float = 1.0) -> np.ndarray:
    """Tic-tac de reloj: el ácido que come el cable."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    for k, s in enumerate(np.arange(0, dur - 0.05, 60 / bpm)):
        c = band(noise(0.03), 2500 if k % 2 else 1800, 7000) * env_ar(int(0.03 * SR), 0.0005, 0.006) * hard
        i = int(s * SR)
        out[i:i + len(c)] += c[: n - i]
    return out


def sea(dur: float, strength: float = 1.0) -> np.ndarray:
    """Agua contra el casco: ruido grave con oleaje lento."""
    t = tvec(dur)
    swell = 0.55 + 0.45 * np.sin(2 * np.pi * 0.16 * t) ** 2
    x = band(noise(dur), 80, 700) * swell + band(noise(dur), 900, 3000) * 0.25 * swell ** 3
    return (x * strength * fade(len(t), 1.5, 1.5)).astype(np.float32)


def ship_engine(dur: float, f0: float = 32, rpm: float = 2.2) -> np.ndarray:
    """Máquinas de un destructor: zumbido grave con golpe de pistones."""
    t = tvec(dur)
    ph = 2 * np.pi * f0 * t
    tone = np.sin(ph) + 0.5 * np.sin(2 * ph + 1) + 0.25 * np.sin(3 * ph)
    chug = 0.7 + 0.3 * np.sin(2 * np.pi * rpm * t) ** 4
    x = (tone * 0.5 + band(noise(dur), 30, 300) * 0.5) * chug
    return band(x.astype(np.float32), 25, 600) * fade(len(t), 1.0, 1.5)


def gunfire(dur: float, rate: float = 7.0) -> np.ndarray:
    """Cañones y ametralladoras a quemarropa: estampidos secos repartidos en estéreo."""
    n = int(dur * SR)
    out = np.zeros((n, 2), np.float32)
    for s in np.sort(rng.uniform(0, dur - 0.3, int(dur * rate))):
        near = rng.uniform(0.4, 1.0)
        shot = band(noise(0.35), 400, 6000) * env_ar(int(0.35 * SR), 0.0005, 0.02) * near
        shot += band(noise(0.35), 40, 300) * env_ar(int(0.35 * SR), 0.002, 0.08) * near * 1.4
        pan = rng.uniform(0.1, 0.9)
        i = int(s * SR)
        j = min(n, i + len(shot))
        out[i:j, 0] += shot[: j - i] * np.sqrt(1 - pan)
        out[i:j, 1] += shot[: j - i] * np.sqrt(pan)
    return out


def crash() -> np.ndarray:
    """Embestida: golpe grave, chirrido de metal que se dobla y crujido largo."""
    dur = 3.5
    t = tvec(dur)
    hit = boom(dur, 42, 0.9)[: len(t)] * 1.3
    f = 420 - 260 * t / dur + 30 * np.sin(2 * np.pi * 7 * t)
    screech = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 2.7) / SR)
    screech = band(screech.astype(np.float32), 200, 4000) * env_ar(len(t), 0.05, 0.9) * 0.35
    groan = band(noise(dur), 60, 500) * fade(len(t), 0.2, 2.0) * 0.6
    return (hit + screech + groan).astype(np.float32)


def big_explosion() -> np.ndarray:
    """La explosión del Campbeltown: estallido enorme, cola larga y escombros que caen."""
    dur = 6.0
    t = tvec(dur)
    body = band(noise(dur), 18, 220) * env_ar(len(t), 0.006, 1.1) * 2.0
    thump = np.sin(2 * np.pi * (38 * t - 9 * t ** 2)) * env_ar(len(t), 0.003, 0.5) * 1.5
    crack = band(noise(dur), 700, 8000) * env_ar(len(t), 0.001, 0.08)
    x = room((body + thump + crack).astype(np.float32), 1.2, 0.5)
    for s in rng.uniform(1.0, 5.0, 40):  # escombros
        d = band(noise(0.2), 800, 5000) * env_ar(int(0.2 * SR), 0.001, 0.03) * rng.uniform(0.05, 0.25)
        i = int(s * SR)
        x[i:i + len(d)] += d[: len(x) - i]
    return x


def fire(dur: float) -> np.ndarray:
    """Crepitar de incendio: rumor grave y chasquidos al azar."""
    n = int(dur * SR)
    out = band(noise(dur), 60, 500) * 0.5
    for s in rng.uniform(0, dur - 0.05, int(dur * 14)):
        i = int(s * SR)
        k = int(0.006 * SR)
        out[i:i + k] += rng.standard_normal(k).astype(np.float32) * rng.uniform(0.2, 0.8)
    return band(out, 50, 6000) * fade(n, 0.8, 1.2)


def searchlight() -> np.ndarray:
    """Golpe metálico del reflector al encenderse, con zumbido eléctrico."""
    dur = 2.0
    t = tvec(dur)
    clunk = band(noise(dur), 300, 3000) * env_ar(len(t), 0.001, 0.05)
    hum = (np.sin(2 * np.pi * 100 * t) + 0.5 * np.sin(2 * np.pi * 200 * t)) * fade(len(t), 0.05, 1.2) * 0.25
    return (clunk + hum).astype(np.float32)


def salute_bell() -> np.ndarray:
    """Campana suave y lejana para el homenaje (transición emotiva, no un efecto literal)."""
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

    # Gancho: golpe en t=0, golpes secos en cada corte y el tic-tac del ácido.
    put(boom(2.2, 50, 0.6), 0.0, 1.0)
    put(sea(at(5) + 1), 0.0, 0.35)
    for t0 in (word(1, 8), at(2), word(2, 10), at(3), at(4)):
        put(boom(1.0, 70, 0.3), t0 - 0.04, 0.45)
    put(tick(at(5) - at(3) + 0.3, 120), at(3), 0.5)
    put(heartbeat(at(5) - at(4) + 0.4, 70), at(4), 0.45)

    # El Tirpitz en Noruega y el dique: transiciones y el mar.
    put(whoosh(), at(5) - 0.5, 0.5)
    put(ship_engine(at(8) - at(6), 26, 1.4), at(6), 0.5)
    put(sea(at(10) - at(6), 0.6), at(6), 0.4)
    put(boom(1.4, 60, 0.4), word(7, 7), 0.4)                   # hundir convoyes
    put(whoosh(), at(9) - 0.5, 0.4)
    put(boom(1.2, 55, 0.2), word(10, 5), 0.45)                  # la compuerta
    put(flak(1.8), word(12, 15), 0.45, 0.3)                     # búnkeres y cañones
    put(flak(2.2), word(12, 17), 0.4, 0.7)

    # Operación Chariot: el barco bomba se arma.
    put(boom(1.6, 48, 0.5), word(14, 3), 0.55)
    put(ship_engine(at(24) - at(15), 34, 2.4), at(15), 0.45)
    put(whoosh(), at(17) - 0.4, 0.35)
    put(boom(1.0, 60, 0.6), word(18, 4), 0.45)                  # 4.500 kilos
    put(tick(at(21) - at(20), 100, 0.7), at(20), 0.4)           # espoletas químicas
    put(sea(at(24) - at(21), 0.8), at(21), 0.45)
    put(fire(at(24) - word(23, 2) + 1), word(23, 2), 0.5)       # las lanchas arden

    # 1:28: reflectores, fuego a quemarropa, Beattie acelera.
    put(searchlight(), word(25, 1), 0.6, 0.3)
    put(searchlight(), word(25, 1) + 0.25, 0.5, 0.75)
    put(gunfire(at(28) - word(25, 9) + 0.5, 8), word(25, 9), 0.6)
    put(fire(at(29) - at(26)), at(26), 0.45)
    put(ship_engine(word(28, 5) - at(27) + 0.3, 40, 3.5), at(27), 0.6)

    # 1:34: la embestida.
    put(crash(), word(28, 5), 0.9)
    put(heartbeat(at(29) - word(28, 14) + 0.3, 64), word(28, 14), 0.4)

    # Prisioneros y la burla; vuelve el tic-tac, cada vez más cerca.
    put(sea(at(32) - at(29), 0.35), at(29), 0.4)
    put(tick(word(35, 1) - at(32) - 0.35, 110, 1.0), at(32), 0.55)
    put(heartbeat(word(35, 1) - at(33) - 0.35, 78), at(33), 0.5)

    # Mediodía: la explosión.
    put(big_explosion(), word(35, 3) - 0.05, 1.3)
    put(boom(1.4, 60, 0.8), at(36), 0.5)
    put(fire(at(38) - at(36)), at(36), 0.45)

    # Homenaje y cierre.
    put(salute_bell(), at(38) + 0.2, 0.3)
    put(boom(1.2, 55, 0.0), word(40, 0), 0.35)
    put(boom(2.5, 45, 0.0), at(41) - 0.1, 0.4)
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
