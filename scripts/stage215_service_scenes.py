#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
CSS='<link rel="stylesheet" href="/assets/stage215-service-scenes.css">'
SCENES={
'telegram-bots':'''<aside class="p215-system p215-system--telegram" aria-label="Схема Telegram-бота: событие проходит через бот, проверку, API и рабочую систему"><div class="p215-system__top"><small>BOT FLOW · 01</small><span class="p215-status"><i></i>scenario online</span></div><div class="p215-flow"><i class="p215-packet" aria-hidden="true"></i><div class="p215-node"><small>01 / INPUT</small><strong>Telegram</strong><span>сообщение / кнопка</span></div><div class="p215-node"><small>02 / LOGIC</small><strong>Bot layer</strong><span>state / validation</span></div><div class="p215-node"><small>03 / DATA</small><strong>API / DB</strong><span>read / write</span></div><div class="p215-node"><small>04 / ACTION</small><strong>CRM / Payment</strong><span>status / result</span></div></div><div class="p215-log"><code>event → validate → action → response</code><b>CONTROLLED FLOW</b></div></aside>''',
'n8n-automation':'''<aside class="p215-system p215-system--n8n" aria-label="Схема n8n workflow: webhook, проверка, действие в CRM и уведомление"><div class="p215-system__top"><small>WORKFLOW · 04</small><span class="p215-status"><i></i>execution healthy</span></div><div class="p215-flow"><i class="p215-packet" aria-hidden="true"></i><div class="p215-node"><small>TRIGGER</small><strong>Webhook</strong><span>new event</span></div><div class="p215-node"><small>CHECK</small><strong>Validate</strong><span>rules / data</span></div><div class="p215-node"><small>ACTION</small><strong>CRM / API</strong><span>write / sync</span></div><div class="p215-node"><small>OUTPUT</small><strong>Notify</strong><span>Telegram / mail</span></div></div><div class="p215-log"><code>retry: 3 · idempotency: on · errors: logged</code><b>NO SILENT FAILURES</b></div></aside>''',
'wordpress-development':'''<aside class="hero-side"><div class="p215-system p215-system--wordpress" aria-label="Схема точечной доработки существующего WordPress сайта"><div class="p215-system__top"><small>EXISTING SITE · PATCH MAP</small><span class="p215-status"><i></i>keep what works</span></div><div class="p215-stack"><div class="p215-layer"><i>01</i><div><strong>Theme</strong><span>шаблоны и текущий UI</span></div><b>KEEP</b></div><div class="p215-layer" data-patch="true"><i>02</i><div><strong>Forms / logic</strong><span>ошибка → причина → фикс</span></div><b>PATCH</b></div><div class="p215-layer" data-patch="true"><i>03</i><div><strong>Mobile / speed</strong><span>адаптив и загрузка</span></div><b>PATCH</b></div><div class="p215-layer"><i>04</i><div><strong>SEO / schema</strong><span>индексация и разметка</span></div><b>CHECK</b></div></div><div class="p215-patch-note">Меняется только тот слой, который мешает задаче. Рабочая тема и данные остаются на месте.</div></div></aside>'''
}
for slug,scene in SCENES.items():
 p=ROOT/slug/'index.html'
 if not p.is_file():raise SystemExit(f'stage215 missing {slug}')
 s=p.read_text(encoding='utf8')
 s=re.sub(r'\s*<link[^>]+stage215-service-scenes\.css[^>]*>','',s,flags=re.I)
 s=re.sub(r'\sdata-stage215-service="[^"]+"','',s)
 if slug in ('telegram-bots','n8n-automation'):
  pat=r'<div class="p155-service-preview">.*?</div></section>'
  repl='<div class="p155-service-preview">'+scene+'</div></section>'
  s,n=re.subn(pat,repl,s,count=1,flags=re.S)
 else:
  pat=r'<aside class="hero-side">.*?</aside></section>'
  s,n=re.subn(pat,scene+'</section>',s,count=1,flags=re.S)
 if n!=1:raise SystemExit(f'stage215 hero replace failed {slug}')
 s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+f' data-stage215-service="{slug.replace("-development","").replace("-automation","")}">',s,count=1,flags=re.I)
 if n!=1:raise SystemExit(f'stage215 body missing {slug}')
 s=s.replace('</head>',CSS+'</head>',1)
 p.write_text(s,encoding='utf8')
# Guards.
for slug in SCENES:
 s=(ROOT/slug/'index.html').read_text(encoding='utf8')
 if s.count('stage215-service-scenes.css')!=1 or s.count('p215-system')<1:raise SystemExit(f'stage215 shell guard {slug}')
 if slug!='wordpress-development' and s.count('p215-node')!=4:raise SystemExit(f'stage215 node guard {slug}')
print('stage215 service scenes: telegram=bot-flow, n8n=workflow, wordpress=patch-map')
