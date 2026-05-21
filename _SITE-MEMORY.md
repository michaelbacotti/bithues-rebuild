# SITE MEMORY — Bithues

## Identity
- Entity: Bithues (book review and literary publication)
- Purpose: Book reviews, reading guides, articles, and original short fiction
- Repo: github.com/michaelbacotti/bithues-rebuild
- Live URL: www.bithues.com (Cloudflare Pages)
- Staging URL: bithues-rebuild.pages.dev (Cloudflare Pages preview)
- Architecture: Flat HTML — see skills/website-flat-html.md

## Design Reference (from live bithues.com homepage, 2026-05-13)
- Background: #FAF8F5 (warm cream)
- Surface: #FFFFFF
- Text: #2C2416 (dark brown)
- Accent: #8B4513 (saddle brown)
- Fonts: Libre Baskerville (serif headings), Source Sans 3 (body)
- Hero: centered large wordmark, generous padding (72px top), tagline below
- Cards: tag pill + date label, serif title, muted excerpt
- Tags: uppercase, small, rounded — gold for reviews, green for articles, purple for stories

## File Roles
- `/style.css` — ALL styles. Never edit during routine content updates.
- `/nav.js` — Site-wide nav. Edit here to change nav on all pages.
- `/footer.js` — Site-wide footer. Edit here to change footer on all pages.
- `/_template.html` — Base for new pages. Copy it, never edit or serve it.
- `/reviews/` — Book review content pages
- `/articles/` — Article content pages
- `/stories/` — Short story content pages

## Critical Rules
- All paths to style.css, nav.js, footer.js must start with `/`
- No build step. No Hugo. No GitHub Actions.
- Scripts go at end of body, after the div containers they populate
- Always verify live in browser after every deploy — not just curl
- DO NOT link to real books or real authors as if they were reviewed — use clearly fictional placeholders

## Section Pages
- `index.html` — Homepage (feed of latest content)
- `reviews.html` — Book review listing
- `articles.html` — Articles listing
- `stories.html` — Short stories listing
- `about.html` — About page

## Placeholder Content Rules
All book titles, author names, and story titles are FICTIONAL. Do not create pages that could be mistaken for real published works.

## Change Log
- 2026-05-13 — Initial build — flat HTML literary site (warm cream/serif design)