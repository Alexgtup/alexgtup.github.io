#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
CSS='<link rel="stylesheet" href="/assets/stage221-lab-hubs.css">'
DEMO_META={
 'SheetPilot AI':('01','PRODUCT / XLSX','OPEN SERVICE'),
 'SEO Control Center':('02','PRODUCT / SEO','OPEN DEMO'),
 'SiteAudit Studio':('03','PRODUCT / CRAWL','OPEN SERVICE'),
 'FreelanceOS':('04','PRODUCT / CRM','OPEN LOCAL'),
}
TOOL_META={
 '/tools/json-formatter/':('01','JSON','validate','format'),
 '/tools/utm-builder/':('02','URL','build','utm'),
 '/tools/cron-builder/':('03','schedule','compose','cron'),
 '/tools/jwt-decoder/':('04','token','decode','payload'),
 '/tools/robots-validator/':('05','robots','parse','rules'),
 '/tools/sitemap-validator/':('06','xml','inspect','urls'),
}
DEMO_CONSOLE='''<aside class="p221-lab-console" aria-label="Лаборатория демо-проектов"><div class="p221-lab-console__top"><small>ALEXUYS LAB / PRODUCTS</small><span>4 inspectable systems</span></div><div class="p221-lab-console__body"><div class="p221-lab-row"><b>01</b><div><strong>SheetPilot AI</strong><em>Excel → command → preview</em></div><span>service</span></div><div class="p221-lab-row"><b>02</b><div><strong>SEO Control Center</strong><em>sites → events → search data</em></div><span>demo</span></div><div class="p221-lab-row"><b>03</b><div><strong>SiteAudit Studio</strong><em>URL → crawl → signals</em></div><span>service</span></div><div class="p221-lab-row"><b>04</b><div><strong>FreelanceOS</strong><em>lead → pipeline → follow-up</em></div><span>local</span></div></div></aside>'''
TOOLS_CONSOLE='''<aside class="p221-lab-console" aria-label="Принцип работы браузерных инструментов"><div class="p221-lab-console__top"><small>ALEXUYS LAB / TOOLS</small><span>6 focused utilities</span></div><div class="p221-lab-console__body"><div class="p221-lab-row"><b>IN</b><div><strong>Paste or configure</strong><em>JSON · URL · token · XML</em></div><span>input</span></div><div class="p221-lab-row"><b>DO</b><div><strong>Process locally</strong><em>format · build · decode · parse</em></div><span>browser</span></div><div class="p221-lab-row"><b>OUT</b><div><strong>Use the result</strong><em>copy · inspect · fix · ship</em></div><span>output</span></div></div></aside>'''

def clean(s,hub):
 s=re.sub(r'\s*<link[^>]+stage221-lab-hubs\.css[^>]*>','',s,flags=re.I)
 s=re.sub(r'\sdata-stage221-hub="[^"]+"','',s)
 s=re.sub(r'\s*<aside class="p221-lab-console".*?</aside>','',s,flags=re.I|re.S)
 s=re.sub(r'\s*<div class="p221-card-meta">.*?</div>','',s,flags=re.I|re.S)
 s=re.sub(r'\s*<div class="p221-tool-flow">.*?</div>','',s,flags=re.I|re.S)
 s=re.sub(r'\sdata-stage221-rank="[^"]+"','',s)
 s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+f' data-stage221-hub="{hub}">',s,count=1,flags=re.I)
 if n!=1:raise SystemExit(f'stage221 body missing {hub}')
 s=s.replace('</head>',CSS+'</head>',1)
 return s

# demos
p=ROOT/'demos/index.html';s=clean(p.read_text(encoding='utf8'),'demos')
anchor='<div class="stage94-hero-actions"><a class="stage94-action-primary" href="#demo-products">Смотреть демо ↓</a><a class="stage94-action-secondary" href="/cases/">Все кейсы</a></div>'
if anchor not in s:raise SystemExit('stage221 demo hero anchor missing')
s=s.replace(anchor,anchor+DEMO_CONSOLE,1)
# decorate each existing real card without rewriting its copy
for title,(rank,kind,state) in DEMO_META.items():
 pat=rf'(<article class="growth-card"[^>]*>)(?=.*?<h3>{re.escape(title)}</h3>)'
 m=re.search(pat,s,re.S)
 if not m:raise SystemExit(f'stage221 demo card missing {title}')
 start=m.start(1);end=m.end(1);tag=m.group(1)
 tag=tag[:-1]+f' data-stage221-rank="{rank}">'
 s=s[:start]+tag+s[end:]
 # insert meta before existing growth-label in this card
 card_start=start; label_pos=s.find('<span class="growth-label">',card_start)
 if label_pos<0:raise SystemExit(f'stage221 demo label missing {title}')
 meta=f'<div class="p221-card-meta"><small>{kind}</small><b>{state}</b></div>'
 s=s[:label_pos]+meta+s[label_pos:]
p.write_text(s,encoding='utf8')

# tools
p=ROOT/'tools/index.html';s=clean(p.read_text(encoding='utf8'),'tools')
anchor='<div class="stage94-hero-actions"><a class="stage94-action-primary" href="#tool-list">Открыть инструменты ↓</a><a class="stage94-action-secondary" href="/cases/">Кейсы</a></div>'
if anchor not in s:raise SystemExit('stage221 tools hero anchor missing')
s=s.replace(anchor,anchor+TOOLS_CONSOLE,1)
for href,(rank,inp,action,out) in TOOL_META.items():
 pat=rf'<a class="dt-tool-card" href="{re.escape(href)}"[^>]*>.*?</a>'
 m=re.search(pat,s,re.S)
 if not m:raise SystemExit(f'stage221 tool missing {href}')
 block=m.group(0)
 block=block.replace(f'href="{href}"',f'href="{href}" data-stage221-rank="{rank}"',1)
 flow=f'<div class="p221-tool-flow"><span>{inp}</span><i></i><b>{action}</b><i></i><span>{out}</span></div>'
 block=block[:-4]+flow+'</a>'
 s=s[:m.start()]+block+s[m.end():]
p.write_text(s,encoding='utf8')

# guards
for rel,hub,count in [('demos/index.html','demos',4),('tools/index.html','tools',6)]:
 s=(ROOT/rel).read_text(encoding='utf8')
 if s.count('stage221-lab-hubs.css')!=1:raise SystemExit(f'stage221 css guard {rel}')
 if len(re.findall(r'<body\b[^>]*data-stage221-hub="'+hub+r'"',s,re.I))!=1:raise SystemExit(f'stage221 body guard {rel}')
 if s.count('data-stage221-rank=')!=count:raise SystemExit(f'stage221 rank guard {rel}')
 if s.count('p221-lab-console__body')!=1:raise SystemExit(f'stage221 console guard {rel}')
print('stage221 lab hubs: demos=4 product systems, tools=6 local pipelines')
