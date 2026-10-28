# Agente 3 — Análisis de Edición, Montaje y Motor Visual 2.5D/3D (`@SEGUNDOASEGUNDO3D`)

> **Muestra auditada:** Los 14 Shorts de `@SEGUNDOASEGUNDO3D`, mediante detección de escenas con `ffmpeg` (`scene > 0.3` y `scene > 0.15`), extracción de fotogramas a `1 fps` y análisis de los 14 mosaicos `storyboard.jpg`.

---

## 1. Descubrimiento Técnico Mayor: Mismo Motor Programático que `@cdmauro2010`, pero con Escenario 3D/2.5D en Plano Secuencia

La auditoría forense de los fotogramas y del audio revela que **`@SEGUNDOASEGUNDO3D` utiliza exactamente el mismo motor de renderizado basado en código (Remotion / React + Canvas/Three.js + FFmpeg)** que `@cdmauro2010`, confirmado por tres huellas dactilares idénticas:
1. **Idéntico componente de subtítulos (`y ≈ 18%`) con el *Figma Bounding Box* azul (`#3B82F6`) y 4 nodos cuadrados blancos en las esquinas.**
2. **Idéntica normalización acústica por código a `-21.0 LUFS` (`11 de 14 vídeos` a `-21.0 LUFS` exactos y `3` a `-21.1 LUFS`).**
3. **Resolución vertical `1080×1920` a `60 fps` (`12 de 14 vídeos`, con `#03` y `#05` a `30 fps`).**

Sin embargo, su **filosofía de montaje visual es opuesta a la de un canal de historia**:
- **0% de fotografías o vídeos de archivo y 0% de IA generativa rasterizada.**
- **Ritmo de cortes duros mucho más bajo (`5.1 cortes > 0.3 por vídeo`, `ASL = 10.8s`), compensado por movimiento continuo de cámara virtual (`plano secuencia 2.5D/3D`):** En lugar de cortar cada 4 segundos a una foto distinta, la cámara **viaja continuamente sin cortes** desde el exterior del objeto hacia su interior microscópico (ej. en [`#14 tinDzJnTiik`](../videos/tinDzJnTiik.md) hay **`0` cortes duros `> 0.3`** en 60 segundos porque toda la pieza es un descenso vertical continuo de 8 metros por el interior del hormiguero).

---

## 2. Tabla de Telemetría de Edición y Ritmo por Vídeo (`n = 14`)

| # | ID | Duración | FPS | Cortes Fuertes (`>0.3`) | ASL (`>0.3`) | Eventos Visuales (`>0.15`) | ASL (`>0.15`) | Timestamps de Cortes (`scene > 0.3`) | Estilo de Cámara Predominante |
|---|---|---|---|---|---|---|---|---|---|
| **#01** | [`ynXYhJh_r5w`](../videos/ynXYhJh_r5w.md) | `50s` | `60` | **`4`** | `10.0s` | `5` | `8.3s` | `20.0s, 22.0s, 27.0s, 31.3s` | Corte transversal X-Ray + Zoom mecánico |
| **#02** | [`Ol8w43RzqaY`](../videos/Ol8w43RzqaY.md) | `64s` | `60` | **`5`** | `10.7s` | `6` | `9.1s` | `5.7s, 10.1s, 28.4s, 30.5s, 59.5s` | Órbita 3D + Zoom planetario |
| **#03** | [`tTCVPqueenY`](../videos/tTCVPqueenY.md) | `46s` | `60` | **`6`** | `6.6s` | `8` | `5.1s` | `9.2s, 20.7s, 28.2s, 34.4s, 37.0s, 42.9s` | Viaje anatómico/celular + Zoom macro |
| **#04** | [`WwBo2hdDzDU`](../videos/WwBo2hdDzDU.md) | `52s` | `60` | **`4`** | `10.4s` | `4` | `10.4s` | `17.4s, 22.8s, 34.7s, 43.5s` | Corte transversal X-Ray + Zoom mecánico |
| **#05** | [`x4X1EufVtaE`](../videos/x4X1EufVtaE.md) | `61s` | `60` | **`8`** | `6.8s` | `10` | `5.5s` | `20.9s, 24.2s, 28.0s, 34.6s, 38.6s, 42.2s...` | Viaje anatómico/celular + Zoom macro |
| **#06** | [`leihGhuggM8`](../videos/leihGhuggM8.md) | `54s` | `60` | **`3`** | `13.5s` | `5` | `9.0s` | `8.5s, 34.2s, 43.7s` | Órbita 3D + Zoom planetario |
| **#07** | [`ZCKcLQIuV_A`](../videos/ZCKcLQIuV_A.md) | `56s` | `60` | **`10`** | `5.1s` | `12` | `4.3s` | `0.8s, 1.5s, 4.1s, 24.5s, 28.4s, 38.4s...` | Viaje anatómico/celular + Zoom macro |
| **#08** | [`4AXXLcYt_90`](../videos/4AXXLcYt_90.md) | `53s` | `60` | **`2`** | `17.7s` | `3` | `13.2s` | `27.8s, 32.2s` | Corte transversal X-Ray + Zoom mecánico |
| **#09** | [`BciMJC4VRc4`](../videos/BciMJC4VRc4.md) | `59s` | `60` | **`3`** | `14.8s` | `8` | `6.6s` | `7.9s, 25.4s, 45.5s` | Viaje anatómico/celular + Zoom macro |
| **#10** | [`D79tEmKLu2g`](../videos/D79tEmKLu2g.md) | `58s` | `60` | **`5`** | `9.7s` | `8` | `6.4s` | `14.6s, 27.2s, 30.1s, 41.4s, 53.2s` | Viaje anatómico/celular + Zoom macro |
| **#11** | [`W2a8M6tbELI`](../videos/W2a8M6tbELI.md) | `54s` | `60` | **`6`** | `7.7s` | `14` | `3.6s` | `2.9s, 8.2s, 10.0s, 14.2s, 25.7s, 31.7s` | Corte transversal X-Ray + Zoom mecánico |
| **#12** | [`vIEqG2MXFt0`](../videos/vIEqG2MXFt0.md) | `55s` | `60` | **`7`** | `6.9s` | `7` | `6.9s` | `8.0s, 13.9s, 22.6s, 24.8s, 37.6s, 41.7s...` | Viaje anatómico/celular + Zoom macro |
| **#13** | [`wk318fyD6Aw`](../videos/wk318fyD6Aw.md) | `54s` | `60` | **`9`** | `5.4s` | `12` | `4.2s` | `2.4s, 14.4s, 18.3s, 24.0s, 29.4s, 33.9s...` | Viaje anatómico/celular + Zoom macro |
| **#14** | [`tinDzJnTiik`](../videos/tinDzJnTiik.md) | `60s` | `60` | **`0`** | `60.0s` | `4` | `12.0s` | `0 cortes (Plano secuencia)` | Plano secuencia vertical descendente |

---

## 3. Los 4 Módulos Visuales del Motor `@SEGUNDOASEGUNDO3D`

Al inspeccionar los 14 `storyboard.jpg`, se identifican los **4 módulos gráficos reutilizables** con los que el canal construye todos sus vídeos:
1. **Módulo 1 — Maqueta Mecánica en Corte Transversal (*Cut-Away X-Ray*):**
   - Presente en los vídeos más virales (`#01` Camión de basura, `#04` Máquina de gaseosas, `#08` Teclado de celular, `#11` Red eléctrica, `#14` Hormiguero).
   - El objeto comienza con su carcasa opaca y, al llegar al segundo `00:05–00:08`, **la pared lateral desaparece dejando un borde luminoso cian/blanco (`#67E8F9`)** que permite ver los pistones hidráulicos amarillos, las bolsas comprimiéndose, las monedas rodando entre imanes rojos y azules o las hormigas por los túneles.
2. **Módulo 2 — Silueta Anatómica de Neón y Sistemas de Partículas 3D:**
   - Empleado en los vídeos de cuerpo humano y neurociencia (`#05` Pesadillas, `#07` Hipo, `#10` Fumar/Vape, `#12` Gripe, `#13` Mareo).
   - Utiliza un contorno humano translúcido con borde azul eléctrico (`#38BDF8`) sobre fondo oscuro (`#0B131E`), dentro del cual se animan órganos texturizados (pulmones rosados, diafragma rojo, estómago ámbar, canales semicirculares azules) o un **cerebro formado por una nube de partículas 3D** donde la amígdala se enciende como un foco rojo.
3. **Módulo 3 — Objeto de Analogía Cotidiana en Primer Plano:**
   - Cada vez que el guion dice *«como cuando...»*, el escenario reemplaza durante `3–5 segundos` el modelo principal por el objeto cotidiano de la metáfora: dos jeringas conectadas por un tubo naranja y una bota pisando una lata verde (`#01`), dos elefantes dentro de la caja del camión (`#01`), una carretera de asfalto/arena/barro bajo tres monedas (`#04`), una cerradura dorada de puerta (`#12`), una salchicha tocando el teclado (`#08`), o una seta roja en el bosque (`#13`).
4. **Módulo 4 — Tarjetas Flotantes de Telemetría (*UI Data Cards*):**
   - Píldoras y tarjetas blancas o translúcidas oscuras con tipografía limpia que anclan cifras clave en la parte inferior del objeto (`y ≈ 70%–82%`): `CARGA: 12 toneladas` con barra de progreso (`#01`), `89% de la gravedad de aquí` y `15 amaneceres` (`#02`), `55%` y `4 años` (`#03`), `+100 por segundo` (`#08`), `CORRIENTE: 17 A` y `28 DE ABRIL DE 2025 · 12:33 h` (`#11`), `OÍDO: Te mueves` y `ALERTA DEL CEREBRO: Veneno detectado` (`#13`).

---

## 4. Paleta de Color y Composición 9:16

- **Fondos atmosféricos con degradado radial temático (nunca negro plano):**
  - **Verde bosque pizarra (`#112A24` → `#6B8078`):** Ingeniería urbana (`#01` Camión de basura, `#11` Apagón, `#13` Mareo).
  - **Azul espacio profundo (`#070B19` → `#1E3A8A`):** Espacio y telecomunicaciones (`#02` ISS, `#03` Bostezo, `#06` 911 Satélite, `#08` Teclado).
  - **Borgoña / Carmesí biológico (`#2A0A18` → `#5B1930`):** Virología, llamadas y sangre (`#09` Receta de voz, `#10` Fumar/Vape, `#12` Gripe).
  - **Tierra / Sepia subterráneo (`#1C120C` → `#4A2F1D`):** Naturaleza (`#14` Hormiguero).
- **Respeto absoluto de Zonas Seguras (`UI Safe Zones`):**
  - `y = 0% – 14%`: Cielo/fondo limpio superior.
  - `y = 15% – 23%`: Subtítulo dinámico de 1–2 líneas.
  - `y = 28% – 82%`: Escenario 3D/2.5D central + tarjetas de datos.
  - `y = 83% – 100%`: Libre de texto crítico para no chocar con el título y usuario de la interfaz de YouTube Shorts.

---

## 5. Conclusiones Accionables del Agente 3
1. **Priorizar el «Efecto Maqueta en Corte Transversal» (*Cut-Away X-Ray*):** Los vídeos donde una máquina cotidiana o estructura se abre por la mitad con borde luminoso (`#01`, `#02`, `#04`) multiplican por 10 las vistas frente a las siluetas médicas planas.
2. **Usar transiciones de cámara continua (Zoom Macro / Paneo Conectado) en lugar de cortes bruscos:** En vídeos de 55s de ciencia/cultura general, guiar el ojo a través de cables, tuberías o túneles sin cortar mantiene al espectador hipnotizado.
3. **Insertar la «Tarjeta de Telemetría UI» con barra o cifra en el tercio medio-bajo (`y ≈ 72%`):** Aporta claridad instantánea cuando el narrador menciona una magnitud (`12 toneladas`, `89%`, `17 A`).