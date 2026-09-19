#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'guides/index.html'
if not p.is_file():raise SystemExit('stage225 guides missing')
s=p.read_text(encoding='utf8')
s=re.sub(r'\s*<link[^>]+stage225-guides-path\.css[^>]*>','',s,flags=re.I)
if '</head>' not in s:raise SystemExit('stage225 head missing')
s=s.replace('</head>','<link rel="stylesheet" href="/assets/stage225-guides-path.css"></head>',1)
p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
for gid,count in [('decision-cost','2'),('decision-format','2'),('decision-architecture','3'),('decision-start','1'),('decision-repair','1')]:
 if f'id="{gid}"' not in f or f'data-count="{count}"' not in f:raise SystemExit(f'stage225 decision guard {gid}')
if f.count('class="p223-guide"')!=9:raise SystemExit(f'stage225 expected 9 guide routes, got {f.count("class=\"p223-guide\"")}')
if f.count('stage225-guides-path.css')!=1:raise SystemExit('stage225 stylesheet guard')
print('stage225 guides path: lanes=5, guides=9, existing decision-library preserved')
