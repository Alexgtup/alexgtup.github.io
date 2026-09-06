#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib
import os
import re
import subprocess
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def normalize_hero_opening_tag(path: Path) -> None:
    """Put the hero class first so downstream build patches do not depend on source attribute order."""
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r'<section(?P<before>[^>]*?)class="(?P<classes>[^"]*\bhero\b[^"]*)"(?P<after>[^>]*)>', re.I)
    match = pattern.search(text)
    if not match:
        return
    classes = match.group("classes")
    replacement = f'<section class="{classes}"{match.group("before")}{match.group("after")}>'
    text = text[:match.start()] + replacement + text[match.end():]
    path.write_text(text, encoding="utf-8")


# Stage 40 already calls this finalization step on every production build. Run the
# competitor-gap patch here so it is part of the same validated pipeline without
# duplicating another fragile workflow entry. Normalize hero attribute order first:
# some service sources use `class="hero container"`, others put class after aria attrs.
# The child flag prevents recursion when Stage 42 fingerprints its final CSS.
if os.environ.get("ALEXUYS_STAGE42_CHILD") != "1":
    for route in ("telegram-bots", "n8n-automation", "project-repair", "web-development"):
        normalize_hero_opening_tag(root / route / "index.html")
    stage42 = Path(__file__).with_name("stage42_competitor_gap.py")
    if stage42.is_file():
        env = os.environ.copy()
        env["ALEXUYS_STAGE42_CHILD"] = "1"
        subprocess.check_call([sys.executable, str(stage42), str(root)], env=env)

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
