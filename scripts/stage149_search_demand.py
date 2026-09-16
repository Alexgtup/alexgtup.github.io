#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
BASE = "https://alexgtup.github.io"
TODAY = "2026-09-16"

PAGES = {
    "/telegram-bots/": {
        "title": "Разработка Telegram-ботов на заказ - CRM, API, Mini Apps | Alexuys",
        "description": "Разработка Telegram-ботов на заказ для бизнеса: заявки, CRM, API, платежи, уведомления и Mini Apps. Запуск нового бота и доработка существующего проекта.",
        "heading": "Разработка Telegram-бота: задачи, с которыми приходят чаще всего.",
        "intro": "Обычно нужен не просто бот, а законченный путь: принять заявку, проверить данные, получить оплату, передать клиента в CRM или дать пользователю интерфейс внутри Telegram.",
        "items": [
            ("Telegram-бот для бизнеса", "Заявки, анкеты, уведомления, каталог, подписки и внутренние сценарии без ручной обработки каждого сообщения."),
            ("Telegram + CRM и API", "Передача лидов, статусов и данных между ботом, сайтом, CRM, платежами и другими сервисами."),
            ("Telegram Mini App", "Формы, каталог, кабинет и полноценный интерфейс внутри Telegram, когда обычных кнопок уже мало."),
        ],
        "links": [("/cases/fin-planner/", "Кейс Telegram-продукта"), ("/telegram-bot-repair/", "Доработка Telegram-бота"), ("/api-integrations/", "API-интеграции")],
    },
    "/n8n-automation/": {
        "title": "n8n автоматизация бизнеса на заказ - CRM, Telegram, API | Alexuys",
        "description": "n8n автоматизация бизнес-процессов: заявки, CRM, Telegram, Google Sheets, API, webhooks и уведомления. Проектирование, запуск и доработка workflow.",
        "heading": "n8n автоматизация бизнеса: что имеет смысл отдавать workflow.",
        "intro": "Лучший кандидат на автоматизацию - повторяющийся процесс с понятным событием и результатом. n8n особенно полезен там, где одинаковые данные вручную переносят между формами, CRM, таблицами, Telegram и API.",
        "items": [
            ("Автоматизация заявок", "Форма или сообщение создаёт запись, проверяет данные, назначает ответственного и отправляет уведомление."),
            ("CRM и сервисы через n8n", "Синхронизация статусов, клиентов, документов и уведомлений между рабочими системами."),
            ("Webhooks и API", "Обработка событий внешних сервисов с retry, логированием и защитой от дублей."),
        ],
        "links": [("/guides/n8n-vs-backend/", "n8n или backend"), ("/api-integrations/", "Интеграция API"), ("/cases/seo-control-center/", "Кейс автоматизации")],
    },
    "/crm-development/": {
        "title": "Разработка CRM под заказ - система под процессы бизнеса | Alexuys",
        "description": "Разработка CRM системы под заказ: заявки, сделки, роли, статусы, отчеты и интеграции с сайтом, Telegram и API. Своя CRM без лишних функций коробочного продукта.",
        "heading": "CRM под заказ: система под ваш процесс, а не ещё одна таблица.",
        "intro": "Собственная CRM становится оправданной, когда сотрудники уже подстраивают работу под Excel, мессенджеры или ограничения готовой системы. Сначала фиксируются сущности, роли и этапы, затем интерфейс и автоматизация.",
        "items": [
            ("CRM система под заказ", "Клиенты, заявки, сделки, задачи и история действий в одном рабочем контуре."),
            ("CRM для отдела продаж", "Воронка, статусы, ответственные, напоминания и отчётность без лишних модулей."),
            ("Интеграции CRM", "Сайт, Telegram, почта и внешние API подключаются к единому источнику данных."),
        ],
        "links": [("/cases/auto-crm/", "CRM для автосалона"), ("/guides/custom-crm-or-ready/", "Своя CRM или готовая"), ("/api-integrations/", "Интеграции CRM")],
    },
    "/backend-development/": {
        "title": "Backend и API для приложения - разработка серверной части | Alexuys",
        "description": "Backend и API для веб- и мобильных приложений: серверная логика, база данных, авторизация, webhooks, интеграции и REST API. Разработка и доработка backend.",
        "heading": "Backend и API для приложения: серверная часть основного сценария.",
        "intro": "Мобильному приложению, веб-интерфейсу или боту нужен предсказуемый серверный контракт: хранение данных, авторизация, бизнес-правила и понятное поведение при ошибках. Backend проектируется вокруг этих сценариев, а не вокруг набора случайных endpoints.",
        "items": [
            ("Backend для приложения", "Авторизация, данные пользователя, бизнес-правила, файлы, уведомления и состояние продукта."),
            ("REST API для frontend", "Понятные endpoints, валидация, коды ошибок, ограничения и стабильный контракт между интерфейсом и сервером."),
            ("База данных и интеграции", "PostgreSQL, внешние API, webhooks и фоновые задачи связываются вокруг одной модели данных."),
        ],
        "links": [("/api-integrations/", "Интеграции API"), ("/mvp-development/", "Backend для MVP"), ("/app-development/", "Мобильная разработка")],
    },
    "/api-integrations/": {
        "title": "Интеграция API на заказ - CRM, Telegram, платежи и сервисы | Alexuys",
        "description": "Интеграция REST API и webhooks: CRM, Telegram, сайты, платежи, базы данных и внешние сервисы. Синхронизация данных, обработка ошибок и повторных событий.",
        "heading": "Интеграция API: связать сервисы так, чтобы данные не терялись.",
        "intro": "Интеграция нужна, чтобы убрать ручной перенос данных и соединить используемые инструменты. Кроме успешного запроса проектируются повторы, таймауты, авторизация, журналирование и источник истины.",
        "items": [
            ("REST API интеграция", "Подключение внешнего сервиса к сайту, backend, CRM или внутренней системе."),
            ("CRM, Telegram и платежи", "Заявка или оплата автоматически меняет данные и запускает следующий шаг процесса."),
            ("Webhooks и синхронизация", "События обрабатываются без дублей, а временный сбой внешнего сервиса не теряет операцию."),
        ],
        "links": [("/backend-development/", "Разработка backend"), ("/n8n-automation/", "Автоматизация n8n"), ("/crm-development/", "CRM под заказ")],
    },
    "/mvp-development/": {
        "title": "Разработка MVP на заказ - веб-сервис или приложение | Alexuys",
        "description": "Разработка MVP продукта: веб-сервис, приложение, Telegram Mini App или внутренний инструмент. Главный пользовательский сценарий, backend, API и запуск первой версии.",
        "heading": "Разработка MVP: первая версия должна проверять идею.",
        "intro": "Для MVP важен один законченный пользовательский путь. Регистрация, основное действие, данные и результат должны работать вместе; второстепенные функции добавляются после проверки первой версии.",
        "items": [
            ("MVP веб-сервиса", "Frontend, backend, база данных и основной сценарий без преждевременного усложнения архитектуры."),
            ("MVP мобильного приложения", "Первый рабочий путь для мобильного продукта с API и серверной логикой."),
            ("MVP Telegram Mini App", "Быстрый формат, если продукту подходит аудитория Telegram и нужен интерфейс сложнее обычного бота."),
        ],
        "links": [("/web-development/", "Веб-разработка"), ("/app-development/", "Мобильное приложение"), ("/guides/development-cost/", "Стоимость разработки")],
    },
    "/web-development/": {
        "title": "Разработка веб-приложений на заказ - сервисы, кабинеты, SaaS | Alexuys",
        "description": "Разработка веб-приложений и сервисов на заказ: личные кабинеты, SaaS, внутренние системы, каталоги, frontend, backend и API. От первого сценария до запуска.",
        "heading": "Веб-приложение на заказ: интерфейс, данные и backend как один продукт.",
        "intro": "Веб-приложение - это рабочий сценарий: пользователь входит, выполняет действие, данные сохраняются, а система выдаёт результат. Поэтому интерфейс, backend и интеграции проектируются вместе.",
        "items": [
            ("Личный кабинет", "Авторизация, роли, данные пользователя, формы, документы, статусы и действия внутри системы."),
            ("SaaS и веб-сервис", "Продукт с собственной логикой, backend, API и возможностью развивать функции после запуска."),
            ("Внутренняя система", "Интерфейс для сотрудников: заявки, каталоги, отчеты и автоматизация рабочего процесса."),
        ],
        "links": [("/cases/factory-catalog/", "Кейс B2B-каталога"), ("/backend-development/", "Backend и API"), ("/mvp-development/", "Разработка MVP")],
    },
    "/wordpress-development/": {
        "title": "Доработка WordPress сайта - разработчик WordPress | Alexuys",
        "description": "Доработка WordPress сайта: исправление ошибок, формы, темы и плагины, мобильная версия, скорость, API, техническое SEO и микроразметка без лишней пересборки.",
        "heading": "Доработка WordPress: исправить проблему и сохранить рабочую основу.",
        "intro": "Для действующего WordPress-сайта чаще нужна аккуратная доработка: исправить форму, адаптив, тему, плагин, скорость, SEO или интеграцию. Сначала проверяется текущая реализация, затем выбирается минимальный безопасный объём изменений.",
        "items": [
            ("Доработка WordPress сайта", "Новые блоки и страницы, изменение шаблона, логики, форм и пользовательских сценариев."),
            ("Исправление WordPress", "PHP, JavaScript, плагины, тема, мобильная версия и конфликты после обновлений."),
            ("WordPress SEO и скорость", "Canonical, sitemap, микроразметка, индексация, производительность и технические ошибки."),
        ],
        "links": [("/project-repair/", "Доработка существующего проекта"), ("/web-development/", "Веб-разработка"), ("/api-integrations/", "API для WordPress")],
    },
}

STYLE = '''<style id="stage149-search-demand">
.search-demand{padding:clamp(4.6rem,7vw,7rem) 0;border-top:1px solid rgba(255,255,255,.08)}
.search-demand__shell{width:min(100%,88rem);margin:auto;padding-inline:clamp(1.1rem,4vw,4rem)}
.search-demand__head{display:grid;grid-template-columns:minmax(7rem,.25fr) minmax(0,1fr);gap:clamp(1.2rem,4vw,4rem);margin-bottom:2rem}
.search-demand__eyebrow{color:#78818b;font:750 .64rem/1.3 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase}
.search-demand h2{margin:0;max-width:17ch;font-size:clamp(2.3rem,4.2vw,4.4rem);line-height:.98;letter-spacing:-.05em}
.search-demand__intro{max-width:52rem;color:#929ba5;line-height:1.72}
.search-demand__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem}
.search-demand__card{padding:1.15rem;border:1px solid rgba(255,255,255,.09);border-radius:1rem;background:rgba(255,255,255,.018)}
.search-demand__card h3{margin:0 0 .55rem;font-size:1.05rem}.search-demand__card p{margin:0;color:#8f98a2;font-size:.86rem;line-height:1.62}
.search-demand__links{display:flex;gap:.55rem;flex-wrap:wrap;margin-top:1.15rem}.search-demand__links a{padding:.62rem .75rem;border:1px solid rgba(255,255,255,.09);border-radius:.7rem;text-decoration:none;font-size:.76rem}
@media(max-width:760px){.search-demand__head,.search-demand__grid{grid-template-columns:1fr}.search-demand{padding:4rem 0}}
</style>'''


def page_path(route: str) -> Path:
    return ROOT / ("index.html" if route == "/" else route.strip("/") + "/index.html")


def set_title(src: str, value: str) -> str:
    if not re.search(r"<title>.*?</title>", src, re.I | re.S):
        raise SystemExit("stage149: title missing")
    return re.sub(r"<title>.*?</title>", f"<title>{html.escape(value)}</title>", src, count=1, flags=re.I | re.S)


def set_meta(src: str, attr: str, key: str, value: str) -> str:
    escaped = html.escape(value, quote=True)
    patterns = [
        rf'<meta\s+content="[^"]*"\s+{attr}="{re.escape(key)}"\s*/?>',
        rf'<meta\s+{attr}="{re.escape(key)}"\s+content="[^"]*"\s*/?>',
    ]
    replacement = f'<meta content="{escaped}" {attr}="{key}"/>'
    for pattern in patterns:
        if re.search(pattern, src, re.I):
            return re.sub(pattern, replacement, src, count=1, flags=re.I)
    raise SystemExit(f"stage149: missing {attr}={key}")


def pop_section(src: str, class_token: str) -> tuple[str, str]:
    start_re = re.compile(rf'<section\b[^>]*class="[^"]*{re.escape(class_token)}[^"]*"[^>]*>', re.I)
    start = start_re.search(src)
    if not start:
        return src, ""
    depth = 0
    end_pos = None
    for tag in re.finditer(r'</?section\b[^>]*>', src[start.start():], re.I):
        token = tag.group(0)
        if token.lower().startswith('</section'):
            depth -= 1
            if depth == 0:
                end_pos = start.start() + tag.end()
                break
        else:
            depth += 1
    if end_pos is None:
        raise SystemExit(f"stage149: unbalanced section {class_token}")
    block = src[start.start():end_pos]
    return src[:start.start()] + src[end_pos:], block


def contact_pos(src: str) -> int:
    for token in ("p129-contact", "p130-footer-cta", "contact"):
        match = re.search(rf'<section\b[^>]*class="[^"]*{re.escape(token)}[^"]*"[^>]*>', src, re.I)
        if match:
            return match.start()
    raise SystemExit("stage149: final contact section missing")


def render(data: dict) -> str:
    cards = ''.join(
        f'<article class="search-demand__card"><h3>{html.escape(title)}</h3><p>{html.escape(text)}</p></article>'
        for title, text in data["items"]
    )
    links = ''.join(f'<a href="{url}">{html.escape(label)} ↗</a>' for url, label in data["links"])
    return (
        '<section class="search-demand" aria-labelledby="search-demand-title">'
        '<div class="search-demand__shell">'
        '<div class="search-demand__head"><span class="search-demand__eyebrow">ЗАДАЧИ / ПОИСК</span><div>'
        f'<h2 id="search-demand-title">{html.escape(data["heading"])}</h2>'
        f'<p class="search-demand__intro">{html.escape(data["intro"])}</p></div></div>'
        f'<div class="search-demand__grid">{cards}</div><div class="search-demand__links">{links}</div>'
        '</div></section>'
    )


changed = []
for route, data in PAGES.items():
    path = page_path(route)
    if not path.is_file():
        raise SystemExit(f"stage149: page missing {route}")
    src = path.read_text(encoding="utf-8")
    src, _ = pop_section(src, "search-demand")
    src, depth_block = pop_section(src, "x146-depth")
    src = re.sub(r'<style id="stage149-search-demand">.*?</style>', '', src, count=1, flags=re.I | re.S)
    src = set_title(src, data["title"])
    src = set_meta(src, "name", "description", data["description"])
    src = set_meta(src, "property", "og:title", data["title"])
    src = set_meta(src, "property", "og:description", data["description"])
    src = set_meta(src, "name", "twitter:title", data["title"])
    src = set_meta(src, "name", "twitter:description", data["description"])
    if "</head>" not in src:
        raise SystemExit(f"stage149: head marker missing {route}")
    src = src.replace("</head>", STYLE + "</head>", 1)
    pos = contact_pos(src)
    before_contact = (depth_block + render(data))
    src = src[:pos] + before_contact + src[pos:]
    path.write_text(src, encoding="utf-8")
    changed.append(route)

# Service hub: move any late search-depth helper before the final CTA and add a direct commercial index.
hub = page_path('/services/')
hub_src = hub.read_text(encoding='utf-8')
hub_src, _ = pop_section(hub_src, 'search-demand-hub')
hub_src, hub_depth = pop_section(hub_src, 'x146-depth')
hub_block = '''<section class="search-demand-hub" style="padding:2rem 0 4rem"><div class="container"><p style="color:#7f8892;font-size:.72rem;margin:0 0 .75rem">Популярные направления</p><div style="display:flex;gap:.55rem;flex-wrap:wrap"><a href="/telegram-bots/">Telegram-боты</a><a href="/n8n-automation/">Автоматизация n8n</a><a href="/crm-development/">CRM под заказ</a><a href="/backend-development/">Backend и API</a><a href="/api-integrations/">API-интеграции</a><a href="/mvp-development/">MVP</a><a href="/web-development/">Веб-приложения</a><a href="/wordpress-development/">WordPress</a></div></div></section>'''
hub_pos = contact_pos(hub_src)
hub_src = hub_src[:hub_pos] + hub_depth + hub_block + hub_src[hub_pos:]
hub.write_text(hub_src, encoding='utf-8')

sitemap = ROOT / 'sitemap.xml'
xml = sitemap.read_text(encoding='utf-8')
for route in changed + ['/services/']:
    loc = BASE + route
    pattern = re.compile(rf'(<url>.*?<loc>{re.escape(loc)}</loc>.*?</url>)', re.S)
    match = pattern.search(xml)
    if not match:
        raise SystemExit(f'stage149: sitemap entry missing {loc}')
    block = match.group(1)
    if '<lastmod>' in block:
        fresh = re.sub(r'<lastmod>[^<]+</lastmod>', f'<lastmod>{TODAY}</lastmod>', block, count=1)
    else:
        fresh = block.replace(f'<loc>{loc}</loc>', f'<loc>{loc}</loc><lastmod>{TODAY}</lastmod>', 1)
    xml = xml[:match.start(1)] + fresh + xml[match.end(1):]
sitemap.write_text(xml, encoding='utf-8')

for route, data in PAGES.items():
    out = page_path(route).read_text(encoding='utf-8')
    for token in (data['title'], data['description'], 'search-demand__grid'):
        if token not in out:
            raise SystemExit(f'stage149: guard failed {route}: {token[:40]}')
    demand_pos = out.find('<section class="search-demand"')
    cta_pos = contact_pos(out)
    if demand_pos < 0 or demand_pos > cta_pos:
        raise SystemExit(f'stage149: demand block must precede contact {route}')

print('stage149 search demand: ' + ', '.join(changed))
