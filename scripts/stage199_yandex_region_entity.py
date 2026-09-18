#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'

HOME_TITLE='Разработчик сайтов, программного обеспечения и автоматизации'
HOME_DESC='Разработка сайтов и веб-приложений, программного обеспечения, автоматизации бизнеса, backend/API, CRM, ИИ и мобильных приложений.'
COVERAGE='Работаю удалённо с заказчиками по всей России.'


def rewrite_jsonld(text:str, fn):
    def repl(m):
        try: data=json.loads(m.group(2))
        except Exception: return m.group(0)
        new=fn(data)
        return m.group(1)+json.dumps(new,ensure_ascii=False,separators=(',',':'))+m.group(3)
    return re.sub(r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',repl,text,flags=re.I|re.S)


def walk(obj, callback):
    if isinstance(obj,dict):
        callback(obj)
        for v in obj.values(): walk(v,callback)
    elif isinstance(obj,list):
        for v in obj: walk(v,callback)

# Home visible region signal + structured entity alignment.
home=ROOT/'index.html'
if not home.is_file(): raise SystemExit('stage199: home missing')
s=home.read_text(encoding='utf-8')
if 'stage199-coverage' not in s:
    pat=r'(<div class="p128-actions">.*?</div>)'
    m=re.search(pat,s,re.I|re.S)
    if not m: raise SystemExit('stage199: home actions missing')
    block=m.group(1)+f'<p class="stage199-coverage">{COVERAGE}</p>'
    s=s[:m.start()]+block+s[m.end():]
    style='<style id="stage199-region-style">.stage199-coverage{margin:18px 0 0;color:rgba(226,233,236,.62);font-size:14px;line-height:1.55}.p130-region-signal{margin:18px 0 0;color:rgba(226,233,236,.66);font-size:15px;line-height:1.6}@media(max-width:600px){.stage199-coverage,.p130-region-signal{font-size:13px}}</style>'
    s=s.replace('</head>',style+'</head>',1)

service_order=[
 ('/web-development/','Разработка сайтов и веб-приложений'),
 ('/development/','Разработка программного обеспечения'),
 ('/automation-services/','Автоматизация бизнеса'),
 ('/ai-automation/','ИИ и AI-автоматизация'),
 ('/api-integrations/','API-интеграции'),
 ('/crm-development/','Разработка CRM'),
 ('/app-development/','Разработка мобильных приложений'),
 ('/telegram-bots/','Разработка Telegram-ботов'),
 ('/marketplace-integration/','Интеграция с маркетплейсами'),
 ('/1c-integration/','Интеграция 1С'),
 ('/project-repair/','Доработка существующих проектов'),
 ('/backend-development/','Backend-разработка'),
 ('/n8n-automation/','Автоматизация n8n'),
 ('/python-development/','Python-разработка'),
]

def home_patch(data):
    def cb(o):
        typ=o.get('@type')
        if typ=='Person' and o.get('@id')==BASE+'/#person':
            o['jobTitle']=HOME_TITLE
            o['description']=HOME_DESC
        if typ=='ItemList' and o.get('name')=='Услуги разработки':
            o['itemListElement']=[{'@type':'ListItem','position':i,'url':BASE+href,'name':name} for i,(href,name) in enumerate(service_order,1)]
    walk(data,cb); return data
s=rewrite_jsonld(s,home_patch)
home.write_text(s,encoding='utf-8')

# About page contains the explicit regional evidence used in Yandex Webmaster.
about=ROOT/'about'/'index.html'
if not about.is_file(): raise SystemExit('stage199: about missing')
s=about.read_text(encoding='utf-8')
if 'p130-region-signal' not in s:
    m=re.search(r'(<p class="p130-lead">.*?</p>)',s,re.I|re.S)
    if not m: raise SystemExit('stage199: about lead missing')
    s=s[:m.end()]+f'<p class="p130-region-signal">{COVERAGE}</p>'+s[m.end():]
    if 'stage199-region-style' not in s:
        style='<style id="stage199-region-style">.p130-region-signal{margin:18px 0 0;color:rgba(226,233,236,.66);font-size:15px;line-height:1.6}@media(max-width:600px){.p130-region-signal{font-size:13px}}</style>'
        s=s.replace('</head>',style+'</head>',1)

def about_patch(data):
    def cb(o):
        if o.get('@type')=='Person' and o.get('@id')==BASE+'/#person':
            o['jobTitle']=HOME_TITLE
            o['description']=HOME_DESC
    walk(data,cb);return data
s=rewrite_jsonld(s,about_patch)
about.write_text(s,encoding='utf-8')

# Service schemas explicitly state the remote service area. `areaServed` is valid for Service.
service_count=0
for p in ROOT.rglob('index.html'):
    text=p.read_text(encoding='utf-8',errors='ignore')
    touched=[0]
    def service_patch(data):
        def cb(o):
            if o.get('@type')=='Service':
                o['areaServed']={'@type':'Country','name':'Россия'}
                touched[0]+=1
        walk(data,cb);return data
    new=rewrite_jsonld(text,service_patch)
    if touched[0]:
        p.write_text(new,encoding='utf-8');service_count+=touched[0]

for name in ('sitemap.xml','sitemap-google.xml'):
    p=ROOT/name
    if not p.exists(): continue
    text=p.read_text(encoding='utf-8')
    for route in ('/','/about/'):
        text=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
    p.write_text(text,encoding='utf-8')

# Guards.
h=home.read_text(encoding='utf-8'); a=about.read_text(encoding='utf-8')
for needle in [COVERAGE,HOME_TITLE,HOME_DESC,'/marketplace-integration/']:
    if needle not in h: raise SystemExit(f'stage199 home guard failed: {needle}')
for needle in [COVERAGE,HOME_TITLE,HOME_DESC]:
    if needle not in a: raise SystemExit(f'stage199 about guard failed: {needle}')
if service_count<10: raise SystemExit(f'stage199: suspiciously low Service schema count {service_count}')
print(f'stage199 yandex region/entity: service_schemas={service_count}, coverage=home+about')
