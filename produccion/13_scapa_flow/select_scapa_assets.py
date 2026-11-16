"""AG-21 · Scapa Flow (1919). Copia las fotos elegidas de assets/candidatas/ a assets/ y arma assets_metadata.json.

Revisadas a ojo en la hoja de contactos: todas son de la flota alemana de 1918-1919 (rendición en el Forth,
internamiento y hundimiento en Scapa Flow), de Reuter, de Fremantle o de Versalles. Sin esvásticas: la Marina
Imperial usaba la cruz de hierro, que no hace falta tapar. Descartadas: scapa.jpg (paisaje moderno),
scuttle_2 («Salvage at Scapa Flow», reflotamiento de años después) y scuttle_5 (el casco casi no se ve).

La licencia y el autor se piden a Commons en una sola consulta (el buscador de fetch_scapa_assets.py
corta con 503 si se le pide seguido).
Uso (desde la raíz del repo): python produccion/13_scapa_flow/select_scapa_assets.py
"""
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("produccion/13_scapa_flow/assets")
USER_AGENT = "HistoricalShortsArchivalFetcher/1.0 (https://commons.wikimedia.org)"

# final ← (candidata, archivo de Commons o artículo de Wikipedia cuya imagen principal se bajó)
CHOSEN = {
    "bayern_hundiendose.jpg": ("bayern_0.jpg", "File:SMS Bayern sinking (cropped).jpg"),
    "bayern_vertical.jpg": ("bayern_1.jpg", "File:SMS Bayern sinking.jpg"),
    "derfflinger_volcado.jpg": ("scuttle_3.jpg", "File:SMS Derfflinger scuttled.jpg"),
    "hindenburg_fondo.jpg": ("scuttle_4.jpg", "File:SMS Hindenburg scuttled.jpg"),
    "libro_reuter.jpg": ("scuttle_0.jpg", "File:Admiral Ludwig von Reuter Scapa Flow Grave of Imperial German Navy.jpg"),
    "oficiales_rendicion.jpg": ("fleet_firth_0.jpg", "File:The Surrender of the German High Seas Fleet, November 1918 Q19287A.jpg"),
    "rendicion_amanecer.jpg": ("fleet_firth_1.jpg", "File:The Surrender of the German High Seas Fleet, November 1918 Q19287.jpg"),
    "flota_forth.jpg": ("fleet_firth_2.jpg", "File:Ships of the surrendered German High Seas Fleet in the Forth, November 1918 RMG PW0908.jpg"),
    "flota_pears.jpg": ("fleet_firth_3.jpg", "File:The German Fleet at Anchor off Inchkeith, Firth of Forth - after the Surrender, 22nd November 1918 Art.IWMART1926.jpg"),
    "flota_wyllie.jpg": ("fleet_firth_4.jpg", "File:Ships of the surrendered German High Seas Fleet off Inchkeith, in the Forth, November 1918 RMG PW0909.jpg"),
    "grosser_kurfurst.jpg": ("fleet_firth_5.jpg", "File:The 'Grosser Kurfürst' and other units of the High Seas Fleet sailing to surrender, 21 November 1918 RMG PW0660.jpg"),
    "versalles_orpen.jpg": ("versailles_0.jpg", "File:Orpen, William (Sir) (RA) - The Signing of Peace in the Hall of Mirrors, Versailles, 28th June 1919 - Google Art Project.jpg"),
    "versalles_detalle.jpg": ("versailles_3.jpg", "File:William Orpen - The Signing of Peace in the Hall of Mirrors - Detail 2.jpg"),
    "reuter.jpg": ("reuter.jpg", "en:Ludwig_von_Reuter"),
    "fremantle.jpg": ("fremantle.jpg", "en:Sydney_Fremantle"),
    "friedrich.jpg": ("friedrich.jpg", "en:SMS_Friedrich_der_Grosse_(1911)"),
    "hindenburg_scapa.jpg": ("hindenburg.jpg", "en:SMS_Hindenburg"),
    "seydlitz.jpg": ("seydlitz.jpg", "en:SMS_Seydlitz"),
    "tratado_paz.jpg": ("versailles.jpg", "en:Treaty_of_Versailles"),
}


def api(host: str, params: dict) -> dict:
    """Vía curl: Wikimedia responde 503 a urllib aunque lleve el mismo User-Agent."""
    url = f"https://{host}/w/api.php?" + urllib.parse.urlencode({**params, "format": "json"})
    for k in range(3):
        r = subprocess.run(["curl", "-s", "-w", "\n%{http_code}", "-A", USER_AGENT, url], capture_output=True, check=True)
        body, code = r.stdout.rsplit(b"\n", 1)
        if code == b"200":
            return json.loads(body)
        time.sleep(10 * (k + 1))
    raise RuntimeError(f"{url} → {code.decode()}")


# Artículos → nombre del archivo de su imagen principal. Si Wikimedia no responde (corta por IP), las fotos
# se copian igual con su fuente y la licencia queda vacía: volver a correr el script para completarla.
articles = {v[1][3:]: final for final, v in CHOSEN.items() if v[1].startswith("en:")}
file_of: dict[str, str] = {}
by_title: dict[str, dict] = {}
try:
    pages = api("en.wikipedia.org", {"action": "query", "titles": "|".join(articles), "prop": "pageimages", "piprop": "name", "redirects": 1})["query"]
    norm = {n["to"]: n["from"] for n in pages.get("normalized", []) + pages.get("redirects", [])}
    for p in pages["pages"].values():
        title = p["title"]
        while title in norm:
            title = norm[title]
        file_of[articles[title.replace(" ", "_")]] = "File:" + p["pageimage"]
except RuntimeError as e:
    print(f"[WARN] {e}")

titles = {final: (file_of.get(final) or v[1]) for final, v in CHOSEN.items()}
try:
    info = api("commons.wikimedia.org", {"action": "query", "titles": "|".join(t for t in titles.values() if t.startswith("File:")), "prop": "imageinfo", "iiprop": "url|extmetadata"})["query"]
    cnorm = {n["to"]: n["from"] for n in info.get("normalized", [])}
    for p in info["pages"].values():
        by_title[cnorm.get(p["title"], p["title"])] = p
except RuntimeError as e:
    print(f"[WARN] {e}")
# Las que no están en Commons son archivos locales de Wikipedia (p. ej. el retrato de Reuter, PD-US).
local = [t for t in titles.values() if t.startswith("File:") and "imageinfo" not in by_title.get(t, {})]
if local:
    try:
        info = api("en.wikipedia.org", {"action": "query", "titles": "|".join(local), "prop": "imageinfo", "iiprop": "url|extmetadata"})["query"]
        cnorm = {n["to"]: n["from"] for n in info.get("normalized", [])}
        for p in info["pages"].values():
            by_title[cnorm.get(p["title"], p["title"])] = p
    except RuntimeError as e:
        print(f"[WARN] {e}")

meta = {}
for final, (cand, origin) in CHOSEN.items():
    shutil.copyfile(BASE / "candidatas" / cand, BASE / final)
    p = by_title.get(titles[final], {})
    ii = (p.get("imageinfo") or [{}])[0]
    em = ii.get("extmetadata", {})
    meta[final] = {
        "source": ("en.wikipedia.org/wiki/" + origin[3:] + (" · commons:" + titles[final] if final in file_of else "") if origin.startswith("en:") else "commons:" + titles[final]),
        "url": ii.get("descriptionurl", ""),
        "license": em.get("LicenseShortName", {}).get("value", ""),
        "artist": " ".join(re.sub(r"<[^>]+>", "", em.get("Artist", {}).get("value", "")).split())[:80],
    }
    print(f"{final:26} {meta[final]['license']:22} {meta[final]['artist'][:40]}")

(BASE / "assets_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(meta)} fotos → {BASE / 'assets_metadata.json'}")
