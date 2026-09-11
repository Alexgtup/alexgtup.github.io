#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BUNDLE = ROOT / 'assets' / 'stage105-final-ui.css'
MARK = '/* stage114-service-proof */'
PROFILE = 'https://freelance.ru/gglalex'
REVIEWS = 'https://freelance.ru/reviews/gglalex/'

CSS = r'''
/* stage114-service-proof */
/* Search visitors should see independent proof before deciding whether to scroll. */
.s114-proofbar{
  margin-top:1rem;
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:.55rem;
  max-width:46rem;
}
.s114-proofbar>a,.s114-proofbar>div{
  position:relative;
  min-width:0;
  min-height:4.25rem;
  display:flex;
  flex-direction:column;
  justify-content:center;
  padding:.72rem .82rem;
  border:1px solid var(--ds-line,rgba(255,255,255,.1));
  border-radius:.92rem;
  background:color-mix(in srgb,var(--ds-surface,#111318) 88%,transparent);
  text-decoration:none;
  transition:border-color .18s ease,transform .18s ease,background .18s ease;
}
.s114-proofbar>a:hover{
  transform:translateY(-1px);
  border-color:color-mix(in srgb,var(--ds-accent,#c9ff4a) 50%,var(--ds-line,rgba(255,255,255,.1)));
  background:color-mix(in srgb,var(--ds-surface,#111318) 82%,var(--ds-accent,#c9ff4a) 5%);
}
.s114-proofbar strong{
  display:block;
  color:var(--ds-text,#f3f5f7);
  font-size:.97rem;
  line-height:1.15;
  letter-spacing:-.025em;
}
.s114-proofbar span{
  display:block;
  margin-top:.22rem;
  color:var(--ds-muted,#9ca2aa);
  font-size:.72rem;
  line-height:1.3;
}
.s114-proofbar>a:first-child::after{
  content:"↗";
  position:absolute;
  right:.72rem;
  top:.62rem;
  color:var(--ds-accent,#c9ff4a);
  font-size:.78rem;
  font-weight:900;
}
.s114-proofbar__verified span::before{
  content:"●";
  margin-right:.3rem;
  color:var(--ds-accent,#c9ff4a);
  font-size:.64em;
  vertical-align:.12em;
}

/* Keep the service hero facts as secondary technical context after human proof. */
.s48-hero .s48-facts{margin-top:.72rem!important}

@media(max-width:820px){
  .s114-proofbar{grid-template-columns:1fr 1fr;gap:.45rem;margin-top:.85rem}
  .s114-proofbar>a:first-child{grid-column:1/-1}
  .s114-proofbar>a,.s114-proofbar>div{min-height:3.85rem;padding:.68rem .75rem;border-radius:.82rem}
  .s114-proofbar strong{font-size:.92rem}
}

@media(max-width:430px){
  .s114-proofbar{grid-template-columns:1fr}
  .s114-proofbar>a:first-child{grid-column:auto}
  .s114-proofbar>a,.s114-proofbar>div{min-height:3.6rem}
}
'''

if not BUNDLE.is_file():
    raise SystemExit('stage114: final UI bundle missing')

case_count = len(list((ROOT / 'cases').glob('*/index.html')))
if case_count < 8:
    raise SystemExit(f'stage114: case inventory too small: {case_count}')

proof = f'''<div class="s114-proofbar" aria-label="Независимое подтверждение опыта">
<a class="s114-proofbar__verified" href="{REVIEWS}" target="_blank" rel="noopener noreferrer"><strong>20 отзывов · 9/10</strong><span>публичная репутация на Freelance.ru</span></a>
<a href="/cases/"><strong>{case_count} кейсов</strong><span>задача, логика и реализация</span></a>
<div><strong>6 лет опыта</strong><span>разработка и доработка проектов</span></div>
</div>'''

patched: list[str] = []
for path in sorted(ROOT.glob('*/index.html')):
    rel = path.relative_to(ROOT).as_posix()
    html = path.read_text(encoding='utf-8', errors='ignore')
    if 'class="s48-hero"' not in html or 'class="s48-actions"' not in html:
        continue
    if 'class="s114-proofbar"' in html:
        continue
    # s48-actions contains only anchors, so its closing div is a stable insertion point.
    pattern = re.compile(r'(<div class="s48-actions">.*?</div>)(\s*<div class="s48-facts">)', re.S)
    new, count = pattern.subn(r'\1\n' + proof + r'\2', html, count=1)
    if count != 1:
        raise SystemExit(f'stage114: could not place proofbar on {rel}')
    path.write_text(new, encoding='utf-8')
    patched.append(rel)

if len(patched) < 12:
    raise SystemExit(f'stage114: only {len(patched)} RU service pages patched')

bundle_text = BUNDLE.read_text(encoding='utf-8')
if MARK not in bundle_text:
    BUNDLE.write_text(bundle_text.rstrip() + '\n\n' + CSS.strip() + '\n', encoding='utf-8')

# Rotate shared UI cache references after appending this final-build CSS.
bundle_text = BUNDLE.read_text(encoding='utf-8')
digest = hashlib.sha256(bundle_text.encode('utf-8')).hexdigest()[:12]
href_re = re.compile(r'(/assets/stage105-final-ui\.css)\?v=[^"\']+', re.I)
refs = 0
for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    new, count = href_re.subn(rf'\1?v={digest}', html)
    refs += count
    if new != html:
        path.write_text(new, encoding='utf-8')
if refs < 70:
    raise SystemExit(f'stage114: only {refs} final UI refs rotated')

# Guard the most valuable current organic entry pages explicitly.
priority = [
    'telegram-bots/index.html',
    'web-development/index.html',
    'project-repair/index.html',
    'n8n-automation/index.html',
    'api-integrations/index.html',
]
for rel in priority:
    html = (ROOT / rel).read_text(encoding='utf-8')
    if html.count('class="s114-proofbar"') != 1:
        raise SystemExit(f'stage114: proofbar guard failed on {rel}')
    if REVIEWS not in html or f'>{case_count} кейсов<' not in html:
        raise SystemExit(f'stage114: proof content guard failed on {rel}')

print(
    f'stage114 service proof: patched={len(patched)}; cases={case_count}; '
    f'priority={len(priority)}; cache_refs={refs}; bundle={digest}; guards OK'
)
