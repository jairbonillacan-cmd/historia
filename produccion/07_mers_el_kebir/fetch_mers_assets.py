"""AG-16 · Mers el-Kebir (1940). Baja candidatas de Wikipedia / Wikimedia Commons a assets/candidatas/.

Después de revisar cada foto a ojo (barco o personaje correcto, sin cuerpos ni esvásticas visibles),
las elegidas se copian a assets/ con nombre final y quedan registradas en assets/assets_metadata.json.
"""
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

USER_AGENT = "HistoricalShortsArchivalFetcher/1.0 (https://commons.wikimedia.org)"
OUT_DIR = Path("produccion/07_mers_el_kebir/assets/candidatas")
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIKI_ARTICLES = [
    ("en", "Attack_on_Mers-el-Kébir", "attack"),
    ("en", "François_Darlan", "darlan"),
    ("en", "Marcel-Bruno_Gensoul", "gensoul"),
    ("en", "James_Somerville", "somerville"),
    ("en", "French_battleship_Bretagne", "bretagne"),
    ("en", "French_battleship_Dunkerque", "dunkerque"),
    ("en", "French_battleship_Strasbourg", "strasbourg"),
    ("en", "French_battleship_Provence", "provence"),
    ("en", "HMS_Hood", "hood"),
    ("en", "Scuttling_of_the_French_fleet_at_Toulon", "toulon"),
    ("en", "Armistice_of_22_June_1940", "armistice"),
    ("en", "Cedric_Holland", "holland"),
]

COMMONS_QUERIES = {
    "mers": "Mers-el-Kebir 1940",
    "mers2": "Mers el Kebir attack battleship",
    "bretagne": "battleship Bretagne",
    "dunkerque": "Dunkerque battleship 1940",
    "strasbourg": "Strasbourg battleship",
    "hood": "HMS Hood 1940",
    "forceh": "Force H 1940",
    "churchill": "Winston Churchill 1940",
    "darlan": "Amiral Darlan",
    "toulon": "Toulon 1942 sabordage",
    "armistice": "Compiègne armistice 1940",
    "roosevelt": "Franklin Roosevelt 1940",
    "valiant": "HMS Valiant 1940 guns",
    "radio": "1940 radio operator navy",
}

meta = {}


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def save(name: str, img_url: str, source: str, license_: str = "", artist: str = "") -> None:
    ext = ".png" if img_url.lower().split("?")[0].endswith(".png") else ".jpg"
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
