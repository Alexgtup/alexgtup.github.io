#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'

FAQS={
'web-development':[
 ('Что входит в разработку сайта под ключ?','Обычно это структура и сценарии, интерфейс, frontend, нужная серверная логика, формы и интеграции, адаптивная версия, проверка и публикация. Состав зависит от типа сайта и того, что уже готово.'),
 ('От чего зависит цена разработки сайта?','От количества уникальных экранов и сценариев, объёма backend-логики, интеграций, личного кабинета, контента и состояния исходного проекта. Точную оценку разумнее давать после разбора первого рабочего сценария.'),
],
'development':[
 ('Что входит в услугу разработки программного обеспечения?','Проектирование рабочего сценария, интерфейс при необходимости, серверная логика, данные, роли, API и интеграции, тестирование и запуск. Большую систему можно выпускать по законченным этапам.'),
 ('Как оценивается стоимость разработки программного обеспечения?','По объёму сценариев и бизнес-логики, интеграциям, модели данных, ролям, требованиям к интерфейсу и готовности текущего кода. Сначала фиксируется минимальный рабочий контур, затем следующий этап.'),
],
'app-development':[
 ('От чего зависит цена разработки мобильного приложения?','От количества пользовательских сценариев, уникальных экранов, backend и API, авторизации, платежей, push-уведомлений и необходимости поддерживать несколько платформ.'),
 ('Можно заказать разработку мобильного приложения поэтапно?','Да. Первый этап лучше ограничить главным пользовательским сценарием и версией, которую можно установить и проверить на реальном устройстве. Остальные функции добавляются после проверки основы.'),
],
'automation-services':[
 ('Какие бизнес-процессы можно автоматизировать?','Передачу заявок в CRM, обработку форм и таблиц, отчёты, документы, уведомления, синхронизацию сервисов, регулярные проверки и другие повторяющиеся операции с понятными правилами.'),
 ('Автоматизация бизнеса обязательно требует n8n?','Нет. n8n подходит для многих интеграционных процессов, но для сложной логики может понадобиться Python или отдельный backend. Инструмент выбирается после описания процесса и требований к надёжности.'),
],
'ai-automation':[
 ('Когда имеет смысл разработка ИИ-решения для бизнеса?','Когда в процессе есть повторяющаяся работа с текстами, документами, классификацией, поиском, подготовкой ответов или извлечением данных и результат можно проверить по понятным правилам.'),
 ('Можно внедрить ИИ в существующий процесс без отдельного продукта?','Да. AI можно подключить как один контролируемый этап к CRM, внутреннему сервису, таблицам, Telegram или API, не перестраивая весь рабочий процесс вокруг нейросети.'),
],
}

def append_faq(slug,items):
 p=ROOT/slug/'index.html'
 if not p.is_file(): raise SystemExit(f'stage190: missing {slug}')
 s=p.read_text(encoding='utf-8')
 marker=f'data-stage190-russian-faq="{slug}"'
 if marker not in s:
  m=re.search(r'(<div class="stage174-faq__grid">)(.*?)(</div></div></section>)',s,re.I|re.S)
  if m:
   extra=''.join(f'<details {marker}><summary>{q}</summary><p>{a}</p></details>' for q,a in items)
   s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
  else:
   # stage172 generated service pages use card-based FAQ rather than stage174 details.
   sec=re.search(r'(<section class="secondary-demand"[^>]*data-stage172-faq="true".*?<div class="secondary-demand__grid">)(.*?)(</div></div></section>)',s,re.I|re.S)
   if not sec: raise SystemExit(f'stage190: visible FAQ missing {slug}')
   extra=''.join(f'<article {marker} class="secondary-demand__card"><h3>{q}</h3><p>{a}</p></article>' for q,a in items)
   s=s[:sec.start()]+sec.group(1)+sec.group(2)+extra+sec.group(3)+s[sec.end():]
 # Prefer the explicit stage174 schema; generated pages may have an un-IDed FAQPage script.
 sm=re.search(r'<script id="stage174-faq-schema" type="application/ld\+json">(.*?)</script>',s,re.I|re.S)
 if not sm:
  for candidate in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.I|re.S):
   if '"FAQPage"' in candidate.group(1):
    sm=candidate; break
 if not sm: raise SystemExit(f'stage190: schema missing {slug}')
 obj=json.loads(sm.group(1)); existing={x.get('name') for x in obj.get('mainEntity',[])}
 for q,a in items:
  if q not in existing:
   obj.setdefault('mainEntity',[]).append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}})
 blob=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
 s=s[:sm.start(1)]+blob+s[sm.end(1):]
 p.write_text(s,encoding='utf-8')
 return '/'+slug+'/'

changed=[append_faq(slug,items) for slug,items in FAQS.items()]
for name in ('sitemap.xml','sitemap-google.xml'):
 p=ROOT/name
 if not p.exists(): continue
 text=p.read_text(encoding='utf-8')
 for route in changed:
  url=BASE+route
  text=re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
 p.write_text(text,encoding='utf-8')
for slug,items in FAQS.items():
 s=(ROOT/slug/'index.html').read_text(encoding='utf-8')
 if s.count(f'data-stage190-russian-faq="{slug}"')!=len(items): raise SystemExit(f'stage190: visible FAQ count failed {slug}')
 sm=re.search(r'<script id="stage174-faq-schema" type="application/ld\+json">(.*?)</script>',s,re.I|re.S)
 if not sm:
  for candidate in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',s,re.I|re.S):
   if '"FAQPage"' in candidate.group(1): sm=candidate; break
 if not sm: raise SystemExit(f'stage190: schema guard missing {slug}')
 obj=json.loads(sm.group(1)); names={x.get('name') for x in obj.get('mainEntity',[])}
 for q,_ in items:
  if q not in names: raise SystemExit(f'stage190: schema guard failed {slug}: {q}')
print(f'stage190 russian commercial depth: pages={len(changed)}, faq={sum(map(len,FAQS.values()))}')
