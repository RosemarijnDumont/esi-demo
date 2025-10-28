// tests/ui/darkMode.spec.js
import { test, expect } from '@playwright/test';

test.describe('Dark Mode Functionality and Contrast', () => {

    test.beforeEach(async ({ page }) => {
        await page.goto('/'); // Adjust to your application's base URL
    });

    test('should toggle to dark mode and apply dark mode styles', async ({ page }) => {
        // Initial state: should be light mode or system preferred, we'll assume light for this test start
        const body = page.locator('body');
        await expect(body).not.toHaveClass(/dark-mode/);

        // Toggle theme to dark mode
        await page.locator('button', { hasText: 'Toggle Theme' }).click();
        await expect(body).toHaveClass(/dark-mode/);

        // Verify a dark mode specific style (e.g., background color)
        const bgColor = await body.evaluate((ele) => {
            return window.getComputedStyle(ele).getPropertyValue('background-color');
        });
        // Expect a dark background color (adjust hex/rgb as per your CSS)
        expect(['rgb(18, 18, 18)', '#121212']).toContain(bgColor);

        // Verify a neutral element's color in dark mode
        const paragraphColor = await page.locator('p').first().evaluate((ele) => {
            return window.getComputedStyle(ele).getPropertyValue('color');
        });
        expect(['rgb(224, 224, 224)', '#e0e0e0']).toContain(paragraphColor); // Light text in dark mode
    });

    test('should maintain sufficient contrast in dark mode', async ({ page }) => {
        // Ensure dark mode is active for contrast testing
        const body = page.locator('body');
        if (!(await body.hasClass('dark-mode'))) {
            await page.locator('button', { hasText: 'Toggle Theme' }).click();
            await expect(body).toHaveClass(/dark-mode/);
        }

        // Example: Check contrast for text on a card background
        const card = page.locator('.card');
        const cardBgColor = await card.evaluate((ele) => {
            return window.getComputedStyle(ele).getPropertyValue('background-color');
        });
        const cardTextColor = await page.locator('.card p').first().evaluate((ele) => {
            return window.getComputedStyle(ele).getPropertyValue('color');
        });

        // These are example color values. You might need a more robust contrast checking library
        // or to convert RGB to a comparable format and calculate luminance ratio if precise AA/AAA is needed.
        // For simplicity, we're checking for expected dark background and light text.
        expect(['rgb(30, 30, 30)', '#1e1e1e']).toContain(cardBgColor); // Dark card background
        expect(['rgb(224, 224, 224)', '#e0e0e0']).toContain(cardTextColor); // Light text on card

        // A real contrast check would involve converting colors to a luminance value and calculating ratio.
        // For Playwright, this often means integrating with a separate accessibility testing library like axe-core.

        // Example: Further check for primary button contrast
        const primaryButton = page.locator('.btn-primary');
        const btnBgColor = await primaryButton.evaluate(ele => window.getComputedStyle(ele).getPropertyValue('background-color'));
        const btnTextColor = await primaryButton.evaluate(ele => window.getComputedStyle(ele).getPropertyValue('color'));

        expect(['rgb(100, 181, 246)', '#64b5f6']).toContain(btnBgColor); // Light blue button
        expect(['rgb(18, 18, 18)', '#121212']).toContain(btnTextColor); // Dark text on button
    });

    test('should apply responsive styles on smaller screens', async ({ page }) => {
        await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE size

        const navbar = page.locator('.navbar');
        await expect(navbar).toHaveCSS('flex-direction', 'column');

        const navMenuItem = page.locator('.navbar-menu');
        await expect(navMenuItem).toHaveCSS('display', 'none'); // Hidden by default

        // Simulate menu toggle if you have one
        // await page.locator('.menu-toggle-button').click();
        // await expect(navMenuItem).toHaveCSS('display', 'flex');

        await page.setViewportSize({ width: 768, height: 1024 }); // iPad portrait size
        await expect(page.locator('body')).toHaveCSS('font-size', '14px'); // Example font size adjustment
    });
});
