#!/usr/bin/env python3
from pathlib import Path
import hashlib,re,subprocess,sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BUNDLE=ROOT/'assets'/'stage105-final-ui.css'
CSS=ROOT/'assets'/'stage135-world-system.css'
QA=ROOT/'assets'/'stage136-visual-qa.css'
SAFE=ROOT/'assets'/'stage137-motion-failsafe.css'
JS=ROOT/'assets'/'stage135-world-system.js'
for p in (BUNDLE,CSS,QA,SAFE,JS):
    if not p.is_file(): raise SystemExit(f'stage135: missing {p}')

bundle=BUNDLE.read_text(encoding='utf-8')
for source,marker in (
    (CSS,'/* stage135-world-system */'),
    (QA,'/* stage136-visual-qa */'),
    (SAFE,'/* stage137-motion-failsafe */'),
):
    css=source.read_text(encoding='utf-8').strip()
    if marker not in css: raise SystemExit(f'stage135: marker missing in {source.name}')
    if marker not in bundle:
        bundle=bundle.rstrip()+'\n\n'+css+'\n'
BUNDLE.write_text(bundle,encoding='utf-8')
subprocess.run(['node','--check',str(JS)],check=True)
css_digest=hashlib.sha256(BUNDLE.read_bytes()).hexdigest()[:12]
js_digest=hashlib.sha256(JS.read_bytes()).hexdigest()[:12]

changed=0; families={}
for path in sorted(ROOT.rglob('*.html')):
    html=path.read_text(encoding='utf-8',errors='ignore')
    if '<body' not in html or '<main' not in html: continue
    rel=path.relative_to(ROOT).as_posix()
    if rel in {'404.html','google4d4487812e36d65c.html','yandex_d89618159a40495b.html','yandex_e868ce83ed0c1276.html'}: continue
    bodym=re.search(r'<body\b([^>]*)>',html,re.I)
    attrs=bodym.group(1) if bodym else ''
    famm=re.search(r'data-ux-family="([^"]+)"',attrs,re.I)
    ux=famm.group(1) if famm else ''
    if rel.startswith('en/'):
        family='international'
    elif ux=='guide': family='guide'
    elif ux=='tool': family='tool'
    elif ux=='product': family='product'
    elif rel=='demos/index.html': family='demo'
    elif 'data-wow="true"' in attrs: family='cinematic'
    elif ux in {'home','service','case','hub'}: family='cinematic'
    else: family='core'
    attrs=re.sub(r'\sdata-x135="[^"]*"','',attrs)
    attrs=re.sub(r'\sdata-x135-family="[^"]*"','',attrs)
    newbody=f'<body{attrs} data-x135="true" data-x135-family="{family}">'
    html=html[:bodym.start()]+newbody+html[bodym.end():]
    html=re.sub(r'(/assets/stage105-final-ui\.css)\?v=[^\"\']+',rf'\1?v={css_digest}',html,flags=re.I)
    html=re.sub(r'<script\b[^>]*stage135-world-system\.js[^>]*></script>','',html,flags=re.I)
    tag=f'<script defer src="/assets/stage135-world-system.js?v={js_digest}"></script>'
    if '</body>' not in html: raise SystemExit(f'stage135: closing body missing {rel}')
    html=html.replace('</body>',tag+'</body>',1)
    path.write_text(html,encoding='utf-8')
    changed+=1; families[family]=families.get(family,0)+1

if changed<70: raise SystemExit(f'stage135: expected >=70 pages, got {changed}')
for needed in ('guide','tool','international','cinematic'):
    if families.get(needed,0)==0: raise SystemExit(f'stage135: family missing: {needed}')
final_bundle=BUNDLE.read_text(encoding='utf-8')
for marker in ('/* stage136-visual-qa */','/* stage137-motion-failsafe */'):
    if marker not in final_bundle: raise SystemExit(f'stage135: final layer missing: {marker}')
print(f'stage135 world system: pages={changed}; families={families}; css={css_digest}; js={js_digest}; stage136 QA + stage137 motion fail-safe')
