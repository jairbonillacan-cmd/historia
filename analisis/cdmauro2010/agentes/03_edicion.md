# Informe del Agente 3: Edición, Montaje y Lenguaje Visual (`@cdmauro2010`)

> **Muestra analizada:** 20 YouTube Shorts (`#01` al `#20`) | **Formato nativo:** `1080x1920 px` (`9:16`) @ `60 fps` constantes | **Duración:** `177s – 180s` (formato Short extendido de 3 minutos).

---

## 0. Hallazgo Visual Crítico: El Sistema de Motion Graphics Programático

Al inspeccionar fotograma a fotograma los mosaicos `storyboard.jpg` y `hook_3s.jpg` de los 20 vídeos junto con la telemetría de cortes (`scene > 0.3` y `scene > 0.15`), emerge el hallazgo técnico central de esta auditoría:

**`@cdmauro2010` NO utiliza plantillas genéricas de CapCut, ni metraje de stock comercial aleatorio (Pexels/Storyblocks), ni imágenes generadas por IA (Midjourney/DALL-E/Flux).**

En su lugar, el canal opera un **sistema propietario de motion graphics programático y vectorial minimalista a `60 fps`** (desarrollado en código mediante **Remotion / Motion Canvas / HTML5 Canvas + SVG + CSS** o un motor modular equivalente automatizado) que combina **cuatro pilares visuales**:

1. **Fotografías y metraje histórico real de archivo (Wikimedia Commons / Dominio Público / CC BY-SA):** Nunca se muestran crudos sin contexto; se encuadran en la zona central o a pantalla completa con viñeteado oscuro superior/inferior y llevan siempre una **píldora de atribución documental rigurosa** en la esquina inferior izquierda (ej. `FOTO DE ARCHIVO · PRINCETON, 1936 · DOMINIO PÚBLICO` o `RÉPLICA DE LA BOMBA · FOTO: MIKE PEEL · CC BY-SA 4.0`).
2. **Cartografía vectorial minimalista 2D:** Mapas limpios con costas vectorizadas, océanos en azul marino profundo con retícula táctica sutil (`#0B2545`) o tonos pergamino (`#C9BC9C`), flechas curvas animadas de avance de tropas, cercos punteados y etiquetas geográficas en píldoras oscuras (`VARSOVIA`, `PEARL HARBOR`, `STALINGRADO`, `INCHON`).
3. **Reconstrucciones tipográficas de documentos históricos y telegramas:** Tarjetas sobre papel crema (`#F4EFE6`) ligeramente rotadas (`-1.5°` a `+2°`), maquetadas en tipografía monoespaciada (`Courier Prime` / `JetBrains Mono`), con sellos vectoriales rojos (`ULTRA · ALTO SECRETO`, `NO RENDIRSE`, `HALT! ALTO!`, `BLOQUEO`) y una **nota de honestidad editorial al pie** (`RECONSTRUCCIÓN · TEXTO DE EJEMPLO` o `RECONSTRUCCIÓN · VALORES DE EJEMPLO`).
4. **Infografías, diagramas e ilustraciones vectoriales 2D/Voxel:** Desde anillos de cifrado de Enigma, pantallas de osciloscopio de radar (`SCR-270, OPANA`), relojes analógicos sincronizados con el minuto exacto del suceso y balanzas de decisión (`SÍ` vs. `NO`), hasta escenas completas en ilustración geométrica 2D (serie Roma/Estoicismo y Hernán Cortés) o incluso dioramas *pixel-art / voxel* estilo bloques 2D (`#11` Napoleón).

---

## 1. Resumen Cuantitativo Global de los 20 Shorts

| # | ID | Título corto | Dur. | Cortes Fuertes (`>0.3`) | ASL (`>0.3`) | Cortes/10s (`>0.3`) | Cortes Totales (`>0.15`) | ASL (`>0.15`) | Cortes/10s (`>0.15`) | Sub-estilo Visual Dominante |
| :-: | :--- | :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :--- |
| **#01** | `UsMkfLhccJM` | Enigma y Alan Turing | 180s | 41 | 4.29s | 2.28 | 62 | 2.86s | 3.44 | Archivo SGM + Documentos + Diagramas |
| **#02** | `t89RDX8qolU` | Pearl Harbor 1941 | 180s | 46 | 3.83s | 2.56 | 74 | 2.40s | 4.11 | Archivo SGM + Radar Vector + Mapas |
| **#03** | `Dn8s4cqsNCQ` | Hiroshima 1945 | 180s | 39 | 4.50s | 2.17 | 45 | 3.91s | 2.50 | Archivo SGM + Balanza + Mapas |
| **#04** | `4VT2qvIRUkg` | Iwo Jima 1945 | 180s | 36 | 4.86s | 2.00 | 47 | 3.75s | 2.61 | Archivo SGM + Mapa Isla Táctico |
| **#05** | `lYVMDblBX3Y` | Midway 1942 | 180s | 25 | 6.92s | 1.39 | 38 | 4.62s | 2.11 | Archivo SGM + Cronómetros + Cubierta 2D |
| **#06** | `KCrSmZt-A0w` | Dunkerque 1940 | 178s | 37 | 4.68s | 2.08 | 44 | 3.96s | 2.47 | Archivo SGM + Panel 4 Hipótesis + Mapas |
| **#07** | `yeMKOTtYlWU` | Stalingrado | 180s | 51 | 3.46s | 2.83 | 122 | 1.46s | 6.78 | Archivo SGM Intenso + Orden Nº 227 + Mapas |
| **#08** | `VKEIpXxGMVk` | Cândido Godói / Mengele | 178s | 26 | 6.59s | 1.46 | 29 | 5.93s | 1.63 | Híbrido Ilustración 2D + Archivo + ADN |
| **#09** | `UjI03Si4VA8` | Primera Guerra Mundial | 180s | 47 | 3.75s | 2.61 | 114 | 1.57s | 6.33 | Mapas Pergamino 1914 + Archivo PGM |
| **#10** | `g_M7r8EMoFg` | El Caballo de Troya | 180s | 32 | 5.45s | 1.78 | 39 | 4.50s | 2.17 | Pintura Clásica + Metraje + Mapa Naranja |
| **#11** | `V3ase69Rap8` | Napoleón (Austerlitz/Waterloo) | 179s | 16 | 10.53s | 0.89 | 19 | 8.95s | 1.06 | Diorama Pixel-Art / Bloques 2D + Relojes |
| **#12** | `GZNpPvHITiM` | Marco Aurelio (12 años) | 179s | 19 | 8.95s | 1.06 | 26 | 6.63s | 1.45 | Ilustración Geométrica 2D + Escultura |
| **#13** | `ff2r8EirvVI` | Hernán Cortés y las naves | 179s | 24 | 7.16s | 1.34 | 27 | 6.39s | 1.51 | Ilustración Geométrica 2D + Grabados |
| **#14** | `VFppMLRXRqk` | Marco Aurelio y Cómodo | 179s | 28 | 6.17s | 1.56 | 35 | 4.97s | 1.96 | Ilustración Geométrica 2D + Numismática |
| **#15** | `fGYdtXyKbtQ` | Meditaciones (Marco Aurelio) | 177s | 29 | 5.90s | 1.64 | 32 | 5.36s | 1.81 | Ilustración Geométrica 2D + Cuaderno |
| **#16** | `3tSKNGKJOrc` | Epicteto el esclavo | 178s | 28 | 6.14s | 1.57 | 35 | 4.94s | 1.97 | Ilustración Geométrica 2D + Arqueología |
| **#17** | `kOpUJPR9BOM` | Dien Bien Phu | 179s | 29 | 5.97s | 1.62 | 32 | 5.42s | 1.79 | Esquema Topográfico 2D + Archivo + Mapas |
| **#18** | `Km3mMU1pOpM` | Truman destituye a MacArthur | 180s | 36 | 4.86s | 2.00 | 38 | 4.62s | 2.11 | Infografía Política 2D + Archivo + Mapas |
| **#19** | `OmO_msj8Wy8` | Desembarco de Inchon | 180s | 40 | 4.39s | 2.22 | 41 | 4.29s | 2.28 | Simulación Mareas 2D + Mapas + Archivo |
| **#20** | `RT6my9-VxFI` | Puente Aéreo de Berlín | 180s | 32 | 5.45s | 1.78 | 32 | 5.45s | 1.78 | Infografía Logística 2D + Archivo Aviación |
| **MEDIA** | — | **Promedio de los 20 vídeos** | **179.3s** | **33.1** | **5.74s** | **1.84** | **46.6** | **4.60s** | **2.59** | **Sistema Híbrido Programático** |

---

## 2. Fichas Individuales de Edición y Montaje (`#01` a `#20`)

### #01 | `UsMkfLhccJM` — Enigma: Alan Turing y el equipo que descifró el código nazi
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `41` cortes | **ASL (0.3):** `4.29s` | **Cortes/10s:** `2.28`
  - **Cortes totales (`scene > 0.15`):** `62` cortes | **ASL (0.15):** `2.86s` | **Cortes/10s:** `3.44`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 7` | `30-60s: 8` | `60-90s: 6` | `90-120s: 8` | `120-150s: 7` | `150-180s: 5`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 24` | `30-60s: 8` | `60-90s: 7` | `90-120s: 9` | `120-150s: 8` | `150-180s: 6`
  - **Análisis de la curva:** El bloque `0-30s` registra una explosión de `24` micro-eventos visuales (`>0.15`) entre `1.13s` y `4.93s` causados por el contador numérico animado a alta velocidad (`158.962.555.217.826.360.000` / `017.407.874.577.000`) sobre el vídeo en primer plano de las teclas de una máquina Enigma real. A partir del segundo `30`, el ritmo se estabiliza en una cadencia metronómica de `6–8` cortes fuertes por cada 30 segundos, desacelerando ligeramente en el cierre reflexivo (`150-180s: 5` cortes).
- **Material visual observado (`storyboard.jpg` y `hook_3s.jpg`):**
  1. **Vídeo de archivo en bucle (`0-10s` y `172-180s`):** Primer plano real de dedos pulsando teclas metálicas e iluminando lámparas de una máquina Enigma (`VIDEO · UNA ENIGMA REAL · Z22 · CC BY-SA 4.0`), con rótulo central `ENIGMA` y contador dorado `017.407.874.577.000`.
  2. **Retratos históricos de Alan Turing:** Fotografía de archivo a los `27 AÑOS` (`FOTO DE ARCHIVO · PRINCETON, 1936 · DOMINIO PÚBLICO`) y retrato maduro en `1952` (`FOTO DE ARCHIVO · ELLIOTT & FRY, 1951 · DOMINIO PÚBLICO`) con etiqueta superior tipo ficha `[1952]`.
  3. **Reconstrucciones documentales sobre papel crema (`#F4EFE6`):**
     - Hoja de claves mensuales alemana (`GEHEIM! · CLAVES DEL MES` con columnas `DÍA | ROTORES | ANILLOS | TABLERO DE CLAVIJAS`, reloj analógico en la esquina superior derecha y nota legal inferior `RECONSTRUCCIÓN · VALORES DE EJEMPLO`).
     - Carta a Winston Churchill (`Secret and Confidential / Prime Minister only / Dear Prime Minister...` firmada por `A. M. TURING, W. G. WELCHMAN, C. H. O'D. ALEXANDER, P. S. MILNER-BARRY`).
     - Telegrama militar alemán (`MENSAJE DESCIFRADO / DE: JEFE DE SUBMARINOS / A: GRUPO DEL ATLÁNTICO NORTE...`) con sello rojo rectangular inclinado `ULTRA · ALTO SECRETO` y pie `RECONSTRUCCIÓN · TEXTO DE EJEMPLO`.
  4. **Diagramas e infografías vectoriales:** Anillo circular de 26 letras (`A–Z`) con conectores internos dorados e indicador central `A` bajo el título `EL PUNTO DÉBIL` (explicando que ninguna letra puede cifrarse como sí misma).
  5. **Cartografía vectorial:** Mapa de Europa oriental (`VARSOVIA` con punto rojo) y mapa del Atlántico Norte mostrando la ruta punteada `HALIFAX` → `LIVERPOOL` (`CONVOY`) acechada por iconos vectoriales rojos (`SUBMARINOS EN MANADA`).
  6. **Fotografía técnica en Bletchley Park:** Rotores rojos de la Bombe (`RÉPLICA EN BLETCHLEY PARK / «VICTORY»`, atribuida `RÉPLICA DE LA BOMBA · FOTO: MIKE PEEL · CC BY-SA 4.0`).
- **Movimiento y animaciones:** Contador numérico rápido en el hook, rotación de agujas del reloj a medianoche, resaltado de palabras clave en subtítulos con **caja de selección vectorial azul con nodos** (`[medianoche:]`, `[débil]`), trazado progresivo de líneas en el anillo de cifrado y estampado seco del sello `ULTRA`.
- **Composición 9:16 y color/grading:** Fondo negro puro (`#0D0D0D`) en escenas de documentos y diagramas; fotografías en blanco y negro con alto contraste y viñeteado suave superior para garantizar legibilidad del subtítulo en `y ≈ 320px`. La píldora de atribución se ancla invariablemente a la izquierda en `y ≈ 1440px`, dejando el 25% inferior completamente libre para la interfaz de YouTube Shorts.

---

### #02 | `t89RDX8qolU` — Pearl Harbor 1941: la alerta del radar que fue ignorada
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `46` cortes | **ASL (0.3):** `3.83s` | **Cortes/10s:** `2.56`
  - **Cortes totales (`scene > 0.15`):** `74` cortes | **ASL (0.15):** `2.40s` | **Cortes/10s:** `4.11`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 12` | `30-60s: 5` | `60-90s: 7` | `90-120s: 12` | `120-150s: 5` | `150-180s: 5`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 14` | `30-60s: 6` | `60-90s: 7` | `90-120s: 18` | `120-150s: 5` | `150-180s: 24`
  - **Análisis de la curva:** Estructura bimodal de alta energía: un arranque explosivo (`0-30s: 12` cortes fuertes) y un segundo clímax en `90-120s` (`12` cortes fuertes, `18` suaves) que coincide con el momento exacto del ataque japonés a las 07:55. En `150-180s` se detectan `24` micro-cortes suaves (`163.62s–165.37s`) producidos por la animación secuencial de la infografía de los 8 acorazados estadounidenses (`6 DE 8 VUELVEN A PELEAR`).
- **Material visual observado (`storyboard.jpg` y `hook_3s.jpg`):**
  1. **Metraje y fotografía de archivo en color y B/N:** Explosión ígnea en color sobre acorazado en Pearl Harbor (`FOTO DE ARCHIVO · ARCHIVO DE EE. UU. · DOMINIO PÚBLICO`) con etiqueta mecanografiada `7 DE DICIEMBRE DE 1941`; metraje de `«DECEMBER 7TH», JOHN FORD Y GREGG TOLAND, 1943 · DOMINIO PÚBLICO`; retrato de `ALMIRANTE ISOROKU YAMAMOTO / UN GOLPE POR SORPRESA` (`FOTO DE ARCHIVO · MINISTERIO DE MARINA DE JAPÓN`); fotografía aérea japonesa de columnas de agua (`TORPEDOS CONTRA LOS ACORAZADOS / ARMADA IMPERIAL JAPONESA`); explosión del USS Shaw (`EN 2 HORAS`).
  2. **Reconstrucción técnica del radar (`RECONSTRUCCIÓN · RADAR SCR-270, OPANA`):** Pantalla de osciloscopio verde militar con cuadrícula y curva de señal verde brillante que se dispara a los `212 KM` bajo el titular amarillo `+50 AVIONES`.
  3. **Ilustración vectorial táctica:** Vista cenital de aviones blancos estacionados ala con ala junto a una pista (`Por eso, los aviones`), mapa vectorial de Oahu con el puerto interior `PEARL HARBOR` y ondas concéntricas de sonar en la entrada (`6:45 / EL DESTRUCTOR WARD`), y matriz de 8 siluetas vectoriales de acorazados donde 2 quedan oscurecidos y 6 se iluminan en azul claro (`NI EL COMBUSTIBLE NI LOS TALLERES / 6 DE 8 VUELVEN A PELEAR`).
  4. **Documento cifrado:** Recorte de papel crema con tres líneas de texto en clave (`NVEJGMTYJKNMVGQARL...`) bajo el subtítulo `Washington`.
- **Movimiento y animaciones:** Efecto máquina de escribir en la cinta `7 DE DICIEMBRE DE 1941` (visible en `hook_3s.jpg` frame 2 a 3: `7 DE DICIEMBRE DE 1` → `1941`), pulso de onda expansiva en el mapa del USS Ward, oscilación viva del trazo verde del radar SCR-270, encendido secuencial de siluetas de acorazados y cajas de selección azul en `[alerta]`, `[acorazados;]` y `[horas:]`.
- **Composición 9:16 y color/grading:** Contraste dramático entre el naranja/ámbar de fuego del hook y cierre (que sirve de bucle visual perfecto entre el último frame y el primero) y los tonos fríos azul marino/verde osciloscopio de la sección intermedia.

---

### #03 | `Dn8s4cqsNCQ` — Hiroshima 1945: ¿era necesaria la bomba atómica?
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `39` cortes | **ASL (0.3):** `4.50s` | **Cortes/10s:** `2.17`
  - **Cortes totales (`scene > 0.15`):** `45` cortes | **ASL (0.15):** `3.91s` | **Cortes/10s:** `2.50`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 10` | `30-60s: 6` | `60-90s: 8` | `90-120s: 5` | `120-150s: 5` | `150-180s: 5`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 10` | `30-60s: 11` | `60-90s: 8` | `90-120s: 6` | `120-150s: 5` | `150-180s: 5`
  - **Análisis de la curva:** El ritmo arranca con fuerza (`10` cortes en `0-30s` y `11` eventos en `30-60s`) durante el planteamiento del dilema militar en Okinawa y Kyushu, vuelve a acelerarse en el momento de la detonación (`60-90s: 8` cortes) y desciende deliberadamente a `5` cortes cada 30s durante toda la segunda mitad (`90-180s`) para sostener el peso ético e historiográfico del debate (`LOS QUE DICEN QUE SÍ` vs. `NO`).
- **Material visual observado (`storyboard.jpg`):**
  1. **Archivo cinematográfico e histórico:** Bombardero B-29 sobre las nubes (`PELÍCULA DE ARCHIVO · «TALE OF TWO CITIES», EJÉRCITO DE EE. UU., 1946`), retrato de `HARRY S. TRUMAN, PRESIDENTE DE EE. UU. / EL QUE DECIDÍA`, combate y humo negro en Okinawa con tarjetas superpuestas `+12.000 ESTADOUNIDENSES MUERTOS` (azul) y `+100.000 JAPONESES, SOLDADOS Y CIVILES` (rojo), fotografía de Attlee, Truman y Stalin en `POTSDAM, 26 DE JULIO DE 1945`, primer plano del reloj de bolsillo detenido en `8:15` (`PELÍCULA DE ARCHIVO · HARRY MIMURA, USAAF, HIROSHIMA, 1946`), retrato del Emperador Hirohito (`LO QUE TRABABA TODO`), y fotografía en color de la Cúpula Genbaku hoy (`FOTO DE ARCHIVO · MUSTANG JOE · CC0`).
  2. **Cartografía vectorial:** Mapa táctico de la isla de `KYUSHU` lleno de puntos rojos y blancos que se duplican (`×2 SOLDADOS DE LO PREVISTO`), y mapa de Manchuria/Corea/Japón el `8 DE AGOSTO DE 1945` mostrando la invasión soviética de Manchuria en ocre.
  3. **Infografía vectorial de balanza:** Balanza dorada sobre fondo negro con platillos `SÍ` (azul) y `NO` (rojo), que al final se carga con bloques de peso blancos (`GOBIERNO DIVIDIDO`, `LA INVASIÓN` en el lado `SÍ` vs. `STALIN`, `LA URSS`, `EL ACUERDO`, `JAPÓN DERROTADO` en el lado `NO`) bajo el titular `NADIE PUEDE PROBARLO`.
- **Movimiento y animaciones:** Multiplicación de puntos de tropas sobre Kyushu, caída física de bloques argumentales sobre los platillos de la balanza inclinando el brazo metálico, y selección vectorial azul en `[Potsdam,]` y `[probar]`.
- **Composición 9:16 y color/grading:** Uso ejemplar de la semántica del color: azul (`#60A5FA`) asociado a la tesis oficial/estadounidense y coral rojo (`#E05A47`) asociado a las bajas japonesas y a la contra-tesis revisionista, cerrando con dorado (`#F0B429`) para la pregunta abierta final `¿ERA NECESARIA? ¿O HABÍA OTRO CAMINO?`.

---

### #04 | `4VT2qvIRUkg` — Iwo Jima 1945: la historia detrás de la foto y la segunda bandera
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `36` cortes | **ASL (0.3):** `4.86s` | **Cortes/10s:** `2.00`
  - **Cortes totales (`scene > 0.15`):** `47` cortes | **ASL (0.15):** `3.75s` | **Cortes/10s:** `2.61`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 5` | `30-60s: 6` | `60-90s: 8` | `90-120s: 7` | `120-150s: 6` | `150-180s: 4`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 6` | `30-60s: 9` | `60-90s: 10` | `90-120s: 10` | `120-150s: 8` | `150-180s: 4`
  - **Análisis de la curva:** Presenta una curva en campana clásica: inicio mesurado (`0-30s: 5` cortes) porque abre con el clip original en color de Bill Genaust ondeando la bandera, acelera en el nudo central (`60-120s: 15` cortes fuertes, `20` suaves) al contrastar la primera bandera con la segunda y la batalla subterránea, y reposa en los últimos 30 segundos (`4` cortes) al reflexionar sobre la gira de bonos de guerra.
- **Material visual observado (`storyboard.jpg`):**
  1. **Archivo histórico:** Filmación original en color de 16mm del izamiento (`PELÍCULA DE ARCHIVO · BILL GENAUST, USMC, 23-2-1945 · DOMINIO PÚBLICO`), desembarco anfibio en las playas de ceniza volcánica con ondas de alarma superpuestas (`SUENAN LAS SIRENAS`), la icónica foto de `JOE ROSENTHAL, ASSOCIATED PRESS`, y la foto de Louis Lowery enmarcada tipo Polaroid inclinada (`10:20 · LA PRIMERA`).
  2. **Cartografía e infografía vectorial de la isla:**
     - Mapa del Pacífico occidental con ruta `MARIANAS` → `IWO JIMA` → `TOKIO` (`LOS BOMBARDEROS`).
     - Silueta vectorial de la isla de Iwo Jima vista desde arriba en cuatro estados distintos: (a) red de túneles rojos con sello `NO RENDIRSE / CADA UNO: 10 ENEMIGOS`, (b) zoom macro al cono volcánico del Monte Suribachi (`LA PUNTA SUR`), (c) avance progresivo dividido por línea punteada azul (`DÍA 29 DE 36 / LA FOTO, DÍA 5 / CUEVA POR CUEVA`).
  3. **Reconstrucción de cartel propagandístico:** Póster vertical con la foto de Rosenthal, franja roja `COMPRÁ BONOS / 7.º EMPRÉSTITO DE GUERRA` y píldora `LA GIRA: BRADLEY, GAGNON Y HAYES`.
- **Movimiento y animaciones:** Trazado de vectores de vuelo naranja/azul desde las Marianas a Tokio, estampado del sello rojo `NO RENDIRSE`, ondas concéntricas de sirena sobre fotografía fija, barrido de línea de frente (`DÍA 5` a `DÍA 29`) sobre la silueta de la isla, y cajas azules en `[semana.]`, `[sirenas.]` y `[Rosenthal,]`.
- **Composición 9:16 y color/grading:** La forma alargada diagonal de la isla de Iwo Jima se aprovecha magistralmente en el formato vertical `9:16`, ocupando el centro limpio de la pantalla sobre un fondo azul profundo con cuadrícula cartográfica.

---

### #05 | `lYVMDblBX3Y` — Midway 1942: los minutos que cambiaron la guerra del Pacífico
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `25` cortes | **ASL (0.3):** `6.92s` | **Cortes/10s:** `1.39`
  - **Cortes totales (`scene > 0.15`):** `38` cortes | **ASL (0.15):** `4.62s` | **Cortes/10s:** `2.11`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 6` | `30-60s: 2` | `60-90s: 5` | `90-120s: 5` | `120-150s: 5` | `150-180s: 2`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 10` | `30-60s: 6` | `60-90s: 6` | `90-120s: 5` | `120-150s: 6` | `150-180s: 5`
  - **Análisis de la curva:** Aunque los cortes bruscos (`>0.3`) son solo `25` (ASL `6.92s`), el ritmo percibido es alto (`38` eventos `>0.15`) porque gran parte de la acción ocurre mediante **animación continua dentro del mismo plano** (ej. en `30-60s` con la matriz numérica de criptoanálisis de Rochefort y en `90-120s` con el cambio de bombas por torpedos sobre la cubierta del portaaviones japonés).
- **Material visual observado (`storyboard.jpg`):**
  1. **Archivo cinematográfico e histórico:** Metraje en color de *The Battle of Midway* (`JOHN FORD, 1942 · DOMINIO PÚBLICO`), fotografía de Joseph Rochefort recortada sobre fondo negro rodeada por una matriz verde de códigos numéricos de 5 dígitos (`49374 84574...`), vista aérea del atolón de Midway, el `USS YORKTOWN` maniobrando (`3 DÍAS DE REPARACIÓN A CONTRARRELOJ`), aviones torpederos estadounidenses a ras del mar (`LOS TORPEDEROS`), y foto cenital de tres portaaviones japoneses dejando estelas curvas de evasión bajo tres impactos ardientes (`5 MINUTOS`).
  2. **Elementos gráficos de cronómetro:** Cajas rectangulares oscuras con borde rojo y dígitos monoespaciados en rojo coral (`10:22` → `10:25`) superpuestas tanto al inicio como en el clímax de los 5 minutos fatales.
  3. **Diagramas vectoriales:** Cubierta de madera de portaaviones japonés con el círculo rojo del Hinomaru y 8 aviones grises alternando iconos de torpedos y bombas (`cambiar`), y vista de tres torpedos vectoriales acercándose en diagonal (`A las diez y veinte / 10:20`).
- **Movimiento y animaciones:** Avance del reloj digital `10:22` a `10:25`, parpadeo de columnas de números en la pantalla de inteligencia naval, permutación animada de bombas/torpedos junto a los aviones en cubierta, y aparición de dos botones de decisión al final (`ATACAR YA` en rojo vs. `ESPERAR A ESTAR LISTO` en azul).
- **Composición 9:16 y color/grading:** Predominio de azul océano profundo (`#0A2239`) contrastado con el rojo coral (`#E05A47`) de los relojes digitales y del sol naciente japonés.

---

### #06 | `KCrSmZt-A0w` — Dunkerque 1940: ¿por qué Hitler frenó los tanques?
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `37` cortes | **ASL (0.3):** `4.68s` | **Cortes/10s:** `2.08`
  - **Cortes totales (`scene > 0.15`):** `44` cortes | **ASL (0.15):** `3.96s` | **Cortes/10s:** `2.47`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 5` | `30-60s: 7` | `60-90s: 6` | `90-120s: 8` | `120-150s: 5` | `150-180s: 6`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 8` | `30-60s: 7` | `60-90s: 6` | `90-120s: 8` | `120-150s: 7` | `150-180s: 8`
  - **Análisis de la curva:** Es una de las curvas más equilibradas del corpus (`6–8` cortes cada 30s de principio a fin). Esta regularidad responde a una estructura capitular explícita: el vídeo presenta una **matriz interactiva de 4 tarjetas** (`1. TANQUES GASTADOS`, `2. LA PROMESA DE GÖRING`, `3. EL MIEDO`, `4. QUIÉN MANDA`) y regresa a esa matriz cada ~25 segundos para iluminar en rojo la siguiente hipótesis.
- **Material visual observado (`storyboard.jpg`):**
  1. **Composición en pantalla dividida (Split-screen horizontal) y archivo:** En el hook (`0-6s`) y el cierre, divide la zona central en dos franjas horizontales: arriba tanques en marcha (`PELÍCULA DE ARCHIVO · «DIVIDE AND CONQUER», EE. UU., 1943`) donde se estampa el sello rojo `HALT! ALTO!`, y abajo la playa de Dunkerque llena de restos (`FOTO DE ARCHIVO · IWM · DOMINIO PÚBLICO`). También incluye a Hitler frente a la Torre Eiffel (`BUNDESARCHIV, HEINRICH HOFFMANN`), `HERMANN GÖRING`, y Winston Churchill con subfusil Tommy (`IWM, WILLIAM GEORGE HORTON`).
  2. **Sistema de UI de 4 tarjetas (Grid 2x2):** Cuatro botones rectangulares con bordes redondeados en la parte media-baja de la imagen que cambian de gris translúcido a rojo sólido (`#C83E31`) a medida que se explican las `CUATRO RAZONES` y se vuelven a mostrar juntos en la pregunta final (`¿QUÉ PESÓ MÁS?`).
  3. **Cartografía vectorial:** Mapa del bolsillo de `DUNKERQUE` con puntos de `GB`, `FR`, `BE` y flecha negra de cerco (`400.000 HOMBRES ENCERRADOS`), y mapa táctico del asedio de `LILLE` (`RESISTEN`) con línea roja discontinua.
- **Movimiento y animaciones:** Estampado del sello `HALT!`, encendido secuencial de las 4 píldoras de razones (estilo menú de videojuego/documental interactivo), y cinco apariciones del recuadro de selección azul en subtítulos (`[Dunkerque,]`, `[razones,]`, `[Göring]`, `[ayuda]`, `[Churchill]`).
- **Composición 9:16 y color/grading:** Tonos sepia y monocromáticos de archivo contrastados con el rojo intenso de las tarjetas activas y el dorado de los titulares (`DUNKERQUE`, `CUATRO RAZONES`, `SE NECESITAN BARCOS`).

---

### #07 | `yeMKOTtYlWU` — Stalingrado en 3 minutos: «Ni un paso atrás»
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `51` cortes (el más alto del canal) | **ASL (0.3):** `3.46s` | **Cortes/10s:** `2.83`
  - **Cortes totales (`scene > 0.15`):** `122` cortes (máximo absoluto del corpus) | **ASL (0.15):** `1.46s` | **Cortes/10s:** `6.78`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 5` | `30-60s: 7` | `60-90s: 12` | `90-120s: 6` | `120-150s: 14` | `150-180s: 7`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 26` | `30-60s: 8` | `60-90s: 13` | `90-120s: 41` | `120-150s: 26` | `150-180s: 8`
  - **Análisis de la curva:** Es el montaje más vertiginoso y agresivo de los 20 vídeos. Tiene dos picos masivos de actividad visual: en `60-90s` (`12` cortes fuertes, combate urbano edificio por edificio y cruce nocturno del Volga bajo fuego) y en `90-150s` (`20` cortes fuertes y `67` eventos `>0.15`), donde el frenesí de metraje soviético en la nieve y la pinza de la Operación Urano (`KALACH` ↔ `STALINGRADO`) disparan la tasa de cambio de fotograma.
- **Material visual observado (`storyboard.jpg`):**
  1. **Archivo soviético y alemán de alto impacto:** Metraje de `«STALINGRADO», CDSF, 1943 · DOMINIO PÚBLICO` (bombardeos, combate en pisos derruidos `CADA PISO`, lanchas cruzando el Volga `DE NOCHE, BAJO EL FUEGO`, soldados en ventisca a `-30 °C BAJO CERO / SIN COMIDA / SIN MUNICIÓN`), la fuente de los niños Barmaley (`FOTO DE ARCHIVO · SERGEY STRUNNIKOV`), vista aérea de la Luftwaffe (`BUNDESARCHIV, KLOSE`), y captura del mariscal Friedrich Paulus (`OBEDECER`).
  2. **Documento histórico original:** Página impresa original en ruso de la Orden Nº 227 (`ПРИКАЗ № 227`) con cinta mecanografiada superpuesta `28 DE JULIO DE 1942` (`FOTO DE ARCHIVO · P. FISKÓ · DOMINIO PÚBLICO`).
  3. **Cartografía vectorial:** Mapa de avance alemán hacia el Volga y el Cáucaso con grandes flechas negras sombreadas (`STALINGRADO`), y mapa invernal gris claro de la Operación Urano donde dos flechas rojas soviéticas se cierran en pinza sobre `KALACH` dejando cercado al 6.º Ejército en `STALINGRADO`.
- **Movimiento y animaciones:** Crecimiento de vectores de ataque sobre el mapa del Volga, choque de flechas rojas en `KALACH`, superposición de etiqueta climática azul hielo `-30 °C BAJO CERO`, y cajas de selección azul en `[civiles.]` y `[obedecer]`.
- **Composición 9:16 y color/grading:** Paleta gélida en blanco y negro de alto grano contrastada con el rojo sangre del titular `STALINGRADO` y las flechas soviéticas, y el azul glacial de las etiquetas de invierno (`DE NOCHE, BAJO EL FUEGO`, `-30 °C`).

---

### #08 | `VKEIpXxGMVk` — Cândido Godói: el pueblo de los gemelos y la teoría sobre Mengele
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `26` cortes | **ASL (0.3):** `6.59s` | **Cortes/10s:** `1.46`
  - **Cortes totales (`scene > 0.15`):** `29` cortes | **ASL (0.15):** `5.93s` | **Cortes/10s:** `1.63`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 6` | `30-60s: 5` | `60-90s: 5` | `90-120s: 4` | `120-150s: 3` | `150-180s: 3`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 6` | `30-60s: 5` | `60-90s: 6` | `90-120s: 5` | `120-150s: 3` | `150-180s: 4`
  - **Análisis de la curva:** Presenta un ritmo pausado de investigación científica/misterio que va desacelerando gradualmente de `6` cortes en los primeros 30s a `3` cortes en los tramos finales (`120-180s`), permitiendo que las animaciones explicativas (el gráfico de barras por décadas `'30–'90` y la doble hélice de ADN) se desarrollen sin cortes abruptos.
- **Material visual observado (`storyboard.jpg`):**
  1. **Escenario e ilustración vectorial 2D:** Pueblo pintoresco con camino central, casas con entramado e iglesia al fondo donde van apareciendo parejas de gemelos rubios idénticos (`Imaginá vivir...`); el mismo pueblo de noche cuando entra la silueta negra de un hombre con sombrero y maletín dejando frascos de medicina en el suelo (`LA TEORÍA`); y cuna de madera al final con dos bebés gemelos dormidos.
  2. **Fotografías y documentos reales:** Pórtico de entrada a la ciudad (`FOTO · CÂNDIDO GODÓI · CC BY-SA 3.0 · FELIPE P / «TERRA DOS GÊMEOS»`), niños gemelos sobrevivientes en Auschwitz (`FOTO · CHICOS LIBERADOS, 1945 · FILMACIÓN SOVIÉTICA`), pasaporte falso de la Cruz Roja Italiana con sello `ANNULLATO` a nombre de `«HELMUT GREGOR»` (`CC BY-SA 3.0 · JACKDAWSON`), y retrato policial de Josef Mengele (`1985: ABREN LA TUMBA`).
  3. **Visualización de datos y ciencia:** Mapa vectorial verde de Rio Grande do Sul (`CÂNDIDO GODÓI`), gráfico de barras cronológico por décadas (`'30 '40 '50 '60 '70 '80 '90`) demostrando que los gemelos ya nacían antes de los años 60, y doble hélice de ADN en rosa/azul con un par de bases brillando en dorado (`UNA VARIANTE DE UN GEN`, el gen TP53).
- **Movimiento y animaciones:** Multiplicación de parejas de niños gemelos en la calle del pueblo, haz de linterna de la silueta oscura en los barracones, animación de barras estadísticas por décadas, rotación/iluminación del gen mutado en la hélice de ADN, y selección azul en `[Gregor.]` y `[remedios]`.
- **Composición 9:16 y color/grading:** Alterna el verde campestre luminoso de la aldea brasileña con el fondo negro abisal (`#0B0E14`) de la sección de Auschwitz y la genética molecular.

---

### #09 | `UjI03Si4VA8` — La Primera Guerra Mundial en 3 minutos: de Sarajevo al armisticio
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `47` cortes (2.º más alto del corpus) | **ASL (0.3):** `3.75s` | **Cortes/10s:** `2.61`
  - **Cortes totales (`scene > 0.15`):** `114` cortes | **ASL (0.15):** `1.57s` | **Cortes/10s:** `6.33`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 8` | `30-60s: 9` | `60-90s: 10` | `90-120s: 6` | `120-150s: 7` | `150-180s: 7`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 8` | `30-60s: 9` | `60-90s: 69` | `90-120s: 6` | `120-150s: 15` | `150-180s: 7`
  - **Análisis de la curva:** Ritmo altísimo y sostenido (`8–10` cortes fuertes cada 30s en la primera mitad y `6–7` en la segunda). El pico extremo de `69` detecciones suaves (`>0.15`) entre `68.15s` y `72.32s` se debe a una ráfaga de metraje de archivo de combate y artillería en *The Battle of the Somme (1916)* con fogonazos y trepidación de celuloide a cada fotograma.
- **Material visual observado (`storyboard.jpg`):**
  1. **Cartografía histórica estilo pergamino (`#C9BC9C` sobre mar `#0B1724`):** Una variante cromática exclusiva para la Primera Guerra Mundial. Muestra `SARAJEVO` con ondas concéntricas y flechas naranjas de reacción en cadena hacia los imperios europeos (`LAS ALIANZAS`, `28 DE JULIO - 4 DE AGOSTO DE 1914`), el Plan Schlieffen a través de Bélgica hacia `PARÍS` (`SEPTIEMBRE DE 1914 · EL MARNE`) con flechas rojas alemanas frenadas por una línea azul francesa, y el plano final `EL POLVORÍN`.
  2. **Fotografía y cine de época (1914–1918):** Movilización en `París, 2 de agosto de 1914` (`AGENCE ROL · GALLICA`), arresto en `Sarajevo, 28-6-1914`, soldados británicos en `THE BATTLE OF THE SOMME, 1916 · IWM` con triple titular `AMETRALLADORAS / ALAMBRE / ARTILLERÍA`, trinchera francesa en `VERDÚN · 1916` con contador `75 DÍAS` (que avanza hasta 300), manifestación bolchevique con pancartas (`RUSIA SALE / A. R. WILLIAMS · PETROGRADO, 1917`), y cruz de piedra cubierta de musgo en un cementerio militar bajo nieve/hojas secas (`D-KURU · CC BY-SA 4.0`).
- **Movimiento y animaciones:** Propagación en cadena de las alianzas sobre el mapa de Europa (coloreando países secuencialmente en salmón y azul), contador de días de Verdún en esquina superior izquierda (`75 DÍAS` → `300`), y cajas azules en `[alianzas:]` y `[Marne,]`.
- **Composición 9:16 y color/grading:** Estética de archivo de principios del siglo XX: mapas en tonos hueso/pergamino y rojo terracota que armonizan con el blanco y negro virado al sepia de las placas fotográficas de la Agence Rol. Notice que este vídeo utiliza la píldora de contexto blanco sobre negro con borde fino (`París, 2 de agosto de 1914`) justo encima de la micro-píldora de crédito.

---

### #10 | `g_M7r8EMoFg` — El caballo de Troya: el engaño que abrió las puertas de una ciudad
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `32` cortes | **ASL (0.3):** `5.45s` | **Cortes/10s:** `1.78`
  - **Cortes totales (`scene > 0.15`):** `39` cortes | **ASL (0.15):** `4.50s` | **Cortes/10s:** `2.17`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 6` | `30-60s: 8` | `60-90s: 5` | `90-120s: 4` | `120-150s: 5` | `150-180s: 4`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 7` | `30-60s: 10` | `60-90s: 5` | `90-120s: 6` | `120-150s: 7` | `150-180s: 4`
  - **Análisis de la curva:** Al tratarse de un relato mitológico-arqueológico sin metraje bélico del siglo XX, el ritmo es más contemplativo (`ASL 5.45s`), con un pico narrativo en `30-60s` (`8` cortes fuertes, `10` suaves) cuando se presenta la construcción del caballo por Odiseo y su abandono en la playa, manteniendo `4–5` cortes por bloque en la segunda mitad.
- **Material visual observado (`storyboard.jpg`):**
  1. **Pintura histórica del siglo XVIII y XIX (Dominio Público):** *La procesión del caballo de Troya* y *La construcción del caballo* de Giovanni Domenico Tiepolo (`G. D. TIEPOLO, c. 1760 · NATIONAL GALLERY`), *El caballo de Troya* de Henri-Paul Motte (`H.-P. MOTTE, 1874`), *Casandra* de Evelyn De Morgan (`E. DE MORGAN, «CASANDRA», 1898`), y el grupo escultórico del Laocoonte en penumbra.
  2. **Metraje documental y fotografía contemporánea:** Recreación 3D del caballo en la playa con niebla (`ZDF / TERRA X · CC BY 4.0`, usado tanto en plano general como en zoom a `LA TRAMPILLA`), monumento del caballo en Çanakkale (`CABALLO EN EL SITIO DE TROYA · MTHELETTER · CC BY-SA 4.0`), y murallas ciclópeas reales (`MICENAS · LE MONDE EN VIDÉO · CC BY 3.0`) con el doble titular `¿UNA MÁQUINA DE ASEDIO? / ¿UN TERREMOTO?`.
  3. **Cartografía estilizada:** Mapa del estrecho de los Dardanelos y el mar Egeo en un llamativo esquema de **negro sobre naranja fuego degradado** (`TROYA / COSTA DE LA ACTUAL TURQUÍA`).
- **Movimiento y animaciones:** Superposición de llamas vectoriales animadas en la base del cuadro de Tiepolo (`UN REGALO`), paneos suaves tipo *Ken Burns* sobre los lienzos clásicos para seguir la acción narrativa (de los constructores a las murallas), niebla en movimiento en `LA TRAMPILLA`, y selección azul en `[Troya,]` y `[desaparece.]`.
- **Composición 9:16 y color/grading:** Uso de pinturas verticales o reencuadres verticales de óleos clásicos, unificados mediante un etalonaje cálido (ocres, bronces y naranjas de Troya en llamas).

---

### #11 | `V3ase69Rap8` — Napoleón: cuándo actuar y cuándo esperar | De Austerlitz a Waterloo
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `16` cortes (el mínimo absoluto del corpus) | **ASL (0.3):** `10.53s` | **Cortes/10s:** `0.89`
  - **Cortes totales (`scene > 0.15`):** `19` cortes | **ASL (0.15):** `8.95s` | **Cortes/10s:** `1.06`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 6` | `30-60s: 2` | `60-90s: 3` | `90-120s: 0` | `120-150s: 2` | `150-180s: 3`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 7` | `30-60s: 4` | `60-90s: 3` | `90-120s: 0` | `120-150s: 2` | `150-180s: 3`
  - **Análisis de la curva:** ¿Por qué este vídeo tiene `0` cortes de escena detectados por FFmpeg entre `90s` y `120s` (`80.47s` → `140.0s`, un plano continuo de `59.5 segundos`)? La inspección del `storyboard.jpg` lo explica de inmediato: es un **experimento de animación continua en diorama 2D de bloques pixel-art (estética tipo Minecraft 2D)**. En lugar de cortar entre planos estáticos, la cámara virtual realiza un *travelling* lateral continuo y anima a los personajes sobre la colina de Pratzen en Austerlitz (`AUSTERLITZ 2·12·1805` → `PRATZEN, VACÍO` → `¿CUÁNTO TARDÁS?` → `VICTORIA`).
- **Material visual observado (`storyboard.jpg` y `hook_3s.jpg`):**
  1. **Escenario 100% Pixel-Art / Voxel 2D Programático:** No utiliza ninguna fotografía de archivo. Todo el vídeo está construido con *sprites* de bloques pixelados e iluminación volumétrica suave:
     - Habitación de Napoleón con su asistente abrochándole el chaleco mientras saltan chispas amarillas de impaciencia y un reloj analógico marca el paso del tiempo (`APURADO`, y al cierre `CERO ERRORES`).
     - Primer plano vertical de los botones dorados del chaleco trabándose en los ojales (`Los dedos se trababan`).
     - Columnata clásica de bloques de piedra y ladrillo.
     - Mapa en perspectiva de bloques de hierba atravesado por dos franjas de agua (`CANAL DE LA MANCHA` arriba y `DANUBIO` abajo) en `1805`.
     - Reloj gigante con la cita enmarcada `«PÍDANME CUALQUIER COSA, MENOS TIEMPO»`.
     - Escena lateral del campo de batalla de `AUSTERLITZ 2·12·1805` (Napoleón a caballo a la izquierda, `2 EMPERADORES` en la colina de `PRATZEN, VACÍO`, diálogo tipo bocadillo `¿CUÁNTO TARDÁS?`, y toma de la colina con bandera tricolor `VICTORIA`).
     - Escena lluviosa sobre barro rojizo en `WATERLOO 1815` con el reloj marcando las `11:30` y el texto `LOS PRUSIANOS`.
- **Movimiento y animaciones:** Animación *frame-by-frame* de los brazos pixelados de Napoleón, partículas cuadradas amarillas, rotación de las agujas de los relojes vectoriales, desplazamiento lateral de tropas a caballo sobre el terreno escalonado, lluvia en Waterloo, y el mismo motor de subtítulos superior con caja azul en `[emperadores:]` y `[equivocarte.]`.
- **Composición 9:16 y color/grading:** Los personajes y el terreno se sitúan entre `y = 750px` y `y = 1750px`, dejando el cielo o la pared superior despejados para los subtítulos (`y = 320px`) y los titulares con contorno negro (`APURADO`, `VICTORIA`, `CERO ERRORES`).

---

### #12 | `GZNpPvHITiM` — ¿Por qué Marco Aurelio dormía en el suelo a los 12 años?
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `19` cortes | **ASL (0.3):** `8.95s` | **Cortes/10s:** `1.06`
  - **Cortes totales (`scene > 0.15`):** `26` cortes | **ASL (0.15):** `6.63s` | **Cortes/10s:** `1.45`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 5` | `30-60s: 3` | `60-90s: 3` | `90-120s: 3` | `120-150s: 2` | `150-180s: 3`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 5` | `30-60s: 4` | `60-90s: 5` | `90-120s: 4` | `120-150s: 4` | `150-180s: 4`
  - **Análisis de la curva:** Inaugura en el corpus el **sub-estilo de Ilustración Geométrica 2D para Historia Antigua y Filosofía**, caracterizado por un ritmo pausado, meditativo y fluido (`4–5` cambios suaves cada 30s, ASL `6.63s`), donde las transiciones entre escenas se apoyan en movimientos de cámara vectoriales (zooms hacia el fondo de una columnata o apertura de un cuaderno) más que en cortes bruscos.
- **Material visual observado (`storyboard.jpg`):**
  1. **Ilustración vectorial geométrica con iluminación radial:**
     - Gran salón imperial romano con columnas de mármol en perspectiva central y un lecho púrpura al fondo (`El palacio` / `Familia riquísima`), donde aparece el joven Marco Aurelio vestido con túnica blanca y manto oliva; en la escena final, el salón está oscuro y él duerme en el suelo sobre una estera junto a la cama vacía (`No era para sufrir`).
     - Primer plano en primera persona (POV) de una mano con manga púrpura escribiendo sobre un cuaderno abierto (`Meditaciones, libro 1` / `«un catre y una piel»` y más adelante `Meditaciones 6.30` / `«No te vuelvas un César»`).
     - Metáfora visual psicológica: una gigantesca mano negra en sombra cerniéndose sobre el joven Marco Aurelio iluminado por una vela (`Quitarle poder al miedo`).
     - Escena de la subasta imperial (`Los vestidos de su esposa` con copas de oro, joyas y estatuas) y campamento militar nocturno junto al río bajo un cielo estrellado (`En la frontera del Danubio`).
     - Cierre simbólico: el libro púrpura `MARCO AURELIO / MEDITACIONES` iluminado frente a una copa de oro apagada en la penumbra (`Las copas de oro, no`).
  2. **Fotografía arqueológica:** Busto en mármol de Marco Aurelio joven con una corona de laurel dorada vectorial animada flotando sobre su frente (`FOTO · MARCO AURELIO JOVEN, MUSEOS CAPITOLINOS · DOMINIO PÚBLICO` y píldora `Iba a ser emperador`).
- **Movimiento y animaciones:** Zoom *dolly-in* por el pasillo de columnas, escritura progresiva de líneas en el cuaderno, caída de joyas brillantes, titileo de hogueras en el Danubio y desvanecimiento de la copa de oro.
- **Composición 9:16 y color/grading:** Paleta cálida dorada, bronce y púrpura imperial (`#7A1C54`). Introduce un elemento de diseño distintivo de la serie antigua: **píldoras de contexto alineadas a la izquierda con borde dorado fino** (`El palacio`, `Meditaciones, libro 1`, `En la frontera del Danubio`).

---

### #13 | `ff2r8EirvVI` — Hernán Cortés no quemó sus naves: la historia detrás del mito
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `24` cortes | **ASL (0.3):** `7.16s` | **Cortes/10s:** `1.34`
  - **Cortes totales (`scene > 0.15`):** `27` cortes | **ASL (0.15):** `6.39s` | **Cortes/10s:** `1.51`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 3` | `30-60s: 5` | `60-90s: 4` | `90-120s: 4` | `120-150s: 5` | `150-180s: 3`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 3` | `30-60s: 5` | `60-90s: 4` | `90-120s: 4` | `120-150s: 7` | `150-180s: 4`
  - **Análisis de la curva:** Ritmo narrativo constante de `4–5` cortes por bloque de 30s, con un repunte de actividad en `120-150s` (`7` eventos `>0.15`) durante el clímax de la marcha hacia Tenochtitlan y la construcción de los 13 bergantines con las piezas salvadas de las naves hundidas.
- **Material visual observado (`storyboard.jpg`):**
  1. **Ilustración vectorial geométrica 2D:**
     - Hook visual (`0-11s`): Fila de soldados españoles con morrión y lanzas de espaldas contemplando barcos envueltos en grandes llamas naranjas (representando el mito popular antes de desmentirlo).
     - Costa de `CUBA, 1519` enmarcada por dos palmeras con la flota en el horizonte.
     - Dos emisarios mexicas con penachos de plumas verdes/rojas y escudos entregando el gran disco solar de oro (`llegaron con regalos`).
     - Fundación de `Villa Rica de la Vera Cruz` con una cruz de madera clavada en la playa frente a los soldados.
     - Escena nocturna de conspiración (`La conjura para huir`) y primer plano de un casco de madera encallado con agujeros negros en la línea de flotación mientras los demás barcos se hunden al fondo (`Perforados y desarmados`).
     - Columna de guerreros indígenas aliados (tlaxcaltecas) marchando por las montañas verdes, y flota de **13 bergantines** con cruces rojas en las velas navegando en el lago Texcoco.
  2. **Retratos y pinturas históricas enmarcadas:** Retrato del siglo XVI de `Hernán Cortés / Rebelde` (`FOTO · CORTÉS, s. XVI · CC BY-SA 3.0`) y biombo/pintura colonial de `8 de noviembre de 1519 / «Un encantamiento»` (`FOTO · ENCUENTRO DE CORTÉS Y MOCTEZUMA · DOMINIO PÚBLICO`).
- **Movimiento y animaciones:** Fuego animado en el hook, hundimiento progresivo de los cascos perforados en el mar, marcha rítmica de lanzas y escudos por las colinas, y cuatro cajas de selección azul en subtítulos (`[naves,]`, `[rebelde.]`, `[Cruz,]`, `[perforados]`).
- **Composición 9:16 y color/grading:** Composición por franjas horizontales limpias (cielo degradado arriba para subtítulos, horizonte marítimo o montañoso en el medio, personajes en el tercio medio-bajo).

---

### #14 | `VFppMLRXRqk` — ¿Por qué Marco Aurelio dejó Roma en manos de Cómodo?
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `28` cortes | **ASL (0.3):** `6.17s` | **Cortes/10s:** `1.56`
  - **Cortes totales (`scene > 0.15`):** `35` cortes | **ASL (0.15):** `4.97s` | **Cortes/10s:** `1.96`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 6` | `30-60s: 3` | `60-90s: 3` | `90-120s: 6` | `120-150s: 5` | `150-180s: 5`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 9` | `30-60s: 5` | `60-90s: 5` | `90-120s: 6` | `120-150s: 5` | `150-180s: 5`
  - **Análisis de la curva:** Fuerte arranque en `0-30s` (`9` eventos `>0.15`) al contrastar el mito de *Gladiador* con la sucesión de los Cinco Buenos Emperadores (`CASI 100 AÑOS`), Valle reflexivo entre `30-90s` (`5` eventos por bloque) explicando la crianza de Cómodo en el Danubio, y reactivación en `90-180s` (`5–6` cortes por bloque) con la muerte de Marco Aurelio y las locuras de Cómodo en el Coliseo.
- **Material visual observado (`storyboard.jpg`):**
  1. **Ilustración vectorial simbólica:**
     - Una mano imperial sosteniendo una corona de laurel de oro resplandeciente y pasándola a otra mano (`0-8s`), y la misma corona oxidándose/oscureciéndose al final cuando Dion Casio dice que Roma pasó «de un reino de oro a uno de hierro y óxido».
     - Fila de emperadores antoninos (`CASI 100 AÑOS`).
     - Marco Aurelio y el joven Cómodo de espaldas mirando el campamento nocturno (`Al frente del Danubio`).
     - Tablilla de `CONSVL` con monedas de oro y mazo sobre fondo púrpura oscuro.
     - Escena del anfiteatro: Cómodo vestido de gladiador en la arena alzando una cabeza de avestruz ante los senadores sentados en primera fila (`avestruz`).
     - Cierre luminoso: el cuaderno abierto de las *Meditaciones* irradiando ondas concéntricas de luz rodeado de ediciones modernas en distintos idiomas (`Las Meditaciones sobrevivieron`).
  2. **Numismática, escultura y grabado histórico:** Moneda de oro romana (`FOTO · ÁUREO DE CÓMODO · CC BY-SA 2.5 · CNG`), busto de `Marco Aurelio, 58 años` (`DOMINIO PÚBLICO`), y grabado de `Casio Dion, senador` (`DOMINIO PÚBLICO`).
- **Movimiento y animaciones:** Transferencia de la corona de laurel entre manos, degradación de color de oro brillante a hierro oxidado en la corona del final, ondas de luz emanando del libro, y caja de selección azul en `[avestruz]`.
- **Composición 9:16 y color/grading:** Cuando se insertan imágenes cuadradas de monedas o bustos (`1:1`), el sistema coloca una copia desenfocada y oscurecida (`blur(40px) brightness(0.35)`) de la misma imagen en las bandas superior e inferior para mantener la atmósfera cromática sin invadir la zona de subtítulos.

---

### #15 | `fGYdtXyKbtQ` — Marco Aurelio y sus Meditaciones: el diario del emperador estoico
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `29` cortes | **ASL (0.3):** `5.90s` | **Cortes/10s:** `1.64`
  - **Cortes totales (`scene > 0.15`):** `32` cortes | **ASL (0.15):** `5.36s` | **Cortes/10s:** `1.81`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 6` | `30-60s: 4` | `60-90s: 5` | `90-120s: 6` | `120-150s: 3` | `150-180s: 5`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 6` | `30-60s: 5` | `60-90s: 5` | `90-120s: 7` | `120-150s: 4` | `150-180s: 5`
  - **Análisis de la curva:** Mantiene un pulso sumamente estable (`5–7` eventos cada 30s), alternando escenas íntimas a la luz de una vela con momentos de crisis imperial (la peste antonina, la subasta del palacio y la rebelión de Avidio Casio en el año 175).
- **Material visual observado (`storyboard.jpg`):**
  1. **Ilustración vectorial geométrica:**
     - Trono imperial elevado al final de un pasillo flanqueado por legionarios con escudos rojos `SPQR`.
     - Cuaderno abierto a la luz de una vela en la tienda de campaña (motivo recurrente en el hook `0-5s` y en el cierre `172-177s` para crear un bucle perfecto).
     - Guerreros germanos con escudos redondos al otro lado del río (`La guerra`).
     - Mazo de subasta sobre mesa frente a columnas (`El remate`).
     - Pergamino escrito en caracteres griegos clásicos encabezado por `ΤΑ ΕΙΣ ΕΑΥΤΟΝ` con la píldora `En griego`, seguido de hojas de notas tachadas y reordenadas (`Recordatorios`).
     - Reloj de arena dorada cayendo (`Se ordena: hacé`), figura solitaria en un círculo de luz (`convierte`), y rebelión de `Avidio Casio` en el `AÑO 175` con cartel `MARCVS MORTVVS?` frente a las legiones.
  2. **Archivo numismático y escultórico:** Moneda de oro de Marco Aurelio (`FOTO · ÁUREO DEL 174 · DOMINIO PÚBLICO · CNG`) y fotografía de la estatua ecuestre en bronce del Capitolio (`FOTO · ESTATUA ECUESTRE · DOMINIO PÚBLICO · ALVESGASPAR`).
- **Movimiento y animaciones:** Parpadeo cálido del halo de la vela junto al cuaderno, caída de granos en el reloj de arena, aparición de caracteres griegos, y cajas de selección azul en `[recordatorios.]` y `[noche,]`.
- **Composición 9:16 y color/grading:** Iluminación de claroscuro nocturno (fondos marrón sepia oscuro `#231911` iluminados por el foco ámbar `#F6C863` de la vela).

---

### #16 | `3tSKNGKJOrc` — Epicteto: el esclavo que inspiró a Marco Aurelio | Estoicismo
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `28` cortes | **ASL (0.3):** `6.14s` | **Cortes/10s:** `1.57`
  - **Cortes totales (`scene > 0.15`):** `35` cortes | **ASL (0.15):** `4.94s` | **Cortes/10s:** `1.97`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 5` | `30-60s: 4` | `60-90s: 5` | `90-120s: 2` | `120-150s: 7` | `150-180s: 5`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 9` | `30-60s: 5` | `60-90s: 5` | `90-120s: 3` | `120-150s: 8` | `150-180s: 5`
  - **Análisis de la curva:** Destaca por un arranque dinámico (`9` eventos suaves en `0-30s`), una pausa filosófica en `90-120s` (`3` eventos, donde ilustra la parábola del robo de la lámpara de hierro y la vasija de barro), y una aceleración en `120-150s` (`8` eventos) cuando despliega el diagrama estoico de la dicotomía del control (`Depende de vos` vs. `No depende`).
- **Material visual observado (`storyboard.jpg`):**
  1. **Ilustración vectorial y metáforas visuales:**
     - Pierna desnuda con un grillete de hierro y cadena tensa en el tobillo (`0-4s`), la misma pierna siendo retorcida por dos manos (`Según un relato antiguo`), el grillete abriéndose con chispas de luz (`Libre`), y en el plano final la pierna con la cadena rota junto a una lámpara de aceite encendida.
     - Emperador Marco Aurelio en su trono leyendo un rollo de papiro.
     - Epicteto con barba y bastón caminando por una calle romana (`Rengo para siempre`).
     - Habitación nocturna donde roban su lámpara (`Una lámpara de hierro`) y primer plano de una vasija de terracota iluminada por un haz de luz que luego aparece rota en pedazos en el suelo (`jarra`).
     - **Diagrama filosófico en pantalla dividida vertical:** Línea divisoria central dorada; a la izquierda `Depende de vos` con tres píldoras doradas sólidas (`DECIDIR`, `QUERER`, `PENSAR`) sobre una mano abierta; a la derecha `No depende` en gris oscuro.
  2. **Fotografía arqueológica:** Ruinas del teatro romano de `Hierápolis / Hacia el año 50` (`FOTO · HIERÁPOLIS · CC BY-SA 2.0 · C. RADDATO`) y busto de `MARCO AURELIO JOVEN · DOMINIO PÚBLICO · D. DESCOUENS`.
- **Movimiento y animaciones:** Tensión y ruptura de los eslabones de la cadena, fractura física de la vasija de barro, aparición escalonada de los bloques `DECIDIR / QUERER / PENSAR`, y cuatro cajas de selección azul en subtítulos (`[esclavo]`, `[rengo]`, `[jarra,]`, `[vos.]`).
- **Composición 9:16 y color/grading:** Excelente aprovechamiento del eje vertical gracias al motivo de la pierna encadenada y la división vertical de la dicotomía estoica.

---

### #17 | `kOpUJPR9BOM` — Dien Bien Phu: la trampa que derrotó a Francia en Vietnam
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `29` cortes | **ASL (0.3):** `5.97s` | **Cortes/10s:** `1.62`
  - **Cortes totales (`scene > 0.15`):** `32` cortes | **ASL (0.15):** `5.42s` | **Cortes/10s:** `1.79`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 4` | `30-60s: 5` | `60-90s: 4` | `90-120s: 6` | `120-150s: 6` | `150-180s: 4`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 6` | `30-60s: 5` | `60-90s: 5` | `90-120s: 6` | `120-150s: 6` | `150-180s: 4`
  - **Análisis de la curva:** Cadencia táctica muy homogénea (`5–6` eventos por tramo de 30s), diseñada para explicar paso a paso la ingeniería militar del asedio: cómo Francia ocupa el fondo del valle y cómo el general Giap sube la artillería a las montañas circundantes y excava trincheras concéntricas.
- **Material visual observado (`storyboard.jpg`):**
  1. **Esquemas topográficos y tácticos 2D:**
     - Cielo azul grisáceo con decenas de paracaídas blancos descendiendo bajo el titular `NOVIEMBRE 1953`.
     - Vista en perspectiva del valle verde de Dien Bien Phu rodeado de montañas oscuras, con la pista de aterrizaje en el centro y las posiciones fortificadas francesas marcadas con banderines azules e iluminadas con nombres femeninos (`Gabrielle`, `Béatrice`, `Isabelle` bajo `NOMBRES DE MUJER`).
     - Siluetas de soldados del Viet Minh en la ladera nocturna bajo la lluvia arrastrando un cañón cuesta arriba con cuerdas blancas (`A MANO Y CON SOGAS`).
     - El mismo valle rodeado ahora por una corona de puntos rojos de artillería en las crestas montañosas (`4 A 1`), suministros cayendo en paracaídas fuera del perímetro, y en el cierre un anillo amarillo de trincheras estrangulando la pista (`SUBESTIMAR`).
     - Infografía aérea sobre fondo azul cuadriculado: dos filas de bombarderos plateados bajo el sello azul `OPERACIÓN BUITRE / B-29 · 42`.
  2. **Cartografía y archivo histórico:** Mapa de Indochina con círculo amarillo sobre `Dien Bien Phu` respecto a `Hanói`, y mapa final de la partición de Vietnam en el `PARALELO 17` (`NORTE: COMUNISTA` en rojo con estrella amarilla). Fotografías de Ho Chi Minh (`7 AÑOS de guerra en Indochina / FOTO DE ARCHIVO · 1946`) y de soldados del Viet Minh alzando la bandera sobre el búnker de De Castries (`7 MAY 1954 / El puesto de mando, 7-5-1954 / FOTO DE ARCHIVO · EJÉRCITO POPULAR DE VIETNAM`).
- **Movimiento y animaciones:** Descenso fluido de paracaidistas, tracción del cañón por la pendiente bajo lluvia diagonal, aparición de puntos rojos en la cresta del valle, avance de líneas de trinchera y caja azul en `[sogas.]`.
- **Composición 9:16 y color/grading:** La cuenca geográfica del valle se dibuja como un anfiteatro en la mitad inferior de la pantalla vertical, haciendo que el espectador sienta visualmente el encierro de las tropas francesas abajo y la altura de las montañas arriba.

---

### #18 | `Km3mMU1pOpM` — ¿Por qué Truman destituyó a MacArthur? | Guerra de Corea
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `36` cortes | **ASL (0.3):** `4.86s` | **Cortes/10s:** `2.00`
  - **Cortes totales (`scene > 0.15`):** `38` cortes | **ASL (0.15):** `4.62s` | **Cortes/10s:** `2.11`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 7` | `30-60s: 6` | `60-90s: 6` | `90-120s: 7` | `120-150s: 6` | `150-180s: 4`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 8` | `30-60s: 6` | `60-90s: 6` | `90-120s: 7` | `120-150s: 7` | `150-180s: 4`
  - **Análisis de la curva:** Ritmo político-militar ágil y constante (`6–8` cortes cada 30s durante los primeros dos minutos y medio), alternando mapas estratégicos de Corea/China con documentos presidenciales y diagramas institucionales.
- **Material visual observado (`storyboard.jpg` y `hook_3s.jpg`):**
  1. **Infografías políticas y tipográficas 2D:**
     - Hook (`0-4s`): Silueta nocturna de colinas con destellos de artillería y bengalas desenfocadas bajo `ABRIL 1951.`.
     - Escritorio presidencial con lámpara verde de banquero y documento `PROPUESTA DE PAZ` (`MARZO 1951`).
     - Carpeta abierta mostrando un texto subrayado en rojo: `Un desafío a la autoridad del presidente.` bajo el titular dorado `AUTORIDAD`.
     - Balanza de poder (`ECHAR A UN HÉROE`): en el platillo izquierdo el gorro negro con insignia presidencial/civil y en el derecho las **5 estrellas doradas de General del Ejército** con la gorra de MacArthur.
     - Rueda de prensa nocturna a la `1:00 AM` (`11 ABR 1951` con reloj analógico marcando la 1:00 y fila de periodistas con libretas blancas iluminadas).
     - Avión aterrizando frente al puente Golden Gate al atardecer ante una multitud con pancartas (`SAN FRANCISCO`).
     - **Tipografía cinética de tachado sobre mapa (`EQUIVOCADO`):** La célebre frase del general Omar Bradley («la guerra equivocada, en el lugar equivocado, en el momento equivocado, con el enemigo equivocado») ejecutada mediante las palabras `GUERRA`, `LUGAR`, `MOMENTO`, `ENEMIGO` atravesadas secuencialmente por una línea roja horizontal.
     - Cierre institucional (`¿QUIÉN MANDA?`): La Casa Blanca arriba conectada por un haz vertical donde caen votos dentro de una urna electoral en la base.
  2. **Archivo y cartografía:** Fotografía de `Gral. Douglas MacArthur, Corea, 1950` (`HÉROE / FOTO DE ARCHIVO · EJÉRCITO DE EE. UU., 1950`), y mapas de la península de Corea mostrando la frontera del río Yalu en rojo (`«CASI NINGUNA CHANCE»`) y la amenaza naval sobre Taiwán/China (`LA GUERRA A CHINA`).
- **Movimiento y animaciones:** Tachado animado en rojo de la lista vertical (`~~GUERRA~~ / ~~LUGAR~~ / ~~MOMENTO~~ / ~~ENEMIGO~~`), oscilación de la balanza de 5 estrellas, vuelo del avión por San Francisco, caída de papeletas en la urna, y selección azul en `[héroe:]` y `[autoridad]`.
- **Composición 9:16 y color/grading:** Transiciones limpias entre el azul naval de los mapas de Corea, el marrón caoba de los despachos de Washington y el atardecer naranja de San Francisco.

---

### #19 | `OmO_msj8Wy8` — Inchon: la apuesta de MacArthur contra la marea | Ep. 4
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `40` cortes | **ASL (0.3):** `4.39s` | **Cortes/10s:** `2.22`
  - **Cortes totales (`scene > 0.15`):** `41` cortes | **ASL (0.15):** `4.29s` | **Cortes/10s:** `2.28`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 8` | `30-60s: 5` | `60-90s: 6` | `90-120s: 7` | `120-150s: 7` | `150-180s: 7`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 9` | `30-60s: 5` | `60-90s: 6` | `90-120s: 7` | `120-150s: 7` | `150-180s: 7`
  - **Análisis de la curva:** Prácticamente todos los cortes son cambios netos de escena (`40` de `41`), manteniendo una cadencia alta de `7` cortes cada 30s en toda la segunda mitad (`90-180s`) para sostener el suspenso de la operación anfibia dividida en marea matutina (`06:30`) y marea vespertina.
- **Material visual observado (`storyboard.jpg`):**
  1. **Simulaciones e infografías vectoriales 2D:**
     - Hook visual del problema de las mareas (`0-8s`): Un buque de desembarco `LST` flotando en marea alta azul (`SEPTIEMBRE 1950`) que en el siguiente plano queda inclinado y varado sobre una llanura de barro marrón al bajar el mar.
     - Vista cenital del estrecho canal navegable (`se vuelve kilómetros de barro / MAREA BAJA`) con una lancha atrapada.
     - Hoja de calendario de `SEPTIEMBRE 1950` (`15 SEP 1950`) donde todos los días del mes están tachados con una diagonal roja excepto el día `15`, rodeado por un círculo amarillo luminoso (el único día con marea suficientemente alta).
  2. **Cartografía estratégica de Corea:**
     - Invasión norcoreana del `25 JUN 1950` (flechas rojas cruzando el paralelo 38), el cerco del perímetro de `Pusan` (`230 KM`), la maniobra envolvente anfibia con flecha amarilla curva entrando por `Inchon` hacia `Seúl` (`+200 KM DETRÁS`), el colapso del ejército norcoreano atrapado entre dos frentes, y el mapa final `PARTIDA HASTA HOY`.
  3. **Fotografía de archivo:** Bombardeo naval sobre la isla de `Wolmido, 13-9-1950` (`WOLMIDO`), reunión de alto mando `Collins · MacArthur · Sherman` bajo la píldora roja `DUDAS` (`FOTO DE ARCHIVO · MARINA DE EE. UU., 1950`), y marines desembarcando entre humo a las `06:30 desembarco` (`CUERPO DE MARINES DE EE. UU., 15-9-1950`).
- **Movimiento y animaciones:** Descenso del nivel del agua dejando al buque `LST` inclinado en el lodo, trazado curvo de la flecha amarilla hacia Inchon, tachado rápido de los días del calendario hasta resaltar el `15`, y caja azul en `[dudas.]`.
- **Composición 9:16 y color/grading:** Contraste cromático constante entre el terracota rojizo (Corea del Norte / barro de Inchon) y el azul verdoso/marino (Corea del Sur / fuerzas de la ONU).

---

### #20 | `RT6my9-VxFI` — Puente aéreo de Berlín: vencieron el bloqueo sin disparar
- **Ritmo cuantitativo:**
  - **Cortes fuertes (`scene > 0.3`):** `32` cortes | **ASL (0.3):** `5.45s` | **Cortes/10s:** `1.78`
  - **Cortes totales (`scene > 0.15`):** `32` cortes | **ASL (0.15):** `5.45s` | **Cortes/10s:** `1.78`
  - **Curva de ritmo cada 30s (`>0.3`):** `0-30s: 6` | `30-60s: 6` | `60-90s: 5` | `90-120s: 5` | `120-150s: 5` | `150-180s: 5`
  - **Curva de ritmo cada 30s (`>0.15`):** `0-30s: 6` | `30-60s: 6` | `60-90s: 5` | `90-120s: 5` | `120-150s: 5` | `150-180s: 5`
  - **Análisis de la curva:** Es la curva más simétrica de todo el canal: exactamente `6, 6, 5, 5, 5, 5` cortes cada 30 segundos, con `0` diferencia entre `scene > 0.3` y `scene > 0.15`. Esto demuestra una edición puramente programática donde cada escena dura entre `5.0s` y `5.8s` y cambia mediante corte seco limpio.
- **Material visual observado (`storyboard.jpg`):**
  1. **Infografías y escenas vectoriales 2D:**
     - Hook (`0-8s`): Carretera de asfalto vista desde arriba que se cierra con una barrera roja y blanca y el sello rojo `BLOQUEO` bajo `JUNIO 1948`.
     - Vista cenital de un avión plateado despegando entre nubes (`UNA TERCERA`).
     - Estanterías de madera casi vacías sobre fondo negro (`COMIDA: SEMANAS`).
     - Pantalla dividida horizontal explicando el dilema aliado: arriba un convoy de camiones militares verdes frenado ante la barrera (`CONVOY = GUERRA`) y abajo las siluetas en ruinas de Berlín (`IRSE = ENTREGARLA`).
     - Avión en el cielo encuadrado por una mira telescópica roja (`= GUERRA`, explicando por qué Stalin tampoco podía derribarlos sin iniciar la guerra).
     - Infografía cuantitativa de suministros (`5.000 T / DÍA`): sacos dorados apilados a la izquierda (`COMIDA 1.400`) y una montaña gris de carbón cayendo a la derecha (`CARBÓN 3.000`).
     - Corte esquemático del corredor aéreo: cinco aviones (`U.S. AIR FORCE`) volando en escalones de altitud separados entre las nubes (`Si no aterriza a la primera, vuelve con su carga`).
     - Pequeños paracaídas blancos con caramelos de colores cayendo sobre fondo oscuro.
  2. **Archivo histórico:** Billete original del `DEUTSCHE MARK` (`21 JUN 1948 / FOTO DE ARCHIVO · MUSEO NACIONAL DE HISTORIA DE EE. UU.`), avión lanzando dulces (`CARAMELOS PARA LOS CHICOS / FUERZA AÉREA DE EE. UU., 1949`), fila de aviones C-54 descargando en pista (`2.334.374 toneladas`), y la icónica foto de los niños berlineses sobre los escombros saludando al avión que aterriza en `Tempelhof, 1948` (`FUERZA AÉREA DE EE. UU., 1948`).
- **Movimiento y animaciones:** Bajada de la barrera del bloqueo, apilamiento físico de sacos y caída de partículas de carbón, tráfico escalonado de aviones de izquierda a derecha, descenso de paracaídas con dulces, y cuatro cajas de selección azul en subtítulos (`[tercera.]`, `[semanas.]`, `[derribarlo.]`, `[toneladas.]`).
- **Composición 9:16 y color/grading:** Contraste entre el gris asfalto/carbón del bloqueo y el azul celeste luminoso (`#4A89DC`) del corredor aéreo.

---

## 3. Patrones Transversales de Edición y Montaje

### 3.1. Arquitectura del Lienzo `1080x1920` y Zonas Seguras (Safe Zones)
A lo largo de los 20 vídeos, `@cdmauro2010` aplica una **retícula geométrica invariable** que resuelve el mayor problema de diseño en YouTube Shorts (la superposición de la interfaz de usuario de la app móvil sobre el contenido):

```
+---------------------------------------+ y = 0 px
|      MARGEN SUPERIOR DE SEGURIDAD     | (0 - 260 px: Viñeta oscura / cielo)
+---------------------------------------+ y = 260 px
|     [ ZONA DE SUBTÍTULOS DINÁMICOS ]  | (260 - 440 px: Texto 2 líneas + Caja Azul)
|     "¿Cómo se rompe un [código]..."   |
+---------------------------------------+ y = 440 px
|    [ ZONA DE TITULARES / FECHAS ]     | (440 - 650 px: Cintas fecha / H1 Dorado)
|         "UNA CLAVE NUEVA"             |
+---------------------------------------+ y = 650 px
|                                       |
|                                       |
|          NÚCLEO VISUAL ACTIVO         | (650 - 1440 px: Mapas, Fotos 4:3/1:1,
|      (Centro geométrico y óptico)     |  Documentos crema, Diagramas 2D)
|                                       |
|                                       |
|  [FOTO DE ARCHIVO · CC BY-SA 4.0]     | <-- y = 1420 - 1480 px (X = 40 px izq.)
+---------------------------------------+ y = 1520 px
|                                       |
|    20% INFERIOR RESERVADO (UI SHORTS) | (1520 - 1920 px: Libre de texto crítico;
|    (@handle, título, audio, botones   |  solo fondo oscuro o blur de relleno)
|     de Like/Comentarios a la derecha) |
+---------------------------------------+ y = 1920 px
```

- **Por qué los subtítulos van arriba (`y ≈ 300–400 px`) y no abajo:** En un Short educativo con mapas, documentos e infografías, colocar los subtítulos en el tercio inferior taparía las etiquetas del mapa o chocaba con el título del vídeo de la interfaz de YouTube. Al fijarlos en el **tercio superior (`y ≈ 320 px`)** sobre un degradado oscuro suave (`linear-gradient(180deg, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0) 100%)`), la vista del espectador lee la frase arriba e inmediatamente baja medio centímetro al centro (`y = 650–1400 px`) donde ocurre la demostración visual.
- **El secreto de la micro-píldora de atribución (`y ≈ 1440 px`):** Se sitúa siempre pegada al margen izquierdo (`x ≈ 36–48 px`), exactamente **por encima del nombre del canal (`@cdmauro2010`) de la UI de YouTube** y lejos de la columna derecha de iconos (Like, Dislike, Comentarios, Compartir).

### 3.2. Paleta Cromática Exacta del Sistema Visual

| Rol Visual | Color / Muestra | Código HEX Aprox. | Uso Específico en los 20 Vídeos |
| :--- | :--- | :---: | :--- |
| **Fondo Base Abisal** | Negro Carbón / Pizarra | `#0D0D0D` – `#141619` | Fondo de diagramas, documentos, balanzas y viñetas superiores/inferiores. |
| **Océano Cartográfico** | Azul Marino Táctico | `#0B2545` – `#13315C` | Fondo de mapas SGM y Guerra Fría con retícula ortogonal al `8%` de opacidad. |
| **Tierra Cartográfica (Estándar)** | Verde Oliva / Musgo | `#6B7F46` – `#7E8F56` | Territorio general en mapas de Europa (`#01`, `#06`) y Pacífico/Asia (`#02`, `#03`, `#17`, `#19`). |
| **Tierra Cartográfica (PGM)** | Pergamino / Arena | `#C9BC9C` – `#D6C9AC` | Variante histórica exclusiva de Primera Guerra Mundial (`#09`). |
| **Papel de Reconstrucción** | Crema Archivo | `#F4EFE6` – `#EFE8D8` | Cartas, telegramas, hojas de claves Enigma y calendarios (`#01`, `#02`, `#18`, `#19`). |
| **Acento Primario (Titulares)** | Dorado / Ámbar | `#F0B429` – `#F5C451` | Titulares clave (`27 AÑOS`, `EL PUNTO DÉBIL`, `8:15`, `AUTORIDAD`, preguntas finales). |
| **Acento de Alerta / Conflicto** | Rojo Coral / Carmín | `#E05A47` – `#D63629` | Sellos (`ULTRA`, `HALT!`, `BLOQUEO`), bajas, cronómetros (`10:22`), flechas enemigas, tachados. |
| **Acento Aliado / Selección** | Azul Eléctrico / Cielo | `#3B82F6` – `#60A5FA` | **Caja de selección con nodos en subtítulos**, flechas aliadas, platillo `SÍ`. |
| **Subtítulo Palabra Activa** | Blanco Puro | `#FFFFFF` | Palabra pronunciada en ese instante (en **Bold**). |
| **Subtítulo Palabra Pasada** | Gris Neutro | `#9AA0A6` | Palabras ya pronunciadas de la línea activa (`opacity: 0.55`). |

### 3.3. Deducción Técnica del Software / Pipeline de Producción
Todas las evidencias visuales recopiladas en los 20 `storyboard.jpg` y `hook_3s.jpg` apuntan de forma concluyente a un **pipeline de vídeo programático basado en código (Remotion / Motion Canvas / HTML5 + CSS + SVG renderizado a `60 fps` vía Headless Chromium + FFmpeg)**, o en su defecto un motor de plantillas automatizadas por expresiones/JSON en After Effects. Las **6 pruebas técnicas irrefutables** son:

1. **El componente de selección tipo "Vector Bounding Box" en los subtítulos:** Cuando el narrador enfatiza un término clave (`[medianoche:]`, `[Potsdam,]`, `[Rosenthal,]`, `[Gregor.]`, `[tercera.]`), aparece alrededor de esa palabra un **rectángulo azul (`#3B82F6`) con fondo azul translúcido y dos pequeños nodos circulares blancos con borde azul en las esquinas superior-izquierda e inferior-derecha**. Este adorno se ajusta automáticamente al `width` y `height` exactos del `<span>` de la palabra, incluyendo su signo de puntuación adjunto (`minutos?`, `acorazados;`, `iniciativa:`), comportamiento nativo de un componente React/HTML envolviendo un nodo de texto (`<HighlightWord>`) en **Remotion**.
2. **El efecto de desenfoque progresivo (`CSS filter: blur()`) en subtítulos:** En los `hook_3s.jpg` (`#18` frame 1) se observa que las palabras futuras de la frase están presentes en el DOM pero con `filter: blur(8px); opacity: 0.25`, pasando a `filter: blur(0px); font-weight: 700; color: #FFF` en el timestamp exacto del *word-level alignment* (generado con WhisperX / Forced Alignment) y luego a `font-weight: 400; color: #9AA0A6`.
3. **Píldoras de atribución generadas desde metadatos estructurados:** Todas las atribuciones siguen el mismo patrón de concatenación con punto medio (`·`): `TIPO DE RECURSO · AUTOR/ORIGEN, FECHA · LICENCIA` (ej. `FOTO DE ARCHIVO · ARCHIVO DE EE. UU. · DOMINIO PÚBLICO` o `VIDEO · UNA ENIGMA REAL · Z22 · CC BY-SA 4.0`), renderizadas en una etiqueta con `border-radius: 4px`, `background: rgba(0,0,0,0.68)`, `padding: 4px 10px` y fuente sans-serif condensada en mayúsculas.
4. **Reconstrucciones documentales HTML/CSS con nota legal estandarizada:** Los documentos históricos (`#01`, `#02`, `#18`, `#19`) no son escaneos de baja calidad encontrados en Google, sino contenedores limpiamente maquetados en código (tablas alineadas para los rotores de Enigma, bloques `<hr>` grises simulando párrafos en la carta a Churchill, grillas CSS para el calendario de septiembre de 1950) con el pie fijo `RECONSTRUCCIÓN · TEXTO DE EJEMPLO`.
5. **Consistencia absoluta de exportación y sonorización:** Los 20 vídeos tienen exactamente `1080x1920 @ 60fps` y una sonoridad integrada clavada en **`-21.0 LUFS` (`±0.1 LU`)** con un rango dinámico (`LRA`) de `2.3 a 3.9 LU` y media de `-24.0 dB`. Esa precisión de `0.0 a 0.1 dB` entre 20 vídeos distintos solo ocurre cuando el render final pasa por un script automatizado de post-procesamiento en **FFmpeg** (ej. filtro `loudnorm=I=-21:TP=-1.5:LRA=3`).
6. **Bucle visual perfecto (Seamless Loop) entre el cierre y el hook:** En casi todos los vídeos (`#01` teclas de Enigma, `#02` fuego de Pearl Harbor, `#10` cuadro de Tiepolo, `#11` habitación de Napoleón, `#15` cuaderno con vela), el último plano (`172–180s`) reutiliza el mismo escenario o clip de fondo que el segundo `0.0s`, haciendo que la reproducción en bucle de YouTube Shorts sea visualmente continua.

---

## 4. Entregable Práctico: "Receta de Edición" Paso a Paso y Conclusiones Accionables

### 4.1. Receta de Edición Replicable (Pipeline `@cdmauro2010`)

#### Paso 1: Locución, Timestamps por Palabra y Normalización de Audio
1. Grabar o generar la locución de `~175 segundos` con pausas dramáticas intencionales de `0.55s – 0.90s` antes de cada giro narrativo (promedio del canal: `72` pausas `>= 0.20s` por vídeo) y un silencio de cola final de `1.1s – 2.5s` tras la pregunta de cierre.
2. Extraer el JSON de alineación palabra por palabra (*word-level timestamps*) usando **WhisperX** o ** CrisperWhisper**.
3. Marcar en el JSON de guion `2 a 4 palabras clave` por minuto con el atributo `highlight: "box"` para activar la caja de selección azul.
4. Procesar el máster de audio (voz + cama ambiental sutil) con FFmpeg a **`-21.0 LUFS`** y `60 fps`:
   ```bash
   ffmpeg -i input.mp4 -af "loudnorm=I=-21.0:TP=-1.5:LRA=3.0" -r 60 -c:v libx264 -crf 18 output_60fps.mp4
   ```

#### Paso 2: Configuración del Lienzo Maestro `1080x1920` (`9:16` @ `60 fps`)
1. **Capa 1 (Fondo):** Sólido oscuro `#0E1013` (para escenas de documentos/diagramas) o contenedor de imagen/vídeo de archivo centrado. Si la foto de archivo es horizontal (`4:3`) o cuadrada (`1:1`), encuadrarla entre `y = 420px` y `y = 1480px` y colocar detrás una copia escalada al `100%` de alto con `filter: blur(45px) brightness(0.35)`.
2. **Capa 2 (Viñeta de Legibilidad):** Degradado negro superior de `y = 0` a `y = 520px` (`rgba(0,0,0,0.8)` a `0%`) y degradado inferior de `y = 1450px` a `y = 1920px`.
3. **Capa 3 (Píldora de Atribución):** En toda imagen o clip externo, renderizar en `x = 40px, y = 1445px` una etiqueta oscura (`background: rgba(15,15,15,0.75)`, `border-radius: 4px`, texto blanco `#E5E7EB` a `16px` Bold):
   `FOTO DE ARCHIVO · [FUENTE], [AÑO] · [DOMINIO PÚBLICO / CC BY-SA 4.0]`.

#### Paso 3: Construcción de los 4 Módulos Visuales (Cambio cada `4.5s – 6.0s`)
Alternar en la línea de tiempo (objetivo: **`30 a 42` cortes de escena fuertes** en 180 segundos, es decir, **un cambio visual relevante cada `4.3 a 6.0 segundos`**, complementado con micro-animaciones internas cada `2.0 segundos`):
- **Módulo A — Foto/Vídeo de Archivo con Cinta de Fecha:** Aplicar un *zoom-in* suave del `100%` al `108%` a lo largo de 5 segundos. Si introduce un lugar o fecha, animar una cinta color crema (`#F4EFE6`) con borde izquierdo rojo (`4px solid #D63629`) y texto monoespaciado tipo máquina de escribir (`7 DE DICIEMBRE DE 1941`).
- **Módulo B — Mapa Vectorial Táctico:** Usar GeoJSON/SVG simplificado de la región. Color de mar `#0B2545` con cuadrícula de `60x60px` a `rgba(255,255,255,0.06)`, tierra `#6B7F46`. Animar flechas curvas (`stroke-dasharray`) y etiquetas de ciudades en píldoras negras (`background: #18181B`, punto de color + texto blanco en mayúsculas).
- **Módulo C — Documento Reconstruido:** Crear una tarjeta de `860px` de ancho, fondo `#F4EFE6`, rotación `-1.5deg`, sombra proyectada profunda y fuente `Courier Prime`. Añadir al final un sello rojo (`#D63629`, borde doble, rotación `-8deg`) que entra con escala de `1.8` a `1.0` en `12 frames` (`0.2s`), y fijar abajo a la izquierda en gris `#71717A` (`14px`): `RECONSTRUCCIÓN · TEXTO DE EJEMPLO`.
- **Módulo D — Diagrama de Decisión o Contraste:** Cuando el guion plantee un dilema o desmienta un mito, usar fondo negro `#0D0D0D` y construir:
  - Una **balanza dorada** (`SÍ` en azul `#60A5FA` vs. `NO` en rojo `#E05A47`) donde caen bloques con los argumentos.
  - Una **lista vertical de tachado** (palabras en blanco `56px` Bold atravesadas secuencialmente por una barra roja `#E05A47`).
  - Una **matriz 2x2 de tarjetas** que se iluminan en rojo a medida que avanza la explicación.

#### Paso 4: Subtítulos Superiores y Bucle de Cierre
1. Renderizar los subtítulos en `y = 320px` (máximo 2 líneas, fuente geométrica como `Inter` / `Plus Jakarta Sans` `42px`). Colorear las palabras pasadas en `#9AA0A6`, la palabra actual en `#FFFFFF Bold`, las palabras futuras con `blur(8px)`, y activar la caja azul con nodos en las palabras marcadas.
2. En los últimos `8 segundos` (`172–180s`), volver al mismo fondo visual del segundo `0` y mostrar en el centro en dorado (`#F0B429`, `54px` ExtraBold) la pregunta dilemática final + la píldora `CONTÁMELO EN LOS COMENTARIOS`.

---

### 4.2. Cinco Conclusiones Accionables para Replicar o Superar al Canal

1. **Sustituir la "hiper-edición vacía" por la "progresión informativa dentro del plano":** `@cdmauro2010` demuestra que para retener en Shorts de 3 minutos **no hace falta cortar cada 1.2 segundos con efectos estridentes**. Su ASL de cortes duros es de **`5.74s`** (`33` escenas por vídeo), pero su ASL de eventos visuales (`>0.15`) baja a **`4.60s`** (y en vídeos bélicos como `#01`, `#02`, `#07` y `#09` a **`1.46s – 2.86s`**) porque **cada plano tiene progresión interna**: aparece un mapa → se traza una flecha → surge una cifra → se tacha una fecha. **Regla práctica:** Nunca dejes una imagen estática más de `2.5 segundos` sin que aparezca una etiqueta, un vector o un cambio de estado dentro de la escena.
2. **Adoptar la "Honestidad Documental Explícita" como diferenciador de autoridad:** En un ecosistema saturado de vídeos históricos con imágenes de IA deformes y anacrónicas, etiquetar cada foto real con su licencia (`DOMINIO PÚBLICO / CC BY-SA`) y cada recreación tipográfica con `RECONSTRUCCIÓN · TEXTO DE EJEMPLO` dispara la confianza percibida del espectador y blinda al canal frente a reclamaciones de derechos o desinformación.
3. **Separar el ritmo según el subgénero histórico:** Los datos de los 20 vídeos revelan dos velocidades de montaje deliberadas:
   - **Historia Militar / SGM / PGM (`#01` a `#07`, `#09`, `#18` a `#20`):** Exige entre **`36 y 51` cortes fuertes** (`ASL 3.4s – 4.8s`), uso intensivo de mapas tácticos, cronómetros y metraje de archivo.
   - **Historia Antigua, Filosofía y Mitos (`#10` a `#16`):** Funciona mejor con **`16 a 29` cortes fuertes** (`ASL 5.9s – 10.5s`), apoyándose en escenas ilustradas 2D continuas, metáforas visuales (coronas que se oxidan, cadenas que se rompen, cuadernos a la luz de una vela) y bustos/monedas reales.
4. **Blindar el 20% inferior (`y > 1520px`) y subir el subtítulo a `y = 320px`:** Es el acierto ergonómico más importante del canal. Al mantener los subtítulos arriba y la acción en el centro, ningún elemento gráfico compite jamás con la botonera ni los textos superpuestos de la interfaz de YouTube Shorts.
5. **Automatizar en código (Remotion) los componentes repetitivos:** Las cintas de fechas mecanografiadas, los relojes analógicos, las cajas de selección azul en subtítulos, los sellos rojos y las píldoras de atribución representan el `70%` de la identidad visual del canal y son 100% parametrizables mediante componentes reutilizables alimentados por un archivo JSON por episodio.
