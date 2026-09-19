#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'services/index.html'
if not p.is_file():raise SystemExit('stage224 services missing')
s=p.read_text(encoding='utf8')
CSS='<link rel="stylesheet" href="/assets/stage224-services-decision.css">'
PRIMARY=['/web-development/','/telegram-bots/','/automation-services/','/api-integrations/','/crm-development/','/project-repair/']
SECONDARY=['/development/','/1c-integration/','/ai-automation/','/app-development/','/ecommerce-development/','/marketplace-integration/']
CODES={'/web-development/':'BUILD','/telegram-bots/':'BOT','/automation-services/':'FLOW','/api-integrations/':'LINK','/crm-development/':'OPS','/project-repair/':'FIX','/development/':'DEV','/1c-integration/':'1C','/ai-automation/':'AI','/app-development/':'APP','/ecommerce-development/':'SHOP','/marketplace-integration/':'MKT'}
# cleanup
s=re.sub(r'\s*<link[^>]+stage224-services-decision\.css[^>]*>','',s,flags=re.I)
s=re.sub(r'\sdata-stage224-services="true"','',s)
s=re.sub(r'\sdata-stage224-primary="[^"]+"','',s)
s=re.sub(r'\sdata-stage224-secondary="true"','',s)
s=re.sub(r'\sdata-stage224-code="[^"]+"','',s)
s=re.sub(r'<div class="p224-specialist-label"[^>]*>.*?</div>','',s,flags=re.S)
s=re.sub(r'<p class="p224-decision-intro">.*?</p>','',s,flags=re.S)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage224-services="true">',s,count=1,flags=re.I)
if n!=1:raise SystemExit('stage224 body missing')
s=s.replace('</head>',CSS+'</head>',1)
# Intro explains choice model without adding another SEO section.
intro='<div class="p129-section-head"><p class="p130-kicker">CAPABILITIES</p><h2>Выберите результат, а не стек.</h2><p class="p224-decision-intro">Шесть основных сценариев закрывают большинство задач: запустить интерфейс, собрать Telegram-продукт, автоматизировать процесс, связать системы, построить внутренний контур или довести существующий проект. Технологию подбираю уже под этот результат.</p></div>'
head_pat=r'<div class="p129-section-head"><p class="p130-kicker">CAPABILITIES</p><h2>(?:Основные направления\.|Выберите результат, а не стек\.)</h2>(?:<p class="p224-decision-intro">.*?</p>)?</div>'
s,n=re.subn(head_pat,intro,s,count=1,flags=re.S)
if n!=1:raise SystemExit('stage224 list heading missing')
# Extract all ten canonical rows then recompose only the row span. Earlier stages may
# append SEO/discovery blocks inside the same section, so do not depend on a specific
# sequence of closing </div></section> tags.
row_pat=re.compile(r'<a\b(?=[^>]*class="[^"]*\bp130-row\b[^"]*")(?=[^>]*href="([^"]+)")[^>]*>.*?</a>',re.S|re.I)
row_matches=[m for m in row_pat.finditer(s) if m.group(1) in set(PRIMARY+SECONDARY)]
rows=[m.group(1) for m in row_matches]
if len(row_matches)!=12 or set(rows)!=set(PRIMARY+SECONDARY):raise SystemExit(f'stage224 route mismatch: {rows}')
blocks={m.group(1):m.group(0) for m in row_matches}
out=[]
for idx,route in enumerate(PRIMARY,1):
 b=blocks[route].replace(f'href="{route}"',f'href="{route}" data-stage224-primary="{idx:02d}" data-stage224-code="{CODES[route]}"',1)
 out.append(b)
out.append('<div class="p224-specialist-label" aria-hidden="true">SPECIALIST ROUTES · 06</div>')
for route in SECONDARY:
 b=blocks[route].replace(f'href="{route}"',f'href="{route}" data-stage224-secondary="true" data-stage224-code="{CODES[route]}"',1)
 out.append(b)
first=min(m.start() for m in row_matches); last=max(m.end() for m in row_matches)
s=s[:first]+''.join(out)+s[last:]
# Replace single featured card with verified commercial client work.
featured='''<section class="p130-featured"><div class="p130-shell"><a class="p130-featured-card" href="/cases/wordpress-commercial/"><div class="p130-featured-media"><img src="/assets/cases/wordpress-commercial/wordpress-commercial-01.webp" width="1600" height="1000" alt="Коммерческий WordPress — реальный проект" loading="lazy" decoding="async"></div><div class="p130-featured-copy"><p class="p130-kicker">FEATURED / CLIENT WORK</p><h2>Коммерческий WordPress</h2><p>Доработка существующего сайта: формы, калькуляторы, страницы, мобильная версия и технические исправления без полной пересборки рабочей темы.</p><span class="p129-textlink">Открыть реальный кейс ↗</span></div></a></div></section>'''
s,n=re.subn(r'<section\b(?=[^>]*class="[^"]*\bp130-featured\b[^"]*")[^>]*>.*?</section>',featured,s,count=1,flags=re.S|re.I)
if n!=1:raise SystemExit('stage224 featured missing')
p.write_text(s,encoding='utf8')
# guards
f=p.read_text(encoding='utf8')
for route in PRIMARY+SECONDARY:
 if f.count(f'href="{route}"')<1:raise SystemExit(f'stage224 lost route {route}')
if f.count('data-stage224-primary=')!=6:raise SystemExit('stage224 primary count')
if f.count('data-stage224-secondary="true"')!=6:raise SystemExit('stage224 secondary count')
for needle in ['data-stage224-services="true"','stage224-services-decision.css','/cases/wordpress-commercial/','SPECIALIST ROUTES · 06']:
 if needle not in f:raise SystemExit(f'stage224 guard {needle}')
print('stage224 services decision: primary=6, specialist=6, featured=wordpress-commercial')
