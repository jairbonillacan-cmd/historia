# Motor Remotion de Shorts (`@DuskRevela`)

Estilo documental de archivo a pantalla completa (`1080×1920 @ 60fps`): foto de época con acercamiento lento y grade sepia, grano y viñeta, mapas animados del lugar, cintas de fecha, datos grandes con conteo, titulares, pies de foto y subtítulos palabra por palabra.

## Uso

```bash
cd remotion
npm install
npm run studio          # previsualizar y ajustar en el navegador
npm run render:kiska    # → produccion/05_isla_kiska/isla_kiska_short.mp4
node scripts/stills.mjs Kiska 1.5 24 60   # cuadros sueltos en out/ para revisar rápido
```

El `publicDir` es `../produccion`, así que fotos y audio se leen directo de cada carpeta de video, sin copiarlos.

## Un video nuevo

1. En `produccion/<carpeta>/`: `audio/audio_master_*.wav` + `timeline_chunks.json` (los genera `build_audio_and_timeline_*.py`) y las fotos en `assets/`.
2. Crear `src/videos/<tema>.ts` copiando `kiska.ts`: cada entrada del plan arranca en la cláusula `from` y dura hasta la siguiente.
3. Registrarlo en `src/Root.tsx`.

### Tipos de escena (`visual`)
| `kind` | Para qué |
|---|---|
| `photo` | Foto de archivo a pantalla completa. `zoom`, `focus`, `drift` controlan el acercamiento lento; `portrait` para retratos o fotos chicas; `fog`, `flashes`, `dim` como efectos. |
| `map` | Mapa del Pacífico Norte (Natural Earth). Cámara `from`→`to`, países resaltados, marcadores, flechas o convoyes (`ships`), `crossfire`, `fog`. |
| `radar` | Pantalla de radar con barrido, con o sin ecos. |
| `dilemma` | Cierre con dos opciones para invitar a comentar. |

### Capas (`overlays`), con `at` = cláusula en la que entran
`ribbon` (fecha), `stat` (dato con conteo, `slot` 0–2 para apilar), `title` (`low` en mapas), `caption` (pie de foto + fuente).

Los mapas usan `world-atlas` (50m) y `src/geo/aleutians_10m.json` (islas recortadas de Natural Earth 10m). Para otra región, recortar un archivo igual.
