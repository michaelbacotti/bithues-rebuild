# Bithues.com — Website Template & Style Documentation

_This document is the canonical reference for rebuilding bithues.com from scratch or adding new pages in the correct format. It documents the complete site structure, HTML templates, CSS system, nav/footer architecture, and all patterns used across the site._

---

## Table of Contents

1. [Site Structure](#1-site-structure)
2. [Page Shell — The Standard HTML Template](#2-page-shell--the-standard-html-template)
3. [CSS Reference](#3-css-reference)
4. [Nav System](#4-nav-system)
5. [Footer System](#5-footer-system)
6. [AdSense Block](#6-adsense-block)
7. [Review Page Structure](#7-review-page-structure)
8. [Article Page Structure](#8-article-page-structure)
9. [Story Page Structure](#9-story-page-structure)
10. [Legal Pages (Privacy, Terms, Contact)](#10-legal-pages-privacy-terms-contact)
11. [Author Pages](#11-author-pages)
12. [Author Personality System](#12-author-personality-system)
13. [All CSS — Full Stylesheet](#13-all-css--full-stylesheet)
14. [Site-Wide Patterns & Constants](#14-site-wide-patterns--constants)

---

## 1. Site Structure

### Directory Tree

```
bithues-rebuild/
├── index.html                    ← Homepage (JS-driven feed from search.json)
├── reviews.html                  ← Reviews listing (JS-driven, filtered to Book Review)
├── articles.html                 ← Articles listing (JS-driven, filtered to Article)
├── stories.html                  ← Stories listing (JS-driven, filtered to Short Story)
├── about.html                    ← About page
├── contact.html                  ← Contact page
├── privacy.html                  ← Privacy policy
├── terms.html                    ← Terms of service
├── search.html                   ← Search page
├── style.css                     ← Main stylesheet
├── nav.js                        ← Dynamic navigation loader
├── footer.js                     ← Dynamic footer loader
├── favicon.svg                   ← SVG favicon
├── apple-touch-icon.png
├── site.webmanifest
├── ads.txt
├── search.json                   ← Search index (used by JS feed + search)
├── add_schema.py                 ← JSON-LD injection script
├── add_schema2.py
├── _add_links_v2.py
├── fix_amazon_images.py
│
├── articles/                     ← Article pages (URL slugs, no dates in filenames)
│   ├── best-books-book-clubs.html
│   ├── best-books-for-entrepreneurs.html
│   ├── best-books-summer-2026.html
│   ├── best-first-time-authors.html
│   ├── best-historical-fiction-beginners.html
│   ├── book-of-enoch-2026.html
│   ├── books-like-anxious-people.html
│   ├── books-like-atomic-habits.html
│   ├── books-like-dark-matter.html
│   ├── books-like-dune.html
│   ├── books-like-enders-game.html
│   ├── books-like-hyperion.html
│   ├── books-like-physics-of-time.html
│   ├── books-like-the-midnight-library.html
│   ├── books-like-the-martian.html
│   ├── books-like-the-name-of-the-wind.html
│   ├── business-leadership-guide.html
│   ├── complete-fantasy-encyclopedia.html
│   ├── dna-ancestry-historical-fiction.html
│   ├── fantasy-for-beginners.html
│   ├── frog-and-toad-classic-childrens-books.html
│   ├── horror-for-beginners.html
│   ├── hopepunk-beginners-guide.html
│   ├── how-to-read-more-books.html
│   ├── how-we-review-books.html
│   ├── little-mike-series.html
│   ├── memoir-biography-guide.html
│   ├── mesoamerican-fiction-homeschool-guide.html
│   ├── meet-indie-authors.html
│   ├── quantum-physics-beginners.html
│   ├── quantum-physics-beginners-guide.html
│   ├── reading-order-guide-high-fantasy.html
│   ├── reading-challenge-2026.html
│   ├── speed-reading-basics.html
│   ├── a-global-heartbeat-called-michael-jackson.html
│   └── images/                   ← Article hero images
│
├── reviews/                      ← Book review pages (URL slugs)
│   ├── beyond-the-veil.html
│   ├── blood-ember.html
│   ├── consciousness-in-higher-dimensional-spacetime.html
│   ├── cords-of-empire.html
│   ├── dawn-of-civilization.html
│   ├── disclosure-2026.html
│   ├── discovering-washington-dc.html
│   ├── echoes-of-aetheris.html
│   ├── echoes-of-transcendence.html
│   ├── first-contact-diary.html
│   ├── horizonte-rojo.html
│   ├── little-mike-builds-a-robot.html
│   ├── little-mike-fun-at-the-beach.html
│   ├── little-mike-learns-to-fly.html
│   ├── living-with-a-moving-planet.html
│   ├── men-of-three-seas.html
│   ├── microbiology-abcs.html
│   ├── mindful-memory.html
│   ├── mythic-menagerie.html
│   ├── otomi.html
│   ├── power-of-changing-your-mind.html
│   ├── red-horizon.html
│   ├── resonance-drift.html
│   ├── richmond-cipher.html
│   ├── the-burning-song.html
│   ├── the-martian.html
│   ├── the-orchardist-harvest.html
│   ├── the-perfection-cycle.html
│   ├── the-physics-of-time.html
│   ├── the-quiet-hours.html
│   ├── time-investing.html
│   ├── veiled-presence.html
│   └── ...
│
├── stories/                     ← Original short story pages
│   ├── jaspers-flight.html
│   ├── the-harvest.html
│   ├── the-last-garden.html
│   ├── the-last-song.html
│   ├── the-weight-of-summer-light.html
│   └── images/
│
├── authors/                     ← Author pages (pen name slugs)
│   ├── AUTHORS.md              ← Author personality system documentation
│   ├── eleanor-ashford.html
│   ├── eleanor-ashford.md
│   ├── marcus-cole.html
│   ├── marcus-cole.md
│   ├── julian-cross.html
│   ├── julian-cross.md
│   ├── sarah-voss.html
│   ├── sarah-voss.md
│   ├── david-okonkwo.html
│   └── david-okonkwo.md
│
├── qa-reports/                  ← QA outputs
├── test-results/                ← Test failure screenshots
└── _archive/                    ← Deleted file archives
```

### File Naming Conventions

- **URL slugs only** — no dates, no category prefixes in filenames
- Format: `kebab-case.html` (e.g., `the-martian.html`, not `the-martian-review.html`)
- Article images: stored in `/articles/images/`, named to match article slug
- Review images: Amazon image URLs, cover dimensions ~110px wide

### Page Categories

| Category | Directory | CSS Class | Pill Class | search.json `category` |
|----------|----------|-----------|-----------|------------------------|
| Book Review | `/reviews/` | `.review-body` | `.pill-book-review` | `Book Review` |
| Article | `/articles/` | `.article-body` | `.pill-article` | `Article` |
| Short Story | `/stories/` | `.story-body` | `.pill-short-story` | `Short Story` |

---

## 2. Page Shell — The Standard HTML Template

_Every page on bithues.com follows this structure. Extract from `index.html`._

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title | Bithues</title>
  <meta name="description" content="Meta description here.">
  <link rel="stylesheet" href="/style.css">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="canonical" href="https://www.bithues.com/PAGE-SLUG">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9312870448453345" crossorigin="anonymous"></script>
</head>
<body>

  <div id="site-nav"></div>

  <!-- PAGE CONTENT HERE -->

  <div id="site-footer"></div>

  <script src="/nav.js"></script>
  <script src="/footer.js"></script>
</body>
</html>
```

### Element-by-Element Notes

| Element | Purpose |
|---------|---------|
| `<meta charset="UTF-8">` | Always first in `<head>` |
| `<meta name="viewport">` | Mobile responsive |
| `<title>` | Format: `Page Title | Bithues` |
| `<meta name="description">` | One clear sentence, 150–160 chars |
| `<link rel="stylesheet" href="/style.css">` | Always `/style.css` (root-relative) |
| `<link rel="icon" type="image/svg+xml" href="/favicon.svg">` | SVG favicon |
| `<link rel="apple-touch-icon" href="/apple-touch-icon.png">` | iOS home screen icon |
| `<link rel="manifest" href="/site.webmanifest">` | PWA manifest |
| `<link rel="canonical">` | Full canonical URL https://www.bithues.com/... |
| `<script async src="...googlesyndication.com/...">` | AdSense, always in `<head>` |
| `<div id="site-nav"></div>` | nav.js injects here |
| `<div id="site-footer"></div>` | footer.js injects here |
| `<script src="/nav.js">` | At end of `<body>`, before `</body>` |
| `<script src="/footer.js">` | At end of `<body>`, before `</body>` |

---

## 3. CSS Reference

### `:root` Variables (extracted from `style.css`)

```css
:root {
  --color-bg: #FAF8F5;
  --color-surface: #FFFFFF;
  --color-text: #3d2b1f;
  --color-text-muted: #5a4a3a;
  --color-text-light: #8a7a6a;
  --color-accent: #8b6914;
  --color-accent-hover: #a67c00;
  --color-border: #d9d3cc;
  --color-border-light: #f0ebe3;
  --color-tag-review: #c8a96e;
  --color-tag-review-bg: #c8a96e;
  --color-tag-article: #7bafc4;
  --color-tag-article-bg: #7bafc4;
  --color-tag-story: #7c9e87;
  --color-tag-story-bg: #7c9e87;
  --font-serif: 'Libre Baskerville', Georgia, 'Times New Roman', serif;
  --font-sans: 'Source Sans 3', 'Helvetica Neue', Arial, sans-serif;
  --max-width: 680px;
  --max-width-wide: 1100px;
}
```

### Key CSS Classes

#### `.main` — Main content wrapper
```css
.main { max-width: var(--max-width); margin: 0 auto; padding: 48px 24px 80px; }
```

#### `.feed` — Vertical card list container
```css
.feed { display: flex; flex-direction: column; }
```

#### `.card` — Feed/card item
```css
.card { padding: 2rem 0; border-bottom: 1px solid var(--color-border); }
.card:last-child { border-bottom: none; }
.card-meta-top { display: flex; align-items: center; gap: 12px; margin-bottom: 0.6rem; }
.card-title { font-family: var(--font-serif); font-size: 1.45rem; font-weight: 700; line-height: 1.3; margin-bottom: 0.7rem; letter-spacing: -0.01em; color: var(--color-text); }
.card-title a { color: inherit; }
.card-title a:hover { color: var(--color-accent); text-decoration: underline; }
.card-excerpt { font-size: 16px; color: var(--color-text-muted); line-height: 1.7; display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden; -webkit-line-clamp: 3; }
.card[data-category="Book Review"] .card-excerpt { -webkit-line-clamp: 2; }
.card[data-category="Short Story"] .card-excerpt { -webkit-line-clamp: 4; }
```

#### `.hero` — Page header
```css
.hero { border-bottom: 1px solid var(--color-border-light); padding: 72px 24px 64px; text-align: center; }
.hero-inner { max-width: var(--max-width); margin: 0 auto; }
.hero-title { font-family: var(--font-serif); font-size: 52px; font-weight: 700; letter-spacing: -0.03em; color: var(--color-text); line-height: 1.15; }
.hero-tagline { font-size: 18px; color: var(--color-text-muted); margin-top: 12px; line-height: 1.6; }
.hero--small { padding: 48px 24px 40px; }
.hero--small .hero-title { font-size: 40px; }
```

#### `.content-header` — Article/story page header
```css
.content-header { padding: 48px 24px 40px; text-align: center; }
.content-header-inner { max-width: var(--max-width); margin: 0 auto; }
.content-title { font-family: var(--font-serif); font-size: 36px; font-weight: 700; letter-spacing: -0.02em; color: var(--color-text); line-height: 1.2; margin-bottom: 16px; }
.content-meta { font-size: 14px; color: var(--color-text-light); margin-top: 12px; }
```

#### `.content-body` — Article/story body wrapper
```css
.content-body { max-width: var(--max-width); margin: 0 auto; padding: 0 24px 80px; font-size: 17px; line-height: 1.8; }
.content-body p { margin-bottom: 1.4em; }
.content-body h2 { font-family: var(--font-serif); font-size: 24px; font-weight: 700; margin: 2em 0 0.6em; color: var(--color-text); }
.content-body blockquote { border-left: 3px solid var(--color-accent); padding-left: 20px; margin: 1.5em 0; color: var(--color-text-muted); font-style: italic; }
```

#### `.about-body` — Legal/about page body
```css
.about-body { max-width: var(--max-width); margin: 0 auto; padding: 48px 24px 80px; font-size: 17px; line-height: 1.8; }
.about-body h2 { font-family: var(--font-serif); font-size: 24px; font-weight: 700; margin: 2em 0 0.6em; }
```

#### `.tag` classes — Category pills
```css
/* Base pill */
[class^="pill-"] { display: inline-block; font-size: 10px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; padding: 3px 8px; border-radius: 3px; background: transparent; }

/* Book Review pill */
.pill-book-review { color: #8a6f3e; border: 1px solid #8a6f3e; }
/* Article pill */
.pill-article { color: #4a7490; border: 1px solid #4a7490; }
/* Short Story pill */
.pill-short-story { color: #5a7a65; border: 1px solid #5a7a65; }

/* Legacy tag classes */
.tag { display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; padding: 3px 8px; border-radius: 3px; line-height: 1.5; background: transparent; border: 1px solid currentColor; }
.tag--review { color: #8a6f3e; border-color: #8a6f3e; }
.tag--article { color: #4a7490; border-color: #4a7490; }
.tag--story { color: #5a7a65; border-color: #5a7a65; }
```

#### `.share-bar` — Social share buttons
```css
.share-bar { display: flex; align-items: center; gap: 10px; max-width: var(--max-width); margin: 16px auto 32px; padding: 16px 24px; border-top: 1px solid #e8e4dd; border-bottom: 1px solid #e8e4dd; }
.share-label { font-size: 11px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #999; margin-right: 4px; }
.share-btn { display: inline-flex; align-items: center; gap: 5px; padding: 7px 12px 7px 16px; border-radius: 4px; font-size: 12px; text-decoration: none; border: 1px solid #8a6f3e; background: transparent; cursor: pointer; font-family: inherit; color: #8a6f3e; transition: opacity 0.15s; }
.share-btn:hover { opacity: 0.7; }
```

#### `.related-links` — "Continue Reading" section
```css
.related-links { max-width: var(--max-width); margin: 0 auto 40px; padding: 0 24px; }
```

#### `.footer`
```css
.footer { border-top: 1px solid var(--color-border-light); padding: 40px 24px; margin-top: 40px; }
.footer-inner { max-width: var(--max-width-wide); margin: 0 auto; display: flex; flex-wrap: wrap; gap: 24px; align-items: center; }
.footer-brand { font-family: var(--font-serif); font-size: 18px; font-weight: 700; color: var(--color-text); }
.footer-brand:hover { color: var(--color-accent); }
.footer-nav { display: flex; gap: 20px; }
.footer-nav a { font-size: 14px; color: var(--color-text-muted); }
.footer-nav a:hover { color: var(--color-accent); }
.footer-copy { font-size: 13px; color: var(--color-text-light); margin-left: auto; }
```

#### `.review-page-header` — Review page header structure
```css
.review-page-header { max-width: 680px; margin: 48px auto 40px; padding: 0 24px; }
.review-body p { margin-bottom: 1.4em; line-height: 1.8; }
.review-body h2 { margin-top: 2em; margin-bottom: 0.6em; font-size: 1.1rem; font-weight: 600; color: #3a2e1e; }
```

#### `.nav`
```css
.nav { position: sticky; top: 0; background: rgba(250, 248, 245, 0.95); backdrop-filter: blur(8px); border-bottom: 1px solid var(--color-border-light); z-index: 100; }
.nav-inner { max-width: var(--max-width-wide); margin: 0 auto; padding: 0 24px; display: flex; align-items: center; gap: 32px; height: 60px; }
.nav-logo { font-family: var(--font-serif); font-size: 22px; font-weight: 700; color: var(--color-text); letter-spacing: -0.02em; }
.nav-logo:hover { color: var(--color-accent); }
.nav-links { display: flex; gap: 24px; }
.nav-link { font-size: 15px; font-weight: 500; color: var(--color-text-muted); transition: color 0.2s; }
.nav-link:hover, .nav-link.active { color: var(--color-accent); }
```

#### `.article-hero` — Hero image wrapper
```css
.article-hero { margin: 1.5rem 0 2rem; border-radius: 4px; overflow: hidden; }
.article-hero img { width: 100%; height: auto; display: block; }
```

#### `.section-header`
```css
.section-header { display: flex; align-items: baseline; gap: 16px; margin-bottom: 32px; padding-bottom: 12px; border-bottom: 2px solid var(--color-border); }
.section-title { font-family: var(--font-serif); font-size: 22px; font-weight: 700; color: var(--color-text); }
.section-link { font-size: 14px; color: var(--color-accent); margin-left: auto; }
```

#### `.book-grid`
```css
.book-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1.2rem; margin: 1.5rem 0; }
.book-card { text-align: center; }
.book-card img { width: 120px; height: auto; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.12); }
.book-card p { font-size: 0.85rem; margin: 0.5rem 0; line-height: 1.4; }
.book-card a { color: var(--accent, #8b6914); font-weight: 600; }
```

---

## 4. Nav System

**File:** `/nav.js`
**Injection target:** `<div id="site-nav"></div>`

nav.js is an IIFE that builds the full `<nav>` element and injects it into `#site-nav`. It also implements the search dropdown.

### Nav Structure Produced

```html
<nav class="nav">
  <div class="nav-inner">
    <a href="/" class="nav-logo">Bithues</a>
    <div class="nav-links">
      <a href="/which-book-should-i-read-next/" class="nav-link">Find Books</a>
      <a href="/reviews.html" class="nav-link">Reviews</a>
      <a href="/articles.html" class="nav-link">Articles</a>
      <a href="/stories.html" class="nav-link">Stories</a>
      <a href="/about.html" class="nav-link">About</a>
    </div>
    <div class="nav-search">
      <button class="search-toggle" aria-label="Search">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
      </button>
      <div class="search-panel">
        <input type="text" class="search-input" placeholder="Search..." autocomplete="off">
        <div class="search-results"></div>
      </div>
    </div>
  </div>
</nav>
```

### Nav Links (all pages)

| Text | href |
|------|------|
| Bithues | `/` |
| Find Books | `/which-book-should-i-read-next/` |
| Reviews | `/reviews.html` |
| Articles | `/articles.html` |
| Stories | `/stories.html` |
| About | `/about.html` |

### Search Behavior
- Click toggle → opens panel, focuses input
- `Escape` key → closes panel, clears input
- `Enter` key → navigates to `/search.html?q=<query>`
- 2+ characters → live searches `/search.json` (title, category, summary), shows top 6 results
- Click outside → closes panel

---

## 5. Footer System

**File:** `/footer.js`
**Injection target:** `<div id="site-footer"></div>`

footer.js is an IIFE that builds the full `<footer>` element and injects it into `#site-footer`.

### Footer Structure Produced

```html
<footer class="footer">
  <div class="footer-inner">
    <a href="/" class="footer-brand">Bithues</a>
    <nav class="footer-nav">
      <a href="/which-book-should-i-read-next/">Find Books</a>
      <a href="/reviews.html">Reviews</a>
      <a href="/articles.html">Articles</a>
      <a href="/stories.html">Stories</a>
      <a href="/about.html">About</a>
      <a href="/contact.html">Contact</a>
      <a href="/terms.html">Terms</a>
      <a href="/privacy.html">Privacy</a>
    </nav>
    <p class="footer-copy">&copy; 2026 Bithues. All rights reserved.</p>
  </div>
</footer>
```

Note: Year is dynamically generated via `new Date().getFullYear()`.

---

## 6. AdSense Block

Place between the closing `</article>` (or last content) and `<div id="site-footer">`.

### HTML

```html
<div style="margin:2rem 0;padding:.75rem;background:var(--surface);border-radius:var(--radius);text-align:center;">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9312870448453345" data-ad-slot="7590828986" data-ad-format="auto" data-full-width-responsive="true"></ins>
</div>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
```

### Publisher ID
```
ca-pub-9312870448453345
```

### Ad Slot
```
7590828986
```

---

## 7. Review Page Structure

**Example file:** `/reviews/the-martian.html`

### Complete Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Martian — Review | Bithues</title>
  <meta name="description" content="Andy Weir's debut novel turned the hard-science sci-fi genre on its head...">
  <link rel="stylesheet" href="/style.css">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <style>
    .review-page-header {
      max-width: 680px;
      margin: 48px auto 40px;
      padding: 0 24px;
    }
    .review-body p {
      margin-bottom: 1.4em;
      line-height: 1.8;
    }
    .review-body h2 {
      margin-top: 2em;
      margin-bottom: 0.6em;
      font-size: 1.1rem;
      font-weight: 600;
      color: #3a2e1e;
    }
  </style>
  <link rel="canonical" href="https://www.bithues.com/reviews/the-martian">
  <!-- JSON-LD BreadcrumbList -->
  <!-- JSON-LD Article -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9312870448453345" crossorigin="anonymous"></script>
</head>
<body>
  <div id="site-nav"></div>

  <main class="main">
    <article class="content-article">

      <!-- HEADER: review-page-header -->
      <div class="review-page-header">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
          <span class="pill pill-book-review">Book Review</span>
          <span style="font-size:12px; color:#999;">January 2026</span>
        </div>
        <h1 style="font-size:2rem; line-height:1.2; margin:0 0 20px; color:#2c1f14;">The Martian</h1>
        <div style="display:flex; gap:24px; align-items:flex-start;">
          <a href="https://www.amazon.com/dp/B082BHWQCJ?tag=michaelbacoti-20" target="_blank" rel="noopener" style="flex-shrink:0;">
            <img src="https://images-na.ssl-images-amazon.com/images/P/B082BHWQCJ.01._SX150_.jpg" alt="The Martian book cover"
                 style="width:110px; border-radius:3px; box-shadow:0 2px 10px rgba(0,0,0,0.12); display:block;">
          </a>
          <div>
            <p style="margin:0 0 4px; font-size:15px; color:#3a2e1e;">by Andy Weir</p>
            <p style="margin:0 0 0; font-size:12px; color:#888; letter-spacing:0.03em;">Science Fiction</p>
          </div>
        </div>
      </div>

      <!-- BODY: review-body -->
      <div class="review-body" style="max-width:680px; margin:0 auto; padding:0 24px 48px;">
        <p>Review paragraphs go here...</p>
        <!-- Amazon CTA -->
        <div style="margin:32px 0 16px; padding:20px 0; border-top:1px solid #e8e4dd; border-bottom:1px solid #e8e4dd; text-align:center;">
          <p style="font-size:13px; color:#888; margin:0 0 10px; letter-spacing:0.04em; text-transform:uppercase;">Enjoyed this review?</p>
          <a href="https://www.amazon.com/dp/B082BHWQCJ?tag=michaelbacoti-20" target="_blank" rel="noopener"
             style="display:inline-block; padding:10px 28px; border:1px solid #8a6f3e; color:#8a6f3e; font-size:13px; text-decoration:none; border-radius:3px; letter-spacing:0.05em;">
            Buy on Amazon &rarr;
          </a>
        </div>
      </div>
    </article>
  </main>

  <!-- SHARE BAR -->
  <div class="share-bar"> ... </div>

  <!-- RELATED LINKS -->
  <div class="related-links">
    <h3 style="...">Continue Reading</h3>
    <div style="...">
      <a href="/..." style="...">...</a>
    </div>
  </div>

  <!-- AdSense -->
  <div style="margin:2rem 0;padding:.75rem;background:var(--surface);border-radius:var(--radius);text-align:center;">
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9312870448453345" data-ad-slot="7590828986" data-ad-format="auto" data-full-width-responsive="true"></ins>
  </div>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>

  <div id="site-footer"></div>
  <script src="/nav.js"></script>
  <script src="/footer.js"></script>
</body>
</html>
```

### Amazon Affiliate Link Format

```
https://www.amazon.com/dp/<ASIN>?tag=michaelbacoti-20
```

Replace `<ASIN>` with the book's Amazon Standard Identification Number.

### Star Ratings
Star ratings are **not used** on Bithues reviews. Instead, qualitative language is used to convey quality (see Author Personality System).

---

## 8. Article Page Structure

**Example file:** `/articles/horror-for-beginners.html`

### Complete Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Why We Read Horror: The Power of Fear | Bithues</title>
  <meta name="description" content="Horror genre guide — one clear sentence.">
  <link rel="stylesheet" href="/style.css">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="canonical" href="https://www.bithues.com/articles/horror-for-beginners">
  <!-- JSON-LD BreadcrumbList -->
  <!-- JSON-LD Article -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9312870448453345" crossorigin="anonymous"></script>
</head>
<body>
  <div id="site-nav"></div>

  <main>
    <div class="content-header">
      <div class="content-header-inner">
        <span class="tag tag--article">Article</span>
        <h1 class="content-title">Why We Read Horror: The Power of Fear</h1>
      </div>
    </div>

    <!-- OPTIONAL: Hero image -->
    <div class="content-image">
      <img src="/articles/images/horror-for-beginners.jpg" alt="Horror Fiction for Beginners" style="width:100%;max-height:400px;object-fit:cover;border-radius:4px;margin-bottom:1.5rem;">
    </div>

    <!-- Body -->
    <div class="content-body">
      <p>Article content...</p>
    </div>
  </main>

  <!-- SHARE BAR -->
  <div class="share-bar"> ... </div>

  <!-- RELATED LINKS -->
  <div class="related-links"> ... </div>

  <!-- AdSense -->
  ...

  <div id="site-footer"></div>
  <script src="/nav.js"></script>
  <script src="/footer.js"></script>
</body>
</html>
```

### Article Header Structure
- `.content-header` (centered, padded)
  - `.content-header-inner` (max-width wrapper)
    - `<span class="tag tag--article">Article</span>`
    - `<h1 class="content-title">...</h1>`

### Article Hero Image
- Optional, placed after `.content-header`, before `.content-body`
- Container: `<div class="content-image">`
- Image: full-width, max-height 400px, object-fit cover, border-radius 4px

---

## 9. Story Page Structure

**Example file:** `/stories/jaspers-flight.html`

### Complete Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jasper's Flight — Story | Bithues</title>
  <meta name="description" content="Jasper's Flight — Story — Short Story by Bithues">
  <link rel="stylesheet" href="/style.css">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <style>
    .story-body p { margin-bottom: 1.5em; line-height: 1.85; font-size: 17px; }
  </style>
  <link rel="canonical" href="https://www.bithues.com/stories/jaspers-flight">
  <!-- JSON-LD -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9312870448453345" crossorigin="anonymous"></script>
</head>
<body>
  <div id="site-nav"></div>

  <header class="content-header">
    <div class="content-header-inner">
      <span class="tag tag--story">Short Story</span>
      <h1 class="content-title">Jasper's Flight — Story</h1>
      <p class="content-meta">by Bithues</p>
    </div>
  </header>

  <!-- Optional hero image -->
  <div class="content-image">
    <img src="/stories/images/jaspers-flight.jpg" alt="Jasper's Flight — Story" style="...">
  </div>

  <!-- Story body -->
  <div class="content-body story-body">
    <p>The morning Jasper woke with wings...</p>
    <!-- story paragraphs -->
  </div>

  <!-- SHARE BAR -->
  <div class="share-bar"> ... </div>

  <!-- RELATED LINKS -->
  <div class="related-links"> ... </div>

  <!-- AdSense -->
  ...

  <div id="site-footer"></div>
  <script src="/nav.js"></script>
  <script src="/footer.js"></script>
</body>
</html>
```

### Story Page Patterns
- Tag: `<span class="tag tag--story">Short Story</span>`
- Author line: `<p class="content-meta">by Bithues</p>` (inside `.content-header-inner`)
- Story body: uses `class="story-body"` on `.content-body`
- `.story-body p` styles: margin-bottom 1.5em, line-height 1.85, font-size 17px

---

## 10. Legal Pages (Privacy, Terms, Contact)

**Example files:** `privacy.html`, `terms.html`, `contact.html`

All three use the same structure: `.hero` + `.about-body`.

### Structure

```html
<header class="hero">
  <div class="hero-inner">
    <h1 class="hero-title">Page Title</h1>
    <p class="hero-tagline">Subtitle or description.</p>
  </div>
</header>

<div class="about-body">
  <p>Content...</p>
  <h2>Section heading</h2>
  <p>More content...</p>
</div>

<!-- AdSense block -->
...

<div id="site-footer"></div>
<script src="/nav.js"></script>
<script src="/footer.js"></script>
```

### Privacy Page Extras
- `<link rel="apple-touch-icon" href="/apple-touch-icon.png">`
- `<link rel="manifest" href="/site.webmanifest">`
- Email: `hello@bithues.com`

---

## 11. Author Pages

### `/authors/AUTHORS.md`

The complete author personality system documentation. Defines 5 pen name personalities with coverage areas, voice rules, and assignment guidelines.

### Individual Author `.md` Profiles

Each author has a `.md` profile file (e.g., `eleanor-ashford.md`) containing:
- Profile narrative (background, age, location, strengths, weaknesses)
- Prose style description
- Sample sentence
- Coverage areas
- Review cadence
- Voice checklist

### Individual Author `.html` Pages

Minimal HTML pages (e.g., `eleanor-ashford.html`) — placeholder pages with:
- `<h1>` with author name (lowercase)
- Short description
- "Back to Bithues" link

---

## 12. Author Personality System

### The Five Pen Names

| Name | Coverage |
|------|----------|
| **Eleanor Ashford** | Literary fiction, translated lit, historical, short story collections, reading memoirs |
| **Marcus Cole** | SF, fantasy, horror, graphic novels, genre craft analysis |
| **Julian Cross** | Political fiction, social novels, memoirs, publishing industry, essays |
| **Sarah Voss** | Short story collections, flash fiction, debut novels, small press, experimental |
| **David Okonkwo** | History, biography, business, thrillers, "Which Book to Read Next" guides |

### Fallback Byline

`Bithues Editorial` — used for site-level content (best-of lists, reading challenges, announcements, homepage features).

### Amazon Affiliate Tag

```
?tag=michaelbacoti-20
```

---

## 13. All CSS — Full Stylesheet

The complete `style.css` is provided below. This is the **entire** stylesheet used across all pages.

```css
/* ============================================
   Bithues — Main Stylesheet
   Literary, warm, text-forward design
   Flat HTML — no build step
   ============================================ */

:root {
  --color-bg: #FAF8F5;
  --color-surface: #FFFFFF;
  --color-text: #3d2b1f;
  --color-text-muted: #5a4a3a;
  --color-text-light: #8a7a6a;
  --color-accent: #8b6914;
  --color-accent-hover: #a67c00;
  --color-border: #d9d3cc;
  --color-border-light: #f0ebe3;
  --color-tag-review: #c8a96e;
  --color-tag-review-bg: #c8a96e;
  --color-tag-article: #7bafc4;
  --color-tag-article-bg: #7bafc4;
  --color-tag-story: #7c9e87;
  --color-tag-story-bg: #7c9e87;
  --font-serif: 'Libre Baskerville', Georgia, 'Times New Roman', serif;
  --font-sans: 'Source Sans 3', 'Helvetica Neue', Arial, sans-serif;
  --max-width: 680px;
  --max-width-wide: 1100px;
}

/* Reset */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }

body {
  font-family: var(--font-sans);
  font-size: 17px;
  line-height: 1.7;
  color: var(--color-text);
  background-color: var(--color-bg);
  -webkit-font-smoothing: antialiased;
}

a { color: var(--color-accent); text-decoration: none; transition: color 0.2s; }
a:hover { color: var(--color-accent-hover); }

/* ============================================
   Navigation
   ============================================ */
.nav {
  position: sticky;
  top: 0;
  background: rgba(250, 248, 245, 0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--color-border-light);
  z-index: 100;
}

.nav-inner {
  max-width: var(--max-width-wide);
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 32px;
  height: 60px;
}

.nav-logo {
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.02em;
}
.nav-logo:hover { color: var(--color-accent); }

.nav-links { display: flex; gap: 24px; }
.nav-link {
  font-size: 15px;
  font-weight: 500;
  color: var(--color-text-muted);
  transition: color 0.2s;
}
.nav-link:hover, .nav-link.active { color: var(--color-accent); }

/* ============================================
   Hero
   ============================================ */
.hero {
  border-bottom: 1px solid var(--color-border-light);
  padding: 72px 24px 64px;
  text-align: center;
}
.hero-inner { max-width: var(--max-width); margin: 0 auto; }
.hero-title {
  font-family: var(--font-serif);
  font-size: 52px;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--color-text);
  line-height: 1.15;
}
.hero-tagline {
  font-size: 18px;
  color: var(--color-text-muted);
  margin-top: 12px;
  line-height: 1.6;
}

.hero--small { padding: 48px 24px 40px; }
.hero--small .hero-title { font-size: 40px; }

/* ============================================
   Main Layout
   ============================================ */
.main { max-width: var(--max-width); margin: 0 auto; padding: 48px 24px 80px; }

/* ============================================
   Feed
   ============================================ */
.feed { display: flex; flex-direction: column; }

/* ============================================
   Article Cards — Stacked Vertical Layout
   ============================================ */
.card {
  padding: 2rem 0;
  border-bottom: 1px solid var(--color-border);
}
.card:last-child { border-bottom: none; }

.card-meta-top {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 0.6rem;
}

.card-date {
  font-size: 12px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-text-light);
}

.card-title {
  font-family: var(--font-serif);
  font-size: 1.45rem;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: 0.7rem;
  letter-spacing: -0.01em;
  color: var(--color-text);
}
.card-title a { color: inherit; }
.card-title a:hover { color: var(--color-accent); text-decoration: underline; }

.card-excerpt {
  font-size: 16px;
  color: var(--color-text-muted);
  line-height: 1.7;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  -webkit-line-clamp: 3;
}

.card[data-category="Book Review"] .card-excerpt { -webkit-line-clamp: 2; }
.card[data-category="Short Story"] .card-excerpt { -webkit-line-clamp: 4; }

/* ============================================
   Tags / Category Pills
   ============================================ */
[class^="pill-"] {
  display: inline-block;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 3px;
  background: transparent;
}

.pill-book-review { color: #8a6f3e; border: 1px solid #8a6f3e; }
.pill-short-story { color: #5a7a65; border: 1px solid #5a7a65; }
.pill-article { color: #4a7490; border: 1px solid #4a7490; }

.tag {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 3px;
  line-height: 1.5;
  background: transparent;
  border: 1px solid currentColor;
}
.tag--review { color: #8a6f3e; border-color: #8a6f3e; }
.tag--article { color: #4a7490; border-color: #4a7490; }
.tag--story { color: #5a7a65; border-color: #5a7a65; }
.tag--genre { background: var(--color-border-light); color: var(--color-text-muted); border-color: transparent; }

/* ============================================
   Section Headers
   ============================================ */
.section-header {
  display: flex;
  align-items: baseline;
  gap: 16px;
  margin-bottom: 32px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--color-border);
}
.section-title {
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text);
}
.section-link { font-size: 14px; color: var(--color-accent); margin-left: auto; }

/* ============================================
   Content Pages (Reviews, Articles, Stories)
   ============================================ */
.content-header { padding: 48px 24px 40px; text-align: center; }
.content-header-inner { max-width: var(--max-width); margin: 0 auto; }

.content-title {
  font-family: var(--font-serif);
  font-size: 36px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--color-text);
  line-height: 1.2;
  margin-bottom: 16px;
}

.content-meta { font-size: 14px; color: var(--color-text-light); margin-top: 12px; }

.content-body {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 24px 80px;
  font-size: 17px;
  line-height: 1.8;
}
.content-body p { margin-bottom: 1.4em; }
.content-body h2 {
  font-family: var(--font-serif);
  font-size: 24px;
  font-weight: 700;
  margin: 2em 0 0.6em;
  color: var(--color-text);
}
.content-body blockquote {
  border-left: 3px solid var(--color-accent);
  padding-left: 20px;
  margin: 1.5em 0;
  color: var(--color-text-muted);
  font-style: italic;
}

/* ============================================
   About Page
   ============================================ */
.about-body {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 48px 24px 80px;
  font-size: 17px;
  line-height: 1.8;
}
.about-body h2 {
  font-family: var(--font-serif);
  font-size: 24px;
  font-weight: 700;
  margin: 2em 0 0.6em;
}

/* ============================================
   Footer
   ============================================ */
.footer {
  border-top: 1px solid var(--color-border-light);
  padding: 40px 24px;
  margin-top: 40px;
}
.footer-inner {
  max-width: var(--max-width-wide);
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  align-items: center;
}
.footer-brand {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
}
.footer-brand:hover { color: var(--color-accent); }
.footer-nav { display: flex; gap: 20px; }
.footer-nav a { font-size: 14px; color: var(--color-text-muted); }
.footer-nav a:hover { color: var(--color-accent); }
.footer-copy { font-size: 13px; color: var(--color-text-light); margin-left: auto; }

/* ============================================
   Book Cover Thumbnails (Review Pages)
   ============================================ */
.review-header {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.book-cover-thumb {
  width: 75px;
  height: auto;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  flex-shrink: 0;
  margin-top: 0.25rem;
}
.book-cover-placeholder {
  width: 75px;
  height: 113px;
  background: #e8e0d5;
  border-radius: 2px;
  flex-shrink: 0;
  margin-top: 0.25rem;
}
.review-meta h1 {
  font-size: 1.6rem;
  margin-bottom: 0.3rem;
}
.review-meta .author {
  color: var(--color-text-muted);
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

/* ============================================
   Text-only review card on listings
   ============================================ */
.review-card-text {
  padding: 1.5rem 0;
  border-bottom: 1px solid var(--border);
}

/* ============================================
   Article/Story cards with optional thumbnail
   ============================================ */
.card-with-thumb {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}
.card-with-thumb .card-thumb {
  width: 80px;
  height: auto;
  border-radius: 3px;
  flex-shrink: 0;
}

/* ============================================
   Article Hero Images
   ============================================ */
.article-hero {
  margin: 1.5rem 0 2rem;
  border-radius: 4px;
  overflow: hidden;
}
.article-hero img {
  width: 100%;
  height: auto;
  display: block;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 640px) {
  .hero { padding: 48px 20px 40px; }
  .hero-title { font-size: 36px; }
  .hero--small .hero-title { font-size: 30px; }
  .main { padding: 32px 20px 60px; }
  .content-title { font-size: 28px; }
  .nav-inner { gap: 16px; }
  .footer-inner { flex-direction: column; align-items: flex-start; }
}

/* ============================================
   Search
   ============================================ */
.nav-search {
  position: relative;
  flex-shrink: 0;
  margin-left: auto;
}

.search-toggle {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-light);
  padding: 4px 8px;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}
.search-toggle:hover { color: var(--color-accent); }

.search-panel {
  display: none;
  position: absolute;
  right: 0;
  top: 100%;
  z-index: 200;
  min-width: 320px;
}
.search-panel.open { display: block; }

.search-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  font-family: inherit;
  font-size: 0.9rem;
  color: var(--color-text);
  border-radius: 0;
  outline: none;
}
.search-input::placeholder { color: var(--color-text-light); }

.search-results {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-top: none;
  max-height: 400px;
  overflow-y: auto;
}

.search-result-item {
  display: block;
  padding: 10px 14px;
  border-bottom: 1px solid var(--color-border-light);
  text-decoration: none;
}
.search-result-item:last-child { border-bottom: none; }
.search-result-item:hover { background: rgba(0,0,0,0.03); }

.result-title {
  font-size: 0.9rem;
  color: var(--color-text);
  font-weight: 500;
  display: block;
  margin-bottom: 3px;
}
.result-category {
  font-size: 0.7rem;
  color: var(--color-accent);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
}
.result-summary {
  font-size: 0.78rem;
  color: var(--color-text-light);
  margin-top: 2px;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.search-no-results {
  padding: 12px 14px;
  font-size: 0.85rem;
  color: var(--color-text-light);
  text-align: center;
}

/* ============================================
   Search Page
   ============================================ */
.search-page {
  max-width: 680px;
  margin: 0 auto;
  padding: 3rem 1.5rem;
}
.search-page h1 {
  font-family: var(--font-serif);
  font-size: 2rem;
  color: var(--color-text);
  margin-bottom: 1.5rem;
}
.search-page-form {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2rem;
}
.search-page-input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  font-family: inherit;
  font-size: 1rem;
  color: var(--color-text);
  outline: none;
}
.search-page-btn {
  padding: 10px 20px;
  background: var(--color-accent);
  color: var(--color-surface);
  border: none;
  font-size: 0.9rem;
  cursor: pointer;
  font-family: inherit;
}
.search-page-btn:hover { background: var(--color-accent-hover); }

/* Share bar */
.share-bar { display: flex; align-items: center; gap: 10px; max-width: var(--max-width); margin: 16px auto 32px; padding: 16px 24px; border-top: 1px solid #e8e4dd; border-bottom: 1px solid #e8e4dd; }
.share-label { font-size: 11px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #999; margin-right: 4px; }
.share-btn { display: inline-flex; align-items: center; gap: 5px; padding: 7px 12px 7px 16px; border-radius: 4px; font-size: 12px; text-decoration: none; border: 1px solid #8a6f3e; background: transparent; cursor: pointer; font-family: inherit; color: #8a6f3e; transition: opacity 0.15s; }
.share-btn:hover { opacity: 0.7; }

/* Book comparison table */
.book-comparison { margin: 1.5rem 0; overflow-x: auto; }
.book-comparison table { width: 100%; border-collapse: collapse; }
.book-comparison th { background: var(--accent, #8b6914); color: white; padding: 0.6rem 0.8rem; text-align: left; font-size: 0.9rem; }
.book-comparison td { padding: 0.5rem 0.8rem; border-bottom: 1px solid #e5e5e5; font-size: 0.9rem; }

/* Book grid */
.book-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1.2rem; margin: 1.5rem 0; }
.book-card { text-align: center; }
.book-card img { width: 120px; height: auto; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.12); }
.book-card p { font-size: 0.85rem; margin: 0.5rem 0; line-height: 1.4; }
.book-card a { color: var(--accent, #8b6914); font-weight: 600; }

/* Source links */
.source-link { font-size: 0.8rem; color: #666; margin-top: 0.5rem; }
.source-link a { color: #888; }

/* Hero Book Cover */
.hero-book-cover {
  text-align: center;
  margin: 0 auto 28px;
  padding: 0;
}
.hero-book-cover img {
  width: 200px;
  height: auto;
  border-radius: 6px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  display: block;
  margin: 0 auto;
}
.hero-book-cover img:hover {
  box-shadow: 0 6px 28px rgba(0,0,0,0.22);
  transform: translateY(-2px);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.hero-book-caption {
  text-align: center;
  font-size: 13px;
  color: var(--color-text-light);
  margin-top: 10px;
}
.hero-book-caption a { color: var(--color-accent); font-weight: 600; }

/* Related links block */
.related-links {
  max-width: var(--max-width);
  margin: 0 auto 40px;
  padding: 0 24px;
}

/* Story page image */
.review-image-wrap {
  max-width: 680px;
  margin: 0 auto;
}
```

---

## 14. Site-Wide Patterns & Constants

### CSS Class Naming Conventions
- BEM-ish with functional prefixes: `.card`, `.card-title`, `.card-meta-top`
- Category pills: `.pill-book-review`, `.pill-article`, `.pill-short-story`
- Legacy tags: `.tag--review`, `.tag--article`, `.tag--story`
- Modifier pattern: `class="hero hero--small"`

### Font Usage
| Element | Font |
|---------|------|
| Headings, hero title, card titles | `--font-serif` = `Libre Baskerville`, Georgia, serif |
| Body, nav, UI | `--font-sans` = `Source Sans 3`, Helvetica Neue, Arial, sans-serif |

### Color Palette
| Token | Value | Usage |
|-------|-------|-------|
| `--color-bg` | `#FAF8F5` | Page background (warm cream/paper) |
| `--color-surface` | `#FFFFFF` | Card backgrounds, AdSense blocks |
| `--color-text` | `#3d2b1f` | Primary text (dark brown) |
| `--color-text-muted` | `#5a4a3a` | Secondary text, bylines |
| `--color-text-light` | `#8a7a6a` | Meta text, dates |
| `--color-accent` | `#8b6914` | Links, accent color (gold/amber) |
| `--color-accent-hover` | `#a67c00` | Link hover |
| `--color-border` | `#d9d3cc` | Dividers |
| `--color-border-light` | `#f0ebe3` | Subtle borders, nav bottom |

### AdSense Publisher ID
```
ca-pub-9312870448453345
```

### Amazon Affiliate Tag
```
?tag=michaelbacoti-20
```

### JSON-LD Schema
Reviews and articles include two JSON-LD blocks:
1. **BreadcrumbList** — Home → category → page title
2. **Article** — headline, url, publisher

### search.json
All content pages are indexed in `/search.json` with shape:
```json
{
  "title": "...",
  "url": "/reviews/the-martian",
  "category": "Book Review",
  "summary": "First 1-2 sentence summary..."
}
```
The homepage, reviews.html, articles.html, and stories.html all fetch this file client-side and render a JS-driven feed using the `.feed` + `.card` pattern.

### CSS Variables Available

```css
--max-width         → 680px   (text column width)
--max-width-wide   → 1100px  (nav/footer max width)
--radius           → undefined (not set globally)
--surface          → #FFFFFF
--shadow           → undefined (not set globally)
```
Note: `--radius` and `--shadow` are referenced in AdSense inline styles but not defined in `:root`. The inline AdSense wrapper uses `border-radius:var(--radius)` which resolves to empty if undefined. This is a minor inconsistency — the wrapper falls back to no border-radius.

### Canonical URL Pattern
```
https://www.bithues.com/<SLUG>
```
(e.g., `https://www.bithues.com/reviews/the-martian`)

### Pagination
Listing pages (homepage, reviews, articles, stories) use JS-driven client-side pagination:
- Homepage: 5 items/page
- Listing pages: 10 items/page
- Uses `changePage(+1)` / `changePage(-1)` global functions
- Prev/Next buttons with inline styles

### No Star Ratings
Bithues reviews do not use star ratings. Quality is conveyed through qualitative prose language, per the Author Personality System voice guidelines.