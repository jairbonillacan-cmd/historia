"""AG-16 · Mers el-Kebir (1940). Música de fondo y efectos de sonido sintetizados desde cero (sin samples
de terceros: libres de derechos y monetizables), mezclados bajo la voz censurada.

Arma audio/musica.wav, audio/sfx.wav y audio/audio_master_final.wav (voz + música con ducking + efectos, -14 LUFS).
Los efectos van a tiempos de palabra de timeline_chunks.json.

Uso (desde la raíz del repo, después de build_audio_and_timeline_mers.py y npm run mute:mers):
    python produccion/07_mers_el_kebir/build_music_sfx_mers.py
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("produccion/07_mers_el_kebir")
VOICE = BASE / "audio/audio_master_censurado.wav"
MUSIC = BASE / "audio/musica.wav"
SFX = BASE / "audio/sfx.wav"
FINAL = BASE / "audio/audio_master_final.wav"
SR = 48000
rng = np.random.default_rng(1940)

timeline = json.loads((BASE / "timeline_chunks.json").read_text(encoding="utf-8"))
DUR = timeline["total_duration"] + 0.6
N = int(DUR * SR)
WORDS = [(c["index"], w) for c in timeline["chunks"] for w in c["words"]]


def at(word: str, clause: int, edge: str = "start") -> float:
    return next(w[edge] for i, w in WORDS if i == clause and w["word"] == word)


def clause_start(i: int) -> float:
    return next(c["start"] for c in timeline["chunks"] if c["index"] == i)


# ---------- utilidades ----------

def t(n: int) -> np.ndarray:
    return np.arange(n) / SR


def band(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    """Filtro pasabanda por FFT con bordes suaves."""
    f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.clip((f - lo * 0.7) / (lo * 0.3 + 1e-9), 0, 1) if lo > 0 else np.ones_like(f)
    g *= np.clip((hi * 1.3 - f) / (hi * 0.3), 0, 1)
    return np.fft.irfft(np.fft.rfft(x) * g, len(x))


def noise(sec: float) -> np.ndarray:
    return rng.standard_normal(int(sec * SR))


def add(buf: np.ndarray, x: np.ndarray, start: float, gain: float = 1.0) -> None:
    a = int(start * SR)
    b = min(len(buf), a + len(x))
    if b > a:
        buf[a:b] += x[: b - a] * gain


def norm(x: np.ndarray) -> np.ndarray:
    return x / (np.abs(x).max() + 1e-9)


def write(path: Path, x: np.ndarray) -> None:
    st = np.stack([x, x], axis=1) if x.ndim == 1 else x
    pcm = (np.clip(st, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ---------- efectos ----------

def boom(size: float = 1.0, dist: float = 0.0) -> np.ndarray:
    """Cañonazo: golpe grave con caída de tono + cola de ruido. `dist` 0–1 lo vuelve lejano (más opaco, menos ataque)."""
    sec = 1.8 + 1.8 * size
    tt = t(int(sec * SR))
    f = 38 + 60 * np.exp(-tt * 9)
    thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (3.2 / size))
    body = norm(band(noise(sec), 30, 900 - 600 * dist)) * np.exp(-tt * (2.2 / size))
    crack = norm(band(noise(sec), 800, 5000)) * np.exp(-tt * 40) * (1 - dist)
    x = 1.0 * thump + 0.8 * body + 0.35 * crack
    att = np.clip(tt / (0.004 + 0.03 * dist), 0, 1)
    return norm(x * att) * (1 - 0.45 * dist)


def explosion() -> np.ndarray:
    """El Bretagne volando: estallido + estruendo largo + escombros."""
    sec = 6.5
    tt = t(int(sec * SR))
    rumble = norm(band(noise(sec), 20, 260)) * (np.exp(-tt * 0.7) * np.clip(tt / 0.02, 0, 1))
    roar = norm(band(noise(sec), 120, 2200)) * np.exp(-tt * 1.6) * np.clip(tt / 0.01, 0, 1)
    debris = norm(band(noise(sec), 1500, 7000)) * np.exp(-((tt - 1.2) ** 2) / 0.6) * (rng.random(len(tt)) > 0.985)
    x = np.zeros(len(tt))
    x += 1.0 * rumble + 0.6 * roar + 0.25 * norm(band(debris, 1500, 7000))
    x[: len(boom(1.6))] += boom(1.6)
    return norm(x)


def whoosh(sec: float = 1.1) -> np.ndarray:
    tt = t(int(sec * SR))
    env = np.sin(np.pi * tt / sec) ** 2
    return norm(band(noise(sec), 300, 2500) * env)


def impact() -> np.ndarray:
    """Golpe cinematográfico grave para remarcar un momento."""
    sec = 3.0
    tt = t(int(sec * SR))
    f = 32 + 40 * np.exp(-tt * 6)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 1.6)
    x += 0.4 * norm(band(noise(sec), 40, 400)) * np.exp(-tt * 4)
    return norm(x * np.clip(tt / 0.003, 0, 1))


def tick() -> np.ndarray:
    tt = t(int(0.05 * SR))
    return norm(band(noise(0.05), 1800, 6000) * np.exp(-tt * 260) + 0.5 * np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 300))


def radio(sec: float) -> np.ndarray:
    """Estática de radio con cortes + morse."""
    tt = t(int(sec * SR))
    flutter = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 3.3 * tt + 2 * np.sin(2 * np.pi * 0.7 * tt)))
    x = norm(band(noise(sec), 400, 3200)) * flutter * 0.35
    code = ".-. .- -.. .. ---  ..-. .-. .- -. -.-."  # «RADIO FRANC»
    pos, unit = 0.25, 0.075
    for ch in code:
        if ch == " ":
            pos += unit * 3
            continue
        d = unit * (3 if ch == "-" else 1)
        a, b = int(pos * SR), int((pos + d) * SR)
        if b < len(x):
            seg = tt[: b - a]
            x[a:b] += 0.5 * np.sin(2 * np.pi * 760 * seg) * np.clip(seg / 0.004, 0, 1) * np.clip((d - seg) / 0.004, 0, 1)
        pos += d + unit
    fade = np.clip(tt / 0.15, 0, 1) * np.clip((sec - tt) / 0.4, 0, 1)
    return x * fade


def sea(sec: float) -> np.ndarray:
    tt = t(int(sec * SR))
    swell = 0.55 + 0.45 * np.sin(2 * np.pi * tt / 5.5 - 1.5)
    fade = np.clip(tt / 1.5, 0, 1) * np.clip((sec - tt) / 2.0, 0, 1)
    return norm(band(noise(sec), 80, 1400)) * swell * fade


def horn(sec: float = 2.6) -> np.ndarray:
    """Sirena de barco lejana."""
    tt = t(int(sec * SR))
    x = sum(np.sin(2 * np.pi * f0 * k * tt) / k ** 1.3 for f0 in (73, 110) for k in range(1, 9))
    env = np.clip(tt / 0.25, 0, 1) * np.clip((sec - tt) / 0.6, 0, 1)
    return norm(band(x * env, 60, 900))


def build_sfx() -> np.ndarray:
    s = np.zeros(N)
    # Gancho: el cañoneo que se anuncia
    add(s, boom(1.0, dist=0.7), at("cañonear", 2), 0.55)
    add(s, boom(0.8, dist=0.8), at("cañonear", 2) + 0.9, 0.35)
    # Armisticio: golpe seco
    add(s, impact(), at("armisticio.", 4) + 0.1, 0.45)
    # Invasión: golpe
    add(s, impact(), at("invadida", 12), 0.4)
    # Transiciones de mapa
    for c in (5, 13, 17, 38):
        add(s, whoosh(), clause_start(c) - 0.45, 0.28)
    # Puerto de Mers el-Kebir: mar de fondo y llegada de la flota británica
    add(s, sea(19.0), clause_start(14) - 0.5, 0.10)
    add(s, horn(), at("flota", 17) - 0.2, 0.30)
    # Ultimátum de seis horas: reloj
    t0, t1 = at("ultimátum", 19), at("fuego.", 21, "end")
    k = 0
    while t0 + k * 0.75 < t1:
        add(s, tick(), t0 + k * 0.75, 0.18 if k % 2 else 0.24)
        k += 1
    add(s, impact(), at("fuego.", 21), 0.6)
    # Radio interceptada
    a = at("radio.", 26) - 0.3
    add(s, radio(at("interceptan", 27, "end") + 1.0 - a), a, 0.35)
    # Antes de que oscurezca: golpe que corta
    add(s, impact(), at("oscurezca", 29, "end") + 0.2, 0.5)
    # 17:54 · fuego
    add(s, boom(1.5), at("17:54", 30) - 0.15, 0.85)
    salvo = [118.3, 119.0, 119.9, 120.6, 121.8, 122.9, 124.0, 125.1, 125.7]
    for i, x in enumerate(salvo):
        add(s, boom(0.9 + 0.3 * rng.random(), dist=0.35 + 0.4 * rng.random()), x, 0.32 + 0.12 * (i % 2))
    add(s, boom(1.3), at("fuego", 33) - 0.05, 0.6)
    add(s, boom(1.1, dist=0.3), at("quemarropa,", 33, "end") - 0.1, 0.5)
    # El Bretagne vuela por los aires
    add(s, explosion(), at("vuela", 34) - 0.1, 0.95)
    add(s, boom(1.0, dist=0.6), at("encallados.", 35) - 0.4, 0.3)
    # Tolón: barcos hundidos por sus propios marineros
    add(s, boom(1.2, dist=0.85), at("hundieron", 39), 0.35)
    # Cierre
    add(s, impact(), clause_start(40) - 0.05, 0.4)
    return s


# ---------- música ----------
# Pad cinematográfico en re menor con progresión lenta y un pulso grave que sube en la tensión.

NOTE = {"D2": 73.42, "F2": 87.31, "G2": 98.0, "A2": 110.0, "Bb2": 116.54, "C3": 130.81, "D3": 146.83, "E3": 164.81,
        "F3": 174.61, "G3": 196.0, "A3": 220.0, "Bb3": 233.08, "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "A4": 440.0}
CHORDS = {
    "Dm": ["D2", "A2", "D3", "F3", "A3", "D4"],
    "Bb": ["Bb2", "F3", "Bb3", "D4", "F4"],
    "Gm": ["G2", "D3", "G3", "Bb3", "D4"],
    "A": ["A2", "E3", "A3", "C4", "E4"],  # A sus/m sin tercera mayor para que no brille
    "F": ["F2", "C3", "F3", "A3", "C4", "F4"],
    "C": ["C3", "G3", "C4", "E4"],
}


def pad_chord(names: list[str], sec: float) -> np.ndarray:
    tt = t(int(sec * SR))
    x = np.zeros(len(tt))
    for n in names:
        f = NOTE[n]
        for det in (-0.12, 0.0, 0.13):
            ph = rng.random() * 2 * np.pi
            for k, amp in ((1, 1.0), (2, 0.35), (3, 0.15), (4, 0.06)):
                x += amp * np.sin(2 * np.pi * f * (1 + det / 100) * k * tt + ph * k)
    lfo = 0.8 + 0.2 * np.sin(2 * np.pi * 0.11 * tt + rng.random() * 6)
    return x * lfo / len(names)


def build_music() -> np.ndarray:
    # (desde, hasta, acordes, nivel)
    sections = [
        (0.0, 51.5, ["Dm", "Bb", "Gm", "A"], 0.8),
        (51.5, 101.0, ["Dm", "Gm", "Bb", "A"], 0.9),
        (101.0, 115.6, ["Gm", "A", "Gm", "A"], 1.0),
        (115.6, 138.2, ["Dm", "Dm"], 0.55),
        (138.2, 155.2, ["Bb", "F", "Gm", "A"], 0.8),
        (155.2, DUR, ["Dm", "Bb"], 0.75),
    ]
    m = np.zeros(N)
    xf = 2.5
    for a, b, prog, lvl in sections:
        step = (b - a) / len(prog)
        for i, ch in enumerate(prog):
            s0 = a + i * step
            sec = step + xf
            x = pad_chord(CHORDS[ch], sec)
            tt = t(len(x))
            env = np.clip(tt / xf, 0, 1) * np.clip((sec - tt) / xf, 0, 1)
            add(m, x * env * lvl, max(0.0, s0 - xf / 2))
    # Drone grave de re todo el video
    tt = t(N)
    m += 0.35 * np.sin(2 * np.pi * 36.71 * tt) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.05 * tt))
    # Pulso tipo timbal desde que aparece la flota, acelerando hacia el ataque
    pulse = np.zeros(N)
    beat = t(int(0.9 * SR))
    hit = np.sin(2 * np.pi * (55 + 30 * np.exp(-beat * 20)) * beat) * np.exp(-beat * 6)
    x, period = clause_start(17), 1.6
    while x < 115.4:
        prog = (x - 64) / (115.4 - 64)
        add(pulse, hit, x, 0.25 + 0.45 * prog)
        x += period * (1 - 0.45 * prog)
    m += pulse
    # Entrada y salida suaves
    m *= np.clip(tt / 2.0, 0, 1) * np.clip((DUR - tt) / 3.0, 0, 1)
    return norm(m)


def run(*args: str) -> str:
    return subprocess.run(["ffmpeg", "-hide_banner", "-y", *args], capture_output=True, text=True, check=True).stderr


def main() -> None:
    print("Sintetizando música…")
    write(MUSIC, build_music() * 0.8)
    print("Sintetizando efectos…")
    write(SFX, build_sfx() * 0.9)

    # Música: suave, opaca, con reverb, a -26 LUFS; se agacha bajo la voz (sidechain).
    # Efectos: con un poco de sala. Todo a -14 LUFS al final.
    graph = (
        "[1:a]lowpass=f=2200,aecho=0.8:0.7:90|160:0.25|0.18,loudnorm=I=-26:TP=-6:LRA=11[mus];"
        "[0:a]asplit=2[v][vsc];"
        "[mus][vsc]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=600[duck];"
        "[2:a]aecho=0.8:0.6:60|130:0.2|0.12,volume=0.9[fx];"
        "[v][duck][fx]amix=inputs=3:normalize=0:duration=first,"
        "loudnorm=I=-14:TP=-1.5:LRA=11[out]"
    )
    run("-i", str(VOICE), "-i", str(MUSIC), "-i", str(SFX), "-filter_complex", graph, "-map", "[out]",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(FINAL))
    stats = run("-i", str(FINAL), "-af", "ebur128=peak=true", "-f", "null", "-")
    print(stats[stats.rindex("Summary:"):].strip())
    print(f"→ {FINAL}")


if __name__ == "__main__":
    main()
