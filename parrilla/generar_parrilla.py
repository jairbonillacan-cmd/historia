"""Genera la parrilla de publicación a partir de parrilla/temas.psv.

Asigna a cada tema una fecha y una franja (S1..S5) entre el 28/10/2026 y el 27/12/2026.
Los temas con fecha_fija (efemérides) se colocan en su día; el resto rellena los huecos en orden.

Salidas:
  parrilla/parrilla.csv  -> una fila por vídeo (id, fecha, franja, horas, eje, título, ángulo, ruta del guion)
  parrilla/PARRILLA.md   -> calendario legible por semanas
"""
from __future__ import annotations

import csv
import re
import unicodedata
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INICIO = date(2026, 10, 28)
FIN = date(2026, 12, 27)

FRANJAS = {
    "S1": {"eje": "Antigüedad", "art": "09:00", "utc6": "06:00"},
    "S2": {"eje": "Medieval, Moderna y siglo XIX", "art": "12:30", "utc6": "09:30"},
    "S3": {"eje": "América e Hispanoamérica", "art": "16:00", "utc6": "13:00"},
    "S4": {"eje": "Guerras mundiales (1914–1945)", "art": "19:00", "utc6": "16:00"},
    "S5": {"eje": "Guerra Fría y siglo XX (1945–1991)", "art": "21:00", "utc6": "18:00"},
}
DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]


def slugify(texto: str, max_len: int = 60) -> str:
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^a-zA-Z0-9]+", "-", texto.lower()).strip("-")
    return texto[:max_len].rstrip("-")


def main() -> None:
    fechas = [INICIO + timedelta(days=i) for i in range((FIN - INICIO).days + 1)]
    with open(ROOT / "parrilla" / "temas.psv", encoding="utf-8") as f:
        temas = list(csv.DictReader(f, delimiter="|"))

    filas = []
    for franja in FRANJAS:
        propios = [t for t in temas if t["eje"] == franja]
        assert len(propios) == len(fechas), f"{franja}: {len(propios)} temas para {len(fechas)} días"
        asignacion: dict[date, dict] = {}
        for t in propios:
            if t["fecha_fija"]:
                d = date.fromisoformat(t["fecha_fija"])
                assert d not in asignacion, f"{franja}: fecha fija duplicada {d}"
                asignacion[d] = t | {"efemeride": "sí"}
        libres = iter(t for t in propios if not t["fecha_fija"])
        for d in fechas:
            if d not in asignacion:
                asignacion[d] = next(libres) | {"efemeride": ""}
        for d, t in asignacion.items():
            vid = f"{d.isoformat()}_{franja}"
            filas.append({
                "id": vid,
                "fecha": d.isoformat(),
                "dia": DIAS[d.weekday()],
                "franja": franja,
                "hora_ART": FRANJAS[franja]["art"],
                "hora_UTC-6": FRANJAS[franja]["utc6"],
                "eje": FRANJAS[franja]["eje"],
                "efemeride": t["efemeride"],
                "titulo": t["titulo"],
                "angulo": t["angulo"],
                "guion": f"guiones/{d.isoformat()}/{franja}_{slugify(t['titulo'])}.md",
            })

    filas.sort(key=lambda r: (r["fecha"], r["franja"]))
    titulos = [r["titulo"] for r in filas]
    assert len(set(titulos)) == len(titulos), "Hay títulos duplicados"

    with open(ROOT / "parrilla" / "parrilla.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    md = [
        "# Parrilla de contenido — 28 oct → 27 dic 2026",
        "",
        f"**{len(filas)} Shorts** · 5 al día · 3 min (177–180 s) · locución con voseo rioplatense para ElevenLabs v4.",
        "",
        "| Franja | Hora ART (UTC-3) | Hora UTC-6 | Eje temático |",
        "|---|---|---|---|",
        *[f"| {k} | {v['art']} | {v['utc6']} | {v['eje']} |" for k, v in FRANJAS.items()],
        "",
        "> Cada franja tiene siempre una época distinta, así dos vídeos seguidos nunca son del mismo tema",
        "> (evita la fatiga temática detectada en el análisis de @cdmauro2010). ⭐ = efeméride del día.",
        "",
    ]
    semana_actual = None
    for r in filas:
        d = date.fromisoformat(r["fecha"])
        semana = (d - INICIO).days // 7 + 1
        if semana != semana_actual:
            semana_actual = semana
            fin_semana = min(INICIO + timedelta(days=semana * 7 - 1), FIN)
            ini_semana = INICIO + timedelta(days=(semana - 1) * 7)
            md += ["", f"## Semana {semana} · {ini_semana:%d/%m} – {fin_semana:%d/%m}", "",
                   "| Fecha | Franja | Hora ART | Título | Guion |", "|---|---|---|---|---|"]
        estrella = " ⭐" if r["efemeride"] else ""
        md.append(f"| {r['dia']} {d:%d/%m} | {r['franja']} | {r['hora_ART']} | {r['titulo']}{estrella} | [abrir]({'../' + r['guion']}) |")
    (ROOT / "parrilla" / "PARRILLA.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"OK: {len(filas)} vídeos, {len(fechas)} días")


if __name__ == "__main__":
    main()
