#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
IMG_RE = re.compile(r'<img\b[^>]*>', re.I | re.S)
ATTR_RE = lambda name: re.compile(rf'\s+{re.escape(name)}\s*=\s*(["\']).*?\1', re.I | re.S)


def relpath(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def set_attr(tag: str, name: str, value: str) -> str:
    pattern = ATTR_RE(name)
    replacement = f' {name}="{value}"'
    if pattern.search(tag):
        return pattern.sub(replacement, tag, count=1)
    return tag[:-1].rstrip() + replacement + '>'


def get_attr(tag: str, name: str) -> str | None:
    m = re.search(rf'\b{re.escape(name)}\s*=\s*(["\'])(.*?)\1', tag, re.I | re.S)
    return m.group(2) if m else None


def hero_count(rel: str) -> int:
    if rel == 'index.html':
        return 1
    if rel == 'cases/index.html':
        return 2
    if rel.startswith('cases/') and rel.endswith('/index.html'):
        return 1
    return 0


pages = 0
images = 0
eager = 0
lazy = 0
changed_pages = 0
problems: list[str] = []

for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<body' not in html or path.name.startswith(('google', 'yandex_')):
        continue
    rel = relpath(path)
    matches = list(IMG_RE.finditer(html))
    if not matches:
        continue
    pages += 1
    hero_images = hero_count(rel)
    out = html
    replacements: list[tuple[int, int, str]] = []
    for index, match in enumerate(matches):
        tag = match.group(0)
        images += 1
        tag = set_attr(tag, 'decoding', 'async')
        if index < hero_images:
            tag = set_attr(tag, 'loading', 'eager')
            # Only the primary visual receives high priority. A secondary collage
            # image should be eager but must not compete with the LCP candidate.
            if index == 0:
                tag = set_attr(tag, 'fetchpriority', 'high')
            elif get_attr(tag, 'fetchpriority') == 'high':
                tag = set_attr(tag, 'fetchpriority', 'auto')
            eager += 1
        else:
            tag = set_attr(tag, 'loading', 'lazy')
            # Lower-page media should never retain an accidental high priority.
            if get_attr(tag, 'fetchpriority') == 'high':
                tag = set_attr(tag, 'fetchpriority', 'low')
            lazy += 1
        replacements.append((match.start(), match.end(), tag))
    for start, end, tag in reversed(replacements):
        out = out[:start] + tag + out[end:]
    if out != html:
        path.write_text(out, encoding='utf-8')
        changed_pages += 1

# Final invariant pass: every content image reserves layout space upstream and
# now also has an explicit loading/decoding strategy.
for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<body' not in html or path.name.startswith(('google', 'yandex_')):
        continue
    rel = relpath(path)
    for tag in IMG_RE.findall(html):
        for attr in ('width', 'height', 'alt', 'loading', 'decoding'):
            if get_attr(tag, attr) is None:
                problems.append(f'{rel}: image missing {attr}')
                break
        loading = get_attr(tag, 'loading')
        if loading not in ('eager', 'lazy'):
            problems.append(f'{rel}: unexpected image loading={loading!r}')

if eager < 5:
    problems.append(f'only {eager} eager hero images detected')
if images < 25:
    problems.append(f'only {images} content images audited')

if problems:
    raise SystemExit('stage112 media loading failed:\n' + '\n'.join(problems[:50]))

print(
    f'stage112 media loading: pages={pages}; images={images}; eager={eager}; '
    f'lazy={lazy}; changed_pages={changed_pages}; explicit loading/decoding OK'
)
