"""Tapa en las fotos de assets/ lo que puede disparar filtros de YouTube (cuerpos entre los escombros).
Corre una sola vez sobre las originales de assets/candidatas/; las coordenadas son en píxeles de cada foto."""
from pathlib import Path
from PIL import Image, ImageFilter

BASE = Path("produccion/08_messines/assets")
REGIONS = {
    "devastation.jpg": ("candidatas/battle_3.jpg", [(1040, 600, 1520, 920)]),  # soldado caído entre los escombros
}

for out, (src, boxes) in REGIONS.items():
    im = Image.open(BASE / src).convert("RGB")
    for box in boxes:
        patch = im.crop(box)
        w, h = patch.size
        patch = patch.resize((max(1, w // 10), max(1, h // 10))).resize((w, h), Image.NEAREST).filter(ImageFilter.GaussianBlur(6))
        im.paste(patch, box)
    im.save(BASE / out, quality=95)
    print(f"{out}: {len(boxes)} zonas tapadas")
