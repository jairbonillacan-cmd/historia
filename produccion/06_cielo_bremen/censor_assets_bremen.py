"""Desenfoca símbolos que disparan filtros de YouTube (esvásticas) directamente en las fotos de assets/.
Corre una sola vez sobre las originales de assets/candidatas/; las coordenadas son en píxeles de cada foto."""
from pathlib import Path
from PIL import Image, ImageFilter

BASE = Path("produccion/06_cielo_bremen/assets")
REGIONS = {
    "bf109_flight.jpg": ("candidatas/bf109_flight_3.jpg", [(622, 236, 680, 290)]),  # esvástica en la deriva
    "stigler.png": ("candidatas/stigler.png", [(78, 490, 190, 560), (165, 0, 235, 28)]),  # águilas del uniforme y la gorra
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
