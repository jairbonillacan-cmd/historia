import timeline from "../../../produccion/14_operacion_bernhard/timeline_chunks.json";
import type { Pt, Timeline, VideoPlan } from "../engine/types";

// AG-22 · Operación Bernhard (1942). Cada entrada arranca en la cláusula `from` (o en su palabra `word`)
// de timeline_chunks.json. Los cortes van sobre la palabra clave para que el ritmo siga a la voz.
const A = "assets/";
const TL = timeline as Timeline;
const BUNDESARCHIV = "Bundesarchiv, Bild 101I-567-1503A-07 · Toni Schneiders · CC BY-SA 3.0 DE";

// Segundos desde el inicio de la cláusula `i` hasta su palabra `k` (para marcas dentro de una escena).
const since = (i: number, k: number, from = i, fromWord?: number) => {
  const c = (n: number) => TL.chunks.find((x) => x.index === n)!;
  const t0 = fromWord === undefined ? c(from).start : c(from).words[fromWord].start;
  return Math.round((c(i).words[k].start - t0) * 100) / 100;
};

const SACHSENHAUSEN: Pt = [13.26, 52.77];
const LONDON: Pt = [-0.13, 51.5];
const AUSCHWITZ: Pt = [19.2, 50.03];
const BUCHENWALD: Pt = [11.25, 51.02];
const DACHAU: Pt = [11.47, 48.27];
const MAUTHAUSEN: Pt = [14.5, 48.26];
const ANATOLIA: Pt = [32.5, 39.5];

export const bernhard: VideoPlan = {
  folder: "14_operacion_bernhard",
  audio: "audio/audio_master_final.wav", // voz (npm run mute:bernhard) + música y efectos (build_music_and_sfx_bernhard.py)
  timeline: TL,
  endCta: { question: "¿Qué habrías hecho vos?", a: "ESTIRAR", b: "NEGARME", footer: "Dejame tu respuesta 👇" },
  items: [
    // ── Gancho: un corte cada ~1,5–2 s ──
    {
      from: 1,
      visual: { kind: "banknote", mode: "inspect" },
      overlays: [
        { kind: "impact", strength: 1.2 },
        { kind: "ribbon", text: "UN BILLETE PERFECTO" },
      ],
    },
    {
      from: 1,
      word: 8,
      visual: { kind: "photo", src: A + "note50.jpg", zoom: [1.1, 1.3], focus: [0.5, 0.5] },
      overlays: [{ kind: "slam", text: "£50", color: "amber", size: 220 }],
    },
    {
      from: 2,
      visual: { kind: "photo", src: A + "note10_museo.jpg", zoom: [1.2, 1.38], focus: [0.45, 0.45] },
      overlays: [{ kind: "slam", text: "Exacto", color: "cream", at: 2, word: 5 }],
    },
    {
      from: 3,
      visual: { kind: "photo", src: A + "note50_trasluz.jpg", zoom: [1.05, 1.25], focus: [0.2, 0.6] },
      overlays: [{ kind: "title", text: "Al trasluz", color: "amber", at: 3, word: 4 }],
    },
    {
      from: 3,
      word: 8,
      visual: {
        kind: "banknote",
        mode: "backlight",
        marks: [
          { part: "watermark", label: "MARCA DE AGUA", at: 0.2, side: "down" },
          { part: "pinhole", label: "AGUJERO DE ALFILER", at: since(3, 14, 3, 8), color: "red", side: "up" },
        ],
      },
    },
    {
      from: 4,
      visual: { kind: "photo", src: A + "boe.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.4] },
      overlays: [{ kind: "title", text: "Como los de Londres", color: "cream", at: 4, word: 3 }],
    },
    {
      from: 5,
      visual: { kind: "photo", src: A + "britannia.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.5, 0.4] },
      overlays: [
        { kind: "stamp", text: "FALSO", color: "red", at: 5, word: 5 },
        { kind: "impact", strength: 0.7, at: 5, word: 5 },
      ],
    },
    {
      from: 6,
      visual: { kind: "photo", src: A + "sachs_barracks.jpg", zoom: [1.05, 1.22], focus: [0.4, 0.5] },
      overlays: [{ kind: "title", text: "Alambre de púas", color: "cream", at: 6, word: 6 }],
    },
    {
      from: 6,
      word: 10,
      visual: { kind: "photo", src: A + "sachs_aerial.jpg", zoom: [1.1, 1.35], focus: [0.5, 0.5] },
      overlays: [
        { kind: "impact" },
        { kind: "slam", text: "Alemania", color: "red" },
        { kind: "caption", text: "Foto aérea del campo de Sachsenhausen", source: "RAF · dominio público" },
      ],
    },
    // ── El plan ──
    {
      from: 7,
      visual: {
        kind: "map",
        from: { center: [8, 52], scale: 1500 },
        to: { center: [12, 52.5], scale: 2300 },
        highlight: [{ country: "germany", color: "red" }],
        markers: [{ at: SACHSENHAUSEN, label: "SACHSENHAUSEN", color: "red", appear: 1.4 }],
      },
      overlays: [{ kind: "ribbon", text: "ALEMANIA · 1942" }],
    },
    {
      from: 7,
      word: 10,
      visual: { kind: "photo", src: A + "note20_pmg.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.45] },
      overlays: [{ kind: "title", text: "La mayor falsificación de la historia", color: "amber" }],
    },
    {
      from: 8,
      visual: { kind: "photo", src: A + "note50.jpg", zoom: [1.3, 1.45], focus: [0.3, 0.4] },
      overlays: [{ kind: "slam", text: "Operación Bernhard", color: "amber", size: 104, at: 8, word: 1 }],
    },
    {
      from: 8,
      word: 9,
      visual: { kind: "photo", src: A + "kruger.jpg", portrait: true, zoom: [1.0, 1.1], focus: [0.75, 0.4] },
      overlays: [
        { kind: "title", text: "Bernhard Krüger", color: "red", low: true, at: 8, word: 10 },
        { kind: "caption", text: "Bernhard Krüger, mayor de las SS, detenido después de la guerra" },
      ],
    },
    {
      from: 9,
      visual: { kind: "photo", src: A + "he111_formation.jpg", zoom: [1.1, 1.25], focus: [0.5, 0.5] },
      overlays: [{ kind: "title", text: "Simple y letal", color: "red", at: 9, word: 5 }],
    },
    {
      from: 10,
      visual: { kind: "banknote", mode: "press" },
      overlays: [{ kind: "title", text: "Millones de libras falsas", color: "amber", low: true, at: 10, word: 1 }],
    },
    {
      from: 10,
      word: 7,
      visual: { kind: "photo", src: A + "he111_london.jpg", zoom: [1.05, 1.25], focus: [0.4, 0.4] },
      overlays: [
        { kind: "caption", text: "Heinkel He 111 sobre el Támesis, Londres", source: "Luftwaffe · dominio público" },
        { kind: "reticle", x: 500, y: 760, lock: 1.0 },
      ],
    },
    {
      from: 10,
      word: 13,
      visual: { kind: "banknote", mode: "rain", background: A + "london_1942.jpg" },
      overlays: [{ kind: "title", text: "Que nadie confíe en su dinero", color: "cream", at: 10, word: 16 }],
    },
    {
      from: 10,
      word: 25,
      visual: {
        kind: "map",
        from: { center: [2, 53], scale: 2600 },
        to: { center: [-1, 53], scale: 3400 },
        highlight: [{ country: "uk", color: "red" }],
        markers: [{ at: LONDON, label: "LONDRES", color: "red", appear: 0.3 }],
      },
      overlays: [
        { kind: "impact", strength: 1.2, at: 10, word: 27 },
        { kind: "slam", text: "Hiperinflación", color: "red", size: 110, at: 10, word: 28 },
      ],
    },
    // ── Los prisioneros ──
    {
      from: 11,
      visual: { kind: "photo", src: A + "britannia.jpg", portrait: true, zoom: [1.15, 1.3], focus: [0.5, 0.3] },
      overlays: [{ kind: "title", text: "Los mejores de Europa", color: "amber", low: true, at: 11, word: 5 }],
    },
    {
      from: 12,
      visual: {
        kind: "map",
        from: { center: [14, 51], scale: 2300 },
        to: { center: [14.5, 50.5], scale: 2600 },
        highlight: [{ country: "germany", color: "red" }],
        markers: [
          { at: SACHSENHAUSEN, label: "SACHSENHAUSEN", color: "red", appear: 0.3 },
          { at: BUCHENWALD, label: "BUCHENWALD", color: "amber", appear: 0.9, side: "left", pulse: false },
          { at: AUSCHWITZ, label: "AUSCHWITZ", color: "amber", appear: 1.4, pulse: false },
          { at: DACHAU, label: "DACHAU", color: "amber", appear: 1.9, side: "left", pulse: false },
          { at: MAUTHAUSEN, label: "MAUTHAUSEN", color: "amber", appear: 2.3, pulse: false },
        ],
      },
      overlays: [{ kind: "ribbon", text: "KRÜGER RECORRE LOS CAMPOS" }],
    },
    {
      from: 12,
      word: 9,
      visual: { kind: "photo", src: A + "sachs_interior.jpg", zoom: [1.05, 1.18], focus: [0.5, 0.5], dim: 0.25 },
      overlays: [{ kind: "stat", value: 142, label: "PRISIONEROS JUDÍOS", color: "amber" }],
    },
    {
      from: 13,
      visual: { kind: "photo", src: A + "note20_pmg.jpg", zoom: [1.3, 1.4], focus: [0.5, 0.6], dim: 0.55 },
      overlays: [
        {
          kind: "options",
          items: ["Grabadores", "Impresores", "Matemáticos", "Químicos", "Banqueros"],
          times: [0, since(13, 1), since(13, 2), since(13, 3), since(13, 5)],
        },
      ],
    },
    {
      from: 14,
      visual: { kind: "photo", src: A + "note50.jpg", zoom: [1.6, 1.8], focus: [0.12, 0.3] },
      overlays: [
        { kind: "title", text: "Salomon Smolianoff", color: "amber", at: 14, word: 3 },
        { kind: "slam", text: "El mejor falsificador", color: "cream", size: 96, y: 1150, at: 14, word: 10 },
      ],
    },
    {
      from: 15,
      visual: { kind: "photo", src: A + "sachs_aerial.jpg", zoom: [1.2, 1.45], focus: [0.45, 0.45] },
      overlays: [
        { kind: "ribbon", text: "SACHSENHAUSEN · BLOQUES 18 Y 19" },
        { kind: "spotlight", x: 540, y: 1000, r: 160, label: "BLOQUES 18 Y 19", color: "red", at: 15, word: 4 },
      ],
    },
    {
      from: 15,
      word: 12,
      visual: { kind: "photo", src: A + "sachs_barracks.jpg", zoom: [1.2, 1.35], focus: [0.6, 0.5], dim: 0.2 },
      overlays: [{ kind: "stamp", text: "SECRETO ABSOLUTO", color: "red" }],
    },
    // ── El equilibrio ──
    {
      from: 16,
      visual: { kind: "photo", src: A + "sachs_interior.jpg", zoom: [1.15, 1.3], focus: [0.4, 0.5], dim: 0.3 },
      overlays: [
        { kind: "redpulse", bpm: 70 },
        { kind: "title", text: "Un equilibrio aterrador", color: "red", at: 16, word: 7 },
      ],
    },
    {
      from: 17,
      visual: { kind: "photo", src: A + "note50_trasluz.jpg", zoom: [1.1, 1.2], focus: [0.5, 0.5], dim: 0.5 },
      overlays: [{ kind: "countdown", hours: 12, dur: 3.0, label: "MIENTRAS TARDEN, VIVEN" }],
    },
    {
      from: 18,
      visual: { kind: "photo", src: A + "sachs_barracks.jpg", zoom: [1.0, 1.12], focus: [0.3, 0.5], dim: 0.55 },
      overlays: [
        {
          kind: "options",
          title: "SI…",
          items: ["Fracasan", "Terminan rápido"],
          times: [since(18, 2), since(18, 5)],
          crossAt: since(19, 3, 18),
        },
      ],
    },
    {
      from: 19,
      word: 4,
      visual: { kind: "photo", src: A + "sachs_aerial.jpg", zoom: [1.3, 1.5], focus: [0.5, 0.5], dim: 0.35, fog: 0.4 },
      overlays: [
        { kind: "impact", strength: 1.1, at: 19, word: 5 },
        { kind: "slam", text: "Borrar las pruebas", color: "red", size: 100, at: 19, word: 5 },
      ],
    },
    // ── Los tres secretos ──
    {
      from: 20,
      visual: { kind: "photo", src: A + "boe.jpg", zoom: [1.15, 1.3], focus: [0.5, 0.35] },
      overlays: [{ kind: "stat", value: 3, label: "SECRETOS DEL BANCO DE INGLATERRA", color: "amber", at: 20, word: 4 }],
    },
    {
      from: 21,
      visual: {
        kind: "banknote",
        mode: "inspect",
        marks: [{ part: "paper", label: "TRAPOS DE LINO", at: since(21, 7), side: "down" }],
      },
    },
    {
      from: 21,
      word: 10,
      visual: {
        kind: "map",
        from: { center: [22, 46], scale: 1150 },
        to: { center: [23, 45.5], scale: 1250 },
        highlight: [
          { country: "turkey", color: "amber" },
          { country: "germany", color: "red" },
        ],
        arrows: [{ path: [ANATOLIA, [24, 45], SACHSENHAUSEN], color: "amber", appear: 0.3, duration: 1.4 }],
        markers: [
          { at: ANATOLIA, label: "TURQUÍA", color: "amber", appear: 0.2, pulse: false },
          { at: SACHSENHAUSEN, label: "SACHSENHAUSEN", color: "red", appear: 1.5, side: "left" },
        ],
      },
    },
    {
      from: 22,
      visual: {
        kind: "banknote",
        mode: "backlight",
        marks: [{ part: "watermark", label: "COPIADA A MANO", at: since(22, 2), side: "down" }],
      },
    },
    {
      from: 22,
      word: 8,
      visual: { kind: "photo", src: A + "note50.jpg", zoom: [1.5, 1.7], focus: [0.25, 0.22] },
      overlays: [
        { kind: "title", text: "El algoritmo de las series", color: "amber", at: 22, word: 10 },
        { kind: "spotlight", x: 330, y: 1000, r: 150, label: "Nº DE SERIE", color: "amber", at: 22, word: 16 },
      ],
    },
    {
      from: 23,
      visual: { kind: "photo", src: A + "note10_museo.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5] },
      overlays: [{ kind: "title", text: "Envejecidos a mano", color: "cream", at: 23, word: 1 }],
    },
    {
      from: 23,
      word: 10,
      visual: { kind: "photo", src: A + "note50_trasluz.jpg", zoom: [1.2, 1.4], focus: [0.6, 0.5] },
      overlays: [{ kind: "slam", text: "Uno por uno", color: "cream", at: 23, word: 11 }],
    },
    {
      from: 24,
      visual: {
        kind: "banknote",
        mode: "inspect",
        marks: [
          { part: "pinhole", label: "ALFILERES", at: since(24, 4), color: "red", side: "up" },
          { part: "signature", label: "DOBLADOS", at: since(24, 1), side: "down" },
        ],
      },
    },
    {
      from: 25,
      visual: { kind: "photo", src: A + "boe.jpg", zoom: [1.3, 1.45], focus: [0.5, 0.6] },
      overlays: [{ kind: "title", text: "Como los cajeros ingleses", color: "cream", at: 25, word: 3 }],
    },
    // ── El resultado ──
    {
      from: 26,
      visual: { kind: "photo", src: A + "note20_pmg.jpg", zoom: [1.0, 1.15], focus: [0.5, 0.5] },
      overlays: [
        { kind: "caption", text: "Billete de £20 de la Operación Bernhard, certificado como falsificación", source: "Dominio público" },
        { kind: "impact", strength: 1.0, at: 26, word: 13 },
        { kind: "slam", text: "Indetectables", color: "red", y: 1150, at: 26, word: 13 },
      ],
    },
    {
      from: 27,
      visual: { kind: "banknote", mode: "press" },
      overlays: [
        { kind: "stat", value: 9, suffix: " MILLONES", label: "DE BILLETES", color: "cream", slot: 0, at: 27, word: 2 },
        { kind: "stat", value: 134, prefix: "£", suffix: " MILLONES", label: "EN LIBRAS FALSAS", color: "amber", slot: 1, at: 27, word: 10 },
      ],
    },
    {
      from: 28,
      visual: { kind: "banknote", mode: "rain", background: A + "london_1942b.jpg" },
      overlays: [{ kind: "stat", value: 10, prefix: "+", suffix: "%", label: "DEL EFECTIVO BRITÁNICO", color: "red", at: 28, word: 2 }],
    },
    {
      from: 29,
      visual: { kind: "photo", src: A + "note10_museo.jpg", zoom: [1.25, 1.4], focus: [0.5, 0.5] },
      overlays: [
        { kind: "title", text: "Para pagar espías", color: "amber", at: 29, word: 4 },
        { kind: "caption", text: "Libra de la Operación Bernhard en el Museo Internacional del Espía", source: "Joyofmuseums · CC BY-SA 4.0" },
      ],
    },
    {
      from: 30,
      word: 3,
      visual: { kind: "photo", src: A + "gransasso.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.45] },
      overlays: [
        { kind: "caption", text: "Rescate de Mussolini en el Gran Sasso, 1943", source: BUNDESARCHIV },
        { kind: "title", text: "El rescate de Mussolini", color: "cream", at: 30, word: 5 },
      ],
    },
    // ── El dólar y el sabotaje ──
    {
      from: 31,
      visual: { kind: "photo", src: A + "dollar_1934.jpg", zoom: [1.05, 1.25], focus: [0.5, 0.5] },
      overlays: [
        { kind: "ribbon", text: "1944" },
        { kind: "slam", text: "El dólar", color: "amber", y: 1250, at: 31, word: 9 },
      ],
    },
    {
      from: 32,
      visual: { kind: "photo", src: A + "sachs_interior.jpg", zoom: [1.1, 1.25], focus: [0.6, 0.5], dim: 0.2 },
      overlays: [
        { kind: "impact", strength: 0.8, at: 32, word: 4 },
        { kind: "slam", text: "Sabotaje", color: "amber", at: 32, word: 4 },
      ],
    },
    {
      from: 33,
      visual: { kind: "banknote", mode: "press" },
      overlays: [
        { kind: "redpulse", bpm: 66 },
        { kind: "title", text: "Ganar tiempo", color: "amber", low: true, at: 33, word: 6 },
      ],
    },
    {
      from: 34,
      visual: {
        kind: "timeline",
        title: "OPERACIÓN BERNHARD",
        events: [
          { date: "1942", label: "Empiezan las libras", at: 0.2 },
          { date: "1944", label: "Les ordenan el dólar", at: 0.8, color: "red" },
          { date: "MAYO 1945", label: "Liberan el campo", at: since(34, 6), color: "blue" },
        ],
      },
    },
    // ── Epílogo ──
    {
      from: 35,
      visual: { kind: "photo", src: A + "boe.jpg", zoom: [1.0, 1.15], focus: [0.5, 0.4] },
      overlays: [{ kind: "title", text: "Al terminar la guerra", color: "cream", at: 35, word: 1 }],
    },
    {
      from: 35,
      word: 10,
      visual: { kind: "banknote", mode: "inspect" },
      overlays: [
        { kind: "stamp", text: "RETIRADO", color: "red", y: 1000, delay: 0.3 },
        { kind: "title", text: "Todos los mayores de £5", color: "cream", low: true, at: 35, word: 15 },
      ],
    },
    {
      from: 36,
      visual: { kind: "photo", src: A + "sachs_barracks.jpg", zoom: [1.05, 1.15], focus: [0.5, 0.5], dim: 0.25 },
      overlays: [{ kind: "stat", value: 142, label: "PRISIONEROS", color: "amber", at: 36, word: 3 }],
    },
    // ── Cierre ──
    {
      from: 37,
      visual: { kind: "dilemma", background: A + "sachs_interior.jpg", aAt: 37, bAt: 38, footerAt: 38 },
    },
  ],
};
