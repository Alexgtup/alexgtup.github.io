#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
home=root/'index.html'; before=hashlib.sha256(home.read_bytes()).hexdigest()
slugs=('n8n-vs-backend','site-vs-web-app','repair-vs-rewrite')
for slug in slugs:
    p=root/'guides'/slug/'index.html'
    if not p.is_file(): raise SystemExit(f'stage55 missing {p}')
    t=p.read_text(encoding='utf8')
    old='<a href="/guides/">Гайды</a><a class="cta"'
    new='<a href="/guides/">Гайды</a><a href="/about/">Обо мне</a><a class="cta"'
    if old in t: t=t.replace(old,new,1)
    footer='© Alexuys · Александр Александров · <a href="/guides/">Все гайды</a>'
    fixed='© Alexuys · Александр Александров · <a href="/services/">Услуги</a> · <a href="/cases/">Кейсы</a> · <a href="/about/">Обо мне</a> · <a href="/privacy/">Конфиденциальность</a> · <a href="/guides/">Все гайды</a>'
    if footer in t: t=t.replace(footer,fixed,1)
    p.write_text(t,encoding='utf8')
if hashlib.sha256(home.read_bytes()).hexdigest()!=before: raise SystemExit('stage55 invariant failed: homepage changed')
print('stage55: decision guide shell normalized; homepage unchanged')
