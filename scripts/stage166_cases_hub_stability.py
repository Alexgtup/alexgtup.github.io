#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
PAGE = ROOT / "cases" / "index.html"
MARKER = "stage166-cases-hub-stability"

if not PAGE.is_file():
    raise SystemExit("stage166: cases hub missing")

html = PAGE.read_text(encoding="utf-8")
html = re.sub(
    r'<script\b[^>]*src=["\'][^"\']*stage145-cases-gallery-interactive\.js[^"\']*["\'][^>]*>\s*</script>',
    '', html, flags=re.I,
)
html = re.sub(
    r'<link\b[^>]*href=["\'][^"\']*stage145-cases-gallery-interactive\.css[^"\']*["\'][^>]*>',
    '', html, flags=re.I,
)
html = re.sub(r'<style\s+id=["\']stage166-cases-hub-stability["\']>.*?</style>', '', html, flags=re.I | re.S)

STYLE = r'''<style id="stage166-cases-hub-stability">
main.p130-hub[data-stage130-hub="cases"] :is(.x145-cases-webgl,.x145-liquid-lens,.x145-index-mark,.x145-index-caption){
  display:none!important;position:absolute!important;width:0!important;height:0!important;
  min-width:0!important;min-height:0!important;margin:0!important;padding:0!important;pointer-events:none!important;
}
main.p130-hub[data-stage130-hub="cases"] .p130-hero{
  min-height:0!important;height:auto!important;padding:clamp(42px,4vw,64px) 0 clamp(52px,5vw,76px)!important;
  transform:none!important;translate:none!important;
}
main.p130-hub[data-stage130-hub="cases"] .p130-list-section{
  min-height:0!important;height:auto!important;padding:0 0 clamp(80px,7vw,112px)!important;
  transform:none!important;translate:none!important;
}
main.p130-hub[data-stage130-hub="cases"] .p130-list-section>.p130-shell,
main.p130-hub[data-stage130-hub="cases"] .p130-mosaic{
  position:relative!important;inset:auto!important;margin-top:0!important;transform:none!important;translate:none!important;
}
@media(max-width:980px){main.p130-hub[data-stage130-hub="cases"] .p130-hero{padding:36px 0 52px!important;}}
</style>'''

if "</head>" not in html:
    raise SystemExit("stage166: head missing")
html = html.replace("</head>", STYLE + "</head>", 1)
PAGE.write_text(html, encoding="utf-8")

final = PAGE.read_text(encoding="utf-8")
if final.count(MARKER) != 1:
    raise SystemExit("stage166: marker count invalid")
if "stage145-cases-gallery-interactive.js" in final or "stage145-cases-gallery-interactive.css" in final:
    raise SystemExit("stage166: legacy stage145 remains")
if 'data-stage130-hub="cases"' not in final or 'class="p130-mosaic"' not in final:
    raise SystemExit("stage166: cases DOM guard failed")

print("stage166 cases hub stability: legacy WebGL removed, flow guarded")
for script in (
    "stage172_search_expansion.py",
    "stage173_growth_consolidation.py",
    "stage167_final_design_system.py",
    "stage169_retire_legacy_depth_theme.py",
    "stage170_case_about_contrast.py",
    "stage171_contrast_contract_audit.py",
):
    subprocess.run([sys.executable, str(Path(__file__).with_name(script)), str(ROOT)], check=True)
