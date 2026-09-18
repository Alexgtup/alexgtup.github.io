#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'
CFG={
 'telegram-bots':{
  'title':'Разработчик Telegram-ботов на заказ - цена и кейсы | Alexuys',
  'desc':'Разработчик Telegram-ботов на заказ: Python/aiogram, API, CRM, оплаты, Mini App и автоматизация. Кейсы, этапы работы и ориентиры стоимости.',
  'schema_name':'Разработчик Telegram-ботов на заказ - цена и кейсы',
 },
 'guides/telegram-bot-cost':{
  'title':'Сколько стоит сделать Telegram-бота на заказ в 2026 | Alexuys',
  'desc':'Сколько стоит сделать Telegram-бота на заказ в 2026 году: ориентиры цены, что влияет на стоимость, примеры функций и как подготовить задачу к оценке.',
  'headline':'Сколько стоит сделать Telegram-бота на заказ в 2026 году',
 },
 'telegram-mini-apps':{
  'title':'Разработка Telegram Mini App на заказ - Mini Apps под ключ | Alexuys',
  'desc':'Разработка Telegram Mini App на заказ: интерфейс внутри Telegram, backend, авторизация, платежи, API и интеграции. Кейсы и прямая работа с разработчиком.',
  'schema_name':'Разработка Telegram Mini App на заказ - Mini Apps под ключ',
 },
}

def path(slug):
 p=ROOT/slug/'index.html'
 if not p.is_file(): raise SystemExit(f'stage197: missing {slug}')
 return p

def set_meta(s,title,desc):
 s=re.sub(r'<title\b[^>]*>.*?</title>',f'<title>{html.escape(title)}</title>',s,count=1,flags=re.I|re.S)
 for attr,key,val in [('name','description',desc),('property','og:title',title),('property','og:description',desc),('name','twitter:title',title),('name','twitter:description',desc)]:
  pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
  repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
  if re.search(pat,s,re.I): s=re.sub(pat,repl,s,count=1,flags=re.I)
  else: s=s.replace('</head>',repl+'</head>',1)
 return s

def sync_jsonld(s,slug,cfg):
 def repl(m):
  try:o=json.loads(m.group(2))
  except Exception:return m.group(0)
  typ=o.get('@type')
  changed=False
  if slug=='telegram-bots' and typ in ('Service','WebPage'):
   o['name']=cfg['schema_name']; o['description']=cfg['desc']; changed=True
  elif slug=='telegram-mini-apps' and typ=='Service':
   o['name']=cfg['schema_name']; o['description']=cfg['desc']; changed=True
  elif slug=='guides/telegram-bot-cost' and typ=='Article':
   o['headline']=cfg['headline']; o['description']=cfg['desc']; o['dateModified']=TODAY; changed=True
  if not changed:return m.group(0)
  return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
 return re.sub(r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',repl,s,flags=re.I|re.S)

changed=[]
for slug,cfg in CFG.items():
 p=path(slug);s=p.read_text(encoding='utf-8')
 s=set_meta(s,cfg['title'],cfg['desc'])
 s=sync_jsonld(s,slug,cfg)
 p.write_text(s,encoding='utf-8');changed.append('/'+slug+'/')

for name in ('sitemap.xml','sitemap-google.xml'):
 p=ROOT/name
 if not p.exists():continue
 text=p.read_text(encoding='utf-8')
 for route in changed:
  text=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
 p.write_text(text,encoding='utf-8')

for slug,cfg in CFG.items():
 s=path(slug).read_text(encoding='utf-8')
 for needle in [cfg['title'],cfg['desc']]:
  if needle not in s:raise SystemExit(f'stage197 guard failed {slug}: {needle}')
 # Ensure no stale hard floor remains in Telegram bot schema/metadata after the rewrite.
 if slug=='telegram-bots' and 'от 15 000 ₽' in s:
  # The page body may legitimately show price bands elsewhere; only JSON-LD/meta should be clean.
  for m in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',s,re.I|re.S):
   if 'от 15 000 ₽' in m.group(1): raise SystemExit('stage197: stale 15k schema remains')
print('stage197 yandex CTR opportunities: pages=3')
