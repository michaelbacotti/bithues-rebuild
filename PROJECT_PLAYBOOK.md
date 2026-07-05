# PROJECT_PLAYBOOK — Bithues (bithues.com)

> How to work in the Bithues Character Engine + KU Discovery Engine
> Last updated: 2026-07-05

---

## How to Create a New Character Dossier

1. **Read the source.** Check existing manuscripts in `projects/bithues/content/` or `books/` for character details (name, appearance, personality, relationships, story arc, themes).

2. **Check for duplicates.** Scan existing files in `characters/` to avoid creating a duplicate entry for the same character.

3. **Fill the template** (see `templates/character_dossier_template.md`):
   - Name, story origin, role (protagonist/antagonist/guide/etc.)
   - Appearance, personality traits, core conflicts
   - Key relationships (family, allies, enemies, mentors, rivals)
   - Featured in: which books/chapters/scenes
   - Associated themes (trauma, redemption, heritage, war, spirituality)
   - Notes / gaps requiring human review

4. **Save to:** `projects/bithues/website/characters/[slug].md`
   - Slug format: lowercase, hyphens, e.g., `otomi-warrior.md`, `lena-skywalker.md`

5. **Update relationships.** Append the new character to `characters/relationships.md` using the established relationship format.

6. **Quality check before publishing:**
   - Are there at least 3 substantive paragraphs?
   - Are sources/book references included?
   - Is the tone consistent with existing dossiers?
   - Does it link to related characters?

7. **Approval:** If the character involves sensitive cultural material (specific tribal traditions, historical trauma), flag for human review before deploying.

---

## How to Create a New KU Book Metadata Entry

1. **Get book details.** From Amazon page, manuscript notes, or existing book pages in `projects/bithues/website/books/`.

2. **Fill the template** (see `templates/book_ku_metadata_template.md`):
   - Title, author, ASIN, KU status (in/out), series name and number
   - Length (word count range: short story / novella / novel / series)
   - Reading time estimate
   - Mood tags (dark, hopeful, meditative, intense, playful)
   - Theme tags (Native American history, military, family saga, trauma, etc.)
   - Content advisories (violence, trauma, language — where relevant)
   - Blurb / hook paragraph
   - Related reading paths (which paths include this book)

3. **Save to:** `projects/bithues/website/ku/[slug].md`
   - Slug format: lowercase, hyphens, e.g., `the-winter-commander.md`

4. **Quality check:**
   - Is the KU status correct (confirmed from Amazon)?
   - Are mood/theme tags consistent with the book's actual content?
   - Does it link to at least one reading path or character?

---

## How to Create a Thematic Hub Page

1. **Identify theme.** Propose a theme that appears across multiple books (e.g., "Ghosts and Ancestors", "Military Service and Identity").

2. **Draft the hub** using `templates/theme_hub_template.md`:
   - Theme name, brief explanation
   - Key characters associated
   - Key scenes/passages (non-spoiler summary)
   - Books in this theme (with KU links)
   - Related themes hub pages

3. **Save to:** `projects/bithues/website/characters/themes/[theme-slug].md`

4. **Cross-link.** Update the theme index at `characters/themes/index.md`.

---

## Templates to Use

| Template | Location | Use for |
|----------|----------|---------|
| `character_dossier_template.md` | `projects/bithues/website/templates/` | New character entries |
| `book_ku_metadata_template.md` | `projects/bithues/website/templates/` | New KU book entries |
| `theme_hub_template.md` | `projects/bithues/website/templates/` | Thematic hub pages |
| `reading_path_template.md` | `projects/bithues/website/templates/` | KU reading paths |

---

## Approval Workflow

| Action | Who approves |
|--------|-------------|
| New character dossier (standard cultural content) | Agent can publish |
| Character involving specific tribal traditions or sensitive historical trauma | Human review required |
| New KU book entry | Agent can publish |
| New thematic hub | Human review recommended |
| Changes to home page, nav, or legal pages | Human required |
| Bulk generation (>5 entries at once) | Human review first |

---

## Quality Bar ("3-5 examples before scaling" — Implementation §6.5)

Before generating many entries at once:
1. Create 3–5 examples manually
2. Review with human
3. Confirm quality level matches existing site tone
4. Then scale with the confirmed pattern

---

## Content Lane Summary

| Lane | Frequency | Owner |
|------|-----------|-------|
| Character dossiers | As new books published | Agent + human review |
| KU metadata entries | As new books published | Agent |
| Theme hubs | Quarterly review | Agent + human review |
| Reading paths | Quarterly review | Agent |

---

## Reference

- Implementation §6.1, §6.2, §6.5
- `Reports/LIVING_INTELLIGENCE_PROPERTIES.md` — Bithues section
- `projects/bithues/website/PROJECT_INDEX.md`
