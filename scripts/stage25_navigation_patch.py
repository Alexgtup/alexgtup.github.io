#!/usr/bin/env python3
from pathlib import Path
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def route(path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "index.html": return "/"
    if rel.endswith("/index.html"): return "/" + rel[:-10]
    return "/" + rel


def find_anchor(fragment: str, href_pattern: str) -> str:
    pattern = rf'<a\b[^>]*href=["\']{href_pattern}["\'][^>]*>.*?</a>'
    m = re.search(pattern, fragment, re.I|re.S)
    return m.group(0) if m else ""

changed = []
for path in sorted(root.rglob("*.html")):
    html = path.read_text(encoding="utf-8")
    if "</head>" not in html: continue
    rt = route(path)
    if rt in ("/", "/404.html") or path.name.startswith(("google", "yandex_")):
        continue

    lang_m = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', html, re.I)
    lang = (lang_m.group(1).lower() if lang_m else "")
    if lang.startswith("en"):
        continue

    original = html

    # One navigation order for all internal Russian pages. Preserve an existing
    # EN switch only when the page already has a real translated counterpart.
    nav_m = re.search(r'(<nav\b[^>]*>)(.*?)(</nav>)', html, re.I|re.S)
    if nav_m:
        inner = nav_m.group(2)
        en_anchor_m = re.search(r'<a\b[^>]*href=["\'](/en/[^"\']*)["\'][^>]*>.*?</a>', inner, re.I|re.S)
        en_anchor = en_anchor_m.group(0) if en_anchor_m else ""
        cta_m = re.search(r'<a\b[^>]*href=["\']https://t\.me/Alexuys["\'][^>]*>.*?</a>', inner, re.I|re.S)
        cta = cta_m.group(0) if cta_m else '<a class="cta" href="https://t.me/Alexuys" rel="noreferrer noopener" target="_blank">Обсудить задачу ↗</a>'
        core = (
            '<a href="/cases/">Кейсы</a>'
            '<a href="/services/">Услуги</a>'
            '<a href="/guides/">Разборы</a>'
            '<a href="/about/">Обо мне</a>'
        )
        nav_inner = core + en_anchor + cta
        html = html[:nav_m.start(2)] + nav_inner + html[nav_m.end(2):]

    # One utility footer for internal RU pages. Page-specific conversion links
    # remain in the content/CTA above; the footer itself should not change shape.
    footer_m = re.search(r'(<footer\b[^>]*>).*?(</footer>)', html, re.I|re.S)
    if footer_m:
        footer_inner = (
            '<div class="container stage25-footer-inner">'
            '<span>© 2026 Alexuys</span>'
            '<nav class="stage25-footer-links" aria-label="Ссылки в подвале">'
            '<a href="/services/">Услуги</a>'
            '<a href="/cases/">Кейсы</a>'
            '<a href="/guides/">Разборы</a>'
            '<a href="/about/">Обо мне</a>'
            '<a href="/privacy/">Конфиденциальность</a>'
            '</nav></div>'
        )
        replacement = footer_m.group(1) + footer_inner + footer_m.group(2)
        html = html[:footer_m.start()] + replacement + html[footer_m.end():]

    if html != original:
        path.write_text(html, encoding="utf-8")
        changed.append(rt)

print(f"stage25 navigation patch: {len(changed)} RU internal pages normalized")
