#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage169-legacy-depth-retired"

STAMP = '<meta name="stage169-legacy-depth-retired" content="true">'
changed = []

for path in sorted(ROOT.rglob("index.html")):
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("en/"):
        continue
    text = path.read_text(encoding="utf-8")
    before = text

    # The old stylesheet intentionally paints Stage130 discovery sections as
    # light paper. The final stage167/168 system now owns the same component,
    # so keeping both only creates specificity conflicts.
    text = re.sub(
        r'<link\b[^>]*href=["\'][^"\']*stage146-seo-depth\.css[^"\']*["\'][^>]*>',
        '',
        text,
        flags=re.I,
    )

    text = re.sub(
        r'<meta\s+name=["\']stage169-legacy-depth-retired["\'][^>]*>',
        '',
        text,
        flags=re.I,
    )
    if "</head>" in text:
        text = text.replace("</head>", STAMP + "</head>", 1)

    if text != before:
        path.write_text(text, encoding="utf-8")
        changed.append(rel)

for rel in [
    "cases/index.html",
    "services/index.html",
    "guides/index.html",
    "api-integrations/index.html",
]:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"stage169: missing {rel}")
    text = path.read_text(encoding="utf-8")
    if "stage146-seo-depth.css" in text:
        raise SystemExit(f"stage169: legacy depth css remains in {rel}")
    if MARKER not in text:
        raise SystemExit(f"stage169: marker missing in {rel}")
    if 'class="x146-depth"' in text:
        if "stage167-final-design-system" not in text or "stage168-final-specificity-guard" not in text:
            raise SystemExit(f"stage169: final depth styling missing in {rel}")

print(f"stage169 legacy depth theme retired: {len(changed)} pages touched")
