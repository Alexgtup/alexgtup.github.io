#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'


def meta_replace(s,key,val,attr='name'):
    pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
    repl=f'<meta {attr}="{key}" content="{val}"/>'
    return re.sub(pat,repl,s,count=1,flags=re.I) if re.search(pat,s,re.I) else s

def json_patch(s, fn):
    def repl(m):
        try:o=json.loads(m.group(2))
        except Exception:return m.group(0)
        def walk(x):
            if isinstance(x,dict):
                fn(x)
                for v in x.values(): walk(v)
            elif isinstance(x,list):
                for v in x: walk(v)
        walk(o)
        return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
    return re.sub(r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',repl,s,flags=re.I|re.S)

changed=[]

# 1) Align AI landing with a broad Russian commercial phrase while keeping process-focused differentiation.
p=ROOT/'ai-automation'/'index.html';s=p.read_text(encoding='utf-8')
title='Разработка ИИ и ИИ-агентов для бизнеса | Alexuys'
desc='Разработка ИИ-решений и ИИ-агентов для бизнеса: автоматизация процессов, AI + API, работа с данными, контроль результата и интеграция в существующие системы.'
s=re.sub(r'<title[^>]*>.*?</title>',f'<title>{title}</title>',s,count=1,flags=re.I|re.S)
s=meta_replace(s,'description',desc)
s=meta_replace(s,'og:title',title,'property');s=meta_replace(s,'og:description',desc,'property')
s=meta_replace(s,'twitter:title',title);s=meta_replace(s,'twitter:description',desc)
s=s.replace('<h1>ИИ для бизнеса и AI-автоматизация. <em>Внутри реального процесса.</em></h1>','<h1>Разработка ИИ и ИИ-агентов для бизнеса. <em>Внутри реального процесса.</em></h1>',1)
def ai_schema(o):
    if o.get('@type')=='Service' and o.get('url')==BASE+'/ai-automation/':
        o['name']='Разработка ИИ и ИИ-агентов для бизнеса'
        o['description']=desc
s=json_patch(s,ai_schema)
p.write_text(s,encoding='utf-8');changed.append('/ai-automation/')

# 2) Put the broadest Russian commercial development routes into the first homepage decision block.
p=ROOT/'index.html';s=p.read_text(encoding='utf-8')
old=re.search(r'<div class="p128-cap__list" data-stage189-market-core="true">.*?</div>',s,re.I|re.S)
if not old: raise SystemExit('stage203 home capability list missing')
home_items=[
('/web-development/','Сайты и веб-приложения','Сайты под ключ, кабинеты, каталоги и web apps'),
('/development/','Программное обеспечение','Внутренние системы, backend, API и цифровые продукты'),
('/1c-integration/','Интеграция 1С','Сайт, CRM, каталог, заказы и обмен данными'),
('/ai-automation/','ИИ и ИИ-агенты','AI внутри процесса, API, данные и контроль результата'),
('/automation-services/','Автоматизация бизнеса','Процессы, данные, интеграции, n8n и Python'),
('/app-development/','Мобильные приложения','iOS, React Native, backend и пользовательские сценарии'),
]
block='<div class="p128-cap__list" data-stage189-market-core="true" data-stage203-demand-priority="true">'+''.join(
    f'<a href="{href}"><span>{i:02d}</span><strong>{name}</strong><em>{desc2}</em><b>↗</b></a>' for i,(href,name,desc2) in enumerate(home_items,1)
)+'</div>'
s=s[:old.start()]+block+s[old.end():]
# Reorder ItemList as an information architecture signal, not as a keyword dump.
order=[
('/web-development/','Разработка сайтов и веб-приложений'),
('/development/','Разработка программного обеспечения'),
('/1c-integration/','Интеграция 1С'),
('/ai-automation/','Разработка ИИ и ИИ-агентов'),
('/automation-services/','Автоматизация бизнеса'),
('/app-development/','Разработка мобильных приложений'),
('/api-integrations/','API-интеграции'),
('/ecommerce-development/','Разработка интернет-магазинов'),
('/crm-development/','Разработка CRM'),
('/telegram-bots/','Разработка Telegram-ботов'),
('/marketplace-integration/','Интеграция с маркетплейсами'),
('/wordpress-development/','Разработка и доработка WordPress'),
('/backend-development/','Backend-разработка'),
('/n8n-automation/','Автоматизация n8n'),
('/python-development/','Python-разработка'),
('/project-repair/','Доработка существующих проектов'),
]
def home_schema(o):
    if o.get('@type')=='ItemList' and o.get('name')=='Услуги разработки':
        o['itemListElement']=[{'@type':'ListItem','position':i,'url':BASE+h,'name':n} for i,(h,n) in enumerate(order,1)]
s=json_patch(s,home_schema)
p.write_text(s,encoding='utf-8');changed.append('/')

# 3) Services hub: surface 1C/API/ecommerce instead of hiding them in deep task maps.
p=ROOT/'services'/'index.html';s=p.read_text(encoding='utf-8')
s=s.replace('Сайты, веб-приложения, программное обеспечение, мобильные приложения, CRM, backend/API и автоматизация. Стек выбирается после того, как понятен нужный результат.',
'''Сайты и веб-приложения, программное обеспечение, интеграция 1С, ИИ, автоматизация бизнеса, мобильные приложения, API и CRM. Стек выбирается после того, как понятен нужный результат.''',1)
old=re.search(r'<div class="p130-list" data-stage189-russian-services="true">.*?</div>',s,re.I|re.S)
if not old: raise SystemExit('stage203 services list missing')
service_items=[
('/web-development/','Разработка сайтов и веб-приложений','Сайты под ключ, каталоги, кабинеты, web apps и SaaS.'),
('/development/','Разработка программного обеспечения','Внутренние системы, backend и цифровые продукты под процесс.'),
('/1c-integration/','Интеграция 1С','Обмен с сайтом, CRM, каталогом, заказами и внешними API.'),
('/ai-automation/','Разработка ИИ и ИИ-агентов','AI-функции и агенты внутри реального рабочего процесса.'),
('/automation-services/','Автоматизация бизнеса','Бизнес-процессы, данные, n8n, Python и интеграции.'),
('/app-development/','Мобильные приложения','iOS и React Native: от сценария до рабочей версии.'),
('/api-integrations/','API-интеграции','REST API, webhooks и надёжный обмен между системами.'),
('/ecommerce-development/','Интернет-магазины','Каталог, корзина, оплата, 1С и внешние интеграции.'),
('/crm-development/','CRM и внутренние системы','Заявки, клиенты, роли, статусы и автоматизация процесса.'),
('/marketplace-integration/','Интеграция с маркетплейсами','1С, Ozon, Wildberries, Яндекс Маркет, остатки и заказы.'),
('/telegram-bots/','Telegram-боты и Mini Apps','Боты, интерфейсы, оплаты и интеграции внутри Telegram.'),
('/project-repair/','Доработка существующего проекта','Чужой код, ошибки, новые функции и незавершённый релиз.'),
]
block='<div class="p130-list" data-stage189-russian-services="true" data-stage203-demand-priority="true">'+''.join(
 f'<a class="p130-row" href="{h}"><span>{i:02d}</span><strong>{n}</strong><em>{d}</em><b>↗</b></a>' for i,(h,n,d) in enumerate(service_items,1)
)+'</div>'
s=s[:old.start()]+block+s[old.end():]
p.write_text(s,encoding='utf-8');changed.append('/services/')

# Refresh lastmod only for pages whose rendered content changed.
for name in ('sitemap.xml','sitemap-google.xml'):
    sp=ROOT/name
    if not sp.exists(): continue
    t=sp.read_text(encoding='utf-8')
    for route in changed:
        t=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',t,count=1)
    sp.write_text(t,encoding='utf-8')

# Guards.
a=(ROOT/'ai-automation'/'index.html').read_text(encoding='utf-8')
h=(ROOT/'index.html').read_text(encoding='utf-8')
sv=(ROOT/'services'/'index.html').read_text(encoding='utf-8')
for x in [title,'<h1>Разработка ИИ и ИИ-агентов для бизнеса. <em>Внутри реального процесса.</em></h1>']:
    if x not in a: raise SystemExit('stage203 AI guard '+x)
for x in ['data-stage203-demand-priority="true"','/1c-integration/','/ai-automation/']:
    if x not in h: raise SystemExit('stage203 home guard '+x)
for x in ['/1c-integration/','/api-integrations/','/ecommerce-development/','data-stage203-demand-priority="true"']:
    if x not in sv: raise SystemExit('stage203 services guard '+x)
print('stage203 Russian demand priority: home=6, services=12, ai-intent=aligned')
