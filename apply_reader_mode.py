#!/usr/bin/env python3
"""
Bithues Story Reader Mode - Transform all 30 story pages
to an elegant, continuous reader layout.
"""
import os
import re
import sys
from html.parser import HTMLParser

STORIES_DIR = "/Users/mike/.openclaw/workspace-bacottibot/websites/bithues-rebuild-2026-05-13/stories"
ROOT = "/Users/mike/.openclaw/workspace-bacottibot/websites/bithues-rebuild-2026-05-13"

# ─── Story Reader Template ────────────────────────────────────────────────────

READER_CSS = """
/* ─── Story Reader Mode ─────────────────────────────── */
.story-hero {
  text-align: center;
  padding: 48px 24px 40px;
}
.story-hero-inner {
  max-width: var(--max-width);
  margin: 0 auto;
}
.story-hero .tag {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 3px;
  border: 1px solid #5a7a65;
  color: #5a7a65;
  margin-bottom: 20px;
}
.story-hero h1 {
  font-family: var(--font-serif);
  font-size: clamp(28px, 5vw, 42px);
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--color-text);
  line-height: 1.2;
  margin-bottom: 14px;
}
.story-hero .byline {
  font-size: 14px;
  color: var(--color-text-light);
  font-style: italic;
}

.story-hero-image {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 24px;
}
.story-hero-image img {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  border-radius: 4px;
  display: block;
}

.story-ad-section {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 24px 24px 0;
  text-align: center;
}
.story-ad-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-text-light);
  margin-bottom: 8px;
}

/* ─── Reader Container ──────────────────────────────── */
.reader-wrap {
  position: relative;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 48px 24px 80px;
}

/* Bookmark button */
.reader-bookmark {
  position: absolute;
  top: -8px;
  right: 24px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: var(--color-text-light);
  border-radius: 4px;
  transition: color 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.reader-bookmark:hover { color: var(--color-accent); }
.reader-bookmark:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
.reader-bookmark .bm-label { white-space: nowrap; }
.reader-bookmark-tooltip {
  position: absolute;
  right: 0;
  top: calc(100% + 4px);
  background: var(--color-text);
  color: var(--color-surface);
  font-size: 11px;
  font-family: var(--font-sans);
  padding: 5px 10px;
  border-radius: 3px;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s;
}
.reader-bookmark-tooltip.show { opacity: 1; }

/* Progress bar */
.reader-progress-bar {
  position: absolute;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--color-accent);
  width: 0%;
  border-radius: 0 2px 2px 0;
  transition: width 0.1s linear;
}

/* ─── Story Body ─────────────────────────────────────── */
.reader-body {
  font-family: var(--font-serif);
  font-size: 18px;
  line-height: 1.85;
  color: var(--color-text);
}
.reader-body p {
  margin-bottom: 1.5em;
  font-size: 18px;
  line-height: 1.85;
}
.reader-body p:last-child { margin-bottom: 0; }

/* ─── Share/Back Footer ───────────────────────────────── */
.reader-footer {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 32px 24px 48px;
  border-top: 1px solid var(--color-border-light);
  display: flex;
  justify-content: center;
}
.reader-back-link {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-accent);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: color 0.2s;
}
.reader-back-link:hover { color: var(--color-accent-hover); }

@media (max-width: 640px) {
  .reader-body { font-size: 16px; }
  .reader-body p { font-size: 16px; }
  .story-hero h1 { font-size: 28px; }
  .reader-bookmark .bm-label { display: none; }
}
"""

READER_SCRIPT = """
<script>
// Progress bar
(function () {
  var bar = document.getElementById('story-progress-bar');
  var reader = document.getElementById('reader-container');
  if (!bar || !reader) return;

  function updateProgress() {
    var rect = reader.getBoundingClientRect();
    var total = reader.offsetHeight - window.innerHeight;
    var scrolled = Math.max(0, -rect.top);
    var pct = total > 0 ? Math.min(100, (scrolled / total) * 100) : 0;
    bar.style.width = pct + '%';
  }

  window.addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();
})();

// Bookmark / copy link
(function () {
  var btn = document.getElementById('reader-bookmark-btn');
  var tip = document.getElementById('reader-bookmark-tip');
  if (!btn || !tip) return;

  btn.addEventListener('click', function () {
    navigator.clipboard.writeText(window.location.href).then(function () {
      tip.classList.add('show');
      setTimeout(function () { tip.classList.remove('show'); }, 2000);
    }).catch(function () {
      var el = document.createElement('input');
      el.value = window.location.href;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      tip.classList.add('show');
      setTimeout(function () { tip.classList.remove('show'); }, 2000);
    });
  });
})();
</script>
"""

BOOKMARK_SVG = (
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>'
    '<path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>'
    '</svg>'
)


# ─── HTML Parser to extract story parts ────────────────────────────────────────

class StoryExtractor(HTMLParser):
    """Extract title, category, byline, hero_image, and story body HTML.
    Handles both the original content-body format and the new reader-body format.
    """

    def __init__(self):
        super().__init__()
        self.state = 'idle'
        self.in_story_body = False
        self.in_content_image = False
        self.in_content_header = False
        self.title = ''
        self.category = ''
        self.byline = ''
        self.hero_image = None
        self.hero_image_alt = ''
        self.paragraphs = []
        self.current_tag = ''
        self.current_attrs = {}
        self.current_data = ''
        self.in_p = False
        self.p_buf = ''

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', '')
        self.current_tag = tag
        self.current_attrs = attrs_dict

        if self.state == 'idle':
            if tag in ('main', 'article'):
                pass  # container, stay in idle
            elif tag == 'div':
                if 'content-header' in cls or 'review-page-header' in cls:
                    self.in_content_header = True
                    self.state = 'header'
                elif 'content-image' in cls:
                    self.in_content_image = True
                elif 'story-body' in cls or 'reader-body' in cls or 'content-body' in cls or 'review-body' in cls:
                    self.in_story_body = True
                    self.state = 'body'
                elif 'share-bar' in cls:
                    self.state = 'sharebar'

        elif self.state == 'header':
            if tag == 'h1':
                self.current_data = ''
            elif tag == 'span' and ('tag' in cls or 'pill' in cls):
                self.current_data = ''
            elif tag == 'p' and 'content-meta' in cls:
                self.current_data = ''
            elif tag == 'div':
                if 'content-image' in cls:
                    self.in_content_image = True
                elif 'story-body' in cls or 'reader-body' in cls or 'content-body' in cls or 'review-body' in cls:
                    self.in_story_body = True
                    self.state = 'body'
                elif 'share-bar' in cls:
                    self.state = 'sharebar'
                else:
                    # nested div inside header that isn't a content section — stay in header
                    pass

        elif self.state == 'body':
            if tag == 'p':
                self.in_p = True
                self.p_buf = ''
            elif tag == 'div' and 'share-bar' in cls:
                self.state = 'sharebar'

    def handle_endtag(self, tag):
        if self.state == 'header':
            if tag == 'span':
                if 'tag' in self.current_attrs.get('class', ''):
                    self.category = self.current_data.strip()
            elif tag == 'h1':
                self.title = self.current_data.strip()
            elif tag == 'p' and 'content-meta' in self.current_attrs.get('class', ''):
                text = self.current_data.strip()
                if text.startswith('by '):
                    self.byline = text

        elif self.state == 'body':
            if tag == 'p' and self.in_p:
                txt = self.p_buf.strip()
                if txt:
                    self.paragraphs.append(txt)
                self.in_p = False
                self.p_buf = ''
            elif tag == 'div':
                cls = self.current_attrs.get('class', '')
                if 'story-body' in cls or 'reader-body' in cls:
                    self.in_story_body = False
                    self.state = 'sharebar'

    def handle_data(self, data):
        if self.state == 'header':
            if self.current_tag in ('h1', 'span', 'p'):
                self.current_data += data
        if self.in_p:
            self.p_buf += data
        if self.in_content_image and self.current_tag == 'img':
            src = self.current_attrs.get('src', '')
            alt = self.current_attrs.get('alt', '')
            if src:
                self.hero_image = src
                self.hero_image_alt = alt
            self.in_content_image = False


def extract_story(filepath):
    """Return dict with extracted story data."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        raw = f.read()

    slug = os.path.basename(filepath).replace('.html', '')

    # Extract canonical URL
    canonical_match = re.search(r'rel="canonical"[^>]+href="([^"]+)"', raw)
    canonical = canonical_match.group(1) if canonical_match else ''

    # Extract title from <title> tag
    title_match = re.search(r'<title>([^<]+)</title>', raw)
    title_from_tag = ''
    if title_match:
        title_raw = title_match.group(1).strip()
        if '|' in title_raw:
            title_from_tag = title_raw.split('|')[0].strip()
        elif title_raw:
            title_from_tag = title_raw

    # Extract meta description
    desc_match = re.search(r'<meta name="description"[^>]+content="([^"]+)"', raw)
    description = desc_match.group(1) if desc_match else ''

    # Fallback: derive title from description
    if not title_from_tag and description and ' — ' in description:
        title_from_tag = description.split(' — ')[0].strip()

    # Final fallback: derive from slug
    if not title_from_tag:
        title_from_tag = ' '.join(w.capitalize() for w in slug.replace('-', ' '))

    # Parse the HTML
    parser = StoryExtractor()
    try:
        parser.feed(raw)
    except Exception as e:
        print(f"    [PARSE ERROR] {filepath}: {e}")
        return None

    title = parser.title if parser.title else title_from_tag
    category = parser.category if parser.category else 'Short Story'
    byline = parser.byline if parser.byline else 'by Bithues'

    story_body_html = ''
    for p in parser.paragraphs:
        story_body_html += f'<p>{p}</p>\n'

    if not story_body_html:
        print(f"    [NO BODY] {filepath} — no story body found, skipping")
        return None

    return {
        'title': title,
        'category': category,
        'byline': byline,
        'hero_image': parser.hero_image,
        'hero_image_alt': parser.hero_image_alt or title,
        'story_body_html': story_body_html,
        'canonical': canonical,
        'description': description,
        'slug': slug,
    }


# ─── Build output HTML ─────────────────────────────────────────────────────────

def build_reader_page(data):
    slug = data['slug']
    title = data['title']
    category = data['category']
    byline = data['byline']
    hero_image = data['hero_image']
    hero_image_alt = data['hero_image_alt']
    story_body_html = data['story_body_html']
    canonical = data['canonical']
    description = data['description']

    # Check if hero image exists locally
    hero_exists = False
    if hero_image:
        for path in [
            os.path.join(STORIES_DIR, 'images', f'{slug}.jpg'),
            os.path.join(STORIES_DIR, 'images', f'{slug}.png'),
            os.path.join(STORIES_DIR, f'{slug}.jpg'),
            os.path.join(ROOT, hero_image.lstrip('/')),
        ]:
            if os.path.exists(path):
                hero_exists = True
                break

    hero_section = ''
    if hero_image:
        if hero_exists:
            hero_section = f'''
  <div class="story-hero-image">
    <img src="{hero_image}" alt="{hero_image_alt or title}" style="width:100%;max-height:400px;object-fit:cover;border-radius:4px;display:block;">
  </div>'''

    ad_section = '''
  <div class="story-ad-section">
    <p class="story-ad-label">Advertisement</p>
    <ins class="adsbygoogle" style="display:block;width:100%;max-width:600px;margin:0 auto;" data-ad-client="ca-pub-9312870448453345" data-ad-slot="7590828986" data-ad-format="auto" data-full-width-responsive="true"></ins>
  </div>'''

    json_title = title.replace('"', '&quot;')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Bithues</title>
  <meta name="description" content="{description or title + ' — Short Story by Bithues'}">
  <link rel="stylesheet" href="/style.css">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="canonical" href="{canonical}">
  <style>
{READER_CSS}
  </style>
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://www.bithues.com/"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "Stories",
      "item": "https://www.bithues.com/stories"
    }},
    {{
      "@type": "ListItem",
      "position": 3,
      "name": "{json_title} | Bithues"
    }}
  ]
}}
</script>
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{json_title} | Bithues",
  "url": "{canonical}",
  "publisher": {{
    "@type": "Organization",
    "name": "Bithues",
    "url": "https://www.bithues.com"
  }}
}}
</script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9312870448453345" crossorigin="anonymous"></script>
</head>
<body>
  <div id="site-nav"></div>

  <article>
    <!-- Story Header -->
    <header class="story-hero">
      <div class="story-hero-inner">
        <span class="tag">{category}</span>
        <h1>{title}</h1>
        <p class="byline">{byline}</p>
      </div>
    </header>

{hero_section}
{ad_section}

    <!-- Reader Container -->
    <div class="reader-wrap">
      <button id="reader-bookmark-btn" class="reader-bookmark" aria-label="Copy link to this story">
        {BOOKMARK_SVG}
        <span class="bm-label">Share</span>
        <span id="reader-bookmark-tip" class="reader-bookmark-tooltip" aria-live="polite">Link copied!</span>
      </button>
      <div id="story-progress-bar" class="reader-progress-bar" role="progressbar" aria-label="Reading progress" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
      <div id="reader-container">
        <div class="reader-body">
{story_body_html}        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="reader-footer">
      <a href="/stories/" class="reader-back-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M12 5l-7 7 7 7"/></svg>
        All Stories
      </a>
    </footer>
  </article>

  <div id="site-footer"></div>
  <script src="/nav.js"></script>
  <script src="/footer.js"></script>
  <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
{READER_SCRIPT}
</body>
</html>'''


# ─── Main ───────────────────────────────────────────────────────────────────────

def main():
    files = sorted(f for f in os.listdir(STORIES_DIR) if f.endswith('.html'))
    print(f"Found {len(files)} story files\n")

    results = {'ok': [], 'skip': [], 'fail': []}

    for fname in files:
        path = os.path.join(STORIES_DIR, fname)
        slug = fname.replace('.html', '')
        print(f"Processing: {fname}")

        data = extract_story(path)
        if data is None:
            results['skip'].append(fname)
            continue

        try:
            html = build_reader_page(data)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"  ✓ Done: {data['title'][:55]}")
            results['ok'].append(fname)
        except Exception as e:
            import traceback
            print(f"  ✗ FAIL {fname}: {e}")
            traceback.print_exc()
            results['fail'].append(fname)

    print(f"\n{'─'*50}")
    print(f"Done: {len(results['ok'])} ok / {len(results['skip'])} skipped / {len(results['fail'])} failed")
    if results['fail']:
        print("FAILED:", results['fail'])
    if results['skip']:
        print("SKIPPED:", results['skip'])


if __name__ == '__main__':
    main()