import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Grain, Vignette } from "../engine/Film";
import { accent, archivalFilter, fonts } from "../engine/theme";

const A = "07_mers_el_kebir/assets/";

// Portada del Short (1080×1920). El titular va entre y≈520 y y≈1400 para que también
// se lea en el recorte cuadrado que YouTube usa en la grilla del canal.
export const MersCover: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#0b0b0b" }}>
    {/* Fondo: el Bretagne en llamas desenfocado arriba y entero abajo, con luz de incendio */}
    <Img
      src={staticFile(A + "bretagne_burning.jpg")}
      style={{ position: "absolute", inset: -80, width: "calc(100% + 160px)", height: "calc(100% + 160px)", objectFit: "cover", filter: `${archivalFilter} blur(18px) brightness(0.45)` }}
    />
    <Img
      src={staticFile(A + "bretagne_burning.jpg")}
      style={{
        position: "absolute",
        left: -120,
        top: 1150,
        width: 1320,
        height: 914,
        objectFit: "cover",
        filter: `${archivalFilter} contrast(1.3) brightness(0.95)`,
        maskImage: "linear-gradient(180deg, transparent 0%, #000 22%)",
        WebkitMaskImage: "linear-gradient(180deg, transparent 0%, #000 22%)",
      }}
    />
    <AbsoluteFill style={{ background: "radial-gradient(ellipse 90% 40% at 45% 82%, rgba(255,80,20,0.6), rgba(255,80,20,0) 70%)", mixBlendMode: "screen" }} />
    <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.15) 40%, rgba(0,0,0,0) 70%, rgba(0,0,0,0.35) 100%)" }} />
    <Vignette strength={0.7} />

    {/* Churchill en tarjeta inclinada */}
    <div
      style={{
        position: "absolute",
        left: 250,
        top: 110,
        width: 580,
        height: 560,
        overflow: "hidden",
        border: `10px solid ${accent.cream}`,
        boxShadow: "0 30px 70px rgba(0,0,0,0.85)",
        transform: "rotate(-4deg)",
      }}
    >
      <Img src={staticFile(A + "churchill.jpg")} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "50% 18%", filter: `${archivalFilter} contrast(1.2)` }} />
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, padding: "10px 0 8px", background: "rgba(12,12,12,0.85)", textAlign: "center", fontFamily: fonts.title, fontWeight: 900, fontSize: 40, letterSpacing: 4, color: accent.cream }}>
        WINSTON CHURCHILL
      </div>
    </div>

    <AbsoluteFill style={{ alignItems: "center", paddingTop: 720 }}>
      <div style={{ display: "flex", alignItems: "stretch", boxShadow: "0 8px 24px rgba(0,0,0,0.5)" }}>
        <div style={{ width: 10, background: accent.red }} />
        <div style={{ background: "#EFE8D6", color: "#1b1b1b", fontFamily: fonts.mono, fontWeight: 700, fontSize: 38, letterSpacing: 3, padding: "10px 22px 8px" }}>3 JULIO 1940 · ARGELIA</div>
      </div>

      <div
        style={{
          marginTop: 26,
          fontFamily: fonts.title,
          fontWeight: 900,
          fontSize: 230,
          lineHeight: 0.88,
          color: "#fff",
          letterSpacing: -8,
          textShadow: "0 12px 40px rgba(0,0,0,0.9)",
        }}
      >
        ATACÓ
      </div>
      <div
        style={{
          marginTop: 6,
          padding: "6px 30px 10px",
          background: accent.red,
          transform: "rotate(-2deg)",
          fontFamily: fonts.title,
          fontWeight: 900,
          fontSize: 112,
          lineHeight: 1,
          color: "#fff",
          letterSpacing: -2,
          boxShadow: `0 0 50px ${accent.red}aa, 0 14px 30px rgba(0,0,0,0.6)`,
        }}
      >
        A SU ALIADO
      </div>

      <div style={{ marginTop: 56, display: "flex", alignItems: "center", gap: 26 }}>
        <div style={{ padding: "14px 28px 12px", background: "rgba(12,12,12,0.86)", border: `3px solid ${accent.amber}`, borderRadius: 12, textAlign: "center" }}>
          <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 92, lineHeight: 1, color: accent.amber }}>1.297</div>
          <div style={{ fontFamily: fonts.body, fontWeight: 800, fontSize: 26, letterSpacing: 2, color: "#fff", marginTop: 4 }}>MARINEROS FRANCESES</div>
        </div>
        <div style={{ fontFamily: fonts.title, fontWeight: 900, fontSize: 60, lineHeight: 1.05, color: accent.cream, textShadow: "0 6px 24px rgba(0,0,0,0.9)" }}>
          EN 10
          <br />
          MINUTOS
        </div>
      </div>
    </AbsoluteFill>

    {/* Sello sobre la foto */}
    <div
      style={{
        position: "absolute",
        left: 560,
        top: 470,
        padding: "8px 22px 4px",
        border: `8px double ${accent.red}`,
        borderRadius: 10,
        color: accent.red,
        fontFamily: fonts.title,
        fontWeight: 900,
        fontSize: 58,
        letterSpacing: 4,
        background: "rgba(10,10,10,0.55)",
        transform: "rotate(10deg)",
        textShadow: `0 0 20px ${accent.red}66`,
      }}
    >
      ¿TRAICIÓN?
    </div>
    <Grain opacity={0.14} />
  </AbsoluteFill>
);
