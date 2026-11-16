"""Transcribe una locución con tiempos por palabra (faster-whisper, CPU).

Uso: python produccion/transcribir_whisper.py <audio> <salida.json> [modelo=small]
Imprime cada frase con su tiempo y guarda [{start, end, text, words:[{word, start, end, p}]}].

El audio se decodifica con ffmpeg y se pasa como array: la versión de PyAV instalada no
acepta el argumento que faster-whisper le pasa al abrir archivos.
"""
import json
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding="utf-8")

src, out = sys.argv[1], sys.argv[2]
model = WhisperModel(sys.argv[3] if len(sys.argv) > 3 else "small", device="cpu", compute_type="int8")
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
segments, _ = model.transcribe(np.frombuffer(pcm, np.float32), language="es", word_timestamps=True, beam_size=5)

result = []
for s in segments:
    result.append({
        "start": s.start,
        "end": s.end,
        "text": s.text.strip(),
        "words": [{"word": w.word.strip(), "start": w.start, "end": w.end, "p": w.probability} for w in s.words],
    })
    print(f"{s.start:7.2f} {s.text.strip()}", flush=True)

with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
