#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,json,re,sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'
TODAY='2026-09-19'

TITLES={
 'api-development':'Разработка API и REST API для продукта | Alexuys',
 'app-development':'Разработка мобильных приложений iOS и React Native | Alexuys',
 'backend-development':'Backend-разработка: API и базы данных | Alexuys',
 'cases':'Кейсы разработки, автоматизации и интеграций | Alexuys',
 'cases/marketplace-monitor':'Автоматизация Ozon, Wildberries и Яндекс Маркет | кейс',
 'cases/ozon-scanner':'Автоматизация склада Ozon: сканер и Excel | кейс Alexuys',
 'excel-google-sheets-automation':'Автоматизация Excel и Google Sheets на Python | Alexuys',
 'n8n-automation':'n8n автоматизация: CRM, Telegram и API | Alexuys',
 'python-development':'Python-разработка: боты, backend и автоматизация | Alexuys',
 'services':'Разработка ПО, сайтов и автоматизация на заказ | Alexuys',
 'site-repair':'Доработка сайтов: исправления и функционал | Alexuys',
 'telegram-bot-repair':'Доработка Telegram-ботов на Python | Alexuys',
 'telegram-mini-apps':'Разработка Telegram Mini Apps на заказ | Alexuys',
 'tilda-development':'Разработка и доработка сайтов на Tilda | Alexuys',
 'ai-chatbot-development':'Разработка AI-чат-ботов и ассистентов | Alexuys',
 'ai-automation':'AI-автоматизация бизнеса и внедрение ИИ | Alexuys',
}

AI={
 'ai-chatbot-development':{
   'desc':'Разработка AI-чат-ботов и ассистентов для Telegram и сайта: база знаний, ответы по данным, API, формы, передача диалога человеку и контролируемые действия.',
   'h1':'Разработка AI-чат-ботов и ассистентов. <em>Telegram, сайт и база знаний.</em>',
   'task_h2':'AI-чат-бот для Telegram или сайта: ответы, данные и передача человеку.',
   'task_intro':'AI-чат помогает пользователю получить консультацию, найти ответ в базе знаний, оставить заявку или выполнить действие через API. Если вопрос требует проверки, диалог передаётся человеку вместе с собранными данными. Для автоматизации внутренних процессов можно связать ассистента с CRM и рабочими сервисами.',
 },
 'ai-automation':{
   'desc':'AI-автоматизация бизнеса и внедрение ИИ в рабочие процессы: анализ процесса, пилот на реальных данных, API и n8n, проверка результата, логирование и безопасные ограничения.',
   'h1':'AI-автоматизация бизнеса. <em>Внедрение ИИ в рабочие процессы.</em>',
 },
}

def path_for(slug:str)->Path:
    p=ROOT/slug/'index.html'
    if not p.is_file(): raise SystemExit(f'stage207 missing page: {slug}')
    return p

def set_meta(s:str,title:str,desc:str|None=None)->str:
    s,n=re.subn(r'<title\b[^>]*>.*?</title>',f'<title>{html.escape(title)}</title>',s,count=1,flags=re.I|re.S)
    if n!=1: raise SystemExit('stage207 title tag missing')
    def replace_meta(attr,key,value):
        nonlocal s
        pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
        repl=f'<meta {attr}="{key}" content="{html.escape(value,quote=True)}"/>'
        if re.search(pat,s,re.I): s=re.sub(pat,repl,s,count=1,flags=re.I)
    replace_meta('property','og:title',title)
    replace_meta('name','twitter:title',title)
    if desc is not None:
        replace_meta('name','description',desc)
        replace_meta('property','og:description',desc)
        replace_meta('name','twitter:description',desc)
    return s

def set_h1(s:str,value:str,slug:str)->str:
    s,n=re.subn(r'<h1\b([^>]*)>.*?</h1>',lambda m:f'<h1{m.group(1)}>{value}</h1>',s,count=1,flags=re.I|re.S)
    if n!=1: raise SystemExit(f'stage207 h1 missing {slug}')
    return s

def set_first_task(s:str,h2:str,intro:str,slug:str)->str:
    pat=r'(<section class="secondary-demand"[^>]*data-stage172-tasks="true".*?<div class="secondary-demand__head">.*?<div><h2>)(.*?)(</h2><p class="secondary-demand__intro">)(.*?)(</p>)'
    m=re.search(pat,s,re.I|re.S)
    if not m: raise SystemExit(f'stage207 task section missing {slug}')
    return s[:m.start()]+m.group(1)+h2+m.group(3)+intro+m.group(5)+s[m.end():]

def sync_schema_names(s:str,title:str,desc:str|None=None)->str:
    clean=re.sub(r'\s*\|\s*(?:Alexuys|кейс(?:\s+Alexuys)?)\s*$','',title,flags=re.I).strip()
    out=[]; last=0; touched=0
    for m in re.finditer(r'<script([^>]*)type="application/ld\+json"([^>]*)>(.*?)</script>',s,re.I|re.S):
        try:o=json.loads(m.group(3))
        except Exception: continue
        changed=False
        stack=[o]
        while stack:
            x=stack.pop()
            if isinstance(x,dict):
                typ=x.get('@type')
                if typ in ('Service','WebPage'):
                    x['name']=clean; changed=True
                    if desc and 'description' in x: x['description']=desc
                stack.extend(x.values())
            elif isinstance(x,list): stack.extend(x)
        if not changed: continue
        out.append(s[last:m.start(3)])
        out.append(json.dumps(o,ensure_ascii=False,separators=(',',':')))
        last=m.end(3); touched+=1
    if touched:
        out.append(s[last:]); s=''.join(out)
    return s

# Give the strongest Telegram money page a direct homepage path without adding another visual section.
home_path=ROOT/'index.html'
home=home_path.read_text(encoding='utf-8')
telegram_link='<a data-stage207-priority="telegram" href="/telegram-bots/"><strong>Telegram-боты</strong><span>Боты, CRM и API</span><b>↗</b></a>'
if 'href="/telegram-bots/"' not in home:
    anchor='<a href="/n8n-automation/"><strong>n8n / workflows</strong><span>Связать сервисы</span><b>↗</b></a>'
    if anchor not in home: raise SystemExit('stage207 homepage n8n anchor missing')
    home=home.replace(anchor,anchor+telegram_link,1)
    home_path.write_text(home,encoding='utf-8')

changed=[]
for slug,title in TITLES.items():
    if not (35 <= len(title) <= 65): raise SystemExit(f'stage207 title length {slug}: {len(title)}')
    p=path_for(slug); s=p.read_text(encoding='utf-8')
    desc=AI.get(slug,{}).get('desc')
    s=set_meta(s,title,desc)
    if slug in AI:
        s=set_h1(s,AI[slug]['h1'],slug)
        if 'task_h2' in AI[slug]: s=set_first_task(s,AI[slug]['task_h2'],AI[slug]['task_intro'],slug)
    s=sync_schema_names(s,title,desc)
    p.write_text(s,encoding='utf-8'); changed.append('/'+slug+'/')

# Keep the secondary Google sitemap aligned with the canonical sitemap for the WordPress money page.
main=(ROOT/'sitemap.xml').read_text(encoding='utf-8')
google_path=ROOT/'sitemap-google.xml'; google=google_path.read_text(encoding='utf-8')
wp=f'{BASE}/wordpress-development/'
if wp not in google:
    m=re.search(r'<url><loc>'+re.escape(wp)+r'</loc>.*?</url>',main,re.S)
    if not m: raise SystemExit('stage207 WordPress missing from canonical sitemap')
    google=google.replace('</urlset>',m.group(0)+'\n</urlset>',1)
# Refresh changed routes in both sitemap files when present.
for name in ('sitemap.xml','sitemap-google.xml'):
    p=ROOT/name
    t=(google if name=='sitemap-google.xml' else p.read_text(encoding='utf-8'))
    for route in ['/',*changed]:
        t=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',t,count=1)
    p.write_text(t,encoding='utf-8')

# Guards: distinct AI intent, title length, sitemap consistency.
chat=path_for('ai-chatbot-development').read_text(encoding='utf-8')
auto=path_for('ai-automation').read_text(encoding='utf-8')
for needle in ['AI-чат-ботов и ассистентов','Telegram, сайт и база знаний','AI-чат помогает пользователю']:
    if needle not in chat: raise SystemExit(f'stage207 AI chat guard: {needle}')
for needle in ['AI-автоматизация бизнеса','Внедрение ИИ в рабочие процессы']:
    if needle not in auto: raise SystemExit(f'stage207 AI automation guard: {needle}')
if 'href="/telegram-bots/"' not in home_path.read_text(encoding='utf-8'): raise SystemExit('stage207 homepage Telegram guard')
if wp not in (ROOT/'sitemap-google.xml').read_text(encoding='utf-8'): raise SystemExit('stage207 sitemap-google WordPress guard')
for slug,title in TITLES.items():
    s=path_for(slug).read_text(encoding='utf-8')
    m=re.search(r'<title>(.*?)</title>',s,re.S)
    if not m or html.unescape(m.group(1))!=title: raise SystemExit(f'stage207 title guard: {slug}')
print(f'stage207 search concentration: titles={len(TITLES)}, ai_intents=2, sitemap_google_wordpress=ok')
