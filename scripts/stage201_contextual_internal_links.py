#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'

# Donor -> [(target, anchor)]. Every edge is task-adjacent; no global keyword cloud.
EDGES={
 'ai-automation':[
  ('/automation-services/','Автоматизация бизнеса ↗'),
  ('/python-development/','Python для AI-интеграций ↗'),
 ],
 '1c-integration':[
  ('/automation-services/','Автоматизация бизнес-процессов ↗'),
  ('/bitrix-development/','1С-Битрикс и интеграции ↗'),
 ],
 'excel-google-sheets-automation':[
  ('/automation-services/','Автоматизация бизнеса ↗'),
 ],
 'automation-services':[
  ('/marketplace-integration/','Автоматизация маркетплейсов ↗'),
 ],
 'crm-integration':[
  ('/marketplace-integration/','CRM и маркетплейсы ↗'),
 ],
 'api-development':[
  ('/python-development/','Python-разработка ↗'),
 ],
 'web-scraping-parsers':[
  ('/python-development/','Python-разработка ↗'),
 ],
 'site-repair':[
  ('/bitrix-development/','Доработка 1С-Битрикс ↗'),
 ],
 'ecommerce-development':[
  ('/bitrix-development/','Интернет-магазин на 1С-Битрикс ↗'),
  ('/telegram-mini-apps/','Магазин в Telegram Mini App ↗'),
 ],
 'app-development':[
  ('/telegram-mini-apps/','Telegram Mini App ↗'),
 ],
 'personal-cabinet-development':[
  ('/telegram-mini-apps/','Личный кабинет в Telegram Mini App ↗'),
 ],
}

changed=[]; added=0

def inject(slug:str, edges:list[tuple[str,str]]):
 global added
 p=ROOT/slug/'index.html'
 if not p.is_file(): raise SystemExit(f'stage201 missing donor: {slug}')
 s=p.read_text(encoding='utf-8')
 pending=[(href,label) for href,label in edges if f'href="{href}"' not in s]
 if not pending: return
 links=''.join(f'<a data-stage201-authority="true" href="{href}">{label}</a>' for href,label in pending)
 # Prefer the compact related-services nav when one already exists.
 m=re.search(r'(<nav class="secondary-demand__links"[^>]*>)(.*?)(</nav>)',s,re.I|re.S)
 if m:
  s=s[:m.start()]+m.group(1)+m.group(2)+links+m.group(3)+s[m.end():]
 else:
  # Otherwise place the same compact nav immediately after the existing related-cards block.
  m=re.search(r'(<div class="p129-related-grid[^>]*>.*?</div>)',s,re.I|re.S)
  if not m: raise SystemExit(f'stage201 no related container: {slug}')
  nav=f'<nav class="secondary-demand__links" data-stage201-authority="true" aria-label="Связанные направления">{links}</nav>'
  s=s[:m.end()]+nav+s[m.end():]
 p.write_text(s,encoding='utf-8')
 changed.append('/'+slug+'/'); added+=len(pending)

for slug,edges in EDGES.items(): inject(slug,edges)

for name in ('sitemap.xml','sitemap-google.xml'):
 p=ROOT/name
 if not p.exists(): continue
 s=p.read_text(encoding='utf-8')
 for route in changed:
  s=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',s,count=1)
 p.write_text(s,encoding='utf-8')

# Guards: every intended edge must exist after the stage; don't require duplicate injections.
for slug,edges in EDGES.items():
 s=(ROOT/slug/'index.html').read_text(encoding='utf-8')
 for href,_ in edges:
  if f'href="{href}"' not in s: raise SystemExit(f'stage201 guard failed {slug} -> {href}')
print(f'stage201 contextual authority: donor_pages={len(changed)}, links_added={added}')
