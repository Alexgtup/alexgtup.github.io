#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

STYLE_LINK_RE = re.compile(r'<link\b[^>]*\bhref=["\']([^"\']+\.css)["\'][^>]*>', re.I)
INLINE_RE = re.compile(r'<style\b[^>]*>(.*?)</style>', re.I | re.S)
RULE_RE = re.compile(r'([^{}]+)\{([^{}]*)\}', re.S)


def route(path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "index.html": return "/"
    if rel.endswith("/index.html"): return "/" + rel[:-10]
    return "/" + rel


def linked_css(html: str):
    out = []
    for href in STYLE_LINK_RE.findall(html):
        if not href.startswith('/'):
            continue
        p = root / href.lstrip('/')
        if p.is_file():
            out.append((href, p.read_text(encoding='utf-8', errors='ignore')))
    return out


def selector_for(css: str, pos: int) -> str:
    # Best-effort selector nearest a declaration. Auditing only; not CSS evaluation.
    left = css.rfind('}', 0, pos)
    brace = css.rfind('{', left + 1, pos + 1)
    if brace < 0:
        brace = css.rfind('{', 0, pos + 1)
    if brace < 0:
        return '(unknown)'
    start = max(css.rfind('}', 0, brace), css.rfind(';', 0, brace)) + 1
    sel = re.sub(r'\s+', ' ', css[start:brace]).strip()
    if len(sel) > 110: sel = sel[-110:]
    return sel or '(unknown)'

issues = defaultdict(list)
summary = defaultdict(int)

for page in sorted(root.rglob('*.html')):
    html = page.read_text(encoding='utf-8', errors='ignore')
    if '</head>' not in html or page.name.startswith(('google','yandex_')):
        continue
    rt = route(page)
    sources = [('inline', '\n'.join(INLINE_RE.findall(html)))] + linked_css(html)

    # HTML table containment: every table should be inside an overflow-capable wrapper.
    for m in re.finditer(r'<table\b', html, re.I):
        before = html[max(0, m.start()-700):m.start()]
        if not re.search(r'class=["\'][^"\']*(?:table-wrap|table-scroll|overflow)[^"\']*["\'][^>]*>[^<]*$', before, re.I|re.S):
            # Parent matching is approximate; only report for review.
            issues['table-review'].append((rt, 'HTML', '<table>'))
            summary['table-review'] += 1

    seen = set()
    for source_name, css in sources:
        if not css: continue

        for m in re.finditer(r'position\s*:\s*sticky', css, re.I):
            sel = selector_for(css, m.start())
            key=(source_name,'sticky',sel)
            if key in seen: continue
            seen.add(key)
            if any(x in sel.lower() for x in ('.header','.site-header','.intl-header','.process-intro')):
                continue
            issues['sticky-review'].append((rt, source_name, sel))
            summary['sticky-review'] += 1

        for m in re.finditer(r'grid-template-columns\s*:\s*repeat\(\s*(\d+)', css, re.I):
            cols=int(m.group(1))
            if cols < 3: continue
            sel=selector_for(css,m.start())
            key=(source_name,'grid',sel,cols)
            if key in seen: continue
            seen.add(key)
            # A page is suspicious only if there is no mobile media rule at all in that source.
            has_mobile=bool(re.search(r'@media\s*\(\s*max-width\s*:\s*(?:9\d\d|8\d\d|7\d\d|6\d\d|5\d\d|4\d\d)px\s*\)', css, re.I))
            if not has_mobile:
                issues['multi-column-no-mobile'].append((rt, source_name, f'{sel} [{cols} cols]'))
                summary['multi-column-no-mobile'] += 1

        for m in re.finditer(r'min-width\s*:\s*(\d+(?:\.\d+)?)(px|rem)', css, re.I):
            value=float(m.group(1)); unit=m.group(2).lower(); px=value if unit=='px' else value*16
            if px < 700: continue
            sel=selector_for(css,m.start())
            if 'table' in sel.lower(): continue
            key=(source_name,'minwidth',sel,round(px))
            if key in seen: continue
            seen.add(key)
            issues['large-min-width'].append((rt, source_name, f'{sel} [{px:.0f}px]'))
            summary['large-min-width'] += 1

        for m in re.finditer(r'position\s*:\s*fixed', css, re.I):
            sel=selector_for(css,m.start())
            if any(x in sel.lower() for x in ('cookie','skip-link','scroll-progress','site::before','.site:before')):
                continue
            key=(source_name,'fixed',sel)
            if key in seen: continue
            seen.add(key)
            issues['fixed-review'].append((rt, source_name, sel))
            summary['fixed-review'] += 1

print('stage35 responsive risk audit')
for kind in ('multi-column-no-mobile','large-min-width','sticky-review','fixed-review','table-review'):
    rows=issues.get(kind,[])
    print(f'  {kind}: {len(rows)}')
    for rt, source, detail in rows[:35]:
        print(f'    {rt} :: {source} :: {detail}')
