#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
js = root / "assets" / "site-enhancements.js"
if not js.is_file():
    raise SystemExit("stage38: site-enhancements.js not found")

text = js.read_text(encoding="utf-8")
old = "return src && !src.startsWith('data:');"
new = "return src && !src.startsWith('data:') && !img.closest('a,button');"

if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise SystemExit("stage38: lightbox eligibility predicate not found")

js.write_text(text, encoding="utf-8")
print("stage38 interaction patch: linked/button images excluded from lightbox")
