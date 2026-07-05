# PROJECT_INDEX — Bithues (bithues.com)

> Character Engine + KU Discovery Engine
> Last updated: 2026-07-05

## Purpose & Audience

Bithues is a living book hub that helps readers navigate Mike Bacotti's fictional universe (Native American historical fiction, military fiction, literary fiction) and discover the right book based on mood, theme, length, and reading context — with a bias toward Kindle Unlimited.

**Audience:** Readers who liked Mike's books; readers searching for KU fiction in themes Mike writes about (Native American history, military service, trauma and healing, family sagas).

---

## Live-Site Paths

```
projects/bithues/website/          ← bithues-rebuild GitHub repo
  characters/                      ← Character Engine (ALLOWED WRITE PATH)
  ku/                              ← KU Discovery Engine (ALLOWED WRITE PATH)
  articles/                        ← ALLOWED WRITE PATH
  templates/                       ← templates used by build pipeline
```

**Protected (do not edit without explicit human approval):**
- `about/`, `contact/`, `disclaimer/`, `privacy/`
- `build.py`, `_template*`, nav files
- Home page, sitemap, robots.txt

---

## Core Engines

### Character Engine
Turns Mike's fictional universe into an explorable atlas: character dossiers, relationship maps, timelines, and thematic hubs that link back to books.

**Key artifacts:**
- `characters/` — one `.md` file per character
- `characters/relationships.md` — relationship graph
- `characters/timeline.md` — in-universe chronology
- `characters/themes/` — thematic hub pages (e.g., "Warriors and Guardians", "Mothers and Daughters")

### KU Discovery Engine
KU-first discovery layer matching readers to books based on mood, time available, and theme.

**Key artifacts:**
- `ku/` — one metadata `.md` per book with KU tags, mood, length, themes
- `ku/paths/` — curated multi-book reading paths
- `ku/finder/` — discovery selector pages

---

## Monetization

| Method | Where |
|--------|-------|
| Kindle Unlimited reads | Primary — book pages, KU discovery paths |
| Amazon Associates | Book pages, KU pages ( contextual links) |
| AdSense | Articles, theme hubs, character pages (not on core KU conversion pages) |

---

## OptionStrat / Affiliate Notes

- Not applicable to Bithues directly. Amazon Associates applies.
- Amazon affiliate links: use contextual, descriptive anchor text; include disclosure.

---

## Status & Pending Tasks

- [ ] Folder structure `characters/` and `ku/` created (LIP-01, 2026-07-05)
- [ ] LIP-04: First character dossier pilot
- [ ] LIP-05: First KU book metadata entry pilot
- [ ] Template files for character dossier and book KU metadata
- [ ] Relationship map first draft
- [ ] OptionStrat affiliate scan (N/A for Bithues)

---

## Related Documents

- `Reports/LIVING_INTELLIGENCE_PROPERTIES.md` — Bithues section
- `Reports/LIVING_INTELLIGENCE_IMPLEMENTATION.md` — §2, §4
- `projects/bithues/website/PROJECT_PLAYBOOK.md` — how to work here
- `skills/bithues.character_engine` — skill proposal (pending approval)
- `skills/bithues.ku_discovery` — skill proposal (pending approval)

## Source

Wiki synthesis: `wiki/main/syntheses/living-intelligence-properties-strategy.md`
