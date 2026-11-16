import React from "react";
import { AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { accent, fonts } from "./theme";
import type { Accent } from "./types";
import { CensoredText } from "./CensoredText";

// Palabra gigante que entra de golpe (escala 2.4 → 1), tiembla un instante y queda.
export const Slam: React.FC<{ text: string; color?: Accent; y?: number; size?: number }> = ({ text, color = "cream", y = 980, size }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const hit = interpolate(frame, [0, 5], [2.4, 1], { extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  const settle = spring({ frame: frame - 5, fps, config: { damping: 9, stiffness: 260, mass: 0.5 } });
  const scale = frame < 5 ? hit : 1 + (1 - settle) * 0.08;
  const shake = frame >= 5 && frame < 14 ? (random(`slam-${frame}`) - 0.5) * 18 : 0;
  const fontSize = size ?? (text.length > 10 ? 120 : text.length > 6 ? 150 : 190);
  const c = accent[color];
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          top: y - fontSize * 0.6,
          left: 0,
          right: 0,
          textAlign: "center",
          fontFamily: fonts.title,
          fontWeight: 900,
          fontSize,
          lineHeight: 1,
          letterSpacing: -3,
          color: c,
          textTransform: "uppercase",
          WebkitTextStroke: "3px rgba(0,0,0,0.85)",
          textShadow: `0 0 40px ${c}88, 0 10px 40px rgba(0,0,0,0.9)`,
          transform: `translate(${shake}px, ${shake * 0.6}px) scale(${scale})`,
          opacity: interpolate(frame, [0, 2], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        <CensoredText text={text} blur={1.5} />
      </div>
    </AbsoluteFill>
  );
};

// Mira de caza (anillo, cruz y marcas de distancia) que se cierra sobre el blanco y se fija en rojo.
export const Reticle: React.FC<{ x?: number; y?: number; lock?: number }> = ({ x = 540, y = 980, lock = 1.2 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const p = interpolate(t, [0, lock], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const locked = t >= lock;
  const r = 330 - 150 * p;
  const color = locked ? accent.red : "#E8F0E8";
  const jx = locked ? 0 : Math.sin(t * 9) * 14 * (1 - p);
  const jy = locked ? 0 : Math.cos(t * 7) * 10 * (1 - p);
  const blink = locked && Math.floor(frame / 6) % 2 === 0;
  const rot = (1 - p) * 40;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <svg width={1080} height={1920}>
        <g transform={`translate(${x + jx}, ${y + jy}) rotate(${rot})`} stroke={color} fill="none" strokeWidth={5} opacity={0.92}>
          <circle r={r} strokeDasharray="22 14" />
          <circle r={r * 0.32} strokeWidth={4} />
          <circle r={7} fill={color} />
          {[0, 90, 180, 270].map((a) => (
            <line key={a} x1={0} y1={-r - 40} x2={0} y2={-r * 0.45} transform={`rotate(${a})`} strokeWidth={6} />
          ))}
          {Array.from({ length: 24 }, (_, i) => (
            <line key={i} x1={0} y1={-r} x2={0} y2={-r + (i % 2 ? 14 : 26)} transform={`rotate(${i * 15})`} strokeWidth={3} />
          ))}
        </g>
      </svg>
      <div
        style={{
          position: "absolute",
          left: x - 200,
          top: y + 230,
          width: 400,
          textAlign: "center",
          fontFamily: fonts.mono,
          fontWeight: 700,
          fontSize: 38,
          letterSpacing: 6,
          color,
          opacity: locked ? (blink ? 1 : 0.35) : 0.8,
          textShadow: "0 2px 10px rgba(0,0,0,0.9)",
        }}
      >
        {locked ? "◉ BLANCO FIJADO" : `DIST ${Math.round(900 - 700 * p)} M`}
      </div>
    </AbsoluteFill>
  );
};

// Destello blanco cálido de un impacto. La sacudida la aplica ShortVideo a toda la escena.
export const ImpactFlash: React.FC<{ strength?: number }> = ({ strength = 1 }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 2, 10], [0, 0.75 * strength, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 50%, rgba(255,246,225,1), rgba(255,200,140,0.7))", opacity: o, pointerEvents: "none" }} />;
};

// Desplazamiento de cámara de una sacudida que empezó hace `since` cuadros.
export function shakeOffset(since: number, strength: number, fps: number): [number, number, number] {
  const dur = 0.45 * fps;
  if (since < 0 || since > dur) return [0, 0, 0];
  const k = (1 - since / dur) ** 2 * strength;
  return [(random(`sx-${since}`) - 0.5) * 60 * k, (random(`sy-${since}`) - 0.5) * 60 * k, (random(`sr-${since}`) - 0.5) * 2.2 * k];
}

// ───────────── siluetas vistas desde arriba (nariz hacia arriba) ─────────────

// B-17: envergadura 420, largo 300, origen en el centro del ala.
export const B17_PARTS = {
  nose: [0, -128],
  cockpit: [0, -92],
  engine1: [-135, -16],
  engine2: [-70, -24],
  engine3: [70, -24],
  engine4: [135, -16],
  waist: [0, 70],
  tail: [0, 160],
} as const;

export const B17Top: React.FC<{ fill?: string; stroke?: string; strokeWidth?: number; noseGone?: boolean; props?: number; deadEngines?: number[] }> = ({
  fill = "#2a2d30",
  stroke = "#0d0d0d",
  strokeWidth = 3,
  noseGone,
  props = 0,
  deadEngines = [],
}) => (
  <g stroke={stroke} strokeWidth={strokeWidth} strokeLinejoin="round">
    {/* ala */}
    <path d="M-210,-6 L-24,-40 L24,-40 L210,-6 L210,10 L24,22 L-24,22 L-210,10 Z" fill={fill} />
    {/* estabilizador */}
    <path d="M-88,150 L-14,128 L14,128 L88,150 L88,168 L14,172 L-14,172 L-88,168 Z" fill={fill} />
    {/* fuselaje */}
    <path d={noseGone ? "M-20,-108 L20,-108 L22,-60 L20,150 L10,184 L-10,184 L-20,150 L-22,-60 Z" : "M0,-150 C14,-150 22,-128 22,-100 L22,-60 L20,150 L10,184 L-10,184 L-20,150 L-22,-60 L-22,-100 C-22,-128 -14,-150 0,-150 Z"} fill={fill} />
    {noseGone && <path d="M-20,-108 L-12,-118 L-4,-109 L5,-120 L12,-110 L20,-108" fill="none" stroke="#c9b48a" strokeWidth={3} />}
    {/* motores y hélices */}
    {[-135, -70, 70, 135].map((x, i) => (
      <g key={x}>
        <rect x={x - 10} y={-58} width={20} height={58} rx={8} fill={fill} />
        {deadEngines.includes(i + 1) ? (
          <line x1={x - 22} y1={-62} x2={x + 22} y2={-58} stroke="#c9b48a" strokeWidth={4} />
        ) : (
          <ellipse cx={x} cy={-62} rx={26} ry={4} fill="rgba(220,220,220,0.35)" stroke="none" transform={`rotate(${props * (i % 2 ? 1 : -1)}, ${x}, -62)`} />
        )}
      </g>
    ))}
  </g>
);

// Bf 109: envergadura ~200, más corto y fino.
export const Bf109Top: React.FC<{ fill?: string; props?: number }> = ({ fill = "#5b6066", props = 0 }) => (
  <g stroke="#0d0d0d" strokeWidth={3} strokeLinejoin="round">
    <path d="M-100,-4 C-100,-12 -30,-22 -14,-24 L14,-24 C30,-22 100,-12 100,-4 L96,8 L14,14 L-14,14 L-96,8 Z" fill={fill} />
    <path d="M-38,96 L-8,88 L8,88 L38,96 L36,106 L-36,106 Z" fill={fill} />
    <path d="M0,-80 C8,-80 12,-66 12,-50 L10,90 L4,112 L-4,112 L-10,90 L-12,-50 C-12,-66 -8,-80 0,-80 Z" fill={fill} />
    <ellipse cx={0} cy={-30} rx={6} ry={14} fill="#9fb4c2" stroke="none" opacity={0.7} />
    <ellipse cx={0} cy={-84} rx={30} ry={4} fill="rgba(220,220,220,0.35)" stroke="none" transform={`rotate(${props}, 0, -84)`} />
  </g>
);
