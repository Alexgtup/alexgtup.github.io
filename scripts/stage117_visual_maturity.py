#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
BUNDLE = ROOT / "assets" / "stage105-final-ui.css"
SOURCE_CSS = Path(__file__).resolve().parents[1] / "assets" / "stage117-visual-maturity.css"
MARK = "/* stage117-visual-maturity */"

if not BUNDLE.is_file():
    raise SystemExit("stage117: final UI bundle missing")
if not SOURCE_CSS.is_file():
    raise SystemExit("stage117: visual maturity source CSS missing")

css = SOURCE_CSS.read_text(encoding="utf-8").strip()
if MARK not in css:
    raise SystemExit("stage117: source CSS marker missing")

text = BUNDLE.read_text(encoding="utf-8")
if MARK not in text:
    BUNDLE.write_text(text.rstrip() + "\n\n" + css + "\n", encoding="utf-8")

bundle_text = BUNDLE.read_text(encoding="utf-8")
digest = hashlib.sha256(bundle_text.encode("utf-8")).hexdigest()[:12]
href_re = re.compile(r"(/assets/stage105-final-ui\.css)\?v=[^\"']+", re.I)

pages = refs = 0
home_seen = cases_seen = service_seen = False
for path in sorted(ROOT.rglob("*.html")):
    html = path.read_text(encoding="utf-8", errors="ignore")
    if "<body" not in html:
        continue
    pages += 1
    home_seen = home_seen or 'data-page="home"' in html
    cases_seen = cases_seen or 'data-page="cases"' in html
    service_seen = service_seen or 'data-ux-family="service"' in html
    new, count = href_re.subn(rf"\1?v={digest}", html)
    refs += count
    if new != html:
        path.write_text(new, encoding="utf-8")

problems: list[str] = []
for required in (".portfolio-showcase__layout", ".portfolio-carousel__grid", ".project-radar__filters", ".stage109-case-diagram"):
    if required not in bundle_text:
        problems.append(f"missing visual maturity rule: {required}")
if not home_seen:
    problems.append("home marker not found")
if not cases_seen:
    problems.append("cases marker not found")
if not service_seen:
    problems.append("service family marker not found")
if refs < 70:
    problems.append(f"only {refs} final UI references rotated")
if problems:
    raise SystemExit("stage117 visual maturity failed:\n" + "\n".join(problems))

print(f"stage117 visual maturity: pages={pages}; cache_refs={refs}; bundle={digest}; editorial art direction applied")
