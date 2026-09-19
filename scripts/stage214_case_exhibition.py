#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'cases/index.html'
if not p.is_file():raise SystemExit('stage214 cases page missing')
s=p.read_text(encoding='utf8')
# Idempotent cleanup.
s=re.sub(r'\s*<div class="p214-curator".*?</div>\s*</div>', '', s, flags=re.S)
s=re.sub(r'<div class="p214-archive-label"[^>]*>.*?</div>', '', s, flags=re.S)
s=re.sub(r'\s*<span class="p214-case-meta">.*?</span>', '', s, flags=re.S)
s=re.sub(r'\sdata-stage214-featured="[^"]+"', '', s)
s=re.sub(r'\sdata-stage214-rank="[^"]+"', '', s)
s=re.sub(r'\s*<link[^>]+stage214-case-exhibition\.css[^>]*>', '', s, flags=re.I)
s=re.sub(r'\sdata-stage214-cases="true"', '', s)
# Find the mosaic and all case anchors.
m=re.search(r'(<div class="p130-mosaic">)(.*?)(</div></div></section>)',s,re.S)
if not m:raise SystemExit('stage214 mosaic missing')
inner=m.group(2)
anchors=re.findall(r'<a class="[^"]*p130-tile[^"]*" href="/cases/[^"]+/">.*?</a>',inner,re.S)
if len(anchors)!=13:raise SystemExit(f'stage214 expected 13 case tiles, got {len(anchors)}')
by_href={re.search(r'href="([^"]+)"',a).group(1):a for a in anchors}
order=['/cases/wordpress-commercial/','/cases/fin-planner/','/cases/marketplace-monitor/','/cases/portfolio-site/','/cases/ozon-scanner/','/cases/swift-calendar/','/cases/sheetpilot-ai/','/cases/seo-control-center/','/cases/auto-crm/','/cases/factory-catalog/','/cases/taxi-app/','/cases/siteaudit-studio/','/cases/freelance-os/']
if set(order)!=set(by_href):raise SystemExit('stage214 case route set mismatch')
labels={
'/cases/wordpress-commercial/':'01 · WORDPRESS / PRODUCTION',
'/cases/fin-planner/':'02 · TELEGRAM / PRODUCT',
'/cases/marketplace-monitor/':'03 · MARKETPLACES / DATA',
'/cases/portfolio-site/':'04 · WEB / PRODUCT SYSTEM',
'/cases/ozon-scanner/':'05 · OZON / OPERATIONS',
'/cases/swift-calendar/':'06 · iOS / SWIFT',
'/cases/sheetpilot-ai/':'07 · AI / EXCEL',
'/cases/seo-control-center/':'08 · SEO / MONITORING',
'/cases/auto-crm/':'09 · CRM / OPERATIONS',
'/cases/factory-catalog/':'10 · B2B / CATALOG',
'/cases/taxi-app/':'11 · MOBILE / PRODUCT',
'/cases/siteaudit-studio/':'12 · SEO / TOOLING',
'/cases/freelance-os/':'13 · CRM / WORKFLOW',
}
out=[]
for i,route in enumerate(order,1):
 a=by_href[route]
 a=re.sub(r'class="([^"]*p130-tile[^"]*)"',lambda x:'class="'+' '.join(y for y in x.group(1).split() if y!='p130-tile--wide')+'"',a,count=1)
 attrs=f' data-stage214-rank="{i:02d}"'+(f' data-stage214-featured="{i}"' if i<=4 else '')
 a=a.replace(f'href="{route}"',f'href="{route}"{attrs}',1)
 a=a.replace('<div class="p130-tile__body">',f'<div class="p130-tile__body"><span class="p214-case-meta">{labels[route]}</span>',1)
 if i==5:out.append('<div class="p214-archive-label" aria-hidden="true">Ещё реальные проекты · 09</div>')
 out.append(a)
new_inner=''.join(out)
s=s[:m.start()]+m.group(1)+new_inner+m.group(3)+s[m.end():]
# Add curation header immediately before mosaic.
curator='<div class="p214-curator"><div><p class="p214-curator__eyebrow">SELECTED / 04 · REAL WORK</p></div><div><h2>Разные задачи. Один уровень проработки.</h2><p>Сначала — четыре проекта из разных классов: коммерческий WordPress, Telegram-продукт, автоматизация маркетплейсов и этот portfolio system. Ниже — остальные реальные работы без концептов и вымышленных экранов.</p></div></div>'
s=s.replace('<div class="p130-mosaic">',curator+'<div class="p130-mosaic">',1)
# Body flag + CSS.
s,n=re.subn(r'<body\b([^>]*)>',lambda x:'<body'+x.group(1)+' data-stage214-cases="true">',s,count=1,flags=re.I)
if n!=1:raise SystemExit('stage214 body missing')
s=s.replace('</head>','<link rel="stylesheet" href="/assets/stage214-case-exhibition.css"></head>',1)
p.write_text(s,encoding='utf8')
# Guards.
f=p.read_text(encoding='utf8')
if f.count('data-stage214-featured=')!=4:raise SystemExit('stage214 featured count')
if f.count('p214-case-meta')!=13:raise SystemExit('stage214 meta count')
if f.count('p214-curator')<1 or f.count('stage214-case-exhibition.css')!=1:raise SystemExit('stage214 shell guard')
pos=[f.find(f'href="{r}"') for r in order]
if pos!=sorted(pos):raise SystemExit('stage214 order guard')
print('stage214 case exhibition: featured=4, archive=9, order=wordpress/telegram/marketplace/portfolio')
