import timeline from "../../../produccion/12_operacion_cartago/timeline_chunks.json";
import type { Pt, Timeline, VideoPlan } from "../engine/types";

// AG-20 · Operación Cartago (Copenhague, 1945). Cada entrada arranca en la cláusula `from` (o en su palabra `word`)
// de timeline_chunks.json. Los cortes van sobre la palabra clave para que el ritmo siga a la voz.
const A = "assets/";
const NATMUS_BYSA = "Nationalmuseet (Frihedsmuseet) · CC BY-SA 2.0";
const RECON = "Reconstrucción documental · Animación";

const COPENHAGEN: Pt = [12.57, 55.68];
const LONDON: Pt = [-0.13, 51.5];
const FERSFIELD: Pt = [1.07, 52.38];

const EUROPE = { center: [7, 55] as Pt, scale: 1900 };

export const cartago: VideoPlan = {
  folder: "12_operacion_cartago",
  audio: "audio/audio_master_final.wav", // voz (npm run mute:cartago) + música y efectos (build_music_and_sfx_cartago.py)
  timeline: timeline as Timeline,
  endCta: { question: "¿Das la orden de despegar?", a: "SÍ", b: "NO", footer: "Dejame tu respuesta 👇" },
  items: [
    // ── Gancho: un corte cada ~1,5–2 s ──
    {
      from: 1,
      visual: { kind: "skyline", stage: "pole", hitAt: 99 },
      overlays: [
        { kind: "impact", strength: 1.2 },
        { kind: "ribbon", text: "COPENHAGUE · 1945" },
        { kind: "slam", text: "30 metros", color: "amber", at: 1, word: 5 },
      ],
    },
    {
      from: 1,
      word: 9,
      visual: { kind: "photo", src: A + "shellhus_aereo.jpg", portrait: true, zoom: [1.1, 1.25], focus: [0.3, 0.4] },
      overlays: [{ kind: "caption", text: "Copenhague desde un Mosquito, 21 de marzo de 1945" }],
    },
    {
      from: 2,
      visual: { kind: "photo", src: A + "mosquito_eg_t.jpg", portrait: true, zoom: [1.15, 1.3], focus: [0.55, 0.5] },
      overlays: [{ kind: "slam", text: "Un solo obstáculo", color: "cream", size: 96 }],
    },
    {
      from: 2,
      word: 3,
      visual: { kind: "skyline", stage: "pole", hitAt: 2.4 },
      overlays: [
        { kind: "impact", strength: 1.1, at: 2, word: 11 },
        { kind: "title", text: "Un roce", color: "red", at: 2, word: 11 },
      ],
    },
    {
      from: 3,
      visual: { kind: "photo", src: A + "shellhus_llamas.jpg", portrait: true, zoom: [1.05, 1.2], focus: [0.5, 0.5], flashes: true },
      overlays: [{ kind: "title", text: "El ataque más preciso", color: "amber", at: 3, word: 2 }],
    },
    {
      from: 3,
      word: 7,
      visual: { kind: "photo", src: A + "mosquito_formacion.jpg", zoom: [1.15, 1.3], focus: [0.45, 0.4] },
      overlays: [{ kind: "slam", text: "II Guerra Mundial", color: "cream", size: 104 }],
    },
    {
      from: 3,
      word: 11,
      visual: { kind: "photo", src: A + "colegio_llamas.jpg", zoom: [1.05, 1.2], focus: [0.45, 0.5], dim: 0.15 },
      overlays: [
        { kind: "impact", strength: 1.3 },
        { kind: "slam", text: "Pesadilla", color: "red", y: 1250 },
      ],
    },
    // ── Contexto ──
    {
      from: 4,
      visual: {
        kind: "map",
        from: { center: [10, 55.5], scale: 1600 },
        to: { center: [11.5, 55.6], scale: 2800 },
        highlight: [
          { country: "germany", color: "red" },
          { country: "denmark", color: "amber" },
        ],
        markers: [{ at: COPENHAGEN, label: "COPENHAGUE", color: "amber", appear: 1.2 }],
      },
      overlays: [{ kind: "ribbon", text: "MARZO DE 1945" }],
    },
    {
      from: 4,
      word: 6,
      visual: { kind: "photo", src: A + "daneses_1940.jpg", zoom: [1.05, 1.18], focus: [0.5, 0.5] },
      overlays: [
        { kind: "caption", text: "Soldados daneses el 9 de abril de 1940, día de la invasión alemana" },
        { kind: "title", text: "Ocupada", color: "red", at: 4, word: 8 },
      ],
    },
    {
      from: 5,
      visual: { kind: "photo", src: A + "shellhus_antes.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.5, 0.4] },
      overlays: [
        { kind: "caption", text: "El Shellhus, en el centro de Copenhague" },
        { kind: "title", text: "Shellhuset", color: "cream", at: 5, word: 9 },
      ],
    },
    {
      from: 6,
      visual: { kind: "photo", src: A + "shellhus_1940.jpg", portrait: true, zoom: [1.1, 1.25], focus: [0.4, 0.4], dim: 0.3 },
      overlays: [
        { kind: "impact", strength: 0.8, at: 6, word: 5 },
        { kind: "slam", text: "Gestapo", color: "red", at: 6, word: 5, y: 1300 },
      ],
    },
    {
      from: 7,
      visual: { kind: "shellhus", marks: [{ floor: 2, label: "FICHEROS SECRETOS", at: 1.3, color: "amber" }] },
      overlays: [{ kind: "ribbon", text: "CUARTEL DE LA GESTAPO" }],
    },
    {
      from: 8,
      visual: { kind: "photo", src: A + "resistentes_1945.jpg", zoom: [1.1, 1.22], focus: [0.4, 0.6] },
      overlays: [
        { kind: "caption", text: "Resistentes daneses en Copenhague (mayo de 1945)" },
        { kind: "title", text: "A punto de caer", color: "red", at: 8, word: 5 },
      ],
    },
    {
      from: 9,
      visual: {
        kind: "map",
        from: EUROPE,
        to: { center: [5.5, 54], scale: 1700 },
        highlight: [
          { country: "denmark", color: "amber" },
          { country: "uk", color: "blue" },
        ],
        arrows: [{ path: [COPENHAGEN, [6, 54.5], LONDON], color: "amber", appear: 0.3, duration: 1.6 }],
        markers: [
          { at: COPENHAGEN, label: "COPENHAGUE", color: "amber", appear: 0.1, pulse: false },
          { at: LONDON, label: "LONDRES", color: "blue", appear: 1.6, side: "left" },
        ],
      },
      overlays: [{ kind: "title", text: "Una medida extrema", color: "amber", low: true, at: 9, word: 8 }],
    },
    {
      from: 10,
      visual: {
        kind: "quote",
        text: "Bombardeen el Shellhus, aunque esté en medio de Copenhague.",
        author: "Pedido de la resistencia danesa a Londres",
        background: A + "shellhus_antes.jpg",
        stamp: "RECONSTRUCCIÓN",
      },
    },
    {
      from: 10,
      word: 9,
      visual: { kind: "photo", src: A + "mosquito_bombas.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.75] },
      overlays: [{ kind: "title", text: "Quemar los archivos", color: "amber" }],
    },
    {
      from: 10,
      word: 16,
      visual: { kind: "shellhus", marks: [{ floor: 6, label: "PRISIONEROS", at: 0.2, color: "red" }] },
      overlays: [{ kind: "redpulse", bpm: 70 }],
    },
    // ── La trampa ──
    {
      from: 11,
      visual: { kind: "photo", src: A + "mosquito_preparacion.jpg", zoom: [1.05, 1.2], focus: [0.4, 0.5] },
      overlays: [{ kind: "slam", text: "Trampa mortal", color: "red", at: 11, word: 4 }],
    },
    {
      from: 12,
      visual: { kind: "photo", src: A + "shellhus_antes.jpg", portrait: true, zoom: [1.25, 1.45], focus: [0.5, 0.2], dim: 0.25 },
      overlays: [{ kind: "title", text: "Saben que vienen", color: "cream" }],
    },
    {
      from: 13,
      visual: { kind: "shellhus", marks: [{ floor: 6, label: "30 PRISIONEROS", at: 0.7, color: "red" }] },
      overlays: [{ kind: "ribbon", text: "ÚLTIMO PISO, BAJO EL TECHO" }],
    },
    {
      from: 14,
      word: 4,
      visual: { kind: "photo", src: A + "shellhus_1940.jpg", portrait: true, zoom: [1.2, 1.3], focus: [0.5, 0.15], dim: 0.45 },
      overlays: [
        { kind: "impact", strength: 0.7 },
        { kind: "slam", text: "Escudos humanos", color: "red", y: 1300, size: 100 },
      ],
    },
    {
      from: 15,
      visual: { kind: "shellhus", aroundAt: 2.0 },
      overlays: [{ kind: "ribbon", text: "EN MEDIO DE LA CIUDAD" }],
    },
    {
      from: 15,
      word: 10,
      visual: { kind: "photo", src: A + "colegio_1924.jpg", portrait: true, zoom: [1.0, 1.08], focus: [0.5, 0.5] },
      overlays: [{ kind: "title", text: "Y colegios", color: "amber" }],
    },
    // ── El plan ──
    {
      from: 16,
      visual: { kind: "photo", src: A + "mosquito_eg_t.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.5, 0.5] },
      overlays: [
        { kind: "caption", text: "Mosquito FB.VI del escuadrón 487 (RNZAF), 1944" },
        { kind: "slam", text: "Operación Cartago", color: "amber", at: 16, word: 6, size: 100 },
      ],
    },
    {
      from: 16,
      word: 9,
      visual: { kind: "photo", src: A + "mosquito_formacion.jpg", zoom: [1.05, 1.18], focus: [0.5, 0.45] },
      overlays: [{ kind: "stat", value: 20, label: "CAZABOMBARDEROS MOSQUITO", color: "amber", at: 16, word: 10 }],
    },
    {
      from: 16,
      word: 13,
      visual: { kind: "photo", src: A + "bateson.jpg", portrait: true, zoom: [1.0, 1.1], focus: [0.5, 0.3] },
      overlays: [
        { kind: "caption", text: "Robert Bateson, al mando de la misión (1944)" },
        { kind: "title", text: "Robert Bateson", color: "cream", low: true, at: 16, word: 16 },
      ],
    },
    {
      from: 17,
      visual: {
        kind: "map",
        from: EUROPE,
        to: { center: [7, 55.2], scale: 2000 },
        highlight: [
          { country: "uk", color: "blue" },
          { country: "denmark", color: "amber" },
        ],
        arrows: [{ path: [FERSFIELD, [5, 55.6], [8.2, 56.0], [10.5, 55.8], COPENHAGEN], color: "blue", appear: 0.2, duration: 1.3 }],
        markers: [
          { at: FERSFIELD, label: "INGLATERRA", color: "blue", appear: 0.1, pulse: false, side: "left" },
          { at: COPENHAGEN, label: "COPENHAGUE", color: "amber", appear: 1.2 },
        ],
      },
      overlays: [{ kind: "title", text: "Mar del Norte", color: "blue", low: true, at: 17, word: 4 }],
    },
    {
      from: 17,
      word: 7,
      visual: { kind: "skyline", stage: "sea" },
      overlays: [
        { kind: "caption", text: "Recreación: vuelo rasante sobre el mar", source: RECON },
        { kind: "title", text: "Pegados a las olas", color: "cream", at: 17, word: 10 },
      ],
    },
    {
      from: 17,
      word: 12,
      visual: { kind: "radar", blips: false },
      overlays: [{ kind: "title", text: "Invisibles al radar", color: "blue", low: true }],
    },
    {
      from: 17,
      word: 16,
      visual: { kind: "skyline", stage: "spires" },
      overlays: [{ kind: "stat", value: 15, label: "METROS SOBRE LOS TEJADOS", color: "red", at: 17, word: 21 }],
    },
    {
      from: 18,
      visual: {
        kind: "timeline",
        title: "TRES OLEADAS",
        events: [
          { date: "1.ª OLEADA", label: "6 aviones · 11:15", at: 0.8, color: "amber" },
          { date: "2.ª OLEADA", label: "un par de minutos después", at: 1.4, color: "cream" },
          { date: "3.ª OLEADA", label: "detrás de la segunda", at: 2.2, color: "cream" },
        ],
      },
    },
    // ── El ataque ──
    {
      from: 19,
      visual: { kind: "photo", src: A + "shellhus_aereo.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.5, 0.5] },
      overlays: [
        { kind: "ribbon", text: "21 DE MARZO DE 1945 · 11:15" },
        { kind: "caption", text: "Un Mosquito sobre Copenhague durante el ataque" },
      ],
    },
    {
      from: 20,
      word: 5,
      visual: { kind: "skyline", stage: "spires" },
      overlays: [
        { kind: "stat", value: 6, label: "AVIONES EN LA PRIMERA OLEADA", color: "amber", at: 20, word: 10 },
        { kind: "title", text: "Bajo las agujas", color: "cream", at: 20, word: 17 },
      ],
    },
    {
      from: 21,
      visual: { kind: "shellhus", hitAt: 0.3, marks: [{ floor: 2, label: "DE LLENO", at: 0.9, color: "red" }] },
      overlays: [{ kind: "impact", strength: 1.4, delay: 0.3 }],
    },
    {
      from: 22,
      visual: { kind: "photo", src: A + "shellhus_llamas.jpg", portrait: true, zoom: [1.1, 1.25], focus: [0.6, 0.5] },
      overlays: [
        { kind: "caption", text: "El Shellhus en llamas, 21 de marzo de 1945" },
        { kind: "embers", intensity: 0.8 },
        { kind: "title", text: "Los archivos arden", color: "amber", at: 22, word: 1 },
      ],
    },
    {
      from: 22,
      word: 4,
      visual: { kind: "shellhus", hitAt: -1, escapeAt: 1.0 },
      overlays: [{ kind: "ribbon", text: "18 PRISIONEROS ESCAPAN" }],
    },
    {
      from: 23,
      visual: { kind: "photo", src: A + "shellhus_despues.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.5, 0.5] },
      overlays: [
        { kind: "caption", text: "El Shellhus después del ataque" },
        { kind: "slam", text: "Quirúrgico", color: "cream", at: 23, word: 6 },
      ],
    },
    // ── El poste ──
    {
      from: 24,
      visual: { kind: "skyline", stage: "pole", hitAt: 3.2 },
      overlays: [
        { kind: "caption", text: "Recreación: el ala toca la torre de luz", source: RECON },
        { kind: "impact", strength: 1.3, at: 24, word: 12 },
        { kind: "title", text: "Toca la torre", color: "red", at: 24, word: 12 },
      ],
    },
    {
      from: 25,
      visual: { kind: "photo", src: A + "mosquito_nubes.jpg", zoom: [1.0, 1.15], focus: [0.5, 0.5], drift: [0, 40], dim: 0.25 },
      overlays: [{ kind: "title", text: "Pierde el control", color: "red", at: 25, word: 2 }],
    },
    {
      from: 25,
      word: 7,
      visual: { kind: "skyline", stage: "pole", hitAt: -1, crashAt: 0.05 },
      overlays: [
        { kind: "impact", strength: 1.5 },
        { kind: "stat", value: 800, label: "METROS MÁS ALLÁ", color: "red", at: 25, word: 9 },
      ],
    },
    {
      from: 26,
      word: 3,
      visual: { kind: "photo", src: A + "colegio_1924.jpg", portrait: true, zoom: [1.05, 1.15], focus: [0.5, 0.5] },
      overlays: [
        { kind: "caption", text: "Institut Jeanne d'Arc, colegio católico de Frederiksberg" },
        { kind: "title", text: "Juana de Arco", color: "amber", at: 26, word: 5 },
      ],
    },
    {
      from: 27,
      visual: { kind: "photo", src: A + "colegio_llamas.jpg", zoom: [1.0, 1.12], focus: [0.55, 0.5] },
      overlays: [
        { kind: "caption", text: "El colegio Juana de Arco en llamas, 21 de marzo de 1945" },
        { kind: "embers", intensity: 1 },
      ],
    },
    // ── La segunda oleada ──
    {
      from: 28,
      visual: { kind: "photo", src: A + "mosquito_vuelo.jpg", portrait: true, zoom: [1.05, 1.2], focus: [0.4, 0.5] },
      overlays: [
        { kind: "ribbon", text: "DOS MINUTOS DESPUÉS" },
        { kind: "title", text: "2.ª y 3.ª oleada", color: "cream", at: 28, word: 7 },
      ],
    },
    {
      from: 29,
      visual: { kind: "photo", src: A + "calle_humo.jpg", portrait: true, zoom: [1.05, 1.2], focus: [0.6, 0.5], fog: 0.45 },
      overlays: [{ kind: "caption", text: "Humo sobre Copenhague, 21 de marzo de 1945" }],
    },
    {
      from: 30,
      visual: { kind: "skyline", stage: "smoke", confuseAt: 2.3 },
    },
    {
      from: 31,
      word: 10,
      visual: { kind: "photo", src: A + "maglekildevej.jpg", zoom: [1.05, 1.2], focus: [0.6, 0.5] },
      overlays: [
        { kind: "impact", strength: 1.2 },
        { kind: "caption", text: "Maglekildevej, junto al colegio, tras el bombardeo", source: NATMUS_BYSA },
      ],
    },
    // ── El precio ──
    {
      from: 32,
      visual: { kind: "photo", src: A + "shellhus_ruina.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.6, 0.5] },
      overlays: [
        { kind: "caption", text: "Ruinas del Shellhus" },
        { kind: "title", text: "Objetivo destruido", color: "cream", at: 32, word: 3 },
      ],
    },
    {
      from: 32,
      word: 5,
      visual: { kind: "photo", src: A + "colegio_ruinas.jpg", portrait: true, zoom: [1.0, 1.1], focus: [0.5, 0.5], dim: 0.3 },
      overlays: [
        { kind: "stat", value: 86, label: "NIÑOS", color: "red", at: 32, word: 10 },
        { kind: "stat", value: 18, label: "ADULTOS", color: "cream", at: 32, word: 13, slot: 1 },
      ],
    },
    {
      from: 33,
      visual: { kind: "photo", src: A + "capilla.jpg", portrait: true, zoom: [1.0, 1.1], focus: [0.5, 0.6] },
      overlays: [{ kind: "caption", text: "Capilla del Institut Jeanne d'Arc (1924)" }],
    },
    {
      from: 34,
      visual: { kind: "photo", src: A + "resistentes_1945.jpg", zoom: [1.2, 1.3], focus: [0.6, 0.6] },
      overlays: [{ kind: "title", text: "La resistencia se salvó", color: "blue", at: 34, word: 4 }],
    },
    {
      from: 35,
      visual: { kind: "photo", src: A + "colegio_1924.jpg", portrait: true, zoom: [1.1, 1.2], focus: [0.5, 0.5], dim: 0.35 },
      overlays: [{ kind: "title", text: "El precio más alto", color: "red", at: 35, word: 4 }],
    },
    // ── Cierre ──
    {
      from: 36,
      visual: { kind: "photo", src: A + "shellhus_antes.jpg", portrait: true, zoom: [1.05, 1.2], focus: [0.5, 0.4] },
      overlays: [
        { kind: "reticle", x: 540, y: 980, lock: 1.6 },
        { kind: "title", text: "Lleno de rehenes", color: "red", at: 36, word: 10 },
      ],
    },
    {
      from: 37,
      visual: { kind: "dilemma", background: A + "mosquito_formacion.jpg", aAt: 37, bAt: 37, footerAt: 37 },
    },
  ],
};
