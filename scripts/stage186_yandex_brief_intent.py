#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html, json, re, sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BASE = 'https://alexgtup.github.io'
TODAY = '2026-09-18'
REL = 'guides/telegram-bot-brief/index.html'
PATH = ROOT / REL
if not PATH.is_file():
    raise SystemExit('stage186: telegram brief missing')
s = PATH.read_text(encoding='utf-8')

TITLE = 'Как составить ТЗ на Telegram-бота - пример и шаблон | Alexuys'
DESC = 'Как должно выглядеть ТЗ на Telegram-бота: цель, пользователь, сценарий, данные, CRM/API, оплаты и критерии готовности. Короткий пример и шаблон без лишней формальности.'

# Search snippet: align with the three real Yandex query formulations already seen.
s = re.sub(r'<title>.*?</title>', '<title>'+html.escape(TITLE)+'</title>', s, count=1, flags=re.I|re.S)
for attr,key,val in [
    ('name','description',DESC),('property','og:title',TITLE),('property','og:description',DESC),
    ('name','twitter:title',TITLE),('name','twitter:description',DESC),
]:
    pat = rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
    repl = f'<meta {attr}="{key}" content="{html.escape(val, quote=True)}"/>'
    if re.search(pat, s, re.I):
        s = re.sub(pat, repl, s, count=1, flags=re.I)
    else:
        s = s.replace('</head>', repl+'</head>', 1)

# Above-the-fold answer: make the page useful before the long-form explanation starts.
s = re.sub(
    r'<p class="lead">.*?</p>',
    '<p class="lead">Как составить ТЗ на Telegram-бота без документа на десятки страниц: зафиксировать цель, пользователя, главный сценарий, данные, интеграции и критерий готовности. Ниже — короткий шаблон и заполненный пример.</p>',
    s, count=1, flags=re.I|re.S,
)
s = re.sub(
    r'(<section id="why"><h2>).*?(</h2>)',
    r'\1Как должно выглядеть ТЗ для Telegram-бота\2',
    s, count=1, flags=re.I|re.S,
)
s = re.sub(
    r'<div class="answer">.*?</div>',
    '<div class="answer" data-stage186-direct-answer="true"><b>Минимальное ТЗ на Telegram-бота — это 6 вещей:</b> цель, кто пользуется ботом, главный путь от /start до результата, какие данные вводятся и хранятся, какие сервисы подключаются и по какому признаку задача считается готовой.</div>',
    s, count=1, flags=re.I|re.S,
)
s = re.sub(
    r'(<section id="example"><h2>).*?(</h2>)',
    r'\1Пример лёгкого ТЗ на Telegram-бота\2',
    s, count=1, flags=re.I|re.S,
)
s = s.replace('<a href="#why">Зачем нужен короткий бриф</a>', '<a href="#why">Как должно выглядеть ТЗ</a>', 1)
s = s.replace('<a href="#example">Пример заполнения</a>', '<a href="#example">Пример лёгкого ТЗ</a>', 1)
s = s.replace('Обновлено 05.09.2026', 'Обновлено 18.09.2026', 1)
s = s.replace('"dateModified":"2026-09-05"', '"dateModified":"2026-09-18"')

# Add the exact question to the visible FAQ and its schema, without duplicating it on reruns.
Q = 'Как должно выглядеть ТЗ для Telegram-бота?'
A = 'Достаточно описать цель, пользователя, основной сценарий, данные, интеграции и критерий готовности. Кнопки, структура базы и технический стек можно уточнить после разбора задачи.'
if Q not in s:
    marker = '<div class="faq">'
    if marker not in s:
        raise SystemExit('stage186: visible FAQ marker missing')
    s = s.replace(marker, marker+f'<details data-stage186-brief-faq="true"><summary>{Q}</summary><p>{A}</p></details>', 1)

faq_match = None
for m in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', s, re.I|re.S):
    if '"FAQPage"' in m.group(1):
        faq_match = m
        break
if not faq_match:
    raise SystemExit('stage186: FAQ schema missing')
obj = json.loads(faq_match.group(1))
if Q not in {x.get('name') for x in obj.get('mainEntity', [])}:
    obj.setdefault('mainEntity', []).insert(0, {'@type':'Question','name':Q,'acceptedAnswer':{'@type':'Answer','text':A}})
    blob = json.dumps(obj, ensure_ascii=False, separators=(',',':'))
    s = s[:faq_match.start(1)] + blob + s[faq_match.end(1):]

PATH.write_text(s, encoding='utf-8')

# Refresh only the materially changed URL in discovery files.
url = BASE + '/guides/telegram-bot-brief/'
for name in ('sitemap.xml','sitemap-google.xml'):
    p = ROOT / name
    if not p.exists():
        continue
    text = p.read_text(encoding='utf-8')
    text = re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+', rf'\g<1>{TODAY}', text, count=1)
    p.write_text(text, encoding='utf-8')

# Hard guards.
final = PATH.read_text(encoding='utf-8')
for needle in [TITLE, DESC, 'data-stage186-direct-answer="true"', 'Пример лёгкого ТЗ на Telegram-бота', Q, '"dateModified":"2026-09-18"']:
    if needle not in final:
        raise SystemExit(f'stage186: guard failed: {needle}')
print('stage186 yandex brief intent: page=1, faq=1')
