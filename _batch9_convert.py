#!/usr/bin/env python3
"""
Convert 17 source files (batch 9) to flat HTML pages.
Migrate from Hugo-converted content to flat HTML bithues-rebuild.
"""

import re, os, json
from pathlib import Path

SRC = Path("/Users/mike/.openclaw/workspace-bacottibot/_trash/websites-bithues-Website-2026-05-12/blog-bithues-converted/content")
DEST_BASE = Path("/Users/mike/.openclaw/workspace-bacottibot/websites/bithues-rebuild-2026-05-13")
TEMPLATE_PATH = DEST_BASE / "_template.html"
STORIES_DIR = DEST_BASE / "stories"
REVIEWS_DIR = DEST_BASE / "reviews"
ARTICLES_DIR = DEST_BASE / "articles"
SEARCH_JSON_PATH = DEST_BASE / "search.json"

TEMPLATE = TEMPLATE_PATH.read_text()

# Files 121-137 (0-indexed 120-136)
FILES = [
    "the-echoes-return",
    "the-ember-song",
    "the-forbidden-library",
    "the-forgotten-minute",
    "the-harvest",
    "the-humble-mind",
    "the-last-arena",
    "the-last-garden",
    "the-last-gift",
    "the-last-signal",
    "the-last-song",
    "the-last-winter",
    "the-listen",
    "the-martian",
    "the-other-side",
    "the-power-of-changing-your-mind",
    "the-question",
]

def slug_to_urlslug(slug):
    return slug.lower().replace(" ", "-")

def get_category_page(cat):
    return f"/{cat.lower()}.html"

def extract_content(src_path):
    """Extract the body content from a source HTML file, strip AdSense and inline styles."""
    html = src_path.read_text(encoding="utf-8")
    
    # Find body div content
    # Pattern: after the hero div closes, the story-body div opens
    # We want everything in story-body or review-body
    
    # Try to find story-body div
    story_match = re.search(r'<div class="story-body"[^>]*>(.*?)</div>\s*</div>\s*</div>\s*</div>\s*</main>', html, re.DOTALL)
    review_match = re.search(r'<div class="review-body"[^>]*>(.*?)<!-- end review-body -->', html, re.DOTALL)
    
    if story_match:
        body_html = story_match.group(1)
    elif review_match:
        body_html = review_match.group(1)
    else:
        # Fallback: try to find content between hero and end of main
        main_match = re.search(r'<main class="main">(.*?)</main>', html, re.DOTALL)
        if main_match:
            body_html = main_match.group(1)
            # Strip hero section
            hero_match = re.search(r'<div class="feed-section-body">.*?</div>\s*</div>\s*<div style="max-width', body_html, re.DOTALL)
            if hero_match:
                body_html = body_html[hero_match.end():]
        else:
            body_html = "<p>Content not found.</p>"
    
    # Strip AdSense blocks
    body_html = re.sub(r'<ins[^>]*class="adsbygoogle"[^>]*>.*?</ins>', '', body_html, flags=re.DOTALL)
    body_html = re.sub(r'<script[^>]*adsbygoogle[^>]*>.*?</script>', '', body_html, flags=re.DOTALL)
    
    # Strip inline styles from content
    body_html = re.sub(r'\s*style="[^"]*"', '', body_html)
    body_html = re.sub(r"\s*style='[^']*'", '', body_html)
    
    # Clean up empty style attributes
    body_html = re.sub(r'\s+', ' ', body_html)
    
    return body_html.strip()

def extract_meta(src_path):
    """Extract title, category, genre/excerpt, rating, and author from source HTML."""
    html = src_path.read_text(encoding="utf-8")
    
    title_match = re.search(r'<title>(.*?) \| Bithues</title>', html)
    title = title_match.group(1).strip() if title_match else "Untitled"
    
    # Determine category from HTML structure and URL
    hero_cat = ""
    if "Book Review" in html:
        hero_cat = "Book Review"
    elif "Short Story" in html:
        hero_cat = "Short Story"
    
    genre = ""
    genre_match = re.search(r'<span[^>]*>[\s]*(Spiritual Fiction|Fantasy|Epic Fantasy|Literary Fiction|Self-Help Fiction|Survival Fiction|Sci-Fi|Science Fiction|Psychological Fiction|Meta-Fiction|Historical Fiction)', html)
    if genre_match:
        genre = genre_match.group(1)
    
    author = ""
    author_link = re.search(r'href="/authors"[^>]*>([^<]+)', html)
    if author_link:
        author = author_link.group(1).strip()
    
    rating = ""
    rating_match = re.search(r'[★]+', html)
    if rating_match:
        rating = rating_match.group(0)
    
    page_url_slug = src_path.stem  # e.g. "the-martian"
    category = "stories" if hero_cat == "Short Story" else "reviews" if hero_cat == "Book Review" else "articles"
    
    return {
        "title": title,
        "category": hero_cat,
        "genre": genre,
        "author": author,
        "rating": rating,
        "url_slug": page_url_slug,
        "category_folder": category,
    }

def build_page(meta, body_html, template=TEMPLATE):
    """Build a flat HTML page from meta + body content."""
    title = meta["title"]
    desc = meta.get("desc", f"Read {title} on Bithues.")
    cat = meta["category"]
    
    # Build category label
    cat_label = cat  # e.g. "Short Story" or "Book Review"
    
    page = template.replace("PAGE TITLE", title)
    page = page.replace("PAGE DESCRIPTION", desc)
    
    # Build main content
    content = ""
    
    if meta["category"] == "Book Review":
        content += f'''
  <div class="review-hero" style="background:var(--surface);border-radius:var(--radius);box-shadow:var(--shadow);padding:2rem 2.25rem;margin-bottom:1.25rem;">
    <div class="hero-eyebrow" style="font-size:.72rem;font-weight:600;color:var(--gold);text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;">Book Review</div>
    <h1 style="font-family:'Lora',serif;font-size:1.9rem;font-weight:700;color:var(--navy);line-height:1.25;margin-bottom:.6rem;">{title}</h1>
    <p class="hero-sub" style="font-size:1rem;color:var(--text-mid);line-height:1.6;margin-bottom:1rem;max-width:640px;">In-depth review of {title} on Bithues.</p>
    <div class="meta-row" style="display:flex;flex-wrap:wrap;align-items:center;gap:.35rem;font-size:.82rem;color:var(--text-dim);">'''
        if meta["author"]:
            content += f'''
      <a href="/authors" style="color:var(--orange);text-decoration:none">{meta["author"]}</a>
      <span style="color:var(--border);">·</span>'''
        if meta["genre"]:
            content += f'''
      <span>{meta["genre"]}</span>
      <span style="color:var(--border);">·</span>'''
        if meta["rating"]:
            content += f'''
      <span style="color:var(--gold);letter-spacing:1px;">{meta["rating"]}</span>'''
        content += f'''
    </div>
  </div>
  <div class="review-body" style="display:grid;grid-template-columns:180px 1fr;gap:2.5rem;background:var(--surface);border-radius:var(--radius);box-shadow:var(--shadow);padding:2rem 2.25rem;margin-bottom:1.25rem;align-items:start;">
    <div class="book-cover" style="background:var(--border);border-radius:var(--radius);aspect-ratio:2/3;display:flex;align-items:center;justify-content:center;font-size:.75rem;color:var(--text-dim);text-align:center;padding:1rem;">
      Cover
    </div>
    <div class="review-text">
      {body_html}
    </div>
  </div>'''
    else:
        # Story or Article
        genre_html = f'''<span>{meta["genre"]}</span><span style="color:var(--border);">·</span>''' if meta["genre"] else ""
        content += f'''
  <div class="story-hero" style="padding:2rem 0 1.5rem;border-bottom:1px solid var(--border);margin-bottom:2rem;">
    <div style="font-size:.7rem;color:var(--gold);font-weight:600;letter-spacing:.5px;text-transform:uppercase;margin-bottom:.4rem;">{cat_label}</div>
    <h1 style="font-family:'Lora',serif;font-size:1.75rem;font-weight:700;color:var(--navy);line-height:1.2;margin-bottom:.5rem;">{title}</h1>
    <div style="font-size:.78rem;color:var(--text-dim);display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;">
      {genre_html}
      <span> read</span>
    </div>
  </div>
  <div style="max-width:680px;margin:0 auto;">
    <div style="font-family:'Lora',serif;font-size:1.1rem;line-height:1.85;color:var(--text);margin-bottom:2.5rem;">
      {body_html}
    </div>
  </div>'''
    
    # Replace the placeholder comment with actual content
    page = page.replace("<!-- PAGE CONTENT GOES HERE -->", content)
    
    return page

def update_search_json(meta):
    """Add an entry to search.json."""
    if SEARCH_JSON_PATH.exists():
        data = json.loads(SEARCH_JSON_PATH.read_text())
    else:
        data = []
    
    # Check for existing entry
    url = f"/{meta['category_folder']}/{meta['url_slug']}.html"
    existing = [i for i, e in enumerate(data) if e.get("url") == url]
    for idx in reversed(existing):
        data.pop(idx)
    
    entry = {
        "title": meta["title"],
        "category": meta["category"],
        "url": url,
    }
    data.append(entry)
    
    SEARCH_JSON_PATH.write_text(json.dumps(data, indent=2))
    return url

def main():
    STORIES_DIR.mkdir(exist_ok=True)
    REVIEWS_DIR.mkdir(exist_ok=True)
    ARTICLES_DIR.mkdir(exist_ok=True)
    
    results = []
    
    for fname in FILES:
        src_path = SRC / f"{fname}.html"
        if not src_path.exists():
            print(f"SKIP (not found): {fname}")
            continue
        
        print(f"Processing: {fname}")
        
        meta = extract_meta(src_path)
        body = extract_content(src_path)
        
        dest_dir = {
            "stories": STORIES_DIR,
            "reviews": REVIEWS_DIR,
            "articles": ARTICLES_DIR,
        }.get(meta["category_folder"], STORIES_DIR)
        
        dest_path = dest_dir / f"{fname}.html"
        
        page_html = build_page(meta, body)
        dest_path.write_text(page_html, encoding="utf-8")
        
        url = update_search_json(meta)
        results.append((meta["title"], meta["category"], url))
        print(f"  -> {dest_path} ({meta['category_folder']})")
    
    print(f"\nDone! {len(results)} files processed.")
    for title, cat, url in results:
        print(f"  [{cat}] {title} -> {url}")

if __name__ == "__main__":
    main()