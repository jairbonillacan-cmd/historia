"""AG-22 · Operación Bernhard. Arma las fotos finales de assets/ a partir de las candidatas revisadas a ojo.

Recorta (el billete de £50 sin la funda de la tasadora) y tapa con pixelado + blur horneado en el archivo
cualquier símbolo que pueda disparar filtros. Registra cada foto en assets/assets_metadata.json.
Uso (desde la raíz del repo): python produccion/14_operacion_bernhard/censor_assets_bernhard.py
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("produccion/14_operacion_bernhard/assets")
CAND = BASE / "candidatas"

# final: (candidata, recorte o None, zonas a tapar en píxeles de la candidata)
PICKS = {
    "note50.jpg": ("forged3_1.jpg", (140, 195, 1350, 965), []),  # £50 falso sin la funda PMG
    "note20_pmg.jpg": ("forged3_0.jpg", None, []),  # £20 con la etiqueta «OPERATION BERNHARD»
    "note50_trasluz.jpg": ("forged_3.jpg", None, []),
    "note10_museo.jpg": ("forged_0.jpg", None, []),
    "britannia.jpg": ("forged2_0.jpg", None, []),
    "boe.jpg": ("boe.jpg", None, []),
    "kruger.jpg": ("kruger.jpg", None, []),
    "smolianoff.jpg": ("smolianoff.jpg", None, []),
    "sachs_aerial.jpg": ("sachs_aerial_2.jpg", None, []),
    "sachs_barracks.jpg": ("sachs_barracks_4.jpg", None, []),
    "sachs_interior.jpg": ("sachs_barracks_0.jpg", None, []),
    # mancha clara abajo a la derecha que podría ser un brazalete: se tapa por las dudas
    "sachs_prisoners.jpg": ("sachsenhausen.jpg", None, [(1770, 1110, 1920, 1292)]),
    "sachs_prisoners_b.jpg": ("sachs_1938_3.jpg", None, []),
    "sachs_gate.jpg": ("bundes_sachs_2.jpg", None, []),
    "sachs_rollcall.jpg": ("bundes_sachs_4.jpg", None, []),
    "boe_postcard.jpg": ("boe_old_0.jpg", None, []),
    "cicero.jpg": ("cicero_0.jpg", None, []),
    "he111_london.jpg": ("he111_0.jpg", None, []),
    "he111_formation.jpg": ("he111_2.jpg", None, []),
    "dollar_1934.jpg": ("dollar_0.jpg", None, []),
    "london_1942.jpg": ("london42_0.jpg", None, []),
    "london_1942b.jpg": ("london42_3.jpg", None, []),
    "gransasso.jpg": ("mussolini_0.jpg", None, []),
}

cand_meta = json.loads((CAND / "candidatas_metadata.json").read_text(encoding="utf-8"))
meta = {}
for out, (src, crop, boxes) in PICKS.items():
    im = Image.open(CAND / src).convert("RGB")
    for box in boxes:
        patch = im.crop(box)
        w, h = patch.size
        patch = patch.resize((max(1, w // 12), max(1, h // 12))).resize((w, h), Image.NEAREST).filter(ImageFilter.GaussianBlur(6))
        im.paste(patch, box)
    if crop:
        im = im.crop(crop)
    im.save(BASE / out, quality=94)
    meta[out] = {**cand_meta.get(src, {}), "candidate": src, "covered": len(boxes)}
    print(f"{out:22} ← {src}{' · ' + str(len(boxes)) + ' zona(s) tapada(s)' if boxes else ''}")

(BASE / "assets_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(meta)} fotos en {BASE}")
