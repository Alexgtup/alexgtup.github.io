#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file(): raise SystemExit('stage232 home missing')
s=p.read_text(encoding='utf8')
# idempotent cleanup
s=re.sub(r'\s*<meta[^>]+data-stage232-cache[^>]*>','',s,flags=re.I)
s=re.sub(r'\sdata-stage232-build="[^"]+"','',s)
# Browser-side hints are intentionally homepage-only; assets are already content-hashed.
meta='''<meta data-stage232-cache="true" http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"><meta data-stage232-cache="true" http-equiv="Pragma" content="no-cache"><meta data-stage232-cache="true" http-equiv="Expires" content="0">'''
if '</head>' not in s: raise SystemExit('stage232 head missing')
s=s.replace('</head>',meta+'</head>',1)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage232-build="reference-images-236">',s,count=1,flags=re.I)
if n!=1: raise SystemExit('stage232 body missing')
# Version the three visual assets at the HTML/CSS edge as well so a stale asset cache cannot mask a new scene.
s=s.replace('/assets/home-system-reference.webp"','/assets/home-system-reference.webp?v=236"')
p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
for needle in ['data-stage232-build="reference-images-236"','data-stage232-cache="true"','home-system-reference.webp?v=236']:
 if needle not in f: raise SystemExit(f'stage232 guard {needle}')
print('stage232 homepage cache bust: no-store hints + explicit svg-world build marker')
