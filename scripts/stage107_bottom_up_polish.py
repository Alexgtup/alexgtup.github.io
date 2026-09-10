#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from collections import Counter
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')

MAIN_RE = re.compile(r'<main\b[^>]*>.*?</main>', re.I | re.S)
FOOTER_RE = re.compile(r'<footer\b[^>]*>.*?</footer>', re.I | re.S)
DETAIL_RE = re.compile(
    r'\s*<details\b(?=[^>]*class=["\'][^"\']*\bux-seo-more\b[^"\']*["\'])[^>]*>.*?</details>\s*',
    re.I | re.S,
)
SECTION_RE = re.compile(r'<section\b[^>]*>.*?</section>', re.I | re.S)
TELEGRAM_RE = re.compile(r'https://t\.me/Alexuys', re.I)

RU_FOOTER = '''<footer class="footer stage107-footer" data-nosnippet="">
  <div class="container stage107-footer__inner">
    <div class="stage107-footer__brand">
      <a href="/" aria-label="Alexuys - на главную">alexuys</a>
      <span>WEB · APPS · AUTOMATION</span>
    </div>
    <nav class="stage107-footer__nav" aria-label="Ссылки в подвале">
      <a href="/services/">Услуги</a>
      <a href="/cases/">Кейсы</a>
      <a href="/guides/">Разборы</a>
      <a href="/tools/">Инструменты</a>
      <a href="/demos/">Демо</a>
      <a href="/about/">Обо мне</a>
    </nav>
    <div class="stage107-footer__meta">
      <span>© 2026 Alexuys · Александр</span>
      <a href="mailto:alexgtup@gmail.com">alexgtup@gmail.com</a>
      <a href="https://freelance.ru/gglalex" target="_blank" rel="noopener noreferrer">Freelance.ru ↗</a>
      <a href="/privacy/">Конфиденциальность</a>
    </div>
  </div>
</footer>'''

EN_FOOTER = '''<footer class="intl-footer stage107-footer" data-nosnippet="">
  <div class="intl-container stage107-footer__inner">
    <div class="stage107-footer__brand">
      <a href="/en/" aria-label="Alexuys - home">alexuys</a>
      <span>WEB · APPS · AUTOMATION</span>
    </div>
    <nav class="stage107-footer__nav" aria-label="Footer navigation">
      <a href="/en/services/">Services</a>
      <a href="/en/cases/">Cases</a>
      <a href="/en/guides/">Guides</a>
      <a href="/en/about/">About</a>
    </nav>
    <div class="stage107-footer__meta">
      <span>© 2026 Alexuys</span>
      <a href="mailto:alexgtup@gmail.com">alexgtup@gmail.com</a>
      <a href="/en/privacy/">Privacy</a>
      <a href="/" hreflang="ru" lang="ru">Русская версия</a>
    </div>
  </div>
</footer>'''


def relpath(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_en(html: str) -> bool:
    m = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', html, re.I)
    return bool(m and m.group(1).lower().startswith('en'))


def add_endcap_marker(tag: str) -> str:
    if 'stage107-endcap' in tag:
        return tag
    cm = re.search(r'class=(["\'])(.*?)\1', tag, re.I | re.S)
    if cm:
        classes = cm.group(2).split()
        classes.append('stage107-endcap')
        replacement = f'class={cm.group(1)}{" ".join(classes)}{cm.group(1)}'
        tag = tag[:cm.start()] + replacement + tag[cm.end():]
    else:
        tag = tag[:-1] + ' class="stage107-endcap">'
    if 'data-stage107-endcap=' not in tag:
        tag = tag[:-1] + ' data-stage107-endcap="true">'
    return tag


def mark_last_contact(main: str, rel: str) -> tuple[str, bool]:
    if rel in {'index.html', '404.html'}:
        return main, False

    # First prefer semantic contact surfaces. This covers services, cases, hubs,
    # tools, demos and the product contact without flattening their useful copy.
    candidates: list[tuple[int, int, str]] = []
    tag_re = re.compile(r'<(?:section|div)\b[^>]*>', re.I | re.S)
    for m in tag_re.finditer(main):
        tag = m.group(0)
        if re.search(
            r'(?:\bid=["\'](?:contact|case-contact|hub-contact|demo-contact)["\'])|'
            r'(?:\bclass=["\'][^"\']*\b(?:s48-contact|s50-cta|s64-conversion|dt-contact|ux-product-contact|cta-box)\b)',
            tag,
            re.I,
        ):
            candidates.append((m.start(), m.end(), tag))

    if candidates:
        start, end, tag = candidates[-1]
        return main[:start] + add_endcap_marker(tag) + main[end:], True

    # Editorial/EN pages sometimes use a neutral section as their final CTA.
    # Mark the last section that actually contains the Telegram action.
    sections = list(SECTION_RE.finditer(main))
    for sec in reversed(sections):
        block = sec.group(0)
        if not TELEGRAM_RE.search(block):
            continue
        opening = re.match(r'<section\b[^>]*>', block, re.I | re.S)
        if not opening:
            continue
        new_open = add_endcap_marker(opening.group(0))
        new_block = new_open + block[opening.end():]
        return main[:sec.start()] + new_block + main[sec.end():], True
    return main, False


def move_seo_before_contact(main: str, rel: str) -> tuple[str, int]:
    # Tool pages and the demos hub had progressive SEO details after the primary
    # contact section. That makes a completed page feel as if it continues after
    # the CTA. Keep the detail, but place it before the conversion ending.
    target = rel == 'demos/index.html' or rel == 'tools/index.html' or (
        rel.startswith('tools/') and rel.endswith('/index.html')
    )
    if not target:
        return main, 0

    details = list(DETAIL_RE.finditer(main))
    if not details:
        return main, 0

    contact_openings = list(re.finditer(
        r'<section\b(?=[^>]*(?:\bid=["\'](?:hub-contact|demo-contact)["\']|class=["\'][^"\']*\bdt-contact\b))[^>]*>',
        main,
        re.I | re.S,
    ))
    if not contact_openings:
        return main, 0
    contact_start = contact_openings[-1].start()
    after = [m for m in details if m.start() > contact_start]
    if not after:
        return main, 0

    blocks = [m.group(0).strip() for m in after]
    for m in reversed(after):
        main = main[:m.start()] + '\n' + main[m.end():]

    # Removing content after contact does not move the contact start.
    insert = '\n'.join(blocks) + '\n'
    main = main[:contact_start] + insert + main[contact_start:]
    return main, len(blocks)


changed: list[str] = []
footer_changed = 0
moved_details = 0
endcaps = 0

for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    rel = relpath(path)
    if '<main' not in html or rel == '404.html' or path.name.startswith(('google', 'yandex_')):
        continue
    original = html

    mm = MAIN_RE.search(html)
    if mm:
        main = mm.group(0)
        main, moved = move_seo_before_contact(main, rel)
        moved_details += moved
        main, marked = mark_last_contact(main, rel)
        endcaps += int(marked)
        html = html[:mm.start()] + main + html[mm.end():]

    fm = FOOTER_RE.search(html)
    if fm:
        footer = EN_FOOTER if is_en(html) else RU_FOOTER
        html = html[:fm.start()] + footer + html[fm.end():]
        footer_changed += 1

    if html != original:
        path.write_text(html, encoding='utf-8')
        changed.append(rel)

# Final invariants: every user-facing page gets one shared footer, and utility
# SEO disclosure never follows the primary contact surface again.
problems: list[str] = []
footer_signatures = Counter()
for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    rel = relpath(path)
    if '<main' not in html or rel == '404.html' or path.name.startswith(('google', 'yandex_')):
        continue
    if html.count('stage107-footer') != 1:
        problems.append(f'{rel}: shared footer count={html.count("stage107-footer")}')
    footer = FOOTER_RE.search(html)
    if not footer:
        problems.append(f'{rel}: footer missing')
        continue
    hrefs = tuple(re.findall(r'<a\b[^>]*href=["\']([^"\']+)', footer.group(0), re.I))
    footer_signatures[hrefs] += 1

    if rel == 'demos/index.html' or rel == 'tools/index.html' or (rel.startswith('tools/') and rel.endswith('/index.html')):
        main_m = MAIN_RE.search(html)
        if main_m:
            main = main_m.group(0)
            contact = re.search(
                r'<section\b(?=[^>]*(?:\bid=["\'](?:hub-contact|demo-contact)["\']|class=["\'][^"\']*\bdt-contact\b))[^>]*>',
                main,
                re.I | re.S,
            )
            if contact and any(m.start() > contact.start() for m in DETAIL_RE.finditer(main)):
                problems.append(f'{rel}: SEO disclosure remains after contact')

if len(footer_signatures) > 2:
    problems.append(f'footer signatures={len(footer_signatures)} (expected RU + EN only)')

if problems:
    raise SystemExit('stage107 bottom-up polish failed:\n' + '\n'.join(problems[:40]))

print(
    f'stage107 bottom-up: pages_changed={len(changed)}; footers={footer_changed}; '
    f'endcaps={endcaps}; seo_details_moved={moved_details}; footer_signatures={len(footer_signatures)}'
)
