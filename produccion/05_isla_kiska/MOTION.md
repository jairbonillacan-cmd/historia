# MOTION.md: living illustrations & scene specification (`05_isla_kiska`)

> Este documento conserva el contexto completo de `produccion/05_isla_kiska` (AG-14: *Isla de Kiska 1943 — Cuando 34.000 soldados asaltaron una isla donde ya no había nadie*) para continuar y renderizar directamente en casa.

---

## Estado actual de `05_isla_kiska`

1. **Audio y Sincronización (`LISTO`):**
   - `audio/voz_raw.mp3` (locución original en ElevenLabs v4).
   - `audio/audio_master_180s.wav` (`171.75 s`, masterizado a `-21.0 LUFS` con impacto naval diegético en `t = 0.00s` y arranque instantáneo de voz en `t = 0.05s`).
   - `timeline_chunks.json` (`47 cláusulas`, `36 escenas`, palabras alineadas al milisegundo y `is_bbox` en palabras nucleares).
   - Generado por [`build_audio_and_timeline_kiska.py`](./build_audio_and_timeline_kiska.py).

2. **Fotografías Históricas Verificadas en `assets/` (`LISTO` — 10 imágenes verificadas visualmente):**
   - `kiska_landing.jpg` — Desembarco estadounidense en Kiska (`Operation Cottage`, agosto de 1943, Dominio Público).
   - `attu_battle.jpg` — Mortero estadounidense en la batalla de Attu (mayo de 1943, Dominio Público).
   - `masatomi_kimura.jpg` / `masatomi_kimura_ja.jpg` — Retrato del contraalmirante japonés Masatomi Kimura (Dominio Público).
   - `abner_read.jpg` — Destructor estadounidense `USS Abner Read (DD-526)` en junio de 1943 (Dominio Público).
   - `kiska_japanese.jpg` — Ocupación japonesa de Kiska (1942–1943, Dominio Público).
   - `aleutians_campaign.jpg` — Tropas aliadas arrastrando suministros en el barro y nieve de las Aleutianas (Dominio Público).
   - `b24_aleutians.jpg` — Bombardero `B-24 Liberator` del 21st Bomb Squadron en las Aleutianas, marzo de 1943 (Dominio Público).
   - `kiska_bunkers.jpg` — Submarinos enanos e instalaciones japonesas abandonadas en Kiska (Dominio Público).
   - `uss_idaho_kiska.jpg` — Acorazado estadounidense `USS Idaho (BB-42)` disparando sus cañones hacia Kiska (Dominio Público).

3. **Siguiente paso al descargar en casa:**
   - Crear y ejecutar `produccion/05_isla_kiska/render_isla_kiska.py` tomando como plantilla directa [`produccion/04_castillo_itter/render_castillo_itter.py`](../04_castillo_itter/render_castillo_itter.py) y [`produccion/03_operacion_tigre/render_operacion_tigre.py`](../03_operacion_tigre/render_operacion_tigre.py), implementando las **36 escenas** de `timeline_chunks.json` (con hook explosivo en `Escenas 1..6` durante los primeros `12.8 s`, fotografías estáticas `PHOTOS_STEADY_STAGE` con `0.0 px` de temblor, personajes `rossark-motion-skill` para Masatomi Kimura, artilleros de radar en la Batalla de los Puntos Fantasma y patrullas de EE. UU. y Canadá en la niebla, más verificación final con `ffmpeg-skill`).
