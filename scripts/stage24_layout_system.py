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

class_re = re.compile(r'class=["\']([^"\']+)["\']', re.I)

def class_tokens(html: str) -> set[str]:
    out = set()
    for class_value in class_re.findall(html):
        out.update(class_value.split())
    return out

max_values = Counter()
changed = 0
classic_container = 0
intl_container = 0
with_shared_shell = 0
without_shared_shell = []
class_counter = Counter()

for path in html_files:
    html = path.read_text(encoding="utf-8")
    for value in re.findall(r"--max\s*:\s*([^;}]+)", html):
        max_values[value.strip()] += 1
    for value in re.findall(r"--imax\s*:\s*([^;}]+)", html):
        max_values[f"intl:{value.strip()}"] += 1

    tokens = class_tokens(html)
    has_classic = "container" in tokens
    has_intl = "intl-container" in tokens
    if has_classic:
        classic_container += 1
    if has_intl:
        intl_container += 1
    if has_classic or has_intl:
        with_shared_shell += 1
    else:
        without_shared_shell.append(str(path.relative_to(root)))
        for cls in tokens:
            class_counter[cls] += 1

    if 'data-stage24-layout="true"' not in html:
        html = html.replace("</head>", link + "\n</head>", 1)
        path.write_text(html, encoding="utf-8")
        changed += 1

missing = []
for path in html_files:
    html = path.read_text(encoding="utf-8")
    if 'data-stage24-layout="true"' not in html:
        missing.append(str(path.relative_to(root)))
if missing:
    raise SystemExit("stage24: layout stylesheet missing from: " + ", ".join(missing[:10]))

allowed_no_shell = {"404.html"}
regressions = []
for rel in without_shared_shell:
    name = Path(rel).name
    if rel in allowed_no_shell or name.startswith(("google", "yandex_")):
        continue
    regressions.append(rel)
if regressions:
    raise SystemExit("stage24: substantive page without shared shell (.container or .intl-container): " + ", ".join(regressions))

values = ", ".join(f"{k}×{v}" for k, v in sorted(max_values.items())) or "none"
skipped = ", ".join(skipped_stubs) if skipped_stubs else "none"
legacy = ", ".join(without_shared_shell) if without_shared_shell else "none"
common_classes = ", ".join(f"{k}×{v}" for k, v in class_counter.most_common(20)) or "none"
print(
    f"stage24 layout: {changed} HTML patched; shared shell {with_shared_shell} pages "
    f"(.container={classic_container}, .intl-container={intl_container}); original width vars: {values}; skipped stubs: {skipped}"
)
print(f"stage24 allowed utility pages without shared shell ({len(without_shared_shell)}): {legacy}")
print(f"stage24 non-shell common classes: {common_classes}")
print("stage24 shared shell invariant OK")
