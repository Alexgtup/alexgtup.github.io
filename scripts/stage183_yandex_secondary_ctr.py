#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html, re, sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'
TODAY='2026-09-18'

def load(rel):
    p=ROOT/rel/'index.html'
    if not p.is_file(): raise SystemExit(f'stage183: missing {rel}')
    return p,p.read_text(encoding='utf-8')

def set_meta(s,title,desc):
    s,n=re.subn(r'<title>.*?</title>','<title>'+html.escape(title)+'</title>',s,count=1,flags=re.I|re.S)
    if n!=1: raise SystemExit('stage183: title missing')
    for attr,key,val in [('name','description',desc),('property','og:title',title),('property','og:description',desc),('name','twitter:title',title),('name','twitter:description',desc)]:
        pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
        repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
        if re.search(pat,s,re.I): s=re.sub(pat,repl,s,count=1,flags=re.I)
        else: s=s.replace('</head>',repl+'</head>',1)
    return s

def replace_once(s,old,new,label):
    if new in s:return s
    if old not in s:raise SystemExit(f'stage183: marker missing {label}')
    return s.replace(old,new,1)

# /development/: Yandex already shows the exact commercial query "разработка на заказ" around position 9.
p,s=load('development')
title='Разработка на заказ - сайты, боты и автоматизация | Alexuys'
desc='Разработка на заказ: веб-сервисы, сайты, Telegram-боты, CRM, backend, API, Python и автоматизация. Реальные кейсы, рабочие демо и доработка существующих проектов.'
s=set_meta(s,title,desc)
s=replace_once(s,'<h1>Программист под задачу. <em>От небольшого скрипта до веб-сервиса.</em></h1>','<h1>Разработка на заказ. <em>От небольшого скрипта до веб-сервиса.</em></h1>','development h1')
s=replace_once(s,'<p class="p129-lead">Если пока непонятно, нужен сайт, бот, приложение или внутренняя система, можно начать с результата: кто будет пользоваться, что должно происходить и что уже есть сейчас.</p>','<p class="p129-lead">Разработка под конкретный результат: сайт, Telegram-бот, веб-сервис, backend, API, автоматизация или доработка существующего проекта. Если формат пока не определён, достаточно описать, кто будет пользоваться системой и что должно заработать.</p>','development lead')
p.write_text(s,encoding='utf-8')

# /cases/: query "готовые кейсы" already ranks ~7.3, while title starts with a generic "Кейсы".
p,s=load('cases')
title='Готовые кейсы разработки - Telegram, CRM, iOS и веб | Alexuys'
desc='Готовые кейсы разработки с реальными интерфейсами: Telegram-боты, CRM, iOS, B2B-каталоги и веб-сервисы. Задача, реализация и то, что можно проверить.'
s=set_meta(s,title,desc)
s=replace_once(s,'<h1>Реальные проекты. <span>Без витрины из концептов.</span></h1>','<h1>Готовые кейсы разработки. <span>Реальные проекты, а не концепты.</span></h1>','cases h1')
p.write_text(s,encoding='utf-8')

# /n8n-automation/: Yandex already shows "n8n automation workflow" around position 8.5.
p,s=load('n8n-automation')
title='n8n workflow и автоматизация на заказ - CRM, Telegram, API | Alexuys'
desc='n8n workflow и автоматизация бизнес-процессов: CRM, Telegram, Google Sheets, API, webhooks и уведомления. Проектирование, запуск и доработка сценариев.'
s=set_meta(s,title,desc)
s=replace_once(s,'<h1>Автоматизировать повторяющиеся действия. <em>n8n и Make — если они подходят задаче.</em></h1>','<h1>n8n workflow и автоматизация. <em>Связать сервисы в один рабочий сценарий.</em></h1>','n8n h1')
p.write_text(s,encoding='utf-8')

# Refresh discovery freshness only for pages changed by this pass.
targets={f'{BASE}/development/',f'{BASE}/cases/',f'{BASE}/n8n-automation/'}
for name in ('sitemap.xml','sitemap-google.xml'):
    path=ROOT/name
    if not path.exists():continue
    text=path.read_text(encoding='utf-8')
    for url in targets:
        text=re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
    path.write_text(text,encoding='utf-8')

guards={
 'development':['Разработка на заказ - сайты, боты и автоматизация','<h1>Разработка на заказ.'],
 'cases':['Готовые кейсы разработки - Telegram, CRM, iOS и веб','<h1>Готовые кейсы разработки.'],
 'n8n-automation':['n8n workflow и автоматизация на заказ','<h1>n8n workflow и автоматизация.'],
}
for rel,needles in guards.items():
    text=(ROOT/rel/'index.html').read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text: raise SystemExit(f'stage183: guard failed {rel}: {needle}')
print(f'stage183 yandex secondary ctr: pages={len(guards)}')
