#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html as html_lib
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage161-yandex-search-cleanup"

PAGES = {
    "/telegram-bots/": {
        "title": "Разработка Telegram-ботов на заказ - цена и кейсы | Alexuys",
        "description": "Разработчик Telegram-ботов: создание бота под задачу, API, оплаты, CRM и автоматизация. Кейсы, этапы работы и ориентир стоимости от 15 000 руб.",
        "keywords": "разработка telegram ботов, разработчик телеграм ботов, telegram бот на заказ, цена telegram бота, заказать telegram бота",
    },
    "/telegram-mini-apps/": {
        "title": "Telegram Mini App на заказ - разработка Mini Apps | Alexuys",
        "description": "Разработка Telegram Mini App на заказ: интерфейс внутри Telegram, backend, API, авторизация и интеграции. Примеры работ и прямой контакт с разработчиком.",
        "keywords": "telegram mini app на заказ, разработка mini apps, заказать telegram mini app, telegram web app разработка",
    },
    "/web-development/": {
        "title": "Разработка веб-сервисов на заказ - сайты и web apps | Alexuys",
        "description": "Разработка веб-сервисов и сайтов на заказ: интерфейс, backend, API, базы данных и интеграции. Реальные кейсы, запуск и доработка существующих проектов.",
        "keywords": "разработка веб сервисов, веб сервис на заказ, разработка сайта на заказ, web app разработка, веб разработчик",
    },
    "/backend-development/": {
        "title": "Backend-разработка на заказ - API и базы данных | Alexuys",
        "description": "Backend-разработчик на проект: серверная логика, REST API, базы данных, роли, интеграции и фоновые задачи. Разработка и доработка существующего backend.",
        "keywords": "backend разработчик на заказ, backend разработка, разработка api, серверная разработка, backend на проект",
    },
    "/project-repair/": {
        "title": "Доработка чужого проекта - сайты, боты и backend | Alexuys",
        "description": "Исправление и доработка существующего проекта: ошибки, чужой код, интеграции, адаптив, backend и Telegram-боты. Сначала воспроизводится проблема, затем локальная правка.",
        "keywords": "доработка чужого проекта, исправить проект, доработка сайта, доработка telegram бота, исправление чужого кода",
    },
    "/development/": {
        "title": "Разработка на заказ - сайты, боты, backend и автоматизация | Alexuys",
        "description": "Разработка цифровых проектов на заказ: Telegram-боты, веб-сервисы, backend, CRM, API и автоматизация. Кейсы, рабочие демо и прямой контакт с разработчиком.",
        "keywords": "разработка на заказ, разработчик на проект, разработка веб сервисов, разработка telegram ботов, backend разработка",
    },
    "/guides/telegram-bot-cost/": {
        "title": "Сколько стоит Telegram-бот в 2026 - цена разработки | Alexuys",
        "description": "Сколько стоит сделать Telegram-бота на заказ в 2026 году: ориентиры цены, что влияет на стоимость, примеры функций и как подготовить задачу к оценке.",
        "keywords": "сколько стоит telegram бот, цена telegram бота, стоимость разработки telegram бота, сделать бота в телеграмме цена",
    },
    "/guides/telegram-bot-brief/": {
        "title": "ТЗ на Telegram-бот - пример и шаблон требований | Alexuys",
        "description": "Как составить ТЗ на Telegram-бота: простой пример структуры, сценарии пользователя, команды, интеграции, данные и критерии готовности проекта.",
        "keywords": "тз на telegram бота, пример тз для бота, как написать тз для telegram, техническое задание telegram бот",
    },
    "/cases/seo-control-center/": {
        "title": "SEO Control Center - мониторинг индексации, позиций и CTR | кейс",
        "description": "Кейс SEO Control Center: мониторинг sitemap, индексации, поисковых запросов, позиций и CTR. Next.js, PostgreSQL, n8n и интеграции с поисковыми данными.",
        "keywords": "seo control center, мониторинг seo, мониторинг индексации, позиции сайта, ctr поиска, seo панель",
    },
    "/cases/sheetpilot-ai/": {
        "title": "ИИ-ассистент для Excel - SheetPilot AI | кейс разработки",
        "description": "SheetPilot AI - ИИ-ассистент для Excel: загрузка XLSX, изменение таблицы по текстовой команде, предпросмотр и экспорт нового файла. Python и FastAPI.",
        "keywords": "ии ассистент для excel, ai excel, редактировать excel с ии, обработка excel python, sheetpilot ai",
    },
    "/cases/fin-planner/": {
        "title": "Telegram-бот для учета доходов и расходов | кейс Fin Planner",
        "description": "Кейс Fin Planner: Telegram-бот для учета доходов и расходов, категорий и финансовой статистики. Сценарии пользователя, интерфейс и логика проекта.",
        "keywords": "telegram бот учет финансов, бот доходы расходы, финансовый бот telegram, учет расходов telegram",
    },
    "/tools/sitemap-validator/": {
        "title": "Sitemap Validator онлайн - проверить sitemap.xml бесплатно | Alexuys",
        "description": "Проверить sitemap.xml онлайн: формат XML, URL, структуру sitemap и типичные ошибки. Бесплатный Sitemap Validator работает прямо в браузере.",
        "keywords": "sitemap validator, sitemap test, проверить sitemap xml, validate sitemap, sitemap validator online",
    },
    "/demos/": {
        "title": "Демо веб-сервисов - Excel AI и SEO-мониторинг | Alexuys",
        "description": "Рабочие демо моих веб-сервисов: ИИ-ассистент для Excel SheetPilot AI и SEO Control Center. Можно открыть продукт, проверить сценарий и изучить кейс разработки.",
        "keywords": "демо веб сервисов, примеры веб разработки, sheetpilot ai, seo control center, портфолио разработчика",
    },
}

META_TAG_RE = re.compile(r"<meta\b[^>]*>", re.I)
TITLE_RE = re.compile(r"<title\b[^>]*>.*?</title>", re.I | re.S)


def route_path(route: str) -> Path:
    if route == "/":
        return ROOT / "index.html"
    return ROOT / route.strip("/") / "index.html"


def attr_value(tag: str, attr: str) -> str | None:
    m = re.search(rf"\b{re.escape(attr)}\s*=\s*([\"'])(.*?)\1", tag, re.I | re.S)
    return m.group(2) if m else None


def remove_meta(doc: str, *, name: str | None = None, prop: str | None = None) -> str:
    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        if name is not None and (attr_value(tag, "name") or "").lower() == name.lower():
            return ""
        if prop is not None and (attr_value(tag, "property") or "").lower() == prop.lower():
            return ""
        return tag
    return META_TAG_RE.sub(repl, doc)


def add_head(doc: str, markup: str) -> str:
    if "</head>" not in doc.lower():
        raise RuntimeError("missing </head>")
    return re.sub(r"</head>", markup + "\n</head>", doc, count=1, flags=re.I)


def set_search_meta(doc: str, title: str, description: str, keywords: str) -> str:
    esc_title = html_lib.escape(title, quote=False)
    esc_desc = html_lib.escape(description, quote=True)
    esc_keywords = html_lib.escape(keywords, quote=True)
    if TITLE_RE.search(doc):
        doc = TITLE_RE.sub(f"<title>{esc_title}</title>", doc, count=1)
    else:
        doc = add_head(doc, f"<title>{esc_title}</title>")

    for name in ("description", "keywords", "twitter:title", "twitter:description"):
        doc = remove_meta(doc, name=name)
    for prop in ("og:title", "og:description"):
        doc = remove_meta(doc, prop=prop)

    markup = (
        f'<meta name="description" content="{esc_desc}"/>\n'
        f'<meta name="keywords" content="{esc_keywords}"/>\n'
        f'<meta property="og:title" content="{html_lib.escape(title, quote=True)}"/>\n'
        f'<meta property="og:description" content="{esc_desc}"/>\n'
        f'<meta name="twitter:title" content="{html_lib.escape(title, quote=True)}"/>\n'
        f'<meta name="twitter:description" content="{esc_desc}"/>\n'
        f'<!-- {MARKER} -->'
    )
    return add_head(doc, markup)


def set_yandex_noindex(doc: str) -> str:
    doc = remove_meta(doc, name="yandex")
    return add_head(doc, '<meta name="yandex" content="noindex,follow"/>')


changed = []
for route, cfg in PAGES.items():
    path = route_path(route)
    if not path.exists():
        raise SystemExit(f"stage161: missing priority page {route}: {path}")
    doc = path.read_text(encoding="utf-8")
    doc = set_search_meta(doc, cfg["title"], cfg["description"], cfg["keywords"])
    path.write_text(doc, encoding="utf-8")
    changed.append(route)

# English pages remain indexable by Google/Bing, but Yandex should stop treating
# a large translated cluster as low-value search inventory. Yandex officially
# supports a bot-specific <meta name="yandex" content="noindex"> directive.
en_root = ROOT / "en"
en_changed = 0
if en_root.is_dir():
    for path in sorted(en_root.rglob("index.html")):
        doc = path.read_text(encoding="utf-8")
        doc = set_yandex_noindex(doc)
        path.write_text(doc, encoding="utf-8")
        en_changed += 1

# Guards: final output must contain unique priority metadata and Yandex-only
# noindex must not leak to Russian pages.
for route, cfg in PAGES.items():
    path = route_path(route)
    doc = path.read_text(encoding="utf-8")
    if doc.count(f"<title>{html_lib.escape(cfg['title'], quote=False)}</title>") != 1:
        raise SystemExit(f"stage161: title guard failed: {route}")
    if doc.count('name="description"') != 1:
        raise SystemExit(f"stage161: description uniqueness failed: {route}")
    if route != "/en/" and 'name="yandex" content="noindex' in doc:
        raise SystemExit(f"stage161: yandex noindex leaked to priority RU page: {route}")

if en_root.is_dir():
    bad = [str(p) for p in en_root.rglob("index.html") if 'name="yandex" content="noindex,follow"' not in p.read_text(encoding="utf-8")]
    if bad:
        raise SystemExit("stage161: EN Yandex noindex guard failed: " + ", ".join(bad[:5]))

print(f"stage161 Yandex/search cleanup: {len(changed)} priority pages, {en_changed} EN pages Yandex-noindex")
