import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Grain, Vignette } from "../engine/Film";
import { accent, archivalFilter, fonts } from "../engine/theme";

// Portada del Short (1080×1920). El texto va entre y≈520 y y≈1400 para que también
// se lea en el recorte cuadrado que YouTube usa en la grilla del canal.
// Arriba el B-17 destrozado en la mira (tachada), abajo Stigler: «NO DISPARÓ» entre los dos.
export const BremenCover: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#0b0b0b" }}>
    <Img
      src={staticFile("06_cielo_bremen/assets/b17_damaged_tail.jpg")}
      style={{ position: "absolute", top: 0, left: 0, width: 1080, height: 1100, objectFit: "cover", objectPosition: "30% 50%", filter: `${archivalFilter} brightness(0.85)`, WebkitMaskImage: "linear-gradient(180deg, #000 70%, transparent 100%)" }}
    />
    <Img
      src={staticFile("06_cielo_bremen/assets/stigler.png")}
      style={{
        position: "absolute",
        left: 0,
        bottom: 0,
        width: 1080,
        height: 1000,
        objectFit: "cover",
        objectPosition: "50% 30%",
        filter: `${archivalFilter} brightness(0.9)`,
        WebkitMaskImage: "linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.6) 25%, #000 45%)",
      }}
    />
    <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.05) 18%, rgba(0,0,0,0.55) 38%, rgba(0,0,0,0.55) 62%, rgba(0,0,0,0.1) 78%, rgba(0,0,0,0.6) 100%)" }} />
    <Vignette strength={0.65} />

    {/* Mira tachada sobre la cola del bombardero */}
    <svg width={1080} height={1920} style={{ position: "absolute" }}>
      <g transform="translate(330, 300)" stroke={accent.red} strokeWidth={7} fill="none" opacity={0.95}>
        <circle r={150} strokeDasharray="26 16" />
        <circle r={46} />
        {[0, 90, 180, 270].map((a) => (
          <line key={a} x1={0} y1={-185} x2={0} y2={-70} transform={`rotate(${a})`} />
        ))}
        <line x1={-170} y1={-170} x2={170} y2={170} strokeWidth={16} />
      </g>
    </svg>

    <AbsoluteFill style={{ alignItems: "center", paddingTop: 520 }}>
      <div style={{ display: "flex", alignItems: "stretch", boxShadow: "0 8px 24px rgba(0,0,0,0.5)" }}>
        <div style={{ width: 10, background: accent.red }} />
        <div style={{ background: "#EFE8D6", color: "#1b1b1b", fontFamily: fonts.mono, fontWeight: 700, fontSize: 40, letterSpacing: 3, padding: "10px 22px 8px" }}>
          BREMEN · DICIEMBRE 1943
        </div>
      </div>

      <div style={{ marginTop: 36, fontFamily: fonts.title, fontWeight: 900, fontSize: 150, lineHeight: 0.9, color: "#fff", letterSpacing: -4, textShadow: "0 10px 40px rgba(0,0,0,0.95)" }}>
        NO
      </div>
      <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 196, lineHeight: 0.95, color: accent.amber, letterSpacing: -6, textShadow: "0 10px 50px rgba(0,0,0,0.95), 0 0 70px rgba(240,180,41,0.35)" }}>
        DISPARÓ
      </div>
      <div
        style={{
          marginTop: 26,
          fontFamily: fonts.title,
          fontWeight: 900,
          fontSize: 60,
          lineHeight: 1.05,
          color: accent.cream,
          textAlign: "center",
          padding: "0 90px",
          textShadow: "0 6px 30px rgba(0,0,0,0.95)",
        }}
      >
        EL AS ALEMÁN QUE <span style={{ color: accent.amber }}>SALVÓ</span> A SU ENEMIGO
      </div>
    </AbsoluteFill>
    <Grain opacity={0.14} />
  </AbsoluteFill>
);
