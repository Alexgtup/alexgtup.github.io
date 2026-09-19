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
# Match the approved mock navigation on the homepage only.
desktop='<nav class="stage98-nav" aria-label="Основная навигация"><a href="/cases/">Кейсы</a><a href="/services/">Услуги</a><a href="/guides/">Разборы</a><a href="/demos/">Демо</a><a href="/tools/">Инструменты</a><a href="/about/">Обо мне</a><a class="stage98-cta" href="https://t.me/Alexuys" rel="noopener noreferrer" target="_blank">Обсудить проект ↗</a></nav>'
s,n=re.subn(r'<nav class="stage98-nav"[^>]*>.*?</nav>',desktop,s,count=1,flags=re.S|re.I)
if n!=1: raise SystemExit('stage229 desktop nav missing')
mobile='<nav aria-label="Мобильная навигация"><a href="/cases/">Кейсы</a><a href="/services/">Услуги</a><a href="/guides/">Разборы</a><a href="/demos/">Демо</a><a href="/tools/">Инструменты</a><a href="/about/">Обо мне</a><a class="stage98-mobile-cta" href="https://t.me/Alexuys" rel="noopener noreferrer" target="_blank">Обсудить проект ↗</a></nav>'
s,n=re.subn(r'<nav aria-label="Мобильная навигация">.*?</nav>',mobile,s,count=1,flags=re.S|re.I)
if n!=1: raise SystemExit('stage229 mobile nav missing')
p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
for needle in ['data-stage226-home="true"','data-stage228-home="true"','data-stage229-home="true"','stage229-home-reference-layout.css','p128-work-list','p128-cap__list','stage174-popular','stage173-map','p128-proof','p128-start','href="/demos/">Демо','href="/tools/">Инструменты']:
 if needle not in f: raise SystemExit(f'stage229 guard {needle}')
if f.count('stage229-home-reference-layout.css')!=1: raise SystemExit('stage229 duplicate stylesheet')
if f.count('data-stage223-rank=')!=4: raise SystemExit('stage229 selected-work contract')
print('stage229 homepage reference layout: compact hero, asymmetric 2x2 work, bento capabilities, dark continuation, rail removed')
