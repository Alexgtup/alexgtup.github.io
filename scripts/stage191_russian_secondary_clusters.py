#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'

CFG={
'api-integrations':{
 'title':'API-интеграция на заказ - интеграция систем через API | Alexuys',
 'desc':'API-интеграция на заказ: настройка обмена данными между сайтом, CRM, Telegram, платежами, 1С и внешними сервисами. REST API, webhooks, авторизация, логи и обработка ошибок.',
 'h1':'API-интеграция систем. <em>CRM, сайт, Telegram и внешние сервисы.</em>',
 'faq':[
  ('Что входит в настройку интеграции API?','Проверка документации и доступов, схема обмена данными, авторизация, запросы или webhooks, преобразование данных, обработка ошибок, логирование и проверка рабочего сценария.'),
  ('Можно связать несколько систем через REST API?','Да. Если сервисы предоставляют API или webhooks, можно связать сайт, CRM, платежи, Telegram, 1С и другие системы в один контролируемый поток данных.'),
 ]},
'bitrix-development':{
 'title':'Разработка и доработка сайта на 1С-Битрикс | Alexuys',
 'desc':'Разработка и доработка сайта на 1С-Битрикс: шаблоны, компоненты, формы, каталог, PHP/JavaScript, API, интеграция с 1С, производительность и техническое SEO.',
 'h1':'Разработка сайта на 1С-Битрикс. <em>Доработка и интеграции.</em>',
 'faq':[
  ('От чего зависит цена разработки сайта на Битрикс?','От объёма шаблонов и компонентов, структуры каталога, интеграций, обмена с 1С, бизнес-логики и состояния текущего проекта. Для существующего сайта сначала оценивается конкретный участок.'),
  ('Можно доработать существующий сайт на 1С-Битрикс?','Да. Не обязательно пересобирать сайт. Можно исправить компонент, форму, каталог, шаблон, интеграцию или производительность внутри текущего проекта.'),
 ]},
'tilda-development':{
 'title':'Разработка и доработка сайта на Tilda - Zero Block и код | Alexuys',
 'desc':'Разработка и доработка сайта на Tilda: Zero Block, HTML/CSS/JavaScript, адаптив, формы, калькуляторы, анимации, API и интеграции. Можно работать поверх существующего проекта.',
 'h1':'Разработка сайта на Tilda. <em>Zero Block, код и интеграции.</em>',
 'faq':[
  ('Сколько стоит разработка сайта на Tilda?','Стоимость зависит от количества уникальных блоков, адаптива, форм, анимаций, калькуляторов и интеграций. Небольшую задачу можно оценить отдельно без пересборки всего сайта.'),
  ('Можно заказать доработку уже готового сайта на Tilda?','Да. Можно править Zero Block, адаптив, формы, JavaScript, внешний вид и интеграции в существующем проекте без переноса на другую платформу.'),
 ]},
'wordpress-development':{
 'title':'Разработка и доработка WordPress сайта | Alexuys',
 'desc':'Разработка и доработка WordPress сайта: тема, плагины, формы, адаптив, PHP/JavaScript, API-интеграции, скорость, техническое SEO и микроразметка без лишней пересборки.',
 'h1':'Разработка WordPress сайта. <em>Доработка без пересборки.</em>',
 'faq':[
  ('Сколько стоит разработка или доработка сайта на WordPress?','Цена зависит от объёма темы и шаблонов, плагинов, форм, интеграций и состояния существующего сайта. Отдельную правку или новый блок можно оценивать независимо от всего проекта.'),
  ('Можно доработать WordPress без полной пересборки?','Да. Если текущая тема и код позволяют, изменения вносятся точечно: шаблоны, формы, стили, плагины, API, микроразметка или производительность.'),
 ]},
'excel-google-sheets-automation':{
 'title':'Автоматизация Excel и Google Sheets - Python, API, отчёты | Alexuys',
 'desc':'Автоматизация Excel и Google Sheets: обработка файлов и данных, отчёты, формулы, API, объединение таблиц, генерация документов, Python/openpyxl и AI-ассистенты.',
 'h1':'Автоматизация Excel и Google Sheets. <em>Данные и отчёты без ручной рутины.</em>',
 'faq':[
  ('Что можно автоматизировать в Excel?','Обработку и объединение файлов, перенос и проверку данных, регулярные отчёты, расчёты, генерацию документов, загрузку из API и другие повторяющиеся операции.'),
  ('Когда для автоматизации Excel нужен Python?','Когда задача выходит за пределы формул и макросов: много файлов, сложное преобразование данных, API, расписание, обработка больших таблиц или отдельный рабочий процесс.'),
 ]},
}

def meta(s,title,desc):
 s=re.sub(r'<title\b[^>]*>.*?</title>',f'<title>{html.escape(title)}</title>',s,count=1,flags=re.I|re.S)
 for attr,key,val in [('name','description',desc),('property','og:title',title),('property','og:description',desc),('name','twitter:title',title),('name','twitter:description',desc)]:
  pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
  repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
  s=re.sub(pat,repl,s,count=1,flags=re.I) if re.search(pat,s,re.I) else s.replace('</head>',repl+'</head>',1)
 return s

def h1(s,value,slug):
 s,n=re.subn(r'<h1\b([^>]*)>.*?</h1>',lambda m:f'<h1{m.group(1)}>{value}</h1>',s,count=1,flags=re.I|re.S)
 if n!=1: raise SystemExit(f'stage191: h1 missing {slug}')
 return s

def add_visible_and_schema(s,slug,items):
 marker=f'data-stage191-russian-faq="{slug}"'
 if marker not in s:
  # stage174 details
  m=re.search(r'(<div class="stage174-faq__grid">)(.*?)(</div></div></section>)',s,re.I|re.S)
  if m:
   extra=''.join(f'<details {marker}><summary>{q}</summary><p>{a}</p></details>' for q,a in items)
   s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
  else:
   # stage172 card FAQ
   m=re.search(r'(<section class="secondary-demand"[^>]*data-stage172-faq="true".*?<div class="secondary-demand__grid">)(.*?)(</div></div></section>)',s,re.I|re.S)
   if m:
    extra=''.join(f'<article {marker} class="secondary-demand__card"><h3>{q}</h3><p>{a}</p></article>' for q,a in items)
    s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
   else:
    # WordPress has no standard FAQ block: add a restrained one before final contact/end of main.
    anchor='</main>'
    if anchor not in s: raise SystemExit(f'stage191: FAQ anchor missing {slug}')
    cards=''.join(f'<details {marker}><summary>{q}</summary><p>{a}</p></details>' for q,a in items)
    style='''<style id="stage191-faq-style">
[data-stage191-faq-section]{padding:clamp(56px,6vw,88px) 0;border-top:1px solid rgba(255,255,255,.08);background:#090b0e;color:#f2f5f3}
[data-stage191-faq-section] .stage174-shell{width:min(1180px,calc(100% - 40px));margin:0 auto}
[data-stage191-faq-section] .stage174-head{display:grid;grid-template-columns:minmax(110px,.28fr) minmax(0,1fr);gap:34px;margin-bottom:28px}
[data-stage191-faq-section] .stage174-head>p{margin:0;color:#7f8891;font:700 11px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.14em}
[data-stage191-faq-section] .stage174-head h2{margin:0;font-size:clamp(34px,4vw,58px);line-height:1;letter-spacing:-.045em}
[data-stage191-faq-section] .stage174-head div>p{margin:12px 0 0;color:#9199a2;max-width:56ch}
[data-stage191-faq-section] .stage174-faq__grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
[data-stage191-faq-section] details{padding:0 20px;border:1px solid rgba(255,255,255,.1);border-radius:16px;background:rgba(255,255,255,.025)}
[data-stage191-faq-section] summary{cursor:pointer;list-style:none;padding:20px 0;font-weight:750}
[data-stage191-faq-section] summary::-webkit-details-marker{display:none}
[data-stage191-faq-section] details p{margin:0;padding:0 0 20px;color:#9ca4ad;line-height:1.65}
@media(max-width:700px){[data-stage191-faq-section] .stage174-head,[data-stage191-faq-section] .stage174-faq__grid{grid-template-columns:1fr}[data-stage191-faq-section] .stage174-shell{width:calc(100% - 24px)}}
</style>'''
    block=f'{style}<section class="stage174-faq" data-stage191-faq-section="true"><div class="stage174-shell"><div class="stage174-head"><p>BEFORE START</p><div><h2>Частые вопросы до оценки.</h2><p>Коротко о стоимости, объёме работ и вариантах доработки.</p></div></div><div class="stage174-faq__grid">{cards}</div></div></section>'
    s=s.replace(anchor,block+anchor,1)
 # Find an existing FAQPage schema, otherwise create one.
 sm=None
 for cand in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.I|re.S):
  if '"FAQPage"' in cand.group(1): sm=cand; break
 if sm:
  obj=json.loads(sm.group(1)); existing={x.get('name') for x in obj.get('mainEntity',[])}
  for q,a in items:
   if q not in existing: obj.setdefault('mainEntity',[]).append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}})
  blob=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
  s=s[:sm.start(1)]+blob+s[sm.end(1):]
 else:
  obj={'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in items]}
  blob='<script type="application/ld+json" data-stage191-faq-schema="true">'+json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'</script>'
  s=s.replace('</head>',blob+'</head>',1)
 return s

changed=[]
for slug,cfg in CFG.items():
 p=ROOT/slug/'index.html'
 if not p.is_file(): raise SystemExit(f'stage191: missing {slug}')
 s=p.read_text(encoding='utf-8')
 s=meta(s,cfg['title'],cfg['desc'])
 s=h1(s,cfg['h1'],slug)
 s=add_visible_and_schema(s,slug,cfg['faq'])
 p.write_text(s,encoding='utf-8'); changed.append('/'+slug+'/')

for name in ('sitemap.xml','sitemap-google.xml'):
 p=ROOT/name
 if not p.exists(): continue
 text=p.read_text(encoding='utf-8')
 for route in changed:
  text=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
 p.write_text(text,encoding='utf-8')

for slug,cfg in CFG.items():
 s=(ROOT/slug/'index.html').read_text(encoding='utf-8')
 for needle in [cfg['title'],cfg['desc'],re.sub('<[^>]+>','',cfg['h1']).split('.')[0],f'data-stage191-russian-faq="{slug}"']:
  if needle not in s: raise SystemExit(f'stage191: guard failed {slug}: {needle}')
 if s.count(f'data-stage191-russian-faq="{slug}"')!=2: raise SystemExit(f'stage191: faq count failed {slug}')
 # visible/schema consistency
 qs=[q for q,_ in cfg['faq']]
 for q in qs:
  if s.count(q)<2: raise SystemExit(f'stage191: FAQ/schema mismatch {slug}: {q}')
print(f'stage191 russian secondary clusters: pages={len(changed)}, faq={sum(len(v["faq"]) for v in CFG.values())}')
