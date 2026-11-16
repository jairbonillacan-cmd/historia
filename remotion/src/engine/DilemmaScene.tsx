import React from "react";
import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { accent, archivalFilter, fonts } from "./theme";
import { CensoredText } from "./CensoredText";

type Props = {
  folder: string;
  background: string;
  question: string;
  a: string;
  b: string;
  footer: string;
  // segundos (relativos a la escena) en los que entra cada opción y el pie
  aAt: number;
  bAt: number;
  footerAt: number;
};

// Cierre: dilema binario para invitar a comentar.
export const DilemmaScene: React.FC<Props> = ({ folder, background, question, a, b, footer, aAt, bAt, footerAt }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = (at: number) => spring({ frame: frame - at * fps, fps, config: { damping: 11, stiffness: 170, mass: 0.6 } });
  const qIn = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: "clamp" });
  const tilt = Math.sin((frame / fps) * 1.6) * 4;

  const option = (label: string, color: string, p: number, side: -1 | 1) => (
    <div
      style={{
        width: 420,
        padding: "34px 0 30px",
        textAlign: "center",
        background: "rgba(12,12,12,0.86)",
        border: `4px solid ${color}`,
        borderRadius: 18,
        transform: `scale(${0.5 + 0.5 * p}) rotate(${side * (1 - p) * 8}deg)`,
        opacity: Math.min(1, p * 1.5),
        boxShadow: `0 0 50px ${color}55`,
      }}
    >
      <div style={{ fontFamily: fonts.body, fontWeight: 800, fontSize: 28, color: "rgba(255,255,255,0.7)", letterSpacing: 3 }}>{side < 0 ? "OPCIÓN A" : "OPCIÓN B"}</div>
      <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 78, color, lineHeight: 1.05, marginTop: 6 }}>{label}</div>
    </div>
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#0b0b0b" }}>
      <Img src={staticFile(`${folder}/${background}`)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: `${archivalFilter} brightness(0.38) blur(3px)` }} />
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 600 }}>
        <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 70, color: accent.cream, textAlign: "center", lineHeight: 1.05, padding: "0 70px", opacity: qIn, textShadow: "0 6px 30px rgba(0,0,0,0.9)" }}><CensoredText text={question} blur={1.8} /></div>
        <svg width={420} height={110} style={{ marginTop: 34, transform: `rotate(${tilt}deg)` }}>
          <line x1={20} y1={20} x2={400} y2={20} stroke={accent.amber} strokeWidth={8} strokeLinecap="round" />
          <line x1={210} y1={20} x2={210} y2={105} stroke={accent.amber} strokeWidth={8} />
          <circle cx={210} cy={20} r={12} fill={accent.amber} />
        </svg>
        <div style={{ display: "flex", gap: 40, marginTop: 20 }}>
          {option(a, accent.red, pop(aAt), -1)}
          {option(b, accent.blue, pop(bAt), 1)}
        </div>
        <div
          style={{
            marginTop: 70,
            padding: "18px 40px",
            borderRadius: 999,
            background: accent.red,
            color: "#fff",
            fontFamily: fonts.body,
            fontWeight: 800,
            fontSize: 38,
            letterSpacing: 1,
            transform: `scale(${pop(footerAt) * (1 + Math.sin((frame / fps) * 8) * 0.03)})`,
          }}
        >
          {footer}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
