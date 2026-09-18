# Mutual Futures

**From business succession to mutual wealth, universal intelligence and more possible lives.**

A standalone public workbench by Luke Nathan Hayes / Strange But True / Aura of Intelligence. It connects voluntary succession of existing staffed businesses with member ownership, upgrading, Try Everything Once, Intermittent Retirement, universal intelligence and universal adequate income, legal reflection and radical overcompliance, civic health research, existential resilience, world travel and Kardashev galactic games.

**Repository:** https://github.com/auraofintelligence/mutual-futures

**Intended public page:** https://auraofintelligence.github.io/mutual-futures/

## Build and publishing status

The complete static website is committed in [`site/`](site/). GitHub Actions successfully generated and checked the site on 18 September 2026. It contains 21 chapter and utility pages plus a custom 404, four browser-local tools, ten source reading guides, fourteen project connections and fifteen external source records. See [`site/build-report.md`](site/build-report.md) and the [checked build run](https://github.com/auraofintelligence/mutual-futures/actions/runs/35311007789).

**The public Pages deployment is not yet verified live.** The build passed, but the first-time Pages enablement step returned `Resource not accessible by integration`. An owner can resolve that setting at [Settings > Pages](https://github.com/auraofintelligence/mutual-futures/settings/pages): under Build and deployment, select **GitHub Actions** as the source. Then re-run the failed deployment or run the publishing workflow from the [Actions page](https://github.com/auraofintelligence/mutual-futures/actions/workflows/publish.yml).

No Notion, Google Drive or other staging service is needed by the website or its deployment workflow.

## What is included

- Multi-page, responsive HTML with purple, teal and gold styling, raster illustrations and a PNG favicon.
- A searchable site index, previous/next chapter navigation, back-to-top controls, keyboard access and reduced-motion support.
- Browser-local tools for capital allocation, work-and-life planning, permissions and dependency scenarios. These are exploratory tools, not financial forecasts or a complete simulation of society.
- A source library with ten reading guides, original-document metadata and checksums. **The unchanged PDF/DOCX originals are not yet present in this repository.** Reading guides are not labelled as original documents.
- Fourteen related-project links with their respective purposes. An outbound connection does not itself confirm a reciprocal edit to the linked project.
- A [comprehensive About description](ABOUT.md), source attribution and [Strange But True Public Source Licence](LICENCE.md).

The site does not collect accounts, analytics, personal profiles or form submissions. No font files are bundled. Source-project illustrations retain their provenance. The implementation contains no SVG assets.

## Scope and status of the ideas

The content distinguishes Luke's proposals, source documents, illustrative calculations, prototype tools and independently sourced facts. Participation, personal data, cultural authority and political choice remain distinct from ownership of commercial assets. No founder or other veto powers are proposed.

The legal reflection and proposed cyber-republic referendum horizon no later than 2031 are Luke's stated project aims, not an official referendum announcement or a predicted result. The legal engine has a separate development path; its integration into the Aura app is not claimed complete. Health and existential-threat research retain their respective evidence and development status.

This workbench is not an operating acquisition fund, an investment offer or a claim that the proposed transition has already occurred.

## Local build

Use Python 3.12 or a compatible Python 3 installation:

```sh
python tools/fetch_assets.py
python tools/build.py
python tools/check.py
node --check assets/app.js
python -m http.server 8000 --directory site
```

Then open `http://localhost:8000`. The asset-fetch step needs internet access on the first run; already committed assets remain available locally. Generated pages are stored in `site/`. The GitHub workflow performs the build and checks before attempting Pages deployment.

## Repository About settings

The longer description, suggested GitHub description, public-page URL and topic list are prepared in [`ABOUT.md`](ABOUT.md). This file is not a claim that GitHub's separate sidebar settings have already been changed.

Suggested topics:

`mutual-wealth` `business-succession` `cooperatives` `workforce-transition` `try-everything-once` `intermittent-retirement` `universal-intelligence` `adequate-income` `sovereign-ai` `digital-twins` `legal-reflection` `existential-resilience` `civic-health` `queensland` `oceania` `gajra-earth` `aura-of-intelligence` `kardashev` `world-travel` `github-pages`

## Authorship and licence

Concept, direction and source family: Luke Nathan Hayes / Strange But True / Aura of Intelligence. This implementation was prepared with ChatGPT. Earlier projects retain their original collaborator credits.

Strange But True Public Source Licence: non-commercial reuse with attribution; commercial, corporate, institutional and government uses require separate written permission. This is public-source work, not an unrestricted open-source licence.
