"""AG-18 · Operación Chariot, Saint-Nazaire (1942). Baja candidatas de Wikipedia / Wikimedia Commons a assets/candidatas/.

Después de revisar cada foto a ojo (personaje correcto, sin esvásticas visibles que disparen filtros),
las elegidas se copian a assets/ con nombre final y quedan registradas en assets/assets_metadata.json.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

USER_AGENT = "HistoricalShortsArchivalFetcher/1.0 (https://commons.wikimedia.org)"
OUT_DIR = Path("produccion/09_saint_nazaire/assets/candidatas")
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIKI_ARTICLES = [
    ("en", "St_Nazaire_Raid", "raid"),
    ("en", "HMS_Campbeltown_(I42)", "campbeltown"),
    ("en", "Normandie_dry_dock", "dique"),
    ("en", "German_battleship_Tirpitz", "tirpitz"),
    ("en", "German_battleship_Bismarck", "bismarck"),
    ("en", "Stephen_Halden_Beattie", "beattie"),
    ("en", "Robert_Ryder", "ryder"),
    ("en", "Augustus_Charles_Newman", "newman"),
    ("en", "Fairmile_B_motor_launch", "fairmile"),
    ("en", "Victoria_Cross", "vc"),
    ("fr", "Forme_Joubert", "joubert"),
    ("en", "Saint-Nazaire", "ciudad"),
]

COMMONS_QUERIES = {
    "raid": "St Nazaire raid 1942",
    "raid2": "Saint-Nazaire 1942 Campbeltown",
    "campbeltown": "HMS Campbeltown dock gate",
    "campbeltown2": "HMS Campbeltown 1940 destroyer",
    "commandos": "British commandos prisoners Saint-Nazaire",
    "chariot": "Operation Chariot",
    "tirpitz": "Tirpitz battleship Norway",
    "tirpitz2": "Schlachtschiff Tirpitz",
    "fairmile": "Fairmile B motor launch",
    "mtb74": "MGB 314 St Nazaire",
    "joubert": "Forme Joubert Saint-Nazaire",
    "dock": "Saint-Nazaire dry dock 1942",
    "searchlight": "German searchlight 1942 coast",
    "flak": "Flak Saint-Nazaire",
    "loire": "Loire estuary Saint-Nazaire aerial",
    "vc": "Victoria Cross medal",
    "convoy": "Atlantic convoy 1942",
    "beattie": "Stephen Beattie VC",
    "townclass": "Town-class destroyer 1940",
    "wreck": "Campbeltown wreck Saint-Nazaire",
}

meta = {}


def get(url: str) -> bytes:
    """Wikimedia responde 503 cuando se satura: reintenta con espera creciente."""
    for k in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as r:
                time.sleep(1.0)
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or k == 5:
                raise
            time.sleep(4 * (k + 1))
    raise RuntimeError(url)


def save(name: str, img_url: str, source: str, license_: str = "", artist: str = "") -> None:
    ext = ".png" if img_url.lower().split("?")[0].endswith(".png") else ".jpg"
    if (OUT_DIR / (name + ext)).exists():
        meta[name + ext] = {"source": source, "url": img_url, "license": license_, "artist": artist}
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

(OUT_DIR / "candidatas_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(meta)} candidatas en {OUT_DIR}")
