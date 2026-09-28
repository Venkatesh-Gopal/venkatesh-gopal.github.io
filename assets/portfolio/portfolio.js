(() => {
  const root = document.documentElement;
  const button = document.querySelector(".theme-toggle");
  const preference = window.matchMedia("(prefers-color-scheme: dark)");
  let chosen = null;
  try {
    chosen = localStorage.getItem("vg-colour-theme");
  } catch (_) {
    /* Storage may be disabled. */
  }
  const apply = (value) => {
    root.dataset.theme = value;
    button?.setAttribute("aria-pressed", String(value === "dark"));
  };
  apply(chosen === "dark" || chosen === "light" ? chosen : preference.matches ? "dark" : "light");
  if (button) {
    button.hidden = false;
    button.addEventListener("click", () => {
      chosen = root.dataset.theme === "dark" ? "light" : "dark";
      apply(chosen);
      try {
        localStorage.setItem("vg-colour-theme", chosen);
      } catch (_) {
        /* Keep the toggle functional. */
      }
    });
  }
  preference.addEventListener("change", (event) => {
    if (!chosen) apply(event.matches ? "dark" : "light");
  });
})();
