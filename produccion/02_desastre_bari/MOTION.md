# MOTION.md: living illustrations in this project (`02_desastre_bari`)

> Copy this file next to the project's art and fill in **Part 2** as you learn the project. Part 1 is the method and stays as it is. The `rossark-motion-skill` reads this file first, and Part 2 overrides the skill's defaults.

---

## Part 1. The method

**The goal:** anything drawn (a character, a plant, a flame, a street, a logo, a chart) feels alive and calm. Nothing teleports, nothing bounces, nothing shouts.

### Principles
1. **Never teleport:** interpolate everything; never swap drawings.
2. **Calm by default:** strong curves, no bouncy overshoot.
3. **Small amplitudes:** when unsure, halve it.
4. **Arcs and pivots:** each moving part is a layer rotating around its joint (stem base, hinge, neck, hook).
5. **Overlap and follow-through:** tips and trailing parts move later and further; give each part the same wave with a growing phase delay.
6. **Variety without chaos:**
   - repeated items get a seeded phase, speed and size;
   - nothing moves in sync, and there's no random value per frame.
7. **One main action per scene, plus two or three idle loops.** Side things stay quiet.
8. **Opacity only to appear or disappear.**
9. **The layout never moves:** motion lives inside the drawing.
10. **Reduced motion:** loops freeze on a good frame 0, and one-shots show their final frame.
11. **Nothing runs unseen:** pause off screen, when hidden and in the background.
12. **Enough frames:** anything under ~100 ms flickers at 30 fps; render and export at 60 when you can. Blinks close in ~110 ms and reopen in ~190 ms.

---

## Part 2. This project (`02_desastre_bari`)

### Where the code is
- **Platform:** Python offline vector/canvas renderer (`1080x1920 @ 60fps`) + `ffmpeg-skill` verification and packaging pipeline.
- **Motion engine and live face:** Ported 1:1 from `rossark-motion-skill` (`EASE_IN_OUT`, `EASE_OUT`, `EASE_IN`, `track`, `flow`, `seg`, `wave`, `loop_p`, `bell`, `seeded`, `draw_rossark_character`).
- **Art kit, characters, poses (`1080×1920`, Stage `Y = 580..1490`):**
  1. **Mariscal Británico Arthur Coningham (`role="coningham"`):** RAF blue-grey uniform, gold wings badge, confident/dismissive expression (`smug` brow, waving hand dismissing German air attack).
  2. **Médico del Puerto (`role="port_doctor"`):** White medical coat with Red Cross armband, worried brow, holding blanket over poisoned sailor.
  3. **Marinero Aliado Herido (`role="sailor_victim"`):** Covered in dark oil + yellow mustard-gas droplets, heavy closed eyelids (`lid = 0.88`, blinded by mustard gas vapor), shivering.
  4. **Teniente Coronel Médico Dr. Stewart Alexander (`role="alexander"`):** US Army Medical Corps olive uniform, focused investigator gaze (`lookX`/`lookY` inspecting blood cells & medical dossier), raising his articulated arm to order immediate decontamination washing.
  5. **Primer Ministro Winston Churchill (`role="churchill"`):** Dark pinstripe suit, bow tie, censoring "GAS MOSTAZA" from British archives.

### The owner's rules
- Zero image jitter/tremor (`PHOTOS_STEADY_STAGE` pre-composited once at startup).
- Practically all storytelling backed by custom 2D vector / SVG-style motion graphics and `rossark-motion-skill` living 2.5D characters, travelling water waves, rising toxic smoke wisps (`bell(p)`), falling bombs (`seeded(i)`), microscopic white-blood-cell / tumor-cell animation, and waiting-to-be-tapped jiggle buttons.
- Verified with `ffmpeg-skill` (`probe.py`, `check.py --platform shorts`, `look.py --safe tiktok`).
