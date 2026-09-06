#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
page = root / "index.html"
if not page.is_file():
    raise SystemExit("stage37: homepage not found")

html = page.read_text(encoding="utf-8")
old = '<a class="skip-link" href="#content">Перейти к содержанию</a>'
new = '<a class="skip-link" href="#main-content">Перейти к содержанию</a>'

if old in html:
    html = html.replace(old, new, 1)
elif new not in html:
    raise SystemExit("stage37: expected homepage skip-link not found")

if 'id="main-content"' not in html:
    raise SystemExit("stage37: #main-content target missing")

page.write_text(html, encoding="utf-8")
print("stage37 accessibility patch: homepage skip-link -> #main-content")
