"""AG-15 · Cielo de Bremen (1943).

Arma audio/audio_master_159s.wav (voz natural 1.0x, -14 LUFS) y timeline_chunks.json.
Los tiempos de cada palabra salen de audio/whisper_words.json (faster-whisper, word_timestamps)
y el texto exacto del guion AG15, alineados palabra por palabra.

Uso (desde la raíz del repo): python produccion/06_cielo_bremen/build_audio_and_timeline_bremen.py
Después: cd remotion && npm run mute:bremen
"""
import difflib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("produccion/06_cielo_bremen")
RAW = BASE / "audio/voz_raw.mp3"
MASTER = BASE / "audio/audio_master_159s.wav"
WHISPER = BASE / "audio/whisper_words.json"
SCRIPT = Path("guiones_antigravity/elevenlabs/AG15.txt")
OUT = BASE / "timeline_chunks.json"

# Números dichos en letras → como se leen en pantalla.
NUMBERS = [
    ("mil novecientos cuarenta y tres", "1943"),
    ("veintiún", "21"),
    ("B diecisiete", "B-17"),
    ("quince", "15"),
    ("sesenta", "60"),
    ("veintisiete", "27"),
    ("ciento nueve", "109"),
    ("cuarenta", "40"),
    ("seis mil", "6.000"),
]

# Palabra nuclear de cada cláusula cuando la heurística no alcanza (texto exacto de la palabra).
BBOX_PREFERRED = {"colador.", "Stigler", "Brown", "paracaídas.", "conciencia?", "hermanos", "Suecia,", "Caballero,", "torniquetes"}

# Misma lista de raíces que remotion/src/engine/censor.ts: nunca llevan caja azul.
CENSORED = re.compile(
    r"(?<![^\W\d_])(muert|mat(ar|an|ó|aron|anza)|asesin|masacr|suicid|carnicer|sangr|cadáver|ejecut|tortur|nazi|"
    r"fusil(a|an|ar|aron|ado|ados|amiento)|paredón|rematar)",
    re.I,
)
STOP = set("el la los las un una de del en y a al que se su sus por para con sin ese esa lo le no si ya ha es más".split())

MAX_GROUP = 4      # palabras por bloque del subtítulo
MAX_CHUNK = 12     # palabras por cláusula antes de partir en una coma


def norm(w: str) -> str:
    w = unicodedata.normalize("NFD", w.lower())
    return "".join(c for c in w if c.isalnum() and not unicodedata.combining(c))


def script_words() -> list[str]:
    text = SCRIPT.read_text(encoding="utf-8")
    text = re.sub(r"\[[^\]]+\]", " ", text)
    for spoken, shown in NUMBERS:
        text = re.sub(rf"\b{spoken}\b", shown, text)
    text = text.replace("Brown, de apenas", "Brown de apenas")
    return text.split()


def whisper_words() -> list[dict]:
    segs = json.loads(WHISPER.read_text(encoding="utf-8"))
    return [w for s in segs for w in s["words"] if norm(w["word"])]


def align(script: list[str], heard: list[dict]) -> list[tuple[float, float]]:
    """Tiempos para cada palabra del guion. Las que whisper oyó distinto toman el tramo de lo que oyó."""
    a = [norm(w) for w in script]
    b = [norm(w["word"]) for w in heard]
    times: list[tuple[float, float] | None] = [None] * len(script)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                times[i1 + k] = (heard[j1 + k]["start"], heard[j1 + k]["end"])
        elif op == "replace":
            t0, t1 = heard[j1]["start"], heard[j2 - 1]["end"]
            lens = [max(1, len(a[i])) for i in range(i1, i2)]
            acc, total = 0, sum(lens)
            for k, n in enumerate(lens):
                times[i1 + k] = (t0 + (t1 - t0) * acc / total, t0 + (t1 - t0) * (acc + n) / total)
                acc += n
            print(f"  ~ {' '.join(script[i1:i2])}  ←  {' '.join(w['word'] for w in heard[j1:j2])}")
        elif op == "delete":
            print(f"  ? sin audio: {' '.join(script[i1:i2])}")
    # Lo que whisper no oyó se reparte entre los vecinos.
    for i, t in enumerate(times):
        if t is None:
            prev_end = times[i - 1][1] if i else 0.0
            nxt = next((times[j][0] for j in range(i + 1, len(times)) if times[j]), prev_end + 0.3)
            times[i] = (prev_end, max(prev_end + 0.05, nxt))
    return times  # type: ignore[return-value]


def split_chunks(words: list[str]) -> list[list[int]]:
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        end_sentence = w[-1] in ".?:"
        soft = w.endswith(",") and len(cur) >= 6
        if end_sentence or (soft and len(cur) + remaining_in_sentence(words, i) > MAX_CHUNK):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def remaining_in_sentence(words: list[str], i: int) -> int:
    n = 0
    for w in words[i + 1:]:
        n += 1
        if w[-1] in ".?:":
            break
    return n


def groups(idx: list[int], words: list[str]) -> list[int]:
    """Bloques de hasta MAX_GROUP palabras, cortando en las comas."""
    out, g, n = [], 0, 0
    for k, i in enumerate(idx):
        if n == MAX_GROUP:
            g, n = g + 1, 0
        out.append(g)
        n += 1
        if words[i].endswith(",") and k < len(idx) - 1:
            g, n = g + 1, 0
    return out


def pick_bbox(ws: list[str]) -> int:
    def score(k: int) -> float:
        w = ws[k]
        clean = w.strip("¿?.,:;")
        if CENSORED.search(clean) or norm(clean) in STOP:
            return -1
        s = len(norm(clean)) * 0.1
        if w in BBOX_PREFERRED:
            s += 5
        if any(c.isdigit() for c in clean):
            s += 4
        if clean[:1].isupper() and k > 0:
            s += 2
        return s
    return max(range(len(ws)), key=score)


def master_audio() -> float:
    """Voz a -14 LUFS sin tocar velocidad ni tono (loudnorm en dos pasadas, modo lineal)."""
    probe = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(RAW), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    ).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    af = (
        "loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:"
        f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
        f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}"
    )
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(RAW), "-af", af, "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(MASTER)],
        check=True,
    )
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(MASTER)],
        capture_output=True, text=True, check=True,
    ).stdout)
    return dur


def main() -> None:
    words = script_words()
    heard = whisper_words()
    print(f"Guion: {len(words)} palabras · whisper: {len(heard)}")
    times = align(words, heard)

    chunks = []
    for n, idx in enumerate(split_chunks(words), start=1):
        ws = [words[i] for i in idx]
        gs = groups(idx, words)
        b = pick_bbox(ws)
        chunks.append({
            "index": n,
            "scene_id": n,
            "start": round(times[idx[0]][0], 3),
            "end": round(times[idx[-1]][1], 3),
            "text": " ".join(ws),
            "bbox_word": ws[b],
            "words": [
                {"word": w, "start": round(times[i][0], 3), "end": round(times[i][1], 3), "is_bbox": k == b, "group_id": gs[k]}
                for k, (i, w) in enumerate(zip(idx, ws))
            ],
        })

    dur = master_audio()
    OUT.write_text(json.dumps({"total_duration": round(dur, 2), "chunks": chunks}, ensure_ascii=False, indent=2), encoding="utf-8")
    for c in chunks:
        print(f"{c['index']:>3} {c['start']:7.2f}–{c['end']:7.2f}  {c['text']}")
    print(f"{len(chunks)} cláusulas · {dur:.2f} s → {OUT} · {MASTER}")


if __name__ == "__main__":
    main()
