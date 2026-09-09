#!/usr/bin/env python3
from pathlib import Path
import html as htmlmod
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')

def main_bounds(text: str):
    start = re.search(r'<main\b[^>]*>', text, re.I)
    if not start: return None
    end = re.search(r'</main>', text[start.end():], re.I)
    if not end: return None
    return start.start(), start.end(), start.end()+end.start(), start.end()+end.end()

def top_sections(text: str):
    bounds = main_bounds(text)
    if not bounds: return []
    _, ms, me, _ = bounds
    frag = text[ms:me]
    tokens = re.compile(r'<section\b[^>]*>|</section\s*>', re.I)
    depth=0; start=None; out=[]
    for m in tokens.finditer(frag):
        tok=m.group(0)
        if tok.lower().startswith('<section'):
            if depth==0: start=m.start()
            depth+=1
        else:
            depth-=1
            if depth==0 and start is not None:
                full=frag[start:m.end()]
                hm=re.search(r'<h[12]\b[^>]*>(.*?)</h[12]>',full,re.I|re.S)
                heading=''
                if hm:
                    heading=re.sub(r'<[^>]+>',' ',hm.group(1))
                    heading=re.sub(r'\s+',' ',htmlmod.unescape(heading)).strip()
                out.append({'start':ms+start,'end':ms+m.end(),'html':full,'heading':heading})
                start=None
    return out

def remove_matching(text: str, headings=(), contains=()):
    while True:
        hit=None
        for s in top_sections(text):
            if any(s['heading'].startswith(h) for h in headings) or any(c in s['html'] for c in contains):
                hit=s; break
        if not hit: return text
        text=text[:hit['start']]+text[hit['end']:]

rules={
    'auto-crm': dict(
        headings=('Что в этом кейсе действительно подтверждается.','Что учесть в похожем проекте.','Какой тип разработки стоит за этим проектом.'),
        contains=('Своя CRM или готовое решение →',),
    ),
    'factory-catalog': dict(
        headings=('Что в этом кейсе действительно подтверждается.','Что учесть в похожем проекте.','Какой тип разработки стоит за этим проектом.'),
        contains=(),
    ),
    'taxi-app': dict(
        headings=('Что в этом кейсе действительно подтверждается.','Что учесть в похожем проекте.','Какой тип разработки стоит за этим проектом.'),
        contains=(),
    ),
    'fin-planner': dict(headings=('Telegram может быть полноценным продуктом.',), contains=()),
    'sheetpilot-ai': dict(headings=('Fullstack-проект, а не чат поверх API.',), contains=()),
    'swift-calendar': dict(headings=('Мобильная разработка с продуктовой логикой.',), contains=()),
}

changed=0; report=[]; errors=[]
for slug, rule in rules.items():
    p=root/'cases'/slug/'index.html'
    if not p.exists():
        errors.append(f'missing case {slug}'); continue
    text=p.read_text(encoding='utf-8',errors='ignore')
    before=len(top_sections(text))
    new=remove_matching(text,rule['headings'],rule['contains'])
    after=len(top_sections(new))
    if new!=text:
        p.write_text(new,encoding='utf-8'); changed+=1
    report.append((slug,before,after))

expected_max={'auto-crm':3,'factory-catalog':3,'taxi-app':3,'fin-planner':6,'sheetpilot-ai':6,'swift-calendar':4}
for slug,_,after in report:
    if after>expected_max[slug]: errors.append(f'{slug}: still {after} top-level sections, expected <= {expected_max[slug]}')

if errors:
    raise SystemExit('stage98 case polish failed:\n'+'\n'.join(errors))
print('stage98 case polish: '+', '.join(f'{s} {b}->{a}' for s,b,a in report)+f'; changed={changed}')
