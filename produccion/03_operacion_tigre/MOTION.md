# MOTION.md — Operación Tigre (1944): Motion Graphics & Visual System V2

## 1. Apertura Inmediata de Alto Impacto (`t = 0.00s`)
- **Inicio instantáneo de narración (`0.00s`):** La voz en off arranca en el cuadro `0` (`"28 de abril de 1944..."`) acompañada de un ping de sonar naval (`1320 Hz`) y un impacto sub-grave diegético bajo la voz, eliminando cualquier espera inicial.
- **Hook Visual Cinético (`Escenas 1 a 6`, `0.00s – 15.65s`, ritmo rápido de `~2.5s` por corte):**
  - **S01 (`0.00s – 3.00s`):** Composición de combate naval de alto contraste (LST en llamas `lst_burning.jpg` + mira táctica HUD + radar naval giratorio a `60 fps` + partículas de brasas ascendentes + contador cinético `28 ABR 1944 · ALERTA ROJA`).
  - **S02 (`3.00s – 5.97s`):** Mapa de sala de guerra del Canal de la Mancha con barrido de radar activo, vectores de invasión animados con estela luminosa hacia Normandía y anillo de cuenta regresiva (`D-38 DÍAS · 5 SEMANAS PARA EL DÍA D`).
  - **S03 (`5.97s – 7.76s`):** Bloqueo de mira de reconocimiento aéreo sobre `slapton_sands.jpg` con escáner láser topográfico barriendo la costa del sur de Inglaterra y telemetría de coordenadas (`50°16'N 03°38'W`).
  - **S04 (`7.76s – 12.11s`):** Matriz cinética de bajas (`15×10` iconos tácticos = `750 soldados`) iluminándose en rojo carmesí en tiempo real + contador gigante `0 -> 750 MUERTOS` + onda sísmica/ECG en vivo y fuego multicapa `rossark`.
  - **S05 (`12.11s – 13.24s`):** Tarjeta táctica `FRANCIA · COMBATE REAL` anulada por doble haz diagonal rojo animado (`X NO ESTÁN EN FRANCIA`).
  - **S06 (`13.24s – 15.98s`):** Expediente clasificado de la `OPERACIÓN TIGRE` desplegándose con física de resorte (`spring_val`), láser de seguridad y golpe de sello `[ENSAYO SECRETO · SHAEF]` con onda expansiva.

## 2. Sistema de Motion Graphics Continuo (`Escenas 7 a 37`)
- **HUD Táctico Naval Activo en Todas las Escenas:** Barra superior de telemetría (`Y = 656`) con cronómetro de misión en tiempo real, oscilador de señal de radio en vivo, retículas de esquina animadas (`[ ]`) y sistema de partículas contextual (brasas y humo en escenas de fuego; ondas de sonar y barrido de radar en escenas nocturnas; líneas de escaneo en documentos clasificados).
- **Fotografías de Archivo 100% Estáticas (`0.0 px` de jitter):** Las 8 fotografías históricas verificadas de Wikimedia Commons permanecen fijas al píxel para evitar temblor, enmarcadas dentro de visores tácticos con superposiciones vectoriales animadas a `60 fps`.
- **Física `rossark-motion-skill`:**
  - `flow()` (interpolación monótona cúbica de Fritsch–Carlson) y `spring_val()` (resorte subamortiguado) para entradas escalonadas de tarjetas, barras de progreso, agujas de reloj (`07:30 -> 08:30 AM`), inversión física de `180°` del cinturón salvavidas `M1926`, escala de balanza dorada y botones finales con `squash & stretch`.
