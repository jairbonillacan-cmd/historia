# Especificación de guiones — Shorts de historia (formato ElevenLabs v4)

Documento de referencia **obligatorio** para escribir cualquier guion de la parrilla
([`parrilla/parrilla.csv`](parrilla.csv)). Basado en el análisis de `@cdmauro2010`
([`analisis/cdmauro2010/10_kit_produccion.md`](../analisis/cdmauro2010/10_kit_produccion.md)).
Guion modelo: [`guiones/2026-10-28/S5_crisis-de-los-misiles-el-trato-secreto-que-evito-la-guerra-n.md`](../guiones/2026-10-28/S5_crisis-de-los-misiles-el-trato-secreto-que-evito-la-guerra-n.md).
Validador: `python parrilla/validar_guiones.py --franja Sx --desde AAAA-MM-DD --hasta AAAA-MM-DD --solo-validar`.

---

## 1. Formato del vídeo

- **Duración:** 177–180 s. Vertical 1080×1920, 60 fps.
- **Locución:** **460–500 palabras** (sin contar las etiquetas de audio) ≈ 160 palabras por minuto.
- **Estructura en 5 bloques** (la voz entra en 00:02.5; los primeros 2,5 s son solo sonido ambiente + rótulo):

| Bloque | Tiempo | Palabras | Función |
|---|---|---|---|
| 1. Gancho | 00:02.5–00:15 | 32–38 | Anclaje «[Mes] de [año]» o paradoja/cifra imposible. Abre la incógnita sin resolverla. Termina en `[long pause]`. |
| 2. Contexto | 00:15–00:58 | 110–120 | Lugar, fecha, quién es quién, qué está en juego. Micro-conflicto #1. |
| 3. Desarrollo | 00:58–01:57 | 155–165 | 3 obstáculos encadenados («Pero había un problema», «Peor aún», «Nadie esperaba que…»). |
| 4. Giro / clímax | 01:57–02:44 | 120–130 | El momento exacto de la decisión (hora, minuto, cifra) y sus consecuencias. Debate historiográfico si lo hay. |
| 5. Cierre + pregunta | 02:44–03:00 | 38–45 | Frase que conecta con el gancho + **dilema binario en voseo** + «Contámelo en los comentarios». |

## 2. Estilo de redacción

- **Voseo rioplatense natural**: «imaginá», «pensá», «mirá», «fijate», «¿vos qué habrías hecho?», «contámelo en los comentarios». Nada de «tú/vosotros».
- **Presente histórico** en los bloques 2–4 («Kennedy recibe las fotos», no «recibió»).
- **Frases cortas**: media de 10–12 palabras, ninguna de más de 16. Sin «el cual», «debido a que».
- **Cifras concretas en lugar de adjetivos**: no «muchísimos soldados» sino «cuarenta mil soldados».
- **Prohibido**: «Dale like», «suscribite», «¿lo sabías?», emojis en la locución, relleno.
- **Rigor**: solo hechos bien establecidos. Si un dato está discutido, decilo («según Tito Livio…», «los historiadores no se ponen de acuerdo…»). Nunca inventes citas: si una frase famosa es apócrifa, aclaralo. Verificá con búsqueda web cualquier cifra o fecha de la que no estés seguro.
- **Inspiración, no copia**: no reutilices frases ni guiones de `@cdmauro2010`.

## 3. Reglas de la locución para ElevenLabs v4

El bloque de locución se copia **tal cual** en ElevenLabs (modelo Eleven v4). Por eso:

1. **Solo texto hablado + etiquetas de audio** entre corchetes. Nada de títulos, nombres de bloque, acotaciones, markdown, emojis ni comillas tipográficas raras.
2. **Etiquetas permitidas** (en inglés, que es como las interpreta el modelo). Usar **entre 8 y 14 por guion**, nunca dos seguidas ni más de una por frase:
   - Ritmo: `[pause]` (pausa breve), `[long pause]` (silencio dramático).
   - Tono (se mantiene hasta la siguiente etiqueta de tono): `[serious]`, `[calm]`, `[tense]`, `[slowly]`.
   - Intimidad / efecto: `[whispers]` (máx. 1 por guion), `[breathes]` (máx. 1).
3. **Pausas obligatorias** (4): `[long pause]` al final del gancho; `[pause]` antes del primer «Pero…» del desarrollo; `[long pause]` justo antes de revelar el clímax; `[pause]` antes de la pregunta final.
4. **La primera línea empieza con una etiqueta de tono** (normalmente `[serious]` o `[calm]`).
5. **Números, fechas y años siempre en letras**, como se pronuncian en Argentina:
   - `1962` → «mil novecientos sesenta y dos»; `216 a.C.` → «doscientos dieciséis antes de Cristo».
   - `40.000` → «cuarenta mil»; `3,5` → «tres coma cinco»; `10:22` → «las diez y veintidós».
   - Siglos: «el siglo diecinueve» (no XIX).
   - **En la locución no puede aparecer ni un solo dígito.**
6. **Sin abreviaturas ni símbolos**: «Estados Unidos» (no EE. UU.), «la Unión Soviética» (no URSS), «kilómetros», «por ciento», «grados bajo cero», «doctor». Siglas que se deletrean, con espacios: «la C I A», «la K G B», «la O T A N» se lee bien como «la OTAN» (palabra) → usar «la OTAN». Regla: si la sigla se pronuncia como palabra (OTAN, NASA, ONU), escribila junta; si se deletrea (CIA, KGB, FBI, RAF), separala con espacios.
7. **Nombres extranjeros**: usar la forma española habitual (Jruschov, Mólotov, Gengis Kan). Si un nombre es difícil, anotá la pronunciación en la ficha (no en la locución).
8. **Énfasis**: hasta 3 palabras en MAYÚSCULAS en todo el guion, solo en el clímax o el gancho.
9. **Puntuación**: punto y seguido para cortar frases; raya (—) para una interrupción; puntos suspensivos máximo 2 veces por guion.
10. Longitud del bloque: ~2.800–3.300 caracteres (dentro del límite por generación).

**Ajustes recomendados en ElevenLabs:** modelo *Eleven v4* · voz masculina grave, rioplatense (Voice Library → español → Argentina, o un clon de voz propio) · estabilidad *Natural* · velocidad 1.0. Generar, escuchar y, si va por encima de 178 s, subir la velocidad a 1.03–1.05.

## 4. Plantilla del archivo `.md` de cada guion

Ruta: la indicada en la columna `guion` de `parrilla.csv` (`guiones/AAAA-MM-DD/Sx_slug.md`). Copiar esta estructura exacta (los encabezados `##` y el bloque ```` ```text ```` de la locución son leídos por un script; no cambiarlos):

````markdown
# {Título exacto de la parrilla}

| Campo | Valor |
|---|---|
| ID | {AAAA-MM-DD_Sx} |
| Publicación | {día dd/mm/aaaa} · {hora} ART (UTC-3) · {hora} UTC-6 |
| Eje | {eje} |
| Fórmula de título | {A: pregunta paradójica · B: entidad + giro · C: hito + ventana de tiempo} |
| Potencial viral | {Alto / Muy alto} — {por qué, en una frase} |
| Portada (.webp) | Texto: «{2–4 PALABRAS}» · Imagen: {descripción} |
| Frame 00:01 | {rótulo FECHA · LUGAR en mayúsculas sobre qué imagen} |
| Sonido de apertura (00:00–00:02.5) | {foley concreto, ej. teletipo, viento, cascos} |
| Dilema final | {opción A} vs {opción B} |
| Pronunciación | {notas o «—»} |

## Locución — ElevenLabs v4

```text
[serious] ...texto completo...
```

## Guion de edición

| Tiempo | Locución (inicio de frase) | Visual | Texto en pantalla | SFX |
|---|---|---|---|---|
| 00:00–00:02.5 | — | ... | FECHA · LUGAR | ... |
| ... (12–18 filas, cambio de plano cada ~4,5 s, alternando: archivo real · mapa 2D · documento reconstruido · diagrama) |

## Descripción y hashtags

```text
{Descripción de 3 párrafos según la plantilla SEO del kit, con voseo}

💬 ¿Vos qué habrías hecho: {A} o {B}?

📌 Guardá este video y seguí el canal para más decisiones que cambiaron la historia.

#{Tag1} #{Tag2} #{Tag3} #{Tag4} #{Tag5}
```

## Verificación histórica

- {Dato clave 1} — {fuente: obra, autor o institución}
- {Dato clave 2} — {fuente}
- {Dato clave 3} — {fuente}
- Debate / matices: {si aplica}
````

Reglas de la sección de hashtags: exactamente 5, semánticos (entidad, personaje, conflicto, lugar, disciplina). Nunca `#shorts`, `#viral`, `#fyp`, `#parati`.

## 5. Checklist antes de guardar

- [ ] Título idéntico al de la parrilla.
- [ ] Locución de 460–500 palabras sin etiquetas, sin dígitos, sin abreviaturas.
- [ ] 8–14 etiquetas, con las 4 pausas obligatorias.
- [ ] Voseo en el cierre y pregunta binaria.
- [ ] Cifras de los rótulos de edición = cifras dichas en la locución.
- [ ] 5 hashtags. 3+ datos verificados con fuente.
