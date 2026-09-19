#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file(): raise SystemExit('stage229 home missing')
s=p.read_text(encoding='utf8')
s=re.sub(r'\s*<link[^>]+stage229-home-reference-layout\.css[^>]*>','',s,flags=re.I)
s=re.sub(r'\sdata-stage229-home="true"','',s)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage229-home="true">',s,count=1,flags=re.I)
if n!=1: raise SystemExit('stage229 body missing')
s=s.replace('</head>','<link rel="stylesheet" href="/assets/stage229-home-reference-layout.css"></head>',1)
p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
for needle in ['data-stage226-home="true"','data-stage228-home="true"','data-stage229-home="true"','stage229-home-reference-layout.css','p128-work-list','p128-cap__list','stage174-popular','stage173-map','p128-proof','p128-start']:
 if needle not in f: raise SystemExit(f'stage229 guard {needle}')
if f.count('stage229-home-reference-layout.css')!=1: raise SystemExit('stage229 duplicate stylesheet')
if f.count('data-stage223-rank=')!=4: raise SystemExit('stage229 selected-work contract')
print('stage229 homepage reference layout: compact hero, asymmetric 2x2 work, bento capabilities, dark continuation, rail removed')
