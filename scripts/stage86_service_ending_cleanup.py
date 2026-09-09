#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

MAIN_RE = re.compile(r"<main\b[^>]*>.*?</main>", re.I | re.S)
CONTACT_RE = re.compile(
    r"\s*<section\b[^>]*class=[\"'][^\"']*\bs48-contact\b[^\"']*[\"'][^>]*>.*?</section>\s*",
    re.I | re.S,
)
AUX_RE = re.compile(
    r"\s*<section\b[^>]*class=[\"'][^\"']*\b(?:s66-tool-link|s68-entry)\b[^\"']*[\"'][^>]*>.*?</section>\s*",
    re.I | re.S,
)
DIRECT_RE = re.compile(r"https://t\.me/Alexuys|mailto:alexgtup@gmail\.com", re.I)

service_dirs = [
    "telegram-bots", "web-development", "n8n-automation", "api-integrations",
    "project-repair", "app-development", "ai-automation", "crm-development",
    "ios-development", "telegram-mini-apps", "python-development",
    "backend-development", "mvp-development", "development",
]

changed: list[str] = []
moved = 0

for name in service_dirs:
    path = root / name / "index.html"
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    mm = MAIN_RE.search(text)
    if not mm:
        raise SystemExit(f"stage86: missing <main>: {name}")
    main = mm.group(0)
    original = main
    contact_matches = list(CONTACT_RE.finditer(main))
    if not contact_matches:
        continue

    contact = contact_matches[-1]
    tail = main[contact.end():]
    aux_after = list(AUX_RE.finditer(tail))
    if aux_after:
        # Keep the service-specific tool/product recommendation, but place it before
        # the shared contact surface so every service page ends the same way.
        aux_html = "\n".join(m.group(0).strip() for m in aux_after)
        for m in reversed(aux_after):
            absolute_start = contact.end() + m.start()
            absolute_end = contact.end() + m.end()
            main = main[:absolute_start] + "\n" + main[absolute_end:]
        # Contact positions may have changed only after it, so its original start is stable.
        contact_again = list(CONTACT_RE.finditer(main))[-1]
        main = main[:contact_again.start()] + "\n" + aux_html + "\n" + main[contact_again.start():]
        moved += len(aux_after)

    if main != original:
        text = text[:mm.start()] + main + text[mm.end():]
        path.write_text(text, encoding="utf-8")
        changed.append(name)

problems: list[str] = []
for name in service_dirs:
    path = root / name / "index.html"
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    mm = MAIN_RE.search(text)
    if not mm:
        continue
    main = mm.group(0)
    contacts = list(CONTACT_RE.finditer(main))
    if not contacts:
        continue
    contact = contacts[-1]
    if AUX_RE.search(main[contact.end():]):
        problems.append(f"{name}: auxiliary block remains after contact")
    # Contact is expected to remain the last substantive section and retain a direct action.
    if not DIRECT_RE.search(contact.group(0)):
        problems.append(f"{name}: contact lost direct action")
    section_starts = list(re.finditer(r"<section\b", main, re.I))
    if section_starts and section_starts[-1].start() != contact.start() + len(contact.group(0)) - len(contact.group(0).lstrip()):
        # Avoid brittle whitespace offsets: compare the final opening tag location instead.
        last_contact_open = main.find("<section", contact.start())
        if section_starts[-1].start() != last_contact_open:
            problems.append(f"{name}: s48-contact is not final section")

if problems:
    raise SystemExit("stage86 service ending invariant failed: " + "; ".join(problems))

print(f"stage86 service endings: changed={len(changed)}; auxiliary blocks moved before contact={moved}")
if changed:
    print("stage86 normalized pages: " + ", ".join(changed))
