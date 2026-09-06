#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

# Homepage skip-link target.
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

# Images already inside links/buttons are part of an existing interaction and must not
# become nested lightbox buttons or intercept navigation to a case/service page.
js = root / "assets" / "site-enhancements.js"
if not js.is_file():
    raise SystemExit("stage37: site-enhancements.js not found")
text = js.read_text(encoding="utf-8")
old_predicate = "return src && !src.startsWith('data:');"
new_predicate = "return src && !src.startsWith('data:') && !img.closest('a,button');"
if old_predicate in text:
    text = text.replace(old_predicate, new_predicate, 1)
elif new_predicate not in text:
    raise SystemExit("stage37: lightbox eligibility predicate not found")
js.write_text(text, encoding="utf-8")

print("stage37 accessibility/interactions: skip-link fixed; linked/button images excluded from lightbox")

# Stage 39 is chained here because the protected deployment workflow contains the
# IndexNow key and should not be rewritten just to add another build step.
stage39 = Path(__file__).with_name("stage39_growth_patch.py")
if not stage39.is_file():
    raise SystemExit("stage37: stage39 growth patch not found")
subprocess.run([sys.executable, str(stage39), str(root)], check=True)
