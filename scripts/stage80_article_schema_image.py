#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
IMAGE = {
    "@type": "ImageObject",
    "url": "https://alexgtup.github.io/assets/og/alexuys-default.jpg",
    "width": 1200,
    "height": 630,
}
SCRIPT_RE = re.compile(
    r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    flags=re.IGNORECASE | re.DOTALL,
)


def has_type(value, expected: str) -> bool:
    if isinstance(value, str):
        return value == expected
    if isinstance(value, list):
        return expected in value
    return False


def patch_node(node) -> int:
    changed = 0
    if isinstance(node, dict):
        if has_type(node.get("@type"), "Article") and not node.get("image"):
            node["image"] = dict(IMAGE)
            changed += 1
        for value in node.values():
            changed += patch_node(value)
    elif isinstance(node, list):
        for value in node:
            changed += patch_node(value)
    return changed


def patch_html(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    article_count = 0
    changed_count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal article_count, changed_count
        raw = match.group(2).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"stage80: invalid JSON-LD in {path}: {exc}")

        def count_articles(node) -> int:
            if isinstance(node, dict):
                count = 1 if has_type(node.get("@type"), "Article") else 0
                return count + sum(count_articles(v) for v in node.values())
            if isinstance(node, list):
                return sum(count_articles(v) for v in node)
            return 0

        article_count += count_articles(data)
        changed = patch_node(data)
        changed_count += changed
        if not changed:
            return match.group(0)
        payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        return f"{match.group(1)}{payload}{match.group(3)}"

    patched = SCRIPT_RE.sub(repl, text)
    if changed_count:
        path.write_text(patched, encoding="utf-8")
    return article_count, changed_count


pages = sorted((ROOT / "guides").glob("*/index.html")) + sorted((ROOT / "en" / "guides").glob("*/index.html"))
total_articles = 0
total_changed = 0
article_pages = 0

for page in pages:
    articles, changed = patch_html(page)
    if articles:
        article_pages += 1
        total_articles += articles
        total_changed += changed

# Hard guard: every Article in guide pages must now expose a valid image object.
for page in pages:
    text = page.read_text(encoding="utf-8")
    for match in SCRIPT_RE.finditer(text):
        data = json.loads(match.group(2).strip())

        def verify(node) -> None:
            if isinstance(node, dict):
                if has_type(node.get("@type"), "Article"):
                    image = node.get("image")
                    if not isinstance(image, dict) or image.get("url") != IMAGE["url"]:
                        raise SystemExit(f"stage80: Article image guard failed in {page}")
                for value in node.values():
                    verify(value)
            elif isinstance(node, list):
                for value in node:
                    verify(value)

        verify(data)

if article_pages == 0:
    raise SystemExit("stage80: no Article guide pages found")

print(
    f"stage80: Article image schema guarded on {article_pages} guide pages; "
    f"articles={total_articles}; patched={total_changed}"
)
