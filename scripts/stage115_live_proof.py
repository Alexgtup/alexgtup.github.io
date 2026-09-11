#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BUNDLE = ROOT / 'assets' / 'stage105-final-ui.css'
HOME = ROOT / 'index.html'
MARK = '/* stage115-live-proof */'

LIVE_CASES = {
    'cases/seo-control-center/index.html': ('https://seo-control-center-prod2.onrender.com/demo', 'Открыть рабочее демо ↗'),
    'cases/sheetpilot-ai/index.html': ('https://sheetpilot-ai-6omr.onrender.com', 'Открыть рабочее демо ↗'),
    'cases/siteaudit-studio/index.html': ('https://siteaudit-studio.onrender.com/', 'Открыть рабочий сервис ↗'),
    'cases/freelance-os/index.html': ('/freelance-os/', 'Открыть FreelanceOS ↗'),
}

CSS = r'''
/* stage115-live-proof */
.s115-live-proof{
  position:relative!important;
  border-color:color-mix(in srgb,var(--ds-accent,#c9ff4a) 62%,transparent)!important;
  background:color-mix(in srgb,var(--ds-accent,#c9ff4a) 10%,var(--ds-surface,#111318))!important;
  color:var(--ds-text,#f3f5f7)!important;
  box-shadow:0 12px 30px rgba(0,0,0,.09);
}
.s115-live-proof::before{
  content:"";width:.44rem;height:.44rem;border-radius:50%;
  background:var(--ds-accent,#c9ff4a);box-shadow:0 0 0 .25rem color-mix(in srgb,var(--ds-accent,#c9ff4a) 13%,transparent);
}
.s115-live-proof:hover{transform:translateY(-1px);border-color:var(--ds-accent,#c9ff4a)!important}
.s113-review-meta{margin-top:auto;padding:0;border:0;background:none!important}
.s113-review-meta cite{display:block;font-style:normal;font-weight:800}
.s113-review-meta time{display:block;margin-top:.28rem;color:var(--ds-muted,#9ca2aa);font-size:.78rem}

/* A live case should visually announce verifiability in the first screen. */
body[data-ux-family="case"] :is(.hero,.s51-hero):has(.s115-live-proof){position:relative}
body[data-ux-family="case"] :is(.hero,.s51-hero):has(.s115-live-proof)::after{
  content:"LIVE · МОЖНО ПРОВЕРИТЬ";
  position:absolute;right:clamp(1rem,4vw,4.5rem);top:1.1rem;
  color:var(--ds-accent,#c9ff4a);
  font:800 .61rem/1 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  letter-spacing:.075em;
}
@media(max-width:820px){
  body[data-ux-family="case"] :is(.hero,.s51-hero):has(.s115-live-proof)::after{display:none}
  .s115-live-proof{width:100%}
}
'''

if not BUNDLE.is_file() or not HOME.is_file():
    raise SystemExit('stage115: final bundle/home missing')

# Semantic cleanup: review attribution is card metadata, not a second page footer.
home = HOME.read_text(encoding='utf-8')
review_pattern = re.compile(
    r'(<article class="s113-review-card"><blockquote>.*?</blockquote>)<footer>(.*?)</footer>(</article>)',
    re.S,
)
home, review_fixed = review_pattern.subn(r'\1<div class="s113-review-meta">\2</div>\3', home)
if review_fixed != 3:
    raise SystemExit(f'stage115: expected 3 review metadata fixes, got {review_fixed}')
HOME.write_text(home, encoding='utf-8')


def insert_live_action(html: str, href: str, label: str) -> tuple[str, bool]:
    if 's115-live-proof' in html:
        return html, False
    external = href.startswith('http')
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
    # Keep the button compatible with all three case hero families while adding
    # one shared class for visual emphasis.
    if 'class="stage94-hero-actions"' in html:
        tag = f'<a class="stage94-action-secondary s115-live-proof" href="{href}"{attrs}>{label}</a>'
        pattern = re.compile(r'(<div class="stage94-hero-actions">)')
    elif 'class="s51-actions"' in html:
        tag = f'<a class="s51-btn s115-live-proof" href="{href}"{attrs}>{label}</a>'
        pattern = re.compile(r'(<div class="s51-actions">)')
    elif 'class="actions"' in html:
        tag = f'<a class="btn s115-live-proof" href="{href}"{attrs}>{label}</a>'
        pattern = re.compile(r'(<div class="actions">)')
    else:
        raise SystemExit('stage115: no known hero action family')
    new, count = pattern.subn(r'\1' + tag, html, count=1)
    return new, count == 1

patched = []
for rel, (href, label) in LIVE_CASES.items():
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f'stage115: missing case {rel}')
    html = path.read_text(encoding='utf-8')
    html, changed = insert_live_action(html, href, label)
    if not changed:
        raise SystemExit(f'stage115: live action not inserted on {rel}')
    path.write_text(html, encoding='utf-8')
    patched.append(rel)

bundle = BUNDLE.read_text(encoding='utf-8')
if MARK not in bundle:
    BUNDLE.write_text(bundle.rstrip() + '\n\n' + CSS.strip() + '\n', encoding='utf-8')

bundle = BUNDLE.read_text(encoding='utf-8')
digest = hashlib.sha256(bundle.encode('utf-8')).hexdigest()[:12]
href_re = re.compile(r'(/assets/stage105-final-ui\.css)\?v=[^"\']+', re.I)
refs = 0
for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    new, count = href_re.subn(rf'\1?v={digest}', html)
    refs += count
    if new != html:
        path.write_text(new, encoding='utf-8')
if refs < 70:
    raise SystemExit(f'stage115: only {refs} final UI refs rotated')

# Guards: buttons are first-screen actions and old review footer markup is gone.
if '<article class="s113-review-card"' not in HOME.read_text(encoding='utf-8'):
    raise SystemExit('stage115: reviews section disappeared')
if re.search(r's113-review-card.*?<footer>', HOME.read_text(encoding='utf-8'), re.S):
    raise SystemExit('stage115: nested review footer remains')
for rel, (href, _) in LIVE_CASES.items():
    html = (ROOT / rel).read_text(encoding='utf-8')
    hero_end = html.find('</section>', html.find('<section'))
    hero = html[:hero_end] if hero_end > 0 else html
    if 's115-live-proof' not in hero or href not in hero:
        raise SystemExit(f'stage115: live proof not in hero on {rel}')

print(
    f'stage115 live proof: review_semantics={review_fixed}; live_cases={len(patched)}; '
    f'cache_refs={refs}; bundle={digest}; guards OK'
)
