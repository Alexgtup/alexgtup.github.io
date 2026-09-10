#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html as H
import json
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
BASE = "https://alexgtup.github.io"
PERSON_ID = BASE + "/#person"
DATE = "2026-09-10"
SAME_AS = [
    "https://github.com/Alexgtup",
    "https://freelance.ru/gglalex",
    "https://t.me/Alexuys",
]
OLD_VISIBLE_NAMES = ("Александр Александров", "Alexandr Alexandrov")


def walk(value, english: bool) -> None:
    if isinstance(value, list):
        for item in value:
            walk(item, english)
        return
    if not isinstance(value, dict):
        return

    typ = value.get("@type")
    types = typ if isinstance(typ, list) else [typ]
    name = value.get("name")
    url = value.get("url")
    developer_person = (
        "Person" in types
        and (
            value.get("@id") == PERSON_ID
            or name in {"Александр", "Alexander", "Alexuys", "gglalex"}
            or (isinstance(url, str) and url.rstrip("/").endswith("/about"))
        )
    )
    if developer_person:
        value["@id"] = PERSON_ID
        value["name"] = "Alexander" if english else "Александр"
        value["alternateName"] = ["Alexuys", "gglalex", "Alexander", "Александр"]
        current = value.get("sameAs", [])
        if not isinstance(current, list):
            current = [current]
        value["sameAs"] = list(dict.fromkeys([x for x in current + SAME_AS if x]))

    for child in value.values():
        walk(child, english)


def normalize_jsonld(text: str, english: bool, rel: str) -> str:
    pattern = re.compile(
        r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
        re.I | re.S,
    )

    def repl(match: re.Match[str]) -> str:
        raw = match.group(2).strip()
        try:
            obj = json.loads(raw)
        except Exception as exc:
            raise SystemExit(f"stage104: invalid JSON-LD in {rel}: {exc}")
        walk(obj, english)
        return match.group(1) + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + match.group(3)

    return pattern.sub(repl, text)


def canonical_url(text: str) -> str | None:
    match = re.search(r'<link\b[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', text, re.I)
    if not match:
        match = re.search(r'<link\b[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', text, re.I)
    return H.unescape(match.group(1)).strip() if match else None


changed_pages: set[str] = set()
fresh_pages: set[str] = set()
CONTENT_ROUTES = {"/", "/about/", "/services/", "/freelance-developer/", "/project-repair/", "/mvp-development/"}
modified_html = 0
checked = 0
for path in ROOT.rglob("*.html"):
    rel = path.relative_to(ROOT).as_posix()
    if rel == "404.html" or rel.startswith(("google", "yandex")):
        continue
    text = path.read_text(encoding="utf-8", errors="strict")
    old = text
    english = rel.startswith("en/")
    body_before = text.split("</head>", 1)[1] if "</head>" in text else text
    body_before = re.sub(r"<(script|style)\b.*?</\1>", "", body_before, flags=re.I | re.S)
    visible_identity_change = any(name in body_before for name in OLD_VISIBLE_NAMES)

    text = text.replace("Александр Александров", "Александр")
    text = text.replace("Alexandr Alexandrov", "Alexander")
    text = normalize_jsonld(text, english, rel)

    if text != old:
        path.write_text(text, encoding="utf-8")
        modified_html += 1
        canonical = canonical_url(text)
        if canonical and canonical.startswith(BASE):
            changed_pages.add(canonical)
            route = re.sub(r"^https://alexgtup\.github\.io", "", canonical) or "/"
            if visible_identity_change or route in CONTENT_ROUTES:
                fresh_pages.add(canonical)
    checked += 1

sitemap_path = ROOT / "sitemap.xml"
if not sitemap_path.is_file():
    raise SystemExit("stage104: sitemap.xml missing")
sitemap = sitemap_path.read_text(encoding="utf-8")
lastmod_updates = 0
for url in sorted(fresh_pages):
    pattern = re.compile(rf'(<loc>{re.escape(url)}</loc>\s*<lastmod>)[^<]+(</lastmod>)')
    sitemap, count = pattern.subn(rf'\g<1>{DATE}\g<2>', sitemap, count=1)
    if count:
        lastmod_updates += 1
sitemap_path.write_text(sitemap, encoding="utf-8")

all_user_html = []
for path in ROOT.rglob("*.html"):
    rel = path.relative_to(ROOT).as_posix()
    if rel == "404.html" or rel.startswith(("google", "yandex")):
        continue
    all_user_html.append(path.read_text(encoding="utf-8"))
joined = "\n".join(all_user_html)
for stale in OLD_VISIBLE_NAMES:
    if stale in joined:
        raise SystemExit(f"stage104: stale developer identity remains: {stale}")

home = (ROOT / "index.html").read_text(encoding="utf-8")
if PERSON_ID not in home or '"name":"Александр"' not in home:
    raise SystemExit("stage104: canonical homepage Person entity missing")

pattern = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
for path in ROOT.rglob("*.html"):
    rel = path.relative_to(ROOT).as_posix()
    if rel == "404.html" or rel.startswith(("google", "yandex")):
        continue
    text = path.read_text(encoding="utf-8")
    english = rel.startswith("en/")
    expected = "Alexander" if english else "Александр"
    for raw in pattern.findall(text):
        try:
            obj = json.loads(raw.strip())
        except Exception as exc:
            raise SystemExit(f"stage104: JSON-LD parse guard failed in {rel}: {exc}")
        stack = [obj]
        while stack:
            item = stack.pop()
            if isinstance(item, list):
                stack.extend(item)
            elif isinstance(item, dict):
                typ = item.get("@type")
                types = typ if isinstance(typ, list) else [typ]
                if "Person" in types and item.get("@id") == PERSON_ID and item.get("name") != expected:
                    raise SystemExit(
                        f"stage104: inconsistent canonical Person name in {rel}: {item.get('name')!r} != {expected!r}"
                    )
                stack.extend(item.values())

print(
    f"stage104 entity consistency: checked={checked}; modified_html={modified_html}; "
    f"entity_changed_pages={len(changed_pages)}; fresh_sitemap_pages={len(fresh_pages)}; lastmod_updated={lastmod_updates}; "
    f"canonical_person={PERSON_ID}"
)
