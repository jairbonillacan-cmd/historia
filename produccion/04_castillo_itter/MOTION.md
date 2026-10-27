# MOTION.md: living illustrations in this project (`04_castillo_itter`)

> This file documents the motion engine, character rigs, and project-specific rules for `produccion/04_castillo_itter` (AG-13: *Castillo de Itter 1945 — El día que estadounidenses y alemanes pelearon juntos contra las SS*).

---

## Part 1. The method (`rossark-motion-skill`)

1. **Never teleport:** interpolate everything; never swap drawings abruptly.
2. **Calm by default:** use cubic-bezier curves (`EASE_IN_OUT (0.77, 0, 0.175, 1)`, `EASE_OUT (0.23, 1, 0.32, 1)`, `EASE_IN (0.55, 0, 1, 0.45)`) and monotone cubic Hermite splines (`flow()`).
3. **Arcs, pivots, and follow-through:** every articulated part rotates around its joint; child segments (`head`, `forearm`) lag behind their parent by `90–110 ms`.
4. **Variety without chaos:** repeated items (flames, smoke wisps, tracer rounds, snow/pine sway) use deterministic `seeded(i)` phases, never `random()` per frame.
5. **Steady archival plates (`0.0 px` tremor):** archival photographs are pre-composited once at startup (`PHOTOS_STEADY_STAGE`) and never resampled per frame. All motion lives in the vector layers drawn over or beside them.

---

## Part 2. This project (`04_castillo_itter`)

### Where the code is
- **Renderer:** `render_castillo_itter.py` (`1080×1920 @ 60fps` output, BT.709, `-14.0 LUFS` final Short MP4).
- **Audio & Alignment:** `produccion/04_castillo_itter/audio/audio_master_180s.wav` (`-21.0 LUFS` pre-master) + `produccion/04_castillo_itter/timeline_chunks.json` (49 clauses, 489 words, 48 `is_bbox` nuclear keywords, 40 distinct scenes).
- **Explosive Opening Hook (`Scenes 1..7`, `00:00 – 00:16.6`):**
  - 7 rapid-fire 1-to-1 visual cuts synced to the 7 opening clauses (*"Mirá esta escena"* -> *"tanque estadounidense en llamas"* -> *"disparando por las mismas ventanas"* -> *"soldados de Estados Unidos"* -> *"soldados del ejército alemán"* -> *"dos ex primeros ministros de Francia"* -> *"Todos peleando del mismo lado contra un enemigo común"*).
- **Characters (`draw_rossark_soldier`):**
  1. **Capitán John «Jack» Lee / Soldado de EE. UU. (`role="us_soldier"`):** US Army olive-drab uniform, M1 steel helmet with white star / captain bars, 2.5D head turn (`yaw`), realistic `110ms/40ms/190ms` `'out'` blinks, and articulated arms holding/aiming rifle.
  2. **Mayor Josef «Sepp» Gangl / Soldado de la Wehrmacht (`role="wehrmacht"`):** Feldgrau regular German army uniform, peaked officer field cap (`Bergmütze`), Iron Cross badge, 2.5D head turn (`yaw`), and articulated arms.
  3. **Ex Primer Ministro Francés Armado (`role="french_vip"`):** Paul Reynaud / Édouard Daladier in dark double-breasted statesman suit with French tricolor lapel cockade, holding a rifle at the crenellations of Castle Itter.
  4. **Efectivo de las Waffen-SS (`role="waffen_ss"`):** Dark charcoal/camouflage tunic and helmet in the surrounding pine forest.
  5. **Cocinero Andreas Krobot (`role="cyclist"`):** Riding his bicycle down the mountain road from Itter to Wörgl with bobbing frame and rotating spoked wheels.

### Verification commands
- `python .agents/skills/ffmpeg-skill/scripts/probe.py produccion/04_castillo_itter/castillo_itter_short.mp4 --json`
- `python .agents/skills/ffmpeg-skill/scripts/check.py produccion/04_castillo_itter/castillo_itter_short.mp4 --platform shorts --json`
- `python .agents/skills/ffmpeg-skill/scripts/look.py produccion/04_castillo_itter/castillo_itter_short.mp4 --tiles 4x3 --safe tiktok -o produccion/04_castillo_itter/ffmpeg_skill_look_sheet.png`
