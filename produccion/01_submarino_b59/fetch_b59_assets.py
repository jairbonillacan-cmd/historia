import os
import json
import time
import urllib.request
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}

articles = {
    "b59_surface.jpg": "Soviet_submarine_B-59",
    "arkhipov.jpg": "Vasili_Arkhipov",
    "uss_randolph.jpg": "USS_Randolph_(CV-15)",
    "kennedy_1962.jpg": "John_F._Kennedy",
    "cuban_crisis.jpg": "Cuban_Missile_Crisis",
    "k19_sub.jpg": "Soviet_submarine_K-19",
    "foxtrot_sub.jpg": "Foxtrot-class_submarine"
}

for fname, title in articles.items():
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        orig_url = data.get('originalimage', {}).get('source')
        if orig_url:
            out_path = os.path.join('produccion/01_submarino_b59/assets', fname)
            img_req = urllib.request.Request(orig_url, headers=headers)
            with urllib.request.urlopen(img_req, timeout=15) as img_resp:
                with open(out_path, 'wb') as f:
                    f.write(img_resp.read())
            print(f"Upgraded {fname} to full-res ({os.path.getsize(out_path)} bytes)")
    except Exception as e:
        print(f"Kept thumb for {fname}: {e}")
    time.sleep(0.4)
