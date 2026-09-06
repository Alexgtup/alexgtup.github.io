#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

assets = (
    "/assets/site-enhancements.css",
    "/assets/site-enhancements.js",
    "/assets/layout-system.css",
    "/assets/universal-media.css",
    "/assets/search-intent.css",
    "/assets/international.css",
)

versions: dict[str, str] = {}
for public_path in assets:
    target = root / public_path.lstrip("/")
    if target.is_file():
        digest = hashlib.sha256(target.read_bytes()).hexdigest()[:12]
        versions[public_path] = digest

if not versions:
    raise SystemExit("stage41: no shared assets found")

changed_pages = 0
for page in root.rglob("*.html"):
    text = page.read_text(encoding="utf-8", errors="ignore")
    original = text
    for public_path, digest in versions.items():
        # Source templates intentionally keep clean asset URLs. At build time we append
        # a content-derived version so a changed CSS/JS file cannot be paired with stale
        # browser/CDN cache from the previous deployment.
        pattern = re.escape(public_path) + r"(?:\?v=[A-Za-z0-9._-]+)?"
        text = re.sub(pattern, f"{public_path}?v={digest}", text)
    if text != original:
        page.write_text(text, encoding="utf-8")
        changed_pages += 1

print("stage41 asset fingerprints:")
for public_path, digest in versions.items():
    print(f"  {public_path}?v={digest}")
print(f"  HTML pages updated: {changed_pages}")
