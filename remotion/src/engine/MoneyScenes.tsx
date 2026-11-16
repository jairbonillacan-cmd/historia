import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { accent, archivalFilter, fonts } from "./theme";
import type { NotePart, Visual } from "./types";

// Billete blanco del Banco de Inglaterra (1930-1956) dibujado en SVG: grande, legible y sin depender de fotos.
// Modos: `inspect` (sobre la mesa, con las marcas de cada secreto), `backlight` (al trasluz: aparece la marca
// de agua y el agujero de alfiler), `rain` (lluvia de billetes) y `press` (la imprenta apila billetes).

const NOTE_W = 900;
const NOTE_H = 560;
const SCRIPT = "'Palatino Linotype', 'Book Antiqua', Georgia, serif";
const INK = "#1b1a17";

// Posición de cada parte dentro del billete (coordenadas del billete, origen arriba a la izquierda).
const PARTS: Record<NotePart, [number, number]> = {
  vignette: [110, 120],
  watermark: [150, 430],
  pinhole: [860, 42],
  serial: [300, 160],
  paper: [620, 470],
  signature: [740, 505],
};

type Props = Extract<Visual, { kind: "banknote" }> & { folder: string };

const Note: React.FC<{ value: string; serial: string; date: string; backlight?: number; pinhole?: number; aged?: number }> = ({
  value,
  serial,
  date,
  backlight = 0,
  pinhole = 0,
  aged = 0,
}) => (
  <g>
    <rect width={NOTE_W} height={NOTE_H} fill={`rgb(${246 - aged * 18},${243 - aged * 22},${232 - aged * 30})`} />
    {/* fibras del papel de lino */}
    {Array.from({ length: 60 }, (_, i) => (
      <line
        key={i}
        x1={random(`fx-${i}`) * NOTE_W}
        y1={random(`fy-${i}`) * NOTE_H}
        x2={random(`fx-${i}`) * NOTE_W + 14}
        y2={random(`fy-${i}`) * NOTE_H + 4}
        stroke="#b9ae98"
        strokeOpacity={0.35 + aged * 0.3}
        strokeWidth={1}
      />
    ))}
    {/* marca de agua: ondas y la figura, visibles solo al trasluz */}
    <g opacity={backlight * 0.55}>
      <ellipse cx={150} cy={420} rx={95} ry={110} fill="none" stroke="#6d6450" strokeWidth={10} strokeOpacity={0.5} />
      <path d="M110,470 Q150,360 190,470 Z" fill="#6d6450" fillOpacity={0.45} />
      <circle cx={150} cy={355} r={22} fill="#6d6450" fillOpacity={0.45} />
      {Array.from({ length: 9 }, (_, i) => (
        <path key={i} d={`M260,${300 + i * 26} q60,-14 120,0 t120,0 t120,0 t120,0`} fill="none" stroke="#6d6450" strokeWidth={3} strokeOpacity={0.35} />
      ))}
    </g>
    {/* viñeta de Britannia */}
    <g transform="translate(110,120)">
      <circle r={78} fill="none" stroke={INK} strokeWidth={3} />
      <circle r={66} fill="none" stroke={INK} strokeWidth={1.5} />
      {Array.from({ length: 22 }, (_, i) => (
        <line key={i} x1={-60} y1={-56 + i * 5.3} x2={60} y2={-56 + i * 5.3} stroke={INK} strokeOpacity={0.35} strokeWidth={1.2} />
      ))}
      <path d="M-22,52 Q-30,0 -6,-18 L6,-18 Q30,0 22,52 Z" fill={INK} fillOpacity={0.8} />
      <circle cx={0} cy={-30} r={12} fill={INK} fillOpacity={0.85} />
      <line x1={26} y1={-58} x2={20} y2={52} stroke={INK} strokeWidth={3} />
    </g>
    <text x={540} y={92} textAnchor="middle" fontFamily={SCRIPT} fontStyle="italic" fontWeight={700} fontSize={66} fill={INK}>
      Bank of England
    </text>
    <text x={300} y={168} fontFamily={SCRIPT} fontStyle="italic" fontSize={30} fill={INK}>
      {serial}
    </text>
    <text x={560} y={168} fontFamily={SCRIPT} fontStyle="italic" fontSize={36} fill={INK}>
      to pay the Bearer on Demand
    </text>
    <text x={540} y={238} textAnchor="middle" fontFamily={SCRIPT} fontStyle="italic" fontSize={46} fill={INK}>
      the Sum of {value} Pounds
    </text>
    <text x={540} y={300} textAnchor="middle" fontFamily={SCRIPT} fontStyle="italic" fontSize={32} fill={INK}>
      {date}
    </text>
    <text x={560} y={380} fontFamily={SCRIPT} fontStyle="italic" fontSize={30} fill={INK}>
      For the Gov. and Comp. of the
    </text>
    <text x={600} y={420} fontFamily={SCRIPT} fontStyle="italic" fontSize={30} fill={INK}>
      Bank of England.
    </text>
    <text x={70} y={500} fontFamily={SCRIPT} fontStyle="italic" fontWeight={700} fontSize={72} fill={INK}>
      {value}
    </text>
    <path d="M660,505 q20,-30 40,-4 t40,-6 t50,4 t40,-10" fill="none" stroke={INK} strokeWidth={2.5} />
    <text x={720} y={538} fontFamily={SCRIPT} fontStyle="italic" fontSize={20} fill={INK}>
      Chief Cashier.
    </text>
    {/* agujero de alfiler: un punto oscuro que al trasluz deja pasar la luz */}
    {pinhole > 0 && (
      <g transform={`translate(${PARTS.pinhole[0]},${PARTS.pinhole[1]})`}>
        <circle r={4} fill={backlight > 0.3 ? "#fffbe6" : "#3a352c"} />
        {backlight > 0.3 && <circle r={18 * backlight} fill="#fff6c8" opacity={0.5 * pinhole} />}
      </g>
    )}
    <rect width={NOTE_W} height={NOTE_H} fill="none" stroke="#cfc6b2" strokeWidth={2} />
  </g>
);

export const BanknoteScene: React.FC<Props> = ({ folder, mode, value = "Fifty", serial = "A/N 49486", date = "London 20 June 1936", marks = [], background }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const p = frame / durationInFrames;

  const bg = background ? (
    <Img
      src={staticFile(`${folder}/${background}`)}
      style={{ position: "absolute", inset: -40, width: "calc(100% + 80px)", height: "calc(100% + 80px)", objectFit: "cover", filter: `${archivalFilter} blur(10px) brightness(0.45)` }}
    />
  ) : null;

  if (mode === "rain") {
    return (
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 40%, #3a3328, #120f0b 75%)", overflow: "hidden" }}>
        {bg}
        <svg width={1080} height={1920}>
          {Array.from({ length: 34 }, (_, i) => {
            const depth = 0.35 + random(`d-${i}`) * 0.65;
            const fall = (random(`y-${i}`) * 2400 + t * (260 + 320 * depth)) % 2400;
            const x = random(`x-${i}`) * 1180 - 50 + Math.sin(t * (1 + random(`w-${i}`) * 2) + i) * 60;
            const rot = random(`r-${i}`) * 360 + t * (40 + random(`rs-${i}`) * 90) * (i % 2 ? 1 : -1);
            const flip = Math.cos(t * (2 + random(`f-${i}`) * 3) + i);
            const s = 0.22 * depth;
            return (
              <g key={i} transform={`translate(${x},${fall - 300}) rotate(${rot}) scale(${s}, ${s * (0.35 + 0.65 * Math.abs(flip))}) translate(${-NOTE_W / 2},${-NOTE_H / 2})`} opacity={0.5 + depth * 0.5}>
                <Note value={value} serial={serial} date={date} />
              </g>
            );
          })}
        </svg>
        <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.55), transparent 30%, transparent 70%, rgba(0,0,0,0.6))" }} />
      </AbsoluteFill>
    );
  }

  if (mode === "press") {
    // Cada golpe de la platina suma un billete a la pila.
    const period = 0.42;
    const k = Math.floor(t / period);
    const local = (t % period) / period;
    const plate = local < 0.25 ? interpolate(local, [0, 0.25], [0, 1]) : interpolate(local, [0.25, 1], [1, 0], { easing: Easing.out(Easing.cubic) });
    return (
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 55%, #2b261e, #0c0a08 75%)" }}>
        {bg}
        <svg width={1080} height={1920}>
          {/* pila de billetes que crece */}
          {Array.from({ length: Math.min(k, 40) }, (_, i) => (
            <g key={i} transform={`translate(${90 + (random(`px-${i}`) - 0.5) * 16},${1360 - i * 9}) scale(1, 0.32)`}>
              <Note value={value} serial={serial} date={date} />
            </g>
          ))}
          {/* billete que sale de la prensa */}
          <g transform={`translate(90,${1000 - Math.min(k, 40) * 9}) scale(1, ${0.32 + (1 - local) * 0.4})`} opacity={1 - local * 0.4}>
            <Note value={value} serial={serial} date={date} />
          </g>
          {/* platina de la imprenta */}
          <rect x={60} y={560 + plate * 180} width={960} height={200} fill="#3b3a36" stroke="#6b665c" strokeWidth={4} />
          <rect x={60} y={540 + plate * 180} width={960} height={24} fill="#57534a" />
          {[220, 540, 860].map((x) => (
            <rect key={x} x={x - 14} y={300} width={28} height={260 + plate * 180} fill="#2a2925" />
          ))}
        </svg>
      </AbsoluteFill>
    );
  }

  // inspect / backlight
  const backlight = mode === "backlight" ? interpolate(t, [0.2, 1.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const enter = spring({ frame, fps, config: { damping: 16, stiffness: 90 } });
  const zoom = interpolate(p, [0, 1], [1.0, 1.1]);
  const CX = 540;
  const CY = 1010;
  const S = 1.08 * zoom;
  const tilt = -4 + (1 - enter) * -10;
  const pin = marks.some((m) => m.part === "pinhole" && t >= m.at) ? 1 : 0;
  const toScreen = ([px, py]: [number, number]) => {
    const a = (tilt * Math.PI) / 180;
    const x = (px - NOTE_W / 2) * S;
    const y = (py - NOTE_H / 2) * S;
    return [CX + x * Math.cos(a) - y * Math.sin(a), CY + x * Math.sin(a) + y * Math.cos(a)];
  };

  return (
    <AbsoluteFill style={{ background: mode === "backlight" ? `radial-gradient(circle at 50% 52%, rgba(255,240,200,${0.35 + backlight * 0.65}), #1a150e 60%)` : "radial-gradient(ellipse at 50% 45%, #4a3f30, #15110c 75%)" }}>
      {bg}
      <svg width={1080} height={1920}>
        <g transform={`translate(${CX},${CY + (1 - enter) * 200}) rotate(${tilt}) scale(${S}) translate(${-NOTE_W / 2},${-NOTE_H / 2})`} opacity={enter}>
          <rect x={10} y={16} width={NOTE_W} height={NOTE_H} fill="#000" opacity={0.45 * (1 - backlight)} filter="blur(8px)" />
          <g opacity={1 - backlight * 0.25}>
            <Note value={value} serial={serial} date={date} backlight={backlight} pinhole={pin || (mode === "backlight" ? 1 : 0)} />
          </g>
        </g>
        {marks.map((m, i) => {
          const local = t - m.at;
          if (local < 0) return null;
          const [x, y] = toScreen(PARTS[m.part]);
          const c = accent[m.color ?? "amber"];
          const pop = spring({ frame: local * fps, fps, config: { damping: 10, stiffness: 200, mass: 0.5 } });
          const pulse = local % 1;
          const up = m.side ? m.side === "up" : y < CY;
          const ly = up ? 700 - (i % 2) * 70 : 1390 + (i % 2) * 70;
          const lx = Math.min(1020, Math.max(60, x));
          return (
            <g key={i}>
              <circle cx={x} cy={y} r={24 + pulse * 46} fill="none" stroke={c} strokeWidth={4} opacity={1 - pulse} />
              <circle cx={x} cy={y} r={20 * pop} fill={c} fillOpacity={0.3} stroke={c} strokeWidth={4} />
              <line x1={x} y1={y} x2={lx} y2={ly + (up ? 14 : -48)} stroke={c} strokeWidth={3} opacity={pop} />
              <text
                x={Math.min(1020, Math.max(60, lx))}
                y={ly}
                textAnchor={lx > 760 ? "end" : lx < 320 ? "start" : "middle"}
                fontFamily={fonts.title}
                fontWeight={900}
                fontSize={42}
                fill="#fff"
                stroke="#000"
                strokeWidth={7}
                paintOrder="stroke"
                opacity={pop}
              >
                {m.label}
              </text>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
