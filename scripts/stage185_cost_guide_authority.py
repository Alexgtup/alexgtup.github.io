#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'; TARGET='/guides/telegram-bot-cost/'

def load(rel):
 p=ROOT/rel/'index.html'
 if not p.is_file():raise SystemExit(f'stage185: missing {rel}')
 return p,p.read_text(encoding='utf-8')
def once(s,old,new,label):
 if new in s:return s
 if old not in s:raise SystemExit(f'stage185: marker missing {label}')
 return s.replace(old,new,1)

p,s=load('telegram-mini-apps')
old='<section class="p131-bridge" aria-label="Ещё по теме"><div class="p131-bridge__inner"><span>Ещё по теме</span><a href="/guides/bot-vs-mini-app-vs-web/">Бот, Mini App или веб ↗</a><a href="/guides/telegram-bot-brief/">Короткий бриф ↗</a></div></section>'
new='<section class="p131-bridge" aria-label="Ещё по теме"><div class="p131-bridge__inner"><span>Ещё по теме</span><a href="/guides/bot-vs-mini-app-vs-web/">Бот, Mini App или веб ↗</a><a href="/guides/telegram-bot-cost/">Стоимость Telegram-бота ↗</a><a href="/guides/telegram-bot-brief/">Короткий бриф ↗</a></div></section>'
s=once(s,old,new,'miniapp -> cost');p.write_text(s,encoding='utf-8')

p,s=load('guides/bot-vs-mini-app-vs-web')
old='<a class="link-card" href="/ios-development/"><small>iOS</small><strong>iOS на Swift</strong><span>Нативный продукт и мобильный пользовательский сценарий.</span></a></div>'
new='<a class="link-card" href="/ios-development/"><small>iOS</small><strong>iOS на Swift</strong><span>Нативный продукт и мобильный пользовательский сценарий.</span></a><a class="link-card" href="/guides/telegram-bot-cost/"><small>БЮДЖЕТ</small><strong>Сколько стоит Telegram-бот</strong><span>От чего зависит оценка и где появляется основной объём разработки.</span></a></div>'
s=once(s,old,new,'comparison -> cost');p.write_text(s,encoding='utf-8')

p,s=load('cases/fin-planner')
old='<p>Учёт, аналитика и планирование доступны в одном чате без отдельного приложения для базового пользовательского пути. Если сценарию нужен более сложный интерфейс, рядом подходит <a href="/telegram-mini-apps/">Telegram Mini App</a>.</p>'
new='<p>Учёт, аналитика и планирование доступны в одном чате без отдельного приложения для базового пользовательского пути. Если сценарию нужен более сложный интерфейс, рядом подходит <a href="/telegram-mini-apps/">Telegram Mini App</a>. Для оценки похожего проекта есть отдельный разбор <a href="/guides/telegram-bot-cost/">стоимости Telegram-бота</a>.</p>'
s=once(s,old,new,'finplanner -> cost');p.write_text(s,encoding='utf-8')

changed=['telegram-mini-apps','guides/bot-vs-mini-app-vs-web','cases/fin-planner']
for name in ('sitemap.xml','sitemap-google.xml'):
 sm=ROOT/name
 if not sm.exists():continue
 text=sm.read_text(encoding='utf-8')
 for rel in changed:
  url=f'{BASE}/{rel}/'; text=re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
 sm.write_text(text,encoding='utf-8')
for rel in changed:
 if TARGET not in (ROOT/rel/'index.html').read_text(encoding='utf-8'):raise SystemExit(f'stage185: cost link missing in {rel}')
print(f'stage185 cost guide authority: sources={len(changed)}')
