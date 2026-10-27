---
name: historical-shorts-audio-sync
description: >-
  Local audio mastering, silence gating, diegetic pre-hook foley assembly, and
  word-level forced alignment pipeline for 180-second historical Shorts. Use
  this skill whenever the user provides a raw voiceover recording (e.g.
  voz_raw.mp3) and needs a broadcast-normalized -21.0 LUFS master WAV and a
  word-level timestamp JSON file (timeline_chunks.json) for Remotion rendering.
---

# Historical Documentary Shorts — Local Audio & Word-Level Sync Pipeline

Use this skill when processing a raw narration audio file (`voz_raw.mp3` or `.wav`) into a `180s` master track (`audio_master_180s.wav`) and a frame-accurate word-level alignment JSON (`timeline_chunks.json`).

---

## 1. Acoustic Architecture (3 Layers, 0% Background Music)

1. **Layer 1 — Diegetic Pre-Hook (`[00:00.00 – 00:02.00]`):**
   - Never start vocal narration at frame `0`.
   - Open with `1.6s – 2.5s` of **hyper-specific diegetic foley** at `-14 dB` (e.g., sonar ping, mechanical typewriter/cipher keys, polar wind in snow, telegraph Morse, or ticking clock) that fades out smoothly by `00:12`.
2. **Layer 2 — Dry A Capella Narration & Surgical Silences (`[00:02.00 – 02:57.00]`):**
   - **0% background music (`BGM`)** throughout the body of the Short.
   - Between spoken clauses, enforce a clean digital silence floor (`-inf dB`) using an audio gate (`agate`) or programmatic chunk assembly.
   - **4 Mandatory Dramatic Pauses per Video:**
     - **Gate Pause (End of Hook, `~00:14`):** `0.70s – 0.95s` of absolute silence before the date/location that opens the Context block.
     - **Adversative Turn Pause (`~00:58`):** `0.55s – 0.70s` before *"Pero había un problema"* / *"El problema era otro"*.
     - **Climax Pause (`~01:58`):** `0.65s – 0.85s` immediately before revealing the decisive order or outcome.
     - **Pre-Question Pause (`~02:48`):** `0.60s` before asking the second-person dilemma question.
3. **Layer 3 — Circular Acoustic Tail (`[02:57.00 – 03:00.00]`):**
   - After *"Contámelo en los comentarios"*, leave **`1.8s – 3.0s` of tail without voice** where the opening diegetic foley (`00:00`) resurfaces, creating a seamless acoustic loop when the Short replays.

---

## 2. Automated EBU R128 Mastering Chain (`-21.0 LUFS`)

Always normalize the assembled audio track using this exact FFmpeg filter chain:

```bash
ffmpeg -y -i assembled_pre_lufs.wav -af "\
highpass=f=85,\
acompressor=threshold=-20dB:ratio=3.5:attack=5:release=80:makeup=4dB,\
agate=threshold=-38dB:range=-90dB:attack=2:release=40,\
loudnorm=I=-21.0:TP=-1.5:LRA=3.0" \
-ar 48000 -ac 2 audio_master_180s.wav
```

---

## 3. Word-Level Alignment JSON Contract (`timeline_chunks.json`)

The Remotion visual engine consumes a JSON file structured into sentence/clause chunks (`3–7 words` per display group, or `1` short sentence per chunk) with millisecond-accurate `start` and `end` timestamps and `is_bbox` flags on `3–5` nuclear keywords per minute:

```json
{
  "total_duration": 179.26,
  "chunks": [
    {
      "index": 1,
      "scene_id": 1,
      "start": 1.85,
      "end": 4.516,
      "pause_after": 0.35,
      "text": "27 de octubre de 1962.",
      "bbox_word": "1962.",
      "words": [
        { "word": "27", "start": 1.85, "end": 2.146, "is_bbox": false },
        { "word": "de", "start": 2.146, "end": 2.442, "is_bbox": false },
        { "word": "octubre", "start": 2.442, "end": 3.479, "is_bbox": false },
        { "word": "de", "start": 3.479, "end": 3.775, "is_bbox": false },
        { "word": "1962.", "start": 3.775, "end": 4.516, "is_bbox": true }
      ]
    }
  ]
}
```

## 4. Helper Script

Run [scripts/master_and_align.py](./scripts/master_and_align.py) to master an input audio file to `-21.0 LUFS`, verify integrated loudness with `ffprobe`/`ffmpeg ebur128`, and validate or generate `timeline_chunks.json`.
