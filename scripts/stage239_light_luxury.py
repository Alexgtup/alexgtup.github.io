#!/usr/bin/env python3
from pathlib import Path
import re,sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file():
    raise SystemExit('stage239 home missing')

s=p.read_text(encoding='utf8')
s=re.sub(r'\s*<link[^>]+stage239-light-luxury\.css[^>]*>','',s,flags=re.I)
s=re.sub(r'\sdata-stage239-light-luxury="true"','',s)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage239-light-luxury="true">',s,count=1,flags=re.I)
if n!=1:
    raise SystemExit('stage239 body missing')

# Homepage is now intentionally light.
s=re.sub(r'<meta\s+content="dark"\s+name="color-scheme"\s*/?>','<meta content="light" name="color-scheme"/>',s,count=1,flags=re.I)
s=re.sub(r'<meta\s+content="#08090b"\s+name="theme-color"\s*/?>','<meta content="#f2f1ed" name="theme-color"/>',s,count=1,flags=re.I)
s=s.replace('</head>','<link rel="stylesheet" href="/assets/stage239-light-luxury.css?v=2396"></head>',1)
p.write_text(s,encoding='utf8')

f=p.read_text(encoding='utf8')
for needle in [
    'data-stage239-light-luxury="true"',
    'stage239-light-luxury.css?v=2396',
    'content="light" name="color-scheme"',
    'content="#f2f1ed" name="theme-color"',
    'data-stage238-home-cards="true"'
]:
    if needle not in f:
        raise SystemExit(f'stage239 guard {needle}')

asset=ROOT/'assets'/'home-light-luxury.webp'
if not asset.is_file() or asset.stat().st_size < 5000:
    raise SystemExit('stage239 background asset missing/too small')

print('stage239 light luxury homepage: approved generated background + light glass visual system')
