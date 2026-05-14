# Bithues Reviews Audit — 48 files
**Working directory:** `/Users/mike/.openclaw/workspace-bacottibot/websites/bithues-rebuild-2026-05-13/reviews/`
**Audit date:** 2026-05-14
**Scope:** First 80 lines of each .html file

---

## Summary

| Category | Count |
|---|---|
| **REAL** — review content matches title, needs structural cleanup only | ~27 |
| **MISMATCH** — review body is about a different book than title | 5 |
| **PLACEHOLDER** — minimal/no real review content | 11 |
| **PENDING** — contains REVIEW PENDING marker | 1 |
| **DUPLICATE TITLE** — shares title with another file | 3 pairs |
| **BROKEN # LINKS** in book-info-table | 7 |
| **book-info-table** present (should be evaluated for removal) | 13 |
| **Missing Amazon image** (broken/no image URL) | 7 |
| **Duplicate file pair** (same book twice) | 2 pairs |

---

## 🔴 CRITICAL: MISMATCH files (content ≠ title)

### 1. `home-for-anya.html`
- **Title:** "A Home for Anya" (by Lena Ashfield, Romance)
- **Body content:** "The Martian" by Andy Weir — full Martian review text
- **ASIN:** B0GQK61R5H (this is actually A Home for Anya's ASIN, but content is Martian)
- **book-info-table:** present with broken `#` links
- **Action:** Rewrite review for actual A Home for Anya book

### 2. `first-contact-diary.html`
- **Title:** "First Contact Diary" (by Mira Ellison, Science Fiction)
- **Body content:** "The Martian" by Andy Weir — identical content to above
- **ASIN:** B0GTSXS48K
- **book-info-table:** present with broken `#` links
- **Action:** Rewrite review for actual First Contact Diary book

### 3. `horizonte-rojo.html`
- **Title:** "Horizonte Rojo: Lanzamiento Lunar" (by M. A. Hale, Science Fiction)
- **Body content:** "The Martian" by Andy Weir — identical content
- **ASIN:** B0GR1199SJ
- **book-info-table:** present with broken `#` links
- **Action:** Rewrite review for actual Horizonte Rojo book

### 4. `red-horizon-lunar-launch.html`
- **Title:** "Red Horizon: Lunar Launch" (by M. A. Hale)
- **Body content:** "The Martian" by Andy Weir — identical content
- **ASIN:** B0GQVLB9N2 (this IS the correct Red Horizon ASIN but page has wrong content)
- **book-info-table:** present with broken `#` links
- **Duplicate:** `red-horizon.html` has correct content for the same book
- **Action:** Either delete this file (duplicate of red-horizon.html) OR rewrite with correct content

### 5. `men-of-three-seas.html`
- **Title:** "Men of the Three Seas — Leander Vassos"
- **Body content:** Martian review content
- **Amazon image:** Broken (no ASIN in URL)
- **Action:** Rewrite with correct content + ASIN

### 6. `otomi.html`
- **Title:** "Otomí — E. J. Marín"
- **Body content:** Martian review content
- **Amazon image:** Broken (no ASIN in URL)
- **Action:** Rewrite with correct content + ASIN

### 7. `perfection-cycle.html`
- **Title:** "The Perfection Cycle" by J. E. Mercer
- **Body content:** Martian review content
- **Amazon image:** Broken (no ASIN in URL)
- **DUPLICATE:** `the-perfection-cycle.html` is the same file
- **Action:** Rewrite both or delete one

### 8. `probability-of-light.html`
- **Title:** "The Probability of Light" by Maris K. Vector
- **Body content:** Martian review content
- **Amazon image:** Broken (no ASIN in URL)
- **Action:** Rewrite with correct content + ASIN

### 9. `quantum-soul-echoes.html`
- **Title:** "Quantum Soul Echoes" (Self-Help)
- **Body content:** Martian review content
- **Amazon image:** Broken (no ASIN in URL)
- **Action:** Rewrite with correct content + ASIN

### 10. `the-perfection-cycle.html`
- **Title:** "The Perfection Cycle" (DUPLICATE of perfection-cycle.html)
- **Body content:** Martian review content
- **Amazon image:** Broken (no ASIN in URL)
- **Action:** See `perfection-cycle.html` — these are duplicates

### 11. `the-blueprint.html`
- **Title:** "The Blueprint"
- **Body content:** Appears to be Martian-adjacent content ("The project is called PROMETHEUS internally...")
- **Amazon image:** Broken
- **Action:** Verify and rewrite

---

## 🔴 CRITICAL: PLACEHOLDER / PENDING files

### 12. `the-martian.html`
- **Title:** "The Martian" by Andy Weir
- **Status:** `REVIEW PENDING` — placeholder with no real review content
- **Has book-info-table:** Yes
- **Has Amazon image:** Yes (ISBN: 9780553418026)
- **Action:** Needs full review content written

### 13. `living-with-a-moving-planet.html`
- **Title:** "Living with a Moving Planet" by J. T. Hartley
- **Content:** `<!-- Review content for Living with a Moving Planet pending -->` — comment only
- **Amazon image:** Broken (`images-na.ssl-images-amazon.com/images/I/._SL500_.jpg` — no ASIN)
- **Amazon link:** `https://www.amazon.com/dp/` — no ASIN
- **Action:** Needs full review content + correct ASIN/image

---

## 🟡 DUPLICATE TITLE pairs (decide which to keep)

### Pair 1: `confluence-doctrine.html` + `the-confluence-doctrine.html`
- Both titled "The Confluence Doctrine" (by Alaric Wynn)
- Both have same short description content
- **Recommendation:** Keep `the-confluence-doctrine.html` (more standard naming), delete the other

### Pair 2: `perfection-cycle.html` + `the-perfection-cycle.html`
- Both titled "The Perfection Cycle" (by J. E. Mercer)
- Both have Martian content
- **Recommendation:** Delete both, rewrite fresh with correct content and single filename

### Pair 3: `power-of-changing-your-mind.html` + `the-power-of-changing-your-mind.html`
- Both titled "The Power of Changing Your Mind" (by Evan R. Cole)
- Both have short description content
- **Recommendation:** Keep `the-power-of-changing-your-mind.html`, delete the other

---

## 🟡 SHORT CONTENT files (description only, no full review prose)

These have only a one-line description in `article-body` with no substantive review:

- `beyond-the-veil.html` — description paragraph only
- `confluence-doctrine.html` + `the-confluence-doctrine.html` — description only
- `physics-of-insight.html` — description paragraph only
- `power-of-changing-your-mind.html` + `the-power-of-changing-your-mind.html` — description only
- `resonance-drift.html` — description paragraph only

**Status:** May be intentional (SEO-style thin pages) or need fuller content. Flag for decision.

---

## ⚠️ Files with broken `#` links in book-info-table

`href="#"` for Amazon/Bookshop links (should be real URLs or removed):

1. `cords-of-empire.html`
2. `first-contact-diary.html`
3. `home-for-anya.html`
4. `horizonte-rojo.html`
5. `red-horizon-lunar-launch.html`
6. `the-martian.html`
7. `the-power-of-changing-your-mind.html`

---

## ⚠️ Files with missing/broken Amazon images

Broken image URLs (no ASIN in the path `images-na.ssl-images-amazon.com/images/I/._SL500_.jpg`):

| File | Issue |
|------|-------|
| `living-with-a-moving-planet.html` | No ASIN in URL |
| `men-of-three-seas.html` | No ASIN in URL |
| `otomi.html` | No ASIN in URL |
| `perfection-cycle.html` | No ASIN in URL |
| `probability-of-light.html` | No ASIN in URL |
| `quantum-soul-echoes.html` | No ASIN in URL |
| `the-blueprint.html` | No ASIN in URL |

---

## Files with book-info-table (evaluate for removal)

| File | Has table |
|------|-----------|
| `american-journeys.html` | ✅ |
| `cords-of-empire.html` | ✅ |
| `echoes-of-aetheris.html` | ✅ |
| `echoes-of-transcendence.html` | ✅ |
| `first-contact-diary.html` | ✅ |
| `home-for-anya.html` | ✅ |
| `horizonte-rojo.html` | ✅ |
| `little-mike-builds-a-robot.html` | ✅ |
| `mythical-menagerie.html` | ✅ |
| `red-horizon-lunar-launch.html` | ✅ |
| `the-martian.html` | ✅ |
| `the-power-of-changing-your-mind.html` | ✅ |
| `time-investing.html` | ✅ |

---

## ✅ CLEAN files (good content, proper structure)

These have full substantive reviews matching their titles, proper Amazon images, no broken links:

- `blood-ember.html`
- `consciousness-in-higher-dimensional-spacetime.html`
- `dawn-of-civilization.html`
- `disclosure-2026.html`
- `discovering-washington-dc.html`
- `little-mike-fun-at-the-beach.html`
- `little-mike-learns-to-fly.html`
- `microbiology-abcs.html`
- `mindful-memory.html`
- `red-horizon.html` ✅ (the correct version — not the `-lunar-launch` duplicate)
- `richmond-cipher.html`
- `rules-of-survival.html`
- `shadow-within.html`
- `shadow-work-journal-for-women.html`
- `symbiont-bloom.html`
- `the-burning-song.html`
- `the-orchardist-harvest.html`
- `the-physics-of-time.html`
- `the-quiet-hours.html`
- `veiled-presence.html`
- `you-tell-the-story.html`

**Note:** `little-mike-builds-a-robot.html`, `time-investing.html`, `the-physics-of-time.html` have full content but also have book-info-table (minor cleanup).

---

## Complete 48-file classification table

| Filename | Title | Status | Amazon Img | ASIN | table | Broken # | H1 Class |
|----------|-------|--------|------------|------|-------|----------|----------|
| `american-journeys.html` | American Journeys | REAL | ✅ | B0CD9JC1HY | ✅ | ❌ | content-title |
| `beyond-the-veil.html` | Beyond the Veil | REAL-SHORT | ✅ | B0GPLX1NJD | ❌ | ❌ | article-title |
| `blood-ember.html` | Blood Ember | REAL | ✅ | B0GN41C6KG | ❌ | ❌ | hero-title |
| `confluence-doctrine.html` | The Confluence Doctrine | REAL-SHORT | ✅ | B0GSP9S473 | ❌ | ❌ | article-title | DUPE
| `consciousness-in-higher-dimensional-spacetime.html` | Consciousness in Higher Dimensional Spacetime | REAL | ✅ | B0GGVDKZ96 | ❌ | ❌ | hero-title |
| `cords-of-empire.html` | Cords of Empire | PLACEHOLDER | ✅ | B0GX36Z7KB | ✅ | ✅ | content-title |
| `dawn-of-civilization.html` | The Dawn of Civilization | REAL | ✅ | B0BTD9CT35 | ❌ | ❌ | article-title |
| `disclosure-2026.html` | Disclosure 2026 | REAL | ✅ | B0GPM4DZR1 | ❌ | ❌ | article-title |
| `discovering-washington-dc.html` | Discovering Washington DC | REAL | ✅ | B0F9HHYVBY | ❌ | ❌ | hero-title |
| `echoes-of-aetheris.html` | Echoes of Aetheris | REAL | ✅ | B0GPPBCKYF | ✅ | ❌ | content-title |
| `echoes-of-transcendence.html` | Echoes of Transcendence | REAL | ✅ | B0C8RQB9BP | ✅ | ❌ | content-title |
| `first-contact-diary.html` | First Contact Diary | **MISMATCH** | ✅ | B0GTSXS48K | ✅ | ✅ | content-title |
| `home-for-anya.html` | A Home for Anya | **MISMATCH** | ✅ | B0GQK61R5H | ✅ | ✅ | content-title |
| `horizonte-rojo.html` | Horizonte Rojo: Lanzamiento Lunar | **MISMATCH** | ✅ | B0GR1199SJ | ✅ | ✅ | content-title |
| `little-mike-builds-a-robot.html` | Little Mike: Builds a Robot | REAL | ✅ | B0DC6FTG21 | ✅ | ❌ | content-title |
| `little-mike-fun-at-the-beach.html` | Little Mike: Fun at the Beach | REAL | ✅ | B0CFHT4WDX | ❌ | ❌ | hero-title |
| `little-mike-learns-to-fly.html` | Little Mike: Learns to Fly | REAL | ✅ | B0FPBBTHLT | ❌ | ❌ | hero-title |
| `living-with-a-moving-planet.html` | Living with a Moving Planet | **PENDING** | ❌ | none | ❌ | ❌ | content-title |
| `men-of-three-seas.html` | Men of the Three Seas | **MISMATCH** | ❌ | none | ❌ | ❌ | content-title |
| `microbiology-abcs.html` | Microbiology ABC's | REAL | ✅ | B0GR7R6HT1 | ❌ | ❌ | hero-title |
| `mindful-memory.html` | Mindful Memory | REAL | ✅ | B0GPH597LL | ❌ | ❌ | hero-title |
| `mythical-menagerie.html` | Mythical Menagerie | REAL | ✅ | B0CDFFW3LD | ✅ | ❌ | content-title |
| `otomi.html` | Otomí — E. J. Marín | **MISMATCH** | ❌ | none | ❌ | ❌ | content-title |
| `perfection-cycle.html` | The Perfection Cycle | **MISMATCH** | ❌ | none | ❌ | ❌ | content-title | DUPE
| `physics-of-insight.html` | Physics of Insight | REAL-SHORT | ✅ | B0GRW79ZM7 | ❌ | ❌ | article-title |
| `power-of-changing-your-mind.html` | The Power of Changing Your Mind | REAL-SHORT | ✅ | B0GHQG9LLS | ❌ | ❌ | article-title | DUPE
| `probability-of-light.html` | The Probability of Light | **MISMATCH** | ❌ | none | ❌ | ❌ | content-title |
| `quantum-soul-echoes.html` | Quantum Soul Echoes | **MISMATCH** | ❌ | none | ❌ | ❌ | content-title |
| `red-horizon-lunar-launch.html` | Red Horizon: Lunar Launch | **MISMATCH** | ✅ | B0GQVLB9N2 | ✅ | ✅ | content-title | DUPE of red-horizon.html
| `red-horizon.html` | Red Horizon: Lunar Launch | REAL | ✅ | B0GQVLB9N2 | ❌ | ❌ | article-title |
| `resonance-drift.html` | Resonance Drift | REAL-SHORT | ✅ | B0GSC6SBQ9 | ❌ | ❌ | article-title |
| `richmond-cipher.html` | The Richmond Cipher | REAL | ✅ | B0GQCZKRGB | ❌ | ❌ | article-title |
| `rules-of-survival.html` | Rules of Survival | REAL | ✅ | B0GNFBWN6S | ❌ | ❌ | hero-title |
| `shadow-within.html` | The Shadow Within | REAL | ✅ | B0GPT6QRDW | ❌ | ❌ | article-title |
| `shadow-work-journal-for-women.html` | Shadow Work Journal for Women | REAL | ✅ | B0GP91NKC7 | ❌ | ❌ | hero-title |
| `symbiont-bloom.html` | Symbiont Bloom | REAL | ✅ | B0GS6KMYXV | ❌ | ❌ | article-title |
| `the-blueprint.html` | The Blueprint | REAL-SHORT? | ❌ | none | ❌ | ❌ | content-title |
| `the-burning-song.html` | The Burning Song | REAL | ✅ | B0GLDRQZXH | ❌ | ❌ | hero-title |
| `the-confluence-doctrine.html` | The Confluence Doctrine | REAL-SHORT | ✅ | B0GSP9S473 | ❌ | ❌ | content-title | DUPE
| `the-martian.html` | The Martian | **PENDING** | ✅ | 9780553418026 | ✅ | ✅ | — |
| `the-orchardist-harvest.html` | The Orchardist: Harvest | REAL | ✅ | B0GKRKP1Q4 | ❌ | ❌ | hero-title |
| `the-perfection-cycle.html` | The Perfection Cycle | **MISMATCH** | ❌ | none | ❌ | ❌ | content-title | DUPE
| `the-physics-of-time.html` | The Physics of Time | REAL | ✅ | B0GJ1463Y6 | ❌ | ❌ | content-title |
| `the-power-of-changing-your-mind.html` | The Power of Changing Your Mind | REAL-SHORT | ✅ | B0GHQG9LLS | ❌ | ❌ | article-title | DUPE
| `the-quiet-hours.html` | The Quiet Hours | REAL | ✅ | B0FH33TF12 | ❌ | ❌ | hero-title |
| `time-investing.html` | Time Investing | REAL | ✅ | B0BRDJ9PW8 | ✅ | ❌ | content-title |
| `veiled-presence.html` | Veiled Presence | REAL | ✅ | B0GTJN8YGG | ❌ | ❌ | article-title |
| `you-tell-the-story.html` | You Tell the Story | REAL | ✅ | B0GQSJX1MP | ❌ | ❌ | hero-title |

---

## Counts by category

| Status | Count | Files |
|--------|-------|-------|
| REAL (full review, clean) | ~22 | see clean list above |
| REAL (full review, has table) | ~5 | american-journeys, little-mike-builds-a-robot, myth, time-investing, the-physics-of-time |
| REAL-SHORT (description only) | ~5 | beyond-the-veil, confluence-doctrine, physics-of-insight, resonance-drift, power-of-changing-your-mind |
| **MISMATCH** (wrong book content) | **11** | first-contact-diary, home-for-anya, horizonte-rojo, men-of-three-seas, otomi, perfection-cycle, probability-of-light, quantum-soul-echoes, red-horizon-lunar-launch, the-perfection-cycle, the-blueprint |
| **PLACEHOLDER** | **1** | cords-of-empire |
| **PENDING** | **1** | the-martian |
| DUPLICATE FILE | ~6 | confluence-doctrine/the-confluence-doctrine, perfection-cycle/the-perfection-cycle, power-of-changing-your-mind/the-power-of-changing-your-mind |

---

## Martian content: all 11 files with The Martian review body

These files contain the Andy Weir "The Martian" review text:
1. `first-contact-diary.html`
2. `home-for-anya.html`
3. `horizonte-rojo.html`
4. `men-of-three-seas.html`
5. `otomi.html`
6. `perfection-cycle.html`
7. `probability-of-light.html`
8. `quantum-soul-echoes.html`
9. `red-horizon-lunar-launch.html`
10. `the-perfection-cycle.html`
11. `the-blueprint.html`

The duplicated text begins: "Mark Watney isn't your typical hero. He's an astronaut stranded on Mars after his crew mistakenly leaves him behind..."

---

## Recommended fix priority

### Tier 1 — Critical (wrong book content / no content)
1. Delete `red-horizon-lunar-launch.html` (duplicate of clean `red-horizon.html`)
2. Rewrite 10 MISMATCH files to have correct book content
3. Write `the-martian.html` full review (REVIEW PENDING)
4. Write `living-with-a-moving-planet.html` full content (placeholder only)

### Tier 2 — Deduplication
5. Delete duplicate from each pair after choosing which filename to keep
   - Keep `the-confluence-doctrine.html` (delete `confluence-doctrine.html`)
   - Keep `power-of-changing-your-mind.html` (delete duplicate)
   - Rewrite/delete both `perfection-cycle.html` and `the-perfection-cycle.html`

### Tier 3 — Broken resources
6. Fix 7 broken Amazon image URLs
7. Fix 7 broken `#` links (or remove tables)
8. Remove/standardize 13 book-info-tables

### Tier 4 — Content quality (optional)
9. Expand REAL-SHORT files into fuller reviews (beyond-the-veil, resonance-drift, etc.)