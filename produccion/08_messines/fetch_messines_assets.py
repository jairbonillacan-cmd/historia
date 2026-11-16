"""AG-17 · Messines (1917). Baja candidatas de Wikipedia / Wikimedia Commons a assets/candidatas/.

Después de revisar cada foto a ojo (personaje y hecho correctos: Messines / Flandes 1917, nada de la Segunda Guerra ni fotos modernas equivocadas),
las elegidas se copian a assets/ con nombre final y quedan registradas en assets/assets_metadata.json.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

USER_AGENT = "HistoricalShortsArchivalFetcher/1.0 (https://commons.wikimedia.org)"
OUT_DIR = Path("produccion/08_messines/assets/candidatas")
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIKI_ARTICLES = [
    ("en", "Herbert_Plumer,_1st_Viscount_Plumer", "plumer"),
    ("en", "Battle_of_Messines_(1917)", "messines"),
    ("en", "Mines_on_the_first_day_of_the_Battle_of_Messines", "mines"),
    ("en", "Spanbroekmolen", "spanbroek"),
    ("en", "Lone_Tree_Crater", "lonetree"),
    ("en", "Hill_60_(Ypres)", "hill60"),
    ("en", "Tunnelling_companies_of_the_Royal_Engineers", "tunnellers"),
    ("en", "1st_Australian_Tunnelling_Company", "aus_tunnel"),
    ("en", "Mesen", "mesen"),
    ("en", "Wijtschate", "wytschaete"),
]

COMMONS_QUERIES = {
    "crater_1917": "Messines 1917 mine crater",
    "spanbroek": "Spanbroekmolen crater",
    "pool_peace": "Pool of Peace Spanbroekmolen",
    "ridge": "Messines Ridge 1917",
    "battle": "Battle of Messines June 1917",
    "ruins": "Messines ruins 1917",
    "wytschaete": "Wytschaete 1917",
    "tunnellers": "tunnelling company Royal Engineers 1917",
    "tunnel": "British tunnel mine 1916 Western Front",
    "geophone": "geophone listening tunnel First World War",
    "hill60": "Hill 60 Ypres 1917",
    "caterpillar": "Caterpillar crater Hill 60",
    "aus_tunnel": "Australian tunnellers 1917",
    "nz_tunnel": "New Zealand Tunnelling Company",
    "canada_tunnel": "Canadian tunnelling company 1916",
    "trench_flanders": "trench Flanders 1917 mud",
    "plumer": "General Plumer 1917",
    "explosion": "mine explosion Western Front 1916",
    "hawthorn": "Hawthorn Ridge mine explosion",
    "german_trench": "German trench Messines 1917",
    "soldiers_messines": "Messines June 1917 soldiers",
    "lightning": "lightning strike field Belgium",
}

META = OUT_DIR / "candidatas_metadata.json"
meta = json.loads(META.read_text(encoding="utf-8")) if META.exists() else {}


def get(url: str) -> bytes:
    """Commons responde 503/429 si se le pega seguido: pausa entre pedidos y reintentos con espera."""
    for attempt in range(5):
        time.sleep(1.0 + 4 * attempt)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or attempt == 4:
                raise


def save(name: str, img_url: str, source: str, license_: str = "", artist: str = "") -> None:
    ext = ".png" if img_url.lower().split("?")[0].endswith(".png") else ".jpg"
    if (OUT_DIR / (name + ext)).exists():
        return
    b = get(img_url)
    if len(b) < 15000:
        return
    (OUT_DIR / (name + ext)).write_bytes(b)
    meta[name + ext] = {"source": source, "url": img_url, "license": license_, "artist": artist}
    print(f"[OK] {name}{ext} ← {source} [{len(b)//1024} KB] {license_}")


# Con argumentos solo se repiten esas búsquedas (útil cuando Commons respondió 503 a algunas).
ONLY = set(sys.argv[1:])

for lang, title, name in WIKI_ARTICLES:
    if ONLY and name not in ONLY:
        continue
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
    if ONLY and name not in ONLY:
        continue
    params = {
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"filetype:bitmap {q}",
        "gsrnamespace": "6", "gsrlimit": "5", "prop": "imageinfo", "iiprop": "url|extmetadata|mime", "iiurlwidth": "1600",
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
