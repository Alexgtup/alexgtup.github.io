#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def route(path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "index.html": return "/"
    if rel == "404.html": return "/404.html"
    if rel.endswith("/index.html"): return "/" + rel[:-10]
    return "/" + rel


def hrefs(fragment: str):
    return re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\']', fragment, re.I)

pages = []
for path in sorted(root.rglob("*.html")):
    html = path.read_text(encoding="utf-8")
    if "</head>" not in html: continue
    if path.name.startswith(("google", "yandex_")): continue
    lang_m = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', html, re.I)
    lang = (lang_m.group(1).lower() if lang_m else "")
    nav_m = re.search(r'<nav\b[^>]*>(.*?)</nav>', html, re.I|re.S)
    foot_m = re.search(r'<footer\b[^>]*>(.*?)</footer>', html, re.I|re.S)
    nav = nav_m.group(1) if nav_m else ""
    foot = foot_m.group(1) if foot_m else ""
    pages.append((route(path), lang, hrefs(nav), hrefs(foot)))

required_ru = ["/cases/", "/services/", "/guides/", "/about/"]
required_en = ["/en/cases/", "/en/services/", "/en/guides/", "/en/about/"]
required_footer_ru = ["/services/", "/cases/", "/guides/", "/about/", "/privacy/"]
required_footer_en = ["/en/services/", "/en/cases/", "/en/guides/", "/en/about/", "/en/privacy/"]
missing_nav = []
missing_footer = []
nav_signatures = Counter()
footer_signatures = Counter()

for rt, lang, nav_links, footer_links in pages:
    # Homepage intentionally navigates to its own sections; 404 is utility UI.
    if rt in ("/", "/404.html"):
        continue

    nav_req = required_en if lang.startswith("en") else required_ru
    footer_req = required_footer_en if lang.startswith("en") else required_footer_ru

    absent_nav = [x for x in nav_req if x not in nav_links]
    absent_footer = [x for x in footer_req if x not in footer_links]
    if absent_nav:
        missing_nav.append((rt, lang, absent_nav))
    if absent_footer:
        missing_footer.append((rt, lang, absent_footer))

    nav_signatures[tuple(nav_links)] += 1
    footer_signatures[tuple(footer_links)] += 1

print(f"stage25 nav guard: {len(pages)} documents; {len(nav_signatures)} nav signatures; {len(footer_signatures)} footer signatures")
print(f"stage25 missing core nav: {len(missing_nav)}; missing core footer: {len(missing_footer)}")
for rt, lang, absent in missing_nav:
    print(f"NAV {rt} [{lang}] missing={','.join(absent)}")
for rt, lang, absent in missing_footer:
    print(f"FOOTER {rt} [{lang}] missing={','.join(absent)}")

if missing_nav or missing_footer:
    raise SystemExit("stage25: shared navigation/footer invariant failed")

print("stage25 navigation/footer invariant OK")
