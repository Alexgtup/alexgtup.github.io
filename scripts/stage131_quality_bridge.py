#!/usr/bin/env python3
from pathlib import Path
import re,sys,html
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')

DIMS={
'/assets/cases/fin-planner/fin-planner-original-800w.webp':('800','605'),
'/assets/cases/fin-planner/fin-planner-card-01-720w.webp':('720','900'),
'/assets/cases/fin-planner/fin-planner-card-02-720w.webp':('720','900'),
'/assets/cases/swift-calendar/calendar-original-800w.webp':('800','551'),
'/assets/cases/swift-calendar/calendar-card-02-720w.webp':('720','900'),
'/assets/cases/sheetpilot-ai/sheetpilot-01-720w.webp':('720','540'),
'/assets/cases/seo-control-center/seo-control-center-card-02.svg':('1536','1024'),
}

BRIDGES={
'/services/':[
('/telegram-mini-apps/','Telegram Mini Apps'),('/telegram-bot-repair/','Доработка Telegram-бота'),('/ai-automation/','AI-автоматизация'),('/backend-development/','Backend'),('/development/','Общая разработка'),('/freelance-developer/','Прямая работа'),('/cases/factory-catalog/','B2B-каталог'),('/guides/custom-crm-or-ready/','Своя CRM или готовая')],
'/web-development/':[
('/guides/site-vs-web-app/','Сайт или веб-приложение'),('/cases/factory-catalog/','B2B-каталог'),('/ai-automation/','AI-функции'),('/development/','Другие форматы разработки')],
'/telegram-bots/':[
('/telegram-mini-apps/','Telegram Mini Apps'),('/telegram-bot-repair/','Доработка бота'),('/guides/bot-vs-mini-app-vs-web/','Бот, Mini App или веб'),('/guides/telegram-bot-brief/','Короткий бриф')],
'/project-repair/':[
('/telegram-bot-repair/','Доработка Telegram-бота'),('/guides/repair-vs-rewrite/','Чинить или переписывать'),('/freelance-developer/','Прямая работа')],
'/n8n-automation/':[
('/guides/n8n-vs-backend/','n8n или backend'),('/guides/n8n-vs-make/','n8n или Make'),('/ai-automation/','AI-автоматизация'),('/cases/seo-control-center/','SEO Control Center')],
'/backend-development/':[
('/guides/n8n-vs-backend/','n8n или backend'),('/development/','Разработка продукта'),('/ai-automation/','AI-функции')],
'/crm-development/':[
('/guides/custom-crm-or-ready/','Своя CRM или готовая'),('/development/','Разработка продукта')],
'/telegram-mini-apps/':[
('/guides/bot-vs-mini-app-vs-web/','Бот, Mini App или веб'),('/guides/telegram-bot-brief/','Короткий бриф')],
'/ai-automation/':[
('/guides/n8n-vs-make/','n8n или Make'),('/cases/seo-control-center/','SEO Control Center')],
'/development/':[
('/guides/site-vs-web-app/','Сайт или веб-приложение'),('/telegram-mini-apps/','Telegram Mini Apps')],
'/freelance-developer/':[
('/freelance-os/','FreelanceOS'),('/cases/freelance-os/','Кейс FreelanceOS')],
'/about/':[
('/freelance-developer/','Прямая работа'),('/freelance-os/','FreelanceOS'),('/cases/seo-control-center/','SEO Control Center')],
'/telegram-bot-repair/':[
('/guides/repair-vs-rewrite/','Чинить или переписывать'),('/guides/telegram-bot-brief/','Короткий бриф')],
}

def file_for(route): return ROOT/(route.strip('/') or 'index.html') if route=='/' else ROOT/route.strip('/')/'index.html'

def add_dims(src):
    for path,(w,h) in DIMS.items():
        pat=rf'<img\b(?![^>]*\bwidth=)(?=[^>]*src="{re.escape(path)}")([^>]*)>'
        src=re.sub(pat,lambda m:f'<img width="{w}" height="{h}"{m.group(1)}>',src,flags=re.I)
    return src

def bridge_html(items):
    links=''.join(f'<a href="{u}">{html.escape(t)} ↗</a>' for u,t in items)
    return f'<section class="p131-bridge" aria-label="Ещё по теме"><div class="p131-bridge__inner"><span>Ещё по теме</span>{links}</div></section>'

changed=0
for path in ROOT.rglob('*.html'):
    txt=path.read_text(encoding='utf-8',errors='ignore')
    new=add_dims(txt)
    if new!=txt:
        path.write_text(new,encoding='utf-8'); changed+=1

for route,items in BRIDGES.items():
    f=file_for(route)
    if not f.is_file(): raise SystemExit(f'stage131: missing {route}')
    txt=f.read_text(encoding='utf-8')
    if 'p131-bridge' in txt: continue
    block=bridge_html(items)
    marker='<section class="p129-contact">' if 'p129-contact' in txt else '<section class="p130-footer-cta">'
    if marker not in txt: raise SystemExit(f'stage131: insertion marker missing {route}')
    txt=txt.replace(marker,block+marker,1)
    f.write_text(txt,encoding='utf-8')
print(f'stage131 quality bridge: media_fixed_pages={changed}; discovery_bridges={len(BRIDGES)}')
