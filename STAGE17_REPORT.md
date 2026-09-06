# Stage 17 — International SEO / English

Built: 2026-09-06

## Added

- English section under `/en/` with 17 localized pages.
- Separate English self-canonical URLs.
- Bidirectional `hreflang` for mapped RU/EN page pairs plus `x-default` to Russian.
- Visible RU/EN language switch on mapped Russian pages and all English pages.
- English Service / FAQ / Breadcrumb / Person / CreativeWork structured data.
- English privacy page for international visitors.
- English URLs added to sitemap and `llms.txt`.
- Dedicated responsive `assets/international.css`.
- CI checks for the English layer.

## Important

Russian URLs were not moved. Existing indexed or submitted Russian URLs remain unchanged.
English pages use unique translated body content, not only translated navigation.

## Validation

- 48 unique URLs in sitemap (31 existing Russian + 17 English).
- 17 reciprocal RU/EN hreflang pairs.
- 0 missing sitemap pages.
- 0 duplicate titles.
- 0 canonical mismatches or duplicate canonicals.
- 0 JSON-LD parse errors.
- 0 internal broken links.
- 0 images without explicit width/height.
- 288 Chromium layout checks: 48 pages × 6 widths (320, 390, 768, 1024, 1440, 1920), 0 horizontal overflow and 0 H1 errors.
- Visual screenshots reviewed for English home, services, Telegram bot service, Fin Planner case, About, and the Russian homepage with the new language layer.
- `site-enhancements.js` passes `node --check` after adding the mobile English switch.

Chromium navigation to localhost/live URLs is blocked by the execution environment, so the responsive pass renders the exact built HTML and CSS with Chromium `set_content`; this still exercises real layout/CSS at each viewport rather than only parsing styles statically.
