#!/usr/bin/env python3
"""Better body extraction for batch 8."""
import os, re, json

SRC = "/Users/mike/.openclaw/workspace-bacottibot/_trash/websites-bithues-Website-2026-05-12/blog-bithues-converted/content"
DST = "/Users/mike/.openclaw/workspace-bacottibot/websites/bithues-rebuild-2026-05-13"
TEMPLATE_PATH = f"{DST}/_template.html"

def load_template():
    with open(TEMPLATE_PATH) as f:
        return f.read()

TEMPLATE = load_template()

FILES = [
    "reading-challenge-2026.html",
    "reading-order-guide-high-fantasy.html",
    "read-more-this-year.html",
    "red-horizon-lunar-launch.html",
    "romance-for-beginners.html",
    "rules-of-the-game.html",
    "shadow-work-guide.html",
    "speed-reading-basics.html",
    "they-walk-among-us.html",
    "the-blueprint.html",
    "the-borrowed-life.html",
    "the-cartographer-of-sea-serpents.html",
    "the-confluence-doctrine.html",
    "the-disclosure.html",
    "the-door-between-worlds.html",
]

CATEGORIES = {
    "reading-challenge-2026.html": ("Article", "article"),
    "reading-order-guide-high-fantasy.html": ("Article", "article"),
    "read-more-this-year.html": ("Article", "article"),
    "red-horizon-lunar-launch.html": ("Book Review", "review"),
    "romance-for-beginners.html": ("Article", "article"),
    "rules-of-the-game.html": ("Short Story", "story"),
    "shadow-work-guide.html": ("Article", "article"),
    "speed-reading-basics.html": ("Article", "article"),
    "they-walk-among-us.html": ("Short Story", "story"),
    "the-blueprint.html": ("Book Review", "review"),
    "the-borrowed-life.html": ("Short Story", "story"),
    "the-cartographer-of-sea-serpents.html": ("Short Story", "story"),
    "the-confluence-doctrine.html": ("Book Review", "review"),
    "the-disclosure.html": ("Short Story", "story"),
    "the-door-between-worlds.html": ("Short Story", "story"),
}

ASINS = {
    "red-horizon-lunar-launch.html": "B0GQVLB9N2",
    "the-blueprint.html": "B0GQK61R5H",
    "the-confluence-doctrine.html": "B0GSP9S473",
}

def clean_all_junk(html):
    """Remove nav, footer, scripts, fonts, CSS links, AdSense, share rows, related sections."""
    text = html
    # Remove nav
    text = re.sub(r'<nav class="nav">.*?</nav>', '', text, flags=re.DOTALL)
    # Remove footer
    text = re.sub(r'<footer class="footer">.*?</footer>', '', text, flags=re.DOTALL)
    # Remove scripts
    text = re.sub(r'<script>.*?</script>', '', text, flags=re.DOTALL)
    # Remove Google Fonts
    text = re.sub(r'<link[^>]*googleapis[^>]*>', '', text)
    text = re.sub(r'<link[^>]*gstatic[^>]*>', '', text)
    # Remove old CSS
    text = re.sub(r'<link[^>]*href="css/style\.css"[^>]*>', '', text)
    # Remove AdSense
    text = re.sub(r'<div style="margin:2\.5rem 0;padding:1rem;background:var\(--surface\);border-radius:var\(--radius\);box-shadow:var\(--shadow\);text-align:center;">.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="adsense-block".*?</div>', '', text, flags=re.DOTALL)
    # Remove share rows
    text = re.sub(r'<div style="display:flex;align-items:center;gap:\.75rem;padding:1\.25rem 0;border-top:1px solid var\(--border\);border-bottom:1px solid var\(--border\);margin:1\.5rem 0;">.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="share-row"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="story-share-row"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="share-row"[^>]*>.*?</div>\s*</main>', '', text, flags=re.DOTALL)
    # Remove related sections / "You might also like"
    text = re.sub(r'<div class="related-section"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div style="margin-top:2rem;">.*?</main>', '', text, flags=re.DOTALL)
    return text

def extract_body_content(html, fname, cat_type):
    """Extract just the body paragraphs, no wrappers."""
    text = clean_all_junk(html)
    
    # For articles: extract from .article-body div
    if cat_type == "article":
        m = re.search(r'<div class="article-body"[^>]*>(.*?)</div>\s*<div style="margin:2\.5rem', text, flags=re.DOTALL)
        if m:
            content = m.group(1)
        else:
            # try without the margin check
            m = re.search(r'<div class="article-body"[^>]*>(.*?)</div>\s*<div', text, flags=re.DOTALL)
            if m:
                content = m.group(1)
            else:
                content = ""
    # For reviews: extract from .review-prose
    elif cat_type == "review":
        m = re.search(r'<div class="review-prose">(.*?)</div>\s*<table', text, flags=re.DOTALL)
        if m:
            content = m.group(1)
        else:
            # Try review-body div
            m = re.search(r'<div class="review-body"[^>]*>.*?<div class="review-prose">(.*?)</div>', text, flags=re.DOTALL)
            if m:
                content = m.group(1)
            else:
                content = ""
    # For stories: extract from .story-body
    else:
        m = re.search(r'<div class="story-body"[^>]*>(.*?)</div>\s*<div class="story-share-row"', text, flags=re.DOTALL)
        if m:
            content = m.group(1)
        else:
            content = ""
    
    # Strip the inner wrapper divs from body content
    content = re.sub(r'<div class="(article-body|story-body|review-prose|content-body)"[^>]*>', '', content)
    content = re.sub(r'</div>\s*$', '', content.strip())
    
    # Clean up any remaining old-style inline wrappers that aren't p tags
    # Remove the max-width container div wrapper
    content = re.sub(r'^<div style="max-width:680px;margin:2rem auto 0;">', '', content)
    content = re.sub(r'</div>\s*$', '', content.strip())
    
    return content.strip()

def extract_title(html):
    m = re.search(r'<title>(.*?) \| Bithues</title>', html)
    return m.group(1) if m else "Untitled"

def determine_dest(fname, cat_type):
    if cat_type == "review": return "reviews"
    elif cat_type == "article": return "articles"
    else: return "stories"

def make_page(fname, title, body_content, cat_label, cat_tag, asin=None):
    output = TEMPLATE.replace("PAGE TITLE", title, 1)
    output = output.replace("PAGE DESCRIPTION — one clear sentence.", title, 1)
    
    if cat_tag == "review" and asin:
        header = f'''<header class="content-header">
    <div class="content-header-inner">
      <span class="tag tag--review">{cat_label}</span>
      <h1 class="content-title">{title}</h1>
    </div>
  </header>

  <main class="content-body">
    <div class="review-header">
      <img src="https://images-na.ssl-images-amazon.com/images/I/{asin}._SL500_.jpg"
           class="book-cover-thumb"
           alt="{title} cover"
           loading="lazy"
           onerror="this.style.display='none';this.nextElementSibling.style.display='flex';" />
      <div class="book-cover-placeholder" style="display:none;"></div>
    </div>
    {body_content}
  </main>

  <div id="site-footer"></div>

  <script src="/nav.js"></script>
  <script src="/footer.js"></script>'''
    else:
        header = f'''<header class="content-header">
    <div class="content-header-inner">
      <span class="tag tag--{cat_tag}">{cat_label}</span>
      <h1 class="content-title">{title}</h1>
    </div>
  </header>

  <main class="content-body">
    {body_content}
  </main>

  <div id="site-footer"></div>

  <script src="/nav.js"></script>
  <script src="/footer.js"></script>'''
    
    output = re.sub(r'<main>\s*<!-- PAGE CONTENT GOES HERE -->\s*</main>\s*<div id="site-footer"></div>',
                    header, output, flags=re.DOTALL)
    return output

def fix_links(html):
    """Fix relative hrefs to absolute paths."""
    html = re.sub(r'href="index\.html"', 'href="/index.html"', html)
    html = re.sub(r'href="about\.html"', 'href="/about.html"', html)
    html = re.sub(r'href="browse\.html"', 'href="/browse.html"', html)
    html = re.sub(r'href="/authors"', 'href="/reviews.html"', html)
    html = re.sub(r'href="/reviews/home-for-anya/"', 'href="/reviews/home-for-anya.html"', html)
    html = re.sub(r'href="/reviews/32/"', 'href="/reviews/32.html"', html)
    html = re.sub(r'href="/reviews/6/"', 'href="/reviews/6.html"', html)
    html = re.sub(r'href="/stories/american-voices/"', 'href="/stories/american-voices.html"', html)
    html = re.sub(r'href="/stories/before-the-streetlights-came-on/"', 'href="/stories/before-the-streetlights-came-on.html"', html)
    html = re.sub(r'href="/stories/blood-ties/"', 'href="/stories/blood-ties.html"', html)
    return html

results = []
for fname in FILES:
    path = os.path.join(SRC, fname)
    if not os.path.exists(path):
        print(f"SKIP: {fname} not found")
        continue
    
    with open(path) as f:
        source = f.read()
    
    cat_label, cat_type = CATEGORIES[fname]
    asin = ASINS.get(fname)
    title = extract_title(source)
    body = extract_body_content(source, fname, cat_type)
    
    if not body.strip():
        print(f"EMPTY BODY: {fname}")
        body = "<p>Content unavailable.</p>"
    
    page_html = make_page(fname, title, body, cat_label, cat_type, asin)
    page_html = fix_links(page_html)
    
    dest_folder = determine_dest(fname, cat_type)
    out_path = os.path.join(DST, dest_folder, fname)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    with open(out_path, 'w') as f:
        f.write(page_html)
    
    print(f"OK: {out_path}")
    results.append({
        'title': title,
        'category': cat_label,
        'url': f"/{dest_folder}/{fname}",
        'fname': fname,
    })

# Update search.json
search_path = os.path.join(DST, "search.json")
with open(search_path) as f:
    search_data = json.load(f)

# Remove any entries from batch8 files
existing_urls = {e['url'] for e in search_data}
for r in results:
    if r['url'] not in existing_urls:
        search_data.append({
            'title': r['title'],
            'category': r['category'],
            'url': r['url'],
            'summary': r['title'],
        })
        existing_urls.add(r['url'])

with open(search_path, 'w') as f:
    json.dump(search_data, f, indent=2)

print(f"\nBatch 8 complete: {len(results)} files")
for r in results:
    print(f"  {r['category']}: {r['url']}")