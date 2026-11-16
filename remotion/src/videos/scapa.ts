import timeline from "../../../produccion/13_scapa_flow/timeline_chunks.json";
import type { Pt, Timeline, VideoPlan } from "../engine/types";

// AG-21 · Scapa Flow (1919). Cada entrada arranca en la cláusula `from` (o en su palabra `word`)
// de timeline_chunks.json. Los `impact` caen sobre los golpes de build_music_and_sfx_scapa.py.
const A = "assets/";
const RN = "Royal Navy · Dominio público";
const IWM = "Imperial War Museum · Dominio público";

const SCAPA: Pt = [-3.1, 58.88];
const ROSYTH: Pt = [-3.4, 56.03];
const OPEN_SEA: Pt = [-1.2, 59.6];

const NORTH_SEA = { center: [2, 55.5] as Pt, scale: 1700 };
const ORKNEY = { center: [-3.05, 58.9] as Pt, scale: 16000 };

export const scapa: VideoPlan = {
  folder: "13_scapa_flow",
  audio: "audio/audio_master_final.wav", // voz (npm run mute:scapa) + música y efectos (build_music_and_sfx_scapa.py)
  timeline: timeline as Timeline,
  endCta: { question: "¿Qué harías vos en su lugar?", a: "CEDER", b: "HUNDIR", footer: "Dejame tu respuesta 👇" },
  items: [
    // ── Gancho: un corte cada ~1,5–2 s ──
    {
      from: 1,
      visual: { kind: "photo", src: A + "flota_wyllie.jpg", zoom: [1.25, 1.4], focus: [0.45, 0.6] },
      overlays: [
        { kind: "impact", strength: 1.2 },
        { kind: "ribbon", text: "ESCOCIA · 21 DE JUNIO DE 1919" },
      ],
    },
    {
      from: 1,
      word: 11,
      visual: { kind: "fleet", mode: "port", smoke: false, ships: 4 },
    },
    {
      from: 1,
      word: 18,
      visual: { kind: "photo", src: A + "flota_forth.jpg", zoom: [1.2, 1.35], focus: [0.5, 0.5] },
      overlays: [{ kind: "title", text: "La flota más grande del planeta", color: "cream" }],
    },
    {
      from: 2,
      visual: { kind: "photo", src: A + "rendicion_amanecer.jpg", zoom: [1.1, 1.3], focus: [0.55, 0.55] },
      overlays: [{ kind: "impact", strength: 0.7 }],
    },
    {
      from: 2,
      word: 6,
      visual: { kind: "photo", src: A + "oficiales_rendicion.jpg", zoom: [1.1, 1.25], focus: [0.55, 0.5] },
    },
    {
      from: 2,
      word: 11,
      visual: { kind: "scuttle", stage: "list", eventAt: 0.3 },
      overlays: [
        { kind: "impact", strength: 0.8 },
        { kind: "slam", text: "¡Se inclina!", color: "red", at: 2, word: 20 },
      ],
    },
    {
      from: 3,
      visual: { kind: "photo", src: A + "bayern_vertical.jpg", zoom: [1.05, 1.25], focus: [0.5, 0.4] },
      overlays: [{ kind: "stat", value: 5, label: "HORAS", color: "cream" }],
    },
    {
      from: 3,
      word: 3,
      visual: { kind: "scuttle", stage: "sink", eventAt: 0 },
      overlays: [
        { kind: "impact", strength: 1.1 },
        { kind: "stat", value: 52, label: "BARCOS ALEMANES AL FONDO", color: "red" },
      ],
    },
    {
      from: 3,
      word: 12,
      visual: { kind: "photo", src: A + "hindenburg_fondo.jpg", zoom: [1.1, 1.3], focus: [0.5, 0.5] },
      overlays: [{ kind: "slam", text: "Ni un disparo", color: "cream", at: 3, word: 15 }],
    },
    // ── Contexto ──
    {
      from: 4,
      transition: "whip",
      visual: {
        kind: "map",
        from: NORTH_SEA,
        to: { center: [-2.6, 58.6], scale: 5200 },
        highlight: [
          { country: "uk", color: "blue" },
          { country: "germany", color: "red" },
        ],
        markers: [{ at: SCAPA, label: "SCAPA FLOW", color: "amber", appear: 2.4 }],
      },
      overlays: [{ kind: "ribbon", text: "JUNIO DE 1919" }],
    },
    {
      from: 6,
      visual: { kind: "photo", src: A + "grosser_kurfurst.jpg", zoom: [1.1, 1.25], focus: [0.5, 0.5] },
      overlays: [{ kind: "stat", value: 7, label: "MESES DE PAZ", color: "cream", at: 6, word: 6 }],
    },
    {
      from: 7,
      visual: { kind: "photo", src: A + "versalles_orpen.jpg", zoom: [1.0, 1.15], focus: [0.5, 0.75] },
      overlays: [{ kind: "caption", text: "La firma de la paz en el Salón de los Espejos", source: "William Orpen, 1919 · Dominio público" }],
    },
    {
      from: 8,
      visual: { kind: "photo", src: A + "versalles_detalle.jpg", portrait: true, zoom: [1.05, 1.2], focus: [0.5, 0.6] },
      overlays: [{ kind: "title", text: "¿Quién se queda con los barcos?", color: "amber", at: 8, word: 4 }],
    },
    {
      from: 9,
      visual: { kind: "fleet", mode: "port", smoke: false, ships: 3 },
      overlays: [{ kind: "stat", value: 74, label: "BUQUES ALEMANES ANCLADOS", color: "amber" }],
    },
    {
      from: 9,
      word: 9,
      visual: { kind: "photo", src: A + "hindenburg_scapa.jpg", zoom: [1.2, 1.4], focus: [0.5, 0.55] },
      overlays: [{ kind: "caption", text: "Buques alemanes internados en Scapa Flow", source: IWM }],
    },
    {
      from: 10,
      visual: { kind: "photo", src: A + "seydlitz.jpg", zoom: [1.1, 1.25], focus: [0.6, 0.5] },
      overlays: [{ kind: "stat", value: 5000, label: "MARINEROS A BORDO", color: "cream", at: 10, word: 4 }],
    },
    {
      from: 10,
      word: 10,
      visual: { kind: "photo", src: A + "reuter.jpg", portrait: true, zoom: [1.0, 1.1], focus: [0.4, 0.3] },
      overlays: [{ kind: "title", text: "Ludwig von Reuter", color: "amber", low: true }],
    },
    {
      from: 11,
      visual: { kind: "radar", blips: false },
      overlays: [{ kind: "slam", text: "Sin radio", color: "red", at: 11, word: 3 }],
    },
    {
      from: 11,
      word: 6,
      visual: { kind: "photo", src: A + "seydlitz.jpg", zoom: [1.3, 1.45], focus: [0.3, 0.5], dim: 0.15 },
      overlays: [{ kind: "stat", value: 4, label: "DÍAS DE ATRASO", color: "amber", at: 11, word: 12 }],
    },
    // ── El plazo ──
    {
      from: 12,
      visual: { kind: "photo", src: A + "tratado_paz.jpg", portrait: true, zoom: [1.0, 1.15], focus: [0.5, 0.3] },
      overlays: [
        { kind: "countdown", hours: 72, dur: 4, label: "PLAZO PARA FIRMAR", at: 12, word: 8 },
        { kind: "ribbon", text: "21 DE JUNIO · MEDIODÍA", at: 12, word: 16 },
      ],
    },
    {
      from: 13,
      visual: { kind: "photo", src: A + "reuter.jpg", portrait: true, zoom: [1.1, 1.25], focus: [0.4, 0.25], dim: 0.25 },
      overlays: [
        { kind: "redpulse", bpm: 70 },
        { kind: "title", text: "¿Y si vuelve la guerra?", color: "red", low: true },
      ],
    },
    {
      from: 14,
      word: 8,
      visual: {
        kind: "map",
        from: { center: [-2.4, 57.6], scale: 3600 },
        to: { center: [-2.9, 58.7], scale: 7000 },
        highlight: [{ country: "uk", color: "blue" }],
        arrows: [
          { path: [ROSYTH, [-2.2, 57.4], [-2.6, 58.6]], color: "blue", appear: 0.1, duration: 1.4 },
          { path: [OPEN_SEA, [-2.4, 59.0]], color: "blue", appear: 0.4, duration: 1.2 },
        ],
        markers: [{ at: SCAPA, label: "FLOTA ALEMANA", color: "red", appear: 0.2 }],
      },
      overlays: [{ kind: "slam", text: "Por la fuerza", color: "red", at: 14, word: 14 }],
    },
    {
      from: 15,
      visual: {
        kind: "quote",
        text: "Ningún buque de guerra alemán se entrega sin pelear.",
        author: "Código naval de la Marina Imperial (paráfrasis)",
        background: A + "friedrich.jpg",
        stamp: "PROHIBIDO",
      },
    },
    {
      from: 16,
      visual: { kind: "photo", src: A + "grosser_kurfurst.jpg", zoom: [1.3, 1.5], focus: [0.4, 0.55], dim: 0.2 },
      overlays: [{ kind: "options", title: "A BORDO", items: ["Cañones", "Munición"], times: [1.3, 1.9], crossAt: 2.3 }],
    },
    // ── La jugada ──
    {
      from: 17,
      visual: { kind: "photo", src: A + "libro_reuter.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.5, 0.3] },
      overlays: [{ kind: "slam", text: "Jugada silenciosa", color: "amber", at: 17, word: 4 }],
    },
    {
      from: 18,
      visual: {
        kind: "quote",
        text: "Al ver la señal, hundir el buque. No debe caer en manos del enemigo.",
        author: "Orden secreta de Reuter (reconstrucción)",
        background: A + "flota_pears.jpg",
        stamp: "SECRETO",
      },
    },
    {
      from: 19,
      visual: { kind: "scuttle", stage: "signal", eventAt: 0.4 },
    },
    {
      from: 20,
      visual: { kind: "photo", src: A + "hindenburg_scapa.jpg", zoom: [1.3, 1.45], focus: [0.4, 0.6], dim: 0.4 },
      overlays: [{ kind: "options", title: "AL VER LA BANDERA", items: ["Abrir las válvulas", "Romper las cañerías", "Soldar las escotillas"], times: [0.3, 2.5, 4.2], at: 20, word: 1 }],
    },
    // ── 21 de junio ──
    {
      from: 22,
      visual: {
        kind: "map",
        from: ORKNEY,
        to: { center: [-2.7, 58.95], scale: 11000 },
        arrows: [{ path: [[-3.15, 58.84], [-2.9, 58.75], [-2.4, 58.7], [-1.6, 58.75]], color: "blue", appear: 2.4, duration: 2.4, ships: true }],
        markers: [
          { at: [-3.18, 58.87], label: "FLOTA ALEMANA", color: "red", appear: 0.3, side: "left" },
          { at: [-1.7, 58.78], label: "MAR ABIERTO", color: "blue", appear: 4.2, pulse: false },
        ],
      },
      overlays: [{ kind: "ribbon", text: "21 DE JUNIO · MAÑANA" }],
    },
    {
      from: 24,
      visual: { kind: "photo", src: A + "rendicion_amanecer.jpg", zoom: [1.25, 1.4], focus: [0.5, 0.45] },
      overlays: [
        { kind: "impact", strength: 0.8 },
        { kind: "slam", text: "Oportunidad perfecta", color: "amber", size: 84 },
      ],
    },
    {
      from: 25,
      visual: { kind: "fleet", mode: "port", smoke: false, ships: 2 },
      overlays: [
        { kind: "slam", text: "10:30", color: "amber", size: 150, at: 25, word: 2 },
        { kind: "redpulse", bpm: 76 },
      ],
    },
    {
      from: 26,
      visual: { kind: "photo", src: A + "reuter.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.4, 0.3] },
      overlays: [{ kind: "redpulse", bpm: 76 }],
    },
    {
      from: 26,
      word: 9,
      visual: { kind: "scuttle", stage: "signal", eventAt: 0.15 },
      overlays: [{ kind: "title", text: "Tres palabras", color: "cream", low: true, at: 26, word: 12 }],
    },
    {
      from: 27,
      transition: "flash",
      visual: { kind: "photo", src: A + "flota_wyllie.jpg", zoom: [1.4, 1.55], focus: [0.5, 0.55], dim: 0.45 },
      overlays: [
        { kind: "impact", strength: 1.4 },
        { kind: "stamp", text: "PÁRRAFO ONCE", color: "red", y: 900, rotate: -6 },
        { kind: "stamp", text: "CONFIRMAR", color: "amber", y: 1150, rotate: 4, at: 27, word: 2 },
      ],
    },
    // ── El hundimiento ──
    {
      from: 28,
      visual: { kind: "photo", src: A + "flota_forth.jpg", zoom: [1.3, 1.45], focus: [0.6, 0.5] },
      overlays: [{ kind: "caption", text: "Buques de la Flota de Alta Mar alemana, 1918", source: "William Lionel Wyllie · Dominio público" }],
    },
    {
      from: 29,
      visual: { kind: "scuttle", stage: "valve", eventAt: 4.2 },
      overlays: [
        { kind: "title", text: "Las tomas de mar", color: "cream", at: 30, word: 1 },
        { kind: "impact", strength: 1.2, at: 30, word: 6 },
      ],
    },
    {
      from: 30,
      word: 11,
      visual: { kind: "scuttle", stage: "list", eventAt: 0 },
      overlays: [{ kind: "slam", text: "Nadie puede cerrarlas", color: "red", size: 84, at: 30, word: 13 }],
    },
    {
      from: 31,
      visual: { kind: "photo", src: A + "friedrich.jpg", zoom: [1.0, 1.15], focus: [0.5, 0.5] },
      overlays: [
        { kind: "ribbon", text: "12:00 · MEDIODÍA" },
        { kind: "caption", text: "SMS Friedrich der Grosse", source: IWM },
      ],
    },
    {
      from: 31,
      word: 7,
      visual: { kind: "scuttle", stage: "capsize", eventAt: 0.2 },
      overlays: [{ kind: "impact", strength: 1.3, at: 31, word: 14 }],
    },
    {
      from: 32,
      visual: { kind: "fleet", mode: "sail", smoke: true, ships: 3 },
      overlays: [{ kind: "title", text: "A toda máquina", color: "blue" }],
    },
    {
      from: 33,
      visual: { kind: "scuttle", stage: "boil" },
      overlays: [{ kind: "slam", text: "El mar hierve", color: "cream", at: 33, word: 3 }],
    },
    {
      from: 34,
      visual: { kind: "photo", src: A + "derfflinger_volcado.jpg", zoom: [1.15, 1.3], focus: [0.5, 0.5] },
      overlays: [{ kind: "caption", text: "El crucero de batalla Derfflinger, volcado en Scapa Flow", source: RN }],
    },
    {
      from: 34,
      word: 8,
      visual: { kind: "photo", src: A + "hindenburg_scapa.jpg", zoom: [1.1, 1.25], focus: [0.5, 0.55], flashes: true },
      overlays: [{ kind: "impact", strength: 0.8, delay: 0.3 }],
    },
    {
      from: 35,
      visual: { kind: "scuttle", stage: "sink", eventAt: 0.5 },
      overlays: [
        { kind: "stat", value: 9, label: "MARINEROS ALEMANES", color: "red", at: 35, word: 2 },
        { kind: "title", text: "Los últimos caídos de la Gran Guerra", color: "cream", low: true, at: 35, word: 4 },
      ],
    },
    {
      from: 36,
      visual: { kind: "photo", src: A + "hindenburg_fondo.jpg", zoom: [1.25, 1.4], focus: [0.5, 0.45] },
      overlays: [
        { kind: "impact", strength: 1.1 },
        { kind: "slam", text: "Inútil", color: "red", size: 130 },
      ],
    },
    {
      from: 37,
      visual: { kind: "photo", src: A + "bayern_hundiendose.jpg", zoom: [1.05, 1.25], focus: [0.45, 0.45] },
      overlays: [
        { kind: "stat", value: 52, label: "BUQUES HUNDIDOS", color: "red", slot: 0 },
        { kind: "stat", value: 400000, label: "TONELADAS DE ACERO", color: "amber", slot: 1, at: 37, word: 2 },
        { kind: "caption", text: "El acorazado Bayern se va a pique, 21 de junio de 1919", source: RN },
      ],
    },
    // ── Epílogo ──
    {
      from: 38,
      visual: {
        kind: "versus",
        left: { src: A + "fremantle.jpg", name: "Sydney Fremantle", lines: ["VICEALMIRANTE", "ROYAL NAVY", "VIGILABA LA FLOTA"], color: "blue", focus: [0.5, 0.3] },
        right: { src: A + "reuter.jpg", name: "Ludwig von Reuter", lines: ["CONTRALMIRANTE", "MARINA IMPERIAL", "HUNDIÓ SU FLOTA"], color: "amber", focus: [0.4, 0.3] },
      },
    },
    {
      from: 38,
      word: 9,
      visual: { kind: "photo", src: A + "fremantle.jpg", portrait: true, zoom: [1.05, 1.15], focus: [0.5, 0.3], dim: 0.3 },
      overlays: [{ kind: "slam", text: "Deshonra", color: "red", y: 1320 }],
    },
    {
      from: 39,
      visual: {
        kind: "quote",
        text: "Cualquier marino británico habría hecho lo mismo.",
        author: "Un almirante inglés, en privado",
        background: A + "rendicion_amanecer.jpg",
      },
    },
    // ── Cierre ──
    {
      from: 40,
      visual: { kind: "dilemma", background: A + "bayern_vertical.jpg", aAt: 41, bAt: 41, footerAt: 41 },
    },
  ],
};
