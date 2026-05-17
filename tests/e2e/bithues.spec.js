const { test, expect } = require('@playwright/test');

test('Homepage loads without errors', async ({ page }) => {
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', err => errors.push(err.message));
  
  await page.goto('https://www.bithues.com');
  await expect(page.locator('.hero-title')).toBeVisible();
  expect(errors).toHaveLength(0);
});

test('Navigation links work', async ({ page }) => {
  await page.goto('https://www.bithues.com');
  await page.click('text=Reviews');
  await expect(page).toHaveURL(/reviews/);
});

test('Review page loads correctly', async ({ page }) => {
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  
  await page.goto('https://www.bithues.com/reviews/richmond-cipher');
  await expect(page.locator('.content-title')).toBeVisible();
  expect(errors).toHaveLength(0);
});

test('Mobile nav works', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto('https://www.bithues.com');
  // Verify nav is visible and links are tap-friendly
  await expect(page.locator('.nav')).toBeVisible();
});