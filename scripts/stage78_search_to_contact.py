#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
TARGETS = [
    "/demos/",
    "/freelance-os/",
    "/tools/",
    "/tools/json-formatter/",
    "/tools/utm-builder/",
    "/tools/cron-builder/",
    "/tools/jwt-decoder/",
    "/tools/robots-validator/",
    "/tools/sitemap-validator/",
]
LINK = '<a href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer" data-contact="telegram">Обсудить задачу в Telegram ↗</a>'


def page(route: str) -> Path:
    return root / route.strip("/") / "index.html"

patched = []
for route in TARGETS:
    p = page(route)
    if not p.is_file():
        raise SystemExit(f"stage78: missing {route}")
    text = p.read_text(encoding="utf-8")

    # Work only inside the final Stage77 section so the organic visitor always
    # has a direct next action at the actual end of the page.
    sections = list(re.finditer(r'<section\b[^>]*class=["\'][^"\']*s77-section[^"\']*["\'][^>]*>.*?</section>', text, flags=re.I | re.S))
    if not sections:
        raise SystemExit(f"stage78: no Stage77 section on {route}")
    last = sections[-1]
    section = last.group(0)
    if 'https://t.me/Alexuys' not in section:
        if 'class="s77-links"' in section:
            section = section.replace('</div></section>', LINK + '</div></section>', 1)
        else:
            section = section.replace('</section>', f'<div class="s77-links">{LINK}</div></section>', 1)
        text = text[:last.start()] + section + text[last.end():]
        p.write_text(text, encoding="utf-8")
        patched.append(route)

    final = p.read_text(encoding="utf-8")
    sections = list(re.finditer(r'<section\b[^>]*class=["\'][^"\']*s77-section[^"\']*["\'][^>]*>.*?</section>', final, flags=re.I | re.S))
    if not sections or 'https://t.me/Alexuys' not in sections[-1].group(0):
        raise SystemExit(f"stage78: final contact invariant failed {route}")

print(f"stage78: direct final contact guarded on {len(TARGETS)} search/product pages; patched={len(patched)}")
