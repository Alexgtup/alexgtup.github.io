#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=ROOT/'cases/index.html'
if not p.is_file(): raise SystemExit('stage227 cases missing')
s=p.read_text(encoding='utf8')
FEATURED={'/cases/wordpress-commercial/','/cases/fin-planner/','/cases/marketplace-monitor/','/cases/portfolio-site/'}
MAP={
'/cases/marketplace-monitor/':('/assets/cases/marketplace-monitor/marketplace-monitor-01.webp','/assets/cases/marketplace-monitor/marketplace-monitor-01-800w.webp',1448),
'/cases/ozon-scanner/':('/assets/cases/ozon-scanner/ozon-scanner-01.webp','/assets/cases/ozon-scanner/ozon-scanner-01-800w.webp',1448),
'/cases/wordpress-commercial/':('/assets/cases/wordpress-commercial/wordpress-commercial-01.webp','/assets/cases/wordpress-commercial/wordpress-commercial-01-800w.webp',1045),
'/cases/portfolio-site/':('/assets/cases/portfolio-site/portfolio-site-01.webp','/assets/cases/portfolio-site/portfolio-site-01-800w.webp',1600),
'/cases/sheetpilot-ai/':('/assets/cases/sheetpilot-ai/sheetpilot-live-01.webp','/assets/cases/sheetpilot-ai/sheetpilot-live-01-800w.webp',1600),
'/cases/seo-control-center/':('/assets/cases/seo-control-center/seo-control-center-live-01.webp','/assets/cases/seo-control-center/seo-control-center-live-01-800w.webp',1600),
'/cases/auto-crm/':('/assets/cases/auto-crm/auto-crm-real-01.webp','/assets/cases/auto-crm/auto-crm-real-01-800w.webp',1280),
'/cases/factory-catalog/':('/assets/cases/factory-catalog/factory-catalog-real-01.webp','/assets/cases/factory-catalog/factory-catalog-real-01-800w.webp',1345),
'/cases/siteaudit-studio/':('/assets/cases/siteaudit-studio/siteaudit-live-01.webp','/assets/cases/siteaudit-studio/siteaudit-live-01-800w.webp',1600),
'/cases/freelance-os/':('/assets/cases/freelance-os/freelance-os-live-01.webp','/assets/cases/freelance-os/freelance-os-live-01-800w.webp',1600),
}

def patch_anchor(route,src,small,orig_w):
 global s
 pat=re.compile(r'<a\b(?=[^>]*href="'+re.escape(route)+r'")[^>]*>.*?</a>',re.S|re.I)
 m=pat.search(s)
 if not m: raise SystemExit(f'stage227 route missing {route}')
 block=m.group(0)
 ipat=re.compile(r'<img\b(?=[^>]*src="'+re.escape(src)+r'")[^>]*>',re.I)
 im=ipat.search(block)
 if not im: raise SystemExit(f'stage227 image missing {route} {src}')
 tag=im.group(0)
 tag=re.sub(r'\s+(?:srcset|sizes)="[^"]*"','',tag,flags=re.I)
 sizes='(max-width: 700px) calc(100vw - 24px), (max-width: 1000px) calc(50vw - 22px), '+('58vw' if route in FEATURED else '33vw')
 tag=tag[:-1]+f' srcset="{small} 800w, {src} {orig_w}w" sizes="{sizes}">'
 block=block[:im.start()]+tag+block[im.end():]
 s=s[:m.start()]+block+s[m.end():]

for route,(src,small,w) in MAP.items():
 patch_anchor(route,src,small,w)

p.write_text(s,encoding='utf8')
f=p.read_text(encoding='utf8')
if f.count('srcset=') < len(MAP): raise SystemExit('stage227 srcset count')
for route,(src,small,w) in MAP.items():
 if f'{small} 800w' not in f: raise SystemExit(f'stage227 srcset guard {route}')
 asset=ROOT/small.lstrip('/')
 if not asset.is_file(): raise SystemExit(f'stage227 derivative missing {asset}')
# Preserve canonical case set and Stage214 curation.
if len(set(re.findall(r'href="(/cases/[^\"]+/)"',f))) < 13: raise SystemExit('stage227 case route guard')
if f.count('data-stage214-featured=') != 4: raise SystemExit('stage227 Stage214 featured guard')
print(f'stage227 cases responsive media: patched={len(MAP)}, featured={len(FEATURED)}, original fallbacks retained')
