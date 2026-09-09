#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
DESIGN_MARK = 'data-stage98-design="true"'
SHELL_MARK = 'data-stage98-shell="true"'
DESIGN_LINK = '<link href="/assets/stage98-design-system.css?v=20260909-1" rel="stylesheet" data-stage98-design="true"/>'
SHELL_LINK = '<link href="/assets/stage98-shell.css?v=20260910-1" rel="stylesheet" data-stage98-shell="true"/>'

design_css = root / 'assets/stage98-design-system.css'
shell_css = root / 'assets/stage98-shell.css'
if not design_css.exists() or not shell_css.exists():
    raise SystemExit('stage98: required stylesheet missing')

design_text = design_css.read_text(encoding='utf-8')
shell_text = shell_css.read_text(encoding='utf-8')
for token in ('--ds-accent:#c9ff4a;', '.portfolio-showcase__layout', '.portfolio-carousel__grid', '.stage95-service-core', '.case-library__grid'):
    if token not in design_text:
        raise SystemExit('stage98: required design rule missing: ' + token)
for token in ('.stage98-header', '.stage98-mobile-menu', '.s44-service-map', 'repeat(4,minmax(0,1fr))'):
    if token not in shell_text:
        raise SystemExit('stage98: required shell rule missing: ' + token)

PROJECT_COPY = {
    'CRM · LOCAL-FIRST': 'CRM · WORKFLOW',
    'SEO · NODE.JS · CRAWLER': 'SEO · АУДИТ',
    'SEO · FULLSTACK · AUTOMATION': 'SEO · МОНИТОРИНГ',
    'AI · EXCEL · FULLSTACK': 'AI · EXCEL',
    'TELEGRAM · FINANCE': 'TELEGRAM · ФИНАНСЫ',
    'iOS · SWIFT · PRODUCT UI': 'iOS · SWIFT',
    'CRM · INTERNAL PRODUCT': 'CRM · АВТОСАЛОН',
    'MOBILE · EXISTING PRODUCT': 'MOBILE · PRODUCT',
    'WEB · B2B': 'B2B · WEB',
    'Мобильный пользовательский сценарий и работа с существующим продуктом сервиса поездок.': 'Ключевой сценарий заказа поездки и доработка существующего мобильного продукта.',
    '<span>Automation</span>': '<span>Автоматизация</span>',
    '<span>Mobile</span>': '<span>Мобильные</span>',
    '>Featured<': '>Флагман<',
    '>Live<': '>Демо<',
    '>Platform<': '>Платформа<',
    '>CASE<': '>КЕЙС<',
}

RU_COPY = {
    'ALEXUYS · DIGITAL DEVELOPMENT': 'ALEXUYS · РАЗРАБОТКА',
    'REAL PROJECTS · PORTFOLIO': 'КЕЙСЫ · ПОРТФОЛИО',
    'DECISION GUIDES': 'РАЗБОРЫ',
    'ALEXANDR · DEVELOPER': 'АЛЕКСАНДР · РАЗРАБОТЧИК',
    '<span>GUIDE</span>': '<span>РАЗБОР</span>',
    '<small>Telegram · product case</small>': '<small>Telegram · кейс</small>',
    '<small>iOS · real UI</small>': '<small>iOS · интерфейс</small>',
    '<span>EXISTING PROJECT</span>': '<span>ДОРАБОТКА</span>',
    '<span>AUTOMATION</span>': '<span>АВТОМАТИЗАЦИЯ</span>',
    '04 · AUTOMATION': '04 · АВТОМАТИЗАЦИЯ',
    '05 · INTEGRATIONS': '05 · API / CRM',
    '06 · EXISTING PROJECT': '06 · ДОРАБОТКА',
    'Разрабатываю цифровые продукты с нуля и подключаюсь к уже существующим проектам. Веб-сервисы, мобильные приложения, боты, CRM, API-интеграции и автоматизация — напрямую с разработчиком, без передачи задачи между менеджерами.': 'Разрабатываю и дорабатываю сайты, веб-сервисы, приложения, Telegram-ботов, CRM и автоматизацию. Работаю напрямую: от сценария и интерфейса до запуска.',
    'Смотреть реальные проекты ↓': 'Смотреть проекты ↓',
    'Меньше обещаний. <em>Больше проверяемых вещей.</em>': 'Как строится работа. <em>Прямо и по этапам.</em>',
    'На странице должно быть понятно не только «что умею», но и как будет выглядеть работа после первого сообщения.': 'Сначала фиксируем рабочий результат, затем реализацию и способ проверки.',
    'Отзывы находятся не на этом сайте.': 'Отзывы и история работы — в публичном профиле.',
    'Публичный профиль Freelance.ru можно открыть до обращения: 20 отзывов, оценки 9/10 по профессионализму и коммуникации, 6 лет опыта в профиле. Сайт использует внешнюю репутацию как проверяемый источник, а не рисует собственный рейтинг.': 'На Freelance.ru есть публичные отзывы и история выполненных работ. Профиль можно проверить до обращения.',
    'Реальные проекты. <em>Без декоративных концептов.</em>': 'Проекты, которые <em>можно посмотреть.</em>',
    'Кейсы нужны не для длинного рассказа о технологиях. Здесь можно отдельно посмотреть интерфейс, рабочую задачу и тип логики, с которой уже приходилось работать.': 'В каждом кейсе — задача, интерфейс и ключевая логика. Этого достаточно, чтобы быстро понять тип и уровень работы.',
    'Меньше SEO-воды. <em>Больше решений.</em>': 'Разборы, которые помогают <em>выбрать следующий шаг.</em>',
    'Каждая страница должна помогать выбрать следующий шаг, а не просто повторять коммерческий запрос.': 'Коротко сравниваю варианты, ограничения и стоимость решения — без лишней теории.',
    'Обсудить задачу в Telegram ↗': 'Обсудить проект ↗',
    'Описать задачу в Telegram ↗': 'Обсудить проект ↗',
    'Написать в Telegram ↗': 'Обсудить проект ↗',
    'Написать @Alexuys ↗': 'Обсудить проект ↗',
    'Обсудить похожую задачу ↗': 'Обсудить проект ↗',
}

FEATURED = ['seo-control-center','sheetpilot-ai','fin-planner','swift-calendar','freelance-os','siteaudit-studio','auto-crm','taxi-app','factory-catalog']


def replace_body(html: str, replacements: dict[str, str]) -> str:
    m = re.search(r'<body\b[^>]*>', html, re.I)
    if not m:
        return html
    head, body = html[:m.end()], html[m.end():]
    for old, new in replacements.items():
        body = body.replace(old, new)
    return head + body


def normalize_home_proof(html: str) -> str:
    replacements = (
        (r'<a\b[^>]*href="https://freelance\.ru/gglalex"[^>]*>\s*<strong>Отзывы</strong>\s*<span>публично на Freelance\.ru</span>\s*</a>',
         '<a href="https://freelance.ru/gglalex" rel="me noopener noreferrer" target="_blank"><strong>Freelance.ru</strong><span>отзывы и история работ</span></a>'),
        (r'<a\b[^>]*href="https://freelance\.ru/gglalex"[^>]*>\s*<strong>Задания</strong>\s*<span>история выполненных работ</span>\s*</a>',
         '<a href="/cases/"><strong>Кейсы</strong><span>интерфейсы и рабочая логика</span></a>'),
        (r'<div>\s*<strong>2023</strong>\s*<span>профиль на площадке</span>\s*</div>',
         '<a href="/demos/"><strong>Демо</strong><span>проекты можно открыть</span></a>'),
        (r'<a\b[^>]*href="/cases/"[^>]*>\s*<strong>Кейсы</strong>\s*<span>проекты и рабочие продукты</span>\s*</a>',
         '<a href="/project-repair/"><strong>Доработка</strong><span>можно с существующим кодом</span></a>'),
    )
    for pattern, replacement in replacements:
        html = re.sub(pattern, replacement, html, count=1, flags=re.I | re.S)
    return html


def grid_fragment(html: str, start_token: str, end_token: str) -> str:
    start = html.find(start_token)
    if start < 0:
        return ''
    start += len(start_token)
    end = html.find(end_token, start)
    return '' if end < 0 else html[start:end]


def reorder_cards(html: str, start_token: str, end_token: str, cls: str) -> str:
    start = html.find(start_token)
    if start < 0:
        return html
    content_start = start + len(start_token)
    end = html.find(end_token, content_start)
    if end < 0:
        return html
    fragment = html[content_start:end]
    pattern = re.compile(rf'<a class="{re.escape(cls)}[^\"]*"[^>]*href="/cases/([^/]+)/"[^>]*>.*?</a>', re.S)
    cards = [(m.group(1), m.group(0)) for m in pattern.finditer(fragment)]
    if len(cards) < 2:
        return html
    rank = {slug: i for i, slug in enumerate(FEATURED)}
    cards.sort(key=lambda item: rank.get(item[0], 999))
    return html[:content_start] + ''.join(card for _, card in cards) + html[end:]


checked = changed = 0
errors = []
home_seen = False
for path in sorted(root.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<main' not in html or '</head>' not in html:
        continue
    checked += 1
    original = html
    rel = str(path.relative_to(root)).replace('\\', '/')

    if rel in {'index.html', 'cases/index.html'}:
        html = replace_body(html, PROJECT_COPY)
    if not rel.startswith('en/'):
        html = replace_body(html, RU_COPY)

    if rel == 'index.html':
        home_seen = True
        html = html.replace('data-project-showcase data-page-size="3"', 'data-project-showcase data-page-size="4"')
        html = html.replace('Выбранные проекты. <em>Реальная работа.</em>', 'Выбранные проекты. <em>Реальные интерфейсы и логика.</em>')
        html = html.replace('CRM, автоматизация, web, mobile и Telegram. Коротко о задаче, интерфейсе и результате.', 'Несколько сильных работ вместо длинной витрины: задача, интерфейс, логика и то, что получилось в итоге.')
        html = normalize_home_proof(html)
        html = html.replace('Не концепты ради картинки — интерфейсы из реальных проектов.', 'Интерфейсы из опубликованных кейсов.')
        html = reorder_cards(html, '<div class="portfolio-carousel__grid">', '</div></div></div><aside class="project-radar"', 'portfolio-card')

    if rel == 'cases/index.html':
        html = reorder_cards(html, '<div class="case-library__grid">', '</div><div class="case-library-empty"', 'case-library-card')

    if rel == 'services/index.html':
        html = re.sub(r'<section\b[^>]*id="service-demos"[^>]*>.*?</section>', '', html, count=1, flags=re.I | re.S)

    html = re.sub(r'\s*<link\b[^>]*data-stage98-design=["\']true["\'][^>]*/?>', '', html, flags=re.I)
    html = re.sub(r'\s*<link\b[^>]*data-stage98-shell=["\']true["\'][^>]*/?>', '', html, flags=re.I)
    html = html.replace('</head>', DESIGN_LINK + '\n' + SHELL_LINK + '\n</head>', 1)
    if html != original:
        path.write_text(html, encoding='utf-8')
        changed += 1

for path in sorted(root.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<main' not in html or '</head>' not in html:
        continue
    rel = str(path.relative_to(root)).replace('\\', '/')
    if html.count(DESIGN_MARK) != 1 or html.count(SHELL_MARK) != 1:
        errors.append(f'{rel}: stage98 design/shell missing or duplicated')
    if not html.split('</head>', 1)[0].rstrip().endswith(SHELL_LINK):
        errors.append(f'{rel}: stage98 shell is not final stylesheet')

if not home_seen:
    errors.append('homepage not found')
else:
    home = (root / 'index.html').read_text(encoding='utf-8', errors='ignore')
    if 'data-project-showcase data-page-size="4"' not in home:
        errors.append('homepage showcase is not 4-up')
    frag = grid_fragment(home, '<div class="portfolio-carousel__grid">', '</div></div></div><aside class="project-radar"')
    slugs = re.findall(r'<a class="portfolio-card[^\"]*"[^>]*href="/cases/([^/]+)/"', frag, re.S)
    if slugs[:4] != FEATURED[:4]:
        errors.append(f'real-interface projects are not leading homepage: {slugs[:4]}')
    for stale in ('<strong>2023</strong>', 'профиль на площадке', 'ALEXUYS · DIGITAL DEVELOPMENT', 'product case', 'real UI'):
        if stale in home:
            errors.append('stale homepage copy remains: ' + stale)
    for required in ('<strong>Freelance.ru</strong>', '<strong>Демо</strong>', '<strong>Доработка</strong>'):
        if required not in home:
            errors.append('homepage proof item missing: ' + required)

services = root / 'services' / 'index.html'
if services.exists() and 'id="service-demos"' in services.read_text(encoding='utf-8', errors='ignore'):
    errors.append('services duplicate demo promo remains')

if errors:
    raise SystemExit('stage98 design audit failed:\n' + '\n'.join(errors[:40]))

print(f'stage98 design system: changed={changed}; checked={checked}; robust proof strip; unified surfaces; compact services flow')
