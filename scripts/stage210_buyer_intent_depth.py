#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json,re,sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-19'
CFG={
 'telegram-bot-repair':{
  'title':'Доработка Telegram-бота на Python и aiogram | Alexuys',
  'desc':'Доработка существующего Telegram-бота на Python и aiogram: ошибки, inline-кнопки, FSM, SQLite/PostgreSQL, рассылки, админ-функции, CRM/API, оплаты и запуск на VPS.',
  'h1':'Доработка Telegram-бота на Python и aiogram. <em>Без переписывания с нуля.</em>',
  'task_h2':'Доработка Telegram-бота: исправить текущий код и добавить нужную функцию.',
  'task_intro':'Если код уже есть, сначала проверяется запуск, версия Python и aiogram, состояния, база и проблемный сценарий. После этого можно локально исправить ошибку или добавить новую функцию, не заменяя рабочие части проекта.',
  'cards':[
   ('Python и aiogram 3','Routers и handlers, inline-кнопки, callback-логика, FSM, команды и переходы в существующем проекте.'),
   ('SQLite и PostgreSQL','Хранение пользователей, заявок, статусов и состояний без потери уже накопленных данных.'),
   ('Рассылки, админка и API','Рассылки, просмотр заявок, CRM/API, webhooks, оплаты и другие функции поверх работающего бота.'),
  ]
 },
 'wordpress-development':{
  'title':'Доработка WordPress сайта — разработчик | Alexuys',
  'desc':'Доработка существующего WordPress сайта: ошибки, тема и плагины, новые блоки и страницы, формы, адаптив, PHP/JavaScript, API, скорость и техническое SEO без полной пересборки.',
  'h1':'Доработка WordPress сайта. <em>Без полной пересборки.</em>',
  'demand_h2':'Доработка существующего WordPress сайта: сначала проверить тему, плагины и риски.',
  'demand_intro':'Если сайт уже работает, задача обычно не в новой сборке, а в точечном изменении: исправить ошибку, форму или мобильную версию, добавить блок, страницу, интеграцию, ускорение или SEO-правку. Сначала проверяется текущая реализация и только затем меняется код.',
 }
}

def page(slug):
 p=ROOT/slug/'index.html'
 if not p.is_file():raise SystemExit(f'stage210 missing {slug}')
 return p

def meta(s,title,desc):
 s,n=re.subn(r'<title\b[^>]*>.*?</title>',f'<title>{html.escape(title)}</title>',s,count=1,flags=re.I|re.S)
 if n!=1:raise SystemExit('stage210 title missing')
 for attr,key,val in [('name','description',desc),('property','og:title',title),('property','og:description',desc),('name','twitter:title',title),('name','twitter:description',desc)]:
  pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
  repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
  if re.search(pat,s,re.I):s=re.sub(pat,repl,s,count=1,flags=re.I)
 return s

def h1(s,value,slug):
 s,n=re.subn(r'<h1\b([^>]*)>.*?</h1>',lambda m:f'<h1{m.group(1)}>{value}</h1>',s,count=1,flags=re.I|re.S)
 if n!=1:raise SystemExit(f'stage210 h1 missing {slug}')
 return s

def sync_schema(s,title,desc):
 clean=re.sub(r'\s*\|\s*Alexuys\s*$','',title).strip();out=[];last=0;touched=0
 for m in re.finditer(r'<script([^>]*)type="application/ld\+json"([^>]*)>(.*?)</script>',s,re.I|re.S):
  try:o=json.loads(m.group(3))
  except Exception:continue
  changed=False;stack=[o]
  while stack:
   x=stack.pop()
   if isinstance(x,dict):
    if x.get('@type') in ('Service','WebPage'):
     x['name']=clean;x['description']=desc;changed=True
    stack.extend(x.values())
   elif isinstance(x,list):stack.extend(x)
  if changed:
   out.append(s[last:m.start(3)]);out.append(json.dumps(o,ensure_ascii=False,separators=(',',':')));last=m.end(3);touched+=1
 if touched:out.append(s[last:]);return ''.join(out)
 return s

changed=[]
# Telegram repair: tune SERP + hero + existing task section, not page length.
slug='telegram-bot-repair';c=CFG[slug];p=page(slug);s=p.read_text(encoding='utf-8')
s=meta(s,c['title'],c['desc']);s=h1(s,c['h1'],slug)
pat=r'(<section class="secondary-demand"[^>]*data-stage150="service".*?<div class="secondary-demand__head">.*?<div><h2>)(.*?)(</h2><p class="secondary-demand__intro">)(.*?)(</p>)(.*?<div class="secondary-demand__grid">)(.*?)(</div><nav class="secondary-demand__links")'
m=re.search(pat,s,re.I|re.S)
if not m:raise SystemExit('stage210 telegram task block missing')
cards=''.join(f'<article class="secondary-demand__card"><h3>{q}</h3><p>{a}</p></article>' for q,a in c['cards'])
s=s[:m.start()]+m.group(1)+c['task_h2']+m.group(3)+c['task_intro']+m.group(5)+cards+m.group(7)+s[m.end():]
s=sync_schema(s,c['title'],c['desc']);p.write_text(s,encoding='utf-8');changed.append('/'+slug+'/')

# WordPress: exact existing-site intent in SERP + hero + existing search-demand section.
slug='wordpress-development';c=CFG[slug];p=page(slug);s=p.read_text(encoding='utf-8')
s=meta(s,c['title'],c['desc']);s=h1(s,c['h1'],slug)
pat=r'(<section class="search-demand"[^>]*>.*?<div class="search-demand__head">.*?<div><h2[^>]*>)(.*?)(</h2><p class="search-demand__intro">)(.*?)(</p>)'
m=re.search(pat,s,re.I|re.S)
if not m:raise SystemExit('stage210 wordpress demand block missing')
s=s[:m.start()]+m.group(1)+c['demand_h2']+m.group(3)+c['demand_intro']+m.group(5)+s[m.end():]
s=sync_schema(s,c['title'],c['desc']);p.write_text(s,encoding='utf-8');changed.append('/'+slug+'/')

for name in ('sitemap.xml','sitemap-google.xml'):
 p=ROOT/name
 if not p.exists():continue
 t=p.read_text(encoding='utf-8')
 for route in changed:t=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',t,count=1)
 p.write_text(t,encoding='utf-8')

# Guards.
for slug,c in CFG.items():
 s=page(slug).read_text(encoding='utf-8')
 if not 35<=len(c['title'])<=65:raise SystemExit(f'stage210 title length {slug}: {len(c["title"])}')
 for needle in [c['title'],c['desc'],c['h1']]:
  if needle not in s:raise SystemExit(f'stage210 guard {slug}: {needle}')
if 'SQLite и PostgreSQL' not in page('telegram-bot-repair').read_text(encoding='utf-8'):raise SystemExit('stage210 telegram buyer tasks guard')
if 'Доработка существующего WordPress сайта' not in page('wordpress-development').read_text(encoding='utf-8'):raise SystemExit('stage210 wordpress existing-site guard')
print('stage210 buyer intent depth: telegram-repair=exact, wordpress=existing-site')
