#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from html import escape, unescape
import re
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
DATE = "2026-09-09"
BASE = "https://alexgtup.github.io"

# Stage76 pages are deliberately NOT touched here: they are the Yandex control group.
META = {
    "/cases/": (
        "Готовые кейсы разработки — Telegram, CRM, iOS и веб | Alexuys",
        "Готовые кейсы разработки: Telegram-боты, CRM, iOS, B2B-каталоги и веб-сервисы. Что было нужно, что реализовано и что можно проверить.",
    ),
    "/guides/telegram-bot-cost/": (
        "Сколько стоит сделать Telegram-бот на заказ в 2026 | Alexuys",
        "Сколько стоит сделать Telegram-бота на заказ в 2026 году: сценарии, база данных, CRM/API, оплаты, Mini App, ошибки и ориентир первого рабочего этапа.",
    ),
    "/cases/fin-planner/": (
        "Telegram-бот для учета доходов и расходов — кейс Fin Planner",
        "Кейс Telegram-бота для учета доходов и расходов: бюджет, регулярные операции, баланс, цели, отчеты и финансовый анализ внутри Telegram.",
    ),
    "/mvp-development/": (
        "MVP на заказ — веб-сервис, приложение или Telegram-бот | Alexuys",
        "Разработка MVP на заказ: веб-сервис, приложение или Telegram-бот с одним рабочим пользовательским сценарием, реальными данными и запуском по этапам.",
    ),
    "/cases/auto-crm/": (
        "CRM для автосалона — заявки и автоматизация | Alexuys",
        "Кейс CRM для автосалона: заявки, статусы, менеджеры, рабочие данные и автоматизация процесса в одной системе. Что было реализовано и как устроен сценарий.",
    ),
    "/freelance-developer/": (
        "Фриланс-разработчик — сайты, боты и автоматизация | Alexuys",
        "Фриланс-разработчик для сайтов, Telegram-ботов, CRM, n8n/Make и API-интеграций. Форматы работ, ориентиры бюджета, кейсы и прямой контакт.",
    ),
    "/project-repair/": (
        "Доработка сайта и проекта — ошибки, функции, API | Alexuys",
        "Доработка существующего сайта, бота или приложения: исправление ошибок, новые функции, API-интеграции и работа с чужим кодом без ненужного переписывания.",
    ),
    "/python-development/": (
        "Python-разработчик — FastAPI, боты и автоматизация | Alexuys",
        "Python-разработка на заказ: FastAPI, Telegram-боты, API, обработка данных и автоматизация. Реальные проекты, интеграции и прямой контакт с разработчиком.",
    ),
    "/tools/": (
        "DevTools Hub — JSON, UTM, Cron, JWT, robots и sitemap",
        "Бесплатные браузерные инструменты: JSON Formatter, UTM Builder, Cron Builder, JWT Decoder, robots.txt Validator и Sitemap XML Validator. Без регистрации.",
    ),
    "/web-development/": (
        "Сайты и веб-сервисы на заказ — frontend, backend, API | Alexuys",
        "Разработка сайтов и веб-сервисов на заказ: интерфейсы, backend, API, формы, кабинеты, данные и интеграции. Реальные кейсы и запуск по этапам.",
    ),
    "/en/backend-development/": (
        "Backend development services — APIs and data | Alexuys",
        "Backend development services for APIs, product logic, databases and integrations. Practical architecture, error handling and a verifiable delivery path.",
    ),
    "/en/custom-crm-development/": (
        "Custom CRM development services for business | Alexuys",
        "Custom CRM development around the actual workflow: leads, stages, roles, data and integrations. Built as a working process rather than a generic template.",
    ),
    "/en/ios-development/": (
        "iOS app development in Swift — freelance developer | Alexuys",
        "Native iOS app development in Swift for focused products and existing applications: interface, product logic, integrations and release-oriented delivery.",
    ),
    "/en/mvp-development/": (
        "MVP development services — working first release | Alexuys",
        "MVP development for web apps, mobile products and Telegram projects. One real user flow, real data and a first release that can be tested before scaling.",
    ),
    "/en/python-development/": (
        "Python development services — FastAPI and automation | Alexuys",
        "Python development services for FastAPI backends, APIs, Telegram bots, data processing and automation. Real projects and direct developer communication.",
    ),
    "/en/services/": (
        "Software development services — web, bots, automation | Alexuys",
        "Software development services for Telegram bots, web apps, CRM, Python/backend, n8n automation and API integrations. Choose the path by the actual workflow.",
    ),
    "/en/cases/": (
        "Software development case studies — web, bots and CRM | Alexuys",
        "Software development case studies covering Telegram products, custom CRM, iOS, mobile app repair and B2B web systems, with implementation details you can inspect.",
    ),
}

H1 = {
    "/cases/": "Готовые кейсы разработки: Telegram, CRM, приложения и веб.",
    "/guides/telegram-bot-cost/": "Сколько стоит сделать Telegram-бот на заказ",
    "/cases/fin-planner/": "Telegram-бот для учета доходов и расходов — Fin Planner.",
    "/mvp-development/": "MVP на заказ: веб-сервис, приложение или Telegram-бот.",
}

STYLE = '''<style data-stage77-css="true">
.s77-section{width:min(100%,92rem);margin:clamp(2.4rem,6vw,5rem) auto 0;padding:clamp(1.2rem,3vw,2rem) clamp(1rem,4vw,2.2rem);border:1px solid rgba(255,255,255,.08);border-radius:18px;background:rgba(255,255,255,.018)}
.s77-section h2{margin:0 0 .7rem;font-size:clamp(1.25rem,2.3vw,1.85rem)}.s77-section h3{margin:1.15rem 0 .35rem;font-size:1rem}.s77-section p{margin:.45rem 0;color:#aeb6bd;line-height:1.65}.s77-section ul,.s77-section ol{margin:.55rem 0 0;padding-left:1.25rem;color:#aeb6bd}.s77-section li{margin:.32rem 0;line-height:1.55}.s77-links{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:1rem}.s77-links a{display:inline-flex;padding:.55rem .75rem;border:1px solid rgba(255,255,255,.1);border-radius:10px;text-decoration:none}.s77-links a:hover{text-decoration:underline}
@media(max-width:640px){.s77-section{border-radius:14px}.s77-links{display:grid}.s77-links a{width:100%}}
</style>'''

TOOL_DETAILS = {
    "/tools/json-formatter/": (
        "Как использовать JSON Formatter",
        "Инструмент форматирует JSON, проверяет синтаксис и помогает быстро увидеть структуру объекта без отправки данных на внешний API.",
        ["Вставьте JSON в исходное поле.", "Запустите форматирование и проверьте сообщение об ошибке, если JSON невалиден.", "Скопируйте отформатированный результат для кода, документации или API-запроса."],
        "Подходит для ответов REST API, конфигураций, webhook payload и отладки интеграций. Особенно полезен, когда ошибка скрывается в лишней запятой, кавычке или неправильной вложенности.",
        [("/api-integrations/", "API-интеграции"), ("/tools/jwt-decoder/", "JWT Decoder")],
    ),
    "/tools/utm-builder/": (
        "Как собрать UTM-ссылку",
        "UTM Builder собирает ссылку с utm_source, utm_medium, utm_campaign и дополнительными параметрами, чтобы источники переходов не смешивались в аналитике.",
        ["Укажите целевой URL.", "Добавьте источник, канал и кампанию.", "Скопируйте готовую ссылку и используйте ее в профиле, публикации или рекламном размещении."],
        "Для повторяемой аналитики лучше заранее договориться о едином написании source/medium/campaign. Тогда одинаковые источники не распадутся на несколько строк из-за регистра или разных названий.",
        [("/freelance-developer/", "Посадочная для входящего трафика"), ("/tools/json-formatter/", "JSON Formatter")],
    ),
    "/tools/cron-builder/": (
        "Как собрать cron-выражение",
        "Cron Builder помогает составить стандартное выражение из пяти полей: минуты, часы, день месяца, месяц и день недели — с видимой структурой каждого значения.",
        ["Задайте нужное расписание по полям.", "Проверьте итоговое выражение перед копированием.", "Тестируйте расписание в своей среде, потому что timezone и cron-реализация могут отличаться."],
        "Подходит для фоновых задач, синхронизаций, n8n/self-hosted процессов и серверных jobs. Для критичных процессов дополнительно проверяйте timezone и поведение при пропущенном запуске.",
        [("/n8n-automation/", "Автоматизация n8n"), ("/backend-development/", "Backend-разработка")],
    ),
    "/tools/jwt-decoder/": (
        "Как читать JWT локально",
        "JWT Decoder показывает header и payload токена прямо в браузере. Инструмент не подтверждает подлинность подписи: он предназначен для чтения структуры и отладки.",
        ["Вставьте JWT.", "Проверьте header, payload, issuer, audience и timestamps.", "Для проверки подписи используйте серверную валидацию с правильным ключом и алгоритмом."],
        "Не вставляйте рабочие секреты в неизвестные онлайн-сервисы. Этот декодер обрабатывает ввод локально, но сам факт декодирования JWT не означает, что токен действителен или безопасен.",
        [("/backend-development/", "Backend-разработка"), ("/api-integrations/", "API-интеграции")],
    ),
    "/tools/robots-validator/": (
        "Как проверить robots.txt",
        "Validator разбирает базовые директивы robots.txt и помогает увидеть структурные ошибки до того, как они превратятся в проблему обхода сайта.",
        ["Вставьте содержимое robots.txt.", "Проверьте User-agent, Allow/Disallow и Sitemap.", "Сопоставьте правила с теми URL, которые действительно должны быть доступны поисковым роботам."],
        "robots.txt управляет обходом, но не является универсальным способом удалить страницу из поиска. Для закрытия от индексации используйте корректный noindex там, где робот может получить страницу.",
        [("/tools/sitemap-validator/", "Sitemap XML Validator"), ("/cases/siteaudit-studio/", "SiteAudit Studio")],
    ),
    "/tools/sitemap-validator/": (
        "Как проверить sitemap.xml",
        "Sitemap XML Validator проверяет XML-структуру карты сайта и базовую корректность URL, чтобы быстрее отсеять синтаксические ошибки перед отправкой в панели вебмастеров.",
        ["Вставьте sitemap.xml.", "Проверьте XML и список loc URL.", "Убедитесь, что в карте находятся только канонические индексируемые страницы с корректными абсолютными адресами."],
        "Sitemap помогает обнаружению URL, но сам по себе не гарантирует обход или попадание в индекс. Его задача — дать поисковику чистый список канонических страниц, а не заменить внутреннюю перелинковку.",
        [("/tools/robots-validator/", "robots.txt Validator"), ("/cases/siteaudit-studio/", "SiteAudit Studio")],
    ),
}

EXTRA_BLOCKS = {
    "/tools/": '''<section class="s77-section" data-stage77-extra="tools"><h2>Инструменты для реальной проверки, а не для витрины</h2><p>Каждая утилита решает одну маленькую задачу прямо в браузере: привести JSON в порядок, собрать UTM, проверить cron, прочитать JWT, разобрать robots.txt или sitemap.xml. Инструменты не требуют регистрации и полезны как во время разработки, так и при техническом SEO-аудите.</p><p>Для проверки целого сайта используйте SiteAudit Studio, а для задач с API, backend или автоматизацией переходите в соответствующий раздел разработки.</p><div class="s77-links"><a href="/cases/siteaudit-studio/">SiteAudit Studio</a><a href="/api-integrations/">API-интеграции</a><a href="/backend-development/">Backend</a></div></section>''',
    "/demos/": '''<section class="s77-section" data-stage77-extra="demos"><h2>Что проверять в демо</h2><p>Демо нужны не для статичной картинки. Откройте продукт, выполните основной пользовательский сценарий и посмотрите, как интерфейс связан с реальной логикой. Для SheetPilot это загрузка XLSX, команда, предпросмотр и экспорт; для SEO Control Center — сбор и представление поисковых данных.</p><p>Рядом с каждым демо есть отдельный кейс с техническим разбором. Так можно оценить не только внешний вид, но и сам способ реализации.</p><div class="s77-links"><a href="/cases/sheetpilot-ai/">Кейс SheetPilot AI</a><a href="/cases/seo-control-center/">Кейс SEO Control Center</a><a href="/web-development/">Разработка веб-сервисов</a></div></section>''',
    "/freelance-os/": '''<section class="s77-section" data-stage77-extra="freelance-os"><h2>Как работает FreelanceOS</h2><p>FreelanceOS — local-first CRM для самостоятельной работы с заказами. Лиды, источник обращения, статус сделки, follow-up, задачи, бюджет и выручка сохраняются в браузере пользователя, поэтому для базового сценария не требуется отдельный аккаунт или серверная база.</p><h3>Что можно вести</h3><ul><li>лиды и источник каждого обращения;</li><li>этап сделки и следующий follow-up;</li><li>задачи, бюджет, часы и фактическую выручку;</li><li>конверсию источников и резервную копию через JSON export/import.</li></ul><p>Отдельный кейс показывает, как local-first подход используется в интерфейсе и почему для MVP он позволяет получить работающий продукт без лишней инфраструктуры.</p><div class="s77-links"><a href="/cases/freelance-os/">Кейс FreelanceOS</a><a href="/crm-development/">Разработка CRM</a><a href="/mvp-development/">Разработка MVP</a></div></section>''',
}


def html_path(route: str) -> Path:
    return root / "index.html" if route == "/" else root / route.strip("/") / "index.html"


def set_meta(text: str, title: str, description: str, route: str) -> str:
    et = escape(title, quote=False)
    ed = escape(description, quote=True)
    text, n = re.subn(r"<title>.*?</title>", f"<title>{et}</title>", text, count=1, flags=re.I | re.S)
    if n != 1:
        raise SystemExit(f"stage77: title missing: {route}")

    def repl(attr: str, key: str, value: str, src: str) -> str:
        patterns = [
            rf'(<meta\b[^>]*\b{attr}=["\']{re.escape(key)}["\'][^>]*\bcontent=["\'])[^"\']*(["\'][^>]*>)',
            rf'(<meta\b[^>]*\bcontent=["\'])[^"\']*(["\'][^>]*\b{attr}=["\']{re.escape(key)}["\'][^>]*>)',
        ]
        for pattern in patterns:
            out, count = re.subn(pattern, lambda m: m.group(1) + value + m.group(2), src, count=1, flags=re.I)
            if count:
                return out
        return src

    text = repl("name", "description", ed, text)
    text = repl("property", "og:title", escape(title, quote=True), text)
    text = repl("property", "og:description", ed, text)
    text = repl("name", "twitter:title", escape(title, quote=True), text)
    text = repl("name", "twitter:description", ed, text)
    return text


def set_h1(text: str, value: str, route: str) -> str:
    out, n = re.subn(r'(<h1\b[^>]*>).*?(</h1>)', lambda m: m.group(1) + escape(value, quote=False) + m.group(2), text, count=1, flags=re.I | re.S)
    if n != 1:
        raise SystemExit(f"stage77: H1 missing: {route}")
    return out


def ensure_style(text: str) -> str:
    if 'data-stage77-css="true"' in text:
        return text
    out, n = re.subn(r'</head>', STYLE + '</head>', text, count=1, flags=re.I)
    if n != 1:
        raise SystemExit("stage77: </head> missing")
    return out


def add_block(route: str, block: str) -> None:
    p = html_path(route)
    text = p.read_text(encoding="utf-8")
    if 'data-stage77-extra=' in text:
        return
    text = ensure_style(text)
    text, n = re.subn(r'</main>', block + '</main>', text, count=1, flags=re.I)
    if n != 1:
        raise SystemExit(f"stage77: </main> missing: {route}")
    p.write_text(text, encoding="utf-8")


changed: set[str] = set()
for route, (title, desc) in META.items():
    p = html_path(route)
    if not p.is_file():
        raise SystemExit(f"stage77: missing metadata target {route}")
    text = p.read_text(encoding="utf-8")
    text = set_meta(text, title, desc, route)
    if route in H1:
        text = set_h1(text, H1[route], route)
    p.write_text(text, encoding="utf-8")
    changed.add(route)

for route, (heading, summary, steps, note, links) in TOOL_DETAILS.items():
    lis = ''.join(f'<li>{escape(step)}</li>' for step in steps)
    rel = ''.join(f'<a href="{escape(href, quote=True)}">{escape(label)}</a>' for href, label in links)
    block = f'<section class="s77-section" data-stage77-extra="tool"><h2>{escape(heading)}</h2><p>{escape(summary)}</p><ol>{lis}</ol><h3>Что учитывать</h3><p>{escape(note)}</p><div class="s77-links">{rel}</div></section>'
    add_block(route, block)
    changed.add(route)

for route, block in EXTRA_BLOCKS.items():
    add_block(route, block)
    changed.add(route)

# The full search surface is the sitemap, not every technical HTML file.
sitemap = root / "sitemap.xml"
if not sitemap.is_file():
    raise SystemExit("stage77: sitemap.xml missing")
tree = ET.parse(sitemap)
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs = [(n.text or '').strip() for n in tree.findall('.//s:loc', ns) if (n.text or '').strip()]
if len(locs) != 74 or len(set(locs)) != 74:
    raise SystemExit(f"stage77: expected 74 unique sitemap URLs, got {len(locs)}/{len(set(locs))}")

s = sitemap.read_text(encoding="utf-8")
for route in sorted(changed):
    url = BASE + ('/' if route == '/' else route)
    pattern = re.compile(rf'(<loc>{re.escape(url)}</loc>\s*<lastmod>)[^<]+(</lastmod>)')
    s, n = pattern.subn(rf'\g<1>{DATE}\g<2>', s, count=1)
    if n != 1:
        raise SystemExit(f"stage77: sitemap lastmod missing: {url}")
sitemap.write_text(s, encoding="utf-8")

# ---- Site-wide final audit: every sitemap page must satisfy the same core invariants. ----
def route_from_url(url: str) -> str:
    if url == BASE + '/':
        return '/'
    return '/' + url.split(BASE + '/', 1)[1].strip('/') + '/'


def plain(fragment: str) -> str:
    fragment = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', ' ', fragment, flags=re.I | re.S)
    fragment = re.sub(r'<[^>]+>', ' ', fragment)
    return re.sub(r'\s+', ' ', unescape(fragment)).strip()


def category(route: str) -> str:
    if route == '/': return 'home'
    if route.startswith('/tools/') and route != '/tools/': return 'tool'
    if route.startswith('/cases/') and route != '/cases/': return 'case'
    if route.startswith('/guides/') and route != '/guides/': return 'guide'
    if route.startswith('/en/cases/') and route != '/en/cases/': return 'en_case'
    if route.startswith('/en/guides/') and route != '/en/guides/': return 'en_guide'
    if route.startswith('/en/') and route not in ('/en/', '/en/about/', '/en/services/', '/en/cases/', '/en/guides/'): return 'en_service'
    if route in ('/services/', '/cases/', '/guides/', '/about/', '/demos/', '/tools/', '/freelance-developer/', '/en/', '/en/about/', '/en/services/', '/en/cases/', '/en/guides/'): return 'hub'
    return 'service'

MIN_WORDS = {'home': 350, 'service': 280, 'case': 250, 'guide': 300, 'tool': 220, 'hub': 160, 'en_case': 180, 'en_guide': 250, 'en_service': 220}
seen_title: dict[str, str] = {}
seen_desc: dict[str, str] = {}
seen_h1: dict[str, str] = {}
report = []

for url in locs:
    route = route_from_url(url)
    p = html_path(route)
    if not p.is_file():
        raise SystemExit(f"stage77: sitemap target missing: {route}")
    text = p.read_text(encoding="utf-8")

    tm = re.search(r'<title>(.*?)</title>', text, flags=re.I | re.S)
    dm = re.search(r'<meta\b[^>]*\bname=["\']description["\'][^>]*\bcontent=["\']([^"\']*)["\']', text, flags=re.I)
    if not dm:
        dm = re.search(r'<meta\b[^>]*\bcontent=["\']([^"\']*)["\'][^>]*\bname=["\']description["\']', text, flags=re.I)
    h1s = re.findall(r'<h1\b[^>]*>(.*?)</h1>', text, flags=re.I | re.S)
    cm = re.search(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*\bhref=["\']([^"\']+)["\']', text, flags=re.I)
    if not cm:
        cm = re.search(r'<link\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*\brel=["\']canonical["\']', text, flags=re.I)
    rm = re.search(r'<meta\b[^>]*\bname=["\']robots["\'][^>]*\bcontent=["\']([^"\']*)["\']', text, flags=re.I)
    if not (tm and dm and len(h1s) == 1 and cm and rm):
        raise SystemExit(f"stage77: core metadata invariant failed: {route}")

    title = plain(tm.group(1))
    desc = unescape(dm.group(1)).strip()
    h1 = plain(h1s[0])
    canonical = cm.group(1).strip()
    robots = rm.group(1).lower()
    mainm = re.search(r'<main\b[^>]*>(.*?)</main>', text, flags=re.I | re.S)
    bodytext = plain(mainm.group(1) if mainm else text)
    words = len(re.findall(r'[A-Za-zА-Яа-яЁё0-9]+', bodytext))
    internal = len(set(re.findall(r'href=["\'](/[^"\'#?]*)', text, flags=re.I)))

    if canonical != url:
        raise SystemExit(f"stage77: canonical mismatch {route}: {canonical} != {url}")
    if 'noindex' in robots:
        raise SystemExit(f"stage77: sitemap page is noindex: {route}")
    if not (25 <= len(title) <= 80):
        raise SystemExit(f"stage77: title length {len(title)}: {route}: {title}")
    if not (100 <= len(desc) <= 190):
        raise SystemExit(f"stage77: description length {len(desc)}: {route}")
    if internal < 4:
        raise SystemExit(f"stage77: too few internal links ({internal}): {route}")
    minimum = MIN_WORDS[category(route)]
    if words < minimum:
        raise SystemExit(f"stage77: thin page {route}: {words} < {minimum} words")

    for store, value, label in ((seen_title, title, 'title'), (seen_desc, desc, 'description'), (seen_h1, h1, 'h1')):
        key = value.casefold()
        if key in store:
            raise SystemExit(f"stage77: duplicate {label}: {route} == {store[key]}: {value}")
        store[key] = route

    report.append((route, category(route), words, internal, len(title), len(desc)))

print(f"stage77: audited {len(report)} sitemap pages; changed {len(changed)} pages")
for route, kind, words, links, tl, dl in sorted(report):
    print(f"stage77 OK {route} type={kind} words={words} links={links} title={tl} desc={dl}")
