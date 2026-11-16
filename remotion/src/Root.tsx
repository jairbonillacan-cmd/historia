import React from "react";
import { Composition, Still } from "remotion";
import { BremenCover } from "./covers/BremenCover";
import { CartagoCover } from "./covers/CartagoCover";
import { KielCover } from "./covers/KielCover";
import { KiskaCover } from "./covers/KiskaCover";
import { MersCover } from "./covers/MersCover";
import { MessinesCover } from "./covers/MessinesCover";
import { NazaireCover } from "./covers/NazaireCover";
import { ShortVideo } from "./engine/ShortVideo";
import { FPS, H, W } from "./engine/theme";
import type { VideoPlan } from "./engine/types";
import { bernhard } from "./videos/bernhard";
import { bremen } from "./videos/bremen";
import { cartago } from "./videos/cartago";
import { kiel } from "./videos/kiel";
import { kiska } from "./videos/kiska";
import { mers } from "./videos/mers";
import { messines } from "./videos/messines";
import { nazaire } from "./videos/nazaire";
import { scapa } from "./videos/scapa";

const videos: Record<string, VideoPlan> = {
  Kiska: kiska,
  Bremen: bremen,
  Mers: mers,
  Kiel: kiel,
  Messines: messines,
  Nazaire: nazaire,
  Scapa: scapa,
  Cartago: cartago,
  Bernhard: bernhard,
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
    <Still id="BremenPortada" component={BremenCover} width={W} height={H} />
    <Still id="MersPortada" component={MersCover} width={W} height={H} />
    <Still id="MessinesPortada" component={MessinesCover} width={W} height={H} />
    <Still id="KielPortada" component={KielCover} width={W} height={H} />
    <Still id="NazairePortada" component={NazaireCover} width={W} height={H} />
    <Still id="CartagoPortada" component={CartagoCover} width={W} height={H} />
  </>
);
