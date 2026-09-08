#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
page = ROOT / "freelance-developer" / "index.html"
if not page.is_file():
    raise SystemExit(f"missing {page}")

html = page.read_text(encoding="utf-8")

# Keep search snippets durable: avoid counters that become stale every time the marketplace changes.
html = html.replace(
    'Частный фриланс-разработчик: Telegram-боты, доработка сайтов, n8n/Make, API и автоматизация. Публичный профиль Freelance.ru, 19 выполненных заданий, оценки 9/9, реальные кейсы.',
    'Частный фриланс-разработчик: Telegram-боты, доработка сайтов и веб-проектов, n8n/Make, API-интеграции, технический SEO и автоматизация. Публичный профиль Freelance.ru и реальные кейсы.'
)
html = html.replace(
    'Telegram-боты, автоматизация, API-интеграции и доработка существующих проектов. Без передачи задачи менеджеру: обсуждение, реализация и доработка идут напрямую с разработчиком.',
    'Telegram-боты, автоматизация, API-интеграции, доработка существующих проектов и технический SEO. Без передачи задачи менеджеру: обсуждение, реализация и доработка идут напрямую с разработчиком.'
)

old_proof = '<div class="proofbar"><a href="https://freelance.ru/gglalex" rel="noopener noreferrer" target="_blank"><strong>19</strong><span>выполненных заданий</span></a><a href="https://freelance.ru/gglalex" rel="noopener noreferrer" target="_blank"><strong>9 / 9</strong><span>профессионализм и коммуникация</span></a><div><strong>с 2023</strong><span>публичная история на площадке</span></div><a href="/cases/"><strong>5</strong><span>подробных кейсов на сайте</span></a></div>'
new_proof = '<div class="proofbar"><a href="https://freelance.ru/gglalex" rel="noopener noreferrer" target="_blank"><strong>Freelance.ru</strong><span>внешний профиль и отзывы</span></a><a href="https://freelance.ru/reviews/gglalex/" rel="noopener noreferrer" target="_blank"><strong>20+</strong><span>публичных отзывов и оценок</span></a><div><strong>с 2023</strong><span>публичная история на площадке</span></div><a href="/cases/"><strong>10+</strong><span>кейсов и рабочих продуктов</span></a></div>'
if old_proof in html:
    html = html.replace(old_proof, new_proof)
elif new_proof not in html:
    raise SystemExit("freelance proofbar marker changed; review Stage72")

# Five distinct entry offers: keep Telegram as an established offer and add four marketplace-ready scopes.
old_cards = '<div class="cards"><article class="card"><div class="price">ОТ 5 000 ₽</div><h3>Доработка проекта</h3><p>Локальная ошибка, чужой код, форма, адаптив, интеграция или незавершённый функционал.</p><a href="/project-repair/">Что входит →</a></article><article class="card"><div class="price">ОТ 15 000 ₽</div><h3>Telegram-бот</h3><p>Первый рабочий сценарий: заявки, анкета, уведомления, данные или интеграция.</p><a href="/telegram-bots/">Разработка бота →</a></article><article class="card"><div class="price">ОТ 15 000 ₽</div><h3>n8n / Make</h3><p>Webhook, API, CRM, Telegram и таблицы в одном автоматизированном процессе.</p><a href="/n8n-automation/">Автоматизация →</a></article></div>'
new_cards = '<div class="cards" data-freelance-offers="v2"><article class="card"><div class="price">ОТ 10 000 ₽</div><h3>Доработка проекта</h3><p>Одна законченная правка или связанный блок: ошибка, форма, API, каталог, кабинет или существующий функционал.</p><a href="/project-repair/">Доработка проекта →</a></article><article class="card"><div class="price">ОТ 15 000 ₽</div><h3>Telegram-бот</h3><p>Первый рабочий сценарий: заявки, анкета, уведомления, данные, CRM, API или оплаты.</p><a href="/telegram-bots/">Разработка бота →</a></article><article class="card"><div class="price">ОТ 15 000 ₽</div><h3>n8n / Make</h3><p>Один законченный workflow: webhook, CRM, Telegram, таблицы и внешние API в одном процессе.</p><a href="/n8n-automation/">Автоматизация →</a></article><article class="card"><div class="price">ОТ 15 000 ₽</div><h3>API / CRM интеграция</h3><p>Связка существующих систем через REST API и webhooks с проверкой данных и сценария от события до результата.</p><a href="/api-integrations/">Интеграции по API →</a></article><article class="card"><div class="price">ОТ 12 000 ₽</div><h3>Технический SEO-аудит</h3><p>Индексация, robots/sitemap, canonical, технические дубли, внутренние ссылки и приоритетный план исправлений.</p><a href="/cases/siteaudit-studio/">Посмотреть аудит →</a></article></div>'
if old_cards in html:
    html = html.replace(old_cards, new_cards)
elif 'data-freelance-offers="v2"' not in html:
    raise SystemExit("freelance offer cards marker changed; review Stage72")

html = html.replace(
    '.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:.72rem}',
    '.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:.72rem}'
)

old_schema = '{"@context":"https://schema.org","@type":"ItemList","name":"Основные услуги фриланс-разработчика","itemListElement":[{"@type":"ListItem","position":1,"url":"https://alexgtup.github.io/project-repair/","name":"Доработка существующего проекта"},{"@type":"ListItem","position":2,"url":"https://alexgtup.github.io/telegram-bots/","name":"Разработка Telegram-бота"},{"@type":"ListItem","position":3,"url":"https://alexgtup.github.io/n8n-automation/","name":"Автоматизация n8n / Make"}]}'
new_schema = '{"@context":"https://schema.org","@type":"ItemList","name":"Основные услуги фриланс-разработчика","itemListElement":[{"@type":"ListItem","position":1,"url":"https://alexgtup.github.io/project-repair/","name":"Доработка существующего проекта"},{"@type":"ListItem","position":2,"url":"https://alexgtup.github.io/telegram-bots/","name":"Разработка Telegram-бота"},{"@type":"ListItem","position":3,"url":"https://alexgtup.github.io/n8n-automation/","name":"Автоматизация n8n / Make"},{"@type":"ListItem","position":4,"url":"https://alexgtup.github.io/api-integrations/","name":"Интеграция API / CRM / Telegram"},{"@type":"ListItem","position":5,"url":"https://alexgtup.github.io/cases/siteaudit-studio/","name":"Технический SEO-аудит"}]}'
if old_schema in html:
    html = html.replace(old_schema, new_schema)
elif new_schema not in html:
    raise SystemExit("freelance ItemList marker changed; review Stage72")

required = [
    'data-freelance-offers="v2"',
    'href="/project-repair/"',
    'href="/telegram-bots/"',
    'href="/n8n-automation/"',
    'href="/api-integrations/"',
    'href="/cases/siteaudit-studio/"',
    'Технический SEO-аудит',
]
missing = [item for item in required if item not in html]
if missing:
    raise SystemExit("Stage72 missing targets: " + ", ".join(missing))

page.write_text(html, encoding="utf-8")
print("Stage72 freelance offer hub: OK")
