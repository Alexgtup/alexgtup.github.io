#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-19'

CASES={
 'marketplace-monitor':[
   ('/marketplace-integration/','Интеграция с маркетплейсами','Ozon, Wildberries, Яндекс Маркет, данные и заказы'),
   ('/automation-services/','Автоматизация бизнеса','Регулярный сбор, сверка и обработка данных без ручной рутины'),
   ('/excel-google-sheets-automation/','Excel и Google Sheets','Таблицы, история изменений и автоматическое обновление данных'),
 ],
 'ozon-scanner':[
   ('/marketplace-integration/','Интеграция с маркетплейсами','Складские процессы, остатки и связанные операции'),
   ('/automation-services/','Автоматизация бизнеса','Сканирование запускает дальнейшую цепочку без ручного переноса'),
   ('/excel-google-sheets-automation/','Excel и Google Sheets','Автоматическое заполнение и связанная логика таблиц'),
 ],
 'wordpress-commercial':[
   ('/wordpress-development/','WordPress-разработка','Доработка темы, форм, калькуляторов, адаптива и страниц'),
   ('/site-repair/','Доработка сайта','Исправления и новый функционал без переписывания проекта'),
   ('/web-development/','Сайты и веб-приложения','Интерфейс, формы, интеграции и технический запуск'),
 ],
 'portfolio-site':[
   ('/web-development/','Сайты и веб-приложения','Многостраничная структура, адаптив и рабочие пользовательские сценарии'),
   ('/development/','Разработка ПО','Структура продукта, данные, техническая база и развитие проекта'),
   ('/services/','Все направления','Разработка, автоматизация, интеграции и доработка существующих проектов'),
 ],
}
STYLE='''<style id="stage206-case-service-style">
.x206-case-services{padding:clamp(58px,6vw,88px) 0;background:#0a0d10;color:#eef2ef;border-top:1px solid rgba(255,255,255,.08)}
.x206-case-services .x206-shell{width:min(1180px,calc(100% - 48px));margin:0 auto}.x206-case-services__head{display:grid;grid-template-columns:.38fr 1fr;gap:clamp(24px,5vw,68px);align-items:start;margin-bottom:30px}.x206-case-services__head span{color:#7f898f;font:700 11px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.15em}.x206-case-services__head h2{margin:0;font-size:clamp(34px,4vw,58px);line-height:.98;letter-spacing:-.045em}.x206-case-services__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.x206-case-services__grid a{min-height:170px;padding:22px;border:1px solid rgba(255,255,255,.1);border-radius:18px;background:rgba(255,255,255,.025);color:#eef2ef!important;text-decoration:none!important;display:flex;flex-direction:column;justify-content:space-between;gap:22px}.x206-case-services__grid a:hover{border-color:rgba(201,255,74,.42);transform:translateY(-2px)}.x206-case-services__grid strong{font-size:22px;letter-spacing:-.03em}.x206-case-services__grid p{margin:0;color:#a7b0b5;line-height:1.55}.x206-case-services__grid b{font-size:13px;color:#c9ff4a;font-weight:700}
@media(max-width:800px){.x206-case-services__head,.x206-case-services__grid{grid-template-columns:1fr}.x206-case-services .x206-shell{width:calc(100% - 28px)}.x206-case-services__grid a{min-height:132px}}
</style>'''

changed=[]
for slug,links in CASES.items():
    p=ROOT/'cases'/slug/'index.html'
    if not p.is_file(): raise SystemExit(f'stage206 case missing: {slug}')
    s=p.read_text(encoding='utf-8')
    if 'stage206-case-service-style' not in s:
        s=s.replace('</head>',STYLE+'</head>',1)
    if 'data-stage206-case-services="true"' not in s:
        cards=''.join(f'<a href="{href}"><strong>{name}</strong><p>{desc}</p><b>Открыть направление ↗</b></a>' for href,name,desc in links)
        block=f'<section class="x206-case-services" data-stage206-case-services="true"><div class="x206-shell"><div class="x206-case-services__head"><span>СВЯЗАННЫЕ УСЛУГИ</span><h2>Если задача похожа — продолжить отсюда.</h2></div><div class="x206-case-services__grid">{cards}</div></div></section>'
        marker='<section class="s64-conversion stage108-endcap"'
        i=s.find(marker)
        if i<0: raise SystemExit(f'stage206 case CTA missing: {slug}')
        s=s[:i]+block+s[i:]
    p.write_text(s,encoding='utf-8');changed.append('/cases/'+slug+'/')

# Two-way proof: automation page should point back to both relevant real cases.
p=ROOT/'automation-services'/'index.html'
if not p.is_file(): raise SystemExit('stage206 automation missing')
s=p.read_text(encoding='utf-8')
case_links=[
 ('/cases/marketplace-monitor/','Кейс: мониторинг маркетплейсов ↗'),
 ('/cases/ozon-scanner/','Кейс: Ozon-склад и сканер ↗'),
]
for href,label in case_links:
    if f'href="{href}"' not in s:
        m=re.search(r'(<nav class="secondary-demand__links"[^>]*>)(.*?)(</nav>)',s,re.I|re.S)
        if not m: raise SystemExit('stage206 automation related nav missing')
        add=f'<a data-stage206-case-proof="true" href="{href}">{label}</a>'
        s=s[:m.start()]+m.group(1)+m.group(2)+add+m.group(3)+s[m.end():]
p.write_text(s,encoding='utf-8');changed.append('/automation-services/')

for name in ('sitemap.xml','sitemap-google.xml'):
    sp=ROOT/name
    if not sp.exists(): continue
    t=sp.read_text(encoding='utf-8')
    for route in changed:
        t=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',t,count=1)
    sp.write_text(t,encoding='utf-8')

for slug,links in CASES.items():
    s=(ROOT/'cases'/slug/'index.html').read_text(encoding='utf-8')
    if s.count('data-stage206-case-services="true"')!=1: raise SystemExit(f'stage206 duplicate block {slug}')
    for href,_,_ in links:
        if f'href="{href}"' not in s: raise SystemExit(f'stage206 missing link {slug}->{href}')
a=(ROOT/'automation-services'/'index.html').read_text(encoding='utf-8')
for href,_ in case_links:
    if f'href="{href}"' not in a: raise SystemExit(f'stage206 automation proof missing {href}')
print('stage206 case-service authority: case_pages=4, automation_backlinks=2')
