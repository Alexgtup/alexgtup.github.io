#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file(): raise SystemExit('stage237 home missing')
s=p.read_text(encoding='utf8')
s=re.sub(r'\s*<link[^>]+stage237-selected-work-showcase\.css[^>]*>','',s,flags=re.I)
s=re.sub(r'\sdata-stage237-cards="true"','',s)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage237-cards="true">',s,count=1,flags=re.I)
if n!=1: raise SystemExit('stage237 body missing')
s=s.replace('</head>','<link rel="stylesheet" href="/assets/stage237-selected-work-showcase.css"></head>',1)
p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
for needle in ['data-stage237-cards="true"','stage237-selected-work-showcase.css','p233-case-cap','p233-media-callout']:
 if needle not in f: raise SystemExit(f'stage237 guard {needle}')
if f.count('class="p233-case ')!=4: raise SystemExit('stage237 card count')
print('stage237 selected work showcase: stronger framed covers + glass neon cards')
