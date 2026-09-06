#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
home = root / "index.html"
if not home.is_file():
    raise SystemExit("stage57: homepage missing")
home_before = hashlib.sha256(home.read_bytes()).hexdigest()

SERVICE_ASSETS = (
    "/assets/universal-media.css",
    "/assets/site-enhancements.css",
)

SKIP_STYLE = """<style data-stage57-skip-link>\n.skip-link{position:fixed;left:12px;top:12px;z-index:10000;padding:.7rem .9rem;border-radius:.65rem;background:#c9ff4a;color:#08090b;font:800 .78rem/1.1 Inter,system-ui,sans-serif;text-decoration:none;transform:translateY(-180%);transition:transform .16s ease}.skip-link:focus{transform:translateY(0);outline:2px solid #08090b;outline-offset:2px}\n</style>"""

service_asset_repairs = 0
skip_repairs = 0
empty_paragraphs_removed = 0
heading_repairs = 0


def has_asset(text: str, public_path: str) -> bool:
    return re.search(re.escape(public_path) + r'(?:\?v=[A-Za-z0-9._-]+)?', text) is not None


def insert_before_layout_or_head(text: str, fragment: str) -> str:
    layout = re.search(r'<link\b[^>]*href=["\']/assets/layout-system\.css(?:\?v=[^"\']+)?["\'][^>]*>', text, flags=re.I)
    if layout:
        return text[:layout.start()] + fragment + "\n" + text[layout.start():]
    pos = text.lower().find("</head>")
    if pos < 0:
        raise SystemExit("stage57: page missing </head>")
    return text[:pos] + fragment + "\n" + text[pos:]


for page in root.rglob("*.html"):
    if page == home:
        continue
    text = page.read_text(encoding="utf-8", errors="ignore")
    original = text

    # Stage 48 components are styled in site-enhancements.css. Six legacy source
    # pages did not load that asset, which made the production HTML look unstyled.
    if re.search(r'class=["\'][^"\']*\bs48[-_]', text):
        missing = [asset for asset in SERVICE_ASSETS if not has_asset(text, asset)]
        if missing:
            links = "\n".join(f'<link href="{asset}" rel="stylesheet"/>' for asset in missing)
            text = insert_before_layout_or_head(text, links)
            service_asset_repairs += 1

        # Empty template paragraphs create visible dead spacing between section
        # headings and content. Remove only from Stage 48 service pages.
        text, removed = re.subn(r'<p>\s*</p>', '', text, flags=re.I)
        empty_paragraphs_removed += removed

    # A skip link must be visually hidden until keyboard focus. If a page does not
    # load the shared stylesheet and has no local rule, install the tiny local rule.
    if re.search(r'class=["\'][^"\']*\bskip-link\b', text):
        has_shared = has_asset(text, "/assets/site-enhancements.css")
        has_local = re.search(r'\.skip-link\s*\{', text) is not None
        if not has_shared and not has_local:
            text = insert_before_layout_or_head(text, SKIP_STYLE)
            skip_repairs += 1

    # The catalog UI title is interface chrome, not a document subsection. Keeping
    # it as H3 caused H1 -> H3 before the first H2 in the article hierarchy.
    if page == root / "cases" / "factory-catalog" / "index.html":
        text, n = re.subn(
            r'<h3>\s*Выбор продукции\s*</h3>',
            '<div class="s51-ui-title">Выбор продукции</div>',
            text,
            count=1,
            flags=re.I,
        )
        if n:
            ui_style = '<style data-stage57-catalog-ui>.s51-catalog-main .s51-ui-title{margin:.25rem 0 0;font-size:1.45rem;line-height:1.2;font-weight:800;letter-spacing:-.025em}</style>'
            text = insert_before_layout_or_head(text, ui_style)
            heading_repairs += 1

    if text != original:
        page.write_text(text, encoding="utf-8")

# Guard 1: homepage is explicitly frozen by project direction.
home_after = hashlib.sha256(home.read_bytes()).hexdigest()
if home_after != home_before:
    raise SystemExit("stage57: homepage changed; forbidden")

# Guard 2: no Stage 48 component may reach production without its stylesheet.
missing_component_css: list[str] = []
visible_skip_links: list[str] = []
heading_jumps: list[str] = []
remaining_empty_service_p: list[str] = []

for page in root.rglob("*.html"):
    text = page.read_text(encoding="utf-8", errors="ignore")
    rel = "/" + page.relative_to(root).as_posix()
    if rel.endswith("/index.html"):
        rel = rel[:-len("index.html")]
    elif rel == "/index.html":
        rel = "/"

    if re.search(r'class=["\'][^"\']*\bs48[-_]', text):
        if not has_asset(text, "/assets/site-enhancements.css"):
            missing_component_css.append(rel)
        if re.search(r'<p>\s*</p>', text, flags=re.I):
            remaining_empty_service_p.append(rel)

    if re.search(r'class=["\'][^"\']*\bskip-link\b', text):
        has_shared = has_asset(text, "/assets/site-enhancements.css")
        has_local = re.search(r'\.skip-link\s*\{', text) is not None
        if not (has_shared or has_local):
            visible_skip_links.append(rel)

    # Lightweight heading hierarchy guard: a document should not jump H1 -> H3.
    levels = [int(x) for x in re.findall(r'<h([1-6])\b', text, flags=re.I)]
    for prev, cur in zip(levels, levels[1:]):
        if cur > prev + 1:
            heading_jumps.append(f"{rel}: H{prev}->H{cur}")
            break

errors = []
if missing_component_css:
    errors.append("Stage48 CSS missing: " + ", ".join(missing_component_css))
if visible_skip_links:
    errors.append("unstyled skip-link: " + ", ".join(visible_skip_links))
if remaining_empty_service_p:
    errors.append("empty service paragraphs: " + ", ".join(remaining_empty_service_p))
if heading_jumps:
    errors.append("heading hierarchy jumps: " + ", ".join(heading_jumps))
if errors:
    raise SystemExit("stage57 visual integrity failed:\n  " + "\n  ".join(errors))

print("stage57 visual integrity:")
print(f"  service pages with asset dependencies repaired: {service_asset_repairs}")
print(f"  skip-link local styles added: {skip_repairs}")
print(f"  empty service paragraphs removed: {empty_paragraphs_removed}")
print(f"  heading hierarchy repairs: {heading_repairs}")
print(f"  homepage sha256 unchanged: {home_after}")
print("  CSS dependency / skip-link / heading guards: OK")
