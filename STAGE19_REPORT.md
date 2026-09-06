# Stage 19 — Stability, metadata and crawl hardening

Date: 2026-09-06

## Why this stage exists

Stage 15–18 exposed a deployment weakness: the GitHub Actions validator looked for a literal HTML attribute order in canonical tags. Valid HTML such as `<link href="..." rel="canonical">` failed a check that expected `rel="canonical"` first. The site content was correct, but deployment stopped before GitHub Pages publication.

Stage 19 replaces brittle string matching with parser-based validation and tightens metadata/crawl quality without adding more doorway-style SEO pages.

## Fixes

- Replaced canonical grep checks with `scripts/validate_site.py`, using Python stdlib HTMLParser.
- Updated `actions/upload-pages-artifact` to v4.
- Validator checks sitemap URLs, canonical equality, unique titles/canonicals, descriptions, H1, robots, JSON-LD, images, local internal links, target=_blank security, RSS, hreflang reciprocity and image budgets.
- Privacy pages are now `noindex,follow` and removed from sitemap. They remain accessible from the footer.
- All indexable pages use the same robots directive with large image/snippet/video previews allowed.
- Added a neutral 1200×630 Open Graph preview image for pages that had no social image.
- Standardized Twitter cards to `summary_large_image` and added image alt/dimensions.
- Added explicit `noopener noreferrer` to external links opened in a new tab.
- Shortened titles that exceeded a practical SERP length while preserving the main query intent.
- Filled structured-data gaps: Article publication dates/publisher and missing CreativeWork author.
- Unified the canonical Person entity URL across RU/EN while keeping localized profile pages.
- Rebuilt 404 as bilingual: `/en/...` errors now show English actions and copy.
- Added keyboard skip links and reduced-motion support.

## Final local validation

- 56 indexable URLs in sitemap.
- 58 content pages checked (56 indexable + 2 noindex privacy pages).
- 62 HTML files including 404/verification files.
- 0 duplicate titles.
- 0 duplicate canonicals.
- 0 missing descriptions.
- 0 missing H1 on content pages.
- 0 missing OG/Twitter core metadata.
- 0 missing internal assets/resources.
- 0 target=_blank links without noopener+noreferrer.
- 0 JSON-LD parse errors.
- RU and EN feeds parse successfully.

## Search-result gap observed

Current competing pages in Telegram/Mini App/CRM queries often surface concrete proof near the top: starting price, delivery range, source-code ownership, real demos/cases, reviews, or explicit post-launch support. Alexuys already has cases and direct-developer positioning, but no verified public review count or universal fixed price. Stage 19 intentionally does not invent those signals.

Next ranking gains should come from stable publication/indexation first, then real proof and external mentions rather than another large batch of near-duplicate service pages.
