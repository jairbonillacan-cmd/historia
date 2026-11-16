# Prompt — Short completo a partir de un audio (`@DuskRevela`)

Abrí una conversación nueva en este repositorio, adjuntá el `.mp3` y pegá el bloque de abajo
(cambiá solo la ruta del audio). La referencia completa es `produccion/06_cielo_bremen/`.

```markdown
Haz un Short documental completo con este audio: <RUTA_DEL_MP3>

Trabajá en este repositorio (`@DuskRevela`, 1080×1920 @ 60 fps, -14 LUFS) y tomá como referencia
el video ya terminado `produccion/06_cielo_bremen/` + `remotion/src/videos/bremen.ts`. Leé primero
`remotion/README.md`, `remotion/src/engine/types.ts` y esos dos archivos, y copiá su arquitectura.

## 1. Audio y guion
- Creá `produccion/NN_<tema>/` (siguiente número libre) y copiá el audio a `audio/voz_raw.mp3`.
- Transcribí con `python produccion/transcribir_whisper.py <audio> audio/whisper_words.json`.
- Buscá el guion original en `guiones_antigravity/elevenlabs/` o `elevenlabs/` (grep de un nombre
  propio de la transcripción) y usalo como texto exacto de los subtítulos.
- Copiá `build_audio_and_timeline_bremen.py` como `build_audio_and_timeline_<tema>.py`: ajustá
  `NUMBERS` (números en letras → cifras), `BBOX_PREFERRED` y las rutas. Genera `timeline_chunks.json`
  alineando guion y whisper palabra por palabra, y el master de voz a -14 LUFS **sin tocar
  velocidad ni tono**. Verificá que se alineen todas las palabras.

## 2. Censura (solo lo grave)
- La lista vive en `remotion/src/engine/censor.ts`. Se censura solo lo grave: muerte, matar,
  asesinato, masacre, suicidio, sangre, cadáver, ejecución, tortura, nazi, fusilar, paredón,
  rematar. **No** se censuran guerra, heridos, disparos, explosiones, bombas, armas, ataques.
  Si el guion trae otra palabra grave, agregala ahí (afecta a todos los videos).
- Texto: la palabra se tiene que poder leer. Las vocales pasan a símbolos (`m*$rt#`) con un blur
  leve; ya lo hacen `maskWord`, `Caption` y `CensoredText`.
- Audio: nada de pitidos. Se silencia la segunda mitad de la palabra («muer…») con
  `remotion/scripts/mute.ts`; agregá `mute:<tema>` en `remotion/package.json`.
- Verificá re-transcribiendo el audio censurado y midiendo la energía en cada tramo silenciado.

## 3. Fotos de archivo
- Copiá `fetch_bremen_assets.py`: bajá candidatas de Wikipedia/Commons a `assets/candidatas/`,
  armá una hoja de contactos y **miralas**: personaje y hecho correctos, nada de fotos modernas
  equivocadas ni de otra guerra. Elegí 15–20 y registralas en `assets/assets_metadata.json`.
- Nada de esvásticas ni símbolos que disparen filtros: descartá la foto o tapala con
  `censor_assets_<tema>.py` (pixelado + blur horneado en el archivo, como en Bremen).
- Fotos CC BY-SA: atribución en el `source` del pie de foto.

## 4. Música y efectos (sin copyright, monetizable)
- Nada descargado: todo sintetizado con numpy. Copiá `build_music_and_sfx_bremen.py`, adaptá
  `SECTIONS_START` (armonía según el arco del guion) y `build_sfx` (efectos anclados a cláusulas
  con `at(i)`: golpe en t=0, golpes en cada corte del gancho, latidos en la tensión, motores,
  viento, explosiones, lo que pida la historia).
- Música con ducking bajo la voz (-24 dB con voz, -15 dB en pausas), efectos con ducking leve,
  mezcla final `audio/audio_master_final.wav` a -14 LUFS. Esto reemplaza la regla de "0 % BGM"
  del prompt maestro anterior.
- Comprobá inteligibilidad: la transcripción de la mezcla debe coincidir ≥ 95 % con la de la voz sola.

## 5. Plan visual dinámico y viral
- Creá `remotion/src/videos/<tema>.ts` y registralo en `src/Root.tsx` y en `render:<tema>`.
- Unos 45–55 cortes en ~160 s; en el gancho, un corte cada 1,5–2 s. Usá `word` para cortar sobre
  la palabra clave dentro de una cláusula, y `at` + `word` para clavar las capas.
- Escenas: `photo`, `map` (agregá países en `MapScene` si hace falta), `radar`, `bomber`
  (diagrama técnico con daños), `escort` (aviones desde arriba), `quote` (cita a máquina),
  `versus`, `medal`, y `dilemma` para el cierre. Si la historia pide otra animación (barcos,
  tanques, documento, línea de tiempo…), agregala al motor como escena opcional, sin romper los
  videos existentes: otras sesiones usan el mismo motor.
- Capas: `slam` (palabra-golpe), `reticle`, `impact` (destello + sacudida), `stat`, `title`,
  `ribbon`, `caption`. Nunca dos escenas iguales seguidas.
- Zonas: subtítulo arriba; en retratos, títulos con `low: true` para no tapar la cara; nada de
  texto por debajo de y = 1520.

## 6. Revisión y render
- Cuadros sueltos: `node scripts/stills.mjs <Id> <segundos…>` → hojas de contacto → mirarlas y
  corregir textos cortados, solapes, títulos sobre caras.
- `npm run render:<tema>` en segundo plano. Verificá 1080×1920, 60 fps y -14 LUFS con ffprobe/ebur128.
- Al final contame qué palabras se censuraron, qué fotos se taparon, y que no escuchaste el audio
  ni viste el video de corrido.
```
