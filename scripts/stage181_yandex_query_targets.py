#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re, sys, xml.etree.ElementTree as ET

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BASE = 'https://alexgtup.github.io'
TODAY = '2026-09-18'
MARKER = 'stage181-yandex-query-targets'


def read(rel: str) -> tuple[Path, str]:
    p = ROOT / rel
    if not p.is_file():
        raise SystemExit(f'stage181: missing {rel}')
    return p, p.read_text(encoding='utf-8')


def write(p: Path, s: str) -> None:
    p.write_text(s, encoding='utf-8')


def replace_once(s: str, old: str, new: str, label: str) -> str:
    if new in s:
        return s
    if old not in s:
        raise SystemExit(f'stage181: marker not found: {label}')
    return s.replace(old, new, 1)

# 1) Excel/OpenPyXL cluster: align the commercial page with queries already seen in Yandex.
p, s = read('excel-google-sheets-automation/index.html')
old_title = 'Автоматизация Excel и Google Sheets на заказ | Alexuys'
new_title = 'Автоматизация Excel на Python, openpyxl и Google Sheets | Alexuys'
old_desc = 'Автоматизация Excel и Google Sheets: обработка файлов, формулы, отчёты, API, объединение данных, генерация документов и AI-ассистенты.'
new_desc = 'Автоматизация Excel и Google Sheets на Python/openpyxl: обработка XLSX и CSV, отчёты, API, массовые изменения и AI-ассистенты. Реальный кейс SheetPilot AI.'
s = s.replace(old_title, new_title)
s = s.replace(old_desc, new_desc)
s = replace_once(
    s,
    '<h1>Excel и Google Sheets <em>без повторяющейся ручной работы.</em></h1>',
    '<h1>Автоматизация Excel и Google Sheets. <em>Python, openpyxl и AI.</em></h1>',
    'excel h1',
)
excel_block = '''<section class="secondary-demand" data-stage181-excel-query="true"><div class="secondary-demand__shell"><div class="secondary-demand__head"><p class="secondary-demand__eyebrow">PYTHON / OPENPYXL / AI</p><div><h2>Excel + Python/openpyxl + AI: где это действительно полезно.</h2><p class="secondary-demand__intro">Если нужно регулярно менять XLSX-файлы, объединять таблицы или обрабатывать команды обычным языком, AI лучше использовать как планировщик действий, а сами изменения выполнять проверяемым Python-кодом.</p></div></div><div class="secondary-demand__grid"><article class="secondary-demand__card"><h3>openpyxl для XLSX</h3><p>Чтение листов, ячеек, формул и структуры книги; массовые изменения значений; сохранение результата отдельным файлом.</p></article><article class="secondary-demand__card"><h3>AI как слой понимания</h3><p>Команда пользователя преобразуется в ограниченный план операций. Код проверяет план и только после этого применяет изменения к таблице.</p></article><article class="secondary-demand__card"><h3>Google Sheets и API</h3><p>Когда данные должны жить не в одном файле, таблица связывается с CRM, сайтом, Telegram или внутренним сервисом через API.</p></article></div><div class="search-demand__links"><a href="/cases/sheetpilot-ai/">Кейс: ИИ-ассистент для Excel на openpyxl ↗</a><a href="/python-scripts/">Python-скрипты для данных ↗</a></div></div></section>'''
if 'data-stage181-excel-query="true"' not in s:
    anchor = '<section class="p129-related wow-reveal">'
    if anchor not in s:
        raise SystemExit('stage181: excel related anchor missing')
    s = s.replace(anchor, excel_block + anchor, 1)
write(p, s)

# 2) SheetPilot: answer the exact informational intent that is already getting Yandex impressions/clicks.
p, s = read('cases/sheetpilot-ai/index.html')
sheet_block = '''<section class="section p132-panel wow-reveal" data-stage181-openpyxl-answer="true"><div class="container"><div class="section-head"><div class="kicker">OPENPYXL + AI</div><div><h2>Как отредактировать Excel с ИИ <em>через openpyxl.</em></h2><p class="section-copy">В SheetPilot нейросеть не получает прямой доступ к файлу. Она переводит команду вроде «увеличь цены на 7%» в ограниченный план, а Python/openpyxl читает XLSX, проверяет диапазоны, показывает изменения и создаёт новый файл. Так AI отвечает за понимание запроса, а изменение Excel остаётся контролируемой операцией кода.</p><p class="section-copy"><a href="/excel-google-sheets-automation/">Автоматизация Excel и Google Sheets на Python ↗</a></p></div></div></div></section>'''
if 'data-stage181-openpyxl-answer="true"' not in s:
    gallery = re.search(r'<section\b[^>]*\bid=["\']gallery["\'][^>]*>', s, re.I)
    if not gallery:
        raise SystemExit('stage181: sheetpilot gallery anchor missing')
    s = s[:gallery.start()] + sheet_block + s[gallery.start():]
write(p, s)

# 3) Telegram brief: make the first substantive heading answer the query wording seen in Yandex.
p, s = read('guides/telegram-bot-brief/index.html')
s = s.replace('<h2>Зачем нужен короткий бриф</h2>', '<h2>Как должно выглядеть ТЗ для Telegram-бота</h2>', 1)
s = s.replace(
    '<div class="answer"><b>Для оценки Telegram-бота не нужен документ на 40 страниц.</b>',
    '<div class="answer"><b>Хорошее ТЗ на Telegram-бота начинается не со списка кнопок, а с цели, пользователя и главного сценария.</b>',
    1,
)
write(p, s)

# 4) Cost guide: lead the short answer with the exact commercial question already producing impressions.
p, s = read('guides/telegram-bot-cost/index.html')
s = s.replace('<section id="short"><h2>Короткий ответ</h2>', '<section id="short"><h2>Сколько стоит сделать бота в Telegram</h2>', 1)
write(p, s)

# 5) Final hreflang guard for every generated stage172 commercial page.
fixed_hreflang = 0
for p in ROOT.rglob('index.html'):
    s = p.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'data-stage172=["\']([^"\']+)["\']', s)
    if not m:
        continue
    slug = m.group(1)
    url = f'{BASE}/{slug}/'
    changed = False
    for lang in ('ru', 'x-default'):
        pat = rf'<link\b(?=[^>]*\bhreflang=["\']{re.escape(lang)}["\'])[^>]*>'
        repl = f'<link rel="alternate" hreflang="{lang}" href="{url}"/>'
        if re.search(pat, s, re.I):
            ns = re.sub(pat, repl, s, count=1, flags=re.I)
            changed |= ns != s
            s = ns
    canonical = re.search(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*\bhref=["\']([^"\']+)', s, re.I)
    if not canonical or canonical.group(1) != url:
        raise SystemExit(f'stage181: canonical mismatch for {slug}: {canonical.group(1) if canonical else "missing"}')
    for lang in ('ru','x-default'):
        if f'hreflang="{lang}" href="{url}"' not in s:
            raise SystemExit(f'stage181: hreflang {lang} mismatch for {slug}')
    if changed:
        p.write_text(s, encoding='utf-8')
        fixed_hreflang += 1

# 6) Refresh lastmod only for URLs materially changed in this batch.
targets = {
    f'{BASE}/excel-google-sheets-automation/',
    f'{BASE}/cases/sheetpilot-ai/',
    f'{BASE}/guides/telegram-bot-brief/',
    f'{BASE}/guides/telegram-bot-cost/',
}
for name in ('sitemap.xml', 'sitemap-google.xml'):
    path = ROOT / name
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    for url in targets:
        text = re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+', rf'\g<1>{TODAY}', text, count=1)
    path.write_text(text, encoding='utf-8')

# Hard guards.
for rel, needle in {
    'excel-google-sheets-automation/index.html':'data-stage181-excel-query="true"',
    'cases/sheetpilot-ai/index.html':'data-stage181-openpyxl-answer="true"',
    'guides/telegram-bot-brief/index.html':'Как должно выглядеть ТЗ для Telegram-бота',
    'guides/telegram-bot-cost/index.html':'Сколько стоит сделать бота в Telegram',
}.items():
    if needle not in (ROOT/rel).read_text(encoding='utf-8'):
        raise SystemExit(f'stage181: guard failed {rel}')

print(f'stage181 yandex query targets: hreflang_fixed={fixed_hreflang}, target_pages={len(targets)}')
