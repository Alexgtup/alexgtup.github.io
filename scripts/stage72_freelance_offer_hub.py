#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
page = ROOT / "freelance-developer" / "index.html"
if not page.is_file():
    raise SystemExit(f"missing {page}")

html = page.read_text(encoding="utf-8")

# Stage50 owns the final freelance page body; Stage53 owns durable trust stats.
# Patch only positioning/offers and preserve Stage53's non-stale reputation block.
old_desc = 'Фриланс-разработчик с публичным профилем Freelance.ru: сайты, приложения, Telegram, автоматизация, API и доработка проектов. Реальные кейсы и прямой контакт.'
new_desc = 'Фриланс-разработчик с публичным профилем Freelance.ru: сайты и веб-сервисы, Telegram, n8n/Make, API-интеграции, доработка проектов и технический SEO. Реальные кейсы и прямой контакт.'
html = html.replace(old_desc, new_desc)

old_hero = 'Если важно сначала проверить исполнителя, а потом писать — здесь собраны понятные точки доверия: реальные кейсы, публичный профиль Freelance.ru, ориентиры первого этапа и прямой контакт.'
new_hero = 'Если важно сначала проверить исполнителя, а потом писать — здесь собраны реальные кейсы, публичный профиль Freelance.ru и конкретные форматы первого этапа: Telegram, n8n, API-интеграции, доработка проекта и технический SEO.'
if old_hero in html:
    html = html.replace(old_hero, new_hero)
elif new_hero not in html:
    raise SystemExit('Stage72 hero marker changed')

# Stage53 must remain the source of truth for reputation facts.
stage53_stats = '<div class="s50-stats"><div><strong>Отзывы</strong><span>публично на Freelance.ru</span></div><div><strong>Задания</strong><span>история выполненных работ</span></div><div><strong>2023</strong><span>профиль на площадке</span></div></div>'
if stage53_stats not in html:
    raise SystemExit('Stage72 expected Stage53 trust stats are missing')

html = html.replace(
    '<a href="/cases/"><strong>Реальные кейсы</strong><span>5 проектов →</span></a>',
    '<a href="/cases/"><strong>Реальные кейсы</strong><span>кейсы и рабочие продукты →</span></a>'
)

old_step = '<section class="s50-section"><div class="container"><div class="s50-head"><span>02 / ПЕРВЫЙ ШАГ</span><div><h2>Не обязательно заказывать <em>большой проект сразу.</em></h2><p>Для существующего проекта можно начать с небольшой правки. Для нового — с одного законченного сценария. Полный объём оценивается после понимания задачи, поэтому стартовая цена не превращается в потолок бюджета.</p></div></div><div class="s50-principles"><article><strong>от 5 000 ₽</strong><h3>Небольшая доработка</h3><p>Ошибка или изолированная функция в существующем проекте.</p></article><article><strong>от 15 000 ₽</strong><h3>Bot / automation</h3><p>Первый рабочий сценарий Telegram или n8n/Make.</p></article><article><strong>по задаче</strong><h3>Полный продукт</h3><p>Web, mobile, CRM, backend или проект с несколькими интеграциями.</p></article></div></div></section>'
new_step = '<section class="s50-section" data-freelance-offers="v2"><div class="container"><div class="s50-head"><span>02 / ГОТОВЫЕ ФОРМАТЫ</span><div><h2>Можно начать <em>с конкретного законченного результата.</em></h2><p>Это не фиксированная цена на любой проект, а понятная граница первого этапа. Если задача шире, объём согласуется до расширения работ.</p></div></div><div class="s50-principles"><article><strong>от 10 000 ₽</strong><h3><a href="/project-repair/" data-offer="project_repair">Доработка проекта →</a></h3><p>Одна ограниченная задача или связанный блок правок в существующем сайте, backend или приложении.</p></article><article><strong>от 15 000 ₽</strong><h3><a href="/telegram-bots/" data-offer="telegram_bot">Telegram-бот →</a></h3><p>Первый рабочий сценарий: заявки, данные, CRM/API, уведомления или оплаты.</p></article><article><strong>от 15 000 ₽</strong><h3><a href="/n8n-automation/" data-offer="n8n">n8n / Make →</a></h3><p>Один законченный workflow с webhook, CRM, Telegram, таблицами или внешним API.</p></article><article><strong>от 15 000 ₽</strong><h3><a href="/api-integrations/" data-offer="api_integration">API / CRM интеграция →</a></h3><p>Связка существующих систем через REST API и webhooks с проверкой данных и результата.</p></article><article><strong>от 12 000 ₽</strong><h3><a href="/cases/siteaudit-studio/" data-offer="seo_audit">Технический SEO-аудит →</a></h3><p>Индексация, robots/sitemap, canonical, технические дубли, внутренние ссылки и план исправлений.</p></article></div></div></section>'
if old_step in html:
    html = html.replace(old_step, new_step)
elif 'data-freelance-offers="v2"' not in html:
    raise SystemExit('Stage72 offer section marker changed')

old_schema = '{"@context":"https://schema.org","@type":"ItemList","name":"Основные услуги фриланс-разработчика","itemListElement":[{"@type":"ListItem","position":1,"url":"https://alexgtup.github.io/project-repair/","name":"Доработка существующего проекта"},{"@type":"ListItem","position":2,"url":"https://alexgtup.github.io/telegram-bots/","name":"Разработка Telegram-бота"},{"@type":"ListItem","position":3,"url":"https://alexgtup.github.io/n8n-automation/","name":"Автоматизация n8n / Make"}]}'
new_schema = '{"@context":"https://schema.org","@type":"ItemList","name":"Основные услуги фриланс-разработчика","itemListElement":[{"@type":"ListItem","position":1,"url":"https://alexgtup.github.io/project-repair/","name":"Доработка существующего проекта"},{"@type":"ListItem","position":2,"url":"https://alexgtup.github.io/telegram-bots/","name":"Разработка Telegram-бота"},{"@type":"ListItem","position":3,"url":"https://alexgtup.github.io/n8n-automation/","name":"Автоматизация n8n / Make"},{"@type":"ListItem","position":4,"url":"https://alexgtup.github.io/api-integrations/","name":"Интеграция API / CRM / Telegram"},{"@type":"ListItem","position":5,"url":"https://alexgtup.github.io/cases/siteaudit-studio/","name":"Технический SEO-аудит"}]}'
if old_schema in html:
    html = html.replace(old_schema, new_schema)
elif new_schema not in html:
    raise SystemExit('Stage72 ItemList marker changed')

required = [
    'data-stage50-hub="freelance"',
    'data-freelance-offers="v2"',
    stage53_stats,
    'data-offer="project_repair"',
    'data-offer="telegram_bot"',
    'data-offer="n8n"',
    'data-offer="api_integration"',
    'data-offer="seo_audit"',
    'href="/project-repair/"',
    'href="/telegram-bots/"',
    'href="/n8n-automation/"',
    'href="/api-integrations/"',
    'href="/cases/siteaudit-studio/"',
    'Технический SEO-аудит',
]
missing = [item for item in required if item not in html]
if missing:
    raise SystemExit('Stage72 missing targets: ' + ', '.join(missing))

page.write_text(html, encoding="utf-8")
print('Stage72 freelance offer hub: OK')
