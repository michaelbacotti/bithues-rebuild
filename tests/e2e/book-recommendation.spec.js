const { test, expect } = require('@playwright/test');

test('Book recommendation quiz loads and works', async ({ page }) => {
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  
  await page.goto('https://www.bithues.com/which-book-should-i-read-next/');
  await expect(page.locator('.hero-title')).toBeVisible();
  
  // Click through a few questions
  await page.click('text=Adventurous');
  await page.click('text=Relaxing');
  await page.click('text=Light and easy');
  await page.click('text=Fiction');
  await page.click('text=Short');
  await page.click('text=Entertaining');
  await page.click('text=Anyone');
  
  // Check results appeared
  await expect(page.locator('#results')).toBeVisible();
  expect(errors).toHaveLength(0);
});