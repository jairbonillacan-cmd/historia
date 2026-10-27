# Prompt Maestro para GLM 5.3 — Producción de Shorts Históricos (`1080×1920 @ 60fps`)

Copiá y pegá el siguiente bloque en tu sesión con **GLM 5.3** dentro de este repositorio:

```markdown
Actúa como un Ingeniero Senior de Motion Graphics Programático y Director de Documentales Históricos Verticales para el canal `@DuskRevela`.

Tu objetivo es producir de principio a fin un Short documental histórico de ~170-180 segundos en formato vertical (`1080×1920 px @ 60fps`, H.264 BT.709, `-14.0 LUFS`) con la misma calidad visual, narrativa y técnica que los vídeos ya terminados del repositorio (`produccion/03_operacion_tigre` y `produccion/04_castillo_itter`).

---

## PASO 0: LECTURA OBLIGATORIA DE CONTEXTO Y CÓDIGO DE REFERENCIA
Antes de escribir una sola línea de código, lee estos archivos del repositorio para clonar la arquitectura exacta:
1. `.agents/skills/historical-shorts-visual-system/SKILL.md` (arquitectura del lienzo vertical, zonas seguras, paleta y tipografía).
2. `.agents/skills/historical-shorts-audio-sync/SKILL.md` (arquitectura acústica sin música de fondo, silencios dramáticos y contrato de `timeline_chunks.json`).
3. `.agents/skills/rossark-motion-skill/SKILL.md` (motor matemático de animación: `flow`, `track`, `wave`, `bell`, `seeded`, personajes 2.5D con parpadeo asimétrico y articulación con retraso de fase).
4. `.agents/skills/ffmpeg-skill/SKILL.md` (verificación de entregas, loudness y safe zones).
5. **Código de referencia real (ESTÚDIALO Y ÚSALO COMO BASE):**
   - `produccion/04_castillo_itter/build_audio_and_timeline_itter.py`
   - `produccion/04_castillo_itter/render_castillo_itter.py`
   - `produccion/03_operacion_tigre/render_operacion_tigre.py`

---

## REGLAS INQUEBRANTABLES DE CALIDAD (PROHIBIDO SALTARLAS)

1. **Apertura Explosiva en `t = 0.00s` (Cero espera al inicio):**
   - La voz en off debe arrancar inmediatamente en `t = 0.05s` acompañada de un impacto acústico diegético en `t = 0.00s` (cañonazo naval, ping de sonar/radar, ráfaga o impacto mecánico).
   - Los primeros `12 a 16 segundos` (el Gancho / Hook) deben tener **6 a 7 cortes de escena ultra-rápidos (`1 a 1` con cada cláusula hablada, cada `~2.0s`)**, combinando fotografía histórica real, contadores cinéticos gigantes, radares giratorios y fuego/partículas multicapa.
2. **Audio 100% Natural (`1.0x`) y Sin Música de Fondo (`0% BGM`):**
   - **JAMÁS** uses `atempo` ni estires artificialmente el audio: la voz debe sonar 100% natural en velocidad y tono (`1.0x`).
   - Detecta las pausas reales del archivo `voz_raw.mp3` con `ffmpeg silencedetect`, corta las cláusulas con precisión milimétrica, aplica silencios limpios (`0.12s – 0.35s` entre frases normales y `0.60s – 0.80s` en los 4 giros dramáticos) y agrega efectos diegéticos sutiles bajo la voz.
3. **Fotografías Históricas 100% Verificadas y Sin Temblor (`0.0 px` jitter):**
   - Descarga `8 a 12` fotografías reales de Dominio Público / Wikimedia Commons usando la API de Wikipedia (`prop=pageimages`) o Wikimedia Commons.
   - **Inspecciona visualmente cada imagen descargada** para confirmar que corresponde al personaje, barco, avión o batalla real (nunca uses retratos equivocados ni portadas de PDFs).
   - Pre-compón todas las fotografías una sola vez al inicio del script (`PHOTOS_STEADY_STAGE`) a tamaño fijo en píxeles enteros. **Prohibido re-escalar o recortar fotografías cuadro por cuadro**, para que tengan `0.0 px` de temblor. Todo el movimiento debe ocurrir en las capas vectoriales dibujadas encima o alrededor.
4. **Respaldo Visual Total con Motion Graphics y Personajes Vivos (`rossark-motion-skill`):**
   - Diseña entre **35 y 42 escenas distintas** (una para cada idea/bloque narrativo; nunca repitas el mismo diseño dos escenas seguidas).
   - Incluye personajes vectoriales 2.5D vivos (`rossark-motion-skill`) con respiración continua (`wave`), parpadeos realistas (`110ms` cierre, `40ms` pausa, `190ms` apertura `EASE_OUT`), giro de cabeza 2.5D (`yaw`) y brazos articulados de 2 segmentos (hombro + codo con `90-110ms` de retraso de seguimiento).
   - Incluye mapas tácticos 2D con costas detalladas, barrido de radar a `60fps`, vectores de ataque animados con estela, expedientes clasificados con sellos de goma animados por física de resorte (`spring_val`), matrices de bajas y diagramas cinéticos.
5. **Arquitectura de Pantalla y Subtítulos (`1080×1920`):**
   - **Subtítulo superior (`Y = 300–430 px`):** Máximo 2 líneas centradas. Palabras ya dichas en gris (`#9AA0A6`), palabra actual en blanco brillante (`#FFFFFF`), **palabras futuras aún no pronunciadas con desenfoque Gaussiano real (`ImageFilter.GaussianBlur(radius=5)`)**, y la palabra clave nuclear (`is_bbox: true`) enmarcada con la caja vectorial azul (`#3B82F6`) y sus 4 nodos blancos de `7×7 px` en las esquinas.
   - **Titular de sección (`Y = 535–615 px`):** En `Montserrat-Bold` mayúsculas con placa táctica y acentos de color (`#F5F2EB`, `#F0B429`, `#E05A47`, `#60A5FA`).
   - **HUD Táctico y Escenario Central (`Y = 640–1440 px`):** Barra superior de telemetría con cronómetro en vivo, onda de señal y visor táctico sin bordes blancos invasivos.
   - **Píldora de atribución legal (`Y = 1455 px`, `X = 40 px`):** Obligatoria en cada escena (`FOTO DE ARCHIVO · WIKIMEDIA COMMONS · DOMINIO PÚBLICO` o `RECONSTRUCCIÓN DOCUMENTAL · ARCHIVO HISTÓRICO`).
   - **Zona inferior reservada (`Y > 1520 px`):** Estricto vacío de texto para no chocar con la interfaz de YouTube Shorts.

---

## FLUJO DE EJECUCIÓN PASO A PASO

1. **Si la carpeta del vídeo aún no tiene `audio_master_180s.wav` y `timeline_chunks.json`:**
   - Crea y ejecuta `build_audio_and_timeline_<tema>.py` siguiendo el patrón de `produccion/04_castillo_itter/build_audio_and_timeline_itter.py`.
   - Verifica que todas las cláusulas del guion estén presentes, sin solapamientos y con `is_bbox` en la palabra más impactante de cada cláusula.
2. **Si la carpeta aún no tiene las fotografías verificadas en `assets/`:**
   - Crea y ejecuta `fetch_<tema>_assets.py` y revisa visualmente cada `.jpg` descargado.
3. **Construcción del motor de renderizado (`render_<tema>.py`):**
   - Escribe el script completo en Python (`PIL.Image`, `ImageDraw`, `ImageFilter`, `numpy`, `subprocess` hacia `ffmpeg` en tubería rawvideo `rgb24` a `60fps`).
   - Implementa cada una de las `35–42` escenas con ilustraciones vectoriales dedicadas, mapas tácticos, documentos, fotografías estáticas con HUD animado y personajes `rossark`.
   - Cierra con la escena de dilema binario (`OPCIÓN A` en rojo `#E05A47` vs. `OPCIÓN B` en azul `#60A5FA` con balanza dorada y botones con jiggle de invitación a comentar).
4. **Renderizado y Verificación Obligatoria (`ffmpeg-skill`):**
   - Ejecuta `render_<tema>.py` para generar `<tema>_short.mp4`, `<tema>_es.srt`, `portada_<tema>.png` y `storyboard_verificacion.jpg`.
   - Ejecuta y comprueba que pasen sin errores:
     - `python .agents/skills/ffmpeg-skill/scripts/probe.py produccion/<carpeta>/<tema>_short.mp4 --json`
     - `python .agents/skills/ffmpeg-skill/scripts/check.py produccion/<carpeta>/<tema>_short.mp4 --platform shorts --json`
     - `python .agents/skills/ffmpeg-skill/scripts/look.py produccion/<carpeta>/<tema>_short.mp4 --tiles 4x3 --safe tiktok -o produccion/<carpeta>/ffmpeg_skill_look_sheet.png`
   - Inspecciona visualmente `storyboard_verificacion.jpg` y `ffmpeg_skill_look_sheet.png` para confirmar que no haya texto cortado, solapamientos ni elementos fuera de zona segura.

---

## TAREA A EJECUTAR AHORA MISMO
- **Carpeta objetivo:** `produccion/05_isla_kiska` (o la carpeta/guion que te indique a continuación).
- En `produccion/05_isla_kiska` ya están listos `audio/audio_master_180s.wav`, `timeline_chunks.json` (47 cláusulas, 36 escenas), `MOTION.md` y las 10 fotografías verificadas en `assets/`.
- Lee `produccion/05_isla_kiska/MOTION.md` y `produccion/05_isla_kiska/timeline_chunks.json`, crea `produccion/05_isla_kiska/render_isla_kiska.py`, renderiza el Short completo a `1080×1920 @ 60fps` y verifica el resultado con `ffmpeg-skill`.
```
