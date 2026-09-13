#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
home = ROOT / 'index.html'
if not home.is_file():
    raise SystemExit('stage127: home missing')
html = home.read_text(encoding='utf-8')

# Stop the carousel JS on the homepage. The premium layout is a curated 4-case mosaic.
html = html.replace(' data-project-showcase=""', ' data-wow-showcase=""', 1)
html = html.replace(' data-project-showcase', ' data-wow-showcase', 1)
html = html.replace(' data-page-size="4"', '', 1)

marker = '<div class="s44-visual-note"><i></i><span>Откройте карточки - это реальные опубликованные кейсы.</span></div>'
if 's127-shot--seo' not in html:
    extra = '''<a class="s44-shot s127-shot--seo" href="/cases/seo-control-center/" aria-label="Открыть кейс SEO Control Center">
<img src="/assets/cases/seo-control-center/seo-control-center-card-02.svg" alt="Интерфейс SEO Control Center" width="1536" height="1024" loading="lazy" decoding="async">
<span><b>SEO CONTROL CENTER</b><small>Мониторинг · кейс</small></span>
</a>
<a class="s44-shot s127-shot--sheet" href="/cases/sheetpilot-ai/" aria-label="Открыть кейс SheetPilot AI">
<img src="/assets/cases/sheetpilot-ai/sheetpilot-01-720w.webp" alt="Интерфейс SheetPilot AI" width="1440" height="1080" loading="lazy" decoding="async">
<span><b>SHEETPILOT AI</b><small>Excel · продукт</small></span>
</a>
'''
    if marker not in html:
        raise SystemExit('stage127: hero visual marker missing')
    html = html.replace(marker, extra + marker, 1)

# Keep the process promise honest: remove the redundant hidden step and leave three real steps.
html, removed = re.subn(r'<article><span>02</span><h3>Можно прийти с чужим кодом</h3><p>.*?</p></article>', '', html, count=1, flags=re.S)
if removed != 1:
    raise SystemExit('stage127: redundant process step not found')
html = html.replace('<span>03</span><h3>Согласуем первый результат</h3>', '<span>02</span><h3>Согласуем первый результат</h3>', 1)
html = html.replace('<span>04</span><h3>Запускаем и передаём</h3>', '<span>03</span><h3>Запускаем и передаём</h3>', 1)

home.write_text(html, encoding='utf-8')
print('stage127 wow direction: homepage hero collage + curated work mosaic + process numbering ready')
