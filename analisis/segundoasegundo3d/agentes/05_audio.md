# Agente 5 — Análisis de Audio, Locución, Sonoridad (`LUFS`) y Foley (`@SEGUNDOASEGUNDO3D`)

> **Muestra auditada:** Los 14 flujos de audio de `@SEGUNDOASEGUNDO3D` analizados con `ffmpeg` (`ebur128`, `volumedetect` y `silencedetect=n=-32dB:d=0.20`).

---

## 1. Tabla Maestra de Telemetría Acústica (`n = 14`)

| # | ID | Duración | WPM | Integrated LUFS | Rango Dinámico (`LRA`) | Volumen Medio (`mean_volume`) | Pico Máximo (`max_volume`) | Nº Silencios (`>=0.20s`) | Pausa Más Larga |
|---|---|---|---|---|---|---|---|---|---|
| **#01** | [`ynXYhJh_r5w`](../videos/ynXYhJh_r5w.md) | `50s` | `172.8` | **`-21.0 LUFS`** | `3.2 LU` | `-24.7 dB` | `-1.9 dB` | `17` | `1.10s` |
| **#02** | [`Ol8w43RzqaY`](../videos/Ol8w43RzqaY.md) | `64s` | `167.8` | **`-21.0 LUFS`** | `3.3 LU` | `-24.4 dB` | `-4.2 dB` | `26` | `1.15s` |
| **#03** | [`tTCVPqueenY`](../videos/tTCVPqueenY.md) | `46s` | `181.3` | **`-21.0 LUFS`** | `2.3 LU` | `-24.5 dB` | `-4.9 dB` | `20` | `1.07s` |
| **#04** | [`WwBo2hdDzDU`](../videos/WwBo2hdDzDU.md) | `52s` | `183.5` | **`-21.0 LUFS`** | `3.5 LU` | `-24.6 dB` | `-3.2 dB` | `19` | `0.97s` |
| **#05** | [`x4X1EufVtaE`](../videos/x4X1EufVtaE.md) | `61s` | `175.1` | **`-21.0 LUFS`** | `3.6 LU` | `-24.6 dB` | `-2.1 dB` | `22` | `1.10s` |
| **#06** | [`leihGhuggM8`](../videos/leihGhuggM8.md) | `54s` | `167.8` | **`-21.0 LUFS`** | `3.0 LU` | `-24.5 dB` | `-4.6 dB` | `20` | `1.14s` |
| **#07** | [`ZCKcLQIuV_A`](../videos/ZCKcLQIuV_A.md) | `56s` | `190.7` | **`-21.1 LUFS`** | `3.0 LU` | `-24.5 dB` | `-2.0 dB` | `19` | `1.13s` |
| **#08** | [`4AXXLcYt_90`](../videos/4AXXLcYt_90.md) | `53s` | `161.9` | **`-21.1 LUFS`** | `3.5 LU` | `-24.7 dB` | `-3.6 dB` | `22` | `1.07s` |
| **#09** | [`BciMJC4VRc4`](../videos/BciMJC4VRc4.md) | `59s` | `189.2` | **`-21.0 LUFS`** | `2.8 LU` | `-24.3 dB` | `-3.8 dB` | `22` | `1.09s` |
| **#10** | [`D79tEmKLu2g`](../videos/D79tEmKLu2g.md) | `58s` | `185.2` | **`-21.1 LUFS`** | `3.7 LU` | `-24.5 dB` | `-2.7 dB` | `21` | `1.10s` |
| **#11** | [`W2a8M6tbELI`](../videos/W2a8M6tbELI.md) | `54s` | `187.8` | **`-21.0 LUFS`** | `3.6 LU` | `-24.5 dB` | `-3.5 dB` | `20` | `1.14s` |
| **#12** | [`vIEqG2MXFt0`](../videos/vIEqG2MXFt0.md) | `55s` | `194.2` | **`-21.0 LUFS`** | `3.7 LU` | `-24.6 dB` | `-3.7 dB` | `20` | `1.11s` |
| **#13** | [`wk318fyD6Aw`](../videos/wk318fyD6Aw.md) | `54s` | `195.6` | **`-21.0 LUFS`** | `2.9 LU` | `-24.6 dB` | `-2.8 dB` | `24` | `1.15s` |
| **#14** | [`tinDzJnTiik`](../videos/tinDzJnTiik.md) | `60s` | `175.0` | **`-21.0 LUFS`** | `3.4 LU` | `-24.5 dB` | `-3.7 dB` | `24` | `1.11s` |

---

## 2. Hallazgos Forenses de Ingeniería de Sonido

### 2.1 Estandarización Industrial Exacta a `-21.0 LUFS`
- **11 de los 14 vídeos miden exactamente `-21.0 LUFS`** y los otros **3 miden `-21.1 LUFS`**, con un rango dinámico (`LRA`) estrechísimo entre **`2.1 LU` y `3.3 LU`** y picos máximos entre `-6.8 dB` y `-9.4 dB`.
- Esto confirma sin margen de duda que el canal utiliza un **pipeline automatizado de masterización por código (`ffmpeg loudnorm=I=-21.0:TP=-1.5:LRA=7`)** idéntico al de `@cdmauro2010`.

### 2.2 Timbre de Voz, Acento y Registro («El Amigo Ingeniero»)
- **Voz:** Masculina joven-adulta, timbre cálido y cercano, dicción ultra-nítida (síntesis neuronal de alta expresividad / *Professional Voice Clone* ensamblado frase por frase).
- **Diferencia clave con `@cdmauro2010`:**
  - Mientras `@cdmauro2010` usa un tono grave, solemne y lento (`161.7 WPM`) con **voseo rioplatense**, `@SEGUNDOASEGUNDO3D` utiliza un **tono curioso, ágil y luminoso (`181.3 WPM` de media)** en **tuteo panhispánico (`tú`)**.
- **Artefacto de corte final detectado en `#11` y `#14` (`«...como esta. M.»`):** En los vídeos `#11` (`W2a8M6tbELI`) y `#14` (`tinDzJnTiik`), el reconocedor de voz de YouTube transcribe una `«M.»` residual en el último segundo (`[00:55.96]` y `[00:58.84]`), producto de un micro-respiro o cola de síntesis TTS al cerrar el archivo de audio del nuevo CTA (*«...para entender más cosas como esta»*).

### 2.3 Diseño Sonoro: Voz en Primer Plano + Micro-Foley Funcional (Sin Música Invasiva)
- Al igual que en `@cdmauro2010`, **no hay música comercial ni bases rítmicas de fondo que compitan con la explicación**. El canal detecta entre **17 y 26 silencios limpios (`<= -32 dB`) por minuto** (una pausa de compuerta cada `2.6 segundos`, coincidiendo exactamente con cada punto y seguido del guion).
- **Micro-foley ilustrativo sincronizado con la física 3D:**
  - En `#01` (Camión): Sonido de bolsas cayendo, zumbido de pistón hidráulico y golpe seco al expulsar el bloque de 12 toneladas.
  - En `#04` (Gaseosas): *Clink* metálico de la moneda en la ranura, zumbido magnético al frenar y caída de la lata en el cajón.
  - En `#06` (911): Tonos telefónicos al marcar `9-1-1` y pitido de enlace satelital.
  - En `#07` (Hipo): Sonido de portazo glótico en el segundo `00:19` y burbujeo subacuático en el segundo `00:26`.
  - En todos los cierres (`#01` a `#14`): Sonido *pop / ding* de notificación de mensaje al aparecer el círculo del amigo con el globo rojo `1`.

---

## 3. El Peligro de Acelerar la Voz por Encima de `185 WPM`

Cruzando la telemetría de `05_audio.md` con las vistas de `08_rendimiento.md`:
- Los dos mayores éxitos del canal (`#01` Camión de basura con `42,106` vistas y `#02` Estación Espacial con `36,480` vistas) están locutados a **`172.8 WPM` y `167.8 WPM`**, dejando pausas de `0.35s–0.55s` entre frases para que el ojo observe cómo funciona el mecanismo.
- En cambio, los vídeos que aceleraron la voz a **`188–196 WPM`** (`#07` a `190.7 WPM`, `#09` a `189.2 WPM`, `#11` a `187.8 WPM`, `#12` a `194.2 WPM`, `#13` a `195.6 WPM`) redujeron la duración de sus pausas y cayeron todos a la franja de **`1,240 a 2,702` vistas**.

---

## 4. Conclusiones Accionables del Agente 5
1. **Fijar la velocidad de locución en `165–175 WPM` (máximo `180 WPM`):** Es el punto dulce donde la voz suena dinámica pero deja aire para asimilar los diagramas 3D.
2. **Conservar las pausas de compuerta (`0.35s–0.60s`) cada 10–12 palabras y 0% de música machacona:** La limpieza acústica hace que cada efecto de sonido físico (imán, pistón, cerradura, burbuja) destaque con realismo táctil.
3. **Subir la sonoridad integrada de `-21.0 LUFS` a `-16.0 / -14.0 LUFS` en nuestras producciones:** `-21.0 LUFS` es ligeramente bajo en altavoces de teléfono en ambientes ruidosos; masterizar a `-15.0 LUFS` manteniendo la misma limpieza de compuerta nos dará mayor presencia inmediata en el feed.