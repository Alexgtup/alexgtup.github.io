# SiteAudit Studio

Deterministic technical website audit for public HTTP(S) sites. Enter a URL, receive an explainable report, then work through concrete issues instead of an opaque AI-generated score.

## MVP checks

- HTTP status and redirect chain;
- title, description, H1, canonical and robots meta;
- robots.txt discovery and basic blocking detection;
- sitemap discovery and URL count;
- limited crawl of internal HTML pages;
- sampled internal-link status checks;
- image `alt`, document language and viewport;
- HTTPS and baseline security headers;
- category scores and prioritized recommendations;
- shareable `?url=` report link.

## Security model

The auditor makes outbound requests, so SSRF protection is part of the product:

- only `http:` and `https:` targets are accepted;
- localhost and local-style hostnames are rejected;
- DNS is resolved before every request;
- every resolved address must be public unicast;
- the HTTP request is pinned to the validated IP while preserving the original `Host` header and TLS SNI;
- every redirect target is validated again;
- redirect count, response size and time are limited;
- audit API is rate-limited.

## Stack

`Node.js 20+` · `Express` · `Cheerio` · `Helmet` · `express-rate-limit` · `ipaddr.js` · vanilla HTML/CSS/JS

No paid AI API is required.

## Local run

```bash
npm install
npm test
npm start
```

Open `http://localhost:3000`.

## Render

Root directory: `projects/siteaudit-studio`

Build command: `npm install`

Start command: `npm start`

## Portfolio purpose

The project is intended to become a live demo, RU/EN case study, technical SEO search entry point and practical tool used during real website reviews.

Portfolio: https://alexgtup.github.io/
