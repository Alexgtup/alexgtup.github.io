# Stage 16 — Semantic Depth + AI Citation

## Что изменено
- 13 коммерческих страниц получили короткие самостоятельные answer-блоки: определение услуги, когда она подходит, что влияет на оценку и ссылки на смежные материалы.
- Добавлены два полноценных гайда: `/guides/development-cost/` и `/guides/bot-vs-mini-app-vs-web/`.
- `robots.txt` явно разрешает OAI-SearchBot, PerplexityBot, Claude-SearchBot, Claude-User, YandexAdditionalBot и Bingbot.
- Title suffix унифицирован до `| Alexuys`; автор сохранён как Александр / Alexuys.
- Добавлены `meta author` и `rel=author`.
- Кейсы CRM / завод / такси получили CreativeWork + BreadcrumbList schema.
- Guides hub получил ItemList schema.
- Обновлены sitemap, feed.xml и llms.txt.
- Исправлен остаточный overflow `/app-development/` в отдельном `search-intent.css`; узкий privacy title также защищён.

## QA
- 31 URL в sitemap.
- 31/31 URL имеют существующий `index.html`.
- Browser layout QA: 31 маршрутов × 6 ширин (320, 390, 768, 1024, 1440, 1920) = 186 проверок.
- Итог: 0 horizontal overflow, 0 H1 errors.
- JSON-LD, canonical, title uniqueness, internal links, image dimensions, feed.xml, sitemap.xml, manifest и JS проверены отдельно.

## Зачем
Цель этапа — не создавать сотни doorway-страниц, а усилить тематическую полноту и дать поисковикам/AI-системам короткие, однозначные фрагменты, которые можно извлечь как ответ на запрос.
