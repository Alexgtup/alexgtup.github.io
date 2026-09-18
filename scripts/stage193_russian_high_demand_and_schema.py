#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'

def path(slug):
 p=ROOT/slug/'index.html'
 if not p.is_file(): raise SystemExit(f'stage193: missing {slug}')
 return p

def set_meta(s,title=None,desc=None):
 if title:
  s=re.sub(r'<title\b[^>]*>.*?</title>',f'<title>{html.escape(title)}</title>',s,count=1,flags=re.I|re.S)
  for attr,key in [('property','og:title'),('name','twitter:title')]:
   pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
   repl=f'<meta {attr}="{key}" content="{html.escape(title,quote=True)}"/>'
   s=re.sub(pat,repl,s,count=1,flags=re.I) if re.search(pat,s,re.I) else s.replace('</head>',repl+'</head>',1)
 if desc:
  for attr,key in [('name','description'),('property','og:description'),('name','twitter:description')]:
   pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
   repl=f'<meta {attr}="{key}" content="{html.escape(desc,quote=True)}"/>'
   s=re.sub(pat,repl,s,count=1,flags=re.I) if re.search(pat,s,re.I) else s.replace('</head>',repl+'</head>',1)
 return s

def replace_h1(s,value,slug):
 s,n=re.subn(r'<h1\b([^>]*)>.*?</h1>',lambda m:f'<h1{m.group(1)}>{value}</h1>',s,count=1,flags=re.I|re.S)
 if n!=1: raise SystemExit(f'stage193: h1 missing {slug}')
 return s


def fit_desktop_h1(s,slug):
 marker=f'stage193-hero-fit-{slug}'
 if marker in s: return s
 selector=f'html body[data-page="{slug}"] main.p129-service .p129-svc-hero .p129-svc-copy h1'
 style=('<style id="%s">'
        '@media(min-width:901px){%s{font-size:78px!important;line-height:.91!important;letter-spacing:-.058em!important}}'
        '@media(min-width:901px) and (max-width:1199px){%s{font-size:58px!important;line-height:.92!important;letter-spacing:-.055em!important}}'
        '</style>') % (marker,selector,selector)
 return s.replace('</head>',style+'</head>',1)

def add_stage174_faq(s,slug,q,a):
 marker=f'data-stage193-faq="{slug}"'
 if marker not in s:
  m=re.search(r'(<div class="stage174-faq__grid">)(.*?)(</div></div></section>)',s,re.I|re.S)
  if not m: raise SystemExit(f'stage193: stage174 FAQ missing {slug}')
  extra=f'<details {marker}><summary>{q}</summary><p>{a}</p></details>'
  s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
 sm=re.search(r'<script id="stage174-faq-schema" type="application/ld\+json">(.*?)</script>',s,re.I|re.S)
 if not sm: raise SystemExit(f'stage193: FAQ schema missing {slug}')
 obj=json.loads(sm.group(1)); names={x.get('name') for x in obj.get('mainEntity',[])}
 if q not in names: obj.setdefault('mainEntity',[]).append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}})
 blob=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
 s=s[:sm.start(1)]+blob+s[sm.end(1):]
 return s

def add_bridge_link(s,label):
 if '/guides/development-cost/' in s: return s
 link=f'<a href="/guides/development-cost/">{label} ↗</a>'
 m=re.search(r'(<section class="p131-bridge"[^>]*>.*?<div class="p131-bridge__inner">.*?)(</div></section>)',s,re.I|re.S)
 if m:
  return s[:m.start()]+m.group(1)+link+m.group(2)+s[m.end():]
 # Some service pages use secondary-demand links instead of a bridge.
 m=re.search(r'(<nav class="secondary-demand__links"[^>]*>.*?)(</nav>)',s,re.I|re.S)
 if m:
  return s[:m.start()]+m.group(1)+link+m.group(2)+s[m.end():]
 return s

changed=[]

# WEB: high-volume “сайт под ключ” / “создание сайта под ключ”, without creating a competing URL.
p=path('web-development'); s=p.read_text(encoding='utf-8')
if 'data-stage193-site-turnkey="true"' not in s:
 old_head='Веб-приложение на заказ: интерфейс, данные и backend как один продукт.'
 new_head='Сайт под ключ и веб-приложение на заказ: от структуры до запуска.'
 if old_head not in s: raise SystemExit('stage193: web search-demand heading missing')
 s=s.replace(old_head,new_head,1)
 old_intro='Веб-приложение - это рабочий сценарий: пользователь входит, выполняет действие, данные сохраняются, а система выдаёт результат. Поэтому интерфейс, backend и интеграции проектируются вместе.'
 new_intro='Для сайта под ключ важен полный рабочий путь: структура и контент, интерфейс, адаптив, формы, нужная серверная логика, интеграции и публикация. Для веб-приложения к этому добавляются состояние пользователя, данные, роли и действия внутри системы.'
 s=s.replace(old_intro,new_intro,1)
 old_card='<article class="search-demand__card"><h3>Личный кабинет</h3><p>Авторизация, роли, данные пользователя, формы, документы, статусы и действия внутри системы.</p></article>'
 new_card='<article class="search-demand__card" data-stage193-site-turnkey="true"><h3>Создание сайта под ключ</h3><p>Структура, интерфейс, адаптив, формы, CMS или backend, интеграции, техническая проверка и публикация в одном законченном сценарии.</p></article>'
 if old_card not in s: raise SystemExit('stage193: web card marker missing')
 s=s.replace(old_card,new_card,1)
s=add_bridge_link(s,'Стоимость разработки сайта')
s=fit_desktop_h1(s,'web-development')
s=add_stage174_faq(s,'web-development','Что входит в создание сайта под ключ?','Структура и пользовательский сценарий, интерфейс, адаптив, формы, CMS или backend при необходимости, интеграции, техническая проверка и публикация. Состав зависит от типа сайта и готовности исходных материалов.')
p.write_text(s,encoding='utf-8');changed.append('/web-development/')

# SOFTWARE: capture “разработка ПО на заказ”, “создание ПО на заказ” and software for business.
p=path('development'); s=p.read_text(encoding='utf-8')
if 'data-stage193-software-order="true"' not in s:
 anchor='<section class="stage172-task-map"'
 i=s.find(anchor)
 if i<0: raise SystemExit('stage193: development task-map anchor missing')
 block='''<section class="secondary-demand" data-stage193-software-order="true"><div class="secondary-demand__shell"><div class="secondary-demand__head"><p class="secondary-demand__eyebrow">ПО / НА ЗАКАЗ</p><div><h2>Разработка ПО на заказ для бизнеса.</h2><p class="secondary-demand__intro">Когда готовый сервис не повторяет реальный процесс, программное обеспечение можно собрать под конкретных пользователей, данные и правила — от одного рабочего модуля до внутренней системы.</p></div></div><div class="secondary-demand__grid"><article class="secondary-demand__card"><h3>Внутренняя система</h3><p>Роли, заявки, статусы, документы, данные и действия сотрудников в одном рабочем контуре.</p></article><article class="secondary-demand__card"><h3>Backend и интеграции</h3><p>API, базы данных, внешние сервисы и автоматизация соединяются вокруг бизнес-логики, а не существуют отдельно.</p></article><article class="secondary-demand__card"><h3>Запуск по этапам</h3><p>Создание ПО можно начать с минимального законченного сценария, проверить его и только затем расширять систему.</p></article></div><nav class="secondary-demand__links" aria-label="Связанные материалы"><a href="/guides/development-cost/">Стоимость разработки ПО ↗</a><a href="/backend-development/">Backend-разработка ↗</a><a href="/crm-development/">CRM на заказ ↗</a></nav></div></section>'''
 s=s[:i]+block+s[i:]
s=add_bridge_link(s,'Стоимость разработки ПО')
s=fit_desktop_h1(s,'development')
s=add_stage174_faq(s,'development','Что входит в разработку ПО на заказ?','Рабочие сценарии, модель данных, роли и права, интерфейс при необходимости, backend, API и интеграции, тестирование и запуск. Большой проект можно разделить на законченные этапы.')
p.write_text(s,encoding='utf-8');changed.append('/development/')

# AI: high-volume “ИИ для бизнеса” owns this page; keep development/automation language in body and description.
p=path('ai-automation'); s=p.read_text(encoding='utf-8')
ai_title='ИИ для бизнеса и AI-автоматизация | Alexuys'
ai_desc='ИИ для бизнеса и AI-автоматизация: AI-агенты, обработка текста и данных, поиск, классификация, API, n8n и интеграция ИИ в существующие рабочие процессы.'
s=set_meta(s,ai_title,ai_desc)
s=replace_h1(s,'ИИ для бизнеса и AI-автоматизация. <em>Внутри реального процесса.</em>','ai-automation')
s=s.replace('AI автоматизация: модель должна закрывать конкретный шаг процесса.','ИИ для бизнеса: модель должна закрывать конкретный шаг процесса.',1)
s=s.replace('AI имеет смысл внедрять там, где понятны входные данные, ожидаемый результат и способ проверить ответ. Это может быть классификация, извлечение данных, подготовка черновика, анализ файла или следующий шаг внутри автоматизированного workflow.','ИИ для бизнеса имеет смысл внедрять там, где понятны входные данные, ожидаемый результат и способ проверить ответ: классификация, извлечение данных, подготовка черновика, поиск, анализ файла или следующий шаг внутри автоматизированного workflow.',1)
s=add_bridge_link(s,'Стоимость разработки')
s=fit_desktop_h1(s,'ai-automation')
p.write_text(s,encoding='utf-8');changed.append('/ai-automation/')

# App: give the cost guide a strong contextual inbound link without changing its already-good intent.
p=path('app-development'); s=p.read_text(encoding='utf-8')
s=add_bridge_link(s,'Стоимость разработки приложения')
s=fit_desktop_h1(s,'app-development')
p.write_text(s,encoding='utf-8');changed.append('/app-development/')

# Synchronize stale Service/WebPage JSON-LD with the current visible title and description.
service_slugs=['development','web-development','app-development','automation-services','ai-automation','crm-development','mvp-development','api-integrations','bitrix-development','tilda-development','wordpress-development','excel-google-sheets-automation','backend-development','project-repair']
for slug in service_slugs:
 p=path(slug); s=p.read_text(encoding='utf-8')
 tm=re.search(r'<title[^>]*>(.*?)</title>',s,re.I|re.S)
 dm=re.search(r'<meta\b(?=[^>]*name=["\']description["\'])[^>]*content=["\']([^"\']*)',s,re.I|re.S)
 if not tm or not dm: raise SystemExit(f'stage193: meta missing for schema sync {slug}')
 title=html.unescape(re.sub('<[^>]+>','',tm.group(1))).strip()
 name=re.sub(r'\s*\|\s*Alexuys\s*$','',title).strip()
 desc=html.unescape(dm.group(1)).strip()
 out=[]; last=0; touched=0
 for m in re.finditer(r'<script([^>]*)type="application/ld\+json"([^>]*)>(.*?)</script>',s,re.I|re.S):
  try: obj=json.loads(m.group(3))
  except: continue
  if obj.get('@type') not in ['Service','WebPage']: continue
  obj['name']=name; obj['description']=desc
  blob=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
  out.append(s[last:m.start(3)]); out.append(blob); last=m.end(3); touched+=1
 if touched:
  out.append(s[last:]); s=''.join(out)
 p.write_text(s,encoding='utf-8')

# Fresh lastmod for changed content pages.
for name in ('sitemap.xml','sitemap-google.xml'):
 sp=ROOT/name
 if not sp.exists(): continue
 text=sp.read_text(encoding='utf-8')
 for route in changed:
  text=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
 sp.write_text(text,encoding='utf-8')

# Guards.
checks={
 'web-development':['data-stage193-site-turnkey="true"','Создание сайта под ключ','Стоимость разработки сайта ↗'],
 'development':['data-stage193-software-order="true"','Разработка ПО на заказ для бизнеса.','Что входит в разработку ПО на заказ?'],
 'ai-automation':[ai_title,ai_desc,'ИИ для бизнеса: модель должна закрывать конкретный шаг процесса.'],
 'app-development':['Стоимость разработки приложения ↗'],
}
for slug,needles in checks.items():
 data=path(slug).read_text(encoding='utf-8')
 for needle in needles:
  if needle not in data: raise SystemExit(f'stage193: guard failed {slug}: {needle}')
# Ensure stale web schema price claim is gone after sync.
web=path('web-development').read_text(encoding='utf-8')
if 'Разработка сайтов и веб-сервисов от 15 000 ₽' in web: raise SystemExit('stage193: stale web schema description remains')
print(f'stage193 russian high demand + schema sync: changed={len(changed)}, schema_pages={len(service_slugs)}')
