#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
CSS_MARK = 'data-stage94-site-ux="true"'
JS_MARK = 'data-stage94-site-ux="true"'
CSS_LINK = '<link href="/assets/stage94-site-ux.css?v=20260909-1" rel="stylesheet" data-stage94-site-ux="true"/>'
JS_LINK = '<script defer src="/assets/stage94-site-ux.js?v=20260909-1" data-stage94-site-ux="true"></script>'

SERVICE_ROUTES = {
    '/development/', '/telegram-bots/', '/telegram-mini-apps/', '/n8n-automation/',
    '/crm-development/', '/web-development/', '/backend-development/', '/api-integrations/',
    '/project-repair/', '/telegram-bot-repair/', '/mvp-development/', '/ios-development/',
    '/python-development/', '/ai-automation/', '/app-development/'
}
CASE_GAPS = {
    '/cases/seo-control-center/': 'case-interface',
    '/cases/siteaudit-studio/': 'case-overview',
    '/cases/freelance-os/': 'case-overview',
}


def route_for(path: Path) -> str:
    rel = path.relative_to(root)
    if rel.name != 'index.html':
        return ''
    parent = str(rel.parent).replace('\\', '/')
    return '/' if parent == '.' else '/' + parent.strip('/') + '/'


def classify(route: str) -> str:
    if route == '/':
        return 'home'
    if route.startswith('/en/'):
        if route == '/en/':
            return 'home'
        if route.startswith('/en/cases/') and route != '/en/cases/':
            return 'case'
        if route.startswith('/en/guides/') and route != '/en/guides/':
            return 'guide'
        if route in {'/en/services/', '/en/cases/', '/en/guides/', '/en/about/'}:
            return 'hub'
        if route == '/en/privacy/':
            return 'legal'
        return 'service'
    if route.startswith('/cases/') and route != '/cases/':
        return 'case'
    if route.startswith('/guides/') and route != '/guides/':
        return 'guide'
    if route.startswith('/tools/') and route != '/tools/':
        return 'tool'
    if route in {'/cases/', '/guides/', '/tools/', '/services/', '/demos/', '/about/', '/freelance-developer/'}:
        return 'hub'
    if route == '/freelance-os/':
        return 'product'
    if route in SERVICE_ROUTES:
        return 'service'
    if route == '/privacy/':
        return 'legal'
    return 'page'


def add_body_family(html: str, family: str) -> str:
    m = re.search(r'<body\b([^>]*)>', html, re.I)
    if not m:
        return html
    tag = m.group(0)
    if 'data-ux-family=' in tag:
        return html
    new = tag[:-1] + f' data-ux-family="{family}">'
    return html[:m.start()] + new + html[m.end():]


def ensure_main(html: str) -> str:
    if re.search(r'<main\b[^>]*\bid=["\']main-content["\']', html, re.I):
        return html
    return re.sub(r'<main\b(?![^>]*\bid=)([^>]*)>', r'<main id="main-content"\1>', html, count=1, flags=re.I)


def ensure_skip(html: str, is_en: bool) -> str:
    if re.search(r'<a\b[^>]*(?:class=["\'][^"\']*skip[^"\']*["\']|href=["\']#main-content["\'])', html, re.I):
        return html
    label = 'Skip to content' if is_en else 'К содержанию'
    link = f'<a class="stage94-skip-link" href="#main-content">{label}</a>'
    return re.sub(r'(<body\b[^>]*>)', r'\1' + link, html, count=1, flags=re.I)


def inject_assets(html: str) -> str:
    if CSS_MARK not in html:
        html = html.replace('</head>', CSS_LINK + '\n</head>', 1)
    if JS_MARK not in html:
        html = html.replace('</body>', JS_LINK + '\n</body>', 1)
    return html


def add_id_to_first_after(html: str, hero_class: str, target_id: str) -> str:
    start = html.find(hero_class)
    if start < 0 or f'id="{target_id}"' in html or f"id='{target_id}'" in html:
        return html
    end = html.find('</section>', start)
    if end < 0:
        return html
    tail = html[end + 10:]
    m = re.search(r'<section\b(?![^>]*\bid=)([^>]*)>', tail, re.I)
    if not m:
        return html
    replacement = '<section id="' + target_id + '"' + m.group(1) + '>'
    pos = end + 10 + m.start()
    return html[:pos] + replacement + html[pos + (m.end() - m.start()):]


def add_actions_after_pattern(html: str, section_class: str, anchor_pattern: str, actions: str) -> str:
    if 'stage94-hero-actions' in html:
        return html
    section_match = re.search(
        rf'<section\b[^>]*class=["\'][^"\']*{re.escape(section_class)}[^"\']*["\'][^>]*>.*?</section>',
        html, re.I | re.S,
    )
    if not section_match:
        return html
    section = section_match.group(0)
    anchors = list(re.finditer(anchor_pattern, section, re.I | re.S))
    if not anchors:
        return html
    anchor = anchors[-1]
    updated = section[:anchor.end()] + actions + section[anchor.end():]
    return html[:section_match.start()] + updated + html[section_match.end():]


def action_row(primary_href: str, primary_text: str, secondary_href: str | None = None, secondary_text: str | None = None) -> str:
    secondary = (
        f'<a class="stage94-action-secondary" href="{secondary_href}">{secondary_text}</a>'
        if secondary_href and secondary_text else ''
    )
    return (
        f'<div class="stage94-hero-actions">'
        f'<a class="stage94-action-primary" href="{primary_href}">{primary_text}</a>'
        f'{secondary}</div>'
    )


changed = 0
full_pages: list[tuple[str, Path]] = []
for path in sorted(root.rglob('*.html')):
    html = path.read_text(encoding='utf-8')
    if '<body' not in html or '<main' not in html or '</head>' not in html:
        continue
    route = route_for(path)
    if not route:
        continue
    original = html
    family = classify(route)
    html = add_body_family(html, family)
    html = ensure_main(html)
    html = ensure_skip(html, route.startswith('/en/'))

    if route in CASE_GAPS:
        target = CASE_GAPS[route]
        if f'id="{target}"' not in html and f"id='{target}'" not in html:
            html = add_id_to_first_after(html, 'hero', target)
        html = add_actions_after_pattern(
            html,
            'hero',
            r'<p\b[^>]*class=["\'][^"\']*lead[^"\']*["\'][^>]*>.*?</p>',
            action_row('#' + target, 'Смотреть интерфейс ↓', '/cases/', 'Все кейсы'),
        )

    if route == '/tools/':
        html = add_id_to_first_after(html, 'dt-hero', 'tool-list')
        html = add_actions_after_pattern(
            html,
            'dt-hero',
            r'<span\b[^>]*class=["\'][^"\']*dt-privacy[^"\']*["\'][^>]*>.*?</span>',
            action_row('#tool-list', 'Открыть инструменты ↓', '/cases/', 'Кейсы'),
        )
    elif route.startswith('/tools/') and route != '/tools/':
        html = add_id_to_first_after(html, 'dt-hero', 'tool-workspace')
        html = add_actions_after_pattern(
            html,
            'dt-hero',
            r'<span\b[^>]*class=["\'][^"\']*dt-privacy[^"\']*["\'][^>]*>.*?</span>',
            action_row('#tool-workspace', 'К инструменту ↓', '/tools/', 'Все инструменты'),
        )
    elif route == '/demos/':
        html = add_actions_after_pattern(
            html,
            'growth-hero',
            r'<p\b[^>]*>.*?</p>',
            action_row('#demo-products', 'Смотреть демо ↓', '/cases/', 'Все кейсы'),
        )

    if route in {'/en/services/', '/en/cases/', '/en/guides/'}:
        html = add_id_to_first_after(html, 'intl-hero', 'browse')
        label = {
            '/en/services/': 'Browse services ↓',
            '/en/cases/': 'Browse cases ↓',
            '/en/guides/': 'Browse guides ↓',
        }[route]
        html = add_actions_after_pattern(
            html,
            'intl-hero',
            r'<p\b[^>]*class=["\'][^"\']*intl-lead[^"\']*["\'][^>]*>.*?</p>',
            action_row('#browse', label),
        )

    html = inject_assets(html)
    if html != original:
        path.write_text(html, encoding='utf-8')
        changed += 1
    full_pages.append((route, path))

missing = []
for route, path in full_pages:
    html = path.read_text(encoding='utf-8')
    if (
        'id="main-content"' not in html
        or 'href="#main-content"' not in html
        or CSS_MARK not in html
        or JS_MARK not in html
        or 'data-ux-family=' not in html
    ):
        missing.append(route)
if missing:
    raise SystemExit('stage94 baseline missing: ' + ', '.join(missing[:12]))

for route in list(CASE_GAPS) + ['/tools/', '/demos/', '/en/services/', '/en/cases/', '/en/guides/']:
    path = root / (route.strip('/') or '.') / 'index.html'
    if path.is_file() and 'stage94-hero-actions' not in path.read_text(encoding='utf-8'):
        raise SystemExit('stage94 hero action missing: ' + route)

print(f'stage94 sitewide UX: patched {changed}/{len(full_pages)} full pages; skip/main/family baseline complete')
