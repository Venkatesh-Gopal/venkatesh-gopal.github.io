const { defineConfig } = require("@playwright/test");
module.exports = defineConfig({
  testDir: ".",
  testMatch: "portfolio.spec.js",
  use: { baseURL: "http://127.0.0.1:8765", screenshot: "only-on-failure" },
  webServer: { command: "python3 -m http.server 8765 --directory _site", cwd: require("node:path").resolve(__dirname, ".."), port: 8765 },
});
