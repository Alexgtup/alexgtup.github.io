# Stage 18 — International authority layer

Date: 2026-09-06

## Added
- /en/cases/ hub
- /en/cases/auto-crm/
- /en/cases/taxi-app/
- /en/cases/factory-catalog/
- /en/guides/ hub
- /en/guides/development-cost/
- /en/guides/telegram-bot-cost/
- /en/guides/bot-vs-mini-app-vs-web/
- /en/guides/n8n-vs-make/
- /en/project-repair/
- /en/feed.xml

## Technical changes
- English navigation now points to proper Cases and Guides hubs.
- Mobile English drawer added.
- Person schema uses one canonical @id: https://alexgtup.github.io/#person.
- Sitemap includes hreflang annotations for RU/EN pairs.
- Russian paired pages now expose English alternates for the new case/guide routes.
- Analytics click goals recognize English services, cases, guides and About.

## Intent
The English cluster now has both commercial pages and supporting proof/educational content. This gives search engines and answer systems clearer evidence for claims about CRM, Telegram, automation, web, mobile and project repair without creating thin keyword variants.

## Validation
- 58 unique sitemap URLs.
- 0 missing sitemap pages.
- 0 broken internal links.
- 0 duplicate titles.
- 0 duplicate canonicals.
- JSON-LD parses successfully on all indexed HTML pages.
- English pages have en / ru / x-default hreflang in HTML.
- Sitemap contains 162 xhtml hreflang alternate links.
- English RSS and main RSS are valid XML.
- site-enhancements.js passes node --check.
- Responsive QA: 58 routes × 6 widths (320, 390, 768, 1024, 1440, 1920) = 348 checks.
- Document horizontal overflow: 0.
- H1 count errors: 0.
- English internal element overflow: 0.
- English mobile drawer opens correctly and exposes Services, Cases, Guides, About, RU and Telegram.

## Visual review
Final renders were reviewed at 390px and 1440px for the English home, Services, About, Cases, CRM case, Guides, development-cost guide and project-repair page.
