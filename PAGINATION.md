# Story Pagination — Bithues

## Implementation Summary

**`build.py`** modified to add page-turn pagination for long stories.

### Key additions

**`chunk_body(body, chunk_size=1500)`**
- Multi-paragraph stories (≥2 `\n\n` blocks): accumulates paragraphs into ~1500-word pages
- Single-block stories (no `\n\n`): splits by sentence boundaries using `(?<=[.!?])\s+`
- Always returns at least 1 page

**`page_nav_html(slug, current_page, total_pages)`**
- Returns `<div class="page-nav">` with "Page X of Y" + prev/next links
- Only shown when `total_pages > 1`
- Disabled state for first/last page boundaries

**`generate_story_page()`**
- Added `page_num` and `total_pages` params (default 1, 1)
- Passed through to `story_page_html()`
- Single-page stories (total_pages=1): no pagination UI, unchanged behavior

**`main()`**
- Stories ≥ 2000 words → `chunk_body()`, writes one HTML per chunk with `?page=N`
- Stories < 2000 words → single HTML, no change

**URL format:** `/blood-ties.html?page=1`, `/blood-ties.html?page=2`, etc.
Jump-to anchor: `?page=N#content`

---

## Word Counts — All 37 Stories (sorted descending)

| Story | Words | Pages (1500/page) |
|---|---|---|
| blood-ties | 4304 | 3 |
| the-time-auction | 3533 | 3 |
| the-space-between | 2248 | 2 |
| the-quiet-town | 2203 | 2 |
| the-shadow-garden | 2098 | 2 |
| the-kepler-conspiracy | 2082 | 2 |
| the-sound-between-stars | 2078 | 2 |
| american-voices | 0 | single (draft/empty body) |
| before-the-streetlights-came-on | 0 | single (draft/empty body) |
| city-of-wonders | 0 | single (draft/empty body) |
| ice-memory | 0 | single (draft/empty body) |
| jaspers-flight | 0 | single (draft/empty body) |
| mabi | 0 | single (draft/empty body) |
| oliver-and-the-ocean | 0 | single (draft/empty body) |
| rules-of-the-game | 0 | single (draft/empty body) |
| the-borrowed-life | 0 | single (draft/empty body) |
| the-cartographer-of-sea-serpents | 0 | single (draft/empty body) |
| the-disclosure | 0 | single (draft/empty body) |
| the-door-between-worlds | 0 | single (draft/empty body) |
| the-echoes-return | 0 | single (draft/empty body) |
| the-ember-song | 0 | single (draft/empty body) |
| the-forbidden-library | 0 | single (draft/empty body) |
| the-forgotten-minute | 0 | single (draft/empty body) |
| the-harvest | 0 | single (draft/empty body) |
| the-humble-mind | 0 | single (draft/empty body) |
| the-last-arena | 0 | single (draft/empty body) |
| the-last-garden | 0 | single (draft/empty body) |
| the-last-gift | 0 | single (draft/empty body) |
| the-last-signal | 0 | single (draft/empty body) |
| the-last-song | 0 | single (draft/empty body) |
| the-last-winter | 0 | single (draft/empty body) |
| the-listen | 0 | single (draft/empty body) |
| the-other-side | 0 | single (draft/empty body) |
| the-question | 0 | single (draft/empty body) |
| the-seed-library-at-the-end-of-may | 0 | single (draft/empty body) |
| the-weight-of-summer-light | 0 | single (draft/empty body) |
| they-walk-among-us | 0 | single (draft/empty body) |

---

## Pagination Stats

- **Stories ≥ 2000 words:** 7 (paginated into 16 total HTML files)
- **Stories < 2000 words:** 30 (single-page HTML)
- **Total story HTML files generated:** 46
- **Threshold:** 2000 words
- **Target chunk size:** ~1500 words

---

## Notes

- 30 stories show 0 words — these are draft stubs with only front matter and no body content. They render as empty single pages.
- Pagination HTML uses CSS classes: `.page-nav`, `.page-info`, `.page-prev`, `.page-next`, `.page-links`, `.page-prev.disabled`, `.page-next.disabled` — add minimal styles to `style.css` if needed.
- Story cards on listing/index pages link to `/slug.html` (page 1), which is correct for both single-page and paginated stories.
- Previous/Next story navigation (bottom of page) applies between stories, not between pages of the same story — page 1 of a long story links to previous story; last page links to next story; middle pages have no story-level prev/next.