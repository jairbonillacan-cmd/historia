import timeline from "../../../produccion/05_isla_kiska/timeline_chunks.json";
import type { Pt, Timeline, VideoPlan } from "../engine/types";

// AG-14 · Isla de Kiska (1943). Cada entrada arranca en la cláusula `from` de timeline_chunks.json.
const H = "assets/hires/";
const A = "assets/";

const KISKA: Pt = [177.55, 51.98];
const ATTU: Pt = [173.2, 52.85];
const ADAK: Pt = [-176.65, 51.85];
const KURILES: Pt = [155.9, 50.4];
const ALASKA: Pt = [-152, 63.5];

export const kiska: VideoPlan = {
  folder: "05_isla_kiska",
  audio: "audio/audio_master_censurado.wav", // generado con: npm run mute:kiska
  timeline: timeline as Timeline,
  endCta: { question: "¿Qué pesa más en una guerra?", a: "HONOR", b: "VIDA", footer: "Dejame tu respuesta 👇" },
  items: [
    // Gancho: cortes cada ~2 s
    {
      from: 1,
      visual: { kind: "photo", src: A + "kiska_landing.jpg", zoom: [1.12, 1.24], focus: [0.4, 0.55] },
      overlays: [
        { kind: "stat", value: 300, prefix: "+", label: "BAJAS ALIADAS", color: "red" },
        { kind: "title", text: "Muertos y heridos", color: "red", at: 2 },
      ],
    },
    {
      from: 3,
      visual: { kind: "photo", src: H + "kiska_bombed_1943.jpg", zoom: [1.0, 1.18], focus: [0.5, 0.45] },
      overlays: [{ kind: "ribbon", text: "ISLA DE KISKA · 1943" }],
    },
    {
      from: 4,
      visual: { kind: "photo", src: A + "kiska_bunkers.jpg", zoom: [1.08, 1.2], focus: [0.55, 0.5] },
      overlays: [
        { kind: "stat", value: 0, label: "SOLDADOS ENEMIGOS", color: "amber" },
        { kind: "caption", text: "Submarinos japoneses abandonados en Kiska" },
      ],
    },
    {
      from: 5,
      visual: { kind: "photo", src: H + "troops_loading.jpg", zoom: [1.05, 1.15], focus: [0.35, 0.6] },
      overlays: [{ kind: "title", text: "Un absurdo", color: "amber" }],
    },
    {
      from: 6,
      visual: {
        kind: "map",
        from: { center: [-160, 55], scale: 620 },
        to: { center: [-172, 54], scale: 900 },
        highlight: [
          { country: "usa", color: "blue" },
          { country: "canada", color: "blue" },
        ],
        markers: [
          { at: ALASKA, label: "ALASKA", pulse: false, appear: 0.6 },
          { at: KISKA, label: "KISKA", color: "red", appear: 1.6, side: "left" },
        ],
      },
    },
    // Contexto
    {
      from: 7,
      visual: { kind: "photo", src: A + "kiska_japanese.jpg", zoom: [1.05, 1.14], focus: [0.6, 0.4] },
      overlays: [
        { kind: "ribbon", text: "JUNIO DE 1942" },
        { kind: "caption", text: "Tropas japonesas en Kiska, 1942" },
      ],
    },
    {
      from: 8,
      visual: {
        kind: "map",
        from: { center: [163, 46], scale: 900 },
        to: { center: [175.5, 52.2], scale: 4200 },
        highlight: [
          { country: "japan", color: "red" },
          { country: "usa", color: "blue" },
        ],
        arrows: [
          { path: [[145, 42], KURILES, ATTU], color: "red", appear: 0.6, duration: 2.2 },
          { path: [[145, 42], KURILES, KISKA], color: "red", appear: 1.2, duration: 2.4 },
        ],
        markers: [
          { at: ATTU, label: "ATTU", color: "red", appear: 4.4, side: "left" },
          { at: KISKA, label: "KISKA", color: "red", appear: 4.9 },
        ],
      },
      overlays: [{ kind: "title", text: "Único territorio de EE. UU. invadido", color: "red", at: 10, low: true }],
    },
    {
      from: 11,
      visual: { kind: "photo", src: A + "aleutians_campaign.jpg", portrait: true, zoom: [1.0, 1.05] },
      overlays: [
        { kind: "ribbon", text: "MAYO DE 1943" },
        { kind: "caption", text: "Suministros en Attu, 1943" },
      ],
    },
    {
      from: 12,
      visual: {
        kind: "map",
        from: { center: [174.5, 52.6], scale: 9000 },
        to: { center: ATTU, scale: 19000 },
        arrows: [{ path: [[173.9, 52.1], [173.3, 52.78]], color: "blue", appear: 0.3, duration: 1.4 }],
        markers: [{ at: ATTU, label: "ATTU", color: "blue", appear: 1.2 }],
      },
    },
    {
      from: 13,
      visual: { kind: "photo", src: A + "attu_battle.jpg", zoom: [1.04, 1.16], focus: [0.5, 0.35] },
      overlays: [
        { kind: "title", text: "Una carnicería", color: "red" },
        { kind: "stat", value: 2500, label: "DEFENSORES JAPONESES", color: "red", at: 14 },
        { kind: "caption", text: "Mortero estadounidense en Attu, mayo de 1943", at: 14 },
      ],
    },
    {
      from: 15,
      visual: {
        kind: "map",
        from: { center: [175.5, 52.4], scale: 5000 },
        to: { center: KISKA, scale: 20000 },
        markers: [{ at: KISKA, label: "OBJETIVO: KISKA", color: "red", appear: 0.3 }],
      },
    },
    {
      from: 16,
      visual: { kind: "photo", src: H + "cruiser_attacked.jpg", zoom: [1.0, 1.2], focus: [0.5, 0.5] },
      overlays: [
        { kind: "stat", value: 5000, prefix: "+", label: "JAPONESES ESTIMADOS", color: "amber", at: 16 },
        { kind: "caption", text: "Foto aérea de reconocimiento, Kiska 1943" },
      ],
    },
    {
      from: 17,
      visual: { kind: "photo", src: H + "planning.jpg", zoom: [1.06, 1.16], focus: [0.45, 0.5] },
      overlays: [{ kind: "caption", text: "Planificando la expedición a Kiska", source: "Foto de archivo · US Navy · Dominio público" }],
    },
    {
      from: 19,
      visual: { kind: "photo", src: H + "invasion_fleet.jpg", zoom: [1.0, 1.14], focus: [0.6, 0.55] },
      overlays: [
        { kind: "stat", value: 34400, label: "SOLDADOS", color: "amber" },
        { kind: "stat", value: 100, label: "BARCOS DE GUERRA", color: "cream", slot: 1, at: 19 },
        { kind: "caption", text: "La flota de invasión, agosto de 1943" },
      ],
    },
    {
      from: 20,
      visual: { kind: "photo", src: H + "pby_snow.jpg", zoom: [1.05, 1.2], focus: [0.4, 0.5], fog: 0.55, dim: 0.15 },
      overlays: [{ kind: "title", text: "Bajo la niebla", color: "cream", at: 21 }],
    },
    // La batalla de los puntos fantasma
    {
      from: 22,
      visual: { kind: "photo", src: H + "uss_mississippi.jpg", zoom: [1.04, 1.16], focus: [0.45, 0.6] },
      overlays: [
        { kind: "ribbon", text: "26 DE JULIO DE 1943" },
        { kind: "caption", text: "USS Mississippi en Adak, mayo de 1943" },
      ],
    },
    {
      from: 23,
      visual: { kind: "radar", blips: true },
      overlays: [{ kind: "title", text: "7 ecos en el radar", color: "amber", low: true }],
    },
    {
      from: 24,
      visual: { kind: "photo", src: H + "cruisers_off_kiska.jpg", zoom: [1.04, 1.18], focus: [0.5, 0.4], flashes: true },
      overlays: [
        { kind: "stat", value: 1000, prefix: "+", label: "PROYECTILES AL MAR VACÍO", color: "amber" },
        { kind: "caption", text: "Cruceros de EE. UU. frente a Kiska, 1943" },
      ],
    },
    {
      from: 25,
      visual: { kind: "radar", blips: false },
      overlays: [{ kind: "title", text: "Los puntos fantasma", color: "amber", at: 26, low: true }],
    },
    {
      from: 27,
      visual: {
        kind: "map",
        from: { center: [179.2, 51.8], scale: 6500 },
        to: { center: [179.8, 51.7], scale: 5800 },
        arrows: [{ path: [[177.0, 51.5], [179.5, 51.3], [-178.2, 51.5]], color: "blue", ships: true, appear: 0.2, duration: 6 }],
        markers: [{ at: KISKA, label: "KISKA", color: "red", pulse: false, side: "left" }],
        fog: 0.25,
      },
    },
    // Kimura
    {
      from: 29,
      visual: { kind: "photo", src: A + "masatomi_kimura.jpg", portrait: true, zoom: [1.0, 1.06], focus: [0.5, 0.35] },
      overlays: [{ kind: "caption", text: "Contraalmirante Masatomi Kimura" }],
    },
    {
      from: 30,
      visual: { kind: "photo", src: A + "kiska_japanese.jpg", zoom: [1.25, 1.35], focus: [0.25, 0.5], dim: 0.25 },
      overlays: [{ kind: "title", text: "La vida primero", color: "amber" }],
    },
    {
      from: 31,
      visual: {
        kind: "map",
        from: { center: [175.8, 51.6], scale: 7500 },
        to: { center: [176.4, 51.75], scale: 9500 },
        arrows: [
          { path: [[172.5, 53.6], [175.3, 52.9], [177.5, 52.02]], color: "red", ships: true, appear: 0.3, duration: 3.4 },
          { path: [[177.5, 52.02], [175.6, 53.2], [172.5, 54.0]], color: "red", ships: true, appear: 7.4, duration: 2.6 },
        ],
        markers: [{ at: KISKA, label: "KISKA", color: "red", appear: 0 }],
        fog: 0.6,
      },
      overlays: [
        { kind: "ribbon", text: "28 DE JULIO DE 1943" },
        { kind: "stat", value: 5183, label: "SOLDADOS EVACUADOS", color: "red", at: 33 },
        { kind: "stat", value: 55, label: "MINUTOS", color: "amber", slot: 1, at: 34 },
        { kind: "title", text: "Sin dejar rastro", color: "cream", at: 35 },
      ],
    },
    // Bombas sobre la nada
    {
      from: 36,
      visual: { kind: "photo", src: H + "pv1_bombs.jpg", zoom: [1.05, 1.15], focus: [0.4, 0.5] },
      overlays: [
        { kind: "ribbon", text: "AGOSTO DE 1943" },
        { kind: "caption", text: "Cargando bombas en un PV-1 Ventura, Aleutianas" },
      ],
    },
    {
      from: 37,
      visual: { kind: "photo", src: A + "b24_aleutians.jpg", zoom: [1.08, 1.18], focus: [0.4, 0.5] },
      overlays: [
        { kind: "title", text: "Campamentos vacíos", color: "amber" },
        { kind: "caption", text: "B-24 Liberator en Amchitka, marzo de 1943" },
      ],
    },
    {
      from: 38,
      visual: { kind: "photo", src: H + "kiska_bombed_1943.jpg", zoom: [1.3, 1.5], focus: [0.4, 0.6], flashes: true },
      overlays: [{ kind: "title", text: "Sus propias bombas", color: "red", at: 40 }],
    },
    // El desembarco
    {
      from: 41,
      visual: { kind: "photo", src: H + "allied_landing.jpg", zoom: [1.04, 1.16], focus: [0.35, 0.6], fog: 0.2 },
      overlays: [
        { kind: "ribbon", text: "15 DE AGOSTO DE 1943" },
        { kind: "stat", value: 34000, label: "SOLDADOS ALIADOS", color: "amber" },
        { kind: "caption", text: "Desembarco aliado en Kiska, 15-8-1943" },
      ],
    },
    {
      from: 42,
      visual: { kind: "photo", src: H + "troops_loading.jpg", zoom: [1.3, 1.4], focus: [0.3, 0.7], fog: 0.65, dim: 0.3 },
      overlays: [{ kind: "title", text: "El miedo", color: "cream" }],
    },
    {
      from: 43,
      visual: {
        kind: "map",
        from: { center: [177.5, 52.0], scale: 26000 },
        to: { center: [177.48, 52.02], scale: 32000 },
        crossfire: [177.45, 52.03],
        fog: 0.4,
      },
      overlays: [{ kind: "title", text: "Fuego amigo", color: "red", at: 44, low: true }],
    },
    {
      from: 45,
      visual: { kind: "photo", src: H + "lily_beach_guns.jpg", zoom: [1.05, 1.15], focus: [0.5, 0.45] },
      overlays: [
        { kind: "title", text: "Minas", color: "red" },
        { kind: "caption", text: "Lily Beach, Kiska, 16-8-1943" },
      ],
    },
    {
      from: 46,
      visual: { kind: "photo", src: A + "abner_read.jpg", zoom: [1.1, 1.22], focus: [0.4, 0.5] },
      overlays: [
        { kind: "caption", text: "USS Abner Read (DD-526), junio de 1943" },
        { kind: "title", text: "Le arranca la popa", color: "red", at: 47 },
      ],
    },
    {
      from: 48,
      visual: { kind: "photo", src: A + "kiska_bunkers.jpg", zoom: [1.2, 1.3], focus: [0.4, 0.6] },
      overlays: [{ kind: "caption", text: "Instalaciones japonesas abandonadas en Kiska" }],
    },
    {
      from: 49,
      visual: { kind: "photo", src: H + "phone_shack.jpg", zoom: [1.04, 1.14], focus: [0.4, 0.6] },
      overlays: [
        { kind: "stat", value: 4, label: "PERROS ABANDONADOS", color: "amber" },
        { kind: "caption", text: "Puesto telefónico japonés tomado por EE. UU." },
      ],
    },
    // Balance
    {
      from: 50,
      visual: { kind: "photo", src: H + "cruisers_off_kiska.jpg", zoom: [1.3, 1.4], focus: [0.5, 0.3], fog: 0.5, dim: 0.35 },
      overlays: [{ kind: "title", text: "Un combate contra nada", color: "cream" }],
    },
    {
      from: 51,
      visual: { kind: "photo", src: H + "allied_landing.jpg", zoom: [1.25, 1.35], focus: [0.6, 0.4], dim: 0.45 },
      overlays: [
        { kind: "stat", value: 90, prefix: "+", label: "MUERTOS EN TIERRA", color: "red" },
        { kind: "stat", value: 70, label: "MUERTOS EN EL ABNER READ", color: "red", slot: 1, at: 52 },
        { kind: "stat", value: 200, label: "HERIDOS", color: "amber", slot: 2, at: 53 },
      ],
    },
    {
      from: 54,
      visual: { kind: "photo", src: H + "lily_beach_guns.jpg", zoom: [1.25, 1.4], focus: [0.7, 0.4], fog: 0.6, dim: 0.2 },
      overlays: [{ kind: "title", text: "34.000 contra la niebla", color: "cream" }],
    },
    // Cierre
    {
      from: 55,
      visual: { kind: "dilemma", background: A + "kiska_japanese.jpg", aAt: 56, bAt: 57, footerAt: 58 },
    },
  ],
};
