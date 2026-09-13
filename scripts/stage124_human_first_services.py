#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def route_file(route: str) -> Path:
    return ROOT / route.strip("/") / "index.html"


def fact_block(items: list[tuple[str, str]]) -> str:
    return '<div class="s48-facts">' + ''.join(
        f'<div><strong>{strong}</strong><span>{label}</span></div>' for strong, label in items
    ) + '</div>'


SERVICES = {
    "/telegram-bots/": {
        "kicker": "TELEGRAM-БОТЫ",
        "h1": "Разработка Telegram-бота под вашу задачу. <em>От первого сценария до запуска.</em>",
        "lead": "Бот для заявок, оплат, уведомлений или внутренних задач. Сначала запускаем один понятный сценарий, затем при необходимости подключаем CRM, платежи и другие сервисы. Первый этап — от 15 000 ₽.",
        "facts": [
            ("от 15 000 ₽", "первый рабочий этап"),
            ("Fin Planner", "пример реального бота"),
            ("CRM и оплаты", "подключаются при необходимости"),
        ],
        "flow": ["Клиент", "Бот", "Проверка", "Нужный сервис", "Результат"],
    },
    "/n8n-automation/": {
        "kicker": "АВТОМАТИЗАЦИЯ РУЧНОЙ РАБОТЫ",
        "h1": "Автоматизировать повторяющиеся действия. <em>n8n и Make — если они подходят задаче.</em>",
        "lead": "Если заявки, статусы или данные приходится переносить между сервисами вручную, соберу автоматический сценарий: нужное событие запускает проверки, действия и уведомления. Первый этап — от 15 000 ₽.",
        "facts": [
            ("от 15 000 ₽", "первый рабочий этап"),
            ("Несколько сервисов", "работают как один процесс"),
            ("Ошибки", "не теряются незаметно"),
        ],
        "flow": ["Событие", "Проверка", "Автоматизация", "Нужные сервисы", "Готово"],
    },
    "/web-development/": {
        "kicker": "САЙТЫ И ВЕБ-СЕРВИСЫ",
        "h1": "Сайт или веб-сервис. <em>От понятного интерфейса до рабочего запуска.</em>",
        "lead": "Лендинг, каталог, личный кабинет или внутренний сервис — с формами, данными и нужной логикой. Можно начать новый проект или доработать существующий.",
        "facts": [
            ("Сайт", "от лендинга до кабинета"),
            ("Реальный кейс", "B2B-каталог завода"),
            ("По этапам", "можно начать с первой версии"),
        ],
        "flow": ["Человек", "Интерфейс", "Логика", "Данные", "Результат"],
    },
    "/api-integrations/": {
        "kicker": "СВЯЗАТЬ СЕРВИСЫ",
        "h1": "Связать сайт, CRM, Telegram и другие сервисы. <em>Данные передаются автоматически.</em>",
        "lead": "Если информация живёт в разных системах и её приходится переносить вручную, настрою обмен: что передаём, когда, куда и что делать при ошибке. Технический способ связи подбирается после проверки сервисов.",
        "facts": [
            ("Сервисы", "работают вместе"),
            ("Данные", "передаются автоматически"),
            ("Ошибки", "остаются под контролем"),
        ],
        "flow": ["Сервис A", "Передача", "Проверка", "Сервис B", "Статус"],
    },
    "/project-repair/": {
        "kicker": "ДОРАБОТКА ГОТОВОГО ПРОЕКТА",
        "h1": "Проект уже есть, но что-то не работает или нужно продолжить. <em>Сначала найдём причину.</em>",
        "lead": "Можно прислать существующий сайт, бот, приложение или код. Сначала локализую проблему, затем меняю только нужный участок — без переписывания всего проекта без причины.",
        "facts": [
            ("от 10 000 ₽", "небольшая точечная задача"),
            ("Чужой код", "можно прислать существующий проект"),
            ("Без переписывания", "если текущая база пригодна"),
        ],
        "flow": ["Проблема", "Проверка", "Нужный участок", "Исправление", "Тест"],
    },
}

changed_routes = 0
for route, cfg in SERVICES.items():
    path = route_file(route)
    if not path.is_file():
        raise SystemExit(f"stage124-services: missing {route}")
    text = path.read_text(encoding="utf-8")
    hero_match = re.search(r'<section class="s48-hero".*?</section>', text, re.S)
    if not hero_match:
        raise SystemExit(f"stage124-services: hero missing {route}")
    hero = hero_match.group(0)
    original_hero = hero

    hero, n1 = re.subn(r'<span class="s48-kicker">.*?</span>', f'<span class="s48-kicker">{cfg["kicker"]}</span>', hero, count=1, flags=re.S)
    hero, n2 = re.subn(r'<h1 id="s48-title">.*?</h1>', f'<h1 id="s48-title">{cfg["h1"]}</h1>', hero, count=1, flags=re.S)
    hero, n3 = re.subn(r'<p class="s48-lead">.*?</p>', f'<p class="s48-lead">{cfg["lead"]}</p>', hero, count=1, flags=re.S)
    hero = hero.replace('>Когда подходит ↓</a>', '>Подходит ли вам ↓</a>', 1)
    hero = hero.replace('<strong>20 отзывов · 9/10</strong><span>публичная репутация на Freelance.ru</span>', '<strong>20 отзывов</strong><span>публично на Freelance.ru</span>', 1)

    facts_html = fact_block(cfg["facts"])
    hero, n4 = re.subn(
        r'<div class="s48-facts">.*?</div></div><div class="s48-system"',
        facts_html + '</div><div class="s48-system"',
        hero,
        count=1,
        flags=re.S,
    )

    hero = hero.replace('<span>СЦЕНАРИЙ</span><i></i><b>LIVE</b>', '<span>КАК ЭТО РАБОТАЕТ</span><i></i><b>СХЕМА</b>', 1)
    nodes = re.findall(r'(<div class="s48-node"><span>\d+</span><strong>)(.*?)(</strong></div>)', hero, re.S)
    if len(nodes) != 5:
        raise SystemExit(f"stage124-services: expected 5 flow nodes on {route}, got {len(nodes)}")
    flow_iter = iter(cfg["flow"])
    hero = re.sub(
        r'(<div class="s48-node"><span>\d+</span><strong>)(.*?)(</strong></div>)',
        lambda m: m.group(1) + next(flow_iter) + m.group(3),
        hero,
        count=5,
        flags=re.S,
    )

    if not all((n1, n2, n3, n4)):
        raise SystemExit(f"stage124-services: incomplete hero rewrite on {route}: {n1,n2,n3,n4}")
    if hero == original_hero:
        raise SystemExit(f"stage124-services: hero unchanged on {route}")
    text = text[:hero_match.start()] + hero + text[hero_match.end():]
    path.write_text(text, encoding="utf-8")
    changed_routes += 1

# The service hub already explains the choice through six visible cards. Convert
# Stage120's repeated SEO-oriented explainer into a small optional helper.
services_path = route_file('/services/')
services = services_path.read_text(encoding='utf-8')
section_match = re.search(r'<section class="s44-section" data-stage120="services-intent".*?</section>', services, re.S)
if not section_match:
    raise SystemExit('stage124-services: services-intent section missing')
section = section_match.group(0)
nav_match = re.search(r'<nav class="s101-more" aria-label="Популярные услуги">.*?</nav>', section, re.S)
if not nav_match:
    raise SystemExit('stage124-services: services-intent nav missing')
helper = (
    '<details class="s124-service-help" data-stage124="service-help">'
    '<summary>Не уверены, что выбрать?</summary>'
    '<div><p>Опишите, что должно работать в итоге. Формат и технологии можно определить после короткого разбора задачи.</p>'
    + nav_match.group(0) + '</div></details>'
)
services = services[:section_match.start()] + helper + services[section_match.end():]

SERVICE_HUB_COPY = {
    'Сайт, веб-сервис или MVP': 'Сайт или веб-сервис',
    'От лендинга и каталога до кабинета, внутренней системы и полноценного веб-продукта.': 'Сайт, каталог, личный кабинет или внутренний сервис — от структуры до рабочего запуска.',
    'Telegram-бот или Mini App': 'Telegram-бот или мини-приложение',
    'Заявки, платежи, подписки, CRM/API, базы данных и продуктовая логика.': 'Бот для заявок, оплат, уведомлений или внутренних задач.',
    'Пользовательские сценарии для смартфона: iOS/Swift и кроссплатформенная разработка.': 'Приложение под понятный пользовательский сценарий — от интерфейса до рабочей версии.',
    'Автоматизация процесса': 'Убрать ручную рутину',
    'n8n/Make, webhooks, формы, CRM, Telegram, таблицы и уведомления без ручного переноса данных.': 'Убрать повторяющиеся действия и ручной перенос данных между сервисами.',
    'API и связь систем': 'Связать несколько сервисов',
    'Обмен данными между сервисами, CRM, платежами, backend и внешними API.': 'Связать сайт, CRM, платежи, таблицы и другие сервисы между собой.',
    'Доработка чужого или незавершённого проекта': 'Продолжить или исправить готовый проект',
    'Одна правка, ошибка, форма, адаптив, интеграция, новый функционал, старый код или проект, который нужно довести до релиза.': 'Исправить конкретную проблему, продолжить чужой код или довести незавершённый проект до запуска.',
}
for old, new in SERVICE_HUB_COPY.items():
    services = services.replace(old, new)
services_path.write_text(services, encoding='utf-8')

# Case library: lead with outcomes; technical tags remain inside each case page.
cases_path = route_file('/cases/')
cases = cases_path.read_text(encoding='utf-8')
cases, c1 = re.subn(
    r'<h1 id="s50-title">.*?</h1>',
    '<h1 id="s50-title">Примеры реальных проектов. <em>Что было сделано и как это работает.</em></h1>',
    cases,
    count=1,
    flags=re.S,
)
cases = cases.replace(
    'В каждом кейсе — задача, интерфейс и ключевая логика. Этого достаточно, чтобы быстро понять тип и уровень работы.',
    'В каждом кейсе — задача, что было сделано и скриншоты результата. Технические детали оставлены внутри для тех, кому они нужны.',
    1,
)
CASE_LABELS = {
    'SEO · МОНИТОРИНГ': 'Поисковое продвижение',
    'AI · EXCEL': 'Работа с Excel',
    'TELEGRAM · ФИНАНСЫ': 'Бот для учёта финансов',
    'iOS · SWIFT': 'Мобильное приложение',
    'CRM · WORKFLOW': 'Управление заказами',
    'SEO · АУДИТ': 'Проверка сайта',
    'CRM · АВТОСАЛОН': 'Учёт заявок',
    'MOBILE · PRODUCT': 'Сервис такси',
    'B2B · WEB': 'Каталог для бизнеса',
}
for old, new in CASE_LABELS.items():
    cases = cases.replace(old, new)
if c1 != 1:
    raise SystemExit(f'stage124-services: cases H1 rewrite count={c1}')
cases_path.write_text(cases, encoding='utf-8')

print(f"stage124 human-first services: service_heroes={changed_routes}; services_hub=1; cases=1")
