#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html, json, re, sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BASE = 'https://alexgtup.github.io'
TODAY = '2026-09-18'
NEW_SLUG = 'marketplace-integration'
NEW_URL = f'{BASE}/{NEW_SLUG}/'


def read(slug: str) -> tuple[Path, str]:
    p = ROOT / slug / 'index.html'
    if not p.is_file():
        raise SystemExit(f'stage195: missing {slug}')
    return p, p.read_text(encoding='utf-8')


def set_meta(s: str, title: str, desc: str) -> str:
    s = re.sub(r'<title\b[^>]*>.*?</title>', f'<title>{html.escape(title)}</title>', s, count=1, flags=re.I | re.S)
    values = [
        ('name', 'description', desc),
        ('property', 'og:title', title),
        ('property', 'og:description', desc),
        ('name', 'twitter:title', title),
        ('name', 'twitter:description', desc),
    ]
    for attr, key, value in values:
        pat = rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
        repl = f'<meta {attr}="{key}" content="{html.escape(value, quote=True)}"/>'
        s = re.sub(pat, repl, s, count=1, flags=re.I) if re.search(pat, s, re.I) else s.replace('</head>', repl + '</head>', 1)
    return s


def set_h1(s: str, value: str, slug: str) -> str:
    s, n = re.subn(r'<h1\b([^>]*)>.*?</h1>', lambda m: f'<h1{m.group(1)}>{value}</h1>', s, count=1, flags=re.I | re.S)
    if n != 1:
        raise SystemExit(f'stage195: h1 missing {slug}')
    return s


def fit_h1(s: str, slug: str, marker_prefix: str = 'stage195') -> str:
    marker = f'{marker_prefix}-hero-fit-{slug}'
    if marker in s:
        return s
    selector = f'html body[data-page="{slug}"] main.p129-service .p129-svc-hero .p129-svc-copy h1'
    style = (
        f'<style id="{marker}">'
        f'@media(min-width:901px){{{selector}{{font-size:78px!important;line-height:.91!important;letter-spacing:-.058em!important}}}}'
        f'@media(min-width:901px) and (max-width:1199px){{{selector}{{font-size:58px!important;line-height:.92!important;letter-spacing:-.055em!important}}}}'
        '</style>'
    )
    return s.replace('</head>', style + '</head>', 1)


def sync_page_service_schema(s: str, title: str, desc: str, url: str | None = None) -> str:
    name = re.sub(r'\s*\|\s*Alexuys\s*$', '', title).strip()
    url = url or ''

    def repl(m: re.Match[str]) -> str:
        raw = m.group(2)
        try:
            obj = json.loads(raw)
        except Exception:
            return m.group(0)
        typ = obj.get('@type')
        if typ in ('WebPage', 'Service'):
            obj['name'] = name
            obj['description'] = desc
            if url:
                obj['url'] = url
                if typ == 'Service':
                    obj['@id'] = url + '#service'
            return m.group(1) + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + m.group(3)
        return m.group(0)

    return re.sub(
        r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
        repl,
        s,
        flags=re.I | re.S,
    )


def add_stage174_faq(s: str, slug: str, items: list[tuple[str, str]]) -> str:
    marker = f'data-stage195-faq="{slug}"'
    if marker not in s:
        m = re.search(r'(<div class="stage174-faq__grid">)(.*?)(</div></div></section>)', s, re.I | re.S)
        if not m:
            raise SystemExit(f'stage195: stage174 FAQ missing {slug}')
        extra = ''.join(f'<details {marker}><summary>{q}</summary><p>{a}</p></details>' for q, a in items)
        s = s[:m.start()] + m.group(1) + m.group(2) + extra + m.group(3) + s[m.end():]
    sm = re.search(r'<script id="stage174-faq-schema" type="application/ld\+json">(.*?)</script>', s, re.I | re.S)
    if not sm:
        # fallback to any FAQPage script
        for candidate in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', s, re.I | re.S):
            if '"FAQPage"' in candidate.group(1):
                sm = candidate
                break
    if not sm:
        raise SystemExit(f'stage195: FAQ schema missing {slug}')
    obj = json.loads(sm.group(1))
    names = {x.get('name') for x in obj.get('mainEntity', [])}
    for q, a in items:
        if q not in names:
            obj.setdefault('mainEntity', []).append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}})
    blob = json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
    return s[:sm.start(1)] + blob + s[sm.end(1):]


def add_stage172_faq(s: str, slug: str, items: list[tuple[str, str]]) -> str:
    marker = f'data-stage195-faq="{slug}"'
    if marker not in s:
        m = re.search(r'(<section class="secondary-demand"[^>]*data-stage172-faq="true".*?<div class="secondary-demand__grid">)(.*?)(</div></div></section>)', s, re.I | re.S)
        if not m:
            raise SystemExit(f'stage195: stage172 FAQ missing {slug}')
        extra = ''.join(f'<article {marker} class="secondary-demand__card"><h3>{q}</h3><p>{a}</p></article>' for q, a in items)
        s = s[:m.start()] + m.group(1) + m.group(2) + extra + m.group(3) + s[m.end():]
    sm = None
    for candidate in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', s, re.I | re.S):
        if '"FAQPage"' in candidate.group(1):
            sm = candidate
            break
    if not sm:
        raise SystemExit(f'stage195: FAQ schema missing {slug}')
    obj = json.loads(sm.group(1))
    names = {x.get('name') for x in obj.get('mainEntity', [])}
    for q, a in items:
        if q not in names:
            obj.setdefault('mainEntity', []).append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}})
    blob = json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
    return s[:sm.start(1)] + blob + s[sm.end(1):]


def update_task_section(s: str, slug: str, h2: str, intro: str) -> str:
    pat = r'(<section class="secondary-demand"[^>]*data-stage172-tasks="true".*?<div class="secondary-demand__head">.*?<div><h2>)(.*?)(</h2><p class="secondary-demand__intro">)(.*?)(</p>)'
    m = re.search(pat, s, re.I | re.S)
    if not m:
        raise SystemExit(f'stage195: task section missing {slug}')
    return s[:m.start()] + m.group(1) + h2 + m.group(3) + intro + m.group(5) + s[m.end():]


def append_task_card(s: str, slug: str, marker: str, title: str, text: str) -> str:
    if marker in s:
        return s
    m = re.search(r'(<section class="secondary-demand"[^>]*data-stage172-tasks="true".*?<div class="secondary-demand__grid">)(.*?)(</div></div></section>)', s, re.I | re.S)
    if not m:
        raise SystemExit(f'stage195: task grid missing {slug}')
    extra = f'<article class="secondary-demand__card" {marker}><h3>{title}</h3><p>{text}</p></article>'
    return s[:m.start()] + m.group(1) + m.group(2) + extra + m.group(3) + s[m.end():]


def update_lastmods(routes: list[str]) -> None:
    for name in ('sitemap.xml', 'sitemap-google.xml'):
        p = ROOT / name
        if not p.exists():
            continue
        text = p.read_text(encoding='utf-8')
        for route in routes:
            url = BASE + route
            text = re.sub(r'(<loc>' + re.escape(url) + r'</loc><lastmod>)[^<]+', rf'\g<1>{TODAY}', text, count=1)
        p.write_text(text, encoding='utf-8')


# -----------------------------------------------------------------------------
# 1) New, distinct intent: marketplace integrations.
# -----------------------------------------------------------------------------
source_path, source = read('1c-integration')
new_dir = ROOT / NEW_SLUG
new_dir.mkdir(parents=True, exist_ok=True)
new_page = new_dir / 'index.html'

MP_TITLE = 'Интеграция с маркетплейсами - 1С, Ozon, Wildberries | Alexuys'
MP_DESC = 'Интеграция с маркетплейсами: 1С, Ozon, Wildberries, Яндекс Маркет — товары, цены, остатки, заказы и статусы через API. Синхронизация, логи и обработка ошибок.'
MP_NAME = 'Интеграция с маркетплейсами - 1С, Ozon, Wildberries'
mp_faq = [
    ('Можно интегрировать 1С с Ozon, Wildberries и Яндекс Маркет?', 'Да, если у нужной площадки и конфигурации 1С есть поддерживаемый способ обмена. Сначала определяется, какие данные являются источником в 1С, а какие приходят с маркетплейса.'),
    ('Какие данные можно синхронизировать с маркетплейсами?', 'Обычно это товары и артикулы, цены, остатки, заказы, статусы, склады и служебные идентификаторы. Конкретный набор зависит от API площадки и бизнес-процесса.'),
    ('Можно начать интеграцию с одного маркетплейса?', 'Да. Это удобный первый этап: настроить один устойчивый поток данных, проверить идентификаторы и обработку ошибок, а затем подключать следующую площадку.'),
    ('Как избежать дублей заказов и повторной обработки?', 'Используются стабильные идентификаторы заказа, идемпотентная обработка событий, журнал синхронизации и явные правила повторного запуска после ошибки.'),
]

main = '''<main id="main-content" class="p129-service" data-stage129-service="true" data-stage195="marketplace-integration">
<section class="p129-svc-hero p155-service-hero" data-stage155-service-scene="true"><div class="p155-service-band"><div class="p129-svc-copy"><p class="p129-kicker"><i></i>MARKETPLACE INTEGRATION</p><h1>Интеграция с маркетплейсами. <em>1С, Ozon, Wildberries и Яндекс Маркет.</em></h1><p class="p129-lead">Связать каталог, цены, остатки, заказы и статусы так, чтобы данные не переносились вручную между учётной системой и площадками. Обмен строится вокруг API, стабильных идентификаторов, логов и понятного поведения при ошибке.</p><div class="p129-svc-actions"><a class="p129-btn" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Обсудить задачу ↗</a><a class="p129-textlink" href="#result">Что получится ↓</a></div></div></div><div class="p155-service-preview"><aside class="p129-svc-board"><span class="p129-svc-no">32</span><h2>Фокус на результате.</h2><ul><li>Каталог синхронизируется</li><li>Заказы не копируются вручную</li><li>Ошибки видны и повторяются</li></ul></aside></div></section>
<section class="p129-outcomes wow-reveal" id="result"><div class="p129-shell"><div class="p129-section-head"><p class="p129-kicker">RESULT / 32</p><h2>Не набор API-запросов. <span>Рабочий обмен между системами.</span></h2></div><div class="p129-outcome-list"><article class="p129-outcome"><span>01</span><h3>Единый каталог</h3><p>Товары, артикулы, цены и остатки передаются по согласованным правилам, без ручного копирования между кабинетами.</p></article><article class="p129-outcome"><span>02</span><h3>Заказы и статусы</h3><p>Новые заказы попадают в рабочую систему, а нужные изменения статуса возвращаются в интеграционный контур.</p></article><article class="p129-outcome"><span>03</span><h3>Контроль обмена</h3><p>Ошибки и ограничения API фиксируются, повторная обработка не создаёт дублей, а проблемный объект можно найти по логу.</p></article></div></div></section>
<section class="s175-depth" data-stage175-depth="true"><div class="s175-shell"><div class="s175-head"><span class="s175-k">SCOPE / ESTIMATE</span><div><h2>Что входит в рабочую версию.</h2><p>Интеграция с маркетплейсами оценивается по количеству площадок, сущностей, направлений обмена и правилам обработки данных. Начать можно с одного законченного потока и одной площадки.</p></div></div><div class="s175-grid"><article class="s175-card"><small>FIRST VERSION</small><h3>Базовый контур</h3><ul><li>Авторизация и проверка API</li><li>Сопоставление товаров и идентификаторов</li><li>Цены и остатки</li><li>Заказы, статусы и журнал ошибок</li></ul></article><article class="s175-card"><small>WHAT CHANGES SCOPE</small><h3>Что меняет объём</h3><ul><li>Количество маркетплейсов и кабинетов</li><li>Связка с 1С, CRM или своей системой</li><li>Склады, варианты цены и большой каталог</li><li>Лимиты API и частота синхронизации</li></ul></article></div><div class="s175-brief"><p><strong>Для оценки не нужен большой документ.</strong> Достаточно назвать площадки, текущий источник товаров и заказов и показать, какие данные сейчас приходится переносить вручную.</p><a href="/guides/api-integration-checklist/">Чек-лист перед интеграцией ↗</a></div></div></section>
<section class="secondary-demand" data-stage195-marketplace-tasks="true"><div class="secondary-demand__shell"><div class="secondary-demand__head"><p class="secondary-demand__eyebrow">MARKETPLACES / API</p><div><h2>Интеграция с маркетплейсами: какие процессы связываются.</h2><p class="secondary-demand__intro">Обычно задача состоит не в одном запросе к API, а в устойчивой синхронизации каталога, остатков и заказов между площадкой и системой, где команда реально работает.</p></div></div><div class="secondary-demand__grid"><article class="secondary-demand__card"><h3>1С ↔ маркетплейсы</h3><p>Номенклатура, цены, остатки, заказы и статусы между учётной системой и площадками.</p></article><article class="secondary-demand__card"><h3>Ozon / Wildberries / Яндекс Маркет</h3><p>Работа с доступными API конкретной площадки, кабинетами продавца и служебными идентификаторами.</p></article><article class="secondary-demand__card"><h3>Остатки и цены</h3><p>Обновление по складам и товарам с контролем ошибок, лимитов и устаревших данных.</p></article><article class="secondary-demand__card"><h3>Заказы и статусы</h3><p>Передача заказа в 1С, CRM или свой backend и возврат нужных состояний в рабочий процесс.</p></article></div></div></section>
<section class="p129-related wow-reveal"><div class="p129-shell"><div class="p129-section-head"><p class="p129-kicker">EXPLORE</p><h2>Связанные направления. <span>Если часть контура уже существует.</span></h2></div><div class="p129-related-grid wow-reveal"><a href="/1c-integration/"><span>Следующий шаг</span><strong>Интеграция 1С</strong><b>↗</b></a><a href="/api-integrations/"><span>Следующий шаг</span><strong>API-интеграции</strong><b>↗</b></a><a href="/ecommerce-development/"><span>Следующий шаг</span><strong>Интернет-магазин</strong><b>↗</b></a></div></div></section>
<section class="secondary-demand" data-stage195-marketplace-faq="true"><div class="secondary-demand__shell"><div class="secondary-demand__head"><p class="secondary-demand__eyebrow">FAQ</p><div><h2>Перед стартом интеграции.</h2><p class="secondary-demand__intro">Нужны доступы к API, понятный источник данных и правила, по которым системы должны обновлять друг друга.</p></div></div><div class="secondary-demand__grid">''' + ''.join(f'<article class="secondary-demand__card"><h3>{q}</h3><p>{a}</p></article>' for q, a in mp_faq) + '''</div></div></section>
<section class="p129-contact wow-reveal"><div class="p129-shell"><div class="p129-contact-card wow-reveal"><div><p class="p129-kicker">START</p><h2>Покажите текущий обмен данными.</h2><p>Для первого сообщения достаточно назвать маркетплейсы, 1С/CRM или другую систему и описать, какие данные сейчас переносятся вручную.</p></div><a class="p129-btn" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Написать в Telegram ↗</a></div></div></section>
</main>'''

clone = source
clone = set_meta(clone, MP_TITLE, MP_DESC)
clone = re.sub(r'<link\b(?=[^>]*rel=["\']canonical["\'])[^>]*>', f'<link rel="canonical" href="{NEW_URL}"/>', clone, count=1, flags=re.I)
clone = re.sub(r'<meta\b(?=[^>]*property=["\']og:url["\'])[^>]*>', f'<meta property="og:url" content="{NEW_URL}"/>', clone, count=1, flags=re.I)
clone = re.sub(r'(<body\b[^>]*\bdata-page=["\'])[^"\']+(["\'])', rf'\g<1>{NEW_SLUG}\2', clone, count=1, flags=re.I)
clone = re.sub(r'<main\b.*?</main>', main, clone, count=1, flags=re.I | re.S)
clone = fit_h1(clone, NEW_SLUG)

# Replace the page-specific schemas while keeping global scripts/assets from the proven service template.
def schema_new_page(m: re.Match[str]) -> str:
    raw = m.group(2)
    try:
        obj = json.loads(raw)
    except Exception:
        return m.group(0)
    typ = obj.get('@type')
    if typ == 'WebPage':
        obj.update({'name': MP_NAME, 'url': NEW_URL, 'description': MP_DESC, 'inLanguage': 'ru-RU'})
    elif typ == 'Service':
        obj.update({'@id': NEW_URL + '#service', 'name': MP_NAME, 'url': NEW_URL, 'description': MP_DESC})
    elif typ == 'BreadcrumbList':
        obj['itemListElement'] = [
            {'@type': 'ListItem', 'position': 1, 'name': 'Главная', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Услуги', 'item': BASE + '/services/'},
            {'@type': 'ListItem', 'position': 3, 'name': 'Интеграция с маркетплейсами', 'item': NEW_URL},
        ]
    elif typ == 'FAQPage':
        obj['mainEntity'] = [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in mp_faq]
    else:
        return m.group(0)
    return m.group(1) + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + m.group(3)

clone = re.sub(r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', schema_new_page, clone, flags=re.I | re.S)
new_page.write_text(clone, encoding='utf-8')

# -----------------------------------------------------------------------------
# 2) Add the new service to the hub and create internal authority links.
# -----------------------------------------------------------------------------
p, s = read('services')
if '/marketplace-integration/' not in s:
    telegram = '<a class="p130-row" href="/telegram-bots/"><span>08</span>'
    if telegram not in s:
        raise SystemExit('stage195: services telegram anchor missing')
    market = '<a class="p130-row" href="/marketplace-integration/"><span>08</span><strong>Интеграция с маркетплейсами</strong><em>1С, Ozon, Wildberries, Яндекс Маркет, товары, остатки и заказы.</em><b>↗</b></a>'
    s = s.replace(telegram, market + '<a class="p130-row" href="/telegram-bots/"><span>09</span>', 1)
    s = s.replace('<a class="p130-row" href="/project-repair/"><span>09</span>', '<a class="p130-row" href="/project-repair/"><span>10</span>', 1)
if 'stage195-services-mobile-h1' not in s:
    style = '<style id="stage195-services-mobile-h1">@media(max-width:600px){body[data-page="services"] main.p130-hub h1 span{display:block!important;max-width:100%!important;width:100%!important;overflow-wrap:anywhere!important}}</style>'
    s = s.replace('</head>', style + '</head>', 1)
p.write_text(s, encoding='utf-8')

related_replacements = {
    '1c-integration': (
        '<a href="/crm-development/"><span>Следующий шаг</span><strong>CRM</strong><b>↗</b></a>',
        '<a href="/marketplace-integration/"><span>Следующий шаг</span><strong>Маркетплейсы</strong><b>↗</b></a>',
    ),
    'ecommerce-development': (
        '<a href="/personal-cabinet-development/"><span>Следующий шаг</span><strong>Личный кабинет</strong><b>↗</b></a>',
        '<a href="/marketplace-integration/"><span>Следующий шаг</span><strong>Маркетплейсы</strong><b>↗</b></a>',
    ),
    'api-integrations': (
        '<a href="/backend-development/"><span>Следующий шаг</span><strong>Серверная логика</strong><b>↗</b></a>',
        '<a href="/marketplace-integration/"><span>Следующий шаг</span><strong>Маркетплейсы</strong><b>↗</b></a>',
    ),
}
for slug, (old, new) in related_replacements.items():
    p, s = read(slug)
    if '/marketplace-integration/' not in s:
        if old not in s:
            raise SystemExit(f'stage195: related anchor missing {slug}')
        s = s.replace(old, new, 1)
    p.write_text(s, encoding='utf-8')

# -----------------------------------------------------------------------------
# 3) High-demand intent inside existing pages (no new competing URLs).
# -----------------------------------------------------------------------------
# AI agents / assistants -> ai-automation.
p, s = read('ai-automation')
if 'data-stage195-ai-agent="true"' not in s:
    m = re.search(r'(<section class="secondary-demand"[^>]*data-stage150="service".*?<div class="secondary-demand__grid">)(.*?)(</div><nav class="secondary-demand__links")', s, re.I | re.S)
    if not m:
        raise SystemExit('stage195: ai demand grid missing')
    extra = '<article class="secondary-demand__card" data-stage195-ai-agent="true"><h3>ИИ-агент для бизнеса</h3><p>Получает контекст, выполняет ограниченный набор действий через API или workflow и передаёт результат дальше с логированием и проверками.</p></article><article class="secondary-demand__card" data-stage195-ai-assistant="true"><h3>ИИ-ассистент</h3><p>Помогает сотруднику искать, классифицировать, извлекать и подготавливать данные, не забирая критичные решения у человека.</p></article>'
    s = s[:m.start()] + m.group(1) + m.group(2) + extra + m.group(3) + s[m.end():]
    s = s.replace('ИИ для бизнеса: модель должна закрывать конкретный шаг процесса.', 'ИИ-агенты и AI-автоматизация для бизнеса: конкретный шаг процесса, а не декоративный AI.', 1)
s = add_stage174_faq(s, 'ai-automation', [
    ('Что такое ИИ-агент для бизнеса?', 'Это программный сценарий, где модель получает контекст, выбирает действие из ограниченного набора, обращается к API или workflow и возвращает результат. Надёжность обеспечивается правилами, логами и проверками.'),
    ('Чем ИИ-ассистент отличается от полной автоматизации?', 'Ассистент помогает человеку подготовить или найти результат, а автоматизация может сама передавать данные и запускать следующий шаг. Для критичных действий полезно оставлять подтверждение человеком.'),
])
p.write_text(s, encoding='utf-8')

# Document workflow -> automation-services.
p, s = read('automation-services')
s = update_task_section(
    s,
    'automation-services',
    'Автоматизация бизнеса: заявки, документы, отчёты и обмен данными.',
    'Автоматизировать стоит повторяющийся процесс с понятным входом и результатом: заявки, документы, таблицы, отчёты, синхронизацию сервисов или регулярные проверки. Документооборот можно включить в общий workflow без ручного переноса файлов и статусов.',
)
s = append_task_card(s, 'automation-services', 'data-stage195-document-flow="true"', 'Автоматизация документооборота', 'Создание, передача, проверка и маршрутизация документов между сотрудниками и сервисами по понятным правилам.')
s = add_stage172_faq(s, 'automation-services', [
    ('Что можно автоматизировать в документообороте?', 'Создание документов из данных, маршрутизацию на проверку, уведомления, перенос статусов, сохранение файлов, реестры и передачу информации между CRM, таблицами, API и другими системами.'),
])
p.write_text(s, encoding='utf-8')

# Landing / corporate site -> web-development.
p, s = read('web-development')
if 'data-stage195-landing="true"' not in s:
    m = re.search(r'(<section class="search-demand".*?<div class="search-demand__grid">)(.*?)(</div><div class="search-demand__links">)', s, re.I | re.S)
    if not m:
        raise SystemExit('stage195: web search-demand grid missing')
    extra = '<article class="search-demand__card" data-stage195-landing="true"><h3>Лендинг под ключ</h3><p>Одностраничный сайт с понятной структурой, адаптивом, формами, аналитикой и технической подготовкой к публикации.</p></article><article class="search-demand__card" data-stage195-corporate="true"><h3>Корпоративный сайт</h3><p>Структура услуг и компании, управляемый контент, формы, каталог или интеграции — без превращения информационного сайта в тяжёлое приложение.</p></article>'
    s = s[:m.start()] + m.group(1) + m.group(2) + extra + m.group(3) + s[m.end():]
s = add_stage174_faq(s, 'web-development', [
    ('Когда нужен лендинг, а когда корпоративный сайт?', 'Лендинг подходит для одного предложения и короткого пути до заявки. Корпоративный сайт нужен, когда есть несколько услуг, разделы о компании, кейсы, статьи, каталог или регулярное развитие контента.'),
])
p.write_text(s, encoding='utf-8')

# Personal cabinet -> own exact query page.
p, s = read('personal-cabinet-development')
PC_TITLE = 'Разработка личного кабинета для сайта на заказ | Alexuys'
PC_DESC = 'Разработка личного кабинета для сайта на заказ: авторизация, профиль, заявки, документы, платежи, статусы, роли, уведомления, backend, API и админ-панель.'
s = set_meta(s, PC_TITLE, PC_DESC)
s = set_h1(s, 'Разработка личного кабинета для сайта. <em>Данные, роли и действия пользователя.</em>', 'personal-cabinet-development')
s = fit_h1(s, 'personal-cabinet-development')
s = update_task_section(
    s,
    'personal-cabinet-development',
    'Разработка личного кабинета: клиент, партнёр, B2B или сервис.',
    'Личный кабинет нужен, когда пользователь должен войти, увидеть собственные данные, выполнить действие и вернуться к истории. Сценарий определяет роли, backend, документы, платежи и интеграции.',
)
s = add_stage172_faq(s, 'personal-cabinet-development', [
    ('От чего зависит стоимость разработки личного кабинета?', 'От количества ролей и пользовательских сценариев, модели данных, документов и платежей, интеграций, требований к интерфейсу и того, существует ли уже сайт или backend.'),
])
s = sync_page_service_schema(s, PC_TITLE, PC_DESC)
p.write_text(s, encoding='utf-8')

# -----------------------------------------------------------------------------
# 4) Discovery files: 72 URLs, with the new route included in both XML sitemaps.
# -----------------------------------------------------------------------------
for name in ('sitemap.xml', 'sitemap-google.xml'):
    p = ROOT / name
    if not p.exists():
        continue
    text = p.read_text(encoding='utf-8')
    if NEW_URL not in text:
        entry = f'<url><loc>{NEW_URL}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>'
        if '</urlset>' not in text:
            raise SystemExit(f'stage195: invalid {name}')
        text = text.replace('</urlset>', entry + '</urlset>', 1)
    else:
        text = re.sub(r'(<loc>' + re.escape(NEW_URL) + r'</loc><lastmod>)[^<]+', rf'\g<1>{TODAY}', text, count=1)
    p.write_text(text, encoding='utf-8')

txt = ROOT / 'sitemap.txt'
xml_map = ROOT / 'sitemap.xml'
if txt.exists() and xml_map.exists():
    import xml.etree.ElementTree as ET
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    xml_urls = [x.text.strip() for x in ET.parse(xml_map).findall('.//s:loc', ns) if x.text and x.text.strip()]
    txt.write_text('\n'.join(xml_urls) + '\n', encoding='utf-8')

changed_routes = [
    '/services/', '/1c-integration/', '/ecommerce-development/', '/api-integrations/',
    '/ai-automation/', '/automation-services/', '/web-development/', '/personal-cabinet-development/',
]
update_lastmods(changed_routes)

# Guards.
checks = {
    NEW_SLUG: [MP_TITLE, MP_DESC, 'data-stage195-marketplace-tasks="true"', 'data-stage195-marketplace-faq="true"', '/1c-integration/', '/api-integrations/'],
    'services': ['/marketplace-integration/', '<span>10</span><strong>Доработка существующего проекта</strong>'],
    '1c-integration': ['/marketplace-integration/'],
    'ecommerce-development': ['/marketplace-integration/'],
    'api-integrations': ['/marketplace-integration/'],
    'ai-automation': ['data-stage195-ai-agent="true"', 'data-stage195-ai-assistant="true"', 'Что такое ИИ-агент для бизнеса?'],
    'automation-services': ['data-stage195-document-flow="true"', 'Что можно автоматизировать в документообороте?'],
    'web-development': ['data-stage195-landing="true"', 'data-stage195-corporate="true"', 'Когда нужен лендинг, а когда корпоративный сайт?'],
    'personal-cabinet-development': [PC_TITLE, PC_DESC, 'Разработка личного кабинета для сайта.', 'От чего зависит стоимость разработки личного кабинета?'],
}
for slug, needles in checks.items():
    data = (ROOT / slug / 'index.html').read_text(encoding='utf-8')
    for needle in needles:
        if needle not in data:
            raise SystemExit(f'stage195: guard failed {slug}: {needle}')

# New page canonical/schema guards.
new_html = new_page.read_text(encoding='utf-8')
if f'<link rel="canonical" href="{NEW_URL}"/>' not in new_html:
    raise SystemExit('stage195: marketplace canonical failed')
if new_html.count('1c-integration/#service'):
    raise SystemExit('stage195: stale 1c service schema remains')
faq_names = [q for q, _ in mp_faq]
for q in faq_names:
    if new_html.count(q) < 2:
        raise SystemExit(f'stage195: marketplace FAQ/schema mismatch: {q}')

# Sitemap guards.
for name in ('sitemap.xml', 'sitemap-google.xml', 'sitemap.txt'):
    p = ROOT / name
    if p.exists() and p.read_text(encoding='utf-8').count(NEW_URL) != 1:
        raise SystemExit(f'stage195: {name} marketplace count != 1')

print('stage195 russian marketplace + demand: new_pages=1, enhanced=8, sitemap_url=72')
