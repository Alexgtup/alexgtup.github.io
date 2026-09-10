#!/usr/bin/env python3
from pathlib import Path
import re
import sys
from urllib.parse import quote

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BASE = 'https://alexgtup.github.io'
TODAY = '2026-09-10'

changed = []


def read(route):
    p = root / ('index.html' if route == '/' else route.strip('/') + '/index.html')
    return p, p.read_text(encoding='utf-8')


def write(route, path, old, new):
    if new != old:
        path.write_text(new, encoding='utf-8')
        changed.append(route)


def tg(text):
    return 'https://t.me/Alexuys?text=' + quote(text, safe='')


# Homepage: lower the perceived entry barrier without lowering or changing prices.
p, text = read('/')
old = text
lead_old = 'Разрабатываю Telegram-ботов, сайты и веб-сервисы, CRM, API-интеграции и автоматизацию. Можно прийти с новой задачей или существующим проектом — общение напрямую с разработчиком, без передачи между менеджерами.'
lead_new = 'Разрабатываю Telegram-ботов, сайты и веб-сервисы, CRM, API-интеграции и автоматизацию. Можно прийти с новой задачей, одной небольшой правкой или существующим проектом - общение напрямую с разработчиком, без передачи между менеджерами.'
if lead_old in text:
    text = text.replace(lead_old, lead_new, 1)
elif lead_new not in text:
    raise SystemExit('stage102: homepage lead marker missing')

if 'data-stage102-fastlane="true"' not in text:
    marker = '<noscript><style>#s44-brief-form{display:none}</style>'
    i = text.find(marker)
    if i < 0:
        raise SystemExit('stage102: homepage brief marker missing')
    block = (
        '<div class="s102-fastlane" data-stage102-fastlane="true">'
        '<div><span>БЫСТРЫЙ ВХОД</span><strong>Не обязательно готовить большое ТЗ.</strong>'
        '<p>Если нужна одна правка, проверка или продолжение прошлой задачи - можно сразу прислать ссылку и пару строк.</p></div>'
        '<div class="s102-fastlane__actions">'
        f'<a class="button" data-cta="quick-task" href="{tg("Здравствуйте. Нужна небольшая разовая задача.\n\nСсылка / что нужно поправить: ")}" target="_blank" rel="noopener noreferrer">Небольшая задача ↗</a>'
        f'<a class="button" data-cta="repeat-client" href="{tg("Здравствуйте. Мы уже работали вместе. Хочу продолжить прошлый проект.\n\nЧто нужно сделать дальше: ")}" target="_blank" rel="noopener noreferrer">Продолжить прошлый проект ↗</a>'
        '</div></div>'
    )
    text = text[:i] + block + text[i:]

select_old = '<select name="type"><option>Сайт / веб-сервис</option>'
select_new = '<select name="type"><option>Небольшая правка / разовая задача</option><option>Продолжить прошлый проект</option><option>Сайт / веб-сервис</option>'
if select_old in text:
    text = text.replace(select_old, select_new, 1)
elif select_new not in text:
    raise SystemExit('stage102: homepage brief select marker missing')
write('/', p, old, text)

# Services hub: make it explicit that the catalog also fits small standalone jobs.
p, text = read('/services/')
old = text
needle = 'Не обязательно выбирать технологию до разговора. Здесь услуги сгруппированы по результату: новый продукт, автоматизация, интеграция или доработка уже существующего проекта.'
replacement = 'Не обязательно выбирать технологию до разговора. Можно прийти с одной небольшой правкой, новым продуктом, автоматизацией, интеграцией или доработкой уже существующего проекта.'
if needle in text:
    text = text.replace(needle, replacement, 1)
elif replacement not in text:
    raise SystemExit('stage102: services intro marker missing')
needle2 = 'Ошибка, форма, адаптив, интеграция, новый функционал, старый код или проект, который нужно довести до релиза.'
replacement2 = 'Одна правка, ошибка, форма, адаптив, интеграция, новый функционал, старый код или проект, который нужно довести до релиза.'
if needle2 in text:
    text = text.replace(needle2, replacement2, 1)
elif replacement2 not in text:
    raise SystemExit('stage102: services repair marker missing')
write('/services/', p, old, text)

# Freelance landing: optimize for trust + low-friction first order and repeat orders.
p, text = read('/freelance-developer/')
old = text
needle = 'Если важно сначала проверить исполнителя, а потом писать — здесь собраны реальные кейсы, публичный профиль Freelance.ru и конкретные форматы первого этапа: Telegram, n8n, API-интеграции, доработка проекта и технический SEO.'
replacement = 'Если важно сначала проверить исполнителя, а потом писать - здесь собраны реальные кейсы, публичный профиль Freelance.ru с отзывами и историей работ, а также понятные форматы для небольшой задачи, Telegram, n8n, API-интеграции, доработки проекта и технического SEO.'
if needle in text:
    text = text.replace(needle, replacement, 1)
elif replacement not in text:
    raise SystemExit('stage102: freelance hero marker missing')

replacements = {
    'идеей нового продукта': 'небольшой правкой или разовой задачей',
    'ручным процессом для автоматизации': 'идеей нового продукта или автоматизацией',
}
for source, target in replacements.items():
    if source in text:
        text = text.replace(source, target, 1)
    elif target not in text:
        raise SystemExit('stage102: freelance profile marker missing: ' + source)

case_btn = '<a class="s50-btn" href="/cases/">Кейсы</a>'
quick_btn = f'<a class="s50-btn" data-cta="quick-task" href="{tg("Здравствуйте. Нужна небольшая задача.\n\nЧто нужно сделать: ")}" target="_blank" rel="noopener noreferrer">Небольшая задача ↗</a>'
if case_btn in text:
    text = text.replace(case_btn, quick_btn, 1)
elif quick_btn not in text:
    raise SystemExit('stage102: freelance contact button marker missing')

if 'data-stage102-repeat="true"' not in text:
    contact_marker = '<p>Можно прислать даже короткое описание без подготовленного ТЗ.</p>'
    repeat = (
        contact_marker
        + f'<p class="s102-repeat" data-stage102-repeat="true">Уже работали вместе? <a data-cta="repeat-client" href="{tg("Здравствуйте. Мы уже работали вместе. Хочу продолжить прошлый проект.\n\nСледующая задача: ")}" target="_blank" rel="noopener noreferrer">Продолжить прошлый проект →</a></p>'
    )
    if contact_marker not in text:
        raise SystemExit('stage102: freelance repeat marker missing')
    text = text.replace(contact_marker, repeat, 1)
write('/freelance-developer/', p, old, text)

# Honest freshness: touch sitemap only for pages whose visible content changed.
sitemap = root / 'sitemap.xml'
xml = sitemap.read_text(encoding='utf-8')
for route in sorted(set(changed)):
    loc = BASE + route
    pattern = re.compile(rf'(<url>\s*.*?<loc>{re.escape(loc)}</loc>.*?</url>)', re.S)
    match = pattern.search(xml)
    if not match:
        raise SystemExit('stage102: sitemap entry missing ' + loc)
    block = match.group(1)
    if '<lastmod>' in block:
        patched = re.sub(r'<lastmod>[^<]+</lastmod>', f'<lastmod>{TODAY}</lastmod>', block, count=1)
    else:
        patched = block.replace(f'<loc>{loc}</loc>', f'<loc>{loc}</loc><lastmod>{TODAY}</lastmod>', 1)
    xml = xml[:match.start(1)] + patched + xml[match.end(1):]
sitemap.write_text(xml, encoding='utf-8')

# Guards: existing price markers must survive. This stage is about volume, not repricing.
for route in ('/', '/services/', '/freelance-developer/'):
    _, html = read(route)
    if route == '/' and html.count('data-stage102-fastlane="true"') != 1:
        raise SystemExit('stage102: homepage fastlane guard failed')
    if '15 000 ₽' not in html:
        raise SystemExit('stage102: existing price markers unexpectedly disappeared on ' + route)

print('stage102 volume growth: changed=' + ','.join(changed) + '; pricing unchanged; quick-task and repeat-client paths added')
