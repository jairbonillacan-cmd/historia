# Historia

Análisis de Shorts de YouTube de historia y producción de contenido propio en ese nicho.

## Canal de referencia
- [@cdmauro2010](https://www.youtube.com/@cdmauro2010/shorts) — análisis completo en [`analisis/cdmauro2010/`](analisis/cdmauro2010/)

## Parrilla de contenido (28 oct → 27 dic 2026)
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

## Estructura
```
prompts/      # Prompts para los agentes de análisis (Gemini 4 Argon)
analisis/     # Informes del análisis del canal de referencia
parrilla/     # Temas, calendario, especificación y scripts
guiones/      # Un .md por vídeo: ficha, locución, guion de edición, descripción y fuentes
elevenlabs/   # Solo la locución de cada vídeo (.txt), lista para pegar en ElevenLabs v4
produccion/   # Material de producción por vídeo (audio, assets)
data/raw/     # Vídeos y frames descargados (ignorado por git)
```

## Flujo de producción
1. Abrir el guion del día en `guiones/AAAA-MM-DD/`.
2. Pegar `elevenlabs/AAAA-MM-DD/Sx.txt` en ElevenLabs (modelo Eleven v4, voz rioplatense grave) y exportar el audio.
3. Editar siguiendo la tabla «Guion de edición» (subtítulos arriba, cambio de plano cada ~4,5 s, sin música de fondo).
4. Publicar a la hora de la franja con la descripción y los 5 hashtags del guion.

## Scripts
```bash
python parrilla/generar_parrilla.py   # regenera parrilla.csv y PARRILLA.md desde temas.psv
python parrilla/validar_guiones.py    # valida todos los guiones y exporta elevenlabs/*.txt + ESTADO.md
```
