import React from "react";
import { maskWord, splitCensored } from "./censor";

// Texto con las palabras sensibles con símbolos y un desenfoque leve. `blur` en px; tiene que seguir leyéndose.
export const CensoredText: React.FC<{ text: string; blur: number }> = ({ text, blur }) => (
  <>
    {splitCensored(text).map((s, i) =>
      s.hit ? (
        <span key={i} style={{ filter: `blur(${blur}px)`, display: "inline-block" }}>
          {maskWord(s.text)}
        </span>
      ) : (
        <React.Fragment key={i}>{s.text}</React.Fragment>
      ),
    )}
  </>
);
