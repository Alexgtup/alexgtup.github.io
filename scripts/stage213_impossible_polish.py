#!/usr/bin/env python3
from pathlib import Path
import hashlib,re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
PAGES=['/','/services/','/cases/','/about/','/freelance-developer/','/telegram-bots/','/telegram-bot-repair/','/wordpress-development/','/n8n-automation/','/web-development/','/project-repair/','/cases/fin-planner/','/cases/wordpress-commercial/','/cases/portfolio-site/','/cases/seo-control-center/']
css=ROOT/'assets/stage213-impossible-polish.css';js=ROOT/'assets/stage213-impossible-polish.js'
if not css.is_file() or not js.is_file():raise SystemExit('stage213 assets missing')
jsv=hashlib.sha256(js.read_bytes()).hexdigest()[:12]
changed=0
for route in PAGES:
 p=ROOT/('index.html' if route=='/' else route.strip('/')+'/index.html')
 if not p.is_file():raise SystemExit(f'stage213 missing page {route}')
 s=p.read_text(encoding='utf8')
 s=re.sub(r'\s*<link[^>]+stage213-impossible-polish\.css[^>]*>','',s,flags=re.I)
 s=re.sub(r'\s*<script[^>]+stage213-impossible-polish\.js[^>]*></script>','',s,flags=re.I)
 s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+(m.group(1) if 'data-stage213=' in m.group(1) else m.group(1)+' data-stage213="true"')+'>',s,count=1,flags=re.I)
 if n!=1:raise SystemExit(f'stage213 body missing {route}')
 if '</head>' not in s or '</body>' not in s:raise SystemExit(f'stage213 shell missing {route}')
 s=s.replace('</head>','<link rel="stylesheet" href="/assets/stage213-impossible-polish.css"></head>',1)
 s=s.replace('</body>',f'<script defer src="/assets/stage213-impossible-polish.js?v={jsv}"></script></body>',1)
 p.write_text(s,encoding='utf8');changed+=1
for route in PAGES:
 p=ROOT/('index.html' if route=='/' else route.strip('/')+'/index.html');s=p.read_text(encoding='utf8')
 if s.count('data-stage213="true"')!=1 or s.count('stage213-impossible-polish.css')!=1 or s.count('stage213-impossible-polish.js')!=1:raise SystemExit(f'stage213 guard {route}')
print(f'stage213 impossible polish: pages={changed}, reactive-depth=desktop, mobile=safe, js={jsv}')
