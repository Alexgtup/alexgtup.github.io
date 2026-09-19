#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
STYLE='''<style id="stage218-hub-contrast-contract">
/* Stage218: final readable light-paper accents for the two primary portfolio hubs. */
body[data-stage218-hub-contrast="true"] .stage178-route-note{color:#171914!important}
body[data-stage218-hub-contrast="true"] .stage178-route-note strong{color:#171914!important}
body[data-stage218-hub-contrast="true"] main.p130-hub[data-stage130-hub="services"] .secondary-demand__card>span{color:#46543f!important}
body[data-stage218-hub-contrast="true"] main.p130-hub[data-stage130-hub="services"] .stage174-popular .stage174-head>p:first-child{color:#555e58!important}
body[data-stage218-hub-contrast="true"] main.p130-hub[data-stage130-hub="services"] .stage174-popular__links a>span{color:#596259!important}
</style>'''
for route in ['cases','services']:
 p=ROOT/route/'index.html'
 if not p.is_file():raise SystemExit(f'stage218 missing {route}')
 s=p.read_text(encoding='utf8')
 s=re.sub(r'\s*<style\b[^>]*id="stage218-hub-contrast-contract"[^>]*>.*?</style>','',s,flags=re.I|re.S)
 s=re.sub(r'\sdata-stage218-hub-contrast="true"','',s,count=1)
 s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage218-hub-contrast="true">',s,count=1,flags=re.I)
 if n!=1:raise SystemExit(f'stage218 body missing {route}')
 if '</head>' not in s:raise SystemExit(f'stage218 head missing {route}')
 s=s.replace('</head>',STYLE+'</head>',1)
 p.write_text(s,encoding='utf8')
# guards
for route in ['cases','services']:
 s=(ROOT/route/'index.html').read_text(encoding='utf8')
 if s.count('id="stage218-hub-contrast-contract"')!=1 or len(re.findall(r'<body\b[^>]*data-stage218-hub-contrast="true"',s,re.I))!=1:
  raise SystemExit(f'stage218 duplicate guard {route}')
 if 'stage178-route-note' not in s:raise SystemExit(f'stage218 route-note missing {route}')
print('stage218 hub contrast contract: /cases/ + /services/')
