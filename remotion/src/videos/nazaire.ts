import timeline from "../../../produccion/09_saint_nazaire/timeline_chunks.json";
import type { Pt, Timeline, VideoPlan } from "../engine/types";

// AG-18 · Operación Chariot, Saint-Nazaire (1942). Cada entrada arranca en la cláusula `from` (o en su palabra `word`)
// de timeline_chunks.json. Los cortes van sobre la palabra clave; embestida y explosión van clavadas a los
// mismos tiempos que los efectos de build_music_and_sfx_saint_nazaire.py.
const A = "assets/";
const tl = timeline as Timeline;
const BA = (n: string) => `Bundesarchiv, Bild ${n} · CC BY-SA 3.0 DE`;

// Segundos entre el inicio de la palabra `k0` y el de la palabra `k1` de la cláusula `i`.
const gap = (i: number, k0: number, k1: number) => {
  const w = tl.chunks.find((c) => c.index === i)!.words;
  return w[k1].start - w[k0].start;
};

const NAZAIRE: Pt = [-2.2, 47.28];
const TRONDHEIM: Pt = [10.4, 63.43];
const FALMOUTH: Pt = [-5.07, 50.15];
const ATLANTIC: Pt = [-14, 52];
const ESTUARY = { center: [-2.3, 47.2] as Pt, scale: 26000 };

export const nazaire: VideoPlan = {
  folder: "09_saint_nazaire",
  audio: "audio/audio_master_final.wav", // voz censurada (npm run mute:nazaire) + música y efectos (build_music_and_sfx_saint_nazaire.py)
  timeline: tl,
  progress: true,
  endCta: { question: "¿Valió la pena el sacrificio?", a: "SÍ, VALIÓ", b: "NO VALIÓ", footer: "Dejame tu respuesta 👇" },
  items: [
    // ── Gancho: un corte cada ~1,5–2,5 s ──
    {
      from: 1,
      visual: { kind: "photo", src: A + "campbeltown_proa.jpg", zoom: [1.2, 1.08], focus: [0.35, 0.35] },
      overlays: [
        { kind: "impact", strength: 1.2 },
        { kind: "ribbon", text: "SAINT-NAZAIRE · 1942" },
      ],
    },
    {
      from: 1,
      word: 8,
      visual: { kind: "photo", src: A + "campbeltown_puente.jpg", zoom: [1.05, 1.2], focus: [0.3, 0.4] },
      overlays: [{ kind: "slam", text: "Encallado", color: "amber", y: 1250, at: 1, word: 13 }],
    },
    {
      from: 2,
      transition: "whip",
      visual: { kind: "photo", src: A + "campbeltown_compuerta.jpg", zoom: [1.1, 1.25], focus: [0.6, 0.45] },
      overlays: [{ kind: "title", text: "Se ríen y sacan fotos", color: "cream" }],
    },
    {
      from: 2,
      word: 9,
      visual: { kind: "photo", src: A + "campbeltown_dique.jpg", zoom: [1.05, 1.2], focus: [0.55, 0.5] },
      overlays: [{ kind: "stamp", text: "¿Un fracaso?", y: 1180, at: 2, word: 11 }],
    },
    {
      from: 3,
      visual: { kind: "photo", src: A + "campbeltown_puente.jpg", zoom: [1.35, 1.5], focus: [0.25, 0.25], dim: 0.2 },
    },
    {
      from: 3,
      word: 3,
      transition: "flash",
      visual: {
        kind: "destroyer",
        title: "HMS CAMPBELTOWN · LO QUE NADIE VE",
        chargeAt: 0.6,
        cutAt: 0,
        marks: [{ part: "charge", label: "BAJO SUS PIES", at: 1.4 }],
      },
      overlays: [{ kind: "impact", strength: 0.6, delay: 0.6 }],
    },
    {
      from: 4,
      visual: { kind: "photo", src: A + "campbeltown_proa.jpg", zoom: [1.3, 1.45], focus: [0.3, 0.3], dim: 0.45 },
      overlays: [
        { kind: "redpulse", bpm: 80 },
        { kind: "countdown", hours: 0.004, dur: 3.2, label: "EL ÁCIDO AVANZA" },
      ],
    },
    // ── El Tirpitz y el dique ──
    {
      from: 5,
      transition: "zoom",
      visual: { kind: "photo", src: A + "tirpitz_mar.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5], dim: 0.15 },
      overlays: [{ kind: "title", text: "El miedo a un solo barco", color: "cream", at: 5, word: 4 }],
    },
    {
      from: 6,
      visual: { kind: "photo", src: A + "tirpitz_noruega.jpg", zoom: [1.0, 1.15], focus: [0.55, 0.55] },
      overlays: [
        { kind: "slam", text: "Tirpitz", color: "red", y: 1250, size: 150, at: 6, word: 3 },
        { kind: "caption", text: "El Tirpitz camuflado en un fiordo noruego" },
      ],
    },
    {
      from: 6,
      word: 5,
      visual: { kind: "photo", src: A + "bismarck.jpg", zoom: [1.05, 1.18], focus: [0.4, 0.5] },
      overlays: [{ kind: "caption", text: "El Bismarck, su gemelo", source: "Bundesarchiv · Wikimedia Commons" }],
    },
    {
      from: 6,
      word: 9,
      visual: {
        kind: "map",
        from: { center: [9, 62], scale: 1500 },
        to: { center: [-2, 57], scale: 1000 },
        highlight: [{ country: "norway", color: "red" }],
        markers: [{ at: TRONDHEIM, label: "TIRPITZ", color: "red", appear: 0.2 }],
        arrows: [{ path: [TRONDHEIM, [3, 63.5], [-8, 60], ATLANTIC], color: "red", appear: 1.3, duration: 1.8 }],
      },
      overlays: [{ kind: "title", text: "Al Atlántico", color: "red", low: true, at: 7, word: 4 }],
    },
    {
      from: 7,
      word: 7,
      visual: { kind: "photo", src: A + "convoy.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5] },
      overlays: [
        { kind: "impact", strength: 0.7 },
        { kind: "caption", text: "Convoy aliado en el Atlántico, c. 1942" },
      ],
    },
    {
      from: 8,
      visual: {
        kind: "map",
        from: { center: [-6, 50], scale: 2000 },
        to: { center: [-3, 47.8], scale: 3600 },
        highlight: [
          { country: "france", color: "amber" },
          { country: "uk", color: "blue" },
        ],
        arrows: [{ path: [[-12, 48.5], [-6, 47.6], NAZAIRE], color: "red", appear: 0.6, duration: 1.6 }],
        markers: [{ at: NAZAIRE, label: "SAINT-NAZAIRE", color: "red", appear: 2.0, side: "left" }],
      },
      overlays: [{ kind: "title", text: "Un único dique", color: "amber", low: true, at: 8, word: 3 }],
    },
    {
      from: 9,
      visual: { kind: "photo", src: A + "dique_aereo_antes.jpg", zoom: [1.05, 1.25], focus: [0.5, 0.45] },
      overlays: [
        { kind: "ribbon", text: "DIQUE NORMANDIE" },
        { kind: "caption", text: "El puerto de Saint-Nazaire desde el aire", source: "IWM C 2351 · Dominio público" },
      ],
    },
    {
      from: 10,
      visual: { kind: "photo", src: A + "campbeltown_compuerta.jpg", zoom: [1.2, 1.35], focus: [0.35, 0.65], dim: 0.2 },
      overlays: [{ kind: "stat", value: 10, suffix: " m", label: "DE ACERO DE ESPESOR", color: "amber", at: 10, word: 9 }],
    },
    {
      from: 11,
      visual: { kind: "photo", src: A + "tirpitz_noruega.jpg", zoom: [1.25, 1.4], focus: [0.6, 0.55], dim: 0.25 },
      overlays: [{ kind: "slam", text: "Nunca saldría", color: "cream", y: 1250, at: 11, word: 2 }],
    },
    {
      from: 12,
      visual: {
        kind: "map",
        from: { center: [-2.5, 47.2], scale: 14000 },
        to: ESTUARY,
        highlight: [{ country: "france", color: "amber" }],
        arrows: [{ path: [[-2.62, 47.12], [-2.38, 47.2], NAZAIRE], color: "blue", appear: 0.4, duration: 2.0 }],
        markers: [{ at: NAZAIRE, label: "DIQUE", color: "red", appear: 1.6, side: "left" }],
      },
      overlays: [{ kind: "stat", value: 5, suffix: " km", label: "DE RÍO VIGILADO", color: "blue", at: 12, word: 7 }],
    },
    {
      from: 12,
      word: 15,
      visual: { kind: "raid", stage: "lights" },
      overlays: [{ kind: "slam", text: "Búnkeres y cañones", color: "red", size: 96, y: 1450 }],
    },
    {
      from: 13,
      visual: { kind: "photo", src: A + "puerto_bombardeo.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5] },
      overlays: [{ kind: "stamp", text: "Imposible", y: 1150, at: 13, word: 6 }],
    },
    // ── Operación Chariot ──
    {
      from: 14,
      transition: "flash",
      visual: { kind: "photo", src: A + "lancha_ml.jpg", zoom: [1.15, 1.3], focus: [0.5, 0.55], dim: 0.35 },
      overlays: [
        { kind: "ribbon", text: "OPERACIÓN CHARIOT" },
        { kind: "slam", text: "Chariot", color: "amber", at: 14, word: 4 },
        { kind: "stamp", text: "Sin retorno", y: 1300, at: 14, word: 8 },
      ],
    },
    {
      from: 15,
      visual: { kind: "photo", src: A + "destructor_1940.jpg", zoom: [1.0, 1.12], focus: [0.5, 0.5] },
      overlays: [{ kind: "caption", text: "Destructores veteranos cedidos por EE. UU. en 1940, como el Campbeltown", source: "NARA 196521 · Dominio público" }],
    },
    {
      from: 16,
      visual: { kind: "photo", src: A + "destructor_town.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5] },
      overlays: [
        { kind: "slam", text: "Campbeltown", color: "amber", y: 1250, size: 110 },
        { kind: "caption", text: "HMS Buxton, gemelo del Campbeltown, 1942", source: "IWM A 8659 · Dominio público" },
      ],
    },
    {
      from: 17,
      visual: {
        kind: "destroyer",
        title: "HMS CAMPBELTOWN · EL DISFRAZ",
        cutAt: 0.5,
        flagAt: gap(17, 0, 9),
        marks: [
          { part: "funnels", label: "2 CHIMENEAS MENOS", at: 0.9, color: "amber" },
          { part: "flag", label: "BANDERA ALEMANA", at: gap(17, 0, 9) + 0.2, side: "left" },
        ],
      },
    },
    {
      from: 17,
      word: 13,
      visual: { kind: "photo", src: A + "campbeltown_dique.jpg", zoom: [1.2, 1.35], focus: [0.62, 0.4], dim: 0.15 },
      overlays: [{ kind: "title", text: "Un patrullero alemán… falso", color: "cream" }],
    },
    {
      from: 18,
      visual: {
        kind: "destroyer",
        title: "HMS CAMPBELTOWN · LA CARGA",
        cutAt: 0,
        chargeAt: gap(18, 0, 2),
        marks: [{ part: "charge", label: "4.500 KG", at: gap(18, 0, 4) }],
      },
      overlays: [{ kind: "impact", strength: 0.7, at: 18, word: 4 }],
    },
    {
      from: 19,
      visual: { kind: "photo", src: A + "campbeltown_puente.jpg", zoom: [1.25, 1.4], focus: [0.25, 0.5], dim: 0.3 },
      overlays: [
        { kind: "title", text: "Acero y cemento", color: "cream", at: 19, word: 4 },
        { kind: "stamp", text: "Imposible desactivar", y: 1250, rotate: -5, at: 19, word: 11 },
      ],
    },
    {
      from: 20,
      visual: {
        kind: "destroyer",
        title: "HMS CAMPBELTOWN · LA ESPOLETA",
        cutAt: 0,
        chargeAt: 0,
        marks: [{ part: "charge", label: "ESPOLETAS DE ÁCIDO", at: 0.3, color: "amber" }],
      },
    },
    {
      from: 21,
      visual: { kind: "photo", src: A + "lancha_ml.jpg", zoom: [1.0, 1.15], focus: [0.5, 0.6] },
      overlays: [
        { kind: "caption", text: "Lancha motora (ML) como las del raid", source: "IWM A 13626A · Dominio público" },
        { kind: "stat", value: 611, label: "COMANDOS Y MARINEROS", color: "amber", at: 21, word: 5 },
      ],
    },
    {
      from: 21,
      word: 11,
      visual: { kind: "photo", src: A + "convoy_cielo.jpg", zoom: [1.1, 1.25], focus: [0.5, 0.6], dim: 0.2 },
      overlays: [
        { kind: "stat", value: 16, label: "LANCHAS DE MADERA", color: "amber" },
        { kind: "title", text: "Llenas de combustible", color: "red", low: true, at: 21, word: 16 },
      ],
    },
    {
      from: 22,
      visual: {
        kind: "map",
        from: { center: [-4, 49], scale: 3000 },
        to: { center: [-2.6, 47.25], scale: 12000 },
        highlight: [
          { country: "france", color: "amber" },
          { country: "uk", color: "blue" },
        ],
        arrows: [{ path: [FALMOUTH, [-4.6, 48], [-2.7, 47.15], NAZAIRE], color: "blue", appear: 0.1, duration: 2.4, ships: true }],
        markers: [{ at: NAZAIRE, label: "SAINT-NAZAIRE", color: "red", appear: 1.8, side: "left" }],
      },
      overlays: [{ kind: "ribbon", text: "27 DE MARZO DE 1942 · NOCHE" }],
    },
    {
      from: 23,
      visual: { kind: "raid", stage: "river" },
      overlays: [{ kind: "embers", intensity: 0.7, at: 23, word: 2 }],
    },
    // ── El ataque ──
    {
      from: 24,
      transition: "glitch",
      visual: { kind: "photo", src: A + "puente_mando.jpg", zoom: [1.1, 1.25], focus: [0.6, 0.4], dim: 0.4 },
      overlays: [{ kind: "slam", text: "1:28", color: "amber", size: 220, y: 1150, at: 24, word: 2 }],
    },
    {
      from: 25,
      visual: { kind: "raid", stage: "lights" },
      overlays: [
        { kind: "title", text: "Descubiertos", color: "red", at: 25, word: 3 },
        { kind: "impact", strength: 1.0, at: 25, word: 9 },
        { kind: "slam", text: "A quemarropa", color: "red", y: 1450, at: 25, word: 12 },
      ],
    },
    {
      from: 26,
      visual: { kind: "photo", src: A + "campbeltown_puente.jpg", zoom: [1.05, 1.2], focus: [0.75, 0.3], flashes: true },
      overlays: [
        { kind: "embers", intensity: 1 },
        { kind: "impact", strength: 0.6, at: 26, word: 8 },
      ],
    },
    {
      from: 27,
      visual: { kind: "photo", src: A + "beattie.jpg", portrait: true, zoom: [1.0, 1.1], focus: [0.5, 0.3] },
      overlays: [
        { kind: "caption", text: "Stephen Beattie, comandante del Campbeltown" },
        { kind: "slam", text: "A toda máquina", color: "amber", y: 1350, size: 100, at: 27, word: 5 },
      ],
    },
    {
      from: 28,
      visual: { kind: "raid", stage: "ram", hitAt: gap(28, 0, 5) + 0.15 },
      overlays: [
        { kind: "ribbon", text: "1:34" },
        { kind: "impact", strength: 1.8, at: 28, word: 5, delay: 0.15 },
        { kind: "slam", text: "Embiste", color: "red", y: 1450, at: 28, word: 5, delay: 0.15 },
      ],
    },
    {
      from: 28,
      word: 8,
      visual: { kind: "photo", src: A + "campbeltown_compuerta.jpg", zoom: [1.05, 1.18], focus: [0.5, 0.5] },
      overlays: [
        { kind: "stat", value: 35, suffix: " km/h", label: "CONTRA LA COMPUERTA", color: "red" },
        { kind: "title", text: "Clavado en el acero", color: "cream", at: 28, word: 14 },
      ],
    },
    // ── Después ──
    {
      from: 29,
      visual: { kind: "photo", src: A + "campbeltown_dique.jpg", zoom: [1.0, 1.12], focus: [0.5, 0.55] },
      overlays: [{ kind: "caption", text: "El Campbeltown en el dique, con la popa hundida", source: BA("101II-MW-3722-03") }],
    },
    {
      from: 30,
      visual: { kind: "photo", src: A + "lancha_ml.jpg", zoom: [1.3, 1.45], focus: [0.6, 0.5], dim: 0.4 },
      overlays: [{ kind: "stat", value: 611, label: "SALIERON DE INGLATERRA", color: "cream", at: 30, word: 4 }],
    },
    {
      from: 31,
      visual: { kind: "photo", src: A + "campbeltown_proa.jpg", zoom: [1.15, 1.3], focus: [0.6, 0.35], dim: 0.35 },
      overlays: [{ kind: "stat", value: 400, prefix: "+", label: "CAÍDOS O PRISIONEROS", color: "red", at: 31, word: 2 }],
    },
    {
      from: 32,
      visual: { kind: "photo", src: A + "beattie.jpg", portrait: true, zoom: [1.1, 1.2], focus: [0.5, 0.3], dim: 0.25 },
      overlays: [
        { kind: "ribbon", text: "28 DE MARZO · MAÑANA" },
        { kind: "title", text: "Interrogado", color: "cream", low: true, at: 32, word: 4 },
      ],
    },
    {
      from: 33,
      visual: {
        kind: "quote",
        text: "Una compuerta de ese tamaño no se rompe con un simple choque.",
        author: "Oficial alemán, a Beattie",
        background: A + "campbeltown_compuerta.jpg",
        stamp: "RECONSTRUCCIÓN",
      },
    },
    // ── La explosión ──
    {
      from: 34,
      visual: { kind: "photo", src: A + "campbeltown_puente.jpg", zoom: [1.3, 1.5], focus: [0.35, 0.35], dim: 0.4 },
      overlays: [
        { kind: "redpulse", bpm: 96 },
        { kind: "countdown", hours: 0.0017, dur: gap(34, 0, 8), label: "MEDIODÍA" },
      ],
    },
    {
      from: 34,
      word: 8,
      visual: {
        kind: "destroyer",
        title: "HMS CAMPBELTOWN · 4.500 KG",
        cutAt: 0,
        chargeAt: 0,
        marks: [{ part: "charge", label: "DETONADOR ACTIVADO", at: 0.5 }],
      },
      overlays: [{ kind: "redpulse", bpm: 140 }],
    },
    {
      from: 35,
      visual: { kind: "raid", stage: "blast", blastAt: gap(35, 0, 3) - 0.05 },
      overlays: [
        { kind: "impact", strength: 2, at: 35, word: 3 },
        { kind: "slam", text: "TOTAL", color: "red", size: 200, y: 1450, at: 35, word: 3, delay: 0.1 },
      ],
    },
    {
      from: 36,
      visual: { kind: "photo", src: A + "dique_aereo_despues.jpg", zoom: [1.05, 1.22], focus: [0.6, 0.45] },
      overlays: [
        { kind: "embers", intensity: 0.8 },
        { kind: "title", text: "La compuerta, arrancada", color: "amber", at: 36, word: 5 },
        { kind: "caption", text: "El dique Normandie inundado tras la explosión", source: "IWM C 3317A · Dominio público" },
      ],
    },
    {
      from: 37,
      visual: { kind: "photo", src: A + "puerto_bombardeo.jpg", zoom: [1.2, 1.35], focus: [0.45, 0.6], dim: 0.35 },
      overlays: [{ kind: "stat", value: 300, prefix: "+", label: "BAJAS ALEMANAS", color: "red", at: 37, word: 4 }],
    },
    {
      from: 37,
      word: 7,
      visual: { kind: "photo", src: A + "dique_aereo_despues.jpg", zoom: [1.3, 1.45], focus: [0.4, 0.5], dim: 0.15 },
      overlays: [{ kind: "stamp", text: "Fuera de servicio", y: 1150, at: 37, word: 10 }],
    },
    // ── Epílogo y cierre ──
    {
      from: 38,
      transition: "flash",
      visual: { kind: "medal", label: "5 CRUCES VICTORIA" },
    },
    {
      from: 38,
      word: 10,
      visual: { kind: "photo", src: A + "tirpitz_mar.jpg", zoom: [1.2, 1.35], focus: [0.4, 0.4], dim: 0.2 },
      overlays: [{ kind: "title", text: "Nunca tocó el Atlántico", color: "amber", at: 38, word: 16 }],
    },
    {
      from: 39,
      visual: { kind: "photo", src: A + "destructor_1940.jpg", zoom: [1.2, 1.3], focus: [0.5, 0.4], dim: 0.4 },
      overlays: [{ kind: "ribbon", text: "EL PRECIO" }],
    },
    {
      from: 40,
      visual: { kind: "photo", src: A + "campbeltown_proa.jpg", zoom: [1.0, 1.1], focus: [0.5, 0.4], dim: 0.3 },
      overlays: [{ kind: "slam", text: "2 de cada 3", color: "red", y: 1200, size: 140, at: 40, word: 3 }],
    },
    {
      from: 41,
      visual: { kind: "dilemma", background: A + "campbeltown_compuerta.jpg", aAt: 41, bAt: 41, footerAt: 41 },
    },
  ],
};
