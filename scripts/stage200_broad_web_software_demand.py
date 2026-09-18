#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'
CFG={
 'web-development':{
  'title':'Разработка сайтов под ключ и веб-приложений | Alexuys',
  'desc':'Разработка сайтов под ключ и веб-приложений: лендинги, каталоги, личные кабинеты, backend, API, интеграции, адаптив и запуск.',
  'h1':'Разработка сайтов и веб-приложений. <em>От структуры до рабочего запуска.</em>',
  'lead':'Лендинг, каталог, личный кабинет или веб-приложение — с адаптивным интерфейсом, backend, данными и нужными интеграциями. Новый проект можно собрать до запуска или продолжить уже работающий сайт.',
  'schema_name':'Разработка сайтов под ключ и веб-приложений',
 },
 'development':{
  'title':'Разработка ПО на заказ - сайты, сервисы и автоматизация | Alexuys',
  'desc':'Разработка программного обеспечения на заказ: веб-сервисы, внутренние системы, backend, API, Python, автоматизация и доработка существующих проектов.',
  'h1':'Разработка ПО на заказ. <em>От задачи до рабочего продукта.</em>',
  'lead':'Разработка программного обеспечения под конкретный процесс: веб-сервис, внутренняя система, backend, автоматизация или интеграция. Если формат ещё не выбран, начинаю с пользовательского сценария и первого проверяемого результата.',
  'schema_name':'Разработка программного обеспечения на заказ',
 },
}

def meta(s,title,desc):
 s=re.sub(r'<title\b[^>]*>.*?</title>',f'<title>{html.escape(title)}</title>',s,count=1,flags=re.I|re.S)
 for attr,key,val in [('name','description',desc),('property','og:title',title),('property','og:description',desc),('name','twitter:title',title),('name','twitter:description',desc)]:
  pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
  repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
  s=re.sub(pat,repl,s,count=1,flags=re.I) if re.search(pat,s,re.I) else s.replace('</head>',repl+'</head>',1)
 return s

def jsonld(s,cfg):
 def repl(m):
  try:o=json.loads(m.group(2))
  except Exception:return m.group(0)
  def walk(x):
   if isinstance(x,dict):
    if x.get('@type') in ('Service','WebPage'):
     x['name']=cfg['schema_name'];x['description']=cfg['desc']
    for v in x.values():walk(v)
   elif isinstance(x,list):
    for v in x:walk(v)
  walk(o)
  return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
 return re.sub(r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',repl,s,flags=re.I|re.S)

changed=[]
for slug,cfg in CFG.items():
 p=ROOT/slug/'index.html'
 if not p.is_file(): raise SystemExit(f'stage200 missing: {slug}')
 s=p.read_text(encoding='utf-8')
 s=meta(s,cfg['title'],cfg['desc'])
 s,n=re.subn(r'<h1[^>]*>.*?</h1>',f'<h1>{cfg["h1"]}</h1>',s,count=1,flags=re.I|re.S)
 if n!=1: raise SystemExit(f'stage200 h1 missing: {slug}')
 s,n=re.subn(r'<p class="p129-lead">.*?</p>',f'<p class="p129-lead">{cfg["lead"]}</p>',s,count=1,flags=re.I|re.S)
 if n!=1: raise SystemExit(f'stage200 lead missing: {slug}')
 s=jsonld(s,cfg)
 p.write_text(s,encoding='utf-8');changed.append('/'+slug+'/')

for name in ('sitemap.xml','sitemap-google.xml'):
 p=ROOT/name
 if not p.exists():continue
 s=p.read_text(encoding='utf-8')
 for route in changed:
  s=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',s,count=1)
 p.write_text(s,encoding='utf-8')

for slug,cfg in CFG.items():
 s=(ROOT/slug/'index.html').read_text(encoding='utf-8')
 for needle in [cfg['title'],cfg['desc'],cfg['schema_name']]:
  if needle not in s: raise SystemExit(f'stage200 guard {slug}: {needle}')
print('stage200 broad web/software demand: pages=2')
