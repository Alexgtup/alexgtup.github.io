# Stage 20 — Telegram authority cluster and commercial proof

Date: 2026-09-06

## Goal

The site already had a technically correct Telegram service page, but broad commercial queries such as «разработка Telegram-бота» still did not surface the portfolio prominently. Stage 20 strengthens one canonical commercial landing instead of creating multiple near-duplicate doorway pages.

Primary target URL: https://alexgtup.github.io/telegram-bots/

## What changed

### 1. Telegram landing became the explicit cluster hub

The published `/telegram-bots/` page now includes a visible proof section linking to:

- the real Fin Planner Telegram case;
- the public Freelance.ru executor profile;
- the Telegram bot cost guide;
- the Telegram bot brief guide.

No review counts, fixed prices, delivery times or other unverified commercial claims were invented.

### 2. Supporting pages now point back to the commercial landing

Contextual visible links to `/telegram-bots/` were added to the deployed versions of:

- `/cases/fin-planner/`;
- `/guides/telegram-bot-cost/`;
- `/guides/telegram-bot-brief/`;
- `/guides/bot-vs-mini-app-vs-web/`;
- `/services/`.

This makes the architecture explicit: guides answer informational intent, the case proves implementation, and `/telegram-bots/` remains the main commercial target.

### 3. External/entity signals were strengthened

- Repository README now names Telegram bot development as the main commercial direction and links directly to the service page and supporting content.
- `GITHUB_PROFILE_README.md` was refocused on Telegram development and the real Fin Planner case.
- `llms.txt` now explicitly identifies `/telegram-bots/` as the primary URL for Telegram bot development / creation / order intent.
- Existing homepage Person schema already connects Alexander / Alexuys with GitHub, Freelance.ru and Telegram through `sameAs`; this was verified rather than duplicated.

### 4. Build process keeps these changes safe

A new `scripts/stage20_patch.py` applies the cluster blocks to the generated `_site` before validation. The normal parser-based site validator runs after the patch, so malformed links or HTML still block deployment.

The deploy workflow also submits the six affected public URLs to IndexNow when the Stage 20 patch changes.

## Production verification

GitHub Pages workflow run `34021465693` completed successfully.

Build output:

- `stage20 patched: /telegram-bots/, /cases/fin-planner/, /guides/telegram-bot-cost/, /guides/telegram-bot-brief/, /guides/bot-vs-mini-app-vs-web/, /services/`
- `validation OK: 56 sitemap URLs, 62 HTML files, 58 indexable/noindex pages checked`
- Pages deployment: success
- IndexNow URLs submitted: 6
- IndexNow HTTP response: 200

## Ranking strategy after Stage 20

Do not create more pages that merely rephrase «разработка Telegram-бота», «создание Telegram-бота» and «Telegram-бот на заказ». Those intents should consolidate on `/telegram-bots/`.

Next gains should come from:

1. search-console query data after the new cluster is crawled;
2. real external mentions that link to the Telegram landing or its case;
3. additional real Telegram cases when available;
4. stronger conversion/proof content only when the claim can be verified;
5. title/snippet changes based on impressions and CTR rather than repeated same-day rewrites.
