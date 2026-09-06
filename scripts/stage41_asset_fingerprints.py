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
# competitor-gap patch here so it is part of the same validated pipeline without
# duplicating another fragile workflow entry. The child flag prevents recursion:
# Stage 42 calls this script once more after changing CSS, and that child run only
# fingerprints the final assets.
if os.environ.get("ALEXUYS_STAGE42_CHILD") != "1":
    stage42 = Path(__file__).with_name("stage42_runner.py")
    if stage42.is_file():
        env = os.environ.copy()
        env["ALEXUYS_STAGE42_CHILD"] = "1"
        subprocess.check_call([sys.executable, str(stage42), str(root)], env=env)

    # Normalize final public claims against the directly verifiable Freelance.ru
    # profile and install referral tracking after all commercial patches have run.
    stage43 = Path(__file__).with_name("stage43_freelance_sync.py")
    if stage43.is_file():
        subprocess.check_call([sys.executable, str(stage43), str(root)])

    # Rebuild the two highest-level decision pages after all older growth patches.
    # This deliberately replaces accumulated homepage/service fragments with one
    # coherent user journey, then improves information scent on core service pages.
    stage44 = Path(__file__).with_name("stage44_experience_rebuild.py")
    if stage44.is_file():
        subprocess.check_call([sys.executable, str(stage44), str(root)])

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
