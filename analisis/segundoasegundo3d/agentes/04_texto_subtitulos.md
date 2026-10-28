# Agente 4 — Análisis de Subtítulos, Tipografía y Rótulos en Pantalla (`@SEGUNDOASEGUNDO3D`)

> **Muestra auditada:** Inspección píxel a píxel de los fotogramas `1080×1920` y mosaicos `hook_3s.jpg` / `storyboard.jpg` de los 14 Shorts del canal.

---

## 1. Especificación Técnica del Sistema de Subtítulos (`y ≈ 18%`)

`@SEGUNDOASEGUNDO3D` emplea el mismo motor tipográfico programático que `@cdmauro2010`, pero simplificado para no tapar las maquetas 3D:
- **Posición vertical fija:** Centrado horizontalmente (`x = 540 px`) en el **tercio superior (`y = 310 px a 410 px`, `16%–21%` de la altura)**.
- **Familia tipográfica:** Sans-serif geométrica humanista (**`Inter` / `Plus Jakarta Sans`**), sin bordes negros gruesos (*stroke* `0 px`), apoyada sobre una suave viñeta oscura superior.
- **Longitud de bloque:** **1 a 2 líneas cortas (`3 a 7 palabras` por pantalla, `18–32 caracteres por línea`)**.
- **Animación de Karaoke por Luminancia y Peso:**
  - **Palabras ya pronunciadas o por pronunciar:** Gris medio translúcido (`#8A8F98` / `rgba(255,255,255,0.52)`), peso `Medium (500)`.
  - **Palabra activa en el instante exacto (`word-level timestamp`):** Blanco puro (`#FFFFFF`), peso `Bold/ExtraBold (700/800)`.
- **La Firma Visual: El *Figma Bounding Box* Azul (`#3B82F6`):**
  - Entre **1 y 4 palabras clave por vídeo** (casi siempre en el Hook inicial y en la última palabra del Reframe o CTA) reciben un **rectángulo de selección vectorial azul (`#3B82F6`, trazo `2.5 px`, relleno `rgba(59, 130, 246, 0.18)`) con 4 pequeños cuadrados blancos (`6×6 px`) en los vértices**.

---

## 2. Inventario Completo de Palabras con *Figma Bounding Box* y Rótulos 3D por Vídeo (`n = 14`)

| # | ID | Palabras con *Figma Bounding Box* Azul (`#3B82F6`) | Rótulos Técnicos / Píldoras UI dentro del Escenario 3D | Erratas o Glifos Detectados |
|---|---|---|---|---|
| **#01** | [`ynXYhJh_r5w`](../videos/ynXYhJh_r5w.md) | `[cientos]`, `[elefantes.]`, `[aprieta]`, `[basura.]` | `Tolva · aquí caen las bolsas`, `Cilindro`, `CARGA · 12 toneladas` | Ninguno (100% limpio) |
| **#02** | [`Ol8w43RzqaY`](../videos/Ol8w43RzqaY.md) | `[enchufaron]`, `[curva]`, `[gravedad.]` | `la Estación`, `400 km`, `89% de la gravedad de aquí`, `15 amaneceres`, `1998 -> 2026`, `Amigo` | Falta tilde en título (`construyo`) |
| **#03** | [`tTCVPqueenY`](../videos/tTCVPqueenY.md) | `[bostezando?]`, `[pensarlo.]`, `[mitad]`, `[bosteza.]` | `55%`, `desconocido`, `4 años` | Falta tilde en título (`por que` / `como`) |
| **#04** | [`WwBo2hdDzDU`](../videos/WwBo2hdDzDU.md) | `[imán]`, `[suelta]` | `1,00` | Ninguno (100% limpio) |
| **#05** | [`x4X1EufVtaE`](../videos/x4X1EufVtaE.md) | `[alarma]`, `[estrés,]`, `[pesadilla]`, `[raros.]` | `amígdala`, `noradrenalina` | Glifo roto `am[X]gdala` por tilde en `00:16` |
| **#06** | [`leihGhuggM8`](../videos/leihGhuggM8.md) | `[compañía.]`, `[«SOS»:]`, `[satélite]` | `Sin servicio`, `Otra compañía`, `Tu compañía`, `911`, `SOS`, `Emergencia por satélite · Estoy perdido en la montaña · Conectado` | Ninguno (100% limpio) |
| **#07** | [`ZCKcLQIuV_A`](../videos/ZCKcLQIuV_A.md) | `[hipo.]` | *Ninguno (solo animación 3D)* | Ninguno (100% limpio) |
| **#08** | [`4AXXLcYt_90`](../videos/4AXXLcYt_90.md) | `[prestas]`, `[errores.]` | `+100 por segundo`, `hola` | Ninguno (100% limpio) |
| **#09** | [`BciMJC4VRc4`](../videos/BciMJC4VRc4.md) | `[receta,]` | `FUNERARIA`, `1L`, `Amigo · Llamada perdida` | Ninguno (100% limpio) |
| **#10** | [`D79tEmKLu2g`](../videos/D79tEmKLu2g.md) | `[humo?]`, `[pelitos]`, `[otra]`, `[aire]` | `monóxido de carbono` | Ninguno (100% limpio) |
| **#11** | [`W2a8M6tbELI`](../videos/W2a8M6tbELI.md) | *Ninguno en frames muestreados* | `Central · donde se fabrica`, `Tu casa · donde se usa`, `Se fabrica · las centrales`, `Se gasta · todos nosotros`, `CORRIENTE · 17 A`, `CARGA DE CADA CENTRAL · 78% · 0%`, `PORTUGAL · ESPAÑA · FRANCIA · 28 DE ABRIL DE 2025 · 12:33 h`, `Tu amigo`, `@segundoasegundo3d · cómo funcionan las cosas · ✓Siguiendo` | Ninguno (100% limpio) |
| **#12** | [`vIEqG2MXFt0`](../videos/vIEqG2MXFt0.md) | `[defensas,]`, `[peor.]` | *Ninguno (solo animación 3D)* | Ninguno (100% limpio) |
| **#13** | [`wk318fyD6Aw`](../videos/wk318fyD6Aw.md) | *Ninguno en frames muestreados* | `Inicio`, `OÍDO · Te mueves`, `ALERTA DEL CEREBRO · Veneno detectado`, `SOSPECHOSO · El carro`, ` SÍGUEME EN · @segundoasegundo3d · ✓Siguiendo` | Falta tilde en título (`por que` / `como`) |
| **#14** | [`tinDzJnTiik`](../videos/tinDzJnTiik.md) | `[basura]` | `Tu amigo`, `@segundoasegundo3d · cómo funcionan las cosas · ✓Siguiendo` | Falta tilde en título (`por que` / `como`) |

---

## 3. Diferencia Clave frente a `@cdmauro2010`: Ausencia de Titular Central `ALL CAPS`

- En `@cdmauro2010` (Historia), debajo del subtítulo (`y = 32%`) había siempre un gran titular de sección en `ALL CAPS ExtraBold` (`EL PUNTO DÉBIL`, `OPERACIÓN OVERLORD`).
- En `@SEGUNDOASEGUNDO3D` (Cultura General 3D), **se elimina por completo ese titular `ALL CAPS` intermedio** para dejar libre el `75%` central de la pantalla a la maqueta 3D. En su lugar, utiliza **dos tipos de micro-etiquetas integradas en el objeto**:
  1. **Etiquetas de Puntero (*Callout Lines*):** Línea fina con un nodo circular en el extremo que señala una pieza exacta de la máquina (`Tolva · aquí caen las bolsas`, `Cilindro`, `Empujas · aquí` en `#01`; `Central · donde se fabrica` y `Tu casa · donde se usa` en `#11`).
  2. **Tarjetas de Estado tipo App/Widget iOS (`UI Cards`):** Tarjetas blancas redondeadas (`border-radius: 16px`) con indicador de color semántico (`• OÍDO: Te mueves` en azul, `• ALERTA DEL CEREBRO: Veneno detectado` en rojo, `• SOSPECHOSO: El carro` en ámbar en `#13`; `CARGA: 12 toneladas` en `#01`; `CORRIENTE: 17 A` en `#11`).

---

## 4. Auditoría de Control de Calidad Tipográfico (Errores a Evitar)

1. **Bug de fuente sin soporte de tildes en etiquetas 3D (`#05 x4X1EufVtaE`):** En el segundo `[00:16]` del vídeo de las pesadillas, la etiqueta flotante bajo el cerebro intenta renderizar `amígdala`, pero la fuente secundaria usada en ese componente no tenía el glifo `í` y renderizó el carácter de reemplazo **`am[☒]gdala`**.
2. **Descuidos ortográficos en los títulos de YouTube:** En 4 de los 14 títulos publicados faltan tildes en pronombres interrogativos o verbos pasados (`construyo` en `#02`, `por que` en `#03`, `Por qué` sin `¿` de apertura en `#13`, `como` sin tilde en `#14`), mientras que **dentro del vídeo los subtítulos tienen una ortografía y puntuación impecables (con signos `¿ ?`, `« »` y dos puntos `:` perfectos)**.

---

## 5. Conclusiones Accionables del Agente 4
1. **Mantener el subtítulo en `y ≈ 18%` sin titular `ALL CAPS` debajo cuando el protagonista es una maqueta 3D/2.5D:** Así el modelo tridimensional respira a pantalla completa.
2. **Usar Etiquetas de Puntero (*Callouts* con línea y punto) y Tarjetas Widget estilo iOS:** Son mucho más limpias y modernas para explicar máquinas o anatomía que poner texto suelto encima del dibujo.
3. **Verificar siempre el soporte UTF-8 (`á, é, í, ó, ú, ñ, ¿, «, »`) en todas las fuentes de canvas/3D** para evitar glifos rotos como `am[☒]gdala`.