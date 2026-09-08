#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
old = '@media(max-width:560px){.fos-card-preview__stats{grid-template-columns:1fr 1fr}.freelanceos-case-mini__rows{grid-template-columns:1fr 1fr}}'
new = '@media(max-width:560px){.fos-card-preview__stats{grid-template-columns:1fr 1fr}.freelanceos-case-mini__stats{grid-template-columns:1fr}.freelanceos-case-mini__rows{grid-template-columns:1fr 1fr}}'
patched = 0
for path in root.rglob('*.html'):
    body = path.read_text(encoding='utf-8')
    if 'freelanceos-integrated-style' not in body:
        continue
    if new in body:
        continue
    if old not in body:
        raise SystemExit(f'stage70: expected FreelanceOS responsive marker missing in {path.relative_to(root)}')
    path.write_text(body.replace(old, new, 1), encoding='utf-8')
    patched += 1

# Every page carrying the integration style must now include the mobile collapse.
for path in root.rglob('*.html'):
    body = path.read_text(encoding='utf-8')
    if 'freelanceos-integrated-style' in body and '.freelanceos-case-mini__stats{grid-template-columns:1fr}' not in body:
        raise SystemExit(f'stage70: mobile stats collapse missing in {path.relative_to(root)}')

print(f'stage70: FreelanceOS compact preview mobile collapse guarded on {patched} pages')