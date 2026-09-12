#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html as H
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
BASE = "https://alexgtup.github.io"
TODAY = "2026-09-13"

TITLE_FIXES = {
    "/telegram-bots/": "Разработка Telegram-ботов на заказ — от 15 000 ₽ | Alexuys",
    "/n8n-automation/": "Автоматизация n8n на заказ — CRM, API, Telegram | Alexuys",
}

META_FIXES = {
    "/telegram-bots/": "Разработка Telegram-ботов на заказ: Python и aiogram 3, CRM/API, оплаты, базы данных и автоматизация. Первый рабочий сценарий — от 15 000 ₽.",
    "/n8n-automation/": "Автоматизация n8n и Make на заказ: CRM, Telegram, API, webhooks, таблицы и уведомления. Сборка рабочего workflow с обработкой ошибок и запуском.",
}

H1_FIXES = {
    "/telegram-bots/": "Разработка Telegram-ботов на заказ. <em>От сценария до рабочего запуска.</em>",
    "/n8n-automation/": "Автоматизация n8n и Make. <em>Связать системы и убрать ручные действия.</em>",
}

HOME_LINKS = [
    ("Разработка Telegram-ботов", "/telegram-bots/"),
    ("Разработка сайтов и веб-сервисов", "/web-development/"),
    ("Автоматизация n8n", "/n8n-automation/"),
    ("Разработка CRM", "/crm-development/"),
    ("API-интеграции", "/api-integrations/"),
    ("Доработка готового проекта", "/project-repair/"),
    ("Доработка Telegram-бота", "/telegram-bot-repair/"),
    ("Все услуги", "/services/"),
    ("Кейсы", "/cases/"),
    ("Гайды", "/guides/"),
]


def route_file(route: str) -> Path:
    return ROOT / ("index.html" if route == "/" else route.strip("/") + "/index.html")


def set_title(text: str, value: str, route: str) -> str:
    escaped = H.escape(value, quote=True)
    text, count = re.subn(r"<title>.*?</title>", f"<title>{escaped}</title>", text, count=1, flags=re.I | re.S)
    if count != 1:
        raise SystemExit(f"stage120: title missing on {route}")
    for attr, key in (("property", "og:title"), ("name", "twitter:title")):
        pat = re.compile(rf'(<meta\b(?=[^>]*\b{attr}="{re.escape(key)}")[^>]*\bcontent=")[^"]*(")', re.I)
        text = pat.sub(lambda m: m.group(1) + escaped + m.group(2), text, count=1)
    return text


def set_description(text: str, value: str, route: str) -> str:
    escaped = H.escape(value, quote=True)
    pat = re.compile(r'(<meta\b(?=[^>]*\bname="description")[^>]*\bcontent=")[^"]*(")', re.I)
    text, count = pat.subn(lambda m: m.group(1) + escaped + m.group(2), text, count=1)
    if count != 1:
        raise SystemExit(f"stage120: description missing on {route}")
    for attr, key in (("property", "og:description"), ("name", "twitter:description")):
        mp = re.compile(rf'(<meta\b(?=[^>]*\b{attr}="{re.escape(key)}")[^>]*\bcontent=")[^"]*(")', re.I)
        text = mp.sub(lambda m: m.group(1) + escaped + m.group(2), text, count=1)
    return text


def set_service_h1(text: str, value: str, route: str) -> str:
    text, count = re.subn(
        r'<h1\b[^>]*id="s48-title"[^>]*>.*?</h1>',
        f'<h1 id="s48-title">{value}</h1>',
        text,
        count=1,
        flags=re.I | re.S,
    )
    if count != 1:
        raise SystemExit(f"stage120: service H1 missing on {route}")
    return text


def insert_before_contact(text: str, block: str, route: str) -> str:
    patterns = [
        r'<section\b[^>]*class="[^"]*\bs48-contact\b[^"]*"[^>]*>',
        r'<section\b[^>]*class="[^"]*\bs50-cta\b[^"]*"[^>]*>',
        r'<section\b[^>]*\bid="contact"[^>]*>',
        r'</main>',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            return text[:match.start()] + block + "\n" + text[match.start():]
    raise SystemExit(f"stage120: no insertion point on {route}")


def add_home_priority_paths() -> bool:
    route = "/"
    path = route_file(route)
    text = path.read_text(encoding="utf-8")
    if 'data-stage120="home-priority"' in text:
        return False
    anchors = "".join(f'<a href="{href}">{H.escape(label)}</a>' for label, href in HOME_LINKS)
    block = (
        '<nav class="s101-more s120-priority" data-stage120="home-priority" '
        'aria-label="Основные направления разработки">'
        f'{anchors}</nav>'
    )
    text = insert_before_contact(text, block, route)
    path.write_text(text, encoding="utf-8")
    return True


def enrich_services_hub() -> bool:
    route = "/services/"
    path = route_file(route)
    text = path.read_text(encoding="utf-8")
    if 'data-stage120="services-intent"' in text:
        return False
    block = '''<section class="s44-section" data-stage120="services-intent" aria-labelledby="s120-services-title">
<div class="container"><div class="s44-section-head"><span>КАК ВЫБРАТЬ НАПРАВЛЕНИЕ</span><div>
<h2 id="s120-services-title">Не обязательно заранее знать стек. <em>Достаточно понять, что должно заработать.</em></h2>
<p>Если нужен интерфейс для клиентов или сотрудников, обычно речь идёт о сайте, веб-сервисе, CRM или мобильном приложении. Если основная задача происходит внутри Telegram - стоит начать с Telegram-бота или Mini App. Когда данные уже живут в нескольких системах и их приходится переносить вручную, чаще нужна API-интеграция или автоматизация n8n/Make.</p>
<p>Существующий проект не обязательно переписывать: отдельное направление посвящено доработке чужого кода, восстановлению интеграций и добавлению функций. Для новой идеи можно начать с MVP - одного законченного пользовательского сценария, который реально проверить до развития всего продукта.</p>
<nav class="s101-more" aria-label="Популярные услуги"><a href="/telegram-bots/">Разработка Telegram-ботов</a><a href="/web-development/">Разработка сайтов</a><a href="/n8n-automation/">Автоматизация n8n</a><a href="/crm-development/">Разработка CRM</a><a href="/api-integrations/">API-интеграции</a><a href="/project-repair/">Доработка проектов</a></nav>
</div></div></div></section>'''
    text = insert_before_contact(text, block, route)
    path.write_text(text, encoding="utf-8")
    return True


def enrich_freelance_page() -> bool:
    route = "/freelance-developer/"
    path = route_file(route)
    text = path.read_text(encoding="utf-8")
    if 'data-stage120="freelance-intent"' in text:
        return False
    block = '''<section class="s50-section" data-stage120="freelance-intent" aria-labelledby="s120-freelance-title"><div class="container">
<div class="s50-head"><span>ПРЯМАЯ РАБОТА</span><div><h2 id="s120-freelance-title">Фриланс-разработчик подходит, когда нужен <em>прямой контакт с исполнителем.</em></h2>
<p>Можно прийти с новой задачей, существующим сайтом, ботом или репозиторием. Для небольших доработок важнее быстро локализовать проблему и определить проверяемый результат; для нового продукта - выбрать первый законченный этап без лишней архитектуры заранее.</p>
<p>Основные направления: разработка Telegram-ботов, сайтов и веб-сервисов, CRM, API-интеграций, автоматизация n8n/Make и доработка существующих проектов. Кейсы и публичный профиль позволяют проверить опыт до обращения.</p>
<nav class="s101-more" aria-label="Направления фриланс-разработки"><a href="/telegram-bots/">Telegram-боты</a><a href="/web-development/">Web-разработка</a><a href="/project-repair/">Доработка проекта</a><a href="/cases/">Кейсы</a></nav>
</div></div></div></section>'''
    text = insert_before_contact(text, block, route)
    path.write_text(text, encoding="utf-8")
    return True


def patch_priority_service_pages() -> int:
    changed = 0
    for route, title in TITLE_FIXES.items():
        path = route_file(route)
        if not path.is_file():
            raise SystemExit(f"stage120: missing priority page {route}")
        text = path.read_text(encoding="utf-8")
        new = set_title(text, title, route)
        new = set_description(new, META_FIXES[route], route)
        new = set_service_h1(new, H1_FIXES[route], route)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def update_sitemap_lastmod(routes: set[str]) -> int:
    path = ROOT / "sitemap.xml"
    if not path.is_file():
        raise SystemExit("stage120: sitemap missing")
    text = path.read_text(encoding="utf-8")
    changed = 0
    for route in routes:
        url = BASE + ("/" if route == "/" else route)
        pattern = re.compile(rf'(<url>\s*<loc>{re.escape(url)}</loc>)(.*?)(</url>)', re.S)
        match = pattern.search(text)
        if not match:
            raise SystemExit(f"stage120: sitemap URL missing: {url}")
        middle = match.group(2)
        if re.search(r'<lastmod>[^<]+</lastmod>', middle):
            new_middle = re.sub(r'<lastmod>[^<]+</lastmod>', f'<lastmod>{TODAY}</lastmod>', middle, count=1)
        else:
            new_middle = f'<lastmod>{TODAY}</lastmod>' + middle
        replacement = match.group(1) + new_middle + match.group(3)
        text = text[:match.start()] + replacement + text[match.end():]
        changed += 1
    path.write_text(text, encoding="utf-8")
    return changed


def inbound_sources(target: str) -> int:
    needle = f'href="{target}"'
    sources: set[str] = set()
    for path in ROOT.rglob("*.html"):
        if path.name != "index.html":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if needle in text:
            sources.add(path.relative_to(ROOT).as_posix())
    return len(sources)


priority_changed = patch_priority_service_pages()
home_changed = add_home_priority_paths()
services_changed = enrich_services_hub()
freelance_changed = enrich_freelance_page()
lastmod_changed = update_sitemap_lastmod({"/", "/services/", "/telegram-bots/", "/n8n-automation/", "/freelance-developer/"})

checks = {
    "/services/": 5,
    "/cases/": 5,
    "/guides/": 5,
    "/freelance-developer/": 2,
    "/telegram-bot-repair/": 3,
}
for target, minimum in checks.items():
    count = inbound_sources(target)
    if count < minimum:
        raise SystemExit(f"stage120: weak inbound graph for {target}: {count} < {minimum}")

telegram = route_file("/telegram-bots/").read_text(encoding="utf-8")
n8n = route_file("/n8n-automation/").read_text(encoding="utf-8")
services = route_file("/services/").read_text(encoding="utf-8")
for needle, page in (
    ("Разработка Telegram-ботов на заказ", telegram),
    ("Python и aiogram 3", telegram),
    ("Автоматизация n8n на заказ", n8n),
    ('data-stage120="services-intent"', services),
):
    if needle not in page:
        raise SystemExit(f"stage120: search-intent invariant missing: {needle}")

print(
    "stage120 Google discovery: "
    f"priority_pages={priority_changed}; home={int(home_changed)}; services={int(services_changed)}; "
    f"freelance={int(freelance_changed)}; lastmod={lastmod_changed}; "
    + ", ".join(f"{target} inbound={inbound_sources(target)}" for target in checks)
)
