#!/usr/bin/env python3
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json, os, re, sys, xml.etree.ElementTree as ET

BASE = 'https://alexgtup.github.io'
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang = ''
        self.title_depth = 0
        self.title = ''
        self.h1_count = 0
        self.meta = []
        self.links = []
        self.images = []
        self.anchors = []
        self.ids = set()
        self.jsonld_chunks = []
        self._jsonld = False
        self._jsonbuf = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.html_lang = a.get('lang','')
        elif tag == 'title': self.title_depth += 1
        elif tag == 'h1': self.h1_count += 1
        elif tag == 'meta': self.meta.append(a)
        elif tag == 'link': self.links.append(a)
        elif tag == 'img': self.images.append(a)
        elif tag == 'a': self.anchors.append(a)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'script' and a.get('type','').lower() == 'application/ld+json':
            self._jsonld = True; self._jsonbuf = []
    def handle_endtag(self, tag):
        if tag == 'title' and self.title_depth: self.title_depth -= 1
        if tag == 'script' and self._jsonld:
            self.jsonld_chunks.append(''.join(self._jsonbuf).strip())
            self._jsonld = False; self._jsonbuf = []
    def handle_data(self, data):
        if self.title_depth: self.title += data
        if self._jsonld: self._jsonbuf.append(data)

def meta_content(page, key, value):
    for m in page.meta:
        if m.get(key,'').lower() == value.lower(): return m.get('content','')
    return ''

def link_rel(page, rel):
    out=[]
    for l in page.links:
        rels=(l.get('rel') or '').lower().split()
        if rel.lower() in rels: out.append(l)
    return out

def public_url_to_file(url_or_path: str) -> Path | None:
    if not url_or_path: return None
    p=urlparse(url_or_path)
    if p.scheme in ('mailto','tel','javascript','data'): return None
    if p.scheme and p.netloc and p.netloc != 'alexgtup.github.io': return None
    path=p.path or '/'
    if path == '/': return ROOT/'index.html'
    dest=ROOT/path.lstrip('/')
    if path.endswith('/'): return dest/'index.html'
    if dest.is_file(): return dest
    if dest.suffix: return dest
    return dest/'index.html'

def route_for_file(page: Path) -> str:
    rel=page.relative_to(ROOT).as_posix()
    if rel=='index.html': return '/'
    if rel=='404.html': return '/404'
    if rel.endswith('/index.html'): return '/'+rel[:-len('index.html')]
    return '/'+rel

errors=[]
# required artifacts
for req in ['index.html','404.html','sitemap.xml','robots.txt','feed.xml','en/feed.xml','favicon.ico','favicon.svg','favicon-96.png','site.webmanifest','assets/og/alexuys-default.jpg']:
    if not (ROOT/req).is_file(): errors.append(f'missing required artifact: {req}')

# sitemap and hreflang
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
tree=ET.parse(ROOT/'sitemap.xml')
url_nodes=tree.findall('.//s:url',ns)
sitemap_urls=[]; sitemap_alts={}
for node in url_nodes:
    loc=node.find('s:loc',ns)
    if loc is None or not (loc.text or '').strip(): errors.append('sitemap URL without loc'); continue
    url=loc.text.strip(); sitemap_urls.append(url)
    sitemap_alts[url]={(x.attrib.get('hreflang'),x.attrib.get('href')) for x in node.findall('x:link',ns)}
if len(sitemap_urls)!=len(set(sitemap_urls)): errors.append('duplicate URL in sitemap')
for url in sitemap_urls:
    target=public_url_to_file(url)
    if not target or not target.is_file(): errors.append(f'sitemap URL missing page: {url} -> {target}')
for forbidden in [BASE+'/privacy/',BASE+'/en/privacy/']:
    if forbidden in sitemap_urls: errors.append(f'noindex privacy URL present in sitemap: {forbidden}')
# reciprocal hreflang in sitemap
for url,alts in sitemap_alts.items():
    amap={k:v for k,v in alts if k and v}
    if 'ru' in amap and 'en' in amap:
        partner=amap['en'] if url==amap['ru'] else amap['ru']
        if partner in sitemap_alts:
            pmap={k:v for k,v in sitemap_alts[partner] if k and v}
            if pmap.get('ru')!=amap.get('ru') or pmap.get('en')!=amap.get('en'):
                errors.append(f'non-reciprocal sitemap hreflang: {url} <-> {partner}')

seen_titles={}; seen_canon={}
html_files=sorted(ROOT.rglob('*.html'))
for pagefile in html_files:
    name=pagefile.name
    is_verify=name.startswith('google') or name.startswith('yandex_')
    text=pagefile.read_text(encoding='utf-8',errors='ignore')
    pp=PageParser(); pp.feed(text)
    route=route_for_file(pagefile)
    is_404=route=='/404'
    if is_verify: continue
    if not pp.html_lang: errors.append(f'missing html lang: {route}')
    if not is_404:
        if pp.h1_count != 1: errors.append(f'H1 count {pp.h1_count}: {route}')
        if not pp.title.strip(): errors.append(f'missing title: {route}')
        else:
            t=pp.title.strip()
            if t in seen_titles: errors.append(f'duplicate title: {route} and {seen_titles[t]}')
            seen_titles[t]=route
        desc=meta_content(pp,'name','description')
        if not desc.strip(): errors.append(f'missing description: {route}')
        can=link_rel(pp,'canonical')
        if len(can)!=1: errors.append(f'canonical count {len(can)}: {route}')
        elif not can[0].get('href'): errors.append(f'canonical without href: {route}')
        else:
            href=can[0]['href']
            if href in seen_canon: errors.append(f'duplicate canonical: {route} and {seen_canon[href]} -> {href}')
            seen_canon[href]=route
            expected=BASE+route
            if href!=expected: errors.append(f'canonical mismatch: {route}: {href} != {expected}')
        robots=meta_content(pp,'name','robots').replace(' ','')
        if route in ('/privacy/','/en/privacy/'):
            if 'noindex' not in robots: errors.append(f'privacy must be noindex: {route}')
        else:
            for tok in ['index','follow','max-image-preview:large','max-snippet:-1','max-video-preview:-1']:
                if tok not in robots: errors.append(f'robots missing {tok}: {route}: {robots}')
        for keytype,key in [('property','og:title'),('property','og:description'),('property','og:image'),('property','og:url'),('name','twitter:card'),('name','twitter:image')]:
            if not meta_content(pp,keytype,key): errors.append(f'missing {key}: {route}')
        if meta_content(pp,'name','twitter:card') != 'summary_large_image': errors.append(f'twitter card not large: {route}')
        og_image = meta_content(pp,'property','og:image')
        og_target = public_url_to_file(og_image)
        if og_target and og_image.startswith(BASE) and not og_target.is_file(): errors.append(f'broken OG image: {route}: {og_image}')
        if not meta_content(pp,'property','og:image:width') or not meta_content(pp,'property','og:image:height'):
            errors.append(f'OG image dimensions missing: {route}')
        # indexable sitemap pages must be in sitemap (privacy intentionally excluded)
        page_url=BASE+route
        if route not in ('/privacy/','/en/privacy/') and page_url not in sitemap_urls:
            errors.append(f'indexable page absent from sitemap: {route}')
    # images
    for im in pp.images:
        if 'alt' not in im: errors.append(f'image without alt: {route}: {str(im)[:120]}')
        if not im.get('width') or not im.get('height'): errors.append(f'image without dimensions: {route}: {str(im)[:120]}')
        src=im.get('src','')
        target=public_url_to_file(src)
        if target and src.startswith('/') and not target.is_file(): errors.append(f'broken local image: {route}: {src}')
    # links and blank safety
    for a in pp.anchors:
        href=a.get('href','')
        if a.get('target')=='_blank':
            rels=set((a.get('rel') or '').lower().split())
            if not {'noopener','noreferrer'} <= rels: errors.append(f'_blank missing noopener/noreferrer: {route}: {href}')
        target=public_url_to_file(href)
        if target and (href.startswith('/') or href.startswith(BASE)) and not target.exists():
            errors.append(f'broken internal link: {route}: {href} -> {target}')
    # JSON-LD
    for chunk in pp.jsonld_chunks:
        try:
            data=json.loads(chunk)
        except Exception as e:
            errors.append(f'invalid JSON-LD: {route}: {e}'); continue
        objs=data if isinstance(data,list) else [data]
        for obj in objs:
            if not isinstance(obj,dict): continue
            typ=obj.get('@type')
            if typ=='Article':
                for k in ('datePublished','dateModified','author','publisher'):
                    if not obj.get(k): errors.append(f'Article missing {k}: {route}')
            if typ=='CreativeWork' and not obj.get('author'): errors.append(f'CreativeWork missing author: {route}')

# privacy pages must exist despite noindex
for path in ['privacy/index.html','en/privacy/index.html']:
    if not (ROOT/path).is_file(): errors.append(f'missing privacy page: {path}')
# legacy build must not leak
for p in ROOT.rglob('*'):
    if '_next' in p.parts or p.name.startswith('__next.'):
        errors.append(f'legacy Next file leaked: {p}')
# image budgets
for p in ROOT.glob('assets/cases/**/*.webp'):
    if '-720w.' not in p.name and '-800w.' not in p.name and p.stat().st_size > 400_000:
        errors.append(f'case image budget exceeded: {p}: {p.stat().st_size}')
for p in ROOT.glob('assets/og/*'):
    if p.stat().st_size > 300_000: errors.append(f'OG image budget exceeded: {p}: {p.stat().st_size}')
# feeds parse
ET.parse(ROOT/'feed.xml'); ET.parse(ROOT/'en/feed.xml')
if errors:
    print('\n'.join('ERROR: '+e for e in errors))
    raise SystemExit(f'validation failed with {len(errors)} error(s)')
print(f'validation OK: {len(sitemap_urls)} sitemap URLs, {len(html_files)} HTML files, {len(seen_titles)} indexable/noindex pages checked')
