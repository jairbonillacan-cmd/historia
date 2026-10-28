# FASE 2 — Kit de Producción Replicable para el Nicho de Geografía (Manual Operativo)

> **Propósito:** Traducir la ingeniería inversa de los 20 Shorts más vistos de `@GeoGlobeTales` (`665.5 millones de vistas`) en un **manual técnico paso a paso** para producir nuestros propios Shorts de Geografía en español (`1080×1920 @ 60fps`), independiente del sistema de Historia.

---

## 1. Plantillas de Guion Geográfico por Bloques (con Tiempos y Conteo de Palabras)

Mientras que en Historia la velocidad óptima era de `155–160 WPM` (`180s`), en **Geografía** la velocidad ganadora verificada en `@GeoGlobeTales` es un `+11%` más rápida (`179.3 WPM` en inglés, que adaptado a la longitud silábica del español equivale a **`168–175 palabras por minuto` = `2.85 palabras por segundo`**).

Existen dos formatos maestros según el tipo de fenómeno geográfico:
- **Modalidad A — Formato Estándar de `60 Segundos` (`165–175 palabras`):** Utilizado en **12 de los 20 vídeos top** (`#02` Darién, `#04` Línea del 80% de EE. UU., `#05` Islas Diómedes, `#08` Tíbet, `#10` Jet Stream, `#11` Husos Horarios, `#13` Línea de Wallace, `#15` Gibraltar, `#17` Oklahoma, `#18` Exclaves, `#19` Nado más largo). Ideal para **una sola línea invisible, estrecho, frontera o paradoja física**.
- **Modalidad B — Formato Extendido de `85–100 Segundos` (`240–285 palabras`):** Utilizado en **8 de los 20 vídeos top** (`#01` 27 años caminando `103s`, `#03` Fronteras de España `97s`, `#09` Isla Märket `98s`, `#07` Muro de árboles `94s`). Ideal para **catálogos de 4–5 anomalías de un mismo país o expediciones que cruzan múltiples continentes**.

### 1.1 Plantilla A — Formato de 60 Segundos (`Objetivo: 60s` / `170 palabras`)

| Bloque | Tiempo (`[MM:SS]`) | Duración | Nº Palabras | Función Cartográfica y Fórmula de Guion |
|---|---|---|---|---|
| **1. Hook de Latencia Cero** | `[00:00 – 00:07]` | `7 s` | `18–22 pal.` | **Arranque en `0.00s` mientras se dibuja la línea/polígono en el mapa.**<br>*Ej.: «¿Por qué ningún avión comercial sobrevuela esta zona del planeta que es casi cuatro veces más grande que Francia?»* |
| **2. Magnitud y Escala Comparada** | `[00:07 – 00:20]` | `13 s` | `35–38 pal.` | **Ubicación exacta + Superposición de escala (*True Size*) + Falsa respuesta obvia.**<br>*Muestra en el mapa dónde está el lugar, cuánto mide en `km` y descarta la explicación que todo el mundo cree.* |
| **3. Mecánica Física / Cartográfica** | `[00:20 – 00:42]` | `22 s` | `60–65 pal.` | **Las 2 o 3 causas reales (Altitud/Profundidad/Clima/Tratado) + Corte Transversal 2D.**<br>*Pasa de la vista satelital cenital a un corte lateral 2D o animación de corrientes/nubes con cifras exactas.* |
| **4. Giro o Caso Extremo** | `[00:42 – 00:54]` | `12 s` | `32–36 pal.` | **La consecuencia más insólita sobre la vida humana o el mapa político.**<br>*Introduce el dato que nadie espera (ej. viajar 21 horas en el tiempo caminando 3,8 km, o que el Chimborazo gane al Everest por 2 km).* |
| **5. Remate Circular (Loop)** | `[00:54 – 01:00]` | `6 s` | `15–18 pal.` | **Cierre contundente que re-conecta con la imagen del segundo `00:00`.**<br>*Corta en seco en el segundo `60.0` para provocar el bucle automático.* |

---

### 1.2 Plantilla B — Formato Catálogo / Expedición de 95 Segundos (`Objetivo: 95s` / `270 palabras`)

| Bloque | Tiempo (`[MM:SS]`) | Duración | Nº Palabras | Estructura de Escalera de Rarezas (`Ej.: Las 5 fronteras más raras de un país`) |
|---|---|---|---|---|
| **1. Hook Cartográfico** | `[00:00 – 00:08]` | `8 s` | `22–25 pal.` | Presenta el país/ruta iluminado en el mapa: *«A simple vista, las fronteras de [País] parecen normales, pero esconden cinco de las anomalías más extrañas del planeta.»* |
| **2. Anomalía #1 (El Exclave)** | `[00:08 – 00:26]` | `18 s` | `50 pal.` | Zoom rápido a la primera rareza (ej. un pueblo rodeado al 100% por otro país) + causa breve. |
| **3. Anomalía #2 (La Frontera Cambiante / Microestado)** | `[00:26 – 00:45]` | `19 s` | `55 pal.` | Paneo continuo por la frontera hacia el segundo punto + animación gráfica del cambio o regla curiosa. |
| **4. Anomalía #3 (El Salto Continental)** | `[00:45 – 01:08]` | `23 s` | `65 pal.` | Giro de cámara hacia otro continente o isla remota conectada al país + comparación de distancias en `km`. |
| **5. Anomalía #4 / Récord Mundial + Loop** | `[01:08 – 01:35]` | `27 s` | `75 pal.` | Guarda la anomalía más extrema (ej. la frontera más corta del mundo de 85 metros) para el clímax y cierra con zoom-out general al segundo `00:00`. |

---

## 2. Arquitectura del Lienzo Vertical Cartográfico (`1080×1920 @ 60fps`)

A diferencia del canal de Historia (donde el mapa vive en un recuadro central y el subtítulo va arriba), en **Geografía el mapa satelital ocupa el `100%` de la pantalla (`1080×1920`)** para crear inmersión de vuelo:

```text
+---------------------------------------+  Y = 0 px (0%)
|                                       |
|   ZONA SUPERIOR DE AIRE Y ORIENTACIÓN |  Horizonte del globo 3D / Norte del mapa
|     (Sin textos fijos permanentes)    |
+---------------------------------------+  Y = 260 px (13.5%)
|                                       |
|                                       |
|      ESCENARIO CARTOGRÁFICO ACTIVO    |  Polígonos neón, líneas de ruta animadas,
|     (Foco de la cámara 3D satelital)  |  siluetas comparativas ("True Size"),
|                                       |  banderas 3D, cotas en km/mi y cortes 2D.
|        [ Rótulo: "4.500 m" ]          |  Y = 260 - 1320 px (13.5% - 68.7%)
|        [ País / Flecha / Pin ]        |
|                                       |
+---------------------------------------+  Y = 1340 px (69.8%)
|     [ SUBTÍTULO MINIMALISTA ]         |  2 a 4 palabras por bloque, blanco #FFFFFF
|      "al este de esta línea"          |  con sombra negra suave, SIN caja de fondo.
|                                       |  Y = 1360 - 1460 px (71% - 76%)
+---------------------------------------+  Y = 1500 px (78.1%)
|                                       |
|   ZONA RESERVADA UI YOUTUBE SHORTS    |  Libre de rótulos y subtítulos
|   (@canal, título, audio, botones)    |  (El mapa satelital sigue viéndose de fondo)
+---------------------------------------+  Y = 1920 px (100%)
```

### 2.1 Los 5 Módulos Visuales del Motor de Geografía
1. **Módulo 1 — Vuelo Satelital con Polígonos de Neón (*Neon GIS Layer*):**
   - Teselas satelitales reales de alta resolución (`Esri World Imagery` / `Mapbox Satellite`) con ligera corrección de color (océanos en azul petróleo profundo `#0B3C5D`, vegetación saturada).
   - Bordes de países o regiones trazados con `stroke-width: 6px` blanco/color + `drop-shadow` de neón (`#00E5FF` cian, `#FF3B30` rojo, `#FFD60A` amarillo, `#30D158` verde) y relleno al `25%–35%` de opacidad o rayado diagonal (`45deg`).
2. **Módulo 2 — Superposición de Escala Real (*True Size Comparator*):**
   - Extrae el polígono GeoJSON de un país o región de referencia (ej. España, Francia, México, provincia de Buenos Aires) y lo desplaza/superpone sobre la zona estudiada corregido por proyección esférica para demostrar visualmente su tamaño real.
3. **Módulo 3 — Diagrama de Corte Transversal 2D (*Cross-Section View*):**
   - Cuando se explica una profundidad marina (estrecho de Gibraltar, fosa de las Marianas, estrecho de Lombok) o una barrera montañosa (Andes, Himalaya, sombra orográfica), el plano satelital desliza hacia arriba dando paso a un **corte lateral 2D** con cotas punteadas (`4.500 m`, `900 m`) y vectores animados (aviones, nubes, barcos, raíces).
4. **Módulo 4 — Vista Orbital en Globo 3D (*3D Geoid / Great Circle View*):**
   - Esfera 3D sobre fondo espacial oscuro (`#061A14` a `#02060D`) para mostrar por qué las rutas aéreas o marítimas curvas en un mapa plano son en realidad **líneas rectas sobre la curvatura terrestre**, o para ilustrar el abultamiento ecuatorial.
5. **Módulo 5 — Mapa Histórico en Pergamino (`Sepia Flashback`):**
   - Cuando hay que explicar un tratado fronterizo del pasado (`1809`, `1845`, `1659`), el mapa satelital aplica una transición de textura de papel antiguo (`#C9AE92` tierra, `#657E85` mar) durante `8–12 segundos` antes de volver al satélite actual.

---

## 3. Especificación de Subtítulos y Rótulos Cartográficos (*Map Callouts*)

### 3.1 Tabla de Parámetros Tipográficos (`1080×1920`)

| Elemento | Posición (`Y`) | Fuente | Peso y Tamaño | Color y Sombra | Regla de Oro |
|---|---|---|---|---|---|
| **Subtítulo Principal** | `Y = 1380–1450 px` (`72%–75.5%`), centrado | `Inter`, `Roboto` o `Montserrat` | `SemiBold (600)` o `Bold (700)`<br>`42–46 px` | Texto: `#FFFFFF`<br>Sombra: `0 3px 10px rgba(0,0,0,0.85)` + `stroke 1.5px #000000` | **Máximo 2 a 4 palabras en pantalla a la vez (`1 sola línea`)**. Cero cajas de fondo para no tapar el mapa. |
| **Etiqueta de País / Región** | Anclada al centroide del polígono en el mapa | `Montserrat` o `Plus Jakarta Sans` | `ExtraBold (800)` · `ALL CAPS` o `Title Case`<br>`44–68 px` | Texto: `#FFFFFF`<br>Sombra dura negra `0 4px 12px rgba(0,0,0,0.9)` | Se inclina en perspectiva 3D (`rotateX / rotateZ`) acompañando el giro de la cámara satelital. |
| **Cota de Distancia / Altitud** | Paralela a la flecha de medición en el mapa | `JetBrains Mono` o `Inter Bold` | `Bold (700)`<br>Principal: `38 px`<br>Secundaria: `26 px` | Principal (`km`/`m`): `#FFFFFF` o `#00E5FF`<br>Secundaria (`mi`/`ft`): `#D1D5DB` | Siempre junto a una línea punteada o flecha de doble punta (`<--->`). |
| **Rótulo de Gancho (0–3s)** | Flotando junto al foco del mapa (`Y = 550–850 px`) | `Montserrat Black` | `Black (900)`<br>`54–64 px` | Palabra clave sobre pastilla roja `#E11D48` o azul `#2563EB`; resto en blanco | Aparece solo en los primeros `3–4 segundos` (`[27 años] caminando`, `[NO] tan simple`). |

---

## 4. Guía de Audio, Locución, Música y SFX Cartográficos

1. **Locución (Voz en Español):**
   - **Velocidad:** **`168–175 WPM`** (tono despierto, curioso, ágil, de divulgador científico-geográfico moderno, sin la solemnidad grave ni las pausas largas del canal de Historia).
   - **Silencios entre frases:** Cortos y dinámicos (**`0.15s a 0.30s`**), manteniendo un flujo constante de información.
   - **Nivel de sonoridad integrado:** **`-16.0 a -18.0 LUFS`** (`True Peak <= -1.0 dBTP`).
2. **Música de Fondo (`BGM`):**
   - A diferencia de Historia (`0% BGM`), en Geografía **sí se utiliza una cama musical continua de principio a fin** a **`-24 dB / -26 dB`** (por debajo de la voz): sintetizador minimalista con pulso rítmico suave (*marimba/pluck synth*, *ambient tech puzzle*, `110–124 BPM`) que aporta sensación de viaje y movimiento continuo.
3. **Los 4 Efectos de Sonido (`SFX`) Obligatorios del Mapa (a `-18 dB / -20 dB`):**
   - **`Map Whoosh` (barrido de aire grave-medio):** Sincronizado con cada *zoom-in* o desplazamiento rápido de la cámara entre continentes.
   - **`Neon Line Draw` (zumbido sutil / trazo láser o lápiz):** Mientras se dibuja una frontera, ruta o línea divisoria sobre el mapa.
   - **`Pin / Flag Pop` (burbuja / clic seco de madera):** Cada vez que aparece una bandera 3D, un icono o una silueta de país en pantalla.
   - **`Counter Tick` (repiqueteo digital rápido):** Cuando un número sube rápidamente en pantalla (`80%`, `220.000.000`, `47.000 km`).

---

## 5. Fórmulas de Packaging y Títulos Ganadores en Español

Estructura bipartita probada en el Top 20 de `@GeoGlobeTales`:
**`[Gancho de Paradoja o Superlativo] + [1–2 Emojis (Bandera + 🤯/😱/🌍/✈️)] + [Nombre del Lugar o Fenómeno]`**

1. **Fórmula 1 — La Frontera / Anomalía Más Extraña (`Promedio: 39.0M vistas`):**
   - *Plantilla:* `Las Fronteras Más Extrañas de [País] 🤯 [Bandera] Vecinos Ocultos que Nadie Conoce 👀`
   - *Ejemplo:* `La Frontera Más Extraña entre Argentina y Uruguay 🇦🇷🇺🇾🤯 La Isla Martín García`
2. **Fórmula 2 — La Línea Invisible que Divide un País (`Promedio: 34.4M vistas`):**
   - *Plantilla:* `¿Por Qué el [X]% de [País] Vive de Este Lado de Esta Línea? [Bandera]🤯`
   - *Ejemplo:* `¿Por Qué el 80% de los Brasileños Vive Cerca de Esta Línea? 🇧🇷🤯 El Muro Geográfico`
3. **Fórmula 3 — Por Qué NO Existe [Puente / Carretera / Vuelos] Aquí (`Promedio: 36.6M vistas`):**
   - *Plantilla:* `¿Por Qué NO Hay Ningún Puente Sobre el Río Amazonas? 🌉🤯 El Río Más Grande del Mundo 🌊`
   - *Ejemplo:* `¿Por Qué los Aviones NO Vuelan Sobre el Tíbet? ✈️🚫 La Zona Prohibida del Mapa 🌍`
4. **Fórmula 4 — La Diferencia Entre [A], [B] y [C] que Todos Confunden (`Promedio: 25.1M vistas`):**
   - *Plantilla:* `La Diferencia entre Reino Unido, Gran Bretaña e Inglaterra 🇬🇧🤯 ¿Por Qué Tienen 3 Nombres?`
5. **Fórmula 5 — Récord de Ruta o Distancia Extrema en el Globo (`Promedio: 41.6M vistas`):**
   - *Plantilla:* `La Distancia Más Larga que Podrías Caminar Sin Tocar el Mar 🌍😱 Una Ruta de [X] km`
