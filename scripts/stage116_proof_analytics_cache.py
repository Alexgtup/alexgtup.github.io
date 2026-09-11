#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
JS = ROOT / 'assets' / 'stage101-intent-handoff.js'

if not JS.is_file():
    raise SystemExit('stage116: intent handoff JS missing')

source = JS.read_text(encoding='utf-8')
for token in ('live_proof_open', 'review_open', 'proof_cases_open', 'reviews_anchor_open'):
    if token not in source:
        raise SystemExit(f'stage116: proof analytics token missing: {token}')

digest = hashlib.sha256(source.encode('utf-8')).hexdigest()[:12]
pattern = re.compile(r'(/assets/stage101-intent-handoff\.js)(?:\?v=[^"\']+)?', re.I)
refs = 0
changed = 0
for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if 'stage101-intent-handoff.js' not in html:
        continue
    new, count = pattern.subn(rf'\1?v={digest}', html)
    refs += count
    if new != html:
        path.write_text(new, encoding='utf-8')
        changed += 1

if refs < 70:
    raise SystemExit(f'stage116: only {refs} analytics refs found')

# Important entry pages must reference exactly the current content hash.
for rel in (
    'index.html',
    'telegram-bots/index.html',
    'web-development/index.html',
    'project-repair/index.html',
    'n8n-automation/index.html',
    'api-integrations/index.html',
    'cases/seo-control-center/index.html',
):
    html = (ROOT / rel).read_text(encoding='utf-8')
    expected = f'/assets/stage101-intent-handoff.js?v={digest}'
    if html.count(expected) != 1:
        raise SystemExit(f'stage116: fingerprint guard failed on {rel}')

print(f'stage116 proof analytics cache: digest={digest}; refs={refs}; changed_pages={changed}; guards OK')
