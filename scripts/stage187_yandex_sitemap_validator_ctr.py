#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html, json, re, sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'
p=ROOT/'tools/sitemap-validator/index.html'
if not p.is_file(): raise SystemExit('stage187: sitemap validator missing')
s=p.read_text(encoding='utf-8')

TITLE='Sitemap Validator - проверить sitemap.xml онлайн | Alexuys'
DESC='Sitemap Validator: проверка sitemap.xml онлайн — XML, loc, дубли, urlset/sitemapindex. Базовая XML-проверка Google News sitemap без валидации news:* тегов.'

s=re.sub(r'<title>.*?</title>','<title>'+html.escape(TITLE)+'</title>',s,count=1,flags=re.I|re.S)
for attr,key,val in [
 ('name','description',DESC),('property','og:title',TITLE),('property','og:description',DESC),
 ('name','twitter:title',TITLE),('name','twitter:description',DESC),
]:
    pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
    repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
    if re.search(pat,s,re.I): s=re.sub(pat,repl,s,count=1,flags=re.I)
    else: s=s.replace('</head>',repl+'</head>',1)

# Keep the visible copy precise: this is a structural/XML validator, not a full Google News policy validator.
old='Вставьте XML карты сайта. Валидатор проверит XML-синтаксис, тип sitemap, элементы loc, абсолютность URL, дубли и смешение доменов.'
new='Вставьте XML карты сайта. Sitemap Validator проверит XML-синтаксис, urlset или sitemapindex, элементы loc, абсолютность URL, дубли и смешение доменов.'
if new not in s:
    if old not in s: raise SystemExit('stage187: hero lead marker missing')
    s=s.replace(old,new,1)

# Add structured FAQ only for answers that are already visible on the page.
if 'data-stage187-sitemap-faq-schema="true"' not in s:
    faq={
      '@context':'https://schema.org','@type':'FAQPage','mainEntity':[
        {'@type':'Question','name':'Поддерживается sitemap index?','acceptedAnswer':{'@type':'Answer','text':'Да. Валидатор распознаёт sitemapindex и проверяет loc дочерних sitemap-файлов.'}},
        {'@type':'Question','name':'Можно проверить Google News sitemap?','acceptedAnswer':{'@type':'Answer','text':'Да, для базовой XML-проверки: структура urlset, элементы loc, абсолютные URL и дубли. Специальные требования Google News к news:publication, news:publication_date и news:title эта версия не валидирует.'}},
        {'@type':'Question','name':'XML отправляется на сервер?','acceptedAnswer':{'@type':'Answer','text':'Нет. DOMParser разбирает содержимое локально в браузере.'}},
      ]
    }
    blob='<script type="application/ld+json" data-stage187-sitemap-faq-schema="true">'+json.dumps(faq,ensure_ascii=False,separators=(',',':'))+'</script>'
    s=s.replace('</head>',blob+'</head>',1)

p.write_text(s,encoding='utf-8')

url=BASE+'/tools/sitemap-validator/'
for name in ('sitemap.xml','sitemap-google.xml'):
    sm=ROOT/name
    if not sm.exists(): continue
    text=sm.read_text(encoding='utf-8')
    text=re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
    sm.write_text(text,encoding='utf-8')

final=p.read_text(encoding='utf-8')
for needle in [TITLE,DESC,'Sitemap Validator проверит XML-синтаксис','data-stage187-sitemap-faq-schema="true"','Google News sitemap']:
    if needle not in final: raise SystemExit(f'stage187: guard failed: {needle}')
print('stage187 yandex sitemap validator ctr: page=1, faq_schema=1')
