#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'index.html'
if not p.is_file(): raise SystemExit('stage230 home missing')
s=p.read_text(encoding='utf8')
# idempotent cleanup
s=re.sub(r'\s*<link[^>]+stage230-reference-fidelity\.css[^>]*>','',s,flags=re.I)
s=re.sub(r'\sdata-stage230-home="true"','',s)
s=re.sub(r'\s*<div class="p230-(?:tower|columns|orbit)"[^>]*></div>','',s,flags=re.I)
s=re.sub(r'\s*<div class="p230-case-foot">.*?</div>','',s,flags=re.I|re.S)
s,n=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1)+' data-stage230-home="true">',s,count=1,flags=re.I)
if n!=1: raise SystemExit('stage230 body missing')
s=s.replace('</head>','<link rel="stylesheet" href="/assets/stage230-reference-fidelity.css"></head>',1)
# Reference hero has three proof metrics, not four.
proof='<div class="p128-proofbar" aria-label="Проверяемые факты"><a href="/cases/"><strong>13</strong><span>реальных кейсов</span></a><a href="/demos/"><strong>4</strong><span>публичных демо</span></a><a href="/tools/"><strong>6</strong><span>tools</span></a></div>'
s,n=re.subn(r'<div class="p128-proofbar"[^>]*>.*?</div>',proof,s,count=1,flags=re.S)
if n!=1: raise SystemExit('stage230 proofbar missing')
# Add sculptural connectors behind the existing five live panels.
anchor='<div class="p226-beam" aria-hidden="true"></div>'
insert='<div class="p230-columns" aria-hidden="true"></div><div class="p230-tower" aria-hidden="true"></div><div class="p230-orbit" aria-hidden="true"></div>'+anchor
if anchor not in s: raise SystemExit('stage230 hero anchor missing')
s=s.replace(anchor,insert,1)
# Add factual footers to the four real cases; no invented KPIs.
meta={
 '01':('CLIENT WORK','PRODUCTION'),
 '02':('TELEGRAM UI','FULL FLOW'),
 '03':('SEARCH DATA','MULTI-SITE'),
 '04':('XLSX INPUT','EXPORT'),
}
for rank,(a,b) in meta.items():
 pat=rf'(<article class="p128-feature p128-feature--portfolio[^>]*data-stage223-rank="{rank}"[^>]*>.*?<div class="p128-feature__copy">)(.*?)(</div></article>)'
 m=re.search(pat,s,re.S)
 if not m: raise SystemExit(f'stage230 case {rank} missing')
 body=m.group(2)
 foot=f'<div class="p230-case-foot"><span>{a}<b>REAL</b></span><span>{b}<b>VERIFIED</b></span></div>'
 body=body+foot
 block=m.group(1)+body+m.group(3)
 s=s[:m.start()]+block+s[m.end():]
p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
for needle in ['data-stage230-home="true"','stage230-reference-fidelity.css','p230-tower','p230-columns','p230-orbit','13</strong><span>реальных кейсов','4</strong><span>публичных демо','6</strong><span>tools']:
 if needle not in f: raise SystemExit(f'stage230 guard {needle}')
if f.count('p230-case-foot')!=4: raise SystemExit(f'stage230 case-foot count {f.count("p230-case-foot")}')
if f.count('stage230-reference-fidelity.css')!=1: raise SystemExit('stage230 duplicate stylesheet')
print('stage230 reference fidelity: continuous space scene, 3 hero metrics, integrated tower, 4-up real work, mountain capability landscape')
