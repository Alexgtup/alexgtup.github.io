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
LINK = '<a class="s78-contact-link" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer" data-contact="telegram">Обсудить задачу в Telegram ↗</a>'
STYLE = '''<style data-stage78-contact-css="true">
.s77-section[data-stage78-contact="true"] .s77-links{align-items:center;margin-top:1.2rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,.08)}
.s77-section[data-stage78-contact="true"] .s78-contact-link{margin-left:auto;background:#c9ff4a;border-color:#c9ff4a;color:#090a0b;font-weight:850;text-decoration:none!important;box-shadow:none}
.s77-section[data-stage78-contact="true"] .s78-contact-link:hover{border-color:#d9ff7c;background:#d9ff7c;text-decoration:none!important}
@media(max-width:640px){.s77-section[data-stage78-contact="true"] .s77-links{gap:.5rem}.s77-section[data-stage78-contact="true"] .s78-contact-link{order:-1;width:100%;min-height:2.9rem;margin-left:0;align-items:center;justify-content:center;text-align:center}}
</style>'''


def page(route: str) -> Path:
    return root / route.strip("/") / "index.html"


patched = []
for route in TARGETS:
    p = page(route)
    if not p.is_file():
        raise SystemExit(f"stage78: missing {route}")
    text = p.read_text(encoding="utf-8")

    if 'data-stage78-contact-css="true"' not in text:
        if "</head>" not in text:
            raise SystemExit(f"stage78: no head on {route}")
        text = text.replace("</head>", STYLE + "\n</head>", 1)

    # Work only inside the final Stage77 section so the organic visitor always
    # has a direct next action at the actual end of the page. Keep the useful
    # explanatory content and secondary internal links; only the contact action
    # receives primary visual weight.
    sections = list(re.finditer(r'<section\b[^>]*class=["\'][^"\']*s77-section[^"\']*["\'][^>]*>.*?</section>', text, flags=re.I | re.S))
    if not sections:
        raise SystemExit(f"stage78: no Stage77 section on {route}")
    last = sections[-1]
    section = last.group(0)

    opening_end = section.find(">")
    opening = section[: opening_end + 1]
    if 'data-stage78-contact="true"' not in opening:
        opening = opening[:-1] + ' data-stage78-contact="true">'
        section = opening + section[opening_end + 1 :]

    if 'https://t.me/Alexuys' not in section:
        if 'class="s77-links"' in section:
            section = section.replace('</div></section>', LINK + '</div></section>', 1)
        else:
            section = section.replace('</section>', f'<div class="s77-links">{LINK}</div></section>', 1)
    elif 'class="s78-contact-link"' not in section:
        section = re.sub(
            r'<a\b([^>]*href=["\']https://t\.me/Alexuys["\'][^>]*)>',
            r'<a class="s78-contact-link"\1>',
            section,
            count=1,
            flags=re.I,
        )

    updated = text[: last.start()] + section + text[last.end() :]
    if updated != p.read_text(encoding="utf-8"):
        p.write_text(updated, encoding="utf-8")
        patched.append(route)

    final = p.read_text(encoding="utf-8")
    sections = list(re.finditer(r'<section\b[^>]*class=["\'][^"\']*s77-section[^"\']*["\'][^>]*>.*?</section>', final, flags=re.I | re.S))
    if not sections:
        raise SystemExit(f"stage78: final section missing {route}")
    last_section = sections[-1].group(0)
    opening = last_section.split(">", 1)[0]
    if (
        'data-stage78-contact="true"' not in opening
        or 'https://t.me/Alexuys' not in last_section
        or 'class="s78-contact-link"' not in last_section
        or 'data-stage78-contact-css="true"' not in final
    ):
        raise SystemExit(f"stage78: final contact hierarchy invariant failed {route}")

print(f"stage78: direct final contact hierarchy guarded on {len(TARGETS)} search/product pages; patched={len(patched)}")
