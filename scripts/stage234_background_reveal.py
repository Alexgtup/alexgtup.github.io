#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file(): raise SystemExit('stage234 home missing')
s=p.read_text(encoding='utf8')
s=re.sub(r'\s*<link[^>]+stage234-background-reveal\.css[^>]*>','',s,flags=re.I)
s=re.sub(r'\sdata-stage234-home="true"','',s)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage234-home="true">',s,count=1,flags=re.I)
if n!=1: raise SystemExit('stage234 body missing')
s=s.replace('</head>','<link rel="stylesheet" href="/assets/stage234-background-reveal.css?v=238"></head>',1)
p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
for needle in ['data-stage231-home="true"','data-stage233-home="true"','data-stage234-home="true"','stage234-background-reveal.css','home-system-reference.webp']:
 if needle not in f: raise SystemExit(f'stage234 guard {needle}')
print('stage234 background reveal: space/work/mountain SVG layers made explicit and visible')
