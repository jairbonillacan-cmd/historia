// Exporta los momentos de cada evento visual (cortes, titulares, datos, mapas, radar...)
// para que scripts/sound_design.py ponga música y efectos sincronizados.
// Uso: npx tsx scripts/cues.ts <video>   (p. ej. kiska) → produccion/<carpeta>/audio/cues.json
import { writeFileSync } from "node:fs";
import path from "node:path";
import type { VideoPlan } from "../src/engine/types";
import { kiska } from "../src/videos/kiska";

const videos: Record<string, VideoPlan> = { kiska };

type Cue = { t: number; kind: string; dur?: number; n?: number };

const id = process.argv[2];
const plan = videos[id];
if (!plan) {
  console.error(`Video desconocido: ${id}. Opciones: ${Object.keys(videos).join(", ")}`);
  process.exit(1);
}

const chunkStart = (i: number) => plan.timeline.chunks.find((c) => c.index === i)!.start;
const total = plan.timeline.total_duration + 0.6;
const cues: Cue[] = [];

plan.items.forEach((item, k) => {
  const start = k === 0 ? 0 : chunkStart(item.from);
  const next = plan.items[k + 1];
  const end = next ? chunkStart(next.from) : total;
  const dur = end - start;
  const v = item.visual;

  if (k > 0) cues.push({ t: start, kind: "cut" });

  if (v.kind === "photo") {
    if (v.flashes) cues.push({ t: start, kind: "flashes", dur });
    if (v.fog) cues.push({ t: start, kind: "wind", dur, n: v.fog });
  }
  if (v.kind === "map") {
    cues.push({ t: start, kind: "sea", dur, n: 0.4 + (v.fog ?? 0) });
    for (const a of v.arrows ?? []) cues.push({ t: start + (a.appear ?? 0), kind: a.ships ? "ships" : "arrow", dur: a.duration ?? 1.4 });
    for (const m of v.markers ?? []) cues.push({ t: start + (m.appear ?? 0), kind: "marker" });
    if (v.crossfire) cues.push({ t: start, kind: "crossfire", dur });
  }
  if (v.kind === "radar") cues.push({ t: start, kind: "radar", dur, n: v.blips ? 7 : 0 });
  if (v.kind === "dilemma") {
    cues.push({ t: chunkStart(v.aAt), kind: "option" });
    cues.push({ t: chunkStart(v.bAt), kind: "option" });
    cues.push({ t: chunkStart(v.footerAt), kind: "cta" });
  }

  for (const o of item.overlays ?? []) {
    const t = o.at ? chunkStart(o.at) : start;
    if (o.kind === "title") cues.push({ t, kind: "impact" });
    if (o.kind === "stat") cues.push({ t, kind: "count" });
    if (o.kind === "ribbon") cues.push({ t, kind: "typewriter", n: o.text.length });
  }
});

cues.sort((a, b) => a.t - b.t);
const out = path.join(process.cwd(), "..", "produccion", plan.folder, "audio", "cues.json");
writeFileSync(out, JSON.stringify({ total, cues }, null, 1));
console.log(`${cues.length} eventos → ${out}`);
