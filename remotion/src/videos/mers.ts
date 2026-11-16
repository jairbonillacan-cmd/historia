import timeline from "../../../produccion/07_mers_el_kebir/timeline_chunks.json";
import type { Pt, Timeline, VideoPlan } from "../engine/types";

// AG-16 · Mers el-Kebir (1940). Cada entrada arranca en la cláusula `from` de timeline_chunks.json.
// Los `impact` van clavados a los efectos de build_music_sfx_mers.py (cañonazos, explosión, golpes).
const A = "assets/";

const MERS: Pt = [-0.7, 35.73];
const LONDON: Pt = [-0.13, 51.5];
const GIBRALTAR: Pt = [-5.35, 36.14];
const TOULON: Pt = [5.93, 43.12];
const PARIS: Pt = [2.35, 48.86];

const WEST_EUROPE = { center: [2, 44] as Pt, scale: 1900 };

export const mers: VideoPlan = {
  folder: "07_mers_el_kebir",
  audio: "audio/audio_master_final.wav", // voz censurada (npm run mute:mers) + música y efectos (build_music_sfx_mers.py)
  timeline: timeline as Timeline,
  progress: true,
  endCta: { question: "¿Churchill fue realista o se pasó del límite?", a: "REALISTA", b: "SE PASÓ", footer: "Dejame tu respuesta 👇" },
  items: [
    // Gancho
    {
      from: 1,
      visual: { kind: "photo", src: A + "bretagne_burning.jpg", zoom: [1.25, 1.05], focus: [0.4, 0.5], flashes: true },
      overlays: [
        { kind: "impact", strength: 1.2 },
        { kind: "ribbon", text: "MERS EL-KEBIR · 1940" },
        { kind: "slam", text: "Amigos eternos", color: "cream", size: 88, at: 1, word: 5 },
        { kind: "stamp", text: "No existen", y: 1230, at: 1, word: 8 },
      ],
    },
    {
      from: 2,
      transition: "whip",
      visual: { kind: "photo", src: A + "churchill.jpg", portrait: true, zoom: [1.0, 1.14], focus: [0.5, 0.3], dim: 0.15 },
      overlays: [
        { kind: "slam", text: "Churchill", color: "amber", y: 1300, at: 2, word: 11 },
      ],
    },
    {
      from: 2,
      word: 17,
      transition: "flash",
      visual: { kind: "photo", src: A + "attack_firing.jpg", zoom: [1.1, 1.28], focus: [0.4, 0.4], flashes: true },
      overlays: [
        { kind: "impact", strength: 0.6 },
        { kind: "title", text: "Cañonear a su aliado", color: "red" },
      ],
    },
    {
      from: 3,
      transition: "whip",
      visual: { kind: "photo", src: A + "churchill_group.jpg", zoom: [1.05, 1.22], focus: [0.5, 0.45] },
      overlays: [{ kind: "title", text: "Aliados hasta ayer", color: "amber" }],
    },
    // Contexto
    {
      from: 4,
      transition: "glitch",
      visual: { kind: "photo", src: A + "armistice.png", zoom: [1.05, 1.22], focus: [0.5, 0.55] },
      overlays: [
        { kind: "ribbon", text: "22 DE JUNIO DE 1940" },
        { kind: "caption", text: "Compiègne, firma del armisticio franco-alemán" },
        { kind: "stamp", text: "Armisticio", y: 1000, at: 4, word: 13 },
        { kind: "impact", strength: 0.8, at: 4, word: 13 },
      ],
    },
    {
      from: 5,
      transition: "whip",
      visual: {
        kind: "map",
        from: { center: [2, 50], scale: 2400 },
        to: { center: [0, 50.5], scale: 2900 },
        highlight: [
          { country: "germany", color: "red" },
          { country: "france", color: "red" },
          { country: "uk", color: "blue" },
        ],
        markers: [
          { at: LONDON, label: "SOLA", color: "blue", appear: 0.8, side: "left" },
          { at: PARIS, label: "OCUPADA", color: "red", appear: 0.4, pulse: false },
        ],
      },
    },
    {
      from: 6,
      transition: "zoom",
      visual: { kind: "photo", src: A + "churchill.jpg", portrait: true, zoom: [1.12, 1.28], focus: [0.5, 0.25], dim: 0.25 },
      overlays: [
        { kind: "redpulse", bpm: 60 },
        { kind: "title", text: "Le quita el sueño", color: "amber", low: true },
      ],
    },
    {
      from: 7,
      transition: "whip",
      visual: { kind: "photo", src: A + "dunkerque.jpg", zoom: [1.05, 1.25], focus: [0.5, 0.5] },
      overlays: [
        { kind: "stat", value: 4, suffix: "ª", label: "FLOTA MÁS PODEROSA DEL MUNDO", color: "amber", at: 7, word: 6 },
        { kind: "caption", text: "Acorazado francés Dunkerque" },
      ],
    },
    {
      from: 8,
      transition: "zoom",
      visual: { kind: "photo", src: A + "bretagne_port.jpg", zoom: [1.04, 1.2], focus: [0.5, 0.5] },
      overlays: [{ kind: "stamp", text: "Desarmados", color: "amber", y: 1000, at: 8, word: 9 }],
    },
    {
      from: 9,
      transition: "flash",
      visual: { kind: "quote", text: "Ni un solo barco pasará a manos alemanas.", author: "Almirante François Darlan (paráfrasis)", background: A + "darlan.jpg", stamp: "PROMESA" },
    },
    {
      from: 10,
      visual: {
        kind: "versus",
        left: { src: A + "churchill.jpg", name: "Churchill", lines: ["Reino Unido", "NO LE CREE"], color: "blue", focus: [0.5, 0.25] },
        right: { src: A + "darlan.jpg", name: "Darlan", lines: ["Flota francesa", "JURA POR SU HONOR"], color: "red", focus: [0.5, 0.3] },
      },
    },
    {
      from: 11,
      transition: "glitch",
      visual: { kind: "photo", src: A + "provence.jpg", zoom: [1.05, 1.25], focus: [0.5, 0.5], dim: 0.2 },
      overlays: [
        { kind: "redpulse", bpm: 80 },
        { kind: "title", text: "¿Acorazados para Hitler?", color: "red" },
      ],
    },
    {
      from: 12,
      transition: "whip",
      visual: {
        kind: "map",
        from: { center: [0, 51], scale: 2200 },
        to: { center: [-1, 51.8], scale: 2900 },
        highlight: [
          { country: "germany", color: "red" },
          { country: "uk", color: "blue" },
        ],
        arrows: [{ path: [[3.5, 51.0], [1.5, 51.0], [0.2, 51.3]], color: "red", appear: 0.4, duration: 2, ships: true }],
      },
      overlays: [
        { kind: "title", text: "Invasión en meses", color: "red", low: true },
        { kind: "impact", strength: 0.7, at: 12, word: 10 },
      ],
    },
    // Mers el-Kebir
    {
      from: 13,
      transition: "whip",
      visual: {
        kind: "map",
        from: WEST_EUROPE,
        to: { center: [-0.5, 37.5], scale: 2800 },
        highlight: [
          { country: "uk", color: "blue" },
          { country: "france", color: "red" },
          { country: "algeria", color: "amber" },
        ],
        markers: [{ at: MERS, label: "MERS EL-KEBIR", color: "amber", appear: 1.4 }],
      },
      overlays: [{ kind: "ribbon", text: "ARGELIA FRANCESA" }],
    },
    {
      from: 14,
      transition: "zoom",
      visual: { kind: "photo", src: A + "mouillage.jpg", zoom: [1.05, 1.3], focus: [0.4, 0.45] },
      overlays: [
        { kind: "stat", value: 4, label: "GRANDES ACORAZADOS", color: "amber", at: 15, word: 1 },
        { kind: "caption", text: "La escuadra francesa fondeada en Mers el-Kebir" },
      ],
    },
    {
      from: 16,
      transition: "whip",
      visual: { kind: "photo", src: A + "strasbourg.jpg", zoom: [1.05, 1.22], focus: [0.5, 0.5] },
      overlays: [{ kind: "title", text: "Amarrados al muelle", color: "cream" }],
    },
    {
      from: 17,
      transition: "whip",
      visual: {
        kind: "map",
        from: { center: [-3, 36.3], scale: 4200 },
        to: { center: [-2.2, 36.1], scale: 4800 },
        highlight: [{ country: "algeria", color: "amber" }],
        arrows: [{ path: [GIBRALTAR, [-3.2, 36.0], [-1.2, 35.85]], color: "blue", appear: 0.4, duration: 2.6, ships: true }],
        markers: [
          { at: GIBRALTAR, label: "GIBRALTAR", color: "blue", appear: 0.2, pulse: false, side: "left" },
          { at: MERS, label: "MERS EL-KEBIR", color: "amber", appear: 0.2 },
        ],
      },
      overlays: [{ kind: "ribbon", text: "3 DE JULIO DE 1940" }],
    },
    {
      from: 18,
      transition: "zoom",
      visual: { kind: "photo", src: A + "somerville.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.5, 0.25] },
      overlays: [
        { kind: "caption", text: "Almirante James Somerville, Fuerza H" },
        { kind: "stamp", text: "Orden de Londres", y: 1250, rotate: 6, at: 18, word: 10 },
      ],
    },
    {
      from: 19,
      transition: "flash",
      visual: { kind: "photo", src: A + "hood.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5], dim: 0.45 },
      overlays: [
        { kind: "ribbon", text: "ULTIMÁTUM" },
        { kind: "countdown", hours: 6, dur: 2.3, label: "PARA DECIDIR", at: 19, word: 2 },
      ],
    },
    {
      from: 20,
      transition: "whip",
      visual: { kind: "photo", src: A + "hood_sea.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5], dim: 0.55 },
      overlays: [
        { kind: "options", title: "3 CAMINOS", items: ["Unirse a Gran Bretaña", "Escoltados a América", "Hundir sus barcos"], times: [0, 1.8, 3.5], crossAt: 5.68 },
        { kind: "slam", text: "Fuego", color: "red", y: 1350, size: 210, at: 21, word: 4 },
        { kind: "impact", strength: 1.2, at: 21, word: 5 },
      ],
    },
    {
      from: 22,
      transition: "flash",
      visual: { kind: "photo", src: A + "holland.jpg", zoom: [1.05, 1.22], focus: [0.5, 0.5] },
      overlays: [{ kind: "title", text: "Cuestión de orgullo", color: "amber" }],
    },
    {
      from: 23,
      transition: "zoom",
      visual: { kind: "photo", src: A + "holland.jpg", zoom: [1.25, 1.45], focus: [0.42, 0.45] },
      overlays: [
        { kind: "caption", text: "El capitán Cedric Holland, enviado con el ultimátum" },
        { kind: "stamp", text: "Rango menor", y: 1000, at: 23, word: 13 },
      ],
    },
    {
      from: 24,
      transition: "whip",
      visual: { kind: "photo", src: A + "bretagne.jpg", zoom: [1.05, 1.22], focus: [0.5, 0.5], dim: 0.25 },
      overlays: [{ kind: "stamp", text: "Opción oculta", rotate: 7, at: 25, word: 1 }],
    },
    {
      from: 26,
      transition: "glitch",
      visual: { kind: "photo", src: A + "dunkerque.jpg", zoom: [1.2, 1.4], focus: [0.4, 0.5], dim: 0.3 },
      overlays: [
        { kind: "redpulse", bpm: 85 },
        { kind: "slam", text: "Defenderse", color: "red", at: 26, word: 4 },
      ],
    },
    {
      from: 27,
      transition: "glitch",
      visual: { kind: "radar", blips: true },
      overlays: [
        { kind: "title", text: "Mensaje interceptado", color: "blue", low: true },
        { kind: "stamp", text: "Interceptado", y: 900, at: 27, word: 2 },
      ],
    },
    {
      from: 28,
      transition: "zoom",
      visual: { kind: "photo", src: A + "churchill.jpg", portrait: true, zoom: [1.15, 1.4], focus: [0.5, 0.25], dim: 0.35 },
      overlays: [
        { kind: "redpulse", bpm: 100 },
        { kind: "title", text: "Antes de que oscurezca", color: "red", at: 29, low: true },
        { kind: "impact", strength: 0.9, at: 29, word: 8, delay: 0.76 },
      ],
    },
    // El ataque
    {
      from: 30,
      transition: "flash",
      visual: { kind: "photo", src: A + "attack_firing.jpg", zoom: [1.1, 1.35], focus: [0.55, 0.3], flashes: true },
      overlays: [
        { kind: "slam", text: "17:54", color: "amber", size: 230, at: 30, word: 2 },
        { kind: "impact", strength: 1.5, at: 30, word: 2 },
      ],
    },
    {
      from: 31,
      transition: "whip",
      visual: { kind: "photo", src: A + "shells_landing.jpg", zoom: [1.05, 1.28], focus: [0.5, 0.35], flashes: true },
      overlays: [
        { kind: "embers", intensity: 0.6 },
        { kind: "title", text: "Encerrados en el puerto", color: "red" },
        ...[0.3, 1.0, 1.9, 2.6, 3.8].map((delay) => ({ kind: "impact" as const, strength: 0.5, delay })),
      ],
    },
    {
      from: 32,
      transition: "whip",
      visual: { kind: "photo", src: A + "sortie_feu.jpg", zoom: [1.05, 1.22], focus: [0.5, 0.4], fog: 0.25 },
      overlays: [
        { kind: "embers", intensity: 0.5 },
        { kind: "title", text: "Sin vapor para huir", color: "cream" },
        ...[0.36, 1.46, 2.56, 3.16].map((delay) => ({ kind: "impact" as const, strength: 0.45, delay })),
      ],
    },
    {
      from: 33,
      transition: "zoom",
      visual: { kind: "photo", src: A + "attack_firing.jpg", zoom: [1.25, 1.5], focus: [0.5, 0.25], flashes: true },
      overlays: [
        { kind: "embers", intensity: 0.8 },
        { kind: "stat", value: 10, label: "MINUTOS DE FUEGO", color: "red" },
        { kind: "impact", strength: 1.2, at: 33, word: 4 },
        { kind: "impact", strength: 0.8, at: 33, word: 6, delay: 0.5 },
      ],
    },
    {
      from: 34,
      word: 3,
      transition: "flash",
      visual: { kind: "photo", src: A + "bretagne_burning.jpg", zoom: [1.05, 1.3], focus: [0.4, 0.5], flashes: true },
      overlays: [
        { kind: "impact", strength: 2 },
        { kind: "embers", intensity: 1.3 },
        { kind: "caption", text: "El acorazado Bretagne en llamas, 3 de julio de 1940" },
        { kind: "slam", text: "Hundido", color: "red", y: 1250, at: 34, word: 9 },
      ],
    },
    {
      from: 35,
      transition: "whip",
      visual: { kind: "photo", src: A + "mogador.jpg", zoom: [1.05, 1.22], focus: [0.55, 0.5] },
      overlays: [
        { kind: "embers", intensity: 0.5 },
        { kind: "caption", text: "El destructor Mogador tras el ataque" },
        { kind: "impact", strength: 0.5, delay: 0.6 },
      ],
    },
    {
      from: 36,
      transition: "zoom",
      visual: { kind: "photo", src: A + "plaque_1297.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.45], dim: 0.2 },
      overlays: [{ kind: "stat", value: 1297, label: "MARINEROS FRANCESES", color: "red", at: 36, word: 1 }],
    },
    {
      from: 37,
      transition: "whip",
      visual: { kind: "photo", src: A + "roosevelt.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.5, 0.3] },
      overlays: [
        { kind: "caption", text: "Franklin D. Roosevelt, presidente de EE. UU." },
        { kind: "title", text: "Londres no se rinde", color: "blue", low: true, at: 37, word: 10 },
      ],
    },
    // Epílogo
    {
      from: 38,
      transition: "whip",
      visual: {
        kind: "map",
        from: { center: [5, 44.5], scale: 3200 },
        to: { center: [5.9, 43.6], scale: 4400 },
        highlight: [{ country: "france", color: "red" }],
        markers: [{ at: TOULON, label: "TOLÓN", color: "amber", appear: 0.8 }],
      },
      overlays: [{ kind: "ribbon", text: "NOVIEMBRE DE 1942" }],
    },
    {
      from: 39,
      transition: "zoom",
      visual: { kind: "photo", src: A + "toulon_aerial.jpg", zoom: [1.05, 1.25], focus: [0.4, 0.5] },
      overlays: [
        { kind: "impact", strength: 0.7, at: 39, word: 4 },
        { kind: "stamp", text: "Promesa cumplida", color: "amber", y: 1000, rotate: -6, at: 39, word: 8 },
      ],
    },
    // Cierre
    {
      from: 40,
      transition: "flash",
      visual: { kind: "dilemma", background: A + "attack_firing.jpg", aAt: 40, bAt: 41, footerAt: 41 },
      overlays: [{ kind: "impact", strength: 0.6 }],
    },
  ],
};
