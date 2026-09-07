#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys, xml.etree.ElementTree as ET

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
route='/cases/sheetpilot-ai/'
url='https://alexgtup.github.io'+route

STYLE='\n<style id="sheetpilot-promo-style">\n.sp-promo{padding:clamp(4rem,8vw,7rem) 0;border-top:1px solid rgba(255,255,255,.075);border-bottom:1px solid rgba(255,255,255,.075)}.sp-promo .container{width:min(100%,92rem);margin-inline:auto;padding-inline:clamp(1.1rem,4vw,4.5rem)}.sp-promo__head{display:flex;justify-content:space-between;gap:1rem;align-items:end;margin-bottom:1.3rem}.sp-promo__head span{color:#d4fe6a;font:800 .62rem/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.09em}.sp-promo__head a{color:#9da6ae;font-size:.75rem}.sp-promo__card{display:grid;grid-template-columns:minmax(0,.88fr) minmax(28rem,1.12fr);gap:clamp(1.2rem,4vw,3rem);align-items:center;padding:clamp(1rem,2vw,1.5rem);border:1px solid rgba(212,254,106,.18);border-radius:1.5rem;background:radial-gradient(circle at 90% 0,rgba(212,254,106,.09),transparent 26rem),linear-gradient(145deg,#11171d,#0b0f14);text-decoration:none;overflow:hidden}.sp-promo__copy{padding:clamp(.5rem,2vw,1.2rem)}.sp-promo__badge{display:inline-flex;padding:.42rem .6rem;border:1px solid rgba(212,254,106,.22);border-radius:999px;color:#d4fe6a;font:800 .61rem/1 ui-monospace,monospace}.sp-promo h2{margin:1rem 0 0;max-width:9ch;font-size:clamp(2.8rem,5.5vw,5.8rem);line-height:.92;letter-spacing:-.06em}.sp-promo h2 em{font-style:normal;color:#d4fe6a}.sp-promo p{max-width:39rem;margin:1rem 0 0;color:#929ca5;line-height:1.65}.sp-promo__meta{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:1.2rem}.sp-promo__meta i{font-style:normal;padding:.38rem .55rem;border:1px solid rgba(255,255,255,.095);border-radius:999px;color:#89949e;font-size:.65rem}.sp-promo__visual{border:1px solid rgba(255,255,255,.09);border-radius:1.1rem;background:#080b0f;padding:.35rem;overflow:hidden}.sp-promo__visual img{display:block;width:100%;height:auto;border-radius:.85rem}.sp-promo__arrow{display:inline-block;margin-top:1.35rem;color:#d4fe6a;font-weight:800;font-size:.78rem}@media(max-width:900px){.sp-promo__card{grid-template-columns:1fr}.sp-promo__visual{order:-1}.sp-promo h2{max-width:12ch}}@media(max-width:620px){.sp-promo__head{align-items:flex-start;flex-direction:column}.sp-promo{padding:3.7rem 0}.sp-promo__card{border-radius:1.15rem}}\n</style>\n'
PROMO='\n<section class="sp-promo" data-sheetpilot-promo="true"><div class="container"><div class="sp-promo__head"><span>НОВЫЙ КЕЙС · AI + EXCEL</span><a href="/cases/">Все проекты →</a></div><a class="sp-promo__card" href="/cases/sheetpilot-ai/"><div class="sp-promo__copy"><span class="sp-promo__badge">РАБОЧИЙ MVP</span><h2>SheetPilot <em>AI</em></h2><p>ИИ-ассистент для Excel: загрузка XLSX, команда обычным языком, контролируемый план изменений, предпросмотр и экспорт нового файла.</p><div class="sp-promo__meta"><i>FastAPI</i><i>openpyxl</i><i>Groq / GPT-OSS</i><i>Structured JSON</i></div><span class="sp-promo__arrow">Открыть кейс ↗</span></div><div class="sp-promo__visual"><img src="/assets/cases/sheetpilot-ai/sheetpilot-01-720w.webp" width="720" height="540" loading="lazy" decoding="async" alt="SheetPilot AI — ИИ-ассистент для редактирования Excel"/></div></a></div></section>\n'

def inject(page: Path):
    if not page.is_file():
        raise SystemExit(f'sheetpilot: page not found: {page}')
    text=page.read_text(encoding='utf-8')
    if 'data-sheetpilot-promo="true"' not in text:
        if '</head>' not in text or '</main>' not in text:
            raise SystemExit(f'sheetpilot: expected HTML markers missing: {page}')
        text=text.replace('</head>', STYLE+'</head>',1)
        text=text.replace('</main>', PROMO+'</main>',1)
        page.write_text(text,encoding='utf-8')

inject(root/'index.html')
inject(root/'cases'/'index.html')

sm=root/'sitemap.xml'
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ET.register_namespace('xhtml','http://www.w3.org/1999/xhtml')
tree=ET.parse(sm); r=tree.getroot(); ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
locs={(n.text or '').strip() for n in r.findall('.//'+ns+'loc')}
if url not in locs:
    node=ET.SubElement(r,ns+'url'); loc=ET.SubElement(node,ns+'loc'); loc.text=url
    tree.write(sm,encoding='utf-8',xml_declaration=True)

for name in ('sitemap.txt','llms.txt'):
    p=root/name
    if p.is_file():
        t=p.read_text(encoding='utf-8')
        line=url if name=='sitemap.txt' else f'- {url} — SheetPilot AI, ИИ-ассистент для обработки Excel-файлов'
        if line not in t:
            p.write_text(t.rstrip()+"\n"+line+"\n",encoding='utf-8')

print('stage58: SheetPilot AI case promoted on home + cases hub and added to sitemap')
