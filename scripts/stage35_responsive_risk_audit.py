#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
STYLE_LINK_RE = re.compile(r'<link\b[^>]*\bhref=["\']([^"\']+\.css)["\'][^>]*>', re.I)
INLINE_RE = re.compile(r'<style\b[^>]*>(.*?)</style>', re.I | re.S)
RULE_RE = re.compile(r'([^{}]+)\{([^{}]*)\}', re.S)


def route(path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == 'index.html': return '/'
    if rel.endswith('/index.html'): return '/' + rel[:-10]
    return '/' + rel


def compact(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()


def rules(css: str):
    for m in RULE_RE.finditer(css):
        selector = compact(m.group(1))
        declarations = m.group(2)
        if not selector or selector.startswith('@'):
            continue
        yield selector, declarations


def media_blocks(css: str):
    pos = 0
    while True:
        m = re.search(r'@media\s*([^\{]+)\{', css[pos:], re.I)
        if not m: break
        start = pos + m.start()
        brace = pos + m.end() - 1
        depth = 1; i = brace + 1
        while i < len(css) and depth:
            if css[i] == '{': depth += 1
            elif css[i] == '}': depth -= 1
            i += 1
        condition = compact(m.group(1))
        body = css[brace+1:i-1] if depth == 0 else css[brace+1:]
        yield condition, body
        pos = max(i, brace + 1)


def is_mobile_condition(condition: str) -> bool:
    vals = [int(x) for x in re.findall(r'max-width\s*:\s*(\d+)px', condition, re.I)]
    return bool(vals and min(vals) <= 1000)


def selector_parts(selector: str):
    return [compact(x) for x in selector.split(',') if compact(x)]


def has_mobile_decl(css: str, selector: str, prop: str, value_re: str) -> bool:
    parts = selector_parts(selector)
    for condition, block in media_blocks(css):
        if not is_mobile_condition(condition):
            continue
        for sel, dec in rules(block):
            if not any(p == sel or p in selector_parts(sel) for p in parts):
                continue
            if re.search(rf'{re.escape(prop)}\s*:\s*(?:{value_re})', dec, re.I):
                return True
    return False


class TableAudit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.bad=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs); classes=set((a.get('class') or '').split())
        if tag.lower()=='table':
            ancestor_classes=set()
            for _, cls in self.stack: ancestor_classes |= cls
            if not any(('table-wrap' in c or 'table-scroll' in c or 'overflow' in c) for c in ancestor_classes):
                self.bad += 1
        self.stack.append((tag.lower(), classes))
    def handle_endtag(self, tag):
        tag=tag.lower()
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                del self.stack[i:]; return


issues=defaultdict(list)
inline_sources=[]
asset_sources={}

for page in sorted(root.rglob('*.html')):
    html=page.read_text(encoding='utf-8',errors='ignore')
    if '</head>' not in html or page.name.startswith(('google','yandex_')): continue
    rt=route(page)
    inline='\n'.join(INLINE_RE.findall(html))
    if inline: inline_sources.append((rt,'inline',inline))
    for href in STYLE_LINK_RE.findall(html):
        if not href.startswith('/'): continue
        p=root/href.lstrip('/')
        if p.is_file() and href not in asset_sources:
            asset_sources[href]=p.read_text(encoding='utf-8',errors='ignore')
    parser=TableAudit(); parser.feed(html)
    if parser.bad:
        issues['table-without-scroll'].append((rt,'HTML',f'{parser.bad} table(s)'))

sources=inline_sources + [(f'asset:{href}',href,css) for href,css in sorted(asset_sources.items())]

known_fixed=(
    'media-lightbox','mobile-project-cta','mobile-site-drawer','intl-mobile-drawer',
    'cookie','skip-link','scroll-progress','site::before','site:before'
)

for owner, source_name, css in sources:
    seen=set()
    for selector, dec in rules(css):
        low=selector.lower()

        if re.search(r'position\s*:\s*sticky', dec, re.I):
            if any(x in low for x in ('.header','.site-header','.intl-header')):
                continue
            if has_mobile_decl(css, selector, 'position', r'static|relative'):
                continue
            key=('sticky',selector)
            if key not in seen:
                seen.add(key); issues['sticky-without-mobile-reset'].append((owner,source_name,selector))

        g=re.search(r'grid-template-columns\s*:\s*repeat\(\s*(\d+)', dec, re.I)
        if g and int(g.group(1)) >= 3:
            if has_mobile_decl(css, selector, 'grid-template-columns', r'1fr|repeat\(\s*[12]\s*,'):
                continue
            key=('grid',selector)
            if key not in seen:
                seen.add(key); issues['multi-column-without-collapse'].append((owner,source_name,f'{selector} [{g.group(1)} cols]'))

        mw=re.search(r'min-width\s*:\s*(\d+(?:\.\d+)?)(px|rem)', dec, re.I)
        if mw:
            value=float(mw.group(1)); unit=mw.group(2).lower(); px=value if unit=='px' else value*16
            if px >= 700 and 'table' not in low:
                # A matching mobile max-width/width reset makes this safe.
                if not (has_mobile_decl(css, selector, 'min-width', r'0|auto') or has_mobile_decl(css, selector, 'width', r'100%|auto')):
                    key=('minwidth',selector,round(px))
                    if key not in seen:
                        seen.add(key); issues['large-min-width-without-reset'].append((owner,source_name,f'{selector} [{px:.0f}px]'))

        if re.search(r'position\s*:\s*fixed', dec, re.I):
            if any(x in low for x in known_fixed):
                continue
            key=('fixed',selector)
            if key not in seen:
                seen.add(key); issues['fixed-review'].append((owner,source_name,selector))

print('stage35 unresolved responsive risks')
order=('multi-column-without-collapse','large-min-width-without-reset','sticky-without-mobile-reset','fixed-review','table-without-scroll')
for kind in order:
    rows=issues.get(kind,[])
    print(f'  {kind}: {len(rows)}')
    for owner,source,detail in rows[:40]:
        print(f'    {owner} :: {source} :: {detail}')
