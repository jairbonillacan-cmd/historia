import React from "react";
import { AbsoluteFill, Easing, interpolate, random, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Dreadnought } from "./NavalScenes";
import { accent } from "./theme";
import type { Visual } from "./types";

// Hundimiento deliberado de una flota (Scapa Flow, 1919). Barcos de perfil sobre una bahía gris;
// todo lo que queda bajo la línea de flotación lo tapa el mar que se dibuja encima de cada barco.
type ScuttleProps = Extract<Visual, { kind: "scuttle" }>;

const HORIZON = 1060;
const SKY = "linear-gradient(180deg, #4d5357 0%, #7c8180 40%, #a3a49d 55.2%, #50575a 55.2%, #262c2f 100%)";
const SEA_TOP = "#4d5458";
const SEA_BOTTOM = "#22282b";
const SHIP = "#1b1d1f";
const KEEL = "#5b2c24"; // pintura antiincrustante del casco, que queda a la vista cuando el barco vuelca

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const ScuttleScene: React.FC<ScuttleProps> = ({ stage, eventAt = 0.8 }) => {
  switch (stage) {
    case "signal":
      return <SignalMast eventAt={eventAt} />;
    case "valve":
      return <SeaValve eventAt={eventAt} />;
    case "boil":
      return <BoilingSea />;
    default:
      return <Bay stage={stage} eventAt={eventAt} />;
  }
};

// ───────────── la bahía con barcos que se inclinan, vuelcan o se van al fondo ─────────────

type ShipState = { x: number; y: number; s: number; rot: number; sink: number; flip: number; haze: number };

const Bay: React.FC<{ stage: "list" | "capsize" | "sink"; eventAt: number }> = ({ stage, eventAt }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const zoom = interpolate(frame, [0, durationInFrames], [1.0, 1.07]);
  const e = t - eventAt;

  let ships: ShipState[];
  if (stage === "list") {
    // El acorazado de enfrente se inclina de proa y empieza a asentarse; detrás, la flota fondeada.
    const k = interpolate(e, [0, 2.4], [0, 1], { ...clamp, easing: Easing.out(Easing.quad) });
    ships = [
      { x: 560, y: HORIZON + 300, s: 1.0, rot: -13 * k, sink: 70 * k, flip: 1, haze: 1 },
      { x: 200, y: HORIZON + 70, s: 0.42, rot: 0, sink: 0, flip: 1, haze: 0.82 },
      { x: 880, y: HORIZON + 34, s: 0.3, rot: -3 * k, sink: 6 * k, flip: 1, haze: 0.7 },
    ];
  } else if (stage === "capsize") {
    // Vuelta de campana: visto de perfil, el barco se da vuelta sobre la línea de flotación y asoma la quilla.
    const roll = interpolate(e, [0, 2.6], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
    ships = [
      { x: 540, y: HORIZON + 330, s: 1.02, rot: 4 * Math.sin(roll * Math.PI), sink: 30 * roll + Math.max(0, e - 2.6) * 6, flip: 1 - 1.55 * roll, haze: 1 },
      { x: 860, y: HORIZON + 50, s: 0.34, rot: -6, sink: 18, flip: 1, haze: 0.75 },
    ];
  } else {
    // Varios barcos a la vez, cada uno en otro punto del hundimiento.
    const p = (d: number, len: number) => interpolate(t - eventAt - d, [0, len], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
    ships = [
      { x: 330, y: HORIZON + 280, s: 0.78, rot: 14 * p(0, 5), sink: 140 * p(0, 5), flip: 1, haze: 1 },
      { x: 830, y: HORIZON + 150, s: 0.5, rot: -18 * p(0.6, 4), sink: 160 * p(0.6, 4), flip: 1, haze: 0.9 },
      { x: 150, y: HORIZON + 50, s: 0.3, rot: 6, sink: 60 + 120 * p(0, 6), flip: 1, haze: 0.75 },
      { x: 640, y: HORIZON + 22, s: 0.22, rot: 0, sink: 40 + 140 * p(1.2, 5), flip: 1, haze: 0.65 },
    ];
  }

  // Del fondo hacia adelante: cada barco lleva su propia franja de mar encima, que le tapa lo sumergido.
  const order = [...ships].sort((a, b) => a.y - b.y);
  const splash = stage === "capsize" ? interpolate(e, [0.2, 0.7, 2.4], [0, 1, 0], clamp) : 0;

  return (
    <AbsoluteFill style={{ background: SKY }}>
      <svg width={1080} height={1920} style={{ transform: `scale(${zoom})`, transformOrigin: "50% 60%" }}>
        <defs>
          <linearGradient id="scuttle-sea" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor={SEA_TOP} />
            <stop offset="1" stopColor={SEA_BOTTOM} />
          </linearGradient>
          <filter id="scuttle-blur" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation={14} />
          </filter>
        </defs>
        {/* costa baja de las Orcadas */}
        <path d={`M-20,${HORIZON} L-20,${HORIZON - 36} Q160,${HORIZON - 70} 330,${HORIZON - 30} Q520,${HORIZON - 8} 700,${HORIZON - 44} Q900,${HORIZON - 80} 1100,${HORIZON - 26} L1100,${HORIZON} Z`} fill="#5d6260" opacity={0.7} />
        {order.map((p, i) => (
          <g key={i}>
            <g opacity={p.haze} transform={`translate(${p.x}, ${p.y + p.sink}) rotate(${p.rot}) scale(${p.s}, ${p.s * p.flip})`}>
              <path d="M-470,0 L490,0 Q470,60 380,78 L-360,78 Q-460,60 -470,0 Z" fill={KEEL} />
              <Dreadnought fill={SHIP} />
            </g>
            <rect x={-200} y={p.y - 2} width={1480} height={1920} fill="url(#scuttle-sea)" />
            <Bubbles cx={p.x} cy={p.y} w={520 * p.s} t={t} seed={i} amount={stage === "list" && i > 0 ? 0 : 1} />
          </g>
        ))}
        <Ripples t={t} />
        {splash > 0 && (
          <g filter="url(#scuttle-blur)" opacity={splash}>
            {Array.from({ length: 14 }, (_, k) => (
              <ellipse key={k} cx={140 + k * 60 + random(`sp${k}`) * 40} cy={HORIZON + 310 - random(`sh${k}`) * 120 * splash} rx={40} ry={50 + random(`sr${k}`) * 60} fill="#e9e5da" opacity={0.28} />
            ))}
          </g>
        )}
        {stage === "sink" && <Lifeboats t={t} />}
      </svg>
    </AbsoluteFill>
  );
};

// Burbujas y espuma que suben a lo largo del casco.
const Bubbles: React.FC<{ cx: number; cy: number; w: number; t: number; seed: number; amount: number }> = ({ cx, cy, w, t, seed, amount }) => {
  if (!amount) return null;
  return (
    <g>
      {Array.from({ length: 34 }, (_, k) => {
        const life = 1.1 + random(`bl${seed}-${k}`) * 0.9;
        const age = (t + random(`bo${seed}-${k}`) * life) % life;
        const q = age / life;
        const x = cx + (random(`bx${seed}-${k}`) - 0.5) * 2 * w;
        const r = (4 + random(`br${seed}-${k}`) * 12) * (w / 500) * (0.4 + q);
        return <circle key={k} cx={x} cy={cy + 6 + random(`by${seed}-${k}`) * 30 * (w / 500)} r={r} fill="none" stroke="#e9e5da" strokeWidth={2} opacity={(1 - q) * 0.6} />;
      })}
      <ellipse cx={cx} cy={cy + 8} rx={w * 1.05} ry={10 * (w / 500)} fill="#e9e5da" opacity={0.18 + 0.08 * Math.sin(t * 3 + seed)} />
    </g>
  );
};

const Ripples: React.FC<{ t: number }> = ({ t }) => (
  <g>
    {Array.from({ length: 24 }, (_, i) => {
      const y = HORIZON + 14 + i * i * 1.4;
      const off = ((t * (18 + i * 3)) % 220) - 110;
      return <line key={i} x1={-100 + off} y1={y} x2={1180 + off} y2={y} stroke="#e9e5da" strokeOpacity={0.035 + i * 0.002} strokeWidth={1 + i * 0.12} strokeDasharray={`${40 + i * 6} ${30 + i * 5}`} />;
    })}
  </g>
);

// Botes salvavidas con marineros que se alejan remando.
const Lifeboats: React.FC<{ t: number }> = ({ t }) => (
  <g>
    {[
      { x: 120, y: 1560, s: 1.1, v: 18 },
      { x: 700, y: 1680, s: 1.3, v: -14 },
      { x: 520, y: 1470, s: 0.8, v: 10 },
    ].map((b, i) => (
      <g key={i} transform={`translate(${b.x + t * b.v}, ${b.y + Math.sin(t * 1.6 + i) * 6}) scale(${b.s})`}>
        <path d="M-120,0 L120,0 Q100,30 70,34 L-80,34 Q-110,28 -120,0 Z" fill="#141618" />
        {Array.from({ length: 6 }, (_, k) => (
          <circle key={k} cx={-80 + k * 32} cy={-14} r={11} fill="#141618" />
        ))}
        <line x1={-130} y1={20} x2={-170} y2={44 + Math.sin(t * 3 + i) * 8} stroke="#141618" strokeWidth={5} />
        <line x1={130} y1={20} x2={170} y2={44 + Math.sin(t * 3 + i) * 8} stroke="#141618" strokeWidth={5} />
      </g>
    ))}
  </g>
);

// ───────────── el mar que «hierve»: burbujas, espuma y restos ─────────────

const BoilingSea: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 55%, #3b4447, #161b1d 80%)" }}>
      <svg width={1080} height={1920}>
        {/* manchas de aceite que se abren */}
        {Array.from({ length: 6 }, (_, k) => (
          <ellipse key={`o${k}`} cx={180 + random(`ox${k}`) * 720} cy={500 + random(`oy${k}`) * 1000} rx={140 + t * 30 + k * 20} ry={60 + t * 12} fill="#6b5a3a" opacity={0.12} transform={`rotate(${random(`or${k}`) * 40 - 20})`} />
        ))}
        {/* surgentes: anillos que se abren donde sube el aire de los barcos */}
        {Array.from({ length: 22 }, (_, k) => {
          const life = 1.4 + random(`rl${k}`) * 1.2;
          const age = (t + random(`ro${k}`) * life) % life;
          const q = age / life;
          return (
            <circle key={`r${k}`} cx={80 + random(`rx${k}`) * 920 + Math.floor((t + random(`ro${k}`) * life) / life) * 37 % 120} cy={420 + random(`ry${k}`) * 1250} r={20 + q * 170} fill="none" stroke="#e9e5da" strokeWidth={6 * (1 - q)} opacity={(1 - q) * 0.55} />
          );
        })}
        {/* burbujas */}
        {Array.from({ length: 160 }, (_, k) => {
          const life = 0.5 + random(`bl${k}`) * 0.7;
          const age = (t + random(`bo${k}`) * life) % life;
          const q = age / life;
          const r = (6 + random(`br${k}`) * 26) * Math.sin(q * Math.PI);
          return <circle key={`b${k}`} cx={random(`bx${k}`) * 1080} cy={380 + random(`by${k}`) * 1400} r={r} fill="#dfe3e0" fillOpacity={0.12} stroke="#f2f1ea" strokeWidth={2.5} opacity={0.75} />;
        })}
        {/* tablones y restos a la deriva */}
        {Array.from({ length: 7 }, (_, k) => (
          <rect
            key={`d${k}`}
            x={-60 + random(`dx${k}`) * 1080 + t * (10 + k * 3)}
            y={500 + random(`dy${k}`) * 1100 + Math.sin(t * 1.4 + k) * 8}
            width={70 + random(`dw${k}`) * 120}
            height={14}
            rx={4}
            fill="#2b2420"
            transform={`rotate(${random(`dr${k}`) * 60 - 30}, 540, 960)`}
          />
        ))}
      </svg>
    </AbsoluteFill>
  );
};

// ───────────── la señal de banderas que sube por el mástil ─────────────

// Tres banderas del código de señales, una por palabra. Entran a los `eventAt` s, separadas 0,5 s.
const FLAGS: { bg: string; draw: (w: number, h: number) => React.ReactNode }[] = [
  { bg: "#f5f2eb", draw: (w, h) => <rect x={w / 3} y={0} width={w / 3} height={h} fill="#1f4e9c" /> },
  { bg: "#e0b02c", draw: (w, h) => <path d={`M0,0 L${w},${h} M${w},0 L0,${h}`} stroke="#1a1a1a" strokeWidth={16} /> },
  { bg: accent.red, draw: (w, h) => <rect x={w * 0.3} y={h * 0.3} width={w * 0.4} height={h * 0.4} fill="#f5f2eb" /> },
];

const SignalMast: React.FC<{ eventAt: number }> = ({ eventAt }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const MX = 330;
  const TOP = 480;
  const W = 230;
  const H = 150;
  return (
    <AbsoluteFill style={{ background: "linear-gradient(180deg, #5d6366 0%, #8f9290 60%, #a7a59c 100%)" }}>
      <svg width={1080} height={1920}>
        {/* nubes bajas que pasan */}
        {Array.from({ length: 5 }, (_, k) => (
          <ellipse key={k} cx={((random(`c${k}`) * 1400 + t * (14 + k * 6)) % 1500) - 200} cy={300 + k * 230} rx={340} ry={70} fill="#e6e4dc" opacity={0.08} />
        ))}
        {/* mástil, verga y drizas */}
        <rect x={MX - 16} y={TOP - 120} width={32} height={1920} fill="#1d1f21" />
        <rect x={MX - 220} y={TOP - 40} width={440} height={18} fill="#1d1f21" />
        <line x1={MX + 200} y1={TOP - 30} x2={MX + 200} y2={1920} stroke="#1d1f21" strokeWidth={3} />
        {FLAGS.map((f, i) => {
          const s = t - eventAt - i * 0.5;
          const rise = spring({ frame: s * fps, fps, config: { damping: 16, stiffness: 70 } });
          if (s < 0) return null;
          const y = interpolate(rise, [0, 1], [1900, TOP + i * (H + 34)]);
          const wave = Math.sin(t * 7 + i) * 0.06;
          return (
            <g key={i} transform={`translate(${MX + 200}, ${y}) skewY(${wave * 40})`}>
              <rect width={W} height={H} fill={f.bg} />
              <svg width={W} height={H}>{f.draw(W, H)}</svg>
              <rect width={W} height={H} fill="none" stroke="#111" strokeWidth={3} opacity={0.4} />
              <line x1={0} y1={H} x2={0} y2={H + 34} stroke="#1d1f21" strokeWidth={3} />
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

// ───────────── la toma de mar: la rueda de bronce se abre y se rompe ─────────────

const SeaValve: React.FC<{ eventAt: number }> = ({ eventAt }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const CX = 540;
  const CY = 900;
  const R = 280;
  const turn = interpolate(t, [0, eventAt], [0, 420], { ...clamp, easing: Easing.in(Easing.quad) });
  const b = t - eventAt; // golpe de la maza: la rueda se parte en pedazos
  const broken = b >= 0;
  const water = interpolate(t, [0.3, eventAt + 2.5], [1920, 1250], clamp);
  const jet = interpolate(t, [0.2, eventAt], [0.25, 1], clamp);

  const spokes = Array.from({ length: 5 }, (_, k) => (k * 72 * Math.PI) / 180);
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, #2d2a25, #0a0a09 75%)" }}>
      <svg width={1080} height={1920}>
        {/* caño y brida */}
        <rect x={CX - 70} y={CY} width={140} height={1100} fill="#3a352d" />
        <rect x={CX - 120} y={CY + 340} width={240} height={50} rx={8} fill="#4a4338" />
        {/* chorros de agua de mar */}
        {Array.from({ length: 18 }, (_, k) => {
          const a = -0.9 + (k / 17) * 1.8;
          const len = (220 + random(`j${k}`) * 260) * jet * (0.85 + 0.15 * Math.sin(t * 20 + k));
          const x0 = CX + (k % 2 ? 120 : -120);
          const y0 = CY + 365;
          return <line key={k} x1={x0} y1={y0} x2={x0 + Math.sin(a) * len * (k % 2 ? 1 : -1)} y2={y0 + Math.cos(a) * len * 0.4 - 30} stroke="#cfe0e6" strokeWidth={4 + random(`jw${k}`) * 6} strokeLinecap="round" opacity={0.5} />;
        })}
        {/* rueda: entera mientras gira, en pedazos que vuelan después del golpe */}
        {spokes.map((a, k) => {
          const fly = broken ? b : 0;
          const dx = Math.cos(a + 0.6) * fly * 900;
          const dy = Math.sin(a + 0.6) * fly * 700 + fly * fly * 900;
          return (
            <g key={k} transform={`translate(${CX + dx}, ${CY + dy}) rotate(${turn + fly * (k % 2 ? 300 : -260)})`} opacity={broken ? Math.max(0, 1 - b * 0.9) : 1}>
              <path d={arc(R, (k * 72 - 34), (k * 72 + 34))} stroke="#b38c51" strokeWidth={46} fill="none" strokeLinecap="round" />
              <line x1={0} y1={0} x2={Math.cos(a) * R} y2={Math.sin(a) * R} stroke="#9c7742" strokeWidth={30} strokeLinecap="round" />
            </g>
          );
        })}
        <circle cx={CX} cy={CY} r={70} fill="#8a6a3d" />
        <circle cx={CX} cy={CY} r={28} fill="#2b2b2b" />
        {/* chispa del golpe */}
        {broken && b < 0.25 && <circle cx={CX} cy={CY} r={120 + b * 1600} fill="#fff4dc" opacity={1 - b * 4} />}
        {/* el agua que sube en la bodega */}
        <rect x={0} y={water + Math.sin(t * 2) * 6} width={1080} height={1920} fill="#26404a" opacity={0.75} />
        <line x1={0} y1={water + Math.sin(t * 2) * 6} x2={1080} y2={water + Math.sin(t * 2 + 1) * 6} stroke="#cfe0e6" strokeWidth={4} opacity={0.5} />
      </svg>
    </AbsoluteFill>
  );
};

function arc(r: number, a0: number, a1: number): string {
  const p = (a: number) => [Math.cos((a * Math.PI) / 180) * r, Math.sin((a * Math.PI) / 180) * r];
  const [x0, y0] = p(a0);
  const [x1, y1] = p(a1);
  return `M${x0},${y0} A${r},${r} 0 0 1 ${x1},${y1}`;
}
