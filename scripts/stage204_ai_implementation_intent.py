#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'
p=ROOT/'ai-automation'/'index.html'
s=p.read_text(encoding='utf-8')
old_head='ИИ-агенты и AI-автоматизация для бизнеса: конкретный шаг процесса, а не декоративный AI.'
new_head='Внедрение ИИ в бизнес: от процесса до ИИ-агента.'
old_intro='ИИ для бизнеса имеет смысл внедрять там, где понятны входные данные, ожидаемый результат и способ проверить ответ: классификация, извлечение данных, подготовка черновика, поиск, анализ файла или следующий шаг внутри автоматизированного workflow.'
new_intro='Внедрение ИИ в бизнес начинается не с выбора модели, а с конкретного процесса: где теряется время, какие данные приходят на вход, какой результат нужен и как его проверить. После этого можно собрать небольшой пилот на реальных данных, подключить API или workflow и только затем расширять автоматизацию.'
if old_head not in s or old_intro not in s:
    raise SystemExit('stage204 AI section anchor missing')
s=s.replace(old_head,new_head,1).replace(old_intro,new_intro,1)
# Replace the first 5-card task grid in this section with an implementation-first sequence.
section_pos=s.find(new_head)
grid_start=s.find('<div class="secondary-demand__grid">',section_pos)
grid_end=s.find('</div><nav class="secondary-demand__links"',grid_start)
if grid_start<0 or grid_end<0:
    raise SystemExit('stage204 AI grid missing')
new_grid='''<div class="secondary-demand__grid" data-stage204-ai-implementation="true"><article class="secondary-demand__card"><h3>Аудит процесса</h3><p>Определяется повторяющийся участок, входные данные, ожидаемый результат и правило проверки. Если результат нельзя проверить, AI не должен получать критичное действие.</p></article><article class="secondary-demand__card"><h3>Пилот на реальных данных</h3><p>Один сценарий проверяется на небольшом наборе реальных примеров: документы, заявки, таблицы, сообщения или внутренние знания. Это показывает качество до большой интеграции.</p></article><article class="secondary-demand__card"><h3>Интеграция AI + API</h3><p>Рабочий шаг подключается к CRM, внутреннему сервису, Telegram, таблицам или другому API без ручного копирования данных между системами.</p></article><article class="secondary-demand__card"><h3>Контроль результата</h3><p>Формат ответа ограничивается, результат валидируется, ошибки логируются, а для критичных действий остаётся ручное подтверждение или безопасный fallback.</p></article><article class="secondary-demand__card" data-stage195-ai-agent="true"><h3>ИИ-агент для бизнеса</h3><p>Получает контекст, выбирает действие из ограниченного набора, обращается к API или workflow и возвращает результат с журналированием и проверками.</p></article><article class="secondary-demand__card" data-stage195-ai-assistant="true"><h3>ИИ-ассистент</h3><p>Помогает сотруднику искать, классифицировать, извлекать и подготавливать данные, не забирая критичные решения у человека.</p></article></div>'''
s=s[:grid_start]+new_grid+s[grid_end+6:]
# Add one visible FAQ matching the implementation intent without duplicating existing questions.
faq_anchor='<details data-stage190-russian-faq="ai-automation"><summary>Когда имеет смысл разработка ИИ-решения для бизнеса?</summary>'
idx=s.find(faq_anchor)
if idx<0: raise SystemExit('stage204 FAQ anchor missing')
faq_block='<details data-stage204-ai-faq="true"><summary>Что входит во внедрение ИИ в бизнес?</summary><p>Сначала разбирается конкретный процесс и критерий полезного результата, затем делается пилот на реальных данных, после проверки качества подключаются API или workflow, логирование, ограничения и контроль ошибок. Большую систему не нужно строить до проверки одного рабочего сценария.</p></details>'
s=s[:idx]+faq_block+s[idx:]
# Keep FAQ schema aligned with visible FAQ.
def repl(m):
    try:o=json.loads(m.group(2))
    except Exception:return m.group(0)
    if isinstance(o,dict) and o.get('@type')=='FAQPage':
        ents=o.setdefault('mainEntity',[])
        q='Что входит во внедрение ИИ в бизнес?'
        if not any(isinstance(x,dict) and x.get('name')==q for x in ents):
            ents.append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':'Сначала разбирается конкретный процесс и критерий полезного результата, затем делается пилот на реальных данных, после проверки качества подключаются API или workflow, логирование, ограничения и контроль ошибок. Большую систему не нужно строить до проверки одного рабочего сценария.'}})
    return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
s=re.sub(r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',repl,s,flags=re.I|re.S)
p.write_text(s,encoding='utf-8')
# Make the broad demand visible from the homepage without creating a new landing page.
hp=ROOT/'index.html';h=hp.read_text(encoding='utf-8')
h=h.replace('<strong>ИИ и ИИ-агенты</strong><em>AI внутри процесса, API, данные и контроль результата</em>', '<strong>Внедрение ИИ в бизнес</strong><em>ИИ-агенты, API, данные и контроль результата</em>',1)
hp.write_text(h,encoding='utf-8')
# Ecommerce already has price FAQ; add the central cost guide as a relevant related resource.
ep=ROOT/'ecommerce-development'/'index.html';e=ep.read_text(encoding='utf-8')
nav='<nav class="secondary-demand__links" data-stage201-authority="true" aria-label="Связанные направления">'
if nav in e and 'href="/guides/development-cost/"' not in e:
    e=e.replace(nav,nav+'<a data-stage204-cost-link="true" href="/guides/development-cost/">Стоимость разработки ↗</a>',1)
ep.write_text(e,encoding='utf-8')
# Refresh only changed pages in sitemap.
for name in ('sitemap.xml','sitemap-google.xml'):
    sp=ROOT/name
    if not sp.exists(): continue
    t=sp.read_text(encoding='utf-8')
    for route in ['/','/ai-automation/','/ecommerce-development/']:
        t=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',t,count=1)
    sp.write_text(t,encoding='utf-8')
# Guards.
a=p.read_text(encoding='utf-8'); h=hp.read_text(encoding='utf-8'); e=ep.read_text(encoding='utf-8')
for x in [new_head,'data-stage204-ai-implementation="true"','Что входит во внедрение ИИ в бизнес?','Аудит процесса','Пилот на реальных данных']:
    if x not in a: raise SystemExit('stage204 guard AI '+x)
if '<strong>Внедрение ИИ в бизнес</strong>' not in h: raise SystemExit('stage204 home guard')
if 'data-stage204-cost-link="true"' not in e: raise SystemExit('stage204 ecommerce guide guard')
print('stage204 AI implementation intent: process-first section + FAQ + homepage anchor + ecommerce cost link')
