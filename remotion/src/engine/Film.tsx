import React from "react";
import { AbsoluteFill, random, useCurrentFrame, useVideoConfig, interpolate } from "remotion";

// Grano de película: ruido SVG que cambia cada 2 cuadros.
export const Grain: React.FC<{ opacity?: number }> = ({ opacity = 0.16 }) => {
  const frame = useCurrentFrame();
  const seed = Math.floor(frame / 2) % 97;
  return (
    <AbsoluteFill style={{ mixBlendMode: "overlay", opacity, pointerEvents: "none" }}>
      <svg width="100%" height="100%" viewBox="0 0 540 960" preserveAspectRatio="none">
        <filter id={`grain-${seed}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={seed} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="540" height="960" filter={`url(#grain-${seed})`} />
      </svg>
    </AbsoluteFill>
  );
};

export const Vignette: React.FC<{ strength?: number }> = ({ strength = 0.75 }) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(ellipse 75% 60% at 50% 48%, rgba(0,0,0,0) 45%, rgba(0,0,0,${strength}) 100%)`,
      pointerEvents: "none",
    }}
  />
);

// Parpadeo de exposición, como proyector viejo.
export const Flicker: React.FC = () => {
  const frame = useCurrentFrame();
  const v = (random(`flick-${Math.floor(frame / 3)}`) - 0.5) * 0.06;
  return <AbsoluteFill style={{ background: v > 0 ? `rgba(255,248,230,${v})` : `rgba(0,0,0,${-v})`, pointerEvents: "none" }} />;
};

// Bancos de niebla que se desplazan lento. `density` 0..1.
export const Fog: React.FC<{ density: number }> = ({ density }) => {
  const frame = useCurrentFrame();
  const layers = [0, 1, 2];
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {layers.map((i) => {
        const x = ((frame * (0.35 + i * 0.22)) % 1600) - 400;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: -1200 + x * (i % 2 ? -1 : 1),
              top: 380 + i * 360,
              width: 3400,
              height: 900,
              background: "radial-gradient(ellipse 30% 50% at 30% 50%, rgba(225,228,230,0.9), rgba(225,228,230,0) 70%), radial-gradient(ellipse 25% 45% at 70% 45%, rgba(225,228,230,0.8), rgba(225,228,230,0) 70%)",
              filter: "blur(40px)",
              opacity: density * (0.55 + i * 0.12),
            }}
          />
        );
      })}
      <AbsoluteFill style={{ background: `rgba(200,205,210,${density * 0.25})` }} />
    </AbsoluteFill>
  );
};

// Destellos de explosiones/antiaéreos repartidos de forma determinista.
export const Flashes: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const period = Math.round(0.45 * fps);
  const k = Math.floor(frame / period);
  const local = frame - k * period;
  const x = 150 + random(`fx-${k}`) * 780;
  const y = 700 + random(`fy-${k}`) * 600;
  const o = interpolate(local, [0, 3, 14], [0, 1, 0], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ pointerEvents: "none", mixBlendMode: "screen" }}>
      <div
        style={{
          position: "absolute",
          left: x - 160,
          top: y - 160,
          width: 320,
          height: 320,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(255,240,200,0.95), rgba(255,170,80,0.35) 40%, rgba(255,140,60,0) 70%)",
          opacity: o,
        }}
      />
    </AbsoluteFill>
  );
};
