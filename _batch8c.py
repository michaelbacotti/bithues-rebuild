#!/usr/bin/env python3
"""Correct batch 8 conversion with proper body extraction for all types."""
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

JUNK_PATTERNS = [
    (r'<nav class="nav">.*?</nav>', '', 'nav'),
    (r'<footer class="footer">.*?</footer>', '', 'footer'),
    (r'<script>.*?</script>', '', 'script'),
    (r'<link[^>]*googleapis[^>]*>', '', 'gfonts1'),
    (r'<link[^>]*gstatic[^>]*>', '', 'gfonts2'),
    (r'<link[^>]*href="css/style\.css"[^>]*>', '', 'oldcss'),
    (r'<div class="adsense-block".*?</div>', '', 'adsense'),
    (r'<div class="share-row"[^>]*>.*?</div>\s*</div>', '', 'share-row'),
    (r'<div class="story-share-row"[^>]*>.*?</div>\s*</div>', '', 'story-share-row'),
    (r'<div class="related-section"[^>]*>.*?</div>\s*</div>', '', 'related-section'),
    (r'<div style="display:flex;align-items:center;gap:\.75rem;padding:1\.25rem 0;border-top:1px solid var\(--border\);border-bottom:1px solid var\(--border\);margin:1\.5rem 0;">.*?</div>\s*</div>', '', 'share-row-inline'),
    (r'<div style="margin-top:2rem;">.*?</main>', '', 'you-might-also-like'),
    (r'<div class="feed">\s*class="article-hero".*?</div>\s*</div>\s*</div>', '', 'article-hero-dup'),
    (r'<div class="feed">\s*class="review-hero".*?</div>\s*</div>\s*</div>', '', 'review-hero-dup'),
    (r'<div class="feed">\s*<div class="feed-section">\s*<div class="feed-section-body">\s*<div class="story-hero"[^>]*>.*?</div>\s*</div>', '', 'story-hero-dup'),
    (r'<main class="main">\s*<div class="feed">', '<main class="main">', 'feed-wrapper'),
    (r'\s*</div>\s*</main>\s*<footer', '</main><footer', 'extra-divs'),
    (r'<div class="article-hero"[^>]*>.*?</div>\s*</div>\s*</div>', '', 'article-hero-feed'),
    (r'<div class="review-hero"[^>]*>.*?</div>\s*</div>\s*</div>', '', 'review-hero-feed'),
]

def clean_junk(text):
    for pattern, replacement, name in JUNK_PATTERNS:
        text = re.sub(pattern, replacement, text, flags=re.DOTALL)
    return text

def extract_article_body(text):
    """Extract from <div class="article-body"...> until first </div> before junk."""
    lines = text.split('\n')
    in_body = False
    content_lines = []
    for line in lines:
        if 'class="article-body"' in line:
            in_body = True
            continue
        if in_body:
            if '</div>' in line:
                in_body = False
                continue
            content_lines.append(line)
    return '\n'.join(content_lines).strip()

def extract_review_body(text):
    """Extract from <div class="review-prose"> or <div class="review-body">."""
    # Try review-prose first
    m = re.search(r'<div class="review-prose">(.*?)</div>\s*<table', text, flags=re.DOTALL)
    if m:
        return m.group(1)
    # Try review-body with review-prose inside
    m = re.search(r'<div class="review-body"[^>]*>.*?<div class="review-prose">(.*?)</div>', text, flags=re.DOTALL)
    if m:
        return m.group(1)
    return ""

def extract_story_body(text):
    """Extract from <div class="story-body"...> line-by-line until first </div>."""
    lines = text.split('\n')
    in_body = False
    content_lines = []
    for line in lines:
        if 'class="story-body"' in line:
            in_body = True
            continue
        if in_body:
            if '</div>' in line:
                in_body = False
                continue
            content_lines.append(line)
    return '\n'.join(content_lines).strip()

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
    
    output = re.sub(
        r'<main>\s*<!-- PAGE CONTENT GOES HERE -->\s*</main>\s*<div id="site-footer"></div>',
        header, output, flags=re.DOTALL)
    return output

def fix_links(html):
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
    html = re.sub(r'href="/articles/reading-challenge-2026/"', 'href="/articles/reading-challenge-2026.html"', html)
    return html

def process_file(fname):
    path = os.path.join(SRC, fname)
    if not os.path.exists(path):
        return None
    
    with open(path) as f:
        source = f.read()
    
    cat_label, cat_type = CATEGORIES[fname]
    asin = ASINS.get(fname)
    title = extract_title(source)
    
    cleaned = clean_junk(source)
    
    if cat_type == "article":
        body = extract_article_body(cleaned)
    elif cat_type == "review":
        body = extract_review_body(cleaned)
    else:
        body = extract_story_body(cleaned)
    
    if not body.strip():
        print(f"  WARNING: empty body for {fname}")
        body = "<p>Content unavailable.</p>"
    
    page_html = make_page(fname, title, body, cat_label, cat_type, asin)
    page_html = fix_links(page_html)
    
    return {
        'fname': fname,
        'title': title,
        'cat_type': cat_type,
        'cat_label': cat_label,
        'html': page_html,
    }

results = []
for fname in FILES:
    r = process_file(fname)
    if r:
        results.append(r)
        out_path = os.path.join(DST, determine_dest(r['fname'], r['cat_type']), r['fname'])
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w') as f:
            f.write(r['html'])
        print(f"OK: {r['cat_label']} → /{determine_dest(r['fname'], r['cat_type'])}/{r['fname']}")

# Update search.json
search_path = os.path.join(DST, "search.json")
with open(search_path) as f:
    search_data = json.load(f)

existing_urls = {e['url'] for e in search_data}
for r in results:
    url = f"/{determine_dest(r['fname'], r['cat_type'])}/{r['fname']}"
    if url not in existing_urls:
        search_data.append({
            'title': r['title'],
            'category': r['cat_label'],
            'url': url,
            'summary': r['title'],
        })
        existing_urls.add(url)

with open(search_path, 'w') as f:
    json.dump(search_data, f, indent=2)

print(f"\nBatch 8 complete: {len(results)} files")