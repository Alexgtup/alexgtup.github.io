#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-18'
changed=[]

def read(slug):
 p=ROOT/slug/'index.html'
 if not p.is_file(): raise SystemExit(f'stage197: missing {slug}')
 return p,p.read_text(encoding='utf-8')

def write(p,s,slug):
 p.write_text(s,encoding='utf-8');changed.append('/'+slug+'/')

# 1) Services hub: expose two high-demand concrete tasks without replacing the broad architecture.
p,s=read('services')
if 'data-stage197-authority="services"' not in s:
 m=re.search(r'(<nav class="stage174-popular__links"[^>]*>)(.*?)(</nav>)',s,re.I|re.S)
 if not m: raise SystemExit('stage197: services popular links missing')
 extra=('<a data-stage197-authority="services" href="/ai-chatbot-development/"><strong>Разработать ИИ-агента</strong><span>Открыть ↗</span></a>'
        '<a data-stage197-authority="services" href="/ecommerce-development/"><strong>Сделать интернет-магазин</strong><span>Открыть ↗</span></a>')
 s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
write(p,s,'services')

# 2) API integrations -> API development. Distinct intent, but tightly related and useful for users.
p,s=read('api-integrations')
if 'data-stage197-authority="api-development"' not in s:
 # Prefer existing related-material nav.
 patterns=[
  r'(<nav class="x146-depth__links"[^>]*>)(.*?)(</nav>)',
  r'(<div class="search-demand__links">)(.*?)(</div>)',
  r'(<div class="p131-bridge__inner">)(.*?)(</div>)',
 ]
 m=None
 for pat in patterns:
  m=re.search(pat,s,re.I|re.S)
  if m: break
 if not m: raise SystemExit('stage197: api-integrations link container missing')
 extra='<a data-stage197-authority="api-development" href="/api-development/">Разработка REST API ↗</a>'
 s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
write(p,s,'api-integrations')

# 3) General development -> native iOS. The hub already points at mobile development; add the exact native route once.
p,s=read('development')
if 'data-stage197-authority="ios-development"' not in s:
 # Add to the existing PRODUCTS task-map nav, next to product routes.
 m=re.search(r'(<article class="stage172-task-map__group"><p>01 / PRODUCTS</p>.*?<nav[^>]*>)(.*?)(</nav>)',s,re.I|re.S)
 if not m: raise SystemExit('stage197: development products nav missing')
 extra='<a data-stage197-authority="ios-development" href="/ios-development/"><strong>iOS / Swift</strong><span>Нативное приложение</span><b>↗</b></a>'
 s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
write(p,s,'development')

# 4) n8n page -> broad automation service for users whose task no longer fits one workflow tool.
p,s=read('n8n-automation')
if 'data-stage197-authority="automation-services"' not in s:
 patterns=[
  r'(<nav class="secondary-demand__links"[^>]*>)(.*?)(</nav>)',
  r'(<div class="p131-bridge__inner">)(.*?)(</div>)',
  r'(<nav class="x146-depth__links"[^>]*>)(.*?)(</nav>)',
 ]
 m=None
 for pat in patterns:
  m=re.search(pat,s,re.I|re.S)
  if m: break
 if not m: raise SystemExit('stage197: n8n link container missing')
 extra='<a data-stage197-authority="automation-services" href="/automation-services/">Автоматизация бизнеса ↗</a>'
 s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
write(p,s,'n8n-automation')

# 5) App development -> API development, because mobile apps often require an API rather than only an integration.
p,s=read('app-development')
if 'data-stage197-authority="app-api"' not in s:
 m=re.search(r'(<nav class="secondary-demand__links"[^>]*>)(.*?)(</nav>)',s,re.I|re.S)
 if not m: raise SystemExit('stage197: app secondary links missing')
 extra='<a data-stage197-authority="app-api" href="/api-development/">API для приложения ↗</a>'
 s=s[:m.start()]+m.group(1)+m.group(2)+extra+m.group(3)+s[m.end():]
write(p,s,'app-development')

# Refresh discovery dates only for pages materially changed in this pass.
for name in ('sitemap.xml','sitemap-google.xml'):
 sp=ROOT/name
 if not sp.exists(): continue
 text=sp.read_text(encoding='utf-8')
 for route in changed:
  text=re.sub(r'(<loc>'+re.escape(BASE+route)+r'</loc><lastmod>)[^<]+',rf'\g<1>{TODAY}',text,count=1)
 sp.write_text(text,encoding='utf-8')

checks={
 'services':['data-stage197-authority="services"','href="/ai-chatbot-development/"','href="/ecommerce-development/"'],
 'api-integrations':['data-stage197-authority="api-development"','href="/api-development/"'],
 'development':['data-stage197-authority="ios-development"','href="/ios-development/"'],
 'n8n-automation':['data-stage197-authority="automation-services"','href="/automation-services/"'],
 'app-development':['data-stage197-authority="app-api"','href="/api-development/"'],
}
for slug,needles in checks.items():
 s=(ROOT/slug/'index.html').read_text(encoding='utf-8')
 for needle in needles:
  if needle not in s: raise SystemExit(f'stage197 guard failed {slug}: {needle}')
print(f'stage197 internal authority: pages={len(changed)}, links=6')
