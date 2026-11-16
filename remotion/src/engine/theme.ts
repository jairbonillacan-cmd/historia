import { loadFont as loadMontserrat } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import { loadFont as loadCourier } from "@remotion/google-fonts/CourierPrime";
import type { Accent } from "./types";

export const W = 1080;
export const H = 1920;
export const FPS = 60;

export const fonts = {
  title: loadMontserrat("normal", { weights: ["700", "800", "900"], subsets: ["latin", "latin-ext"] }).fontFamily,
  body: loadInter("normal", { weights: ["500", "600", "700", "800"], subsets: ["latin", "latin-ext"] }).fontFamily,
  mono: loadCourier("normal", { weights: ["700"], subsets: ["latin", "latin-ext"] }).fontFamily,
};

export const accent: Record<Accent, string> = {
  amber: "#F0B429",
  red: "#E05A47",
  blue: "#60A5FA",
  cream: "#F5F2EB",
};

export const colors = {
  ocean: "#13202f",
  oceanDeep: "#0b141f",
  land: "#d8ccb0",
  landEdge: "#a8997a",
  grid: "rgba(245,242,235,0.06)",
  ink: "#0d0d0d",
  spoken: "#9AA0A6",
  bbox: "#3B82F6",
};

// Zonas verticales (1080×1920). Debajo de SAFE_BOTTOM no va texto: ahí está la UI de Shorts.
export const layout = {
  captionY: 330,
  ribbonY: 560,
  titleY: 760,
  titleLowY: 1290, // en mapas, para no tapar el centro
  statY: 1040,
  photoCaptionY: 1395,
  safeBottom: 1520,
};

// Grade de archivo: blanco y negro cálido, como película de época.
export const archivalFilter = "grayscale(1) sepia(0.32) contrast(1.12) brightness(0.92)";
