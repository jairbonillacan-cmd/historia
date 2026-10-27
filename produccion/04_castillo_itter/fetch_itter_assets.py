import json
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "HistoricalShortsArchivalFetcher/1.0 (https://commons.wikimedia.org)"
OUT_DIR = Path("produccion/04_castillo_itter/assets")
OUT_DIR.mkdir(parents=True, exist_ok=True)

QUERIES = {
    "schloss_itter.jpg": ["Schloss Itter", "Castle Itter Tyrol"],
    "josef_gangl.jpg": ["Josef Gangl", "Major Josef Gangl"],
    "paul_reynaud.jpg": ["Paul Reynaud 1940", "Paul Reynaud portrait"],
    "edouard_daladier.jpg": ["Edouard Daladier", "Édouard Daladier portrait"],
    "jean_borotra.jpg": ["Jean Borotra tennis", "Jean Borotra"],
    "sherman_1945.jpg": ["M4 Sherman tank 1945 Germany", "M4 Sherman 12th Armored Division"],
    "pak_88mm.jpg": ["Bundesarchiv 8,8 cm Flak", "88mm gun Bundesarchiv 1944"],
    "us_reinforcements_1945.jpg": ["US Army Austria May 1945 tank infantry", "103rd Infantry Division Austria 1945"],
}

def search_and_download(filename: str, queries: list[str]):
    for q in queries:
        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": f"filetype:bitmap {q}",
            "gsrnamespace": "6",
            "gsrlimit": "6",
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|mime",
            "iiurlwidth": "1280",
        }
        url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            title = page.get("title", "")
            ii = (page.get("imageinfo") or [{}])[0]
            mime = ii.get("mime", "")
            if "jpeg" not in mime and "png" not in mime:
                continue
            dl_url = ii.get("thumburl") or ii.get("url")
            if not dl_url:
                continue
            ext = ii.get("extmetadata", {})
            lic = ext.get("LicenseShortName", {}).get("value", "Public domain")
            artist = ext.get("Artist", {}).get("value", "")
            try:
                req_img = urllib.request.Request(dl_url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req_img, timeout=25) as r_img:
                    img_bytes = r_img.read()
                if len(img_bytes) > 15000:
                    dest = OUT_DIR / filename
                    dest.write_bytes(img_bytes)
                    print(f"[OK] {filename} <- {title} ({lic}) [{len(img_bytes)//1024} KB]")
                    return {"file": filename, "title": title, "license": lic, "url": dl_url}
            except Exception as e:
                print(f"  [WARN] Failed {title}: {e}")
    print(f"[FAIL] Could not download {filename}")
    return None

meta = {}
for fname, qs in QUERIES.items():
    res = search_and_download(fname, qs)
    if res:
        meta[fname] = res

(OUT_DIR / "assets_metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
