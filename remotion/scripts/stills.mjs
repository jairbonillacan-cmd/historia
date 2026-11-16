// Renderiza cuadros sueltos para revisar el video sin hacer el render completo.
// Uso: node scripts/stills.mjs Kiska 1.5 11 20 ...   (segundos)
import path from "node:path";
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";

const [id, ...secs] = process.argv.slice(2);
const root = process.cwd();
const serveUrl = await bundle({ entryPoint: path.join(root, "src/index.ts"), publicDir: path.join(root, "..", "produccion") });
const composition = await selectComposition({ serveUrl, id });
for (const s of secs) {
  const frame = Math.min(composition.durationInFrames - 1, Math.round(Number(s) * composition.fps));
  const output = path.join(root, "out", `${id}_${String(s).replace(".", "_")}s.jpg`);
  await renderStill({ serveUrl, composition, frame, output, imageFormat: "jpeg", jpegQuality: 85 });
  console.log(output);
}
