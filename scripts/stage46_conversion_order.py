#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
routes = (
    "telegram-bots/index.html",
    "web-development/index.html",
    "n8n-automation/index.html",
    "project-repair/index.html",
)

contact_re = re.compile(
    r'<section\b(?=[^>]*class="[^"]*\bcontact\b[^"]*")[^>]*>.*?</section>',
    re.S | re.I,
)

changed = []
for rel in routes:
    path = root / rel
    if not path.is_file():
        raise SystemExit(f"stage46: missing {rel}")
    text = path.read_text(encoding="utf-8")
    matches = list(contact_re.finditer(text))
    if len(matches) != 1:
        raise SystemExit(f"stage46: expected exactly one contact section in {rel}, got {len(matches)}")
    contact = matches[0].group(0)
    # If already the final section, keep the build idempotent.
    tail = text[matches[0].end():text.find('</main>', matches[0].end())]
    if '<section' not in tail:
        continue
    text = text[:matches[0].start()] + text[matches[0].end():]
    marker = '</main>'
    if marker not in text:
        raise SystemExit(f"stage46: </main> missing in {rel}")
    text = text.replace(marker, contact + '\n' + marker, 1)
    path.write_text(text, encoding="utf-8")
    changed.append('/' + rel.replace('index.html',''))

print('stage46 contact order:', ', '.join(changed) if changed else 'already final')
