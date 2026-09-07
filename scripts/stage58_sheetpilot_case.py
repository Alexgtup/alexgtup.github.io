#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
route = '/cases/sheetpilot-ai/'
url = 'https://alexgtup.github.io' + route

STYLE = r'''
<style id="sheetpilot-integrated-style">
.s44-case--sheetpilot{grid-column:span 12!important;grid-template-columns:minmax(0,.56fr) minmax(0,.44fr)!important;min-height:23rem!important;border-color:rgba(212,254,106,.18)!important;background:radial-gradient(circle at 90% 0,rgba(212,254,106,.09),transparent 25rem),#0d1116!important}
.s44-case--sheetpilot .s44-case__image{min-height:23rem}.s44-case--sheetpilot .s44-case__image img{object-fit:cover}.s44-case--sheetpilot .s44-case__body>span,.s44-case--sheetpilot .s44-case__body b{color:#d4fe6a}.s44-case--sheetpilot .s44-case__body h3{font-size:clamp(2rem,4vw,4rem)}
.s50-case-list>.sp-sheetpilot-case{border-color:rgba(212,254,106,.18)!important;background:radial-gradient(circle at 90% 0,rgba(212,254,106,.08),transparent 23rem),#0d1116!important}.s50-case-list>.sp-sheetpilot-case span,.s50-case-list>.sp-sheetpilot-case b{color:#d4fe6a!important}
@media(max-width:900px){.s44-case--sheetpilot{grid-template-columns:1fr!important}.s44-case--sheetpilot .s44-case__image{min-height:0}}
</style>
'''

HOME_CARD = r'''
<a class="s44-case s44-case--visual s44-case--sheetpilot" href="/cases/sheetpilot-ai/">
  <div class="s44-case__image"><img src="/assets/cases/sheetpilot-ai/sheetpilot-01-720w.webp" width="720" height="540" loading="lazy" decoding="async" alt="SheetPilot AI — ИИ-ассистент для обработки Excel-файлов"/></div>
  <div class="s44-case__body"><span>AI · EXCEL · FULLSTACK</span><h3>SheetPilot AI</h3><p>Рабочий MVP для обработки Excel обычным языком: загрузка XLSX, ограниченный план изменений, предпросмотр результата и экспорт нового файла.</p><b>Открыть полный кейс ↗</b></div>
</a>
'''

CASES_CARD = r'''
<a class="visual sp-sheetpilot-case" href="/cases/sheetpilot-ai/"><img src="/assets/cases/sheetpilot-ai/sheetpilot-01-720w.webp" width="720" height="540" loading="lazy" decoding="async" alt="Интерфейс SheetPilot AI для обработки Excel"/><div><span>AI · EXCEL · FULLSTACK</span><h3>SheetPilot AI</h3><p>Excel-ассистент: команда обычным языком, безопасный preview изменений и экспорт нового файла.</p><b>Открыть кейс ↗</b></div></a>
'''


def cleanup_old_promo(text: str) -> str:
    text = re.sub(r'\n?<style id="sheetpilot-promo-style">.*?</style>\n?', '\n', text, flags=re.S)
    text = re.sub(r'\n?<section class="sp-promo" data-sheetpilot-promo="true">.*?</section>\n?', '\n', text, flags=re.S)
    return text


def add_style(text: str) -> str:
    if 'id="sheetpilot-integrated-style"' not in text:
        if '</head>' not in text:
            raise SystemExit('sheetpilot: </head> not found')
        text = text.replace('</head>', STYLE + '</head>', 1)
    return text


def patch_home(path: Path) -> None:
    if not path.is_file():
        raise SystemExit(f'sheetpilot: home not found: {path}')
    text = cleanup_old_promo(path.read_text(encoding='utf-8'))
    text = add_style(text)
    if 's44-case--sheetpilot' not in text:
        marker = '<div class="s44-case-grid">'
        if marker not in text:
            raise SystemExit('sheetpilot: home project grid not found')
        text = text.replace(marker, marker + HOME_CARD, 1)
    text = text.replace('<strong>5</strong><span>подробных кейсов на сайте</span>', '<strong>6</strong><span>подробных кейсов на сайте</span>', 1)
    path.write_text(text, encoding='utf-8')


def patch_cases(path: Path) -> None:
    if not path.is_file():
        raise SystemExit(f'sheetpilot: cases hub not found: {path}')
    text = cleanup_old_promo(path.read_text(encoding='utf-8'))
    text = add_style(text)
    if 'sp-sheetpilot-case' not in text:
        marker = '<div class="s50-case-list">'
        if marker not in text:
            raise SystemExit('sheetpilot: cases list not found')
        text = text.replace(marker, marker + CASES_CARD, 1)
    text = text.replace('<strong>5</strong><span>подробных кейсов</span>', '<strong>6</strong><span>подробных кейсов</span>', 1)
    path.write_text(text, encoding='utf-8')


patch_home(root / 'index.html')
patch_cases(root / 'cases' / 'index.html')

sm = root / 'sitemap.xml'
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
tree = ET.parse(sm)
r = tree.getroot()
ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
locs = {(n.text or '').strip() for n in r.findall('.//' + ns + 'loc')}
if url not in locs:
    node = ET.SubElement(r, ns + 'url')
    loc = ET.SubElement(node, ns + 'loc')
    loc.text = url
    tree.write(sm, encoding='utf-8', xml_declaration=True)

for name in ('sitemap.txt', 'llms.txt'):
    p = root / name
    if p.is_file():
        text = p.read_text(encoding='utf-8')
        line = url if name == 'sitemap.txt' else f'- {url} — SheetPilot AI, ИИ-ассистент для обработки Excel-файлов'
        if line not in text:
            p.write_text(text.rstrip() + '\n' + line + '\n', encoding='utf-8')

print('stage58: SheetPilot AI integrated into existing project grids + sitemap')
