#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def route(path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "index.html": return "/"
    if rel.endswith("/index.html"): return "/" + rel[:-10]
    return "/" + rel

rows = []
patterns = Counter()
for path in sorted(root.rglob("*.html")):
    html = path.read_text(encoding="utf-8")
    if "</head>" not in html or path.name.startswith(("google", "yandex_")): continue
    rt = route(path)
    if rt in ("/", "/404.html") or rt.startswith("/en/"): continue
    main_m = re.search(r'<main\b[^>]*>(.*?)</main>', html, re.I|re.S)
    if not main_m: continue
    main = main_m.group(1)
    sections = list(re.finditer(r'<section\b([^>]*)>', main, re.I|re.S))
    if not sections: continue
    last = sections[-1]
    attrs = last.group(1)
    class_m = re.search(r'class=["\']([^"\']*)["\']', attrs, re.I)
    classes = class_m.group(1).strip() if class_m else "(none)"
    # Slice from final section to end of main. This is enough for conversion-link checks.
    tail = main[last.start():]
    has_tg = 'https://t.me/Alexuys' in tail
    has_mail = 'mailto:alexgtup@gmail.com' in tail
    has_container = bool(re.search(r'\bcontainer\b', attrs)) or bool(re.search(r'<div\b[^>]*class=["\'][^"\']*\bcontainer\b', tail, re.I))
    patterns[(classes, has_container, has_tg, has_mail)] += 1
    rows.append((rt, classes, has_container, has_tg, has_mail))

print(f"stage27 endings audit: {len(rows)} RU internal page endings")
print("stage27 ending patterns:")
for (classes, container, tg, mail), count in patterns.most_common():
    print(f"  {count}x class={classes!r} shell={int(container)} telegram={int(tg)} mail={int(mail)}")

print("stage27 endings without shared shell:")
for rt, classes, container, tg, mail in rows:
    if not container:
        print(f"  {rt} :: class={classes!r} telegram={int(tg)} mail={int(mail)}")

print("stage27 endings without direct contact action:")
for rt, classes, container, tg, mail in rows:
    if not tg and not mail and rt not in ("/privacy/",):
        print(f"  {rt} :: class={classes!r}")
