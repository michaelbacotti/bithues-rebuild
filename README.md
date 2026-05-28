# Bithues — Generated Site (bithues-may24)

A prototype short fiction site for **bithues.com**, built as a static site generator from Markdown story files.

## Setup

The site reads from `../content/stories/*.md` (relative to this directory), parses the front matter, and generates a complete static HTML site.

**Requirements:** Python 3 only — no external dependencies.

## Building

```bash
cd /path/to/bithues/test
python3 build.py
```

This generates (or overwrites) all HTML files in the `test/` directory:
- `index.html` — homepage with hero + featured stories
- `stories.html`, `stories2.html`, … — paginated story listing (9 per page)
- `<slug>.html` — individual story pages for all 37 stories
- `about.html`, `contact.html`, `privacy.html`, `terms.html` — static pages

## Story Markdown Format

Each story file in `../content/stories/` should be a `.md` file with YAML front matter:

```markdown
---
title: "Story Title Here"
date: "2026-04-15"
section: stories
type_label: SHORT STORY
summary: "One or two sentence description."
card_image: null
genre_label: "Dark Fantasy"
featured: false
draft: false
---

Story body text goes here. Multiple paragraphs, each separated
by a blank line in the Markdown.
```

### Front Matter Fields

| Field | Type | Notes |
|-------|------|-------|
| `title` | string | Story title; used in page `<title>`, `<h1>`, and cards |
| `date` | string | ISO date `"YYYY-MM-DD"`; shown on cards and story pages |
| `section` | string | Must be `"stories"` |
| `type_label` | string | Category label (e.g., `"SHORT STORY"`) |
| `summary` | string | Card/SEO description; shown under title on cards |
| `card_image` | string | Optional image path; currently unused in generator |
| `genre_label` | string | Genre pill shown on story page (e.g., `"Dark Fantasy"`) |
| `featured` | boolean | `true` = included in homepage featured section |
| `draft` | boolean | `true` = skipped by generator |

## Design

Design language mirrors **dependability.us** aesthetic:
- Dark utility bar (`#111111`) with centered tagline
- Section tab bar with red accent underline on active item (`#c8001e`)
- Serif headings (Georgia) + sans-serif body
- Red top-border article cards in a 3-column grid
- Story pages: genre pill → title → date → story body → share bar → prev/next nav

## File Overview

```
test/
├── _template.html   — base HTML shell (nav slots, footer slots)
├── nav.js            — top bar + tab bar JS (Bithues branded)
├── footer.js         — footer HTML JS component
├── style.css         — full stylesheet (dependability.us aesthetic, Bithues-adapted)
├── build.py          — site generator (Python 3, no deps)
├── index.html        — generated homepage
├── stories.html      — generated story listing (page 1)
├── american-voices.html  (example generated story page)
├── blood-ties.html
├── jaspers-flight.html
├── mabi.html
├── oliver-and-the-ocean.html
└── [36 more story pages]
```

## Development Workflow

1. Add or edit a `.md` file in `../content/stories/`
2. Run `python3 build.py`
3. Serve locally to preview:

```bash
cd /path/to/bithues/bithues-may24
python3 -m http.server 8080
# → http://localhost:8080
```

## Notes

- The generator writes all output into `test/` — it does not touch `../content/stories/`
- To update the site, re-run `build.py` — it overwrites all generated HTML files
- Pagination is built-in at 9 stories per page (configured at top of `build.py` as `PAGINATE`)
- All 37 stories from the content directory are parsed; drafts are skipped
- There is no live reload — edit content, rebuild, refresh