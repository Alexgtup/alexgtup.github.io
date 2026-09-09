#!/usr/bin/env python3
from pathlib import Path
import hashlib, re, sys

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

    # Decision guides were generated before the shared page-family marker existed,
    # so they missed guide-wide mobile typography/rhythm fixes. Classify them once
    # at build time instead of maintaining a separate visual implementation.
    page_marker=f'guides--{slug}'
    body_match=re.search(r'<body\b([^>]*)>', t, flags=re.I)
    if not body_match: raise SystemExit(f'stage55 missing body: {p}')
    body_tag=body_match.group(0)
    if 'data-page=' not in body_tag:
        patched=body_tag[:-1] + f' data-page="{page_marker}">'
        t=t.replace(body_tag,patched,1)
    elif f'data-page="{page_marker}"' not in body_tag and f"data-page='{page_marker}'" not in body_tag:
        t=re.sub(r'data-page=["\'][^"\']+["\']', f'data-page="{page_marker}"', t, count=1, flags=re.I)

    p.write_text(t,encoding='utf8')

for slug in slugs:
    t=(root/'guides'/slug/'index.html').read_text(encoding='utf8')
    if f'data-page="guides--{slug}"' not in t:
        raise SystemExit(f'stage55 data-page invariant failed: {slug}')
if hashlib.sha256(home.read_bytes()).hexdigest()!=before: raise SystemExit('stage55 invariant failed: homepage changed')
print('stage55: decision guide shell + shared guide-family marker normalized; homepage unchanged')
