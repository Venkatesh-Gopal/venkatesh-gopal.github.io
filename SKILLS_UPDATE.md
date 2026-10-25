# Skills cards update — English and German

This is a cumulative update package. It includes the previous website update plus the new skills cards. Use this ZIP instead of the previous website-update.zip. It contains changed files only, not the whole repository.

## Install

1. Extract the ZIP.
2. Upload all contents to the root of your existing GitHub repository, replacing matching files. Include `.github` and retain all other existing files.
3. Commit and wait for GitHub Actions to finish.
4. Check `/skills/` and `/de/skills/`.

## New skills layout

Eight technical cards plus a language card, using the existing font families and green palette. Tools and methods are separate groups of pill-shaped labels.

- FEA and structural simulation
- Mechanical design and CAD
- Python and CAE automation
- CFD simulation
- AI and surrogate modelling
- Materials and failure
- Testing and validation
- CAE model preparation and evaluation
- Languages

Desktop: four columns; intermediate widths: two; mobile: one. Language levels and tools follow the supplied resumes. No proficiency scores or unsupported software from the reference example have been added.

The seven other pages in each language are unchanged from the previous update. Existing stylesheet rules are preserved, with skills-specific rules appended. No menu changes were made beyond those already present in the previous update.

## Verification

Passed: all 16 pages, local links, paired languages, five-item menus, contact links, Python/JavaScript syntax and starter style contract. Both skills pages contain nine cards. Existing non-skills pages match the previous update exactly.

Browser rendering remains unverified because the preview service is unavailable. The production Jekyll build must run in GitHub Actions; Ruby is unavailable here.

## AI and surrogate modelling addition

The new card includes LS-OPT and Python, surrogate modelling, surrogate-based optimisation, material-parameter calibration, and AI-assisted engineering workflows. Specific AI frameworks and model-training experience are not claimed. This version supersedes website-update-v2.zip.
