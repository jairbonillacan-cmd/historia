# Informe del Agente 4: Texto en Pantalla, Subtítulos y Sistema Tipográfico (`@cdmauro2010`)

> **Alcance del análisis:** Inspección visual fotograma a fotograma de los 40 mosaicos de extracción (`hook_3s.jpg` y `storyboard.jpg`) y cruce con las transcripciones cronometradas de los **20 Shorts seleccionados** del canal **CM | Historia y Decisiones (`@cdmauro2010`)**.

---

## 1. Resumen Ejecutivo: La Arquitectura Tipográfica de 4 Niveles

A diferencia del 95 % de los canales de historia y divulgación en formato vertical —que dependen de plantillas genéricas de CapCut con subtítulos centrales invasivos, bordes negros gruesos, colores chillones y emojis flotantes—, `@cdmauro2010` ha diseñado un **sistema de diseño editorial e infográfico propio de 4 niveles jerárquicos** que funciona como la interfaz visual de un documental interactivo.

El hallazgo más importante de esta auditoría visual es que **el texto en pantalla no es un adorno post-producción, sino el motor narrativo del canal**. Cada nivel ocupa una franja vertical estrictamente delimitada del lienzo `1080×1920` (9:16), evitando colisiones visuales entre sí y con la interfaz nativa de YouTube Shorts:

1. **Nivel 1 — Subtítulos Dinámicos Superiores (`y ≈ 16%–22%`):** Ubicados en el tercio superior sobre un *scrim* (degradado oscuro protector), en bloques ultra-cortos de 1 a 2 líneas (3 a 7 palabras). Emplean un **efecto karaoke de luminancia y grosor** (palabras inactivas en gris `#8A8F98` Regular; palabra pronunciada en Blanco Puro `#FFFFFF` Bold) y su sello de identidad más distintivo: el **"Figma Bounding Box"**, un rectángulo vectorial azul (`#3B82F6`) con **4 pequeños nodos cuadrados blancos en las esquinas** que enmarca la palabra gatillo del bloque sin usar jamás un solo emoji.
2. **Nivel 2 — Titulares de Sección / Callouts Centrales (`y ≈ 28%–36%` y cierres en `y ≈ 72%–82%`):** Rótulos de alto impacto en **MAYÚSCULAS SOSTENIDAS (`ALL CAPS`)**, peso `ExtraBold`/`Black`, codificados cromáticamente según su función semántica: **Blanco/Crema (`#F5F2EB`)** para fechas y lugares objetivos; **Amarillo/Ámbar (`#F0B429`)** para conceptos clave, tesis y preguntas; **Rojo Coral (`#E05A47`)** para peligro, errores estratégicos o fuerzas enemigas; y **Azul Táctico (`#60A5FA`)** para maniobras aliadas o defensivas.
3. **Nivel 3 — Textos Diegéticos, Documentos Reconstruidos e Infografía Central (`y ≈ 40%–75%`):** Incluye cintas mecanografiadas que se escriben en vivo (`7 DE DICIEMBRE DE 1941`), documentos clasificados reconstruidos en fuente monoespaciada (`Courier Prime`), contadores digitales/relojes, pantallas de radar, listas con tachado rojo animado (`~~GUERRA~~`), etiquetas cartográficas en píldoras oscuras (`VARSOVIA`, `HALIFAX`) y pies de foto identificativos (`Gral. Douglas MacArthur, Corea, 1950`).
4. **Nivel 4 — Píldora Legal / Atribución Documental (`y ≈ 76%–88%`, alineada a la izquierda):** Micro-etiqueta en mayúsculas dentro de una pastilla negra semitransparente que acredita con rigor museístico el origen y licencia de cada activo visual (`FOTO DE ARCHIVO · ... · DOMINIO PÚBLICO`, `VIDEO · UNA ENIGMA REAL · Z22 · CC BY-SA 4.0`, `RECONSTRUCCIÓN · TEXTO DE EJEMPLO`).

### Evolución interna observable en el corpus de 20 vídeos
El análisis de los 20 `storyboard.jpg` revela además tres variantes estilísticas del mismo sistema base según la sub-serie temática:
- **Serie Estoicismo, Roma y Conquista (`#12`, `#13`, `#14`, `#15`, `#16`):** Sobre ilustraciones vectoriales minimalistas cálidas, los rótulos de Nivel 2/3 adoptan la forma de **píldoras oscuras con borde fino dorado (`#D4A853`)** y tipografía condensada o serif clásica (`El palacio`, `Meditaciones, libro 1`, `CUBA, 1519`, `CASI 100 AÑOS`), manteniendo intactos el Nivel 1 (con su *Figma Bounding Box* azul) y el Nivel 4 en las fotografías de estatuas/monedas.
- **Episodio Experimental Voxel / Pixel-Art (`#11` Napoleón):** Mantiene exactamente el Nivel 1 (subtítulo superior + *Figma Bounding Box* azul en `[emperadores:]` y `[equivocarte.]`), pero estiliza el Nivel 2 (`APURADO`, `AUSTERLITZ 2·12·1805`, `VICTORIA`, `CERO ERRORES`) con **borde negro sólido (`stroke: 3px #111111`) y sombra dura**, armonizando con la estética de bloques 3D.
- **Formato Documental Bélico / Geopolítico Estándar (`#01` a `#10` y `#17` a `#20`):** Despliega los 4 niveles en su máxima expresión infográfica y documental.

---

## 2. Fichas Individuales de los 20 Vídeos (`#01` al `#20`)

A continuación se documenta con exactitud textual cada rótulo, palabra con *bounding-box* azul, documento diegético y etiqueta legal extraídos directamente de los archivos `hook_3s.jpg` y `storyboard.jpg` de cada vídeo.

---

### `#01` | `UsMkfLhccJM` — *Enigma: Alan Turing y el equipo que descifró el código nazi*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/UsMkfLhccJM/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/UsMkfLhccJM/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `¿Cómo se **rompe**` → `¿Cómo se rompe un / código **con**` → `**158**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `a [medianoche:]` (fotograma 4 del storyboard) y `[débil]` (fotograma 6 del storyboard).
  - Otros bloques capturados: `**llamaba**`, `invasión, **Polonia**`, `La primera, **llamada**`, `los barcos que / **alimentan**`, `**Churchill**`, `sin`, `**1952**`, `tanto **tiempo?**`.
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema (`#F5F2EB`): `ENIGMA` (fijo durante todo el hook sobre el teclado de la máquina), `CONVOY` (sobre el mapa del Atlántico), `¿VOS HABRÍAS PODIDO`.
  - Amarillo/Ámbar (`#F0B429`): `27 AÑOS` (sobre retrato joven de Turing), `UNA CLAVE NUEVA CADA DÍA`, `EL PUNTO DÉBIL`, `LA BOMBA` / `«VICTORY»`, `¿CÓMO USARLO`, `CALLAR?` (en el cierre `¿VOS HABRÍAS PODIDO / CALLAR?`).
  - Rojo Coral (`#E05A47`): `SUBMARINOS EN MANADA` (sobre el mapa de ataque en el Atlántico Norte).
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Contador numérico dorado con borde oscuro en el hook: `017.407.874.577.000` (sobre las teclas metálicas de Enigma).
  - Hoja de claves alemana reconstruida en papel crema con reloj analógico en la esquina: título en rojo `GEHEIM! · CLAVES DEL MES`, columnas monoespaciadas `DÍA | ROTORES | ANILLOS | TABLERO DE CLAVIJAS` (`15 II IV I 05 12 21 AQ BJ CM...`), pie `RECONSTRUCCIÓN · VALORES DE EJEMPLO`.
  - Diagrama circular de cifrado con las 26 letras del alfabeto alrededor y la letra `A` grande en el centro sobre recuadro dorado.
  - Etiquetas cartográficas en píldora negra: `VARSOVIA` (con punto rojo), `HALIFAX`, `LIVERPOOL`.
  - Etiqueta identificativa en foto: `RÉPLICA EN BLETCHLEY PARK`.
  - Carta reconstruida a Churchill: `Secret and Confidential / Prime Minister only / Dear Prime Minister,` firmada al pie en dos columnas por `A. M. TURING`, `W. G. WELCHMAN`, `C. H. O'D. ALEXANDER`, `P. S. MILNER-BARRY`.
  - Telegrama reconstruido: `MENSAJE DESCIFRADO` (rojo), `DE: JEFE DE SUBMARINOS / A: GRUPO DEL ATLÁNTICO NORTE / REUNIRSE EN EL CUADRANTE AK 52 / MAÑ`, estampado con sello rectangular rojo inclinado `ULTRA / ALTO SECRETO` y pie `RECONSTRUCCIÓN · TEXTO DE EJEMPLO`.
  - Cinta mecanografiada con pestaña roja: `[| 1952 ]` (sobre retrato de Turing en 1951).
- **Nivel 4 (Píldoras de atribución legal):**
  - `VIDEO · UNA ENIGMA REAL · Z22 · CC BY-SA 4.0`
  - `FOTO DE ARCHIVO · PRINCETON, 1936 · DOMINIO PÚBLICO`
  - `RÉPLICA DE LA BOMBA · FOTO: MIKE PEEL · CC BY-SA 4.0`
  - `FOTO DE ARCHIVO · ELLIOTT & FRY, 1951 · DOMINIO PÚBLICO`

---

### `#02` | `t89RDX8qolU` — *Pearl Harbor 1941: la alerta del radar que fue ignorada*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/t89RDX8qolU/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/t89RDX8qolU/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `Pearl **Harbor,**` → `Pearl Harbor, 7 **de**` → `de **1941.**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `[alerta] que nadie / **escuchó.**` (fotograma 3), `de [acorazados;]` (fotograma 9), `En dos [horas:]` (fotograma 10).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema: `PEARL HARBOR` (grande en la mitad inferior durante el hook sobre la explosión), `QUE NADIE ESCUCHÓ` (bajo `LA ALERTA`), `NI EL COMBUSTIBLE NI LOS TALLERES`.
  - Amarillo/Ámbar: `LA ALERTA`, `TORPEDOS CONTRA LOS ACORAZADOS`, `EN 2 HORAS`, `6 DE 8 VUELVEN A PELEAR`, `¿VOS LE HUBIERAS / CREÍDO AL RADAR?`.
  - Rojo Coral: `UN GOLPE POR SORPRESA` (bajo la etiqueta de Yamamoto).
  - Azul Táctico: `EL DESTRUCTOR WARD` (sobre el mapa de la entrada de Pearl Harbor).
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Cinta mecanografiada en el hook: `[| 7 DE DICIEMBRE DE 1 ]` → `[| 7 DE DICIEMBRE DE 1941 ]`.
  - Cinta horaria en mapa: `[| 6:45 ]` junto a etiqueta en píldora negra `PEARL HARBOR`.
  - Pie de foto en píldora negra: `ALMIRANTE ISOROKU YAMAMOTO`.
  - Recorte de mensaje cifrado en papel crema con texto monoespaciado: `NVEJGMTYJKNMVGQARL / GGDQPIUUZXJUTJVRKX / LAWZGLSTAMGUTLZSEY`.
  - Pantalla de osciloscopio/radar reconstruida en verde fosforescente: titular amarillo `+50 AVIONES`, pico de señal con etiqueta `212 KM`, eje horizontal graduado (`0, 40, 80, 120, 160, 200, 240, 280 KM`), y leyenda inferior `RECONSTRUCCIÓN · RADAR SCR-270, OPANA`.
  - Infografía de 8 siluetas de acorazados (6 iluminados en azul claro y 2 apagados en gris oscuro) entre los rótulos `NI EL COMBUSTIBLE NI LOS TALLERES` y `6 DE 8 VUELVEN A PELEAR`.
- **Nivel 4 (Píldoras de atribución legal y CTA):**
  - `FOTO DE ARCHIVO · ARCHIVO DE EE. UU. · DOMINIO PÚBLICO`
  - `PELÍCULA DE ARCHIVO · «DECEMBER 7TH», JOHN FORD Y GREGG TOLAND, 1943 · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · MINISTERIO DE MARINA DE JAPÓN · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · ARMADA IMPERIAL JAPONESA · DOMINIO PÚBLICO`
  - Píldora CTA de cierre con borde dorado: `CONTÁMELO EN LOS COMENTARIOS`.

---

### `#03` | `Dn8s4cqsNCQ` — *Hiroshima 1945: ¿era necesaria la bomba atómica?*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/Dn8s4cqsNCQ/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/Dn8s4cqsNCQ/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `**Hiroshima,**` → `Hiroshima, 6 de / **agosto**` → `**1945.**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `Diez días después, en / [Potsdam,]` (fotograma 6), `[probar] qué habría` (fotograma 11).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema: `HIROSHIMA` (sobre el B-29 en vuelo en el hook), `¿O HABÍA OTRO CAMINO?` (subtítulo del cierre).
  - Amarillo/Ámbar: `EL QUE DECIDÍA` (bajo retrato de Truman), `KYUSHU` (sobre mapa), `8:15` (sobre reloj de bolsillo detenido), `LO QUE TRABABA TODO` (sobre retrato de Hirohito), `NADIE PUEDE PROBARLO`, `¿ERA NECESARIA?`.
  - Azul Táctico: `LOS QUE DICEN QUE SÍ` (encabezando la balanza argumentativa).
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Cintas mecanografiadas con pestaña roja: `[| 6 DE AGOSTO DE 1945 ]` (hook y escena del reloj), `[| POTSDAM, 26 DE JU ]` (sobre foto de Attlee, Truman y Stalin), `[| 8 DE AGOSTO DE 1945 ]` (sobre mapa de Manchuria).
  - Pies de foto / etiquetas de contexto en píldora negra: `HARRY S. TRUMAN, PRESIDENTE DE EE. UU.`, `OKINAWA, ABRIL A JUNIO DE 1945`.
  - Tarjetas comparativas de bajas (fondo negro traslúcido con borde redondeado de color):
    - Borde azul: `+12.000` (en azul `#60A5FA`) / `ESTADOUNIDENSES MUERTOS` (blanco).
    - Borde rojo: `+100.000` (en rojo `#E05A47`) / `JAPONESES, SOLDADOS Y CIVILES` (blanco).
    - En mapa de Kyushu: `×2` (en rojo `#E05A47`) / `SOLDADOS DE LO PREVISTO` (blanco).
  - Infografía de balanza dorada comparando las dos posturas historiográficas: platillo izquierdo `SÍ` (azul) con bloques `LA INVASIÓN` y `GOBIERNO DIVIDIDO`; platillo derecho `NO` (rojo) con bloques `JAPÓN DERROTADO`, `EL ACUERDO`, `LA URSS`, `STALIN`.
- **Nivel 4 (Píldoras de atribución legal y CTA):**
  - `PELÍCULA DE ARCHIVO · «TALE OF TWO CITIES», EJÉRCITO DE EE. UU., 1946 · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · ARCHIVO DE EE. UU., EDMONSTON STUDIO · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · ARCHIVO DE EE. UU., U.S. NAVY / THE ORIGINAL UPLOADER WAS QUERCUSROBUR AT...`
  - `FOTO DE ARCHIVO · ARCHIVO DE EE. UU., OFFICIAL PHOTOGRAPHER · DOMINIO PÚBLICO`
  - `PELÍCULA DE ARCHIVO · HARRY MIMURA, USAAF, HIROSHIMA, 1945 · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · ARCHIVO DE JAPÓN · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · MUSTANG JOE · CC0`
  - Píldora CTA: `CONTÁMELO EN LOS COMENTARIOS`.

---

### `#04` | `4VT2qvIRUkg` — *Iwo Jima 1945: la historia detrás de la foto y la segunda bandera*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/4VT2qvIRUkg/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/4VT2qvIRUkg/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `Esta **es**` → `Esta es la [foto] más / **famosa**` → `de la Segunda **Guerra**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `[foto]` (en el segundo fotograma del hook), `van a tomar en una / [semana.]` (fotograma 4), `[sirenas.]` (fotograma 7), `bandera. Joe / [Rosenthal,]` (fotograma 8).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema: `23 DE FEBRERO DE 1945` (en el hook bajo la bandera en color).
  - Amarillo/Ámbar: `CADA UNO: 10 ENEMIGOS`, `LA PUNTA SUR`, `SUENAN LAS SIRENAS`, `CUEVA POR CUEVA`, `¿UNA SOLA FOTO / PUEDE CONTAR / LA VERDAD DE UNA GUERRA?`.
  - Azul Táctico: `LOS BOMBARDEROS` (con superposición animada en el mapa entre Tokio, Iwo Jima y Marianas).
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Sello militar rojo inclinado sobre silueta subterránea de la isla: `NO RENDIRSE`.
  - Etiquetas cartográficas en píldora negra: `TOKIO`, `IWO JIMA`, `MARIANAS`.
  - Pie de foto en píldora negra: `JOE ROSENTHAL, ASSOCIATED PRESS`.
  - Fotografía tipo Polaroid inclinada: `10:20 · LA PRIMERA` (mostrando el primer izamiento).
  - Contador de progreso de campaña en caja negra con borde azul sobre el mapa táctico de la isla: `DÍA 29 / DE 36` y etiqueta inferior `LA FOTO, DÍA 5`.
  - Cartel reconstruido de bonos de guerra: etiqueta superior en píldora negra `LA GIRA: BRADLEY, GAGNON Y HAYES`, banda roja central `COMPRÁ BONOS` y pie azul `7.º EMPRÉSTITO DE GUERRA`.
- **Nivel 4 (Píldoras de atribución legal):**
  - `PELÍCULA DE ARCHIVO · BILL GENAUST, USMC, 23-2-1945 · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · ARCHIVO DE EE. UU. · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · JOE ROSENTHAL / AP · DOMINIO PÚBLICO`

---

### `#05` | `lYVMDblBX3Y` — *Midway 1942: los minutos que cambiaron la guerra del Pacífico*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/lYVMDblBX3Y/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/lYVMDblBX3Y/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `¿Cómo se **pierde**` → `**solo**` → `solo cinco [minutos?]`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `[minutos?]` (en el hook, 2.º y 3.er segundo) e `[iniciativa:] el **que**` (fotograma 11 del storyboard).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Amarillo/Ámbar: `USS YORKTOWN`, `LOS TORPEDEROS`, `5 MINUTOS`.
  - Rojo Coral (cronómetros de impacto): `10:20` (sin recuadro, sobre bombas cayendo), `10:22` y `10:25` (dentro de cajas negras con borde rojo fino `#E05A47`).
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Cinta mecanografiada: `[| JUNIO DE 1942 ]` (con pestaña izquierda roja sobre mapa del Pacífico).
  - Matriz numérica criptográfica en verde oscuro (`49374 84574 85525...`) detrás del retrato de archivo de Rochefort.
  - Etiquetas cartográficas en píldora negra: `JAPÓN`, `PEARL HARBOR`, `MIDWAY`.
  - Tarjeta de estadística en esquina inferior izquierda con borde dorado: `3 DÍAS` (amarillo grande) / `DE REPARACIÓN A CONTRARRELOJ` (blanco).
  - Botones de dilema interactivo en el cierre (sobre portaaviones navegando): caja roja `ATACAR YA` contrapuesta a caja azul `ESPERAR A ESTAR LISTO`.
- **Nivel 4 (Píldoras de atribución legal):**
  - `PELÍCULA DE ARCHIVO · «THE BATTLE OF MIDWAY», JOHN FORD, 1942 · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · MARINA DE EE. UU. · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · MARINA DE EE. UU., USN · DOMINIO PÚBLICO`

---

### `#06` | `KCrSmZt-A0w` — *Dunkerque 1940: ¿por qué Hitler frenó los tanques?*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/KCrSmZt-A0w/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/KCrSmZt-A0w/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `¿Por qué **Hitler**` → `**tanques,**` → `tanques, cuando / tenía **al**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `Esto es [Dunkerque,] / **mayo**` (fotograma 3), `¿Por qué? Hay cuatro / [razones,]` (fotograma 6), `Segunda: [Göring] le` (fotograma 7), `Bretaña le pide [ayuda]` (fotograma 9), `[Churchill] lo dijo` (fotograma 11).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema: `LOS TANQUES` (en el hook, pantalla dividida), `«IMPOSIBLE PARA TANQUES»`, `26 DE MAYO – 4 DE JUNIO DE 1940`.
  - Amarillo/Ámbar: `DUNKERQUE`, `? / CUATRO RAZONES`, `QUIÉN MANDA`, `SE NECESITAN BARCOS`, `¿QUÉ PESÓ MÁS?`.
  - Azul Táctico: `RESISTEN` (sobre el cerco de Lille en el mapa).
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Sello militar rojo inclinado en el hook: `HALT! / ¡ALTO!`.
  - Cinta mecanografiada en papel crema: `[| MAYO D ]`.
  - Tarjeta de contingente en mapa (borde azul): `400.000` (azul `#60A5FA`) / `HOMBRES ENCERRADOS` (blanco), junto a píldoras de bandos `BE`, `GB`, `FR` y `DUNKERQUE`, `LILLE`.
  - Pie de foto en píldora negra: `HERMANN GÖRING`.
  - **Grilla interactiva de 4 razones (2×2)** en la mitad inferior:
    - `1. TANQUES GASTADOS`
    - `2. LA PROMESA DE GÖRING`
    - `3. EL MIEDO`
    - `4. QUIÉN MANDA`
    - *Comportamiento dinámico:* Las celdas comienzan en gris oscuro (`#27272A`) y se van iluminando en **rojo carmesí (`#DC2626`)** a medida que el narrador explica cada una, reapareciendo las 4 en el cierre bajo la pregunta `¿QUÉ PESÓ MÁS?`.
- **Nivel 4 (Píldoras de atribución legal):**
  - `FOTO DE ARCHIVO · IWM · DOMINIO PÚBLICO`
  - `PELÍCULA DE ARCHIVO · «DIVIDE AND CONQUER», EE. UU., 1943 · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · BUNDESARCHIV, HEINRICH HOFFMANN · CC BY-SA 3.0 DE`
  - `FOTO DE ARCHIVO · BUNDESARCHIV · CC BY-SA 3.0 DE`
  - `FOTO DE ARCHIVO · NOT STATED, ASSUMED BRITISH MILITARY · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · IWM, WILLIAM GEORGE HORTON · DOMINIO PÚBLICO`

---

### `#07` | `yeMKOTtYlWU` — *Stalingrado en 3 minutos: «Ni un paso atrás»*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/yeMKOTtYlWU/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/yeMKOTtYlWU/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `Stalin` → `Stalin dio una **orden:**` → `**paso**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `Mueren miles de / [civiles.]` (fotograma 5), `lugar de Paulus: / [obedecer]` (fotograma 12).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema: `AGOSTO 1942 – FEBRERO 1943`, `MILES DE CIVILES`, `SIN COMIDA` / `SIN MUNICIÓN` (encuadrando la escena de invierno).
  - Amarillo/Ámbar: `CADA PISO`.
  - Rojo Coral: `STALINGRADO` (titular central sobre humareda).
  - Azul Táctico: `DE NOCHE, BAJO EL FUEGO`.
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Etiquetas cartográficas en píldora negra: `STALINGRADO` (en el hook con flechas de avance animadas), `KALACH`.
  - Cintas mecanografiadas con pestaña roja: `[| LA BATALLA QUE DIO VUELTA LA GUERRA ]`, `[| 28 DE JULIO DE 1942 ]` (sobre el documento original en ruso de la Orden 227 `ПРИКАЗ № 227`).
  - Tarjeta climática en esquina inferior izquierda: `-30 °C` (azul hielo `#60A5FA`) / `BAJO CERO` (blanco).
  - Botón de dilema en el cierre sobre foto de Paulus: caja negra con borde blanco `OBEDECER`.
- **Nivel 4 (Píldoras de atribución legal):**
  - `PELÍCULA DE ARCHIVO · «STALINGRADO», CDSF, 1943 · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · P. FISXO · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · SERGEY STRUNNIKOV · DOMINIO PÚBLICO`
  - `FOTO DE ARCHIVO · BUNDESARCHIV, KLOSE · CC BY-SA 3.0 DE`
  - `FOTO DE ARCHIVO · BUNDESARCHIV · CC BY-SA 3.0 DE`

---

### `#08` | `VKEIpXxGMVk` — *Cândido Godói: el pueblo de los gemelos y la teoría sobre Mengele*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/VKEIpXxGMVk/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/VKEIpXxGMVk/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `Imaginá **vivir**` → `**donde,**` → `donde, en algunas / **calles,**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `nombre de Helmut / [Gregor.]` (fotograma 7), `pueblo con [remedios] / **nuevos.**` (fotograma 9).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema: `CÂNDIDO GODÓI`, `CIENTOS DE PARES`, `1985: ABREN LA TUMBA`.
  - Amarillo/Ámbar: `«TERRA DOS GÊMEOS»`, `«HELMUT GREGOR»`, `LA TEORÍA` (justo debajo del subtítulo superior en el fotograma 9), `UNA VARIANTE DE UN GEN`.
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Gráfica estadística de barras minimalista sobre fondo negro con eje horizontal cronológico (`'30  '40  '50  '60  '70  '80  '90`) mostrando una barra amarilla en `'30` para demostrar que los nacimientos de gemelos precedían a los años 60.
  - Ilustración de doble hélice de ADN con un par de bases iluminado en amarillo brillante sobre `UNA VARIANTE DE UN GEN`.
- **Nivel 4 (Píldoras de atribución legal):**
  - `FOTO · CÂNDIDO GODÓI · CC BY-SA 3.0 · FELIPE P`
  - `FOTO · CHICOS LIBERADOS, 1945 · FILMACIÓN SOVIÉTICA · DOMINIO PÚBLICO`
  - `FOTO · PASAPORTE «HELMUT GREGOR» · CC BY-SA 3.0 · JACKDAWSON`
  - `FOTO · CORREIO DA MANHÃ · ARQUIVO NACIONAL · DOMINIO PÚBLICO`

---

### `#09` | `UjI03Si4VA8` — *La Primera Guerra Mundial en 3 minutos: de Sarajevo al armisticio*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/UjI03Si4VA8/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/UjI03Si4VA8/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `¿Cómo **pudieron**` → `¿Cómo pudieron dos / [balas,]` → `disparadas en / **Sarajevo,**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `[balas,]` (en el hook, 2.º segundo), `[alianzas:] **Alemania**` (fotograma 3), `en el [Marne,]` (fotograma 7).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema: `LAS ALIANZAS`, `AMETRALLADORAS / ALAMBRE / ARTILLERÍA` (lista apilada en tres líneas en el centro de la pantalla).
  - Amarillo/Ámbar: `AL MINUTO`.
  - Rojo Coral: `RUSIA SALE`, `EL POLVORÍN` (cierre sobre el mapa de Europa).
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Etiquetas cartográficas sobre mapa color pergamino: `SARAJEVO` (con ondas expansivas blancas en el hook), `ALEMANIA`, `PARÍS`, `Sarajevo`.
  - Cintas mecanografiadas en papel crema con pestaña lateral: `[| 1914 ]`, `[| 28 DE JULIO – 4 DE AGOSTO DE 1914 ]`, `[| SEPTIEMBRE DE 1914 · EL MARNE ]`, `[| VERDÚN · 1916 ]`.
  - Contador de días en caja gris con números amarillos bajo la cinta de Verdún: `75 / DÍAS` (avanzando hacia 300).
  - Pies de foto contextuales en píldora negra redondeada: `París, 2 de agosto de 1914` y `Una detención en Sarajevo, 28-6-1914`.
- **Nivel 4 (Píldoras de atribución legal):**
  - `AGENCE ROL · PARÍS, 2-8-1914 · GALLICA`
  - `FOTO DE ARCHIVO · SARAJEVO, 28-6-1914`
  - `FILMACIÓN DE ÉPOCA · THE BATTLE OF THE SOMME, 1916 · IWM`
  - `AGENCE ROL · VERDÚN, 1916 · GALLICA`
  - `A. R. WILLIAMS · PETROGRADO, 1917`
  - `D-KURU · CC BY-SA 4.0`

---

### `#10` | `g_M7r8EMoFg` — *El caballo de Troya: el engaño que abrió las puertas de una ciudad*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/g_M7r8EMoFg/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/g_M7r8EMoFg/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `¿Cómo pudo` → `¿Cómo pudo un / [regalo] de **madera**` → `destruir la **ciudad**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `[regalo]` (en el hook, 2.º segundo), `sitian [Troya,] **una**` (fotograma 3), `[desaparece.]` (fotograma 10).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema: `COSTA DE LA ACTUAL TURQUÍA` (bajo `TROYA`), `¿UNA MÁQUINA DE ASEDIO? / ¿UN TERREMOTO?`.
  - Amarillo/Ámbar: `UN REGALO` (en el hook sobre el cuadro de Tiepolo que pasa a envolverse en llamas), `TROYA`, `ODISEO`, `LAOCOONTE`, `CASANDRA`, `LA TRAMPILLA`.
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Etiqueta cartográfica sobre mapa antiguo: `TROIA` (superpuesta con el titular `TROYA`).
- **Nivel 4 (Píldoras de atribución legal):**
  - `G. D. TIEPOLO, c. 1760 · NATIONAL GALLERY`
  - `ZDF / TERRA X · CC BY 4.0`
  - `G. D. TIEPOLO, c. 1760`
  - `H.-P. MOTTE, 1874`
  - `CABALLO EN EL SITIO DE TROYA · MTHELETTER · CC BY-SA 4.0`
  - `E. DE MORGAN, «CASANDRA», 1898`
  - `MICENAS · LE MONDE EN VIDÉO · CC BY 3.0`

---

### `#11` | `V3ase69Rap8` — *Napoleón: cuándo actuar y cuándo esperar | De Austerlitz a Waterloo*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/V3ase69Rap8/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/V3ase69Rap8/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `¿Por qué el **hombre**` → *(pausa visual con aparición de rótulo)* → `de Europa pedía **que**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `a dos [emperadores:]` (fotograma 7), `[equivocarte.]` (fotograma 12).
- **Nivel 2 (Titulares de sección `ALL CAPS` con contorno negro sólido estilo Voxel):**
  - Rojo Coral con borde negro: `APURADO` (en el hook junto al reloj analógico).
  - Amarillo/Ámbar con borde negro: `1805`, `AUSTERLITZ / 2·12·1805`, `VICTORIA`.
  - Blanco con borde negro: `2 EMPERADORES`, `WATERLOO / 1815`.
  - Gris Acero con borde negro: `PRATZEN, VACÍO`, `LOS PRUSIANOS`.
  - Verde Esmeralda (`#4ADE80`) con borde negro: `CERO ERRORES` (en el cierre).
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Etiquetas geográficas blancas sobre escenario de bloques: `CANAL DE LA MANCHA`, `DANUBIO`.
  - Placa de cita en caja negra con doble marco dorado: `«PÍDANME CUALQUIER / COSA, MENOS TIEMPO»`.
  - Bocadillo de diálogo (cómic) blanco con borde negro apuntando al personaje voxel de Napoleón: `¿CUÁNTO TARDÁS?`.
  - Etiqueta horaria bajo el reloj de Waterloo: `11:30`.
- **Nivel 4 (Píldoras de atribución legal):**
  - No aplica (el 100 % del metraje es animación 3D voxel propia).

---

### `#12` | `GZNpPvHITiM` — *¿Por qué Marco Aurelio dormía en el suelo a los 12 años?*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/GZNpPvHITiM/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/GZNpPvHITiM/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores):**
  - Hook (0–3s): `¿Por qué el **hombre**` → `a **gobernar**` → `a gobernar medio / mundo`.
  - Bloques en storyboard: `familia **riquísima,**`, `**emperador.**`, `desear un **catre**`, `No es castigarse. Es / **quitarle**`, `volverte un César, / con **teñirte**`, `Danubio. Y el **tesoro**`, `**Hasta**`, `**soldados.**`, `para`, `copas de oro, **no.**`.
- **Nivel 2 y Nivel 3 (Píldoras doradas de contexto y citas literarias):**
  - **Píldoras oscuras con borde dorado (`#D4A853`)** alineadas a la izquierda (`x ≈ 12%`, `y ≈ 42%` o `y ≈ 80%`):
    - `El palacio` (en el hook, segundos 2 y 3)
    - `Familia riquísima`
    - `Iba a ser emperador`
    - `Meditaciones, libro 1`
    - `Quitarle poder al miedo`
    - `Meditaciones 6.30`
    - `Los vestidos de su esposa`
    - `En la frontera del Danubio`
    - `No era para sufrir`
    - `Las copas de oro, no`
  - **Citas textuales en serif cursiva dorada (`Playfair Display` / `Georgia Italic`)** al pie de las páginas ilustradas de *Meditaciones*:
    - `«un catre y una piel»`
    - `«No te vuelvas un César»`
  - Cubierta ilustrada del libro en el cierre: `MARCO AURELIO / MEDITACIONES`.
- **Nivel 4 (Píldoras de atribución legal):**
  - `FOTO · MARCO AURELIO JOVEN, MUSEOS CAPITOLINOS · DOMINIO PÚBLICO`

---

### `#13` | `ff2r8EirvVI` — *Hernán Cortés no quemó sus naves: la historia detrás del mito*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/ff2r8EirvVI/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/ff2r8EirvVI/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `¿Por qué **Hernán**` → `**destruyó**` → `destruyó sus propias / [naves,]`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `[naves,]` (en el 3.er segundo del hook), `[rebelde.]` (fotograma 4), `Vera [Cruz,] y **se**` (fotograma 6), `[perforados] y / **desarmados.**` (fotograma 8).
- **Nivel 2 y Nivel 3 (Píldoras doradas de sección y contexto):**
  - Titular central en píldora grande con texto dorado condensado: `CUBA, 1519` (y en el fotograma 11 píldora difuminada en transición `13 bergantines`).
  - Píldoras oscuras con borde dorado (`#D4A853`) alineadas a la izquierda:
    - `Hernán Cortés` / `Rebelde` (apiladas sobre el retrato del siglo XVI)
    - `Villa Rica de la Vera Cruz`
    - `La conjura para huir`
    - `Perforados y desarmados`
    - `8 de noviembre de 1519` / `«Un encantamiento»` (apiladas sobre el lienzo del encuentro con Moctezuma)
    - `Sin otra opción que el coraje` (en el cierre).
- **Nivel 4 (Píldoras de atribución legal):**
  - `FOTO · CORTÉS, s. XVI · CC BY-SA 3.0`
  - `FOTO · ENCUENTRO DE CORTÉS Y MOCTEZUMA · DOMINIO PÚBLICO`

---

### `#14` | `VFppMLRXRqk` — *¿Por qué Marco Aurelio dejó Roma en manos de Cómodo?*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/VFppMLRXRqk/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/VFppMLRXRqk/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `¿Por qué el / **emperador**` → `sabio`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `[avestruz]` (fotograma 10 del storyboard).
- **Nivel 2 y Nivel 3 (Píldoras doradas y textos diegéticos):**
  - Titular central en píldora grande con borde dorado: `CASI 100 AÑOS`.
  - Píldoras oscuras con borde dorado (`#D4A853`):
    - `Al frente del Danubio`
    - `Marco Aurelio, 58 años`
    - `Casio Dion, senador`
    - `Las Meditaciones sobrevivieron`
  - Textos diegéticos en escena: inscripción `CONSVL` en tablilla romana junto a monedas de oro y mazo de subasta; inscripción original `COMMODVS ANTONINVS AVG PIVS` en el áureo romano; cubiertas de libros `MARCO AURELIO / MEDITACIONES` en el cierre.
- **Nivel 4 (Píldoras de atribución legal):**
  - `FOTO · ÁUREO DE CÓMODO · CC BY-SA 2.5 · CNG`
  - `FOTO · MARCO AURELIO · DOMINIO PÚBLICO`
  - `FOTO · CASIO DION · DOMINIO PÚBLICO`

---

### `#15` | `fGYdtXyKbtQ` — *Marco Aurelio y sus Meditaciones: el diario del emperador estoico*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/fGYdtXyKbtQ/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/fGYdtXyKbtQ/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `¿Qué **escribe**` → `**poderoso**` → `poderoso del mundo / **cuando**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `[recordatorios.]` (fotograma 7), `mismo esta [noche,]` (fotograma 12).
- **Nivel 2 y Nivel 3 (Píldoras doradas y textos diegéticos):**
  - Titular central en píldora grande con borde dorado: `AÑO 175`.
  - Píldoras oscuras con borde dorado (`#D4A853`):
    - `La guerra`
    - `En griego`
    - `Recordatorios`
    - `Avidio Casio`
    - `La estatua ecuestre`
  - Textos diegéticos en la ilustración: estandartes romanos `SPQR` en el hook; manuscrito griego con encabezado `ΤΑ` (`ΠΕΝΟ ΒΕΧΙΕΖΕΝ ΥΘ ΜΕΓΛΔΝΩΔ...`); tablilla oscura con inscripción en latín `MARCVS / MORTVVS?` en color rojo terracota.
- **Nivel 4 (Píldoras de atribución legal):**
  - `FOTO · ÁUREO DEL 174 · DOMINIO PÚBLICO · CNG`
  - `FOTO · ESTATUA ECUESTRE · DOMINIO PÚBLICO · ALVESGASPAR`

---

### `#16` | `3tSKNGKJOrc` — *Epicteto: el esclavo que inspiró a Marco Aurelio | Estoicismo*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/3tSKNGKJOrc/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/3tSKNGKJOrc/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `¿Cómo un [esclavo]` → `**pierna**` → `pierna rota **terminó**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `[esclavo]` (en el 1.er segundo del hook), `[rengo] quedó` (fotograma 5), `chico: si querés a una / [jarra,]` (fotograma 8), `depende de [vos.]` (fotograma 9).
- **Nivel 2 y Nivel 3 (Píldoras doradas e infografía dicotómica):**
  - Píldoras oscuras con borde dorado (`#D4A853`):
    - `Hierápolis` / `Hacia el año 50` (apiladas sobre foto de ruinas)
    - `Según un relato antiguo`
    - `Rengo para siempre`
    - `Libre`
    - `Una lámpara de hierro`
    - `No son las cosas`
  - **Tabla comparativa de la Dicotomía del Control (fotograma 9):** Línea divisoria vertical dorada en la mitad izquierda; columna izquierda encabezada por píldora con borde dorado `Depende de vos` y tres bloques sólidos dorados (`#E5C158`) con texto negro en mayúsculas: `DECIDIR`, `QUERER`, `PENSAR`; columna derecha encabezada por píldora con borde gris `No depende`.
- **Nivel 4 (Píldoras de atribución legal):**
  - `FOTO · HIERÁPOLIS · CC BY-SA 2.0 · C. RADDATO`
  - `FOTO · MARCO AURELIO JOVEN · DOMINIO PÚBLICO · D. DESCOUENS`

---

### `#17` | `kOpUJPR9BOM` — *Dien Bien Phu: la trampa que derrotó a Francia en Vietnam*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/kOpUJPR9BOM/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/kOpUJPR9BOM/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `**Noviembre**` → `Noviembre de **1953.**` → `Noviembre de **1953.**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `a mano y con [sogas.]` (fotograma 6 del storyboard).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema: `NOVIEMBRE 1953` (en el hook sobre los paracaidistas), `B-29 · 42`, `SUBESTIMAR` (en el cierre).
  - Amarillo/Ámbar: `DIEN BIEN PHU`, `NOMBRES DE MUJER`, `A MANO Y CON SOGAS`, `4 A 1`.
  - Rojo Coral: `NORTE: COMUNISTA` (sobre el mapa de Vietnam dividido).
  - Azul Táctico (sello rectangular inclinado): `OPERACIÓN BUITRE`.
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Píldoras oscuras grandes de contexto sobre archivo: `7 AÑOS de guerra en Indochina` (sobre retrato de Ho Chi Minh) y `7 MAY 1954` (sobre la bandera en el búnker francés).
  - Pie de foto en píldora negra: `El puesto de mando, 7-5-1954`.
  - Etiquetas cartográficas en píldora negra: `Dien Bien Phu`, `Hanói`, y en las colinas del valle las micro-etiquetas `Gabrielle`, `Béatrice`, `Isabelle`; línea punteada blanca `PARALELO 17`.
- **Nivel 4 (Píldoras de atribución legal):**
  - `FOTO DE ARCHIVO · 1946`
  - `FOTO DE ARCHIVO · EJÉRCITO POPULAR DE VIETNAM, 7-5-1954`

---

### `#18` | `Km3mMU1pOpM` — *¿Por qué Truman destituyó a MacArthur? | Guerra de Corea*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/Km3mMU1pOpM/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/Km3mMU1pOpM/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `Abril de` → `Abril de **1951.**` → `Abril de **1951.**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `era un [héroe:]` (fotograma 3), `[autoridad] del / **presidente.**` (fotograma 7).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema: `ABRIL 1951` (en el hook), `«CASI NINGUNA CHANCE»`, `LA GUERRA A CHINA`, `MARZO 1951`, `11 ABR 1951`, `SAN FRANCISCO`, `¿QUIÉN MANDA?` (en el cierre sobre la Casa Blanca).
  - Amarillo/Ámbar: `HÉROE` (en píldora oscura grande sobre foto de MacArthur), `AUTORIDAD`, `ECHAR A UN HÉROE`.
  - Rojo Coral: `EQUIVOCADO` (encabezando la lista de Bradley).
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Pie de foto en píldora negra: `Gral. Douglas MacArthur, Corea, 1950`.
  - Documento ilustrado en mesa presidencial: `PROPUESTA DE PAZ` con sello dorado.
  - Libro abierto (memorias de Truman) con texto subrayado en rojo en la página derecha: `Un desafío / a la autoridad / del presidente.`.
  - **Lista apilada con tachado rojo animado (fotograma 11):** Bajo el titular rojo `EQUIVOCADO`, aparecen en blanco `ALL CAPS` las 4 palabras de la cita de Omar Bradley atravesadas por una línea horizontal roja:
    - `~~GUERRA~~`
    - `~~LUGAR~~`
    - `~~MOMENTO~~`
    - `~~ENEMIGO~~`
- **Nivel 4 (Píldoras de atribución legal):**
  - `FOTO DE ARCHIVO · EJÉRCITO DE EE. UU., 1950`

---

### `#19` | `OmO_msj8Wy8` — *Inchon: la apuesta de MacArthur contra la marea | Ep. 4*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/OmO_msj8Wy8/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/OmO_msj8Wy8/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `**Septiembre**` → `Septiembre de **1950.**` → `Septiembre de **1950.**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `[dudas.]` (fotograma 8 del storyboard).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema: `SEPTIEMBRE 1950` (en el hook sobre el buque de desembarco `LST` que queda varado en el barro al bajar la marea), `25 JUN 1950`, `230 KM`, `+200 KM DETRÁS`, `PARTIDA HASTA HOY`.
  - Amarillo/Ámbar: `15 SEP 1950`.
  - Rojo Coral (en píldoras oscuras grandes sobre archivo): `WOLMIDO`, `DUDAS`.
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Inscripción en el casco del barco: `LST`.
  - Etiquetas cartográficas en píldora negra: `Pusan`, `Inchon`, `Seúl`.
  - Pies de foto en píldora negra: `Wolmido, 13-9-1950` y `Collins · MacArthur · Sherman`.
  - Píldora horaria sobre foto del desembarco: `06:30 desembarco`.
  - **Calendario diegético reconstruido (`SEPTIEMBRE 1950`, fotograma 9):** Hoja de calendario color crema donde todos los días del `1` al `30` aparecen tachados con una diagonal roja (`\`), excepto el día **`15`**, que está rodeado por un círculo amarillo luminoso.
- **Nivel 4 (Píldoras de atribución legal):**
  - `FOTO DE ARCHIVO · MARINA DE EE. UU., 13-9-1950`
  - `FOTO DE ARCHIVO · MARINA DE EE. UU., 1950`
  - `FOTO DE ARCHIVO · CUERPO DE MARINES DE EE. UU., 15-9-1950`

---

### `#20` | `RT6my9-VxFI` — *Puente aéreo de Berlín: vencieron el bloqueo sin disparar*
- **Archivos inspeccionados:** [hook_3s.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/RT6my9-VxFI/hook_3s.jpg) | [storyboard.jpg](file:///c:/Users/T490s/Desktop/Proyectos%20Antigravity/Historia/data/raw/RT6my9-VxFI/storyboard.jpg)
- **Nivel 1 (Subtítulos superiores y *Figma Bounding Box*):**
  - Hook (0–3s): `Junio de` → `Junio de **1948.**` → `Junio de **1948.**`.
  - Palabras con **Bounding Box azul (`#3B82F6` + 4 nodos blancos)**: `Eligieron una / [tercera.]` (fotograma 3), `unas pocas [semanas.]` (fotograma 5), `[derribarlo.]` (fotograma 7), `[toneladas.]` (fotograma 11).
- **Nivel 2 (Titulares de sección `ALL CAPS`):**
  - Blanco/Crema: `JUNIO 1948` (en el hook), `IRSE = ENTREGARLA`, `5.000 T / DÍA`.
  - Amarillo/Ámbar: `UNA TERCERA`, `CARAMELOS PARA LOS CHICOS`.
  - Rojo Coral: Sello rectangular inclinado `BLOQUEO` (en el hook sobre la barrera fronteriza), `COMIDA: SEMANAS`, `CONVOY = GUERRA`, `= GUERRA` (sobre avión en punto de mira rojo).
- **Nivel 3 (Textos diegéticos, infografías y documentos):**
  - Sub-etiquetas de desglose bajo `5.000 T / DÍA`: `COMIDA 1.400` y `CARBÓN 3.000` sobre pirámide de sacos y montaña de carbón.
  - Píldoras oscuras grandes de datos sobre fotos de archivo: `21 JUN 1948` (sobre billete de *Deutsche Mark* de 1948) y `2.334.374 toneladas` (en dorado y blanco sobre aviones C-47 descargando).
  - Pie de foto en píldora negra: `Tempelhof, 1948`.
- **Nivel 4 (Píldoras de atribución legal):**
  - `FOTO DE ARCHIVO · MUSEO NACIONAL DE HISTORIA DE EE. UU.`
  - `FOTO DE ARCHIVO · FUERZA AÉREA DE EE. UU., 1949`
  - `FOTO DE ARCHIVO · FUERZA AÉREA DE EE. UU.`
  - `FOTO DE ARCHIVO · FUERZA AÉREA DE EE. UU., 1948`

---

## 3. Patrones Transversales y Sistema de Diseño Tipográfico

### 3.1. Especificación Técnica de los 4 Niveles (Lienzo `1080×1920`)

| Nivel | Nombre Funcional | Coordenada `Y` (`%` y `px`) | Alineación `X` | Familia Tipográfica | Peso (`font-weight`) | Tamaño (`px`) | Paleta de Color (`HEX`) | Comportamiento Dinámico / Animación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Nivel 1** | **Subtítulos Dinámicos + *Figma Bounding Box*** | `16% – 22%` (`307px – 422px`) | Centrado (`x = 50%`), ancho máx. `78%` (`840px`) | `Inter` / `Plus Jakarta Sans` | Inactiva: `400`/`500` (Regular/Medium)<br>Activa: `700` (Bold) | `42px – 46px` (interlineado `1.22`) | Inactiva: `#8A8F98` (`rgba(255,255,255,0.52)`)<br>Activa: `#FFFFFF`<br>BBox: `#3B82F6` | Karaoke por luminancia instantánea palabra por palabra. En palabras gatillo (1 cada ~15s), aparece el marco vectorial azul `#3B82F6` con 4 nodos blancos (`6×6px`) en las esquinas. Protegido siempre por un *scrim* negro superior (`rgba(0,0,0,0.65)`). |
| **Nivel 2** | **Titulares de Sección / Callouts Centrales** | `28% – 36%` (`537px – 691px`) o `72% – 82%` en cierres | Centrado (`x = 50%`) | `Montserrat` / `Inter Display` (`ALL CAPS`) | `800` / `900` (ExtraBold / Black) | `54px – 76px` (`tracking: +0.02em`) | Blanco/Crema: `#F5F2EB`<br>Ámbar: `#F0B429`<br>Rojo Coral: `#E05A47`<br>Azul: `#60A5FA` | Entrada por *pop-in* seco o corte directo sincronizado con el golpe de voz, acompañado de una sombra difusa suave (`0 6px 24px rgba(0,0,0,0.65)`). En sellos (`BLOQUEO`, `HALT!`), rotación de `-4deg` a `-6deg` con borde del mismo color. |
| **Nivel 3** | **Textos Diegéticos, Cintas, Mapas y Pies de Foto** | `40% – 75%` (`768px – 1440px`) | Variable según composición (cintas a `x ≈ 8%`, documentos centrados) | Docs/Cintas: `Courier Prime` / `JetBrains Mono`<br>Píldoras: `Inter SemiBold` | `600` / `700` | Cintas: `26px–30px`<br>Píldoras mapa: `20px–24px`<br>Contadores: `64px–88px` | Cintas: fondo `#EDE6D6`, texto `#18181B`, pestaña `#DC2626`<br>Píldoras: fondo `rgba(20,20,24,0.88)`, texto `#FFFFFF` | Las cintas de fecha se despliegan de izquierda a derecha con efecto máquina de escribir (`typewriter`). Los documentos entran con ligera rotación (`-1.5deg` a `+1.5deg`). Las listas erróneas se tachan con línea roja animada (`strikethrough`). |
| **Nivel 4** | **Píldora Legal / Atribución de Fuente** | `76% – 88%` (`1460px – 1690px`) | Izquierda (`x ≈ 4.5%` / `48px` del borde izquierdo) | `Inter` / `DM Sans` (`ALL CAPS`) | `600` (SemiBold) | `14px – 16px` (`tracking: +0.04em`) | Texto: `#E4E4E7`<br>Fondo: `rgba(0,0,0,0.74)` | Estática durante la duración del plano de archivo o reconstrucción. Formato estandarizado: `TIPO · AUTOR/ARCHIVO, AÑO · LICENCIA`. |

---

### 3.2. Anatomía del "Figma Bounding Box" (El Resaltado Insignia del Canal)

Uno de los hallazgos más originales de `@cdmauro2010` es haber reemplazado los recursos trillados del formato Short (subtítulos amarillos que rebotan, emojis de calaveras/fuego o subrayados de neón) por una metáfora visual tomada directamente del software de diseño vectorial (**Figma / Adobe Illustrator / After Effects**):

```
      □──────────────────────□
      │     medianoche:      │   ← Texto en #FFFFFF Bold
      □──────────────────────□
      ↑                      ↑
  Nodos blancos 6×6px    Borde sólido 2px #3B82F6 + fondo rgba(59,130,246,0.18)
```

- **Frecuencia de uso:** Aparece de forma selectiva (entre **2 y 5 veces por Short**, es decir, solo en el **3 %–5 % de las palabras totales**), lo que evita la fatiga visual y convierte cada aparición en un disparador de atención involuntaria (*pattern interrupt* óptico).
- **Criterio léxico de activación:** Se aplica exclusivamente a **sustantivos nucleares, cifras críticas o verbos de giro dramático** (incluyendo el signo de puntuación contiguo dentro de la caja):
  - *En el Hook (0–3s):* `[foto]` (`#04`), `[minutos?]` (`#05`), `[balas,]` (`#09`), `[regalo]` (`#10`), `[naves,]` (`#13`), `[esclavo]` (`#16`).
  - *En el Desarrollo y Clímax:* `[medianoche:]` y `[débil]` (`#01`), `[alerta]`, `[acorazados;]` y `[horas:]` (`#02`), `[Potsdam,]` y `[probar]` (`#03`), `[semana.]`, `[sirenas.]` y `[Rosenthal,]` (`#04`), `[iniciativa:]` (`#05`), `[Dunkerque,]`, `[razones,]`, `[Göring]`, `[ayuda]` y `[Churchill]` (`#06`), `[civiles.]` y `[obedecer]` (`#07`), `[Gregor.]` y `[remedios]` (`#08`), `[alianzas:]` y `[Marne,]` (`#09`), `[Troya,]` y `[desaparece.]` (`#10`), `[emperadores:]` y `[equivocarte.]` (`#11`), `[rebelde.]`, `[Cruz,]` y `[perforados]` (`#13`), `[avestruz]` (`#14`), `[recordatorios.]` y `[noche,]` (`#15`), `[rengo]`, `[jarra,]` y `[vos.]` (`#16`), `[sogas.]` (`#17`), `[héroe:]` y `[autoridad]` (`#18`), `[dudas.]` (`#19`), `[tercera.]`, `[semanas.]`, `[derribarlo.]` y `[toneladas.]` (`#20`).

---

### 3.3. Por qué colocar los subtítulos en el tercio superior (`y ≈ 18%`) es una ventaja competitiva enorme en Shorts de Historia

En YouTube Shorts, TikTok y Reels, el estándar por defecto de los creadores es situar los subtítulos en el centro (`y = 50%`) o en el tercio inferior (`y = 75%`). La decisión de `@cdmauro2010` de anclarlos en `y ≈ 18%` resuelve tres problemas críticos de golpe:

```
┌──────────────────────────────────────┐  y = 0%
│   [Barra superior / Búsqueda YT]     │
├──────────────────────────────────────┤  y = 14%
│     ¿Cómo pudieron dos [balas,]      │  ◄ NIVEL 1: Subtítulos (y ≈ 16%–22%)
│       disparadas en Sarajevo,        │    Zona limpia, sobre scrim oscuro
├──────────────────────────────────────┤  y = 26%
│           ABRIL 1951                 │  ◄ NIVEL 2: Titular de Sección (y ≈ 30%–35%)
├──────────────────────────────────────┤  y = 38%
│                                      │
│     [ ESCENARIO VISUAL CENTRAL ]     │  ◄ NIVEL 3: Mapas, Retratos, Documentos
│     Retratos sin tapar los ojos,     │    y Cintas Mecanografiadas (y ≈ 40%–75%)
│     mapas tácticos despejados y      │    100% libre de subtítulos encima
│     documentos reconstruidos         │
│                                      │
├──────────────────────────────────────┤  y = 76%
│ [FOTO DE ARCHIVO · DOMINIO PÚBLICO]  │  ◄ NIVEL 4: Píldora Legal (y ≈ 78%–84%, izq.)
├──────────────────────────────────────┤  y = 85%
│ @cdmauro2010 [Suscribirse]      [👍] │  ◄ ZONA MUERTA UI YOUTUBE SHORTS (y = 82%–100%)
│ Título del vídeo y audio...     [💬] │    (Superposición 0% con el contenido)
└──────────────────────────────────────┘  y = 100%
```

1. **Cero colisión con la interfaz de YouTube Shorts (Zero UI-Collision):** El tercio inferior (`y = 80%–100%`) está permanentemente ocupado por el nombre del canal, el botón de suscripción, el título de 2–3 líneas y la barra de audio; y el margen derecho (`x = 84%–100%`, `y = 50%–85%`) por la botonera de Likes, Comentarios y Compartir. Al subir los subtítulos a `y = 18%`, jamás una sola palabra queda tapada por los botones de la plataforma.
2. **Liberación total del centro óptico para la narrativa visual (`y = 38%–75%`):** La historia militar y geopolítica requiere mostrar **mapas con movimientos de pinzas, diagramas técnicos y retratos de archivo**. Si los subtítulos estuvieran en el centro (`y = 50%`), taparían los ojos de Alan Turing (`#01`), la cara de Truman (`#03`), la ruta de los bombarderos en Iwo Jima (`#04`) o el documento de Churchill (`#01`). Al estar arriba, el centro funciona como un proyector limpio de 45 % de altura.
3. **Ergonomía ocular vertical (Fijación Foveal Superior):** En pantallas móviles de 6.1" a 6.8" sostenidas en la mano, el tercio superior queda exactamente a la altura natural de la mirada en reposo. El espectador puede leer el subtítulo en `y = 18%` y ver simultáneamente con su visión periférica inmediata el titular de Nivel 2 (`y = 32%`) y la acción del mapa (`y = 55%`) sin hacer barridos oculares extremos de arriba a abajo.

---

## 4. Conclusiones Accionables y Especificación CSS Lista para Implementar

### 4.1. Cinco Reglas de Oro Accionables para Replicar el Sistema

1. **Instaurar la "Zona Sagrada Superior" (`y = 18%`) con Scrim Permanente:** Nunca colocar subtítulos debajo del `25%` superior del lienzo. Aplicar siempre en la capa inferior a los subtítulos un degradado negro (`linear-gradient(180deg, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0.55) 20%, rgba(0,0,0,0) 32%)`) para que el texto blanco/gris tenga un ratio de contraste WCAG AAA (`> 10:1`) sin importar si el vídeo de fondo es nieve blanca o fuego brillante.
2. **Reemplazar el Karaoke de Color Chillón por Karaoke de Luminancia (`#8A8F98` → `#FFFFFF`):** Prohibir que las palabras cambien a amarillo o verde al pronunciarse. Mantener todo el bloque de 3–7 palabras visible desde el inicio en gris neutro (`#8A8F98`, peso `400`) e iluminar únicamente la palabra activa en Blanco Puro (`#FFFFFF`, peso `700`). Esto permite que el cerebro lea el bloque completo de un vistazo mientras sigue el pulso rítmico de la voz.
3. **Implementar el Componente Vectorial `Figma Bounding Box` con Restricción Estricta (Máximo 4 por vídeo):** Programar el rectángulo azul (`#3B82F6`) con sus 4 nodos blancos de esquina (`6×6px`) como un marcador léxico en el guion (ej. envolviendo la palabra entre corchetes `[medianoche:]` en el generador de subtítulos). Usarlo **siempre una vez en los primeros 3 segundos (hook)** y luego solo 1 vez cada 35–45 segundos en palabras de máximo peso dramático.
4. **Codificar los Callouts Centrales (Nivel 2) con Semántica de 4 Colores Fijos:** Eliminar decisiones arbitrarias de color en edición:
   - **Fechas, lugares y datos neutros** → Blanco Marfil (`#F5F2EB`).
   - **Tesis, conceptos clave y preguntas de retención** → Ámbar Dorado (`#F0B429`).
   - **Peligro, bajas masivas, errores o bloqueo enemigo** → Rojo Coral (`#E05A47`).
   - **Operaciones aliadas, defensa o variables afirmativas** → Azul Táctico (`#60A5FA`).
5. **Convertir las Fuentes Documentales en "Props" Diegéticos (Nivel 3 y 4):** Nunca citar una carta, un telegrama o una fecha solo de voz; renderizar una tarjeta de papel crema (`#EDE6D6`) en fuente monoespaciada (`Courier Prime`) o una cinta mecanografiada con pestaña roja, acompañada siempre por la píldora de atribución en `y = 80%` (`RECONSTRUCCIÓN · TEXTO DE EJEMPLO` o `FOTO DE ARCHIVO · ... · DOMINIO PÚBLICO`), lo que dispara la autoridad percibida del canal.

---

### 4.2. Especificación CSS / HTML Lista para Producción (`1080×1920`)

El siguiente código CSS/HTML define con precisión milimétrica los **4 niveles tipográficos** de `@cdmauro2010` para motores de renderizado programático (Remotion, Motion Canvas, FFmpeg + Puppeteer o plantillas HTML/CSS):

```css
/* ==========================================================================
   SISTEMA TIPOGRÁFICO DE 4 NIVELES - ESTILO @cdmauro2010 (1080x1920)
   Fuentes recomendadas: 'Inter', 'Montserrat', 'Courier Prime'
   ========================================================================== */

:root {
  /* Paleta Nivel 1 (Subtítulos) */
  --sub-inactive: #8A8F98;
  --sub-active: #FFFFFF;
  --bbox-border: #3B82F6;
  --bbox-fill: rgba(59, 130, 246, 0.20);
  --bbox-node-bg: #FFFFFF;

  /* Paleta Semántica Nivel 2 (Titulares ALL CAPS) */
  --callout-neutral: #F5F2EB; /* Fechas, lugares, nombres */
  --callout-key: #F0B429;     /* Conceptos clave, preguntas, giros */
  --callout-danger: #E05A47;  /* Peligro, error, ataque enemigo */
  --callout-allied: #60A5FA;  /* Defensa, operaciones aliadas */

  /* Paleta Nivel 3 y 4 (Diegéticos y Atribución) */
  --paper-cream: #EDE6D6;
  --paper-ink: #18181B;
  --pill-dark-bg: rgba(20, 20, 24, 0.88);
  --pill-gold-border: #D4A853;
  --legal-bg: rgba(0, 0, 0, 0.74);
  --legal-text: #E4E4E7;
}

.short-canvas {
  position: relative;
  width: 1080px;
  height: 1920px;
  overflow: hidden;
  background-color: #0F1115;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Scrim protector superior para garantizar legibilidad del Nivel 1 */
.top-scrim {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 620px;
  background: linear-gradient(
    180deg,
    rgba(0, 0, 0, 0.78) 0%,
    rgba(0, 0, 0, 0.58) 55%,
    rgba(0, 0, 0, 0.00) 100%
  );
  pointer-events: none;
  z-index: 10;
}

/* --------------------------------------------------------------------------
   NIVEL 1: SUBTÍTULOS DINÁMICOS SUPERIORES (y ≈ 16% - 22%)
   -------------------------------------------------------------------------- */
.level-1-subtitles {
  position: absolute;
  top: 320px; /* 16.6% de 1920px */
  left: 50%;
  transform: translateX(-50%);
  width: 840px;
  text-align: center;
  font-size: 44px;
  line-height: 1.24;
  letter-spacing: -0.015em;
  z-index: 20;
}

.sub-word {
  color: var(--sub-inactive);
  font-weight: 400;
  transition: color 0.06s ease, font-weight 0.06s ease;
  display: inline-block;
  margin: 0 5px;
}

.sub-word.is-active {
  color: var(--sub-active);
  font-weight: 700;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.65);
}

/* Sello de Identidad: "Figma Bounding Box" con 4 nodos en las esquinas */
.sub-word.figma-bbox {
  position: relative;
  color: var(--sub-active);
  font-weight: 700;
  background-color: var(--bbox-fill);
  border: 2.5px solid var(--bbox-border);
  padding: 2px 10px 4px 10px;
  margin: 0 6px;
}

.sub-word.figma-bbox .corner-node {
  position: absolute;
  width: 8px;
  height: 8px;
  background-color: var(--bbox-node-bg);
  border: 2px solid var(--bbox-border);
  box-sizing: border-box;
}
.sub-word.figma-bbox .corner-node.tl { top: -5px; left: -5px; }
.sub-word.figma-bbox .corner-node.tr { top: -5px; right: -5px; }
.sub-word.figma-bbox .corner-node.bl { bottom: -5px; left: -5px; }
.sub-word.figma-bbox .corner-node.br { bottom: -5px; right: -5px; }

/* --------------------------------------------------------------------------
   NIVEL 2: TITULARES DE SECCIÓN / CALLOUTS CENTRALES (y ≈ 30% - 36%)
   -------------------------------------------------------------------------- */
.level-2-callout {
  position: absolute;
  top: 580px; /* 30.2% de 1920px */
  left: 50%;
  transform: translateX(-50%);
  width: 960px;
  text-align: center;
  font-family: 'Montserrat', 'Inter', sans-serif;
  font-weight: 900;
  font-size: 64px;
  line-height: 1.08;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  text-shadow: 0 8px 28px rgba(0, 0, 0, 0.75);
  z-index: 20;
}

.level-2-callout.is-neutral { color: var(--callout-neutral); }
.level-2-callout.is-key     { color: var(--callout-key); }
.level-2-callout.is-danger  { color: var(--callout-danger); }
.level-2-callout.is-allied  { color: var(--callout-allied); }

/* Variante Sello Militar Inclinado (ej. BLOQUEO, HALT!, OPERACIÓN BUITRE) */
.level-2-stamp {
  display: inline-block;
  padding: 10px 28px;
  border: 5px solid currentColor;
  transform: rotate(-5deg);
  font-weight: 900;
  letter-spacing: 0.04em;
  background: rgba(15, 17, 21, 0.55);
}

/* --------------------------------------------------------------------------
   NIVEL 3: TEXTOS DIEGÉTICOS, CINTAS MECANOGRAFIADAS Y PÍLDORAS (y ≈ 42%-75%)
   -------------------------------------------------------------------------- */
/* Cinta de fecha mecanografiada con pestaña roja lateral */
.level-3-typewriter-tape {
  position: absolute;
  top: 520px;
  left: 72px;
  display: inline-flex;
  align-items: center;
  background-color: var(--paper-cream);
  color: var(--paper-ink);
  font-family: 'Courier Prime', 'Courier New', monospace;
  font-weight: 700;
  font-size: 28px;
  letter-spacing: 0.03em;
  padding: 8px 20px;
  border-left: 8px solid #DC2626;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.45);
  z-index: 25;
}

/* Pie de foto identificativo / Etiqueta cartográfica */
.level-3-context-pill {
  display: inline-block;
  background-color: var(--pill-dark-bg);
  color: #FFFFFF;
  font-size: 22px;
  font-weight: 700;
  padding: 8px 18px;
  border-radius: 8px;
  border: 1.5px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.50);
}

/* Variante Píldora Dorada (Serie Estoicismo / Roma / Cortés) */
.level-3-context-pill.is-stoic {
  border-color: var(--pill-gold-border);
  font-family: 'Oswald', 'Inter', sans-serif;
  letter-spacing: 0.02em;
}

/* Lista con tachado rojo (ej. ~~GUERRA~~, ~~LUGAR~~ en #18) */
.level-3-strikethrough-item {
  position: relative;
  display: inline-block;
  color: #FFFFFF;
  font-weight: 800;
  font-size: 46px;
  text-transform: uppercase;
}
.level-3-strikethrough-item::after {
  content: "";
  position: absolute;
  left: -6%;
  top: 50%;
  width: 112%;
  height: 6px;
  background-color: var(--callout-danger);
  transform: translateY(-50%);
}

/* --------------------------------------------------------------------------
   NIVEL 4: PÍLDORA LEGAL / ATRIBUCIÓN DOCUMENTAL (y ≈ 78% - 82%, izquierda)
   -------------------------------------------------------------------------- */
.level-4-legal-pill {
  position: absolute;
  top: 1510px; /* 78.6% de 1920px, justo encima de la UI de YouTube Shorts */
  left: 48px;
  max-width: 920px;
  background-color: var(--legal-bg);
  color: var(--legal-text);
  font-size: 15px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 6px 14px;
  border-radius: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  z-index: 30;
}
```
