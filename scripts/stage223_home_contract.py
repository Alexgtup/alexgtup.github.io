#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file():raise SystemExit('stage223 home missing')
s=p.read_text(encoding='utf8')
CSS='<link rel="stylesheet" href="/assets/stage223-home-contract.css">'
# idempotent shell cleanup
s=re.sub(r'\s*<link[^>]+stage223-home-contract\.css[^>]*>','',s,flags=re.I)
s=re.sub(r'\sdata-stage223-home="true"','',s)
s=re.sub(r'\sdata-stage223-rank="[^"]+"','',s)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage223-home="true">',s,count=1,flags=re.I)
if n!=1:raise SystemExit('stage223 body missing')
s=s.replace('</head>',CSS+'</head>',1)
# Build-time factual counts from generated public surfaces.
case_count=sum(1 for x in (ROOT/'cases').glob('*/index.html') if x.is_file())
demo_count=4
tool_count=sum(1 for x in (ROOT/'tools').glob('*/index.html') if x.is_file())
# tools/ itself is not a utility.
if tool_count<1:raise SystemExit('stage223 tools count invalid')
# Stable, verifiable proof rail; no embedded marketplace rating that can silently go stale.
proof=(f'<div class="p128-proofbar" aria-label="Проверяемые факты">'
       f'<a href="https://freelance.ru/gglalex" target="_blank" rel="me noopener noreferrer"><strong>Отзывы</strong><span>публично на Freelance.ru</span></a>'
       f'<a href="/cases/"><strong>{case_count}</strong><span>реальных кейсов</span></a>'
       f'<a href="/demos/"><strong>{demo_count}</strong><span>публичных демо</span></a>'
       f'<a href="/tools/"><strong>{tool_count}</strong><span>browser-tools</span></a></div>')
s,n=re.subn(r'<div class="p128-proofbar"[^>]*>.*?</div>',proof,s,count=1,flags=re.S)
if n!=1:raise SystemExit('stage223 proofbar missing')
# Broader real-work curation: commercial client work first, then product/system cases.
work='''<div class="p128-work-list">
<article class="p128-feature p128-feature--portfolio wow-reveal" data-stage223-rank="01"><a class="p128-feature__media" href="/cases/wordpress-commercial/" aria-label="Открыть кейс коммерческого WordPress-сайта"><img src="/assets/cases/wordpress-commercial/wordpress-commercial-01.webp" width="1600" height="1000" loading="lazy" decoding="async" alt="Коммерческий WordPress-сайт — реальный проект"></a><div class="p128-feature__copy"><span>01 / WORDPRESS / PRODUCTION</span><h3>Коммерческий WordPress</h3><p>Доработка работающего сайта: формы, калькуляторы, страницы, мобильная версия и технические исправления без полной пересборки.</p><ul class="p128-feature__points"><li>Рабочая тема сохранена</li><li>Формы и логика</li><li>Mobile</li><li>SEO / schema</li></ul><a href="/cases/wordpress-commercial/">Разобрать кейс ↗</a></div></article>
<article class="p128-feature p128-feature--portfolio wow-reveal" data-stage223-rank="02"><a class="p128-feature__media" href="/cases/fin-planner/" aria-label="Открыть кейс Fin Planner"><img src="/assets/cases/fin-planner/fin-planner-original-800w.webp" width="800" height="605" loading="lazy" decoding="async" alt="Fin Planner — Telegram-сервис для учета финансов"></a><div class="p128-feature__copy"><span>02 / TELEGRAM / PRODUCT</span><h3>Fin Planner</h3><p>Финансовый сервис внутри Telegram: учёт операций, цели, прогноз и отчёты в одном пользовательском сценарии.</p><ul class="p128-feature__points"><li>Доходы и расходы</li><li>Состояния</li><li>Данные</li><li>Backend</li></ul><a href="/cases/fin-planner/">Разобрать кейс ↗</a></div></article>
<article class="p128-feature p128-feature--portfolio wow-reveal" data-stage223-rank="03"><a class="p128-feature__media" href="/cases/seo-control-center/" aria-label="Открыть кейс SEO Control Center"><img src="/assets/cases/seo-control-center/seo-control-center-live-01.webp" width="1600" height="1000" loading="lazy" decoding="async" alt="SEO Control Center — панель мониторинга поисковой видимости"></a><div class="p128-feature__copy"><span>03 / SEO / PLATFORM</span><h3>SEO Control Center</h3><p>Панель для контроля индексации, поисковых метрик, sitemap и технических событий по нескольким сайтам.</p><ul class="p128-feature__points"><li>Search data</li><li>Sitemap</li><li>Events</li><li>PostgreSQL</li></ul><a href="/cases/seo-control-center/">Разобрать кейс ↗</a></div></article>
<article class="p128-feature p128-feature--portfolio wow-reveal" data-stage223-rank="04"><a class="p128-feature__media" href="/cases/sheetpilot-ai/" aria-label="Открыть кейс SheetPilot AI"><img src="/assets/cases/sheetpilot-ai/sheetpilot-live-01.webp" width="1600" height="1000" loading="lazy" decoding="async" alt="SheetPilot AI — веб-интерфейс обработки Excel"></a><div class="p128-feature__copy"><span>04 / AI / DATA PRODUCT</span><h3>SheetPilot AI</h3><p>Excel меняется обычной фразой: загрузить файл, описать действие, проверить результат и скачать новую версию.</p><ul class="p128-feature__points"><li>Excel</li><li>Preview</li><li>AI commands</li><li>Export</li></ul><a href="/cases/sheetpilot-ai/">Открыть кейс и демо ↗</a></div></article>
</div>'''
s,n=re.subn(r'<div class="p128-work-list">.*?</div>\s*</div>\s*</section>',work+'</div></section>',s,count=1,flags=re.S)
if n!=1:raise SystemExit('stage223 work list replace failed')
# Replace stale numeric reputation panel with controlled proof surfaces.
nums=(f'<div class="p128-proof__numbers"><div><strong>Отзывы</strong><span>публичный профиль Freelance.ru</span></div>'
      f'<div><strong>{case_count}</strong><span>реальных кейсов на сайте</span></div>'
      f'<div><strong>{demo_count}</strong><span>публичных демо</span></div>'
      f'<div><strong>{tool_count}</strong><span>browser-tools без регистрации</span></div></div>')
s,n=re.subn(r'<div class="p128-proof__numbers">.*?</div>\s*</div>\s*</section>',nums+'</div></section>',s,count=1,flags=re.S)
if n!=1:raise SystemExit('stage223 proof numbers replace failed')
p.write_text(s,encoding='utf8')
# guards
f=p.read_text(encoding='utf8')
for needle in ['data-stage223-home="true"','stage223-home-contract.css','/cases/wordpress-commercial/','/cases/fin-planner/','/cases/seo-control-center/','/cases/sheetpilot-ai/',f'<strong>{case_count}</strong><span>реальных кейсов</span>',f'<strong>{tool_count}</strong><span>browser-tools</span>']:
 if needle not in f:raise SystemExit(f'stage223 guard: {needle}')
for stale in ['<strong>10/10</strong><span>профессионализм</span>','<strong>9</strong><span>подробных кейсов</span>','<strong>18</strong><span>публичных отзывов</span>']:
 if stale in f:raise SystemExit(f'stage223 stale proof remains: {stale}')
if f.count('data-stage223-rank=')!=4:raise SystemExit('stage223 work rank count')
print(f'stage223 homepage contract: cases={case_count}, demos={demo_count}, tools={tool_count}, selected=wordpress/telegram/seo/ai')
