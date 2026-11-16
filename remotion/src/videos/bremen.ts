import timeline from "../../../produccion/06_cielo_bremen/timeline_chunks.json";
import type { Pt, Timeline, VideoPlan } from "../engine/types";

// AG-15 · Cielo de Bremen (1943). Cada entrada arranca en la cláusula `from` (o en su palabra `word`)
// de timeline_chunks.json. Los cortes van sobre la palabra clave para que el ritmo siga a la voz.
const A = "assets/";
const BUNDESARCHIV = "Bundesarchiv, Bild 101I-662-6659-37 · CC BY-SA 3.0 DE";
const RECON = "Reconstrucción documental · Animación";

const BREMEN: Pt = [8.8, 53.08];
const KIMBOLTON: Pt = [-0.39, 52.3];
const COAST: Pt = [8.1, 53.75];
const SWEDEN: Pt = [14.5, 58.6];
const NORTH_SEA: Pt = [3.6, 54.6];

const EUROPE = { center: [9, 55] as Pt, scale: 1900 };

// Posición en pantalla de la cola del B-17 en las escenas `escort` (para la mira).
const TAIL_XY = { x: 470, y: 1180 };

export const bremen: VideoPlan = {
  folder: "06_cielo_bremen",
  audio: "audio/audio_master_final.wav", // voz (npm run mute:bremen) + música y efectos (build_music_and_sfx_bremen.py)
  timeline: timeline as Timeline,
  endCta: { question: "¿Qué harías vos en su lugar?", a: "ORDEN", b: "PIEDAD", footer: "Dejame tu respuesta 👇" },
  items: [
    // ── Gancho: un corte cada ~1,5–2 s ──
    {
      from: 1,
      visual: { kind: "escort", fighter: "behind" },
      overlays: [
        { kind: "impact", strength: 1.2 },
        { kind: "ribbon", text: "CIELO DE ALEMANIA · 1943" },
        { kind: "reticle", ...TAIL_XY, lock: 1.6, at: 1, word: 3 },
      ],
    },
    {
      from: 1,
      word: 8,
      visual: { kind: "photo", src: A + "b17_contrails.jpg", zoom: [1.15, 1.3], focus: [0.6, 0.4] },
      overlays: [{ kind: "slam", text: "II Guerra Mundial", color: "cream", size: 104 }],
    },
    {
      from: 2,
      visual: { kind: "photo", src: A + "b17_damaged_tail.jpg", zoom: [1.05, 1.22], focus: [0.4, 0.5] },
      overlays: [{ kind: "reticle", x: 560, y: 980, lock: 1.0 }],
    },
    {
      from: 2,
      word: 9,
      visual: { kind: "photo", src: A + "b17_crew_wing.jpg", zoom: [1.2, 1.35], focus: [0.3, 0.2] },
      overlays: [
        { kind: "impact" },
        { kind: "slam", text: "Hecho pedazos", color: "red" },
      ],
    },
    {
      from: 3,
      visual: { kind: "photo", src: A + "bf109_cockpit.jpg", zoom: [1.0, 1.25], focus: [0.4, 0.4] },
      overlays: [{ kind: "impact", strength: 0.6, at: 3, word: 3 }],
    },
    {
      from: 3,
      word: 4,
      visual: { kind: "medal", label: "LA MEDALLA MÁS ALTA" },
    },
    {
      from: 4,
      visual: { kind: "photo", src: A + "b17_all_american.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5] },
      overlays: [{ kind: "title", text: "Lo dejás vivo…", color: "cream" }],
    },
    {
      from: 4,
      word: 8,
      visual: { kind: "photo", src: A + "stigler.png", portrait: true, zoom: [1.05, 1.15], focus: [0.5, 0.3], dim: 0.35 },
      overlays: [
        { kind: "impact" },
        { kind: "slam", text: "Fusilado", color: "red", y: 1300 },
      ],
    },
    // ── Contexto ──
    {
      from: 5,
      visual: {
        kind: "map",
        from: { center: [6, 54], scale: 1500 },
        to: { center: [8, 53.5], scale: 2600 },
        highlight: [{ country: "germany", color: "red" }],
        markers: [{ at: BREMEN, label: "BREMEN", color: "red", appear: 1.2 }],
      },
      overlays: [{ kind: "ribbon", text: "20 DE DICIEMBRE DE 1943" }],
    },
    {
      from: 6,
      visual: { kind: "photo", src: A + "crew_ye_olde_pub.jpg", portrait: true, zoom: [1.0, 1.1], focus: [0.2, 0.7] },
      overlays: [
        { kind: "caption", text: "Tripulación del B-17 «Ye Olde Pub». Brown, abajo a la izquierda" },
        { kind: "stat", value: 21, label: "AÑOS TENÍA CHARLIE BROWN", color: "amber", at: 6, word: 11 },
      ],
    },
    {
      from: 7,
      visual: { kind: "photo", src: A + "b17_all_american.jpg", zoom: [1.15, 1.3], focus: [0.4, 0.5] },
      overlays: [
        { kind: "title", text: "Primera misión", color: "cream" },
        { kind: "slam", text: "B-17", color: "amber", y: 1250, at: 7, word: 8 },
      ],
    },
    {
      from: 8,
      visual: {
        kind: "map",
        from: EUROPE,
        to: { center: [5, 53.2], scale: 2600 },
        highlight: [
          { country: "uk", color: "blue" },
          { country: "germany", color: "red" },
        ],
        arrows: [{ path: [KIMBOLTON, [4, 53.6], BREMEN], color: "blue", appear: 0.2, duration: 1.6 }],
        markers: [
          { at: KIMBOLTON, label: "INGLATERRA", color: "blue", appear: 0.1, pulse: false },
          { at: BREMEN, label: "BREMEN", color: "red", appear: 1.5 },
        ],
      },
    },
    {
      from: 8,
      word: 6,
      visual: { kind: "escort", fighter: "none", flak: true },
      overlays: [
        { kind: "impact", strength: 0.8, delay: 0.4 },
        { kind: "title", text: "Fuego feroz", color: "red", at: 8, word: 9 },
      ],
    },
    {
      from: 9,
      visual: { kind: "photo", src: A + "b17_flak.jpg", zoom: [1.04, 1.2], focus: [0.4, 0.5], flashes: true },
      overlays: [{ kind: "impact", strength: 1.4, at: 9, word: 6 }],
    },
    {
      from: 9,
      word: 12,
      visual: { kind: "photo", src: A + "b17_fighter_far.jpg", zoom: [1.1, 1.25], focus: [0.6, 0.4] },
      overlays: [{ kind: "stat", value: 15, label: "CAZAS ALEMANES", color: "red" }],
    },
    {
      from: 10,
      visual: { kind: "photo", src: A + "b17_crew_wing.jpg", zoom: [1.1, 1.25], focus: [0.3, 0.25] },
      overlays: [
        { kind: "impact", strength: 1.2, at: 10, word: 3 },
        { kind: "slam", text: "Un colador", color: "red", at: 10, word: 3 },
      ],
    },
    {
      from: 11,
      visual: {
        kind: "bomber",
        title: "B-17F «YE OLDE PUB» · INFORME DE DAÑOS",
        marks: [
          { part: "nose", label: "NARIZ DESTRUIDA", at: 0.3 },
          { part: "engine2", label: "MOTOR 2 FUERA", at: 1.75 },
          { part: "engine4", label: "MOTOR 4 FUERA", at: 2.2 },
        ],
      },
    },
    {
      from: 11,
      word: 12,
      visual: { kind: "photo", src: A + "b17_propeller.jpg", zoom: [1.05, 1.2], focus: [0.4, 0.5], fog: 0.35 },
      overlays: [{ kind: "stat", value: 60, prefix: "-", suffix: " °C", label: "DENTRO DEL AVIÓN", color: "blue", at: 11, word: 14 }],
    },
    {
      from: 12,
      visual: {
        kind: "bomber",
        title: "B-17F «YE OLDE PUB» · TRIPULACIÓN",
        marks: [
          { part: "nose", label: "NARIZ DESTRUIDA", at: 0, color: "amber" },
          { part: "engine2", label: "MOTOR 2", at: 0, color: "amber" },
          { part: "tail", label: "COLA: SIN ARTILLERO", at: 0.9 },
          { part: "waist", label: "TRIPULANTES HERIDOS", at: 2.9, side: "left" },
          { part: "cockpit", label: "MORFINA CONGELADA", at: 4.0, color: "blue", side: "left" },
        ],
      },
    },
    {
      from: 14,
      visual: { kind: "escort", fighter: "none", smoke: true },
      overlays: [{ kind: "title", text: "Solo y perdido", color: "cream", low: true, at: 14, word: 2 }],
    },
    // ── Stigler ──
    {
      from: 15,
      visual: { kind: "photo", src: A + "bf109_cockpit.jpg", zoom: [1.15, 1.3], focus: [0.6, 0.5], dim: 0.2 },
      overlays: [{ kind: "title", text: "Pura casualidad", color: "amber", at: 15, word: 5 }],
    },
    {
      from: 16,
      visual: { kind: "photo", src: A + "b17_over_germany.jpg", zoom: [1.1, 1.3], focus: [0.3, 0.5] },
      overlays: [{ kind: "caption", text: "B-17 sobre Alemania, 1943" }],
    },
    {
      from: 17,
      visual: {
        kind: "versus",
        left: { src: A + "b17_all_american.jpg", name: "Charlie Brown", lines: ["21 AÑOS", "PILOTO DE B-17", "1.ª MISIÓN"], color: "blue", focus: [0.45, 0.5] },
        right: { src: A + "stigler.png", name: "Franz Stigler", lines: ["AS DE LA LUFTWAFFE", "27 VICTORIAS", "PILOTO DE Bf 109"], color: "amber", focus: [0.5, 0.3] },
      },
    },
    {
      from: 19,
      visual: { kind: "photo", src: A + "b17_fighter_far.jpg", zoom: [1.05, 1.2], focus: [0.6, 0.4] },
      overlays: [
        { kind: "reticle", x: 560, y: 900, lock: 1.2 },
        { kind: "stat", value: 1, label: "DERRIBO PARA LA MEDALLA", color: "amber", at: 20 },
      ],
    },
    {
      from: 20,
      word: 6,
      visual: { kind: "medal", label: "CRUZ DE CABALLERO" },
    },
    {
      from: 22,
      visual: { kind: "photo", src: A + "bf109_flight.jpg", zoom: [1.05, 1.22], focus: [0.4, 0.55] },
      overlays: [
        { kind: "caption", text: "Messerschmitt Bf 109 G en vuelo", source: BUNDESARCHIV },
        { kind: "slam", text: "Bf 109", color: "amber", y: 1150, at: 22, word: 5 },
      ],
    },
    {
      from: 22,
      word: 8,
      visual: { kind: "escort", fighter: "approach", smoke: true },
    },
    {
      from: 23,
      visual: { kind: "escort", fighter: "behind", smoke: true },
      overlays: [{ kind: "reticle", ...TAIL_XY, lock: 1.3 }],
    },
    {
      from: 24,
      visual: { kind: "photo", src: A + "b17_waist_gunner.jpg", zoom: [1.05, 1.18], focus: [0.6, 0.4] },
      overlays: [
        { kind: "caption", text: "Ametralladora de un B-17, 1943" },
        { kind: "slam", text: "Indefensos", color: "red", at: 24, word: 6 },
      ],
    },
    {
      from: 25,
      visual: { kind: "escort", fighter: "behind", smoke: true },
      overlays: [{ kind: "reticle", ...TAIL_XY, lock: 2.2 }],
    },
    {
      from: 25,
      word: 7,
      visual: { kind: "photo", src: A + "stigler.png", portrait: true, zoom: [1.12, 1.25], focus: [0.5, 0.3], dim: 0.15 },
      overlays: [
        { kind: "impact", strength: 0.6, at: 25, word: 8 },
        { kind: "slam", text: "Frena en seco", color: "amber", y: 1320, at: 25, word: 8 },
      ],
    },
    // ── La decisión ──
    {
      from: 26,
      visual: { kind: "photo", src: A + "b17_crew_wing.jpg", zoom: [1.0, 1.15], focus: [0.5, 0.6] },
      overlays: [{ kind: "caption", text: "Tripulación junto al ala destrozada de su B-17" }],
    },
    {
      from: 27,
      visual: { kind: "photo", src: A + "crew_ye_olde_pub.jpg", portrait: true, zoom: [1.1, 1.25], focus: [0.4, 0.6] },
      overlays: [{ kind: "title", text: "Eran chicos", color: "cream", low: true }],
    },
    {
      from: 28,
      visual: { kind: "photo", src: A + "b17_nose_gunner.jpg", zoom: [1.05, 1.18], focus: [0.4, 0.4] },
      overlays: [{ kind: "title", text: "Salvando a sus compañeros", color: "cream", at: 28, word: 3 }],
    },
    {
      from: 29,
      visual: { kind: "photo", src: A + "bf109_flight.jpg", zoom: [1.25, 1.4], focus: [0.3, 0.55], dim: 0.4 },
      overlays: [{ kind: "ribbon", text: "UNA REGLA APRENDIDA EN ÁFRICA" }],
    },
    {
      from: 30,
      visual: {
        kind: "quote",
        text: "Si alguna vez te veo disparar a un hombre en paracaídas, te derribo yo mismo.",
        author: "Gustav Rödel, su comandante en África",
        background: A + "bf109_flight.jpg",
        stamp: "RECONSTRUCCIÓN",
      },
    },
    {
      from: 32,
      visual: { kind: "photo", src: A + "b17_all_american.jpg", zoom: [1.2, 1.4], focus: [0.55, 0.45], fog: 0.25 },
      overlays: [{ kind: "slam", text: "Un paracaídas", color: "cream", at: 32, word: 7 }],
    },
    // ── La escolta ──
    {
      from: 33,
      visual: { kind: "escort", fighter: "wing", smoke: true },
      overlays: [
        { kind: "caption", text: "Recreación: el Bf 109 se pone ala con ala", source: RECON },
        { kind: "slam", text: "Ala con ala", color: "amber", y: 640, size: 120, at: 33, word: 7 },
      ],
    },
    {
      from: 34,
      visual: {
        kind: "map",
        from: { center: [9, 56], scale: 1700 },
        to: { center: [8, 55.5], scale: 1900 },
        highlight: [
          { country: "sweden", color: "amber" },
          { country: "germany", color: "red" },
          { country: "uk", color: "blue" },
        ],
        arrows: [
          { path: [COAST, [11, 56.5], SWEDEN], color: "amber", appear: 0.2, duration: 1.8 },
          { path: [COAST, NORTH_SEA, [0.5, 52.6]], color: "blue", appear: 3.3, duration: 2.6 },
        ],
        markers: [
          { at: SWEDEN, label: "SUECIA NEUTRAL", color: "amber", appear: 1.4 },
          { at: NORTH_SEA, label: "MAR DEL NORTE", color: "blue", appear: 4.0, side: "left", pulse: false },
        ],
      },
    },
    {
      from: 36,
      visual: { kind: "photo", src: A + "flak_gun.jpg", zoom: [1.04, 1.2], focus: [0.5, 0.45], flashes: true },
      overlays: [
        { kind: "title", text: "La muralla antiaérea", color: "red", at: 36, word: 8 },
        { kind: "impact", strength: 0.8, at: 36, word: 8 },
      ],
    },
    {
      from: 36,
      word: 12,
      visual: { kind: "escort", fighter: "wing", flak: true, smoke: true },
    },
    {
      from: 37,
      visual: { kind: "photo", src: A + "stigler.png", portrait: true, zoom: [1.15, 1.3], focus: [0.5, 0.3], dim: 0.35 },
      overlays: [{ kind: "title", text: "Si lo denuncian…", color: "cream", low: true }],
    },
    {
      from: 38,
      word: 3,
      visual: { kind: "photo", src: A + "stigler.png", portrait: true, zoom: [1.3, 1.4], focus: [0.5, 0.3], dim: 0.5 },
      overlays: [
        { kind: "impact" },
        { kind: "slam", text: "El paredón", color: "red", y: 1300 },
      ],
    },
    {
      from: 39,
      visual: { kind: "escort", fighter: "wing", flak: true, smoke: true },
      overlays: [{ kind: "title", text: "Escudo en el aire", color: "amber", low: true, at: 39, word: 2 }],
    },
    {
      from: 39,
      word: 10,
      visual: { kind: "photo", src: A + "flak_gun.jpg", zoom: [1.2, 1.35], focus: [0.4, 0.4], dim: 0.2 },
      overlays: [{ kind: "slam", text: "No disparan", color: "amber", at: 39, word: 13 }],
    },
    {
      from: 40,
      visual: { kind: "escort", fighter: "break", sea: true, smoke: true },
      overlays: [
        { kind: "ribbon", text: "MAR DEL NORTE" },
        { kind: "title", text: "El saludo", color: "amber", low: true, at: 40, word: 7 },
      ],
    },
    {
      from: 41,
      visual: { kind: "photo", src: A + "b17_landing.jpg", zoom: [1.04, 1.16], focus: [0.4, 0.5] },
      overlays: [{ kind: "title", text: "A salvo en Inglaterra", color: "blue", at: 41, word: 2 }],
    },
    // ── Epílogo ──
    {
      from: 42,
      visual: { kind: "photo", src: A + "crew_ye_olde_pub.jpg", portrait: true, zoom: [1.05, 1.15], focus: [0.3, 0.6] },
      overlays: [{ kind: "stat", value: 40, prefix: "+", label: "AÑOS BUSCÁNDOSE", color: "amber", at: 42, word: 5 }],
    },
    {
      from: 42,
      word: 10,
      visual: { kind: "photo", src: A + "stigler.png", portrait: true, zoom: [1.0, 1.08], focus: [0.5, 0.35] },
      overlays: [{ kind: "slam", text: "Hermanos", color: "cream", y: 1320 }],
    },
    // ── Cierre ──
    {
      from: 43,
      visual: { kind: "escort", fighter: "behind", smoke: true },
      overlays: [
        { kind: "reticle", ...TAIL_XY, lock: 1.6 },
        { kind: "stat", value: 6000, label: "METROS DE ALTURA", color: "cream", at: 43, word: 8 },
      ],
    },
    {
      from: 44,
      visual: { kind: "dilemma", background: A + "b17_contrails.jpg", aAt: 44, bAt: 44, footerAt: 44 },
    },
  ],
};
