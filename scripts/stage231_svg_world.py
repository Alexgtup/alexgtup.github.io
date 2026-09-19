#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file(): raise SystemExit('stage231 home missing')
s=p.read_text(encoding='utf8')
s=re.sub(r'\s*<link[^>]+stage231-svg-world\.css[^>]*>','',s,flags=re.I)
s=re.sub(r'\sdata-stage231-home="true"','',s)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage231-home="true">',s,count=1,flags=re.I)
if n!=1: raise SystemExit('stage231 body missing')
s=s.replace('</head>','<link rel="stylesheet" href="/assets/stage231-svg-world.css"></head>',1)
# Replace the old five-card hero DOM with one integrated SVG installation and clickable hotspots.
start=s.find('<div class="p128-hero__visual')
end=s.find('<div class="p128-proofbar"',start)
if start<0 or end<0: raise SystemExit('stage231 hero visual range missing')
hero='''<div class="p128-hero__visual p231-hero-scene" aria-label="Система из пяти направлений разработки"><img class="p231-hero-art" src="/assets/stage231-hero-installation.svg" width="1000" height="760" decoding="async" alt="Центральная цифровая система с Telegram, автоматизацией, аналитикой, WordPress и данными"><a class="p231-hotspot p231-hotspot--telegram" href="/cases/fin-planner/">Fin Planner</a><a class="p231-hotspot p231-hotspot--automation" href="/n8n-automation/">Автоматизация</a><a class="p231-hotspot p231-hotspot--analytics" href="/cases/seo-control-center/">SEO Control Center</a><a class="p231-hotspot p231-hotspot--wordpress" href="/cases/wordpress-commercial/">WordPress Commercial</a><a class="p231-hotspot p231-hotspot--data" href="/cases/sheetpilot-ai/">SheetPilot AI</a><div class="p231-system-note" aria-hidden="true"><b>SYSTEM / 05</b>Больше, чем страницы. Связанные системы.</div></div>'''
s=s[:start]+hero+s[end:]
# Keep the reference's three proof metrics.
proof='<div class="p128-proofbar" aria-label="Проверяемые факты"><a href="/cases/"><strong>13</strong><span>реальных кейсов</span></a><a href="/demos/"><strong>4</strong><span>публичных демо</span></a><a href="/tools/"><strong>6</strong><span>tools</span></a></div>'
s,n=re.subn(r'<div class="p128-proofbar"[^>]*>.*?</div>',proof,s,count=1,flags=re.S)
if n!=1: raise SystemExit('stage231 proofbar missing')
# Match the five capability labels/routes shown in the approved composition.
cap='''<div class="p128-cap__list" data-stage231-reference-capabilities="true"><a href="/web-development/"><span>01</span><strong>Сайты и платформы</strong><em>От лендингов до сложных веб-сервисов</em><b>↗</b></a><a href="/telegram-bots/"><span>02</span><strong>Telegram-продукты</strong><em>Боты, mini apps и интеграции</em><b>↗</b></a><a href="/automation-services/"><span>03</span><strong>Автоматизация</strong><em>Сценарии, API и AI-агенты</em><b>↗</b></a><a href="/tools/"><span>04</span><strong>Аналитика и инструменты</strong><em>Данные, визуализация и контроль</em><b>↗</b></a><a href="/mvp-development/"><span>05</span><strong>Приложения и MVP</strong><em>Быстрый запуск и рост продукта</em><b>↗</b></a></div>'''
s,n=re.subn(r'<div class="p128-cap__list"[^>]*>.*?</div>',cap,s,count=1,flags=re.S)
if n!=1: raise SystemExit('stage231 capability list missing')
p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
for needle in ['data-stage231-home="true"','stage231-svg-world.css','stage231-hero-installation.svg','p231-hotspot--telegram','p231-hotspot--automation','p231-hotspot--analytics','p231-hotspot--wordpress','p231-hotspot--data','data-stage231-reference-capabilities="true"','Сайты и платформы','Telegram-продукты','Аналитика и инструменты','Приложения и MVP']:
 if needle not in f: raise SystemExit(f'stage231 guard {needle}')
if f.count('stage231-svg-world.css')!=1: raise SystemExit('stage231 duplicate stylesheet')
if f.count('class="p231-hotspot ')!=5: raise SystemExit('stage231 hotspot count')
print('stage231 svg world: integrated hero SVG, continuous space background, mountain valley, five reference capabilities')
