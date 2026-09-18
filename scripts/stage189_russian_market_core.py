#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html, re, sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'
TODAY='2026-09-18'

# Yandex Wordstat, all regions, 18.08–16.09.2026:
# создание сайтов 112594; разработка ПО 34819; разработка сайтов 31554;
# разработка приложений 27844; разработка ИИ 12425; автоматизация бизнеса 10288;
# web apps 7058; mobile apps 5486; automation processes 4349.

def load(rel:str):
    p=ROOT/rel if rel.endswith('.html') else ROOT/rel/'index.html'
    if not p.is_file(): raise SystemExit(f'stage189: missing {rel}')
    return p,p.read_text(encoding='utf-8')

def meta(s:str,title:str|None=None,desc:str|None=None)->str:
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

def set_h1(s:str,value:str,label:str)->str:
    s,n=re.subn(r'<h1\b([^>]*)>.*?</h1>',lambda m:f'<h1{m.group(1)}>{value}</h1>',s,count=1,flags=re.I|re.S)
    if n!=1: raise SystemExit(f'stage189: h1 missing {label}')
    return s

def replace_once(s:str,old:str,new:str,label:str)->str:
    if new in s: return s
    if old not in s: raise SystemExit(f'stage189: marker missing {label}')
    return s.replace(old,new,1)

changed=[]

# Homepage remains a personal/developer landing, but its copy stops centering Telegram.
p,s=load('index.html')
s=meta(s,desc='Разработчик на заказ: сайты и веб-приложения, программное обеспечение, мобильные приложения, автоматизация бизнеса, backend, API, CRM и доработка проектов.')
s=replace_once(s,
    'Сайты, Telegram-сервисы, автоматизация и приложения. Беру задачу целиком или подключаюсь к уже работающему проекту - без лишнего слоя менеджеров и терминов.',
    'Разработка сайтов, веб-приложений, программного обеспечения, автоматизации и мобильных приложений. Беру задачу целиком или подключаюсь к уже работающему проекту - без лишнего слоя менеджеров.',
    'home lead')
old_caps='''<div class="p128-cap__list">
      <a href="/web-development/"><span>01</span><strong>Сайты и веб-сервисы</strong><em>Лендинг, кабинет, каталог, SaaS, внутренний сервис</em><b>↗</b></a>
      <a href="/telegram-bots/"><span>02</span><strong>Telegram-продукты</strong><em>Боты, Mini Apps, оплаты, заявки, личные сценарии</em><b>↗</b></a>
      <a href="/n8n-automation/"><span>03</span><strong>Автоматизация</strong><em>Убрать ручные действия и связать рабочие сервисы</em><b>↗</b></a>
      <a href="/project-repair/"><span>04</span><strong>Доработка проектов</strong><em>Ошибки, чужой код, незавершённый релиз, адаптив</em><b>↗</b></a>
    </div>'''
new_caps='''<div class="p128-cap__list" data-stage189-market-core="true">
      <a href="/web-development/"><span>01</span><strong>Сайты и веб-приложения</strong><em>Лендинг, кабинет, каталог, web app, SaaS</em><b>↗</b></a>
      <a href="/development/"><span>02</span><strong>Программное обеспечение</strong><em>Внутренние сервисы, backend, API, CRM</em><b>↗</b></a>
      <a href="/automation-services/"><span>03</span><strong>Автоматизация бизнеса</strong><em>Процессы, данные, интеграции и AI</em><b>↗</b></a>
      <a href="/app-development/"><span>04</span><strong>Мобильные приложения</strong><em>iOS, React Native и пользовательские сценарии</em><b>↗</b></a>
    </div>'''
s=replace_once(s,old_caps,new_caps,'home capabilities')
p.write_text(s,encoding='utf-8');changed.append('/')

# Services hub owns the broad “разработка на заказ” intent.
p,s=load('services')
s=meta(s,
    'Разработка на заказ - сайты, ПО, приложения и автоматизация | Alexuys',
    'Разработка на заказ: сайты и веб-приложения, программное обеспечение, мобильные приложения, CRM, backend/API, автоматизация бизнеса, AI и доработка проектов.')
s=set_h1(s,'Разработка на заказ. <span>От сайта до ПО и автоматизации.</span>','services')
s=re.sub(r'<p class="p130-lead">.*?</p>', '<p class="p130-lead">Сайты, веб-приложения, программное обеспечение, мобильные приложения, CRM, backend/API и автоматизация. Стек выбирается после того, как понятен нужный результат.</p>', s,count=1,flags=re.I|re.S)
new_list='''<div class="p130-list" data-stage189-russian-services="true"><a class="p130-row" href="/web-development/"><span>01</span><strong>Разработка сайтов и веб-приложений</strong><em>Лендинги, каталоги, кабинеты, web apps и SaaS.</em><b>↗</b></a><a class="p130-row" href="/development/"><span>02</span><strong>Разработка программного обеспечения</strong><em>Внутренние сервисы и цифровые продукты под рабочий процесс.</em><b>↗</b></a><a class="p130-row" href="/app-development/"><span>03</span><strong>Мобильные приложения</strong><em>iOS и React Native: от главного сценария до рабочей версии.</em><b>↗</b></a><a class="p130-row" href="/automation-services/"><span>04</span><strong>Автоматизация бизнеса</strong><em>Бизнес-процессы, данные, интеграции и повторяющиеся операции.</em><b>↗</b></a><a class="p130-row" href="/ai-automation/"><span>05</span><strong>AI-автоматизация и ИИ-решения</strong><em>AI внутри реального процесса с контролируемым результатом.</em><b>↗</b></a><a class="p130-row" href="/backend-development/"><span>06</span><strong>Backend и API</strong><em>Серверная логика, базы данных, роли и интеграции.</em><b>↗</b></a><a class="p130-row" href="/crm-development/"><span>07</span><strong>CRM и внутренние системы</strong><em>Заявки, клиенты, сотрудники и статусы под процесс бизнеса.</em><b>↗</b></a><a class="p130-row" href="/telegram-bots/"><span>08</span><strong>Telegram-боты и Mini Apps</strong><em>Боты, интерфейсы, оплаты и интеграции внутри Telegram.</em><b>↗</b></a><a class="p130-row" href="/project-repair/"><span>09</span><strong>Доработка существующего проекта</strong><em>Чужой код, ошибки, новые функции и незавершённый релиз.</em><b>↗</b></a></div>'''
s,n=re.subn(r'<div class="p130-list">.*?</div></div></section>',new_list+'</div></section>',s,count=1,flags=re.I|re.S)
if n!=1: raise SystemExit('stage189: services list replace failed')
p.write_text(s,encoding='utf-8');changed.append('/services/')

# Development page owns “разработка программного обеспечения”.
p,s=load('development')
s=meta(s,
    'Разработка программного обеспечения на заказ | Alexuys',
    'Разработка программного обеспечения на заказ: веб-сервисы, внутренние системы, backend/API, CRM, автоматизация и приложения. Первый этап можно запускать отдельно.')
s=set_h1(s,'Разработка программного обеспечения на заказ. <em>От MVP до рабочего сервиса.</em>','development')
s=re.sub(r'<p class="p129-lead">.*?</p>', '<p class="p129-lead">Веб-сервисы, внутренние системы, backend/API, CRM, автоматизация и приложения. Можно начать с одного законченного сценария и развивать продукт по этапам.</p>',s,count=1,flags=re.I|re.S)
s=s.replace('DIGITAL DEVELOPMENT','SOFTWARE DEVELOPMENT',1)
p.write_text(s,encoding='utf-8');changed.append('/development/')

# Web page owns websites + web applications.
p,s=load('web-development')
s=meta(s,
    'Разработка сайтов и веб-приложений на заказ | Alexuys',
    'Разработка сайтов и веб-приложений на заказ: лендинги, каталоги, личные кабинеты, web apps, SaaS, backend, API, базы данных и интеграции.')
s=set_h1(s,'Разработка сайтов и веб-приложений на заказ. <em>От интерфейса до запуска.</em>','web')
p.write_text(s,encoding='utf-8');changed.append('/web-development/')

# Mobile apps.
p,s=load('app-development')
s=meta(s,
    'Разработка мобильных приложений на заказ - iOS и React Native | Alexuys',
    'Разработка мобильных приложений на заказ: iOS, Swift и React Native, интерфейс, API, данные, авторизация и рабочая версия для проверки на устройстве.')
s=set_h1(s,'Разработка мобильных приложений на заказ. <em>От первого экрана до рабочей версии.</em>','apps')
p.write_text(s,encoding='utf-8');changed.append('/app-development/')

# Automation page owns the high-volume business automation cluster rather than the n8n brand.
p,s=load('automation-services')
s=meta(s,
    'Автоматизация бизнеса и бизнес-процессов на заказ | Alexuys',
    'Автоматизация бизнеса и бизнес-процессов: n8n, Python, API, CRM, Telegram, Google Sheets, webhooks, отчёты и регулярные операции между сервисами.')
s=set_h1(s,'Автоматизация бизнеса и бизнес-процессов. <em>Меньше ручной работы.</em>','automation')
p.write_text(s,encoding='utf-8');changed.append('/automation-services/')

# AI cluster.
p,s=load('ai-automation')
s=meta(s,
    'AI-автоматизация и разработка ИИ-решений | Alexuys',
    'AI-автоматизация и разработка ИИ-решений для бизнеса: обработка текстов и данных, AI-агенты, API, n8n, поиск, классификация и контроль результата.')
s=set_h1(s,'AI-автоматизация и ИИ-решения для бизнеса. <em>Внутри реального процесса.</em>','ai')
p.write_text(s,encoding='utf-8');changed.append('/ai-automation/')

# CRM, MVP: add missing descriptions and put the transactional phrase in visible H1.
p,s=load('crm-development')
s=meta(s,
    'Разработка CRM на заказ - система под процессы бизнеса | Alexuys',
    'Разработка CRM на заказ: заявки, клиенты, сотрудники, роли, статусы, отчёты, API и интеграции. Система под реальный процесс без лишних модулей.')
s=set_h1(s,'Разработка CRM на заказ. <em>Заявки, клиенты, сотрудники и статусы.</em>','crm')
p.write_text(s,encoding='utf-8');changed.append('/crm-development/')

p,s=load('mvp-development')
s=meta(s,
    'Разработка MVP на заказ - веб-сервис или приложение | Alexuys',
    'Разработка MVP на заказ: один главный пользовательский сценарий, интерфейс, backend, API и рабочая версия для проверки идеи до большой разработки.')
s=set_h1(s,'Разработка MVP на заказ. <em>Первая версия для проверки идеи.</em>','mvp')
p.write_text(s,encoding='utf-8');changed.append('/mvp-development/')

# Refresh discovery timestamps only for materially changed routes.
for name in ('sitemap.xml','sitemap-google.xml'):
    sp=ROOT/name
    if not sp.exists(): continue
    text=sp.read_text(encoding='utf-8')
    for route in changed:
        url=BASE+route
        text=re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
    sp.write_text(text,encoding='utf-8')

# Hard guards.
guards={
 'index.html':['data-stage189-market-core="true"','Разработка сайтов, веб-приложений, программного обеспечения'],
 'services/index.html':['data-stage189-russian-services="true"','Разработка на заказ.','Разработка программного обеспечения'],
 'development/index.html':['Разработка программного обеспечения на заказ','SOFTWARE DEVELOPMENT'],
 'web-development/index.html':['Разработка сайтов и веб-приложений на заказ'],
 'app-development/index.html':['Разработка мобильных приложений на заказ.'],
 'automation-services/index.html':['Автоматизация бизнеса и бизнес-процессов.'],
 'ai-automation/index.html':['AI-автоматизация и ИИ-решения для бизнеса.'],
 'crm-development/index.html':['Разработка CRM на заказ.'],
 'mvp-development/index.html':['Разработка MVP на заказ.'],
}
for rel,needles in guards.items():
    data=(ROOT/rel).read_text(encoding='utf-8')
    for needle in needles:
        if needle not in data: raise SystemExit(f'stage189: guard failed {rel}: {needle}')
print(f'stage189 russian market core: pages={len(changed)}')
