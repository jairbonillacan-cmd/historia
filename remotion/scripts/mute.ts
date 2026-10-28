// Silencia la segunda mitad de cada palabra censurada del audio master: se entiende
// por el contexto («muer…»), pero la palabra completa no llega a sonar.
// Uso: npx tsx scripts/mute.ts <carpeta> <audio_entrada> <audio_salida>
//   p. ej. 05_isla_kiska audio/audio_master_180s.wav audio/audio_master_censurado.wav
// Toma los tiempos de cada palabra de produccion/<carpeta>/timeline_chunks.json.
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { isCensored } from "../src/engine/censor";
import type { Timeline } from "../src/engine/types";

const CUT_FROM = 0.5; // fracción de la palabra desde la que se silencia
const PAD_AFTER = 0.12; // los tiempos de whisper suelen cerrar la palabra antes de que termine de sonar
const RAMP = 0.012; // segundos de fundido para que el corte no haga clic

const [folder, input, output] = process.argv.slice(2);
if (!folder || !input || !output) {
  console.error("Uso: npx tsx scripts/mute.ts <carpeta> <audio_entrada> <audio_salida>");
  process.exit(1);
}
const base = path.join(process.cwd(), "..", "produccion", folder);
const timeline: Timeline = JSON.parse(readFileSync(path.join(base, "timeline_chunks.json"), "utf-8"));

const words = timeline.chunks.flatMap((c) => c.words);
const spans: [number, number][] = [];
for (const [i, w] of words.entries()) {
  if (!isCensored(w.word)) continue;
  const a = w.start + (w.end - w.start) * CUT_FROM;
  const next = words[i + 1]?.start ?? Infinity;
  spans.push([a, Math.min(w.end + PAD_AFTER, Math.max(w.end, next - 0.01))]);
  console.log(`${a.toFixed(2)}s  ${w.word}`);
}
if (!spans.length) {
  console.log("No hay palabras para censurar.");
  process.exit(0);
}

// Ganancia = 1 menos la suma de «ventanas» con rampa en cada tramo (no se solapan).
const r = RAMP.toFixed(3);
const windows = spans.map(([a, b]) => `clip((t-${a.toFixed(3)})/${r},0,1)*clip((${b.toFixed(3)}-t)/${r},0,1)`).join("+");
// asetnsamples achica los cuadros de audio para que la expresión se evalúe cada ~1 ms.
const filter = `asetnsamples=n=64,volume='1-(${windows})':eval=frame`;

execFileSync("ffmpeg", ["-v", "error", "-y", "-i", path.join(base, input), "-af", filter, "-c:a", "pcm_s16le", path.join(base, output)], { stdio: "inherit" });
console.log(`${spans.length} palabras cortadas → produccion/${folder}/${output}`);
