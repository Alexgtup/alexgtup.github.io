#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
REVIEWS=20; PROFESSIONALISM=9; COMMUNICATION=9
changed=0
for p in ROOT.rglob('*.html'):
    s=p.read_text(encoding='utf-8',errors='ignore');before=s
    # Normalize legacy proof cards without exposing complaint counts as a marketing metric.
    s=re.sub(r'<strong>(?:17|18|20) отзывов · \d+ претензий</strong>',f'<strong>{REVIEWS} отзывов в профиле</strong>',s)
    s=re.sub(r'<strong>(?:17|18|20) отзывов · (?:9|10)/10</strong>',f'<strong>{REVIEWS} отзывов · {PROFESSIONALISM}/10</strong>',s)
    s=re.sub(r'<strong>(?:17|18|20) отзывов</strong><span>в публичном профиле Freelance\.ru</span>',f'<strong>{REVIEWS} отзывов</strong><span>в публичном профиле Freelance.ru</span>',s)
    s=re.sub(r'<span>(?:9|10)/10 профессионализм · (?:9|10)/10 коммуникация(?: · публичный профиль Freelance\.ru)?</span>',lambda m: f'<span>{PROFESSIONALISM}/10 профессионализм · {COMMUNICATION}/10 коммуникация' + (' · публичный профиль Freelance.ru' if 'публичный профиль' in m.group(0) else '') + '</span>',s)
    # Plain-text variants used in older trust surfaces.
    s=s.replace('18 отзывов · 0 претензий',f'{REVIEWS} отзывов в профиле')
    s=s.replace('18 отзывов · 10/10',f'{REVIEWS} отзывов · {PROFESSIONALISM}/10')
    s=s.replace('18 отзывов',f'{REVIEWS} отзывов')
    s=s.replace('10/10 профессионализм',f'{PROFESSIONALISM}/10 профессионализм')
    if s!=before:p.write_text(s,encoding='utf-8');changed+=1

issues=[]
for p in ROOT.rglob('*.html'):
    s=p.read_text(encoding='utf-8',errors='ignore')
    for stale in ('18 отзывов','0 претензий','10/10 профессионализм'):
        if stale in s:issues.append(f'{p.relative_to(ROOT)} :: {stale}')
if issues:raise SystemExit('stage212 reputation consistency failed:\n'+'\n'.join(' - '+x for x in issues))
# Ensure current facts exist on representative independent-proof surfaces.
for rel in ('about/index.html','freelance-developer/index.html','telegram-bots/index.html','wordpress-development/index.html','n8n-automation/index.html'):
    p=ROOT/rel
    if not p.is_file() or '20 отзывов' not in p.read_text(encoding='utf-8',errors='ignore'):
        raise SystemExit(f'stage212 current reputation missing: {rel}')
print(f'stage212 reputation consistency: changed={changed}, reviews={REVIEWS}, professionalism={PROFESSIONALISM}, communication={COMMUNICATION}')
