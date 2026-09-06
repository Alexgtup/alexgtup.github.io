#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
link = '<link href="/assets/layout-system.css" rel="stylesheet" data-stage24-layout="true"/>'

html_files = sorted(root.rglob("*.html"))
if not html_files:
    raise SystemExit("stage24: no HTML files found")

max_values = Counter()
changed = 0
with_container = 0

for path in html_files:
    html = path.read_text(encoding="utf-8")
    for value in re.findall(r"--max\s*:\s*([^;}]+)", html):
        max_values[value.strip()] += 1

    if 'class="container' in html or ' container"' in html or " container'" in html:
        with_container += 1

    if 'data-stage24-layout="true"' in html:
        continue
    if "</head>" not in html:
        raise SystemExit(f"stage24: </head> missing in {path.relative_to(root)}")
    html = html.replace("</head>", link + "\n</head>", 1)
    path.write_text(html, encoding="utf-8")
    changed += 1

# Production safety: every HTML document must load the shared geometry layer.
missing = []
for path in html_files:
    html = path.read_text(encoding="utf-8")
    if 'data-stage24-layout="true"' not in html:
        missing.append(str(path.relative_to(root)))
if missing:
    raise SystemExit("stage24: layout stylesheet missing from: " + ", ".join(missing[:10]))

values = ", ".join(f"{k}×{v}" for k, v in sorted(max_values.items())) or "none"
print(f"stage24 layout: {changed} HTML patched; {with_container} pages use .container; original --max values: {values}")
