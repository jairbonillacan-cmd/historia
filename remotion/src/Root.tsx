import React from "react";
import { Composition, Still } from "remotion";
import { KiskaCover } from "./covers/KiskaCover";
import { ShortVideo } from "./engine/ShortVideo";
import { FPS, H, W } from "./engine/theme";
import type { VideoPlan } from "./engine/types";
import { bremen } from "./videos/bremen";
import { kiska } from "./videos/kiska";

const videos: Record<string, VideoPlan> = {
  Kiska: kiska,
  Bremen: bremen,
};

export const RemotionRoot: React.FC = () => (
  <>
    {Object.entries(videos).map(([id, plan]) => {
      // 0.6 s de cola para que el último sonido no quede cortado.
      const totalFrames = Math.ceil((plan.timeline.total_duration + 0.6) * FPS);
      return (
        <Composition
          key={id}
          id={id}
          component={ShortVideo}
          width={W}
          height={H}
          fps={FPS}
          durationInFrames={totalFrames}
          defaultProps={{ plan, fps: FPS, totalFrames }}
        />
      );
    })}
    <Still id="KiskaPortada" component={KiskaCover} width={W} height={H} />
  </>
);
