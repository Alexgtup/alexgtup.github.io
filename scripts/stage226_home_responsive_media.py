#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file(): raise SystemExit('stage226 home missing')
s=p.read_text(encoding='utf8')

def patch(src, srcset, sizes, width=None, height=None, occurrence=None):
    global s
    pat=re.compile(r'<img\b(?=[^>]*\bsrc="'+re.escape(src)+r'")[^>]*>',re.I)
    matches=list(pat.finditer(s))
    if not matches: raise SystemExit(f'stage226 image missing: {src}')
    targets=matches if occurrence is None else [matches[occurrence]]
    # Replace from right to left so offsets remain valid.
    for m in reversed(targets):
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

# Hero portrait cards: mobile/Lighthouse no longer downloads 720px when ~400px is enough.
patch('/assets/cases/fin-planner/fin-planner-card-01-720w.webp',
      '/assets/cases/fin-planner/fin-planner-card-01-400w.webp 400w, /assets/cases/fin-planner/fin-planner-card-01-440w.webp 440w, /assets/cases/fin-planner/fin-planner-card-01-720w.webp 720w',
      '(max-width: 650px) 58vw, (max-width: 980px) 42vw, 380px')
patch('/assets/cases/swift-calendar/calendar-card-01-720w.webp',
      '/assets/cases/swift-calendar/calendar-card-01-400w.webp 400w, /assets/cases/swift-calendar/calendar-card-01-720w.webp 720w',
      '(max-width: 650px) 52vw, (max-width: 980px) 38vw, 320px')

# Selected work: preserve originals for large/high-DPI screens, serve 800px derivatives otherwise.
patch('/assets/cases/wordpress-commercial/wordpress-commercial-01.webp',
      '/assets/cases/wordpress-commercial/wordpress-commercial-01-800w.webp 800w, /assets/cases/wordpress-commercial/wordpress-commercial-01.webp 1045w',
      '(max-width: 980px) calc(100vw - 28px), 58vw', width=1045, height=950)
patch('/assets/cases/seo-control-center/seo-control-center-live-01.webp',
      '/assets/cases/seo-control-center/seo-control-center-live-01-800w.webp 800w, /assets/cases/seo-control-center/seo-control-center-live-01.webp 1600w',
      '(max-width: 980px) calc(100vw - 28px), 50vw')
# SheetPilot appears in hero + selected work. Both are safely covered by 800/1600 candidates.
patch('/assets/cases/sheetpilot-ai/sheetpilot-live-01.webp',
      '/assets/cases/sheetpilot-ai/sheetpilot-live-01-800w.webp 800w, /assets/cases/sheetpilot-ai/sheetpilot-live-01.webp 1600w',
      '(max-width: 980px) calc(100vw - 28px), 50vw')

p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
expected=[
'fin-planner-card-01-400w.webp 400w',
'calendar-card-01-400w.webp 400w',
'wordpress-commercial-01-800w.webp 800w',
'seo-control-center-live-01-800w.webp 800w',
'sheetpilot-live-01-800w.webp 800w',
]
for needle in expected:
    if needle not in f: raise SystemExit(f'stage226 guard missing {needle}')
if f.count('srcset=') < 5: raise SystemExit('stage226 srcset count')
for asset in [
'assets/cases/fin-planner/fin-planner-card-01-400w.webp',
'assets/cases/fin-planner/fin-planner-card-01-440w.webp',
'assets/cases/swift-calendar/calendar-card-01-400w.webp',
'assets/cases/wordpress-commercial/wordpress-commercial-01-800w.webp',
'assets/cases/seo-control-center/seo-control-center-live-01-800w.webp',
'assets/cases/sheetpilot-ai/sheetpilot-live-01-800w.webp']:
    if not (ROOT/asset).is_file(): raise SystemExit(f'stage226 derivative missing: {asset}')
print('stage226 home responsive media: hero=2, wide=3 families, originals retained as srcset fallback')
