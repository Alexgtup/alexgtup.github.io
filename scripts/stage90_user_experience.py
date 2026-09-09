#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

UX_MARK = 'data-stage90-ux="true"'
UX_LINK = '<link href="/assets/ux-content.css?v=20260909-1" rel="stylesheet" data-stage90-ux="true"/>'
SECTION_RE = re.compile(r'<section\b[^>]*>.*?</section>', re.I | re.S)
MAIN_RE = re.compile(r'<main\b[^>]*>.*?</main>', re.I | re.S)


def route_path(route: str) -> Path:
    if route == "/":
        return root / "index.html"
    return root / route.strip("/") / "index.html"


def add_css(text: str) -> str:
    if UX_MARK in text:
        return text
    return text.replace('</head>', UX_LINK + '\n</head>', 1)


def add_class_to_tag(tag: str, class_name: str) -> str:
    cm = re.search(r'class=(["\'])(.*?)\1', tag, re.I | re.S)
    if cm:
        classes = cm.group(2).split()
        if class_name in classes:
            return tag
        classes.append(class_name)
        repl = f'class={cm.group(1)}{" ".join(classes)}{cm.group(1)}'
        return tag[:cm.start()] + repl + tag[cm.end():]
    return tag[:-1] + f' class="{class_name}">'


def add_main_class(text: str, class_name: str) -> str:
    pat = re.compile(r'<main\b[^>]*>', re.I | re.S)
    return pat.sub(lambda m: add_class_to_tag(m.group(0), class_name), text, count=1)


def add_id_to_opening(tag: str, element_id: str) -> str:
    if re.search(r'\bid=["\']', tag, re.I):
        return tag
    return tag[:-1] + f' id="{element_id}">'


def add_id_first_class(text: str, class_name: str, element_id: str, tag_name: str = "section") -> str:
    pat = re.compile(
        rf'<{tag_name}\b(?=[^>]*class=["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\'])[^>]*>',
        re.I | re.S,
    )
    return pat.sub(lambda m: add_id_to_opening(m.group(0), element_id), text, count=1)


def add_id_nth_class(text: str, class_name: str, element_id: str, nth: int) -> str:
    pat = re.compile(
        rf'<section\b(?=[^>]*class=["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\'])[^>]*>',
        re.I | re.S,
    )
    matches = list(pat.finditer(text))
    if len(matches) < nth:
        return text
    m = matches[nth - 1]
    tag = add_id_to_opening(m.group(0), element_id)
    return text[:m.start()] + tag + text[m.end():]


def add_id_aria(text: str, aria_value: str, element_id: str) -> str:
    pat = re.compile(
        rf'<section\b(?=[^>]*aria-labelledby=["\']{re.escape(aria_value)}["\'])[^>]*>',
        re.I | re.S,
    )
    return pat.sub(lambda m: add_id_to_opening(m.group(0), element_id), text, count=1)


def add_id_section_with_heading(text: str, heading_text: str, element_id: str) -> str:
    for m in SECTION_RE.finditer(text):
        block = m.group(0)
        plain = re.sub(r'<[^>]+>', ' ', block)
        plain = re.sub(r'\s+', ' ', plain).strip()
        if heading_text.lower() not in plain.lower():
            continue
        opening_end = block.find('>') + 1
        opening = add_id_to_opening(block[:opening_end], element_id)
        block = opening + block[opening_end:]
        return text[:m.start()] + block + text[m.end():]
    return text


def section_by_id(text: str, element_id: str) -> re.Match[str] | None:
    pat = re.compile(
        rf'<section\b(?=[^>]*\bid=["\']{re.escape(element_id)}["\'])[^>]*>.*?</section>',
        re.I | re.S,
    )
    return pat.search(text)


def move_section_after_id(text: str, moving_id: str, target_id: str) -> str:
    moving = section_by_id(text, moving_id)
    target = section_by_id(text, target_id)
    if not moving or not target or moving.start() == target.start():
        return text
    block = moving.group(0)
    text = text[:moving.start()] + text[moving.end():]
    target = section_by_id(text, target_id)
    if not target:
        return text
    return text[:target.end()] + '\n' + block + text[target.end():]


def insert_after_hero(text: str, nav_html: str, hero_classes: tuple[str, ...]) -> str:
    if 'class="ux-content-nav"' in text:
        return text
    for class_name in hero_classes:
        pat = re.compile(
            rf'(<section\b(?=[^>]*class=["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\'])[^>]*>.*?</section>)',
            re.I | re.S,
        )
        if pat.search(text):
            return pat.sub(lambda m: m.group(1) + '\n' + nav_html, text, count=1)
    return text


def build_nav(links: list[tuple[str, str]], *, primary: tuple[str, str]) -> str:
    parts = [
        '<nav class="ux-content-nav" aria-label="Быстрый переход по странице">',
        '  <div class="container ux-content-nav__inner">',
    ]
    for href, label in links:
        parts.append(f'    <a href="{href}">{label}</a>')
    href, label = primary
    extra = ' target="_blank" rel="noopener noreferrer"' if href.startswith('http') else ''
    parts.append(f'    <a class="ux-content-nav__primary" href="{href}"{extra}>{label}</a>')
    parts.extend(['  </div>', '</nav>'])
    return '\n'.join(parts)


def wrap_s77_sections(text: str, summary: str) -> str:
    def repl(m: re.Match[str]) -> str:
        block = m.group(0)
        if 'ux-seo-more' in block:
            return block
        return f'<details class="ux-seo-more"><summary>{summary}</summary>{block}</details>'

    pat = re.compile(
        r'<section\b(?=[^>]*class=["\'][^"\']*\bs77-section\b[^"\']*["\'])[^>]*>.*?</section>',
        re.I | re.S,
    )
    return pat.sub(repl, text)


def add_id_to_last_contact_section(text: str, element_id: str) -> str:
    mm = MAIN_RE.search(text)
    if not mm:
        return text
    main = mm.group(0)
    sections = list(SECTION_RE.finditer(main))
    candidate = None
    for sec in sections:
        block = sec.group(0)
        opening = block[:block.find('>') + 1]
        if ('https://t.me/Alexuys' in block or 'mailto:alexgtup@gmail.com' in block or
                re.search(r'class=["\'][^"\']*\b(?:contact|cta-box|s51-contact)\b', opening, re.I)):
            candidate = sec
    if not candidate:
        return text
    block = candidate.group(0)
    opening_end = block.find('>') + 1
    opening = add_id_to_opening(block[:opening_end], element_id)
    if opening == block[:opening_end] and f'id="{element_id}"' not in opening:
        return text
    new_block = opening + block[opening_end:]
    new_main = main[:candidate.start()] + new_block + main[candidate.end():]
    return text[:mm.start()] + new_main + text[mm.end():]


def move_case_gallery(text: str) -> str:
    if not section_by_id(text, 'gallery') or not section_by_id(text, 'case-overview'):
        return text
    return move_section_after_id(text, 'gallery', 'case-overview')


changed: list[str] = []

# Browse-first hubs.
hub_configs = {
    '/cases/': {
        'hero': ('s50-hero',),
        'setup': lambda t: add_id_first_class(add_id_aria(t, 'try-projects', 'case-demos'), 's50-cta', 'hub-contact'),
        'links': [('#case-list', 'Кейсы'), ('#case-demos', 'Демо')],
        'primary': ('#hub-contact', 'Написать'),
        'move': ('case-demos', 'case-list'),
    },
    '/services/': {
        'hero': ('s44-services-hero',),
        'setup': lambda t: add_id_first_class(add_id_aria(t, 'try-projects', 'service-demos'), 's44-section', 'service-options'),
        'links': [('#service-options', 'Направления'), ('#service-demos', 'Демо')],
        'primary': ('#hub-contact', 'Написать'),
        'contact_class': 's64-conversion',
        'move': ('service-demos', 'service-options'),
    },
    '/guides/': {
        'hero': ('s50-hero',),
        'setup': lambda t: t,
        'links': [('#guides-list', 'Разборы')],
        'primary': ('#hub-contact', 'Написать'),
        'contact_class': 's64-conversion',
    },
    '/tools/': {
        'hero': ('dt-hero',),
        'setup': lambda t: add_id_first_class(t, 'dt-grid', 'tools-list', tag_name='div'),
        'links': [('#tools-list', 'Инструменты')],
        'primary': ('#hub-contact', 'Написать'),
        'contact_class': 'dt-contact',
    },
    '/demos/': {
        'hero': ('growth-hero',),
        'setup': lambda t: add_id_aria(add_id_aria(t, 'products', 'demo-products'), 'your-product', 'demo-contact'),
        'links': [('#demo-products', 'Продукты')],
        'primary': ('#demo-contact', 'Написать'),
    },
    '/about/': {
        'hero': ('s50-hero',),
        'setup': lambda t: add_id_first_class(add_id_aria(t, 'try-projects', 'about-demos'), 's50-section', 'about-approach'),
        'links': [('#about-approach', 'Подход'), ('#about-demos', 'Демо')],
        'primary': ('#hub-contact', 'Написать'),
        'contact_class': 's64-conversion',
        'move': ('about-demos', 'about-approach'),
    },
    '/freelance-developer/': {
        'hero': ('s50-hero',),
        'setup': lambda t: add_id_nth_class(add_id_nth_class(t, 's50-section', 'freelance-proof', 1), 's50-section', 'freelance-offers', 2),
        'links': [('#freelance-proof', 'Проверить'), ('#freelance-offers', 'Форматы')],
        'primary': ('#hub-contact', 'Написать'),
        'contact_class': 's50-cta',
    },
}

for route, cfg in hub_configs.items():
    path = route_path(route)
    if not path.is_file():
        raise SystemExit(f'stage90: missing hub {route}')
    text = path.read_text(encoding='utf-8')
    original = text
    text = add_css(text)
    text = add_main_class(text, 'ux-hub-main')
    text = cfg['setup'](text)
    contact_class = cfg.get('contact_class')
    if contact_class:
        text = add_id_first_class(text, contact_class, 'hub-contact')
    if 'move' in cfg:
        text = move_section_after_id(text, *cfg['move'])
    nav = build_nav(cfg['links'], primary=cfg['primary'])
    text = insert_after_hero(text, nav, cfg['hero'])
    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(route)

# Utility/product pages keep explanatory SEO copy, but it becomes progressive disclosure.
for path in sorted((root / 'tools').glob('*/index.html')) + [root / 'tools/index.html', root / 'demos/index.html']:
    if not path.is_file():
        continue
    text = path.read_text(encoding='utf-8')
    original = text
    text = add_css(text)
    text = add_main_class(text, 'ux-utility-main')
    text = wrap_s77_sections(text, 'Подробнее о применении')
    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append('/' + path.relative_to(root).parent.as_posix().strip('/') + '/')

fos = root / 'freelance-os/index.html'
if fos.is_file():
    text = fos.read_text(encoding='utf-8')
    original = text
    text = add_css(text)
    text = add_main_class(text, 'ux-product-main')
    text = wrap_s77_sections(text, 'Подробнее о реализации и архитектуре')
    if 'class="ux-product-contact"' not in text:
        contact = '''\n<div class="ux-product-contact" aria-label="Следующий шаг">
  <p>Нужна похожая CRM или внутренняя система?</p>
  <div class="ux-product-contact__actions">
    <a href="/cases/freelance-os/">Посмотреть технический кейс</a>
    <a class="primary" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Обсудить задачу ↗</a>
  </div>
</div>\n'''
        text = text.replace('</main>', contact + '</main>', 1)
    if text != original:
        fos.write_text(text, encoding='utf-8')
        changed.append('/freelance-os/')

# RU case details: interface/proof comes early; compact navigation is based on real sections.
cases_root = root / 'cases'
for path in sorted(cases_root.glob('*/index.html')):
    route = '/' + path.relative_to(root).parent.as_posix().strip('/') + '/'
    text = path.read_text(encoding='utf-8')
    original = text
    text = add_css(text)
    text = add_main_class(text, 'ux-case-main')

    if 'class="s51-hero"' in text or "class='s51-hero'" in text:
        text = add_id_first_class(text, 's51-section', 'case-overview')
        hero_classes = ('s51-hero',)
    else:
        text = add_id_first_class(text, 'section', 'case-overview')
        hero_classes = ('hero',)

    # SEO Control Center has a dedicated UI section but no legacy gallery id.
    if route == '/cases/seo-control-center/':
        text = add_id_section_with_heading(text, 'Интерфейс и возможности сервиса.', 'case-interface')
        if section_by_id(text, 'case-interface') and section_by_id(text, 'case-overview'):
            text = move_section_after_id(text, 'case-interface', 'case-overview')

    text = move_case_gallery(text)
    text = add_id_to_last_contact_section(text, 'case-contact')

    links = [('#case-overview', 'О проекте')]
    if re.search(r'\bid=["\']gallery["\']', text, re.I):
        links.append(('#gallery', 'Интерфейс'))
    elif re.search(r'\bid=["\']case-interface["\']', text, re.I):
        links.append(('#case-interface', 'Интерфейс'))

    primary = ('#case-contact', 'Написать') if re.search(r'\bid=["\']case-contact["\']', text, re.I) else ('https://t.me/Alexuys', 'Написать')
    nav = build_nav(links, primary=primary)
    text = insert_after_hero(text, nav, hero_classes)

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(route)

# Guards: no quick navigation points to a missing local fragment; all transformed
# pages include the UX stylesheet.
problems: list[str] = []
for path in sorted(root.rglob('*.html')):
    text = path.read_text(encoding='utf-8')
    if not any(cls in text for cls in ('ux-hub-main', 'ux-case-main', 'ux-utility-main', 'ux-product-main')):
        continue
    rel = path.relative_to(root).as_posix()
    if UX_MARK not in text:
        problems.append(rel + ':missing-css')
        continue
    ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', text, re.I))
    for href in re.findall(r'<a\b[^>]*href=["\']#([^"\']+)["\']', text, re.I):
        if href not in ids:
            problems.append(rel + ':#' + href)

if problems:
    raise SystemExit('stage90 UX invariant failed: ' + ', '.join(problems[:30]))

print(f'stage90 user experience: changed={len(changed)}')
print('stage90 pages: ' + ', '.join(changed))
