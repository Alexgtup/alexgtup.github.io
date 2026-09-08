#!/usr/bin/env python3
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
routes=['/tools/','/tools/json-formatter/','/tools/utm-builder/','/tools/cron-builder/','/tools/jwt-decoder/']
base='https://alexgtup.github.io'

# DevTools has its own visual system, but must still participate in the site's
# shared layout invariant used by Stage24 and later audits.
for route in routes:
    p=root/(route.strip('/')+'/index.html')
    if not p.is_file(): raise SystemExit(f'stage67: missing {route}')
    body=p.read_text(encoding='utf-8')
    body=body.replace('class="dt-container ', 'class="container dt-container ')
    body=body.replace('class="dt-container"', 'class="container dt-container"')
    p.write_text(body,encoding='utf-8')
    for href in routes:
        if href!=route and href not in body: raise SystemExit(f'stage67: {route} missing crosslink {href}')
    if 'og:image:width' not in body or 'og:image:height' not in body: raise SystemExit(f'stage67: OG dimensions missing {route}')
    if 'class="container dt-container' not in body: raise SystemExit(f'stage67: shared container missing {route}')

sm=root/'sitemap.xml'; ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9'); ET.register_namespace('xhtml','http://www.w3.org/1999/xhtml')
tree=ET.parse(sm); r=tree.getroot(); ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
locs={(n.text or '').strip() for n in r.findall('.//'+ns+'loc')}
for route in routes:
    url=base+route
    if url not in locs:
        node=ET.SubElement(r,ns+'url'); ET.SubElement(node,ns+'loc').text=url
        locs.add(url)
tree.write(sm,encoding='utf-8',xml_declaration=True)

llms=root/'llms.txt'
if llms.is_file():
    body=llms.read_text(encoding='utf-8').rstrip()
    lines=[f'- {base}/tools/ — DevTools Hub, бесплатные инструменты JSON, UTM, Cron и JWT',f'- {base}/tools/json-formatter/ — JSON formatter и validator онлайн',f'- {base}/tools/utm-builder/ — UTM builder для campaign URL',f'- {base}/tools/cron-builder/ — Cron builder для 5-польных расписаний',f'- {base}/tools/jwt-decoder/ — локальный JWT decoder header и payload']
    for line in lines:
        if line not in body: body+='\n'+line
    llms.write_text(body+'\n',encoding='utf-8')

services=root/'services/index.html'
if services.is_file():
    body=services.read_text(encoding='utf-8')
    if 'data-devtools-entry="true"' not in body:
        card='<section data-devtools-entry="true" style="padding:0 0 4rem"><div class="container"><div style="border:1px solid rgba(201,255,74,.18);border-radius:1rem;padding:1rem 1.1rem;background:rgba(201,255,74,.035)"><strong style="display:block">Бесплатные инструменты для разработки и маркетинга</strong><p style="color:#8f9aa5;font-size:.8rem">JSON Formatter, UTM Builder, Cron Builder и JWT Decoder работают прямо в браузере.</p><a href="/tools/">Открыть DevTools Hub →</a></div></div></section>'
        if '</main>' not in body: raise SystemExit('stage67: services </main> missing')
        services.write_text(body.replace('</main>',card+'</main>',1),encoding='utf-8')

locs={(n.text or '').strip() for n in ET.parse(sm).getroot().findall('.//'+ns+'loc')}
for route in routes:
    if base+route not in locs: raise SystemExit(f'stage67: sitemap missing {route}')
print('stage67: DevTools Hub + 4 local tools integrated; shared shell, sitemap and crosslinks guarded')
