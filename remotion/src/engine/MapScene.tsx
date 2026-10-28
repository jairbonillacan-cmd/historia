import React, { useMemo } from "react";
import { AbsoluteFill, Easing, interpolate, random, useCurrentFrame, useVideoConfig } from "remotion";
import { geoGraticule10, geoMercator, geoPath, geoInterpolate } from "d3-geo";
import { feature } from "topojson-client";
import type { Topology, GeometryCollection } from "topojson-specification";
import type { Feature, FeatureCollection, Geometry } from "geojson";
import countries50 from "world-atlas/countries-50m.json";
import aleutians from "../geo/aleutians_10m.json";
import { accent, colors, fonts, H, W } from "./theme";
import { Fog } from "./Film";
import type { MapArrow, MapCamera, MapMarker, Pt, Visual } from "./types";

type Props = Extract<Visual, { kind: "map" }>;

const COUNTRY_IDS = { usa: "840", canada: "124", japan: "392", germany: "276", uk: "826", sweden: "752", france: "250", algeria: "012", italy: "380" } as const;
// Solo dibujamos el Pacífico Norte, Europa y el norte de África; el resto del mundo es costo de render.
const VISIBLE_IDS = new Set([
  "840", "124", "392", "643", "156", "408", "410", "496", "158",
  "276", "826", "752", "578", "208", "528", "056", "250", "616", "372", "040", "756", "203", "246", "440", "428", "233", "442", "112", "724", "380", "348", "703", "804",
  "012", "504", "788", "434", "620", "818", "300", "792", "191", "705", "070", "008", "499", "807", "688", "642", "100", "376", "422", "760", "400", "196", "470",
]);
const MAP_CENTER_Y = 1010;

const topo = countries50 as unknown as Topology<{ countries: GeometryCollection }>;
const allCountries = (feature(topo, topo.objects.countries) as FeatureCollection).features.filter((f) => VISIBLE_IDS.has(String(f.id)));
const islands = aleutians as unknown as Feature<Geometry>;

export const MapScene: React.FC<Props> = ({ from, to, highlight = [], markers = [], arrows = [], fog = 0, crossfire }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const cam = useCamera(from, to ?? from, frame, durationInFrames);

  const projection = useMemo(
    () =>
      geoMercator()
        .rotate([-cam.center[0], 0])
        .center([0, cam.center[1]])
        .scale(cam.scale)
        .translate([W / 2, MAP_CENTER_Y])
        .clipExtent([[-50, -50], [W + 50, H + 50]]),
    [cam.center[0], cam.center[1], cam.scale],
  );
  const path = geoPath(projection);
  const project = (p: Pt) => projection(p) ?? [-999, -999];

  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse 90% 70% at 50% 55%, ${colors.ocean}, ${colors.oceanDeep})` }}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <path d={path(geoGraticule10()) ?? ""} fill="none" stroke={colors.grid} strokeWidth={1.2} />
        {allCountries.map((f) => (
          <path key={String(f.id)} d={path(f) ?? ""} fill={colors.land} stroke={colors.landEdge} strokeWidth={1} />
        ))}
        {highlight.map((h, i) => {
          const f = allCountries.find((c) => String(c.id) === COUNTRY_IDS[h.country]);
          const o = interpolate(frame, [6 + i * 8, 6 + i * 8 + 0.5 * fps], [0, 0.85], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return f ? <path key={h.country} d={path(f) ?? ""} fill={accent[h.color]} opacity={o} stroke="none" /> : null;
        })}
        <path d={path(islands) ?? ""} fill={colors.land} stroke={colors.landEdge} strokeWidth={1.2} />
        {highlight.some((h) => h.country === "usa") && (
          <path d={path(islands) ?? ""} fill={accent.blue} opacity={interpolate(frame, [6, 6 + 0.5 * fps], [0, 0.85], { extrapolateRight: "clamp" })} />
        )}
        {arrows.map((a, i) => (
          <Arrow key={i} arrow={a} project={project} frame={frame} fps={fps} />
        ))}
        {crossfire && <Crossfire at={project(crossfire)} frame={frame} />}
        {markers.map((m, i) => (
          <Marker key={i} marker={m} xy={project(m.at)} frame={frame} fps={fps} />
        ))}
      </svg>
      {fog > 0 && <Fog density={fog} />}
    </AbsoluteFill>
  );
};

function useCamera(a: MapCamera, b: MapCamera, frame: number, total: number): MapCamera {
  const p = interpolate(frame, [0, total], [0, 1], { easing: Easing.inOut(Easing.cubic), extrapolateRight: "clamp" });
  const center = geoInterpolate(a.center, b.center)(p) as Pt;
  const scale = Math.exp(Math.log(a.scale) + (Math.log(b.scale) - Math.log(a.scale)) * p);
  return { center, scale };
}

const Marker: React.FC<{ marker: MapMarker; xy: [number, number]; frame: number; fps: number }> = ({ marker, xy, frame, fps }) => {
  const start = (marker.appear ?? 0) * fps;
  const local = frame - start;
  if (local < 0) return null;
  const o = interpolate(local, [0, 8], [0, 1], { extrapolateRight: "clamp" });
  const color = accent[marker.color ?? "cream"];
  const pulse = (local % (1.2 * fps)) / (1.2 * fps);
  const [x, y] = xy;
  const right = (marker.side ?? "right") === "right";
  const labelW = marker.label.length * 21 + 34;
  return (
    <g opacity={o}>
      {marker.pulse !== false && <circle cx={x} cy={y} r={14 + pulse * 46} fill="none" stroke={color} strokeWidth={4} opacity={1 - pulse} />}
      <circle cx={x} cy={y} r={11} fill={color} stroke="#111" strokeWidth={3} />
      <g transform={`translate(${right ? x + 24 : x - 24 - labelW}, ${y - 24})`}>
        <rect width={labelW} height={48} rx={6} fill="rgba(12,12,12,0.85)" />
        <text x={17} y={34} fontFamily={fonts.body} fontWeight={800} fontSize={30} fill="#fff" letterSpacing={1}>
          {marker.label}
        </text>
      </g>
    </g>
  );
};

// Flecha que se dibuja sola; con `ships` además avanza un convoy por la ruta.
const Arrow: React.FC<{ arrow: MapArrow; project: (p: Pt) => [number, number]; frame: number; fps: number }> = ({ arrow, project, frame, fps }) => {
  const start = (arrow.appear ?? 0) * fps;
  const dur = (arrow.duration ?? 1.4) * fps;
  const p = interpolate(frame - start, [0, dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.quad) });
  if (p <= 0) return null;
  const pts = densify(arrow.path, project);
  const n = Math.max(2, Math.round(pts.length * p));
  const visible = pts.slice(0, n);
  const d = visible.map((q, i) => `${i ? "L" : "M"}${q[0].toFixed(1)},${q[1].toFixed(1)}`).join(" ");
  const color = accent[arrow.color ?? "red"];
  const tip = visible[visible.length - 1];
  const prev = visible[Math.max(0, visible.length - 4)];
  const ang = (Math.atan2(tip[1] - prev[1], tip[0] - prev[0]) * 180) / Math.PI;

  return (
    <g>
      <path d={d} fill="none" stroke="rgba(0,0,0,0.45)" strokeWidth={16} strokeLinecap="round" />
      <path d={d} fill="none" stroke={color} strokeWidth={9} strokeLinecap="round" strokeDasharray={arrow.ships ? "2 18" : undefined} />
      {arrow.ships ? (
        <g transform={`translate(${tip[0]},${tip[1]}) rotate(${ang}) scale(1.5)`}>
          {[0, 1, 2].map((k) => (
            <path key={k} d="M-22,-7 L14,-7 L24,0 L14,7 L-22,7 Z" transform={`translate(${-k * 40},${k % 2 ? 14 : -14})`} fill={color} stroke="#111" strokeWidth={2.5} />
          ))}
        </g>
      ) : (
        <path d="M-6,-18 L24,0 L-6,18 Z" transform={`translate(${tip[0]},${tip[1]}) rotate(${ang})`} fill={color} stroke="#111" strokeWidth={2} />
      )}
    </g>
  );
};

function densify(path: Pt[], project: (p: Pt) => [number, number]): [number, number][] {
  const out: [number, number][] = [];
  for (let i = 0; i < path.length - 1; i++) {
    const f = geoInterpolate(path[i], path[i + 1]);
    for (let k = 0; k < 24; k++) out.push(project(f(k / 24) as Pt));
  }
  out.push(project(path[path.length - 1]));
  return out;
}

// Trazadoras cruzándose: dos patrullas disparándose entre sí.
const Crossfire: React.FC<{ at: [number, number]; frame: number }> = ({ at, frame }) => {
  const shots = Array.from({ length: 7 }, (_, i) => i);
  return (
    <g>
      {shots.map((i) => {
        const k = Math.floor((frame + i * 5) / 9);
        const fromLeft = random(`side-${i}-${k}`) > 0.5;
        const y1 = at[1] - 60 + random(`y1-${i}-${k}`) * 120;
        const y2 = at[1] - 60 + random(`y2-${i}-${k}`) * 120;
        const x1 = at[0] + (fromLeft ? -170 : 170);
        const x2 = at[0] + (fromLeft ? 170 : -170);
        const t = ((frame + i * 5) % 9) / 9;
        const hx = x1 + (x2 - x1) * t;
        const hy = y1 + (y2 - y1) * t;
        const tx = x1 + (x2 - x1) * Math.max(0, t - 0.25);
        const ty = y1 + (y2 - y1) * Math.max(0, t - 0.25);
        return <line key={i} x1={tx} y1={ty} x2={hx} y2={hy} stroke={fromLeft ? accent.blue : accent.amber} strokeWidth={6} strokeLinecap="round" />;
      })}
      <circle cx={at[0] - 170} cy={at[1]} r={16} fill={accent.blue} stroke="#111" strokeWidth={3} />
      <circle cx={at[0] + 170} cy={at[1]} r={16} fill={accent.amber} stroke="#111" strokeWidth={3} />
      <text x={at[0] - 170} y={at[1] + 70} textAnchor="middle" fontFamily={fonts.body} fontWeight={800} fontSize={34} fill="#fff" stroke="#111" strokeWidth={6} paintOrder="stroke">
        EE. UU.
      </text>
      <text x={at[0] + 170} y={at[1] + 70} textAnchor="middle" fontFamily={fonts.body} fontWeight={800} fontSize={34} fill="#fff" stroke="#111" strokeWidth={6} paintOrder="stroke">
        CANADÁ
      </text>
    </g>
  );
};
