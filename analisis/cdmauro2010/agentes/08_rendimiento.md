# Informe del Agente 8: Análisis de Rendimiento Cuantitativo y Cualitativo (`@cdmauro2010`)

> **Corte de Extracción de Datos:** `2026-10-27 16:30:00 UTC` (`13:30:00 ART`, `UTC-3`)
> **Muestra Analizada:** `N = 20` Shorts (`#01` a `#20`, correspondientes a los 20 vídeos más recientes del canal entre el `2026-10-22` y el `2026-10-27`).
> **Volumen Agregado de la Muestra:** `2,869,759` vistas en corte inicial (`2,874,406` en extracción profunda de comentarios) | `133,872` likes | `2,531` comentarios.

---

## 0. Nota Metodológica Crucial: Separación del Efecto de Recencia (`< 24h` vs. Maduros `> 24h`) y Reconciliación de Cortes

Para evitar sesgos graves en la interpretación estadística de los 20 Shorts, este informe aplica dos controles metodológicos estrictos:

1. **Aislamiento del Efecto de Recencia (Ventana de Exploración vs. Ventana de Expansión Algorítmica):**
   - **Cohorte en Fase de Semilla (`< 6h` de vida):** Los vídeos **`#01` (`UsMkfLhccJM`, Enigma/Turing)** y **`#02` (`t89RDX8qolU`, Pearl Harbor)** fueron publicados el mismo día del corte (`2026-10-27` a las `15:21 UTC` y `13:44 UTC`), contando con apenas **`1.14 horas`** (~1h 08m) y **`2.76 horas`** (~2h 45m) de antigüedad respectivamente. Sus vistas brutas (`2,540` y `6,092`) reflejan exclusivamente el **tráfico inicial de suscriptores y notificaciones**, donde el *Engagement Rate* está artificialmente inflado (`8.82%` y `10.52%`) antes de que el algoritmo de Shorts abra el grifo hacia audiencias frías.
   - **Cohorte en Transición (`15h – 24h` de vida):** Los vídeos **`#03` (`Dn8s4cqsNCQ`, Hiroshima, `15.6h`)**, **`#04` (`4VT2qvIRUkg`, Iwo Jima, `17.0h`)**, **`#05` (`lYVMDblBX3Y`, Midway, `19.6h`)** y **`#06` (`KCrSmZt-A0w`, Dunkerque, `22.0h`)** ya han atravesado el primer test de audiencia fría. De hecho, `#05` (*Midway*) ya acumula `170,248` vistas en `19.6h` (`8,695 vistas/h`), mientras que `#04` (*Iwo Jima*, `17,171` vistas en `17.0h`) ya muestra signos claros de estancamiento prematuro (`1,009 vistas/h`).
   - **Cohorte Madura (`> 24h` de vida, `#07` a `#20`, y Sub-cohorte Consolidada `> 15h`, `#03` a `#20`):** Los vídeos `#07` a `#20` tienen entre `25.4 horas` y `114.9 horas` (`1.06` a `4.79 días`), permitiendo evaluar su techo real de distribución en el feed de Shorts. Por ello, todos los rankings de Vistas y el análisis de **Ganadores vs. Perdedores (Bottom 3)** separan explícitamente el ranking bruto (`N = 20`) del ranking ajustado por madurez (excluyendo `#01` y `#02`).
2. **Trazabilidad entre el Corte de Índice Inicial y la Extracción Profunda:**
   - En los vídeos de mayor velocidad activa de tráfico se registran mínimas variaciones positivas entre la captura del índice general y el volcado profundo de comentarios minutos después: `#18` (`457,751` → `457,924`), `#12` (`299,497` con `6.60%` ER → `301,299` con `6.65%` ER), `#17` (`291,098` → `291,387`) y `#03` (`55,735` con `5.58‰` Comment Rate → `58,214` con `5.34‰`). Ambas cifras se consignan en las tablas para garantizar exactitud total.

---

## 1. Ficha de Rendimiento Individual de los 20 Vídeos (`#01` al `#20`)

### 1.1. Tabla Maestra de Rendimiento Cuantitativo y Técnico (`#01` – `#20`)

| # | ID | Título del Short | Fecha Pub (UTC) | Antigüedad (`16:30 UTC`) | Vistas (Índice / Prof.) | Likes | Com. | Eng. Rate `(L+C)/V` | Like Rate `L/V` | Comment Rate (`Com/1k V`) | Velocidad (`Vistas/h`) | Velocidad (`Vistas/Día`) | WPM | Cortes/10s (`>0.3` / `>0.15`) |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#01** | `UsMkfLhccJM` | Enigma: Alan Turing y el equipo que descifró el código nazi | `2026-10-27 15:21` | **1.14 h** *(0.05d)* | **2,540** | 223 | 1 | **8.82%** | 8.78% | **0.39‰** | 2,224/h | *53,378/d*\* | 148.3 | 2.28 / 3.44 |
| **#02** | `t89RDX8qolU` | Pearl Harbor 1941: la alerta del radar que fue ignorada | `2026-10-27 13:44` | **2.76 h** *(0.12d)* | **6,092** | 629 | 12 | **10.52%** | 10.32% | **1.97‰** | 2,206/h | *52,952/d*\* | 157.0 | 2.56 / 4.11 |
| **#03** | `Dn8s4cqsNCQ` | Hiroshima 1945: ¿era necesaria la bomba atómica? \| SGM | `2026-10-27 00:52` | **15.62 h** *(0.65d)* | **58,214** *(55,735)* | 3,628 | 311 | **6.77%** *(7.07%)* | 6.23% | **5.58‰** *(5.34‰)* | 3,726/h | 89,432/d | 164.0 | 2.17 / 2.50 |
| **#04** | `4VT2qvIRUkg` | Iwo Jima 1945: la historia detrás de la foto y la segunda bandera | `2026-10-26 23:29` | **17.01 h** *(0.71d)* | **17,171** | 1,503 | 11 | **8.82%** | 8.75% | **0.64‰** | 1,009/h | 24,226/d | 162.0 | 2.00 / 2.61 |
| **#05** | `lYVMDblBX3Y` | Midway 1942: los minutos que cambiaron la guerra del Pacífico | `2026-10-26 20:55` | **19.58 h** *(0.82d)* | **170,248** | 7,867 | 82 | **4.67%** | 4.62% | **0.48‰** | **8,695/h** | **208,668/d** | 154.7 | 1.39 / 2.11 |
| **#06** | `KCrSmZt-A0w` | Dunkerque 1940: ¿por qué Hitler frenó los tanques? \| SGM | `2026-10-26 18:30` | **21.99 h** *(0.92d)* | **64,786** | 3,165 | 75 | **5.00%** | 4.89% | **1.16‰** | 2,946/h | 70,706/d | 158.4 | 2.08 / 2.47 |
| **#07** | `yeMKOTtYlWU` | Stalingrado en 3 minutos: «Ni un paso atrás» \| SGM | `2026-10-26 15:06` | **25.38 h** *(1.06d)* | **71,565** | 3,885 | 87 | **5.55%** | 5.43% | **1.22‰** | 2,819/h | 67,662/d | 160.7 | 2.83 / 6.78 |
| **#08** | `VKEIpXxGMVk` | Cândido Godói: el pueblo de los gemelos y la teoría sobre Mengele | `2026-10-26 12:03` | **28.44 h** *(1.18d)* | **28,297** | 2,035 | 10 | **7.23%** | 7.19% | **0.35‰** | 995/h | 23,881/d | 158.8 | 1.46 / 1.63 |
| **#09** | `UjI03Si4VA8` | a Primera Guerra Mundial en 3 minutos: de Sarajevo al armisticio | `2026-10-25 18:32` | **45.95 h** *(1.91d)* | **205,332** | 9,241 | 105 | **4.55%** | 4.50% | **0.51‰** | 4,468/h | 107,244/d | 150.7 | 2.61 / 6.33 |
| **#10** | `g_M7r8EMoFg` | El caballo de Troya: el engaño que abrió las puertas de una ciudad | `2026-10-25 15:53` | **48.61 h** *(2.03d)* | **18,048** | 1,152 | 11 | **6.44%** | 6.38% | **0.61‰** | **371/h** | **8,911/d** | 167.0 | 1.78 / 2.17 |
| **#11** | `V3ase69Rap8` | Napoleón: cuándo actuar y cuándo esperar \| De Austerlitz a Waterloo | `2026-10-25 01:13` | **63.27 h** *(2.64d)* | **65,181** | 5,670 | 20 | **8.73%** | 8.70% | **0.31‰** | 1,030/h | 24,725/d | 169.3 | 0.89 / 1.06 |
| **#12** | `GZNpPvHITiM` | ¿Por qué Marco Aurelio dormía en el suelo a los 12 años? | `2026-10-25 00:09` | **64.34 h** *(2.68d)* | **299,497** *(301,299)* | **19,838** | 206 | **6.60%** *(6.65%)* | 6.58% | **0.69‰** | **4,655/h** | **111,711/d** | 166.3 | 1.06 / 1.45 |
| **#13** | `ff2r8EirvVI` | Hernán Cortés no quemó sus naves: la historia detrás del mito | `2026-10-24 01:32` | **86.95 h** *(3.62d)* | **223,683** | 9,803 | 359 | **4.54%** | 4.38% | **1.61‰** | 2,572/h | 61,739/d | 158.9 | 1.34 / 1.51 |
| **#14** | `VFppMLRXRqk` | ¿Por qué Marco Aurelio dejó Roma en manos de Cómodo? | `2026-10-23 23:58` | **88.53 h** *(3.69d)* | **161,559** | 6,134 | 28 | **3.81%** | 3.80% | **0.17‰** | 1,825/h | 43,799/d | 180.0 | 1.56 / 1.96 |
| **#15** | `fGYdtXyKbtQ` | Marco Aurelio y sus Meditaciones: el diario del emperador estoico | `2026-10-23 01:23` | **111.11 h** *(4.63d)* | **93,093** | 4,981 | 18 | **5.37%** | 5.35% | **0.19‰** | 838/h | 20,108/d | 171.2 | 1.64 / 1.81 |
| **#16** | `3tSKNGKJOrc` | Epicteto: el esclavo que inspiró a Marco Aurelio \| Estoicismo | `2026-10-23 00:52` | **111.63 h** *(4.65d)* | **92,214** | 5,372 | 16 | **5.84%** | 5.83% | **0.17‰** | 826/h | 19,826/d | 175.3 | 1.57 / 1.97 |
| **#17** | `kOpUJPR9BOM` | Dien Bien Phu: la trampa que derrotó a Francia en Vietnam | `2026-10-22 22:30` | **113.99 h** *(4.75d)* | **291,098** *(291,387)* | 11,074 | 241 | **3.88%** | 3.80% | **0.83‰** | 2,554/h | 61,291/d | 154.5 | 1.62 / 1.79 |
| **#18** | `Km3mMU1pOpM` | ¿Por qué Truman destituyó a MacArthur? \| Guerra de Corea | `2026-10-22 22:05` | **114.41 h** *(4.77d)* | **457,751** *(457,924)* | 19,219 | **671** | **4.34%** | 4.20% | **1.47‰** | 4,001/h | 96,021/d | 166.0 | 2.00 / 2.11 |
| **#19** | `OmO_msj8Wy8` | Inchon: la apuesta de MacArthur contra la marea \| Ep. 4 | `2026-10-22 21:58` | **114.53 h** *(4.77d)* | **204,776** | 8,211 | 105 | **4.06%** | 4.01% | **0.51‰** | 1,788/h | 42,912/d | 162.0 | 2.22 / 2.28 |
| **#20** | `RT6my9-VxFI` | Puente aéreo de Berlín: vencieron el bloqueo sin disparar | `2026-10-22 21:37` | **114.88 h** *(4.79d)* | **332,747** | 11,546 | 162 | **3.52%** | 3.47% | **0.49‰** | 2,896/h | 69,514/d | 148.3 | 1.78 / 1.78 |

*(\*Nota: Las velocidades por día de `#01` y `#02` son extrapolaciones lineales de sus primeras `1.14h` y `2.76h` de vida).*

---

### 1.2. Fichas Individuales de Diagnóstico (`#01` a `#20`)

#### `#01` | `UsMkfLhccJM` — *Enigma: Alan Turing y el equipo que descifró el código nazi*
- **Métricas Clave:** Vistas: `2,540` | Likes: `223` | Comentarios: `1` | Engagement: `8.82%` | Like Rate: `8.78%` | Comment Rate: `0.39‰`
- **Antigüedad y Velocidad:** `1.14 horas` (`0.048 días` desde `2026-10-27 15:21:28 UTC`) | `2,224 vistas/h` (`53,378 vistas/día` proyectadas).
- **Perfil Técnico y Narrativo:** `180s` | `148.3 WPM` (`445` palabras, el ritmo más pausado junto con `#20`) | `41` cortes fuertes (`2.28 c/10s`, ASL `4.29s`) y `62` totales (`3.44 c/10s`) con arranque hiper-dinámico (`24` cortes suaves en `0-30s`).
- **Diagnóstico de Rendimiento:** **En fase de semilla (`~1h` de vida).** Su volumen bajo de vistas es 100% atribuible a su recencia extrema. Su arranque de `2,224 vistas/h` y `8.82%` de engagement en la primera hora es saludable; además usa el hook de magnitud cuantitativa (*"¿Cómo se rompe un código con 158 trillones de combinaciones que además cambia cada medianoche?"*).

#### `#02` | `t89RDX8qolU` — *Pearl Harbor 1941: la alerta del radar que fue ignorada*
- **Métricas Clave:** Vistas: `6,092` | Likes: `629` | Comentarios: `12` | Engagement: `10.52%` | Like Rate: `10.32%` | Comment Rate: `1.97‰`
- **Antigüedad y Velocidad:** `2.76 horas` (`0.115 días` desde `2026-10-27 13:44:20 UTC`) | `2,206 vistas/h` (`52,952 vistas/día` proyectadas).
- **Perfil Técnico y Narrativo:** `180s` | `157.0 WPM` (`471` palabras) | `46` cortes fuertes (`2.56 c/10s`, ASL `3.83s`) y `74` totales (`4.11 c/10s`).
- **Diagnóstico de Rendimiento:** **En fase de semilla (`~3h` de vida).** Registra el **Engagement Rate más alto de toda la muestra (`10.52%`)** y un altísimo *Comment Rate* temprano (`1.97‰`), impulsado por el debate conspirativo en comentarios (*"AUTOATENTADO / necesitaban un pretexto para entrar en la guerra"*). Apunta a superar las `80k–120k` vistas al madurar.

#### `#03` | `Dn8s4cqsNCQ` — *Hiroshima 1945: ¿era necesaria la bomba atómica? | Segunda Guerra Mundial*
- **Métricas Clave:** Vistas: `58,214` (`55,735` en índice inicial) | Likes: `3,628` | Comentarios: `311` | Engagement: `6.77%` (`7.07%`) | Like Rate: `6.23%` | Comment Rate: `5.58‰` (`5.34‰`)
- **Antigüedad y Velocidad:** `15.62 horas` (`0.651 días` desde `2026-10-27 00:52:39 UTC`) | `3,726 vistas/h` (`89,432 vistas/día`).
- **Perfil Técnico y Narrativo:** `180s` | `164.0 WPM` (`492` palabras) | `39` cortes fuertes (`2.17 c/10s`, ASL `4.50s`). Estructura dialéctica explícita (*"Los que dicen que sí... Los que dicen que no..."*).
- **Diagnóstico de Rendimiento:** **Campeón absoluto de controversia del canal (`5.58‰` comentarios por cada 1.000 vistas, `3.8x` más que el #1 en vistas `#18`).** Con apenas `15.6h` de vida mantiene una velocidad de `3,726 vistas/h` (casi idéntica a la media de `#18` `4,001/h`), perfilándose para superar las `200k` vistas en 72 horas.

#### `#04` | `4VT2qvIRUkg` — *Iwo Jima 1945: la historia detrás de la foto y la segunda bandera*
- **Métricas Clave:** Vistas: `17,171` | Likes: `1,503` | Comentarios: `11` | Engagement: `8.82%` | Like Rate: `8.75%` | Comment Rate: `0.64‰`
- **Antigüedad y Velocidad:** `17.01 horas` (`0.709 días` desde `2026-10-26 23:29:19 UTC`) | `1,009 vistas/h` (`24,226 vistas/día`).
- **Perfil Técnico y Narrativo:** `180s` | `162.0 WPM` (`486` palabras) | `36` cortes fuertes (`2.00 c/10s`, ASL `4.86s`), `82` pausas (segundo máximo del canal).
- **Diagnóstico de Rendimiento:** **Bottom #1 entre vídeos de `>15h` (`17,171` vistas).** Aunque gusta mucho a la audiencia fiel (`8.82%` ER), el algoritmo frenó su alcance frío: el tema es un **micro-detalle fotográfico** (*"la historia detrás de la foto y la segunda bandera"*) en lugar de un dilema estratégico vital, y además sufrió canibalización directa al publicarse solo 2.5 horas después del hit `#05` (*Midway*, `170k`) y 1.4 horas antes de `#03` (*Hiroshima*).

#### `#05` | `lYVMDblBX3Y` — *Midway 1942: los minutos que cambiaron la guerra del Pacífico*
- **Métricas Clave:** Vistas: `170,248` | Likes: `7,867` | Comentarios: `82` | Engagement: `4.67%` | Like Rate: `4.62%` | Comment Rate: `0.48‰`
- **Antigüedad y Velocidad:** `19.58 horas` (`0.816 días` desde `2026-10-26 20:55:08 UTC`) | **`8,695 vistas/h` (`208,668 vistas/día`)**.
- **Perfil Técnico y Narrativo:** `180s` | `154.7 WPM` (`464` palabras) | `25` cortes fuertes (`1.39 c/10s`, ASL `6.92s`) y `38` totales (`2.11 c/10s`).
- **Diagnóstico de Rendimiento:** **Breakout viral en curso (#1 absoluto en Velocidad de Vistas del canal con `8,695 vistas/h`).** Su hook combina shock de compresión temporal + intriga táctica (*"¿Cómo se pierde una guerra en solo 5 minutos? ... todo empezó con un mensaje falso sobre el agua"*). Con menos de 20 horas ya está en el Top 8 histórico de la muestra.

#### `#06` | `KCrSmZt-A0w` — *Dunkerque 1940: ¿por qué Hitler frenó los tanques? | Segunda Guerra Mundialdunkerque*
- **Métricas Clave:** Vistas: `64,786` | Likes: `3,165` | Comentarios: `75` | Engagement: `5.00%` | Like Rate: `4.89%` | Comment Rate: `1.16‰`
- **Antigüedad y Velocidad:** `21.99 horas` (`0.916 días` desde `2026-10-26 18:30:33 UTC`) | `2,946 vistas/h` (`70,706 vistas/día`).
- **Perfil Técnico y Narrativo:** `178s` | `158.4 WPM` (`470` palabras) | `37` cortes fuertes (`2.08 c/10s`, ASL `4.68s`).
- **Diagnóstico de Rendimiento:** **Rendimiento medio-alto sólido (`64.8k` en `<22h`) con alta conversación táctica (`1.16‰` comentarios, #5 del canal).** Presenta un pequeño error tipográfico en el título (`Segunda Guerra Mundialdunkerque`, `84` caracteres, el título más largo del lote), pero su pregunta `¿por qué Hitler frenó los tanques?` sostiene un buen ritmo de `70.7k vistas/día`.

#### `#07` | `yeMKOTtYlWU` — *Stalingrado en 3 minutos: «Ni un paso atrás» | Segunda Guerra Mundial*
- **Métricas Clave:** Vistas: `71,565` | Likes: `3,885` | Comentarios: `87` | Engagement: `5.55%` | Like Rate: `5.43%` | Comment Rate: `1.22‰`
- **Antigüedad y Velocidad:** `25.38 horas` (`1.058 días` desde `2026-10-26 15:06:56 UTC`) | `2,819 vistas/h` (`67,662 vistas/día`).
- **Perfil Técnico y Narrativo:** `180s` | `160.7 WPM` (`482` palabras) | **`51` cortes fuertes (`2.83 c/10s`, ASL `3.46s`) y `122` cortes totales (`6.78 c/10s`) — récord absoluto de densidad de cortes del canal.**
- **Diagnóstico de Rendimiento:** **Caso de estudio sobre rendimiento decreciente de la hiper-edición:** a pesar de tener el montaje más frenético de los 20 vídeos (`51` cortes duros y `122` totales), rinde `71.5k` vistas porque el título es enciclopédico (`Stalingrado en 3 minutos: «Ni un paso atrás»`) en vez de plantear la paradoja brillante que sí tenía en el hook hablado (*"Stalin dio una orden: ni un paso atrás. Meses después, Hitler dio exactamente la misma. Una salvó a su ejército, la otra lo enterró"*).

#### `#08` | `VKEIpXxGMVk` — *Cândido Godói: el pueblo de los gemelos y la teoría sobre Mengele*
- **Métricas Clave:** Vistas: `28,297` | Likes: `2,035` | Comentarios: `10` | Engagement: `7.23%` | Like Rate: `7.19%` | Comment Rate: `0.35‰`
- **Antigüedad y Velocidad:** `28.44 horas` (`1.185 días` desde `2026-10-26 12:03:44 UTC`) | `995 vistas/h` (`23,881 vistas/día`).
- **Perfil Técnico y Narrativo:** `178s` | `158.8 WPM` (`471` palabras) | `26` cortes fuertes (`1.46 c/10s`, ASL `6.59s`). Contiene un `[carraspeo]` audible en el segundo `00:16`.
- **Diagnóstico de Rendimiento:** **Bottom #3 absoluto en vídeos maduros (`28,297` vistas).** Se desvía del posicionamiento nuclear del canal (*"Historia y Decisiones"* estratégicas/filosóficas) hacia el subgénero de misterio genético/curiosidad geográfica periférica, con un hook lento (*"Imagina vivir en un pueblo donde..."*).

#### `#09` | `UjI03Si4VA8` — *a Primera Guerra Mundial en 3 minutos: de Sarajevo al armisticio*
- **Métricas Clave:** Vistas: `205,332` | Likes: `9,241` | Comentarios: `105` | Engagement: `4.55%` | Like Rate: `4.50%` | Comment Rate: `0.51‰`
- **Antigüedad y Velocidad:** `45.95 horas` (`1.915 días` desde `2026-10-25 18:32:56 UTC`) | `4,468 vistas/h` (`107,244 vistas/día`).
- **Perfil Técnico y Narrativo:** `180s` | `150.7 WPM` (`452` palabras) | `47` cortes fuertes (`2.61 c/10s`, ASL `3.75s`) y `114` totales (`6.33 c/10s`). Único Short que actúa como *teaser* de un documental largo de 21 min con CTA de suscripción al final.
- **Diagnóstico de Rendimiento:** **#6 absoluto en vistas (`205.3k`) y #3 en velocidad sostenida (`107.2k vistas/día`).** Funciona a pesar del typo inicial del título (`"a Primera Guerra Mundial..."`) gracias a la magnitud macro-histórica del evento y al hook de efecto mariposa (*"¿Cómo pudieron dos balas, disparadas en Sarajevo, desatar una guerra que mató a más de 15 millones de personas?"*).

#### `#10` | `g_M7r8EMoFg` — *El caballo de Troya: el engaño que abrió las puertas de una ciudad*
- **Métricas Clave:** Vistas: `18,048` | Likes: `1,152` | Comentarios: `11` | Engagement: `6.44%` | Like Rate: `6.38%` | Comment Rate: `0.61‰`
- **Antigüedad y Velocidad:** `48.61 horas` (`2.025 días` desde `2026-10-25 15:53:22 UTC`) | **`371 vistas/h` (`8,911 vistas/día` — mínimo absoluto del canal)**.
- **Perfil Técnico y Narrativo:** `180s` | `167.0 WPM` (`501` palabras) | `32` cortes fuertes (`1.78 c/10s`, ASL `5.45s`), `81` pausas.
- **Diagnóstico de Rendimiento:** **Bottom #2 en vídeos maduros (`18,048` vistas) y #1 peor velocidad diaria (`8,911 vistas/día`).** Fracasa en captación algorítmica porque narra un mito escolar universalmente conocido sin revelar en el título ni en el primer segundo una contradicción o giro desconocido (la desmitificación arqueológica recién aparece en el minuto `02:09`).

#### `#11` | `V3ase69Rap8` — *Napoleón: cuándo actuar y cuándo esperar | De Austerlitz a Waterloo*
- **Métricas Clave:** Vistas: `65,181` | Likes: `5,670` | Comentarios: `20` | Engagement: `8.73%` | Like Rate: `8.70%` | Comment Rate: `0.31‰`
- **Antigüedad y Velocidad:** `63.27 horas` (`2.636 días` desde `2026-10-25 01:13:51 UTC`) | `1,030 vistas/h` (`24,725 vistas/día`).
- **Perfil Técnico y Narrativo:** `179s` | `169.3 WPM` (`505` palabras) | **`16` cortes fuertes (`0.89 c/10s`, ASL `10.53s`, con `0` cortes entre `90-120s`) — mínimo absoluto de edición visual del canal.**
- **Diagnóstico de Rendimiento:** **Anomalía de altísimo Like Rate (`8.70%`, #1 entre vídeos `>24h`) pero alcance limitado (`65.2k` vistas).** El mensaje de desarrollo personal (*"Vísteme despacio, que estoy apurado"*) encanta a quien lo termina (`8.73%` ER), pero el estancamiento visual de `60 segundos` casi sin cortes (`80.47s` a `140.00s`) y comentarios criticando animaciones 3D/Minecraft frenaron su retención en tráfico frío.

#### `#12` | `GZNpPvHITiM` — *¿Por qué Marco Aurelio dormía en el suelo a los 12 años?*
- **Métricas Clave:** Vistas: `299,497` (`301,299` prof.) | Likes: **`19,838` (#1 del canal)** | Comentarios: `206` | Engagement: `6.60%` (`6.65%`) | Like Rate: `6.58%` | Comment Rate: `0.69‰`
- **Antigüedad y Velocidad:** `64.34 horas` (`2.681 días` desde `2026-10-25 00:09:20 UTC`) | **`4,655 vistas/h` (`111,711 vistas/día` — #1 en velocidad entre vídeos `>48h`)**.
- **Perfil Técnico y Narrativo:** `179s` | `166.3 WPM` (`496` palabras) | `19` cortes fuertes (`1.06 c/10s`, ASL `8.95s`).
- **Diagnóstico de Rendimiento:** **Top #3 absoluto en Vistas (`299.5k` / `301.3k`) y #1 absoluto en Likes (`19,838`).** Es el único vídeo de `+250k` vistas que rompe la ley de compresión de engagement manteniendo un extraordinario `6.60%–6.65%` ER. ¿Por qué? Combina una paradoja de estatus extrema en el título (`emperador` vs `dormir en el suelo a los 12 años`) con el clímax de la subasta de los tesoros imperiales y un cierre de alta viralidad emocional (*"¿Qué cosa tenés vos que en realidad ya te tiene a vos?"*).

#### `#13` | `ff2r8EirvVI` — *Hernán Cortés no quemó sus naves: la historia detrás del mito*
- **Métricas Clave:** Vistas: `223,683` | Likes: `9,803` | Comentarios: `359` | Engagement: `4.54%` | Like Rate: `4.38%` | Comment Rate: **`1.61‰` (#2 del canal)**
- **Antigüedad y Velocidad:** `86.95 horas` (`3.623 días` desde `2026-10-24 01:32:49 UTC`) | `2,572 vistas/h` (`61,739 vistas/día`).
- **Perfil Técnico y Narrativo:** `179s` | `158.9 WPM` (`474` palabras) | `24` cortes fuertes (`1.34 c/10s`, ASL `7.16s`).
- **Diagnóstico de Rendimiento:** **Top #5 absoluto en Vistas (`223.7k`) y #1 en controversia dentro de la cohorte madura `>24h` (`1.61‰`, `359` comentarios).** Desmentir una frase hecha universal (*"quemar las naves"*) + tocar la Conquista de México e incluir un punto debatible sobre "Malinche" detonó cientos de comentarios de corrección histórica e identidad hispanoamericana que impulsaron el algoritmo.

#### `#14` | `VFppMLRXRqk` — *¿Por qué Marco Aurelio dejó Roma en manos de Cómodo?*
- **Métricas Clave:** Vistas: `161,559` | Likes: `6,134` | Comentarios: `28` | Engagement: `3.81%` | Like Rate: `3.80%` | Comment Rate: `0.17‰` (mínimo del canal)
- **Antigüedad y Velocidad:** `88.53 horas` (`3.689 días` desde `2026-10-23 23:58:25 UTC`) | `1,825 vistas/h` (`43,799 vistas/día`).
- **Perfil Técnico y Narrativo:** `179s` | **`180.0 WPM` (`537` palabras — velocidad de locución máxima del canal)** | `28` cortes fuertes (`1.56 c/10s`, ASL `6.17s`).
- **Diagnóstico de Rendimiento:** **Top #9 en Vistas (`161.6k`).** El puente con la cultura pop (*"Si viste Gladiador, conocés la versión de Hollywood"*) le dio buen alcance inicial, pero su excesiva velocidad de habla (`180 WPM`) y su pregunta final abstracta (*"¿Hasta dónde somos responsables de lo que hacen los que vienen después?"*) produjeron la tasa de comentarios más baja del canal (`0.17‰`).

#### `#15` | `fGYdtXyKbtQ` — *Marco Aurelio y sus Meditaciones: el diario del emperador estoico*
- **Métricas Clave:** Vistas: `93,093` | Likes: `4,981` | Comentarios: `18` | Engagement: `5.37%` | Like Rate: `5.35%` | Comment Rate: `0.19‰`
- **Antigüedad y Velocidad:** `111.11 horas` (`4.630 días` desde `2026-10-23 01:23:32 UTC`) | `838 vistas/h` (`20,108 vistas/día`).
- **Perfil Técnico y Narrativo:** `177s` | `171.2 WPM` (`505` palabras) | `29` cortes fuertes (`1.64 c/10s`, ASL `5.90s`), LRA `3.9 LU` (mayor rango dinámico vocal).
- **Diagnóstico de Rendimiento:** **Rendimiento medio (`93.1k` vistas, #10 del canal).** Aunque el hook hablado es potente (*"¿Qué escribe el hombre más poderoso del mundo cuando sabe que nadie lo va a leer?"*), el título empaqueta el vídeo como una reseña literaria descriptiva (`Marco Aurelio y sus Meditaciones: el diario del emperador estoico`), logrando un `69%` menos de vistas que `#12` (*dormía en el suelo*).

#### `#16` | `3tSKNGKJOrc` — *Epicteto: el esclavo que inspiró a Marco Aurelio | Estoicismo*
- **Métricas Clave:** Vistas: `92,214` | Likes: `5,372` | Comentarios: `16` | Engagement: `5.84%` | Like Rate: `5.83%` | Comment Rate: `0.17‰`
- **Antigüedad y Velocidad:** `111.63 horas` (`4.651 días` desde `2026-10-23 00:52:19 UTC`) | `826 vistas/h` (`19,826 vistas/día`).
- **Perfil Técnico y Narrativo:** `178s` | `175.3 WPM` (`520` palabras) | `28` cortes fuertes (`1.57 c/10s`, ASL `6.14s`), **`84` pausas (máximo absoluto del canal)**.
- **Diagnóstico de Rendimiento:** **Rendimiento medio (`92.2k` vistas, #11 del canal), gemelo estadístico de `#15` (publicado 31 minutos antes).** Alta aprobación pasiva (`5.83%` Like Rate), pero nula fricción dialéctica en comentarios (`0.17‰`, `335.8 likes` por cada comentario).

#### `#17` | `kOpUJPR9BOM` — *Dien Bien Phu: la trampa que derrotó a Francia en Vietnam*
- **Métricas Clave:** Vistas: `291,098` (`291,387` prof.) | Likes: `11,074` | Comentarios: `241` | Engagement: `3.88%` | Like Rate: `3.80%` | Comment Rate: `0.83‰`
- **Antigüedad y Velocidad:** `113.99 horas` (`4.749 días` desde `2026-10-22 22:30:45 UTC`) | `2,554 vistas/h` (`61,291 vistas/día`).
- **Perfil Técnico y Narrativo:** `179s` | `154.5 WPM` (`461` palabras) | `29` cortes fuertes (`1.62 c/10s`, ASL `5.97s`).
- **Diagnóstico de Rendimiento:** **Top #4 absoluto en Vistas (`291.1k`), rozando el podio a solo `2.8%` de `#12`.** Su éxito radica en la estructura narrativa de **inversión de trampa ("cazador cazado")** (*"Era una trampa para el enemigo. Terminó siendo la trampa de Francia"*) y la hazaña logística visual de Giap subiendo cañones desarmados por la selva, que generó una fuertísima conexión cultural en el Cono Sur (comparándolo con el Cruce de los Andes de San Martín, comentario top con `270 likes`).

#### `#18` | `Km3mMU1pOpM` — *¿Por qué Truman destituyó a MacArthur? | Guerra de Corea*
- **Métricas Clave:** Vistas: **`457,751` (`457,924` prof. — #1 del canal)** | Likes: `19,219` (#2) | Comentarios: **`671` (#1 absoluto)** | Engagement: `4.34%` | Like Rate: `4.20%` | Comment Rate: **`1.47‰` (#3 del canal)**
- **Antigüedad y Velocidad:** `114.41 horas` (`4.767 días` desde `2026-10-22 22:05:14 UTC`) | `4,001 vistas/h` (`96,021 vistas/día`).
- **Perfil Técnico y Narrativo:** `180s` | `166.0 WPM` (`498` palabras) | `36` cortes fuertes (`2.00 c/10s`, ASL `4.86s`), `70` pausas.
- **Diagnóstico de Rendimiento:** **Ganador #1 absoluto del canal (`457.8k` vistas).** Combina todos los disparadores algorítmicos ganadores:
  1. Título en formato pregunta `¿Por qué [Líder A] destituyó a [Líder B]?` (choque de titanes / autoridad civil vs héroe militar).
  2. Dato de alto impacto en el desarrollo (*"presenta una lista de blancos que requería 34 bombas atómicas"*), que monopoliza los comentarios más votados (`495` y `261` likes).
  3. Pregunta de cierre polarizante sobre liderazgo y reglas democráticas (`671` comentarios).

#### `#19` | `OmO_msj8Wy8` — *Inchon: la apuesta de MacArthur contra la marea | Ep. 4*
- **Métricas Clave:** Vistas: `204,776` | Likes: `8,211` | Comentarios: `105` | Engagement: `4.06%` | Like Rate: `4.01%` | Comment Rate: `0.51‰`
- **Antigüedad y Velocidad:** `114.53 horas` (`4.772 días` desde `2026-10-22 21:58:24 UTC`) | `1,788 vistas/h` (`42,912 vistas/día`).
- **Perfil Técnico y Narrativo:** `180s` | `162.0 WPM` (`486` palabras) | `40` cortes fuertes (`2.22 c/10s`, ASL `4.39s`). Contiene un `[carraspeo]` audible en `00:27.52`.
- **Diagnóstico de Rendimiento:** **Top #7 absoluto en Vistas (`204.8k`).** Excelente desempeño por su premisa de "apuesta contra lo imposible", pero rindió un **`55.3%` menos que `#18`** (publicado solo 7 minutos después sobre el mismo protagonista MacArthur) debido a dos lastres: la etiqueta secuencial **`| Ep. 4`** en el título (que genera fricción de entrada en audiencia fría) y la ausencia de un dilema moral controvertido.

#### `#20` | `RT6my9-VxFI` — *Puente aéreo de Berlín: vencieron el bloqueo sin disparar*
- **Métricas Clave:** Vistas: **`332,747` (#2 del canal)** | Likes: `11,546` (#3) | Comentarios: `162` | Engagement: `3.52%` | Like Rate: `3.47%` | Comment Rate: `0.49‰`
- **Antigüedad y Velocidad:** `114.88 horas` (`4.787 días` desde `2026-10-22 21:37:03 UTC`) | `2,896 vistas/h` (`69,514 vistas/día`).
- **Perfil Técnico y Narrativo:** `180s` | `148.3 WPM` (`445` palabras, el ritmo más pausado y claro del lote) | `32` cortes fuertes (`1.78 c/10s`, ASL `5.45s`).
- **Diagnóstico de Rendimiento:** **Ganador #2 absoluto del canal (`332.7k` vistas).** Triunfa por la **resolución lateral de un falso dilema binario** en los primeros 13 segundos (*"Los aliados tenían dos opciones: rendirse o ir a la guerra. Eligieron una tercera"*), respaldada por cifras de escala colosal (`1,383 aviones en 24 horas, casi uno por minuto`) y un ritmo vocal pausado (`148.3 WPM`) que maximiza la comprensión de una audiencia masiva generalista.

---

## 2. Rankings Cruzados Multidimensionales

### 2.1. Ranking 1: Por Vistas Totales (Bruto vs. Ajustado por Madurez)

| Pos. Maduros (`>15h`) | Pos. Bruta (`N=20`) | Vídeo | Vistas (Índice / Prof.) | Antigüedad (`h`) | Velocidad (`Vistas/Día`) | Clasificación de Rendimiento |
| :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| **1º** | 1º | **#18** `Km3mMU1pOpM` — *¿Por qué Truman destituyó a MacArthur?* | **457,751** *(457,924)* | 114.4 h | 96,021/d | 🏆 **TOP 1 ABSOLUTO (Mega-Hit)** |
| **2º** | 2º | **#20** `RT6my9-VxFI` — *Puente aéreo de Berlín: vencieron el bloqueo sin disparar* | **332,747** | 114.9 h | 69,514/d | 🥈 **TOP 2 ABSOLUTO (Mega-Hit)** |
| **3º** | 3º | **#12** `GZNpPvHITiM` — *¿Por qué Marco Aurelio dormía en el suelo a los 12 años?* | **299,497** *(301,299)* | 64.3 h | **111,711/d** | 🥉 **TOP 3 ABSOLUTO (Mega-Hit)** |
| **4º** | 4º | **#17** `kOpUJPR9BOM` — *Dien Bien Phu: la trampa que derrotó a Francia en Vietnam* | **291,098** *(291,387)* | 114.0 h | 61,291/d | 🔥 **Cuasi-Top 3 (`-2.8%` vs #12)** |
| **5º** | 5º | **#13** `ff2r8EirvVI` — *Hernán Cortés no quemó sus naves: la historia detrás del mito* | **223,683** | 87.0 h | 61,739/d | ✅ Éxito Alto (+200k) |
| **6º** | 6º | **#09** `UjI03Si4VA8` — *a Primera Guerra Mundial en 3 minutos: de Sarajevo al armisticio* | **205,332** | 46.0 h | 107,244/d | ✅ Éxito Alto (+200k) |
| **7º** | 7º | **#19** `OmO_msj8Wy8` — *Inchon: la apuesta de MacArthur contra la marea \| Ep. 4* | **204,776** | 114.5 h | 42,912/d | ✅ Éxito Alto (+200k) |
| **8º** | 8º | **#05** `lYVMDblBX3Y` — *Midway 1942: los minutos que cambiaron la guerra del Pacífico* | **170,248** | **19.6 h** | **208,668/d** | 🚀 **Breakout Viral (<24h)** |
| **9º** | 9º | **#14** `VFppMLRXRqk` — *¿Por qué Marco Aurelio dejó Roma en manos de Cómodo?* | **161,559** | 88.5 h | 43,799/d | 📈 Rendimiento Medio-Alto |
| **10º** | 10º | **#15** `fGYdtXyKbtQ` — *Marco Aurelio y sus Meditaciones: el diario del emperador estoico* | **93,093** | 111.1 h | 20,108/d | ⚖️ Rendimiento Medio |
| **11º** | 11º | **#16** `3tSKNGKJOrc` — *Epicteto: el esclavo que inspiró a Marco Aurelio \| Estoicismo* | **92,214** | 111.6 h | 19,826/d | ⚖️ Rendimiento Medio |
| **12º** | 12º | **#07** `yeMKOTtYlWU` — *Stalingrado en 3 minutos: «Ni un paso atrás» \| SGM* | **71,565** | 25.4 h | 67,662/d | ⚖️ En crecimiento (>24h) |
| **13º** | 13º | **#11** `V3ase69Rap8` — *Napoleón: cuándo actuar y cuándo esperar \| De Austerlitz a Waterloo* | **65,181** | 63.3 h | 24,725/d | 📉 Medio-Bajo (Estancado) |
| **14º** | 14º | **#06** `KCrSmZt-A0w` — *Dunkerque 1940: ¿por qué Hitler frenó los tanques? \| SGM* | **64,786** | 22.0 h | 70,706/d | ⚖️ En crecimiento (<24h) |
| **15º** | 15º | **#03** `Dn8s4cqsNCQ` — *Hiroshima 1945: ¿era necesaria la bomba atómica? \| SGM* | **58,214** *(55,735)* | 15.6 h | 89,432/d | 🔥 Alta tracción (<16h) |
| **16º (Bottom 3)** | 16º | **#08** `VKEIpXxGMVk` — *Cândido Godói: el pueblo de los gemelos y la teoría sobre Mengele* | **28,297** | 28.4 h | 23,881/d | ⚠️ **BOTTOM 3 MADURO** |
| **17º (Bottom 2)** | 17º | **#10** `g_M7r8EMoFg` — *El caballo de Troya: el engaño que abrió las puertas de una ciudad* | **18,048** | 48.6 h | **8,911/d** | ❌ **BOTTOM 2 MADURO** |
| **18º (Bottom 1)** | 18º | **#04** `4VT2qvIRUkg` — *Iwo Jima 1945: la historia detrás de la foto y la segunda bandera* | **17,171** | 17.0 h | 24,226/d | ❌ **BOTTOM 1 CONSOLIDADO (>15h)** |
| — | 19º | **#02** `t89RDX8qolU` — *Pearl Harbor 1941: la alerta del radar que fue ignorada* | **6,092** | **2.76 h** | *52,952/d* | 🕒 *Recencia extrema (~3h)* |
| — | 20º | **#01** `UsMkfLhccJM` — *Enigma: Alan Turing y el equipo que descifró el código nazi* | **2,540** | **1.14 h** | *53,378/d* | 🕒 *Recencia extrema (~1h)* |

> [!IMPORTANT]
> **Concentración de Pareto en Vistas:** Los **Top 4 vídeos** (`#18`, `#20`, `#12` y `#17`, el 20% de la muestra) suman **`1,381,093` vistas (`48.1%` del tráfico total del canal en el período)**, mientras que el **Bottom 3 consolidado** (`#04`, `#10` y `#08`) suma apenas **`63,516` vistas (`2.2%` del total)**. Un vídeo del Top 3 (`363,332` vistas de media) multiplica por **`17.2x`** el alcance medio del Bottom 3 (`21,172` vistas).

---

### 2.2. Ranking 2: Por Engagement Rate `(Likes + Comentarios) / Vistas` y Ley de Compresión de Alcance Frío

| Pos. | Vídeo | Engagement Rate | Like Rate | Vistas | Fase de Distribución Algorítmica |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1º** | **#02** `t89RDX8qolU` (*Pearl Harbor*, `2.8h`) | **10.52%** | 10.32% | 6,092 | Fase 1: Audiencia nuclear / suscriptores (<6h) |
| **2º** | **#01** `UsMkfLhccJM` (*Enigma/Turing*, `1.1h`) | **8.82%** | 8.78% | 2,540 | Fase 1: Audiencia nuclear / suscriptores (<6h) |
| **3º** | **#04** `4VT2qvIRUkg` (*Iwo Jima*, `17.0h`) | **8.82%** | 8.75% | 17,171 | Fase 2: Nicho fiel sin expansión a tráfico frío (<30k) |
| **4º** | **#11** `V3ase69Rap8` (*Napoleón*, `63.3h`) | **8.73%** | 8.70% | 65,181 | Fase 2b: Aprobación filosófica alta, techo medio (<70k) |
| **5º** | **#08** `VKEIpXxGMVk` (*Cândido Godói*, `28.4h`) | **7.23%** | 7.19% | 28,297 | Fase 2: Nicho fiel sin expansión a tráfico frío (<30k) |
| **6º** | **#03** `Dn8s4cqsNCQ` (*Hiroshima*, `15.6h`) | **6.77%** *(7.07%)* | 6.23% | 58,214 | Fase 3: Expansión activa con alta controversia |
| **7º** | **#12** `GZNpPvHITiM` (*Marco Aurelio 12 años*, `64.3h`) | **6.60%** *(6.65%)* | 6.58% | **299,497** | 🌟 **Outlier Masivo (+300k vistas sin perder ER)** |
| **8º** | **#10** `g_M7r8EMoFg` (*Caballo de Troya*, `48.6h`) | **6.44%** | 6.38% | 18,048 | Fase 2: Nicho fiel sin expansión a tráfico frío (<30k) |
| **9º** | **#16** `3tSKNGKJOrc` (*Epicteto*, `111.6h`) | **5.84%** | 5.83% | 92,214 | Fase 3: Audiencia filosófica tibia (~90k) |
| **10º** | **#07** `yeMKOTtYlWU` (*Stalingrado*, `25.4h`) | **5.55%** | 5.43% | 71,565 | Fase 3: Audiencia bélica media (~70k) |
| **11º** | **#15** `fGYdtXyKbtQ` (*Meditaciones*, `111.1h`) | **5.37%** | 5.35% | 93,093 | Fase 3: Audiencia filosófica tibia (~90k) |
| **12º** | **#06** `KCrSmZt-A0w` (*Dunkerque*, `22.0h`) | **5.00%** | 4.89% | 64,786 | Fase 3: Audiencia bélica media (~65k) |
| **13º** | **#05** `lYVMDblBX3Y` (*Midway*, `19.6h`) | **4.67%** | 4.62% | 170,248 | Fase 4: Expansión masiva en feed frío (>150k) |
| **14º** | **#09** `UjI03Si4VA8` (*Primera Guerra Mundial*, `46.0h`) | **4.55%** | 4.50% | 205,332 | Fase 4: Expansión masiva en feed frío (>200k) |
| **15º** | **#13** `ff2r8EirvVI` (*Hernán Cortés*, `87.0h`) | **4.54%** | 4.38% | 223,683 | Fase 4: Expansión masiva en feed frío (>200k) |
| **16º** | **#18** `Km3mMU1pOpM` (*Truman vs MacArthur*, `114.4h`) | **4.34%** | 4.20% | **457,751** | Fase 5: Saturación de alcance generalista (>450k) |
| **17º** | **#19** `OmO_msj8Wy8` (*Inchon Ep. 4*, `114.5h`) | **4.06%** | 4.01% | 204,776 | Fase 4: Expansión masiva en feed frío (>200k) |
| **18º** | **#17** `kOpUJPR9BOM` (*Dien Bien Phu*, `114.0h`) | **3.88%** | 3.80% | 291,098 | Fase 5: Saturación de alcance generalista (~300k) |
| **19º** | **#14** `VFppMLRXRqk` (*Marco Aurelio y Cómodo*, `88.5h`) | **3.81%** | 3.80% | 161,559 | Fase 4: Expansión masiva en feed frío (>150k) |
| **20º** | **#20** `RT6my9-VxFI` (*Puente aéreo Berlín*, `114.9h`) | **3.52%** | 3.47% | **332,747** | Fase 5: Saturación de alcance generalista (>300k) |

#### Explicación de la Ley de Compresión de Engagement por Expansión de Alcance Frío:
En YouTube Shorts, **el *Like Rate* guarda una correlación inversa con el volumen de vistas (`r = -0.68` en la muestra)** debido al embudo de audiencias:
1. **De `0` a `30k` vistas (Tráfico Caliente / Semilla):** El Short se muestra a suscriptores y espectadores recurrentes del canal. El *Engagement Rate* se sitúa entre **`6.44%` y `10.52%`** (media: **`8.37%`** en los 5 vídeos `<30k`). Un ER alto con pocas vistas (`#04 Iwo Jima` `8.82%` con `17k` o `#08 Cândido Godói` `7.23%` con `28k`) **no significa éxito**, sino que el vídeo gustó al nicho fiel pero falló en el *Viewed vs. Swiped Away* o en la retención cuando YouTube intentó probarlo fuera del círculo cercano.
2. **De `50k` a `100k` vistas (Tráfico Tibio de Nicho):** El algoritmo amplía a aficionados a la historia y filosofía. El ER se estabiliza entre **`5.00%` y `8.73%`** (media: **`6.21%`**).
3. **Más de `150k` vistas (Alcance Frío Masivo):** Cuando el vídeo rompe la barrera de las `150,000–450,000` vistas (`#18`, `#20`, `#17`, `#13`, `#09`, `#19`, `#05`, `#14`), entra en el feed generalista de usuarios pasivos que consumen el vídeo entero (alta retención) pero dan *like* con menor frecuencia, comprimiendo el ER al rango del **`3.52% – 4.67%`** (media de los vídeos `+150k` excepto `#12`: **`4.17%`**).
4. **La Divergencia entre *Likes* y *Comentarios*:** Mientras el `% de Likes` cae con el tráfico frío, **el ratio de comentarios (`Comment Rate ‰`) se dispara positivamente cuando el vídeo masivo contiene un dilema político, moral o identitario**: `#18` (*Truman/MacArthur*, `457.8k` vistas) logra `1.47‰` (`671` comentarios) y `#13` (*Hernán Cortés*, `223.7k` vistas) logra `1.61‰` (`359` comentarios), frente a solo `0.17‰` en `#14` (*Cómodo*, `161.6k` vistas).
5. **El Caso Excepcional de `#12` (*Marco Aurelio a los 12 años*):** Es el único Short que desafía la compresión algorítmica: con **`299,497` (`301,299`) vistas**, sostiene un **`6.60%` (`6.65%`) de Engagement Rate (`19,838` likes)** porque la enseñanza estoica de austeridad voluntaria despierta un impulso de **guardado y validación identitaria ("dar like como declaración de principios")** incluso en audiencias frías.

---

### 2.3. Ranking 3: Por Controversia / Ratio de Comentarios por cada 1.000 Vistas (`‰`)

| Pos. | Vídeo | Comment Rate (`Com / 1k V`) | Comentarios Totales | Vistas | Ratio `Likes : 1 Com.` | Motor Principal de Controversia / Debate en Comentarios |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1º** | **#03** `Dn8s4cqsNCQ` — *Hiroshima 1945: ¿era necesaria la bomba atómica?* | **5.58‰** *(5.34‰)* | **311** | 58,214 *(55,735)* | **11.7 : 1** | **Debate moral y geopolítico extremo:** Crimen de guerra vs ahorro de vidas en invasión (*Downfall*) vs entrada de la URSS en Manchuria. |
| **2º** | **#02** `t89RDX8qolU` — *Pearl Harbor 1941: la alerta del radar ignorada* | **1.97‰** | 12 | 6,092 | 52.4 : 1 | **Teoría de conspiración / "Falsa bandera":** Debate sobre si Roosevelt dejó ocurrir el ataque como pretexto tras cortar el petróleo. |
| **3º** | **#13** `ff2r8EirvVI` — *Hernán Cortés no quemó sus naves* | **1.61‰** | **359** | 223,683 | **27.3 : 1** | **Fricción identitaria + corrección histórica:** Rol de los aliados indígenas ("la conquista la hicieron los indígenas") y corrección sobre el apodo *Malinche*. |
| **4º** | **#18** `Km3mMU1pOpM` — *¿Por qué Truman destituyó a MacArthur?* | **1.47‰** | **671** | 457,751 | **28.6 : 1** | **Subordinación militar vs Guerra Total:** Impacto por las "34 bombas atómicas" pedidas por MacArthur y debate sobre cadena de mando democrática. |
| **5º** | **#07** `yeMKOTtYlWU` — *Stalingrado en 3 minutos: «Ni un paso atrás»* | **1.22‰** | 87 | 71,565 | 44.7 : 1 | **Debate táctico de sillón ("armchair generals"):** ¿Debió Paulus romper el cerco en noviembre o resistir para cubrir la retirada del Cáucaso? |
| **6º** | **#06** `KCrSmZt-A0w` — *Dunkerque 1940: ¿por qué Hitler frenó los tanques?* | **1.16‰** | 75 | 64,786 | 42.2 : 1 | **Debate multicausal histórico:** Promesa de Göring vs agotamiento de blindados vs teoría de que Hitler buscaba una paz negociada con Inglaterra. |
| **7º** | **#17** `kOpUJPR9BOM` — *Dien Bien Phu: la trampa que derrotó a Francia* | **0.83‰** | **241** | 291,098 | 46.0 : 1 | **Anticolonialismo + paralelismo con San Martín:** Admiración por la hazaña de Giap subiendo cañones desarmados y crítica al colonialismo francés/EE.UU. |
| **8º** | **#12** `GZNpPvHITiM` — *¿Por qué Marco Aurelio dormía en el suelo a los 12 años?* | **0.69‰** | **206** | 299,497 | 96.3 : 1 | **Catarsis personal y crítica política actual:** Testimonios de vida austera en el campo y contraste entre Marco Aurelio subastando joyas vs políticos actuales. |
| **9º** | **#04** `4VT2qvIRUkg` — *Iwo Jima 1945: la historia detrás de la foto* | **0.64‰** | 11 | 17,171 | 136.6 : 1 | **Guerra cultural de símbolos:** Comentarios discutiendo que la foto más famosa de la SGM no es Iwo Jima sino la bandera soviética sobre el Reichstag. |
| **10º** | **#10** `g_M7r8EMoFg` — *El caballo de Troya: el engaño que abrió las puertas* | **0.61‰** | 11 | 18,048 | 104.7 : 1 | **Metáforas políticas contemporáneas:** Analogías con política argentina/latinoamericana y aclaraciones literarias (Ilíada vs Eneida). |
| **11º** | **#09** `UjI03Si4VA8` — *Primera Guerra Mundial en 3 minutos* | **0.51‰** | 105 | 205,332 | 88.0 : 1 | **Determinismo vs azar:** ¿Fueron las dos balas de Gavrilo Princip o el polvorín imperial europeo que iba a estallar igual? |
| **12º** | **#19** `OmO_msj8Wy8` — *Inchon: la apuesta de MacArthur contra la marea \| Ep. 4* | **0.51‰** | 105 | 204,776 | 78.2 : 1 | **Elogio a la audacia táctica:** Comparaciones con Aníbal en los Alpes y mención al teniente hispano Baldomero López. |
| **13º** | **#20** `RT6my9-VxFI` — *Puente aéreo de Berlín: vencieron el bloqueo* | **0.49‰** | 162 | 332,747 | 71.3 : 1 | **Guerra Fría e ideología:** Elogio a la logística de EE.UU., crítica al bloqueo soviético y rescate del canciller argentino Juan Atilio Bramuglia (`119 likes`). |
| **14º** | **#05** `lYVMDblBX3Y` — *Midway 1942: los minutos que cambiaron la guerra* | **0.48‰** | 82 | 170,248 | 95.9 : 1 | **Debate táctico naval:** Análisis del dilema de Nagumo (bombas vs torpedos) y capacidad industrial EE.UU. vs Japón. |
| **15º** | **#01** `UsMkfLhccJM` — *Enigma: Alan Turing y el equipo...* | **0.39‰** | 1 | 2,540 | 223.0 : 1 | *En fase inicial (<1.2h de vida).* |
| **16º** | **#08** `VKEIpXxGMVk` — *Cândido Godói: el pueblo de los gemelos* | **0.35‰** | 10 | 28,297 | 203.5 : 1 | **Consumo pasivo de curiosidad:** Anécdotas familiares sobre mellizos; la desmitificación científica cierra el debate en vez de abrirlo. |
| **17º** | **#11** `V3ase69Rap8` — *Napoleón: cuándo actuar y cuándo esperar* | **0.31‰** | 20 | 65,181 | 283.5 : 1 | **Referencias pop y quejas visuales:** Menciones a la canción del Cuarteto de Nos y críticas a las animaciones rotas/Minecraft. |
| **18º** | **#15** `fGYdtXyKbtQ` — *Marco Aurelio y sus Meditaciones* | **0.19‰** | 18 | 93,093 | 276.7 : 1 | **Aprobación silenciosa:** Citas del libro; sin conflicto ni dilema polarizante que invite a discutir. |
| **19º** | **#16** `3tSKNGKJOrc` — *Epicteto: el esclavo que inspiró a Marco Aurelio* | **0.17‰** | 16 | 92,214 | **335.8 : 1** | **Aprobación silenciosa:** Admiración por la filosofía estoica; pregunta final introspectiva que la audiencia guarda para sí pero no comenta en público. |
| **20º** | **#14** `VFppMLRXRqk` — *¿Por qué Marco Aurelio dejó Roma en manos de Cómodo?* | **0.17‰** | 28 | 161,559 | 219.1 : 1 | **Pregunta de cierre filosófica abstracta:** Menor conversión a comentario de todo el lote maduro. |

---

## 3. Contraste Ganadores (Top 3 + `#17`) vs. Perdedores (Bottom 3 Maduros) Cruzando Variables de los Agentes 1–7

### 3.1. Tabla Comparativa Directa: Élite Viral vs. Estancados

| Dimensión Analizada | 🏆 **GANADORES (Top 3 + `#17` Cuasi-Top 3)**<br>`#18` (`457.8k`), `#20` (`332.7k`), `#12` (`299.5k`), `#17` (`291.1k`) | ❌ **PERDEDORES (Bottom 3 Consolidados `>15h`)**<br>`#04` (`17.2k`), `#10` (`18.0k`), `#08` (`28.3k`) | Diferencial / Brecha |
| :--- | :--- | :--- | :--- |
| **Media de Vistas** | **`363,332`** *(Top 3)* / **`345,273`** *(Top 4)* | **`21,172`** | **17.2x más vistas** (`+1,616%`) |
| **Media de Velocidad (`Vistas/Día`)** | **`92,415 / día`** *(Top 3)* / **`84,634 / día`** *(Top 4)* | **`19,006 / día`** | **4.9x más velocidad diaria** |
| **Media de Comentarios Totales** | **`346.3`** *(Top 3)* / **`320.0`** *(Top 4)* | **`10.7`** | **32.4x más comentarios** |
| **Comment Rate (`Com / 1k Vistas`)** | **`0.88‰`** *(Top 3)* / **`0.87‰`** *(Top 4)* | **`0.53‰`** | **+66% más densidad de debate** |
| **Tema y Época** | **Choque de líderes y decisiones contraintuitivas bajo presión extrema:** Guerra Fría temprana (`1948–1954`: `#18` Corea, `#20` Berlín, `#17` Indochina) y paradoja biográfica del emperador filósofo (`#12`). | **Micro-detalles periféricos o mitos archiconocidos:** Segunda bandera fotográfica (`#04`), leyenda escolar (`#10` Troya) o rumor pseudocientífico en un pueblo (`#08` Cândido Godói). | Foco en **Agencia Humana Decisiva** vs. **Curiosidad Estática**. |
| **Fórmula de Título** | **Pregunta paradójica `¿Por qué [Líder] [Acción extrema]?`** (`#18`, `#12`) o **Victoria/Derrota por inversión táctica** (`#20` *"vencieron sin disparar"*, `#17` *"la trampa que derrotó a Francia"*). Longitud concisa: **`56.5 caracteres`** (`10.5 palabras`). | **Etiqueta nominal + subtítulo explicativo plano (`[Tema]: la historia/el engaño/la teoría detrás de...`).** Sin verbo de decisión en la primera cláusula. Longitud pesada: **`65.3 caracteres`** (`12.7 palabras`). | **`-8.8 caracteres`** más cortos y directos en Ganadores. |
| **Estructura del Hook (`0–12s`)** | **Conflicto o Paradoja en los primeros `4.5s`:** Fecha exacta + choque de poder (`#18`, `#20`), inversión de trampa (`#17`) o estatus extremo vs renuncia (`#12`). | **Arranque descriptivo o hipotético lento:** *"Esta es la foto más famosa..."* (`#04`), *"¿Cómo pudo un regalo de madera..."* (`#10`), *"Imagina vivir en un pueblo..."* (`#08`). | Ganadores sitúan una **decisión humana crítica antes del segundo 10**. |
| **Velocidad de Habla (`WPM`)** | **`159.5 WPM`** *(Top 3)* / **`158.3 WPM`** *(Top 4)* — Rango contenido y articulado (`148.3` a `166.3 WPM`). | **`162.6 WPM`** (`158.8` a `167.0 WPM`). | Ganadores hablan **`3–4 WPM` más pausado** y claro. |
| **Ritmo Visual (`Cortes/10s >0.3`)** | **`1.61 cortes/10s`** (`ASL: 6.42s` en Top 3; `1.62 c/10s` en Top 4). Planos sostenidos con mapas animados y archivo limpio. | **`1.75 cortes/10s`** (`ASL: 5.63s`). | **Menos cortes bruscos = mayor retención narrativa** en este formato. |
| **Pausas Dramáticas (`<= -32dB`)** | **`72.7 pausas`** *(Top 3)* / **`70.8`** *(Top 4)* — Fluidez rítmica sin fragmentación excesiva. | **`79.0 pausas`** (`82` en `#04`, `81` en `#10`, `74` en `#08`). | Los perdedores tienen **`+8.3 pausas`** (locución más entrecortada). |

---

### 3.2. Desglose por Dimensión (Agentes 1–7)

#### A. Tema y Época: El filón de oro de la Guerra Fría Temprana (`1948–1954`) frente a la Saturación de SGM y Mitos Escolares
- **La hegemonía de la Guerra Fría Temprana / Descolonización (`1948–1954`):** Los **4 vídeos** de esta época (`#18` *Truman/MacArthur 1951*, `#20` *Berlín 1948*, `#17` *Dien Bien Phu 1954* y `#19` *Inchon 1950*) superan todos las `200,000` vistas, promediando **`321,593 vistas`**, muy por encima de la Segunda Guerra Mundial madura (`#05` *Midway* `170.2k`, `#07` *Stalingrado* `71.6k`, `#06` *Dunkerque* `64.8k`, `#03` *Hiroshima* `58.2k`, `#04` *Iwo Jima* `17.2k`; media `76,397` vistas). ¿Por qué? La SGM sufre mayor saturación de oferta en YouTube Shorts en español, mientras que **Corea, Berlín 1948 e Indochina 1954 son conflictos de altísima tensión nuclear/estratégica pero mucho menos trillados**, donde la audiencia siente que está descubriendo episodios decisivos que no le enseñaron en la escuela.
- **Líderes en encrucijadas reales vs. Relatos periféricos:** El canal se llama *CM | Historia y Decisiones*. Cuando el vídeo cumple literalmente esa promesa mostrando a un **comandante o gobernante tomando una decisión contraintuitiva de alto riesgo** (Truman despidiendo a MacArthur a la 1 AM, Tunner organizando 1,383 vuelos diarios a Berlín, Giap subiendo artillería desarmada en bicicletas, Cortés hundiendo sus naves, Marco Aurelio subastando las joyas imperiales), las vistas explotan (`223k` a `457k`). Cuando se desvía hacia un **mito literario archiconocido** (`#10 Caballo de Troya`, `18k`), un **rumor pseudocientífico ya desmentido** (`#08 Cândido Godói`, `28k`, donde no hay ninguna decisión estratégica) o el **backstage de una fotografía** (`#04 Iwo Jima`, `17k`), el algoritmo no encuentra tracción masiva.

#### B. Fórmula de Título y Hook: La Paradoja de Autoridad frente al Etiquetado Descriptivo
- **Títulos Ganadores (`¿Por qué [Sujeto de Máximo Poder] [Acción Contraintuitiva]?`):**
  - Los dos vídeos con mayor techo de *Likes* del canal (`#12` con `19,838 likes` y `#18` con `19,219 likes`) usan exactamente la misma plantilla sintáctica de 56 caracteres:
    - `#18`: `¿Por qué Truman destituyó a MacArthur? | Guerra de Corea` (`457,751` vistas)
    - `#12`: `¿Por qué Marco Aurelio dormía en el suelo a los 12 años?` (`299,497` vistas)
  - Esta estructura abre una **brecha de curiosidad cognitiva inmediata (*Information Gap*)**: el espectador conoce el estatus del protagonista (el Presidente / el Emperador) y choca contra una acción aparentemente ilógica (echar a su mejor general en plena guerra / dormir en el piso siendo rico).
- **Hooks Ganadores vs. Perdedores (`0–12s`):**
  - Los ganadores abren con **coordenada temporal + dilema de suma cero o inversión irónica**:
    - `#18`: *"Abril de 1951. En plena guerra, el presidente Truman echa al general más famoso de Estados Unidos. Lo anuncia a la 1 de la mañana y medio país se le pone en contra."*
    - `#20`: *"Junio de 1948. Stalin corta todos los caminos a Berlín Occidental... Los aliados tenían dos opciones: rendirse o ir a la guerra. Eligieron una tercera."*
    - `#17`: *"Noviembre de 1953. Francia tira miles de paracaidistas al fondo de un valle... Era una trampa para el enemigo. Terminó siendo la trampa de Francia."*
  - En cambio, `#08` (*Cândido Godói*, `28.3k`) abre con una invitación imaginativa lenta (*"Imagina vivir en un pueblo donde en algunas calles..."*) y un `[carraspeo]` audible en el segundo `00:16`; `#04` (*Iwo Jima*, `17.2k`) promete desmontar "tres medias verdades" sobre una foto (bajo riesgo dramático); y `#10` (*Troya*, `18.0k`) resume en los primeros 10 segundos lo que todo el mundo ya sabe (*"los troyanos lo metieron ellos mismos"*), eliminando el motivo para quedarse hasta el final.

#### C. Ritmo de Edición (`Cortes/10s`), Velocidad de Habla (`WPM`) y Pausas
- **La paradoja del montaje en divulgación histórica:** Contra el cliché de que "más cortes por segundo = más vistas en Shorts", los datos de `@cdmauro2010` demuestran que **el punto óptimo de edición visual está en el rango moderado de `1.05 a 2.00 cortes fuertes/10s` (`ASL de 4.8s a 8.9s`)**:
  - El Top 3 (`#18`, `#20`, `#12`) promedia **`1.61 cortes/10s`** (`2.00`, `1.78` y `1.06` respectivamente).
  - La sobre-edición extrema como en `#07` (*Stalingrado*, `2.83 cortes fuertes/10s` y `6.78 cortes totales/10s` por parpadeos de archivo) no genera viralidad extra (`71.6k` vistas), mientras que la infra-edición extrema como en `#11` (*Napoleón*, `0.89 cortes/10s` con un bloque de `60s` sin un solo corte entre `01:20` y `02:20`) estanca el alcance en `65.2k` vistas y genera quejas explícitas en comentarios sobre las animaciones.
- **El peligro de superar los `170 WPM`:** Los 4 vídeos donde la locución se acelera por encima de `169 WPM` (`#14 Cómodo` `180.0 WPM`, `#16 Epicteto` `175.3 WPM`, `#15 Meditaciones` `171.2 WPM` y `#11 Napoleón` `169.3 WPM`) promedian **`103,012` vistas**, mientras que los vídeos maduros en la banda de respiración natural de **`148 a 166.5 WPM`** (`#18`, `#20`, `#12`, `#17`, `#13`, `#09`, `#19`, `#05`) promedian **`272,641` vistas (`2.65x` más)**. De hecho, en los comentarios de `#09` ya aparecen ruegos directos de espectadores: *"Por favor, podrías ir más despacio en tu relato? Es muy interesante, pero no lo puedo asimilar bien con tal velocidad"*.

---

### 3.3. Efecto Fatiga de Serie y Canibalización por Ráfagas de Publicación

El análisis cruzado de marcas de tiempo (`UTC`) y temáticas revela **dos fenómenos críticos de desgaste de serie y canibalización algorítmica**:

#### 1. Desgaste Temático en la Miniserie de Marco Aurelio / Estoicismo (`4 vídeos`)
Al comparar el rendimiento de las 4 entregas dedicadas a Marco Aurelio y el estoicismo romano, se observa una **asimetría radical entre el vídeo de gancho concreto/paradójico y las entregas de desarrollo o contexto filosófico**:
- **Entrega Líder (`#12` *¿Por qué Marco Aurelio dormía en el suelo a los 12 años?*):** **`299,497` (`301,299`) vistas** | `19,838` likes (`6.65%` ER) | `111,711 vistas/día`.
- **Entrega de Sucesión (`#14` *¿Por qué Marco Aurelio dejó Roma en manos de Cómodo?*):** **`161,559` vistas (`-46.1%` respecto a `#12`)** | `6,134` likes (`3.81%` ER) | `43,799 vistas/día`.
- **Entrega de Obra (`#15` *Marco Aurelio y sus Meditaciones: el diario del emperador estoico*):** **`93,093` vistas (`-68.9%` respecto a `#12`)** | `4,981` likes (`5.37%` ER) | `20,108 vistas/día`.
- **Entrega de Predecesor (`#16` *Epicteto: el esclavo que inspiró a Marco Aurelio | Estoicismo*):** **`92,214` vistas (`-69.2%` respecto a `#12`)** | `5,372` likes (`5.84%` ER) | `19,826 vistas/día`.

> **Diagnóstico de la Serie Estoica:** Además, `#16` (*Epicteto*, `00:52 UTC`) y `#15` (*Meditaciones*, `01:23 UTC`) se publicaron **con apenas 31 minutos de diferencia** la misma noche del `2026-10-23`, dividiendo exactamente por la mitad la tracción del nicho estoico (`92.2k` y `93.1k` vistas, con idénticos `16` y `18` comentarios). Cuando el canal espació las entregas a **1 vídeo cada 24 horas** (`#14` a las `23:58 UTC` del día 23 y `#12` a las `00:09 UTC` del día 25) y cambió el título descriptivo por una pregunta `¿Por qué Marco Aurelio...?`, las vistas se multiplicaron por **`3.25x`** (de `92.6k` a `301.3k`).

#### 2. Canibalización por Ráfagas Intra-Día y Penalización del Tag `| Ep. X`
El canal tiende a subir bloques de 2 a 5 Shorts el mismo día con pocos minutos u horas de separación:
- **Ráfaga Jueves 22 Oct (`4 vídeos en 53 minutos`, `21:37` a `22:30 UTC`):**
  - `21:37 UTC`: `#20` (*Puente aéreo de Berlín*) → `332,747` vistas.
  - `21:58 UTC` (`+21 min`): `#19` (*Inchon: la apuesta de MacArthur contra la marea | Ep. 4*) → Cae un **`-38.5%`** respecto a `#20` (`204,776` vistas) y un **`-55.3%`** respecto a `#18` (`457,751` vistas, subido solo **7 minutos después** a las `22:05 UTC`). Incluir explícitamente **`| Ep. 4`** en el título de `#19` penalizó su CTR/retención inicial frente a `#18`, que abordaba al mismo general MacArthur pero como historia autoconclusiva sin numeración de episodio.
- **Ráfaga Lunes 26 Oct (`5 vídeos en 12 horas`, `12:03` a `00:52 UTC`):**
  - Publicar 5 vídeos de la Segunda Guerra Mundial en el mismo ciclo diario provocó que, tras el despegue explosivo de `#05` (*Midway*, `20:55 UTC`, `170,248` vistas), el vídeo siguiente subido apenas `2h 34m` después (`#04` *Iwo Jima*, `23:29 UTC`) quedara completamente eclipsado en **`17,171` vistas (`-89.9%`)**.

---

## 4. Formulación de 6 Hipótesis Cuantitativas, Claras y Comprobables

A partir del cruce estadístico de la muestra (`N = 20` totales; `N = 18` consolidados `>15h`; `N = 14` maduros `>24h`), se formulan las siguientes **6 hipótesis cuantitativas verificables**:

1. **Hipótesis 1 (Estructura de Título Interrogativo-Paradójico):**
   *"Los Shorts con títulos estructurados como pregunta causal sobre la decisión de un líder (`¿Por qué [Líder] [Acción paradójica]?` o `¿Cómo...?`) obtienen un **`74.2%` más de Vistas (`1.74x`)** y **`2.19 veces más Likes`** que aquellos con títulos enunciativos o descriptivos (`[Tema]: la historia detrás de...`) (Evidencia: media en vídeos maduros `>24h` de **`285,627 vistas` y `13,798 likes`** en títulos con pregunta `¿Por qué...?` [`#18`, `#12`, `#14`] frente a **`163,991 vistas` y `6,294 likes`** en los 11 vídeos maduros con título declarativo)."*

2. **Hipótesis 2 (Selección de Época y Océano Azul Temático):**
   *"Los Shorts ambientados en la **Guerra Fría Temprana y Descolonización (`1948–1954`)** obtienen **`2.85 veces más Vistas (`+185.0%`)`** que aquellos ambientados en otros períodos históricos dentro de la cohorte consolidada (`>15h`) (Evidencia: media de **`321,593 vistas`** en los 4 vídeos de `1948–1954` [`#18` Corea `457.8k`, `#20` Berlín `332.7k`, `#17` Vietnam `291.1k`, `#19` Inchon `204.8k`] frente a **`112,824 vistas`** de media en los otros 14 vídeos consolidados de SGM, Antigüedad, Conquista y Siglo XIX)."*

3. **Hipótesis 3 (Encuadre Temático: Decisión Estratégica de Líder vs. Mito/Curiosidad Periférica):**
   *"Los Shorts centrados en **decisiones estratégicas o dilemas de mando bajo presión** obtienen **`9.78 veces más Vistas (`+878.0%`)`** y **`4.34 veces más velocidad diaria`** que aquellos centrados en mitos literarios, misterios pseudocientíficos o curiosidades fotográficas (Evidencia: media de **`207,068 vistas` y `82,514 vistas/día`** en los 15 vídeos consolidados de decisiones estratégicas/filosóficas frente a **`21,172 vistas` y `19,006 vistas/día`** en los 3 vídeos periféricos [`#04` Iwo Jima foto `17.2k`, `#10` Caballo de Troya `18.0k`, `#08` Cândido Godói `28.3k`])."*

4. **Hipótesis 4 (Velocidad de Habla Óptima y Comprensión Cognitiva):**
   *"Los Shorts con una velocidad de locución moderada de **`148 a 166.5 WPM`** obtienen **`3.22 veces más Vistas (`+222.4%`)`** que aquellos cuya locución supera el umbral rápido de **`167 WPM`** (Evidencia: media en vídeos maduros `>24h` de **`260,305 vistas`** en los 9 vídeos con `<=166.5 WPM` [`#18`, `#20`, `#12`, `#17`, `#13`, `#09`, `#19`, `#07`, `#08`] frente a **`80,739 vistas`** de media en los 5 vídeos maduros con `>=167 WPM` [`#14` `180.0 WPM`, `#16` `175.3 WPM`, `#15` `171.2 WPM`, `#11` `169.3 WPM`, `#10` `167.0 WPM`])."*

5. **Hipótesis 5 (Polarización del Cierre y Tracción por Comentarios):**
   *"Los Shorts que cierran con un **dilema ético/estratégico binario sobre una acción controvertida** obtienen **`4.49 veces más tasa de comentarios (`Comment Rate ‰`)`** y un **`50.6%` más de Vistas** que aquellos que cierran con una pregunta introspectiva de autoayuda o curiosidad pasiva (Evidencia: media de **`1.75‰` comentarios/1k vistas y `216,127 vistas`** en los 8 vídeos consolidados con dilema estratégico/moral fuerte [`#03`, `#13`, `#18`, `#07`, `#06`, `#17`, `#09`, `#19`] frente a **`0.39‰` comentarios/1k vistas y `143,491 vistas`** en los 10 vídeos consolidados con cierre introspectivo o pasivo)."*

6. **Hipótesis 6 (Espaciamiento de Publicación vs. Saturación en Ráfaga):**
   *"Los Shorts publicados respetando una ventana de enfriamiento de **`>= 18 horas` respecto al vídeo anterior de la misma temática** o abriendo el bloque diario obtienen un **`84.7%` más de Vistas (`1.85x`)** que las entregas secundarias subidas en ráfagas de menos de 3 horas con etiquetas seriadas o solapamiento temático (Evidencia: media de **`258,412 vistas`** en los cabezas de bloque/espaciados [`#20` `332.7k`, `#13` `223.7k`, `#12` `299.5k`, `#09` `205.3k`] frente a **`139,886 vistas`** en los vídeos secundarios de ráfaga, con caídas extremas en `#16/#15` [`92.2k`/`93.1k` a 31 min de distancia], `#19 Ep. 4` [`204.8k` vs `457.8k` de `#18`] y `#04` [`17.2k` tras 4 vídeos previos en el mismo día])."*

---

## 5. Cinco Conclusiones Accionables de Inversión de Esfuerzo y Selección de Temas

1. **Redirigir el 70% de la Parrilla Editorial hacia "Dilemas de Mando en la Guerra Fría (`1947–1975`) y Paradojas de Líderes Antiguos", Eliminando Mitos y Curiosidades Periféricas:**
   - **Acción:** Priorizar episodios donde dos figuras de poder chocan por una decisión límite con riesgo de escalada global (ej. *Crisis de los Misiles de Cuba: ¿por qué Vasili Arkhipov se negó a disparar el torpedo nuclear?*, *¿Por qué Stalin no ayudó al levantamiento de Varsovia?*, *¿Por qué MacArthur cruzó el paralelo 38?*) o paradojas biográficas extremas de líderes antiguos (como `#12 Marco Aurelio`). Descartar por completo temas de mitología escolar (`#10 Troya`), misterios pseudocientíficos (`#08 Cândido Godói`) o historias de fotografías (`#04 Iwo Jima`), que hunden el promedio del canal a `<25k` vistas.

2. **Estandarizar la Plantilla de Título `¿Por qué [Líder] [Acción Contraintuitiva]?` (`< 60 caracteres`) y Prohibir Etiquetas Seriadas (`| Ep. X`):**
   - **Acción:** Todo Short debe abrir su título con una contradicción o decisión desconcertante en menos de 60 caracteres (los 4 mayores éxitos del canal tienen entre `55` y `57` caracteres). Eliminar etiquetas como `| Ep. 4` (que le costó a `#19 Inchon` más de `250,000` vistas frente a `#18`) y sustituir títulos enciclopédicos como `Stalingrado en 3 minutos` o `Marco Aurelio y sus Meditaciones` por el conflicto directo (*"¿Por qué la misma orden salvó a Stalin y destruyó a Hitler?"*).

3. **Fijar el "Sweet Spot" Técnico de Producción en `150–165 WPM` y `1.5–2.2 Cortes Fuertes/10s` (Reasignando Tiempo de Edición Frenética a Guion y Mapas):**
   - **Acción:** No invertir horas extra en hiper-fragmentar el vídeo con más de 45 cortes (`#07 Stalingrado` tuvo `51` cortes fuertes / `122` totales y se quedó en `71.6k` vistas, mientras `#20 Berlín` y `#17 Dien Bien Phu` superaron las `290k–330k` vistas con solo `29–32` cortes bien sincronizados y mapas claros). En cambio, controlar estrictamente que la locución **nunca supere los `165 WPM`** (evitar los `171–180 WPM` de `#14`, `#15` y `#16` que saturan al oyente) y limpiar en postproducción los `[carraspeos]` audibles detectados en `#08` (`00:16`) y `#19` (`00:27`).

4. **Diseñar "Bombas de Comentarios" (Datos Cuantitativos Shock + Pregunta de Juicio de Mando al Cierre):**
   - **Acción:** Incluir entre el minuto `00:45` y `01:30` un **dato numérico extremo o revelación contraintuitiva** (como las *"34 bombas atómicas"* de `#18`, el *"corte de petróleo"* en `#02`, o que Cortés *"no quemó las naves, las desarmó para hacer 13 bergantines"* en `#13`) y cerrar el vídeo preguntando al espectador **qué orden habría firmado él en el puesto de mando** (*"¿Vos habrías echado a un héroe?"*, *"¿Era necesaria o había otro camino?"*) en lugar de preguntas abstractas de autoayuda. Esto multiplica por `4.5x` la tasa de comentarios e impulsa el alcance algorítmico.

5. **Limitar la Frecuencia a Máximo 1–2 Shorts por Día (Separados por `>= 12–18 horas`) y Alternar Épocas para Evitar la Fatiga de Serie:**
   - **Acción:** Abandonar la práctica de subir ráfagas de 4 o 5 vídeos de la misma guerra o del mismo filósofo en una sola tarde/noche. Si se produce una miniserie de 4 episodios (como *Marco Aurelio* o *Guerra de Corea*), publicar primero el episodio con la paradoja más explosiva (`#12` o `#18`) y espaciar las entregas siguientes cada `48–72 horas`, intercalando entre ellas un conflicto bélico de otra época para no saturar ni dividir el presupuesto de impresiones del algoritmo.
