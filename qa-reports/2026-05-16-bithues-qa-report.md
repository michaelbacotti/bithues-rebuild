# Bithues QA Report — 2026-05-16

## Timestamp
2026-05-16T21:58-22:02 EDT

## Site Tested
https://www.bithues.com

## Pages Checked
- Homepage (/)
- Reviews listing (/reviews)
- Sample review (/reviews/richmond-cipher)
- Book quiz (/which-book-should-i-read-next)

## Tools Used

### Linkinator
**Status:** PASSED
- Scanned homepage recursively
- All internal and external links returned HTTP 200
- No broken links detected

### Pa11y (WCAG2AA)
**Status:** Issues found on all pages (exit code 2 = errors detected)
- Homepage: 9 accessibility errors
- Reviews: 3 accessibility errors  
- Quiz: 2 accessibility errors
- Total: 14 issues

**Issues by type:**
1. Missing labels on search input (`#site-nav > nav > div > div:nth-child(3) > div > input`) — affects all pages
2. Insufficient color contrast (4.48:1 vs required 4.5:1) on `.pill-book-review` and `.pill-book-story` spans — background #fbf9f6 recommended
3. Empty heading rank on review pages (skipped h2/h3 nesting)

### Playwright E2E
**Status:** 3/5 passed

**Passed:**
- Homepage loads without errors ✓
- Navigation links work ✓  
- Mobile nav visible ✓

**Failed:**
- Review page (`.content-title` selector not found — page uses `<h1 style="...">` inline, no `.content-title` class)
- Book quiz (quiz answers use "Brief and punchy" not "Short" — test selectors don't match actual button text)

## Accessibility Issues Found (Priority Order)

1. **[HIGH] Search input lacks label** — `WCAG2AA.Principle4.Guideline4_1.4_1_2.H91.InputText.Name`
   - Affects: All pages with nav search
   - Fix: Add `aria-label="Search"` or wrap `<input>` in `<label>` to search input

2. **[MEDIUM] Color contrast on pill tags** — `WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail`
   - Elements: `.pill-book-review`, `.pill-book-story` text (4.48:1 instead of 4.5:1)
   - Fix: Change background to `#fbf9f6` or darken text to `#2c1f14`

3. **[LOW] Heading hierarchy gaps on review pages**
   - Review pages skip h2/h3, jumping from h1 to h4
   - Fix: Add intermediate heading levels

## Recommended Fixes

1. Add `aria-label="Search books, authors, and topics"` to the search `<input>` in nav.js
2. Change pill tag background to `#fbf9f6` in style.css for `.pill-book-review` and `.pill-book-story`
3. Update Playwright tests to use correct selectors (`.hero-title` instead of `.content-title`, correct quiz answer text)
4. Add h2/h3 headings to review page template

## QA Stack Files Created

```
tests/e2e/bithues.spec.js
tests/e2e/book-recommendation.spec.js
playwright.config.js
linkinator.config.json
.pa11yrc
qa-reports/pa11y-homepage.json
qa-reports/pa11y-reviews.json
qa-reports/pa11y-quiz.json
```

## Git Status

NOT committed — pending review of test failures before committing. The test failures are test-authoring issues (wrong selectors), not site issues.

## Summary

Site is healthy: all pages return HTTP 200, no broken links. 3 Playwright tests pass. 2 tests fail due to incorrect test selectors (not site bugs). 14 accessibility issues found, all fixable. Search input labeling and color contrast are the highest-priority fixes.