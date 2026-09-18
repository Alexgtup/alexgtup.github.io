#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'

CFG={
'crm-development':{
 'title':'CRM для бизнеса на заказ - разработка CRM системы | Alexuys',
 'desc':'CRM для бизнеса на заказ: клиенты, заявки, сотрудники, роли, статусы, отчёты, автоматизация, API и интеграции. Система под реальный процесс без лишних модулей.',
 'h1':'CRM для бизнеса на заказ. <em>Система под реальный процесс.</em>',
 'demand_h2':'CRM для бизнеса: система под процесс, а не ещё одна таблица.',
 'demand_intro':'Своя CRM имеет смысл, когда готовая система заставляет сотрудников вести данные в Excel и мессенджерах или обходить ограничения. Сначала фиксируются сущности, роли, этапы и автоматизация, затем интерфейс и интеграции.',
 'faq':[
  ('Что входит в разработку CRM для бизнеса?','Модель клиентов и заявок, роли и права, статусы и история, рабочие экраны, отчёты, автоматизация, API и интеграции с сайтом, 1С, Telegram или другими сервисами.'),
  ('Когда CRM на заказ выгоднее готовой системы?','Когда бизнес-процесс существенно отличается от стандартной воронки, сотрудники постоянно используют обходные схемы, а нужные интеграции и автоматизация становятся дороже поддержки готового продукта.'),
 ]},
'backend-development':{
 'title':'Backend-разработка - API, базы данных и серверная логика | Alexuys',
 'desc':'Backend-разработка: REST API, серверная бизнес-логика, PostgreSQL, авторизация, роли, интеграции, webhooks и фоновые задачи. Разработка и доработка существующего backend.',
 'h1':'Backend-разработка. <em>API, база данных и серверная логика.</em>',
 'demand_h2':'Backend-разработка для сайта, приложения и внутреннего сервиса.',
 'demand_intro':'Backend хранит данные, проверяет права, выполняет бизнес-правила и связывает внешние системы. API и база проектируются вокруг пользовательских сценариев, а не вокруг набора случайных endpoints.',
 'faq':[
  ('Что входит в backend-разработку?','REST API или другой серверный интерфейс, бизнес-логика, работа с базой данных, авторизация и роли, интеграции, фоновые задачи, обработка ошибок и логирование.'),
  ('Можно доработать существующий backend без переписывания?','Да. Обычно сначала воспроизводится проблема или выделяется нужный модуль, после чего изменения вносятся точечно с сохранением работающей части системы.'),
 ]},
'api-development':{
 'title':'Разработка API и REST API - серверный интерфейс для продукта | Alexuys',
 'desc':'Разработка API и REST API: endpoints, авторизация, валидация, webhooks, база данных, документация, интеграции и серверная бизнес-логика для сайта, приложения или сервиса.',
 'h1':'Разработка API и REST API. <em>Понятный контракт между системами.</em>',
 'demand_h2':'Разработка REST API: endpoints, данные, авторизация и ошибки.',
 'demand_intro':'API должен иметь стабильный контракт: понятные endpoints, форматы данных, авторизацию, валидацию и предсказуемые ошибки. Это упрощает frontend, мобильное приложение и интеграции с внешними системами.',
 'faq':[
  ('Что входит в разработку REST API?','Проектирование endpoints и моделей данных, авторизация, валидация, коды ошибок, работа с базой данных, webhooks, ограничения, документация и тестирование основных сценариев.'),
  ('Можно разработать API для существующего проекта?','Да. API можно добавлять постепенно: сначала для одного сценария или интеграции, затем выносить остальные функции по мере необходимости.'),
 ]},
'ios-development':{
 'title':'Разработка приложений для iOS на Swift | Alexuys',
 'desc':'Разработка приложений для iOS на Swift: нативный интерфейс, навигация, состояние, API, авторизация, локальные данные, push-уведомления и доработка существующего iOS проекта.',
 'h1':'Разработка приложений для iOS на Swift. <em>Нативный интерфейс и рабочая логика.</em>',
 'demand_h2':'Разработка iOS-приложения на Swift: интерфейс, данные и API.',
 'demand_intro':'Нативное iOS-приложение начинается с пользовательского сценария, модели данных и взаимодействия с backend. Swift подходит, когда важны системный UX, производительность и глубокая работа с возможностями iPhone.',
 'faq':[
  ('Что входит в разработку приложения для iOS?','Нативные экраны и навигация, состояние приложения, API и авторизация, локальное хранение, обработка ошибок, push-уведомления и системные функции по задаче.'),
  ('Можно доработать существующее iOS-приложение на Swift?','Да. Можно продолжить чужой проект, исправить конкретный сценарий, подключить API или подготовить следующую рабочую версию без обязательной переписки приложения с нуля.'),
 ]},
'app-development':{
 'title':'Разработка мобильных приложений на заказ - iOS и React Native | Alexuys',
 'desc':'Разработка мобильных приложений на заказ: iOS, Swift и React Native, интерфейс, API, данные, авторизация, push-уведомления и рабочая версия для проверки на устройстве.',
 'h1':'Разработка мобильных приложений на заказ. <em>iOS и React Native.</em>',
 'demand_h2':'Заказать разработку мобильного приложения: сначала основной пользовательский путь.',
 'demand_intro':'Для первого релиза важнее один законченный сценарий: пользователь устанавливает приложение, входит, выполняет ключевое действие и получает результат. Архитектура, API и хранение данных строятся вокруг этого пути.',
 'faq':[
  ('Что нужно, чтобы заказать разработку мобильного приложения?','Достаточно описать основной пользовательский путь, показать референс или макет и перечислить системные функции: авторизация, push, карты, платежи, камера, офлайн-режим и нужные API.'),
  ('От чего зависит стоимость мобильного приложения?','От количества сценариев и экранов, backend/API, авторизации, платежей, push-уведомлений, карт, системных функций и количества поддерживаемых платформ.'),
 ]},
}

def page(slug):
 p=ROOT/slug/'index.html'
 if not p.is_file(): raise SystemExit(f'stage196: missing {slug}')
 return p

def set_meta(s,title,desc):
 s=re.sub(r'<title\b[^>]*>.*?</title>',f'<title>{html.escape(title)}</title>',s,count=1,flags=re.I|re.S)
 for attr,key,val in [('name','description',desc),('property','og:title',title),('property','og:description',desc),('name','twitter:title',title),('name','twitter:description',desc)]:
  pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
  repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
  s=re.sub(pat,repl,s,count=1,flags=re.I) if re.search(pat,s,re.I) else s.replace('</head>',repl+'</head>',1)
 return s

def set_h1(s,value,slug):
 s,n=re.subn(r'<h1\b([^>]*)>.*?</h1>',lambda m:f'<h1{m.group(1)}>{value}</h1>',s,count=1,flags=re.I|re.S)
 if n!=1: raise SystemExit(f'stage196: h1 missing {slug}')
 return s

def fit_h1(s,slug):
 marker=f'stage196-hero-fit-{slug}'
 if marker in s:return s
 sel=f'html body[data-page="{slug}"] main.p129-service .p129-svc-hero .p129-svc-copy h1'
 style=('<style id="%s">@media(min-width:901px){%s{font-size:78px!important;line-height:.91!important;letter-spacing:-.058em!important}}@media(min-width:901px) and (max-width:1199px){%s{font-size:58px!important;line-height:.92!important;letter-spacing:-.055em!important}}</style>')%(marker,sel,sel)
 return s.replace('</head>',style+'</head>',1)

def update_demand(s,slug,h2,intro):
 patterns=[
  r'(<section class="search-demand".*?<div class="search-demand__head">.*?<div><h2[^>]*>)(.*?)(</h2><p class="search-demand__intro">)(.*?)(</p>)',
  r'(<section class="secondary-demand".*?<div class="secondary-demand__head">.*?<div><h2>)(.*?)(</h2><p class="secondary-demand__intro">)(.*?)(</p>)',
 ]
 for pat in patterns:
  m=re.search(pat,s,re.I|re.S)
  if m:
   return s[:m.start()]+m.group(1)+h2+m.group(3)+intro+m.group(5)+s[m.end():]
 raise SystemExit(f'stage196: demand section missing {slug}')

def add_faq(s,slug,items):
 marker=f'data-stage196-faq="{slug}"'
 if marker not in s:
  m=re.search(r'(<div class="stage174-faq__grid">)(.*?)(</div></div></section>)',s,re.I|re.S)
  if m:
   extra=''.join(f'<details {marker}><summary>{q}</summary><p>{a}</p></details>' for q,a in items)
   s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
  else:
   m=re.search(r'(<section class="secondary-demand"[^>]*data-stage172-faq="true".*?<div class="secondary-demand__grid">)(.*?)(</div></div></section>)',s,re.I|re.S)
   if m:
    extra=''.join(f'<article {marker} class="secondary-demand__card"><h3>{q}</h3><p>{a}</p></article>' for q,a in items)
    s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
   else:
    # iOS currently has no FAQ section: add one before contact and reuse local secondary-demand styling.
    contact=s.find('<section class="p129-contact')
    if contact<0:raise SystemExit(f'stage196: contact anchor missing {slug}')
    cards=''.join(f'<article {marker} class="secondary-demand__card"><h3>{q}</h3><p>{a}</p></article>' for q,a in items)
    block=f'<section class="secondary-demand" data-stage196-faq-section="true"><div class="secondary-demand__shell"><div class="secondary-demand__head"><p class="secondary-demand__eyebrow">FAQ</p><div><h2>Перед стартом разработки.</h2><p class="secondary-demand__intro">Коротко о том, что входит в работу и как продолжить существующий проект.</p></div></div><div class="secondary-demand__grid">{cards}</div></div></section>'
    s=s[:contact]+block+s[contact:]
 # FAQ schema: update existing or create one.
 sm=None
 for cand in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.I|re.S):
  if '"FAQPage"' in cand.group(1):sm=cand;break
 if sm:
  obj=json.loads(sm.group(1));names={x.get('name') for x in obj.get('mainEntity',[])}
  for q,a in items:
   if q not in names:obj.setdefault('mainEntity',[]).append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}})
  blob=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
  s=s[:sm.start(1)]+blob+s[sm.end(1):]
 else:
  obj={'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in items]}
  blob='<script type="application/ld+json" data-stage196-faq-schema="true">'+json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'</script>'
  s=s.replace('</head>',blob+'</head>',1)
 return s

def sync_schema(s,title,desc):
 name=re.sub(r'\s*\|\s*Alexuys\s*$','',title).strip();out=[];last=0;touched=0
 for m in re.finditer(r'<script([^>]*)type="application/ld\+json"([^>]*)>(.*?)</script>',s,re.I|re.S):
  try:o=json.loads(m.group(3))
  except:continue
  if o.get('@type') not in ['Service','WebPage']:continue
  o['name']=name;o['description']=desc
  out.append(s[last:m.start(3)]);out.append(json.dumps(o,ensure_ascii=False,separators=(',',':')));last=m.end(3);touched+=1
 if touched:out.append(s[last:]);s=''.join(out)
 return s

changed=[]
for slug,c in CFG.items():
 p=page(slug);s=p.read_text(encoding='utf-8')
 s=set_meta(s,c['title'],c['desc']);s=set_h1(s,c['h1'],slug);s=fit_h1(s,slug)
 s=update_demand(s,slug,c['demand_h2'],c['demand_intro']);s=add_faq(s,slug,c['faq']);s=sync_schema(s,c['title'],c['desc'])
 p.write_text(s,encoding='utf-8');changed.append('/'+slug+'/')

for name in ('sitemap.xml','sitemap-google.xml'):
 p=ROOT/name
 if not p.exists():continue
 text=p.read_text(encoding='utf-8')
 for route in changed:text=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
 p.write_text(text,encoding='utf-8')

for slug,c in CFG.items():
 s=page(slug).read_text(encoding='utf-8')
 for needle in [c['title'],c['desc'],c['demand_h2'],f'data-stage196-faq="{slug}"',f'stage196-hero-fit-{slug}']:
  if needle not in s:raise SystemExit(f'stage196: guard failed {slug}: {needle}')
 if s.count(f'data-stage196-faq="{slug}"')!=len(c['faq']):raise SystemExit(f'stage196: faq count failed {slug}')
 for q,_ in c['faq']:
  if s.count(q)<2:raise SystemExit(f'stage196: FAQ/schema mismatch {slug}: {q}')
print(f'stage196 russian backend/mobile/crm: pages={len(changed)}, faq={sum(len(c["faq"]) for c in CFG.values())}')
