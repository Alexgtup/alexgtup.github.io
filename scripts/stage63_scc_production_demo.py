#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
old_urls = (
    'https://seo-control-center-live-demo.onrender.com/',
    'https://seo-control-center-live-demo.onrender.com',
)
new_url = 'https://seo-control-center-prod2.onrender.com/demo'
changed = 0

for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    updated = text
    for old in old_urls:
        updated = updated.replace(old, new_url)
    if updated != text:
        path.write_text(updated, encoding='utf-8')
        changed += 1

required = [
    root / 'cases' / 'seo-control-center' / 'index.html',
    root / 'demos' / 'index.html',
]
for path in required:
    if not path.is_file():
        raise SystemExit(f'stage63: missing required page: {path}')
    if new_url not in path.read_text(encoding='utf-8'):
        raise SystemExit(f'stage63: production SEO Control Center demo link missing: {path}')

print(f'stage63: production SEO Control Center demo link applied to {changed} pages')
