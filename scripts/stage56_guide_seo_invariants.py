#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
home=root/'index.html'; before=hashlib.sha256(home.read_bytes()).hexdigest()
slugs=('n8n-vs-backend','site-vs-web-app','repair-vs-rewrite')
pat=re.compile(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',re.I|re.S)
for slug in slugs:
    p=root/'guides'/slug/'index.html'; t=p.read_text(encoding='utf8')
    marker='<meta name="twitter:card" content="summary_large_image">'
    dims='<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Alexuys — разбор выбора решения">'
    if 'property="og:image:width"' not in t: t=t.replace(marker,dims+marker,1)
    def repl(m):
        try:o=json.loads(m.group(2))
        except Exception:return m.group(0)
        if isinstance(o,dict) and o.get('@type')=='Article':
            o.setdefault('datePublished','2026-09-06');o.setdefault('dateModified','2026-09-06')
        return m.group(1)+json.dumps(o,ensure_ascii=False,separators=(',',':'))+m.group(3)
    t=pat.sub(repl,t)
    p.write_text(t,encoding='utf8')

def add_link(route,href,label):
    p=root/route.strip('/')/'index.html'
    if not p.is_file(): return
    t=p.read_text(encoding='utf8')
    if href in t:return
    # Prefer existing related-link grids; otherwise add before the closing main.
    for marker in ('<div class="s48-related">','<div class="related">'):
        i=t.find(marker)
        if i>=0:
            i+=len(marker);t=t[:i]+f'<a href="{href}"><strong>{label}</strong><span>Практический разбор →</span></a>'+t[i:];break
    else:
        t=t.replace('</main>',f'<section class="section"><div class="container"><p><a href="{href}">{label} →</a></p></div></section></main>',1)
    p.write_text(t,encoding='utf8')

add_link('/development/','/guides/repair-vs-rewrite/','Дорабатывать или переписывать проект')
add_link('/cases/auto-crm/','/guides/custom-crm-or-ready/','Своя CRM или готовое решение')
if hashlib.sha256(home.read_bytes()).hexdigest()!=before:raise SystemExit('stage56 invariant failed: homepage changed')
print('stage56: article metadata and contextual inbound links completed; homepage unchanged')
