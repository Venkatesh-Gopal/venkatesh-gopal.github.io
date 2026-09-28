const { test, expect } = require("@playwright/test");
const routes = [
  "/",
  "/projects/",
  "/experience/",
  "/skills/",
  "/contact/",
  "/projects/steel-repair/",
  "/projects/adhesive-fracture/",
  "/projects/honeycomb/",
];
for (const width of [390, 1440]) {
  for (const language of ["en", "de"]) {
    test(`${language} navigation at ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      for (const route of routes) {
        await page.goto((language === "de" ? "/de" : "") + route);
        await expect(page.locator("html")).toHaveAttribute("lang", language);
        await expect(page.locator("h1")).toHaveCount(1);
        expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBeTruthy();
        await page.locator(`.language-switch a[lang="${language === "de" ? "en" : "de"}"]`).click();
        expect(new URL(page.url()).pathname).toBe((language === "de" ? "" : "/de") + route);
      }
    });
  }
}
test("colour preference survives navigation and reload", async ({ page }) => {
  await page.emulateMedia({ colorScheme: "light" });
  await page.goto("/");
  await page.locator(".theme-toggle").click();
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
});
test("language switching works without JavaScript", async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto("http://127.0.0.1:8765/projects/");
  await page.locator('.language-switch a[lang="de"]').click();
  expect(new URL(page.url()).pathname).toBe("/de/projects/");
  await context.close();
});
