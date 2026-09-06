#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
home = root / "index.html"
if not home.is_file():
    raise SystemExit("stage58: homepage missing")
home_before = hashlib.sha256(home.read_bytes()).hexdigest()

balanced = 0
cta_order = 0

# Four related links looked like 3 + 1 with the shared three-column rule.
# Keep the shared component untouched and balance only pages that actually have four links.
for route in ("api-integrations", "backend-development", "mvp-development"):
    page = root / route / "index.html"
    if not page.is_file():
        raise SystemExit(f"stage58: missing /{route}/")
    text = page.read_text(encoding="utf-8", errors="ignore")
    original = text

    # Only apply if this exact grid has four direct link cards in the current build.
    m = re.search(r'<div class="s48-related">(?P<body>.*?)</div>', text, flags=re.S | re.I)
    if m:
        links = len(re.findall(r'<a\b', m.group("body"), flags=re.I))
        if links == 4:
            text = text[:m.start()] + m.group(0).replace(
                'class="s48-related"', 'class="s48-related s58-related--four"', 1
            ) + text[m.end():]
            if "data-stage58-related" not in text:
                style = '<style data-stage58-related>.s58-related--four{grid-template-columns:repeat(2,minmax(0,1fr))}@media(max-width:820px){.s58-related--four{grid-template-columns:1fr}}</style>'
                pos = text.lower().find("</head>")
                if pos < 0:
                    raise SystemExit(f"stage58: /{route}/ missing </head>")
                text = text[:pos] + style + text[pos:]
            balanced += 1

    if text != original:
        page.write_text(text, encoding="utf-8")

# Stage 56 added the CRM comparison guide after the case's conversion block.
# Related reading should support the story before the final CTA, not continue after it.
page = root / "cases" / "auto-crm" / "index.html"
if page.is_file():
    text = page.read_text(encoding="utf-8", errors="ignore")
    pattern = re.compile(
        r'(?P<contact><section class="contact s51-contact".*?</section>)\s*'
        r'(?P<related><section class="section".*?href="/guides/custom-crm-or-ready/".*?</section>)',
        flags=re.S | re.I,
    )
    text, n = pattern.subn(lambda m: m.group("related") + "\n" + m.group("contact"), text, count=1)
    if n:
        page.write_text(text, encoding="utf-8")
        cta_order += 1

# Hard guard: project direction freezes the homepage.
home_after = hashlib.sha256(home.read_bytes()).hexdigest()
if home_after != home_before:
    raise SystemExit("stage58: homepage changed; forbidden")

# Guard the CRM case: no main section may follow the final contact section.
crm = root / "cases" / "auto-crm" / "index.html"
if crm.is_file():
    text = crm.read_text(encoding="utf-8", errors="ignore")
    main = re.search(r'<main\b.*?</main>', text, flags=re.S | re.I)
    if main:
        block = main.group(0)
        contact_end = block.rfind('</section>')
        contact_start = block.rfind('<section class="contact s51-contact"')
        if contact_start < 0 or contact_end < contact_start:
            raise SystemExit("stage58: auto-crm final contact section missing")
        tail = block[contact_end + len('</section>'):].strip()
        if tail and tail.lower() != '</main>':
            raise SystemExit("stage58: content remains after auto-crm final CTA")

# Guard the balanced route set.
for route in ("api-integrations", "backend-development", "mvp-development"):
    text = (root / route / "index.html").read_text(encoding="utf-8", errors="ignore")
    if 's58-related--four' not in text:
        raise SystemExit(f"stage58: four-card grid not balanced on /{route}/")

print("stage58 visual polish:")
print(f"  four-card related grids balanced: {balanced}")
print(f"  case CTA order restored: {cta_order}")
print(f"  homepage sha256 unchanged: {home_after}")
