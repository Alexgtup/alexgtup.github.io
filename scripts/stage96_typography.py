#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
marker = 'data-stage96-typography="true"'
link = '<link href="/assets/stage96-typography.css?v=20260909-1" rel="stylesheet" data-stage96-typography="true"/>'

css = root / 'assets/stage96-typography.css'
if not css.exists():
    raise SystemExit('stage96: typography stylesheet missing')

changed = 0
checked = 0
families = Counter()
errors = []

for path in sorted(root.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<body' not in html or '</head>' not in html:
        continue

    # Verification stubs have no real page content. Everything with a main landmark
    # is a user-facing page and must receive the same final typography layer.
    if not re.search(r'<main\b', html, re.I):
        continue

    checked += 1
    original = html
    rel = str(path.relative_to(root)).replace('\\', '/')
    body = re.search(r'<body\b([^>]*)>', html, re.I)
    family = re.search(r'data-ux-family=["\']([^"\']+)["\']', body.group(1) if body else '', re.I)

    # The standalone 404 template predates the family system. Give it the neutral
    # family so it receives the same type scale without pretending it is a hub/service.
    if not family:
        html = re.sub(r'<body\b', '<body data-ux-family="page"', html, count=1, flags=re.I)
        family_name = 'page'
    else:
        family_name = family.group(1)
    families[family_name] += 1

    h1_count = len(re.findall(r'<h1\b', html, re.I))
    if rel == '404.html':
        if h1_count < 1:
            errors.append(f'{rel}: expected at least 1 h1, found {h1_count}')
    elif h1_count != 1:
        errors.append(f'{rel}: expected 1 h1, found {h1_count}')

    # Make the layer idempotent and force it to be the last stylesheet in <head>.
    html = re.sub(r'\s*<link\b[^>]*data-stage96-typography=["\']true["\'][^>]*/?>', '', html, flags=re.I)
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
        errors.append(f'{rel}: typography layer missing or duplicated')
    head = html.split('</head>', 1)[0]
    if not head.rstrip().endswith(link):
        errors.append(f'{rel}: typography layer is not last in head')
    if not re.search(r'<body\b[^>]*data-ux-family=["\'][^"\']+["\']', html, re.I):
        errors.append(f'{rel}: missing typography family after finalization')

if errors:
    raise SystemExit('stage96 typography audit failed:\n' + '\n'.join(errors[:30]))

family_report = ', '.join(f'{name}={count}' for name, count in sorted(families.items()))
print(f'stage96 typography: {changed} pages patched; {checked} user-facing pages audited; {family_report}')
print('stage96 scale: desktop H1 normalized by family; mobile H1 capped; body copy >= 1rem; UI actions normalized')
