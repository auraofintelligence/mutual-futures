# Implementation testing

18 September 2026. Actual generated pages and source JavaScript were tested with Chromium.

## Static build checks

The first complete GitHub Actions build passed all page, local-link, anchor, image-reference, language, heading, script-syntax and available-original checksum checks. It produced 22 HTML pages (21 chapters and utility pages plus 404), 10 source reading guides, 14 project connections and 15 external source records.

## Visual checks

Nine representative pages were rendered at 1440 x 1050 and 390 x 844: start, capital, workforce, intelligence, simulation, library, law, galactic and sources. All 18 checks reported no horizontal overflow, missing raster illustrations or JavaScript page exceptions. Desktop and mobile screenshots were visually inspected.

## Functional checks

36 checks passed after correcting Escape-key behaviour in the searchable chapter menu. Coverage includes finance arithmetic, zero-interest repayments, blank and invalid inputs, funding gaps, stress cases, Markdown downloads, work-and-life phase editing and the 16-phase limit, permissions Markdown and JSON downloads, dependency propagation, reset controls, search, source filtering and keyboard focus restoration.

The tested default acquisition scenario has A$1,300,000 uses, no funding gap and A$165,328.64 annual modelled debt service. These are invented assumptions, not a market valuation.

## Boundaries of these tests

Browser tests rendered actual generated HTML with source CSS/JavaScript in an isolated browser document. They did not navigate an authenticated service or a live GitHub Pages origin. They checked downloadable exports and graceful handling when browser storage is unavailable; persistence at a hosted origin has not been independently verified. The dependency tool is a fixed illustrative graph, not a real-world forecast. No external API, bank, payroll, medical or identity system is connected.

Original PDFs and DOCX files are included in the separately prepared complete handover package. The repository build reports originals absent until their actual bytes are uploaded to documents/originals. Reading guides are not original-file substitutes.
