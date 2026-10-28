import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { colors, fonts, layout } from "./theme";
import type { Chunk, Word } from "./types";
import { isCensored, maskWord } from "./censor";

// Subtítulo superior palabra por palabra: dichas en gris, actual en blanco,
// futuras desenfocadas; la palabra nuclear (is_bbox) lleva la caja azul con nodos.
export const Caption: React.FC<{ chunks: Chunk[] }> = ({ chunks }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const chunk = findChunk(chunks, t);
  if (!chunk) return null;

  const groupId = currentGroup(chunk.words, t);
  const words = chunk.words.filter((w) => w.group_id === groupId);

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 620,
          background: "linear-gradient(180deg, rgba(8,8,8,0.82) 0%, rgba(8,8,8,0.55) 55%, rgba(8,8,8,0) 100%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: layout.captionY,
          left: 90,
          right: 90,
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          columnGap: 18,
          rowGap: 6,
          fontFamily: fonts.body,
          fontSize: 58,
          lineHeight: 1.18,
          fontWeight: 600,
          textAlign: "center",
        }}
      >
        {words.map((w, i) => (
          <CaptionWord key={i} w={w} t={t} />
        ))}
      </div>
    </AbsoluteFill>
  );
};

const CaptionWord: React.FC<{ w: Word; t: number }> = ({ w, t }) => {
  const state = t < w.start ? "future" : t < w.end ? "current" : "spoken";
  const color = state === "spoken" ? colors.spoken : "#FFFFFF";
  // Palabra sensible: símbolos en las vocales y un desenfoque leve que deja leerla (en el audio se corta el final).
  const censored = isCensored(w.word);
  const blur = state === "future" ? 6 : censored ? 1.5 : 0;
  const opacity = state === "future" ? 0.55 : 1;
  const weight = state === "current" || w.is_bbox ? 800 : 600;
  const showBox = w.is_bbox && state !== "future";

  return (
    <span
      style={{
        position: "relative",
        color,
        filter: blur ? `blur(${blur}px)` : undefined,
        opacity,
        fontWeight: weight,
        padding: showBox ? "0 10px" : undefined,
        textShadow: "0 3px 14px rgba(0,0,0,0.6)",
      }}
    >
      {showBox && <BBox />}
      {censored ? maskWord(w.word) : w.word}
    </span>
  );
};

const BBox: React.FC = () => {
  const node: React.CSSProperties = {
    position: "absolute",
    width: 9,
    height: 9,
    background: "#fff",
    border: `2px solid ${colors.bbox}`,
  };
  return (
    <span
      style={{
        position: "absolute",
        inset: "2px -2px 0 -2px",
        border: `3px solid ${colors.bbox}`,
        background: "rgba(59,130,246,0.18)",
      }}
    >
      <span style={{ ...node, left: -6, top: -6 }} />
      <span style={{ ...node, right: -6, top: -6 }} />
      <span style={{ ...node, left: -6, bottom: -6 }} />
      <span style={{ ...node, right: -6, bottom: -6 }} />
    </span>
  );
};

// Entre cláusulas mantenemos la anterior en pantalla para que el subtítulo no parpadee.
function findChunk(chunks: Chunk[], t: number): Chunk | undefined {
  let last: Chunk | undefined;
  for (const c of chunks) {
    if (c.start - 0.05 <= t) last = c;
    else break;
  }
  if (last && t > last.end + 1.2) return undefined;
  return last;
}

function currentGroup(words: Word[], t: number): number {
  let g = words[0]?.group_id ?? 0;
  for (const w of words) {
    if (w.start - 0.04 <= t) g = w.group_id;
  }
  return g;
}
