#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re
import subprocess
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BUNDLE = ROOT / 'assets' / 'stage105-final-ui.css'
WOW_CSS = ROOT / 'assets' / 'stage133-wow-system.css'
WOW_JS = ROOT / 'assets' / 'stage133-wow-motion.js'

for required in (BUNDLE, WOW_CSS, WOW_JS):
    if not required.is_file():
        raise SystemExit(f'stage133: missing {required}')

bundle = BUNDLE.read_text(encoding='utf-8')
css = WOW_CSS.read_text(encoding='utf-8').strip()
if '/* stage133-wow-system */' not in css:
    raise SystemExit('stage133: css marker missing')
if '/* stage133-wow-system */' not in bundle:
    bundle = bundle.rstrip() + '\n\n' + css + '\n'
BUNDLE.write_text(bundle, encoding='utf-8')

subprocess.run(['node', '--check', str(WOW_JS)], check=True)
css_digest = hashlib.sha256(BUNDLE.read_bytes()).hexdigest()[:12]
js_digest = hashlib.sha256(WOW_JS.read_bytes()).hexdigest()[:12]

ROUTES = {
    'index.html': 'home',
    'services/index.html': 'services',
    'cases/index.html': 'cases',
    'guides/index.html': 'guides',
    'about/index.html': 'about',
    'freelance-developer/index.html': 'freelance-developer',
}
SERVICE_ROUTES = {
    'telegram-bots','telegram-bot-repair','telegram-mini-apps','web-development','development',
    'n8n-automation','api-integrations','backend-development','crm-development','project-repair',
    'python-development','ai-automation','ios-development','app-development','mvp-development'
}
CASE_ROUTES = {
    'fin-planner','swift-calendar','sheetpilot-ai','seo-control-center','auto-crm',
    'factory-catalog','taxi-app','siteaudit-studio','freelance-os'
}
REVEAL_CLASSES = (
    'p128-feature','p128-capabilities','p128-proof','p128-start',
    'p129-outcomes','p129-case','p129-related','p129-contact',
    'p130-list-section','p130-featured','p130-editorial','p130-footer-cta',
    'p132-panel','p132-end'
)

def add_class_token(html: str, token: str) -> str:
    pattern = re.compile(r'class="([^"]*\b' + re.escape(token) + r'\b[^"]*)"', re.I)
    def repl(match):
        classes = match.group(1).split()
        if 'wow-reveal' not in classes:
            classes.append('wow-reveal')
        return 'class="' + ' '.join(classes) + '"'
    return pattern.sub(repl, html)

def route_key(rel: str):
    if rel in ROUTES:
        return ROUTES[rel]
    parts = rel.split('/')
    if len(parts) == 2 and parts[1] == 'index.html' and parts[0] in SERVICE_ROUTES:
        return parts[0]
    if len(parts) == 3 and parts[0] == 'cases' and parts[2] == 'index.html' and parts[1] in CASE_ROUTES:
        return parts[1]
    return None

changed = 0
for path in sorted(ROOT.rglob('*.html')):
    rel = path.relative_to(ROOT).as_posix()
    key = route_key(rel)
    if not key:
        continue
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<body' not in html:
        continue

    def body_repl(match):
        attrs = match.group(1)
        attrs = re.sub(r'\sdata-wow="[^"]*"', '', attrs)
        attrs = re.sub(r'\sdata-wow-route="[^"]*"', '', attrs)
        return f'<body{attrs} data-wow="true" data-wow-route="{key}">'
    html, body_count = re.subn(r'<body\b([^>]*)>', body_repl, html, count=1, flags=re.I)
    if body_count != 1:
        raise SystemExit(f'stage133: body missing for {rel}')

    for token in REVEAL_CLASSES:
        html = add_class_token(html, token)

    html = re.sub(
        r'(/assets/stage105-final-ui\.css)\?v=[^\"\']+',
        rf'\1?v={css_digest}',
        html,
        flags=re.I,
    )
    script_tag = f'<script defer src="/assets/stage133-wow-motion.js?v={js_digest}"></script>'
    html = re.sub(r'<script\b[^>]*stage133-wow-motion\.js[^>]*></script>', '', html, flags=re.I)
    if '</body>' not in html:
        raise SystemExit(f'stage133: closing body missing for {rel}')
    html = html.replace('</body>', script_tag + '</body>', 1)
    path.write_text(html, encoding='utf-8')
    changed += 1

if changed < 30:
    raise SystemExit(f'stage133: expected >=30 art-directed pages, got {changed}')

print(f'stage133 cinematic system: pages={changed}; css={css_digest}; js={js_digest}; route accents + exhibition layouts + motion enabled')
