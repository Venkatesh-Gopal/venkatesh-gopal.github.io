# Website update — English and German

This small archive contains only the 28 changed or new files. Apply it to your existing repository or an extracted copy of your original ZIP. It has not been pushed or deployed.

## Apply the update

1. Extract the ZIP on your computer.
2. Open your existing `venkatesh-gopal.github.io` checkout.
3. Copy all extracted files and folders into your existing repository root, replacing matching files. Include the updated `.github` workflow files. This is an update package: retain all other existing repository files.
4. Review the changes and commit them to your usual `main` or `master` branch. The existing deployment workflow builds and publishes the site. Alternatively, open a pull request first to review the GitHub checks before merging.
5. Wait for **Portfolio checks** and **Deploy site** in GitHub Actions. Check the English and German pages after deployment. If your Pages settings already use the workflow's publishing branch, leave them unchanged.

For the exact changed/new file list, see **Changed files** below. Existing unrelated source files are preserved.

## What changed

- English and German content across all five main pages and three project detail pages.
- Mechanical engineering positioning spanning design, simulation, validation, and Python automation.
- Five navigation items only: Home / Projects / Experience / Skills / Contact; translated equivalents in German.
- Three project pages remain under Projects; language switches retain the current page.
- Work history and education from the supplied resumes; broader skills and training.
- Direct email, LinkedIn, and GitHub links.
- Expanded project questions, technical scope, and engineering relevance.
- Browser titles, descriptions, and responsive styles.
- Deployment regenerates the pages from the bilingual content file.

Numerical performance figures, broad work-authorisation claims, management experience, and unverified project outcomes have not been added. Project illustrations remain labelled as illustrations.

## Edit later

The source of the English and German copy is `_data/portfolio.json`. The renderer is `bin/build_portfolio.py`; the complete generated pages are in `_pages/portfolio-*.html`. Edit the JSON, then regenerate:

```bash
python3 bin/build_portfolio.py
npm ci
npx prettier '_pages/portfolio-*.html' _pages/404.md _data/portfolio.json assets/portfolio/portfolio.css --write
```

Keep both languages aligned when changing dates, responsibilities, project descriptions, or contact information.

## Local preview without Jekyll

```bash
python3 bin/preview_portfolio.py
python3 test/check_portfolio.py .preview
python3 -m http.server 8765 --directory .preview
```

Open `http://localhost:8765/` and `http://localhost:8765/de/`. This preview renders only the portfolio pages and assets; it does not run Jekyll, plugins, sitemap generation, or the production workflow.

## Production validation

On a machine with Ruby/Bundler and the project dependencies:

```bash
bundle install
bundle exec jekyll build
python3 test/check_portfolio.py _site
```

Use the root-domain configuration already in this repository: `baseurl` remains empty. The original template's `/al-folio` example does not apply to this site.

## Verification in this editing environment

- Passed: all 16 portfolio pages, internal links, exactly five navigation items, active navigation, paired language routes and metadata, direct contact links, work-history presence, and demo-page exclusion in the portfolio-only preview.
- Passed: Python compilation, JavaScript syntax, starter style contract, and formatting checks.
- Not run: full Jekyll build (Ruby/Bundler unavailable).
- Not verified: rendered desktop/mobile appearance or interactive theme behaviour (managed preview service unavailable). Responsive CSS and the existing theme script are included, but browser verification is still required.

## Changed files

- `.github/workflows/deploy.yml`
- `.github/workflows/unit-tests.yml`
- `.gitignore`
- `PORTFOLIO_NOTES.md`
- `UPDATE_GUIDE.md`
- `_config.yml`
- `_data/portfolio.json`
- `_pages/404.md`
- `_pages/portfolio-de-about.html`
- `_pages/portfolio-de-contact.html`
- `_pages/portfolio-de-experience.html`
- `_pages/portfolio-de-projects-adhesive-fracture.html`
- `_pages/portfolio-de-projects-honeycomb.html`
- `_pages/portfolio-de-projects-steel-repair.html`
- `_pages/portfolio-de-projects.html`
- `_pages/portfolio-de-skills.html`
- `_pages/portfolio-en-about.html`
- `_pages/portfolio-en-contact.html`
- `_pages/portfolio-en-experience.html`
- `_pages/portfolio-en-projects-adhesive-fracture.html`
- `_pages/portfolio-en-projects-honeycomb.html`
- `_pages/portfolio-en-projects-steel-repair.html`
- `_pages/portfolio-en-projects.html`
- `_pages/portfolio-en-skills.html`
- `assets/portfolio/portfolio.css`
- `bin/build_portfolio.py`
- `bin/preview_portfolio.py`
- `test/check_portfolio.py`
