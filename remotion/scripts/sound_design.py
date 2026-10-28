"""Música ambiental y efectos de sonido sintetizados desde cero (sin samples ni pistas de terceros),
así que no hay Content ID ni licencias que reclamar: todo es material original del canal.

Uso:
  python scripts/sound_design.py <carpeta> <voz.wav> <salida.wav>
  p. ej. python scripts/sound_design.py 05_isla_kiska audio/audio_master_censurado.wav audio/audio_final_mix.wav

Lee produccion/<carpeta>/audio/cues.json (lo genera scripts/cues.ts) para sincronizar los efectos
con los cortes, titulares, datos, mapas y radar del video. La música baja sola cuando habla la voz.
"""

import json
import sys
import wave
from pathlib import Path

import numpy as np

SR = 48000
rng = np.random.default_rng(1943)

# --- Niveles (lineales, sobre señales normalizadas a pico 1) ----------------------------------
MUSIC_UNDER_VOICE_DB = -17  # RMS de la música con voz encima, relativo a la voz
MUSIC_DUCK_DB = -7  # cuánto baja la música mientras habla la voz
GAIN = {
    "impact": 0.32, "cut": 0.05, "count": 0.07, "typewriter": 0.10, "marker": 0.07,
    "arrow": 0.09, "ships": 0.11, "horn": 0.13, "sea": 0.09, "wind": 0.09, "flashes": 0.22,
    "crossfire": 0.14, "radar": 0.11, "option": 0.18, "cta": 0.14,
}


# --- Utilidades ---------------------------------------------------------------------------
def secs(n):
    return np.arange(int(n * SR)) / SR


def noise(dur):
    return rng.standard_normal(int(dur * SR))


def band(x, lo, hi, soft=0.15):
    """Filtro pasabanda en frecuencia con bordes suaves (lo/hi en Hz)."""
    n = len(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    X = np.fft.rfft(x)
    lo_w = 1 / (1 + (lo / np.maximum(f, 1)) ** (1 / soft * 0.5)) if lo > 0 else 1
    hi_w = 1 / (1 + (f / hi) ** (1 / soft * 0.5)) if hi else 1
    return np.fft.irfft(X * lo_w * hi_w, n)


def norm(x):
    p = np.max(np.abs(x))
    return x / p if p > 0 else x


def decay(dur, tau, attack=0.004):
    t = secs(dur)
    return np.minimum(1, t / attack) * np.exp(-t / tau)


def fftconv(x, ir):
    n = len(x) + len(ir) - 1
    size = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[:n]


def reverb(x, length=2.5, wet=0.35, tone=4000):
    ir = band(noise(length), 0, tone) * np.exp(-secs(length) / (length / 6.9))
    ir = norm(ir) * 0.25
    y = fftconv(x, ir)[: len(x) + len(ir)]
    out = np.zeros(len(y))
    out[: len(x)] += x * (1 - wet)
    return out + norm(y) * np.max(np.abs(x)) * wet


def stereo(x, pan=0.0, width=0.0):
    """pan -1..1; width agrega un pequeño retardo al canal derecho para abrir la imagen."""
    l = x * np.cos((pan + 1) * np.pi / 4)
    r = x * np.sin((pan + 1) * np.pi / 4)
    if width:
        d = int(width * SR)
        r = np.concatenate([np.zeros(d), r[:-d]]) if d else r
    return np.stack([l, r], 1)


def place(buf, sig, t, gain):
    i = int(t * SR)
    if i >= len(buf):
        return
    if sig.ndim == 1:
        sig = stereo(sig)
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


# --- Música: pad oscuro en re menor, sin melodía, para no competir con la voz -------------------
NOTE = lambda name: 440 * 2 ** ((name - 69) / 12)  # MIDI → Hz
CHORDS = [  # Dm, B♭, Gm, A  (graves + tríada media)
    [38, 50, 53, 57], [34, 50, 53, 58], [31, 50, 55, 58], [33, 49, 52, 57],
]
CHORD_LEN = 8.0


def pad_voice(freq, dur, detune):
    t = secs(dur)
    out = np.zeros(len(t))
    for d in (-detune, 0, detune):
        f = freq * 2 ** (d / 1200)
        ph = rng.uniform(0, 2 * np.pi)
        for k in range(1, 7):  # sierra suave aproximada
            out += np.sin(2 * np.pi * f * k * t + ph * k) / k**1.6
    return out


def music_bed(total):
    n = int(total * SR)
    left, right = np.zeros(n), np.zeros(n)
    fade = 2.0
    t0, i = 0.0, 0
    while t0 < total:
        notes = CHORDS[i % len(CHORDS)]
        dur = CHORD_LEN + fade
        env = np.ones(int(dur * SR))
        ramp = int(fade * SR)
        env[:ramp] = np.sin(np.linspace(0, np.pi / 2, ramp)) ** 2
        env[-ramp:] = np.cos(np.linspace(0, np.pi / 2, ramp)) ** 2
        for side, buf in ((-1, left), (1, right)):
            seg = sum(pad_voice(NOTE(m), dur, 7 + side * 2) * (1.4 if m < 40 else 1) for m in notes) * env
            a = int(t0 * SR)
            b = min(n, a + len(seg))
            buf[a:b] += seg[: b - a]
        # campana suave al empezar cada acorde
        top = NOTE(notes[-1] + 12)
        bell = (np.sin(2 * np.pi * top * secs(3.5)) + 0.4 * np.sin(2 * np.pi * top * 2.76 * secs(3.5))) * decay(3.5, 1.1, 0.01)
        a = int(t0 * SR)
        for buf in (left, right):
            b = min(n, a + len(bell))
            buf[a:b] += bell[: b - a] * 0.9
        t0 += CHORD_LEN
        i += 1
    left, right = band(left, 45, 1600), band(right, 45, 1600)
    # pulso grave muy lento, como latido lejano
    t = np.arange(n) / SR
    drone = np.sin(2 * np.pi * NOTE(26) * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t))
    left, right = left + drone * 1.5, right + drone * 1.5
    out = np.stack([reverb(left, 3.5, 0.45, 2500)[:n], reverb(right, 3.5, 0.45, 2500)[:n]], 1)
    # entrada y salida suaves
    f_in, f_out = int(1.5 * SR), int(3 * SR)
    out[:f_in] *= np.linspace(0, 1, f_in)[:, None]
    out[-f_out:] *= np.linspace(1, 0, f_out)[:, None]
    return out


# --- Efectos -------------------------------------------------------------------------------
def sfx_impact():
    d = 2.0
    t = secs(d)
    f = 38 + 55 * np.exp(-t / 0.12)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * decay(d, 0.55)
    hit = band(noise(d), 0, 350) * decay(d, 0.09)
    return reverb(norm(sub + 0.6 * norm(hit)), 2.2, 0.3, 1500)


def sfx_whoosh(dur=0.45, lo=600, hi=5000):
    x = noise(dur)
    t = secs(dur)
    env = np.sin(np.pi * t / dur) ** 2
    return norm(band(x, lo, hi) * env)


def sfx_click():
    x = band(noise(0.012), 1500, 7000) * decay(0.012, 0.002, 0.0005)
    thump = np.sin(2 * np.pi * 180 * secs(0.012)) * decay(0.012, 0.004, 0.0005)
    return norm(x + 0.5 * thump)


def sfx_count():
    # 12 tics que se van espaciando (sigue el conteo con easing) + un «ding» final
    out = np.zeros(int(1.3 * SR))
    for k in range(12):
        p = k / 11
        t = 0.7 * (1 - (1 - p) ** (1 / 3))
        i = int(t * SR)
        c = sfx_click()
        out[i : i + len(c)] += c * 0.6
    ding = np.sin(2 * np.pi * 1568 * secs(0.5)) * decay(0.5, 0.15)
    i = int(0.72 * SR)
    out[i : i + len(ding)] += ding * 0.5
    return norm(out)


def sfx_typewriter(chars):
    dur = 4 / 60 + chars * 1.4 / 60
    out = np.zeros(int((dur + 0.1) * SR))
    for k in range(0, chars, 2):
        i = int((4 / 60 + k * 1.4 / 60 + rng.uniform(0, 0.01)) * SR)
        c = sfx_click() * rng.uniform(0.6, 1)
        out[i : i + len(c)] += c
    return norm(out)


def sfx_marker():
    t = secs(0.35)
    x = (np.sin(2 * np.pi * 880 * t) + 0.5 * np.sin(2 * np.pi * 1320 * t)) * decay(0.35, 0.08)
    return reverb(norm(x), 0.8, 0.25)


def sfx_arrow(dur):
    x = sfx_whoosh(dur, 300, 3000)
    t = secs(dur)
    tone = np.sin(2 * np.pi * np.cumsum(120 + 180 * t / dur) / SR) * np.sin(np.pi * t / dur) ** 2
    return norm(x + 0.3 * tone)


def sfx_rumble(dur, lo=35, hi=160, mod=5.5):
    t = secs(dur)
    x = band(noise(dur), lo, hi) * (0.7 + 0.3 * np.sin(2 * np.pi * mod * t))
    env = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.8)
    return norm(x * env)


def sfx_horn():
    d = 2.6
    t = secs(d)
    env = np.minimum(1, t / 0.25) * np.minimum(1, np.maximum(0, (2.0 - t)) / 0.5)
    x = sum(np.sin(2 * np.pi * f * k * t) / k for f in (110, 164.8) for k in range(1, 9))
    return reverb(norm(band(x * env, 60, 900)), 3.0, 0.4, 1200)


def sfx_ambience(dur, lo, hi, slow):
    t = secs(dur)
    x = band(noise(dur), lo, hi) * (0.55 + 0.45 * np.sin(2 * np.pi * slow * t + rng.uniform(0, 6)))
    env = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 0.8)
    return norm(x * env)


def sfx_distant_boom():
    d = 1.4
    x = band(noise(d), 0, 180) * decay(d, 0.35, 0.01)
    sub = np.sin(2 * np.pi * 42 * secs(d)) * decay(d, 0.4, 0.01)
    return reverb(norm(x + 0.7 * sub), 2.0, 0.4, 600)


def sfx_gunshot():
    d = 0.5
    crack = band(noise(d), 800, 6000) * decay(d, 0.008, 0.0005)
    body = band(noise(d), 80, 900) * decay(d, 0.06, 0.001)
    return reverb(norm(crack + body), 1.2, 0.45, 3000)


def sfx_ping():
    d = 2.2
    t = secs(d)
    x = np.sin(2 * np.pi * 1050 * t) * decay(d, 0.45, 0.003)
    echo = np.concatenate([np.zeros(int(0.32 * SR)), x * 0.35])[: len(x)]
    return reverb(norm(x + echo), 1.5, 0.35)


def sfx_cta():
    t = secs(1.6)
    x = sum(np.sin(2 * np.pi * f * t) * decay(1.6, 0.5, 0.005) for f in (1174.7, 1568))
    return reverb(norm(x), 1.5, 0.3)


def build_sfx(cues, total):
    n = int(total * SR)
    fx = np.zeros((n, 2))
    amb = np.zeros((n, 2))  # ambientes largos: se agachan un poco con la voz
    for c in cues:
        t, k, dur = c["t"], c["kind"], c.get("dur", 0)
        if k == "cut":
            place(fx, stereo(sfx_whoosh(), rng.uniform(-0.4, 0.4)), max(0, t - 0.2), GAIN["cut"])
        elif k == "impact":
            place(fx, stereo(sfx_impact(), 0, 0.012), t, GAIN["impact"])
        elif k == "count":
            place(fx, stereo(sfx_count(), -0.3), t, GAIN["count"])
        elif k == "typewriter":
            place(fx, stereo(sfx_typewriter(c["n"]), -0.5), t, GAIN["typewriter"])
        elif k == "marker":
            place(fx, stereo(sfx_marker(), 0.2, 0.01), t, GAIN["marker"])
        elif k == "arrow":
            place(fx, stereo(sfx_arrow(dur), 0, 0.008), t, GAIN["arrow"])
        elif k == "ships":
            place(amb, stereo(sfx_rumble(dur + 1.0), 0, 0.01), t, GAIN["ships"])
            place(fx, stereo(sfx_horn(), -0.2, 0.015), t, GAIN["horn"])
        elif k == "sea":
            place(amb, stereo(sfx_ambience(dur, 60, 700, 0.11), 0, 0.02), t, GAIN["sea"] * c.get("n", 1))
        elif k == "wind":
            place(amb, stereo(sfx_ambience(dur, 250, 1800, 0.18), 0, 0.02), t, GAIN["wind"] * c.get("n", 1))
        elif k == "flashes":
            for j in range(int(dur / 0.45)):
                place(fx, stereo(sfx_distant_boom(), rng.uniform(-0.6, 0.6), 0.01), t + j * 0.45, GAIN["flashes"] * rng.uniform(0.5, 1))
        elif k == "crossfire":
            tt = t + 0.1
            while tt < t + dur - 0.3:
                place(fx, stereo(sfx_gunshot(), rng.uniform(-0.8, 0.8)), tt, GAIN["crossfire"] * rng.uniform(0.4, 1))
                tt += rng.uniform(0.07, 0.32)
        elif k == "radar":
            for j in range(int(dur / 2.4) + 1):
                place(fx, stereo(sfx_ping(), 0, 0.01), t + j * 2.4, GAIN["radar"])
            place(amb, stereo(sfx_rumble(dur, 50, 70, 0.5)), t, GAIN["radar"] * 0.5)
        elif k == "option":
            place(fx, stereo(sfx_impact(), 0, 0.012), t, GAIN["option"])
        elif k == "cta":
            place(fx, stereo(sfx_cta(), 0, 0.01), t, GAIN["cta"])
    return fx, amb


# --- Mezcla --------------------------------------------------------------------------------
def read_wav(p):
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR, "la voz tiene que estar a 48 kHz"
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
        return x.reshape(-1, w.getnchannels())


def write_wav(p, x):
    with wave.open(str(p), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def voice_envelope(voice, n):
    """1 mientras hay voz, 0 en silencio; ataque rápido y liberación lenta."""
    mono = np.abs(voice).mean(1)
    hop = int(0.01 * SR)
    frames = np.array([np.sqrt(np.mean(mono[i : i + hop] ** 2)) for i in range(0, len(mono), hop)])
    active = (20 * np.log10(frames + 1e-9) > -45).astype(float)
    env = np.zeros_like(active)
    for i in range(len(active)):
        prev = env[i - 1] if i else 0
        env[i] = prev + (active[i] - prev) * (0.5 if active[i] > prev else 0.03)
    full = np.repeat(env, hop)[:n]
    return np.pad(full, (0, max(0, n - len(full))))


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x**2)) + 1e-12)


def main():
    folder, voice_rel, out_rel = sys.argv[1:4]
    base = Path(__file__).resolve().parents[2] / "produccion" / folder
    data = json.loads((base / "audio" / "cues.json").read_text(encoding="utf-8"))
    total = data["total"]
    n = int(total * SR)

    voice = read_wav(base / voice_rel)
    if voice.shape[1] == 1:
        voice = np.repeat(voice, 2, 1)
    voice = np.pad(voice, ((0, max(0, n - len(voice))), (0, 0)))[:n]
    duck = voice_envelope(voice, n)
    speaking = duck > 0.5
    voice_level = rms_db(voice[speaking])

    print("musica...")
    music = music_bed(total)
    music *= 10 ** ((voice_level + MUSIC_UNDER_VOICE_DB - MUSIC_DUCK_DB - rms_db(music)) / 20)
    music *= (1 - duck * (1 - 10 ** (MUSIC_DUCK_DB / 20)))[:, None]

    print("efectos...")
    fx, amb = build_sfx(data["cues"], total)
    amb *= (1 - duck * 0.4)[:, None]

    mix = voice + music + fx + amb
    peak = np.max(np.abs(mix))
    if peak > 0.98:
        mix *= 0.98 / peak
    write_wav(base / out_rel, mix)
    print(f"voz {voice_level:.1f} dB, musica {rms_db(music[speaking]):.1f} dB bajo voz, pico {20*np.log10(peak):.1f} dBFS")
    print(f"-> produccion/{folder}/{out_rel}")


if __name__ == "__main__":
    main()
