#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
BUNDLE = ROOT / "assets" / "stage105-final-ui.css"
ASSET_ROOT = Path(__file__).resolve().parents[1] / "assets"
ART_LAYERS = (
    (ASSET_ROOT / "stage117-visual-maturity.css", "/* stage117-visual-maturity"),
    (ASSET_ROOT / "stage118-real-work.css", "/* stage118-real-work"),
    (ASSET_ROOT / "stage119-case-editorial.css", "/* stage119-case-editorial"),
)

if not BUNDLE.is_file():
    raise SystemExit("stage117: final UI bundle missing")

text = BUNDLE.read_text(encoding="utf-8")
for source, marker in ART_LAYERS:
    if not source.is_file():
        raise SystemExit(f"stage117: art-direction source missing: {source.name}")
    css = source.read_text(encoding="utf-8").strip()
    if marker not in css:
        raise SystemExit(f"stage117: source marker missing: {source.name}")
    if marker not in text:
        text = text.rstrip() + "\n\n" + css + "\n"
BUNDLE.write_text(text, encoding="utf-8")

bundle_text = BUNDLE.read_text(encoding="utf-8")
digest = hashlib.sha256(bundle_text.encode("utf-8")).hexdigest()[:12]
href_re = re.compile(r"(/assets/stage105-final-ui\.css)\?v=[^\"']+", re.I)

pages = refs = 0
home_seen = cases_seen = service_seen = case_family_seen = False
for path in sorted(ROOT.rglob("*.html")):
    html = path.read_text(encoding="utf-8", errors="ignore")
    if "<body" not in html:
        continue
    pages += 1
    home_seen = home_seen or 'data-page="home"' in html
    cases_seen = cases_seen or 'data-page="cases"' in html
    service_seen = service_seen or 'data-ux-family="service"' in html
    case_family_seen = case_family_seen or 'data-ux-family="case"' in html
    new, count = href_re.subn(rf"\1?v={digest}", html)
    refs += count
    if new != html:
        path.write_text(new, encoding="utf-8")

problems: list[str] = []
for required in (
    ".portfolio-showcase__layout",
    ".portfolio-carousel__grid",
    ".project-radar__filters",
    ".stage109-case-diagram",
    ".s44-hero__visual",
    ".s44-proofline",
    ".s113-review-card",
    ".s48-system__top",
    ".s114-proofbar",
    ".s51-implemented",
    ".s51-related",
    ".s51-contact-card",
):
    if required not in bundle_text:
        problems.append(f"missing visual maturity rule: {required}")
if not home_seen:
    problems.append("home marker not found")
if not cases_seen:
    problems.append("cases marker not found")
if not service_seen:
    problems.append("service family marker not found")
if not case_family_seen:
    problems.append("case family marker not found")
if refs < 70:
    problems.append(f"only {refs} final UI references rotated")
if problems:
    raise SystemExit("stage117 visual maturity failed:\n" + "\n".join(problems))

print(f"stage117 visual maturity: pages={pages}; cache_refs={refs}; bundle={digest}; home/service/case editorial art direction applied")
