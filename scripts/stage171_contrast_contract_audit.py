#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    vals = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    vals = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in vals]
    return .2126 * vals[0] + .7152 * vals[1] + .0722 * vals[2]


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)

pairs = {
    "light heading": ("#171914", "#f2efe8", 4.5),
    "light body": ("#555c53", "#ffffff", 4.5),
    "dark heading": ("#f3f6f4", "#0d1115", 4.5),
    "dark case CTA": ("#f3f6f4", "#0b1015", 4.5),
    "lime button": ("#071008", "#c9ff4a", 4.5),
}
for label, (fg, bg, minimum) in pairs.items():
    value = contrast(fg, bg)
    if value < minimum:
        raise SystemExit(f"stage171: {label} contrast {value:.2f} < {minimum}")

sitemap = ROOT / "sitemap.xml"
if not sitemap.is_file():
    raise SystemExit("stage171: sitemap missing")
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = []
for loc in ET.parse(sitemap).findall(".//s:loc", ns):
    value = (loc.text or "").strip()
    if not value.startswith("https://alexgtup.github.io"):
        continue
    rel = value.removeprefix("https://alexgtup.github.io").strip("/")
    if rel == "en" or rel.startswith("en/"):
        continue
    urls.append((ROOT / rel / "index.html") if rel else (ROOT / "index.html"))

for path in urls:
    if not path.is_file():
        raise SystemExit(f"stage171: sitemap page missing {path}")
    text = path.read_text(encoding="utf-8")
    if "stage167-component-theme-pairs" not in text:
        raise SystemExit(f"stage171: theme pairs missing {path}")
    if "stage167-final-design-system" in text:
        raise SystemExit(f"stage171: old global stage167 remains {path}")
    if "stage168-final-specificity-guard" in text:
        raise SystemExit(f"stage171: global specificity guard remains {path}")
    if "stage146-seo-depth.css" in text:
        raise SystemExit(f"stage171: legacy depth CSS remains {path}")
    if "stage170-case-about-contrast" in text:
        raise SystemExit(f"stage171: obsolete about recolor remains {path}")

case_checks = [
    "cases/auto-crm/index.html",
    "cases/taxi-app/index.html",
    "cases/factory-catalog/index.html",
    "cases/seo-control-center/index.html",
    "cases/siteaudit-studio/index.html",
    "cases/freelance-os/index.html",
]
for rel in case_checks:
    text = (ROOT / rel).read_text(encoding="utf-8")
    if "stage170-case-contrast" not in text:
        raise SystemExit(f"stage171: case contrast layer missing {rel}")

print(f"stage171 contrast contract: {len(urls)} RU sitemap pages, {len(pairs)} contrast pairs OK")
