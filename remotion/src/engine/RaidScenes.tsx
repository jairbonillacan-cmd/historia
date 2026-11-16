import React from "react";
import { AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { accent, fonts } from "./theme";
import type { DestroyerPart, Visual } from "./types";

const BLUEPRINT = "#0c1c2e";
const LINE = "#7FB8E6";

// ───────────── destructor de cubierta corrida (clase Town, ex-estadounidense), proa a la derecha ─────────────
// Línea de flotación en y=0, mide ~860 de largo. Cuatro chimeneas finas; en el Campbeltown se quitaron dos
// y las otras se cortaron en ángulo para que pareciera un torpedero alemán.

const FUNNELS = [-150, -60, 30, 120];
const KEPT = [1, 2]; // las que quedan después de la reforma
export const DESTROYER_PARTS: Record<DestroyerPart, [number, number]> = {
  bow: [395, -40],
  charge: [300, -22],
  bridge: [215, -105],
  funnels: [-15, -135],
  flag: [-300, -205],
  stern: [-400, -24],
  gate: [440, -60],
};

const Destroyer: React.FC<{ fill: string; stroke?: string; strokeWidth?: number; cut?: number; flag?: boolean }> = ({ fill, stroke = "none", strokeWidth = 0, cut = 0, flag }) => (
  <g fill={fill} stroke={stroke} strokeWidth={strokeWidth} strokeLinejoin="round">
    {/* casco: proa alta y afilada a la derecha, popa redondeada */}
    <path d="M-430,-30 L-420,-46 L330,-58 L440,-74 L410,0 L-400,0 Q-428,-8 -430,-30 Z" />
    {/* superestructura y puente */}
    <path d="M170,-58 L170,-96 L250,-96 L262,-58 Z" />
    <rect x={190} y={-124} width={52} height={28} />
    {/* cañones */}
    <rect x={300} y={-74} width={26} height={16} />
    <rect x={-360} y={-62} width={26} height={16} />
    {/* chimeneas: las quitadas se desvanecen, las que quedan se recortan en ángulo */}
    {FUNNELS.map((x, i) => {
      const kept = KEPT.includes(i);
      const top = kept ? -150 + 22 * cut : -150;
      const slant = kept ? 26 * cut : 0;
      return (
        <path
          key={i}
          d={`M${x - 14},-58 L${x - 14},${top + slant} L${x + 14},${top} L${x + 14},-58 Z`}
          opacity={kept ? 1 : 1 - cut}
          strokeDasharray={!kept && cut > 0 ? "8 8" : undefined}
        />
      );
    })}
    {/* mástiles */}
    <line x1={180} y1={-124} x2={180} y2={-230} stroke={stroke === "none" ? fill : stroke} strokeWidth={6} />
    <line x1={-300} y1={-46} x2={-300} y2={-200} stroke={stroke === "none" ? fill : stroke} strokeWidth={5} />
    {/* bandera de popa: lisa, sin símbolos */}
    {flag && <path d="M-300,-200 L-236,-194 L-242,-178 L-236,-162 L-300,-166 Z" fill={accent.red} stroke="none" />}
  </g>
);

// ───────────── plano técnico del destructor con marcas ─────────────

export const DestroyerScene: React.FC<Extract<Visual, { kind: "destroyer" }>> = ({ title, marks, cutAt, chargeAt, flagAt }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const draw = interpolate(frame, [0, 0.8 * fps], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const zoom = interpolate(frame, [0, durationInFrames], [1.0, 1.08]);
  const S = 1.12 * zoom;
  const CX = 520;
  const CY = 1080;
  const cut = cutAt === undefined ? 0 : interpolate(t, [cutAt, cutAt + 0.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const charge = chargeAt === undefined ? 0 : interpolate(t, [chargeAt, chargeAt + 0.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const glow = 0.6 + 0.4 * Math.sin(t * 8);

  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 55%, #12304d, ${BLUEPRINT} 70%)` }}>
      <svg width={1080} height={1920}>
        <defs>
          <pattern id="dd-grid" width={40} height={40} patternUnits="userSpaceOnUse">
            <path d="M40,0 L0,0 0,40" fill="none" stroke={LINE} strokeOpacity={0.12} strokeWidth={1} />
          </pattern>
        </defs>
        <rect width={1080} height={1920} fill="url(#dd-grid)" />
        <line x1={0} y1={CY} x2={1080} y2={CY} stroke={LINE} strokeOpacity={0.35} strokeDasharray="14 10" strokeWidth={2} />
        <g transform={`translate(${CX}, ${CY}) scale(${S})`} opacity={draw}>
          <Destroyer fill="rgba(127,184,230,0.08)" stroke={LINE} strokeWidth={1.8} cut={cut} />
          {flagAt !== undefined && t >= flagAt && (
            <path d="M-300,-200 L-236,-194 L-242,-178 L-236,-162 L-300,-166 Z" fill={accent.red} opacity={interpolate(t - flagAt, [0, 0.3], [0, 0.9], { extrapolateRight: "clamp" })} />
          )}
          {charge > 0 && (
            <g opacity={charge}>
              <rect x={262} y={-50} width={84} height={44} fill={accent.red} fillOpacity={0.25 + 0.35 * glow} stroke={accent.red} strokeWidth={3} />
              {[0, 1, 2, 3].map((k) => (
                <rect key={k} x={268 + k * 19} y={-44} width={14} height={32} fill={accent.amber} opacity={0.85} />
              ))}
            </g>
          )}
        </g>
        {marks.map((m, i) => {
          const local = t - m.at;
          if (local < 0) return null;
          const [px, py] = DESTROYER_PARTS[m.part];
          const x = CX + px * S;
          const y = CY + py * S;
          const c = accent[m.color ?? "red"];
          const pop = spring({ frame: local * fps, fps, config: { damping: 10, stiffness: 200, mass: 0.5 } });
          const pulse = local % 1;
          const right = m.side ? m.side === "right" : px >= 0;
          const lx = right ? 1030 : 50;
          const ly = y - 170 - (i % 3) * 110;
          return (
            <g key={i}>
              <circle cx={x} cy={y} r={30 + pulse * 50} fill="none" stroke={c} strokeWidth={4} opacity={1 - pulse} />
              <circle cx={x} cy={y} r={22 * pop} fill={c} fillOpacity={0.35} stroke={c} strokeWidth={4} />
              <polyline points={`${x},${y} ${x},${ly} ${lx},${ly}`} fill="none" stroke={c} strokeWidth={3} opacity={pop} />
              <text x={lx} y={ly - 14} textAnchor={right ? "end" : "start"} fontFamily={fonts.title} fontWeight={900} fontSize={40} fill="#fff" stroke="#000" strokeWidth={6} paintOrder="stroke" opacity={pop}>
                {m.label}
              </text>
            </g>
          );
        })}
      </svg>
      <div style={{ position: "absolute", top: 560, left: 56, right: 56, fontFamily: fonts.mono, fontWeight: 700, fontSize: 32, letterSpacing: 4, color: LINE, opacity: draw }}>{title}</div>
    </AbsoluteFill>
  );
};

// ───────────── el ataque de noche: río, reflectores, embestida y explosión ─────────────

const HORIZON = 1180;
const GATE_X = 930;

export const RaidScene: React.FC<Extract<Visual, { kind: "raid" }>> = ({ stage, hitAt = 1.2, blastAt = 0.4 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const p = frame / durationInFrames;
  const lit = stage !== "river";
  const day = stage === "blast";

  // Posición de la proa del destructor.
  let bowX = 520;
  let tilt = 0;
  let shake = 0;
  if (stage === "river") bowX = 560 + 200 * p;
  else if (stage === "lights") bowX = 520 + 140 * p;
  else if (stage === "ram") {
    const k = interpolate(t, [0, hitAt], [0, 1], { extrapolateRight: "clamp", easing: Easing.in(Easing.quad) });
    bowX = 640 + (GATE_X + 10 - 640) * k;
    const after = t - hitAt;
    if (after > 0) {
      tilt = -3.2 * Math.min(1, after / 0.25);
      shake = after < 0.5 ? Math.sin(after * 90) * 14 * (1 - after / 0.5) : 0;
    }
  } else bowX = GATE_X + 10;
  if (stage === "blast") tilt = -3.2;
  const S = 1.0;
  const shipX = bowX - 440 * S;

  const boom = stage === "blast" ? t - blastAt : -1;
  const sky = day ? "linear-gradient(180deg, #4a4f55, #6c7075 60%, #3a3e42)" : "linear-gradient(180deg, #03060c, #0a1220 60%, #0d1726)";

  return (
    <AbsoluteFill style={{ background: sky, transform: `translate(${shake}px, ${shake * 0.4}px)` }}>
      <svg width={1080} height={1920}>
        <defs>
          <linearGradient id="beam" x1="0" y1="1" x2="0" y2="0">
            <stop offset="0" stopColor="#fffbe8" stopOpacity={0.55} />
            <stop offset="1" stopColor="#fffbe8" stopOpacity={0} />
          </linearGradient>
          <radialGradient id="fireball">
            <stop offset="0" stopColor="#fff6d8" />
            <stop offset="0.35" stopColor="#ffb347" />
            <stop offset="0.7" stopColor="#c2410c" stopOpacity={0.8} />
            <stop offset="1" stopColor="#1a1a1a" stopOpacity={0} />
          </radialGradient>
          <filter id="raid-blur" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation={8} />
          </filter>
        </defs>

        {/* reflectores alemanes desde la orilla */}
        {lit &&
          [0, 1, 2].map((k) => {
            const ox = 640 + k * 150;
            const ang = -90 + Math.sin(t * (0.8 + k * 0.3) + k * 2) * 28 + (stage === "lights" ? interpolate(t, [0, 1.2], [30, 0], { extrapolateRight: "clamp" }) * (k - 1) : 0);
            const on = stage === "lights" ? interpolate(t, [k * 0.18, k * 0.18 + 0.1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : day ? 0 : 1;
            return (
              <g key={k} transform={`translate(${ox}, ${HORIZON - 30}) rotate(${ang + 90})`} opacity={on}>
                <path d="M0,0 L-70,-1500 L70,-1500 Z" fill="url(#beam)" />
              </g>
            );
          })}

        {/* orilla: búnkeres, grúas del puerto y la compuerta del dique */}
        <path d={`M560,${HORIZON} L560,${HORIZON - 40} L640,${HORIZON - 40} L660,${HORIZON - 70} L760,${HORIZON - 70} L780,${HORIZON - 40} L1080,${HORIZON - 40} L1080,${HORIZON + 30} L560,${HORIZON + 30} Z`} fill={day ? "#2b2e31" : "#05080d"} />
        {[700, 860].map((x, i) => (
          <g key={i} stroke={day ? "#2b2e31" : "#0a0f16"} strokeWidth={6} fill="none">
            <line x1={x} y1={HORIZON - 40} x2={x} y2={HORIZON - 300} />
            <line x1={x + 40} y1={HORIZON - 40} x2={x + 40} y2={HORIZON - 300} />
            <line x1={x - 60} y1={HORIZON - 300} x2={x + 140} y2={HORIZON - 300} />
            <line x1={x} y1={HORIZON - 120} x2={x + 40} y2={HORIZON - 200} />
          </g>
        ))}
        <rect x={GATE_X + 10} y={HORIZON - 70} width={150} height={190} fill={day ? "#3a3d40" : "#111821"} stroke={day ? "#55595d" : "#26313d"} strokeWidth={3} />

        {/* agua */}
        <rect x={0} y={HORIZON + 30} width={1080} height={1920 - HORIZON - 30} fill={day ? "#2c3338" : "#060b12"} />
        {Array.from({ length: 36 }, (_, i) => {
          const y = HORIZON + 50 + random(`ry-${i}`) * 700;
          const x = ((random(`rx-${i}`) * 1300 - t * 30) % 1300) + (random(`rx-${i}`) > 0.5 ? 0 : 1300);
          return <rect key={i} x={(x % 1300) - 100} y={y} width={40 + random(`rw-${i}`) * 120} height={3} fill={lit ? "rgba(255,250,230,0.16)" : "rgba(160,190,220,0.08)"} />;
        })}

        {/* lanchas ardiendo en el río */}
        {(stage === "river" || stage === "lights") &&
          [0, 1, 2, 3].map((k) => {
            const x = 110 + k * 250 + (stage === "river" ? 60 * p : 0);
            const y = HORIZON + 170 + (k % 2) * 160;
            const burn = stage === "river" ? interpolate(t, [0.5 + k * 0.5, 0.9 + k * 0.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 1;
            const fl = 0.7 + 0.3 * Math.sin(t * 13 + k * 3);
            return (
              <g key={k}>
                <path d={`M${x - 80},${y} L${x + 90},${y} L${x + 72},${y + 26} L${x - 70},${y + 26} Z`} fill="#0b0b0b" />
                {burn > 0 && (
                  <>
                    <ellipse cx={x} cy={y - 50 * burn} rx={80 * burn} ry={110 * burn * fl} fill="url(#fireball)" opacity={0.95} />
                    <ellipse cx={x} cy={y + 40} rx={70 * burn} ry={14} fill="#ff9a3c" opacity={0.25 * fl} />
                  </>
                )}
              </g>
            );
          })}

        {/* trazadoras hacia el destructor */}
        {(stage === "lights" || stage === "ram") &&
          Array.from({ length: 9 }, (_, i) => {
            const period = 14;
            const k = Math.floor((frame + i * 5) / period);
            const local = ((frame + i * 5) % period) / period;
            const x1 = 620 + random(`tx-${i}-${k}`) * 420;
            const y1 = HORIZON - 60 - random(`ty-${i}-${k}`) * 80;
            const x2 = shipX + random(`sx-${i}-${k}`) * 440 * S;
            const y2 = HORIZON + 20 - random(`sy-${i}-${k}`) * 120;
            const hx = x1 + (x2 - x1) * local;
            const hy = y1 + (y2 - y1) * local;
            const tx = x1 + (x2 - x1) * Math.max(0, local - 0.3);
            const ty = y1 + (y2 - y1) * Math.max(0, local - 0.3);
            return <line key={i} x1={tx} y1={ty} x2={hx} y2={hy} stroke={i % 3 ? accent.amber : accent.red} strokeWidth={5} strokeLinecap="round" />;
          })}

        {/* el destructor */}
        {boom < 0.15 && (
          <g transform={`translate(${shipX + 440 * S}, ${HORIZON + 26}) rotate(${tilt}) translate(${-440 * S}, 0) scale(${S})`}>
            <Destroyer fill={day ? "#26292c" : "#0d1117"} stroke={day ? "none" : lit ? "rgba(255,250,230,0.55)" : "rgba(170,200,235,0.45)"} strokeWidth={2.5} cut={1} flag={stage === "river"} />
            {(stage === "lights" || stage === "ram") && (
              <ellipse cx={-60} cy={-80} rx={60} ry={50 + Math.sin(t * 11) * 8} fill="url(#fireball)" opacity={0.8} />
            )}
          </g>
        )}
        {/* ola de proa al avanzar */}
        {stage !== "blast" && boom < 0 && (
          <path d={`M${bowX - 10},${HORIZON + 26} Q${bowX - 80},${HORIZON + 46} ${bowX - 220},${HORIZON + 40}`} stroke="rgba(230,235,240,0.5)" strokeWidth={6} fill="none" />
        )}
        {/* chispas del choque */}
        {stage === "ram" &&
          t > hitAt &&
          Array.from({ length: 22 }, (_, i) => {
            const a = t - hitAt;
            const ang = -Math.PI / 2 + (random(`sp-${i}`) - 0.5) * 2.4;
            const v = 300 + random(`sv-${i}`) * 500;
            const x = GATE_X + Math.cos(ang) * v * a;
            const y = HORIZON - 20 + Math.sin(ang) * v * a + 600 * a * a;
            return <circle key={i} cx={x} cy={y} r={4} fill={accent.amber} opacity={Math.max(0, 1 - a / 0.9)} />;
          })}

        {/* la explosión */}
        {boom >= 0 && (
          <g>
            <circle cx={GATE_X - 120} cy={HORIZON - 40} r={interpolate(boom, [0, 0.5, 3], [40, 520, 700], { extrapolateRight: "clamp" })} fill="url(#fireball)" opacity={interpolate(boom, [0, 2.5, 4], [1, 0.8, 0.3], { extrapolateRight: "clamp" })} />
            {Array.from({ length: 10 }, (_, i) => {
              const r = 120 + i * 30 + boom * 120;
              return (
                <circle key={i} cx={GATE_X - 140 + (random(`sm-${i}`) - 0.5) * 300} cy={HORIZON - 260 - boom * 140 - i * 30} r={r} fill="#1c1c1c" opacity={interpolate(boom, [0.3, 1.2], [0, 0.55], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })} filter="url(#raid-blur)" />
              );
            })}
            {Array.from({ length: 26 }, (_, i) => {
              const ang = -Math.PI / 2 + (random(`db-${i}`) - 0.5) * 2.8;
              const v = 600 + random(`dv-${i}`) * 900;
              const x = GATE_X - 120 + Math.cos(ang) * v * boom;
              const y = HORIZON - 40 + Math.sin(ang) * v * boom + 500 * boom * boom;
              return <rect key={i} x={x} y={y} width={10 + random(`dw-${i}`) * 18} height={6} fill="#120c08" transform={`rotate(${boom * 400 * (i % 2 ? 1 : -1)}, ${x}, ${y})`} />;
            })}
          </g>
        )}
      </svg>
      {boom >= 0 && boom < 0.5 && <AbsoluteFill style={{ background: "#fff8ea", opacity: interpolate(boom, [0, 0.05, 0.5], [0, 1, 0]) }} />}
    </AbsoluteFill>
  );
};
