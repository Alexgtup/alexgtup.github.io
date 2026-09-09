#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
marker = 'data-stage98-design="true"'
link = '<link href="/assets/stage98-design-system.css?v=20260909-1" rel="stylesheet" data-stage98-design="true"/>'
css = root / 'assets/stage98-design-system.css'
if not css.exists():
    raise SystemExit('stage98: design stylesheet missing')

required_css = (
    '--ds-accent:#c9ff4a;',
    '.portfolio-showcase__layout',
    '.portfolio-carousel__grid',
    '.s44-route-grid',
    '.stage95-service-core',
    '.case-library__grid',
)
css_text = css.read_text(encoding='utf-8')
for token in required_css:
    if token not in css_text:
        raise SystemExit('stage98: required design token/rule missing: ' + token)

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

    if rel == 'index.html':
        home_seen = True
        html = html.replace('data-project-showcase data-page-size="4"', 'data-project-showcase data-page-size="3"')
        html = html.replace('Выбранные проекты. <em>Реальная работа.</em>', 'Выбранные проекты. <em>Реальные интерфейсы и логика.</em>')
        html = html.replace('CRM, автоматизация, web, mobile и Telegram. Коротко о задаче, интерфейсе и результате.', 'Несколько сильных работ вместо длинной витрины: задача, интерфейс, логика и то, что получилось в итоге.')
        html = html.replace('<strong>5</strong><span>подробных кейсов на сайте</span>', '<strong>9</strong><span>подробных кейсов на сайте</span>')

    html = re.sub(r'\s*<link\b[^>]*data-stage98-design=["\']true["\'][^>]*/?>', '', html, flags=re.I)
    html = html.replace('</head>', link + '\n</head>', 1)
    if html != original:
        path.write_text(html, encoding='utf-8')
        changed += 1

for path in sorted(root.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<main' not in html or '</head>' not in html:
        continue
    rel = str(path.relative_to(root)).replace('\\', '/')
    if html.count(marker) != 1:
        errors.append(f'{rel}: design system missing or duplicated')
    head = html.split('</head>', 1)[0]
    if not head.rstrip().endswith(link):
        errors.append(f'{rel}: stage98 is not the final stylesheet')

if not home_seen:
    errors.append('homepage not found')
else:
    home = (root / 'index.html').read_text(encoding='utf-8', errors='ignore')
    if 'data-project-showcase data-page-size="3"' not in home:
        errors.append('homepage showcase is not 3-up')
    if 'project-radar' not in home or 'portfolio-carousel' not in home:
        errors.append('homepage showcase structure missing')

if errors:
    raise SystemExit('stage98 design audit failed:\n' + '\n'.join(errors[:30]))

print(f'stage98 design system: {changed} pages patched; {checked} user-facing pages audited')
print('stage98: one neutral surface language; lime accent; calmer homepage; 3-up projects; unified hub/service/card rhythm')
