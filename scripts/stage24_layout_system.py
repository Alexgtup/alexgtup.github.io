#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
link = '<link href="/assets/layout-system.css" rel="stylesheet" data-stage24-layout="true"/>'

all_html = sorted(root.rglob("*.html"))
if not all_html:
    raise SystemExit("stage24: no HTML files found")

# Search-engine verification stubs can be plain text wrapped in an .html file.
# Only real documents with a closing </head> participate in layout normalization.
html_files = []
skipped_stubs = []
for path in all_html:
    html = path.read_text(encoding="utf-8")
    if "</head>" not in html:
        skipped_stubs.append(str(path.relative_to(root)))
        continue
    html_files.append(path)

if not html_files:
    raise SystemExit("stage24: no full HTML documents found")

max_values = Counter()
changed = 0
with_container = 0
without_container = []
class_counter = Counter()
container_re = re.compile(r'class=["\'][^"\']*\bcontainer\b[^"\']*["\']', re.I)
class_re = re.compile(r'class=["\']([^"\']+)["\']', re.I)

for path in html_files:
    html = path.read_text(encoding="utf-8")
    for value in re.findall(r"--max\s*:\s*([^;}]+)", html):
        max_values[value.strip()] += 1

    if container_re.search(html):
        with_container += 1
    else:
        without_container.append(str(path.relative_to(root)))
        # Count classes on legacy templates to identify their shared shell names.
        for class_value in class_re.findall(html):
            for cls in class_value.split():
                class_counter[cls] += 1

    if 'data-stage24-layout="true"' in html:
        continue
    html = html.replace("</head>", link + "\n</head>", 1)
    path.write_text(html, encoding="utf-8")
    changed += 1

# Production safety: every real HTML document must load the shared geometry layer.
missing = []
for path in html_files:
    html = path.read_text(encoding="utf-8")
    if 'data-stage24-layout="true"' not in html:
        missing.append(str(path.relative_to(root)))
if missing:
    raise SystemExit("stage24: layout stylesheet missing from: " + ", ".join(missing[:10]))

values = ", ".join(f"{k}×{v}" for k, v in sorted(max_values.items())) or "none"
skipped = ", ".join(skipped_stubs) if skipped_stubs else "none"
legacy = ", ".join(without_container) if without_container else "none"
common_classes = ", ".join(f"{k}×{v}" for k, v in class_counter.most_common(20)) or "none"
print(f"stage24 layout: {changed} HTML patched; {with_container} pages use .container; original --max values: {values}; skipped stubs: {skipped}")
print(f"stage24 legacy pages without .container ({len(without_container)}): {legacy}")
print(f"stage24 legacy common classes: {common_classes}")
