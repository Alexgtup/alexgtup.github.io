#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
DATE = "2026-09-09"

TARGETS = [
    "/cases/auto-crm/",
    "/cases/fin-planner/",
    "/cases/freelance-os/",
    "/cases/seo-control-center/",
    "/cases/swift-calendar/",
    "/cases/factory-catalog/",
    "/cases/taxi-app/",
    "/cases/siteaudit-studio/",
    "/cases/sheetpilot-ai/",
    "/guides/site-vs-web-app/",
    "/guides/n8n-vs-backend/",
    "/guides/repair-vs-rewrite/",
]

BLOCK = '''<aside class="s75-author" data-stage75-author="true" aria-label="Автор материала"><div class="s75-author__inner"><span class="s75-author__label">АВТОР И ОТВЕТСТВЕННОСТЬ</span><p><strong>Александр · Alexuys</strong><span>Кейс и технический разбор опубликованы автором портфолио.</span></p><nav aria-label="Ссылки об авторе"><a href="/about/" rel="author">Об авторе</a><a href="https://freelance.ru/gglalex" target="_blank" rel="me noopener noreferrer">Профиль и отзывы ↗</a></nav></div></aside>'''

# Decision guides describe a topic rather than a project; use a slightly different sentence.
GUIDE_BLOCK = BLOCK.replace(
    "Кейс и технический разбор опубликованы автором портфолио.",
    "Разбор подготовлен автором портфолио на основе практики разработки и автоматизации.",
)


def path_for(route: str) -> Path:
    return root / route.strip("/") / "index.html"


changed = []
for route in TARGETS:
    p = path_for(route)
    if not p.is_file():
        raise SystemExit(f"stage75: missing target {route}: {p}")
    text = p.read_text(encoding="utf-8")
    if 'data-stage75-author="true"' not in text:
        block = GUIDE_BLOCK if route.startswith("/guides/") else BLOCK
        text, n = re.subn(r'(<main\b[^>]*>)', lambda m: m.group(1) + block, text, count=1, flags=re.I)
        if n != 1:
            raise SystemExit(f"stage75: main element not found exactly once: {route}")
        p.write_text(text, encoding="utf-8")
        changed.append(route)

    final = p.read_text(encoding="utf-8")
    for required in (
        'data-stage75-author="true"',
        'href="/about/"',
        'https://freelance.ru/gglalex',
        'Александр · Alexuys',
    ):
        if required not in final:
            raise SystemExit(f"stage75: authorship invariant failed {route}: {required}")

css = root / "assets" / "site-enhancements.css"
if not css.is_file():
    raise SystemExit("stage75: site-enhancements.css missing")
styles = css.read_text(encoding="utf-8")
MARK = "/* stage75 visible authorship */"
if MARK not in styles:
    styles += r'''

/* stage75 visible authorship */
.s75-author{border-bottom:1px solid rgba(255,255,255,.065);background:rgba(255,255,255,.012)}
.s75-author__inner{width:min(100%,92rem);margin-inline:auto;padding:.78rem clamp(1.1rem,4vw,4.5rem);display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:.85rem 1.2rem}
.s75-author__label{font:800 .56rem/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.09em;color:#707b85;white-space:nowrap}
.s75-author p{margin:0;display:flex;align-items:baseline;gap:.55rem;min-width:0;font-size:.72rem;color:#8e98a2}.s75-author p strong{color:#d9dde0;font-size:.74rem;white-space:nowrap}.s75-author p span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.s75-author nav{display:flex;gap:.75rem;white-space:nowrap}.s75-author a{color:#aab3bb;text-decoration:none;font-size:.68rem}.s75-author a:hover{text-decoration:underline;color:#eef1f2}
@media(max-width:760px){.s75-author__inner{grid-template-columns:1fr;gap:.34rem;padding-block:.72rem}.s75-author p{display:block}.s75-author p span{display:block;margin-top:.18rem;white-space:normal;line-height:1.45}.s75-author nav{gap:1rem}}
'''
    css.write_text(styles, encoding="utf-8")

# Honest lastmod only for content pages changed by this stage.
sitemap = root / "sitemap.xml"
if not sitemap.is_file():
    raise SystemExit("stage75: sitemap.xml missing")
s = sitemap.read_text(encoding="utf-8")
for route in TARGETS:
    url = f"https://alexgtup.github.io{route}"
    pattern = re.compile(rf'(<loc>{re.escape(url)}</loc>\s*<lastmod>)[^<]+(</lastmod>)')
    s, n = pattern.subn(rf'\g<1>{DATE}\g<2>', s, count=1)
    if n != 1:
        raise SystemExit(f"stage75: sitemap lastmod missing: {url}")
sitemap.write_text(s, encoding="utf-8")

print(f"stage75: visible authorship guarded on {len(TARGETS)} content pages; changed={len(changed)}")
