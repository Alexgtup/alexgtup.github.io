#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html as htmlmod
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
CSS_MARK = 'data-stage95-prune="true"'
CSS_LINK = '<link href="/assets/stage95-prune.css?v=20260909-1" rel="stylesheet" data-stage95-prune="true"/>'

SERVICE_ROUTES = {
    '/development/', '/telegram-bots/', '/telegram-mini-apps/', '/n8n-automation/',
    '/crm-development/', '/web-development/', '/backend-development/', '/api-integrations/',
    '/project-repair/', '/telegram-bot-repair/', '/mvp-development/', '/ios-development/',
    '/python-development/', '/ai-automation/', '/app-development/'
}

def route_for(path: Path) -> str:
    rel = path.relative_to(root)
    if rel.name != 'index.html':
        return ''
    parent = str(rel.parent).replace('\\', '/')
    return '/' if parent == '.' else '/' + parent.strip('/') + '/'

def main_bounds(text: str):
    start = re.search(r'<main\b[^>]*>', text, re.I)
    if not start:
        return None
    end = re.search(r'</main>', text[start.end():], re.I)
    if not end:
        return None
    return start.start(), start.end(), start.end() + end.start(), start.end() + end.end()

def top_sections(text: str):
    bounds = main_bounds(text)
    if not bounds:
        return []
    _, main_start, main_end, _ = bounds
    fragment = text[main_start:main_end]
    token_re = re.compile(r'<section\b[^>]*>|</section\s*>', re.I)
    depth = 0
    start = None
    out = []
    for match in token_re.finditer(fragment):
        token = match.group(0)
        if token.lower().startswith('<section'):
            if depth == 0:
                start = match.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0 and start is not None:
                full = fragment[start:match.end()]
                opening = re.match(r'<section\b[^>]*>', full, re.I).group(0)
                id_match = re.search(r'\bid=["\']([^"\']+)["\']', opening, re.I)
                class_match = re.search(r'\bclass=["\']([^"\']+)["\']', opening, re.I)
                heading_match = re.search(r'<h[12]\b[^>]*>(.*?)</h[12]>', full, re.I | re.S)
                heading = re.sub(r'<[^>]+>', ' ', heading_match.group(1)) if heading_match else ''
                heading = re.sub(r'\s+', ' ', htmlmod.unescape(heading)).strip()
                out.append({
                    'start': main_start + start,
                    'end': main_start + match.end(),
                    'html': full,
                    'id': id_match.group(1) if id_match else None,
                    'classes': class_match.group(1).split() if class_match else [],
                    'heading': heading,
                })
                start = None
    return out

def remove_sections(text: str, predicate):
    while True:
        section = next((s for s in top_sections(text) if predicate(s)), None)
        if not section:
            return text
        text = text[:section['start']] + text[section['end']:]

def remove_nav(text: str, class_name: str) -> str:
    return re.sub(
        rf'\s*<nav\b[^>]*class=["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\'][^>]*>.*?</nav>',
        '', text, flags=re.I | re.S,
    )

def wrap_adjacent_ids(text: str, first_id: str, second_id: str, wrapper: str) -> str:
    if f'class="{wrapper}"' in text:
        return text
    sections = top_sections(text)
    first = next((i for i, s in enumerate(sections) if s['id'] == first_id), None)
    second = next((i for i, s in enumerate(sections) if s['id'] == second_id), None)
    if first is None or second is None or second != first + 1:
        return text
    a, b = sections[first], sections[second]
    between = text[a['end']:b['start']]
    replacement = f'<div class="{wrapper}">{a["html"]}{between}{b["html"]}</div>'
    return text[:a['start']] + replacement + text[b['end']:]

def add_class_to_heading_section(text: str, heading_prefix: str, class_name: str) -> str:
    for section in top_sections(text):
        if not section['heading'].startswith(heading_prefix):
            continue
        opening = re.match(r'<section\b[^>]*>', section['html'], re.I).group(0)
        if class_name in opening:
            return text
        if 'class="' in opening:
            new_open = opening.replace('class="', f'class="{class_name} ', 1)
        elif "class='" in opening:
            new_open = opening.replace("class='", f"class='{class_name} ", 1)
        else:
            new_open = opening[:-1] + f' class="{class_name}">'
        new_section = section['html'].replace(opening, new_open, 1)
        return text[:section['start']] + new_section + text[section['end']:]
    return text

def inject_css(text: str) -> str:
    if CSS_MARK not in text:
        text = text.replace('</head>', CSS_LINK + '\n</head>', 1)
    return text

def simplify_home(text: str) -> str:
    text = remove_nav(text, 'ux-quicknav')
    text = remove_sections(text, lambda s: 'growth-section' in s['classes'] and 'Демо и разборы продуктов' in s['heading'])
    text = remove_sections(text, lambda s: s['id'] == 'process')
    text = wrap_adjacent_ids(text, 'about', 'budget', 'stage95-home-model')
    replacements = {
        '02 / ПРОЕКТЫ': 'ПРОЕКТЫ',
        'Выберите проект. <em>Оцените результат.</em>': 'Выбранные проекты. <em>Реальная работа.</em>',
        'На главной только короткая витрина. Четыре проекта за раз, быстрый фильтр по типу задачи и переход в полноценный кейс без длинного чтения.': 'CRM, автоматизация, web, mobile и Telegram. Коротко о задаче, интерфейсе и результате.',
        '<strong>SHOWCASE</strong>': '<strong>Проекты</strong>',
        '<small>Project radar</small><strong>Найти похожую задачу</strong>': '<small>Фильтр</small><strong>Направление</strong>',
        'Открыть всю библиотеку ↗': 'Все кейсы ↗',
        'Листайте стрелками или свайпом. Фильтр меняет набор проектов без перезагрузки.': '',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def simplify_cases_hub(text: str) -> str:
    text = remove_nav(text, 'ux-content-nav')
    text = remove_nav(text, 'ux-quicknav')
    text = remove_sections(text, lambda s: 'growth-section' in s['classes'])
    text = remove_sections(text, lambda s: 's50-section' in s['classes'] and s['heading'].startswith('Кейс — не доказательство'))
    text = re.sub(r'<div class="case-library__head">.*?</div><div class="case-library__layout">', '<div class="case-library__layout">', text, count=1, flags=re.S)
    text = text.replace('<span>Project radar</span>', '<span>Фильтр</span>')
    text = text.replace('<span>Фильтр работает без перезагрузки</span>', '')
    text = text.replace('Сбросить фильтр', 'Сбросить')
    return text

def simplify_services_hub(text: str) -> str:
    text = remove_nav(text, 'ux-content-nav')
    text = remove_nav(text, 'ux-quicknav')
    bad = ('Отдельные направления для точного входа.', 'Это нормально. Можно начать с проблемы.')
    return remove_sections(text, lambda s: any(s['heading'].startswith(x) for x in bad) or 's68-entry' in s['classes'] or (not s['classes'] and not s['heading']))

def simplify_guides_hub(text: str) -> str:
    text = remove_nav(text, 'ux-content-nav')
    text = remove_nav(text, 'ux-quicknav')
    return remove_sections(text, lambda s: s['heading'].startswith('Решение стало понятнее?'))

def simplify_tools_hub(text: str) -> str:
    text = remove_nav(text, 'ux-content-nav')
    text = remove_nav(text, 'ux-quicknav')
    return remove_sections(text, lambda s: s['heading'].startswith('Инструмент должен экономить действие'))

def simplify_about(text: str) -> str:
    text = remove_nav(text, 'ux-content-nav')
    text = remove_nav(text, 'ux-quicknav')
    return remove_sections(text, lambda s: 'growth-section' in s['classes'])

def simplify_freelance(text: str) -> str:
    text = remove_nav(text, 'ux-content-nav')
    text = remove_nav(text, 'ux-quicknav')
    return remove_sections(text, lambda s: 's68-entry' in s['classes'])

def simplify_service(text: str) -> str:
    text = remove_nav(text, 'ux-quicknav')
    sections = top_sections(text)
    has_proof = any(('s48-proof' in s['classes']) or s['id'] == 'case' for s in sections)
    kept_proof_growth = False
    def remove(section):
        nonlocal kept_proof_growth
        if 's52' in section['classes'] or 's66-tool-link' in section['classes'] or 's68-entry' in section['classes']:
            return True
        if 'Нужно исправить или расширить Telegram-бота?' in section['heading']:
            return True
        if 'growth-section' in section['classes']:
            if not has_proof and not kept_proof_growth and section['heading'].startswith('Реализация на примере проектов'):
                kept_proof_growth = True
                return False
            return True
        return False
    text = remove_sections(text, remove)
    text = add_class_to_heading_section(text, 'Реализация на примере проектов', 'stage95-proof-strip')
    text = add_class_to_heading_section(text, 'Отзывы — на независимой площадке.', 'stage95-review-strip')
    text = wrap_adjacent_ids(text, 'fit', 'result', 'stage95-service-core')
    text = wrap_adjacent_ids(text, 'budget', 'process', 'stage95-service-meta')
    return text

def simplify_case_detail(text: str) -> str:
    text = remove_nav(text, 'ux-content-nav')
    text = remove_nav(text, 'ux-quicknav')
    text = remove_sections(text, lambda s: 'growth-section' in s['classes'])
    sections = top_sections(text)
    has_final_contact = any(('contact' in s['classes'] or 's51-contact' in s['classes']) for s in sections[-2:])
    if has_final_contact:
        text = remove_sections(text, lambda s: not s['classes'] and s['heading'].startswith('Нужен похожий'))
    return text

def simplify_en(text: str, route: str) -> str:
    if route.startswith('/en/guides/') and route != '/en/guides/':
        text = remove_sections(text, lambda s: not s['heading'] and 'intl-container' in s['classes'])
        return remove_sections(text, lambda s: s['heading'].startswith('Useful next pages.'))
    if route.startswith('/en/') and route not in {'/en/', '/en/services/', '/en/cases/', '/en/guides/', '/en/about/', '/en/privacy/'}:
        text = remove_sections(text, lambda s: not s['heading'] and 'intl-container' in s['classes'])
        text = remove_sections(text, lambda s: s['heading'].startswith('Useful next pages.'))
    return text

changed = 0
stats = {}
for path in sorted(root.rglob('*.html')):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '<body' not in text or '<main' not in text or '</head>' not in text:
        continue
    route = route_for(path)
    if not route:
        continue
    original = text
    before = len(top_sections(text))
    if route == '/': text = simplify_home(text)
    elif route == '/cases/': text = simplify_cases_hub(text)
    elif route == '/services/': text = simplify_services_hub(text)
    elif route == '/guides/': text = simplify_guides_hub(text)
    elif route == '/tools/': text = simplify_tools_hub(text)
    elif route == '/about/': text = simplify_about(text)
    elif route == '/freelance-developer/': text = simplify_freelance(text)
    elif route in SERVICE_ROUTES: text = simplify_service(text)
    elif route.startswith('/cases/') and route != '/cases/': text = simplify_case_detail(text)
    if route.startswith('/en/'): text = simplify_en(text, route)
    text = inject_css(text)
    if text != original:
        path.write_text(text, encoding='utf-8')
        changed += 1
    stats[route] = (before, len(top_sections(text)))

assert stats['/'][1] <= 6, stats['/']
assert stats['/services/'][1] <= 4, stats['/services/']
assert stats['/cases/'][1] <= 3, stats['/cases/']
for route in SERVICE_ROUTES:
    if route in stats and route != '/telegram-bot-repair/':
        assert stats[route][1] <= 8, (route, stats[route])
for path in root.rglob('*.html'):
    html = path.read_text(encoding='utf-8', errors='ignore')
    route = route_for(path)
    if route and '<body' in html and '<main' in html and '</head>' in html and CSS_MARK not in html:
        raise SystemExit('stage95 stylesheet missing from ' + str(path.relative_to(root)))

print(f'stage95 prune/unify: patched {changed} pages; home={stats.get("/")}; services={stats.get("/services/")}; cases={stats.get("/cases/")}')
