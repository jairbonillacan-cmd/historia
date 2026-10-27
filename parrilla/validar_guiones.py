"""Valida los guiones y exporta las locuciones listas para ElevenLabs v4.

Uso:
  python parrilla/validar_guiones.py                 # valida todos los guiones existentes y exporta
  python parrilla/validar_guiones.py --franja S3     # solo una franja
  python parrilla/validar_guiones.py --desde 2026-11-01 --hasta 2026-11-15
  python parrilla/validar_guiones.py --solo-validar  # no escribe archivos .txt

Exporta cada locución a elevenlabs/AAAA-MM-DD/Sx.txt (texto listo para pegar o enviar por API)
y genera parrilla/ESTADO.md con el estado de cada vídeo.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECCIONES = ["## Locución — ElevenLabs v4", "## Guion de edición", "## Descripción y hashtags", "## Verificación histórica"]
TAGS_OK = {"pause", "long pause", "serious", "calm", "tense", "slowly", "whispers", "breathes"}
ABREVIATURAS = re.compile(r"\b(EE\. ?UU\.?|URSS|a\.C\.|d\.C\.|km|Dr\.|Sr\.|etc\.)|%|°")
MESES = "enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre"
EMPIEZA_CON_FECHA = re.compile(
    rf"^((año|siglo|otoño|primavera|verano|invierno|mil|{MESES})\b|[a-záéíóúñ ]{{0,40}}\bde ({MESES})\b)")


def extraer_locucion(md: str) -> str | None:
    m = re.search(r"## Locución — ElevenLabs v4\s*```text\s*\n(.*?)```", md, re.S)
    return m.group(1).strip() if m else None


def validar(fila: dict) -> tuple[list[str], list[str], str | None, int]:
    errores, avisos = [], []
    ruta = ROOT / fila["guion"]
    if not ruta.exists():
        return ["falta el archivo"], [], None, 0
    md = ruta.read_text(encoding="utf-8")
    primera = md.splitlines()[0].lstrip("# ").strip() if md else ""
    if primera != fila["titulo"]:
        errores.append(f"título distinto a la parrilla: «{primera}»")
    for s in SECCIONES:
        if s not in md:
            errores.append(f"falta sección «{s}»")
    texto = extraer_locucion(md)
    if texto is None:
        errores.append("no se encontró el bloque ```text de la locución")
        return errores, avisos, None, 0

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
    if not 440 <= palabras <= 520:
        errores.append(f"{palabras} palabras (debe ser 460–500)")
    elif not 460 <= palabras <= 500:
        avisos.append(f"{palabras} palabras (objetivo 460–500)")
    if re.search(r"\d", limpio):
        errores.append(f"dígitos en la locución: {sorted(set(re.findall(r'\S*\d\S*', limpio)))[:5]}")
    abrev = ABREVIATURAS.findall(limpio)
    if abrev:
        errores.append(f"abreviaturas/símbolos en la locución: {sorted(set(abrev))}")
    if re.search(r"[#*_`>|]", limpio):
        errores.append("markdown dentro de la locución")
    if not re.search(r"\b(vos|contámelo|contame|pensá|imaginá|ponete|fijate|mirá|decime|dejá|escribí|defendé)\b", limpio, re.I):
        avisos.append("no se detecta voseo")

    # Variedad: tipo de gancho y frase de cierre asignados en la parrilla
    gancho = fila.get("gancho", "")
    m = re.search(r"\|\s*Tipo de gancho\s*\|\s*([^|\n]+)\|", md)
    if not m:
        avisos.append("falta la fila «Tipo de gancho» en la ficha")
    elif gancho and gancho not in m.group(1).upper():
        avisos.append(f"tipo de gancho «{m.group(1).strip()}» distinto del asignado «{gancho}»")
    primera_frase = re.split(r"[.?!:]", limpio.strip(), maxsplit=1)[0].strip().lower()
    if gancho and gancho != "FECHA" and EMPIEZA_CON_FECHA.match(primera_frase):
        errores.append(f"empieza con fecha pero el gancho asignado es {gancho}: «{primera_frase[:60]}»")
    cierre = fila.get("cierre", "")
    if cierre and not limpio.strip().endswith(cierre):
        errores.append(f"la última frase debe ser «{cierre}»")
    hashtags = re.findall(r"(?<!\w)#\w+", md.split("## Descripción y hashtags")[-1].split("## Verificación")[0])
    if len(hashtags) != 5:
        avisos.append(f"{len(hashtags)} hashtags (deben ser 5)")
    return errores, avisos, texto, palabras


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--franja")
    ap.add_argument("--desde")
    ap.add_argument("--hasta")
    ap.add_argument("--solo-validar", action="store_true")
    args = ap.parse_args()

    with open(ROOT / "parrilla" / "parrilla.csv", encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f))
    sel = [r for r in filas
           if (not args.franja or r["franja"] == args.franja)
           and (not args.desde or r["fecha"] >= args.desde)
           and (not args.hasta or r["fecha"] <= args.hasta)]

    estado, n_ok, n_err, n_falta = [], 0, 0, 0
    for r in sel:
        errores, avisos, texto, palabras = validar(r)
        if errores == ["falta el archivo"]:
            n_falta += 1
            estado.append((r, "⬜ pendiente", ""))
            continue
        if errores:
            n_err += 1
            print(f"✗ {r['id']}: " + "; ".join(errores + avisos))
            estado.append((r, "❌ con errores", "; ".join(errores)))
        else:
            n_ok += 1
            if avisos:
                print(f"~ {r['id']}: " + "; ".join(avisos))
            estado.append((r, f"✅ {palabras} pal.", "; ".join(avisos)))
        if texto and not errores and not args.solo_validar:
            out = ROOT / "elevenlabs" / r["fecha"] / f"{r['franja']}.txt"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(texto + "\n", encoding="utf-8")

    print(f"\nOK: {n_ok} · con errores: {n_err} · pendientes: {n_falta} · total: {len(sel)}")
    if not args.solo_validar and not (args.franja or args.desde or args.hasta):
        lineas = ["# Estado de los guiones", "", f"OK: {n_ok} · con errores: {n_err} · pendientes: {n_falta}", "",
                  "| ID | Título | Estado | Notas |", "|---|---|---|---|"]
        lineas += [f"| {r['id']} | [{r['titulo']}](../{r['guion']}) | {e} | {n} |" for r, e, n in estado]
        (ROOT / "parrilla" / "ESTADO.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
