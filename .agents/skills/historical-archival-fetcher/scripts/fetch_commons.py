#!/usr/bin/env python3
"""
Search Wikimedia Commons for historical photographs or archival video clips,
extract license metadata, format the legal attribution pill, and optionally download.
"""
import argparse
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "HistoricalShortsArchivalFetcher/1.0 (https://commons.wikimedia.org)"


def clean_html(raw: str) -> str:
    text = re.sub(r"<[^>]+>", "", raw or "")
    return html.unescape(text).strip()


def format_license(short_name: str) -> str:
    s = short_name.upper()
    if "PUBLIC DOMAIN" in s or "PD" in s or "CC0" in s:
        return "DOMINIO PÚBLICO"
    if "CC BY-SA" in s:
        return s.replace("CC-BY-SA", "CC BY-SA")
    if "CC BY" in s:
        return s.replace("CC-BY", "CC BY")
    return s or "DOMINIO PÚBLICO"


def search_commons(query: str, limit: int = 5) -> list[dict]:
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap|video {query}",
        "gsrnamespace": "6",
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|mime",
        "iiurlwidth": "1280",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    pages = data.get("query", {}).get("pages", {})
    results = []
    for page in pages.values():
        ii = (page.get("imageinfo") or [{}])[0]
        ext = ii.get("extmetadata", {})
        author = clean_html(ext.get("Artist", {}).get("value", "")) or "ARCHIVO HISTÓRICO"
        author = re.sub(r"\s+", " ", author)[:42].upper()
        lic_raw = clean_html(ext.get("LicenseShortName", {}).get("value", "Public domain"))
        lic = format_license(lic_raw)
        mime = ii.get("mime", "")
        kind = "VIDEO DE ARCHIVO" if "video" in mime or "ogg" in mime or "webm" in mime else "FOTO DE ARCHIVO"
        pill = f"{kind} · {author} · {lic}"
        results.append(
            {
                "title": page.get("title"),
                "mime": mime,
                "url": ii.get("thumburl") or ii.get("url"),
                "original_url": ii.get("url"),
                "license": lic,
                "author": author,
                "attribution_pill": pill,
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Search Wikimedia Commons archival media.")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Max results")
    parser.add_argument("--download-first", type=Path, help="Optional destination path to download the top result")
    args = parser.parse_args()

    items = search_commons(args.query, args.limit)
    print(json.dumps(items, indent=2, ensure_ascii=False))

    if args.download_first and items:
        dl_url = items[0]["url"]
        args.download_first.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(dl_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as resp:
            args.download_first.write_bytes(resp.read())
        print(f"[OK] Downloaded {dl_url} -> {args.download_first}")


if __name__ == "__main__":
    main()
