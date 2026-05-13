#!/usr/bin/env python3
import os, re, json

SRC = "/Users/mike/.openclaw/workspace-bacottibot/_trash/websites-bithues-Website-2026-05-12/blog-bithues-converted/content"
DST = "/Users/mike/.openclaw/workspace-bacottibot/websites/bithues-rebuild-2026-05-13"
TEMPLATE_PATH = f"{DST}/_template.html"

def load_template():
    with open(TEMPLATE_PATH) as f:
        return f.read()

def load_source(name):
    path = os.path.join(SRC, name)
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    return ""

TEMPLATE = load_template()

# Files to process (106-120)
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

# Category/tag mapping
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

# ASIN mapping for reviews
ASINS = {
    "red-horizon-lunar-launch.html": "B0GQVLB9N2",
    "the-blueprint.html": "B0GQK61R5H",
    "the-confluence-doctrine.html": "B0GSP9S473",
}

def get_body_text(html, fname):
    """Extract clean body text from source HTML."""
    text = html

    # Remove nav blocks
    text = re.sub(r'<nav class="nav">.*?</nav>', '', text, flags=re.DOTALL)
    # Remove footer blocks
    text = re.sub(r'<footer class="footer">.*?</footer>', '', text, flags=re.DOTALL)
    # Remove script tags
    text = re.sub(r'<script>.*?</script>', '', text, flags=re.DOTALL)
    # Remove Google Fonts
    text = re.sub(r'<link rel="preconnect"[^>]*>', '', text)
    text = re.sub(r'<link[^>]*fonts\.googleapis[^>]*>', '', text)
    # Remove old CSS link
    text = re.sub(r'<link[^>]*stylesheet[^>]*href="css/style\.css"[^>]*>', '', text)
    # Remove AdSense blocks
    text = re.sub(r'<div style="margin:2\.5rem 0;padding:1rem;background:var\(--surface\);border-radius:var\(--radius\);box-shadow:var\(--shadow\);text-align:center;">.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="adsense-block"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    # Remove share rows
    text = re.sub(r'<div style="display:flex;align-items:center;gap:\.75rem;padding:1\.25rem 0;border-top:1px solid var\(--border\);border-bottom:1px solid var\(--border\);margin:1\.5rem 0;">.*?</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="share-row"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="story-share-row"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    # Remove related sections
    text = re.sub(r'<div class="related-section"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    # Remove "You might also like" sections
    text = re.sub(r'<div style="margin-top:2rem;">.*?</main>', '', text, flags=re.DOTALL)
    # Remove hero section duplicates
    text = re.sub(r'class="article-hero".*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'class="review-hero".*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'class="story-hero".*?</div>\s*</div>', '', text, flags=re.DOTALL)
    # Remove extra feed wrappers
    text = re.sub(r'<div class="feed">\s*class="[^"]*"', '<div class="feed">', text)
    text = re.sub(r'<div class="feed">\s*</div>', '', text)
    # Remove feed section divs
    text = re.sub(r'<div class="feed-section">.*?</div>\s*</div>\s*</div>', '', text, flags=re.DOTALL)
    # Remove article/review body wrappers that contain old structure
    text = re.sub(r'<div style="max-width:680px;margin:2rem auto 0;">', '<div class="content-body">', text)
    text = re.sub(r'<div class="article-body"[^>]*>', '<div class="content-body">', text)
    text = re.sub(r'<div class="story-body"[^>]*>', '<div class="content-body">', text)
    text = re.sub(r'<div class="review-prose">', '<div class="content-body">', text)
    # Remove Amazon cover images with affiliate tags - keep for now, replace later if needed
    # Remove all old style attributes from body content (they're inline junk)
    # Keep the main content divs
    return text

def get_main_content(html, fname):
    """Extract the main content block from source HTML."""
    text = html
    # Remove nav
    text = re.sub(r'<nav class="nav">.*?</nav>', '', text, flags=re.DOTALL)
    # Remove footer
    text = re.sub(r'<footer class="footer">.*?</footer>', '', text, flags=re.DOTALL)
    # Remove script
    text = re.sub(r'<script>.*?</script>', '', text, flags=re.DOTALL)
    # Remove fonts
    text = re.sub(r'<link rel="preconnect"[^>]*>', '', text)
    text = re.sub(r'<link[^>]*fonts[^>]*>', '', text)
    # Remove old css link
    text = re.sub(r'<link[^>]*href="css/style\.css"[^>]*>', '', text)
    # Remove AdSense
    text = re.sub(r'<div style="margin:2\.5rem 0;padding:1rem;background:var\(--surface\);border-radius:var\(--radius\);box-shadow:var\(--shadow\);text-align:center;">.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="adsense-block"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="adsense-block".*?</div>', '', text, flags=re.DOTALL)
    # Remove share rows
    text = re.sub(r'<div style="display:flex;align-items:center;gap:\.75rem;padding:1\.25rem 0;border-top:1px solid var\(--border\);border-bottom:1px solid var\(--border\);margin:1\.5rem 0;">.*?</div>\s*</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="share-row"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="story-share-row"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="share-row"[^>]*>.*?</div>\s*</main>', '', text, flags=re.DOTALL)
    # Remove related sections
    text = re.sub(r'<div class="related-section"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div style="margin-top:2rem;">.*?</main>', '', text, flags=re.DOTALL)
    # Remove duplicate hero headers from main
    text = re.sub(r'<div class="feed">\s*class="article-hero"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="feed">\s*class="review-hero"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="feed">\s*<div class="feed-section">\s*<div class="feed-section-body">\s*<div class="story-hero"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    # Clean up the feed/main structure
    text = re.sub(r'<main class="main">\s*<div class="feed">', '<main class="main">', text)
    text = re.sub(r'<div class="feed">\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s*</div>\s*</main>\s*<footer', '</main><footer', text)
    return text

def extract_hero_section(html, fname, cat_label, cat_tag):
    """Extract the hero section with title and tag."""
    title_match = re.search(r'<h1 class="hero-title">(.*?)</h1>', html)
    if not title_match:
        return ""
    title = title_match.group(1).strip()
    
    return f'''  <div id="site-nav"></div>

  <header class="content-header">
    <div class="content-header-inner">
      <span class="tag tag--{cat_tag}">{cat_label}</span>
      <h1 class="content-title">{title}</h1>
    </div>
  </header>

  <main>'''

def extract_body(html, fname, cat_type):
    """Extract body content from source HTML."""
    text = html
    
    # Remove entire nav
    text = re.sub(r'<nav class="nav">.*?</nav>', '', text, flags=re.DOTALL)
    # Remove entire footer
    text = re.sub(r'<footer class="footer">.*?</footer>', '', text, flags=re.DOTALL)
    # Remove scripts
    text = re.sub(r'<script>.*?</script>', '', text, flags=re.DOTALL)
    # Remove Google Fonts links
    text = re.sub(r'<link[^>]*googleapis[^>]*>', '', text)
    text = re.sub(r'<link[^>]*gstatic[^>]*>', '', text)
    # Remove old CSS
    text = re.sub(r'<link[^>]*href="css/style\.css"[^>]*>', '', text)
    
    # Remove AdSense blocks
    text = re.sub(r'<div style="margin:2\.5rem 0;padding:1rem;background:var\(--surface\);border-radius:var\(--radius\);box-shadow:var\(--shadow\);text-align:center;">\s*<ins[^>]*>.*?</ins>\s*<script[^>]*>.*?</script>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="adsense-block".*?</div>', '', text, flags=re.DOTALL)
    
    # Remove share rows
    text = re.sub(r'<div style="display:flex;align-items:center;gap:\.75rem;padding:1\.25rem 0;border-top:1px solid var\(--border\);border-bottom:1px solid var\(--border\);margin:1\.5rem 0;">.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="share-row"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="story-share-row"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    
    # Remove related sections
    text = re.sub(r'<div class="related-section"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div style="margin-top:2rem;">.*?</main>', '', text, flags=re.DOTALL)
    
    # Remove old hero headers inside feed
    text = re.sub(r'<div class="feed">\s*class="article-hero".*?</div>\s*</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="feed">\s*class="review-hero".*?</div>\s*</div>\s*</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="feed">\s*<div class="feed-section">\s*<div class="feed-section-body">\s*<div class="story-hero"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL)
    
    # Remove the <main class="main"><div class="feed"> wrapper structure
    text = re.sub(r'<main class="main">\s*<div class="feed">', '<main class="main">', text)
    text = re.sub(r'<div class="feed">\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s*</div>\s*</main>\s*<footer', '</main><footer', text)
    
    # Now extract content from article-body/story-body/review-body divs
    body_match = re.search(r'<div class="(?:article-body|story-body|review-prose|content-body)"[^>]*>(.*?)</div>\s*</div>\s*</main>', text, flags=re.DOTALL)
    if body_match:
        content = body_match.group(1)
    else:
        # Try just getting everything between article-body and the next closing divs
        body_match = re.search(r'(<div class="(?:article-body|story-body|review-prose)"[^>]*>.*?)</div>\s*<div style="margin:2\.5rem', text, flags=re.DOTALL)
        if body_match:
            content = body_match.group(1)
        else:
            # Last resort: grab everything from max-width content div
            body_match = re.search(r'<div style="max-width:680px;margin:2rem auto 0;">(.*?)</div>\s*<div style="margin:2\.5rem', text, flags=re.DOTALL)
            if body_match:
                content = body_match.group(1)
            else:
                content = re.search(r'<div class="article-body".*?</div>', text, flags=re.DOTALL)
                if content:
                    content = content.group(0)
                else:
                    content = ""
    
    return content

def extract_title(html):
    m = re.search(r'<title>(.*?) \| Bithues</title>', html)
    return m.group(1) if m else "Untitled"

def extract_description(html):
    m = re.search(r'<meta name="description" content="(.*?)"', html)
    return m.group(1) if m else ""

def make_article_page(fname, title, body_content, cat_label, cat_tag):
    """Create an article page with flat HTML structure."""
    tag_class = f"tag--{cat_tag}"
    
    output = TEMPLATE.replace("PAGE TITLE", title, 1)
    output = output.replace("PAGE DESCRIPTION — one clear sentence.", title, 1)
    
    # Replace body content area
    main_match = re.search(r'<main>(.*)<div id="site-footer">', output, flags=re.DOTALL)
    if main_match:
        header = f'''<header class="content-header">
    <div class="content-header-inner">
      <span class="tag {tag_class}">{cat_label}</span>
      <h1 class="content-title">{title}</h1>
    </div>
  </header>

  <main class="content-body">
    {body_content}
  </main>'''
        output = output[:main_match.start()] + f'<main>\n{header}\n</main>' + output[main_match.end():]
    else:
        output = output.replace('<main>\n  <!-- PAGE CONTENT GOES HERE -->\n  </main>', f'<main>\n  <div class="content-body">\n    {body_content}\n  </div>\n  </main>')
    
    return output

def make_review_page(fname, title, body_content, cat_label, cat_tag, asin=None):
    """Create a review page with book cover."""
    tag_class = f"tag--{cat_tag}"
    
    output = TEMPLATE.replace("PAGE TITLE", title, 1)
    output = output.replace("PAGE DESCRIPTION — one clear sentence.", title, 1)
    
    cover_html = ""
    if asin:
        cover_html = f'''<img src="https://images-na.ssl-images-amazon.com/images/I/{asin}._SL500_.jpg"
           class="book-cover-thumb"
           alt="{title} cover"
           loading="lazy"
           onerror="this.style.display='none';this.nextElementSibling.style.display='flex';" />
      <div class="book-cover-placeholder" style="display:none;"></div>'''
    else:
        cover_html = '<div class="book-cover-placeholder"></div>'
    
    review_header = f'''<header class="content-header">
    <div class="content-header-inner">
      <span class="tag {tag_class}">{cat_label}</span>
      <h1 class="content-title">{title}</h1>
    </div>
  </header>

  <main class="content-body">
    <div class="review-header">
      <div class="book-cover-thumb-wrapper">
        {cover_html}
      </div>
      <div class="review-meta">
        <h1>{title}</h1>
      </div>
    </div>
    {body_content}
  </main>'''
    
    main_match = re.search(r'<main>\s*<!-- PAGE CONTENT GOES HERE -->\s*</main>', output)
    if main_match:
        output = output[:main_match.start()] + f'<main>\n{review_header}\n</main>' + output[main_match.end():]
    else:
        output = output.replace('<main>\n  <!-- PAGE CONTENT GOES HERE -->\n  </main>', f'<main>\n{review_header}\n</main>')
    
    return output

def make_story_page(fname, title, body_content, cat_label, cat_tag):
    """Create a story page."""
    return make_article_page(fname, title, body_content, cat_label, cat_tag)

def determine_dest(fname, cat_type):
    """Determine destination subfolder."""
    if cat_type == "review":
        return "reviews"
    elif cat_type == "article":
        return "articles"
    else:
        return "stories"

def process_file(fname):
    source = load_source(fname)
    if not source:
        print(f"  WARNING: {fname} not found, skipping")
        return None
    
    cat_label, cat_type = CATEGORIES[fname]
    asin = ASINS.get(fname)
    title = extract_title(source)
    
    # Extract the actual body content
    body = extract_body(source, fname, cat_type)
    if not body.strip():
        print(f"  WARNING: No body content for {fname}")
        body = "<p>Content unavailable.</p>"
    
    # Make the page
    if cat_type == "review":
        page_html = make_review_page(fname, title, body, cat_label, cat_type, asin)
    else:
        page_html = make_article_page(fname, title, body, cat_label, cat_type)
    
    # Fix any remaining relative paths
    page_html = re.sub(r'href="index\.html"', 'href="/index.html"', page_html)
    page_html = re.sub(r'href="about\.html"', 'href="/about.html"', page_html)
    page_html = re.sub(r'href="browse\.html"', 'href="/browse.html"', page_html)
    page_html = re.sub(r'href="/authors"', 'href="/reviews.html"', page_html)
    page_html = re.sub(r'href="/reviews/home-for-anya/"', 'href="/reviews/home-for-anya.html"', page_html)
    page_html = re.sub(r'href="/reviews/32/"', 'href="/reviews/32.html"', page_html)
    page_html = re.sub(r'href="/reviews/6/"', 'href="/reviews/6.html"', page_html)
    page_html = re.sub(r'href="/stories/american-voices/"', 'href="/stories/american-voices.html"', page_html)
    page_html = re.sub(r'href="/stories/before-the-streetlights-came-on/"', 'href="/stories/before-the-streetlights-came-on.html"', page_html)
    page_html = re.sub(r'href="/stories/blood-ties/"', 'href="/stories/blood-ties.html"', page_html)
    page_html = re.sub(r'href="/articles/reading-challenge-2026/"', 'href="/articles/reading-challenge-2026.html"', page_html)
    page_html = re.sub(r'from="reviews/', 'href="/reviews/', page_html)
    
    dest_folder = determine_dest(fname, cat_type)
    out_name = fname.replace('.html', '.html')
    out_path = os.path.join(DST, dest_folder, out_name)
    
    return {
        'path': out_path,
        'html': page_html,
        'title': title,
        'category': cat_label,
        'cat_type': cat_type,
        'fname': fname,
    }

def build_search_entry(result):
    url = result['path'].replace(DST, '').replace('.html', '.html')
    return {
        'title': result['title'],
        'category': result['category'],
        'url': url,
        'summary': result['title'],
    }

results = []
for fname in FILES:
    print(f"Processing {fname}...")
    r = process_file(fname)
    if r:
        results.append(r)

# Write all pages
search_entries = []
for r in results:
    dest_folder = determine_dest(r['fname'], r['cat_type'])
    out_path = os.path.join(DST, dest_folder, r['fname'])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        f.write(r['html'])
    print(f"  Wrote: {out_path}")
    
    search_entries.append({
        'title': r['title'],
        'category': r['category'],
        'url': f"/{determine_dest(r['fname'], r['cat_type'])}/{r['fname']}",
        'summary': r['title'],
    })

print(f"\nDone! Processed {len(results)} files.")
print("Search entries:")
for e in search_entries:
    print(f"  {e['url']} ({e['category']})")