#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage169-legacy-depth-retired"
STAMP = '<meta name="stage169-legacy-depth-retired" content="true">'
changed=[]

for path in sorted(ROOT.rglob("index.html")):
    rel=path.relative_to(ROOT).as_posix()
    if rel.startswith("en/"):
        continue
    text=path.read_text(encoding="utf-8")
    before=text
    text=re.sub(r'<link\b[^>]*href=["\'][^"\']*stage146-seo-depth\.css[^"\']*["\'][^>]*>','',text,flags=re.I)
    text=re.sub(r'<meta\s+name=["\']stage169-legacy-depth-retired["\'][^>]*>','',text,flags=re.I)
    if "</head>" in text:
        text=text.replace("</head>",STAMP+"</head>",1)
    if text!=before:
        path.write_text(text,encoding="utf-8")
        changed.append(rel)

for rel in ["cases/index.html","services/index.html","guides/index.html","api-integrations/index.html"]:
    text=(ROOT/rel).read_text(encoding="utf-8")
    if "stage146-seo-depth.css" in text:
        raise SystemExit(f"stage169: legacy depth css remains in {rel}")
    if MARKER not in text:
        raise SystemExit(f"stage169: marker missing in {rel}")
    if 'class="x146-depth"' in text and "stage167-component-theme-pairs" not in text:
        raise SystemExit(f"stage169: component theme pairs missing in {rel}")

print(f"stage169 legacy depth theme retired: {len(changed)} pages touched")
