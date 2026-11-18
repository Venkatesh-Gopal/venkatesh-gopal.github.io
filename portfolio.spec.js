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
        await test.step(`${language} ${route} at ${width}px`, async () => {
          await page.goto((language === "de" ? "/de" : "") + route);
          await expect(page.locator("html")).toHaveAttribute("lang", language);
          await expect(page.locator("h1")).toHaveCount(1);
          await page.evaluate(() => document.fonts.ready);
          const layout = await page.evaluate(() => {
            const viewport = innerWidth;
            return {
              viewport,
              documentWidth: document.documentElement.scrollWidth,
              overflowing: [...document.querySelectorAll("body *")]
                .filter((element) => {
                  const box = element.getBoundingClientRect();
                  return box.width > 0 && (box.right > viewport || box.left < 0);
                })
                .slice(0, 10)
                .map((element) => `${element.tagName.toLowerCase()}.${element.className}`),
            };
          });
          expect(layout.documentWidth, `Horizontal overflow on ${page.url()}: ${JSON.stringify(layout)}`).toBeLessThanOrEqual(layout.viewport);
          const target = (language === "de" ? "" : "/de") + route;
          await page.locator(`.language-switch a[lang="${language === "de" ? "en" : "de"}"]`).click();
          await page.waitForURL((url) => url.pathname === target);
          expect(new URL(page.url()).pathname).toBe(target);
        });
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
  await page.waitForURL((url) => url.pathname === "/de/projects/");
  expect(new URL(page.url()).pathname).toBe("/de/projects/");
  await context.close();
});
