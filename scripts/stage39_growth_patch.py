#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def read(route):
    p = root / ("index.html" if route == "/" else route.strip("/") + "/index.html")
    if not p.is_file():
        raise SystemExit(f"stage39: missing {route}: {p}")
    return p, p.read_text(encoding="utf-8")


def write(p, text):
    p.write_text(text, encoding="utf-8")


def replace_once(text, old, new, label):
    if old in text:
        return text.replace(old, new, 1)
    if new in text:
        return text
    raise SystemExit(f"stage39: marker not found: {label}")


# 1) Homepage: narrow the commercial promise to the three directions most likely
# to convert for a solo developer, while keeping the broader service catalogue below.
p, html = read("/")
html = replace_once(
    html,
    '<h1 id="hero-title">Telegram-боты, автоматизация <span class="soft">и веб-сервисы под задачу.</span></h1>',
    '<h1 id="hero-title">Telegram-боты, автоматизация <span class="soft">и доработка проектов.</span></h1>',
    "homepage H1",
)
html = replace_once(
    html,
    '<p class="hero-copy">Собираю Telegram-боты, автоматизацию, CRM, интеграции и веб-продукты под конкретный процесс — от первой логики до запуска и дальнейшей доработки.</p>',
    '<p class="hero-copy">Разрабатываю и дорабатываю Telegram-ботов, автоматизацию и интеграции. Если проект уже существует, можно начать с конкретной ошибки, сломанного сценария или функции — без обязательного большого ТЗ.</p>',
    "homepage hero copy",
)
html = replace_once(
    html,
    '<div aria-label="Направления работы" class="hero-tags" data-nosnippet=""><span>TELEGRAM</span><span>AI AUTOMATION</span><span>WEB</span><span>INTEGRATIONS</span></div>',
    '<div aria-label="Направления работы" class="hero-tags" data-nosnippet=""><span>TELEGRAM</span><span>AUTOMATION</span><span>PROJECT REPAIR</span><span>INTEGRATIONS</span></div>',
    "homepage hero tags",
)

work_marker = '<section aria-labelledby="work-title" class="section container" id="work">'
quick_start = '''<section aria-labelledby="quick-start-title" class="section container" id="quick-start">
<div class="section-head">
<div class="section-index" data-nosnippet="">01 / Быстрый старт</div>
<div><h2 class="section-title" id="quick-start-title">Понятный первый шаг. <span class="soft">Без оценки вслепую.</span></h2><p class="section-lead">Ориентиры нужны, чтобы сразу понимать порядок бюджета. Точная стоимость зависит от текущего состояния и интеграций. <a class="inline-more" href="https://freelance.ru/gglalex" rel="noopener noreferrer" target="_blank">20+ отзывов и 20+ выполненных заданий на Freelance.ru ↗</a></p></div>
</div>
<div class="route-grid">
<a class="route-card" href="/project-repair/"><span class="route-no">ОТ 5 000 ₽</span><strong>Доработка существующего проекта</strong><p>Ошибка на сайте, сломанный бот, чужой код, интеграция или незавершённый релиз. Сначала локализую проблему.</p><span class="route-link">Доработка проекта ↗</span></a>
<a class="route-card" href="/telegram-bots/"><span class="route-no">ОТ 15 000 ₽</span><strong>Telegram-бот</strong><p>Первый рабочий сценарий: заявки, анкета, уведомления, данные или простая интеграция.</p><span class="route-link">Разработка Telegram-бота ↗</span></a>
<a class="route-card" href="/n8n-automation/"><span class="route-no">ОТ 15 000 ₽</span><strong>Автоматизация n8n / Make</strong><p>Webhook, API, CRM, Telegram или таблицы в одном воспроизводимом процессе с обработкой ошибок.</p><span class="route-link">Автоматизация ↗</span></a>
</div>
</section>
'''
if 'id="quick-start"' not in html:
    if work_marker not in html:
        raise SystemExit("stage39: homepage work marker not found")
    html = html.replace(work_marker, quick_start + work_marker, 1)
write(p, html)

# 2) Project repair becomes the primary landing for small/medium existing-project work.
p, html = read("/project-repair/")
html = replace_once(
    html,
    '<title>Доработка сайта и чужого проекта — исправление ошибок | Alexuys</title>',
    '<title>Доработка сайтов и Telegram-ботов — исправление ошибок | Alexuys</title>',
    "repair title",
)
html = replace_once(
    html,
    'Доработка сайта, Telegram-бота или веб-сервиса: аудит кода, исправление ошибок, интеграций и логики, завершение проекта и подготовка к релизу.',
    'Доработка сайтов, Telegram-ботов и существующих проектов: исправление ошибок, API и интеграций, чужой код, адаптив, завершение и подготовка к релизу.',
    "repair description first occurrence",
)
# Keep social title synchronized if the old wording survived in twitter/og.
html = html.replace('Доработка сайта и чужого проекта — исправление ошибок | Alexuys', 'Доработка сайтов и Telegram-ботов — исправление ошибок | Alexuys')
html = replace_once(
    html,
    '<h1>Доработка сайта <em>и существующего проекта</em></h1>',
    '<h1>Доработка сайта, Telegram-бота <em>и существующего проекта</em></h1>',
    "repair H1",
)
html = replace_once(
    html,
    '<p class="lead">Подключаюсь к проекту, который уже существует: ищу реальную причину ошибки, отделяю критичное от косметики и довожу согласованный участок до проверяемого результата. Подходит для сайтов, ботов и веб-сервисов.</p>',
    '<p class="lead">Если сайт, Telegram-бот или веб-сервис уже существует, не обязательно начинать заново. Сначала воспроизвожу проблему, нахожу её источник и оцениваю минимальный объём, который вернёт рабочий сценарий.</p>',
    "repair lead",
)

repair_marker = '<section class="section container"><div class="section-head"><div class="kicker" data-nosnippet="">Что делаю</div>'
repair_pricing = '''<section class="section container"><div class="section-head"><div class="kicker" data-nosnippet="">Стоимость · ориентир</div><h2>Можно начать <em>с небольшой задачи</em></h2></div><div class="cards"><article class="card"><span class="num" data-nosnippet="">ОТ 5 000 ₽</span><h3>Небольшое исправление</h3><p>Локальный баг, адаптив, форма, настройка или понятная правка в существующем проекте после просмотра реализации.</p></article><article class="card"><span class="num" data-nosnippet="">ОТ 10 000 ₽</span><h3>Логика или интеграция</h3><p>API, webhook, авторизация, Telegram, CRM или сценарий, где нужно найти причину сбоя и проверить соседние состояния.</p></article><article class="card"><span class="num" data-nosnippet="">ПОСЛЕ АУДИТА</span><h3>Продолжить чужой проект</h3><p>Сначала отделяю уже рабочую часть от незавершённой и называю объём до следующего проверяемого результата.</p></article></div><p class="micro">Это ориентиры, а не фиксированный прайс: точную оценку даю после ссылки, скрина, исходников или короткого описания проблемы.</p></section>'''
if 'Стоимость · ориентир' not in html:
    if repair_marker not in html:
        raise SystemExit("stage39: repair insertion marker not found")
    html = html.replace(repair_marker, repair_pricing + repair_marker, 1)
write(p, html)

# 3) Strengthen the weak internal-link graph with contextual links, not footer spam.
p, html = read("/development/")
old = '<a href="/web-development/"><strong>Веб-разработка</strong><span>Сервисы и кабинеты</span></a></div>'
new = '<a href="/web-development/"><strong>Веб-разработка</strong><span>Сервисы и кабинеты</span></a><a href="/app-development/"><strong>Приложения</strong><span>Web, Mini App и iOS по пользовательскому сценарию</span></a></div>'
html = replace_once(html, old, new, "development -> app-development")
write(p, html)

p, html = read("/mvp-development/")
old = '<a href="/cases/"><strong>Кейсы</strong><span>Реальные проекты</span></a></div>'
new = '<a href="/cases/"><strong>Кейсы</strong><span>Реальные проекты</span></a><a href="/app-development/"><strong>Разработка приложений</strong><span>Когда MVP развивается в отдельный продукт</span></a></div>'
html = replace_once(html, old, new, "mvp -> app-development")
write(p, html)

p, html = read("/cases/auto-crm/")
old = '<a href="/n8n-automation/"><strong>n8n / Make</strong><span>Автоматизировать повторяющиеся действия между системами.</span></a></div>'
new = '<a href="/n8n-automation/"><strong>n8n / Make</strong><span>Автоматизировать повторяющиеся действия между системами.</span></a><a href="/guides/custom-crm-or-ready/"><strong>Своя CRM или готовая</strong><span>Разбор, когда кастомная система действительно оправдана.</span></a></div>'
html = replace_once(html, old, new, "auto-crm -> CRM guide")
write(p, html)

p, html = read("/en/services/")
old = '</div></section><section class="intl-container intl-section"><div class="intl-cta-box">'
new = '<a href="/en/guides/development-cost/"><strong>Software development cost guide</strong><span>What actually changes an estimate before the build starts.</span></a></div></section><section class="intl-container intl-section"><div class="intl-cta-box">'
html = replace_once(html, old, new, "en services -> cost guide")
write(p, html)

p, html = read("/en/telegram-bot-development/")
old = '<a href="/en/cases/fin-planner/"><strong>Fin Planner case</strong><span>A real Telegram product in the portfolio</span></a></div>'
new = '<a href="/en/cases/fin-planner/"><strong>Fin Planner case</strong><span>A real Telegram product in the portfolio</span></a><a href="/en/guides/telegram-bot-cost/"><strong>Telegram bot cost guide</strong><span>Estimate scenarios, integrations and production scope.</span></a></div>'
html = replace_once(html, old, new, "en telegram service -> cost guide")
write(p, html)

p, html = read("/en/n8n-automation/")
old = '<a href="/en/backend-development/"><strong>Backend development</strong><span>When the workflow needs a custom service</span></a></div>'
new = '<a href="/en/backend-development/"><strong>Backend development</strong><span>When the workflow needs a custom service</span></a><a href="/en/guides/n8n-vs-make/"><strong>n8n vs Make</strong><span>Choose the automation platform by workflow and maintenance needs.</span></a></div>'
html = replace_once(html, old, new, "en n8n service -> comparison guide")
write(p, html)

print("stage39 growth: homepage focus + pricing, project-repair commercialized, weak internal links strengthened")
