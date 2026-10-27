---
name: historical-shorts-visual-system
description: >-
  Programmatic visual design system and Remotion/React architecture for 3-minute
  (180s) vertical historical documentary Shorts at 1080x1920 @ 60fps. Use this
  skill whenever designing, coding, or rendering historical video scenes,
  top-third dynamic subtitles with vector selection boxes, tactical 2D maps,
  reconstructed historical documents, archival media layouts, or decision
  diagrams.
---

# Historical Documentary Shorts — Visual System (`1080×1920 @ 60fps`)

This skill defines the programmatic motion-graphics architecture for high-retention vertical historical documentaries built in **Remotion (React + HTML5 + CSS + SVG)** at `1080×1920 px` (`9:16`) and `60 fps`.

---

## 1. Core Visual Rules (Anti-Patterns vs. Required Patterns)

1. **NO Wireframe Card Containers (`border` boxes around the stage):**
   - **Never** enclose the central visual stage inside a rectangular card or border frame.
   - Maps, archival photographs/footage, and 2D vector scenes must breathe across the **full `1080px` width** of the canvas, blended organically into the dark background (`#0D0D0D`) using top and bottom linear/radial gradient vignettes.
2. **Zero Generative AI Slop Inside the Video Body:**
   - The `180s` video body uses exclusively **verified archival photography/footage** (Public Domain / `CC BY-SA`), **2D tactical cartography (GeoJSON/SVG)**, **typographic document reconstructions**, and **clean vector diagrams**.
3. **Continuous Intra-Scene Progression (2.0s Micro-Event Rule):**
   - Average strong scene cut length (ASL): **`4.2s – 5.5s`** (`33–42` scenes in `180s`).
   - Within every scene, trigger a deterministic visual micro-event (`spring()` or `interpolate()`) every **`1.8s – 2.5s`**: a map arrow extends (`stroke-dashoffset`), a date tape types in, a red stamp slams onto paper, or a balance scale tips.

---

## 2. Vertical Canvas Architecture & Safe Zones (`1080×1920`)

```text
+---------------------------------------+ Y = 0 px (0%)
|      TOP VIGNETTE & BREATHING ZONE    | Dark gradient rgba(0,0,0,0.85) -> 0%
+---------------------------------------+ Y = 280 px (14.5%)
|   [ LEVEL 1: TOP DYNAMIC SUBTITLE ]   | 1–2 lines (3–7 words), centered
|   "¿Cómo se rompe un [código] con"    | Y = 300 – 430 px (16% – 22%)
+---------------------------------------+
|     [ LEVEL 2: SECTION HEADLINE ]     | ALL CAPS ExtraBold (#F5F2EB / #F0B429 / #E05A47)
|          "EL PUNTO DÉBIL"             | Y = 540 – 660 px (28% – 34%)
+---------------------------------------+ Y = 660 px (34.4%)
|                                       |
|                                       |
|      [ LEVEL 3: ACTIVE VISUAL STAGE ] | Full-bleed Map / Archival Media /
|         (1080 px × 780 px zone)       | Cream Document / 2D Vector Diagram
|                                       | Y = 660 – 1440 px (34.4% – 75%)
|                                       |
+---------------------------------------+ Y = 1440 px (75%)
| [LEVEL 4: LEGAL ATTRIBUTION PILL]     | Left-aligned (X = 40px, Y = 1445–1495px)
+---------------------------------------+ Y = 1520 px (79.2%)
|                                       |
|   RESERVED YOUTUBE SHORTS UI ZONE     | STRICTLY FORBIDDEN for text or data
|   (@handle, title, audio, right icons)| (Only dark vignette or background blur)
+---------------------------------------+ Y = 1920 px (100%)
```

---

## 3. Exact Color Palette & Typography Tokens

| Visual Role | Font / Token | Size & Weight | HEX Code | Behavior & Usage |
| :--- | :--- | :--- | :---: | :--- |
| **Base Abyss Canvas** | Background | — | `#0D0D0D` – `#141619` | Default canvas for documents, diagrams, and vignettes. |
| **Tactical Ocean** | Map Background | — | `#0B2545` – `#13315C` | Naval/map background with `60×60px` grid at `6%` white opacity. |
| **Standard Map Land** | GeoJSON Fill | — | `#6B7F46` – `#7E8F56` | Olive/moss land fill (`1.5px` stroke `#94A86B`). |
| **Parchment Map Land** | GeoJSON Fill | — | `#C9BC9C` – `#D6C9AC` | Alternative land palette for pre-1920 / WWI / Ancient maps. |
| **Archival Paper** | Document Card | — | `#F4EFE6` – `#EFE8D8` | Tilted document card (`-1.5deg`) with deep drop shadow. |
| **Subtitle — Past Word** | `Inter` | `46–48px` Regular (`400`) | `#9AA0A6` (`opacity: 0.55`) | Words already spoken in the active chunk. |
| **Subtitle — Active Word**| `Inter` | `46–48px` Bold (`700`) | `#FFFFFF` | Word currently being spoken at `currentTime`. |
| **Subtitle — Future Word**| `Inter` | `46–48px` Regular (`400`) | `rgba(255,255,255,0.32)` | Words not yet spoken; **must apply `filter: blur(6px)`**. |
| **Vector Selection Box** | `Inter` | `46–48px` Bold (`700`) | Border `#3B82F6` (`2.5px`) | Fill `rgba(59,130,246,0.14)` + 4 white `7×7px` corner nodes (`is_bbox`). |
| **Headline — Neutral** | `Montserrat` | `62–72px` ExtraBold (`800`)| `#F5F2EB` | Dates, places, and neutral section titles (`ALL CAPS`). |
| **Headline — Primary** | `Montserrat` | `62–72px` ExtraBold (`800`)| `#F0B429` | Key strategic concepts, revelations, and final questions. |
| **Headline — Danger** | `Montserrat` | `62–72px` ExtraBold (`800`)| `#E05A47` | Threats, casualties, errors, red rubber stamps, digital timers. |
| **Headline — Tactical** | `Montserrat` | `62–72px` ExtraBold (`800`)| `#60A5FA` | Allied forces, defenses, counter-arguments (`SÍ` plate). |
| **Attribution Pill** | `Inter` / `JetBrains Mono` | `17–19px` SemiBold (`600`) | Text `#E5E7EB` on `#000000B8` | `X = 40px, Y = 1445px`, `border-radius: 5px`, `ALL CAPS`. |

---

## 4. The 4 Visual Modules (Rotate Every `4.2s – 5.5s`)

Never repeat the same module twice in a row with the same layout. Use the reusable React/Remotion components in [references/components.tsx](./references/components.tsx):

### Module A: Verified Archival Media (`<ArchivalMediaScene>`)
- **Full-width framing:** Place the historical photograph or public-domain film clip between `Y = 480px` and `Y = 1480px`. Behind it, render a full-screen (`1080×1920`) copy scaled to cover with `filter: blur(45px) brightness(0.32)` plus top/bottom dark gradients so there are no harsh horizontal edges.
- **Motion:** Continuous `interpolate()` scale from `1.00` to `1.08` over the scene duration.
- **Typewriter Context Tape:** Optional cream ribbon (`#F4EFE6`, left border `5px solid #D63629`, font `Courier Prime` Bold) typing out the date/location (`27 DE OCTUBRE DE 1962`).
- **Mandatory Attribution:** Render `<AttributionPill text="FOTO DE ARCHIVO · [FUENTE], [AÑO] · [DOMINIO PÚBLICO / CC BY-SA 4.0]" />` at `X = 40px, Y = 1445px`.

### Module B: 2D Tactical Cartography (`<TacticalMapScene>`)
- **Canvas:** Full-bleed `1080×1920` or `1080×1100` SVG map over `#0B2545` navy ocean with orthogonal tactical grid (`60×60px`, `rgba(255,255,255,0.06)`).
- **Geography:** Real GeoJSON/SVG coastlines (`#6B7F46` land). Never use rectangle placeholders for countries or islands.
- **Animated Overlays:** Curved attack/convoy arrows animated via `stroke-dashoffset`, pulsing concentric radar/sonar rings, and dark location pills (`background: #18181B`, colored status dot + bold uppercase label).

### Module C: Reconstructed Historical Document (`<ReconstructedDocScene>`)
- **Paper Card:** Centered at `Y = 700–1380px`, width `860px`, background `#F4EFE6`, slight tilt (`transform: rotate(-1.5deg)`), deep shadow (`0 28px 60px rgba(0,0,0,0.75)`), font `Courier Prime` or `JetBrains Mono` in dark ink `#1A1917`.
- **Internal Progression:** Typewriter text reveal, red marker underline (`#D63629`) drawing across the decisive sentence, or an angled red rubber stamp (`ULTRA · ALTO SECRETO`, `ORDEN DE ARMADO`, `BLOQUEO`) slamming down with `spring()` scale `1.8 → 1.0`.
- **Mandatory Editorial Honesty Footer:** Bottom-left of the paper in `#71717A` (`15px` uppercase): `RECONSTRUCCIÓN · TEXTO DE EJEMPLO`.

### Module D: Vector Decision Diagram & Tribunal Closure (`<DecisionBalanceScene>` / `<DilemmaClosureScene>`)
- **Diagrams:** Golden balance scale tipping with `spring()` physics as weighted argument blocks drop onto the left (`#60A5FA`) and right (`#E05A47`) plates; vertical kinetic strikethrough lists (`~~OPCIÓN~~`); analog clocks advancing to the exact minute; or `2×2` tactical reason cards lighting up sequentially.
- **Circular Loop & Tribunal CTA (`164s–180s`):** Return to the visual motif of `00:00` in the background, display the binary ethical/strategic dilemma in two side-by-side comparison columns (`OPCIÓN A` in coral `#E05A47` vs. `OPCIÓN B` in blue `#60A5FA`), and anchor the golden CTA banner `CONTÁMELO EN LOS COMENTARIOS`.

---

## 5. Pre-Render Verification Checklist

Before exporting the final MP4, always render a 12-frame `storyboard_verificacion.jpg` mosaic and verify:
- [ ] Zero wireframe border boxes wrapping the central stage.
- [ ] Top subtitle (`Y = 320px`) blurs future words (`filter: blur(6px)`) and draws the 4-node blue `<VectorSelectionBox>` on `is_bbox` words.
- [ ] Every number/date on screen matches the spoken narration 100%.
- [ ] Every archival image/video displays its `DOMINIO PÚBLICO` / `CC BY-SA` attribution pill at `Y = 1445px`, and every reconstructed document displays `RECONSTRUCCIÓN · TEXTO DE EJEMPLO`.
- [ ] Zero text or graphics appear below `Y = 1520px`.
