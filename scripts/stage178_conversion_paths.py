#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

PAGES = {
    "services/index.html": "Описать задачу и подобрать формат ↗",
    "cases/index.html": "Найти похожий кейс и обсудить ↗",
    "guides/index.html": "Получить ориентир по задаче ↗",
}

STYLE = """<style id="stage178-conversion-paths">
.stage178-route-note{display:flex;gap:18px;align-items:center;justify-content:space-between;margin:32px auto;padding:24px;border:1px solid rgba(20,25,18,.12);border-radius:24px;background:#f5f2ea}.stage178-route-note strong{font-size:20px;letter-spacing:-.03em}.stage178-route-note a{display:inline-flex;padding:12px 18px;border-radius:999px;background:#171914;color:white;text-decoration:none;font-size:14px}@media(max-width:700px){.stage178-route-note{display:block}.stage178-route-note a{margin-top:16px}}
</style>"""

for rel, cta in PAGES.items():
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"stage178: missing {rel}")
    html = path.read_text(encoding="utf-8")
    html = re.sub(r'<style id="stage178-conversion-paths">.*?</style>', '', html, flags=re.S)
    html = re.sub(r'<section class="stage178-route-note">.*?</section>', '', html, flags=re.S)
    if "</head>" not in html or "</main>" not in html:
        raise SystemExit(f"stage178: markers missing {rel}")
    html = html.replace("</head>", STYLE + "</head>", 1)
    block = f'<section class="stage178-route-note"><strong>Не нашли точный сценарий?</strong><a href="https://t.me/Alexuys">{cta}</a></section>'
    html = html.replace("</main>", block + "</main>", 1)
    path.write_text(html, encoding="utf-8")

print("stage178 conversion paths: services, cases and guides connected")
