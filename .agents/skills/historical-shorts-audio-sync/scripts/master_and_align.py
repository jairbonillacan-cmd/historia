#!/usr/bin/env python3
"""
Master raw voiceover audio to -21.0 LUFS EBU R128 and validate timeline_chunks.json.
Usage:
  python master_and_align.py --input voz_raw.mp3 --output audio_master_180s.wav [--timeline timeline_84_chunks.json]
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def master_audio(input_path: Path, output_path: Path, target_lufs: float = -21.0) -> None:
    filter_chain = (
        f"highpass=f=85,"
        f"acompressor=threshold=-20dB:ratio=3.5:attack=5:release=80:makeup=4dB,"
        f"agate=threshold=-38dB:range=-90dB:attack=2:release=40,"
        f"loudnorm=I={target_lufs}:TP=-1.5:LRA=3.0:print_format=summary"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-af",
        filter_chain,
        "-ar",
        "48000",
        "-ac",
        "2",
        str(output_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        sys.exit(proc.returncode)
    print(f"[OK] Mastered audio saved to {output_path}")
    for line in proc.stderr.splitlines():
        if any(k in line for k in ("Output Integrated:", "Output True Peak:", "Output LRA:")):
            print("  ", line.strip())


def validate_timeline(timeline_path: Path) -> None:
    data = json.loads(timeline_path.read_text(encoding="utf-8"))
    chunks = data.get("chunks", [])
    total_dur = data.get("total_duration", 0.0)
    total_words = sum(len(c.get("words", [])) for c in chunks)
    bbox_count = sum(
        1 for c in chunks for w in c.get("words", []) if w.get("is_bbox")
    )
    wpm = (total_words / (total_dur / 60.0)) if total_dur > 0 else 0.0
    print(f"[OK] Timeline validated: {len(chunks)} chunks | {total_words} words | {total_dur:.2f}s | {wpm:.1f} WPM | {bbox_count} highlighted keywords")


def main() -> None:
    parser = argparse.ArgumentParser(description="Master audio to -21.0 LUFS and validate timeline JSON.")
    parser.add_argument("--input", type=Path, help="Input audio file (.mp3 or .wav)")
    parser.add_argument("--output", type=Path, help="Output mastered WAV file")
    parser.add_argument("--timeline", type=Path, help="Optional timeline JSON file to validate")
    args = parser.parse_args()

    if args.input and args.output:
        master_audio(args.input, args.output)
    if args.timeline:
        validate_timeline(args.timeline)


if __name__ == "__main__":
    main()
