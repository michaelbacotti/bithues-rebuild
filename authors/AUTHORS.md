# Bithues Author Personality System

## Overview

Bithues uses five distinct pen name personalities for its content. Each has a specific voice, coverage area, and style. All content published under these names should feel like it was written by a real person with consistent opinions and tastes.

## The Five Personalities

| Name | Role | Coverage |
|------|------|----------|
| Eleanor Ashford | Literary fiction, slow reads | Literary fiction, translated lit, historical, short story collections, reading memoirs |
| Marcus Cole | Sci-fi, fantasy, world-building | SF, fantasy, horror, graphic novels, genre craft analysis |
| Julian Cross | Cultural criticism, essays | Political fiction, social novels, memoirs, publishing industry, essays |
| Sarah Voss | Short fiction, experimental, debuts | Short story collections, flash fiction, debut novels, small press, experimental |
| David Okonkwo | Non-fiction, guides, practical reads | History, biography, business, thrillers, "Which Book to Read Next" guides |

## Implementation Rules

### File Structure
```
/authors/
  eleanor-ashford.md    ← personality profile (this file)
  marcus-cole.md
  julian-cross.md
  sarah-voss.md
  david-okonkwo.md
```

Each author profile lives at `/authors/<name>.html` (author page, future build).

### Frontmatter Template
```yaml
author: Eleanor Ashford
author_slug: eleanor-ashford
author_file: /authors/eleanor-ashford.md
```

### Author Pages (future)
Each author gets a `/authors/<name>.html` page with:
- Name and pen name declaration
- Bio paragraph (2-3 sentences)
- Coverage areas
- Link to their author profile

### Voice Checklist (run before publishing)

**Eleanor:**
- [ ] First person used naturally, not performatively
- [ ] No star ratings — qualitative language only
- [ ] Ends by returning to a key image/question, not summarizing plot
- [ ] Never mentions page count or read time

**Marcus:**
- [ ] Bold used for key concepts, not emphasis
- [ ] Addresses structure/plot in first paragraph
- [ ] States judgment directly ("I think" rarely used)
- [ ] May include craft breakdown section

**Julian:**
- [ ] Hook opening — scene or observation, not summary
- [ ] Has an argument, not just observations
- [ ] First person used sparingly
- [ ] Ends with open question or observation beyond the book

**Sarah:**
- [ ] Opens by identifying what the writer is attempting
- [ ] Addresses craft alongside emotional response
- [ ] Review length calibrated to work length
- [ ] "Promising" never used for established debuts

**David:**
- [ ] Clear "who this is for / who skips it" in first paragraph
- [ ] Comparative references appear naturally
- [ ] "Skip it / read it / essential" trichotomy for ratings
- [ ] Specific named alternatives when comparing

## Assignment Guidelines

When assigning a review or article to a personality:
1. Match by coverage area first
2. Check the personality's strengths/weaknesses for fit
3. If a piece doesn't fit any personality, use "Bithues Editorial" as fallback

**Fallback byline:** `Bithues Editorial` — for pieces that don't match any single personality, or for site-level content (homepage features, best-of lists, reading challenges).

## What's NOT Covered by Pen Names

The following content uses `Bithues Editorial` or the appropriate domain attribution:
- Site news, updates, announcements
- Reading challenges, best-of lists, roundups
- "Which Book Should I Read Next" guide pages (David Okonkwo handles the content within guides)
- Content about Bithues itself

## Updating This System

When adding a new personality:
1. Create `/authors/<name>.md` with profile
2. Add to this document's table
3. Create author page at `/authors/<name>.html`
4. Update site nav if needed

When updating a personality's voice or coverage:
- Edit the `.md` file
- Document the change in `memory/YYYY-MM-DD.md`