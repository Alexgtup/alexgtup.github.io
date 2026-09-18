#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html,re,sys,xml.etree.ElementTree as ET
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'; TODAY='2026-09-19'
CASES=[
('/cases/marketplace-monitor/','Автоматизация маркетплейсов: цены, остатки и история','Ozon, Wildberries и Яндекс Маркет в одном контуре мониторинга.','/assets/cases/marketplace-monitor/marketplace-monitor-01.webp'),
('/cases/ozon-scanner/','Ozon: склад, сканер штрихкодов и Excel','Сканирование запускает упаковку, операции, остатки и подготовку отгрузки.','/assets/cases/ozon-scanner/ozon-scanner-01.webp'),
('/cases/wordpress-commercial/','Доработка коммерческого WordPress-сайта','Страницы, формы, калькуляторы, адаптив и меню без переписывания темы.','/assets/cases/wordpress-commercial/wordpress-commercial-01.webp'),
('/cases/portfolio-site/','Многостраничный сайт-портфолио Alexuys','Услуги, кейсы, адаптив, SEO, schema и внутренняя перелинковка.','/assets/cases/portfolio-site/portfolio-site-01.webp'),
]
IMAGE_DIMS={
'/assets/cases/marketplace-monitor/marketplace-monitor-01.webp':(1448,1086),
'/assets/cases/ozon-scanner/ozon-scanner-01.webp':(1448,1086),
'/assets/cases/wordpress-commercial/wordpress-commercial-01.webp':(1045,950),
'/assets/cases/portfolio-site/portfolio-site-01.webp':(1600,1200),
}
for route,_,_,image in CASES:
 p=ROOT/route.strip('/')/'index.html'
 if not p.is_file(): raise SystemExit(f'stage205 missing case: {p}')
 if not (ROOT/image.lstrip('/')).is_file(): raise SystemExit(f'stage205 missing image: {image}')

STYLE='''<style id="stage205-case-proof-style">.s205-proof{padding:clamp(3.5rem,7vw,6rem) 0;border-top:1px solid rgba(255,255,255,.07)}.s205-proof__head{margin-bottom:1.2rem}.s205-proof__head small{font:800 .63rem/1.2 ui-monospace,monospace;letter-spacing:.08em;color:#7d8790}.s205-proof__head h2{margin:.65rem 0 0;max-width:16ch;font-size:clamp(2rem,4vw,4rem);line-height:.98;letter-spacing:-.05em}.s205-proof__grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem}.s205-proof__card{display:grid;grid-template-columns:8rem 1fr;gap:1rem;align-items:center;padding:.65rem;border:1px solid rgba(255,255,255,.11);border-radius:1rem;background:#0d1217;text-decoration:none}.s205-proof__card img{display:block;width:100%;height:6rem;object-fit:cover;border-radius:.72rem}.s205-proof__card strong{display:block;line-height:1.15}.s205-proof__card span{display:block;margin-top:.45rem;color:#8f99a2;font-size:.78rem;line-height:1.5}@media(max-width:720px){.s205-proof__grid{grid-template-columns:1fr}.s205-proof__card{grid-template-columns:6.5rem 1fr}.s205-proof__card img{height:5.2rem}}</style>'''
PROOF={
 'marketplace-integration/index.html':[CASES[0],CASES[1]],
 'excel-google-sheets-automation/index.html':[CASES[1],CASES[0]],
 'wordpress-development/index.html':[CASES[2]],
 'site-repair/index.html':[CASES[2]],
 'web-development/index.html':[CASES[3]],
 'freelance-developer/index.html':[CASES[3]],
}
changed=[]
for rel,items in PROOF.items():
 p=ROOT/rel
 if not p.is_file(): continue
 s=p.read_text(encoding='utf-8')
 if 'stage205-case-proof-style' not in s:s=s.replace('</head>',STYLE+'</head>',1)
 if 'data-stage205-case-proof' not in s:
  cards=''.join(f'<a class="s205-proof__card" href="{route}"><img src="{img}" width="{IMAGE_DIMS[img][0]}" height="{IMAGE_DIMS[img][1]}" loading="lazy" decoding="async" alt="{html.escape(title,quote=True)}"/><div><strong>{html.escape(title)}</strong><span>{html.escape(desc)}</span></div></a>' for route,title,desc,img in items)
  block=f'<section class="s205-proof" data-stage205-case-proof="true"><div class="container"><div class="s205-proof__head"><small>РЕАЛЬНЫЕ КЕЙСЫ</small><h2>Похожая задача уже была в работе.</h2></div><div class="s205-proof__grid">{cards}</div></div></section>'
  if '</main>' not in s: raise SystemExit(f'stage205 no main close: {rel}')
  s=s.replace('</main>',block+'</main>',1)
 p.write_text(s,encoding='utf-8');changed.append('/'+rel.replace('index.html',''))

# Broaden case hub metadata after stage93 has rebuilt the library.
p=ROOT/'cases/index.html'
s=p.read_text(encoding='utf-8')
title='Кейсы разработки — сайты, автоматизация, маркетплейсы, WordPress и AI | Alexuys'
desc='Реальные кейсы: автоматизация Ozon, Wildberries и Яндекс Маркета, WordPress, AI, CRM, SEO-сервисы, Telegram, iOS и B2B-разработка. Задача, решение, результат и реальные скриншоты.'
s=re.sub(r'<title[^>]*>.*?</title>',f'<title>{title}</title>',s,count=1,flags=re.I|re.S)
for attr,key,val in [('name','description',desc),('property','og:title',title),('property','og:description',desc),('name','twitter:title',title),('name','twitter:description',desc)]:
 pat=rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
 repl=f'<meta {attr}="{key}" content="{html.escape(val,quote=True)}"/>'
 if re.search(pat,s,re.I):s=re.sub(pat,repl,s,count=1,flags=re.I)
p.write_text(s,encoding='utf-8');changed.append('/cases/')

# Add the new case URLs to both XML sitemaps and keep sitemap.txt identical to canonical sitemap.xml.
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
for name in ('sitemap.xml','sitemap-google.xml'):
 sp=ROOT/name
 if not sp.exists():continue
 tree=ET.parse(sp);root=tree.getroot();ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
 existing={n.text.strip() for n in root.findall(f'.//{ns}loc') if n.text}
 for route,_,_,_ in CASES:
  url=BASE+route
  if url not in existing:
   u=ET.SubElement(root,ns+'url');ET.SubElement(u,ns+'loc').text=url;ET.SubElement(u,ns+'lastmod').text=TODAY
 tree.write(sp,encoding='utf-8',xml_declaration=True)
if (ROOT/'sitemap.xml').exists() and (ROOT/'sitemap.txt').exists():
 tree=ET.parse(ROOT/'sitemap.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
 urls=[n.text.strip() for n in tree.findall('.//s:loc',ns) if n.text and n.text.strip()]
 (ROOT/'sitemap.txt').write_text('\n'.join(urls)+'\n',encoding='utf-8')

# Guards.
hub=(ROOT/'cases/index.html').read_text(encoding='utf-8')
for route,_,_,_ in CASES:
 if f'href="{route}"' not in hub: raise SystemExit(f'stage205 hub missing {route}')
for rel in PROOF:
 if 'data-stage205-case-proof="true"' not in (ROOT/rel).read_text(encoding='utf-8'):raise SystemExit(f'stage205 proof missing {rel}')
print(f'stage205 freelance portfolio cases: cases={len(CASES)}, proof_pages={len(PROOF)}')
