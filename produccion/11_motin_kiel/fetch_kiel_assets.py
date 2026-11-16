"""AG-19 · Motín de Kiel (1918). Baja candidatas de Wikipedia / Wikimedia Commons a assets/candidatas/.

Después de revisar cada foto a ojo (personaje y hecho correctos, de la Primera Guerra Mundial),
las elegidas se copian a assets/ con nombre final y quedan registradas en assets/assets_metadata.json.
"""
import json
import re
import time
import sys
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

USER_AGENT = "HistoricalShortsArchivalFetcher/1.0 (https://commons.wikimedia.org)"
OUT_DIR = Path("produccion/11_motin_kiel/assets/candidatas")
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIKI_ARTICLES = [
    ("en", "Kiel_mutiny", "kiel_mutiny"),
    ("de", "Kieler_Matrosenaufstand", "matrosenaufstand"),
    ("en", "Wilhelm_II", "kaiser"),
    ("en", "Reinhard_Scheer", "scheer"),
    ("en", "Franz_von_Hipper", "hipper"),
    ("en", "SMS_Thüringen", "thuringen"),
    ("en", "SMS_Helgoland_(1909)", "helgoland"),
    ("en", "Battle_of_Jutland", "jutland"),
    ("en", "High_Seas_Fleet", "hochseeflotte"),
    ("en", "German_Revolution_of_1918–1919", "revolucion"),
    ("en", "Abdication_of_Wilhelm_II", "abdicacion"),
    ("en", "Armistice_of_11_November_1918", "armisticio"),
    ("en", "Naval_order_of_24_October_1918", "orden19"),
    ("en", "Wilhelmshaven", "wilhelmshaven"),
]

COMMONS_QUERIES = {
    "kiel_1918": "Kiel Matrosenaufstand 1918",
    "kiel_sailors": "Kiel November 1918 Matrosen",
    "soldatenrat": "Soldatenrat 1918 Matrosen",
    "revolution_berlin": "Novemberrevolution Berlin 1918",
    "revolution_berlin2": "Berlin 9 November 1918 Revolution",
    "heizer": "Heizer Kesselraum Kriegsschiff",
    "stokers": "stokers boiler room battleship coal",
    "hochseeflotte": "Hochseeflotte Schlachtschiffe",
    "helgoland_ship": "SMS Helgoland 1911 Linienschiff",
    "thuringen_ship": "SMS Thüringen Linienschiff",
    "jutland": "Skagerrakschlacht 1916",
    "wilhelmshaven": "Wilhelmshaven Kaiserliche Marine Hafen",
    "kaiser_exile": "Wilhelm II Eijsden 1918",
    "kaiser_doorn": "Wilhelm II Doorn",
    "scheer_photo": "Admiral Reinhard Scheer",
    "hipper_photo": "Admiral Franz von Hipper",
    "grand_fleet": "Grand Fleet 1918 battleships",
    "armistice": "Compiègne armistice 1918 wagon",
    "rote_fahne": "rote Fahne Kriegsschiff 1918",
    "noske_kiel": "Noske Kiel 1918",
    # segunda pasada: huecos del plan visual
    "frente_1918": "German soldiers 1918 western front retreat",
    "max_baden": "Prinz Max von Baden 1918",
    "kaiser_marine": "Kaiser Wilhelm II Marineuniform",
    "matrosen_deck": "Matrosen an Deck Linienschiff Kaiserliche Marine",
    "kesselraum": "Kesselraum Linienschiff",
}

# Con argumentos, solo corre esas búsquedas (p. ej. una segunda pasada) y suma al metadata existente.
ONLY = set(sys.argv[1:])
META_FILE = OUT_DIR / "candidatas_metadata.json"
meta = json.loads(META_FILE.read_text(encoding="utf-8")) if ONLY and META_FILE.exists() else {}


def get(url: str) -> bytes:
    """Commons responde 503/429 cuando se le pide rápido: reintenta con espera creciente."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                time.sleep(1.0)
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or attempt == 5:
                raise
            time.sleep(4 * (attempt + 1))
    raise RuntimeError("sin respuesta")


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
            date = re.sub(r"<[^>]+>", "", em.get("DateTimeOriginal", {}).get("value", ""))[:40]
            save(f"{name}_{k}", ii.get("thumburl") or ii["url"], "commons:" + p["title"], lic, (artist + " · " + date).strip(" ·"))
    except Exception as e:
        print(f"[WARN] {q} → {e}")

META_FILE.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(meta)} candidatas en {OUT_DIR}")
