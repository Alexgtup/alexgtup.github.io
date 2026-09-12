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

# The old hero still contains decorative CRM/phone/chat markup for graceful fallback,
# but the final art layer hides it and displays real project imagery instead. Keep
# the accessible label truthful to what visitors now see.
home_path = ROOT / "index.html"
if not home_path.is_file():
    raise SystemExit("stage117: home page missing")
home = home_path.read_text(encoding="utf-8")
old_label = 'aria-label="Визуализация цифровых продуктов: CRM, мобильное приложение и Telegram-бот" class="product-stage"'
new_label = 'aria-label="Реальные интерфейсы проектов Fin Planner и Swift Calendar" class="product-stage"'
if old_label in home:
    home = home.replace(old_label, new_label, 1)
elif new_label not in home:
    raise SystemExit("stage117: homepage product-stage label not found")
home_path.write_text(home, encoding="utf-8")

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
for required in (
    ".portfolio-showcase__layout",
    ".portfolio-carousel__grid",
    ".project-radar__filters",
    ".stage109-case-diagram",
    ".product-stage::before",
    "fin-planner-original.webp",
    "calendar-original.webp",
):
    if required not in bundle_text:
        problems.append(f"missing visual maturity rule: {required}")
final_home = home_path.read_text(encoding="utf-8")
if new_label not in final_home:
    problems.append("real-project hero label missing")
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

print(f"stage117 visual maturity: pages={pages}; cache_refs={refs}; bundle={digest}; editorial art direction + real project hero applied")
