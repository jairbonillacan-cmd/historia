import os
import sys
import json
import html
import re
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ASSETS_DIR = "produccion/03_operacion_tigre/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)
HEADERS = {"User-Agent": "HistoricalShortsArchivalFetcher/1.0 (https://commons.wikimedia.org)"}

def clean_html(raw: str) -> str:
    text = re.sub(r"<[^>]+>", "", raw or "")
    return html.unescape(text).strip()

QUERIES = {
    "slapton_sands.jpg": "Slapton Sands Devon beach",
    "eisenhower_1944.jpg": "Dwight D. Eisenhower 1944",
    "utah_beach_1944.jpg": "Utah Beach landing June 1944",
    "hms_hawkins.jpg": "HMS Hawkins cruiser",
    "lst_convoy_1944.jpg": "USS LST 1944 landing ship tank",
    "lst_burning.jpg": "LST burning 1944 OR LST-507 OR LST-531 OR Exercise Tiger",
    "s_boot_1944.jpg": "Schnellboot S-Boot Kriegsmarine",
    "sherman_slapton.jpg": "Exercise Tiger Sherman tank Slapton Sands",
}

manifest = {}

for out_name, query in QUERIES.items():
    params = urllib.parse.urlencode({
        "action": "query",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": "6",
        "gsrlimit": "8",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|dimensions",
        "iiurlwidth": "1280",
        "format": "json",
    })
    url = f"https://commons.wikimedia.org/w/api.php?{params}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    pages = data.get("query", {}).get("pages", {})
    downloaded = False
    for page in pages.values():
        iinfo = (page.get("imageinfo") or [{}])[0]
        dl_url = iinfo.get("thumburl") or iinfo.get("url")
        if not dl_url or dl_url.lower().endswith(".svg") or dl_url.lower().endswith(".tif") or dl_url.lower().endswith(".gif"):
            continue
        meta = iinfo.get("extmetadata", {})
        lic = clean_html(meta.get("LicenseShortName", {}).get("value", "Public domain"))
        artist = clean_html(meta.get("Artist", {}).get("value", "Archivo Histórico"))
        artist = re.sub(r"\s+", " ", artist)[:40]
        try:
            img_req = urllib.request.Request(dl_url, headers=HEADERS)
            with urllib.request.urlopen(img_req, timeout=25) as ir:
                img_bytes = ir.read()
            if len(img_bytes) > 15000:
                out_path = os.path.join(ASSETS_DIR, out_name)
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                manifest[out_name] = {
                    "title": page.get("title"),
                    "license": lic,
                    "artist": artist,
                    "url": dl_url
                }
                print(f"[OK] {out_name} <- {page.get('title')} ({lic}, {len(img_bytes)//1024} KB)")
                downloaded = True
                break
        except Exception as e:
            print(f"  [retry] {out_name}: {e}")
    if not downloaded:
        print(f"[MISS] {out_name}")

with open(os.path.join(ASSETS_DIR, "manifest.json"), "w", encoding="utf-8") as mf:
    json.dump(manifest, mf, ensure_ascii=False, indent=2)
