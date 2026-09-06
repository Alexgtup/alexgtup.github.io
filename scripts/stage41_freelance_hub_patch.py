#!/usr/bin/env python3
from pathlib import Path
import sys, xml.etree.ElementTree as ET

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
BASE='https://alexgtup.github.io'
URL=BASE+'/freelance-developer/'

# Add sitemap entry to built sitemap without forcing an artificial hreflang pair.
sitemap=root/'sitemap.xml'
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
tree=ET.parse(sitemap); rt=tree.getroot(); ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs=[(n.text or '').strip() for n in rt.findall('.//s:loc',ns)]
if URL not in locs:
    u=ET.SubElement(rt,'{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    ET.SubElement(u,'{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text=URL
    ET.SubElement(u,'{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text='2026-09-06'
    tree.write(sitemap,encoding='utf-8',xml_declaration=True)

stxt=root/'sitemap.txt'
if stxt.is_file():
    text=stxt.read_text(encoding='utf-8')
    if URL not in text:
        stxt.write_text(text.rstrip()+"\n"+URL+"\n",encoding='utf-8')

llms=root/'llms.txt'
if llms.is_file():
    text=llms.read_text(encoding='utf-8')
    line='- '+URL
    if line not in text:
        text += '\n\n## Verified freelance profile / hiring\n'+line+'\n- https://freelance.ru/gglalex\n'
        llms.write_text(text,encoding='utf-8')

# Give the new commercial trust hub visible links from important pages.
block='''<section data-stage41-freelance-hub="true" aria-label="Проверяемый фриланс-разработчик" style="padding:2.8rem 0;border-top:1px solid rgba(255,255,255,.09)"><div class="container"><div style="max-width:62rem"><p style="margin:0 0 .55rem;color:#7d8791;font-size:.72rem;text-transform:uppercase;letter-spacing:.08em">Нужен частный исполнитель</p><h2 style="margin:0;font-size:clamp(2rem,4vw,3.5rem);line-height:1;letter-spacing:-.045em">Фриланс-разработчик с внешней историей работ</h2><p style="margin:1rem 0 0;color:#969fa8">Отдельно собраны цены первого этапа, реальные кейсы, 19 выполненных заданий и оценки 9/9 в публичном профиле Freelance.ru.</p><p style="margin:1.1rem 0 0"><a href="/freelance-developer/" style="font-weight:850">Как заказать разработку и проверить исполнителя →</a></p></div></div></section>'''
for route in ('index.html','services/index.html','about/index.html'):
    p=root/route
    if not p.is_file(): continue
    html=p.read_text(encoding='utf-8')
    if 'data-stage41-freelance-hub="true"' in html: continue
    marker='</main>'
    if marker in html:
        html=html.replace(marker,block+'\n'+marker,1)
        p.write_text(html,encoding='utf-8')

print('stage41 freelance hub connected')
