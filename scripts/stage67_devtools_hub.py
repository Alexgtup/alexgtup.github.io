#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
hub='/tools/'
tools=['/tools/json-formatter/','/tools/utm-builder/','/tools/cron-builder/','/tools/jwt-decoder/','/tools/robots-validator/','/tools/sitemap-validator/']
routes=[hub,*tools]
base='https://alexgtup.github.io'
og_image=base+'/assets/og/alexuys-default.jpg'

contact='''<section class="dt-contact" data-devtools-contact="true"><div class="container dt-container"><div class="dt-contact__card"><div><strong>Нужен похожий инструмент или доработка проекта?</strong><p>Опишите задачу и текущее состояние - можно начать с конкретного рабочего шага.</p></div><a href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Написать в Telegram ↗</a></div></div></section>'''


def set_meta(body: str, route: str) -> str:
    canonical=base+route

    # Rich preview directives required by the site's final SEO validator.
    body=re.sub(
        r'<meta\s+name="robots"\s+content="[^"]*"\s*/?>',
        '<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1">',
        body,
        count=1,
        flags=re.I,
    )
    if not re.search(r'<meta\s+name="robots"\b',body,re.I):
        body=body.replace('</head>','<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1"></head>',1)

    def ensure_property(prop: str, value: str) -> None:
        nonlocal body
        pattern=rf'<meta\s+property="{re.escape(prop)}"\s+content="[^"]*"\s*/?>'
        tag=f'<meta property="{prop}" content="{value}">'
        if re.search(pattern,body,re.I):
            body=re.sub(pattern,tag,body,count=1,flags=re.I)
        else:
            body=body.replace('</head>',tag+'</head>',1)

    def ensure_name(name: str, value: str) -> None:
        nonlocal body
        pattern=rf'<meta\s+name="{re.escape(name)}"\s+content="[^"]*"\s*/?>'
        tag=f'<meta name="{name}" content="{value}">'
        if re.search(pattern,body,re.I):
            body=re.sub(pattern,tag,body,count=1,flags=re.I)
        else:
            body=body.replace('</head>',tag+'</head>',1)

    ensure_property('og:url',canonical)
    ensure_property('og:image',og_image)
    ensure_property('og:image:width','1200')
    ensure_property('og:image:height','630')
    ensure_name('twitter:card','summary_large_image')
    ensure_name('twitter:image',og_image)

    # Keep title/description consistent between normal search and social cards.
    title_match=re.search(r'<title>(.*?)</title>',body,re.I|re.S)
    desc_match=re.search(r'<meta\s+name="description"\s+content="([^"]*)"\s*/?>',body,re.I)
    if title_match:
        ensure_name('twitter:title',re.sub(r'\s+',' ',title_match.group(1)).strip())
    if desc_match:
        ensure_name('twitter:description',desc_match.group(1).strip())
    return body


for route in routes:
    p=root/(route.strip('/')+'/index.html')
    if not p.is_file(): raise SystemExit(f'stage67: missing {route}')
    body=p.read_text(encoding='utf-8')
    body=body.replace('class="dt-container ', 'class="container dt-container ')
    body=body.replace('class="dt-container"', 'class="container dt-container"')
    body=set_meta(body,route)
    if 'data-devtools-contact="true"' not in body:
        if '</main>' not in body: raise SystemExit(f'stage67: </main> missing {route}')
        body=body.replace('</main>',contact+'</main>',1)
    p.write_text(body,encoding='utf-8')
    if hub not in body: raise SystemExit(f'stage67: {route} missing hub link')
    if 'og:image:width' not in body or 'og:image:height' not in body: raise SystemExit(f'stage67: OG dimensions missing {route}')
    if f'property="og:url" content="{base+route}"' not in body: raise SystemExit(f'stage67: og:url missing {route}')
    if 'name="twitter:card" content="summary_large_image"' not in body: raise SystemExit(f'stage67: twitter card missing {route}')
    if 'name="twitter:image"' not in body: raise SystemExit(f'stage67: twitter image missing {route}')
    if 'max-image-preview:large' not in body or 'max-video-preview:-1' not in body: raise SystemExit(f'stage67: rich robots directives missing {route}')
    if 'class="container dt-container' not in body: raise SystemExit(f'stage67: shared container missing {route}')
    if 'https://t.me/Alexuys' not in body: raise SystemExit(f'stage67: final contact missing {route}')

hub_body=(root/'tools/index.html').read_text(encoding='utf-8')
for href in tools:
    if href not in hub_body: raise SystemExit(f'stage67: hub missing tool link {href}')

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
    lines=[
        f'- {base}/tools/ — DevTools Hub, 6 бесплатных инструментов для разработки, SEO и маркетинга',
        f'- {base}/tools/json-formatter/ — JSON formatter и validator онлайн',
        f'- {base}/tools/utm-builder/ — UTM builder для campaign URL',
        f'- {base}/tools/cron-builder/ — Cron builder для 5-польных расписаний',
        f'- {base}/tools/jwt-decoder/ — локальный JWT decoder header и payload',
        f'- {base}/tools/robots-validator/ — robots.txt validator для User-agent, Disallow, Allow и Sitemap',
        f'- {base}/tools/sitemap-validator/ — sitemap XML validator для loc, дублей и хостов',
    ]
    for line in lines:
        if line not in body: body+='\n'+line
    llms.write_text(body+'\n',encoding='utf-8')

services=root/'services/index.html'
if services.is_file():
    body=services.read_text(encoding='utf-8')
    if 'data-devtools-entry="true"' not in body:
        card='''<section data-devtools-entry="true" style="padding:0 0 4rem"><div class="container"><div style="border:1px solid rgba(201,255,74,.18);border-radius:1rem;padding:1rem 1.1rem;background:rgba(201,255,74,.035)"><strong style="display:block">6 бесплатных инструментов для разработки, SEO и маркетинга</strong><p style="color:#8f9aa5;font-size:.8rem">JSON Formatter, UTM Builder, Cron Builder, JWT Decoder, robots.txt Validator и Sitemap Validator работают без регистрации.</p><div style="display:flex;gap:.8rem;flex-wrap:wrap"><a href="/tools/">DevTools Hub →</a><a href="/tools/robots-validator/">robots.txt →</a><a href="/tools/sitemap-validator/">sitemap.xml →</a></div></div></div></section>'''
        if '</main>' not in body: raise SystemExit('stage67: services </main> missing')
        services.write_text(body.replace('</main>',card+'</main>',1),encoding='utf-8')
    else:
        # Upgrade an older card generated by a previous pass so both new SEO tools
        # have a third independent internal referrer.
        if '/tools/robots-validator/' not in body or '/tools/sitemap-validator/' not in body:
            old='<a href="/tools/">Открыть DevTools Hub →</a>'
            new='<a href="/tools/">DevTools Hub →</a> <a href="/tools/robots-validator/">robots.txt →</a> <a href="/tools/sitemap-validator/">sitemap.xml →</a>'
            if old not in body: raise SystemExit('stage67: services DevTools link marker missing')
            services.write_text(body.replace(old,new,1),encoding='utf-8')

# Stage66 adds the SiteAudit context as the final section on web-development.
# Keep that useful discovery block, but make the final section itself actionable.
web=root/'web-development/index.html'
if web.is_file():
    body=web.read_text(encoding='utf-8')
    if 'data-siteaudit-context="true"' in body and 'data-siteaudit-contact="true"' not in body:
        old='<a href="/cases/siteaudit-studio/">Кейс SiteAudit Studio →</a>'
        new=old+'<a data-siteaudit-contact="true" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Обсудить сайт ↗</a>'
        if old not in body: raise SystemExit('stage67: SiteAudit context link marker missing')
        body=body.replace(old,new,1)
        web.write_text(body,encoding='utf-8')

locs={(n.text or '').strip() for n in ET.parse(sm).getroot().findall('.//'+ns+'loc')}
for route in routes:
    if base+route not in locs: raise SystemExit(f'stage67: sitemap missing {route}')
print('stage67: DevTools Hub + 6 tools integrated; SEO metadata, discovery, final contact and sitemap guarded')