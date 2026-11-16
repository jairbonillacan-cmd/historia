import React from "react";
import { AbsoluteFill, interpolate, random, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { accent, fonts } from "./theme";
import type { Visual } from "./types";

// ───────────── corte transversal de una colina con galerías de mina ─────────────
// Trinchera propia a la izquierda, trinchera enemiga en la cima. El dibujo va bajo (y≈950–1500) para dejar
// libres las zonas de títulos y datos; sus textos no bajan de y=1500.

type Props = Extract<Visual, { kind: "mine" }>;

const CREST_X = 720;
const SURFACE = (x: number) => 1100 - 150 * Math.exp(-(((x - CREST_X) / 260) ** 2));
const OWN_X = 170;
const CLAY_TOP = 1350;
const CLAY_BOTTOM = 1560;
const SKY = "#2a2d31";
const MUD = ["#4a3a2a", "#3b2e21"];
const CLAY = "#3a5163";
const TUNNEL = "#120d08";

// Galerías: profundidad y punto final de cada una (la primera es la principal).
const GALLERIES = [
  { y: 1455, end: CREST_X, chamber: true },
  { y: 1415, end: CREST_X - 150, chamber: true },
  { y: 1500, end: CREST_X + 150, chamber: true },
];

function surfacePath(crater: number, dome: number): string {
  const pts: string[] = [];
  for (let x = -20; x <= 1100; x += 10) {
    const g = Math.exp(-(((x - CREST_X) / 190) ** 2));
    const y = SURFACE(x) + crater * 170 * g - dome * 260 * g;
    pts.push(`${x},${y.toFixed(1)}`);
  }
  return `M${pts.join(" L")}`;
}

const Label: React.FC<{ x: number; y: number; text: string; color: string; anchor?: "start" | "middle" | "end"; size?: number; o?: number }> = ({ x, y, text, color, anchor = "middle", size = 36, o = 1 }) => (
  <text x={x} y={y} textAnchor={anchor} fontFamily={fonts.title} fontWeight={900} fontSize={size} fill={color} stroke="#000" strokeWidth={7} paintOrder="stroke" letterSpacing={1} opacity={o}>
    {text}
  </text>
);

// Minero agachado con el pico; `listen` = oreja contra la pared con el estetoscopio.
const Miner: React.FC<{ x: number; y: number; swing: number; listen?: boolean }> = ({ x, y, swing, listen }) => (
  <g transform={`translate(${x}, ${y})`}>
    <circle cx={0} cy={-46} r={11} fill="#d8ccb0" />
    <path d="M-14,-52 Q0,-66 14,-52 Z" fill={accent.amber} />
    <path d="M-10,-34 L8,-34 L12,-8 L-14,-8 Z" fill="#d8ccb0" />
    <path d="M-12,-8 L-18,0 M10,-8 L16,0" stroke="#d8ccb0" strokeWidth={6} strokeLinecap="round" />
    {listen ? (
      <path d="M8,-44 Q30,-44 34,-30" fill="none" stroke={accent.cream} strokeWidth={3} />
    ) : (
      <g transform={`rotate(${swing}, 6, -30)`}>
        <line x1={6} y1={-30} x2={34} y2={-50} stroke="#8a7a60" strokeWidth={5} />
        <path d="M26,-60 L42,-42" stroke={accent.cream} strokeWidth={5} strokeLinecap="round" />
      </g>
    )}
  </g>
);

export const MineScene: React.FC<Props> = ({ stage, blastAt = 0.4, lost = false }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const zoom = interpolate(frame, [0, durationInFrames], [1.0, 1.07]);
  const draw = interpolate(frame, [0, 0.5 * fps], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });

  // Avance de la galería principal (solo en `dig`; en el resto ya está terminada).
  const dig = stage === "dig" ? interpolate(t, [0.3, durationInFrames / fps - 0.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.quad) }) : 1;
  const galleries = stage === "dig" || stage === "listen" ? GALLERIES.slice(0, 1) : GALLERIES;

  // Voladura: domo que sube, destello, escombros y polvo; queda el cráter.
  const bt = t - blastAt;
  const blasting = stage === "blast" && bt >= 0;
  const dome = blasting ? interpolate(bt, [0, 0.18, 0.5], [0, 1, 0], { extrapolateRight: "clamp" }) : 0;
  const crater = blasting ? interpolate(bt, [0.3, 0.9], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const flash = blasting ? interpolate(bt, [0, 0.05, 0.6], [0, 1, 0], { extrapolateRight: "clamp" }) : 0;

  const surf = surfacePath(crater, dome);
  const ground = `${surf} L1100,1960 L-20,1960 Z`;
  const tunnelPath = (g: (typeof GALLERIES)[number], p: number) => {
    const len = g.end - OWN_X;
    return `M${OWN_X},${SURFACE(OWN_X) + 20} L${OWN_X},${g.y} L${OWN_X + len * p},${g.y}`;
  };

  return (
    <AbsoluteFill style={{ background: SKY }}>
      <svg width={1080} height={1920} style={{ transform: `scale(${zoom})`, transformOrigin: "50% 60%" }}>
        <defs>
          <linearGradient id="mine-sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#121417" />
            <stop offset="100%" stopColor={SKY} />
          </linearGradient>
          <linearGradient id="mine-mud" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={MUD[0]} />
            <stop offset="100%" stopColor={MUD[1]} />
          </linearGradient>
          <clipPath id="mine-ground">
            <path d={ground} />
          </clipPath>
          <radialGradient id="mine-glow">
            <stop offset="0%" stopColor="#fff2c8" />
            <stop offset="45%" stopColor="#ff9a3c" stopOpacity={0.9} />
            <stop offset="100%" stopColor="#ff6a00" stopOpacity={0} />
          </radialGradient>
        </defs>
        <rect width={1080} height={1920} fill="url(#mine-sky)" />
        <path d={ground} fill="url(#mine-mud)" />
        <g clipPath="url(#mine-ground)">
          <rect x={0} y={CLAY_TOP} width={1080} height={CLAY_BOTTOM - CLAY_TOP} fill={CLAY} />
          {Array.from({ length: 60 }, (_, i) => (
            <circle key={i} cx={random(`pb-x-${i}`) * 1080} cy={1150 + random(`pb-y-${i}`) * 900} r={2 + random(`pb-r-${i}`) * 5} fill="#000" opacity={0.18} />
          ))}
          {/* galerías */}
          {galleries.map((g, i) => {
            const p = i === 0 ? dig : interpolate(t, [0.2 + i * 0.25, 0.9 + i * 0.25], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            const tip = OWN_X + (g.end - OWN_X) * p;
            const isLost = lost && i === 1;
            return (
              <g key={i} opacity={draw}>
                <path d={tunnelPath(g, p)} fill="none" stroke={TUNNEL} strokeWidth={30} strokeLinejoin="round" />
                <path d={tunnelPath(g, p)} fill="none" stroke="#7a6446" strokeWidth={2} strokeDasharray="6 22" />
                {g.chamber && p >= 1 && stage !== "dig" && !blasting && (
                  <g>
                    <rect x={g.end - 38} y={g.y - 30} width={76} height={60} rx={6} fill={isLost ? "#333" : accent.red} stroke="#000" strokeWidth={4} />
                    {!isLost && <rect x={g.end - 38} y={g.y - 30} width={76} height={60} rx={6} fill="#fff" opacity={0.25 * (0.5 + 0.5 * Math.sin(t * 6 + i))} />}
                    {isLost && (
                      <g stroke={accent.cream} strokeWidth={8} strokeLinecap="round">
                        <line x1={g.end - 46} y1={g.y - 38} x2={g.end + 46} y2={g.y + 38} />
                        <line x1={g.end + 46} y1={g.y - 38} x2={g.end - 46} y2={g.y + 38} />
                      </g>
                    )}
                  </g>
                )}
                {stage === "dig" && i === 0 && p > 0 && p < 1 && <Miner x={tip - 20} y={g.y + 14} swing={Math.sin(t * 11) * 25} />}
                {stage === "dig" && i === 0 && p > 0 && p < 1 && Math.sin(t * 11) > 0.7 && (
                  <g>
                    {[0, 1, 2, 3].map((k) => (
                      <circle key={k} cx={tip + 6 + random(`sp-${frame}-${k}`) * 16} cy={g.y - 10 + random(`sq-${frame}-${k}`) * 20} r={3} fill={accent.amber} />
                    ))}
                  </g>
                )}
              </g>
            );
          })}
          {/* contramina alemana que baja a cazarlos */}
          {stage === "listen" && (
            <ListenLayer t={t} />
          )}
        </g>
        <path d={surf} fill="none" stroke="#1a140e" strokeWidth={6} />
        {/* trincheras */}
        {!blasting && (
          <g>
            <rect x={CREST_X - 70} y={SURFACE(CREST_X) - 4} width={140} height={34} fill="#1a140e" />
            <Label x={CREST_X - 40} y={SURFACE(CREST_X) + 80} text="ALEMANES" color={accent.red} o={draw} />
          </g>
        )}
        <rect x={OWN_X - 60} y={SURFACE(OWN_X) - 4} width={120} height={34} fill="#1a140e" />
        <Label x={OWN_X + 34} y={SURFACE(OWN_X) + 190} text="BRITÁNICOS" color={accent.blue} anchor="start" o={draw} />
        {/* regla de profundidad */}
        <g opacity={draw}>
          <line x1={1010} y1={SURFACE(1010)} x2={1010} y2={GALLERIES[0].y} stroke={accent.cream} strokeWidth={4} />
          {[0, 1, 2, 3].map((k) => {
            const y = SURFACE(1010) + ((GALLERIES[0].y - SURFACE(1010)) * k) / 3;
            return <line key={k} x1={990} y1={y} x2={1030} y2={y} stroke={accent.cream} strokeWidth={4} />;
          })}
          <Label x={990} y={GALLERIES[0].y + 12} text="30 M" color={accent.cream} anchor="end" size={44} />
          <Label x={70} y={CLAY_TOP + 60} text="ARCILLA AZUL" color="#a9c7dc" anchor="start" size={30} />
        </g>
        {blasting && <Blast bt={bt} />}
      </svg>
      {flash > 0 && <AbsoluteFill style={{ background: "radial-gradient(circle at 67% 50%, #fff8e0, #ffb060 60%, rgba(255,120,0,0.4))", opacity: flash }} />}
    </AbsoluteFill>
  );
};

// Pozo alemán que baja desde la cima y ondas de ruido que llegan al minero que escucha.
const ListenLayer: React.FC<{ t: number }> = ({ t }) => {
  const p = interpolate(t, [0.2, 3.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const x0 = CREST_X + 60;
  const y0 = SURFACE(x0) + 20;
  const y1 = y0 + (1350 - y0) * p;
  const listenerX = CREST_X - 150;
  return (
    <g>
      <path d={`M${x0},${y0} L${x0},${y1}`} stroke="#000" strokeWidth={26} />
      <path d={`M${x0},${y0} L${x0},${y1}`} stroke={accent.red} strokeWidth={3} strokeDasharray="10 12" />
      {[0, 1, 2].map((k) => {
        const ph = ((t * 0.9 + k / 3) % 1);
        return <circle key={k} cx={x0} cy={y1} r={30 + ph * 220} fill="none" stroke={accent.red} strokeWidth={5} opacity={(1 - ph) * 0.8} />;
      })}
      <Miner x={listenerX} y={GALLERIES[0].y + 14} swing={0} listen />
      <Label x={x0 - 34} y={y1 - 20} text="ZAPADORES" color={accent.red} anchor="end" size={32} />
    </g>
  );
};

// Columna de tierra, escombros con trayectoria balística y nube de polvo.
const Blast: React.FC<{ bt: number }> = ({ bt }) => {
  const cy = SURFACE(CREST_X);
  const plume = interpolate(bt, [0, 0.6, 3], [0, 1, 1.25], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const fire = interpolate(bt, [0, 0.1, 1.2], [0, 1, 0], { extrapolateRight: "clamp" });
  return (
    <g>
      <ellipse cx={CREST_X} cy={cy - 260 * plume} rx={260 * plume} ry={330 * plume} fill="#2b2118" opacity={0.85} />
      <ellipse cx={CREST_X - 170 * plume} cy={cy - 120 * plume} rx={200 * plume} ry={170 * plume} fill="#3a2d20" opacity={0.75} />
      <ellipse cx={CREST_X + 180 * plume} cy={cy - 140 * plume} rx={210 * plume} ry={180 * plume} fill="#33281c" opacity={0.75} />
      <ellipse cx={CREST_X} cy={cy - 120 * plume} rx={240 * fire + 1} ry={280 * fire + 1} fill="url(#mine-glow)" opacity={fire} />
      {Array.from({ length: 70 }, (_, i) => {
        const ang = (-90 + (random(`db-a-${i}`) - 0.5) * 120) * (Math.PI / 180);
        const v = 900 + random(`db-v-${i}`) * 1400;
        const x = CREST_X + Math.cos(ang) * v * bt;
        const y = cy + Math.sin(ang) * v * bt + 0.5 * 2600 * bt * bt;
        if (y > 1700 || bt <= 0) return null;
        const s = 5 + random(`db-s-${i}`) * 14;
        return <rect key={i} x={x} y={y} width={s} height={s * 0.7} fill={i % 5 ? "#1e1710" : "#5a4632"} transform={`rotate(${bt * 400 * (random(`db-r-${i}`) - 0.5)}, ${x}, ${y})`} />;
      })}
    </g>
  );
};
