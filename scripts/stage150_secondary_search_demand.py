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
    "/telegram-mini-apps/": {
        "title": "Разработка Telegram Mini App на заказ - Web App, Bot API | Alexuys",
        "description": "Разработка Telegram Mini App на заказ: каталог, личный кабинет, формы, оплаты, Telegram Web App API, backend и Bot API. От сценария до запуска.",
        "heading": "Telegram Mini App: когда внутри Telegram нужен полноценный интерфейс.",
        "intro": "Mini App подходит, когда обычного диалога с ботом уже мало: нужен каталог, кабинет, форма с несколькими шагами, оплата или работа с данными в удобном интерфейсе. При этом приложение остаётся связано с ботом, backend и внешними API.",
        "items": [
            ("Каталог и заказ", "Карточки, фильтры, корзина, оформление и передача результата в CRM или внутреннюю систему."),
            ("Личный кабинет", "Авторизация через Telegram, профиль, статусы, документы, история действий и персональные данные."),
            ("Оплаты и backend", "Платёжный сценарий, серверная проверка данных, Bot API, webhooks и интеграции с рабочими сервисами."),
        ],
        "links": [("/telegram-bots/", "Telegram-боты"), ("/backend-development/", "Backend и API"), ("/mvp-development/", "MVP продукта")],
    },
    "/app-development/": {
        "title": "Разработка мобильных приложений на заказ - iOS и React Native | Alexuys",
        "description": "Разработка мобильных приложений на заказ: iOS, Swift, React Native, API, карты, авторизация, личные кабинеты и backend. MVP и развитие существующего приложения.",
        "heading": "Мобильное приложение на заказ: сначала основной пользовательский путь.",
        "intro": "Для первого релиза важнее не количество экранов, а один законченный сценарий: пользователь устанавливает приложение, входит, выполняет основное действие и получает результат. Архитектура, API и хранение данных строятся вокруг этого пути.",
        "items": [
            ("iOS приложение", "Нативные сценарии на Swift, работа с состоянием, API и особенностями платформы."),
            ("React Native", "Кроссплатформенный интерфейс, когда один продукт должен быстрее выйти на несколько мобильных платформ."),
            ("Backend для приложения", "Авторизация, база данных, уведомления, карты, файлы и интеграции через API."),
        ],
        "links": [("/ios-development/", "iOS / Swift"), ("/backend-development/", "Backend для приложения"), ("/cases/taxi-app/", "Кейс приложения такси")],
    },
    "/ios-development/": {
        "title": "Разработка iOS приложений на Swift - приложение для iPhone | Alexuys",
        "description": "Разработка iOS приложений на Swift: интерфейс, состояние, API, локальные данные, уведомления и подготовка рабочей версии для iPhone. Новый проект или доработка.",
        "heading": "iOS разработка на Swift: нативный сценарий вместо уменьшенной веб-страницы.",
        "intro": "Нативное приложение имеет смысл там, где важны поведение iOS, плавный интерфейс, локальное состояние и тесная работа с возможностями устройства. Разработка начинается с пользовательского пути и модели данных, а не с набора отдельных экранов.",
        "items": [
            ("Swift и нативный UI", "Экраны, навигация, состояния и взаимодействия, которые ощущаются частью iOS."),
            ("API и данные", "Авторизация, синхронизация с backend, локальное хранение и обработка сетевых ошибок."),
            ("Доработка iOS проекта", "Продолжение существующего приложения, исправление критичного сценария и подготовка следующей версии."),
        ],
        "links": [("/cases/swift-calendar/", "Кейс Swift Calendar"), ("/app-development/", "Мобильные приложения"), ("/project-repair/", "Доработка проекта")],
    },
    "/python-development/": {
        "title": "Python разработчик на заказ - боты, backend, API, автоматизация | Alexuys",
        "description": "Python разработка на заказ: Telegram-боты, backend, REST API, интеграции, обработка данных и автоматизация. Новый модуль или продолжение существующего кода.",
        "heading": "Python разработчик для backend, ботов, API и прикладной автоматизации.",
        "intro": "Python полезен там, где нужна серверная логика, работа с данными, интеграции или Telegram-сценарий. Язык выбирается под задачу: отдельный API, бот, обработчик данных или модуль можно развивать без обязательной пересборки всего продукта.",
        "items": [
            ("Telegram-боты на Python", "Диалоги, состояния, база данных, оплаты, CRM и внешние API."),
            ("Backend и REST API", "Серверная логика, авторизация, данные, webhooks и контракт для frontend или приложения."),
            ("Скрипты и автоматизация", "Обработка файлов и данных, фоновые задачи, интеграции и повторяемые операции."),
        ],
        "links": [("/telegram-bots/", "Telegram-боты"), ("/backend-development/", "Backend разработка"), ("/api-integrations/", "API-интеграции")],
    },
    "/ai-automation/": {
        "title": "AI автоматизация и AI-агенты на заказ - API, n8n, workflows | Alexuys",
        "description": "AI автоматизация процессов: AI-агенты, обработка текста и данных, интеграции с API, n8n workflows и внутренние инструменты. AI как часть рабочего сценария.",
        "heading": "AI автоматизация: модель должна закрывать конкретный шаг процесса.",
        "intro": "AI имеет смысл внедрять там, где понятны входные данные, ожидаемый результат и способ проверить ответ. Это может быть классификация, извлечение данных, подготовка черновика, анализ файла или следующий шаг внутри автоматизированного workflow.",
        "items": [
            ("AI внутри workflow", "Модель получает подготовленные данные, выполняет один контролируемый шаг и передаёт результат дальше."),
            ("AI + API", "Интеграция с существующим сервисом, CRM, Telegram или внутренней системой без отдельного ручного копирования."),
            ("Контроль результата", "Ограничения, проверки, fallback и логирование там, где ошибочный ответ влияет на рабочий процесс."),
        ],
        "links": [("/n8n-automation/", "n8n автоматизация"), ("/api-integrations/", "API-интеграции"), ("/cases/sheetpilot-ai/", "Кейс SheetPilot AI")],
    },
    "/project-repair/": {
        "title": "Доработка сайта и приложения - исправление чужого кода | Alexuys",
        "description": "Доработка существующего сайта, веб-сервиса или приложения: поиск причины, исправление ошибок, продолжение чужого кода, интеграции и следующий релиз без переписывания с нуля.",
        "heading": "Доработка существующего проекта: сначала найти причину, потом менять код.",
        "intro": "Если продукт уже работает, полная пересборка редко должна быть первым шагом. Сначала воспроизводится проблема, проверяются зависимости и критичный пользовательский путь, после чего можно исправить локальный риск и сохранить рабочие части проекта.",
        "items": [
            ("Исправление чужого кода", "Диагностика ошибки и изменение только той части, которая действительно мешает работе."),
            ("Продолжение разработки", "Новая функция или следующий релиз поверх существующей архитектуры без обязательного старта с нуля."),
            ("Интеграции и технический долг", "API, формы, backend, мобильная версия и накопленные ошибки разбираются по приоритету риска."),
        ],
        "links": [("/wordpress-development/", "Доработка WordPress"), ("/telegram-bot-repair/", "Доработка Telegram-бота"), ("/guides/repair-vs-rewrite/", "Чинить или переписывать")],
    },
    "/telegram-bot-repair/": {
        "title": "Доработка Telegram-бота на Python - aiogram, API, ошибки | Alexuys",
        "description": "Доработка Telegram-бота на Python: aiogram, база данных, API, оплаты, состояния, ошибки и чужой код. Диагностика и развитие существующего бота.",
        "heading": "Доработка Telegram-бота: найти точку сбоя и сохранить рабочую логику.",
        "intro": "У существующего бота уже есть пользователи, данные и рабочие ветки, поэтому переписывать всё ради одной ошибки опасно. Сначала воспроизводится сбой, проверяется состояние пользователя и обмен с внешними сервисами, затем вносится локальное исправление.",
        "items": [
            ("Python и aiogram", "Исправление handlers, состояний, callback-логики и переходов в существующем боте."),
            ("API, CRM и оплаты", "Проверка webhooks, повторных событий, таймаутов и корректной передачи данных между системами."),
            ("Продолжение чужого проекта", "Новые команды, сценарии и интеграции добавляются поверх уже работающего кода."),
        ],
        "links": [("/telegram-bots/", "Новый Telegram-бот"), ("/project-repair/", "Доработка проекта"), ("/cases/fin-planner/", "Кейс Telegram-продукта")],
    },
}

HUB = {
    "title": "Разработка на заказ: сайты, Telegram, CRM, приложения | Alexuys",
    "description": "Разработка на заказ: веб-приложения, Telegram-боты и Mini Apps, CRM, мобильные приложения, Python, API, n8n, WordPress и доработка существующих проектов.",
    "items": [
        ("/telegram-mini-apps/", "Нужен Telegram Mini App", "Каталог, кабинет, формы, оплаты и Web App API внутри Telegram."),
        ("/app-development/", "Нужно мобильное приложение", "iOS, React Native, API и backend вокруг основного пользовательского сценария."),
        ("/ios-development/", "Нужно приложение для iPhone", "Нативная разработка на Swift и работа с существующим iOS-проектом."),
        ("/python-development/", "Нужен Python разработчик", "Боты, backend, REST API, обработка данных и прикладная автоматизация."),
        ("/ai-automation/", "Нужно внедрить AI в процесс", "AI-агенты, обработка данных и модели внутри API или workflow."),
        ("/project-repair/", "Нужно продолжить чужой код", "Диагностика, исправления и следующий релиз без обязательной пересборки."),
        ("/telegram-bot-repair/", "Нужно исправить Telegram-бота", "Python, aiogram, API, состояния, оплаты и интеграции существующего бота."),
        ("/wordpress-development/", "Нужно доработать WordPress", "Формы, тема, плагины, адаптив, скорость, SEO и API."),
    ],
}

STYLE = '''<style id="stage150-secondary-demand">
.secondary-demand{padding:clamp(4.5rem,7vw,6.5rem) 0;border-top:1px solid rgba(255,255,255,.08)}
.secondary-demand__shell{width:min(100%,88rem);margin:auto;padding-inline:clamp(1.1rem,4vw,4rem)}
.secondary-demand__head{display:grid;grid-template-columns:minmax(7rem,.25fr) minmax(0,1fr);gap:clamp(1.2rem,4vw,4rem);margin-bottom:2rem}
.secondary-demand__eyebrow{margin:0;color:#78818b;font:750 .64rem/1.3 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase}
.secondary-demand h2{margin:0;max-width:17ch;font-size:clamp(2rem,4vw,4rem);line-height:1;letter-spacing:-.045em}
.secondary-demand__intro{max-width:52rem;margin:.9rem 0 0;color:#969fa8}
.secondary-demand__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem}
.secondary-demand__card{padding:1.25rem;border:1px solid rgba(255,255,255,.09);border-radius:1.05rem;background:rgba(255,255,255,.025)}
.secondary-demand__card h3{margin:0 0 .55rem;font-size:1rem}.secondary-demand__card p{margin:0;color:#919aa4;font-size:.88rem;line-height:1.65}
.secondary-demand__links{display:flex;gap:.55rem;flex-wrap:wrap;margin-top:1rem}.secondary-demand__links a{padding:.65rem .8rem;border:1px solid rgba(255,255,255,.1);border-radius:.75rem;text-decoration:none;font-size:.78rem}
.secondary-demand--hub .secondary-demand__grid{grid-template-columns:repeat(4,minmax(0,1fr))}.secondary-demand--hub a.secondary-demand__card{color:inherit;text-decoration:none}.secondary-demand--hub .secondary-demand__card span{display:block;margin-top:.8rem;color:#b8c0c8;font-size:.75rem}
@media(max-width:900px){.secondary-demand__grid,.secondary-demand--hub .secondary-demand__grid{grid-template-columns:1fr 1fr}.secondary-demand__head{grid-template-columns:1fr}}
@media(max-width:580px){.secondary-demand__grid,.secondary-demand--hub .secondary-demand__grid{grid-template-columns:1fr}}
</style>'''


def page_path(route: str) -> Path:
    return ROOT / route.strip("/") / "index.html"


def set_title_meta(src: str, title: str, description: str, route: str) -> str:
    src, n = re.subn(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", src, count=1, flags=re.I | re.S)
    if n != 1:
        raise SystemExit(f"stage150: title missing {route}")

    def replace_meta(text: str, attr: str, key: str, value: str) -> str:
        patterns = [
            rf'<meta\s+content="[^"]*"\s+{attr}="{re.escape(key)}"\s*/?>',
            rf'<meta\s+{attr}="{re.escape(key)}"\s+content="[^"]*"\s*/?>',
        ]
        replacement = f'<meta content="{html.escape(value, quote=True)}" {attr}="{key}"/>'
        for pattern in patterns:
            if re.search(pattern, text, flags=re.I):
                return re.sub(pattern, replacement, text, count=1, flags=re.I)
        raise SystemExit(f"stage150: meta {key} missing {route}")

    src = replace_meta(src, "name", "description", description)
    src = replace_meta(src, "property", "og:title", title)
    src = replace_meta(src, "property", "og:description", description)
    src = replace_meta(src, "name", "twitter:title", title)
    src = replace_meta(src, "name", "twitter:description", description)
    return src


def render_service(data: dict) -> str:
    cards = ''.join(
        f'<article class="secondary-demand__card"><h3>{html.escape(title)}</h3><p>{html.escape(text)}</p></article>'
        for title, text in data["items"]
    )
    links = ''.join(f'<a href="{url}">{html.escape(label)} ↗</a>' for url, label in data["links"])
    return (
        '<section class="secondary-demand" data-stage150="service">'
        '<div class="secondary-demand__shell">'
        '<div class="secondary-demand__head"><p class="secondary-demand__eyebrow">SEARCH / TASKS</p><div>'
        f'<h2>{html.escape(data["heading"])}</h2><p class="secondary-demand__intro">{html.escape(data["intro"])}</p>'
        '</div></div>'
        f'<div class="secondary-demand__grid">{cards}</div><nav class="secondary-demand__links" aria-label="Связанные услуги">{links}</nav>'
        '</div></section>'
    )


def render_hub() -> str:
    cards = ''.join(
        f'<a class="secondary-demand__card" href="{url}"><h3>{html.escape(title)}</h3><p>{html.escape(text)}</p><span>Открыть направление ↗</span></a>'
        for url, title, text in HUB["items"]
    )
    return (
        '<section class="secondary-demand secondary-demand--hub" data-stage150="hub">'
        '<div class="secondary-demand__shell">'
        '<div class="secondary-demand__head"><p class="secondary-demand__eyebrow">TASK / ROUTES</p><div>'
        '<h2>Частые задачи, с которыми приходят в разработку.</h2>'
        '<p class="secondary-demand__intro">Выбирать раздел проще от результата: запустить Mini App, сделать мобильное приложение, продолжить чужой код, исправить бота или связать существующий продукт с backend и API.</p>'
        '</div></div>'
        f'<div class="secondary-demand__grid">{cards}</div>'
        '</div></section>'
    )


def insert_before_contact(src: str, block: str, route: str) -> str:
    if 'data-stage150="service"' in src:
        return src
    marker = '<section class="p129-contact'
    idx = src.find(marker)
    if idx < 0:
        raise SystemExit(f"stage150: contact marker missing {route}")
    return src[:idx] + block + src[idx:]


def update_lastmod(routes: list[str]) -> None:
    p = ROOT / "sitemap.xml"
    xml = p.read_text(encoding="utf-8")
    for route in routes:
        loc = BASE + route
        pat = re.compile(rf'(<url>.*?<loc>{re.escape(loc)}</loc>.*?</url>)', re.S)
        m = pat.search(xml)
        if not m:
            raise SystemExit(f"stage150: sitemap entry missing {loc}")
        block = m.group(1)
        if '<lastmod>' in block:
            block2 = re.sub(r'<lastmod>[^<]+</lastmod>', f'<lastmod>{TODAY}</lastmod>', block, count=1)
        else:
            block2 = block.replace(f'<loc>{loc}</loc>', f'<loc>{loc}</loc><lastmod>{TODAY}</lastmod>', 1)
        xml = xml[:m.start(1)] + block2 + xml[m.end(1):]
    p.write_text(xml, encoding="utf-8")


changed = []
for route, data in PAGES.items():
    p = page_path(route)
    if not p.is_file():
        raise SystemExit(f"stage150: page missing {route}")
    src = p.read_text(encoding="utf-8")
    src = set_title_meta(src, data["title"], data["description"], route)
    if 'id="stage150-secondary-demand"' not in src:
        src = src.replace('</head>', STYLE + '</head>', 1)
    src = insert_before_contact(src, render_service(data), route)
    p.write_text(src, encoding="utf-8")
    final = p.read_text(encoding="utf-8")
    for token in (data["title"], data["heading"], 'data-stage150="service"'):
        if token not in final:
            raise SystemExit(f"stage150: guard failed {route}: {token}")
    changed.append(route)

hub_path = page_path('/services/')
hub = hub_path.read_text(encoding='utf-8')
hub = set_title_meta(hub, HUB["title"], HUB["description"], '/services/')
if 'id="stage150-secondary-demand"' not in hub:
    hub = hub.replace('</head>', STYLE + '</head>', 1)

# Replace the small stage149 pill list with a richer task-oriented hub.
hub = re.sub(r'<section class="search-demand-hub".*?</section>', '', hub, count=1, flags=re.S)
if 'data-stage150="hub"' not in hub:
    contact = re.search(r'<section class="p130-footer-cta[^>]*>.*?</section>', hub, flags=re.S)
    if not contact:
        raise SystemExit('stage150: services final CTA missing')
    cta = contact.group(0)
    hub = hub[:contact.start()] + hub[contact.end():]
    main_close = hub.find('</main>')
    if main_close < 0:
        raise SystemExit('stage150: services main closing tag missing')
    hub = hub[:main_close] + render_hub() + cta + hub[main_close:]
hub_path.write_text(hub, encoding='utf-8')

final_hub = hub_path.read_text(encoding='utf-8')
for token in (HUB["title"], 'data-stage150="hub"', '/wordpress-development/', '/telegram-mini-apps/'):
    if token not in final_hub:
        raise SystemExit(f'stage150: services guard failed: {token}')
if final_hub.rfind('p130-footer-cta') < final_hub.rfind('data-stage150="hub"'):
    raise SystemExit('stage150: services CTA must remain after demand hub')

changed.append('/services/')
update_lastmod(changed)
print('stage150 secondary search demand: ' + ', '.join(changed))
