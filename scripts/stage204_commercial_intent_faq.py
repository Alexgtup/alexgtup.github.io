#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-19'

CFG={
 'web-development':{
   'mode':'details',
   'q':'Можно заказать разработку сайта под ключ?',
   'a':'Да. В такой задаче сначала фиксируются структура, ключевой пользовательский сценарий, формы, интеграции и требования к запуску. Затем работа делится на понятные этапы: интерфейс, frontend, backend при необходимости, адаптив, проверка и публикация.'
 },
 'ai-automation':{
   'mode':'details',
   'q':'Что входит во внедрение ИИ в бизнес?',
   'a':'Сначала выбирается конкретный процесс, где AI должен дать измеримый результат. Затем определяются источники данных, правила и ограничения, подключение к API или рабочей системе, проверка ответа и контроль человеком для критичных действий.'
 },
 'automation-services':{
   'mode':'article',
   'q':'Что входит в автоматизацию бизнеса под ключ?',
   'a':'Разбор текущего процесса, выбор одного рабочего сценария, подключение нужных сервисов, обработка ошибок, логирование, уведомления и проверка результата на реальных данных. Инструмент выбирается после понимания процесса, а не заранее.'
 },
 '1c-integration':{
   'mode':'article',
   'q':'Что входит в услугу интеграции 1С?',
   'a':'Определение систем и объектов обмена, сопоставление полей и идентификаторов, настройка передачи данных, обработка повторов и ошибок, журнал обмена и проверка на реальных товарах, заказах, клиентах или документах.'
 },
}

def patch_schema(s:str,q:str,a:str)->str:
    def repl(m):
        try:o=json.loads(m.group(2))
        except Exception:return m.group(0)
        changed=False
        def walk(x):
            nonlocal changed
            if isinstance(x,dict):
                if x.get('@type')=='FAQPage' and isinstance(x.get('mainEntity'),list):
                    names=[str(i.get('name','')) for i in x['mainEntity'] if isinstance(i,dict)]
                    if q not in names:
                        x['mainEntity'].append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}})
                        changed=True
                for v in x.values(): walk(v)
            elif isinstance(x,list):
                for v in x: walk(v)
        walk(o)
        return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3) if changed else m.group(0)
    return re.sub(r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',repl,s,flags=re.I|re.S)

changed=[]
for slug,cfg in CFG.items():
    p=ROOT/slug/'index.html'
    if not p.is_file(): raise SystemExit(f'stage204 missing {slug}')
    s=p.read_text(encoding='utf-8')
    q,a=cfg['q'],cfg['a']
    if q not in s:
        if cfg['mode']=='details':
            m=re.search(r'(<div class="stage174-faq__grid">)(.*?)(</div>)',s,re.I|re.S)
            if not m: raise SystemExit(f'stage204 FAQ grid missing {slug}')
            item=f'<details data-stage204-commercial="true"><summary>{q}</summary><p>{a}</p></details>'
            s=s[:m.start()]+m.group(1)+m.group(2)+item+m.group(3)+s[m.end():]
        else:
            # Match only the FAQ section grid, not any earlier generic card grid.
            sec=re.search(r'(<section class="secondary-demand"[^>]*data-stage172-faq="true"[^>]*>.*?<div class="secondary-demand__grid">)(.*?)(</div></div></section>)',s,re.I|re.S)
            if not sec: raise SystemExit(f'stage204 secondary FAQ missing {slug}')
            item=f'<article class="secondary-demand__card" data-stage204-commercial="true"><h3>{q}</h3><p>{a}</p></article>'
            s=s[:sec.start()]+sec.group(1)+sec.group(2)+item+sec.group(3)+s[sec.end():]
    s=patch_schema(s,q,a)
    p.write_text(s,encoding='utf-8')
    changed.append('/'+slug+'/')

for name in ('sitemap.xml','sitemap-google.xml'):
    p=ROOT/name
    if not p.exists(): continue
    s=p.read_text(encoding='utf-8')
    for route in changed:
        s=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',s,count=1)
    p.write_text(s,encoding='utf-8')

# Visible FAQ and FAQPage must agree. The stage is intentionally idempotent:
# a later/parallel semantic stage may already have added the same useful question.
for slug,cfg in CFG.items():
    s=(ROOT/slug/'index.html').read_text(encoding='utf-8')
    visible=re.sub(r'<script\b[^>]*>.*?</script>','',s,flags=re.I|re.S)
    if cfg['q'] not in visible:
        raise SystemExit(f'stage204 visible question missing {slug}')
    schema_has=False
    for m in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',s,re.I|re.S):
        try:o=json.loads(m.group(1))
        except Exception:continue
        def walk(x):
            nonlocal_marker=[False]
        stack=[o]
        while stack:
            x=stack.pop()
            if isinstance(x,dict):
                if x.get('@type')=='FAQPage' and any(isinstance(q,dict) and q.get('name')==cfg['q'] for q in x.get('mainEntity',[])):
                    schema_has=True
                stack.extend(x.values())
            elif isinstance(x,list):
                stack.extend(x)
    if not schema_has:
        raise SystemExit(f'stage204 FAQ schema missing {slug}')
print('stage204 commercial FAQ alignment: pages=4')
