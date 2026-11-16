import timeline from "../../../produccion/11_motin_kiel/timeline_chunks.json";
import type { Pt, Timeline, VideoPlan } from "../engine/types";

// AG-19 · Motín de Kiel (1918). Cada entrada arranca en la cláusula `from` (o en su palabra `word`)
// de timeline_chunks.json. Los `impact` caen sobre los golpes de build_music_and_sfx_kiel.py.
const A = "assets/";
const BUNDESARCHIV = (id: string) => `Bundesarchiv, Bild ${id} · CC BY-SA 3.0 DE`;
const MEYER = "Foto: Ernst Meyer · Stadtarchiv Kiel · CC BY-SA 3.0 DE";

const KIEL: Pt = [10.13, 54.32];
const WILHELMSHAVEN: Pt = [8.12, 53.52];
const BERLIN: Pt = [13.4, 52.52];
const THAMES: Pt = [1.2, 51.7];
const JUTLAND: Pt = [6.1, 56.7];
const HAMBURG: Pt = [9.99, 53.55];
const COLOGNE: Pt = [6.96, 50.94];
const MUNICH: Pt = [11.58, 48.14];

const NORTH_SEA = { center: [6, 54.6] as Pt, scale: 2200 };

export const kiel: VideoPlan = {
  folder: "11_motin_kiel",
  audio: "audio/audio_master_final.wav", // voz censurada (npm run mute:kiel) + música y efectos (build_music_and_sfx_kiel.py)
  timeline: timeline as Timeline,
  progress: true,
  endCta: { question: "¿Dónde termina la obediencia?", a: "ACATAR", b: "NEGARSE", footer: "Dejame tu respuesta 👇" },
  items: [
    // ── Gancho: un corte cada ~1,5–2 s ──
    {
      from: 1,
      visual: { kind: "photo", src: A + "fogoneros.jpg", zoom: [1.25, 1.1], focus: [0.5, 0.6], flashes: true },
      overlays: [
        { kind: "caption", text: "Sala de calderas de un acorazado, 1917", source: "Dibujo de Muirhead Bone · Dominio público" },
        { kind: "impact", strength: 1.2 },
        { kind: "ribbon", text: "MAR DEL NORTE · 1918" },
        { kind: "impact", strength: 0.7, at: 1, word: 5, delay: 0.15 },
      ],
    },
    {
      from: 1,
      word: 10,
      visual: { kind: "boiler", from: 14, to: 14, label: "SALA DE MÁQUINAS" },
    },
    {
      from: 2,
      visual: { kind: "photo", src: A + "consejo_marineros.jpg", zoom: [1.15, 1.3], focus: [0.4, 0.45] },
      overlays: [{ kind: "slam", text: "Brazos cruzados", color: "amber", at: 2, word: 3 }],
    },
    {
      from: 2,
      word: 7,
      visual: { kind: "boiler", from: 14, to: 0, dropAt: 0.2, dropDur: 1.6, label: "APAGAN EL FUEGO" },
    },
    {
      from: 3,
      visual: { kind: "fleet", mode: "port", smoke: false, ships: 3 },
      overlays: [{ kind: "title", text: "Un gesto silencioso", color: "cream" }],
    },
    {
      from: 3,
      word: 5,
      visual: { kind: "photo", src: A + "thuringen.jpg", zoom: [1.3, 1.45], focus: [0.5, 0.55] },
    },
    {
      from: 4,
      visual: { kind: "photo", src: A + "kaiser.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.5, 0.25], dim: 0.1 },
      overlays: [
        { kind: "impact", at: 4, word: 4 },
        { kind: "slam", text: "Un emperador", color: "red", y: 1320, at: 4, word: 4 },
      ],
    },
    // ── Contexto ──
    {
      from: 5,
      visual: {
        kind: "map",
        from: { center: [10, 52], scale: 1600 },
        to: { center: [8.5, 54], scale: 2300 },
        highlight: [{ country: "germany", color: "red" }],
        markers: [
          { at: WILHELMSHAVEN, label: "WILHELMSHAVEN", color: "amber", appear: 1.0, side: "left" },
          { at: KIEL, label: "KIEL", color: "red", appear: 1.4 },
        ],
      },
      overlays: [{ kind: "ribbon", text: "PRIMERA GUERRA MUNDIAL" }],
    },
    {
      from: 6,
      visual: { kind: "photo", src: A + "hochseeflotte.jpg", portrait: true, zoom: [1.05, 1.2], focus: [0.6, 0.5] },
      overlays: [
        { kind: "title", text: "Flota de Alta Mar", color: "amber" },
        { kind: "caption", text: "La Flota de Alta Mar alemana en formación" },
      ],
    },
    {
      from: 6,
      word: 11,
      visual: { kind: "photo", src: A + "kaiser_marina.jpg", portrait: true, zoom: [1.05, 1.15], focus: [0.5, 0.3] },
      overlays: [{ kind: "slam", text: "Guillermo II", color: "cream", y: 1320 }],
    },
    {
      from: 7,
      visual: { kind: "photo", src: A + "jutlandia.jpg", zoom: [1.05, 1.25], focus: [0.5, 0.5], flashes: true },
      overlays: [
        { kind: "ribbon", text: "JUTLANDIA · 1916" },
        { kind: "impact", strength: 0.8, at: 7, word: 7 },
      ],
    },
    {
      from: 8,
      visual: {
        kind: "map",
        from: NORTH_SEA,
        to: { center: [6.5, 54.2], scale: 2600 },
        highlight: [
          { country: "uk", color: "blue" },
          { country: "germany", color: "red" },
        ],
        arrows: [
          { path: [[-2.5, 58.5], [3.5, 57.5], [5.5, 55.5]], color: "blue", appear: 0.6, duration: 1.4, ships: true },
          { path: [[1.5, 51.4], [3.2, 53.2], [5.2, 54.3]], color: "blue", appear: 1.0, duration: 1.4, ships: true },
        ],
        markers: [
          { at: WILHELMSHAVEN, label: "FLOTA ALEMANA", color: "red", appear: 0.2 },
          { at: JUTLAND, label: "JUTLANDIA", color: "amber", appear: 0.4, pulse: false, side: "left" },
        ],
      },
      overlays: [{ kind: "stat", value: 2, label: "AÑOS ENCERRADOS EN PUERTO", color: "amber", at: 8, word: 4 }],
    },
    {
      from: 9,
      visual: { kind: "photo", src: A + "grand_fleet.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5] },
      overlays: [{ kind: "title", text: "El bloqueo británico", color: "blue", at: 9, word: 3 }],
    },
    {
      from: 10,
      visual: {
        kind: "map",
        from: { center: [5, 50.5], scale: 2600 },
        to: { center: [4.2, 49.8], scale: 3200 },
        highlight: [
          { country: "france", color: "blue" },
          { country: "germany", color: "red" },
        ],
        arrows: [
          { path: [[2.3, 50.3], [3.6, 50.4], [4.6, 50.5]], color: "blue", appear: 0.3, duration: 1.4 },
          { path: [[2.6, 49.3], [3.8, 49.5], [4.9, 49.7]], color: "blue", appear: 0.6, duration: 1.4 },
          { path: [[3.4, 48.7], [4.6, 49.0], [5.6, 49.2]], color: "blue", appear: 0.9, duration: 1.4 },
        ],
        markers: [{ at: [4.9, 49.7], label: "FRENTE OCCIDENTAL", color: "red", appear: 1.5 }],
      },
      overlays: [
        { kind: "ribbon", text: "OCTUBRE DE 1918" },
        { kind: "slam", text: "No da más", color: "red", at: 10, word: 8 },
      ],
    },
    {
      from: 11,
      visual: { kind: "photo", src: A + "berlin_gobierno.jpg", portrait: true, zoom: [1.0, 1.1], focus: [0.5, 0.3] },
      overlays: [
        { kind: "caption", text: "Max von Baden, canciller desde octubre de 1918" },
        { kind: "slam", text: "Armisticio", color: "amber", y: 1250, at: 11, word: 9 },
      ],
    },
    {
      from: 12,
      visual: { kind: "photo", src: A + "armisticio.jpg", portrait: true, zoom: [1.0, 1.1], focus: [0.5, 0.5], dim: 0.2 },
      overlays: [{ kind: "stamp", text: "Guerra perdida", y: 1200, at: 12, word: 3 }],
    },
    // ── Los almirantes ──
    {
      from: 13,
      visual: { kind: "fleet", mode: "port", smoke: true, ships: 4 },
      overlays: [{ kind: "ribbon", text: "ALTO MANDO NAVAL" }],
    },
    {
      from: 14,
      visual: {
        kind: "versus",
        left: { src: A + "scheer.jpg", name: "Reinhard Scheer", lines: ["JEFE DEL ESTADO", "MAYOR NAVAL"], color: "amber", focus: [0.5, 0.3] },
        right: { src: A + "hipper.jpg", name: "Franz von Hipper", lines: ["COMANDANTE DE", "LA FLOTA"], color: "red", focus: [0.5, 0.25] },
      },
    },
    {
      from: 15,
      visual: { kind: "photo", src: A + "helgoland.jpg", zoom: [1.15, 1.3], focus: [0.55, 0.5] },
      overlays: [{ kind: "slam", text: "Intactos", color: "amber", at: 15, word: 8 }],
    },
    {
      from: 15,
      word: 11,
      visual: { kind: "photo", src: A + "grand_fleet.jpg", zoom: [1.25, 1.4], focus: [0.4, 0.5], dim: 0.15 },
      overlays: [{ kind: "title", text: "Sin haber peleado", color: "cream" }],
    },
    {
      from: 16,
      visual: {
        kind: "quote",
        text: "Orden de Operaciones N.º 19: toda la flota contra la Marina británica.",
        author: "Mando Naval, octubre de 1918",
        background: A + "hochseeflotte.jpg",
        stamp: "SECRETO",
      },
    },
    {
      from: 17,
      visual: {
        kind: "map",
        from: NORTH_SEA,
        to: { center: [4, 53.3], scale: 2400 },
        highlight: [
          { country: "uk", color: "blue" },
          { country: "germany", color: "red" },
        ],
        arrows: [{ path: [WILHELMSHAVEN, [4.5, 53.6], [2.4, 52.4], THAMES], color: "red", appear: 0.3, duration: 2.0, ships: true }],
        markers: [
          { at: WILHELMSHAVEN, label: "WILHELMSHAVEN", color: "red", appear: 0.1, pulse: false },
          { at: THAMES, label: "INGLATERRA", color: "blue", appear: 1.8, side: "left" },
        ],
      },
    },
    {
      from: 17,
      word: 10,
      visual: { kind: "photo", src: A + "flota_combate.jpg", zoom: [1.05, 1.2], focus: [0.4, 0.5], flashes: true },
      overlays: [
        { kind: "title", text: "Británicos + EE. UU.", color: "blue" },
        { kind: "caption", text: "Acorazado de la Flota de Alta Mar abriendo fuego", source: "Álbum «Der Weltkrieg», 1923 · CC BY-SA 4.0" },
      ],
    },
    {
      from: 18,
      visual: { kind: "fleet", mode: "sail", smoke: true, ships: 3 },
      overlays: [
        { kind: "title", text: "Todos los barcos", color: "red", low: true, at: 18, word: 5 },
        { kind: "redpulse", bpm: 62 },
      ],
    },
    {
      from: 18,
      word: 9,
      visual: { kind: "photo", src: A + "marineros_wilhelmshaven.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.45] },
      overlays: [
        { kind: "slam", text: "Decenas de miles", color: "red", size: 104 },
        { kind: "caption", text: "Marineros en Wilhelmshaven, noviembre de 1918", source: BUNDESARCHIV("146-1976-067-10A") },
      ],
    },
    {
      from: 19,
      visual: { kind: "photo", src: A + "scheer_2.jpg", portrait: true, zoom: [1.1, 1.22], focus: [0.5, 0.2], dim: 0.35 },
      overlays: [{ kind: "title", text: "«Una muerte honorable»", color: "cream", low: true, at: 19, word: 3 }],
    },
    {
      from: 20,
      visual: { kind: "photo", src: A + "berlin_gobierno.jpg", portrait: true, zoom: [1.15, 1.25], focus: [0.5, 0.3], dim: 0.3 },
      overlays: [{ kind: "stamp", text: "Oculta a Berlín", y: 1150, at: 20, word: 1 }],
    },
    // ── La noche del 29 de octubre ──
    {
      from: 21,
      visual: { kind: "fleet", mode: "port", night: true, smoke: true, ships: 4 },
      overlays: [{ kind: "ribbon", text: "29 DE OCTUBRE DE 1918 · NOCHE" }],
    },
    {
      from: 22,
      visual: {
        kind: "map",
        from: { center: [8, 54], scale: 3200 },
        to: { center: [8.1, 53.6], scale: 5200 },
        highlight: [{ country: "germany", color: "red" }],
        markers: [{ at: WILHELMSHAVEN, label: "WILHELMSHAVEN", color: "amber", appear: 0.3 }],
      },
    },
    {
      from: 22,
      word: 9,
      visual: { kind: "photo", src: A + "thuringen.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.55] },
      overlays: [{ kind: "slam", text: "¡Leven anclas!", color: "amber" }],
    },
    {
      from: 23,
      visual: { kind: "photo", src: A + "consejo_marineros.jpg", zoom: [1.1, 1.25], focus: [0.5, 0.35] },
      overlays: [
        { kind: "stat", value: 40000, label: "MARINEROS", color: "cream", at: 23, word: 2 },
        { kind: "caption", text: "Consejo de marineros del SMS Prinzregent Luitpold, 1918" },
      ],
    },
    {
      from: 23,
      word: 7,
      visual: { kind: "photo", src: A + "marineros_wilhelmshaven.jpg", zoom: [1.3, 1.4], focus: [0.3, 0.5] },
      overlays: [
        { kind: "title", text: "A días del armisticio", color: "amber" },
        { kind: "caption", text: "Wilhelmshaven, noviembre de 1918", source: BUNDESARCHIV("146-1976-067-10A") },
      ],
    },
    {
      from: 23,
      word: 15,
      visual: { kind: "fleet", mode: "port", night: true, smoke: true, ships: 2 },
      overlays: [{ kind: "slam", text: "¿Morir por orgullo?", color: "red", size: 100, at: 23, word: 18 }],
    },
    {
      from: 24,
      visual: { kind: "photo", src: A + "thuringen.jpg", zoom: [1.05, 1.15], focus: [0.45, 0.6] },
      overlays: [{ kind: "caption", text: "SMS Thüringen" }],
    },
    {
      from: 24,
      word: 5,
      visual: { kind: "photo", src: A + "helgoland.jpg", portrait: true, zoom: [1.0, 1.1], focus: [0.5, 0.5] },
      overlays: [{ kind: "caption", text: "SMS Helgoland", source: BUNDESARCHIV("DVM 10 Bild-23-61-09") }],
    },
    {
      from: 25,
      visual: { kind: "photo", src: A + "fogoneros.jpg", zoom: [1.1, 1.3], focus: [0.4, 0.5] },
      overlays: [{ kind: "slam", text: "Bajan las palas", color: "amber", at: 25, word: 2 }],
    },
    {
      from: 25,
      word: 6,
      visual: { kind: "boiler", from: 15, to: 0, dropAt: 0.3, dropDur: 1.8 },
    },
    {
      from: 26,
      visual: { kind: "fleet", mode: "port", night: true, smoke: false, ships: 4 },
      overlays: [{ kind: "slam", text: "Sin vapor", color: "cream", y: 760, at: 26, word: 1 }],
    },
    // ── Hipper responde ──
    {
      from: 27,
      visual: { kind: "photo", src: A + "hipper.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.5, 0.25] },
      overlays: [{ kind: "title", text: "Cancela el ataque", color: "cream", low: true, at: 27, word: 3 }],
    },
    {
      from: 28,
      visual: { kind: "photo", src: A + "consejo_marineros.jpg", zoom: [1.25, 1.4], focus: [0.6, 0.4], dim: 0.35 },
      overlays: [
        { kind: "impact", strength: 0.8 },
        { kind: "stat", value: 1000, label: "MARINEROS ARRESTADOS", color: "red", at: 28, word: 2 },
      ],
    },
    {
      from: 28,
      word: 7,
      visual: {
        kind: "map",
        from: { center: [9, 54], scale: 3000 },
        to: { center: [9.4, 54], scale: 3600 },
        highlight: [{ country: "germany", color: "red" }],
        arrows: [{ path: [WILHELMSHAVEN, [7.6, 54.2], [8.6, 54.0], [9.3, 54.1], KIEL], color: "red", appear: 0.1, duration: 1.0, ships: true }],
        markers: [{ at: KIEL, label: "KIEL", color: "red", appear: 0.8 }],
      },
    },
    {
      from: 28,
      word: 14,
      visual: { kind: "photo", src: A + "hipper.jpg", portrait: true, zoom: [1.25, 1.35], focus: [0.5, 0.25], dim: 0.5 },
      overlays: [
        { kind: "impact" },
        { kind: "slam", text: "Traición", color: "red", y: 1320, at: 28, word: 15 },
      ],
    },
    {
      from: 29,
      visual: { kind: "photo", src: A + "cartel_kiel.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.5, 0.3], dim: 0.1 },
      overlays: [
        { kind: "caption", text: "Postal revolucionaria de Kiel, 1918" },
        { kind: "embers", intensity: 1 },
        { kind: "impact", strength: 1.2, at: 29, word: 4, delay: 0.4 },
        { kind: "slam", text: "La mecha", color: "red", y: 1320, at: 29, word: 2 },
      ],
    },
    // ── La revuelta ──
    {
      from: 30,
      visual: { kind: "photo", src: A + "kiel_multitud_1.jpg", zoom: [1.1, 1.25], focus: [0.5, 0.5] },
      overlays: [
        { kind: "ribbon", text: "KIEL · 3 DE NOVIEMBRE" },
        { kind: "caption", text: "Concentración en Kiel, 10 de noviembre de 1918", source: MEYER },
      ],
    },
    {
      from: 30,
      word: 9,
      visual: { kind: "photo", src: A + "kiel_multitud_2.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.6] },
      overlays: [
        { kind: "title", text: "Marineros y obreros", color: "cream" },
        { kind: "caption", text: "Kiel, 10 de noviembre de 1918", source: MEYER },
      ],
    },
    {
      from: 31,
      visual: { kind: "photo", src: A + "kiel_multitud_3.jpg", zoom: [1.15, 1.3], focus: [0.5, 0.5], flashes: true },
      overlays: [
        { kind: "impact", strength: 1.3, at: 31, word: 3 },
        { kind: "caption", text: "Asamblea en Kiel, 1918", source: MEYER },
      ],
    },
    {
      from: 31,
      word: 4,
      visual: { kind: "fleet", mode: "mutiny", smoke: true, ships: 3 },
      overlays: [{ kind: "slam", text: "Se rebela", color: "red", y: 760, at: 31, word: 8 }],
    },
    {
      from: 32,
      visual: { kind: "photo", src: A + "marineros_armados.jpg", zoom: [1.05, 1.2], focus: [0.4, 0.4] },
      overlays: [
        { kind: "caption", text: "Marineros armados durante la revolución, noviembre de 1918" },
        { kind: "slam", text: "Desarman", color: "red", size: 110, at: 32, word: 2 },
      ],
    },
    {
      from: 33,
      visual: { kind: "fleet", mode: "mutiny", smoke: false, ships: 4 },
      overlays: [{ kind: "title", text: "Banderas rojas", color: "red", at: 33, word: 1 }],
    },
    {
      from: 33,
      word: 9,
      visual: {
        kind: "map",
        from: { center: [10.5, 52.6], scale: 3200 },
        to: { center: [10.5, 51.4], scale: 2900 },
        highlight: [{ country: "germany", color: "red" }],
        arrows: [
          { path: [KIEL, HAMBURG], color: "red", appear: 0.2, duration: 0.6 },
          { path: [HAMBURG, [11.5, 52.9], BERLIN], color: "red", appear: 0.6, duration: 0.8 },
          { path: [HAMBURG, [8.5, 52.2], COLOGNE], color: "red", appear: 0.8, duration: 0.8 },
          { path: [BERLIN, [12.5, 50.2], MUNICH], color: "red", appear: 1.3, duration: 0.8 },
        ],
        markers: [
          { at: KIEL, label: "KIEL", color: "red", appear: 0.1, pulse: false },
          { at: HAMBURG, label: "HAMBURGO", color: "cream", appear: 0.6, side: "left", pulse: false },
          { at: BERLIN, label: "BERLÍN", color: "amber", appear: 1.3 },
          { at: COLOGNE, label: "COLONIA", color: "cream", appear: 1.5, side: "left", pulse: false },
          { at: MUNICH, label: "MÚNICH", color: "cream", appear: 2.0, pulse: false },
        ],
      },
    },
    {
      from: 34,
      visual: {
        kind: "timeline",
        title: "6 DÍAS · UN IMPERIO",
        events: [
          { date: "3 NOV", label: "Kiel se rebela", at: 0.1, color: "amber" },
          { date: "7 NOV", label: "La revuelta llega a Múnich", at: 0.8, color: "red" },
          { date: "9 NOV", label: "Revolución en Berlín", at: 1.6, color: "red" },
        ],
      },
    },
    {
      from: 34,
      word: 5,
      visual: { kind: "photo", src: A + "vorwaerts.jpg", portrait: true, zoom: [1.0, 1.1], focus: [0.5, 0.2] },
      overlays: [
        { kind: "impact", strength: 0.8 },
        { kind: "caption", text: "«¡Huelga general!»: Vorwärts, 9 de noviembre de 1918" },
      ],
    },
    {
      from: 35,
      visual: { kind: "photo", src: A + "berlin_revolucion.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5] },
      overlays: [
        { kind: "ribbon", text: "BERLÍN · 9 DE NOVIEMBRE" },
        { kind: "caption", text: "Proclamación de la república ante el Reichstag" },
      ],
    },
    {
      from: 35,
      word: 5,
      visual: { kind: "photo", src: A + "kaiser.jpg", portrait: true, zoom: [1.1, 1.2], focus: [0.5, 0.25], dim: 0.2 },
      overlays: [{ kind: "stamp", text: "Abdica", y: 1250, at: 35, word: 10 }],
    },
    {
      from: 35,
      word: 11,
      visual: { kind: "photo", src: A + "kaiser_eijsden.jpg", zoom: [1.15, 1.3], focus: [0.45, 0.5] },
      overlays: [
        { kind: "title", text: "Huye a Holanda", color: "amber" },
        { kind: "caption", text: "Guillermo II en Eijsden, 10 de noviembre de 1918", source: BUNDESARCHIV("183-R12318") },
      ],
    },
    {
      from: 36,
      visual: { kind: "photo", src: A + "armisticio.jpg", portrait: true, zoom: [1.05, 1.15], focus: [0.5, 0.5] },
      overlays: [
        { kind: "ribbon", text: "11 DE NOVIEMBRE DE 1918" },
        { kind: "stamp", text: "Fin de la guerra", color: "amber", y: 1250, at: 36, word: 4 },
      ],
    },
    // ── Epílogo ──
    {
      from: 37,
      visual: { kind: "photo", src: A + "jutlandia.jpg", zoom: [1.1, 1.25], focus: [0.45, 0.5], fog: 0.2 },
      overlays: [{ kind: "title", text: "Un hundimiento glorioso", color: "amber", at: 37, word: 3 }],
    },
    {
      from: 37,
      word: 11,
      visual: {
        kind: "versus",
        left: { src: A + "scheer.jpg", name: "Los almirantes", lines: ["QUERÍAN GLORIA"], color: "amber", focus: [0.5, 0.3] },
        right: { src: A + "consejo_marineros.jpg", name: "Los marineros", lines: ["QUERÍAN VIVIR"], color: "red", focus: [0.5, 0.4] },
      },
    },
    {
      from: 38,
      word: 4,
      visual: { kind: "boiler", from: 12, to: 0, dropAt: 0.3, dropDur: 1.4, label: "LES APAGARON EL MOTOR" },
    },
    {
      from: 39,
      visual: { kind: "fleet", mode: "port", night: true, smoke: false, ships: 3 },
      overlays: [{ kind: "title", text: "Pensá en esa noche", color: "cream" }],
    },
    // ── Cierre ──
    {
      from: 40,
      visual: { kind: "dilemma", background: A + "consejo_marineros.jpg", aAt: 41, bAt: 41, footerAt: 41 },
    },
  ],
};
