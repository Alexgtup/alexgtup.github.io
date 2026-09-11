#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BUNDLE = ROOT / 'assets' / 'stage105-final-ui.css'
MARK = '/* stage111-final-polish */'

CSS = r'''
/* stage111-final-polish */
/* Remove the last visual remnants of legacy horizontal rails and default link colour. */
body[data-ux-family="hub"] .dt-tool-card :is(h2,h3){
  color:var(--ds-text,#f3f5f7)!important;
}
body[data-ux-family="hub"] .dt-tool-card:hover :is(h2,h3){
  color:var(--ds-accent,#c9ff4a)!important;
}

/* Tools filter used to start at the viewport edge while the cards used the shared shell. */
body[data-ux-family="hub"] #tool-list>.ux-filterbar{
  width:var(--ds-shell,min(calc(100% - 2.4rem),1280px));
  max-width:1280px;
  margin-left:auto!important;
  margin-right:auto!important;
}

@media(max-width:820px){
  /* Catalog cards should never look accidentally cropped on a phone. The old
     84%-width rail intentionally exposed the next card, but on this portfolio it
     reads as a broken layout. Show complete cards instead. */
  body[data-ux-family="hub"] .ux-hub-main :is(
    .s50-case-list,.s50-guide-grid,.dt-grid,.growth-grid
  ){
    display:grid!important;
    grid-template-columns:1fr!important;
    overflow:visible!important;
    scroll-snap-type:none!important;
    padding-bottom:clamp(1.6rem,5vw,2.4rem)!important;
  }
  body[data-ux-family="hub"] .ux-hub-main :is(
    .s50-case-list,.s50-guide-grid,.dt-grid,.growth-grid
  )>*{
    flex:none!important;
    width:100%!important;
    min-width:0!important;
    max-width:100%!important;
    scroll-snap-align:none!important;
  }

  /* Filter controls are navigation, not a hidden carousel. Keep every option
     discoverable without requiring a sideways gesture. */
  body[data-ux-family="hub"] .ux-filterbar{
    flex-wrap:wrap!important;
    overflow:visible!important;
    overscroll-behavior:auto!important;
    gap:.38rem!important;
  }
  body[data-ux-family="hub"] .ux-filterbar__label{
    position:static!important;
    flex:0 0 100%!important;
    padding:0 0 .2rem!important;
    margin:0!important;
    background:none!important;
  }
  body[data-page="cases"] .case-filter__list{
    display:flex!important;
    flex-wrap:wrap!important;
    overflow:visible!important;
    gap:.35rem!important;
    padding-bottom:0!important;
  }
  body[data-page="cases"] .case-filter__list button{
    flex:1 1 calc(50% - .35rem)!important;
    width:auto!important;
    min-width:0!important;
    justify-content:space-between!important;
  }

  /* Discovery chips previously formed another clipped one-line rail below the
     actual content. Wrap them so the final CTA remains visually connected. */
  body[data-ux-family] main>.s103-discovery{
    flex-wrap:wrap!important;
    overflow:visible!important;
    overscroll-behavior:auto!important;
    gap:.4rem!important;
  }
  body[data-ux-family] main>.s103-discovery a{
    flex:0 1 auto!important;
    min-width:0!important;
    max-width:100%!important;
    white-space:normal!important;
    text-align:left!important;
  }
}

@media(max-width:520px){
  body[data-page="cases"] .case-filter__list button{
    flex-basis:100%!important;
  }
  body[data-ux-family="hub"] #tool-list>.ux-filterbar{
    width:min(calc(100% - 2rem),1280px)!important;
  }
}
'''

if not BUNDLE.is_file():
    raise SystemExit('stage111: final UI bundle missing')

text = BUNDLE.read_text(encoding='utf-8')
if MARK not in text:
    text = text.rstrip() + '\n\n' + CSS.strip() + '\n'
    BUNDLE.write_text(text, encoding='utf-8')

bundle_text = BUNDLE.read_text(encoding='utf-8')
digest = hashlib.sha256(bundle_text.encode('utf-8')).hexdigest()[:12]
href_re = re.compile(r'(/assets/stage105-final-ui\.css)\?v=[^"\']+', re.I)

pages = 0
refs = 0
for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<body' not in html:
        continue
    pages += 1
    new, count = href_re.subn(rf'\1?v={digest}', html)
    refs += count
    if new != html:
        path.write_text(new, encoding='utf-8')

problems: list[str] = []
styles = BUNDLE.read_text(encoding='utf-8')
for required in (
    MARK,
    '#tool-list>.ux-filterbar',
    '.dt-tool-card:hover :is(h2,h3)',
    'body[data-page="cases"] .case-filter__list',
    'main>.s103-discovery',
):
    if required not in styles:
        problems.append(f'missing final polish guard: {required}')

tools = ROOT / 'tools' / 'index.html'
if not tools.is_file():
    problems.append('tools hub missing')
else:
    tool_html = tools.read_text(encoding='utf-8')
    cards = len(re.findall(r'class=["\'][^"\']*\bdt-tool-card\b', tool_html, re.I))
    if cards != 6:
        problems.append(f'tools hub card count={cards}, expected 6')

if refs < 70:
    problems.append(f'only {refs} final UI references rotated')

if problems:
    raise SystemExit('stage111 final polish failed:\n' + '\n'.join(problems))

print(f'stage111 final polish: pages={pages}; cache_refs={refs}; bundle={digest}; mobile rails removed; tool/filter/discovery polish OK')
