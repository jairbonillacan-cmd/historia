"""AG-20 · Operación Cartago (Copenhague, 1945). Baja candidatas de Wikipedia / Wikimedia Commons a assets/candidatas/.

Después de revisar cada foto a ojo (hecho correcto, sin esvásticas visibles que disparen filtros,
nada de cuerpos), las elegidas se copian a assets/ con nombre final y quedan registradas en assets/assets_metadata.json.
"""
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

USER_AGENT = "HistoricalShortsArchivalFetcher/1.0 (https://commons.wikimedia.org)"
OUT_DIR = Path("produccion/12_operacion_cartago/assets/candidatas")
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIKI_ARTICLES = [
    ("en", "Operation_Carthage", "carthage"),
    ("en", "Shellhuset", "shellhus"),
    ("da", "Shellhuset", "shellhus_da"),
    ("en", "Robert_Bateson", "bateson"),
    ("da", "Den_Franske_Skole", "skole_da"),
    ("en", "De_Havilland_Mosquito", "mosquito"),
    ("en", "Occupation_of_Denmark", "occupation"),
    ("en", "Danish_resistance_movement", "resistance"),
    ("en", "Frederiksberg", "frederiksberg"),
]

COMMONS_QUERIES = {
    "shellhus_burning": "Shellhuset 1945 bombing",
    "shellhus_ruin": "Shellhuset ruin Copenhagen",
    "shellhus_raid": "Shell House raid Copenhagen 21 March 1945",
    "franske_skole": "Den Franske Skole 1945 Frederiksberg",
    "jeanne_darc": "Institut Jeanne d'Arc Frederiksberg bombing",
    "mosquito_fb6": "Mosquito FB.VI 1944",
    "mosquito_low": "Mosquito low level attack",
    "mosquito_formation": "de Havilland Mosquito formation",
    "mosquito_crew": "Mosquito crew 1945",
    "mosquito_cockpit": "Mosquito cockpit",
    "mosquito_raid": "Mosquito raid Gestapo",
    "copenhagen_1945": "København 1945 befrielse",
    "copenhagen_occupation": "Copenhagen German occupation soldiers",
    "danish_resistance": "Danish resistance fighters 1945",
    "frihedsmuseet": "Frihedsmuseet modstandsbevægelsen",
    "bateson": "Robert Bateson RAF",
    "aarhus_raid": "Aarhus University Gestapo raid 1944",
    "vesterbro_1945": "Copenhagen 1945 street",
}

meta = {}


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def save(name: str, img_url: str, source: str, license_: str = "", artist: str = "", desc: str = "") -> None:
    ext = ".png" if img_url.lower().split("?")[0].endswith(".png") else ".jpg"
    b = get(img_url)
    if len(b) < 15000:
        return
    (OUT_DIR / (name + ext)).write_bytes(b)
    meta[name + ext] = {"source": source, "url": img_url, "license": license_, "artist": artist, "desc": desc}
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
            desc = re.sub(r"<[^>]+>", "", em.get("ImageDescription", {}).get("value", ""))[:160]
            save(f"{name}_{k}", ii.get("thumburl") or ii["url"], "commons:" + p["title"], lic, artist, desc)
    except Exception as e:
        print(f"[WARN] {q} → {e}")

(OUT_DIR / "candidatas_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(meta)} candidatas en {OUT_DIR}")
