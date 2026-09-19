#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
CFG={
 'wordpress-commercial':{
  'index':'01','type':'WORDPRESS / PRODUCTION','surface':'Действующий коммерческий сайт','scope':'Формы · калькуляторы · mobile','output':'Точечная доработка без rewrite','note':'Рабочая основа сохранена','detail':'Новые блоки и исправления встроены в существующий WordPress-контур.'},
 'fin-planner':{
  'index':'02','type':'TELEGRAM / PRODUCT','surface':'Реальный интерфейс Telegram','scope':'Доходы · расходы · отчёты','output':'Состояния · данные · backend','note':'Telegram — основной интерфейс','detail':'Кейс показывает реальные экраны и пользовательские сценарии продукта.'},
 'portfolio-site':{
  'index':'04','type':'WEB / PRODUCT SYSTEM','surface':'Многостраничный portfolio product','scope':'Cases · services · responsive','output':'SEO · schema · internal graph','note':'Portfolio как система','detail':'Контент, навигация, кейсы и поисковая структура работают как один продукт.'},
}
CSS='<link rel="stylesheet" href="/assets/stage217-flagship-cases.css">'
for slug,c in CFG.items():
 p=ROOT/'cases'/slug/'index.html'
 if not p.is_file():raise SystemExit(f'stage217 missing {slug}')
 s=p.read_text(encoding='utf8')
 # idempotent cleanup
 s=re.sub(r'\s*<link[^>]+stage217-flagship-cases\.css[^>]*>','',s,flags=re.I)
 s=re.sub(r'\sdata-stage217-flagship="[^"]+"','',s)
 s=re.sub(r'\s*<div class="p217-manifest">.*?</div>\s*</div>','',s,flags=re.S)
 s=re.sub(r'\s*<div class="p217-flagship-note">.*?</div>','',s,flags=re.S)
 s=re.sub(r'\s*<div class="p217-coordinates">.*?</div>','',s,flags=re.S)
 s=re.sub(r'\s*<span class="p217-real-badge">.*?</span>','',s,flags=re.S)
 s=re.sub(r'\s*<span class="p217-screen-shade"[^>]*></span>','',s,flags=re.S)
 s=s.replace(' p217-frame','').replace(' p217-hero-shell','')
 s=re.sub(r'\sdata-p217-index="[^"]+"','',s)
 # body flag and CSS
 s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+f' data-stage217-flagship="{slug}">',s,count=1,flags=re.I)
 if n!=1:raise SystemExit(f'stage217 body missing {slug}')
 if '</head>' not in s:raise SystemExit(f'stage217 head missing {slug}')
 s=s.replace('</head>',CSS+'</head>',1)
 manifest=(f'<div class="p217-manifest"><div><small>PROJECT / {c["index"]}</small><strong>{c["type"]}</strong></div>'
           f'<div><small>SURFACE</small><strong>{c["surface"]}</strong></div>'
           f'<div><small>SCOPE</small><strong>{c["scope"]}</strong></div>'
           f'<div><small>OUTPUT</small><strong>{c["output"]}</strong></div></div>')
 if slug=='fin-planner':
  # mark cinematic cover + add manifest immediately after it
  s,n=re.subn(r'<section\b(?=[^>]*class="[^"]*p132-cover[^"]*p155-cover[^"]*")([^>]*)>',lambda m:'<section'+m.group(1).replace('p132-cover p155-cover','p132-cover p155-cover p217-hero-shell')+f' data-p217-index="{c["index"]}">',s,count=1,flags=re.I)
  if n!=1:raise SystemExit('stage217 fin cover opening missing')
  m=re.search(r'<section\b(?=[^>]*class="[^"]*p217-hero-shell[^"]*")[^>]*>.*?</section>',s,re.S|re.I)
  if not m:raise SystemExit('stage217 fin cover missing')
  s=s[:m.end()]+manifest+s[m.end():]
  # frame the existing real screenshot and annotate it without replacing the real UI.
  s=s.replace('<div class="p132-cover-visual">','<div class="p132-cover-visual p217-frame"><span class="p217-screen-shade" aria-hidden="true"></span>',1)
  insert=(f'<div class="p217-coordinates"><span class="p217-coordinate-accent">REAL UI</span><span>TELEGRAM</span><span>PRODUCT</span></div>'
          f'<div class="p217-flagship-note"><small>PROOF / SCREEN</small><strong>{c["note"]}</strong><span>{c["detail"]}</span></div>')
  pat=r'(<div class="p132-cover-visual p217-frame">.*?<span class="p132-cover-tag">.*?</span>)(</div>)'
  s,n=re.subn(pat,lambda m:m.group(1)+insert+m.group(2),s,count=1,flags=re.S)
  if n!=1:raise SystemExit('stage217 fin visual annotation failed')
  # badge in cover copy before h1
  s=s.replace('<h1>',f'<span class="p217-real-badge">REAL PROJECT · {c["type"]}</span><h1>',1)
 else:
  # legacy case hero
  s=s.replace('<section class="hero">',f'<section class="hero p217-hero-shell" data-p217-index="{c["index"]}">',1)
  m=re.search(r'<section class="hero p217-hero-shell".*?</section>',s,re.S)
  if not m:raise SystemExit(f'stage217 hero missing {slug}')
  s=s[:m.end()]+manifest+s[m.end():]
  s=s.replace('<div class="hero-visual">','<div class="hero-visual p217-frame"><span class="p217-screen-shade" aria-hidden="true"></span>',1)
  # add frame metadata just before hero-visual closes, identified by image then div close
  pat=r'(<div class="hero-visual p217-frame">.*?<img[^>]+>)(</div>)'
  note=(f'<div class="p217-coordinates"><span class="p217-coordinate-accent">REAL SCREEN</span><span>{c["index"]} / 13</span><span>PRODUCTION</span></div>'
        f'<div class="p217-flagship-note"><small>PROOF / SCREEN</small><strong>{c["note"]}</strong><span>{c["detail"]}</span></div>')
  s,n=re.subn(pat,lambda m:m.group(1)+note+m.group(2),s,count=1,flags=re.S)
  if n!=1:raise SystemExit(f'stage217 visual metadata failed {slug}')
  s=s.replace('<h1>',f'<span class="p217-real-badge">REAL PROJECT · {c["type"]}</span><h1>',1)
 p.write_text(s,encoding='utf8')
# Guards
for slug,c in CFG.items():
 s=(ROOT/'cases'/slug/'index.html').read_text(encoding='utf8')
 for needle in [f'data-stage217-flagship="{slug}"','stage217-flagship-cases.css','p217-manifest','p217-real-badge','p217-frame','p217-flagship-note',c['type']]:
  if needle not in s:raise SystemExit(f'stage217 guard {slug}: {needle}')
 if s.count('stage217-flagship-cases.css')!=1 or s.count('p217-manifest')<1:raise SystemExit(f'stage217 duplicate guard {slug}')
print('stage217 flagship cases: wordpress-commercial, fin-planner, portfolio-site')
