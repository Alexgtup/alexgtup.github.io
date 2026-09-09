#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')

MARK = '''<span aria-hidden="true" class="stage98-brand-mark"><svg fill="none" viewBox="0 0 36 36"><path d="M8 10h4.5c5.3 0 5.3 8 10.3 8H28" stroke="#f3f4f1" stroke-linecap="round" stroke-width="2"/><path d="M8 26h4.5c5.3 0 5.3-8 10.3-8H28" stroke="#8195ff" stroke-linecap="round" stroke-width="2"/><circle cx="8" cy="10" fill="#f3f4f1" r="2.2"/><circle cx="8" cy="26" fill="#8195ff" r="2.2"/><circle cx="28" cy="18" fill="#c9ff4a" r="2.75"/></svg></span>'''
MENU_ICON = '''<span aria-hidden="true" class="stage98-menu-icon"><i></i><i></i></span>'''


def route_for(rel: str) -> str:
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-10]
    return '/' + rel


def active_key(rel: str, html: str) -> str:
    clean = rel.removeprefix('en/')
    if clean == 'cases/index.html' or clean.startswith('cases/'):
        return 'cases'
    if clean == 'guides/index.html' or clean.startswith('guides/'):
        return 'guides'
    if 'data-ux-family="service"' in html or clean == 'services/index.html':
        return 'services'
    if clean in {'about/index.html', 'freelance-developer/index.html'}:
        return 'about'
    return 'home'


def extract_language_href(old_header: str, rel: str, is_en: bool) -> str:
    tag = re.search(r'<a\b[^>]*class="[^"]*language-switch[^"]*"[^>]*>', old_header, re.I | re.S)
    if tag:
        hm = re.search(r'\bhref="([^"]+)"', tag.group(0), re.I)
        if hm:
            return hm.group(1)
    if is_en:
        ru_rel = rel[3:]
        if (root / ru_rel).exists():
            return route_for(ru_rel)
        return '/'
    en_rel = 'en/' + rel
    if (root / en_rel).exists():
        return route_for(en_rel)
    return '/en/'


def nav_link(href: str, label: str, key: str, active: str) -> str:
    current = ' aria-current="page"' if key == active else ''
    return f'<a href="{href}"{current}>{label}</a>'


def header_html(rel: str, html: str, old_header: str) -> str:
    is_en = rel.startswith('en/')
    active = active_key(rel, html)
    lang_href = extract_language_href(old_header, rel, is_en)
    if is_en:
        links = [
            nav_link('/en/cases/', 'Cases', 'cases', active),
            nav_link('/en/services/', 'Services', 'services', active),
            nav_link('/en/guides/', 'Guides', 'guides', active),
            nav_link('/en/about/', 'About', 'about', active),
        ]
        lang = f'<a class="stage98-lang" href="{lang_href}" hreflang="ru" lang="ru">RU</a>'
        cta = '<a class="stage98-cta" href="https://t.me/Alexuys" rel="noopener noreferrer" target="_blank">Discuss a project ↗</a>'
        mobile_cta = '<a class="stage98-mobile-cta" href="https://t.me/Alexuys" rel="noopener noreferrer" target="_blank">Discuss a project ↗</a>'
        menu_label = 'Open menu'
    else:
        links = [
            nav_link('/cases/', 'Кейсы', 'cases', active),
            nav_link('/services/', 'Услуги', 'services', active),
            nav_link('/guides/', 'Разборы', 'guides', active),
            nav_link('/#process', 'Процесс', 'process', active),
            nav_link('/about/', 'Обо мне', 'about', active),
        ]
        lang = f'<a class="stage98-lang" href="{lang_href}" hreflang="en" lang="en">EN</a>'
        cta = '<a class="stage98-cta" href="https://t.me/Alexuys" rel="noopener noreferrer" target="_blank">Обсудить проект ↗</a>'
        mobile_cta = '<a class="stage98-mobile-cta" href="https://t.me/Alexuys" rel="noopener noreferrer" target="_blank">Обсудить проект ↗</a>'
        menu_label = 'Открыть меню'

    desktop = ''.join(links) + lang + cta
    mobile = ''.join(links) + lang + mobile_cta
    brand_label = 'Alexuys — home' if is_en else 'Alexuys — на главную'
    return f'''<header class="header stage98-header" data-nosnippet="" id="header">
<div class="container stage98-head">
<a class="stage98-brand" href="/" aria-label="{brand_label}">{MARK}<span class="stage98-brand-copy"><strong>alexuys</strong><small>WEB · APPS · AUTOMATION</small></span></a>
<nav class="stage98-nav" aria-label="{'Main navigation' if is_en else 'Основная навигация'}">{desktop}</nav>
<details class="stage98-mobile-menu"><summary aria-label="{menu_label}">{MENU_ICON}</summary><nav aria-label="{'Mobile navigation' if is_en else 'Мобильная навигация'}">{mobile}</nav></details>
</div>
</header>'''

changed = checked = 0
errors = []
for path in sorted(root.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<main' not in html or '<header' not in html:
        continue
    checked += 1
    rel = str(path.relative_to(root)).replace('\\', '/')
    match = re.search(r'<header\b[^>]*>.*?</header>', html, re.I | re.S)
    if not match:
        errors.append(f'{rel}: header not found')
        continue
    old_header = match.group(0)
    new_header = header_html(rel, html, old_header)
    new = html[:match.start()] + new_header + html[match.end():]
    if new != html:
        path.write_text(new, encoding='utf-8')
        changed += 1

for path in sorted(root.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<main' not in html or '<header' not in html:
        continue
    rel = str(path.relative_to(root)).replace('\\', '/')
    if html.count('class="header stage98-header"') != 1:
        errors.append(f'{rel}: final header missing or duplicated')
    if html.count('class="stage98-mobile-menu"') != 1:
        errors.append(f'{rel}: mobile menu missing or duplicated')
    if html.count('class="stage98-cta"') != 1:
        errors.append(f'{rel}: desktop CTA missing or duplicated')

if errors:
    raise SystemExit('stage98 header unify failed:\n' + '\n'.join(errors[:40]))

print(f'stage98 header unify: changed={changed}; checked={checked}; one desktop/mobile navigation system')
