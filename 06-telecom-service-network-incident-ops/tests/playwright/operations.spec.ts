import { test, expect } from '@playwright/test';

test('operations page shell loads', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('body')).toBeVisible();
});
