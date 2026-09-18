#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import shutil
import sys
import xml.etree.ElementTree as ET

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
BASE = "https://alexgtup.github.io"

EN_ANCHOR_RE = re.compile(
    r'<a\b(?=[^>]*\bhref\s*=\s*["\'](?:https://alexgtup\.github\.io)?/en(?:/[^"\']*)?["\'])[^>]*>.*?</a>\s*',
    re.I | re.S,
)
EN_ALT_RE = re.compile(
    r'<link\b(?=[^>]*\bhreflang\s*=\s*["\']en(?:-[^"\']*)?["\'])[^>]*>\s*',
    re.I,
)


def is_en_url(value: str) -> bool:
    value = value.strip()
    return value == BASE + "/en/" or value.startswith(BASE + "/en/")


def clean_sitemap(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    xhtml = "http://www.w3.org/1999/xhtml"
    ET.register_namespace("", ns)
    ET.register_namespace("xhtml", xhtml)
    tree = ET.parse(path)
    root = tree.getroot()
    removed_urls = 0
    removed_alts = 0
    for node in list(root):
        loc = node.find(f"{{{ns}}}loc")
        if loc is not None and is_en_url(loc.text or ""):
            root.remove(node)
            removed_urls += 1
            continue
        for child in list(node):
            if child.tag == f"{{{xhtml}}}link" and is_en_url(child.attrib.get("href", "")):
                node.remove(child)
                removed_alts += 1
    tree.write(path, encoding="utf-8", xml_declaration=True)
    return removed_urls, removed_alts


# Remove the published English tree entirely. Source files remain only as build
# inputs/history; the final GitHub Pages artifact contains no /en/* route.
en_root = ROOT / "en"
removed_en_files = 0
if en_root.exists():
    removed_en_files = sum(1 for p in en_root.rglob("*") if p.is_file())
    shutil.rmtree(en_root)

# Remove visible links and hreflang references to deleted English routes.
html_changed = 0
for path in sorted(ROOT.rglob("*.html")):
    text = path.read_text(encoding="utf-8")
    new = EN_ALT_RE.sub("", text)
    new = EN_ANCHOR_RE.sub("", new)
    if new != text:
        path.write_text(new, encoding="utf-8")
        html_changed += 1

# The mobile drawer used to create an EN link at runtime. Disable that branch in
# the final asset so no dead language switch can reappear client-side.
mobile_js = ROOT / "assets" / "site-enhancements.js"
if mobile_js.exists():
    text = mobile_js.read_text(encoding="utf-8")
    pattern = re.compile(
        r"\n\s*const englishMap = \{.*?\};\s*\n\s*const enLink = englishMap\[location\.pathname\] \? `.*?` : '';",
        re.S,
    )
    text, count = pattern.subn("\n  const enLink = '';", text, count=1)
    if count == 0 and "English version — EN" in text:
        raise SystemExit("stage163: mobile EN switch cleanup failed")
    mobile_js.write_text(text, encoding="utf-8")

# Remove English URLs and xhtml hreflang alternates from crawler discovery files.
removed_sitemap, removed_sitemap_alts = clean_sitemap(ROOT / "sitemap.xml")
removed_google, removed_google_alts = clean_sitemap(ROOT / "sitemap-google.xml")

for filename in ("sitemap.txt", "llms.txt"):
    path = ROOT / filename
    if not path.exists():
        continue
    lines = path.read_text(encoding="utf-8").splitlines()
    lines = [line for line in lines if BASE + "/en/" not in line]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

# sitemap.txt is only an alternate discovery representation of sitemap.xml.
# Regenerate it from the cleaned XML so late-added routes (for example
# wordpress-development) can never leave the two public sitemaps out of sync.
xml_path = ROOT / "sitemap.xml"
txt_path = ROOT / "sitemap.txt"
if xml_path.exists() and txt_path.exists():
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    seen = set()
    for loc in ET.parse(xml_path).findall(".//s:loc", ns):
        value = (loc.text or "").strip()
        if value and value not in seen:
            seen.add(value)
            urls.append(value)
    txt_path.write_text("\n".join(urls).rstrip() + "\n", encoding="utf-8")

# Keep the main feed purely Russian as well if an old EN entry was ever copied in.
feed = ROOT / "feed.xml"
if feed.exists():
    text = feed.read_text(encoding="utf-8")
    entry_re = re.compile(r"<entry\b.*?</entry>\s*", re.I | re.S)
    text = entry_re.sub(lambda m: "" if BASE + "/en/" in m.group(0) else m.group(0), text)
    feed.write_text(text, encoding="utf-8")

# Hard guards.
if (ROOT / "en").exists():
    raise SystemExit("stage163: /en directory still present")

bad_html = []
for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    if re.search(r'href\s*=\s*["\'](?:https://alexgtup\.github\.io)?/en(?:/|["\'])', text, re.I):
        bad_html.append(str(path))
    if re.search(r'hreflang\s*=\s*["\']en(?:-[^"\']*)?["\']', text, re.I):
        bad_html.append(str(path))
if bad_html:
    raise SystemExit("stage163: EN links remain: " + ", ".join(sorted(set(bad_html))[:8]))

for path in (ROOT / "sitemap.xml", ROOT / "sitemap-google.xml", ROOT / "sitemap.txt"):
    if path.exists() and BASE + "/en/" in path.read_text(encoding="utf-8"):
        raise SystemExit(f"stage163: EN URL remains in {path.name}")

if mobile_js.exists() and "English version — EN" in mobile_js.read_text(encoding="utf-8"):
    raise SystemExit("stage163: runtime English switch still present")

print(
    f"stage163 remove English: files={removed_en_files}, html={html_changed}, "
    f"sitemap_urls={removed_sitemap}, sitemap_alts={removed_sitemap_alts}, "
    f"google_urls={removed_google}, google_alts={removed_google_alts}"
)
