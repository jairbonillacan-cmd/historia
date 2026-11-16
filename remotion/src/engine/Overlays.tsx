import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { accent, fonts, layout } from "./theme";
import type { Overlay } from "./types";
import { CensoredText } from "./CensoredText";
import { ImpactFlash, Reticle, Slam } from "./Motion";
import { Countdown, Embers, Options, RedPulse, Spotlight, Stamp } from "./Kinetic";

export const OverlayLayer: React.FC<{ overlay: Overlay }> = ({ overlay }) => {
  switch (overlay.kind) {
    case "ribbon":
      return <Ribbon text={overlay.text} />;
    case "stat":
      return <Stat {...overlay} />;
    case "title":
      return <Title text={overlay.text} color={accent[overlay.color ?? "cream"]} top={overlay.low ? layout.titleLowY : layout.titleY} />;
    case "caption":
      return <PhotoCaption text={overlay.text} source={overlay.source} />;
    case "slam":
      return <Slam text={overlay.text} color={overlay.color} y={overlay.y} size={overlay.size} />;
    case "reticle":
      return <Reticle x={overlay.x} y={overlay.y} lock={overlay.lock} />;
    case "impact":
      return <ImpactFlash strength={overlay.strength} />;
    case "stamp":
      return <Stamp text={overlay.text} color={overlay.color} y={overlay.y} rotate={overlay.rotate} />;
    case "options":
      return <Options items={overlay.items} times={overlay.times} crossAt={overlay.crossAt} title={overlay.title} />;
    case "countdown":
      return <Countdown hours={overlay.hours} dur={overlay.dur} label={overlay.label} />;
    case "spotlight":
      return <Spotlight x={overlay.x} y={overlay.y} r={overlay.r} label={overlay.label} color={overlay.color} />;
    case "embers":
      return <Embers intensity={overlay.intensity} />;
    case "redpulse":
      return <RedPulse bpm={overlay.bpm} />;
  }
};

// Cinta de fecha estilo máquina de escribir, con barra roja a la izquierda.
const Ribbon: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const reveal = interpolate(frame, [0, 0.45 * fps], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const chars = Math.round(text.length * interpolate(frame, [4, 4 + text.length * 1.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          top: layout.ribbonY,
          left: 56,
          display: "flex",
          alignItems: "stretch",
          transform: `translateX(${(1 - reveal) * -40}px)`,
          opacity: reveal,
          boxShadow: "0 6px 20px rgba(0,0,0,0.45)",
        }}
      >
        <div style={{ width: 8, background: accent.red }} />
        <div
          style={{
            background: "#EFE8D6",
            color: "#1b1b1b",
            fontFamily: fonts.mono,
            fontWeight: 700,
            fontSize: 34,
            letterSpacing: 2,
            padding: "8px 18px 6px",
            whiteSpace: "pre",
          }}
        >
          {text.slice(0, chars)}
          <span style={{ opacity: 0 }}>{text.slice(chars)}</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const statTop = (slot: number) => layout.statY + slot * 175;

// Dato grande con conteo animado, sobre placa oscura semitransparente.
const Stat: React.FC<Extract<Overlay, { kind: "stat" }>> = ({ value, prefix = "", suffix = "", label, color = "amber", slot = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame, fps, config: { damping: 14, stiffness: 160, mass: 0.7 } });
  const count = interpolate(frame, [0, 0.7 * fps], [0, value], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const shown = value >= 1000 ? Math.round(count).toLocaleString("es-AR") : Math.round(count).toString();
  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          top: statTop(slot),
          left: 56,
          padding: "14px 28px 16px",
          background: "rgba(14,14,14,0.78)",
          borderRadius: 10,
          border: "1px solid rgba(255,255,255,0.08)",
          transform: `scale(${0.6 + 0.4 * pop})`,
          transformOrigin: "left center",
          opacity: Math.min(1, pop * 1.5),
        }}
      >
        <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 120, lineHeight: 1, color: accent[color], letterSpacing: -2 }}>
          {prefix}
          {shown}
          {suffix}
        </div>
        <div style={{ fontFamily: fonts.body, fontWeight: 800, fontSize: 30, color: "#fff", letterSpacing: 1.5, marginTop: 6 }}>
          <CensoredText text={label} blur={1.2} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Titular grande centrado (p. ej. «UNA CARNICERÍA»).
const Title: React.FC<{ text: string; color: string; top: number }> = ({ text, color, top }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame, fps, config: { damping: 12, stiffness: 180, mass: 0.6 } });
  const fontSize = text.length > 18 ? 74 : text.length > 12 ? 92 : 112;
  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          top,
          left: 60,
          right: 60,
          textAlign: "center",
          fontFamily: fonts.title,
          fontWeight: 900,
          fontSize,
          lineHeight: 1.02,
          color,
          letterSpacing: -1,
          textTransform: "uppercase",
          textShadow: "0 6px 30px rgba(0,0,0,0.85), 0 2px 4px rgba(0,0,0,0.6)",
          transform: `scale(${1.25 - 0.25 * pop})`,
          opacity: Math.min(1, pop * 1.4),
        }}
      >
        <CensoredText text={text} blur={fontSize * 0.025} />
      </div>
    </AbsoluteFill>
  );
};

// Pie de foto abajo a la izquierda + línea de fuente.
const PhotoCaption: React.FC<{ text: string; source?: string }> = ({ text, source }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const o = interpolate(frame, [0, 0.35 * fps], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", top: layout.photoCaptionY, left: 56, right: 56, opacity: o }}>
        <div
          style={{
            display: "inline-block",
            background: "rgba(10,10,10,0.82)",
            color: "#fff",
            fontFamily: fonts.body,
            fontWeight: 700,
            fontSize: 32,
            padding: "8px 16px",
            borderRadius: 6,
          }}
        >
          <CensoredText text={text} blur={1.2} />
        </div>
        <div
          style={{
            marginTop: 10,
            color: "rgba(255,255,255,0.72)",
            fontFamily: fonts.body,
            fontWeight: 600,
            fontSize: 20,
            letterSpacing: 1.2,
            textTransform: "uppercase",
            textShadow: "0 1px 4px rgba(0,0,0,0.9)",
          }}
        >
          {source ?? "Foto de archivo · Wikimedia Commons · Dominio público"}
        </div>
      </div>
    </AbsoluteFill>
  );
};
