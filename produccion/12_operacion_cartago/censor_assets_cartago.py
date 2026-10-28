"""Tapa símbolos que pueden disparar filtros de YouTube directamente en las fotos de assets/.
Corre una sola vez sobre las originales de assets/candidatas/; las coordenadas son en píxeles de cada foto.
En las fotos del Shellhus la bandera de la azotea no se distingue: puede ser la de la ocupación, así que se tapa."""
from pathlib import Path
from PIL import Image, ImageFilter

BASE = Path("produccion/12_operacion_cartago/assets")
REGIONS = {
    "shellhus_antes.jpg": ("candidatas/shellhus_burning_2.jpg", [(205, 88, 250, 135)]),  # bandera en la azotea
    "shellhus_1940.jpg": ("candidatas/shell_all_3.jpg", [(388, 12, 430, 52)]),  # bandera en la azotea
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
