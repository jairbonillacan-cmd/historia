import os
import sys
import json
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ASSETS_DIR = "produccion/02_desastre_bari/assets"
HEADERS = {"User-Agent": "HistoricalShortsArchivalFetcher/1.0 (https://commons.wikimedia.org)"}

EXACT_FILES = {
    "bari_ships.jpg": "File:Atak lotniczy na flotę w Bari (2-2443).jpg",
    "mustard_shells.jpg": "File:155mmMustardGasShells.jpg",
    "allied_hospital.jpg": "File:Mustard gas burns.jpg",
    "edgewood_test.jpg": "File:Edgewood Arsenal - Mustard Gas Test Subjects March 1945.jpg",
    "mustard_poster.jpg": "File:Mustard gas ww2 poster.jpg",
}

for out_name, file_title in EXACT_FILES.items():
    params = urllib.parse.urlencode({
        "action": "query",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": "1280",
        "format": "json",
    })
    url = f"https://commons.wikimedia.org/w/api.php?{params}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        iinfo = (page.get("imageinfo") or [{}])[0]
        dl_url = iinfo.get("thumburl") or iinfo.get("url")
        if not dl_url:
            continue
        img_req = urllib.request.Request(dl_url, headers=HEADERS)
        with urllib.request.urlopen(img_req, timeout=25) as ir:
            img_bytes = ir.read()
        out_path = os.path.join(ASSETS_DIR, out_name)
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        print(f"[OK] {out_name} <- {file_title} ({len(img_bytes)//1024} KB)")
