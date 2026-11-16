"""AG-21 · Scapa Flow (1919). Baja candidatas de Wikipedia / Wikimedia Commons a assets/candidatas/.

Después de revisar cada foto a ojo (personaje y hecho correctos, de 1919 y de esta flota, sin símbolos que disparen filtros),
las elegidas se copian a assets/ con nombre final y quedan registradas en assets/assets_metadata.json.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

USER_AGENT = "HistoricalShortsArchivalFetcher/1.0 (https://commons.wikimedia.org)"
OUT_DIR = Path("produccion/13_scapa_flow/assets/candidatas")
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIKI_ARTICLES = [
    ("en", "Scuttling_of_the_German_fleet_at_Scapa_Flow", "scuttling"),
    ("en", "Ludwig_von_Reuter", "reuter"),
    ("en", "Scapa_Flow", "scapa"),
    ("en", "SMS_Friedrich_der_Grosse_(1911)", "friedrich"),
    ("en", "SMS_Hindenburg", "hindenburg"),
    ("en", "SMS_Bayern_(1915)", "bayern"),
    ("en", "SMS_Emden_(1916)", "emden"),
    ("en", "Treaty_of_Versailles", "versailles"),
    ("en", "Sydney_Fremantle", "fremantle"),
    ("en", "SMS_Seydlitz", "seydlitz"),
    ("en", "Internment_of_the_German_fleet_at_Scapa_Flow", "internment"),
]

COMMONS_QUERIES = {
    "scuttle": "scuttling German fleet Scapa Flow 1919",
    "bayern": "SMS Bayern sinking Scapa Flow",
    "hindenburg": "SMS Hindenburg Scapa Flow sunk",
    "fleet_firth": "German High Seas Fleet Firth of Forth 1918 surrender",
    "interned": "German fleet interned Scapa Flow",
    "seydlitz": "SMS Seydlitz capsized Scapa Flow",
    "destroyer": "German destroyer beached Scapa Flow",
    "salvage": "Scapa Flow salvage German battleship raised",
    "reuter": "Ludwig von Reuter",
    "versailles": "Signing of peace Versailles 1919 Hall of Mirrors",
    "grand_fleet": "Grand Fleet battleships 1918",
    "lifeboats": "German sailors lifeboats Scapa Flow 1919",
    "hms_revenge": "HMS Revenge 1919",
    "orkney": "Scapa Flow Orkney 1919",
    "friedrich": "SMS Friedrich der Grosse",
}

META = OUT_DIR / "candidatas_metadata.json"
meta = json.loads(META.read_text(encoding="utf-8")) if META.exists() else {}


def get(url: str) -> bytes:
    """Wikimedia corta con 503/429 si se le pide rápido: reintenta con espera creciente."""
    for k in range(5):
        time.sleep(1.5)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or k == 4:
                raise
            time.sleep(8 * (k + 1))
    raise RuntimeError(url)


def save(name: str, img_url: str, source: str, license_: str = "", artist: str = "") -> None:
    ext = ".png" if img_url.lower().split("?")[0].endswith(".png") else ".jpg"
    if name + ext in meta and (OUT_DIR / (name + ext)).exists():
        return
    b = get(img_url)
    if len(b) < 15000:
        return
    (OUT_DIR / (name + ext)).write_bytes(b)
    meta[name + ext] = {"source": source, "url": img_url, "license": license_, "artist": artist}
    print(f"[OK] {name}{ext} ← {source} [{len(b)//1024} KB] {license_}")


for lang, title, name in WIKI_ARTICLES:
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "query", "titles": title, "prop": "pageimages", "piprop": "original|thumbnail", "pithumbsize": "1600", "format": "json"}
    )
    try:
        for p in json.loads(get(url))["query"]["pages"].values():
            src = p.get("thumbnail", {}).get("source") or p.get("original", {}).get("source")
            if src:
                save(name, src, f"{lang}.wikipedia.org/wiki/{title}")
            else:
                print(f"[--] {lang}:{title} sin imagen")
    except Exception as e:
        print(f"[WARN] {lang}:{title} → {e}")

for name, q in COMMONS_QUERIES.items():
    params = {
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"filetype:bitmap {q}",
        "gsrnamespace": "6", "gsrlimit": "6", "prop": "imageinfo", "iiprop": "url|extmetadata|mime", "iiurlwidth": "1600",
    }
    try:
        pages = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params))).get("query", {}).get("pages", {})
        for k, p in enumerate(sorted(pages.values(), key=lambda x: x.get("index", 0))):
            ii = p["imageinfo"][0]
            if ii.get("mime") not in ("image/jpeg", "image/png"):
                continue
            em = ii.get("extmetadata", {})
            lic = em.get("LicenseShortName", {}).get("value", "")
            artist = re.sub(r"<[^>]+>", "", em.get("Artist", {}).get("value", ""))[:80]
            save(f"{name}_{k}", ii.get("thumburl") or ii["url"], "commons:" + p["title"], lic, artist)
    except Exception as e:
        print(f"[WARN] {q} → {e}")

META.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(meta)} candidatas en {OUT_DIR}")
