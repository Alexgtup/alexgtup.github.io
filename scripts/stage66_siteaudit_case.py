#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
route = '/cases/siteaudit-studio/'
url = 'https://alexgtup.github.io' + route
demo_url = 'https://siteaudit-studio.onrender.com/'

STYLE = r'''<style id="siteaudit-integrated-style">
.s44-case--siteaudit{grid-column:span 12!important;grid-template-columns:minmax(0,.52fr) minmax(0,.48fr)!important;min-height:22rem!important;border-color:rgba(201,255,74,.22)!important;background:radial-gradient(circle at 92% 0,rgba(201,255,74,.09),transparent 25rem),#0d1116!important}.s44-case--siteaudit .s44-case__body>span,.s44-case--siteaudit .s44-case__body b{color:#c9ff4a}.s44-case--siteaudit .s44-case__body h3{font-size:clamp(2rem,4vw,4rem)}.siteaudit-card-preview{min-height:22rem;padding:1rem;background:#081016;display:flex;flex-direction:column;justify-content:center;gap:.7rem}.siteaudit-card-preview__top{display:flex;justify-content:space-between;align-items:center;gap:.8rem;color:#aab5bf;font:700 .66rem ui-monospace,monospace}.siteaudit-live{background:#c9ff4a;color:#090b0d;padding:.28rem .42rem;border-radius:999px;font-size:.55rem;font-weight:900}.siteaudit-card-preview__body{display:grid;grid-template-columns:.44fr 1.56fr;gap:.6rem}.siteaudit-score{min-height:9rem;border:1px solid rgba(255,255,255,.1);border-radius:.85rem;display:grid;place-items:center;background:#0e141a}.siteaudit-score strong{font-size:2.4rem;color:#c9ff4a}.siteaudit-score small{display:block;text-align:center;color:#6f7c87;font-size:.55rem}.siteaudit-checks{display:grid;gap:.45rem}.siteaudit-check{border:1px solid rgba(255,255,255,.1);border-radius:.7rem;padding:.65rem;background:#10161d;display:grid;grid-template-columns:auto 1fr auto;gap:.5rem;align-items:center}.siteaudit-dot{width:.5rem;height:.5rem;border-radius:50%;background:#c9ff4a}.siteaudit-dot.warn{background:#ffc857}.siteaudit-check span{font-size:.65rem;color:#c2cbd3}.siteaudit-check b{font:800 .57rem ui-monospace,monospace!important;color:#83909b!important}.s50-case-list>.siteaudit-case{border-color:rgba(201,255,74,.22)!important;background:radial-gradient(circle at 90% 0,rgba(201,255,74,.08),transparent 22rem),#0d1116!important}.s50-case-list>.siteaudit-case span,.s50-case-list>.siteaudit-case b{color:#c9ff4a!important}.siteaudit-case-mini{border:1px solid rgba(255,255,255,.09);border-radius:1rem;padding:1rem;background:#0a1016;display:grid;grid-template-columns:.38fr 1.62fr;gap:.6rem;align-items:center;min-height:12rem}.siteaudit-case-mini__score{aspect-ratio:1;border-radius:50%;display:grid;place-items:center;background:conic-gradient(#c9ff4a 82%,rgba(255,255,255,.08) 0);position:relative}.siteaudit-case-mini__score:before{content:"";position:absolute;inset:.48rem;border-radius:50%;background:#0c1218}.siteaudit-case-mini__score strong{position:relative;font-size:1.5rem!important;color:#f3f5f2!important}.siteaudit-case-mini__rows{display:grid;gap:.4rem}.siteaudit-case-mini__rows i{display:block;height:.58rem;border-radius:999px;background:linear-gradient(90deg,rgba(201,255,74,.65),rgba(255,255,255,.07))}
@media(max-width:900px){.s44-case--siteaudit{grid-template-columns:1fr!important}.siteaudit-card-preview{min-height:auto}.siteaudit-card-preview__body{grid-template-columns:1fr}.siteaudit-score{min-height:7rem}}@media(max-width:560px){.siteaudit-case-mini{grid-template-columns:1fr}.siteaudit-case-mini__score{width:6rem;justify-self:center}}
</style>'''

HOME_CARD = r'''<a class="s44-case s44-case--visual s44-case--siteaudit" data-project="siteaudit-studio" href="/cases/siteaudit-studio/">
  <div class="siteaudit-card-preview" aria-hidden="true"><div class="siteaudit-card-preview__top"><span>alexgtup.github.io</span><span class="siteaudit-live">LIVE AUDIT</span></div><div class="siteaudit-card-preview__body"><div class="siteaudit-score"><div><strong>82</strong><small>DEMO SCORE</small></div></div><div class="siteaudit-checks"><div class="siteaudit-check"><i class="siteaudit-dot"></i><span>HTTP / indexability</span><b>OK</b></div><div class="siteaudit-check"><i class="siteaudit-dot"></i><span>robots + sitemap</span><b>OK</b></div><div class="siteaudit-check"><i class="siteaudit-dot warn"></i><span>security headers</span><b>CHECK</b></div><div class="siteaudit-check"><i class="siteaudit-dot"></i><span>internal crawl</span><b>OK</b></div></div></div></div>
  <div class="s44-case__body"><span>SEO · NODE.JS · CRAWLER</span><h3>SiteAudit Studio</h3><p>Live web-сервис для технического аудита сайта: meta, robots, sitemap, links, accessibility и security с SSRF-защищённым crawler.</p><b>Открыть полный кейс ↗</b></div>
</a>'''

CASES_CARD = r'''<a class="visual siteaudit-case" data-project="siteaudit-studio" href="/cases/siteaudit-studio/"><div class="siteaudit-case-mini" aria-hidden="true"><div class="siteaudit-case-mini__score"><strong>82</strong></div><div class="siteaudit-case-mini__rows"><i></i><i></i><i></i><i></i></div></div><div><span>SEO · NODE.JS · CRAWLER</span><h3>SiteAudit Studio</h3><p>Объяснимый технический аудит публичных сайтов с live-demo, limited crawl и защитой от SSRF.</p><b>Открыть кейс ↗</b></div></a>'''

def add_style(text: str) -> str:
    if 'id="siteaudit-integrated-style"' not in text:
        if '</head>' not in text:
            raise SystemExit('stage66: </head> not found')
        text = text.replace('</head>', STYLE + '</head>', 1)
    return text

home = root / 'index.html'
if not home.is_file():
    raise SystemExit('stage66: homepage missing')
text = add_style(home.read_text(encoding='utf-8'))
if 'data-project="siteaudit-studio"' not in text:
    marker = '<div class="s44-case-grid">'
    if marker not in text:
        raise SystemExit('stage66: home project grid not found')
    text = text.replace(marker, marker + HOME_CARD, 1)
text = re.sub(r'<strong>7</strong><span>подробных кейсов на сайте</span>', '<strong>8</strong><span>подробных кейсов на сайте</span>', text, count=1)
home.write_text(text, encoding='utf-8')

cases = root / 'cases' / 'index.html'
if not cases.is_file():
    raise SystemExit('stage66: cases hub missing')
text = add_style(cases.read_text(encoding='utf-8'))
if 'data-project="siteaudit-studio"' not in text:
    marker = '<div class="s50-case-list">'
    if marker not in text:
        raise SystemExit('stage66: cases list not found')
    text = text.replace(marker, marker + CASES_CARD, 1)
text = re.sub(r'<strong>7</strong><span>подробных кейсов</span>', '<strong>8</strong><span>подробных кейсов</span>', text, count=1)
cases.write_text(text, encoding='utf-8')

case_page = root / 'cases' / 'siteaudit-studio' / 'index.html'
if not case_page.is_file():
    raise SystemExit('stage66: case page missing')
case_text = case_page.read_text(encoding='utf-8')
if demo_url not in case_text:
    raise SystemExit('stage66: live demo URL missing from case page')

sm = root / 'sitemap.xml'
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
tree = ET.parse(sm)
r = tree.getroot()
ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
locs = {(n.text or '').strip() for n in r.findall('.//' + ns + 'loc')}
if url not in locs:
    node = ET.SubElement(r, ns + 'url')
    loc = ET.SubElement(node, ns + 'loc')
    loc.text = url
    tree.write(sm, encoding='utf-8', xml_declaration=True)

for name in ('sitemap.txt', 'llms.txt'):
    p = root / name
    if not p.is_file():
        continue
    body = p.read_text(encoding='utf-8')
    line = url if name == 'sitemap.txt' else f'- {url} — SiteAudit Studio, технический SEO-аудит сайта, crawler, robots/sitemap и security checks'
    if line not in body:
        p.write_text(body.rstrip() + '\n' + line + '\n', encoding='utf-8')

home_body = home.read_text(encoding='utf-8')
cases_body = cases.read_text(encoding='utf-8')
if 'data-project="siteaudit-studio"' not in home_body:
    raise SystemExit('stage66: homepage SiteAudit card missing after patch')
if 'data-project="siteaudit-studio"' not in cases_body:
    raise SystemExit('stage66: cases SiteAudit card missing after patch')
if url not in {(n.text or '').strip() for n in ET.parse(sm).getroot().findall('.//' + ns + 'loc')}:
    raise SystemExit('stage66: SiteAudit sitemap URL missing after patch')

print('stage66: SiteAudit Studio integrated into home/cases; live demo + sitemap guarded')
