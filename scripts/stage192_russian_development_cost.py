#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'
p=ROOT/'guides/development-cost/index.html'
if not p.is_file(): raise SystemExit('stage192: development cost guide missing')
s=p.read_text(encoding='utf-8')

TITLE='Сколько стоит разработка сайта и приложения в 2026 | Alexuys'
DESC='Сколько стоит разработка сайта, приложения и программного обеспечения в 2026 году: что влияет на цену, почему оценки отличаются и как получить нормальную стоимость без большого ТЗ.'

s=re.sub(r'<title\b[^>]*>.*?</title>',f'<title>{html.escape(TITLE)}</title>',s,count=1,flags=re.I|re.S)
for attr,key,val in [('name','description',DESC),('property','og:title',TITLE),('property','og:description',DESC),('name','twitter:title',TITLE),('name','twitter:description',DESC)]:
 pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
 repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
 s=re.sub(pat,repl,s,count=1,flags=re.I) if re.search(pat,s,re.I) else s.replace('</head>',repl+'</head>',1)

# Hero: cover the broad Russian price intent explicitly without publishing invented fixed prices.
s=re.sub(r'<h1>.*?</h1>','<h1>Сколько стоит <em>разработка сайта, приложения и ПО</em></h1>',s,count=1,flags=re.I|re.S)
s=re.sub(r'<p class="lead">.*?</p>','<p class="lead">Цена разработки зависит не от одного названия проекта, а от сценариев, интерфейса, backend, данных и интеграций. Ниже — отдельно о стоимости сайта, приложения и программного обеспечения и о том, что реально меняет оценку.</p>',s,count=1,flags=re.I|re.S)
s=s.replace('Обновлено 06.09.2026','Обновлено 18.09.2026',1)

# Add exact-demand sections before the existing estimation guidance.
if 'data-stage192-cost-clusters="true"' not in s:
 anchor='<section id="estimate">'
 if anchor not in s: raise SystemExit('stage192: estimate anchor missing')
 block='''<section id="cost-by-format" data-stage192-cost-clusters="true"><h2>Цена разработки по типу проекта</h2><p>Одинаковая формулировка «сделать сайт» или «сделать приложение» может означать разный объём. Для оценки полезнее смотреть на конкретные части продукта.</p><div class="matrix"><div class="mini"><small>САЙТ / WEB</small><h3>Цена разработки сайта</h3><p>На стоимость влияют уникальные страницы и состояния, формы, каталог или кабинет, адаптив, backend, CMS и внешние интеграции. Лендинг и веб-сервис с ролями и базой данных — это разные по объёму проекты.</p><p><a href="/web-development/">Разработка сайтов и веб-приложений ↗</a></p></div><div class="mini"><small>MOBILE APP</small><h3>Стоимость разработки приложения</h3><p>Основные факторы — количество пользовательских сценариев, экранов, API, авторизация, данные, push-уведомления, платежи и необходимость поддерживать одну или несколько платформ.</p><p><a href="/app-development/">Разработка мобильных приложений ↗</a></p></div><div class="mini"><small>SOFTWARE</small><h3>Стоимость разработки программного обеспечения</h3><p>Для внутренней системы или отдельного ПО важны модель данных, роли, бизнес-логика, API, интеграции, импорт существующих данных и требования к эксплуатации. Большую систему можно оценивать по законченным этапам.</p><p><a href="/development/">Разработка программного обеспечения ↗</a></p></div></div></section>'''
 s=s.replace(anchor,block+anchor,1)

# Extend visible FAQ if one exists; this guide uses a standalone FAQPage schema but not necessarily visible details.
faq_questions=[
 ('От чего зависит цена разработки сайта?','От количества уникальных страниц и состояний, форм и каталога, личного кабинета, backend-логики, CMS, адаптива и интеграций. Точную оценку лучше делать после определения первого рабочего сценария.'),
 ('Что влияет на стоимость разработки приложения?','Количество экранов и сценариев, API, авторизация, данные, push-уведомления, платежи, карты, системные функции и количество поддерживаемых платформ.'),
 ('Как оценить стоимость разработки программного обеспечения?','Сначала фиксируется минимальный рабочий контур: пользователи, роли, данные, бизнес-логика и интеграции. После этого система делится на законченные этапы, которые можно оценивать отдельно.'),
]
# Add a visible compact FAQ before links, matching schema content.
if 'data-stage192-cost-faq="true"' not in s:
 anchor='<section id="links">'
 if anchor not in s: raise SystemExit('stage192: links anchor missing')
 cards=''.join(f'<details data-stage192-cost-faq="true"><summary>{q}</summary><p>{a}</p></details>' for q,a in faq_questions)
 block=f'<section id="cost-faq"><h2>Частые вопросы о стоимости</h2>{cards}</section>'
 s=s.replace(anchor,block+anchor,1)

# Article schema: update headline/description/dateModified/keywords.
for m in list(re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.I|re.S)):
 try: obj=json.loads(m.group(1))
 except: continue
 if obj.get('@type')=='Article':
  obj['headline']='Сколько стоит разработка сайта, приложения и программного обеспечения'
  obj['description']=DESC
  obj['dateModified']=TODAY
  obj['keywords']=['стоимость разработки сайта','цена разработки сайта','стоимость разработки приложения','разработка приложения цена','стоимость разработки программного обеспечения','разработка на заказ']
  blob=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
  s=s[:m.start(1)]+blob+s[m.end(1):]
  break

# FAQ schema: append the same visible questions.
faqm=None
for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.I|re.S):
 if '"FAQPage"' in m.group(1): faqm=m; break
if not faqm: raise SystemExit('stage192: FAQ schema missing')
obj=json.loads(faqm.group(1)); names={x.get('name') for x in obj.get('mainEntity',[])}
for q,a in faq_questions:
 if q not in names: obj.setdefault('mainEntity',[]).append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}})
blob=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
s=s[:faqm.start(1)]+blob+s[faqm.end(1):]

p.write_text(s,encoding='utf-8')

url=BASE+'/guides/development-cost/'
for name in ('sitemap.xml','sitemap-google.xml'):
 sp=ROOT/name
 if not sp.exists(): continue
 text=sp.read_text(encoding='utf-8')
 text=re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
 sp.write_text(text,encoding='utf-8')

final=p.read_text(encoding='utf-8')
for needle in [TITLE,DESC,'data-stage192-cost-clusters="true"','Цена разработки сайта','Стоимость разработки приложения','Стоимость разработки программного обеспечения','data-stage192-cost-faq="true"','"dateModified":"2026-09-18"']:
 if needle not in final: raise SystemExit(f'stage192: guard failed: {needle}')
for q,_ in faq_questions:
 if final.count(q)<2: raise SystemExit(f'stage192: FAQ/schema mismatch: {q}')
print('stage192 russian development cost: page=1, sections=3, faq=3')
