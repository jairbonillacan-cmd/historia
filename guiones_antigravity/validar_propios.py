"""Valida los 10 guiones propios de Antigravity (guiones_antigravity/) con las mismas reglas estrictas
de ESPECIFICACION_GUIONES.md y exporta los .txt listos para ElevenLabs v4 en guiones_antigravity/elevenlabs/.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
SECCIONES = [
    "## Locución — ElevenLabs v4",
    "## Guion de edición",
    "## Descripción y hashtags",
    "## Verificación histórica",
]
TAGS_OK = {"pause", "long pause", "serious", "calm", "tense", "slowly", "whispers", "breathes"}
ABREVIATURAS = re.compile(r"\b(EE\. ?UU\.?|URSS|a\.C\.|d\.C\.|km|Dr\.|Sr\.|etc\.)|%|°")


def extraer_locucion(md: str) -> str | None:
    m = re.search(r"## Locución — ElevenLabs v4\s*```text\s*\n(.*?)```", md, re.S)
    return m.group(1).strip() if m else None


def validar_archivo(ruta: Path) -> tuple[list[str], list[str], str | None, int, str]:
    errores, avisos = [], []
    md = ruta.read_text(encoding="utf-8")
    titulo = md.splitlines()[0].lstrip("# ").strip() if md else ""
    for s in SECCIONES:
        if s not in md:
            errores.append(f"falta sección «{s}»")
    texto = extraer_locucion(md)
    if texto is None:
        errores.append("no se encontró el bloque ```text de la locución")
        return errores, avisos, None, 0, titulo

    tags = re.findall(r"\[([^\]]+)\]", texto)
    malos = sorted({t for t in tags if t not in TAGS_OK})
    if malos:
        errores.append(f"etiquetas no permitidas: {malos}")
    if not 8 <= len(tags) <= 14:
        avisos.append(f"{len(tags)} etiquetas (recomendado 8–14)")
    if tags.count("long pause") < 2 or tags.count("pause") < 2:
        avisos.append("faltan pausas obligatorias (2× [long pause] y 2× [pause])")
    if not texto.startswith("["):
        avisos.append("la locución no empieza con una etiqueta de tono")

    limpio = re.sub(r"\[[^\]]+\]", " ", texto)
    palabras = len(re.findall(r"[\wÁÉÍÓÚÜÑáéíóúüñ]+", limpio))
    if not 460 <= palabras <= 500:
        errores.append(f"{palabras} palabras (debe ser estrictamente 460–500)")
    if re.search(r"\d", limpio):
        errores.append(f"dígitos en la locución: {sorted(set(re.findall(r'\S*\d\S*', limpio)))[:5]}")
    abrev = ABREVIATURAS.findall(limpio)
    if abrev:
        errores.append(f"abreviaturas/símbolos en la locución: {sorted(set(abrev))}")
    if re.search(r"[#*_`>|]", limpio):
        errores.append("markdown dentro de la locución")
    if not re.search(r"\b(vos|contámelo|contame|pensá|imaginá|ponete|fijate|mirá|decime)\b", limpio, re.I):
        avisos.append("no se detecta voseo")
    hashtags = re.findall(r"(?<!\w)#\w+", md.split("## Descripción y hashtags")[-1].split("## Verificación")[0])
    if len(hashtags) != 5:
        errores.append(f"{len(hashtags)} hashtags (deben ser 5)")
    return errores, avisos, texto, palabras, titulo


def main() -> None:
    archivos = sorted(DIR.glob("AG*.md"))
    out_dir = DIR / "elevenlabs"
    out_dir.mkdir(parents=True, exist_ok=True)
    ok, err = 0, 0
    for ruta in archivos:
        errores, avisos, texto, palabras, titulo = validar_archivo(ruta)
        codigo = ruta.name.split("_")[0]
        if errores or avisos:
            err += 1
            print(f"[FALLO] {codigo} ({palabras} pal.): " + "; ".join(errores + avisos))
        else:
            ok += 1
            print(f"[OK] {codigo} ({palabras} pal.): {titulo}")
            if texto:
                (out_dir / f"{codigo}.txt").write_text(texto + "\n", encoding="utf-8")
    print(f"\nResumen: {ok} OK · {err} con errores/avisos · Total: {len(archivos)}")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
