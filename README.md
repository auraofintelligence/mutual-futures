# Mutual Futures

**An AI future worth living in.**

A public proposal by Luke Nathan Hayes for global systems change during the AI and automation transition, guided by Joyful Responsible Abundance. GAJRA Earth connects human self-alignment and AI alignment; Mutual Futures connects productive ownership, income, learning, care and time. Queens contributes women's leadership and enterprise development. C-Hour recognises voluntary contribution alongside paid work and shared prosperity.

**Repository:** https://github.com/auraofintelligence/mutual-futures

**Public page:** https://auraofintelligence.github.io/mutual-futures/

## Build and publishing status

The site uses one font family and four text roles, with an 18px minimum. Titles and introductions precede full-width artwork displayed at its natural proportions, without cropping or dark overlays. The favicon is original AI-generated artwork; its prompt and files are recorded in [favicon-generation.md](docs/favicon-generation.md). The [whole-systems review](docs/whole-systems-editorial-review.md) explains the 24 September content, layout and image revision. Build files use explicit UTF-8 and LF line endings.

The complete static website is committed in [`site/`](site/). It contains 25 chapter and utility pages plus a custom 404, four browser-local tool pages, thirteen reading guides, three unchanged originals, seventeen project connections and fifteen external source records. See [`site/build-report.md`](site/build-report.md).

The build supports GitHub Actions or main / (root) publishing. The live-verification workflow compares deployed pages and linked downloads with the checked build by checksum. Use the dated workflow artifact for the release under review; the older [live-check.json](docs/live-check.json) is a historical snapshot.

No Notion, Google Drive or other staging service is needed by the website or its deployment workflow.

## What is included

- Multi-page, responsive HTML with a neutral light theme, consistent typography, original photorealistic AI concept visuals and an original PNG favicon.
- A searchable site index, previous/next chapter navigation, back-to-top controls, keyboard access and reduced-motion support.
- Browser-local tools for capital allocation, work-and-life planning, permissions and dependency scenarios. These are exploratory tools, not financial forecasts or a complete simulation of society.
- A source library with thirteen reading guides and three unchanged originals: the current C-Hour, Queens and UNGA81 plans. The ten earlier originals remain unavailable in this repository.
- Seventeen related-project records with distinct purposes. The [reciprocal-link audit](docs/reciprocal-links.json) covers the original fourteen connections, not the three newly added records.
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

## Generational handover and technology upgrades

The public narrative connects retiring owners' next chapters with younger generations learning from their knowledge while upgrading businesses through AI, robotics and extended reality (XR) just-in-time learning. Fourteen original photorealistic concept visuals support that story, including eleven distinct Australian business and technology-manufacturing scenes. Each scene is used once across the public pages. Their prompts and asset paths are in [generated-visuals.md](docs/generated-visuals.md).

Tool explanations now precede their controls. Defaults are explained using Real Pickles' reported 2013 community funding campaign, the Victorian teaching-service sabbatical scheme, the OAIC's fictionalised CarCover case and AEMO's report on South Australia's 2016 electricity outage. The general Australian-dollar acquisition-and-upgrade calculator starts blank because transaction assumptions require actual records and quotes.
