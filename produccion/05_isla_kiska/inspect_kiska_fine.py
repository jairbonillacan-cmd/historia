import subprocess
import wave
import struct

raw_mp3 = "produccion/05_isla_kiska/audio/voz_raw.mp3"
clean_wav = "produccion/05_isla_kiska/audio/voz_clean.wav"

subprocess.run([
    "ffmpeg", "-y", "-i", raw_mp3,
    "-af", "highpass=f=85",
    "-ar", "48000", "-ac", "1", clean_wav
], capture_output=True, check=True)

with wave.open(clean_wav, "rb") as wf:
    sr = wf.getframerate()
    raw_bytes = wf.readframes(wf.getnframes())
    samples = struct.unpack(f"<{len(raw_bytes)//2}h", raw_bytes)

def find_dips(t0, t1, win_ms=25, thresh_rms=350):
    w = int(sr * win_ms / 1000)
    s0 = int(t0 * sr)
    s1 = int(t1 * sr)
    dips = []
    in_dip = False
    d_start = 0.0
    for idx in range(s0, s1 - w, w // 2):
        chunk = samples[idx:idx+w]
        rms = (sum(x*x for x in chunk) / len(chunk)) ** 0.5
        t = idx / sr
        if rms < thresh_rms:
            if not in_dip:
                in_dip = True
                d_start = t
        else:
            if in_dip:
                in_dip = False
                if t - d_start >= 0.04:
                    dips.append((round(d_start, 3), round(t, 3), round(t - d_start, 3)))
    if in_dip:
        dips.append((round(d_start, 3), round(t1, 3), round(t1 - d_start, 3)))
    return dips

for label, a, b in [
    ("Hook 1 (0.00-4.01)", 0.00, 4.01),
    ("Hook 2 (4.19-7.50)", 4.19, 7.50),
    ("Pentagono (47.35-53.37)", 47.35, 53.37),
    ("Tres semanas (58.81-65.51)", 58.81, 65.51),
    ("Kimura (77.74-83.03)", 77.74, 83.03),
    ("5183 soldados (91.66-97.22)", 91.66, 97.22),
    ("Bombarderos (101.49-108.18)", 101.49, 108.18),
    ("15 agosto (116.47-122.13)", 116.47, 122.13),
    ("Patrullas (128.18-132.75)", 128.18, 132.75),
    ("34000 hombres (154.75-159.72)", 154.75, 159.72),
]:
    print(f"=== {label} ===")
    for ds, de, dd in find_dips(a, b, win_ms=20, thresh_rms=420):
        print(f"  dip: {ds:.3f}s -> {de:.3f}s ({dd:.3f}s)")
