#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import subprocess
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


def body_hash(html: str) -> str:
    body = html.split('</head>', 1)[1] if '</head>' in html else html
    return hashlib.sha256(body.encode('utf-8')).hexdigest()


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

# Proof/discovery changes happen first. Stage108 normalizes the final DOM rhythm,
# then Stage109 fixes the remaining cross-family visual/content inconsistencies.
# Only after these passes does Stage105 snapshot bodies and build CSS bundles.
subprocess.run(
    [sys.executable, str(Path(__file__).with_name('stage106_proof_graph.py')), str(ROOT)],
    check=True,
)
subprocess.run(
    [sys.executable, str(Path(__file__).with_name('stage108_sitewide_visual_cleanup.py')), str(ROOT)],
    check=True,
)
subprocess.run(
    [sys.executable, str(Path(__file__).with_name('stage109_content_visual_consistency.py')), str(ROOT)],
    check=True,
)

bundle_urls: dict[str, tuple[str, list[str], int]] = {}
for name, members in BUNDLES.items():
    href, size = write_bundle(name, members)
    bundle_urls[name] = (href, members, size)

pages = 0
deduped = 0
bundled = {name: 0 for name in BUNDLES}
body_before: dict[str, str] = {}
for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '</head>' not in html:
        continue
    rel = path.relative_to(ROOT).as_posix()
    body_before[rel] = body_hash(html)
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

body_changed: list[str] = []
for rel, expected in body_before.items():
    path = ROOT / rel
    html = path.read_text(encoding='utf-8', errors='strict')
    if body_hash(html) != expected:
        body_changed.append(rel)
if body_changed:
    raise SystemExit('stage105: page body changed unexpectedly: ' + ', '.join(body_changed[:10]))

key_pages = [
    'index.html', 'services/index.html', 'telegram-bots/index.html',
    'web-development/index.html', 'crm-development/index.html',
    'n8n-automation/index.html', 'freelance-developer/index.html',
]
for rel in key_pages:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f'stage105: key page missing: {rel}')
    html = path.read_text(encoding='utf-8')
    css_count = sum(1 for match in LINK_RE.finditer(html) if css_path(match.group(0)))
    if css_count > 10:
        raise SystemExit(f'stage105: too many CSS requests remain on {rel}: {css_count}')

if bundled['stage105-layout-core.css'] < 60:
    raise SystemExit(f"stage105: layout bundle unexpectedly rare: {bundled['stage105-layout-core.css']}")
if bundled['stage105-theme-search.css'] < 60:
    raise SystemExit(f"stage105: theme bundle unexpectedly rare: {bundled['stage105-theme-search.css']}")
if bundled['stage105-final-ui.css'] < 60:
    raise SystemExit(f"stage105: final UI bundle unexpectedly rare: {bundled['stage105-final-ui.css']}")

# Responsive QA patches the built bundle and rotates its cache key.
subprocess.run(
    [sys.executable, str(Path(__file__).with_name('stage110_responsive_quality.py')), str(ROOT)],
    check=True,
)
# Final polish removes remaining mobile content rails and default-link visual leakage.
subprocess.run(
    [sys.executable, str(Path(__file__).with_name('stage111_final_polish.py')), str(ROOT)],
    check=True,
)
# Normalize the actual published image tags after all DOM-building stages have run.
subprocess.run(
    [sys.executable, str(Path(__file__).with_name('stage112_media_loading.py')), str(ROOT)],
    check=True,
)

sizes = ', '.join(f'{name}={size}' for name, (_, _, size) in bundle_urls.items())
uses = ', '.join(f'{name}={count}' for name, count in bundled.items())
print(f'stage105 performance assets: pages={pages}; duplicate links removed={deduped}; {uses}; bytes before stage110/111: {sizes}')
