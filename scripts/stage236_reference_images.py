#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file(): raise SystemExit('stage236 home missing')
s=p.read_text(encoding='utf8')
s=re.sub(r'\sdata-stage236-reference="[^"]+"','',s)
s=re.sub(r'\s*<link[^>]+data-stage236-preload[^>]*>','',s,flags=re.I)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage236-reference="exact-user-images">',s,count=1,flags=re.I)
if n!=1: raise SystemExit('stage236 body missing')
# Normalize hero source to the exact user-provided image derivative.
s=re.sub(r'/assets/(?:stage235-crystal-system\.svg|home-system-reference\.webp)(?:\?[^"\']*)?', '/assets/home-system-reference.webp?v=236', s)
preloads='<link data-stage236-preload rel="preload" as="image" href="/assets/home-space-reference.webp" fetchpriority="high"><link data-stage236-preload rel="preload" as="image" href="/assets/home-system-reference.webp?v=236" fetchpriority="high">'
if '</head>' not in s: raise SystemExit('stage236 head missing')
s=s.replace('</head>',preloads+'</head>',1)
p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
for needle in ['data-stage236-reference="exact-user-images"','home-system-reference.webp?v=236','data-stage233-home="true"']:
    if needle not in f: raise SystemExit(f'stage236 guard {needle}')
for old in ['stage235-crystal-system.svg','stage231-hero-installation.svg']:
    if old in f: raise SystemExit(f'stage236 old hero survived {old}')
for asset in ['home-space-reference.webp','home-system-reference.webp','home-mountains-reference.webp']:
    if not (ROOT/'assets'/asset).is_file(): raise SystemExit(f'stage236 asset missing {asset}')
print('stage236 exact reference images: uploaded space + system + mountains active')
