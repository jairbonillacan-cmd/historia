---
name: historical-archival-fetcher
description: >-
  Search and download verified historical photographs, portraits, maps, coins,
  and public-domain archival video clips from Wikimedia Commons with automatic
  legal attribution pill generation (DOMINIO PÚBLICO / CC BY-SA). Use this skill
  whenever gathering real historical visual assets for a video scene.
---

# Historical Archival Media Fetcher (Wikimedia Commons)

Use this skill to search, verify, and download real historical photographs, artworks, numismatics, and public-domain motion-picture clips from **Wikimedia Commons**, and to format their mandatory legal attribution string.

---

## 1. Editorial Verification Rules

1. **Historical Subject Accuracy:**
   - Always inspect the downloaded image with `read_file` before placing it in a scene to ensure the person, ship, aircraft, bust, or city matches the exact historical entity and year spoken in the script.
2. **Mandatory Legal Attribution Pill:**
   - Every external archival asset rendered on screen must display its `<AttributionPill>` at `X = 40px, Y = 1445px` using the middot (`·`) format:
     - **Photographs / Artworks:** `FOTO DE ARCHIVO · [AUTOR O INSTITUCIÓN], [AÑO] · [DOMINIO PÚBLICO / CC BY-SA 4.0]`
     - **Archival Film / Video:** `VIDEO DE ARCHIVO · [ORIGEN / ARCHIVO], [AÑO] · [DOMINIO PÚBLICO / CC BY-SA 4.0]`

---

## 2. Searching & Downloading with the Helper Script

Run [scripts/fetch_commons.py](./scripts/fetch_commons.py) to search Wikimedia Commons by query, inspect license metadata, download the file into your production `assets/` directory, and get the ready-to-use attribution string:

```bash
python .agents/skills/historical-archival-fetcher/scripts/fetch_commons.py \
  --query "Vasili Arkhipov" \
  --out-dir "produccion/01_submarino_b59/assets" \
  --limit 3
```
