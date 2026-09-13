#!/usr/bin/env python3
from pathlib import Path
import hashlib,re,subprocess,sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BUNDLE=ROOT/'assets'/'stage105-final-ui.css'
CSS=ROOT/'assets'/'stage134-experimental-web.css'
JS=ROOT/'assets'/'stage134-experimental-web.js'

for p in (BUNDLE,CSS,JS):
    if not p.is_file(): raise SystemExit(f'stage134: missing {p}')

bundle=BUNDLE.read_text(encoding='utf-8')
css=CSS.read_text(encoding='utf-8').strip()
if '/* stage134-experimental-web */' not in css: raise SystemExit('stage134: css marker missing')
if '/* stage134-experimental-web */' not in bundle:
    bundle=bundle.rstrip()+'\n\n'+css+'\n'
BUNDLE.write_text(bundle,encoding='utf-8')
subprocess.run(['node','--check',str(JS)],check=True)
css_digest=hashlib.sha256(BUNDLE.read_bytes()).hexdigest()[:12]
js_digest=hashlib.sha256(JS.read_bytes()).hexdigest()[:12]

changed=0
for path in sorted(ROOT.rglob('*.html')):
    html=path.read_text(encoding='utf-8',errors='ignore')
    if 'data-wow="true"' not in html: continue
    html=re.sub(r'<body\b([^>]*)>',lambda m:'<body'+re.sub(r'\sdata-x134="[^"]*"','',m.group(1))+' data-x134="true">',html,count=1,flags=re.I)
    html=re.sub(r'(/assets/stage105-final-ui\.css)\?v=[^\"\']+',rf'\1?v={css_digest}',html,flags=re.I)
    html=re.sub(r'<script\b[^>]*stage134-experimental-web\.js[^>]*></script>','',html,flags=re.I)
    tag=f'<script defer src="/assets/stage134-experimental-web.js?v={js_digest}"></script>'
    if '</body>' not in html: raise SystemExit(f'stage134: body close missing {path}')
    html=html.replace('</body>',tag+'</body>',1)
    path.write_text(html,encoding='utf-8')
    changed+=1

if changed<30: raise SystemExit(f'stage134: expected >=30 wow pages, got {changed}')
print(f'stage134 experimental web: pages={changed}; css={css_digest}; js={js_digest}; WebGL + view transitions + scroll timelines enabled')
