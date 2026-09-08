#!/usr/bin/env python3
from pathlib import Path
from xml.sax.saxutils import escape
import sys
import xml.etree.ElementTree as ET

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

# Build fallback sitemap formats from the same source URL list so all variants stay in sync.
sitemap_path = root / 'sitemap.xml'
if not sitemap_path.is_file():
    raise SystemExit(f'stage63: missing sitemap: {sitemap_path}')

tree = ET.parse(sitemap_path)
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = []
for node in tree.findall('.//s:loc', ns):
    value = (node.text or '').strip()
    if value and value not in urls:
        urls.append(value)

if not urls:
    raise SystemExit('stage63: source sitemap contains no URLs')

# Minimal XML fallback for Search Console diagnostics.
simple_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]
simple_lines.extend(f'  <url><loc>{escape(url)}</loc></url>' for url in urls)
simple_lines.append('</urlset>')
(root / 'sitemap-google.xml').write_text('\n'.join(simple_lines) + '\n', encoding='utf-8')

# Plain-text sitemap is an independent format supported by Google.
(root / 'sitemap.txt').write_text('\n'.join(urls) + '\n', encoding='utf-8')

print(f'stage63: production SEO Control Center demo link applied to {changed} pages')
print(f'stage63: generated minimal sitemap-google.xml with {len(urls)} URLs')
print(f'stage63: generated sitemap.txt with {len(urls)} URLs')
