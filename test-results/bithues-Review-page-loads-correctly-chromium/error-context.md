# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: bithues.spec.js >> Review page loads correctly
- Location: tests/e2e/bithues.spec.js:19:1

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('.content-title')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('.content-title')

```

```yaml
- navigation:
  - link "Bithues":
    - /url: /
  - link "Reviews":
    - /url: /reviews.html
  - link "Find Books":
    - /url: /which-book-should-i-read-next/
  - link "Articles":
    - /url: /articles.html
  - link "Stories":
    - /url: /stories.html
  - link "About":
    - /url: /about.html
  - button "Search":
    - img
- main:
  - article:
    - text: Book Review January 2026
    - heading "The Richmond Cipher" [level=1]
    - link "The Richmond Cipher book cover":
      - /url: https://www.amazon.com/dp/B0GQCZKRGB?tag=michaelbacoti-20
      - img "The Richmond Cipher book cover"
    - paragraph: by E. Maris
    - paragraph: Historical Fiction
    - paragraph: A historical thriller that weaves cryptography, Civil War intrigue, and a family secret into a page-turning mystery.
    - paragraph: The Richmond Cipher opens in Confederate Richmond, 1863, where a young woman named Mary has been living inside the Executive Mansion as an unwitting intelligence asset. Her gift for codes and ciphers has made her valuable to the Confederacy, but when she discovers that her own family history is entangled with the cipher system she maintains, the stakes of her double life become personal in ways she did not anticipate. The tension between loyalty and identity drives the novel forward as Mary must decide what she owes to a cause she was born into rather than one she chose.
    - paragraph: E. Maris writes historical thriller with genuine command of the period. The detail work is impressive without being ornamental — the cipher mechanisms are explained with enough clarity for novices to follow while remaining faithful to period-accurate cryptographic practice. The novel succeeds when it trusts its protagonist to make difficult choices with imperfect information. Mary is not a superhero; she is a smart, resourceful person operating in circumstances she did not choose and cannot fully control.
    - paragraph: Her moral ambiguity is the book's most interesting dimension, and Maris resists the temptation to resolve it cleanly. The pacing balances atmospheric tension with active plot movement, and the historical setting is rendered with enough specificity to feel lived-in without drowning the narrative in period detail.
    - paragraph: The cipher elements are the real draw here, and Maris delivers them in a way that makes the reader want to work alongside the protagonist rather than simply watch her succeed. For readers who enjoy historical mysteries with intelligent protagonists and a strong sense of period atmosphere, The Richmond Cipher is a welcome addition to the genre.
    - paragraph: Enjoyed this review?
    - link "Buy on Amazon →":
      - /url: https://www.amazon.com/dp/B0GQCZKRGB?tag=michaelbacoti-20
- text: Share
- link "Share on X":
  - /url: https://x.com/intent/tweet?url=https%3A%2F%2Fwww.bithues.com%2Freviews%2Frichmond-cipher&text=The%20Richmond%20Cipher%20%E2%80%94%20Review%20%7C%20Bithues
  - img
- link "Share on Facebook":
  - /url: https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fwww.bithues.com%2Freviews%2Frichmond-cipher
  - img
- link "Share on LinkedIn":
  - /url: https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fwww.bithues.com%2Freviews%2Frichmond-cipher
  - img
- button "Copy link":
  - img
  - text: Copy
- contentinfo:
  - link "Bithues":
    - /url: /
  - navigation:
    - link "Find Books":
      - /url: /which-book-should-i-read-next/
    - link "Reviews":
      - /url: /reviews.html
    - link "Articles":
      - /url: /articles.html
    - link "Stories":
      - /url: /stories.html
    - link "About":
      - /url: /about.html
  - paragraph: © 2026 Bithues. All rights reserved.
```

# Test source

```ts
  1  | const { test, expect } = require('@playwright/test');
  2  | 
  3  | test('Homepage loads without errors', async ({ page }) => {
  4  |   const errors = [];
  5  |   page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  6  |   page.on('pageerror', err => errors.push(err.message));
  7  |   
  8  |   await page.goto('https://www.bithues.com');
  9  |   await expect(page.locator('.hero-title')).toBeVisible();
  10 |   expect(errors).toHaveLength(0);
  11 | });
  12 | 
  13 | test('Navigation links work', async ({ page }) => {
  14 |   await page.goto('https://www.bithues.com');
  15 |   await page.click('text=Reviews');
  16 |   await expect(page).toHaveURL(/reviews/);
  17 | });
  18 | 
  19 | test('Review page loads correctly', async ({ page }) => {
  20 |   const errors = [];
  21 |   page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  22 |   
  23 |   await page.goto('https://www.bithues.com/reviews/richmond-cipher');
> 24 |   await expect(page.locator('.content-title')).toBeVisible();
     |                                                ^ Error: expect(locator).toBeVisible() failed
  25 |   expect(errors).toHaveLength(0);
  26 | });
  27 | 
  28 | test('Mobile nav works', async ({ page }) => {
  29 |   await page.setViewportSize({ width: 375, height: 812 });
  30 |   await page.goto('https://www.bithues.com');
  31 |   // Verify nav is visible and links are tap-friendly
  32 |   await expect(page.locator('.nav')).toBeVisible();
  33 | });
```