#!/usr/bin/env python3
from pathlib import Path
import re,sys,html,subprocess
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
CASES={
'/cases/fin-planner/':('TELEGRAM PRODUCT','/assets/cases/fin-planner/fin-planner-original-800w.webp','800','605','FIN PLANNER'),
'/cases/swift-calendar/':('iOS PRODUCT','/assets/cases/swift-calendar/calendar-original-800w.webp','800','551','SWIFT CALENDAR'),
'/cases/sheetpilot-ai/':('WEB PRODUCT','/assets/cases/sheetpilot-ai/sheetpilot-live-01.webp','1600','1000','SHEETPILOT AI'),
'/cases/seo-control-center/':('SEO / INTERNAL TOOL','/assets/cases/seo-control-center/seo-control-center-live-01.webp','1600','1000','SEO CONTROL CENTER'),
'/cases/auto-crm/':('CRM / INTERNAL SYSTEM','/assets/cases/auto-crm/auto-crm-real-01.webp','1280','502','AUTO CRM'),
'/cases/factory-catalog/':('B2B / WEB','/assets/cases/factory-catalog/factory-catalog-real-01.webp','1345','841','FACTORY CATALOG'),
'/cases/taxi-app/':('MOBILE PRODUCT','/assets/cases/taxi-app/taxi-app-real-01.webp','684','927','TAXI APP'),
'/cases/siteaudit-studio/':('WEB TOOL','/assets/cases/siteaudit-studio/siteaudit-live-01.webp','1600','1000','SITEAUDIT STUDIO'),
'/cases/freelance-os/':('PRODUCTIVITY PRODUCT','/assets/cases/freelance-os/freelance-os-live-01.webp','1600','1000','FREELANCE OS'),
}

def page(route): return ROOT/route.strip('/')/'index.html'
def tag_text(s): return re.sub(r'<[^>]+>','',s).strip()

def extract_main(src):
 m=re.search(r'<main\b([^>]*)>(.*?)</main>',src,re.S|re.I)
 if not m: raise SystemExit('stage132: main missing')
 return m

def first_section(inner):
 m=re.search(r'<section\b[^>]*>.*?</section>',inner,re.S|re.I)
 if not m: raise SystemExit('stage132: hero section missing')
 return m

def add_panel_classes(rest):
 def repl(m):
  attrs=m.group(1)
  cm=re.search(r'class="([^"]*)"',attrs,re.I)
  if cm:
   classes=cm.group(1).split()
   if 'p132-panel' not in classes: classes.append('p132-panel')
   if ('contact' in classes or 'stage108-endcap' in classes) and 'p132-end' not in classes: classes.append('p132-end')
   attrs=attrs[:cm.start(1)]+' '.join(classes)+attrs[cm.end(1):]
  else:
   attrs=attrs+' class="p132-panel"'
  return '<section'+attrs+'>'
 return re.sub(r'<section\b([^>]*)>',repl,rest,flags=re.I)

changed=[]
for route,(kicker,img,w,h,label) in CASES.items():
 f=page(route)
 if not f.is_file(): raise SystemExit(f'stage132: missing {route}')
 src=f.read_text(encoding='utf-8')
 mm=extract_main(src); inner=mm.group(2); hero=first_section(inner)
 hero_html=hero.group(0)
 hm=re.search(r'<h1\b[^>]*>(.*?)</h1>',hero_html,re.S|re.I)
 if not hm: raise SystemExit(f'stage132: h1 missing {route}')
 title=hm.group(1).strip()
 pm=re.search(r'<p\b[^>]*class="[^"]*(?:lead|s51-lead)[^"]*"[^>]*>(.*?)</p>',hero_html,re.S|re.I)
 if not pm: pm=re.search(r'<p\b[^>]*>(.*?)</p>',hero_html,re.S|re.I)
 lead=pm.group(1).strip() if pm else 'Подробный разбор задачи, интерфейса и реализованного результата.'
 rest=inner[:hero.start()]+inner[hero.end():]
 rest=add_panel_classes(rest)
 if img:
  visual=f'<div class="p132-cover-visual"><img src="{img}" width="{w}" height="{h}" alt="{html.escape(label)}" loading="eager" decoding="async"><span class="p132-cover-tag">{html.escape(label)} / REAL INTERFACE</span></div>'
 else:
  visual=f'<div class="p132-cover-visual"><div class="p132-cover-graphic"><strong>{len(changed)+1:02d}</strong><span>{html.escape(label)}</span></div></div>'
 cover=f'''<section class="p132-cover"><div class="p132-shell p132-cover-grid"><div class="p132-cover-copy"><p class="p132-eyebrow">CASE / {html.escape(kicker)}</p><h1>{title}</h1><p>{lead}</p><div class="p132-cover-actions"><a class="p132-primary" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Обсудить похожую задачу ↗</a><a class="p132-back" href="/cases/">Все кейсы</a></div></div>{visual}</div></section>'''
 new_main=f'<main id="main-content" class="p132-case" data-stage132-case="true">{cover}{rest}</main>'
 src=src[:mm.start()]+new_main+src[mm.end():]
 f.write_text(src,encoding='utf-8'); changed.append(route)
print(f'stage132 case rebuild: {len(changed)} detailed cases moved to editorial cover + story system')

subprocess.run(
 [sys.executable,str(Path(__file__).with_name('stage133_cinematic_system.py')),str(ROOT)],
 check=True,
)
