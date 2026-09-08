#!/usr/bin/env python3
from pathlib import Path
import re, sys, xml.etree.ElementTree as ET

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
route = '/cases/seo-control-center/'
url = 'https://alexgtup.github.io' + route

STYLE = r'''<style id="seo-control-center-integrated-style">
.s44-case--seo-control{grid-column:span 12!important;grid-template-columns:minmax(0,.56fr) minmax(0,.44fr)!important;min-height:23rem!important;border-color:rgba(129,149,255,.22)!important;background:radial-gradient(circle at 90% 0,rgba(129,149,255,.12),transparent 25rem),#0d1116!important}
.s44-case--seo-control .s44-case__image{min-height:23rem;background:#08111d}.s44-case--seo-control .s44-case__image img{object-fit:cover}.s44-case--seo-control .s44-case__body>span,.s44-case--seo-control .s44-case__body b{color:#8195ff}.s44-case--seo-control .s44-case__body h3{font-size:clamp(2rem,4vw,4rem)}
.s50-case-list>.scc-case{border-color:rgba(129,149,255,.22)!important;background:radial-gradient(circle at 90% 0,rgba(129,149,255,.10),transparent 23rem),#0d1116!important}.s50-case-list>.scc-case span,.s50-case-list>.scc-case b{color:#8195ff!important}
@media(max-width:900px){.s44-case--seo-control{grid-template-columns:1fr!important}.s44-case--seo-control .s44-case__image{min-height:0}}
</style>'''

HOME_CARD = r'''<a class="s44-case s44-case--visual s44-case--seo-control" data-project="seo-control-center" href="/cases/seo-control-center/">
  <div class="s44-case__image"><img src="/assets/cases/seo-control-center/seo-control-center-card-01.svg" width="1536" height="1024" loading="lazy" decoding="async" alt="SEO Control Center — презентационная карточка SEO-платформы"/></div>
  <div class="s44-case__body"><span>SEO · FULLSTACK · AUTOMATION</span><h3>SEO Control Center</h3><p>Operational dashboard для sitemap, crawler, индексации, поисковых метрик и истории SEO-событий.</p><b>Открыть полный кейс ↗</b></div>
</a>'''

CASES_CARD = r'''<a class="visual scc-case" data-project="seo-control-center" href="/cases/seo-control-center/"><img src="/assets/cases/seo-control-center/seo-control-center-card-02.svg" width="1536" height="1024" loading="lazy" decoding="async" alt="SEO Control Center — презентационный dashboard"/><div><span>SEO · FULLSTACK · AUTOMATION</span><h3>SEO Control Center</h3><p>Единая панель: sitemap, crawler, индексация, GSC, Яндекс, технические события и история изменений.</p><b>Открыть кейс ↗</b></div></a>'''

def add_style(text: str) -> str:
    if 'id="seo-control-center-integrated-style"' not in text:
        if '</head>' not in text: raise SystemExit('stage61: </head> not found')
        text = text.replace('</head>', STYLE + '</head>', 1)
    return text

home = root / 'index.html'
text = add_style(home.read_text(encoding='utf-8'))
if 'data-project="seo-control-center"' not in text:
    marker = '<div class="s44-case-grid">'
    if marker not in text: raise SystemExit('stage61: home project grid not found')
    text = text.replace(marker, marker + HOME_CARD, 1)
text = re.sub(r'<strong>6</strong><span>подробных кейсов на сайте</span>', '<strong>7</strong><span>подробных кейсов на сайте</span>', text, count=1)
home.write_text(text, encoding='utf-8')

cases = root / 'cases' / 'index.html'
text = add_style(cases.read_text(encoding='utf-8'))
if 'data-project="seo-control-center"' not in text:
    marker = '<div class="s50-case-list">'
    if marker not in text: raise SystemExit('stage61: cases list not found')
    text = text.replace(marker, marker + CASES_CARD, 1)
text = re.sub(r'<strong>6</strong><span>подробных кейсов</span>', '<strong>7</strong><span>подробных кейсов</span>', text, count=1)
cases.write_text(text, encoding='utf-8')

sm = root / 'sitemap.xml'
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')
tree = ET.parse(sm); r = tree.getroot(); ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
locs = {(n.text or '').strip() for n in r.findall('.//' + ns + 'loc')}
if url not in locs:
    node = ET.SubElement(r, ns + 'url'); loc = ET.SubElement(node, ns + 'loc'); loc.text = url
    tree.write(sm, encoding='utf-8', xml_declaration=True)

for name in ('sitemap.txt','llms.txt'):
    p = root / name
    if p.is_file():
        t = p.read_text(encoding='utf-8')
        line = url if name == 'sitemap.txt' else f'- {url} — SEO Control Center, мониторинг индексации, поисковых метрик и технического SEO'
        if line not in t: p.write_text(t.rstrip() + '\n' + line + '\n', encoding='utf-8')

# Build guard: fail deploy instead of silently publishing without the cards.
if 'data-project="seo-control-center"' not in home.read_text(encoding='utf-8'):
    raise SystemExit('stage61: homepage SEO Control Center card missing after patch')
if 'data-project="seo-control-center"' not in cases.read_text(encoding='utf-8'):
    raise SystemExit('stage61: cases SEO Control Center card missing after patch')

print('stage61: SEO Control Center integrated into home/cases; presentation cards enabled; sitemap updated')