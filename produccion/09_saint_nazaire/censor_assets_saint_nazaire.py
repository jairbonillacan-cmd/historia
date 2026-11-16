"""AG-18 · Saint-Nazaire (1942). Copia las fotos elegidas de assets/candidatas/ a assets/ con su nombre final,
desenfoca los símbolos que disparan filtros de YouTube (la bandera de guerra del Bismarck) y escribe
assets/assets_metadata.json. Las coordenadas son en píxeles de cada foto original."""
import json
import sys
from pathlib import Path

from PIL import Image, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path("produccion/09_saint_nazaire/assets")
BUNDESARCHIV = "Bundesarchiv, Bild {} · CC BY-SA 3.0 DE"
IWM = "IWM {} · Dominio público"

# nombre final: (candidata, fuente para el pie de foto, descripción, zonas a tapar)
SELECTED = {
    "campbeltown_proa.jpg": ("raid2_2.jpg", BUNDESARCHIV.format("101II-MW-3722-15"), "Soldados alemanes sobre la proa del Campbeltown, 28/3/1942", []),
    "campbeltown_puente.jpg": ("raid2_4.jpg", BUNDESARCHIV.format("101II-MW-3722-18"), "Alemanes recorren el Campbeltown encallado, horas antes de la explosión", []),
    "campbeltown_compuerta.jpg": ("raid2_3.jpg", BUNDESARCHIV.format("101II-MW-3724-02"), "El Campbeltown clavado en la compuerta del dique Normandie", []),
    "campbeltown_dique.jpg": ("raid2_0.jpg", BUNDESARCHIV.format("101II-MW-3722-03"), "El Campbeltown en el dique, con sus chimeneas cortadas", []),
    "dique_aereo_despues.jpg": ("chariot_0.jpg", IWM.format("C 3317A"), "El dique Normandie inundado tras la explosión (foto aérea RAF)", []),
    "dique_aereo_antes.jpg": ("chariot_2.jpg", IWM.format("C 2351"), "Reconocimiento aéreo del puerto de Saint-Nazaire antes del raid", []),
    "puerto_bombardeo.jpg": ("chariot_3.jpg", IWM.format("C 2352"), "Saint-Nazaire bajo bombardeo aéreo", []),
    "tirpitz_noruega.jpg": ("tirpitz2_4.jpg", "Wikimedia Commons · Dominio público", "El Tirpitz camuflado en un fiordo noruego", []),
    "tirpitz_mar.jpg": ("tirpitz2_0.jpg", "Wikimedia Commons · Dominio público", "El Tirpitz a toda máquina (ilustración de época)", []),
    "bismarck.jpg": ("bismarck.jpg", "Bundesarchiv · Wikimedia Commons", "El acorazado Bismarck, gemelo del Tirpitz", [(1266, 372, 1300, 445)]),
    "convoy.jpg": ("convoy_3.jpg", "U.S. Navy · Dominio público", "Convoy aliado en el Atlántico, c. 1942", []),
    "convoy_cielo.jpg": ("convoy_0.jpg", "OWI · Dominio público", "Convoy en el Atlántico, 1942", []),
    "destructor_1940.jpg": ("townclass_0.jpg", "NARA 196521 · Dominio público", "Uno de los 50 destructores viejos cedidos por EE. UU. en 1940, como el Campbeltown", []),
    "destructor_town.jpg": ("townclass_1.jpg", IWM.format("A 8659"), "HMS Buxton, destructor clase Town gemelo del Campbeltown, 1942", []),
    "puente_mando.jpg": ("townclass_2.jpg", IWM.format("A 1063"), "Puente de mando de un destructor británico", []),
    "lancha_ml.jpg": ("chariot_1.jpg", IWM.format("A 13626A"), "Lancha motora de madera (ML) como las del raid", []),
    "beattie.jpg": ("beattie_0.jpg", "Wikimedia Commons · Dominio público", "Stephen Beattie, comandante del Campbeltown", []),
    "cruz_victoria.png": ("vc_3.png", "Wikimedia Commons · Dominio público", "Cruz Victoria", []),
}

cands = json.loads((BASE / "candidatas/candidatas_metadata.json").read_text(encoding="utf-8"))
meta = {}
for out, (src, source, desc, boxes) in SELECTED.items():
    im = Image.open(BASE / "candidatas" / src)
    im = im.convert("RGBA" if out.endswith(".png") else "RGB")
    for box in boxes:
        patch = im.crop(box)
        w, h = patch.size
        patch = patch.resize((max(1, w // 10), max(1, h // 10))).resize((w, h), Image.NEAREST).filter(ImageFilter.GaussianBlur(6))
        im.paste(patch, box)
    im.save(BASE / out, quality=95) if out.endswith(".jpg") else im.save(BASE / out)
    c = cands.get(src, {})
    meta[out] = {"description": desc, "source": source, "origin": c.get("source", ""), "url": c.get("url", ""), "license": c.get("license", ""), "size": list(im.size), "censored_regions": boxes}
    print(f"{out} ← {src} {im.size}" + (f" · {len(boxes)} zonas tapadas" if boxes else ""))

(BASE / "assets_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
