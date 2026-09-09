#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
design_marker = 'data-stage98-design="true"'
shell_marker = 'data-stage98-shell="true"'
design_link = '<link href="/assets/stage98-design-system.css?v=20260909-1" rel="stylesheet" data-stage98-design="true"/>'
shell_link = '<link href="/assets/stage98-shell.css?v=20260909-3" rel="stylesheet" data-stage98-shell="true"/>'
design_css = root / 'assets/stage98-design-system.css'
shell_css = root / 'assets/stage98-shell.css'
if not design_css.exists():
    raise SystemExit('stage98: design stylesheet missing')
if not shell_css.exists():
    raise SystemExit('stage98: shell stylesheet missing')

required_css = (
    '--ds-accent:#c9ff4a;',
    '.portfolio-showcase__layout',
    '.portfolio-carousel__grid',
    '.s44-route-grid',
    '.stage95-service-core',
    '.case-library__grid',
)
design_text = design_css.read_text(encoding='utf-8')
for token in required_css:
    if token not in design_text:
        raise SystemExit('stage98: required design token/rule missing: ' + token)
shell_text = shell_css.read_text(encoding='utf-8')
for token in ('.header,.site-header,.intl-header', '.cta-box,.contact-card', '.footer,.foot,.site-footer', 'repeat(4,minmax(0,1fr))'):
    if token not in shell_text:
        raise SystemExit('stage98: required shell rule missing: ' + token)

project_copy = {
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

ru_body_copy = {
    'ALEXUYS · DIGITAL DEVELOPMENT': 'ALEXUYS · РАЗРАБОТКА',
    'REAL PROJECTS · PORTFOLIO': 'КЕЙСЫ · ПОРТФОЛИО',
    'DECISION GUIDES': 'РАЗБОРЫ',
    'ALEXANDR · DEVELOPER': 'АЛЕКСАНДР · РАЗРАБОТЧИК',
    '<span>GUIDE</span>': '<span>РАЗБОР</span>',
    '<small>Telegram · product case</small>': '<small>Telegram · кейс</small>',
    '<small>iOS · real UI</small>': '<small>iOS · интерфейс</small>',
    '<span>EXISTING PROJECT</span>': '<span>ДОРАБОТКА</span>',
    '<span>AUTOMATION</span>': '<span>АВТОМАТИЗАЦИЯ</span>',
    'Разрабатываю цифровые продукты с нуля и подключаюсь к уже существующим проектам. Веб-сервисы, мобильные приложения, боты, CRM, API-интеграции и автоматизация — напрямую с разработчиком, без передачи задачи между менеджерами.': 'Разрабатываю и дорабатываю сайты, веб-сервисы, приложения, Telegram-ботов, CRM и автоматизацию. Работаю напрямую: от сценария и интерфейса до запуска.',
    'Смотреть реальные проекты ↓': 'Смотреть проекты ↓',
    'Меньше обещаний. <em>Больше проверяемых вещей.</em>': 'Как строится работа. <em>Прямо и по этапам.</em>',
    'На странице должно быть понятно не только «что умею», но и как будет выглядеть работа после первого сообщения.': 'Сначала фиксируем рабочий результат, затем реализацию и способ проверки.',
    'Отзывы находятся не на этом сайте.': 'Отзывы и история работы — в публичном профиле.',
    'Публичный профиль Freelance.ru можно открыть до обращения: 20 отзывов, оценки 9/10 по профессионализму и коммуникации, 6 лет опыта в профиле. Сайт использует внешнюю репутацию как проверяемый источник, а не рисует собственный рейтинг.': 'На Freelance.ru — 20 публичных отзывов, оценки и история выполненных работ. Профиль можно проверить до обращения.',
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

featured_order = [
    'seo-control-center','sheetpilot-ai','fin-planner','swift-calendar',
    'freelance-os','siteaudit-studio','auto-crm','taxi-app','factory-catalog'
]

def replace_body_copy(html: str, replacements: dict[str, str]) -> str:
    m = re.search(r'<body\b[^>]*>', html, re.I)
    if not m:
        return html
    prefix, body = html[:m.end()], html[m.end():]
    for old, new in replacements.items():
        body = body.replace(old, new)
    return prefix + body


def grid_fragment(html: str, start_token: str, end_token: str) -> str:
    start = html.find(start_token)
    if start < 0:
        return ''
    content_start = start + len(start_token)
    end = html.find(end_token, content_start)
    return '' if end < 0 else html[content_start:end]


def card_slugs(fragment: str, class_prefix: str) -> list[str]:
    return re.findall(rf'<a class="{re.escape(class_prefix)}[^\"]*"[^>]*href="/cases/([^/]+)/"', fragment, re.S)


def reorder_anchor_cards(html: str, start_token: str, end_token: str, class_prefix: str) -> str:
    start = html.find(start_token)
    if start < 0:
        return html
    content_start = start + len(start_token)
    end = html.find(end_token, content_start)
    if end < 0:
        return html
    fragment = html[content_start:end]
    pat = re.compile(rf'<a class="{re.escape(class_prefix)}[^\"]*"[^>]*href="/cases/([^/]+)/"[^>]*>.*?</a>', re.S)
    cards = [(m.group(1), m.group(0)) for m in pat.finditer(fragment)]
    if len(cards) < 2:
        return html
    rank = {slug: i for i, slug in enumerate(featured_order)}
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
        html = replace_body_copy(html, project_copy)

    if not rel.startswith('en/'):
        html = replace_body_copy(html, ru_body_copy)

    if rel == 'index.html':
        home_seen = True
        html = html.replace('data-project-showcase data-page-size="3"', 'data-project-showcase data-page-size="4"')
        html = html.replace('Выбранные проекты. <em>Реальная работа.</em>', 'Выбранные проекты. <em>Реальные интерфейсы и логика.</em>')
        html = html.replace('CRM, автоматизация, web, mobile и Telegram. Коротко о задаче, интерфейсе и результате.', 'Несколько сильных работ вместо длинной витрины: задача, интерфейс, логика и то, что получилось в итоге.')
        html = html.replace('<strong>5</strong><span>подробных кейсов на сайте</span>', '<strong>9</strong><span>подробных кейсов на сайте</span>')
        html = reorder_anchor_cards(html, '<div class="portfolio-carousel__grid">', '</div></div></div><aside class="project-radar"', 'portfolio-card')

    if rel == 'cases/index.html':
        html = reorder_anchor_cards(html, '<div class="case-library__grid">', '</div><div class="case-library-empty"', 'case-library-card')

    if rel.startswith('en/'):
        html = re.sub(r'(<header\b.*?</header>)', lambda m: m.group(1).replace('Describe your project in Telegram ↗','Discuss a project ↗').replace('Contact in Telegram ↗','Discuss a project ↗'), html, count=1, flags=re.I|re.S)

    html = re.sub(r'\s*<link\b[^>]*data-stage98-design=["\']true["\'][^>]*/?>', '', html, flags=re.I)
    html = re.sub(r'\s*<link\b[^>]*data-stage98-shell=["\']true["\'][^>]*/?>', '', html, flags=re.I)
    html = html.replace('</head>', design_link + '\n' + shell_link + '\n</head>', 1)
    if html != original:
        path.write_text(html, encoding='utf-8')
        changed += 1

for path in sorted(root.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<main' not in html or '</head>' not in html:
        continue
    rel = str(path.relative_to(root)).replace('\\', '/')
    if html.count(design_marker) != 1 or html.count(shell_marker) != 1:
        errors.append(f'{rel}: stage98 design/shell missing or duplicated')
    head = html.split('</head>', 1)[0]
    if not head.rstrip().endswith(shell_link):
        errors.append(f'{rel}: stage98 shell is not the final stylesheet')

if not home_seen:
    errors.append('homepage not found')
else:
    home = (root / 'index.html').read_text(encoding='utf-8', errors='ignore')
    if 'data-project-showcase data-page-size="4"' not in home:
        errors.append('homepage showcase is not 4-up')
    if 'project-radar' not in home or 'portfolio-carousel' not in home:
        errors.append('homepage showcase structure missing')
    if 'LOCAL-FIRST' in home or 'INTERNAL PRODUCT' in home or 'FULLSTACK · AUTOMATION' in home:
        errors.append('developer-facing project jargon remains on homepage')
    frag = grid_fragment(home, '<div class="portfolio-carousel__grid">', '</div></div></div><aside class="project-radar"')
    slugs = card_slugs(frag, 'portfolio-card')
    if slugs[:4] != featured_order[:4]:
        errors.append(f'real-interface projects are not leading the homepage showcase: {slugs[:4]}')
    if 'ALEXUYS · DIGITAL DEVELOPMENT' in home or 'product case' in home or 'real UI' in home:
        errors.append('prototype-facing homepage copy remains')

if errors:
    raise SystemExit('stage98 design audit failed:\n' + '\n'.join(errors[:30]))

print(f'stage98 design system: {changed} pages patched; {checked} user-facing pages audited')
print('stage98: unified shell and copy; 4-up desktop projects; real-interface work first; prototype jargon removed')
