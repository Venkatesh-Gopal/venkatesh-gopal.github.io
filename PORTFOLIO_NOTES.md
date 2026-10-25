# Bilingual engineering portfolio

English is served at `/`; German starts at `/de/`. There are five main navigation items and three project detail pages in each language. Language links retain the current page. The existing Jekyll project and publishing workflow are preserved.

## Content provenance

The uploaded website source and twelve English/German resumes inform the biography, work history, qualifications, tools, language levels, email, and LinkedIn profile. The engineering profile spans mechanical design, structural and thermomechanical analysis, material modelling, testing, and Python automation. The website's existing steel-repair project is retained without inventing personal responsibilities or results.

No disputed numerical performance figures, work-authorisation scope, managerial responsibilities, or unverified outcomes are published. Part-time research and the short-term March 2026 contract are identified. Project graphics are explicitly labelled illustrations, not simulation results. Template portraits and CV assets are not presented as the user's photo or resume.

## Implementation

`_data/portfolio.json` is the bilingual content source. `bin/build_portfolio.py` generates the complete HTML pages with `layout: null`, preserving existing routes. CSS, JavaScript, and illustrations live in `assets/portfolio/`. The deployment and portfolio-check workflows regenerate pages before the Jekyll build. `bin/preview_portfolio.py` supports a portfolio-only preview without Jekyll.

See `UPDATE_GUIDE.md` for installation, editing, changed files, and validation limitations. This archive has not been pushed to GitHub or deployed.
