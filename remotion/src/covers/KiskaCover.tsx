import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Fog, Grain, Vignette } from "../engine/Film";
import { accent, archivalFilter, fonts } from "../engine/theme";

// Portada del Short (1080×1920). El texto va entre y≈520 y y≈1400 para que también
// se lea en el recorte cuadrado que YouTube usa en la grilla del canal.
export const KiskaCover: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#0b0b0b" }}>
    <Img
      src={staticFile("05_isla_kiska/assets/hires/allied_landing.jpg")}
      style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "38% 50%", transform: "scale(1.08)", filter: `${archivalFilter} brightness(0.8)` }}
    />
    <Fog density={0.35} />
    <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0.15) 30%, rgba(0,0,0,0.2) 62%, rgba(0,0,0,0.85) 100%)" }} />
    <Vignette strength={0.8} />

    <AbsoluteFill style={{ alignItems: "center", paddingTop: 520 }}>
      <div style={{ display: "flex", alignItems: "stretch", boxShadow: "0 8px 24px rgba(0,0,0,0.5)" }}>
        <div style={{ width: 10, background: accent.red }} />
        <div style={{ background: "#EFE8D6", color: "#1b1b1b", fontFamily: fonts.mono, fontWeight: 700, fontSize: 40, letterSpacing: 3, padding: "10px 22px 8px" }}>
          KISKA · ALASKA · 1943
        </div>
      </div>

      <div style={{ marginTop: 50, fontFamily: fonts.title, fontWeight: 900, fontSize: 210, lineHeight: 0.9, color: accent.amber, letterSpacing: -6, textShadow: "0 10px 40px rgba(0,0,0,0.85)" }}>
        34.000
      </div>
      <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 84, lineHeight: 1, color: "#fff", letterSpacing: -1, textShadow: "0 6px 30px rgba(0,0,0,0.9)" }}>
        SOLDADOS
      </div>
      <div
        style={{
          marginTop: 34,
          fontFamily: fonts.title,
          fontWeight: 900,
          fontSize: 74,
          lineHeight: 1.05,
          color: accent.cream,
          textAlign: "center",
          padding: "0 80px",
          textShadow: "0 6px 30px rgba(0,0,0,0.9)",
        }}
      >
        CONTRA UNA ISLA <span style={{ color: accent.red }}>VACÍA</span>
      </div>

      <div style={{ marginTop: 60, padding: "16px 30px 14px", background: "rgba(12,12,12,0.85)", border: `3px solid ${accent.red}`, borderRadius: 12, textAlign: "center" }}>
        <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 96, lineHeight: 1, color: accent.red }}>0</div>
        <div style={{ fontFamily: fonts.body, fontWeight: 800, fontSize: 30, letterSpacing: 2, color: "#fff", marginTop: 4 }}>ENEMIGOS EN LA ISLA</div>
      </div>
    </AbsoluteFill>
    <Grain opacity={0.14} />
  </AbsoluteFill>
);
