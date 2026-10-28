import React from "react";
import { AbsoluteFill, Img, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { accent, archivalFilter, fonts } from "./theme";
import { B17_PARTS, B17Top, Bf109Top } from "./Motion";
import { CensoredText } from "./CensoredText";
import type { Visual } from "./types";

const BLUEPRINT = "#0c1c2e";
const LINE = "#7FB8E6";

// ───────────── plano técnico del B-17 con los daños marcándose uno a uno ─────────────

export const BomberScene: React.FC<Extract<Visual, { kind: "bomber" }>> = ({ title, marks }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const draw = interpolate(frame, [0, 0.8 * fps], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const zoom = interpolate(frame, [0, durationInFrames], [1.0, 1.12]);
  const S = 2.0; // escala del avión en pantalla
  const CX = 540;
  const CY = 1000;
  const noseGone = marks.some((m) => m.part === "nose" && t >= m.at);
  const dead = marks.filter((m) => m.part.startsWith("engine") && t >= m.at).map((m) => Number(m.part.slice(-1)));

  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 50%, #12304d, ${BLUEPRINT} 70%)` }}>
      <svg width={1080} height={1920}>
        <defs>
          <pattern id="bp-grid" width={40} height={40} patternUnits="userSpaceOnUse">
            <path d="M40,0 L0,0 0,40" fill="none" stroke={LINE} strokeOpacity={0.12} strokeWidth={1} />
          </pattern>
        </defs>
        <rect width={1080} height={1920} fill="url(#bp-grid)" />
        <g transform={`translate(${CX}, ${CY}) scale(${S * zoom})`} opacity={draw}>
          <B17Top fill="rgba(127,184,230,0.08)" stroke={LINE} strokeWidth={1.6} noseGone={noseGone} deadEngines={dead} props={Math.sin(t * 40) * 6} />
        </g>
        {marks.map((m, i) => {
          const local = t - m.at;
          if (local < 0) return null;
          const [px, py] = B17_PARTS[m.part];
          const x = CX + px * S * zoom;
          const y = CY + py * S * zoom;
          const c = accent[m.color ?? "red"];
          const pop = spring({ frame: local * fps, fps, config: { damping: 10, stiffness: 200, mass: 0.5 } });
          const pulse = (local % 1) / 1;
          const right = m.side ? m.side === "right" : px >= 0;
          const lx = right ? 1020 : 60;
          const ly = y + (i % 2 ? 60 : -60);
          return (
            <g key={i}>
              <circle cx={x} cy={y} r={30 + pulse * 50} fill="none" stroke={c} strokeWidth={4} opacity={1 - pulse} />
              <circle cx={x} cy={y} r={26 * pop} fill={c} fillOpacity={0.35} stroke={c} strokeWidth={4} />
              <polyline points={`${x},${y} ${x + (right ? 60 : -60)},${ly} ${lx},${ly}`} fill="none" stroke={c} strokeWidth={3} opacity={pop} />
              <text
                x={lx}
                y={ly - 14}
                textAnchor={right ? "end" : "start"}
                fontFamily={fonts.title}
                fontWeight={900}
                fontSize={40}
                fill="#fff"
                stroke="#000"
                strokeWidth={6}
                paintOrder="stroke"
                opacity={pop}
              >
                {m.label}
              </text>
            </g>
          );
        })}
      </svg>
      <div style={{ position: "absolute", top: 560, left: 56, fontFamily: fonts.mono, fontWeight: 700, fontSize: 32, letterSpacing: 4, color: LINE, opacity: draw }}>
        {title}
      </div>
    </AbsoluteFill>
  );
};

// ───────────── los dos aviones desde arriba ─────────────

const Clouds: React.FC<{ speed: number; sea?: boolean }> = ({ speed, sea }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: sea ? "linear-gradient(180deg, #1d2b36, #24343f 50%, #1a2731)" : "linear-gradient(180deg, #6d7378, #8b9095 50%, #5f656a)" }}>
      {sea &&
        Array.from({ length: 40 }, (_, i) => {
          const y = ((random(`wy-${i}`) * 2200 + frame * speed * 0.6) % 2200) - 140;
          return <div key={i} style={{ position: "absolute", left: random(`wx-${i}`) * 1080, top: y, width: 60 + random(`ww-${i}`) * 120, height: 3, background: "rgba(200,220,230,0.18)", borderRadius: 2 }} />;
        })}
      {Array.from({ length: sea ? 6 : 14 }, (_, i) => {
        const size = 300 + random(`cs-${i}`) * 500;
        const y = ((random(`cy-${i}`) * 2600 + frame * speed * (0.8 + random(`cv-${i}`) * 0.5)) % 2600) - size;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: random(`cx-${i}`) * 1180 - 150,
              top: y,
              width: size,
              height: size * 0.6,
              borderRadius: "50%",
              background: "radial-gradient(ellipse, rgba(240,242,245,0.85), rgba(240,242,245,0) 70%)",
              filter: "blur(18px)",
              opacity: sea ? 0.35 : 0.8,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

const Flak: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const period = Math.round(0.5 * fps);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {[0, 1, 2].map((lane) => {
        const f = frame + lane * Math.round(period / 3);
        const k = Math.floor(f / period);
        const local = f - k * period;
        const x = 120 + random(`fkx-${lane}-${k}`) * 840;
        const y = 600 + random(`fky-${lane}-${k}`) * 900;
        const grow = interpolate(local, [0, period], [0.3, 1.4]);
        const flash = interpolate(local, [0, 2, 6], [0, 1, 0], { extrapolateRight: "clamp" });
        return (
          <React.Fragment key={lane}>
            <div style={{ position: "absolute", left: x - 90 * grow, top: y - 90 * grow + local * 3, width: 180 * grow, height: 180 * grow, borderRadius: "50%", background: "radial-gradient(circle, rgba(25,25,25,0.85), rgba(25,25,25,0) 70%)", opacity: 1 - local / period }} />
            <div style={{ position: "absolute", left: x - 60, top: y - 60, width: 120, height: 120, borderRadius: "50%", background: "radial-gradient(circle, rgba(255,230,170,1), rgba(255,150,60,0) 70%)", opacity: flash }} />
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};

const Smoke: React.FC<{ x: number; y: number; scale: number }> = ({ x, y, scale }) => {
  const frame = useCurrentFrame();
  return (
    <>
      {Array.from({ length: 14 }, (_, i) => {
        const age = (frame + i * 4) % 56;
        const s = (14 + age * 1.6) * scale;
        return <circle key={i} cx={x + Math.sin((frame + i * 9) / 7) * 4 * scale} cy={y + age * 9 * scale} r={s} fill="rgba(40,40,40,0.5)" opacity={(1 - age / 56) * 0.7} filter="url(#smoke-blur)" />;
      })}
    </>
  );
};

export const EscortScene: React.FC<Extract<Visual, { kind: "escort" }>> = ({ fighter, flak, sea, smoke }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const p = interpolate(frame, [0, durationInFrames], [0, 1]);
  const S = 1.5;
  const bx = 470 + Math.sin(t * 0.9) * 10;
  const by = 1000 + Math.sin(t * 1.3) * 8;
  const bank = Math.sin(t * 0.7) * 2;
  const prop = Math.sin(t * 50) * 8;

  // Posición del caza según el momento de la historia.
  let fx = 0;
  let fy = 0;
  let fr = 0;
  let fo = 1;
  const ease = Easing.inOut(Easing.cubic);
  if (fighter === "approach") {
    const k = interpolate(p, [0, 0.8], [0, 1], { extrapolateRight: "clamp", easing: ease });
    fx = bx + 30;
    fy = 2100 - (2100 - (by + 430)) * k;
  } else if (fighter === "behind") {
    fx = bx + Math.sin(t * 1.7) * 18;
    fy = by + 420 + Math.sin(t * 2.1) * 12;
  } else if (fighter === "wing") {
    const k = interpolate(p, [0, 0.45], [0, 1], { extrapolateRight: "clamp", easing: ease });
    fx = bx + 30 + (330 - 30) * k;
    fy = by + 420 - (420 - 20) * k + Math.sin(t * 1.5) * 8;
    fr = (1 - k) * -6;
  } else if (fighter === "break") {
    const k = interpolate(p, [0.35, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
    const wave = p < 0.35 ? Math.sin(t * 9) * 8 : 0; // saludo: alabeo
    fx = bx + 330 + 500 * k;
    fy = by + 20 + 700 * k;
    fr = wave + 130 * k;
  } else {
    fo = 0;
  }

  return (
    <AbsoluteFill>
      <Clouds speed={sea ? 6 : 9} sea={sea} />
      {flak && <Flak />}
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        <defs>
          <filter id="smoke-blur" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation={10} />
          </filter>
        </defs>
        {/* sombras */}
        <g transform={`translate(${bx + 60}, ${by + 90}) scale(${S}) rotate(${bank})`} opacity={0.25}>
          <B17Top fill="#000" stroke="none" />
        </g>
        {smoke && (
          <>
            <Smoke x={bx - 70 * S} y={by - 10} scale={1.2} />
            <Smoke x={bx + 70 * S} y={by - 10} scale={1.1} />
          </>
        )}
        <g transform={`translate(${bx}, ${by}) scale(${S}) rotate(${bank})`}>
          <B17Top fill="#3a3f44" props={prop} noseGone deadEngines={smoke ? [2, 3] : []} />
          {/* agujeros */}
          {[[-40, 10], [8, 40], [-5, 110], [120, 0], [-150, 4], [10, -70]].map(([x, y], i) => (
            <circle key={i} cx={x} cy={y} r={4 + (i % 3)} fill="#0b0b0b" />
          ))}
        </g>
        {fo > 0 && (
          <g transform={`translate(${fx}, ${fy}) scale(${S * 0.95}) rotate(${fr})`}>
            <Bf109Top fill="#6a7178" props={prop} />
          </g>
        )}
      </svg>
    </AbsoluteFill>
  );
};

// ───────────── cita escrita a máquina ─────────────

export const QuoteScene: React.FC<Extract<Visual, { kind: "quote" }> & { folder: string }> = ({ folder, text, author, background, stamp = "RECONSTRUCCIÓN" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const chars = Math.floor(interpolate(frame, [6, 6 + text.length * 1.25], [0, text.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const done = 6 + text.length * 1.25;
  const card = spring({ frame, fps, config: { damping: 14, stiffness: 140 } });
  const st = spring({ frame: frame - done - 4, fps, config: { damping: 8, stiffness: 300, mass: 0.6 } });
  const caret = Math.floor(frame / 8) % 2 === 0;
  return (
    <AbsoluteFill>
      <Img src={staticFile(`${folder}/${background}`)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: `${archivalFilter} brightness(0.35) blur(6px)` }} />
      <div
        style={{
          position: "absolute",
          left: 70,
          right: 70,
          top: 660,
          padding: "60px 56px 70px",
          background: "linear-gradient(180deg, #efe6cf, #e2d6b8)",
          boxShadow: "0 30px 80px rgba(0,0,0,0.7)",
          transform: `rotate(${-1.5 + (1 - card) * -6}deg) translateY(${(1 - card) * 300}px)`,
          opacity: card,
        }}
      >
        <div style={{ fontFamily: fonts.mono, fontWeight: 700, fontSize: 52, lineHeight: 1.35, color: "#1d1a14" }}>
          «<CensoredText text={text.slice(0, chars)} blur={1} />
          {chars < text.length && caret ? "▌" : ""}
          {chars >= text.length ? "»" : ""}
        </div>
        <div style={{ marginTop: 34, fontFamily: fonts.body, fontWeight: 800, fontSize: 32, color: "#5a4a30", letterSpacing: 2, opacity: chars >= text.length ? 1 : 0 }}>— {author}</div>
        <div
          style={{
            position: "absolute",
            right: 30,
            bottom: -30,
            padding: "10px 22px",
            border: `6px solid ${accent.red}`,
            color: accent.red,
            fontFamily: fonts.title,
            fontWeight: 900,
            fontSize: 38,
            letterSpacing: 3,
            transform: `rotate(-9deg) scale(${frame > done + 4 ? 2.2 - 1.2 * st : 0})`,
            opacity: frame > done + 4 ? 0.85 : 0,
            background: "rgba(239,230,207,0.3)",
          }}
        >
          {stamp}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ───────────── versus ─────────────

export const VersusScene: React.FC<Extract<Visual, { kind: "versus" }> & { folder: string }> = ({ folder, left, right }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const inL = spring({ frame, fps, config: { damping: 14, stiffness: 160 } });
  const inR = spring({ frame: frame - 6, fps, config: { damping: 14, stiffness: 160 } });
  const vs = spring({ frame: frame - 14, fps, config: { damping: 7, stiffness: 260, mass: 0.6 } });
  const side = (f: typeof left, k: number, dir: -1 | 1) => (
    <div style={{ position: "absolute", top: 600, [dir < 0 ? "left" : "right"]: 0, width: 540, height: 900, overflow: "hidden", transform: `translateX(${dir * (1 - k) * 600}px)` } as React.CSSProperties}>
      <Img
        src={staticFile(`${folder}/${f.src}`)}
        style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: `${(f.focus ?? [0.5, 0.4])[0] * 100}% ${(f.focus ?? [0.5, 0.4])[1] * 100}%`, filter: archivalFilter, transform: `scale(${1.05 + frame / fps / 60})` }}
      />
      <div style={{ position: "absolute", inset: 0, background: `linear-gradient(180deg, rgba(0,0,0,0) 45%, rgba(0,0,0,0.9))`, borderTop: `8px solid ${accent[f.color]}` }} />
      <div style={{ position: "absolute", left: 30, right: 30, bottom: 40, textAlign: dir < 0 ? "left" : "right" }}>
        <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 58, color: accent[f.color], lineHeight: 1, textTransform: "uppercase" }}>{f.name}</div>
        {f.lines.map((l, i) => (
          <div key={i} style={{ marginTop: 10, fontFamily: fonts.body, fontWeight: 800, fontSize: 30, color: "#fff", letterSpacing: 1 }}>
            {l}
          </div>
        ))}
      </div>
    </div>
  );
  return (
    <AbsoluteFill style={{ background: "#0b0b0b" }}>
      {side(left, inL, -1)}
      {side(right, inR, 1)}
      <div style={{ position: "absolute", left: 536, top: 600, width: 8, height: 900, background: "#fff", transform: `scaleY(${vs})`, boxShadow: "0 0 30px #fff" }} />
      <div
        style={{
          position: "absolute",
          left: 390,
          top: 940,
          width: 300,
          textAlign: "center",
          fontFamily: fonts.title,
          fontWeight: 900,
          fontSize: 150,
          color: "#fff",
          WebkitTextStroke: "4px #000",
          textShadow: `0 0 50px ${accent.amber}`,
          transform: `scale(${frame < 14 ? 0 : 2.5 - 1.5 * vs}) rotate(-6deg)`,
        }}
      >
        VS
      </div>
    </AbsoluteFill>
  );
};

// ───────────── condecoración ─────────────

export const MedalScene: React.FC<Extract<Visual, { kind: "medal" }>> = ({ label }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const pop = spring({ frame, fps, config: { damping: 10, stiffness: 120, mass: 0.8 } });
  const spin = 0.55 + 0.45 * Math.abs(Math.cos(t * 1.4)); // giro 3D aparente, sin quedar de canto
  const shine = interpolate((t * 0.8) % 1, [0, 1], [-300, 300]);
  // Cruz paté genérica, sin ningún símbolo en el centro.
  const arm = "M-60,-170 L60,-170 L18,-28 L0,-22 L-18,-28 Z";
  return (
    <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 50%, #2a2418, #0b0a08 70%)" }}>
      <svg width={1080} height={1920}>
        <g transform={`translate(540, 1000) rotate(${t * 12})`} opacity={0.35}>
          {Array.from({ length: 18 }, (_, i) => (
            <path key={i} d="M0,0 L-40,-900 L40,-900 Z" fill={accent.amber} opacity={0.18} transform={`rotate(${i * 20})`} />
          ))}
        </g>
        <defs>
          <linearGradient id="silver" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#f4f4f4" />
            <stop offset="50%" stopColor="#9c9c9c" />
            <stop offset="100%" stopColor="#e6e6e6" />
          </linearGradient>
          <clipPath id="medal-clip">
            {[0, 90, 180, 270].map((a) => (
              <path key={a} d={arm} transform={`rotate(${a})`} />
            ))}
          </clipPath>
        </defs>
        <g transform={`translate(540, 1000) scale(${pop * spin * 1.6}, ${pop * 1.6})`}>
          <rect x={-50} y={-300} width={100} height={130} fill="#1a1a1a" stroke="url(#silver)" strokeWidth={6} />
          {[0, 90, 180, 270].map((a) => (
            <path key={a} d={arm} transform={`rotate(${a})`} fill="#141414" stroke="url(#silver)" strokeWidth={10} strokeLinejoin="round" />
          ))}
          <g clipPath="url(#medal-clip)">
            <rect x={shine - 40} y={-200} width={50} height={400} fill="rgba(255,255,255,0.22)" />
          </g>
        </g>
      </svg>
      <div style={{ position: "absolute", top: 1380, left: 0, right: 0, textAlign: "center", fontFamily: fonts.title, fontWeight: 900, fontSize: 70, color: accent.amber, textShadow: "0 6px 30px rgba(0,0,0,0.9)", opacity: pop }}>
        {label}
      </div>
    </AbsoluteFill>
  );
};
