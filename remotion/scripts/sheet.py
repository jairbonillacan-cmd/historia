# Une cuadros de out/ en una hoja de contacto: python scripts/sheet.py salida.jpg a.jpg b.jpg ...
import sys
from PIL import Image, ImageDraw
out, files = sys.argv[1], sys.argv[2:]
cols = 5; w, h = 324, 576
sheet = Image.new("RGB", (cols * w, ((len(files) + cols - 1) // cols) * (h + 24)), "black")
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((w, h))
    x, y = (i % cols) * w, (i // cols) * (h + 24)
    sheet.paste(im, (x, y)); d.text((x + 6, y + h + 4), f.split("/")[-1].split("\\")[-1], fill="yellow")
sheet.save(out, quality=88)
