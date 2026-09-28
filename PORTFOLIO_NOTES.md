# Bilingual portfolio update

The portfolio now has five navigation sections in English and German, three project detail pages in each language, and a custom 404 page. Language links retain the current page. The pages work without JavaScript; JavaScript adds only a persistent colour theme toggle. Assets are local and no external fonts or translation services are loaded.

English remains at `/`; German starts at `/de/`. Existing English section URLs are preserved. The site remains an al-folio/Jekyll project and retains its deployment workflow.

## Content provenance

Biography, qualifications, language levels and project topics come from the uploaded `_pages/About.md`. Employment dates, numerical results, software proficiency, email and LinkedIn were not supplied and have not been invented. Project graphics are explicitly labelled illustrations, not analysis results. The supplied portraits and CV are Einstein demo assets; they are not presented as Venkatesh's photo or CV. GitHub is the only supplied professional profile.

## Implementation

`_data/portfolio.json` contains the English and German copy. `bin/build_portfolio.py` generates the complete HTML pages, with `layout: null` so that no theme templates are overridden. Custom CSS, JavaScript and SVGs live in `assets/portfolio/`. Original demo source files are retained but excluded from the public build. The starter integration workflow is replaced with portfolio-specific checks because the upstream tests require publishing the demo pages.

## Validation

All 16 pages passed static checks for internal links, paired language metadata, HTML language attributes and demo-content exclusion. JavaScript syntax, the starter style contract and repository-wide Prettier formatting passed. The CSS includes desktop and mobile layouts. Browser execution failed in this environment, so responsive rendering, interactive theme behaviour and visual appearance could not be verified in a running browser. Ruby/Bundler is unavailable in the editing environment, so the complete Jekyll build and plugin audit could not be run locally. The GitHub deployment workflow retains the real Jekyll build, and the portfolio check workflow validates its output.

This archive is an edited repository snapshot. It has not been pushed to GitHub or deployed to the live website.
