#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'

CFG={
'1c-integration':{
 'title':'Интеграция 1С - настройка обмена с сайтом, CRM и API | Alexuys',
 'desc':'Интеграция 1С: настройка обмена с сайтом, CRM, каталогом и API — товары, цены, остатки, заказы, клиенты, статусы, документы и синхронизация.',
 'h1':'Интеграция 1С с сайтом, CRM и API. <em>Обмен данными без ручного переноса.</em>',
 'task_h2':'Настройка интеграции 1С: какие данные связываются.',
 'task_intro':'Интеграция может передавать каталог, цены, остатки, заказы, клиентов, статусы и документы. Сначала определяется источник каждого поля, направление обмена и поведение при ошибке.',
 'faq':[
  ('Что входит в настройку интеграции 1С?','Определение объектов обмена, сопоставление полей и идентификаторов, способ передачи данных, обработка повторов и ошибок, журнал обмена и проверка сценария на реальных данных.'),
  ('Можно интегрировать 1С с сайтом, CRM и внешним API?','Да, если у систем есть поддерживаемый способ обмена. 1С может быть источником каталога, заказов или справочников, а сайт и CRM — получать и возвращать нужные статусы и данные.'),
 ]},
'ecommerce-development':{
 'title':'Разработка интернет-магазина на заказ | Alexuys',
 'desc':'Разработка интернет-магазина на заказ: каталог, фильтры, корзина, checkout, личный кабинет, онлайн-оплата, доставка, CRM, 1С и API. Можно запускать по этапам.',
 'h1':'Разработка интернет-магазина на заказ. <em>Каталог, корзина, оплата и интеграции.</em>',
 'task_h2':'Разработка интернет-магазина: от каталога до оплаченного заказа.',
 'task_intro':'Для магазина важен не только каталог: товары должны находиться, корзина — сохранять состояние, заказ — корректно создаваться, оплата и доставка — возвращать статусы, а CRM или 1С — получать нужные данные.',
 'faq':[
  ('Что входит в разработку интернет-магазина под ключ?','Каталог и карточки товаров, поиск и фильтры, корзина, checkout, оплата и доставка, адаптивная версия, интеграции и публикация. Личный кабинет и сложные обмены добавляются по задаче.'),
  ('От чего зависит цена разработки интернет-магазина?','От размера и структуры каталога, фильтров, вариантов цены, checkout, личного кабинета, способов оплаты и доставки, интеграций с CRM/1С и состояния существующего проекта.'),
 ]},
'site-repair':{
 'title':'Доработка сайта на заказ - исправления и новый функционал | Alexuys',
 'desc':'Доработка сайта на заказ: ошибки, мобильная версия, формы, JavaScript, backend, API, интеграции, скорость, SEO, WordPress и чужой код без обязательной пересборки.',
 'h1':'Доработка сайта на заказ. <em>Исправить ошибку или добавить новый функционал.</em>',
 'task_h2':'Доработка сайта: от одной ошибки до нового функционала.',
 'task_intro':'Можно исправить конкретную проблему или продолжить существующий проект: мобильную версию, формы, JavaScript, backend, интеграции, скорость, SEO или новый раздел — без обязательного переписывания всего сайта.',
 'faq':[
  ('От чего зависит стоимость доработки сайта?','От причины проблемы, доступности исходного кода и окружения, количества затронутых шаблонов, backend-логики и интеграций. Небольшую независимую правку можно оценивать отдельно.'),
 ]},
'crm-integration':{
 'title':'Интеграция CRM с сайтом, 1С, Telegram и API | Alexuys',
 'desc':'Интеграция CRM с сайтом, 1С, Telegram, формами и внешними сервисами: заявки, клиенты, статусы, webhooks, API, уведомления и синхронизация данных.',
 'h1':'Интеграция CRM с сайтом, 1С, Telegram и API. <em>Заявки и статусы без ручного переноса.</em>',
 'task_h2':'Интеграция CRM: сайт, 1С, мессенджеры и внешние сервисы.',
 'task_intro':'CRM может принимать заявки с сайта и Telegram, обмениваться данными с 1С, телефонией, оплатой и внутренними системами. Для надёжной интеграции заранее фиксируются идентификаторы, направление обмена и правила обновления полей.',
 'faq':[
  ('Что входит в интеграцию CRM?','Настройка сущностей и полей, API или webhooks, передача заявок и статусов, защита от дублей, обработка ошибок, логирование и проверка обмена между системами.'),
 ]},
'payment-integration':{
 'title':'Интеграция оплаты на сайт и в приложение | Alexuys',
 'desc':'Интеграция оплаты на сайт, в приложение или Telegram-бот: платежный API, checkout, webhooks, статусы заказа, возвраты, подписки, чеки и выдача доступа после серверной проверки.',
 'h1':'Интеграция оплаты на сайт, в приложение и бота. <em>Checkout, webhooks и статусы.</em>',
 'task_h2':'Интеграция оплаты: checkout, webhooks, статусы и доступ.',
 'task_intro':'Платёжный сценарий включает не только кнопку оплаты: заказ или подписка создаётся на сервере, пользователь проходит checkout, backend получает webhook, проверяет событие и меняет статус или выдаёт доступ.',
 'faq':[
  ('Что входит в подключение оплаты на сайт?','Создание платежа на сервере, checkout или платёжная ссылка, обработка webhooks, безопасное обновление статуса заказа, повторные уведомления, возвраты и выдача результата после подтверждённой оплаты.'),
 ]},
}

def page(slug):
 p=ROOT/slug/'index.html'
 if not p.is_file(): raise SystemExit(f'stage194: missing {slug}')
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
 if n!=1: raise SystemExit(f'stage194: h1 missing {slug}')
 return s

def fit_h1(s,slug):
 marker=f'stage194-hero-fit-{slug}'
 if marker in s:return s
 sel=f'html body[data-page="{slug}"] main.p129-service .p129-svc-hero .p129-svc-copy h1'
 style=('<style id="%s">@media(min-width:901px){%s{font-size:78px!important;line-height:.91!important;letter-spacing:-.058em!important}}@media(min-width:901px) and (max-width:1199px){%s{font-size:58px!important;line-height:.92!important;letter-spacing:-.055em!important}}</style>')%(marker,sel,sel)
 return s.replace('</head>',style+'</head>',1)

def update_task_section(s,slug,h2,intro):
 pat=r'(<section class="secondary-demand"[^>]*data-stage172-tasks="true".*?<div class="secondary-demand__head">.*?<div><h2>)(.*?)(</h2><p class="secondary-demand__intro">)(.*?)(</p>)'
 m=re.search(pat,s,re.I|re.S)
 if not m: raise SystemExit(f'stage194: task section missing {slug}')
 return s[:m.start()]+m.group(1)+h2+m.group(3)+intro+m.group(5)+s[m.end():]

def add_faq(s,slug,items):
 marker=f'data-stage194-faq="{slug}"'
 if marker not in s:
  m=re.search(r'(<section class="secondary-demand"[^>]*data-stage172-faq="true".*?<div class="secondary-demand__grid">)(.*?)(</div></div></section>)',s,re.I|re.S)
  if not m: raise SystemExit(f'stage194: visible FAQ missing {slug}')
  extra=''.join(f'<article {marker} class="secondary-demand__card"><h3>{q}</h3><p>{a}</p></article>' for q,a in items)
  s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
 sm=None
 for cand in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.I|re.S):
  if '"FAQPage"' in cand.group(1): sm=cand; break
 if not sm: raise SystemExit(f'stage194: FAQ schema missing {slug}')
 obj=json.loads(sm.group(1));names={x.get('name') for x in obj.get('mainEntity',[])}
 for q,a in items:
  if q not in names: obj.setdefault('mainEntity',[]).append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}})
 blob=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
 return s[:sm.start(1)]+blob+s[sm.end(1):]

def sync_schema(s,title,desc):
 name=re.sub(r'\s*\|\s*Alexuys\s*$','',title).strip()
 out=[];last=0;touched=0
 for m in re.finditer(r'<script([^>]*)type="application/ld\+json"([^>]*)>(.*?)</script>',s,re.I|re.S):
  try:o=json.loads(m.group(3))
  except:continue
  if o.get('@type') not in ['Service','WebPage']:continue
  o['name']=name;o['description']=desc
  out.append(s[last:m.start(3)]);out.append(json.dumps(o,ensure_ascii=False,separators=(',',':')));last=m.end(3);touched+=1
 if touched:
  out.append(s[last:]);s=''.join(out)
 return s

changed=[]
for slug,c in CFG.items():
 p=page(slug);s=p.read_text(encoding='utf-8')
 s=set_meta(s,c['title'],c['desc']);s=set_h1(s,c['h1'],slug);s=fit_h1(s,slug)
 s=update_task_section(s,slug,c['task_h2'],c['task_intro']);s=add_faq(s,slug,c['faq']);s=sync_schema(s,c['title'],c['desc'])
 p.write_text(s,encoding='utf-8');changed.append('/'+slug+'/')

for name in ('sitemap.xml','sitemap-google.xml'):
 p=ROOT/name
 if not p.exists():continue
 text=p.read_text(encoding='utf-8')
 for route in changed:
  text=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
 p.write_text(text,encoding='utf-8')

for slug,c in CFG.items():
 s=page(slug).read_text(encoding='utf-8')
 for needle in [c['title'],c['desc'],c['task_h2'],f'data-stage194-faq="{slug}"',f'stage194-hero-fit-{slug}']:
  if needle not in s: raise SystemExit(f'stage194: guard failed {slug}: {needle}')
 if s.count(f'data-stage194-faq="{slug}"')!=len(c['faq']):raise SystemExit(f'stage194: faq count failed {slug}')
 for q,_ in c['faq']:
  if s.count(q)<2:raise SystemExit(f'stage194: FAQ/schema mismatch {slug}: {q}')
print(f'stage194 russian integrations/commerce: pages={len(changed)}, faq={sum(len(c["faq"]) for c in CFG.values())}')
