#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file(): raise SystemExit('stage235 home missing')
s=p.read_text(encoding='utf8')
s=re.sub(r'\sdata-stage235-assets="[^"]+"','',s)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage235-assets="reference-images-236">',s,count=1,flags=re.I)
if n!=1: raise SystemExit('stage235 body missing')
# Replace any legacy hero SVG URL, with or without query string.
s=re.sub(r'/assets/stage235-crystal-system\.svg(?:\?[^"\']*)?', '/assets/home-system-reference.webp?v=236', s)
s=re.sub(r'/assets/stage231-hero-installation\.svg(?:\?[^"\']*)?', '/assets/home-system-reference.webp?v=236', s)
p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
for needle in ['data-stage235-assets="reference-images-236"','home-system-reference.webp?v=236']:
 if needle not in f: raise SystemExit(f'stage235 guard {needle}')
if 'stage231-hero-installation.svg' in f: raise SystemExit('stage235 legacy hero svg survived')
print('stage235 asset swap: new cinematic hero active, legacy hero ref removed')
