"""AG-21 · Scapa Flow (1919). Música ambiental y efectos de sonido sintetizados acá mismo.

Todo sale de osciladores y ruido generados con numpy: no hay grabaciones ni pistas de terceros,
así que no hay nada que pueda reclamar Content ID y el video se puede monetizar.

Entrada:  audio/audio_master_censurado.wav (voz ya censurada, npm run mute:scapa) + timeline_chunks.json
Salida:   audio/musica.wav, audio/sfx.wav y audio/audio_master_final.wav (voz + música con ducking + efectos, -14 LUFS)

Uso (desde la raíz del repo): python produccion/13_scapa_flow/build_music_and_sfx_scapa.py
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("produccion/13_scapa_flow")
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

rng = np.random.default_rng(21)
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
    (0.0, ["Dm", "Bb", "Gm", "A"], 0.55),              # el acorazado que se inclina, 52 barcos al fondo
    (at(4), ["Dm9", "Bb", "F", "C"], 0.5),              # Scapa Flow, Versalles: contexto
    (at(10), ["Dsus", "Dm", "Dsus", "Bb"], 0.45),       # Reuter aislado, diarios viejos
    (at(12), ["Gm", "Dm", "A", "Dm"], 0.5),             # el plazo y la guerra que vuelve
    (at(17), ["Dsus", "Bb", "Dsus", "A"], 0.45),        # la jugada silenciosa: nota secreta
    (at(22), ["Dm", "Bb", "Gm", "A"], 0.6),             # la flota inglesa se va: la oportunidad
    (at(28), ["Dm", "Bb", "C", "A"], 0.7),              # las válvulas abiertas
    (at(31), ["Gm", "Dm", "A", "Dm"], 0.55),            # se hunde el Friedrich der Grosse, el mar hierve
    (at(36), ["Dm", "Bb", "Gm", "A"], 0.5),             # es inútil: 52 buques al fondo
    (at(38), ["Fmaj7", "C", "Dm", "Bb"], 0.8),          # «cualquier marino británico habría hecho lo mismo»
    (at(40), ["Dm", "Bb", "Dsus"], 0.6),                # el dilema final
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

    # Piano suave en las partes humanas (Reuter aislado, la confesión del almirante).
    piano = np.zeros(n, np.float32)
    for s, e, name, _ in chord_plan(total):
        if not (at(10) - 0.1 <= s < at(12) or s >= at(38) - 0.1):
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

    # Pulso grave muy suave en el suspenso (la bandera sube, la orden).
    pulse_from, pulse_to = at(24), at(28)
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


def sea(dur: float, strength: float = 1.0) -> np.ndarray:
    """Oleaje de bahía: ruido grave que sube y baja con olas lentas, con algo de espuma."""
    t = tvec(dur)
    swell = 0.55 + 0.45 * np.sin(2 * np.pi * 0.11 * t) * np.sin(2 * np.pi * 0.047 * t + 0.6)
    low = band(noise(dur), 60, 500) * swell
    foam = band(noise(dur), 1200, 5000) * 0.25 * np.clip(swell - 0.4, 0, 1)
    return ((low + foam) * strength * fade(len(t), 1.5, 2.0)).astype(np.float32)


def groan(dur: float = 3.5, f0: float = 38) -> np.ndarray:
    """Casco de acero que cruje al inclinarse: tono grave que se dobla, con roce metálico."""
    t = tvec(dur)
    f = f0 * (1 + 0.25 * np.sin(2 * np.pi * 0.4 * t) - 0.15 * t / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.5 * np.sin(2.01 * ph) + 0.3 * np.sin(3.7 * ph)
    scrape = band(noise(dur), 300, 1400) * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * t) ** 2) * 0.35
    return room(((tone * 0.6 + scrape) * fade(len(t), 0.6, 1.2)).astype(np.float32), 0.8, 0.45)


def bubbles(dur: float, density: float = 30) -> np.ndarray:
    """Agua que borbotea: burbujas que suben de tono (el mar «hierve»)."""
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    for s in rng.uniform(0, max(0.1, dur - 0.08), int(dur * density)):
        d = rng.uniform(0.03, 0.08)
        th = tvec(d)
        f = rng.uniform(250, 900)
        b = np.sin(2 * np.pi * f * (th + 6 * th ** 2)) * env_ar(len(th), 0.002, d / 3)
        i = int(s * SR)
        out[i:i + len(b)] += b[: n - i] * rng.uniform(0.2, 0.7)
    return (band(out, 150, 3000) + band(noise(dur), 80, 600) * 0.4) * fade(n, 0.5, 0.8)


def rush(dur: float) -> np.ndarray:
    """Agua entrando a presión por las tomas de mar."""
    t = tvec(dur)
    x = band(noise(dur), 150, 2200) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.6 * t))
    return (x * fade(len(t), 0.4, 1.0)).astype(np.float32)


def clang(f: float = 210) -> np.ndarray:
    """Maza contra hierro: parciales inarmónicos que resuenan en la bodega."""
    t = tvec(1.6)
    x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for r, a, d in [(1, 1, 4), (2.76, 0.6, 6), (5.4, 0.35, 9), (8.9, 0.2, 14)])
    hit = band(noise(1.6), 1500, 7000) * env_ar(len(t), 0.0005, 0.01) * 0.6
    return room((x + hit).astype(np.float32), 0.5, 0.5)


def rifle(dist: float = 1.0) -> np.ndarray:
    """Disparo de fusil sobre el agua: chasquido y eco largo."""
    dur = 1.8
    t = tvec(dur)
    crack = band(noise(dur), 900, 6000 / dist) * env_ar(len(t), 0.0004, 0.012)
    body = band(noise(dur), 80, 700) * env_ar(len(t), 0.001, 0.08)
    return room((crack + body * 0.8) / dist, 1.2, 0.55)


def horn(dur: float = 3.0, f: float = 98) -> np.ndarray:
    """Sirena de barco lejana: diente de sierra grave a dos voces."""
    t = tvec(dur)
    x = np.zeros(len(t), np.float32)
    for ff, a in [(f, 1), (f * 1.26, 0.6)]:
        x += a * (2 * ((ff * t) % 1) - 1).astype(np.float32)
    return room(band(x, 60, 900) * fade(len(t), 0.25, 0.8), 1.0, 0.5)


def ship_engine(dur: float) -> np.ndarray:
    """Destructor a toda máquina: turbinas y golpeteo de hélices."""
    t = tvec(dur)
    beat = 0.7 + 0.3 * np.sin(2 * np.pi * 5.2 * t)
    x = (band(noise(dur), 40, 300) * beat + np.sin(2 * np.pi * 47 * t) * 0.4 * beat).astype(np.float32)
    return x * fade(len(t), 1.0, 1.2)


def tick(n_ticks: int, every: float = 0.5) -> np.ndarray:
    """Reloj: el plazo de Versalles."""
    out = np.zeros(int((n_ticks * every + 0.2) * SR), np.float32)
    for k in range(n_ticks):
        th = tvec(0.03)
        c = band(noise(0.03), 2000, 8000) * env_ar(len(th), 0.0003, 0.004)
        i = int(k * every * SR)
        out[i:i + len(c)] += c * (1 if k % 2 == 0 else 0.7)
    return out


def paper(dur: float = 1.0) -> np.ndarray:
    """Papel de fumar que se desliza y se dobla."""
    t = tvec(dur)
    crinkle = np.zeros(len(t), np.float32)
    for s in rng.uniform(0, dur - 0.02, 40):
        i = int(s * SR)
        k = int(rng.uniform(0.003, 0.015) * SR)
        crinkle[i:i + k] += rng.standard_normal(len(crinkle[i:i + k])).astype(np.float32) * rng.uniform(0.2, 0.8)
    return band(crinkle, 1500, 9000) * fade(len(t), 0.05, 0.3) + band(noise(dur), 2000, 6000) * 0.1


def halyard(dur: float = 1.6) -> np.ndarray:
    """Driza que corre por la polea al izar las banderas."""
    t = tvec(dur)
    squeak = np.sin(2 * np.pi * (1300 + 300 * np.sin(2 * np.pi * 3 * t)) * t) * (np.sin(2 * np.pi * 3 * t) > 0.6) * 0.25
    rope = band(noise(dur), 800, 3500) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 3 * t)))
    return ((squeak + rope * 0.6) * fade(len(t), 0.1, 0.4)).astype(np.float32)


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

    # Gancho: golpe en t=0, mar de fondo, el casco que cruje al inclinarse y un golpe en cada corte.
    put(boom(2.2, 50, 0.6), 0.0, 1.0)
    put(sea(at(4) + 1.0), 0.0, 0.5)
    put(whoosh(), at(2) - 0.5, 0.45)
    put(boom(1.0, 70, 0.3), at(2) - 0.04, 0.45)
    put(groan(4.0, 36), at(2, "end") - 2.6, 0.75, 0.6)
    put(boom(1.4, 55, 0.4), at(3) - 0.04, 0.55)
    put(bubbles(at(4) - at(3), 22), at(3) + 0.8, 0.5)
    put(boom(2.0, 45, 0.2), at(3, "end") - 0.6, 0.55)  # «…un solo cañonazo»

    # Contexto: mapa, Versalles, la flota anclada.
    put(whoosh(), at(4) - 0.5, 0.45)
    put(sea(at(10) - at(4), 0.7), at(4), 0.45)
    put(whoosh(), at(7) - 0.4, 0.35)
    put(horn(3.5, 87), at(9) + 1.0, 0.3, 0.3)

    # Reuter aislado: viento y mar, diarios viejos.
    put(wind(at(12) - at(10) + 1, 0.6), at(10), 0.5)
    put(sea(at(12) - at(10), 0.6), at(10), 0.4)
    put(paper(0.9), at(11) + 1.6, 0.5, 0.6)

    # El plazo y la guerra que vuelve: reloj y latidos.
    put(tick(int((at(13) - at(12)) / 0.5)), at(12), 0.55, 0.55)
    put(heartbeat(at(15) - at(13) + 0.5, 70), at(13), 0.55)
    put(boom(1.2, 60, 0.3), at(14) - 0.04, 0.4)
    put(clang(150), at(16) + 0.4, 0.25, 0.4)  # cañones vacíos

    # La jugada silenciosa: la nota en papel de fumar, la bandera, válvulas, cañerías, soldadura.
    put(whoosh(), at(17) - 0.5, 0.4)
    put(paper(1.2), at(18) + 2.0, 0.6, 0.45)
    put(halyard(), at(19), 0.5, 0.6)
    put(clang(180), at(20) + 0.9, 0.45, 0.35)
    put(rush(2.0), at(20) + 1.2, 0.35)
    put(clang(240), at(21) + 0.3, 0.4, 0.65)

    # La flota inglesa sale a hacer ejercicios: sirena y máquinas que se alejan, torpedos a lo lejos.
    put(sea(at(25) - at(22), 0.6), at(22), 0.4)
    put(horn(3.0, 92), at(23) + 0.5, 0.45, 0.35)
    away = at(24) - at(23) + 1
    put(ship_engine(away) * np.linspace(1, 0.1, int(away * SR)).astype(np.float32), at(23), 0.4)
    for k in range(3):
        put(boom(1.2, 40, 0.0), at(23) + 2.2 + k * 0.9, 0.18, 0.2 + 0.3 * k)

    # 10:30: suben las banderas. Latido y golpe en la orden.
    put(heartbeat(at(28) - at(25), 76), at(25), 0.55)
    put(halyard(1.8), at(26) + 0.4, 0.55, 0.55)
    put(boom(2.4, 48, 0.5), at(27) - 0.04, 0.85)

    # Hundimiento: mazas contra el hierro, agua que entra, burbujas.
    put(whoosh(), at(28) - 0.4, 0.45)
    for s in np.arange(at(29) + 0.3, at(31) - 0.4, 0.62):
        put(clang(rng.uniform(170, 260)), s + rng.uniform(-0.08, 0.08), 0.45, rng.uniform(0.25, 0.75))
    put(rush(at(31) - at(29) + 1.5), at(29) + 0.5, 0.45)
    put(bubbles(at(31) - at(30) + 1, 25), at(30), 0.4)

    # El Friedrich der Grosse da la vuelta de campana.
    put(groan(4.5, 32), at(31) + 0.6, 0.85, 0.45)
    put(boom(2.8, 40, 0.3), at(31, "end") - 0.8, 0.75)
    put(bubbles(3.5, 40), at(31, "end") - 0.3, 0.55)

    # Vuelven los destructores británicos; el mar hierve.
    put(ship_engine(at(34) - at(32) + 1), at(32), 0.5)
    put(horn(2.0, 110), at(32) + 0.6, 0.35, 0.7)
    put(bubbles(at(34) - at(33) + 1.5, 60), at(33), 0.6)

    # Remolques y disparos.
    for s in [at(34) + 3.0, at(34) + 3.5, at(34) + 4.3]:
        put(rifle(rng.uniform(1.0, 1.6)), s, 0.55, rng.uniform(0.3, 0.7))
    put(heartbeat(at(36) - at(35) + 0.3, 58), at(35), 0.5)

    # Es inútil: golpe grave, el acero que se va al fondo.
    put(boom(2.6, 42, 0.2), at(36) - 0.04, 0.7)
    put(groan(4.0, 30), at(37) + 0.5, 0.6, 0.5)
    put(bubbles(at(37, "end") - at(37), 30), at(37), 0.45)

    # El almirante inglés: mar calmo.
    put(sea(at(40) - at(38) + 1, 0.5), at(38), 0.4)

    # Cierre: un último golpe grave para la pregunta.
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
