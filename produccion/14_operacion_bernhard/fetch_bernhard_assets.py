"""AG-22 · Operación Bernhard (1942). Baja candidatas de Wikipedia / Wikimedia Commons a assets/candidatas/.

Después de revisar cada foto a ojo (personaje correcto, sin esvásticas visibles que disparen filtros),
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
OUT_DIR = Path("produccion/14_operacion_bernhard/assets/candidatas")
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIKI_ARTICLES = [
    ("en", "Operation_Bernhard", "bernhard"),
    ("de", "Unternehmen_Bernhard", "bernhard_de"),
    ("en", "Bernhard_Krüger", "kruger"),
    ("de", "Bernhard_Krüger_(SS-Mitglied)", "kruger_de"),
    ("en", "Salomon_Smolianoff", "smolianoff"),
    ("de", "Salomon_Smolianoff", "smolianoff_de"),
    ("en", "Adolf_Burger", "burger"),
    ("en", "Sachsenhausen_concentration_camp", "sachsenhausen"),
    ("en", "Bank_of_England", "boe"),
    ("en", "Gran_Sasso_raid", "gransasso"),
    ("en", "Lake_Toplitz", "toplitz"),
    ("en", "Bank_of_England_£5_note", "fiver"),
    ("en", "White_note", "whitenote"),
]

COMMONS_QUERIES = {
    "forged": "Operation Bernhard forged note",
    "forged2": "Bernhard forgery pound note",
    "forged3": "counterfeit British pound Sachsenhausen",
    "white50": "Bank of England fifty pound white note",
    "white5": "Bank of England white fiver",
    "boe_bldg": "Bank of England building 1940s",
    "boe_bldg2": "Threadneedle Street Bank of England",
    "sachs_gate": "Sachsenhausen gate tower",
    "sachs_barracks": "Sachsenhausen barracks",
    "sachs_aerial": "Sachsenhausen aerial",
    "sachs_lib": "Sachsenhausen liberation 1945",
    "barbed": "barbed wire fence concentration camp memorial",
    "press": "intaglio printing press",
    "press2": "printing press 1940s",
    "engraver": "engraver at work 1940s",
    "watermark": "watermark banknote light",
    "london42": "London street 1942",
    "london_blitz": "London 1940 Bank junction",
    "he111": "Heinkel He 111 flight",
    "mussolini": "Gran Sasso raid Mussolini 1943",
    "toplitz": "Toplitzsee",
    "dollar": "1934 series 100 dollar note",
    "smolianoff": "Salomon Smolianoff",
    "burger": "Adolf Burger",
    # Segunda tanda, más precisa: las búsquedas genéricas de imprenta y grabador trajeron fotos modernas.
    "bundes_sachs": "Bundesarchiv KZ Sachsenhausen",
    "sachs_1938": "Sachsenhausen 1938",
    "sachs_tor": "Sachsenhausen Turm A",
    "gransasso": "Bundesarchiv Gran Sasso Mussolini",
    "gransasso2": "Mussolini Campo Imperatore 1943",
    "fed100": "1934 100 dollar Federal Reserve Note",
    "fed20": "1934 twenty dollar Federal Reserve Note",
    "threadneedle": "Threadneedle Street 1940",
    "boe_old": "Bank of England 1930s photograph",
    "cicero": "Elyesa Bazna Cicero",
    "lib_sachs": "Sachsenhausen Befreiung 1945",
    "redarmy45": "Soviet soldiers liberation camp April 1945",
}

META = OUT_DIR / "candidatas_metadata.json"
meta = json.loads(META.read_text(encoding="utf-8")) if META.exists() else {}


def get(url: str) -> bytes:
    """Commons responde 503/429 cuando hay muchas descargas seguidas: se reintenta con espera creciente."""
    for k in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            time.sleep(0.8)
            return data
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or k == 5:
                raise
            time.sleep(4 * (k + 1))
    raise RuntimeError("sin respuesta")


def save(name: str, img_url: str, source: str, license_: str = "", artist: str = "") -> None:
    ext = ".png" if img_url.lower().split("?")[0].endswith(".png") else ".jpg"
    if name + ext in meta:
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

META.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(meta)} candidatas en {OUT_DIR}")
