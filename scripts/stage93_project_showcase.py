#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
CSS_MARK = 'data-stage93-project-css="true"'
JS_MARK = 'data-stage93-project-js="true"'
CSS_LINK = '<link href="/assets/portfolio-showcase.css?v=20260909-1" rel="stylesheet" data-stage93-project-css="true"/>'
JS_LINK = '<script defer src="/assets/portfolio-showcase.js?v=20260909-2" data-stage93-project-js="true"></script>'

PROJECTS = [
    dict(slug='freelance-os', title='FreelanceOS', meta='CRM · LOCAL-FIRST', desc='CRM фрилансера: лиды, pipeline, follow-up, задачи, бюджеты и аналитика без регистрации.', cats='crm automation web', tags=['CRM','Kanban','Analytics'], accent='#c9ff4a', kind='poster', glyph='FO', badge='Featured'),
    dict(slug='siteaudit-studio', title='SiteAudit Studio', meta='SEO · NODE.JS · CRAWLER', desc='Live-аудит сайта: meta, robots, sitemap, links, accessibility и security с защищённым crawler.', cats='seo automation web', tags=['SEO','Crawler','Audit'], accent='#c9ff4a', kind='poster', glyph='82', badge='Live'),
    dict(slug='seo-control-center', title='SEO Control Center', meta='SEO · FULLSTACK · AUTOMATION', desc='Панель мониторинга: sitemap, технический аудит, индексация, поисковые метрики и история изменений.', cats='seo automation web', tags=['SEO','GSC','Automation'], accent='#8195ff', kind='image', image='/assets/cases/seo-control-center/seo-control-center-card-02.svg', width=1536, height=1024, badge='Platform'),
    dict(slug='sheetpilot-ai', title='SheetPilot AI', meta='AI · EXCEL · FULLSTACK', desc='Excel-ассистент: команда обычным языком, безопасный preview изменений и экспорт нового файла.', cats='ai automation web', tags=['AI','XLSX','Fullstack'], accent='#c9ff4a', kind='image', image='/assets/cases/sheetpilot-ai/sheetpilot-01.svg', width=1440, height=1080, badge='MVP'),
    dict(slug='fin-planner', title='Фин Планер', meta='TELEGRAM · FINANCE', desc='Telegram-продукт для бюджета: расходы, регулярные операции, цели, отчёты и сценарии внутри бота.', cats='telegram automation', tags=['Telegram','Finance','Reports'], accent='#4bbcff', kind='image', image='/assets/cases/fin-planner/fin-planner-card-02-720w.webp', width=720, height=900, badge='Telegram'),
    dict(slug='swift-calendar', title='Календарь на Swift', meta='iOS · SWIFT · PRODUCT UI', desc='Нативное iOS-приложение с календарными сценариями, событиями, состояниями и подпиской.', cats='mobile', tags=['iOS','Swift','Product UI'], accent='#9d7fff', kind='image', image='/assets/cases/swift-calendar/calendar-card-02-720w.webp', width=720, height=900, badge='iOS'),
    dict(slug='auto-crm', title='CRM автосалона', meta='CRM · INTERNAL PRODUCT', desc='Единый внутренний контур для заявок, статусов и рабочих данных сотрудников.', cats='crm automation web', tags=['CRM','Workflow','Internal'], accent='#85e7dc', kind='poster', glyph='CRM', badge='CRM'),
    dict(slug='taxi-app', title='Приложение такси', meta='MOBILE · EXISTING PRODUCT', desc='Мобильный пользовательский сценарий и работа с существующим продуктом сервиса поездок.', cats='mobile', tags=['Mobile','UX','Product'], accent='#ff967d', kind='poster', glyph='↗', badge='Mobile'),
    dict(slug='factory-catalog', title='Каталог завода', meta='WEB · B2B', desc='Корпоративный каталог продукции: структура данных, навигация по ассортименту и путь до заявки.', cats='web', tags=['B2B','Web','Catalog'], accent='#8195ff', kind='poster', glyph='B2B', badge='Web'),
]
HOME_SLUGS = ['freelance-os','siteaudit-studio','seo-control-center','sheetpilot-ai','fin-planner','swift-calendar','auto-crm','taxi-app']
FILTERS = [('all','Все'),('crm','CRM'),('seo','SEO'),('ai','AI'),('telegram','Telegram'),('automation','Automation'),('mobile','Mobile'),('web','Web')]


def poster(p: dict) -> str:
    return f'''<div class="portfolio-poster" aria-hidden="true"><div class="portfolio-poster__top"><span>{p['badge']}</span><span>CASE</span></div><div class="portfolio-poster__glyph">{p['glyph']}</div><div class="portfolio-poster__bars"><i></i><i></i><i></i></div></div>'''


def image_tag(p: dict) -> str:
    return (f'<img src="{p["image"]}" alt="Превью проекта {p["title"]}" '
            f'width="{p["width"]}" height="{p["height"]}" loading="lazy" decoding="async"/>')


def home_media(p: dict) -> str:
    if p['kind'] == 'image':
        return f'''<div class="portfolio-card__media">{image_tag(p)}<span class="portfolio-card__shade" aria-hidden="true"></span></div>'''
    return f'''<div class="portfolio-card__media">{poster(p)}</div>'''


def home_card(p: dict) -> str:
    extra = ' portfolio-card--poster' if p['kind'] == 'poster' else ''
    return f'''<a class="portfolio-card{extra}" href="/cases/{p['slug']}/" data-project-card data-categories="{p['cats']}" style="--card-accent:{p['accent']}">{home_media(p)}<div class="portfolio-card__body"><div class="portfolio-card__meta"><span>{p['meta']}</span><i aria-hidden="true"></i></div><h3>{p['title']}</h3><p>{p['desc']}</p><div class="portfolio-card__footer"><span>Открыть кейс</span><span aria-hidden="true">↗</span></div></div></a>'''


def case_card(p: dict) -> str:
    extra = ' case-library-card--poster' if p['kind'] == 'poster' else ''
    tags = ''.join(f'<span>{tag}</span>' for tag in p['tags'])
    search = f"{p['title']} {p['meta']} {p['desc']} {' '.join(p['tags'])}".replace('"','&quot;')
    visual = image_tag(p) if p['kind'] == 'image' else poster(p)
    return f'''<a class="case-library-card{extra}" href="/cases/{p['slug']}/" data-case-card data-categories="{p['cats']}" data-search="{search}" style="--card-accent:{p['accent']}"><div class="case-library-card__media">{visual}<span class="case-library-card__badge">{p['badge']}</span></div><div class="case-library-card__body"><div class="case-library-card__meta">{p['meta']}</div><h3>{p['title']}</h3><p>{p['desc']}</p><div class="case-library-card__tags">{tags}</div><div class="case-library-card__action"><span>Открыть кейс</span><i aria-hidden="true">↗</i></div></div></a>'''


def filter_buttons(attr: str, projects: list[dict]) -> str:
    counts = {key: 0 for key, _ in FILTERS}
    counts['all'] = len(projects)
    for p in projects:
        cats = p['cats'].split()
        for key, _ in FILTERS:
            if key != 'all' and key in cats:
                counts[key] += 1
    return ''.join(
        f'<button type="button" {attr}="{key}" aria-pressed="{str(key == "all").lower()}"><span>{label}</span><b>{counts[key]}</b></button>'
        for key, label in FILTERS if counts[key] > 0
    )


def build_home() -> str:
    items = [next(p for p in PROJECTS if p['slug'] == slug) for slug in HOME_SLUGS]
    cards = ''.join(home_card(p) for p in items)
    buttons = filter_buttons('data-project-filter', items)
    category_count = len([key for key, _ in FILTERS if key != 'all' and any(key in p['cats'].split() for p in items)])
    return f'''<section class="portfolio-showcase" id="work" aria-labelledby="projects-title" data-project-showcase data-page-size="4"><div class="container"><div class="portfolio-showcase__head"><div><div class="portfolio-showcase__kicker">02 / ПРОЕКТЫ</div><h2 id="projects-title">Выберите проект. <em>Оцените результат.</em></h2></div><p class="portfolio-showcase__intro">На главной только короткая витрина. Четыре проекта за раз, быстрый фильтр по типу задачи и переход в полноценный кейс без длинного чтения.</p></div><div class="portfolio-showcase__layout"><div class="portfolio-carousel"><div class="portfolio-carousel__top"><div class="portfolio-carousel__status"><strong>SHOWCASE</strong><span data-project-status aria-live="polite"></span></div><div class="portfolio-carousel__controls"><button type="button" data-project-prev aria-label="Предыдущие проекты">←</button><button type="button" data-project-next aria-label="Следующие проекты">→</button></div></div><div class="portfolio-carousel__viewport" data-project-viewport><div class="portfolio-carousel__grid">{cards}</div></div></div><aside class="project-radar" aria-label="Фильтр проектов"><div class="project-radar__head"><div class="project-radar__label"><small>Project radar</small><strong>Найти похожую задачу</strong></div><div class="project-radar__signal" aria-hidden="true"></div></div><div class="project-radar__stats"><div class="project-radar__stat"><span>Показано</span><strong data-project-match-count>{len(items)}</strong></div><div class="project-radar__stat"><span>Категорий</span><strong>{category_count}</strong></div></div><div class="project-radar__filters">{buttons}</div><a class="project-radar__link" href="/cases/">Открыть всю библиотеку ↗</a></aside></div><div class="portfolio-showcase__foot"><span>Листайте стрелками или свайпом. Фильтр меняет набор проектов без перезагрузки.</span><a href="/cases/">Все кейсы →</a></div></div></section>'''


def build_cases() -> str:
    buttons = filter_buttons('data-case-filter', PROJECTS)
    cards = ''.join(case_card(p) for p in PROJECTS)
    return f'''<section class="case-library" id="case-list" aria-labelledby="case-library-title" data-case-library><div class="container"><div class="case-library__head"><div><div class="case-library__kicker">PROJECT LIBRARY · {len(PROJECTS):02d} CASES</div><h2 id="case-library-title">Не листайте всё. <em>Выберите тип задачи.</em></h2></div><p class="case-library__lead">Полная витрина проектов с коротким описанием, визуальным превью и фильтрацией. Внутри каждого кейса - детали, интерфейс и контекст реализации.</p></div><div class="case-library__layout"><aside class="case-filter" aria-label="Фильтр библиотеки кейсов"><div class="case-filter__top"><span>Project radar</span><strong><span data-case-count>{len(PROJECTS)}</span> / {len(PROJECTS)}</strong></div><label class="case-filter__search"><input type="search" aria-label="Поиск по кейсам" placeholder="Название или задача" autocomplete="off" data-case-search/></label><div class="case-filter__list">{buttons}</div><button class="case-filter__reset" type="button" data-case-reset>Сбросить фильтр</button></aside><div class="case-library__content"><div class="case-library__toolbar"><span>Показываю <strong data-case-count>{len(PROJECTS)}</strong> проектов</span><span>Фильтр работает без перезагрузки</span></div><div class="case-library__grid">{cards}</div><div class="case-library-empty" data-case-empty>По этому фильтру проектов не нашлось. Попробуйте другую категорию или очистите поиск.</div></div></div></div></section>'''


def inject_assets(text: str) -> str:
    if CSS_MARK not in text:
        text = text.replace('</head>', CSS_LINK + '\n</head>', 1)
    if JS_MARK not in text:
        text = text.replace('</body>', JS_LINK + '\n</body>', 1)
    return text


def replace_section(text: str, section_id: str, replacement: str) -> str:
    pat = re.compile(rf'<section\b(?=[^>]*\bid=["\']{re.escape(section_id)}["\'])[^>]*>.*?</section>', re.I | re.S)
    if not pat.search(text):
        raise SystemExit(f'stage93: section #{section_id} not found')
    return pat.sub(replacement, text, count=1)


def remove_old_case_filter_assets(text: str) -> str:
    text = re.sub(r'\s*<link[^>]+data-stage91-filter-css=["\']true["\'][^>]*/?>', '', text, flags=re.I)
    text = re.sub(r'\s*<script[^>]+data-stage91-filter-js=["\']true["\'][^>]*></script>', '', text, flags=re.I)
    return text


def refresh_collection_schema(text: str) -> str:
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', text, re.I | re.S):
        try:
            data = json.loads(m.group(1))
        except Exception:
            continue
        if data.get('@type') != 'CollectionPage':
            continue
        data['mainEntity'] = {'@type': 'ItemList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i, 'url': f'https://alexgtup.github.io/cases/{p["slug"]}/', 'name': p['title']}
            for i, p in enumerate(PROJECTS, 1)
        ]}
        payload = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        return text[:m.start(1)] + payload + text[m.end(1):]
    return text


def duplicate_ids(text: str) -> list[str]:
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', text, re.I)
    return sorted({value for value in ids if ids.count(value) > 1})


for p in PROJECTS:
    target = root / 'cases' / p['slug'] / 'index.html'
    if not target.is_file():
        raise SystemExit(f'stage93: missing case target {target}')
    if p['kind'] == 'image':
        asset = root / p['image'].lstrip('/')
        if not asset.is_file():
            raise SystemExit(f'stage93: missing preview asset {asset}')

home = root / 'index.html'
home_text = inject_assets(home.read_text(encoding='utf-8'))
home_text = replace_section(home_text, 'work', build_home())
if home_text.count('data-project-showcase') != 1 or home_text.count('data-project-card') != len(HOME_SLUGS):
    raise SystemExit('stage93: homepage showcase guard failed')
if duplicate_ids(home_text):
    raise SystemExit(f'stage93: homepage duplicate ids: {duplicate_ids(home_text)}')
home.write_text(home_text, encoding='utf-8')

cases = root / 'cases/index.html'
cases_text = inject_assets(cases.read_text(encoding='utf-8'))
cases_text = remove_old_case_filter_assets(cases_text)
cases_text = replace_section(cases_text, 'case-list', build_cases())
cases_text = refresh_collection_schema(cases_text)
if cases_text.count('data-case-library') != 1 or cases_text.count('data-case-card') != len(PROJECTS):
    raise SystemExit('stage93: case library guard failed')
if duplicate_ids(cases_text):
    raise SystemExit(f'stage93: cases duplicate ids: {duplicate_ids(cases_text)}')
if len(re.findall(r'<img\b[^>]*\bwidth=["\']\d+["\'][^>]*\bheight=["\']\d+["\']', home_text, re.I)) < 4:
    raise SystemExit('stage93: homepage intrinsic image dimensions missing')
if len(re.findall(r'<img\b[^>]*\bwidth=["\']\d+["\'][^>]*\bheight=["\']\d+["\']', cases_text, re.I)) < 4:
    raise SystemExit('stage93: case-library intrinsic image dimensions missing')
cases.write_text(cases_text, encoding='utf-8')

print(f'stage93 project showcase: home={len(HOME_SLUGS)} cards / desktop-page=4 / mobile-page=1; cases={len(PROJECTS)} cards; filters={len(FILTERS)}')