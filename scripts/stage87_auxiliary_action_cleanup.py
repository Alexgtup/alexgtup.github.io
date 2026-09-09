#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

MAIN_RE = re.compile(r"<main\b[^>]*>.*?</main>", re.I | re.S)
SECTION_RE = re.compile(r"<section\b[^>]*>.*?</section>", re.I | re.S)
AUX_CLASS_RE = re.compile(r"\b(?:s68-entry|s66-tool-link)\b", re.I)
TELEGRAM_ANCHOR_RE = re.compile(
    r"\s*<a\b[^>]*href=[\"']https://t\.me/Alexuys[^\"']*[\"'][^>]*>.*?</a>\s*",
    re.I | re.S,
)
DIRECT_RE = re.compile(r"https://t\.me/Alexuys|mailto:alexgtup@gmail\.com", re.I)

changed: list[str] = []
removed = 0

for path in sorted(root.rglob("*.html")):
    text = path.read_text(encoding="utf-8")
    mm = MAIN_RE.search(text)
    if not mm:
        continue
    main = mm.group(0)
    original = main
    sections = list(SECTION_RE.finditer(main))

    # Work backwards so offsets of earlier sections stay stable after replacement.
    for index in range(len(sections) - 1, -1, -1):
        sec = sections[index]
        block = sec.group(0)
        opening = block[: block.find(">") + 1]
        if not AUX_CLASS_RE.search(opening) or not TELEGRAM_ANCHOR_RE.search(block):
            continue

        later = main[sec.end():]
        # The product/tool card should not compete with a later explicit contact.
        # If there is no later direct action, it may itself be the page's final CTA.
        if not DIRECT_RE.search(later):
            continue

        cleaned, count = TELEGRAM_ANCHOR_RE.subn("", block)
        if not count:
            continue
        main = main[:sec.start()] + cleaned + main[sec.end():]
        removed += count
        sections = list(SECTION_RE.finditer(main))

    if main != original:
        text = text[:mm.start()] + main + text[mm.end():]
        path.write_text(text, encoding="utf-8")
        changed.append(path.relative_to(root).as_posix())

# Invariant: no auxiliary recommendation may contain Telegram if another direct
# contact action appears later in the same main content.
problems: list[str] = []
for path in sorted(root.rglob("*.html")):
    text = path.read_text(encoding="utf-8")
    mm = MAIN_RE.search(text)
    if not mm:
        continue
    main = mm.group(0)
    for sec in SECTION_RE.finditer(main):
        block = sec.group(0)
        opening = block[: block.find(">") + 1]
        if AUX_CLASS_RE.search(opening) and TELEGRAM_ANCHOR_RE.search(block) and DIRECT_RE.search(main[sec.end():]):
            problems.append(path.relative_to(root).as_posix())
            break

if problems:
    raise SystemExit("stage87 auxiliary action invariant failed: " + ", ".join(problems))

print(f"stage87 auxiliary actions: removed duplicate Telegram links={removed}; changed pages={len(changed)}")
if changed:
    print("stage87 cleaned pages: " + ", ".join(changed))
