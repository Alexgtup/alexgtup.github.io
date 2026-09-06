#!/usr/bin/env python3
from pathlib import Path
from collections import Counter, defaultdict
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def route(path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "index.html": return "/"
    if rel.endswith("/index.html"): return "/" + rel[:-10]
    return "/" + rel


def hrefs(fragment: str):
    return re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\']', fragment, re.I)


def text(fragment: str):
    value = re.sub(r'<script\b.*?</script>', ' ', fragment, flags=re.I|re.S)
    value = re.sub(r'<style\b.*?</style>', ' ', value, flags=re.I|re.S)
    value = re.sub(r'<[^>]+>', ' ', value)
    return ' '.join(value.split())

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
    pages.append((route(path), lang, hrefs(nav), hrefs(foot), text(nav), text(foot)))

required_ru = ["/cases/", "/services/", "/guides/", "/about/"]
required_en = ["/en/cases/", "/en/services/", "/en/guides/", "/en/about/"]
missing = []
nav_signatures = Counter()
footer_signatures = Counter()

for rt, lang, nav_links, footer_links, nav_text, footer_text in pages:
    # Exclude utility documents whose navigation is intentionally minimal.
    if rt in ("/404", "/privacy/", "/en/privacy/"):
        continue
    req = required_en if lang.startswith("en") else required_ru
    absent = [x for x in req if x not in nav_links]
    if absent:
        missing.append((rt, lang, absent, nav_links))
    nav_signatures[tuple(nav_links)] += 1
    footer_signatures[tuple(footer_links)] += 1

print(f"stage25 nav audit: {len(pages)} documents; {len(nav_signatures)} nav signatures; {len(footer_signatures)} footer signatures")
print(f"stage25 pages missing core nav links: {len(missing)}")
for rt, lang, absent, current in missing:
    print(f"NAV {rt} [{lang}] missing={','.join(absent)} current={','.join(current)}")

print("stage25 most common nav signatures:")
for sig, count in nav_signatures.most_common(12):
    print(f"  {count}x :: {' | '.join(sig)}")
print("stage25 most common footer signatures:")
for sig, count in footer_signatures.most_common(12):
    print(f"  {count}x :: {' | '.join(sig)}")
