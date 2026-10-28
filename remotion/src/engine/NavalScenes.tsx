import React from "react";
import { AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { accent, fonts } from "./theme";
import type { Visual } from "./types";

// ───────────── acorazados de perfil sobre el mar ─────────────

// Silueta de un acorazado tipo dreadnought de la Primera Guerra, proa a la izquierda, línea de flotación en y=0.
// Mide ~1000 de largo; `funnels` devuelve la boca de cada chimenea para el humo.
const SHIP_FUNNELS: [number, number][] = [
  [-60, -190],
  [70, -190],
];
const SHIP_MASTS: [number, number][] = [
  [-210, -330],
  [250, -300],
];

export const Dreadnought: React.FC<{ fill: string; flag?: number }> = ({ fill, flag = 0 }) => (
  <g>
    {/* casco */}
    <path d="M-520,-40 L-480,-62 L470,-62 L500,-48 L490,0 L-470,0 Z" fill={fill} />
    {/* torres de proa, centro y popa */}
    {[-390, -300, 300, 395].map((x, i) => (
      <g key={i}>
        <rect x={x - 38} y={-96} width={76} height={34} rx={6} fill={fill} />
        <rect x={x + (x < 0 ? -78 : 20)} y={-86} width={58} height={8} fill={fill} />
      </g>
    ))}
    {/* superestructura y puente */}
    <rect x={-250} y={-118} width={420} height={56} fill={fill} />
    <rect x={-240} y={-170} width={110} height={52} fill={fill} />
    <rect x={-228} y={-196} width={80} height={26} fill={fill} />
    <rect x={160} y={-150} width={90} height={32} fill={fill} />
    {/* chimeneas */}
    {SHIP_FUNNELS.map(([x, y], i) => (
      <path key={i} d={`M${x - 26},-118 L${x - 22},${y} L${x + 22},${y} L${x + 26},-118 Z`} fill={fill} />
    ))}
    {/* mástiles trípode */}
    {SHIP_MASTS.map(([x, y], i) => (
      <g key={i} stroke={fill} strokeWidth={6}>
        <line x1={x} y1={-118} x2={x} y2={y} />
        <line x1={x - 28} y1={-118} x2={x} y2={y + 70} />
        <line x1={x - 50} y1={y + 40} x2={x + 50} y2={y + 40} strokeWidth={5} />
      </g>
    ))}
    {/* bandera roja que se iza por el mástil de proa */}
    {flag > 0 && (
      <g transform={`translate(${SHIP_MASTS[0][0]}, ${-118 + (SHIP_MASTS[0][1] + 118) * flag})`}>
        <path d="M0,0 L96,8 L90,30 L96,54 L0,60 Z" fill={accent.red} />
      </g>
    )}
  </g>
);

type FleetProps = Extract<Visual, { kind: "fleet" }>;

// `port`: fondeados en el puerto, con grúas; `sail`: avanzando con humo; `mutiny`: banderas rojas que suben.
// `smoke: false` = calderas apagadas, sin humo. `night` = cielo nocturno con reflector.
export const FleetScene: React.FC<FleetProps> = ({ mode, smoke = true, night = false, ships = 3 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const HORIZON = 1180;
  const zoom = interpolate(frame, [0, durationInFrames], [1.0, 1.08]);
  const sky = night ? ["#05080f", "#101a2b", "#1c2638"] : ["#5a5f63", "#8a8d8c", "#a9a9a2"];
  const sea = night ? ["#0d1520", "#05090f"] : ["#4f5559", "#24292c"];
  const shipFill = night ? "#020305" : "#1b1d1f";
  const layout = [
    { x: 560, y: HORIZON + 240, s: 1.12, d: 0 },
    { x: 180, y: HORIZON + 70, s: 0.5, d: 1 },
    { x: 900, y: HORIZON + 30, s: 0.36, d: 2 },
    { x: 420, y: HORIZON + 8, s: 0.24, d: 3 },
  ].slice(0, ships);

  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${sky[0]} 0%, ${sky[1]} 45%, ${sky[2]} ${(HORIZON / 1920) * 100}%, ${sea[0]} ${(HORIZON / 1920) * 100}%, ${sea[1]} 100%)` }}>
      <svg width={1080} height={1920} style={{ transform: `scale(${zoom})`, transformOrigin: "50% 62%" }}>
        <defs>
          <filter id="smoke-blur" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation={18} />
          </filter>
        </defs>
        {night &&
          Array.from({ length: 70 }, (_, i) => (
            <circle key={i} cx={random(`sx${i}`) * 1080} cy={random(`sy${i}`) * 900} r={1 + random(`sr${i}`) * 1.6} fill="#fff" opacity={0.25 + 0.5 * random(`so${i}`) * (0.7 + 0.3 * Math.sin(t * 2 + i))} />
          ))}
        {night && (
          <polygon
            points={`120,${HORIZON} ${120 + Math.sin(t * 0.6) * 500 - 160},0 ${120 + Math.sin(t * 0.6) * 500 + 60},0`}
            fill="#f5f2eb"
            opacity={0.07}
          />
        )}
        {mode === "port" && <Harbor y={HORIZON} fill={night ? "#03050a" : "#2d3032"} />}
        {/* reflejos del agua */}
        {Array.from({ length: 26 }, (_, i) => {
          const y = HORIZON + 14 + i * i * 1.2;
          const off = ((t * (20 + i * 3)) % 220) - 110;
          return <line key={i} x1={-100 + off} y1={y} x2={1180 + off} y2={y} stroke="#e9e5da" strokeOpacity={0.04 + i * 0.002} strokeWidth={1 + i * 0.12} strokeDasharray={`${40 + i * 6} ${30 + i * 5}`} />;
        })}
        {[...layout].reverse().map((p, k) => {
          const drift = mode === "sail" ? -t * 26 * p.s : 0;
          const bob = Math.sin(t * 1.2 + p.d) * 4 * p.s;
          const flagT = mode === "mutiny" ? interpolate(t, [0.4 + p.d * 0.35, 1.8 + p.d * 0.35], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }) : 0;
          const haze = 1 - p.d * 0.18;
          return (
            <g key={k} transform={`translate(${p.x + drift}, ${p.y + bob}) scale(${p.s})`} opacity={haze}>
              {smoke && <Smoke t={t} seed={p.d} color={night ? "#5d626b" : "#2a2a2a"} />}
              <Dreadnought fill={shipFill} flag={flagT} />
              {mode === "sail" && <path d="M-520,-6 Q-600,10 -700,4 Q-600,22 -500,14 Z" fill="#e9e5da" opacity={0.35} />}
              <ellipse cx={0} cy={8} rx={540} ry={14} fill="#000" opacity={0.25} />
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

const Harbor: React.FC<{ y: number; fill: string }> = ({ y, fill }) => (
  <g fill={fill}>
    <rect x={-20} y={y - 40} width={1120} height={40} />
    {[90, 330, 780, 990].map((x, i) => (
      <g key={i}>
        <rect x={x} y={y - 260 + i * 20} width={14} height={220 - i * 20} />
        <rect x={x - 70} y={y - 270 + i * 20} width={150} height={12} />
        <line x1={x + 70} y1={y - 262 + i * 20} x2={x + 70} y2={y - 160 + i * 20} stroke={fill} strokeWidth={3} />
      </g>
    ))}
    {[200, 520, 640, 900].map((x, i) => (
      <rect key={i} x={x} y={y - 90 - (i % 2) * 30} width={110} height={60 + (i % 2) * 30} />
    ))}
  </g>
);

// Humo de carbón saliendo de las chimeneas: bocanadas que suben, crecen y se van con el viento.
const Smoke: React.FC<{ t: number; seed: number; color: string }> = ({ t, seed, color }) => (
  <g filter="url(#smoke-blur)">
    {SHIP_FUNNELS.map(([fx, fy], f) =>
      Array.from({ length: 9 }, (_, i) => {
        const life = 4.5;
        const age = (t + i * (life / 9) + seed * 0.7 + f * 0.3) % life;
        const p = age / life;
        return (
          <circle
            key={`${f}-${i}`}
            cx={fx + p * 260 + Math.sin(age * 2 + i) * 14}
            cy={fy - 20 - p * 340}
            r={30 + p * 120}
            fill={color}
            opacity={(1 - p) * 0.55}
          />
        );
      }),
    )}
  </g>
);

// ───────────── manómetro de las calderas que cae a cero ─────────────

type BoilerProps = Extract<Visual, { kind: "boiler" }>;

export const BoilerScene: React.FC<BoilerProps> = ({ from, to, dropAt = 0.6, dropDur = 2.4, label = "PRESIÓN DE CALDERAS" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const MAX = 20;
  const value = interpolate(t, [dropAt, dropAt + dropDur], [from, to], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.quad) });
  const jitter = value > 1 ? Math.sin(t * 37) * 0.12 + Math.sin(t * 23) * 0.08 : 0;
  const ang = (v: number) => -135 + (Math.min(MAX, Math.max(0, v)) / MAX) * 270;
  const heat = value / MAX; // el fuego del hogar se apaga con la presión
  const appear = spring({ frame, fps, config: { damping: 14, stiffness: 150 } });
  const CX = 540;
  const CY = 960;
  const R = 330;

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 55%, #2a2520, #0b0a09 75%)" }}>
      {/* resplandor del hogar */}
      <AbsoluteFill style={{ background: `radial-gradient(ellipse 70% 30% at 50% 100%, rgba(255,120,30,${0.55 * heat * (0.85 + 0.15 * Math.sin(t * 9))}), rgba(0,0,0,0) 70%)` }} />
      <svg width={1080} height={1920}>
        {/* remaches y caño de bronce */}
        <rect x={CX - 30} y={CY + R} width={60} height={260} fill="#6b5232" />
        <g transform={`translate(${CX}, ${CY}) scale(${0.85 + 0.15 * appear})`} opacity={appear}>
          <circle r={R + 40} fill="#8a6a3d" />
          <circle r={R + 22} fill="#b38c51" />
          <circle r={R} fill="#ece4cf" />
          {/* zona roja */}
          <path d={arc(R - 24, ang(16), ang(20))} stroke={accent.red} strokeWidth={34} fill="none" />
          {Array.from({ length: MAX + 1 }, (_, v) => {
            const a = (ang(v) * Math.PI) / 180;
            const long = v % 5 === 0;
            const r1 = R - (long ? 70 : 46);
            return (
              <g key={v}>
                <line x1={Math.sin(a) * r1} y1={-Math.cos(a) * r1} x2={Math.sin(a) * (R - 12)} y2={-Math.cos(a) * (R - 12)} stroke="#1d1a14" strokeWidth={long ? 8 : 4} />
                {long && (
                  <text x={Math.sin(a) * (R - 120)} y={-Math.cos(a) * (R - 120) + 22} textAnchor="middle" fontFamily={fonts.title} fontWeight={900} fontSize={60} fill="#1d1a14">
                    {v}
                  </text>
                )}
              </g>
            );
          })}
          <text y={130} textAnchor="middle" fontFamily={fonts.mono} fontWeight={700} fontSize={42} fill="#5a4a30">
            ATM
          </text>
          <g transform={`rotate(${ang(value + jitter)})`}>
            <path d={`M-14,40 L0,${-R + 50} L14,40 Z`} fill={value < 1 ? accent.red : "#1d1a14"} />
          </g>
          <circle r={34} fill="#2b2b2b" />
          <circle r={12} fill="#b38c51" />
        </g>
        <text x={CX} y={520} textAnchor="middle" fontFamily={fonts.title} fontWeight={900} fontSize={60} letterSpacing={3} fill={accent.cream}>
          {label}
        </text>
        <text x={CX} y={1440} textAnchor="middle" fontFamily={fonts.title} fontWeight={900} fontSize={110} fill={value < 1 ? accent.red : accent.amber}>
          {value.toFixed(1).replace(".", ",")}
        </text>
      </svg>
    </AbsoluteFill>
  );
};

function arc(r: number, a0: number, a1: number): string {
  const p = (a: number) => [Math.sin((a * Math.PI) / 180) * r, -Math.cos((a * Math.PI) / 180) * r];
  const [x0, y0] = p(a0);
  const [x1, y1] = p(a1);
  return `M${x0},${y0} A${r},${r} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1},${y1}`;
}

// ───────────── línea de tiempo vertical ─────────────

type TimelineProps = Extract<Visual, { kind: "timeline" }>;

// Cada hito entra a los `at` segundos de la escena; la línea se dibuja hasta el último visible.
export const TimelineScene: React.FC<TimelineProps> = ({ title, events }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const TOP = 640;
  const BOTTOM = 1440;
  const step = (BOTTOM - TOP) / Math.max(1, events.length - 1);
  const shown = events.filter((e) => t >= e.at).length;
  const lineTo = interpolate(t, [events[0]?.at ?? 0, events[events.length - 1]?.at ?? 1], [TOP, BOTTOM], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const X = 230;

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 40% 45%, #2b2620, #0d0c0a 75%)" }}>
      <svg width={1080} height={1920}>
        {title && (
          <text x={540} y={540} textAnchor="middle" fontFamily={fonts.title} fontWeight={900} fontSize={50} letterSpacing={2} fill={accent.amber} textLength={title.length > 22 ? 960 : undefined} lengthAdjust="spacingAndGlyphs">
            {title}
          </text>
        )}
        <line x1={X} y1={TOP} x2={X} y2={BOTTOM} stroke="#f5f2eb" strokeOpacity={0.15} strokeWidth={6} />
        <line x1={X} y1={TOP} x2={X} y2={shown ? lineTo : TOP} stroke={accent.red} strokeWidth={8} />
        {events.map((e, i) => {
          const local = t - e.at;
          if (local < 0) return null;
          const pop = spring({ frame: local * fps, fps, config: { damping: 11, stiffness: 190, mass: 0.6 } });
          const y = TOP + i * step;
          const c = accent[e.color ?? "cream"];
          return (
            <g key={i} opacity={Math.min(1, pop * 1.2)} transform={`translate(${(1 - pop) * 60}, 0)`}>
              <circle cx={X} cy={y} r={30 * pop} fill={c} />
              <circle cx={X} cy={y} r={30 + ((local % 1.2) / 1.2) * 40} fill="none" stroke={c} strokeWidth={4} opacity={1 - (local % 1.2) / 1.2} />
              <text x={X + 70} y={y - 6} fontFamily={fonts.title} fontWeight={900} fontSize={58} fill={c}>
                {e.date}
              </text>
              <text x={X + 70} y={y + 50} fontFamily={fonts.body} fontWeight={700} fontSize={38} fill="#f5f2eb">
                {e.label}
              </text>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
