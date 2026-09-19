#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file(): raise SystemExit('stage226 media: home missing')
s=p.read_text(encoding='utf8')

# This stage runs after the Stage226 masterpiece rebuild. Hero previews already use
# compact derivatives at CSS sizes ~62-72px; only large Selected Work media need
# responsive candidates. Do not depend on the retired Swift/legacy hero collage.
def patch(src, srcset, sizes, width=None, height=None):
    global s
    pat=re.compile(r'<img\b(?=[^>]*\bsrc="'+re.escape(src)+r'")[^>]*>',re.I)
    matches=list(pat.finditer(s))
    if not matches: raise SystemExit(f'stage226 media image missing: {src}')
    for m in reversed(matches):
        tag=m.group(0)
        tag=re.sub(r'\s+(?:srcset|sizes)="[^"]*"','',tag,flags=re.I)
        if width is not None:
            tag=re.sub(r'\s+width="[^"]*"','',tag,flags=re.I)
            tag=tag[:-1]+f' width="{width}">'
        if height is not None:
            tag=re.sub(r'\s+height="[^"]*"','',tag,flags=re.I)
            tag=tag[:-1]+f' height="{height}">'
        tag=tag[:-1]+f' srcset="{srcset}" sizes="{sizes}">'
        s=s[:m.start()]+tag+s[m.end():]

# Selected Work is 4-up desktop / 1-up mobile after Stage226.
patch('/assets/cases/wordpress-commercial/wordpress-commercial-01.webp',
      '/assets/cases/wordpress-commercial/wordpress-commercial-01-800w.webp 800w, /assets/cases/wordpress-commercial/wordpress-commercial-01.webp 1045w',
      '(max-width: 680px) calc(100vw - 24px), (max-width: 1180px) calc(50vw - 28px), 25vw', width=1045, height=950)
patch('/assets/cases/seo-control-center/seo-control-center-live-01.webp',
      '/assets/cases/seo-control-center/seo-control-center-live-01-800w.webp 800w, /assets/cases/seo-control-center/seo-control-center-live-01.webp 1600w',
      '(max-width: 680px) calc(100vw - 24px), (max-width: 1180px) calc(50vw - 28px), 25vw')
patch('/assets/cases/sheetpilot-ai/sheetpilot-live-01.webp',
      '/assets/cases/sheetpilot-ai/sheetpilot-live-01-800w.webp 800w, /assets/cases/sheetpilot-ai/sheetpilot-live-01.webp 1600w',
      '(max-width: 680px) calc(100vw - 24px), (max-width: 1180px) calc(50vw - 28px), 25vw')

p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
# New hero contract: five live route panels, four image-backed previews, no legacy Swift shot.
for needle in ['p226-panel--telegram','p226-panel--automation','p226-panel--analytics','p226-panel--wordpress','p226-panel--data']:
    if needle not in f: raise SystemExit(f'stage226 media hero guard missing {needle}')
if 'calendar-card-01-720w.webp' in f: raise SystemExit('stage226 media legacy Swift hero survived')
for needle in ['wordpress-commercial-01-800w.webp 800w','seo-control-center-live-01-800w.webp 800w','sheetpilot-live-01-800w.webp 800w']:
    if needle not in f: raise SystemExit(f'stage226 media srcset guard missing {needle}')
for asset in [
'assets/cases/fin-planner/fin-planner-card-01-400w.webp',
'assets/cases/wordpress-commercial/wordpress-commercial-01-800w.webp',
'assets/cases/seo-control-center/seo-control-center-live-01-800w.webp',
'assets/cases/sheetpilot-ai/sheetpilot-live-01-800w.webp']:
    if not (ROOT/asset).is_file(): raise SystemExit(f'stage226 media derivative missing: {asset}')
print('stage226 home responsive media: new hero=5 panels, selected-work=3 responsive families, legacy Swift dependency retired')
