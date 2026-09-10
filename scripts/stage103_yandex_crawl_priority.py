#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
BASE = "https://alexgtup.github.io"

RU_HUBS = {
    "/services/", "/cases/", "/guides/", "/freelance-developer/", "/about/"
}
RU_SERVICES = {
    "/development/", "/app-development/", "/telegram-bots/", "/telegram-mini-apps/",
    "/telegram-bot-repair/", "/n8n-automation/", "/ai-automation/", "/crm-development/",
    "/web-development/", "/api-integrations/", "/project-repair/", "/python-development/",
    "/backend-development/", "/mvp-development/", "/ios-development/"
}

# Extra crawl bridges only where the final graph still had weak commercial pages.
BRIDGES = {
    "/services/": [
        ("Telegram Mini App", "/telegram-mini-apps/"),
        ("Доработка Telegram-бота", "/telegram-bot-repair/"),
    ],
    "/project-repair/": [
        ("Отдельно: доработка Telegram-бота", "/telegram-bot-repair/"),
    ],
    "/mvp-development/": [
        ("MVP внутри Telegram Mini App", "/telegram-mini-apps/"),
    ],
}

COOKIE_REPLACEMENTS = {
    "Метрика учитывает посещения и переходы только с вашего согласия. Вебвизор отключён.":
        "Метрика учитывает посещения, переходы и взаимодействия на странице только с вашего согласия. После разрешения может использоваться Вебвизор для записи взаимодействий.",
    "Yandex Metrica measures visits and link clicks only with your consent. Session recording is disabled.":
        "Yandex Metrica measures visits, link clicks and page interactions only with your consent. After you allow analytics, session interaction recording may be used.",
    "Яндекс Метрика помогает понять, какие страницы полезны и откуда приходят посетители. Счётчик включится только после вашего согласия. Вебвизор отключён.":
        "Яндекс Метрика помогает понять, какие страницы полезны и откуда приходят посетители. Счётчик и Вебвизор включаются только после вашего согласия.",
    "Яндекс Метрика включается только после согласия пользователя. Вебвизор отключён. Аналитика используется для понимания посещаемости и взаимодействия с сайтом.":
        "Яндекс Метрика и Вебвизор включаются только после согласия пользователя. Аналитика используется для понимания посещаемости, переходов и взаимодействия с интерфейсом.",
    "Yandex Metrica is enabled only after user consent. Session recording is disabled.":
        "Yandex Metrica and session interaction recording are enabled only after user consent.",
}


def route_path(route: str) -> Path:
    return ROOT / ("index.html" if route == "/" else route.strip("/") + "/index.html")


def priority_for(url: str) -> str:
    path = urlparse(url).path or "/"
    if path == "/":
        return "1.0"
    if path in RU_HUBS:
        return "0.95"
    if path in RU_SERVICES:
        return "0.90"
    if path.startswith("/cases/"):
        return "0.80"
    if path.startswith("/guides/"):
        return "0.75"
    if path == "/demos/" or path == "/freelance-os/":
        return "0.70"
    if path.startswith("/tools/") or path == "/tools/":
        return "0.60"
    if path.startswith("/en/") or path == "/en/":
        return "0.55"
    return "0.65"


def patch_sitemap() -> int:
    path = ROOT / "sitemap.xml"
    if not path.is_file():
        raise SystemExit("stage103: sitemap.xml missing")
    text = path.read_text(encoding="utf-8")
    count = 0

    def patch(match: re.Match[str]) -> str:
        nonlocal count
        block = match.group(0)
        loc = re.search(r"<loc>([^<]+)</loc>", block)
        if not loc:
            return block
        url = loc.group(1).strip()
        if not url.startswith(BASE):
            return block
        value = priority_for(url)
        block = re.sub(r"\s*<priority>[^<]*</priority>", "", block)
        lm = re.search(r"</lastmod>", block)
        if lm:
            block = block[:lm.end()] + f"<priority>{value}</priority>" + block[lm.end():]
        else:
            loc_end = block.find("</loc>") + len("</loc>")
            block = block[:loc_end] + f"<priority>{value}</priority>" + block[loc_end:]
        count += 1
        return block

    text = re.sub(r"<url>.*?</url>", patch, text, flags=re.S)
    path.write_text(text, encoding="utf-8")
    return count


def insert_bridge(route: str, links: list[tuple[str, str]]) -> bool:
    path = route_path(route)
    if not path.is_file():
        raise SystemExit(f"stage103: missing bridge source {route}")
    text = path.read_text(encoding="utf-8")
    marker = f'data-stage103-yandex-links="{route.strip("/") or "home"}"'
    if marker in text:
        return False

    anchors = "".join(f'<a href="{href}">{label}</a>' for label, href in links)
    block = (
        f'<nav class="s101-more s103-discovery" {marker} '
        'aria-label="Связанные страницы">'
        f'{anchors}</nav>'
    )

    patterns = [
        r'<section\b[^>]*class="[^"]*\bs48-contact\b[^"]*"[^>]*>',
        r'<section\b[^>]*\bid="contact"[^>]*>',
        r'<section\b[^>]*class="[^"]*\bs64-conversion\b[^"]*"[^>]*>',
        r'</main>',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            text = text[:match.start()] + block + "\n" + text[match.start():]
            path.write_text(text, encoding="utf-8")
            return True
    raise SystemExit(f"stage103: no insertion point for {route}")


def sync_consent_copy() -> int:
    changed = 0
    for path in ROOT.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        new = text
        for old, replacement in COOKIE_REPLACEMENTS.items():
            new = new.replace(old, replacement)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def inbound_sources(target: str) -> int:
    sources = set()
    needle = f'href="{target}"'
    for path in ROOT.rglob("*.html"):
        if path.name != "index.html":
            continue
        text = path.read_text(encoding="utf-8")
        if needle in text:
            sources.add(path.relative_to(ROOT).as_posix())
    return len(sources)


sitemap_urls = patch_sitemap()
bridge_changes = sum(insert_bridge(route, links) for route, links in BRIDGES.items())
consent_pages = sync_consent_copy()

# Guard the exact production state we need for Yandex discovery and consent-aware analytics.
sitemap_text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
if sitemap_urls < 70:
    raise SystemExit(f"stage103: unexpectedly few sitemap URLs patched: {sitemap_urls}")
if "<priority>1.0</priority>" not in sitemap_text or "<priority>0.90</priority>" not in sitemap_text:
    raise SystemExit("stage103: sitemap priority invariant failed")

for target in ("/telegram-bot-repair/", "/telegram-mini-apps/"):
    sources = inbound_sources(target)
    if sources < 3:
        raise SystemExit(f"stage103: weak commercial inbound graph remains for {target}: {sources}")

all_html = "\n".join(
    p.read_text(encoding="utf-8") for p in ROOT.rglob("*.html") if p.name == "index.html"
)
if "Вебвизор отключён" in all_html or "Session recording is disabled" in all_html:
    raise SystemExit("stage103: stale analytics consent copy remains")

analytics = (ROOT / "assets/analytics.js").read_text(encoding="utf-8")
for required in ("webvisor: true", "trackLinks: true", "consent !== 'accepted'"):
    if required not in analytics:
        raise SystemExit(f"stage103: analytics invariant missing: {required}")

print(
    f"stage103 Yandex: sitemap priorities={sitemap_urls}; bridge pages={bridge_changes}; "
    f"consent copy pages={consent_pages}; telegram-bot-repair inbound={inbound_sources('/telegram-bot-repair/')}; "
    f"telegram-mini-apps inbound={inbound_sources('/telegram-mini-apps/')}"
)
