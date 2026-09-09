#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
marker = 'data-stage97-layout="true"'
link = '<link href="/assets/stage97-layout.css?v=20260909-1" rel="stylesheet" data-stage97-layout="true"/>'
css = root / 'assets/stage97-layout.css'
if not css.exists():
    raise SystemExit('stage97: layout stylesheet missing')

required_css = (
    '.stage95-home-model,',
    '.stage95-service-core,',
    'grid-template-columns:minmax(0,1fr)!important;',
    '.s44-price-grid strong',
)
css_text = css.read_text(encoding='utf-8')
for token in required_css:
    if token not in css_text:
        raise SystemExit('stage97: required layout guard missing: ' + token)

checked = changed = 0
home_groups = service_groups = 0
errors = []
for path in sorted(root.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<main' not in html or '</head>' not in html:
        continue
    checked += 1
    original = html
    home_groups += html.count('class="stage95-home-model"')
    service_groups += html.count('class="stage95-service-core"') + html.count('class="stage95-service-meta"')
    html = re.sub(r'\s*<link\b[^>]*data-stage97-layout=["\']true["\'][^>]*/?>', '', html, flags=re.I)
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
        errors.append(f'{rel}: stage97 stylesheet missing or duplicated')
    head = html.split('</head>', 1)[0]
    if not head.rstrip().endswith(link):
        errors.append(f'{rel}: stage97 is not the final stylesheet')

if home_groups != 1:
    errors.append(f'homepage grouped section count expected 1, got {home_groups}')
if service_groups < 20:
    errors.append(f'service grouped section count unexpectedly low: {service_groups}')
if errors:
    raise SystemExit('stage97 layout audit failed:\n' + '\n'.join(errors[:30]))

print(f'stage97 layout: {changed} pages patched; {checked} user-facing pages audited; home_groups={home_groups}; service_groups={service_groups}')
print('stage97 layout: grouped full sections stack at full width; dense-card reading scale and price wrapping guarded')
