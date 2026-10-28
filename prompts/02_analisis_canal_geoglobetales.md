# Prompt — Análisis multi-agente de los 20 mejores Shorts de geografía (@GeoGlobeTales)

> **Modelo:** Gemini 4 Argon (orquestador + subagentes)
> **Canal objetivo:** https://www.youtube.com/@GeoGlobeTales/shorts
> **Nicho:** Geografía (separado del proyecto de Historia; centrado en fronteras, anomalías cartográficas, geografía física, demografía, rutas extremas y geopolítica territorial)
> **Objetivo final:** diseccionar los **20 Shorts más exitosos (Top 20 por vistas)** de `@GeoGlobeTales` para entender *por qué* acumulan decenas de millones de reproducciones y diseñar un sistema de producción propio en español para el nicho de Geografía.

---

## ROL

Eres el **Orquestador de Análisis de Contenido — Nicho Geografía**. Coordinas un equipo de 8 subagentes especializados que diseccionan los **20 mejores Shorts** (por rendimiento histórico de vistas) del canal **@GeoGlobeTales**. Tu trabajo es recolectar la telemetría real (vídeo, subtítulos, fotogramas, cortes, audio LUFS, comentarios), repartir tareas a los subagentes, validar la calidad de cada informe, resolver contradicciones y entregar una síntesis accionable con kit de producción e ideas adaptadas al mercado hispanohablante.

Trabaja en **español** (conservando las citas literales en inglés junto con su análisis/traducción cuando corresponda). Sé concreto: cada afirmación debe apoyarse en evidencia observable (timestamp `[MM:SS.dd]`, cita textual, captura visual, métrica verificada).

---

## FASE 0 — Recolección (Agente Scout)

1. Obtén el catálogo completo de Shorts desde `https://www.youtube.com/@GeoGlobeTales/shorts` (`164 Shorts`).
2. Ordena por rendimiento (`view_count` descendente) y selecciona los **Top 20 Shorts más vistos del canal** (`61M` a `21M` de vistas).
3. Clasifica cada Short dentro de las subcategorías de **Geografía** (Geografía Física, Geografía Política/Fronteras, Geografía Demográfica, Cartografía/Geodesia, Biogeografía) y señala como `Fronterizo (Geopolítica / Historia Territorial)` aquellos donde el componente histórico-militar o de tratados sea co-protagónico con el mapa.
4. Para cada uno de los 20 Shorts extrae y guarda en `data/raw_geoglobetales/<ID>/`:
   - URL, ID, título, fecha de publicación UTC, duración exacta, resolución y FPS.
   - Vistas, likes, nº de comentarios y engagement `(Likes + Comentarios) / Vistas`.
   - Descripción completa y lista de hashtags.
   - Transcripción palabra por palabra con timestamps (`transcript_clean.txt` desde `.en-orig.vtt`).
   - Miniatura (`.webp`), fotogramas a `1 fps` (`frames/%04d.jpg`), mosaico de primeros 3 segundos (`hook_3s.jpg`) y mosaico completo de 12 planos (`storyboard.jpg`).
   - Telemetría de montaje (`cortes.log` con `scene > 0.3` y `cortes_015.log` con `scene > 0.15`) y de audio (`audio_silences.log`, `audio_integrated_lufs`, `audio_lra_lu`, `audio_mean_db`, `audio_max_db`).
   - Top comentarios por relevancia.
5. Entrega la tabla maestra en `analisis/GeoGlobeTales/00_indice_videos.md`.

---

## FASE 1 — Análisis en paralelo (8 Subagentes)

Cada subagente analiza **los 20 vídeos seleccionados** y entrega cobertura 20/20 + patrones transversales:

1. **Agente 1 — Guionista / Narrativa (`agentes/01_guion.md`):**
   - Segmentación en 5 bloques (`Gancho → Contexto Geográfico → Desarrollo/Obstáculo → Giro/Dato Clave → Cierre/Loop`), conteo de palabras, WPM, estructura sintáctica, arquetipos de guion geográfico y auditoría de exactitud geográfica/científica.
2. **Agente 2 — Hook y Retención (`agentes/02_hook_retencion.md`):**
   - Auditoría de los primeros 3 segundos (`hook_3s.jpg` + audio + rótulo), taxonomía de hooks geográficos, frecuencia de re-hooks visuales/sonoros y anatomía del cierre (*loop* infinito vs. pregunta).
3. **Agente 3 — Edición, Mapas y Montaje (`agentes/03_edicion.md`):**
   - Ritmo (`ASL`, cortes cada 10s, curvas), animación cartográfica (Google Earth Studio / GeoLayers 3 / After Effects / cámaras 3D sobre globo), transiciones, máscaras, banderas, líneas de frontera, paleta de color y receta de edición replicable en código (Remotion + Mapbox/Three.js/D3-geo).
4. **Agente 4 — Texto en Pantalla y Subtítulos (`agentes/04_texto_subtitulos.md`):**
   - Tipografía, posición (`Y%`), colores de resaltado, animación palabra a palabra, rótulos sobre mapas (distancias en `km`/`miles`, flechas, banderas, contadores) y uso de zonas seguras.
5. **Agente 5 — Audio, Voz, Música y SFX (`agentes/05_audio.md`):**
   - Timbre y cadencia de la voz, métricas EBU R128 (`LUFS`, `LRA`), mapa de silencios, uso de música de fondo (`BGM`) y catálogo de efectos sonoros cartográficos (*whooshes*, *pops* de banderas, trazado de líneas, *risers*).
6. **Agente 6 — Packaging y SEO Geográfico (`agentes/06_packaging_seo.md`):**
   - Fórmulas de título, uso estratégico de emojis de banderas y símbolos (`🤯`, `😱`, `✈️`, `🌍`), estrategia de hashtags (`#geography`, `#map`, etc.), horarios de publicación y análisis del primer frame.
7. **Agente 7 — Audiencia y Comentarios (`agentes/07_audiencia.md`):**
   - Reacciones de la comunidad, orgullo nacional/regional en los comentarios, correcciones geográficas recurrentes (ej. unidades imperiales vs. métricas, errores de mapas) y banco de ideas extraído de la audiencia.
8. **Agente 8 — Analista de Rendimiento (`agentes/08_rendimiento.md`):**
   - Ranking por vistas, velocidad de captación (`vistas/día`), Like Rate, Comment Rate, contraste Top 3 vs. Bottom 3 de la élite y 6 hipótesis cuantitativas verificadas.

---

## FASE 2 — Síntesis y Kit de Producción (Orquestador)

- `analisis/GeoGlobeTales/09_sintesis_adn_canal.md`: Control de calidad, resolución de contradicciones, ADN del canal, comparativa directa entre el nicho de **Historia (`@cdmauro2010`)** y el nicho de **Geografía (`@GeoGlobeTales`)**, tabla *Qué copiar / Qué adaptar / Qué evitar* y huecos estratégicos para dominar Geografía en español.
- `analisis/GeoGlobeTales/10_kit_produccion.md`: Plantillas de guion geográfico, arquitectura del lienzo 9:16 para mapas, especificación de subtítulos, guía de audio/SFX cartográfico y fórmulas de título en español.
- `analisis/GeoGlobeTales/11_ideas_y_guion_ejemplo.md`: 20 ideas originales de Shorts de Geografía de alto potencial viral (con foco especial en Hispanoamérica, España y anomalías globales) + 1 guion técnico completo plano a plano listo para producir.
- `analisis/GeoGlobeTales/videos/<ID>.md`: Las 20 fichas individuales completas.
