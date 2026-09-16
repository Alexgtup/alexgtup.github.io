#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
TODAY = "2026-09-16"
BASE = "https://alexgtup.github.io"

PAGES = {
    "/": {
        "title": "Разработчик Telegram-ботов, CRM, n8n и API | Alexuys",
        "description": "Разработка Telegram-ботов, CRM, n8n/Make-автоматизаций, API и веб-сервисов. Реальные кейсы, прямой контакт с разработчиком, запуск и доработка проектов.",
    },
    "/n8n-automation/": {
        "title": "n8n автоматизация на заказ - CRM, Telegram, API | Alexuys",
        "description": "Настройка n8n и Make под реальные процессы: CRM, Telegram, формы, таблицы, API, webhooks и уведомления. Workflow, тестирование, запуск и доработка.",
    },
    "/telegram-bots/": {
        "title": "Telegram-бот на заказ - разработка, CRM, API, оплаты | Alexuys",
        "description": "Разработка Telegram-ботов: заявки, оплаты, CRM, API, уведомления, личные кабинеты и Mini Apps. Реальные кейсы, запуск и доработка существующих ботов.",
    },
}


def page_path(route: str) -> Path:
    return ROOT / ("index.html" if route == "/" else route.strip("/") + "/index.html")


def replace_meta(html: str, name: str, value: str) -> str:
    patterns = [
        rf'<meta\s+content="[^"]*"\s+name="{re.escape(name)}"\s*/?>',
        rf'<meta\s+name="{re.escape(name)}"\s+content="[^"]*"\s*/?>',
    ]
    replacement = f'<meta content="{value}" name="{name}"/>'
    for pattern in patterns:
        if re.search(pattern, html, flags=re.I):
            return re.sub(pattern, replacement, html, count=1, flags=re.I)
    raise SystemExit(f"stage106: meta {name} missing")


def replace_property(html: str, prop: str, value: str) -> str:
    patterns = [
        rf'<meta\s+content="[^"]*"\s+property="{re.escape(prop)}"\s*/?>',
        rf'<meta\s+property="{re.escape(prop)}"\s+content="[^"]*"\s*/?>',
    ]
    replacement = f'<meta content="{value}" property="{prop}"/>'
    for pattern in patterns:
        if re.search(pattern, html, flags=re.I):
            return re.sub(pattern, replacement, html, count=1, flags=re.I)
    raise SystemExit(f"stage106: property {prop} missing")


changed = []
for route, data in PAGES.items():
    path = page_path(route)
    if not path.is_file():
        raise SystemExit(f"stage106: page missing {route}")
    html = path.read_text(encoding="utf-8")
    old = html
    if not re.search(r"<title>.*?</title>", html, flags=re.I | re.S):
        raise SystemExit(f"stage106: title missing {route}")
    html = re.sub(r"<title>.*?</title>", f'<title>{data["title"]}</title>', html, count=1, flags=re.I | re.S)
    html = replace_meta(html, "description", data["description"])
    html = replace_property(html, "og:title", data["title"])
    html = replace_property(html, "og:description", data["description"])
    html = replace_meta(html, "twitter:title", data["title"])
    html = replace_meta(html, "twitter:description", data["description"])
    if html != old:
        path.write_text(html, encoding="utf-8")
        changed.append(route)

sitemap = ROOT / "sitemap.xml"
xml = sitemap.read_text(encoding="utf-8")
for route in changed:
    loc = BASE + route
    pattern = re.compile(rf'(<url>.*?<loc>{re.escape(loc)}</loc>.*?</url>)', re.S)
    m = pattern.search(xml)
    if not m:
        raise SystemExit(f"stage106: sitemap entry missing {loc}")
    block = m.group(1)
    if "<lastmod>" in block:
        block2 = re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{TODAY}</lastmod>", block, count=1)
    else:
        block2 = block.replace(f"<loc>{loc}</loc>", f"<loc>{loc}</loc><lastmod>{TODAY}</lastmod>", 1)
    xml = xml[:m.start(1)] + block2 + xml[m.end(1):]
sitemap.write_text(xml, encoding="utf-8")

for route, data in PAGES.items():
    html = page_path(route).read_text(encoding="utf-8")
    if html.count(data["title"]) < 3:
        raise SystemExit(f"stage106: title surfaces not synchronized for {route}")
    if data["description"] not in html:
        raise SystemExit(f"stage106: description guard failed for {route}")

print("stage106 search CTR: " + ", ".join(changed))

# Publish the missing WordPress commercial entry after the shared build has
# normalized the existing site. The new page is self-contained and the stage
# also creates its sitemap entry plus contextual inbound links.
subprocess.run(
    [sys.executable, str(Path(__file__).with_name("stage107_wordpress_landing.py")), str(ROOT)],
    check=True,
)
