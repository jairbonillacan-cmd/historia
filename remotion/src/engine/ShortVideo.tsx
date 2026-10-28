import React from "react";
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { Overlay } from "./types";
import { Caption } from "./Caption";
import { BomberScene, EscortScene, MedalScene, QuoteScene, VersusScene } from "./AirScenes";
import { DilemmaScene } from "./DilemmaScene";
import { Flicker, Grain, Vignette } from "./Film";
import { MapScene } from "./MapScene";
import { shakeOffset } from "./Motion";
import { ProgressBar, transitionStyle } from "./Kinetic";
import { OverlayLayer } from "./Overlays";
import { PhotoScene } from "./PhotoScene";
import { RadarScene } from "./RadarScene";
import type { PlanItem, Transition, VideoPlan } from "./types";

// Arma el Short completo: escenas del plan + capas + subtítulos + audio master.
export const ShortVideo: React.FC<{ plan: VideoPlan; fps: number; totalFrames: number }> = ({ plan, fps, totalFrames }) => {
  const chunkStart = (index: number) => {
    const c = plan.timeline.chunks.find((x) => x.index === index);
    if (!c) throw new Error(`Cláusula ${index} no existe en timeline_chunks.json`);
    return c.start;
  };
  // Inicio de la palabra `word` de la cláusula `index` (o de la cláusula entera).
  const wordStart = (index: number, word?: number) => {
    if (word === undefined) return chunkStart(index);
    const w = plan.timeline.chunks.find((x) => x.index === index)?.words[word];
    if (!w) throw new Error(`Palabra ${word} no existe en la cláusula ${index}`);
    return w.start;
  };
  const toFrame = (s: number) => Math.round(s * fps);

  const spans = plan.items.map((item, i) => {
    const start = i === 0 ? 0 : toFrame(wordStart(item.from, item.word));
    const next = plan.items[i + 1];
    const end = next ? toFrame(wordStart(next.from, next.word)) : totalFrames;
    return { item, start, end };
  });
  const overlayStart = (o: Overlay, sceneStart: number) => (o.at ? toFrame(wordStart(o.at, o.word)) - sceneStart : 0) + Math.round((o.delay ?? 0) * fps);

  // Impactos: sacuden toda la escena (no los subtítulos).
  const impacts = spans.flatMap(({ item, start }) =>
    (item.overlays ?? []).flatMap((o) => (o.kind === "impact" ? [{ frame: start + Math.max(0, overlayStart(o, start)), strength: o.strength ?? 1 }] : [])),
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#0b0b0b" }}>
      <Shake impacts={impacts}>
      {spans.map(({ item, start, end }, i) => (
        <Sequence key={i} from={start} durationInFrames={end - start} name={`#${item.from} ${item.visual.kind}`}>
          <Settle transition={item.transition}>
            <SceneVisual item={item} plan={plan} sceneStart={start / fps} chunkStart={chunkStart} />
          </Settle>
          {(item.overlays ?? []).map((o, k) => {
            const at = overlayStart(o, start);
            if (at >= end - start) return null; // cae fuera de la escena
            return (
              <Sequence key={k} from={Math.max(0, at)} durationInFrames={end - start - Math.max(0, at)} layout="none">
                <OverlayLayer overlay={o} />
              </Sequence>
            );
          })}
        </Sequence>
      ))}
      </Shake>
      <Vignette />
      <Flicker />
      <Grain />
      <Caption chunks={plan.timeline.chunks} />
      {plan.progress && <ProgressBar />}
      <Audio src={staticFile(`${plan.folder}/${plan.audio}`)} />
    </AbsoluteFill>
  );
};

const SceneVisual: React.FC<{ item: PlanItem; plan: VideoPlan; sceneStart: number; chunkStart: (i: number) => number }> = ({ item, plan, sceneStart, chunkStart }) => {
  const v = item.visual;
  switch (v.kind) {
    case "photo":
      return <PhotoScene {...v} folder={plan.folder} />;
    case "map":
      return <MapScene {...v} />;
    case "radar":
      return <RadarScene blips={v.blips} />;
    case "dilemma":
      return (
        <DilemmaScene
          folder={plan.folder}
          background={v.background}
          {...plan.endCta}
          aAt={chunkStart(v.aAt) - sceneStart}
          bAt={chunkStart(v.bAt) - sceneStart}
          footerAt={chunkStart(v.footerAt) - sceneStart}
        />
      );
    case "bomber":
      return <BomberScene {...v} />;
    case "escort":
      return <EscortScene {...v} />;
    case "quote":
      return <QuoteScene {...v} folder={plan.folder} />;
    case "versus":
      return <VersusScene {...v} folder={plan.folder} />;
    case "medal":
      return <MedalScene {...v} />;
  }
};

const Shake: React.FC<{ impacts: { frame: number; strength: number }[]; children: React.ReactNode }> = ({ impacts, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  let [x, y, r] = [0, 0, 0];
  for (const imp of impacts) {
    const [dx, dy, dr] = shakeOffset(frame - imp.frame, imp.strength, fps);
    x += dx;
    y += dy;
    r += dr;
  }
  if (!x && !y && !r) return <>{children}</>;
  return <AbsoluteFill style={{ transform: `translate(${x}px, ${y}px) rotate(${r}deg) scale(1.04)` }}>{children}</AbsoluteFill>;
};

// Entrada de escena. Sin `transition`: corte seco con un leve asentamiento de escala, como en el documental de referencia.
const Settle: React.FC<{ transition?: Transition; children: React.ReactNode }> = ({ transition, children }) => {
  const frame = useCurrentFrame();
  const { style, flash } = transitionStyle(transition, frame);
  return (
    <AbsoluteFill style={style}>
      {children}
      {flash > 0 && <AbsoluteFill style={{ background: "#fff8ea", opacity: flash }} />}
    </AbsoluteFill>
  );
};
