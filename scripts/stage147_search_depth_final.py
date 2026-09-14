#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')

subprocess.run(
    [sys.executable, str(Path(__file__).with_name('stage146_search_depth.py')), str(ROOT)],
    check=True,
)

STYLE = '<link href="/assets/stage146-seo-depth.css" rel="stylesheet" data-stage146-seo-depth-style="true"/>'
PAGES = (
    'telegram-bots/index.html',
    'n8n-automation/index.html',
    'crm-development/index.html',
    'web-development/index.html',
    'api-integrations/index.html',
    'project-repair/index.html',
)

changed = 0
for rel in PAGES:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f'stage147: missing {rel}')
    html = path.read_text(encoding='utf-8')
    html = re.sub(r'<link\b[^>]*data-stage146-seo-depth-style="true"[^>]*>\s*', '', html, flags=re.I)
    if '</head>' not in html:
        raise SystemExit(f'stage147: head missing in {rel}')
    html = html.replace('</head>', STYLE + '</head>', 1)
    path.write_text(html, encoding='utf-8')
    changed += 1

if changed != len(PAGES):
    raise SystemExit(f'stage147: expected {len(PAGES)} pages, got {changed}')

print(f'stage147 search depth final: pages={changed}; stylesheet linked')
