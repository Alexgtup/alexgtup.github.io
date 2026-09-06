#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote
import html as H
import json
import re
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
BASE = "https://alexgtup.github.io"
NEW_ROUTE = "/telegram-bot-repair/"
NEW_URL = BASE + NEW_ROUTE
LASTMOD = "2026-09-07"


def page(route: str) -> Path:
    return root / ("index.html" if route == "/" else route.strip("/") + "/index.html")


def replace_meta(text: str, key_type: str, key: str, content: str) -> str:
    esc = H.escape(content, quote=True)
    pat = re.compile(rf'<meta\b(?=[^>]*\b{key_type}=["\']{re.escape(key)}["\'])[^>]*>', re.I)
    repl = f'<meta {key_type}="{H.escape(key, quote=True)}" content="{esc}"/>'
    if pat.search(text):
        return pat.sub(repl, text, count=1)
    pos = text.lower().find('</head>')
    if pos < 0:
        raise SystemExit(f"stage60: </head> missing while setting {key_type}={key}")
    return text[:pos] + repl + text[pos:]


def set_head_and_h1(route: str, title: str, desc: str, h1_html: str | None = None, lead: str | None = None) -> None:
    p = page(route)
    if not p.is_file():
        raise SystemExit(f"stage60: missing target {route}")
    text = p.read_text(encoding="utf-8", errors="ignore")
    et = H.escape(title, quote=False)
    text, n = re.subn(r'<title>.*?</title>', f'<title>{et}</title>', text, count=1, flags=re.I|re.S)
    if n != 1:
        raise SystemExit(f"stage60: title missing on {route}")
    for kind, key, val in (
        ("name", "description", desc),
        ("property", "og:title", title),
        ("property", "og:description", desc),
        ("name", "twitter:title", title),
        ("name", "twitter:description", desc),
    ):
        text = replace_meta(text, kind, key, val)

    if h1_html is not None:
        def h1_repl(m: re.Match[str]) -> str:
            return f'<h1{m.group(1)}>{h1_html}</h1>'
        text, hn = re.subn(r'<h1\b([^>]*)>.*?</h1>', h1_repl, text, count=1, flags=re.I|re.S)
        if hn != 1:
            raise SystemExit(f"stage60: H1 missing on {route}")

    if lead is not None:
        lead_html = H.escape(lead)
        text, ln = re.subn(r'<p\s+class=["\']s48-lead["\']>.*?</p>', f'<p class="s48-lead">{lead_html}</p>', text, count=1, flags=re.I|re.S)
        if ln != 1:
            raise SystemExit(f"stage60: s48 lead missing on {route}")

    p.write_text(text, encoding="utf-8")


TARGETS = {
    "/": (
        "Разработчик на заказ — сайты, Telegram-боты и автоматизация | Alexuys",
        "Частный разработчик на заказ: сайты и веб-сервисы, Telegram-боты, доработка существующих проектов, n8n/Make и API-интеграции. Реальные кейсы и прямой контакт.",
        None,
        None,
    ),
    "/telegram-bots/": (
        "Разработка Telegram-ботов на заказ — Python, CRM, API | Alexuys",
        "Разработка Telegram-ботов на заказ на Python: aiogram 3, заявки, базы данных, CRM/API, оплаты, подписки и запуск на VPS. Реальный кейс и исходный код.",
        "Разработка Telegram-ботов на заказ. <em>Python, aiogram 3, CRM и API.</em>",
        "Новый Telegram-бот под рабочий сценарий: заявки, анкеты, база данных, оплаты, CRM/API и уведомления. Код и окружение передаются, а сложность определяется логикой, а не числом кнопок.",
    ),
    "/n8n-automation/": (
        "Настройка n8n и автоматизация на заказ — workflow, API, Telegram | Alexuys",
        "Настройка n8n и автоматизация на заказ: workflows, webhooks, API, Telegram, CRM, Google Sheets и self-hosted запуск. Сборка, исправление и развитие сценариев.",
        "Настройка n8n и автоматизация на заказ. <em>Workflow, API, Telegram и CRM.</em>",
        "Собираю и дорабатываю workflows в n8n: формы и Telegram, CRM и таблицы, HTTP/API, webhooks, ветки ошибок и уведомления. Можно начать с одного рабочего сценария.",
    ),
    "/project-repair/": (
        "Доработка сайта и существующего проекта — ошибки, функции, API | Alexuys",
        "Доработка существующего сайта или веб-проекта: исправление ошибок, чужой код, формы, адаптив, API, интеграции и новые функции без обязательного переписывания с нуля.",
        "Доработка сайта и существующего проекта. <em>Ошибки, функции, API и чужой код.</em>",
        "Подключаюсь к уже работающему или незавершённому проекту: сначала воспроизвожу проблему и проверяю текущую реализацию, затем меняю только тот контур, который действительно мешает результату.",
    ),
    "/api-integrations/": (
        "Интеграция по API на заказ — CRM, Telegram, webhooks | Alexuys",
        "Интеграция по API на заказ: сайт, CRM, Telegram, платежи и внешние сервисы. REST API, webhooks, авторизация, преобразование данных, обработка ошибок и повторные попытки.",
        "Интеграция по API на заказ. <em>Сайты, CRM, Telegram и webhooks.</em>",
        "Связываю существующие сервисы через REST API и webhooks: получение и передача данных, авторизация, преобразование форматов, обработка ошибок и проверяемый конечный результат.",
    ),
    "/python-development/": (
        "Python-разработчик на заказ — FastAPI, боты, API, автоматизация | Alexuys",
        "Python-разработчик на заказ: FastAPI, Telegram-боты, REST API, скрипты, интеграции и автоматизация. Доработка существующего Python-кода и запуск на сервере.",
        "Python-разработчик на заказ. <em>FastAPI, боты, API и автоматизация.</em>",
        "Python использую для серверной логики, Telegram-ботов, API, скриптов и обработки данных. Можно разработать новый модуль или продолжить существующий код без смены всего стека.",
    ),
    "/web-development/": (
        "Разработка сайтов и веб-сервисов на заказ — frontend, backend, API | Alexuys",
        "Разработка сайтов и веб-сервисов на заказ: каталоги, кабинеты, формы, backend, API-интеграции и адаптив. Новый проект или развитие существующего сайта.",
        "Разработка сайтов и веб-сервисов на заказ. <em>Frontend, backend и интеграции.</em>",
        "Разрабатываю сайты и веб-сервисы, где интерфейс связан с реальной логикой: формы и заявки, каталоги, кабинеты, API, данные и интеграции. Есть отдельный путь для доработки уже существующего проекта.",
    ),
    "/freelance-developer/": (
        "Фриланс-разработчик на заказ — сайты, боты, автоматизация | Alexuys",
        "Фриланс-разработчик на заказ: сайты, Telegram-боты, Python, API, автоматизация и доработка проектов. Публичный профиль Freelance.ru, реальные кейсы и прямой контакт.",
        "Фриланс-разработчик на заказ. <em>Сайты, боты, автоматизация и доработка.</em>",
        None,
    ),
}
for route, args in TARGETS.items():
    set_head_and_h1(route, *args)


source = page("/telegram-bots/")
if not source.is_file():
    raise SystemExit("stage60: telegram source page missing")
text = source.read_text(encoding="utf-8", errors="ignore")
text = re.sub(r'<script\s+type=["\']application/ld\+json["\']>.*?</script>', '', text, flags=re.I|re.S)
text = re.sub(r'<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=)[^>]*>', '', text, flags=re.I)
text = re.sub(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>', f'<link rel="canonical" href="{NEW_URL}"/>', text, count=1, flags=re.I)
text = replace_meta(text, "property", "og:url", NEW_URL)
text = re.sub(r'(<body\b[^>]*\bdata-page=["\'])[^"\']*(["\'])', rf'\1telegram-bot-repair\2', text, count=1, flags=re.I)

telegram = "https://t.me/Alexuys?text=" + quote("Здравствуйте. Нужно доработать существующего Telegram-бота.\n\nЧто есть сейчас: \nЧто нужно изменить: ")

NEW_MAIN = f'''<main id="main-content" data-stage60-service="telegram-bot-repair">
<section class="s48-hero" aria-labelledby="s60-title"><div class="container s48-hero__grid"><div><span class="s48-kicker">TELEGRAM BOT REPAIR · PYTHON</span><h1 id="s60-title">Доработка Telegram-бота на Python. <em>Чужой код не повод начинать с нуля.</em></h1><p class="s48-lead">Если бот уже написан на Python и его нужно исправить, закончить или расширить, сначала проверяю запуск, зависимости и текущую архитектуру. После этого можно добавить нужную функцию без автоматического переписывания всего проекта.</p><div class="s48-actions"><a class="s48-btn s48-btn--primary" href="{telegram}" target="_blank" rel="noopener noreferrer">Показать текущего бота ↗</a><a class="s48-btn" href="#tasks">Что можно доработать ↓</a></div><div class="s48-facts"><div><strong>Python</strong><span>aiogram 3 / async</span></div><div><strong>Чужой код</strong><span>можно продолжать</span></div><div><strong>VPS / Docker</strong><span>проверка запуска</span></div></div></div><div class="s48-system" data-nosnippet=""><div class="s48-system__top"><span>EXISTING BOT</span><i></i><b>REPAIR</b></div><div class="s48-flow"><div class="s48-node"><span>01</span><strong>Код</strong></div><div class="s48-node"><span>02</span><strong>Запуск</strong></div><div class="s48-node"><span>03</span><strong>Ошибка / функция</strong></div><div class="s48-node"><span>04</span><strong>Проверка</strong></div><div class="s48-node"><span>05</span><strong>Релиз</strong></div></div></div></div></section>
<section class="s48-section" id="tasks" aria-labelledby="s60-tasks"><div class="container"><div class="s48-head"><span class="s48-index">01 / ТИПОВЫЕ ДОРАБОТКИ</span><div><h2 id="s60-tasks">Не новый бот. <em>Нужен конкретный следующий результат.</em></h2><p>Частые задачи в существующих ботах — меню и inline-кнопки, FSM-сценарии, база данных, рассылки, админ-функции, API/CRM, платежи и исправление ошибок после обновления зависимостей.</p></div></div><div class="s48-fit-grid"><article><span>01</span><h3>Меню и сценарии</h3><p>Inline/Reply-кнопки, команды, состояния aiogram 3, повторный запуск, проверки и ветвление диалога.</p></article><article><span>02</span><h3>База и админка</h3><p>SQLite или PostgreSQL, хранение заявок, пользователи, статусы, рассылки и служебные команды.</p></article><article><span>03</span><h3>CRM, API и оплаты</h3><p>Webhooks, внешние REST API, передача заявок, уведомления, платежные статусы и интеграции с сайтом.</p></article></div></div></section>
<section class="s48-section s48-output" aria-labelledby="s60-check"><div class="container"><div class="s48-head"><span class="s48-index">02 / ПЕРЕД ПРАВКОЙ</span><div><h2 id="s60-check">Сначала воспроизводим проблему. <em>Потом меняем код.</em></h2></div></div><div class="s48-output-grid"><div class="s48-output-card"><span>ЧТО ПРОВЕРЯЮ</span><ul><li><span>01</span>Версию Python и зависимости</li><li><span>02</span>Точку запуска, конфиг и переменные окружения</li><li><span>03</span>Структуру handlers / routers / services</li><li><span>04</span>Логи, ошибки Telegram API и внешних сервисов</li></ul></div><div class="s48-output-card s48-output-card--contrast"><span>ЗАЧЕМ</span><blockquote>Одна и та же ошибка может быть в коде, окружении, API или данных. Правка без воспроизведения часто создаёт следующую проблему.</blockquote><a href="/guides/repair-vs-rewrite/">Когда дорабатывать, а когда переписывать →</a></div></div></div></section>
<section class="s48-section s48-proof" aria-labelledby="s60-proof"><div class="container"><div class="s48-head"><span class="s48-index">03 / ОПЫТ</span><div><h2 id="s60-proof">Telegram — не отдельная кнопка. <em>Есть backend, данные и интеграции.</em></h2></div></div><a class="s48-case" href="/cases/fin-planner/"><div class="s48-case__image"><img src="/assets/cases/fin-planner/fin-planner-card-02-720w.webp" width="720" height="900" loading="lazy" decoding="async" alt="Интерфейс Telegram-проекта Фин Планер"/></div><div class="s48-case__body"><span>TELEGRAM · REAL PROJECT</span><h3>Фин Планер</h3><p>Пример продукта внутри Telegram с состояниями, данными, регулярными операциями и пользовательской логикой.</p><b>Открыть кейс ↗</b></div></a></div></section>
<section class="s48-section" aria-labelledby="s60-boundary"><div class="container"><div class="s48-head"><span class="s48-index">04 / ГРАНИЦА</span><div><h2 id="s60-boundary">Переписывание — <em>не стартовое условие.</em></h2><p>Если текущая структура позволяет безопасно добавить функцию или исправить ошибку, сохраняется рабочая часть проекта. Полная замена оправдана только когда следующий этап действительно дороже и рискованнее ремонта.</p></div></div><div class="s48-related"><a href="/telegram-bots/"><strong>Нужен новый Telegram-бот</strong><span>Разработка с нуля →</span></a><a href="/project-repair/"><strong>Доработка другого проекта</strong><span>Сайты и web →</span></a><a href="/python-development/"><strong>Python-разработка</strong><span>Backend и API →</span></a></div></div></section>
<section class="s48-section" aria-labelledby="s60-faq"><div class="container"><div class="s48-head"><span class="s48-index">05 / FAQ</span><div><h2 id="s60-faq">Что обычно нужно <em>до начала доработки.</em></h2></div></div><div class="faq"><details><summary>Можно доработать бота после другого разработчика?</summary><p>Да. Нужны исходники или доступ к репозиторию и, если проблема связана с запуском, доступ к окружению или логи. Сначала проверяется текущее состояние, затем определяется минимальный объём изменения.</p></details><details><summary>Работаете с aiogram 3?</summary><p>Да. Можно продолжить существующий проект на aiogram 3, добавить routers/handlers, FSM, базу данных, фоновые задачи и интеграции.</p></details><details><summary>Можно добавить SQLite, PostgreSQL или рассылку?</summary><p>Да. Схема хранения выбирается по текущей архитектуре и объёму данных. Для небольшого бота SQLite может быть достаточен, для серверного проекта с параллельной логикой чаще подходит PostgreSQL.</p></details><details><summary>Когда всё-таки лучше переписать бота?</summary><p>Когда запуск нестабилен из-за базовой архитектуры, критичные зависимости устарели, изменения ломают соседние сценарии или цена каждого следующего изменения становится выше переноса рабочей логики.</p></details></div></div></section>
<section class="s48-contact" aria-labelledby="s60-contact"><div class="container"><div class="s48-contact__box"><div><span class="s48-kicker">ДОРАБОТКА</span><h2 id="s60-contact">Пришлите код или описание ошибки. <em>Начну с текущего состояния.</em></h2><p>Достаточно ссылки на репозиторий, скриншота ошибки, логов или короткого списка изменений. Большое ТЗ для первичной оценки не требуется.</p></div><div class="s48-contact__actions"><a class="s48-btn s48-btn--primary" href="{telegram}" target="_blank" rel="noopener noreferrer">Написать @Alexuys ↗</a><a class="s48-btn" href="/telegram-bots/">Новый бот с нуля</a></div></div></div></section>
</main>'''

text, mn = re.subn(r'<main\b[^>]*>.*?</main>', NEW_MAIN, text, count=1, flags=re.I|re.S)
if mn != 1:
    raise SystemExit("stage60: main replacement failed for telegram-bot-repair")

new_title = "Доработка Telegram-бота на Python / aiogram 3 | Alexuys"
new_desc = "Доработка существующего Telegram-бота: Python, aiogram 3, ошибки, меню, SQLite/PostgreSQL, рассылки, CRM/API, оплаты и запуск на VPS. Работа с чужим кодом."
text = re.sub(r'<title>.*?</title>', f'<title>{H.escape(new_title)}</title>', text, count=1, flags=re.I|re.S)
for kind, key, val in (
    ("name", "description", new_desc),
    ("property", "og:title", new_title),
    ("property", "og:description", new_desc),
    ("name", "twitter:title", new_title),
    ("name", "twitter:description", new_desc),
):
    text = replace_meta(text, kind, key, val)

schema = [
    {"@context":"https://schema.org","@type":"Service","name":"Доработка Telegram-бота на Python","serviceType":"Доработка и исправление существующих Telegram-ботов","provider":{"@id":BASE+"/#person"},"url":NEW_URL,"description":new_desc,"areaServed":"Worldwide"},
    {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":"Можно доработать Telegram-бота после другого разработчика?","acceptedAnswer":{"@type":"Answer","text":"Да. Сначала проверяются исходники, зависимости, запуск и текущая архитектура, затем определяется минимальный объём безопасного изменения."}},
        {"@type":"Question","name":"Можно доработать Telegram-бота на aiogram 3?","acceptedAnswer":{"@type":"Answer","text":"Да. Можно добавить routers и handlers, FSM, базу данных, рассылки, админ-функции, API и webhooks в существующий проект на aiogram 3."}},
        {"@type":"Question","name":"Нужно ли переписывать существующего бота с нуля?","acceptedAnswer":{"@type":"Answer","text":"Не обязательно. Переписывание имеет смысл только когда архитектура или зависимости делают каждое следующее изменение дороже и рискованнее переноса рабочей логики."}},
    ]},
    {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Главная","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":"Telegram-боты","item":BASE+"/telegram-bots/"},
        {"@type":"ListItem","position":3,"name":"Доработка Telegram-бота","item":NEW_URL},
    ]},
]
schema_html = ''.join('<script type="application/ld+json">'+json.dumps(x, ensure_ascii=False, separators=(",",":"))+'</script>' for x in schema)
pos = text.lower().find('</head>')
if pos < 0:
    raise SystemExit("stage60: repair page missing </head>")
text = text[:pos] + schema_html + text[pos:]

new_page = page(NEW_ROUTE)
new_page.parent.mkdir(parents=True, exist_ok=True)
new_page.write_text(text, encoding="utf-8")

ENTRY_BLOCK = f'''<section class="s48-section" data-stage60-repair-entry="true" aria-labelledby="s60-entry-title"><div class="container"><div class="s48-head"><span class="s48-index">УЖЕ ЕСТЬ БОТ</span><div><h2 id="s60-entry-title">Нужна не разработка с нуля, <em>а доработка существующего Telegram-бота?</em></h2><p>Для чужого Python-кода, aiogram 3, ошибок запуска, меню, базы данных, рассылок и API есть отдельная посадочная без смешивания с новым проектом.</p></div></div><div class="s48-related"><a href="{NEW_ROUTE}"><strong>Доработка Telegram-бота</strong><span>Python / aiogram 3 →</span></a></div></div></section>'''

for route in ("/telegram-bots/", "/project-repair/", "/python-development/"):
    p = page(route)
    html = p.read_text(encoding="utf-8", errors="ignore")
    if 'data-stage60-repair-entry="true"' in html:
        continue
    marker_m = re.search(r'<section\b[^>]*class=["\'][^"\']*s48-contact[^"\']*["\'][^>]*>', html, re.I)
    if not marker_m:
        raise SystemExit(f"stage60: contact marker missing on {route}")
    html = html[:marker_m.start()] + ENTRY_BLOCK + '\n' + html[marker_m.start():]
    p.write_text(html, encoding="utf-8")

ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
sitemap = root / 'sitemap.xml'
tree = ET.parse(sitemap)
rt = tree.getroot()
ns = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs = [(n.text or '').strip() for n in rt.findall('.//s:loc', ns)]
if NEW_URL not in locs:
    u = ET.SubElement(rt, '{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    ET.SubElement(u, '{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text = NEW_URL
    ET.SubElement(u, '{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text = LASTMOD
    tree.write(sitemap, encoding='utf-8', xml_declaration=True)

sitemap_txt = root / 'sitemap.txt'
if sitemap_txt.is_file():
    s = sitemap_txt.read_text(encoding='utf-8')
    if NEW_URL not in s:
        sitemap_txt.write_text(s.rstrip() + '\n' + NEW_URL + '\n', encoding='utf-8')

llms = root / 'llms.txt'
if llms.is_file():
    s = llms.read_text(encoding='utf-8')
    if NEW_URL not in s:
        llms.write_text(s.rstrip() + '\n- ' + NEW_URL + '\n', encoding='utf-8')

repair = new_page.read_text(encoding='utf-8', errors='ignore')
checks = {
    'canonical': f'rel="canonical" href="{NEW_URL}"' in repair,
    'h1': 'Доработка Telegram-бота на Python' in repair,
    'aiogram': 'aiogram 3' in repair,
    'single-main': len(re.findall(r'<main\b', repair, re.I)) == 1,
    'single-h1': len(re.findall(r'<h1\b', repair, re.I)) == 1,
    'inbound-telegram': NEW_ROUTE in page('/telegram-bots/').read_text(encoding='utf-8'),
    'inbound-repair': NEW_ROUTE in page('/project-repair/').read_text(encoding='utf-8'),
    'sitemap': NEW_URL in (root/'sitemap.xml').read_text(encoding='utf-8'),
}
failed = [k for k,v in checks.items() if not v]
if failed:
    raise SystemExit('stage60 guards failed: ' + ', '.join(failed))

print('stage60 SERP entrypoints:')
print('  commercial titles/H1 sharpened:', len(TARGETS))
print('  new narrow landing:', NEW_ROUTE)
print('  contextual inbound links: 3')
print('  sitemap/llms discovery: OK')
