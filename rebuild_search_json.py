#!/usr/bin/env python3
"""
rebuild_search_json.py
Reads ALL HTML files in stories/, articles/, reviews/ dirs and extracts
complete metadata to produce a full, accurate search.json.
For reviews: extracts Amazon cover image URL from the HTML.
"""
import json, re, sys
from pathlib import Path

ROOT = Path("/Users/mike/.openclaw/workspace-bacottibot/websites/bithues-rebuild-2026-05-13")

CATEGORIES = {
    "stories": "Short Story",
    "articles": "Article",
    "reviews":  "Book Review",
}

def extract_amazon_image(html: str) -> str | None:
    """Extract Amazon cover image URL from a review HTML file."""
    m = re.search(r'src="(https://images-na\.ssl-images-amazon\.com/images/P/[^"]+)"', html)
    if m:
        return m.group(1)
    # Also check style= background
    m = re.search(r'background-image:\s*url\(["\']?(https://images-na\.ssl-images-amazon\.com/images/P/[^)\'"\s]+)', html)
    if m:
        return m.group(1)
    return None

def extract_meta(html: str, url_path: str) -> dict:
    """Extract title, summary, date, category, image from an HTML file."""
    # Title
    m = re.search(r'<title[^>]*>([^<]+)</title>', html)
    title = m.group(1).strip() if m else url_path

    # Meta description
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    description = m.group(1).strip() if m else ""

    # Category (from section)
    section = "stories"
    for sec in CATEGORIES:
        if f"/{sec}/" in url_path:
            section = sec
            break
    category = CATEGORIES[section]

    # Date — look for meta date or schema date
    m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
    if not m:
        m = re.search(r'<time\s+[^>]*datetime="([^"]+)"', html)
    if not m:
        m = re.search(r'class="card-meta"[^>]*>\s*<span>([^<]+)</span>', html)
    date_str = m.group(1).strip() if m else ""
    # Parse to timestamp
    date_ts = 0
    if date_str:
        try:
            from datetime import datetime
            for fmt in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d", "%B %d %Y"):
                try:
                    dt = datetime.strptime(date_str, fmt)
                    date_ts = dt.timestamp()
                    break
                except: pass
        except: pass
    if not date_ts:
        # Use file mtime as fallback
        date_ts = 0

    # For reviews: get Amazon image
    image = None
    if section == "reviews":
        image = extract_amazon_image(html)
        if not image:
            image = "/images/card-fallback.svg"
    elif section == "articles":
        # Article hero image
        slug = Path(url_path).stem
        for ext in ("jpg", "png", "webp"):
            p = ROOT / "articles" / "images" / f"{slug}.{ext}"
            if p.exists():
                image = f"/articles/images/{slug}.{ext}"
                break
        if not image:
            image = "/images/card-fallback.svg"
    elif section == "stories":
        slug = Path(url_path).stem
        for ext in ("jpg", "png", "webp"):
            p = ROOT / "stories" / "images" / f"{slug}.{ext}"
            if p.exists():
                image = f"/stories/images/{slug}.{ext}"
                break
        if not image:
            image = "/images/card-fallback.svg"

    return {
        "title": title,
        "url": url_path,
        "category": category,
        "summary": description,
        "date": date_ts,
        "image": image,
    }

def main():
    entries = {}
    for section, category in CATEGORIES.items():
        dir_path = ROOT / section
        if not dir_path.exists():
            continue
        for html_file in sorted(dir_path.glob("*.html")):
            if html_file.name in ("index.html"):
                continue
            try:
                html = html_file.read_text(encoding="utf-8")
            except:
                continue
            url_path = f"/{section}/{html_file.name}"
            meta = extract_meta(html, url_path)
            # Use URL as key to dedupe
            entries[url_path] = meta

    result = sorted(entries.values(), key=lambda x: -(x.get("date") or 0))
    out_path = ROOT / "search.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Written {len(result)} entries to {out_path}")
    # Stats
    reviews = [e for e in result if e["category"] == "Book Review"]
    articles = [e for e in result if e["category"] == "Article"]
    stories = [e for e in result if e["category"] == "Short Story"]
    reviews_with_img = [e for e in reviews if e.get("image") and e["image"] != "/images/card-fallback.svg"]
    print(f"  Stories: {len(stories)} | Articles: {len(articles)} | Reviews: {len(reviews)}")
    print(f"  Reviews with Amazon image: {len(reviews_with_img)}/{len(reviews)}")
    print(f"  Stories with image: {len([e for e in stories if e.get('image') and '/card-fallback' not in e.get('image','') and e.get('image')])}/{len(stories)}")
    print(f"  Articles with image: {len([e for e in articles if e.get('image') and '/card-fallback' not in e.get('image','') and e.get('image')])}/{len(articles)}")

if __name__ == "__main__":
    main()