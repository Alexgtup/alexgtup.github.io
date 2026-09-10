#!/usr/bin/env python3
from __future__ import annotations

import html as html_lib
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
BASE = "https://alexgtup.github.io"
TODAY = "2026-09-10"

# Final-stage search entry paths. This intentionally runs after cleanup/UX stages so
# discovery links survive in the exact HTML uploaded to GitHub Pages.
RELATED = {
    "/telegram-bots/": (
        "Перед заявкой можно проверить похожие сценарии",
        [
            ("Реальный Telegram-кейс", "Фин Планер: продуктовая логика, регулярные операции, цели и отчёты внутри Telegram.", "/cases/fin-planner/", "Кейс"),
            ("Сколько стоит Telegram-бот", "Разбор факторов цены и границы первой рабочей версии до начала разработки.", "/guides/telegram-bot-cost/", "Разбор"),
            ("Когда нужен Mini App", "Если кнопок и сообщений уже мало и нужен полноценный интерфейс внутри Telegram.", "/telegram-mini-apps/", "Услуга"),
        ],
    ),
    "/web-development/": (
        "Посмотрите близкие варианты до выбора формата",
        [
            ("B2B-веб кейс", "Каталог производственной компании: структура данных, карточки продукции и заявки.", "/cases/factory-catalog/", "Кейс"),
            ("Сайт или веб-приложение", "Как выбрать формат, когда лендинга уже мало, а полноценный продукт ещё не обязателен.", "/guides/site-vs-web-app/", "Разбор"),
            ("Первый рабочий MVP", "Если задачу лучше выпускать поэтапно и начать с одного законченного пользовательского пути.", "/mvp-development/", "Услуга"),
        ],
    ),
    "/n8n-automation/": (
        "Полезно проверить перед сборкой workflow",
        [
            ("SEO Control Center", "Кейс сервиса, где автоматизация собирает поисковые данные и превращает их в рабочие сигналы.", "/cases/seo-control-center/", "Кейс"),
            ("n8n или backend", "Граница, после которой workflow сложнее поддерживать, чем отдельный сервис.", "/guides/n8n-vs-backend/", "Разбор"),
            ("n8n или Make", "Сравнение двух подходов к low-code автоматизации и дальнейшей поддержке.", "/guides/n8n-vs-make/", "Разбор"),
        ],
    ),
    "/crm-development/": (
        "Перед разработкой CRM стоит сравнить три пути",
        [
            ("CRM для автосалона", "Кейс рабочего контура: заявки, статусы, сотрудники и связанная автоматизация.", "/cases/auto-crm/", "Кейс"),
            ("Своя CRM или готовая", "Когда коробочное решение выгоднее и где появляется смысл в собственной системе.", "/guides/custom-crm-or-ready/", "Разбор"),
            ("Интеграции API", "Если основная задача не новая CRM, а надёжная связь уже существующих систем.", "/api-integrations/", "Услуга"),
        ],
    ),
    "/backend-development/": (
        "Связанные сценарии для backend-задачи",
        [
            ("SEO Control Center", "Пример продукта с серверной логикой, данными и внешними интеграциями.", "/cases/seo-control-center/", "Кейс"),
            ("n8n или backend", "Когда автоматизацию стоит оставить workflow, а когда вынести в код.", "/guides/n8n-vs-backend/", "Разбор"),
            ("Разработка MVP", "Если backend нужен как часть первого законченного релиза продукта.", "/mvp-development/", "Услуга"),
        ],
    ),
    "/python-development/": (
        "Что ещё посмотреть для Python-задачи",
        [
            ("SheetPilot AI", "Рабочий кейс сервиса обработки Excel с серверной Python-логикой и публичным демо.", "/cases/sheetpilot-ai/", "Кейс"),
            ("Доработка Telegram-бота", "Для существующего Python/aiogram-проекта: ошибки, интеграции и продолжение чужого кода.", "/telegram-bot-repair/", "Услуга"),
            ("Разработка MVP", "Если Python - часть первого рабочего продукта, а не отдельный скрипт.", "/mvp-development/", "Услуга"),
        ],
    ),
    "/api-integrations/": (
        "Связанные материалы перед интеграцией",
        [
            ("CRM для автосалона", "Кейс системы, где данные и рабочие статусы объединены в один процесс.", "/cases/auto-crm/", "Кейс"),
            ("Своя CRM или готовая", "Помогает понять, что именно нужно интегрировать и стоит ли строить отдельную систему.", "/guides/custom-crm-or-ready/", "Разбор"),
            ("Доработка проекта", "Если API уже подключён, но обмен ломается или текущую реализацию нужно продолжить.", "/project-repair/", "Услуга"),
        ],
    ),
    "/project-repair/": (
        "Если проект уже существует - сначала полезно сравнить варианты",
        [
            ("SiteAudit Studio", "Кейс рабочего инструмента, где важны проверка текущего состояния и понятный результат.", "/cases/siteaudit-studio/", "Кейс"),
            ("Исправлять или переписывать", "Разбор критериев, когда точечная доработка безопаснее полного переписывания.", "/guides/repair-vs-rewrite/", "Разбор"),
            ("Доработка Telegram-бота", "Отдельный вход для существующих ботов: чужой код, ошибки и сломанные интеграции.", "/telegram-bot-repair/", "Услуга"),
        ],
    ),
}

TITLE_FIXES = {
    "/services/": "Услуги разработки: сайты, Telegram, CRM | Alexuys",
    "/web-development/": "Разработка сайтов и веб-сервисов на заказ | Alexuys",
    "/cases/": "Кейсы разработки: Telegram, CRM, iOS и веб | Alexuys",
    "/guides/": "Гайды по Telegram, n8n, CRM и разработке | Alexuys",
    "/cases/seo-control-center/": "SEO Control Center - SEO и индексация | кейс Alexuys",
}

HREFLANG_FIXES = {
    "/cases/": {
        "ru": f"{BASE}/cases/",
        "en": f"{BASE}/en/cases/",
        "x-default": f"{BASE}/cases/",
    },
    "/guides/": {
        "ru": f"{BASE}/guides/",
        "en": f"{BASE}/en/guides/",
        "x-default": f"{BASE}/guides/",
    },
}


def route_file(route: str) -> Path:
    return ROOT / ("index.html" if route == "/" else route.strip("/") + "/index.html")


def build_related(route: str, title: str, cards: list[tuple[str, str, str, str]]) -> str:
    sid = "stage101-" + route.strip("/").replace("/", "-")
    items = []
    for card_title, body, href, kind in cards:
        items.append(
            '<a class="s101-card" href="{href}">'
            '<span class="s101-kind">{kind}</span>'
            '<h3>{title}</h3>'
            '<p>{body}</p>'
            '<b>Открыть →</b>'
            '</a>'.format(
                href=html_lib.escape(href, quote=True),
                kind=html_lib.escape(kind),
                title=html_lib.escape(card_title),
                body=html_lib.escape(body),
            )
        )
    return (
        f'<section class="s101-related" data-stage101-related="true" aria-labelledby="{sid}">'
        '<div class="container">'
        '<div class="s101-head">'
        '<span>ПРОВЕРИТЬ ДО ОБРАЩЕНИЯ</span>'
        f'<div><h2 id="{sid}">{html_lib.escape(title)}</h2>'
        '<p>Кейс показывает уровень реализации, разбор помогает выбрать подход, соседняя услуга - не переплачивать за неправильный формат.</p></div>'
        '</div>'
        f'<div class="s101-grid">{"".join(items)}</div>'
        '<nav class="s101-more" aria-label="Дополнительные разделы">'
        '<a href="/cases/">Все кейсы</a><a href="/guides/">Все разборы</a><a href="/services/">Все услуги</a>'
        '</nav>'
        '</div></section>'
    )


def insert_before_contact(text: str, block: str, route: str) -> str:
    if 'data-stage101-related="true"' in text:
        return text
    patterns = [
        r'<section\b[^>]*class="[^"]*\bs48-contact\b[^"]*"[^>]*>',
        r'<section\b[^>]*\bid="contact"[^>]*>',
        r'</main>',
    ]
    for pat in patterns:
        match = re.search(pat, text, flags=re.I)
        if match:
            return text[:match.start()] + block + "\n" + text[match.start():]
    raise SystemExit(f"stage101: no insertion point for {route}")


def set_title(text: str, title: str, route: str) -> str:
    escaped = html_lib.escape(title, quote=True)
    text, count = re.subn(r"<title>.*?</title>", f"<title>{escaped}</title>", text, count=1, flags=re.S | re.I)
    if count != 1:
        raise SystemExit(f"stage101: title missing on {route}")
    for attr, key in (("property", "og:title"), ("name", "twitter:title")):
        pat = re.compile(rf'(<meta\b(?=[^>]*\b{attr}="{re.escape(key)}")[^>]*\bcontent=")[^"]*(")', re.I)
        text = pat.sub(lambda m: m.group(1) + escaped + m.group(2), text, count=1)
    return text


def fix_hreflang(text: str, mapping: dict[str, str]) -> str:
    # Remove only alternate language tags, then write a complete reciprocal set.
    text = re.sub(
        r'<link\b(?=[^>]*\brel="alternate")(?=[^>]*\bhreflang="[^"]+")[^>]*>\s*',
        "",
        text,
        flags=re.I,
    )
    tags = "".join(
        f'<link rel="alternate" hreflang="{lang}" href="{html_lib.escape(url, quote=True)}"/>'
        for lang, url in mapping.items()
    )
    return text.replace("</head>", tags + "\n</head>", 1)


def add_tools_to_footer(text: str) -> tuple[str, bool]:
    if 'lang="ru"' not in text[:300].lower() or 'href="/tools/"' in text:
        return text, False
    footer = re.search(r"<footer\b.*?</footer>", text, flags=re.S | re.I)
    if not footer:
        return text, False
    chunk = footer.group(0)
    insertion = '<a href="/tools/">Инструменты</a>'
    # Put it next to the other navigation destinations, before legal/demo links.
    for marker in ('<a href="/privacy/"', '<a href="/demos/"'):
        pos = chunk.find(marker)
        if pos >= 0:
            chunk = chunk[:pos] + insertion + chunk[pos:]
            break
    else:
        chunk = chunk.replace("</footer>", insertion + "</footer>", 1)
    return text[:footer.start()] + chunk + text[footer.end():], True


changed_routes: set[str] = set()

for route, (title, cards) in RELATED.items():
    path = route_file(route)
    if not path.is_file():
        raise SystemExit(f"stage101: missing {path}")
    text = path.read_text(encoding="utf-8")
    new_text = insert_before_contact(text, build_related(route, title, cards), route)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        changed_routes.add(route)

for route, title in TITLE_FIXES.items():
    path = route_file(route)
    if not path.is_file():
        raise SystemExit(f"stage101: missing title page {path}")
    text = path.read_text(encoding="utf-8")
    new_text = set_title(text, title, route)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        changed_routes.add(route)

for route, mapping in HREFLANG_FIXES.items():
    path = route_file(route)
    text = path.read_text(encoding="utf-8")
    new_text = fix_hreflang(text, mapping)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        changed_routes.add(route)

footer_changes = 0
for path in sorted(ROOT.rglob("*.html")):
    if path.name != "index.html":
        continue
    text = path.read_text(encoding="utf-8")
    new_text, changed = add_tools_to_footer(text)
    if changed:
        path.write_text(new_text, encoding="utf-8")
        footer_changes += 1

# Update lastmod only for pages whose primary content/search presentation changed.
sitemap = ROOT / "sitemap.xml"
if not sitemap.is_file():
    raise SystemExit("stage101: sitemap.xml missing")
xml = sitemap.read_text(encoding="utf-8")
for route in sorted(changed_routes):
    loc = BASE + route
    block_re = re.compile(rf"(<url>\s*.*?<loc>{re.escape(loc)}</loc>.*?</url>)", flags=re.S)
    match = block_re.search(xml)
    if not match:
        raise SystemExit(f"stage101: sitemap entry missing for {loc}")
    block = match.group(1)
    if "<lastmod>" in block:
        patched = re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{TODAY}</lastmod>", block, count=1)
    else:
        patched = block.replace(f"<loc>{loc}</loc>", f"<loc>{loc}</loc><lastmod>{TODAY}</lastmod>", 1)
    xml = xml[:match.start(1)] + patched + xml[match.end(1):]
sitemap.write_text(xml, encoding="utf-8")

# Final guards: links that previously became orphans must exist in the final graph.
all_html = "\n".join(p.read_text(encoding="utf-8") for p in ROOT.rglob("*.html") if p.name == "index.html")
for target in ("/telegram-bot-repair/", "/tools/", "/cases/fin-planner/", "/guides/telegram-bot-cost/"):
    if f'href="{target}"' not in all_html:
        raise SystemExit(f"stage101: final discovery link missing: {target}")

for route in RELATED:
    text = route_file(route).read_text(encoding="utf-8")
    if text.count('data-stage101-related="true"') != 1:
        raise SystemExit(f"stage101: related block invariant failed on {route}")
    if text.find('data-stage101-related="true"') > text.find('class="s48-contact'):
        raise SystemExit(f"stage101: related block must precede contact on {route}")

for route, expected in TITLE_FIXES.items():
    text = route_file(route).read_text(encoding="utf-8")
    if f"<title>{html_lib.escape(expected, quote=True)}</title>" not in text:
        raise SystemExit(f"stage101: title guard failed on {route}")

for route, mapping in HREFLANG_FIXES.items():
    text = route_file(route).read_text(encoding="utf-8")
    for lang, url in mapping.items():
        if f'hreflang="{lang}"' not in text or html_lib.escape(url, quote=True) not in text:
            raise SystemExit(f"stage101: hreflang guard failed on {route}: {lang}")

print(f"stage101: search entry flow ready; related={len(RELATED)} title_fixes={len(TITLE_FIXES)} footer_tools={footer_changes} changed_lastmod={len(changed_routes)}")
