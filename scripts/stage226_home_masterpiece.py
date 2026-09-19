#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file():raise SystemExit('stage226 home missing')
s=p.read_text(encoding='utf8')
CSS='<link rel="stylesheet" href="/assets/stage226-home-masterpiece.css">'
# cleanup
s=re.sub(r'\s*<link[^>]+stage226-home-masterpiece\.css[^>]*>','',s,flags=re.I)
s=re.sub(r'\sdata-stage226-home="true"','',s)
s=re.sub(r'\s*<div class="p226-mantra".*?</div>','',s,flags=re.S|re.I)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage226-home="true">',s,count=1,flags=re.I)
if n!=1:raise SystemExit('stage226 body missing')
s=s.replace('</head>',CSS+'</head>',1)
# Let the visible brand text define its accessible name; a legacy aria-label hid the tagline from AT.
s=re.sub(r'(<a\b(?=[^>]*class="[^"]*stage98-brand[^"]*")[^>]*)\s+aria-label="[^"]*"([^>]*>)',r'\1\2',s,count=1,flags=re.I)
# Hero copy follows the approved art direction while the lead carries the commercial search terms.
s,n=re.subn(r'<h1 id="p128-title">.*?</h1>','<h1 id="p128-title">Разработка, которая доходит <span>до запуска.</span></h1>',s,count=1,flags=re.S)
if n!=1:raise SystemExit('stage226 hero h1 missing')
s,n=re.subn(r'<p class="p128-lead">.*?</p>','<p class="p128-lead">Сайты, веб-приложения, Telegram-продукты, автоматизация бизнеса и приложения — от задачи до работающего релиза.</p>',s,count=1,flags=re.S)
if n!=1:raise SystemExit('stage226 hero lead missing')
visual='''<div class="p128-hero__visual p226-system" aria-label="Система из реальных направлений и проектов Alexuys">
<div class="p226-beam" aria-hidden="true"></div><div class="p226-core" aria-hidden="true"><span>IDEAS<br>SYSTEMS<br>PRODUCTS<br>IMPACT</span></div><div class="p226-base" aria-hidden="true"></div>
<a class="p226-panel p226-panel--telegram" href="/cases/fin-planner/"><small>TELEGRAM PRODUCT</small><strong>Fin Planner</strong><span>Сценарии, состояния и данные внутри Telegram.</span><img src="/assets/cases/fin-planner/fin-planner-card-01-720w.webp" width="720" height="900" loading="lazy" decoding="async" alt="Fin Planner"></a>
<a class="p226-panel p226-panel--automation" href="/n8n-automation/"><small>AUTOMATION</small><strong>Workflow system</strong><span>Webhook → проверка → API → результат.</span><div class="p226-flow" aria-hidden="true"><i></i><b></b><i></i><b></b><em>n8n</em></div></a>
<a class="p226-panel p226-panel--analytics" href="/cases/seo-control-center/"><small>ANALYTICS / SEO</small><strong>SEO Control Center</strong><span>Индексация, поисковые данные и события.</span><img src="/assets/cases/seo-control-center/seo-control-center-live-01-800w.webp" width="800" height="500" loading="lazy" decoding="async" alt="SEO Control Center"></a>
<a class="p226-panel p226-panel--wordpress" href="/cases/wordpress-commercial/"><small>WORDPRESS / WEB</small><strong>Commercial site</strong><span>Рабочая тема, формы, страницы и mobile.</span><img src="/assets/cases/wordpress-commercial/wordpress-commercial-01-800w.webp" width="800" height="727" loading="lazy" decoding="async" alt="Коммерческий WordPress"></a>
<a class="p226-panel p226-panel--data" href="/cases/sheetpilot-ai/"><small>DATA → PRODUCT</small><strong>SheetPilot AI</strong><span>Excel, preview, AI-команды и экспорт результата.</span><img src="/assets/cases/sheetpilot-ai/sheetpilot-live-01-800w.webp" width="800" height="500" loading="lazy" decoding="async" alt="SheetPilot AI"></a>
<div class="p226-system-tag" aria-hidden="true">Больше, чем страницы. Связанные системы.</div>
</div>'''
pat=r'<div class="p128-hero__visual[^>]*>.*?(?=<div class="p128-proofbar")'
s,n=re.subn(pat,visual,s,count=1,flags=re.S)
if n!=1:raise SystemExit('stage226 hero visual replace failed')
# Add the thin system mantra after hero, mirroring the reference without fake metrics.
hero_end=re.search(r'<section class="p128-hero".*?</section>',s,re.S)
if not hero_end:raise SystemExit('stage226 hero section missing')
mantra='<div class="p226-mantra" aria-hidden="true"><span>TRUSTED APPROACH · REAL PROJECTS</span><span>IDEAS → SYSTEMS → PRODUCTS → IMPACT</span></div>'
s=s[:hero_end.end()]+mantra+s[hero_end.end():]
# Editorial labels from the reference.
s=s.replace('<h2 id="p128-work-title">Сначала работа. <span>Потом слова.</span></h2>','<h2 id="p128-work-title">Избранные <span>проекты.</span></h2>',1)
s=s.replace('<h2 id="p128-cap-title">С нуля или поверх того, <span>что уже есть.</span></h2>','<h2 id="p128-cap-title">Превращаю задачи <span>в работающие продукты.</span></h2>',1)
s=s.replace('Не нужно знать стек заранее. Достаточно понимать, какой результат должен появиться у пользователя или внутри бизнеса.','Объединяю интерфейс, разработку, данные и автоматизацию, чтобы идея становилась работающей системой.',1)
p.write_text(s,encoding='utf8')
# guards
f=p.read_text(encoding='utf8')
for needle in ['data-stage226-home="true"','stage226-home-masterpiece.css','p226-core','p226-panel--telegram','p226-panel--automation','p226-panel--analytics','p226-panel--wordpress','p226-panel--data','Избранные <span>проекты.</span>','Превращаю задачи <span>в работающие продукты.</span>']:
 if needle not in f:raise SystemExit(f'stage226 guard {needle}')
if f.count('stage226-home-masterpiece.css')!=1 or f.count('class="p226-mantra"')!=1:raise SystemExit('stage226 duplicate guard')
if f.count('class="p226-panel ')!=5:raise SystemExit(f'stage226 panel count {f.count("class=\"p226-panel ")}')
print('stage226 homepage masterpiece: hero-system=5 live routes, selected-work=4 real cases, cinematic capabilities')
