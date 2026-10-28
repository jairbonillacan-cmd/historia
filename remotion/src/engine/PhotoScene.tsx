import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { archivalFilter } from "./theme";
import { Fog, Flashes } from "./Film";
import type { Visual } from "./types";

type Props = Extract<Visual, { kind: "photo" }> & { folder: string };

// Foto de archivo a pantalla completa con acercamiento lento (Ken Burns).
// `portrait`: foto chica o retrato → fondo desenfocado + foto enmarcada al centro.
export const PhotoScene: React.FC<Props> = ({ folder, src, focus = [0.5, 0.5], zoom = [1.06, 1.16], drift = [0, 0], portrait, fog = 0, flashes, dim = 0 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames], [0, 1], { easing: Easing.inOut(Easing.sin) });
  const scale = zoom[0] + (zoom[1] - zoom[0]) * p;
  const tx = drift[0] * p;
  const ty = drift[1] * p;
  const url = staticFile(`${folder}/${src}`);
  const origin = `${focus[0] * 100}% ${focus[1] * 100}%`;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0c0c0c" }}>
      {portrait ? (
        <>
          <Img src={url} style={{ position: "absolute", inset: -60, width: "calc(100% + 120px)", height: "calc(100% + 120px)", objectFit: "cover", filter: `${archivalFilter} blur(28px) brightness(0.55)` }} />
          <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", paddingTop: 140 }}>
            <Img
              src={url}
              style={{
                width: 860,
                maxHeight: 1060,
                objectFit: "cover",
                objectPosition: origin,
                filter: archivalFilter,
                transform: `scale(${scale}) translate(${tx}px, ${ty}px)`,
                boxShadow: "0 30px 80px rgba(0,0,0,0.75)",
              }}
            />
          </AbsoluteFill>
        </>
      ) : (
        <Img
          src={url}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: origin,
            transformOrigin: origin,
            transform: `scale(${scale}) translate(${tx}px, ${ty}px)`,
            filter: archivalFilter,
          }}
        />
      )}
      {dim > 0 && <AbsoluteFill style={{ background: `rgba(0,0,0,${dim})` }} />}
      {flashes && <Flashes />}
      {fog > 0 && <Fog density={fog} />}
    </AbsoluteFill>
  );
};
