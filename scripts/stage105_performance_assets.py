#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
ASSETS = ROOT / 'assets'

BUNDLES = {
    'stage105-layout-core.css': [
        '/assets/layout-system.css',
        '/assets/mobile-polish.css',
        '/assets/visual-system.css',
        '/assets/stage89-guide-rhythm.css',
        '/assets/stage83-mobile-actions.css',
    ],
    'stage105-theme-search.css': [
        '/assets/theme-system.css',
        '/assets/theme-light-legacy-fixes.css',
        '/assets/stage101-search-flow.css',
        '/assets/stage102-volume-growth.css',
    ],
    'stage105-final-ui.css': [
        '/assets/stage95-prune.css',
        '/assets/stage96-typography.css',
        '/assets/stage97-layout.css',
        '/assets/stage98-design-system.css',
        '/assets/stage98-shell.css',
    ],
}

LINK_RE = re.compile(r'<link\b[^>]*>', re.I)
HREF_RE = re.compile(r'\bhref=["\']([^"\']+)["\']', re.I)
REL_RE = re.compile(r'\brel=["\']([^"\']+)["\']', re.I)


def css_path(tag: str) -> str | None:
    href = HREF_RE.search(tag)
    rel = REL_RE.search(tag)
    if not href or not rel or 'stylesheet' not in rel.group(1).lower().split():
        return None
    value = href.group(1)
    if not value.startswith('/assets/'):
        return None
    return value.split('?', 1)[0]


def write_bundle(name: str, members: list[str]) -> tuple[str, int]:
    parts: list[str] = []
    for url in members:
        path = ROOT / url.lstrip('/')
        if not path.is_file():
            raise SystemExit(f'stage105: missing bundle member: {url}')
        text = path.read_text(encoding='utf-8').rstrip()
        parts.append(f'/* {path.name} */\n{text}\n')
    content = '\n'.join(parts)
    target = ASSETS / name
    target.write_text(content, encoding='utf-8')
    digest = hashlib.sha256(content.encode('utf-8')).hexdigest()[:12]
    return f'/assets/{name}?v={digest}', len(content.encode('utf-8'))


def dedupe_stylesheets(html: str) -> tuple[str, int]:
    seen: set[str] = set()
    removals: list[tuple[int, int]] = []
    for match in LINK_RE.finditer(html):
        path = css_path(match.group(0))
        if not path:
            continue
        if path in seen:
            removals.append((match.start(), match.end()))
        else:
            seen.add(path)
    for start, end in reversed(removals):
        html = html[:start] + html[end:]
    return html, len(removals)


def replace_adjacent_bundle(html: str, members: list[str], href: str, marker: str) -> tuple[str, bool]:
    links = [(m, css_path(m.group(0))) for m in LINK_RE.finditer(html)]
    links = [(m, p) for m, p in links if p]
    paths = [p for _, p in links]
    size = len(members)
    for i in range(0, len(paths) - size + 1):
        if paths[i:i + size] != members:
            continue
        chunk = links[i:i + size]
        adjacent = all(
            not html[chunk[j][0].end():chunk[j + 1][0].start()].strip()
            for j in range(size - 1)
        )
        if not adjacent:
            continue
        first = chunk[0][0]
        last = chunk[-1][0]
        replacement = f'<link href="{href}" rel="stylesheet" data-{marker}="true"/>'
        return html[:first.start()] + replacement + html[last.end():], True
    return html, False


if not ASSETS.is_dir():
    raise SystemExit('stage105: assets directory missing')

bundle_urls: dict[str, tuple[str, list[str], int]] = {}
for name, members in BUNDLES.items():
    href, size = write_bundle(name, members)
    bundle_urls[name] = (href, members, size)

pages = 0
deduped = 0
bundled = {name: 0 for name in BUNDLES}
for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '</head>' not in html:
        continue
    pages += 1
    html, removed = dedupe_stylesheets(html)
    deduped += removed
    for name, (href, members, _) in bundle_urls.items():
        marker = name.removesuffix('.css')
        html, changed = replace_adjacent_bundle(html, members, href, marker)
        if changed:
            bundled[name] += 1
    path.write_text(html, encoding='utf-8')

dup_pages: list[str] = []
for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '</head>' not in html:
        continue
    seen: set[str] = set()
    for match in LINK_RE.finditer(html):
        value = css_path(match.group(0))
        if not value:
            continue
        if value in seen:
            dup_pages.append(path.relative_to(ROOT).as_posix())
            break
        seen.add(value)
if dup_pages:
    raise SystemExit('stage105: duplicate stylesheets remain: ' + ', '.join(dup_pages[:10]))

if bundled['stage105-layout-core.css'] < 60:
    raise SystemExit(f"stage105: layout bundle unexpectedly rare: {bundled['stage105-layout-core.css']}")
if bundled['stage105-theme-search.css'] < 60:
    raise SystemExit(f"stage105: theme bundle unexpectedly rare: {bundled['stage105-theme-search.css']}")
if bundled['stage105-final-ui.css'] < 60:
    raise SystemExit(f"stage105: final UI bundle unexpectedly rare: {bundled['stage105-final-ui.css']}")

sizes = ', '.join(f'{name}={size}' for name, (_, _, size) in bundle_urls.items())
uses = ', '.join(f'{name}={count}' for name, count in bundled.items())
print(f'stage105 performance assets: pages={pages}; duplicate links removed={deduped}; {uses}; bytes: {sizes}')
