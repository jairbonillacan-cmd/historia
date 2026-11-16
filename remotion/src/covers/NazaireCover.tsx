import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Grain, Vignette } from "../engine/Film";
import { accent, archivalFilter, fonts } from "../engine/theme";

// Portada del Short (1080×1920). El texto va entre y≈520 y y≈1400 para que también
// se lea en el recorte cuadrado que YouTube usa en la grilla del canal.
// Arriba los alemanes sobre la proa del Campbeltown, abajo el barco clavado en el dique:
// «EL BARCO BOMBA» entre los dos y la carga marcada bajo sus pies.
export const NazaireCover: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#0b0b0b" }}>
    <Img
      src={staticFile("09_saint_nazaire/assets/campbeltown_proa.jpg")}
      style={{ position: "absolute", top: -170, left: 0, width: 1080, height: 1080, objectFit: "cover", objectPosition: "28% 40%", filter: `${archivalFilter} brightness(0.9)`, WebkitMaskImage: "linear-gradient(180deg, #000 70%, transparent 100%)" }}
    />
    <Img
      src={staticFile("09_saint_nazaire/assets/campbeltown_dique.jpg")}
      style={{
        position: "absolute",
        left: 0,
        bottom: 0,
        width: 1080,
        height: 1000,
        objectFit: "cover",
        objectPosition: "60% 50%",
        filter: `${archivalFilter} brightness(0.85)`,
        WebkitMaskImage: "linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.6) 25%, #000 45%)",
      }}
    />
    <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.05) 16%, rgba(0,0,0,0.6) 36%, rgba(0,0,0,0.6) 64%, rgba(0,0,0,0.1) 80%, rgba(0,0,0,0.6) 100%)" }} />
    <Vignette strength={0.65} />

    {/* La carga bajo la cubierta: caja roja punteada sobre el casco, con la mecha */}
    <svg width={1080} height={1920} style={{ position: "absolute" }}>
      <g stroke={accent.red} strokeWidth={7} fill="none" opacity={0.95}>
        <rect x={300} y={345} width={400} height={110} rx={8} strokeDasharray="24 14" fill="rgba(224,90,71,0.22)" />
        <path d="M700,400 Q800,400 840,330 T940,260" strokeWidth={5} strokeDasharray="6 10" />
      </g>
      <circle cx={940} cy={260} r={14} fill={accent.amber} />
      <circle cx={940} cy={260} r={34} fill="none" stroke={accent.amber} strokeWidth={4} opacity={0.6} />
    </svg>

    <AbsoluteFill style={{ alignItems: "center", paddingTop: 540 }}>
      <div style={{ display: "flex", alignItems: "stretch", boxShadow: "0 8px 24px rgba(0,0,0,0.5)" }}>
        <div style={{ width: 10, background: accent.red }} />
        <div style={{ background: "#EFE8D6", color: "#1b1b1b", fontFamily: fonts.mono, fontWeight: 700, fontSize: 40, letterSpacing: 3, padding: "10px 22px 8px" }}>
          SAINT-NAZAIRE · MARZO 1942
        </div>
      </div>

      <div style={{ marginTop: 36, fontFamily: fonts.title, fontWeight: 900, fontSize: 150, lineHeight: 0.9, color: "#fff", letterSpacing: -4, textShadow: "0 10px 40px rgba(0,0,0,0.95)" }}>
        EL BARCO
      </div>
      <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 210, lineHeight: 0.95, color: accent.red, letterSpacing: -6, textShadow: "0 10px 50px rgba(0,0,0,0.95), 0 0 70px rgba(224,90,71,0.35)" }}>
        BOMBA
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
        <span style={{ color: accent.amber }}>4.500 KG</span> BAJO SUS PIES… Y NADIE LO SABÍA
      </div>
    </AbsoluteFill>
    <Grain opacity={0.14} />
  </AbsoluteFill>
);
