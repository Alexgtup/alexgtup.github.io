#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-19'; SLUG='n8n-automation'
TITLE='n8n автоматизация на заказ — от 15 000 ₽ | Alexuys'
DESC='n8n автоматизация на заказ: CRM, Telegram, Google Sheets, API и webhooks. Первый рабочий этап от 15 000 ₽: проектирование, запуск, обработка ошибок и передача workflow.'
H1='n8n автоматизация на заказ. <em>Связать сервисы в один рабочий сценарий.</em>'
p=ROOT/SLUG/'index.html'
if not p.is_file():raise SystemExit('stage211 n8n page missing')
s=p.read_text(encoding='utf-8')
s,n=re.subn(r'<title\b[^>]*>.*?</title>',f'<title>{html.escape(TITLE)}</title>',s,count=1,flags=re.I|re.S)
if n!=1:raise SystemExit('stage211 title missing')
for attr,key,val in [('name','description',DESC),('property','og:title',TITLE),('property','og:description',DESC),('name','twitter:title',TITLE),('name','twitter:description',DESC)]:
 pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
 repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
 if re.search(pat,s,re.I):s=re.sub(pat,repl,s,count=1,flags=re.I)
s,n=re.subn(r'<h1\b([^>]*)>.*?</h1>',lambda m:f'<h1{m.group(1)}>{H1}</h1>',s,count=1,flags=re.I|re.S)
if n!=1:raise SystemExit('stage211 h1 missing')
# Keep Service/WebPage structured data aligned with the visible commercial intent.
out=[];last=0;touched=0
for m in re.finditer(r'<script([^>]*)type="application/ld\+json"([^>]*)>(.*?)</script>',s,re.I|re.S):
 try:o=json.loads(m.group(3))
 except Exception:continue
 changed=False;stack=[o]
 while stack:
  x=stack.pop()
  if isinstance(x,dict):
   if x.get('@type') in ('Service','WebPage'):
    x['name']='n8n автоматизация на заказ';x['description']=DESC;changed=True
   stack.extend(x.values())
  elif isinstance(x,list):stack.extend(x)
 if changed:
  out.append(s[last:m.start(3)]);out.append(json.dumps(o,ensure_ascii=False,separators=(',',':')));last=m.end(3);touched+=1
if touched:out.append(s[last:]);s=''.join(out)
p.write_text(s,encoding='utf-8')
for name in ('sitemap.xml','sitemap-google.xml'):
 sp=ROOT/name
 if not sp.exists():continue
 t=sp.read_text(encoding='utf-8');route=BASE+'/'+SLUG+'/'
 t=re.sub(r'(<loc>'+re.escape(route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',t,count=1);sp.write_text(t,encoding='utf-8')
if not 35<=len(TITLE)<=65:raise SystemExit(f'stage211 title length {len(TITLE)}')
final=p.read_text(encoding='utf-8')
for needle in (TITLE,DESC,H1,'15 000 ₽','retry','workflow'):
 if needle not in final:raise SystemExit(f'stage211 guard missing {needle}')
print(f'stage211 n8n SERP intent: title={len(TITLE)}, exact buyer phrase + public starting price')
