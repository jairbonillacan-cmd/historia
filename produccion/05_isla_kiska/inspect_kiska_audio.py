import os
import re
import shutil
import subprocess

os.makedirs("produccion/05_isla_kiska/audio", exist_ok=True)
os.makedirs("produccion/05_isla_kiska/assets", exist_ok=True)

src_mp3 = "C:/Users/T490s/.gemini/antigravity/brain/36fea9b5-e96c-454f-b457-5781a7819722/.user_uploaded/uploaded_media_1793136218377.mp3"
dst_mp3 = "produccion/05_isla_kiska/audio/voz_raw.mp3"
shutil.copy2(src_mp3, dst_mp3)
print(f"Copied {src_mp3} -> {dst_mp3} ({os.path.getsize(dst_mp3)} bytes)")

for min_d in [0.08, 0.12, 0.15, 0.20]:
    for noise_db in ["-35dB", "-30dB"]:
        res = subprocess.run([
            "ffmpeg", "-i", dst_mp3, "-af", f"silencedetect=noise={noise_db}:d={min_d}", "-f", "null", "-"
        ], capture_output=True, text=True, encoding="utf-8", errors="replace")

        silences = []
        cur_start = None
        for line in res.stderr.splitlines():
            if "silence_start:" in line:
                m = re.search(r"silence_start:\s*([0-9.]+)", line)
                if m: cur_start = float(m.group(1))
            elif "silence_end:" in line and cur_start is not None:
                m_e = re.search(r"silence_end:\s*([0-9.]+)", line)
                m_d = re.search(r"silence_duration:\s*([0-9.]+)", line)
                if m_e and m_d:
                    silences.append((cur_start, float(m_e.group(1)), float(m_d.group(1))))
                    cur_start = None

        m_dur = re.search(r"Duration:\s*(\d+):(\d+):([0-9.]+)", res.stderr)
        total_dur = int(m_dur.group(1))*3600 + int(m_dur.group(2))*60 + float(m_dur.group(3))
        raw_chunks = []
        prev_end = 0.0
        for s_start, s_end, s_dur in silences:
            if s_start > prev_end + 0.04:
                raw_chunks.append((prev_end, s_start, s_dur))
            prev_end = s_end
        if total_dur > prev_end + 0.04:
            raw_chunks.append((prev_end, total_dur, 0.0))
        print(f"[noise={noise_db}, d={min_d}] Raw duration: {total_dur:.2f}s | Chunks: {len(raw_chunks)} | Total silence: {sum(s[2] for s in silences):.2f}s")
        if noise_db == "-30dB" and min_d in (0.12, 0.15):
            for i, (cs, ce, cd) in enumerate(raw_chunks):
                print(f"  Chunk {i+1:02d}: {cs:6.2f}s -> {ce:6.2f}s (dur={ce-cs:4.2f}s, sil_after={cd:4.2f}s)")
