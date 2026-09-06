#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib, json, re, sys

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
home=root/'index.html'; before=hashlib.sha256(home.read_bytes()).hexdigest()
SAME=['https://github.com/Alexgtup','https://freelance.ru/gglalex','https://t.me/Alexuys']

def walk(o, english=False):
    if isinstance(o,dict):
        typ=o.get('@type')
        types=typ if isinstance(typ,list) else [typ]
        if 'Person' in types:
            o['name']='Alexandr Alexandrov' if english else 'Александр Александров'
            o['alternateName']=['Alexuys','gglalex','Александр Александров','Alexandr Alexandrov']
            o['jobTitle']='Software developer: web, mobile, Telegram, backend and automation' if english else 'Разработчик сайтов, приложений, Telegram, backend и автоматизации'
            cur=o.get('sameAs',[])
            if not isinstance(cur,list): cur=[cur]
            o['sameAs']=list(dict.fromkeys([x for x in cur+SAME if x]))
        for v in o.values(): walk(v,english)
    elif isinstance(o,list):
        for v in o: walk(v,english)

def patch_jsonld(text,english):
    pat=re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',re.I|re.S)
    def repl(m):
        raw=m.group(2).strip()
        try:o=json.loads(raw)
        except Exception:return m.group(0)
        walk(o,english)
        return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
    return pat.sub(repl,text)

count=0
for p in root.rglob('*.html'):
    rel=p.relative_to(root).as_posix()
    if rel=='index.html': continue
    if rel=='404.html' or rel.startswith(('google','yandex')): continue
    text=p.read_text(encoding='utf8',errors='ignore'); old=text
    english=rel.startswith('en/')
    text=patch_jsonld(text,english)
    author='Alexandr Alexandrov (Alexuys)' if english else 'Александр Александров (Alexuys)'
    text=re.sub(r'(<meta\s+content=")[^"]*("\s+name="author"\s*/?>)',lambda m:m.group(1)+author+m.group(2),text,count=1,flags=re.I)
    if text!=old:
        p.write_text(text,encoding='utf8');count+=1

stats='<div class="s50-stats"><div><strong>Отзывы</strong><span>публично на Freelance.ru</span></div><div><strong>Задания</strong><span>история выполненных работ</span></div><div><strong>2023</strong><span>профиль на площадке</span></div></div>'
for route in ('about','freelance-developer'):
    p=root/route/'index.html'; text=p.read_text(encoding='utf8')
    text,n=re.subn(r'<div class="s50-stats">.*?</div></div></div>',stats+'</div>',text,count=1,flags=re.S)
    if n!=1: raise SystemExit('stage53 stats block missing '+route)
    if route=='about':
        text=text.replace('ALEXANDR · DEVELOPER','ALEXANDR ALEXANDROV · ALEXUYS',1)
        text=re.sub(r'<title>.*?</title>','<title>Александр Александров — разработчик | Alexuys</title>',text,count=1,flags=re.S)
        text=re.sub(r'(<meta\s+content=")[^"]*("\s+property="og:title"\s*/?>)',r'\1Александр Александров — разработчик | Alexuys\2',text,count=1,flags=re.I)
        text=re.sub(r'(<meta\s+content=")[^"]*("\s+name="twitter:title"\s*/?>)',r'\1Александр Александров — разработчик | Alexuys\2',text,count=1,flags=re.I)
    else:
        text=text.replace('FREELANCE DEVELOPER · VERIFIED PROFILE','ALEXANDR ALEXANDROV · ALEXUYS · FREELANCE',1)
        text=re.sub(r'<title>.*?</title>','<title>Александр Александров — фриланс-разработчик | Alexuys</title>',text,count=1,flags=re.S)
        text=re.sub(r'(<meta\s+content=")[^"]*("\s+property="og:title"\s*/?>)',r'\1Александр Александров — фриланс-разработчик | Alexuys\2',text,count=1,flags=re.I)
        text=re.sub(r'(<meta\s+content=")[^"]*("\s+name="twitter:title"\s*/?>)',r'\1Александр Александров — фриланс-разработчик | Alexuys\2',text,count=1,flags=re.I)
    p.write_text(text,encoding='utf8')

after=hashlib.sha256(home.read_bytes()).hexdigest()
if before!=after: raise SystemExit('stage53 invariant failed: homepage changed')
print('stage53 entity authority:',count,'non-home pages; homepage unchanged')
