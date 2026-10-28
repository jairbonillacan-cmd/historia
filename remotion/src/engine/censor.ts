// Censura de palabras sensibles para no disparar filtros de monetización ni de alcance.
// En pantalla la palabra lleva símbolos en las vocales y un desenfoque leve (maskWord + CensoredText),
// y en el audio se silencia la segunda mitad de la palabra (scripts/mute.ts usa esta misma lista).
// Solo lo grave: heridos, disparos, bombas, guerra, etc. quedan sin censura.
// Cada entrada es la raíz de la palabra: «muert» cubre muerto, muertos, muerte.
const STEMS = [
  "muert",
  "muer(e|en)",
  "mur(ió|ieron)",
  "mat(ar|an|ó|aron|anza)",
  "asesin",
  "masacr",
  "suicid",
  "carnicer",
  "sangr",
  "cadáver",
  "ejecut",
  "tortur",
  "nazi",
  "fusil(a|an|ar|aron|ado|ados|amiento)",
  "paredón",
  "rematar",
];

const WORD = new RegExp(`(?<![\\p{L}])(${STEMS.join("|")})[\\p{L}]*`, "giu");

export type Segment = { text: string; hit: boolean };

// Parte un texto en tramos normales y tramos censurados.
export function splitCensored(text: string): Segment[] {
  const out: Segment[] = [];
  let last = 0;
  for (const m of text.matchAll(WORD)) {
    const i = m.index ?? 0;
    if (i > last) out.push({ text: text.slice(last, i), hit: false });
    out.push({ text: m[0], hit: true });
    last = i + m[0].length;
  }
  if (last < text.length) out.push({ text: text.slice(last), hit: false });
  return out;
}

export function isCensored(word: string): boolean {
  return splitCensored(word).some((s) => s.hit);
}

const SYMBOLS = "*$#";
const VOWEL = /[aeiouáéíóúü]/i;

// Las vocales (salvo la inicial) pasan a símbolos y las consonantes quedan, así se sigue leyendo:
// «muertos» → «m*$rt#s», «MASACRE» → «M*S$CR#».
export function maskWord(word: string): string {
  let n = 0;
  return [...word].map((c, i) => (i > 0 && VOWEL.test(c) ? SYMBOLS[n++ % SYMBOLS.length] : c)).join("");
}
