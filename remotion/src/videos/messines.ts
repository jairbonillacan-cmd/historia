import timeline from "../../../produccion/08_messines/timeline_chunks.json";
import type { Pt, Timeline, VideoPlan } from "../engine/types";

// AG-17 · Messines (1917). Cada entrada arranca en la cláusula `from` (o en su palabra `word`)
// de timeline_chunks.json. La gran voladura cae en el silencio después de la cláusula 29, igual que
// BLAST en build_music_and_sfx_messines.py.
const A = "assets/";
const tl = timeline as Timeline;
const word = (i: number, k: number) => tl.chunks.find((c) => c.index === i)!.words[k].start;
const BLAST = tl.chunks.find((c) => c.index === 29)!.end + 0.45;

const VIENNA = "ViennaUK · CC BY-SA 4.0";

const MESSINES: Pt = [2.89, 50.77];
const LONDON: Pt = [-0.13, 51.5];
const UK_MINES: Pt = [-1.6, 54.6];
const CANADA: Pt = [-75, 46];
const AUSTRALIA: Pt = [146, -33];
const NZ: Pt = [174.8, -41];

export const messines: VideoPlan = {
  folder: "08_messines",
  audio: "audio/audio_master_final.wav", // voz censurada (npm run mute:messines) + música y efectos (build_music_and_sfx_messines.py)
  timeline: tl,
  progress: true,
  endCta: { question: "¿Vos qué habrías hecho?", a: "CAVAR 2 AÑOS", b: "ATACAR YA", footer: "Dejame tu respuesta 👇" },
  items: [
    // ── Gancho: un corte cada ~1,5–2 s ──
    {
      from: 1,
      visual: { kind: "photo", src: A + "trench.jpg", zoom: [1.2, 1.05], focus: [0.5, 0.45], dim: 0.35 },
      overlays: [
        { kind: "impact", strength: 1.1 },
        { kind: "ribbon", text: "FLANDES, BÉLGICA · 1917" },
      ],
    },
    {
      from: 1,
      word: 5,
      transition: "whip",
      visual: { kind: "photo", src: A + "plumer.jpg", portrait: true, zoom: [1.05, 1.15], focus: [0.5, 0.3], dim: 0.1 },
      overlays: [{ kind: "slam", text: "La historia", color: "cream", y: 1300, at: 1, word: 7 }],
    },
    {
      from: 2,
      visual: { kind: "photo", src: A + "ridge_panorama.jpg", zoom: [1.1, 1.25], focus: [0.55, 0.6] },
      overlays: [{ kind: "title", text: "…y la geografía", color: "amber", at: 2, word: 5 }],
    },
    {
      from: 2,
      word: 8,
      transition: "flash",
      visual: { kind: "mine", stage: "blast", blastAt: 0.25 },
      overlays: [{ kind: "impact", strength: 1.4, delay: 0.25 }],
    },
    {
      from: 3,
      visual: { kind: "photo", src: A + "plumer_field.jpg", zoom: [1.1, 1.3], focus: [0.18, 0.55] },
      overlays: [
        { kind: "title", text: "General Herbert Plumer", color: "amber", at: 3, word: 4 },
        { kind: "caption", text: "Plumer y el general Braithwaite en el frente" },
      ],
    },
    {
      from: 3,
      word: 9,
      visual: { kind: "photo", src: A + "plumer_drawing.jpg", portrait: true, zoom: [1.0, 1.12], focus: [0.5, 0.3] },
      overlays: [{ kind: "title", text: "Frente a sus oficiales", color: "cream", low: true }],
    },
    {
      from: 4,
      visual: { kind: "mine", stage: "charges" },
      overlays: [{ kind: "stat", value: 30, suffix: " m", label: "BAJO LAS BOTAS ALEMANAS", color: "amber" }],
    },
    {
      from: 4,
      word: 5,
      visual: { kind: "photo", src: A + "german_dugout.jpg", zoom: [1.05, 1.2], focus: [0.45, 0.5] },
      overlays: [{ kind: "caption", text: "Refugio alemán de hormigón en la cresta, junio de 1917" }],
    },
    {
      from: 4,
      word: 12,
      visual: { kind: "photo", src: A + "mine_charge.jpg", zoom: [1.05, 1.2], focus: [0.55, 0.5] },
      overlays: [
        { kind: "stat", value: 500000, label: "KILOS DE EXPLOSIVOS", color: "red" },
        { kind: "caption", text: "Zapadores británicos con cargas de explosivo, 1916" },
      ],
    },
    {
      from: 4,
      word: 20,
      transition: "flash",
      visual: { kind: "photo", src: A + "explosion.jpg", zoom: [1.1, 1.3], focus: [0.45, 0.4], flashes: true },
      overlays: [
        { kind: "impact", strength: 1.2 },
        { kind: "slam", text: "Estallar", color: "red", y: 1250 },
      ],
    },
    // ── Contexto ──
    {
      from: 5,
      visual: {
        kind: "map",
        from: { center: [4, 51.5], scale: 2600 },
        to: { center: [2.9, 50.85], scale: 9000 },
        highlight: [
          { country: "belgium", color: "amber" },
          { country: "germany", color: "red" },
          { country: "uk", color: "blue" },
        ],
        markers: [{ at: MESSINES, label: "MESSINES", color: "red", appear: 1.4 }],
      },
      overlays: [{ kind: "ribbon", text: "JUNIO DE 1917" }],
    },
    {
      from: 5,
      word: 9,
      visual: { kind: "photo", src: A + "wasteland.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5] },
      overlays: [{ kind: "title", text: "Primera Guerra Mundial", color: "cream" }],
    },
    {
      from: 6,
      visual: { kind: "photo", src: A + "ridge_panorama.jpg", zoom: [1.3, 1.15], focus: [0.4, 0.55], dim: 0.3 },
      overlays: [
        { kind: "title", text: "La colina de Messines", color: "amber", at: 6, word: 4 },
        { kind: "caption", text: "La cresta de Messines y Wytschaete, dibujo de Muirhead Bone" },
      ],
    },
    {
      from: 7,
      visual: { kind: "photo", src: A + "aerial_messines.jpg", zoom: [1.05, 1.25], focus: [0.5, 0.45] },
      overlays: [
        { kind: "title", text: "Un balcón natural", color: "amber" },
        { kind: "reticle", x: 560, y: 1000, lock: 1.2 },
        { kind: "caption", text: "Foto aérea de Messines, 6 de junio de 1917", source: "Archives New Zealand · CC BY 2.0" },
      ],
    },
    {
      from: 7,
      word: 8,
      visual: { kind: "photo", src: A + "trench.jpg", zoom: [1.1, 1.25], focus: [0.45, 0.5], flashes: true },
      overlays: [{ kind: "impact", strength: 0.8 }],
    },
    {
      from: 8,
      visual: { kind: "photo", src: A + "shell_hole.jpg", zoom: [1.05, 1.2], focus: [0.4, 0.5] },
      overlays: [
        { kind: "impact", strength: 0.7, at: 8, word: 12 },
        { kind: "slam", text: "Suicidio", color: "red", y: 1250, at: 8, word: 12 },
      ],
    },
    {
      from: 9,
      visual: { kind: "photo", src: A + "plumer.jpg", portrait: true, zoom: [1.15, 1.25], focus: [0.5, 0.3], dim: 0.15 },
      overlays: [{ kind: "stat", value: 2, label: "AÑOS DE OBRA", color: "amber", at: 9, word: 4 }],
    },
    {
      from: 9,
      word: 10,
      visual: { kind: "photo", src: A + "mine_plan.jpg", zoom: [1.0, 1.15], focus: [0.4, 0.45], dim: 0.4 },
      overlays: [
        { kind: "title", text: "Ingeniería paciente", color: "amber" },
        { kind: "caption", text: "Plano de las galerías de Spanbroekmolen", source: VIENNA },
      ],
    },
    {
      from: 10,
      visual: { kind: "mine", stage: "dig" },
      overlays: [
        { kind: "title", text: "Por arriba, no", color: "red" },
        { kind: "slam", text: "Desde abajo", color: "amber", y: 680, size: 120, at: 11, word: 4 },
      ],
    },
    {
      from: 12,
      visual: {
        kind: "map",
        from: { center: [40, 10], scale: 165 },
        to: { center: [20, 25], scale: 210 },
        highlight: [
          { country: "uk", color: "blue" },
          { country: "canada", color: "blue" },
          { country: "australia", color: "blue" },
          { country: "newzealand", color: "blue" },
          { country: "belgium", color: "amber" },
        ],
        arrows: [
          { path: [UK_MINES, MESSINES], color: "blue", appear: 0.6, duration: 0.8 },
          { path: [CANADA, [-30, 50], MESSINES], color: "blue", appear: 1.5, duration: 1.2 },
          { path: [AUSTRALIA, [80, 5], [30, 35], MESSINES], color: "blue", appear: 2.2, duration: 1.6 },
          { path: [NZ, [100, 0], [35, 33], MESSINES], color: "blue", appear: 3.0, duration: 1.6 },
        ],
        markers: [{ at: MESSINES, label: "MESSINES", color: "amber", appear: 0.2 }],
      },
      overlays: [{ kind: "title", text: "Miles de mineros del carbón", color: "cream", low: true }],
    },
    {
      from: 13,
      word: 6,
      visual: { kind: "photo", src: A + "tunnellers_group.jpg", zoom: [1.05, 1.2], focus: [0.45, 0.55] },
      overlays: [
        { kind: "caption", text: "Mineros de la Compañía de Túneles de Nueva Zelanda" },
        { kind: "stat", value: 30, suffix: " m", label: "DE PROFUNDIDAD", color: "amber", at: 13, word: 13 },
      ],
    },
    // ── La guerra bajo tierra ──
    {
      from: 14,
      visual: { kind: "photo", src: A + "sappers_drawing.jpg", portrait: true, zoom: [1.0, 1.15], focus: [0.5, 0.45], dim: 0.15 },
      overlays: [{ kind: "title", text: "Silencio absoluto", color: "cream", at: 14, word: 5 }],
    },
    {
      from: 14,
      word: 11,
      visual: { kind: "photo", src: A + "tunnellers_bunks.jpg", zoom: [1.05, 1.2], focus: [0.4, 0.5] },
      overlays: [
        { kind: "stat", value: 8, suffix: " km", label: "DE GALERÍAS", color: "amber" },
        { kind: "caption", text: "Literas de mineros bajo tierra, Primera Guerra Mundial" },
      ],
    },
    {
      from: 15,
      visual: { kind: "mine", stage: "listen" },
      overlays: [{ kind: "title", text: "¡Los escuchan!", color: "red", at: 15, word: 3 }],
    },
    {
      from: 16,
      transition: "glitch",
      visual: { kind: "photo", src: A + "ruins_sign.jpg", zoom: [1.05, 1.22], focus: [0.4, 0.5], dim: 0.3 },
      overlays: [{ kind: "slam", text: "Guerra a ciegas", color: "red", size: 120, y: 1250, at: 16, word: 7 }],
    },
    {
      from: 17,
      visual: { kind: "photo", src: A + "tunnellers_group.jpg", zoom: [1.25, 1.4], focus: [0.5, 0.45], dim: 0.35 },
      overlays: [{ kind: "title", text: "Sin hablar", color: "cream", at: 17, word: 3 }],
    },
    {
      from: 17,
      word: 5,
      visual: { kind: "mine", stage: "listen" },
      overlays: [
        { kind: "title", text: "Oído a la pared", color: "amber" },
        { kind: "redpulse", bpm: 72 },
      ],
    },
    {
      from: 18,
      visual: { kind: "photo", src: A + "sappers_drawing.jpg", portrait: true, zoom: [1.2, 1.35], focus: [0.5, 0.55], dim: 0.2 },
      overlays: [
        { kind: "caption", text: "«Zapadores trabajando», David Bomberg (IWM)" },
        { kind: "slam", text: "Cuerpo a cuerpo", color: "red", size: 110, y: 1180, at: 19, word: 1 },
        { kind: "impact", strength: 0.6, at: 19, word: 1 },
      ],
    },
    {
      from: 20,
      transition: "flash",
      visual: { kind: "photo", src: A + "explosion.jpg", zoom: [1.3, 1.15], focus: [0.5, 0.4] },
      overlays: [{ kind: "impact", strength: 0.9, at: 20, word: 1 }],
    },
    {
      from: 21,
      visual: {
        kind: "timeline",
        title: "LA CUENTA REGRESIVA",
        events: [
          { date: "1915", label: "Empiezan a cavar", at: 0.2, color: "cream" },
          { date: "1917", label: "Descubren una cámara", at: word(22, 4) - word(21, 0), color: "red" },
          { date: "7 DE JUNIO", label: "La hora cero", at: word(22, 8) - word(21, 0), color: "amber" },
        ],
      },
      overlays: [{ kind: "impact", strength: 0.7, at: 22, word: 4 }],
    },
    {
      from: 23,
      visual: { kind: "photo", src: A + "german_dugout.jpg", zoom: [1.2, 1.35], focus: [0.6, 0.45], dim: 0.2 },
      overlays: [{ kind: "title", text: "Creen que ganaron", color: "cream" }],
    },
    {
      from: 24,
      visual: { kind: "mine", stage: "charges", lost: true },
      overlays: [{ kind: "title", text: "El dato clave", color: "red", at: 24, word: 4 }],
    },
    {
      from: 25,
      word: 5,
      visual: { kind: "photo", src: A + "mine_charge.jpg", zoom: [1.2, 1.35], focus: [0.6, 0.55], dim: 0.15 },
      overlays: [{ kind: "stat", value: 20, label: "CÁMARAS INTACTAS", color: "red" }],
    },
    {
      from: 26,
      visual: { kind: "mine", stage: "charges", lost: true },
      overlays: [{ kind: "stat", value: 454, label: "TONELADAS DE EXPLOSIVOS", color: "red", at: 26, word: 2 }],
    },
    // ── La hora cero ──
    {
      from: 27,
      transition: "zoom",
      visual: { kind: "photo", src: A + "aerial_messines.jpg", zoom: [1.3, 1.45], focus: [0.5, 0.5], dim: 0.45 },
      overlays: [
        { kind: "ribbon", text: "7 DE JUNIO DE 1917" },
        { kind: "slam", text: "3:10", color: "amber", y: 1250, at: 27, word: 2 },
      ],
    },
    {
      from: 28,
      visual: { kind: "photo", src: A + "ridge_panorama.jpg", zoom: [1.15, 1.3], focus: [0.6, 0.6], fog: 0.4, dim: 0.35 },
      overlays: [{ kind: "title", text: "Todo en calma", color: "cream", at: 28, word: 3 }],
    },
    {
      from: 29,
      visual: { kind: "photo", src: A + "trench.jpg", zoom: [1.3, 1.45], focus: [0.5, 0.6], dim: 0.4 },
      overlays: [{ kind: "title", text: "Al piso", color: "amber", at: 29, word: 4 }],
    },
    {
      from: 29,
      word: 9,
      visual: { kind: "mine", stage: "blast", blastAt: BLAST - word(29, 9) },
      overlays: [
        { kind: "redpulse", bpm: 90 },
        { kind: "title", text: "Las palancas", color: "red", at: 29, word: 10 },
        { kind: "impact", strength: 1.8, delay: BLAST - word(29, 9) },
      ],
    },
    // ── La explosión ──
    {
      from: 30,
      visual: { kind: "photo", src: A + "explosion.jpg", zoom: [1.0, 1.2], focus: [0.45, 0.4], flashes: true },
      overlays: [
        { kind: "stat", value: 19, label: "MINAS A LA VEZ", color: "red", at: 30, word: 3 },
        { kind: "impact", strength: 0.8, at: 30, word: 6 },
        { kind: "embers", intensity: 0.8 },
      ],
    },
    {
      from: 31,
      visual: { kind: "photo", src: A + "hill60_crater.jpg", zoom: [1.05, 1.25], focus: [0.5, 0.55] },
      overlays: [
        { kind: "title", text: "19 cráteres", color: "amber", at: 31, word: 5 },
        { kind: "stat", value: 80, suffix: " m", label: "DE DIÁMETRO", color: "amber", at: 32, word: 2 },
        { kind: "caption", text: "Cráter de Hill 60, una de las 19 minas, hoy", source: VIENNA },
      ],
    },
    {
      from: 33,
      visual: {
        kind: "map",
        from: { center: [2.9, 51], scale: 6000 },
        to: { center: [1.4, 51.2], scale: 3600 },
        highlight: [
          { country: "belgium", color: "amber" },
          { country: "uk", color: "blue" },
        ],
        shockwave: { at: MESSINES, appear: 0.1 },
        markers: [
          { at: MESSINES, label: "MESSINES", color: "red", appear: 0, pulse: false },
          { at: LONDON, label: "LONDRES", color: "blue", appear: word(33, 7) - word(33, 0), side: "left" },
        ],
      },
      overlays: [{ kind: "stat", value: 200, prefix: "+", suffix: " km", label: "SE OYÓ EN LONDRES", color: "cream", at: 34, word: 3 }],
    },
    {
      from: 35,
      visual: { kind: "photo", src: A + "devastation.jpg", zoom: [1.05, 1.2], focus: [0.15, 0.3] },
      overlays: [
        { kind: "title", text: "La mayor explosión", color: "red", at: 35, word: 2 },
        { kind: "slam", text: "Antes del átomo", color: "amber", size: 110, y: 1250, at: 35, word: 12 },
      ],
    },
    {
      from: 36,
      visual: { kind: "photo", src: A + "ruins_messines.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5], dim: 0.15 },
      overlays: [
        { kind: "stat", value: 10000, label: "SOLDADOS ALEMANES", color: "red", at: 36, word: 1 },
        { kind: "caption", text: "Ruinas de Messines, 1917" },
      ],
    },
    {
      from: 36,
      word: 8,
      visual: { kind: "photo", src: A + "troops_cheering.jpg", zoom: [1.05, 1.18], focus: [0.5, 0.45] },
      overlays: [
        { kind: "stat", value: 3, label: "HORAS PARA TOMAR LA COLINA", color: "blue", at: 36, word: 18 },
        { kind: "caption", text: "Tropas británicas tras tomar la cresta, junio de 1917" },
      ],
    },
    // ── La mina olvidada ──
    {
      from: 37,
      visual: { kind: "photo", src: A + "fields_today.jpg", zoom: [1.05, 1.2], focus: [0.6, 0.5] },
      overlays: [
        { kind: "title", text: "Una mina olvidada", color: "amber", at: 37, word: 3 },
        { kind: "stat", value: 38, label: "AÑOS BAJO UNA GRANJA", color: "amber", at: 37, word: 16 },
        { kind: "caption", text: "Campos de Messines, hoy", source: VIENNA },
      ],
    },
    {
      from: 38,
      visual: {
        kind: "timeline",
        title: "LA MINA DORMIDA",
        events: [
          { date: "7 JUN 1917", label: "No detona", at: 0.1, color: "cream" },
          { date: "17 JUL 1955", label: "Un rayo la hace volar", at: word(38, 3) - word(38, 0), color: "amber" },
        ],
      },
      overlays: [
        { kind: "impact", strength: 1.0, at: 38, word: 3 },
        { kind: "impact", strength: 0.8, at: 38, word: 11 },
      ],
    },
    {
      from: 39,
      visual: { kind: "photo", src: A + "spanbroek_crater.jpg", zoom: [1.05, 1.2], focus: [0.5, 0.5], dim: 0.3 },
      overlays: [
        { kind: "title", text: "Paciencia vs. fuerza bruta", color: "amber", at: 39, word: 5 },
        { kind: "caption", text: "Cráter de Spanbroekmolen, hoy «Pool of Peace»", source: "Laika ac · CC BY-SA 2.0" },
      ],
    },
    // ── Cierre ──
    {
      from: 40,
      visual: { kind: "dilemma", background: A + "sappers_drawing.jpg", aAt: 40, bAt: 41, footerAt: 41 },
    },
  ],
};
