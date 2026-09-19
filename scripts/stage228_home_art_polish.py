#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file(): raise SystemExit('stage228 home missing')
s=p.read_text(encoding='utf8')
s=re.sub(r'\s*<link[^>]+stage228-home-art-polish\.css[^>]*>','',s,flags=re.I)
s=re.sub(r'\sdata-stage228-home="true"','',s)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage228-home="true">',s,count=1,flags=re.I)
if n!=1: raise SystemExit('stage228 body missing')
s=s.replace('</head>','<link rel="stylesheet" href="/assets/stage228-home-art-polish.css"></head>',1)
p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
for needle in ['data-stage226-home="true"','data-stage228-home="true"','stage228-home-art-polish.css','p226-core','p226-panel--telegram','p226-panel--automation','p226-panel--analytics','p226-panel--wordpress','p226-panel--data']:
 if needle not in f: raise SystemExit(f'stage228 guard {needle}')
if f.count('stage228-home-art-polish.css')!=1: raise SystemExit('stage228 duplicate stylesheet')
print('stage228 home art polish: core-depth, panel accents, real-project framing, below-fold containment')
