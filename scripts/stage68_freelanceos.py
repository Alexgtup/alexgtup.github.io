#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
base = 'https://alexgtup.github.io'
product_route = '/freelance-os/'
case_route = '/cases/freelance-os/'
product_url = base + product_route
case_url = base + case_route

STYLE = r'''<style id="freelanceos-integrated-style">
.s44-case--freelanceos{grid-column:span 12!important;grid-template-columns:minmax(0,.52fr) minmax(0,.48fr)!important;min-height:22rem!important;border-color:rgba(201,255,74,.22)!important;background:radial-gradient(circle at 92% 0,rgba(201,255,74,.08),transparent 25rem),#0d1116!important}.s44-case--freelanceos .s44-case__body>span,.s44-case--freelanceos .s44-case__body b{color:#c9ff4a}.s44-case--freelanceos .s44-case__body h3{font-size:clamp(2rem,4vw,4rem)}.fos-card-preview{min-height:22rem;padding:1rem;background:#091016;display:flex;flex-direction:column;justify-content:center;gap:.7rem}.fos-card-preview__top{display:flex;justify-content:space-between;align-items:center;gap:.8rem;color:#aab5bf;font:700 .66rem ui-monospace,monospace}.fos-live{background:#c9ff4a;color:#090b0d;padding:.28rem .42rem;border-radius:999px;font-size:.55rem;font-weight:900}.fos-card-preview__stats{display:grid;grid-template-columns:repeat(4,1fr);gap:.45rem}.fos-card-preview__stats div{border:1px solid rgba(255,255,255,.09);border-radius:.65rem;padding:.55rem;background:#0e141a}.fos-card-preview__stats span,.fos-card-preview__stats strong{display:block}.fos-card-preview__stats span{font-size:.48rem;color:#727d88}.fos-card-preview__stats strong{margin-top:.25rem;font-size:.8rem}.fos-card-preview__board{display:grid;grid-template-columns:repeat(4,1fr);gap:.45rem}.fos-mini-col{border:1px solid rgba(255,255,255,.09);border-radius:.7rem;padding:.5rem;min-height:7rem;background:#0d1319}.fos-mini-col>b{display:block;color:#77838e!important;font-size:.48rem}.fos-mini-lead{margin-top:.4rem;border:1px solid rgba(255,255,255,.07);border-radius:.5rem;padding:.45rem;background:#111820}.fos-mini-lead strong,.fos-mini-lead span{display:block}.fos-mini-lead strong{font-size:.55rem}.fos-mini-lead span{margin-top:.18rem;color:#77838e;font-size:.47rem}.s50-case-list>.freelanceos-case{border-color:rgba(201,255,74,.22)!important;background:radial-gradient(circle at 90% 0,rgba(201,255,74,.07),transparent 22rem),#0d1116!important}.s50-case-list>.freelanceos-case span,.s50-case-list>.freelanceos-case b{color:#c9ff4a!important}.freelanceos-case-mini{border:1px solid rgba(255,255,255,.09);border-radius:1rem;padding:1rem;background:#0a1016;display:grid;gap:.55rem;min-height:12rem}.freelanceos-case-mini__stats{display:grid;grid-template-columns:repeat(3,1fr);gap:.4rem}.freelanceos-case-mini__stats i{display:block;height:2.2rem;border:1px solid rgba(255,255,255,.08);border-radius:.55rem;background:linear-gradient(145deg,rgba(201,255,74,.1),rgba(255,255,255,.02))}.freelanceos-case-mini__rows{display:grid;grid-template-columns:repeat(4,1fr);gap:.4rem}.freelanceos-case-mini__rows i{display:block;height:5.5rem;border:1px solid rgba(255,255,255,.08);border-radius:.55rem;background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.015))}.s68-entry{padding:0 0 4rem}.s68-entry__card{display:flex;justify-content:space-between;gap:1.5rem;align-items:center;border:1px solid rgba(201,255,74,.18);border-radius:1rem;padding:1rem 1.1rem;background:radial-gradient(circle at 100% 0,rgba(201,255,74,.06),transparent 20rem),rgba(255,255,255,.025)}.s68-entry__card span{display:block;color:#c9ff4a;font:800 .61rem ui-monospace,monospace;letter-spacing:.06em}.s68-entry__card strong{display:block;margin-top:.35rem;font-size:1rem}.s68-entry__card p{margin:.3rem 0 0;color:#8f9aa5;font-size:.78rem}.s68-entry__actions{display:flex;gap:.5rem;flex:0 0 auto;flex-wrap:wrap}.s68-entry__actions a{text-decoration:none;border:1px solid rgba(201,255,74,.25);border-radius:.75rem;padding:.65rem .8rem;color:#c9ff4a;font-size:.73rem;font-weight:850}
@media(max-width:900px){.s44-case--freelanceos{grid-template-columns:1fr!important}.fos-card-preview{min-height:auto}.fos-card-preview__board{grid-template-columns:1fr 1fr}}@media(max-width:660px){.s68-entry__card{align-items:flex-start;flex-direction:column}.s68-entry__actions{width:100%}.s68-entry__actions a{flex:1 1 auto;text-align:center}}@media(max-width:560px){.fos-card-preview__stats{grid-template-columns:1fr 1fr}.freelanceos-case-mini__rows{grid-template-columns:1fr 1fr}}
</style>'''

HOME_CARD = r'''<a class="s44-case s44-case--visual s44-case--freelanceos" data-project="freelance-os" href="/cases/freelance-os/">
  <div class="fos-card-preview" aria-hidden="true"><div class="fos-card-preview__top"><span>FreelanceOS · pipeline</span><span class="fos-live">LOCAL-FIRST</span></div><div class="fos-card-preview__stats"><div><span>ACTIVE</span><strong>4</strong></div><div><span>PIPELINE</span><strong>283k</strong></div><div><span>REVENUE</span><strong>120k</strong></div><div><span>CONV.</span><strong>67%</strong></div></div><div class="fos-card-preview__board"><div class="fos-mini-col"><b>NEW</b><div class="fos-mini-lead"><strong>Telegram bot</strong><span>28k</span></div></div><div class="fos-mini-col"><b>PROPOSAL</b><div class="fos-mini-lead"><strong>Factory catalog</strong><span>90k</span></div></div><div class="fos-mini-col"><b>WORK</b><div class="fos-mini-lead"><strong>Auto CRM</strong><span>120k</span></div></div><div class="fos-mini-col"><b>WON</b><div class="fos-mini-lead"><strong>n8n automation</strong><span>52k</span></div></div></div></div>
  <div class="s44-case__body"><span>CRM · JAVASCRIPT · LOCAL-FIRST</span><h3>FreelanceOS</h3><p>Рабочая CRM фрилансера: лиды, канбан, follow-up, задачи, источники, бюджеты, выручка и конверсия без регистрации.</p><b>Открыть кейс и live product ↗</b></div>
</a>'''

CASES_CARD = r'''<a class="visual freelanceos-case" data-project="freelance-os" href="/cases/freelance-os/"><div class="freelanceos-case-mini" aria-hidden="true"><div class="freelanceos-case-mini__stats"><i></i><i></i><i></i></div><div class="freelanceos-case-mini__rows"><i></i><i></i><i></i><i></i></div></div><div><span>CRM · JAVASCRIPT · LOCAL-FIRST</span><h3>FreelanceOS</h3><p>CRM для фриланс-практики с pipeline, follow-up, задачами, источниками, бюджетами и JSON backup.</p><b>Открыть кейс ↗</b></div></a>'''


def add_style(text: str) -> str:
    if 'id="freelanceos-integrated-style"' not in text:
        if '</head>' not in text:
            raise SystemExit('stage68: </head> not found')
        text = text.replace('</head>', STYLE + '</head>', 1)
    return text


def contextual_block(label: str) -> str:
    return f'''<section class="s68-entry" data-freelanceos-entry="{label}"><div class="container"><div class="s68-entry__card"><div><span>РАБОЧИЙ ПРОДУКТ</span><strong>FreelanceOS — CRM лида от входящей заявки до оплаты</strong><p>Канбан, follow-up, задачи, источники/UTM, бюджет, выручка и конверсия. Данные остаются в браузере.</p></div><div class="s68-entry__actions"><a href="/freelance-os/">Открыть CRM →</a><a href="/cases/freelance-os/">Кейс →</a><a href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Telegram ↗</a></div></div></div></section>'''

# Canonical product and case must already exist in the clean source tree.
product = root / 'freelance-os' / 'index.html'
case_page = root / 'cases' / 'freelance-os' / 'index.html'
for p, label in ((product, 'product'), (case_page, 'case')):
    if not p.is_file():
        raise SystemExit(f'stage68: missing {label} page')

for asset in ('freelance-os.css', 'freelance-os.js'):
    if not (root / 'assets' / asset).is_file():
        raise SystemExit(f'stage68: missing asset {asset}')

product_body = product.read_text(encoding='utf-8')
if product_url not in product_body or '/assets/freelance-os.css' not in product_body or '/assets/freelance-os.js' not in product_body:
    raise SystemExit('stage68: product metadata/assets incomplete')
if case_route not in product_body:
    product_body = product_body.replace('разработка CRM</a>', 'разработка CRM</a> · <a href="/cases/freelance-os/">кейс FreelanceOS</a>', 1)
if 'applicationCategory":"BusinessApplication"' not in product_body:
    schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"SoftwareApplication","name":"FreelanceOS","applicationCategory":"BusinessApplication","operatingSystem":"Web","description":"Local-first CRM для фрилансера: лиды, pipeline, follow-up, задачи, источники, бюджеты и аналитика.","url":"https://alexgtup.github.io/freelance-os/","inLanguage":"ru-RU","author":{"@id":"https://alexgtup.github.io/#person"}}</script>'
    product_body = product_body.replace('</head>', schema + '</head>', 1)
product.write_text(product_body, encoding='utf-8')

case_body = case_page.read_text(encoding='utf-8')
if product_route not in case_body or 'https://t.me/Alexuys' not in case_body:
    raise SystemExit('stage68: case missing live product/contact path')

home = root / 'index.html'
if not home.is_file(): raise SystemExit('stage68: homepage missing')
body = add_style(home.read_text(encoding='utf-8'))
if 'data-project="freelance-os"' not in body:
    marker = '<div class="s44-case-grid">'
    if marker not in body: raise SystemExit('stage68: home project grid missing')
    body = body.replace(marker, marker + HOME_CARD, 1)
body = re.sub(r'<strong>8</strong><span>подробных кейсов на сайте</span>', '<strong>9</strong><span>подробных кейсов на сайте</span>', body, count=1)
home.write_text(body, encoding='utf-8')

cases = root / 'cases' / 'index.html'
if not cases.is_file(): raise SystemExit('stage68: cases hub missing')
body = add_style(cases.read_text(encoding='utf-8'))
if 'data-project="freelance-os"' not in body:
    marker = '<div class="s50-case-list">'
    if marker not in body: raise SystemExit('stage68: cases list missing')
    body = body.replace(marker, marker + CASES_CARD, 1)
body = re.sub(r'<strong>8</strong><span>подробных кейсов</span>', '<strong>9</strong><span>подробных кейсов</span>', body, count=1)
cases.write_text(body, encoding='utf-8')

# Add multiple independent discovery paths, but keep the final section actionable.
for rel, label in (('crm-development/index.html', 'crm'), ('freelance-developer/index.html', 'freelance'), ('services/index.html', 'services')):
    p = root / rel
    if not p.is_file(): continue
    body = add_style(p.read_text(encoding='utf-8'))
    token = f'data-freelanceos-entry="{label}"'
    if token not in body:
        if '</main>' not in body: raise SystemExit(f'stage68: </main> missing {rel}')
        body = body.replace('</main>', contextual_block(label) + '</main>', 1)
    p.write_text(body, encoding='utf-8')

# Sitemap discovery.
sm = root / 'sitemap.xml'
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
tree = ET.parse(sm)
r = tree.getroot(); ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
locs = {(n.text or '').strip() for n in r.findall('.//' + ns + 'loc')}
for url in (product_url, case_url):
    if url not in locs:
        node = ET.SubElement(r, ns + 'url')
        ET.SubElement(node, ns + 'loc').text = url
        locs.add(url)
tree.write(sm, encoding='utf-8', xml_declaration=True)

llms = root / 'llms.txt'
if llms.is_file():
    body = llms.read_text(encoding='utf-8').rstrip()
    lines = [
        f'- {product_url} — FreelanceOS, local-first CRM фрилансера: лиды, канбан, follow-up, задачи, бюджеты и аналитика',
        f'- {case_url} — кейс разработки FreelanceOS: CRM workflow от входящей заявки до оплаты',
    ]
    for line in lines:
        if line not in body: body += '\n' + line
    llms.write_text(body + '\n', encoding='utf-8')

# Final invariants.
home_body = home.read_text(encoding='utf-8')
cases_body = cases.read_text(encoding='utf-8')
if 'data-project="freelance-os"' not in home_body: raise SystemExit('stage68: home card missing after patch')
if 'data-project="freelance-os"' not in cases_body: raise SystemExit('stage68: cases card missing after patch')
for url in (product_url, case_url):
    if url not in {(n.text or '').strip() for n in ET.parse(sm).getroot().findall('.//' + ns + 'loc')}:
        raise SystemExit(f'stage68: sitemap missing {url}')
for rel, label in (('crm-development/index.html', 'crm'), ('freelance-developer/index.html', 'freelance'), ('services/index.html', 'services')):
    p = root / rel
    if p.is_file():
        body = p.read_text(encoding='utf-8')
        if f'data-freelanceos-entry="{label}"' not in body or product_route not in body or case_route not in body or 'https://t.me/Alexuys' not in body:
            raise SystemExit(f'stage68: contextual discovery incomplete {rel}')

print('stage68: FreelanceOS product + case integrated; home/cases cards, discovery, schema, sitemap and llms guarded')