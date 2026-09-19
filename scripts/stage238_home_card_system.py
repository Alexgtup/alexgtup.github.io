#!/usr/bin/env python3
from pathlib import Path
import re,sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file():
    raise SystemExit('stage238 home missing')

s=p.read_text(encoding='utf8')
s=re.sub(r'\s*<link[^>]+stage238-home-card-system\.css[^>]*>','',s,flags=re.I)
s=re.sub(r'\sdata-stage238-home-cards="true"','',s)
s,n=re.subn(
    r'<body\b([^>]*)>',
    lambda m:'<body'+m.group(1)+' data-stage238-home-cards="true">',
    s,count=1,flags=re.I
)
if n!=1:
    raise SystemExit('stage238 body missing')

s=s.replace('</head>','<link rel="stylesheet" href="/assets/stage238-home-card-system.css?v=2381"></head>',1)
p.write_text(s,encoding='utf8')

f=p.read_text(encoding='utf8')
for needle in [
    'data-stage238-home-cards="true"',
    'stage238-home-card-system.css?v=2381',
    'class="p233-work-grid"',
    'class="p233-build-grid"',
    'class="stage174-popular__links"',
    'class="stage173-grid"',
    'class="p128-proof__numbers"',
    'class="s44-brief p128-form"'
]:
    if needle not in f:
        raise SystemExit(f'stage238 guard {needle}')

print('stage238 homepage card system: projects 2x2 + unified build/task/proof/form cards')
