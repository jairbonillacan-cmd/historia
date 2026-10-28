import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Grain, Vignette } from "../engine/Film";
import { accent, archivalFilter, fonts } from "../engine/theme";

// Portada del Short (1080×1920). El texto va entre y≈520 y y≈1400 para que también
// se lea en el recorte cuadrado que YouTube usa en la grilla del canal.
// Arriba el Mosquito con la mira fija, abajo el colegio en llamas: «UN ROCE» entre los dos.
export const CartagoCover: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#0b0b0b" }}>
    <Img
      src={staticFile("12_operacion_cartago/assets/mosquito_eg_t.jpg")}
      style={{ position: "absolute", top: -240, left: 0, width: 1080, height: 1180, objectFit: "cover", objectPosition: "62% 50%", filter: `${archivalFilter} brightness(0.8)`, WebkitMaskImage: "linear-gradient(180deg, #000 70%, transparent 100%)" }}
    />
    <Img
      src={staticFile("12_operacion_cartago/assets/colegio_llamas.jpg")}
      style={{
        position: "absolute",
        left: 0,
        bottom: 0,
        width: 1080,
        height: 1060,
        objectFit: "cover",
        objectPosition: "58% 45%",
        filter: `${archivalFilter} brightness(0.9)`,
        WebkitMaskImage: "linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.6) 22%, #000 42%)",
      }}
    />
    <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.05) 18%, rgba(0,0,0,0.55) 38%, rgba(0,0,0,0.55) 62%, rgba(0,0,0,0.1) 80%, rgba(0,0,0,0.6) 100%)" }} />
    {/* resplandor del incendio */}
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 40% 85%, rgba(224,90,71,0.32), transparent 55%)" }} />
    <Vignette strength={0.65} />

    {/* Mira fija sobre el Mosquito */}
    <svg width={1080} height={1920} style={{ position: "absolute" }}>
      <g transform="translate(730, 330)" stroke={accent.red} strokeWidth={7} fill="none" opacity={0.95}>
        <circle r={150} strokeDasharray="26 16" />
        <circle r={46} />
        {[0, 90, 180, 270].map((a) => (
          <line key={a} x1={0} y1={-185} x2={0} y2={-70} transform={`rotate(${a})`} />
        ))}
      </g>
    </svg>

    <AbsoluteFill style={{ alignItems: "center", paddingTop: 520 }}>
      <div style={{ display: "flex", alignItems: "stretch", boxShadow: "0 8px 24px rgba(0,0,0,0.5)" }}>
        <div style={{ width: 10, background: accent.red }} />
        <div style={{ background: "#EFE8D6", color: "#1b1b1b", fontFamily: fonts.mono, fontWeight: 700, fontSize: 40, letterSpacing: 3, padding: "10px 22px 8px" }}>
          COPENHAGUE · MARZO 1945
        </div>
      </div>

      <div style={{ marginTop: 36, fontFamily: fonts.title, fontWeight: 900, fontSize: 150, lineHeight: 0.9, color: "#fff", letterSpacing: -4, textShadow: "0 10px 40px rgba(0,0,0,0.95)" }}>
        UN ROCE
      </div>
      <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 178, lineHeight: 0.95, color: accent.red, letterSpacing: -6, textShadow: "0 10px 50px rgba(0,0,0,0.95), 0 0 70px rgba(224,90,71,0.35)" }}>
        FATAL
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
        EL ATAQUE <span style={{ color: accent.amber }}>PERFECTO</span> QUE CAYÓ SOBRE UN COLEGIO
      </div>
    </AbsoluteFill>
    <Grain opacity={0.14} />
  </AbsoluteFill>
);
