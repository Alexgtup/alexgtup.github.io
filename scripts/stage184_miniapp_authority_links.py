#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re, sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'
TODAY='2026-09-18'
TARGET='/telegram-mini-apps/'

def load(rel):
    p=ROOT/rel/'index.html'
    if not p.is_file():raise SystemExit(f'stage184: missing {rel}')
    return p,p.read_text(encoding='utf-8')

def once(s,old,new,label):
    if new in s:return s
    if old not in s:raise SystemExit(f'stage184: marker missing {label}')
    return s.replace(old,new,1)

# Add only contextually relevant links from established pages. No sitewide footer/link farm.
p,s=load('web-development')
old='<div class="search-demand__links"><a href="/cases/factory-catalog/">Кейс B2B-каталога ↗</a><a href="/backend-development/">Backend и API ↗</a><a href="/mvp-development/">Разработка MVP ↗</a></div>'
new='<div class="search-demand__links"><a href="/cases/factory-catalog/">Кейс B2B-каталога ↗</a><a href="/backend-development/">Backend и API ↗</a><a href="/mvp-development/">Разработка MVP ↗</a><a href="/telegram-mini-apps/">Telegram Mini App ↗</a></div>'
s=once(s,old,new,'web -> miniapp');p.write_text(s,encoding='utf-8')

p,s=load('mvp-development')
old='<div class="search-demand__links"><a href="/web-development/">Веб-разработка ↗</a><a href="/app-development/">Мобильное приложение ↗</a><a href="/guides/development-cost/">Стоимость разработки ↗</a></div>'
new='<div class="search-demand__links"><a href="/web-development/">Веб-разработка ↗</a><a href="/app-development/">Мобильное приложение ↗</a><a href="/telegram-mini-apps/">MVP Telegram Mini App ↗</a><a href="/guides/development-cost/">Стоимость разработки ↗</a></div>'
s=once(s,old,new,'mvp -> miniapp');p.write_text(s,encoding='utf-8')

p,s=load('guides/telegram-bot-cost')
old='<a class="link-card" href="/cases/fin-planner/"><small>КЕЙС</small><strong>Фин Планер</strong><span>Реальный Telegram-бот для бюджета, отчётов, целей и финансового анализа.</span></a></div>'
new='<a class="link-card" href="/cases/fin-planner/"><small>КЕЙС</small><strong>Фин Планер</strong><span>Реальный Telegram-бот для бюджета, отчётов, целей и финансового анализа.</span></a><a class="link-card" href="/telegram-mini-apps/"><small>АЛЬТЕРНАТИВА</small><strong>Telegram Mini App на заказ</strong><span>Когда вместо диалога нужен каталог, кабинет, формы или сложный интерфейс внутри Telegram.</span></a></div>'
s=once(s,old,new,'cost -> miniapp');p.write_text(s,encoding='utf-8')

p,s=load('cases/fin-planner')
old='<p>Учёт, аналитика и планирование доступны в одном чате без отдельного приложения для базового пользовательского пути.</p>'
new='<p>Учёт, аналитика и планирование доступны в одном чате без отдельного приложения для базового пользовательского пути. Если сценарию нужен более сложный интерфейс, рядом подходит <a href="/telegram-mini-apps/">Telegram Mini App</a>.</p>'
s=once(s,old,new,'finplanner -> miniapp');p.write_text(s,encoding='utf-8')

changed=['web-development','mvp-development','guides/telegram-bot-cost','cases/fin-planner']
for name in ('sitemap.xml','sitemap-google.xml'):
    sm=ROOT/name
    if not sm.exists():continue
    text=sm.read_text(encoding='utf-8')
    for rel in changed:
        url=f'{BASE}/{rel}/'
        text=re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
    sm.write_text(text,encoding='utf-8')

for rel in changed:
    data=(ROOT/rel/'index.html').read_text(encoding='utf-8')
    if TARGET not in data:raise SystemExit(f'stage184: miniapp link missing in {rel}')
print(f'stage184 miniapp authority links: sources={len(changed)}')
