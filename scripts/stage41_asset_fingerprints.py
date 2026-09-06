#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib
import os
import re
import subprocess
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

# Stage 40 already calls this finalization step on every production build. Run the
# commercial experience passes here so the final fingerprint is generated only
# after every shared CSS/HTML mutation has finished.
if os.environ.get("ALEXUYS_STAGE42_CHILD") != "1":
    stage42 = Path(__file__).with_name("stage42_runner.py")
    if stage42.is_file():
        env = os.environ.copy()
        env["ALEXUYS_STAGE42_CHILD"] = "1"
        subprocess.check_call([sys.executable, str(stage42), str(root)], env=env)

    for child in (
        "stage43_freelance_sync.py",
        "stage44_experience_rebuild.py",
        "stage45_home_anchor_fix.py",
        "stage46_conversion_order.py",
        "stage47_search_quality.py",
        "stage48_service_experience.py",
        "stage49_service_polish.py",
        "stage50_runner.py",
    ):
        target = Path(__file__).with_name(child)
        if target.is_file():
            subprocess.check_call([sys.executable, str(target), str(root)])

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
        pattern = re.escape(public_path) + r"(?:\?v=[A-Za-z0-9._-]+)?"
        text = re.sub(pattern, f"{public_path}?v={digest}", text)
    if text != original:
        page.write_text(text, encoding="utf-8")
        changed_pages += 1

print("stage41 asset fingerprints:")
for public_path, digest in versions.items():
    print(f"  {public_path}?v={digest}")
print(f"  HTML pages updated: {changed_pages}")
