# Historia — `@DuskRevela`

Repositorio completo de análisis, guiones para ElevenLabs v4, branding y motor de producción de Shorts documentales de historia (`1080×1920 @ 60fps`).

---

## 1. Estado actual para continuar en casa

### Vídeos en `produccion/`
| Carpeta | Código | Tema | Estado | Scripts incluidos en la carpeta |
|---|---|---|---|---|
| [`produccion/01_submarino_b59/`](produccion/01_submarino_b59/) | Piloto | **Submarino B-59 (1962)**: Vasili Arkhipov y el torpedo nuclear | **Completado** (`submarino_b59_short.mp4`, `-14.0 LUFS`) | `build_audio_and_timeline_b59.py`, `render_submarino_b59.py`, `fetch_b59_assets.py` |
| [`produccion/02_desastre_bari/`](produccion/02_desastre_bari/) | **AG-11** | **Desastre de Bari (1943)**: bombardeo alemán y gas mostaza aliado secreto | **Completado** (`desastre_bari_short.mp4`, `-14.0 LUFS`) | `build_bari_audio_and_timeline.py`, `render_bari_short.py`, `fetch_bari_assets.py` |
| [`produccion/03_operacion_tigre/`](produccion/03_operacion_tigre/) | **AG-12** | **Operación Tigre (1944)**: el ensayo secreto del Día D donde murieron 749 soldados | **Completado** (`operacion_tigre_short.mp4`, `-14.0 LUFS`) | `build_audio_and_timeline_tigre.py`, `render_operacion_tigre.py`, `fetch_tigre_assets.py` |
| [`produccion/04_castillo_itter/`](produccion/04_castillo_itter/) | **AG-13** | **Castillo de Itter (1945)**: el día que EE. UU. y la Wehrmacht pelearon juntos contra las SS | **Completado** (`castillo_itter_short.mp4`, `-14.0 LUFS`) | `build_audio_and_timeline_itter.py`, `render_castillo_itter.py`, `fetch_itter_assets.py` |
| [`produccion/05_isla_kiska/`](produccion/05_isla_kiska/) | **AG-14** | **Isla de Kiska (1943)**: cuando 34.000 soldados asaltaron una isla vacía | **Listo para renderizar** (`audio_master_180s.wav` + `timeline_chunks.json` + 10 fotos verificadas en `assets/`) | `build_audio_and_timeline_kiska.py`, `fetch_kiska_assets.py`, [`MOTION.md`](produccion/05_isla_kiska/MOTION.md) |

> **Próximo paso inmediato en casa:** Crear y ejecutar `produccion/05_isla_kiska/render_isla_kiska.py` (usando como base `produccion/04_castillo_itter/render_castillo_itter.py` y las especificaciones de [`produccion/05_isla_kiska/MOTION.md`](produccion/05_isla_kiska/MOTION.md)).

---

## 2. Configuración rápida al clonar en otra PC

Las skills propias del proyecto (`historical-shorts-visual-system`, `historical-shorts-audio-sync`, `historical-archival-fetcher`, `remotion-*`) ya están incluidas en `.agents/skills/`. Para restaurar las 2 skills externas con repositorio propio (`ffmpeg-skill` y `rossark-motion-skill`), ejecutá en la raíz del proyecto:

```powershell
git clone https://github.com/kajisho5/ffmpeg-skill .agents/skills/ffmpeg-skill
git clone https://github.com/rossark0/rossark-motion-skill .agents/skills/rossark-motion-skill
```

---

## 3. Guiones propios Antigravity (`guiones_antigravity/`)
- **30 guiones propios (`AG-01` a `AG-30`)** diseñados para `@DuskRevela` (`02:50 min` / `170 s`, `460–500 palabras`, voseo rioplatense, sin pisarse con ningún otro tema del repositorio):
  - Índice completo: [`guiones_antigravity/INDICE_GUIONES_ANTIGRAVITY.md`](guiones_antigravity/INDICE_GUIONES_ANTIGRAVITY.md)
  - Locuciones listas para ElevenLabs v4: [`guiones_antigravity/elevenlabs/`](guiones_antigravity/elevenlabs/) (`AG01.txt` a `AG30.txt`)
  - Validador: `python guiones_antigravity/validar_propios.py`

---

## 4. Parrilla general de contenido (28 oct → 27 dic 2026)
- **305 Shorts** · 5 al día · 3 minutos · voseo rioplatense · locución lista para **ElevenLabs v4**.
- Calendario: [`parrilla/PARRILLA.md`](parrilla/PARRILLA.md) · datos: [`parrilla/parrilla.csv`](parrilla/parrilla.csv)
- Reglas de guion y de ElevenLabs: [`parrilla/ESPECIFICACION_GUIONES.md`](parrilla/ESPECIFICACION_GUIONES.md)
- Estado de cada guion: [`parrilla/ESTADO.md`](parrilla/ESTADO.md)

| Franja | Hora ART (UTC-3) | Hora UTC-6 | Eje |
|---|---|---|---|
| S1 | 09:00 | 06:00 | Antigüedad |
| S2 | 12:30 | 09:30 | Medieval, Moderna y siglo XIX |
| S3 | 16:00 | 13:00 | América e Hispanoamérica |
| S4 | 19:00 | 16:00 | Guerras mundiales (1914–1945) |
| S5 | 21:00 | 18:00 | Guerra Fría y siglo XX (1945–1991) |

---

## 5. Estructura del repositorio
```text
.agents/skills/       # Skills de producción audiovisual, mapas, archivos históricos y motion
analisis/             # Análisis multi-agente de 20 Shorts de @cdmauro2010
branding/             # Identidad visual, paletas, avatares y banners de @DuskRevela
guiones_antigravity/  # 30 guiones propios (AG-01 a AG-30) + locuciones ElevenLabs v4
guiones/              # 305 guiones de la parrilla general por fecha
elevenlabs/           # 305 locuciones (.txt) de la parrilla general
parrilla/             # Calendario, especificación y scripts de validación
produccion/           # Proyectos de vídeo (01_submarino_b59 a 05_isla_kiska) con código, audio, assets y MP4
prompts/              # Prompts de sistema y análisis
```
