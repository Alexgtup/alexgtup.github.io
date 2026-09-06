#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

# Explicit dimensions keep layout stable and satisfy the production media invariant.
for route in ("telegram-bots", "app-development", "ios-development", "mvp-development"):
    p = root / route / "index.html"
    if not p.is_file():
        raise SystemExit(f"stage49: missing {p}")
    text = p.read_text(encoding="utf-8")
    text = re.sub(
        r'(<div class="s48-case__image"><img\s+src="[^"]+"\s+alt="[^"]+")(?![^>]*\bwidth=)',
        r'\1 width="720" height="900"',
        text,
        count=1,
        flags=re.I,
    )
    p.write_text(text, encoding="utf-8")


def add_related(route: str, href: str, title: str) -> None:
    p = root / route.strip("/") / "index.html"
    if not p.is_file():
        return
    text = p.read_text(encoding="utf-8")
    if f'href="{href}"' in text:
        return
    marker = '<div class="s48-related">'
    pos = text.find(marker)
    if pos < 0:
        return
    insert_at = pos + len(marker)
    link = f'<a href="{href}"><strong>{title}</strong><span>Открыть →</span></a>'
    text = text[:insert_at] + link + text[insert_at:]
    p.write_text(text, encoding="utf-8")

# Give weaker commercial pages more contextual inbound discovery paths.
add_related("/n8n-automation/", "/ai-automation/", "AI-автоматизация")
add_related("/api-integrations/", "/ai-automation/", "AI внутри workflow")
add_related("/development/", "/ai-automation/", "AI-автоматизация")
add_related("/development/", "/freelance-developer/", "Проверить исполнителя")
add_related("/project-repair/", "/freelance-developer/", "Фриланс-разработчик")
add_related("/web-development/", "/freelance-developer/", "Проверить профиль")

print("stage49 service polish: media dimensions + inbound discovery links")
