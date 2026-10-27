import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

USER_AGENT = "HistoricalShortsArchivalFetcher/1.0 (https://commons.wikimedia.org)"
OUT_DIR = Path("produccion/05_isla_kiska/assets")
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIKI_ARTICLES = [
    ("en", "Operation_Cottage", "kiska_landing.jpg"),
    ("en", "Battle_of_Attu", "attu_battle.jpg"),
    ("en", "Masatomi_Kimura", "masatomi_kimura.jpg"),
    ("ja", "木村昌福", "masatomi_kimura_ja.jpg"),
    ("en", "USS_Abner_Read_(DD-526)", "abner_read.jpg"),
    ("en", "Japanese_occupation_of_Kiska", "kiska_japanese.jpg"),
    ("en", "Aleutian_Islands_campaign", "aleutians_campaign.jpg"),
    ("en", "Battle_of_the_Pips", "battle_pips.jpg"),
]

meta = {}

for lang, title, fname in WIKI_ARTICLES:
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query",
        "titles": title,
        "prop": "pageimages",
        "piprop": "original|thumbnail",
        "pithumbsize": "1280",
        "format": "json"
    })
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        for p in pages.values():
            img_url = p.get("thumbnail", {}).get("source") or p.get("original", {}).get("source")
            if img_url:
                req_i = urllib.request.Request(img_url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req_i, timeout=25) as ri:
                    b = ri.read()
                if len(b) > 8000:
                    (OUT_DIR / fname).write_bytes(b)
                    print(f"[OK Wiki] {fname} <- {lang}:{title} ({img_url.split('/')[-1]}) [{len(b)//1024} KB]")
                    meta[fname] = {"source": f"{lang}.wikipedia.org/wiki/{title}", "url": img_url}
    except Exception as e:
        print(f"[WARN Wiki] {lang}:{title} -> {e}")

COMMONS_QUERIES = {
    "b24_aleutians.jpg": ["B-24 Aleutians", "B-24 Kiska", "Consolidated B-24 Liberator Aleutian"],
    "uss_idaho_kiska.jpg": ["USS Idaho Kiska", "USS Idaho Attu", "USS Mississippi Kiska"],
    "kiska_bunkers.jpg": ["Kiska 1943 Japanese", "Kiska August 1943", "Operation Cottage Kiska"],
}

for fname, queries in COMMONS_QUERIES.items():
    found = False
    for q in queries:
        if found:
            break
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
        try:
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
                req_img = urllib.request.Request(dl_url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req_img, timeout=25) as r_img:
                    img_bytes = r_img.read()
                if len(img_bytes) > 12000:
                    (OUT_DIR / fname).write_bytes(img_bytes)
                    lic = ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "Public domain")
                    print(f"[OK Commons] {fname} <- {title} ({lic}) [{len(img_bytes)//1024} KB]")
                    meta[fname] = {"title": title, "license": lic, "url": dl_url}
                    found = True
                    break
        except Exception as e:
            print(f"[WARN Commons] {q} -> {e}")

(OUT_DIR / "assets_metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
