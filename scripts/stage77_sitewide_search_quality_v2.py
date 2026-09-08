#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from html.parser import HTMLParser
import re
import sys
import xml.etree.ElementTree as ET

# Reuse the Stage77 patch section exactly as authored, but replace its regex-based
# final audit with an attribute-order-independent HTML parser.
source = Path(__file__).with_name("stage77_sitewide_search_quality.py")
raw = source.read_text(encoding="utf-8")
marker = "# ---- Site-wide final audit: every sitemap page must satisfy the same core invariants. ----"
if marker not in raw:
    raise SystemExit("stage77-v2: audit marker missing in Stage77 source")
prefix = raw.split(marker, 1)[0]
namespace = {"__name__": "stage77_patch", "__file__": str(source)}
exec(compile(prefix, str(source), "exec"), namespace)

root: Path = namespace["root"]
BASE: str = namespace["BASE"]

sitemap = root / "sitemap.xml"
if not sitemap.is_file():
    raise SystemExit("stage77-v2: sitemap.xml missing")
tree = ET.parse(sitemap)
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
locs = [(n.text or "").strip() for n in tree.findall(".//s:loc", ns) if (n.text or "").strip()]
if len(locs) != 74 or len(set(locs)) != 74:
    raise SystemExit(f"stage77-v2: expected 74 unique sitemap URLs, got {len(locs)}/{len(set(locs))}")


def route_from_url(url: str) -> str:
    if url == BASE + "/":
        return "/"
    return "/" + url.split(BASE + "/", 1)[1].strip("/") + "/"


def html_path(route: str) -> Path:
    return root / "index.html" if route == "/" else root / route.strip("/") / "index.html"


def category(route: str) -> str:
    if route == "/":
        return "home"
    if route.startswith("/en/cases/") and route != "/en/cases/":
        return "en_case"
    if route.startswith("/en/guides/") and route != "/en/guides/":
        return "en_guide"
    if route.startswith("/en/") and route not in ("/en/", "/en/about/", "/en/services/", "/en/cases/", "/en/guides/"):
        return "en_service"
    if route.startswith("/tools/") and route != "/tools/":
        return "tool"
    if route.startswith("/cases/") and route != "/cases/":
        return "case"
    if route.startswith("/guides/") and route != "/guides/":
        return "guide"
    if route in ("/services/", "/cases/", "/guides/", "/about/", "/demos/", "/tools/", "/freelance-developer/", "/en/", "/en/about/", "/en/services/", "/en/cases/", "/en/guides/"):
        return "hub"
    return "service"


MIN_WORDS = {
    "home": 350,
    "service": 280,
    "case": 250,
    "guide": 300,
    "tool": 220,
    "hub": 160,
    "en_case": 180,
    "en_guide": 250,
    "en_service": 220,
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.h1_parts: list[list[str]] = []
        self.main_parts: list[str] = []
        self.description = ""
        self.canonical = ""
        self.robots = ""
        self.internal_links: set[str] = set()
        self._title = False
        self._h1_depth = 0
        self._main_depth = 0
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs = {str(k).lower(): (v or "") for k, v in attrs_list}
        if tag in ("script", "style"):
            self._skip_depth += 1
        if tag == "title":
            self._title = True
        if tag == "h1":
            self._h1_depth += 1
            self.h1_parts.append([])
        if tag == "main":
            self._main_depth += 1
        if tag == "meta":
            name = attrs.get("name", "").lower()
            if name == "description":
                self.description = attrs.get("content", "").strip()
            elif name == "robots":
                self.robots = attrs.get("content", "").strip().lower()
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonical = attrs.get("href", "").strip()
        if tag == "a":
            href = attrs.get("href", "").strip()
            if href.startswith("/") and not href.startswith("//"):
                clean = href.split("#", 1)[0].split("?", 1)[0]
                if clean:
                    self.internal_links.add(clean)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._title = False
        if tag == "h1" and self._h1_depth:
            self._h1_depth -= 1
        if tag == "main" and self._main_depth:
            self._main_depth -= 1
        if tag in ("script", "style") and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        value = re.sub(r"\s+", " ", data).strip()
        if not value:
            return
        if self._title:
            self.title_parts.append(value)
        if self._h1_depth and self.h1_parts:
            self.h1_parts[-1].append(value)
        if self._main_depth:
            self.main_parts.append(value)

    @property
    def title(self) -> str:
        return " ".join(self.title_parts).strip()

    @property
    def h1s(self) -> list[str]:
        return [" ".join(parts).strip() for parts in self.h1_parts]

    @property
    def main_text(self) -> str:
        return " ".join(self.main_parts).strip()


seen_title: dict[str, str] = {}
seen_desc: dict[str, str] = {}
seen_h1: dict[str, str] = {}
report: list[tuple[str, str, int, int, int, int]] = []

for url in locs:
    route = route_from_url(url)
    p = html_path(route)
    if not p.is_file():
        raise SystemExit(f"stage77-v2: sitemap target missing: {route}")
    parser = PageParser()
    parser.feed(p.read_text(encoding="utf-8"))

    if not parser.title or not parser.description or len(parser.h1s) != 1 or not parser.canonical or not parser.robots:
        raise SystemExit(
            f"stage77-v2: core metadata invariant failed {route}: "
            f"title={bool(parser.title)} desc={bool(parser.description)} h1={len(parser.h1s)} "
            f"canonical={bool(parser.canonical)} robots={bool(parser.robots)}"
        )

    title = parser.title
    desc = parser.description
    h1 = parser.h1s[0]
    words = len(re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", parser.main_text))
    links = len(parser.internal_links)
    kind = category(route)

    if parser.canonical != url:
        raise SystemExit(f"stage77-v2: canonical mismatch {route}: {parser.canonical} != {url}")
    if "noindex" in parser.robots:
        raise SystemExit(f"stage77-v2: sitemap page is noindex: {route}")
    if not (25 <= len(title) <= 80):
        raise SystemExit(f"stage77-v2: title length {len(title)}: {route}: {title}")
    if not (100 <= len(desc) <= 190):
        raise SystemExit(f"stage77-v2: description length {len(desc)}: {route}")
    if links < 4:
        raise SystemExit(f"stage77-v2: too few internal links ({links}): {route}")
    minimum = MIN_WORDS[kind]
    if words < minimum:
        raise SystemExit(f"stage77-v2: thin page {route}: {words} < {minimum} words")

    for store, value, label in (
        (seen_title, title, "title"),
        (seen_desc, desc, "description"),
        (seen_h1, h1, "h1"),
    ):
        key = value.casefold()
        if key in store:
            raise SystemExit(f"stage77-v2: duplicate {label}: {route} == {store[key]}: {value}")
        store[key] = route

    report.append((route, kind, words, links, len(title), len(desc)))

changed = namespace.get("changed", set())
print(f"stage77-v2: audited {len(report)} sitemap pages; changed {len(changed)} pages")
for route, kind, words, links, tl, dl in sorted(report):
    print(f"stage77 OK {route} type={kind} words={words} links={links} title={tl} desc={dl}")
