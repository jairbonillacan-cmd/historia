import React from "react";
import { AbsoluteFill, Easing, interpolate, random, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { accent, fonts } from "./theme";
import type { Visual } from "./types";

// Ataque aéreo rasante sobre una ciudad (Operación Cartago, Copenhague 1945).
// `skyline`: tejados de perfil con agujas de iglesia y un poste de luz; los Mosquito pasan al ras.
// `shellhus`: corte del edificio con ficheros abajo y celdas arriba; las bombas entran por los pisos bajos.

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const GROUND = 1440;
const SILHOUETTE = "#17181b";

// Mosquito de perfil, morro a la derecha, ~200 px de largo a escala 1.
const Mosquito: React.FC<{ x: number; y: number; rot?: number; scale?: number; fill?: string; t: number }> = ({ x, y, rot = 0, scale = 1, fill = "#0e0f11", t }) => (
  <g transform={`translate(${x}, ${y}) rotate(${rot}) scale(${scale})`}>
    <path d="M-100,-4 L-92,-30 L-80,-30 L-70,-8 L40,-10 Q78,-12 96,-2 Q78,8 40,8 L-90,6 Z" fill={fill} />
    {/* góndola del motor y ala */}
    <path d="M-6,0 L36,-2 Q54,0 56,4 Q40,10 -6,8 Z" fill={fill} />
    <path d="M-20,2 L30,2 L44,12 L-30,12 Z" fill={fill} opacity={0.85} />
    {/* cabina */}
    <path d="M44,-10 Q56,-22 72,-8 Z" fill="#5d6b78" opacity={0.7} />
    {/* hélice girando */}
    <ellipse cx={58} cy={3} rx={3} ry={14 + Math.sin(t * 60) * 4} fill="#cfd4d8" opacity={0.35} />
    {/* estabilizador horizontal */}
    <path d="M-98,-6 L-70,-6 L-74,0 L-100,0 Z" fill={fill} />
  </g>
);

// Columna de humo que sube desde (x, y). `age` en segundos desde que empezó.
const Smoke: React.FC<{ x: number; y: number; age: number; seed: string; size?: number; fire?: boolean }> = ({ x, y, age, seed, size = 1, fire }) => {
  if (age < 0) return null;
  const puffs = Array.from({ length: 48 }, (_, i) => i);
  return (
    <g filter="url(#smoke-blur)">
      {fire &&
        [0, 1, 2].map((k) => (
          <ellipse key={k} cx={x + (k - 1) * 30 * size} cy={y - 10} rx={(46 - k * 8) * size * (0.8 + 0.2 * Math.sin(age * 9 + k))} ry={34 * size} fill={k ? accent.amber : accent.red} opacity={0.55} />
        ))}
      {puffs.map((i) => {
        // Emisión continua: cada bocanada nace, sube 4 s y vuelve a salir de la base.
        const born = i * 0.12;
        if (age < born) return null;
        const life = (age - born) % 4.2;
        const rise = Math.min(1, life / 4);
        const r = (40 + 120 * rise) * size * (0.7 + 0.6 * random(`${seed}r${i}`));
        const dx = (random(`${seed}x${i}`) - 0.5) * 110 * size - rise * 90 * size;
        const py = y - rise * 620 * size;
        return <circle key={i} cx={x + dx} cy={py} r={r} fill={i % 3 ? "#121214" : "#2a2a2c"} opacity={0.6 * (1 - rise * 0.6) * Math.min(1, life * 3)} />;
      })}
    </g>
  );
};

type Building = { x: number; w: number; h: number; spire?: boolean };
const buildings = (seed: string, count: number, from: number, to: number): Building[] =>
  Array.from({ length: count }, (_, i) => {
    const w = 90 + random(`${seed}w${i}`) * 110;
    return { x: from + ((to - from) * i) / count, w, h: 140 + random(`${seed}h${i}`) * 200, spire: random(`${seed}s${i}`) > 0.82 };
  });

const Roofs: React.FC<{ list: Building[]; offset: number; color: string }> = ({ list, offset, color }) => (
  <g fill={color}>
    {list.map((b, i) => {
      const x = b.x - offset;
      return (
        <g key={i}>
          <rect x={x} y={GROUND - b.h} width={b.w} height={b.h} />
          <path d={`M${x - 6},${GROUND - b.h} L${x + b.w / 2},${GROUND - b.h - 50} L${x + b.w + 6},${GROUND - b.h} Z`} />
          {b.spire && <path d={`M${x + b.w / 2 - 22},${GROUND - b.h - 40} L${x + b.w / 2},${GROUND - b.h - 330} L${x + b.w / 2 + 22},${GROUND - b.h - 40} Z`} />}
        </g>
      );
    })}
  </g>
);

const Label: React.FC<{ x: number; y: number; text: string; color: string; opacity: number; anchor?: "start" | "middle" | "end" }> = ({ x, y, text, color, opacity, anchor = "middle" }) => (
  <text x={x} y={y} textAnchor={anchor} fontFamily={fonts.title} fontWeight={900} fontSize={44} fill={color} stroke="#000" strokeWidth={8} paintOrder="stroke" opacity={opacity}>
    {text}
  </text>
);

const POLE_X = 600;
const POLE_TOP = 1010;
const CRASH_X = 860;

export const SkylineScene: React.FC<Extract<Visual, { kind: "skyline" }>> = ({ stage, hitAt = 1.2, crashAt, confuseAt = 1.5 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const dur = durationInFrames / fps;
  const sea = stage === "sea";

  const far = buildings("far", 16, -200, 2400);
  const near = buildings("near", 12, -200, 2600);
  const scroll = stage === "spires" ? t * 260 : stage === "sea" ? 0 : t * 12;

  let planes: React.ReactNode = null;
  let extra: React.ReactNode = null;

  if (sea) {
    planes = [0, 1, 2].map((k) => (
      <Mosquito key={k} t={t} x={230 + k * 280 + Math.sin(t * 1.3 + k) * 14} y={1270 - k * 60 + Math.sin(t * 2 + k) * 6} scale={1.9 - k * 0.35} />
    ));
    extra = (
      <g>
        {Array.from({ length: 9 }, (_, i) => {
          const y = 1340 + i * 26;
          const shift = (t * (180 + i * 40)) % 160;
          return <path key={i} d={Array.from({ length: 10 }, (_, k) => `${k ? "L" : "M"}${k * 160 - shift},${y} Q${k * 160 - shift + 40},${y - 8} ${k * 160 - shift + 80},${y}`).join(" ")} stroke="#9aa6ad" strokeOpacity={0.25 + i * 0.04} strokeWidth={3} fill="none" />;
        })}
        {[0, 1, 2].map((k) => (
          <ellipse key={k} cx={200 + k * 230 + Math.sin(t * 9 + k) * 10} cy={1345} rx={70} ry={8} fill="#d6dde0" opacity={0.18} />
        ))}
      </g>
    );
  } else if (stage === "spires") {
    planes = [0, 1, 2].map((k) => (
      <Mosquito key={k} t={t} x={260 + k * 270 + Math.sin(t * 1.4 + k) * 10} y={1330 - k * 60 + Math.sin(t * 2.2 + k) * 6} scale={1.8 - k * 0.3} />
    ));
  } else if (stage === "pole") {
    // hitAt ≤ 0: el roce ya pasó (la escena arranca con el avión cayendo); hitAt > duración: solo la torre.
    const before = interpolate(t, [0, Math.max(0.01, hitAt)], [-180, POLE_X - 40], { ...clamp, easing: Easing.linear });
    const after = Math.max(0, t - hitAt);
    const fallEnd = Math.max(hitAt + 0.01, crashAt ?? dur);
    const k = interpolate(t, [hitAt, fallEnd], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
    const x = t < hitAt ? before : POLE_X - 40 + (CRASH_X - POLE_X) * k;
    const y = t < hitAt ? POLE_TOP + 10 : POLE_TOP + 10 + (GROUND - 90 - POLE_TOP) * k;
    const rot = t < hitAt ? 0 : 8 + 40 * k + Math.sin(after * 18) * 6 * (1 - k);
    const crashed = crashAt !== undefined && t >= crashAt;
    planes = (
      <g>
        {!crashed && <Mosquito t={t} x={x} y={y} rot={rot} scale={1.7} />}
        {/* el resto de la oleada sigue de largo, más alto */}
        <Mosquito t={t} x={interpolate(t, [0, dur], [-400, 900])} y={880} scale={0.9} />
      </g>
    );
    const spark = interpolate(t - hitAt, [0, 0.08, 0.5], [0, 1, 0], clamp);
    extra = (
      <g>
        {spark > 0 && (
          <g opacity={spark}>
            <circle cx={POLE_X} cy={POLE_TOP + 20} r={90 * spark} fill={accent.amber} opacity={0.5} />
            {Array.from({ length: 10 }, (_, i) => {
              const a = (i / 10) * Math.PI * 2;
              return <line key={i} x1={POLE_X} y1={POLE_TOP + 20} x2={POLE_X + Math.cos(a) * 140} y2={POLE_TOP + 20 + Math.sin(a) * 140} stroke="#fff3c4" strokeWidth={5} />;
            })}
          </g>
        )}
        {crashed && (
          <g>
            <circle cx={CRASH_X} cy={GROUND - 60} r={interpolate(t - crashAt!, [0, 0.4], [20, 220], clamp)} fill={accent.amber} opacity={interpolate(t - crashAt!, [0, 0.6], [0.9, 0], clamp)} />
            <Smoke x={CRASH_X} y={GROUND - 60} age={t - crashAt!} seed="crash" size={1.1} fire />
          </g>
        )}
      </g>
    );
  } else {
    // Humo de dos incendios: la segunda oleada confunde el colegio con el cuartel.
    const left = { x: 270, y: GROUND - 180 };
    const right = { x: 820, y: GROUND - 120 };
    const k = interpolate(t, [confuseAt, confuseAt + 0.9], [0, 1], clamp);
    const tx = left.x + (right.x - left.x) * k;
    const ty = left.y - 120 + (right.y - left.y) * k;
    const lab = interpolate(t, [0.3, 0.8], [0, 1], clamp);
    planes = [0, 1].map((i) => <Mosquito key={i} t={t} x={interpolate(t, [0, dur], [-160 + i * 160, 380 + i * 160])} y={760 + i * 70} scale={0.95} />);
    extra = (
      <g>
        <Smoke x={left.x} y={left.y} age={t + 6} seed="gestapo" size={0.9} fire />
        <Smoke x={right.x} y={right.y} age={t + 6} seed="colegio" size={1.15} fire />
        <Label x={left.x} y={left.y + 110} text="SHELLHUS" color={accent.cream} opacity={lab} />
        <Label x={right.x} y={right.y + 80} text="COLEGIO" color={accent.red} opacity={lab} />
        {/* mira que se desplaza hacia el humo equivocado */}
        <g transform={`translate(${tx}, ${ty})`} opacity={interpolate(t, [0.2, 0.6], [0, 1], clamp)}>
          <circle r={70} fill="none" stroke={accent.red} strokeWidth={5} />
          <line x1={-110} y1={0} x2={-40} y2={0} stroke={accent.red} strokeWidth={5} />
          <line x1={40} y1={0} x2={110} y2={0} stroke={accent.red} strokeWidth={5} />
          <line x1={0} y1={-110} x2={0} y2={-40} stroke={accent.red} strokeWidth={5} />
          <line x1={0} y1={40} x2={0} y2={110} stroke={accent.red} strokeWidth={5} />
        </g>
      </g>
    );
  }

  const poleBend = stage === "pole" ? interpolate(t - hitAt, [0, 0.15, 1.2], [0, 9, 4], clamp) : 0;

  return (
    <AbsoluteFill style={{ background: sea ? "linear-gradient(#3b3f43, #6f7275 62%, #2c3236 70%)" : "linear-gradient(#2e2f33, #77706a 70%, #3a3632)" }}>
      <svg width={1080} height={1920}>
        <defs>
          <filter id="smoke-blur" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation={16} />
          </filter>
        </defs>
        {!sea && (
          <>
            <Roofs list={far} offset={scroll * 0.4} color="#3d3b3a" />
            <Roofs list={near} offset={scroll} color={SILHOUETTE} />
            <rect x={0} y={GROUND} width={1080} height={480} fill="#121214" />
          </>
        )}
        {sea && <rect x={0} y={1330} width={1080} height={590} fill="#1d262c" />}
        {stage === "pole" && (
          <g transform={`rotate(${poleBend}, ${POLE_X}, ${GROUND})`} stroke="#0b0b0c" strokeWidth={6} fill="none">
            {/* torre de luz de celosía, 30 m */}
            <path d={`M${POLE_X - 28},${GROUND} L${POLE_X - 6},${POLE_TOP} L${POLE_X + 6},${POLE_TOP} L${POLE_X + 28},${GROUND}`} />
            {Array.from({ length: 9 }, (_, i) => {
              const y0 = GROUND - (i * (GROUND - POLE_TOP)) / 9;
              const y1 = GROUND - ((i + 1) * (GROUND - POLE_TOP)) / 9;
              const w0 = 28 - (22 * i) / 9;
              const w1 = 28 - (22 * (i + 1)) / 9;
              return <path key={i} d={`M${POLE_X - w0},${y0} L${POLE_X + w1},${y1} M${POLE_X + w0},${y0} L${POLE_X - w1},${y1}`} strokeWidth={3} />;
            })}
            <rect x={POLE_X - 30} y={POLE_TOP - 24} width={60} height={24} fill="#0b0b0c" />
            <circle cx={POLE_X} cy={POLE_TOP - 12} r={8} fill={accent.amber} stroke="none" />
          </g>
        )}
        {extra}
        {planes}
      </svg>
    </AbsoluteFill>
  );
};

// ───────────── corte del Shellhus ─────────────

const FLOORS = 6;
const B_LEFT = 230;
const B_RIGHT = 850;
const B_BOTTOM = 1400;
const FLOOR_H = 108;
const floorY = (f: number) => B_BOTTOM - f * FLOOR_H; // borde superior del piso f (1 = planta baja)

export const ShellhusScene: React.FC<Extract<Visual, { kind: "shellhus" }>> = ({ marks = [], hitAt, escapeAt, aroundAt }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const draw = interpolate(frame, [0, 0.6 * fps], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const zoom = interpolate(frame, [0, durationInFrames], [1, 1.06]);
  const top = floorY(FLOORS);
  const hit = hitAt === undefined ? 0 : interpolate(t, [hitAt, hitAt + 0.5], [0, 1], clamp);
  const burning = hitAt !== undefined && t >= hitAt + 0.3;
  const flick = 0.75 + 0.25 * Math.sin(t * 11);

  // 30 prisioneros en el último piso; 18 escapan por el techo roto.
  const prisoners = Array.from({ length: 30 }, (_, i) => i);
  const esc = escapeAt === undefined ? 0 : interpolate(t, [escapeAt, escapeAt + 2.4], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 55%, #2a2722, #0e0d0b 75%)" }}>
      <svg width={1080} height={1920} style={{ transform: `scale(${zoom})`, transformOrigin: "540px 1100px" }}>
        <g opacity={draw} stroke="#e9e2d0" strokeWidth={3} fill="none">
          {/* manzanas vecinas: casas, hospital, colegio */}
          {aroundAt !== undefined &&
            [
              { x: 40, w: 160, h: 260, label: "CASAS", at: 0 },
              { x: 880, w: 170, h: 330, label: "HOSPITAL", at: 0.6 },
            ].map((b, i) => {
              const o = interpolate(t - aroundAt - b.at, [0, 0.4], [0, 1], clamp);
              return (
                <g key={i} opacity={o}>
                  <rect x={b.x} y={B_BOTTOM - b.h} width={b.w} height={b.h} strokeOpacity={0.6} fill="rgba(233,226,208,0.05)" />
                  <text x={b.x + b.w / 2} y={B_BOTTOM - b.h - 20} textAnchor="middle" fontFamily={fonts.title} fontWeight={900} fontSize={30} fill={accent.amber} stroke="none">
                    {b.label}
                  </text>
                </g>
              );
            })}
          <rect x={B_LEFT} y={top} width={B_RIGHT - B_LEFT} height={B_BOTTOM - top} fill="rgba(233,226,208,0.06)" />
          {Array.from({ length: FLOORS - 1 }, (_, i) => (
            <line key={i} x1={B_LEFT} y1={floorY(i + 1)} x2={B_RIGHT} y2={floorY(i + 1)} strokeOpacity={0.5} />
          ))}
          {/* ficheros en los pisos 1 a 3 */}
          {[1, 2, 3].map((f) =>
            Array.from({ length: 7 }, (_, k) => (
              <g key={`${f}-${k}`}>
                <rect x={B_LEFT + 30 + k * 82} y={floorY(f) + 26} width={56} height={70} strokeOpacity={0.7} strokeWidth={2} />
                <line x1={B_LEFT + 30 + k * 82} y1={floorY(f) + 49} x2={B_LEFT + 86 + k * 82} y2={floorY(f) + 49} strokeWidth={2} strokeOpacity={0.6} />
                <line x1={B_LEFT + 30 + k * 82} y1={floorY(f) + 72} x2={B_LEFT + 86 + k * 82} y2={floorY(f) + 72} strokeWidth={2} strokeOpacity={0.6} />
              </g>
            )),
          )}
          {/* rejas del último piso */}
          {Array.from({ length: 20 }, (_, k) => (
            <line key={k} x1={B_LEFT + 20 + k * 30} y1={floorY(FLOORS) + 10} x2={B_LEFT + 20 + k * 30} y2={floorY(FLOORS - 1) - 6} strokeOpacity={0.35} strokeWidth={2} />
          ))}
          <line x1={B_LEFT - 30} y1={B_BOTTOM} x2={B_RIGHT + 200} y2={B_BOTTOM} strokeOpacity={0.6} />
        </g>
        {/* fuego en los pisos bajos */}
        {burning &&
          [1, 2, 3].map((f) => (
            <rect key={f} x={B_LEFT + 4} y={floorY(f) + 4} width={B_RIGHT - B_LEFT - 8} height={FLOOR_H - 8} fill={f === 2 ? accent.red : accent.amber} opacity={0.45 * flick * hit} />
          ))}
        {/* prisioneros */}
        {prisoners.map((i) => {
          const escaping = [0, 2, 4].includes(i % 5) && esc > 0; // 18 de 30
          const bx = B_LEFT + 30 + (i % 15) * 40;
          const by = floorY(FLOORS) + (i < 15 ? 48 : 88);
          const k = escaping ? Math.min(1, esc * 1.4 - (i % 6) * 0.06) : 0;
          const x = bx + Math.max(0, k) * (B_RIGHT + 140 - bx);
          const y = by - Math.sin(Math.max(0, k) * Math.PI) * 120;
          const c = escaping ? accent.blue : accent.cream;
          return (
            <g key={i} opacity={draw}>
              <circle cx={x} cy={y - 18} r={8} fill={c} />
              <rect x={x - 7} y={y - 9} width={14} height={22} rx={4} fill={c} />
            </g>
          );
        })}
        {/* bombas que entran rasantes por la fachada */}
        {hitAt !== undefined &&
          [1, 2, 3].map((f, i) => {
            const k = interpolate(t, [hitAt - 0.6 + i * 0.12, hitAt + i * 0.12], [0, 1], clamp);
            if (k <= 0 || k >= 1) return null;
            return <ellipse key={f} cx={-60 + (B_LEFT + 120) * k} cy={floorY(f) + FLOOR_H / 2} rx={30} ry={11} fill="#0b0b0c" stroke={accent.amber} strokeWidth={3} />;
          })}
        {hit > 0 && hit < 1 && <circle cx={B_LEFT + 160} cy={floorY(2) + 40} r={80 + 420 * hit} fill={accent.amber} opacity={0.6 * (1 - hit)} />}
        {marks.map((m, i) => {
          const local = t - m.at;
          if (local < 0) return null;
          const pop = spring({ frame: local * fps, fps, config: { damping: 11, stiffness: 190, mass: 0.6 } });
          const y = m.floor === FLOORS ? floorY(FLOORS) - 60 : floorY(m.floor) + FLOOR_H / 2;
          const c = accent[m.color ?? "amber"];
          return (
            <g key={i} opacity={Math.min(1, pop * 1.2)}>
              <rect x={B_LEFT - 8} y={floorY(m.floor) + 2} width={B_RIGHT - B_LEFT + 16} height={FLOOR_H - 4} fill="none" stroke={c} strokeWidth={5} />
              <text x={540} y={y + 16} textAnchor="middle" fontFamily={fonts.title} fontWeight={900} fontSize={46} fill="#fff" stroke="#000" strokeWidth={9} paintOrder="stroke">
                {m.label}
              </text>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
