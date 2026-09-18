#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'

def load(rel):
 p=ROOT/rel/'index.html'
 if not p.is_file(): raise SystemExit(f'stage188: missing {rel}')
 return p,p.read_text(encoding='utf-8')

def h1(s,value,label):
 s,n=re.subn(r'<h1\b[^>]*>.*?</h1>',f'<h1>{value}</h1>',s,count=1,flags=re.I|re.S)
 if n!=1: raise SystemExit(f'stage188: h1 missing {label}')
 return s

def set_meta(s,title,desc=None):
 s=re.sub(r'<title>.*?</title>','<title>'+html.escape(title)+'</title>',s,count=1,flags=re.I|re.S)
 vals=[('property','og:title',title),('name','twitter:title',title)]
 if desc is not None: vals += [('name','description',desc),('property','og:description',desc),('name','twitter:description',desc)]
 for attr,key,val in vals:
  pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
  repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
  if re.search(pat,s,re.I): s=re.sub(pat,repl,s,count=1,flags=re.I)
  else: s=s.replace('</head>',repl+'</head>',1)
 return s

# Query: "разработка веб сервисов" — avg position 9.
p,s=load('web-development')
s=h1(s,'Разработка веб-сервисов на заказ. <em>От интерфейса до рабочего запуска.</em>','web')
p.write_text(s,encoding='utf-8')

# Query: backend commercial variant — avg position 7. Keep strong title, align visible H1.
p,s=load('backend-development')
s=h1(s,'Backend-разработка на заказ. <em>Серверная логика, база данных, роли и API.</em>','backend')
p.write_text(s,encoding='utf-8')

# Query: "исправь проект" — avg position 9; another continuation/repair query is avg position 4.
p,s=load('project-repair')
title='Исправление и доработка проекта - сайты, боты и backend | Alexuys'
desc='Исправление и доработка существующего проекта: ошибки, чужой код, интеграции, адаптив, backend и Telegram-боты. Диагностика причины и точечные изменения без лишнего переписывания.'
s=set_meta(s,title,desc)
s=h1(s,'Исправление и доработка существующего проекта. <em>Без переписывания с нуля.</em>','repair')
p.write_text(s,encoding='utf-8')

routes=['web-development','backend-development','project-repair']
for name in ('sitemap.xml','sitemap-google.xml'):
 sm=ROOT/name
 if not sm.exists(): continue
 text=sm.read_text(encoding='utf-8')
 for rel in routes:
  url=f'{BASE}/{rel}/'; text=re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
 sm.write_text(text,encoding='utf-8')

guards={
 'web-development':'Разработка веб-сервисов на заказ.',
 'backend-development':'Backend-разработка на заказ.',
 'project-repair':'Исправление и доработка существующего проекта.',
}
for rel,needle in guards.items():
 data=(ROOT/rel/'index.html').read_text(encoding='utf-8')
 if needle not in data: raise SystemExit(f'stage188: guard failed {rel}')
print('stage188 yandex service positions: pages=3')
