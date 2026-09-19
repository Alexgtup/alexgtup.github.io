#!/usr/bin/env python3
from pathlib import Path
import re,sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
css=ROOT/'assets'/'stage240-site-contrast.css'
if not css.is_file():
    raise SystemExit('stage240 css missing')

count=0
for p in ROOT.rglob('*.html'):
    s=p.read_text(encoding='utf8',errors='ignore')
    if '</head>' not in s:
        continue
    s=re.sub(r'\s*<link[^>]+stage240-site-contrast\.css[^>]*>','',s,flags=re.I)
    s=s.replace('</head>','<link rel="stylesheet" href="/assets/stage240-site-contrast.css?v=2401"></head>',1)
    p.write_text(s,encoding='utf8')
    count+=1

if count < 20:
    raise SystemExit(f'stage240 too few html files: {count}')
print(f'stage240 contrast QA applied to {count} html files')
