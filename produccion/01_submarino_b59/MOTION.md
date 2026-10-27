# MOTION.md: living illustrations in this project

> Copy this file next to the project's art (for example `src/art/MOTION.md`) and fill in **Part 2** as you learn the project. Part 1 is the method and stays as it is. The `rossark-motion-skill` reads this file first, and Part 2 overrides the skill's defaults.

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
13. **Interface rules:**
    - frequency decides how much (often seen = barely moves; rare moments get the delight);
    - every motion has a purpose;
    - shared elements travel, never teleport;
    - interface moves stay under 300 ms;
    - exits are faster than entrances;
    - nothing appears from scale 0;
    - interruptions continue from the current value.

### The engine
- **Clocks:** a loop clock for idle life, a one-shot clock for a scene that tells an action. One per character, group or scene.
- **Tracks:** keyframes `[ms, value, 'out'?]` read with `track(t, keys)`. The last key equals the first. `track` stops at every key, so use it for one move (a blink, a lid). For acting (a chain of poses), use `flow(t, keys)`, which passes through the keys without stopping and never overshoots.
- **Helpers:**
  - `wave` (−1 to 1), for sway and breathing;
  - `loop` (0 to 1), for drift and falling;
  - `bell`, to fade in and out;
  - `seg`, for one beat of a one-shot;
  - `seeded(i)`, for per-item variety.
- **Curves:**
  - travel uses ease-in-out `(0.77, 0, 0.175, 1)`;
  - open and arrive use ease-out `(0.23, 1, 0.32, 1)`;
  - leaving uses ease-in `(0.55, 0, 1, 0.45)`;
  - endless loops are linear.

### Quick recipes
| Subject | Recipe |
|---|---|
| Character | breathing 1–2 units over 3–5 s; a blink every 3–4 s; pupils glide; head tilt 3–6° |
| Waiting to be tapped | a jiggle every ~270 ms: squash 2%, widen 2%, the bulge trading sides |
| Floating figure | rises in from 30% of its height below, drifts 5% down and up, leaves rising |
| Tail, hair, ears | rotation around the root, phase delayed along the chain, 4–10° |
| Plant | sway 1.5–4° around the base over 3–6 s; leaves on seeded phases |
| Cloth, flag | a wave that travels along the length, growing away from the fixed edge |
| Fire | a lean of 2–4° and a 3–6% stretch on two waves of different periods |
| Smoke, steam | rises 8–14 units and fades in and out with `bell` |
| Water | ripples grow and fade; floating things bob 1–2 units and rock 2° |
| Rain, snow | seeded `loop`s; snow sways sideways |
| Sky | clouds drift over 20–60 s with parallax; sun rays take 30–60 s per turn |
| Lights | a glow of 2–5% over 2–4 s; stars twinkle at seeded times |
| Machines | gears turn linearly by ratio; a clock hand steps with ease-out |
| Phone | ±3° bursts, then a pause |
| Icon, logo | plays once on appear, then rests |
| Chart | a one-shot draw-on, with bars staggered 40–80 ms |

### Acting (a whole character)
- **Every channel:** key pose (`flow`) + idle (`wave`s, never off while on stage) + follow-through (the parent read 90–140 ms earlier) + accents (a `wave` inside a `seg` window).
- **Arms:** an upper arm and a forearm share a round elbow; the forearm points at shoulder angle + elbow bend.
- **Head turns:** slide the face toward the turn (eyes 10, nose 13 in a 100-wide head) and the ears the other way. Blink on the turn.
- **Weight:** the hips shift and carry the upper body, and the legs angle to keep the feet under it.
- **Landing:** hover, then fall with gravity and stretch; squash hard (0.8) on contact and keep the volume (`width = 1 / height^0.6`).
- **In the air:** limp feet (toes down, one knee folded, trading slowly). The shadow stays on the floor and scales with the height.
- **Props:** enter from off screen already moving and roll by distance / radius. The eyes follow them. A kick hits at the middle of the swing; the prop leaves as a throw, spinning, with a short squash.
- **Asymmetry:** the arms never mirror each other.
- **Camera:** a view from a little above is a whole build, not a tweak: the head is 40–50% of the height, the torso is short and narrower than the head, the legs are short, the feet are round from above, and the shadow is a wide oval with the feet in its lower half. Keep it in one `build` object. A flat view keeps a thin pill shadow.
- **Framing:** on a phone, as big as the screen allows, with the feet low.

---

## Part 2. This project (`01_submarino_b59`)

### Where the code is
- **Platform:** Python offline vector/canvas renderer (`1080x1920 @ 60fps`) + `ffmpeg-skill` verification and packaging pipeline.
- **Motion engine and live face:** Ported directly from `rossark-motion-skill/templates/react-native/motion.ts`, `liveFace.tsx`, `ChefScene.swift`, and `RevealScene.swift` into `render_with_new_skills.py` (`EASE_IN_OUT`, `EASE_OUT`, `EASE_IN`, `track`, `flow`, `seg`, `wave`, `loop`, `bell`, `seeded`, `draw_rossark_officer`, `draw_live_eye`, `draw_live_mouth`).
- **Art kit, characters, poses:**
  - **Canvas coordinate system:** `1080×1920` vertical canvas; Central Visual Stage `Y = 580..1490`.
  - **Living Naval Officers (2.5D `rossark` rigs, head = 100 units wide scaled by `1.45–1.85`):**
    1. **Capitán Valentín Savitsky (`officer_type="savitsky"`):** Dark navy uniform with gold buttons, captain's peaked cap, intense furrowed brows (`brow = -0.8`), sweating in +50°C heat with rising `bell(p)` steam wisps, 2.5D head turn (`yaw`), realistic blinks (`110ms` close, `40ms` hold, `190ms` ease-out open), syllable-synced `LiveMouth`, and 2-segment articulated arms with 90ms forearm follow-through turning the nuclear key.
    2. **Oficial Político Iván Maslénnikov (`officer_type="maslennikov"`):** Soviet political officer cap with red star badge, nodding head (`headDy` via `flow`), turning the second firing key.
    3. **Comandante Vasili Arkhipov (`officer_type="arkhipov"`):** Chief of Staff of the Flotilla, calm focused gaze (`lid = 0.08`, rare blinks, deliberate `lookX`/`lookY` glances toward Savitsky and the viewer), head counter-motion (`head(t) = own(t) - 0.45 * lean(t - 110ms)`), raising his articulated right arm to halt the launch and point toward the surface.

### The owner's rules
- *"Añade todavía más animaciones y motion graphics, como cdmauro2010, prácticamente todo el storytelling está respaldado por las animaciones svg y motiongraphics."* (2026-10-27)
- *"Y haz que las imagenes dejen de temblar."* (2026-10-27) -> Archival photographs are pre-composited once at startup (`PHOTOS_STEADY_STAGE`) with `0.0 px` per-frame crop jitter.
- *"Usa estas skills https://github.com/kajisho5/ffmpeg-skill https://github.com/rossark0/rossark-motion-skill y mejoralo"* (2026-10-27) -> Use `rossark-motion-skill` math (`flow`, `track`, `wave`, `bell`, `seeded`, `LiveFace` 2.5D character acting, travelling water waves, rising steam wisps, mid-swing hammer contact with volume-preserving squash, waiting-to-be-tapped button jiggle) and `ffmpeg-skill` (`probe.py`, `check.py --platform shorts`, `look.py --safe tiktok`).

### Rig limits
- Archival photos (`PHOTOS_STEADY_STAGE`) must never be scaled/cropped per frame (prevents integer rounding tremor). All motion happens in the vector layers (`rossark` characters, submarines, water waves, gauges, hands, radar sweeps) drawn over or alongside them.
- Safe zones (`historical-shorts-visual-system` + `ffmpeg-skill --safe tiktok`): Zero text or critical graphics below `Y = 1520px` or in the right UI rail (`X > 920px`).

### How changes are checked
- `python .agents/skills/ffmpeg-skill/scripts/probe.py produccion/01_submarino_b59/submarino_b59_short.mp4 --json`
- `python .agents/skills/ffmpeg-skill/scripts/check.py produccion/01_submarino_b59/submarino_b59_short.mp4 --platform shorts --json`
- `python .agents/skills/ffmpeg-skill/scripts/look.py produccion/01_submarino_b59/submarino_b59_short.mp4 --tiles 4x3 --safe tiktok -o produccion/01_submarino_b59/ffmpeg_skill_look_sheet.png`
