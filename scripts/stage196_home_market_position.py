#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
TODAY='2026-09-18'; BASE='https://alexgtup.github.io'
p=ROOT/'index.html'
if not p.is_file(): raise SystemExit('stage196: home missing')
s=p.read_text(encoding='utf-8')
TITLE='Разработка сайтов, ПО и автоматизация бизнеса | Alexuys'
DESC='Разработка сайтов и веб-приложений, программного обеспечения, мобильных приложений и автоматизации бизнеса. Backend, API, CRM, ИИ, интеграции и доработка существующих проектов.'

def meta(s,title,desc):
 s=re.sub(r'<title\b[^>]*>.*?</title>',f'<title>{html.escape(title)}</title>',s,count=1,flags=re.I|re.S)
 for attr,key,val in [('name','description',desc),('property','og:title',title),('property','og:description',desc),('name','twitter:title',title),('name','twitter:description',desc)]:
  pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
  repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
  s=re.sub(pat,repl,s,count=1,flags=re.I) if re.search(pat,s,re.I) else s.replace('</head>',repl+'</head>',1)
 return s

s=meta(s,TITLE,DESC)
s,n=re.subn(r'<h1 id="p128-title">.*?</h1>', '<h1 id="p128-title">Разработка сайтов и ПО. <span>Автоматизация бизнеса.</span></h1>',s,count=1,flags=re.I|re.S)
if n!=1: raise SystemExit('stage196: home h1 missing')
lead='Разработка сайтов, веб-приложений и программного обеспечения, автоматизация бизнеса и мобильные приложения. Беру задачу целиком или подключаюсь к уже работающему проекту - без лишнего слоя менеджеров.'
s,n=re.subn(r'<p class="p128-lead">.*?</p>',f'<p class="p128-lead">{lead}</p>',s,count=1,flags=re.I|re.S)
if n!=1: raise SystemExit('stage196: lead missing')

# Popular tasks: replace a Telegram-first home entry with the larger AI-for-business intent.
old='<a href="/telegram-bots/"><strong>Запустить Telegram-бота</strong><span>Открыть ↗</span></a>'
new='<a href="/ai-automation/"><strong>Внедрить ИИ в бизнес-процесс</strong><span>Открыть ↗</span></a>'
if old in s: s=s.replace(old,new,1)
elif new not in s: raise SystemExit('stage196: popular Telegram anchor missing')

# The integration map should point to the integration-intent landing, not API creation only.
old='<a href="/api-development/"><strong>API</strong><span>Контракт для систем</span><b>↗</b></a>'
new='<a href="/api-integrations/"><strong>API-интеграции</strong><span>Связать системы</span><b>↗</b></a>'
if old in s: s=s.replace(old,new,1)
elif new not in s: raise SystemExit('stage196: api map anchor missing')

# Add marketplace integration as a first-class integration task.
mp='<a href="/marketplace-integration/"><strong>Маркетплейсы</strong><span>1С, Ozon, Wildberries</span><b>↗</b></a>'
if mp not in s:
 anchor='<a href="/1c-integration/"><strong>1С</strong><span>Каталог и заказы</span><b>↗</b></a>'
 if anchor not in s: raise SystemExit('stage196: 1c map anchor missing')
 s=s.replace(anchor,anchor+mp,1)

# Lastmod for materially changed home.
for name in ('sitemap.xml','sitemap-google.xml'):
 sp=ROOT/name
 if not sp.exists(): continue
 text=sp.read_text(encoding='utf-8')
 text=re.sub(r'(<loc>'+re.escape(BASE+r'/')+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
 sp.write_text(text,encoding='utf-8')

p.write_text(s,encoding='utf-8')
final=p.read_text(encoding='utf-8')
for needle in [TITLE,DESC,'Разработка сайтов и ПО.','Автоматизация бизнеса.','Внедрить ИИ в бизнес-процесс','href="/api-integrations/"','href="/marketplace-integration/"']:
 if needle not in final: raise SystemExit(f'stage196 guard failed: {needle}')
if 'Запустить Telegram-бота' in final: raise SystemExit('stage196: old Telegram popular task remains')
print('stage196 home market position: home=1, popular_ai=1, marketplace_link=1')
