import React from "react";
import { AbsoluteFill, interpolate, random, useCurrentFrame, useVideoConfig } from "remotion";
import { fonts } from "./theme";

const CX = 540;
const CY = 870;
const R = 360;
const GREEN = "#7CFFB2";
const BLIPS = 7;

// Pantalla de radar de 1943: barrido continuo y, si `blips`, los siete ecos fantasma.
export const RadarScene: React.FC<{ blips: boolean }> = ({ blips }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sweep = ((frame / fps) * 150) % 360; // grados

  return (
    <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 53%, #0f2a1d 0%, #06120c 55%, #030806 100%)" }}>
      <svg width={1080} height={1920}>
        <defs>
          <radialGradient id="scope" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#123d29" />
            <stop offset="100%" stopColor="#071a10" />
          </radialGradient>
          <linearGradient id="beam" gradientUnits="userSpaceOnUse" x1={CX} y1={CY} x2={CX + R} y2={CY}>
            <stop offset="0%" stopColor={GREEN} stopOpacity={0.6} />
            <stop offset="100%" stopColor={GREEN} stopOpacity={0.05} />
          </linearGradient>
        </defs>
        <circle cx={CX} cy={CY} r={R + 24} fill="#1c1f1d" stroke="#3a3f3b" strokeWidth={6} />
        <circle cx={CX} cy={CY} r={R} fill="url(#scope)" />
        {[0.25, 0.5, 0.75, 1].map((k) => (
          <circle key={k} cx={CX} cy={CY} r={R * k} fill="none" stroke={GREEN} strokeOpacity={0.22} strokeWidth={2} />
        ))}
        {[0, 30, 60, 90, 120, 150].map((a) => {
          const rad = (a * Math.PI) / 180;
          return <line key={a} x1={CX - Math.cos(rad) * R} y1={CY - Math.sin(rad) * R} x2={CX + Math.cos(rad) * R} y2={CY + Math.sin(rad) * R} stroke={GREEN} strokeOpacity={0.12} strokeWidth={2} />;
        })}
        {/* estela del barrido */}
        {Array.from({ length: 28 }, (_, i) => {
          const a = ((sweep - i * 1.6) * Math.PI) / 180;
          return <line key={i} x1={CX} y1={CY} x2={CX + Math.cos(a) * R} y2={CY + Math.sin(a) * R} stroke={GREEN} strokeOpacity={0.5 * (1 - i / 28)} strokeWidth={5} />;
        })}
        {blips &&
          Array.from({ length: BLIPS }, (_, i) => {
            const ang = 200 + random(`ba-${i}`) * 70;
            const dist = 0.45 + random(`bd-${i}`) * 0.4;
            const a = (ang * Math.PI) / 180;
            const x = CX + Math.cos(a) * R * dist;
            const y = CY + Math.sin(a) * R * dist;
            const since = (((sweep - ang) % 360) + 360) % 360;
            const glow = interpolate(since, [0, 300], [1, 0.15], { extrapolateRight: "clamp" });
            const appear = interpolate(frame, [i * 5, i * 5 + 10], [0, 1], { extrapolateRight: "clamp" });
            return (
              <g key={i} opacity={appear}>
                <circle cx={x} cy={y} r={22} fill={GREEN} opacity={glow * 0.25} />
                <circle cx={x} cy={y} r={10} fill={GREEN} opacity={glow} />
              </g>
            );
          })}
        <circle cx={CX} cy={CY} r={8} fill={GREEN} />
        <text x={CX} y={CY - R + 70} textAnchor="middle" fontFamily={fonts.mono} fontWeight={700} fontSize={28} fill={GREEN} opacity={0.85} letterSpacing={3}>
          {blips ? `CONTACTOS: ${BLIPS}` : "CONTACTOS: 0"}
        </text>
      </svg>
    </AbsoluteFill>
  );
};
