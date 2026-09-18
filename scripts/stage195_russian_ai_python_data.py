#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'

CFG={
'ai-chatbot-development':{
 'title':'Разработка ИИ-агентов и AI-ассистентов для бизнеса | Alexuys',
 'desc':'Разработка ИИ-агентов и AI-ассистентов для бизнеса: Telegram и сайт, база знаний, API, инструменты, structured output, автоматизация, контроль действий и передача человеку.',
 'h1':'Разработка ИИ-агентов и AI-ассистентов. <em>Для реального бизнес-процесса.</em>',
 'task_h2':'ИИ-агент для бизнеса: знания, инструменты и контролируемые действия.',
 'task_intro':'ИИ-агент полезен не как отдельный чат, а когда умеет работать с контекстом, обращаться к API и внутренним данным, выполнять ограниченный набор действий и передавать сложные случаи человеку.',
 'faq':[
  ('Что входит в разработку ИИ-агента?','Определение сценария и доступных действий, подключение модели и данных, инструменты или API, ограничения, журналирование, проверка результата и human handoff для критичных случаев.'),
  ('Можно разработать ИИ-агента для существующего бизнеса?','Да. Агент может работать внутри текущего сайта, CRM, Telegram, внутреннего сервиса или n8n-процесса, не требуя отдельного большого продукта.'),
  ('От чего зависит стоимость разработки ИИ-агента?','От числа сценариев и инструментов, объёма данных и базы знаний, интеграций, требований к качеству ответа, памяти, правам доступа и контролю действий.'),
 ]},
'python-scripts':{
 'title':'Python-автоматизация и скрипты на заказ | Alexuys',
 'desc':'Python-автоматизация и скрипты на заказ: файлы и данные, Excel, API, парсинг, отчёты, фоновые задачи, интеграции и автоматизация повторяющихся операций.',
 'h1':'Python-автоматизация и скрипты. <em>Убрать повторяющиеся ручные задачи.</em>',
 'task_h2':'Автоматизация на Python: файлы, API, данные и регулярные задачи.',
 'task_intro':'Python подходит, когда нужно обрабатывать много файлов, преобразовывать данные, работать с API, запускать задачу по расписанию или автоматизировать процесс, для которого готового no-code сценария уже недостаточно.',
 'faq':[
  ('Какие задачи можно автоматизировать на Python?','Обработку файлов и таблиц, выгрузки и загрузки через API, формирование отчётов, парсинг, проверки данных, генерацию документов и фоновые задачи по расписанию.'),
  ('Когда Python лучше n8n или Make?','Когда логика сложная, данных много, нужны собственные библиотеки, длительная обработка, нестандартные форматы или полный контроль над кодом и окружением.'),
 ]},
'web-scraping-parsers':{
 'title':'Парсинг сайтов на Python - разработка парсеров данных | Alexuys',
 'desc':'Парсинг сайтов на Python и разработка парсеров: HTML/JSON, API, товары и каталоги, CSV/XLSX, дедупликация, обработка данных, расписание и мониторинг изменений.',
 'h1':'Парсинг сайтов и данных на Python. <em>Сбор, очистка и выгрузка результата.</em>',
 'task_h2':'Парсинг сайтов: собрать данные и привести их к рабочему формату.',
 'task_intro':'Парсер должен не просто скачать страницу, а стабильно получить нужные поля, очистить и нормализовать данные, убрать дубли и сохранить результат в CSV, Excel, базу данных или другой сервис.',
 'faq':[
  ('Что входит в парсинг сайта?','Определение источников и полей, получение HTML/JSON или данных через API, разбор структуры, нормализация, дедупликация, сохранение результата и обработка ошибок.'),
  ('Можно настроить регулярный парсинг сайтов?','Да. Парсер можно запускать по расписанию, сравнивать новые данные с предыдущими, сохранять изменения и отправлять результат в файл, базу, CRM или API.'),
 ]},
'personal-cabinet-development':{
 'title':'Разработка личного кабинета для сайта на заказ | Alexuys',
 'desc':'Разработка личного кабинета для сайта на заказ: авторизация, профиль, заявки, документы, платежи, роли, статусы, уведомления, API и административная часть.',
 'h1':'Разработка личного кабинета для сайта. <em>Данные, роли и действия пользователя.</em>',
 'task_h2':'Личный кабинет для сайта: авторизация, данные, документы и действия.',
 'task_intro':'Личный кабинет нужен там, где пользователь возвращается к своим данным: заявкам, документам, заказам, оплатам или статусам. Основу составляют авторизация, роли, модель данных и понятные действия внутри интерфейса.',
 'faq':[
  ('Что входит в разработку личного кабинета для сайта?','Авторизация и восстановление доступа, профиль пользователя, нужные сущности и статусы, формы и документы, API, уведомления и административные действия по задаче.'),
  ('Можно добавить личный кабинет к существующему сайту?','Да, если текущий стек позволяет подключить backend и авторизацию или связать сайт с отдельным сервисом через API. Полная пересборка сайта требуется не всегда.'),
 ]},
}

def page(slug):
 p=ROOT/slug/'index.html'
 if not p.is_file(): raise SystemExit(f'stage195: missing {slug}')
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
 if n!=1: raise SystemExit(f'stage195: h1 missing {slug}')
 return s

def fit_h1(s,slug):
 marker=f'stage195-hero-fit-{slug}'
 if marker in s:return s
 sel=f'html body[data-page="{slug}"] main.p129-service .p129-svc-hero .p129-svc-copy h1'
 style=('<style id="%s">@media(min-width:901px){%s{font-size:78px!important;line-height:.91!important;letter-spacing:-.058em!important}}@media(min-width:901px) and (max-width:1199px){%s{font-size:58px!important;line-height:.92!important;letter-spacing:-.055em!important}}</style>')%(marker,sel,sel)
 return s.replace('</head>',style+'</head>',1)

def update_task(s,slug,h2,intro):
 pat=r'(<section class="secondary-demand"[^>]*data-stage172-tasks="true".*?<div class="secondary-demand__head">.*?<div><h2>)(.*?)(</h2><p class="secondary-demand__intro">)(.*?)(</p>)'
 m=re.search(pat,s,re.I|re.S)
 if not m: raise SystemExit(f'stage195: task section missing {slug}')
 return s[:m.start()]+m.group(1)+h2+m.group(3)+intro+m.group(5)+s[m.end():]

def add_faq(s,slug,items):
 marker=f'data-stage195-faq="{slug}"'
 if marker not in s:
  m=re.search(r'(<section class="secondary-demand"[^>]*data-stage172-faq="true".*?<div class="secondary-demand__grid">)(.*?)(</div></div></section>)',s,re.I|re.S)
  if not m: raise SystemExit(f'stage195: visible FAQ missing {slug}')
  extra=''.join(f'<article {marker} class="secondary-demand__card"><h3>{q}</h3><p>{a}</p></article>' for q,a in items)
  s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
 sm=None
 for cand in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.I|re.S):
  if '"FAQPage"' in cand.group(1):sm=cand;break
 if not sm: raise SystemExit(f'stage195: FAQ schema missing {slug}')
 obj=json.loads(sm.group(1));names={x.get('name') for x in obj.get('mainEntity',[])}
 for q,a in items:
  if q not in names:obj.setdefault('mainEntity',[]).append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}})
 blob=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
 return s[:sm.start(1)]+blob+s[sm.end(1):]

def add_related_link(s,href,label):
 if href in s:return s
 m=re.search(r'(<nav class="secondary-demand__links"[^>]*>.*?)(</nav>)',s,re.I|re.S)
 if not m:return s
 link=f'<a href="{href}">{label} ↗</a>'
 return s[:m.start()]+m.group(1)+link+m.group(2)+s[m.end():]

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
 s=update_task(s,slug,c['task_h2'],c['task_intro']);s=add_faq(s,slug,c['faq'])
 if slug=='ai-chatbot-development':s=add_related_link(s,'/ai-automation/','ИИ-автоматизация для бизнеса')
 if slug=='python-scripts':s=add_related_link(s,'/web-scraping-parsers/','Парсинг сайтов на Python')
 if slug=='web-scraping-parsers':s=add_related_link(s,'/python-scripts/','Python-автоматизация')
 if slug=='personal-cabinet-development':s=add_related_link(s,'/web-development/','Сайты и веб-приложения')
 s=sync_schema(s,c['title'],c['desc']);p.write_text(s,encoding='utf-8');changed.append('/'+slug+'/')

for name in ('sitemap.xml','sitemap-google.xml'):
 p=ROOT/name
 if not p.exists():continue
 text=p.read_text(encoding='utf-8')
 for route in changed:text=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
 p.write_text(text,encoding='utf-8')

for slug,c in CFG.items():
 s=page(slug).read_text(encoding='utf-8')
 for needle in [c['title'],c['desc'],c['task_h2'],f'data-stage195-faq="{slug}"',f'stage195-hero-fit-{slug}']:
  if needle not in s:raise SystemExit(f'stage195: guard failed {slug}: {needle}')
 if s.count(f'data-stage195-faq="{slug}"')!=len(c['faq']):raise SystemExit(f'stage195: faq count failed {slug}')
 for q,_ in c['faq']:
  if s.count(q)<2:raise SystemExit(f'stage195: FAQ/schema mismatch {slug}: {q}')
print(f'stage195 russian ai/python/data: pages={len(changed)}, faq={sum(len(c["faq"]) for c in CFG.values())}')
