import React from "react";
import { AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { accent, fonts, layout } from "./theme";
import type { Accent, Transition } from "./types";
import { CensoredText } from "./CensoredText";

// Sello de goma que cae de golpe sobre la pantalla («INTERCEPTADO», «RECHAZADO»).
export const Stamp: React.FC<{ text: string; color?: Accent; y?: number; rotate?: number }> = ({ text, color = "red", y = 980, rotate = -8 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const hit = spring({ frame, fps, config: { damping: 9, stiffness: 320, mass: 0.6 } });
  const c = accent[color];
  const fontSize = text.length > 12 ? 78 : 104;
  return (
    <AbsoluteFill style={{ alignItems: "center", pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          top: y - fontSize,
          padding: "14px 34px 10px",
          border: `10px double ${c}`,
          borderRadius: 14,
          color: c,
          fontFamily: fonts.title,
          fontWeight: 900,
          fontSize,
          letterSpacing: 6,
          textTransform: "uppercase",
          background: "rgba(10,10,10,0.35)",
          // textura de tinta gastada
          maskImage: "repeating-radial-gradient(circle at 30% 40%, #000 0 3px, rgba(0,0,0,0.78) 3px 5px)",
          WebkitMaskImage: "repeating-radial-gradient(circle at 30% 40%, #000 0 3px, rgba(0,0,0,0.78) 3px 5px)",
          transform: `rotate(${rotate}deg) scale(${2.6 - 1.6 * hit})`,
          opacity: interpolate(frame, [0, 3], [0, 0.92], { extrapolateRight: "clamp" }),
          textShadow: `0 0 24px ${c}66`,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

// Lista de opciones que aparecen una a una (`times` en segundos) y se tachan juntas en `crossAt`.
export const Options: React.FC<{ items: string[]; times: number[]; crossAt?: number; title?: string }> = ({ items, times, crossAt, title }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sec = frame / fps;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", top: 640, left: 70, right: 70 }}>
        {title && (
          <div style={{ fontFamily: fonts.mono, fontWeight: 700, fontSize: 36, letterSpacing: 4, color: accent.amber, marginBottom: 18, textShadow: "0 2px 10px #000" }}>{title}</div>
        )}
        {items.map((it, i) => {
          const local = (sec - (times[i] ?? 0)) * fps;
          const pop = spring({ frame: local, fps, config: { damping: 13, stiffness: 200, mass: 0.6 } });
          const crossed = crossAt !== undefined ? interpolate(sec - crossAt - i * 0.08, [0, 0.18], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
          return (
            <div
              key={i}
              style={{
                position: "relative",
                display: "flex",
                alignItems: "center",
                gap: 26,
                marginBottom: 22,
                padding: "22px 30px",
                background: "rgba(12,12,12,0.86)",
                borderLeft: `10px solid ${crossed > 0.5 ? accent.red : accent.amber}`,
                borderRadius: 10,
                transform: `translateX(${(1 - pop) * -700}px)`,
                opacity: local < 0 ? 0 : 1,
                boxShadow: "0 12px 30px rgba(0,0,0,0.6)",
              }}
            >
              <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 64, color: crossed > 0.5 ? accent.red : accent.amber, width: 54 }}>{i + 1}</div>
              <div style={{ fontFamily: fonts.title, fontWeight: 800, fontSize: 52, color: "#fff", lineHeight: 1.05, textTransform: "uppercase", opacity: 1 - 0.45 * crossed }}>
                <CensoredText text={it} blur={1.2} />
              </div>
              <div style={{ position: "absolute", left: 20, right: 20, top: "50%", height: 9, background: accent.red, transformOrigin: "left", transform: `scaleX(${crossed}) rotate(-2deg)`, boxShadow: `0 0 16px ${accent.red}` }} />
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Cuenta regresiva: anillo que se vacía y reloj digital que corre de `hours`:00:00 a 0 en `dur` segundos.
export const Countdown: React.FC<{ hours: number; dur: number; label?: string }> = ({ hours, dur, label }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = interpolate(frame / fps, [0, dur], [0, 1], { extrapolateRight: "clamp", easing: Easing.in(Easing.quad) });
  const left = Math.max(0, hours * 3600 * (1 - p));
  const hh = String(Math.floor(left / 3600)).padStart(2, "0");
  const mm = String(Math.floor((left % 3600) / 60)).padStart(2, "0");
  const ss = String(Math.floor(left % 60)).padStart(2, "0");
  const pop = spring({ frame, fps, config: { damping: 12, stiffness: 180 } });
  const r = 190;
  const circ = 2 * Math.PI * r;
  const urgent = p > 0.75;
  const c = urgent ? accent.red : accent.amber;
  const beat = urgent ? 1 + 0.04 * Math.abs(Math.sin((frame / fps) * Math.PI * 3)) : 1;
  return (
    <AbsoluteFill style={{ alignItems: "center", pointerEvents: "none" }}>
      <div style={{ position: "absolute", top: 700, width: 460, height: 460, transform: `scale(${pop * beat})` }}>
        <svg width={460} height={460}>
          <circle cx={230} cy={230} r={r + 18} fill="rgba(10,10,10,0.82)" />
          <circle cx={230} cy={230} r={r} fill="none" stroke="rgba(255,255,255,0.12)" strokeWidth={20} />
          <circle cx={230} cy={230} r={r} fill="none" stroke={c} strokeWidth={20} strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={circ * p} transform="rotate(-90 230 230)" style={{ filter: `drop-shadow(0 0 12px ${c})` }} />
          {Array.from({ length: 12 }, (_, i) => (
            <line key={i} x1={230} y1={52} x2={230} y2={70} stroke="rgba(255,255,255,0.4)" strokeWidth={4} transform={`rotate(${i * 30} 230 230)`} />
          ))}
        </svg>
        <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
          <div style={{ fontFamily: fonts.mono, fontWeight: 700, fontSize: 74, color: c, letterSpacing: 2 }}>{`${hh}:${mm}:${ss}`}</div>
          {label && <div style={{ fontFamily: fonts.body, fontWeight: 800, fontSize: 28, color: "#fff", letterSpacing: 3, marginTop: 8 }}>{label}</div>}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Círculo que señala algo en la foto: oscurece el resto, dibuja el anillo y pone una etiqueta.
export const Spotlight: React.FC<{ x: number; y: number; r?: number; label?: string; color?: Accent }> = ({ x, y, r = 170, label, color = "amber" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = interpolate(frame, [0, 0.5 * fps], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const c = accent[color];
  const circ = 2 * Math.PI * r;
  const below = y + r + 120 < layout.safeBottom;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <AbsoluteFill style={{ background: `radial-gradient(circle at ${x}px ${y}px, transparent ${r}px, rgba(0,0,0,${0.55 * p}) ${r + 40}px)` }} />
      <svg width={1080} height={1920} style={{ position: "absolute" }}>
        <circle cx={x} cy={y} r={r} fill="none" stroke={c} strokeWidth={7} strokeDasharray={circ} strokeDashoffset={circ * (1 - p)} transform={`rotate(-90 ${x} ${y})`} style={{ filter: `drop-shadow(0 0 10px ${c})` }} />
      </svg>
      {label && (
        <div
          style={{
            position: "absolute",
            left: Math.min(Math.max(40, x - 260), 520),
            width: 520,
            top: below ? y + r + 24 : y - r - 90,
            textAlign: "center",
            opacity: interpolate(frame, [0.35 * fps, 0.6 * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
          }}
        >
          <span style={{ background: c, color: "#111", fontFamily: fonts.title, fontWeight: 900, fontSize: 40, padding: "6px 18px", borderRadius: 6, textTransform: "uppercase" }}>{label}</span>
        </div>
      )}
    </AbsoluteFill>
  );
};

// Brasas que suben y resplandor de incendio desde abajo.
export const Embers: React.FC<{ intensity?: number }> = ({ intensity = 1 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const n = Math.round(60 * intensity);
  const fadeIn = interpolate(frame, [0, 0.4 * fps], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ pointerEvents: "none", opacity: fadeIn }}>
      <AbsoluteFill style={{ background: `linear-gradient(0deg, rgba(255,90,30,${0.38 * intensity}), rgba(255,90,30,0) 55%)`, mixBlendMode: "screen" }} />
      <svg width={1080} height={1920}>
        {Array.from({ length: n }, (_, i) => {
          const life = 2.2 + random(`el-${i}`) * 2.5;
          const t = ((frame / fps + random(`eo-${i}`) * life) % life) / life;
          const x0 = random(`ex-${i}`) * 1080;
          const x = x0 + Math.sin(t * 6 + i) * 40;
          const y = 1950 - t * (900 + random(`ey-${i}`) * 900);
          const s = 2 + random(`es-${i}`) * 5;
          return <circle key={i} cx={x} cy={y} r={s} fill={i % 3 ? "#FFB347" : "#FF6A2B"} opacity={(1 - t) * 0.9} style={{ filter: "blur(1px)" }} />;
        })}
      </svg>
    </AbsoluteFill>
  );
};

// Viñeta roja que late (tensión).
export const RedPulse: React.FC<{ bpm?: number }> = ({ bpm = 70 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ph = ((frame / fps) * bpm) / 60;
  const beat = Math.exp(-((ph % 1) * 7)) + 0.6 * Math.exp(-(((ph + 0.72) % 1) * 9));
  const fadeIn = interpolate(frame, [0, 0.5 * fps], [0, 1], { extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ pointerEvents: "none", boxShadow: `inset 0 0 ${220 + 120 * beat}px rgba(200,20,10,${(0.35 + 0.35 * beat) * fadeIn})` }} />;
};

// Barra de progreso arriba: invita a quedarse hasta el final.
export const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", top: 0, left: 0, height: 10, width: `${(frame / durationInFrames) * 100}%`, background: `linear-gradient(90deg, ${accent.amber}, ${accent.red})`, boxShadow: `0 0 14px ${accent.red}` }} />
    </AbsoluteFill>
  );
};

// Transición de entrada de una escena. Devuelve el estilo para envolverla y un destello opcional.
export function transitionStyle(kind: Transition | undefined, frame: number): { style: React.CSSProperties; flash: number } {
  switch (kind) {
    case "whip": {
      const p = interpolate(frame, [0, 9], [1, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
      return { style: { transform: `translateX(${p * 420}px) scale(${1 + 0.08 * p})`, filter: p > 0.02 ? `blur(${p * 26}px)` : undefined }, flash: 0 };
    }
    case "zoom": {
      const p = interpolate(frame, [0, 12], [1, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
      return { style: { transform: `scale(${1 + 0.45 * p})`, filter: p > 0.02 ? `blur(${p * 18}px)` : undefined }, flash: 0 };
    }
    case "flash":
      return { style: {}, flash: interpolate(frame, [0, 10], [0.9, 0], { extrapolateRight: "clamp" }) };
    case "glitch": {
      const on = frame < 10;
      const dx = on ? (random(`g-${frame}`) - 0.5) * 80 : 0;
      return { style: on ? { transform: `translateX(${dx}px)`, filter: `hue-rotate(${random(`gh-${frame}`) * 90}deg) contrast(1.6)` } : {}, flash: on && frame % 3 === 0 ? 0.35 : 0 };
    }
    default: {
      const s = interpolate(frame, [0, 10], [1.035, 1], { extrapolateRight: "clamp" });
      return { style: { transform: `scale(${s})` }, flash: 0 };
    }
  }
}
