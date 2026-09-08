#!/usr/bin/env python3
"""Final build pass: shared analytics, specific service evidence and project discovery."""
from pathlib import Path
from html import escape, unescape
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BASE = 'https://alexgtup.github.io'
DATE = '2026-09-08'

def text_only(value):
    return unescape(re.sub('<[^>]+>', '', value)).strip()

def link(url, label, primary=False, demo=None):
    external = url.startswith('https:')
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
    if demo:
        attrs += f' data-demo="{escape(demo)}"'
    return f'<a class="growth-link{" primary" if primary else ""}" href="{escape(url, quote=True)}"{attrs}>{escape(label)}</a>'

PROJECTS = {
    'sheetpilot': ('SheetPilot AI', '/cases/sheetpilot-ai/', 'Python · FastAPI · Excel',
        'Загрузка XLSX, команда обычным языком, предпросмотр изменений и экспорт нового файла. В кейсе показаны интерфейс, ограничения и устройство обработки.',
        '/assets/cases/sheetpilot-ai/'),
    'seo': ('SEO Control Center', '/cases/seo-control-center/', 'Next.js · PostgreSQL · n8n',
        'Панель мониторинга сайтов: sitemap, обход страниц, история индексации и поисковые метрики. В кейсе разобраны хранение данных, интеграции и события.', None),
}

def project_card(key):
    name, url, stack, desc, _ = PROJECTS[key]
    return f'<article class="growth-card"><span class="growth-label">{stack}</span><h3>{name}</h3><p>{desc}</p><div class="growth-actions">{link(url, "Посмотреть проект")}</div></article>'

def project_section(keys, title='Реализация на примере проектов', section_id='related-projects'):
    cards = ''.join(project_card(k) for k in keys)
    return f'<section class="growth-section" aria-labelledby="{section_id}"><div class="growth-shell"><span class="growth-label">ПРОЕКТЫ И ДЕМО</span><h2 id="{section_id}">{title}</h2><div class="growth-grid">{cards}</div><div class="growth-actions">{link("/demos/", "Демо и возможности продуктов")}</div></div></section>'

def head(title, description, route):
    url = BASE + route
    image = BASE + '/assets/og/alexuys-default.jpg'
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/><meta name="color-scheme" content="dark"/>
<title>{escape(title)}</title><meta name="description" content="{escape(description)}"/>
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
<link rel="canonical" href="{url}"/><link rel="icon" href="/favicon.ico"/>
<meta property="og:type" content="website"/><meta property="og:locale" content="ru_RU"/>
<meta property="og:site_name" content="Alexuys"/><meta property="og:title" content="{escape(title)}"/>
<meta property="og:description" content="{escape(description)}"/><meta property="og:url" content="{url}"/>
<meta property="og:image" content="{image}"/><meta property="og:image:width" content="1200"/><meta property="og:image:height" content="630"/>
<meta name="twitter:card" content="summary_large_image"/><meta name="twitter:image" content="{image}"/>
<style>body{{margin:0;background:#080b0f;color:#f4f6f8;font-family:system-ui,sans-serif}}*{{box-sizing:border-box}}a{{color:inherit}}.skip-link{{position:absolute;left:1rem;top:-6rem}}.skip-link:focus{{top:1rem;background:#111;padding:1rem;z-index:10001}}footer{{padding:2rem 0;border-top:1px solid #293039}}</style>
</head><body><a class="skip-link" href="#main-content">Перейти к содержанию</a>
<header><nav class="growth-shell growth-nav" aria-label="Основная навигация"><a href="/">alexuys</a><a href="/services/">Услуги</a><a href="/cases/">Кейсы</a><a href="/demos/" aria-current="page">Демо</a><a href="/guides/">Разборы</a><a href="/about/">Обо мне</a></nav></header>'''

demo_title = 'Демо веб-сервисов и примеры разработки | Alexuys'
demo_desc = 'SheetPilot AI для работы с Excel и SEO Control Center для мониторинга сайтов: демо, сценарии проверки, разбор реализации и заказ похожего сервиса.'
demo = head(demo_title, demo_desc, '/demos/') + '''
<main id="main-content"><section class="growth-hero"><div class="growth-shell"><span class="growth-label">ПРОДУКТЫ В РАБОТЕ</span>
<h1>Посмотрите, как работают мои проекты.</h1><p>Выберите продукт, изучите пользовательский сценарий и технический разбор. Похожий подход можно применить к вашему сайту, приложению или внутреннему сервису.</p></div></section>
<section class="growth-section" aria-labelledby="products"><div class="growth-shell"><h2 id="products">От таблиц до мониторинга сайтов</h2><div class="growth-grid">
<article class="growth-card"><span class="growth-label">EXCEL · PYTHON · AI</span><h3>SheetPilot AI</h3>
<p>Обработка Excel-файла по текстовому описанию. Изменения сначала видны в предпросмотре, результат скачивается отдельным файлом.</p>
<p><strong>Как проверить:</strong> загрузите небольшой тестовый XLSX, выберите лист, опишите одно изменение, сравните предпросмотр и экспортированный результат.</p>
<div class="growth-actions">''' + link('https://sheetpilot-ai-6omr.onrender.com', 'Открыть сервис', True, 'sheetpilot-ai') + link('/cases/sheetpilot-ai/', 'Разбор проекта') + '''</div>
<p>Если сервис не отвечает, откройте кейс: там доступны экраны, поддерживаемые операции и ограничения MVP.</p></article>
<article class="growth-card"><span class="growth-label">SEO · NEXT.JS · АВТОМАТИЗАЦИЯ</span><h3>SEO Control Center</h3>
<p>Мониторинг sitemap, технического состояния страниц, индексации и поисковых метрик нескольких сайтов в одном интерфейсе.</p>
<p><strong>Что посмотреть:</strong> структуру панели, историю событий, обмен данными с внешними API и хранение результатов в PostgreSQL.</p>
<div class="growth-actions">''' + link('https://seo-control-center-live-demo.onrender.com/', 'Открыть демо', True, 'seo-control-center') + link('/cases/seo-control-center/', 'Разбор проекта') + '''</div>
<p>Демо открывает интерфейс для ознакомления. Презентационные карточки в кейсе используют демонстрационные данные.</p></article>
</div></div></section><section class="growth-section" aria-labelledby="your-product"><div class="growth-shell"><h2 id="your-product">Нужен продукт для вашей задачи?</h2>
<p>Можно заказать отдельную функцию в существующем проекте или разработку сервиса с нуля. Пришлите описание задачи и ссылку на пример, который ближе всего по логике.</p><div class="growth-actions">''' + link('https://t.me/Alexuys', 'Обсудить задачу', True) + link('/web-development/', 'Веб-сервисы') + link('/api-integrations/', 'API-интеграции') + link('/n8n-automation/', 'Автоматизация') + '''</div></div></section></main>
<footer><nav class="growth-shell growth-nav" aria-label="Ссылки в подвале"><a href="/">Alexuys</a><a href="/services/">Услуги</a><a href="/cases/">Все кейсы</a><a href="/guides/">Разборы</a><a href="/about/">Обо мне</a><a href="https://freelance.ru/gglalex" target="_blank" rel="noopener noreferrer">Профиль и отзывы</a><a href="mailto:alexgtup@gmail.com">Почта</a><a href="/privacy/">Конфиденциальность</a></nav></footer></body></html>'''
dest = root / 'demos/index.html'
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(demo, encoding='utf-8')

SERVICE_PROJECTS = {
    '/ai-automation/': ['sheetpilot'], '/python-development/': ['sheetpilot'],
    '/n8n-automation/': ['seo'], '/backend-development/': ['sheetpilot', 'seo'],
    '/web-development/': ['sheetpilot', 'seo'], '/api-integrations/': ['seo'],
    '/mvp-development/': ['sheetpilot'], '/development/': ['sheetpilot', 'seo'],
}
FAQ = {
    '/web-development/': [
        ('Можно доработать сайт на WordPress или существующий веб-сервис?', 'Да. Пришлите адрес сайта и список изменений. Для оценки важны текущая платформа, доступность исходников и поведение, которое нужно получить. Небольшие изолированные доработки на сайте указаны от 5 000 руб.'),
        ('Что входит в разработку веб-сервиса?', 'Состав фиксируется по задаче: интерфейс, серверная логика, хранение данных, роли пользователей и интеграции. Например, в SheetPilot AI один полный сценарий включает загрузку Excel, обработку, предпросмотр и экспорт.'),
        ('Что передаётся после запуска?', 'Исходники согласованного этапа, настройки запуска и необходимые доступы. Зависимости от внешних сервисов и их тарифов обсуждаются при оценке.')],
    '/api-integrations/': [
        ('Какие данные нужны для оценки интеграции?', 'Названия двух систем, документация их API и пример данных: например, заявка с сайта, которую нужно создать в CRM. Секретные ключи не нужно публиковать в открытом описании задачи.'),
        ('Что произойдёт при ошибке внешнего API?', 'До реализации определяем, где сохранять ошибку, когда повторять запрос и как исключить повторное создание записи. Эти правила входят в согласованный сценарий обмена.'),
        ('Можно связать сайт, Telegram и таблицы?', 'Да, если сервисы предоставляют подходящий API или webhook. Реализация может быть отдельным backend-модулем или workflow n8n; выбор зависит от данных и правил обмена.')],
    '/n8n-automation/': [
        ('Можно продолжить уже собранный workflow?', 'Да. Для оценки нужны экспорт workflow без секретов, описание ожидаемого результата и пример ошибки или остановившегося выполнения.'),
        ('Сколько стоит настройка n8n?', 'На сайте указан ориентир от 15 000 руб. за первый законченный workflow. Итоговая оценка зависит от числа систем, авторизации, преобразования данных и обработки ошибок.'),
        ('Какие процессы можно автоматизировать?', 'Например, перенос заявки в CRM, уведомление в Telegram, периодический сбор данных из API или подготовку сводки. В SEO Control Center разобран процесс сбора и хранения данных о сайтах.')],
    '/project-repair/': [
        ('Обязательно переписывать проект после другого разработчика?', 'Нет. Сначала нужно воспроизвести проблему и проверить запуск. Если исправление локальное, согласуем его отдельно; если проблема в одном модуле, можно заменить только этот модуль.'),
        ('Какие задачи можно передать на доработку?', 'Ошибки форм и адаптива, новые функции, интеграции API, изменения в Telegram-боте или подготовку незавершённого веб-сервиса к запуску. Для доработки ботов есть отдельная страница.'),
        ('Как начать с небольшой задачи?', 'Пришлите ссылку на проект, шаги воспроизведения и ожидаемое поведение. Ориентир для одной изолированной задачи — от 5 000 руб.; окончательная оценка после просмотра.')],
}

replacements = {
    'Не выдаю смежный проект <em>за кейс именно этой услуги.</em>': 'Примеры реализации <em>и связанные материалы.</em>',
    'Не только описание услуги. <em>Есть связанный реальный проект.</em>': 'Посмотрите, <em>как это реализовано.</em>',
    'Сначала проверяем, <em>нужен ли вообще этот формат.</em>': 'С какими задачами <em>можно обратиться.</em>',
    'На выходе нужен <em>проверяемый рабочий этап.</em>': 'Что входит <em>в работу.</em>',
    'Цена как ориентир, <em>а не ограничение проекта.</em>': 'Стоимость <em>и объём работ.</em>',
    'Без длинного входа <em>до первого полезного результата.</em>': 'Как проходит <em>разработка.</em>',
    'Реальные проекты. <em>Без декоративных концептов.</em>': 'Проекты, <em>интерфейсы и реализация.</em>',
    'Показываю не стек. <em>Показываю, что было собрано.</em>': 'Проекты: <em>от задачи до реализации.</em>',
    'Меньше обещаний. <em>Больше проверяемых вещей.</em>': 'Как будет устроена <em>работа над проектом.</em>',
    'На странице должно быть понятно не только «что умею», но и как будет выглядеть работа после первого сообщения.': 'Обсуждаете задачу напрямую со мной, согласуете первый этап и получаете исходники после реализации.',
    'Сайт использует внешнюю репутацию как проверяемый источник, а не рисует собственный рейтинг.': 'В профиле доступны отзывы заказчиков и история работы на площадке.',
    'Без универсальных обещаний и результатов, которых нельзя проверить по материалам проекта.': 'Ниже — реализованные функции и их роль в пользовательском сценарии.',
    'Не превращаю кейс <em>в рекламную легенду.</em>': 'Что учесть <em>в похожем проекте.</em>',
    'На странице не придумываются проценты роста продаж, скорость обработки или экономия времени: таких публично подтверждённых цифр по проекту нет. Кейс показывает именно тип реализованной системы и рабочую логику.': 'Для новой CRM сначала определяем источники заявок, нужные статусы, действия сотрудников и внешние системы. Это помогает оценить объём до разработки интерфейса.',
    'Кейс полезен как подтверждение опыта с конкретным типом продукта и логики. Для новой задачи всё равно сначала проверяется её собственный контекст, ограничения и текущая реализация.': 'Можно начать с одного процесса и подключать остальные после проверки первого рабочего сценария.',
    'Карточки показывают продукт, <em>не рабочий стол.</em>': 'Интерфейс <em>и возможности сервиса.</em>',
    'Для портфолио подготовлены отдельные презентационные визуалы с интерфейсом и возможностями сервиса. В них нет вкладок браузера, панели macOS, личных файлов и другой информации с рабочего компьютера.': 'Карточки показывают разделы панели, сбор данных о страницах и историю SEO-событий.',
    'Operational dashboard для sitemap, crawler, индексации, поисковых метрик и истории SEO-событий.': 'Панель мониторинга сайтов: sitemap, технический аудит, индексация, поисковые метрики и история изменений.',
}

def cookie_markup(en):
    title, body, decline, allow, settings, privacy = (
        ('Analytics cookies', 'Yandex Metrica measures visits and link clicks only with your consent. Session recording is disabled.', 'Decline', 'Allow', 'Cookie settings', 'Privacy') if en else
        ('Аналитические cookie', 'Метрика учитывает посещения и переходы только с вашего согласия. Вебвизор отключён.', 'Отклонить', 'Разрешить', 'Настройки cookie', 'Конфиденциальность'))
    return f'''<aside class="growth-cookie" data-analytics-consent hidden aria-labelledby="analytics-title" data-nosnippet=""><strong id="analytics-title">{title}</strong><p>{body} <a href="{'/en' if en else ''}/privacy/">{privacy}</a></p><div class="growth-actions"><button class="growth-link" type="button" data-analytics-choice="declined">{decline}</button><button class="growth-link primary" type="button" data-analytics-choice="accepted">{allow}</button></div></aside><button class="growth-cookie-settings" data-analytics-settings hidden type="button" data-nosnippet="">{settings}</button>'''

def remove_legacy_script(match):
    tag, body = match.group(1), match.group(2)
    if 'mc.yandex.ru' not in body:
        return match.group(0)
    if '  const consentKey =' in body:
        return tag + body.split('  const consentKey =', 1)[0] + '})();\n</script>'
    if 'alexuys-analytics-consent-v1' in body:
        return ''
    raise SystemExit('Unexpected legacy analytics block; inspect before removing')

content_changed = {'/demos/'}
count = 0
for p in sorted(root.rglob('*.html')):
    if p.name.startswith(('google', 'yandex_')):
        continue
    rel = p.relative_to(root).as_posix()
    route = '/' if rel == 'index.html' else '/' + rel.removesuffix('index.html')
    en = route.startswith('/en/')
    t = p.read_text(encoding='utf-8')
    if 'data-growth-pass="62"' in t:
        continue
    before = t
    if not en:
        for old, new in replacements.items():
            t = t.replace(old, new)
        # Replace the generic proof section only where an actual related product now exists.
        if route in SERVICE_PROJECTS:
            def proof(m):
                if 'aria-labelledby="s48-proof-title"' in m.group(0):
                    return project_section(SERVICE_PROJECTS[route], section_id='s48-proof-title')
                return m.group(0) + project_section(SERVICE_PROJECTS[route])
            t, n = re.subn(r'<section\b[^>]*class="s48-section s48-proof"[^>]*>.*?</section>', proof, t, count=1, flags=re.S)
            if n != 1:
                raise SystemExit('Missing service proof section: ' + route)
            if route == '/n8n-automation/':
                t = t.replace('Демо и возможности продуктов</a>', 'Демо и возможности продуктов</a>' + link('/guides/n8n-vs-make/', 'n8n или Make') + link('/guides/n8n-vs-backend/', 'Когда нужен backend'), 1)
            t = re.sub(r'(<h2 id="s48-trust-title">.*?</h2>)<p>.*?</p>', r'\1<p>Отзывы заказчиков и история выполненных работ доступны в публичном профиле Freelance.ru.</p>', t, count=1, flags=re.S)
        if route in FAQ:
            items = ''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in FAQ[route])
            section = f'<section class="growth-section growth-faq" aria-labelledby="service-questions"><div class="growth-shell"><h2 id="service-questions">Перед началом работы</h2>{items}</div></section>'
            t = re.sub(r'(<section class="s48-contact")', lambda m: section + m.group(1), t, count=1)
        if route in ['/', '/services/', '/cases/', '/about/']:
            section = '<section class="growth-section" aria-labelledby="try-projects"><div class="growth-shell"><span class="growth-label">ПОСМОТРЕТЬ В ДЕЙСТВИИ</span><h2 id="try-projects">Демо и разборы продуктов</h2><p>Обработка Excel в SheetPilot AI и мониторинг сайтов в SEO Control Center: пользовательские сценарии, возможности и техническая реализация.</p><div class="growth-actions">' + link('/demos/', 'Перейти к демо и проектам', True) + '</div></div></section>'
            t = t.replace('</main>', section + '</main>', 1)
        if route.startswith('/cases/') and route != '/cases/':
            t = t.replace('</main>', '<section class="growth-section"><div class="growth-shell"><div class="growth-actions">' + link('/demos/', 'Демо и другие продукты') + link('https://freelance.ru/gglalex', 'Профиль и отзывы заказчиков') + '</div></div></section></main>', 1)
        # Demos is a real navigation destination, not a list of SEO keyword links.
        t = re.sub(r'(<footer\b.*?)(</nav>)', lambda m: m.group(1) + '<a href="/demos/">Демо</a>' + m.group(2), t, count=1, flags=re.S) if route != '/demos/' else t
    if t != before:
        content_changed.add(route)
    t = re.sub(r'(<script\b[^>]*>)(.*?)</script>', remove_legacy_script, t, flags=re.S)
    t = re.sub(r'<div\b[^>]*class="(?:cookie-consent|cookie)"[^>]*>.*?</div>\s*</div>', '', t, flags=re.S)
    t = re.sub(r'<button\b[^>]*class="cookie-settings"[^>]*>.*?</button>', '', t, flags=re.S)
    # Correct stale WebPage/Service identities left by cloned landing-page templates.
    title_match = re.search(r'<title>(.*?)</title>', t, re.S)
    title = text_only(title_match.group(1)) if title_match else ''
    def normalize_schema(m):
        data = json.loads(m.group(2))
        def fix(obj):
            if not isinstance(obj, dict): return
            kind = obj.get('@type')
            if kind in ('WebPage', 'Service'):
                obj['url'] = BASE + route
                obj['@id'] = BASE + route + ('#webpage' if kind == 'WebPage' else '#service')
                obj['name'] = title
                main = obj.get('mainEntity')
                if isinstance(main, dict) and str(main.get('@id', '')).endswith('#service'):
                    main['@id'] = BASE + route + '#service'
            for item in obj.get('@graph', []): fix(item)
        if isinstance(data, list):
            for item in data: fix(item)
        else: fix(data)
        return m.group(1) + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '</script>'
    t = re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)</script>', normalize_schema, t, flags=re.S)
    t = t.replace('</head>', '<link rel="stylesheet" href="/assets/growth.css" data-growth-pass="62"/></head>', 1)
    # Defer order ensures existing interaction helpers can use the consent state.
    marker = '<script defer src="/assets/analytics.js"></script>'
    js = re.search(r'<script\b[^>]*src="/assets/site-enhancements\.js[^>]*></script>', t)
    if js:
        t = t[:js.start()] + marker + t[js.start():]
    else:
        t = t.replace('</body>', marker + '</body>', 1)
    t = t.replace('</body>', cookie_markup(en) + '</body>', 1)
    for host, project in [('sheetpilot-ai-6omr.onrender.com', 'sheetpilot-ai'), ('seo-control-center-live-demo.onrender.com', 'seo-control-center')]:
        t = re.sub(r'<a\b(?=[^>]*href="https://' + re.escape(host) + r')([^>]*)>',
                   lambda m: m.group(0) if 'data-demo=' in m.group(1) else '<a data-demo="' + project + '"' + m.group(1) + '>', t)
    p.write_text(t, encoding='utf-8')
    count += 1

# Existing enhancement goals must stop after consent is withdrawn, too.
js = root / 'assets/site-enhancements.js'
t = js.read_text(encoding='utf-8')
t = t.replace("if (typeof window.ym !== 'function') return;", "if (window.alexuysAnalytics?.consent !== 'accepted' || typeof window.ym !== 'function') return;")
t = t.replace("if (typeof window.ym === 'function') {", "if (window.alexuysAnalytics?.consent === 'accepted' && typeof window.ym === 'function') {")
js.write_text(t, encoding='utf-8')

NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
ET.register_namespace('', NS[1:-1])
ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
sm = root / 'sitemap.xml'
tree = ET.parse(sm)
nodes = {n.findtext(NS + 'loc'): n for n in tree.getroot().findall(NS + 'url')}
if BASE + '/demos/' not in nodes:
    n = ET.SubElement(tree.getroot(), NS + 'url')
    ET.SubElement(n, NS + 'loc').text = BASE + '/demos/'
    nodes[BASE + '/demos/'] = n
for route in content_changed:
    n = nodes.get(BASE + route)
    if n is not None:
        lastmod = n.find(NS + 'lastmod')
        if lastmod is None: lastmod = ET.SubElement(n, NS + 'lastmod')
        lastmod.text = DATE
tree.write(sm, encoding='utf-8', xml_declaration=True)
for name in ('sitemap.txt', 'llms.txt'):
    f = root / name
    if f.exists() and BASE + '/demos/' not in f.read_text():
        with f.open('a') as out: out.write('\n' + BASE + '/demos/\n')

# Fingerprint final asset bytes after every mutation; no rerun of old page generators.
hashes = {name: hashlib.sha256((root / 'assets' / name).read_bytes()).hexdigest()[:12]
          for name in ('analytics.js', 'growth.css', 'site-enhancements.js')}
for p in root.rglob('*.html'):
    t = p.read_text(encoding='utf-8')
    for name, digest in hashes.items():
        t = re.sub(r'/assets/' + re.escape(name) + r'(?:\?[^"\s<>]*)?', '/assets/' + name + '?v=' + digest, t)
    p.write_text(t, encoding='utf-8')
print(f'stage62: {count} pages share analytics; services linked to products; demos published; final asset hashes applied')
