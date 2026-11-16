// Contrato de datos: timeline_chunks.json (generado por build_audio_and_timeline_*.py)
export type Word = {
  word: string;
  start: number;
  end: number;
  is_bbox: boolean;
  group_id: number;
};

export type Chunk = {
  index: number;
  scene_id: number;
  start: number;
  end: number;
  text: string;
  words: Word[];
};

export type Timeline = {
  total_duration: number;
  chunks: Chunk[];
};

// Capas que aparecen encima de cualquier escena. `at` = índice de cláusula en la que entra,
// `word` = palabra de esa cláusula (para clavarla en la palabra exacta), `delay` = segundos extra.
type When = { at?: number; word?: number; delay?: number };
export type Overlay = When &
  (
    | { kind: "ribbon"; text: string }
    | { kind: "stat"; value: number; prefix?: string; suffix?: string; label: string; color?: Accent; slot?: 0 | 1 | 2 }
    | { kind: "title"; text: string; color?: Accent; low?: boolean }
    | { kind: "caption"; text: string; source?: string }
    | { kind: "slam"; text: string; color?: Accent; y?: number; size?: number } // palabra gigante que golpea la pantalla
    | { kind: "reticle"; x?: number; y?: number; lock?: number } // mira de caza; `lock` = segundos hasta fijar el blanco
    | { kind: "impact"; strength?: number } // destello + sacudida de cámara
    | { kind: "stamp"; text: string; color?: Accent; y?: number; rotate?: number } // sello de goma que cae
    | { kind: "options"; items: string[]; times: number[]; crossAt?: number; title?: string } // lista que se tacha; tiempos en s
    | { kind: "countdown"; hours: number; dur: number; label?: string } // reloj que corre a cero en `dur` s
    | { kind: "spotlight"; x: number; y: number; r?: number; label?: string; color?: Accent } // círculo sobre la foto
    | { kind: "embers"; intensity?: number } // brasas e incendio
    | { kind: "redpulse"; bpm?: number } // viñeta roja que late
  );

// Entrada de escena: barrido con desenfoque, zoom de golpe, destello blanco o interferencia.
export type Transition = "whip" | "zoom" | "flash" | "glitch";

export type Accent = "amber" | "red" | "blue" | "cream";

export type Pt = [number, number]; // [lon, lat]

export type MapMarker = { at: Pt; label: string; color?: Accent; appear?: number; pulse?: boolean; side?: "left" | "right" };
export type MapArrow = { path: Pt[]; color?: Accent; appear?: number; duration?: number; ships?: boolean };
export type MapCamera = { center: Pt; scale: number };

export type Visual =
  | { kind: "photo"; src: string; focus?: [number, number]; zoom?: [number, number]; drift?: [number, number]; portrait?: boolean; fog?: number; flashes?: boolean; dim?: number }
  | {
      kind: "map";
      from: MapCamera;
      to?: MapCamera;
      highlight?: { country: "usa" | "canada" | "japan" | "germany" | "uk" | "sweden" | "france" | "algeria" | "italy" | "denmark"; color: Accent }[];
      markers?: MapMarker[];
      arrows?: MapArrow[];
      fog?: number;
      crossfire?: Pt;
    }
  | { kind: "radar"; blips: boolean }
  | { kind: "dilemma"; background: string; aAt: number; bAt: number; footerAt: number } // *At = índice de cláusula
  // Plano técnico del B-17 visto desde arriba; cada daño se marca a los `at` segundos de la escena.
  | { kind: "bomber"; title: string; marks: { part: BomberPart; label: string; at: number; color?: Accent; side?: "left" | "right" }[] }
  // Los dos aviones desde arriba sobre nubes o mar. `fighter`: dónde está el caza.
  | { kind: "escort"; fighter: "none" | "behind" | "approach" | "wing" | "break"; flak?: boolean; sea?: boolean; smoke?: boolean }
  // Cita escrita a máquina sobre papel, con sello.
  | { kind: "quote"; text: string; author: string; background: string; stamp?: string }
  // Dos personajes enfrentados.
  | { kind: "versus"; left: Fighter; right: Fighter }
  // Condecoración girando con rayos de luz.
  | { kind: "medal"; label: string }
  // Acorazados de perfil (NavalScenes): en el puerto, navegando o con banderas rojas. `smoke: false` = calderas apagadas.
  | { kind: "fleet"; mode: "port" | "sail" | "mutiny"; smoke?: boolean; night?: boolean; ships?: 1 | 2 | 3 | 4 }
  // Manómetro de calderas: la aguja cae de `from` a `to` atmósferas desde `dropAt` s durante `dropDur` s.
  | { kind: "boiler"; from: number; to: number; dropAt?: number; dropDur?: number; label?: string }
  // Línea de tiempo vertical; cada hito entra a los `at` segundos de la escena.
  | { kind: "timeline"; title?: string; events: { date: string; label: string; at: number; color?: Accent }[] }
  // Vuelo rasante sobre una ciudad (CityRaidScenes): `sea` sobre las olas, `spires` entre agujas de iglesia,
  // `pole` el ala toca una torre de luz a los `hitAt` s y el avión cae a los `crashAt` s,
  // `smoke` dos incendios y la mira se corre al equivocado a los `confuseAt` s.
  | { kind: "skyline"; stage: "sea" | "spires" | "pole" | "smoke"; hitAt?: number; crashAt?: number; confuseAt?: number }
  // Corte de un edificio de 6 pisos (CityRaidScenes): ficheros abajo, 30 prisioneros en el último piso.
  // `marks` resaltan un piso (1 = planta baja), `hitAt` bombas en los pisos bajos, `escapeAt` 18 prisioneros escapan,
  // `aroundAt` aparecen las casas y el hospital vecinos.
  | { kind: "shellhus"; marks?: { floor: number; label: string; at: number; color?: Accent }[]; hitAt?: number; escapeAt?: number; aroundAt?: number };

export type BomberPart = "nose" | "engine1" | "engine2" | "engine3" | "engine4" | "tail" | "waist" | "cockpit";
export type Fighter = { src: string; name: string; lines: string[]; color: Accent; focus?: [number, number] };

// Una entrada del plan: arranca en la cláusula `from` (o en su palabra `word`) y dura hasta la siguiente entrada.
export type PlanItem = {
  from: number;
  word?: number;
  transition?: Transition;
  visual: Visual;
  overlays?: Overlay[];
};

export type VideoPlan = {
  folder: string; // carpeta dentro de produccion/
  audio: string;
  timeline: Timeline;
  items: PlanItem[];
  endCta: { question: string; a: string; b: string; footer: string };
  progress?: boolean; // barra de progreso arriba
};
