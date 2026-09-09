#!/usr/bin/env python3
"""Final UX normalization plus deployment gate for analytics and structured-data regressions."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import subprocess
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
repo_root = Path(__file__).resolve().parents[1]

# These finalizers intentionally run after all content/SEO generators so the published
# artifact, not an intermediate template, gets the same UX baseline, pruning and type scale.
subprocess.run([sys.executable, str(repo_root / 'scripts/stage94_sitewide_ux.py'), str(root)], check=True)
subprocess.run([sys.executable, str(repo_root / 'scripts/stage95_prune_and_unify.py'), str(root)], check=True)
subprocess.run([sys.executable, str(repo_root / 'scripts/stage96_typography.py'), str(root)], check=True)
subprocess.run(['node', '--check', str(root / 'assets/stage94-site-ux.js')], check=True)

errors = []
pages = 0
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.scripts = []; self.consent = 0; self.settings = 0; self.ids = []; self.canonical = None; self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'script' and a.get('src'): self.scripts.append(a['src'])
        if 'data-analytics-consent' in a: self.consent += 1
        if 'data-analytics-settings' in a: self.settings += 1
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a.get('href')
        if tag == 'a': self.links.append(a.get('href', ''))

inbound = {'/cases/sheetpilot-ai/': set(), '/cases/seo-control-center/': set(), '/demos/': set()}
for p in root.rglob('*.html'):
    if p.name.startswith(('google', 'yandex_')): continue
    pages += 1
    t = p.read_text(encoding='utf-8'); doc = Page(); doc.feed(t)
    if sum(s.startswith('/assets/analytics.js?v=') for s in doc.scripts) != 1: errors.append(f'{p}: shared analytics missing or duplicated')
    if doc.consent != 1 or doc.settings != 1: errors.append(f'{p}: consent controls missing or duplicated')
    if len(doc.ids) != len(set(doc.ids)): errors.append(f'{p}: duplicate IDs')
    if 'mc.yandex.ru' in t or 'startMetrika' in t: errors.append(f'{p}: old inline analytics remains')
    for target in inbound:
        if target in doc.links: inbound[target].add(str(p))
    for raw in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', t, re.S):
        data = json.loads(raw)
        def check(obj):
            if not isinstance(obj, dict): return
            if obj.get('@type') in ('WebPage', 'Service') and doc.canonical and obj.get('url') != doc.canonical:
                errors.append(f'{p}: schema URL {obj.get("url")} differs from canonical')
            for child in obj.get('@graph', []): check(child)
        if isinstance(data, list):
            for obj in data: check(obj)
        else: check(data)
# After Stage95 pruning, three strong contextual entry points are the floor. The
# previous threshold of four forced duplicate promo sections back into the UI.
for url, sources in inbound.items():
    if len(sources) < 3: errors.append(f'{url}: only {len(sources)} linking pages')
js = (root / 'assets/site-enhancements.js').read_text()
if "if (typeof window.ym !== 'function') return;" in js: errors.append('legacy goal helper does not honor revocation')
if errors: raise SystemExit('\n'.join(errors))
print(f'growth validation OK: {pages} pages; shared consent and analytics; matching schema identities')
for url, sources in inbound.items(): print(f'  {url}: {len(sources)} linking pages')
