#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
CSS_MARK = 'data-stage91-filter-css="true"'
JS_MARK = 'data-stage91-filter-js="true"'
CSS_LINK = '<link href="/assets/ux-filters.css?v=20260909-1" rel="stylesheet" data-stage91-filter-css="true"/>'
JS_LINK = '<script defer src="/assets/ux-filters.js?v=20260909-1" data-stage91-filter-js="true"></script>'


def add_assets(text: str) -> str:
    if CSS_MARK not in text:
        text = text.replace('</head>', CSS_LINK + '\n</head>', 1)
    if JS_MARK not in text:
        text = text.replace('</body>', JS_LINK + '\n</body>', 1)
    return text


def add_attr(tag: str, name: str, value: str | None = None) -> str:
    if re.search(rf'\b{re.escape(name)}(?:=|\s|>)', tag, re.I):
        return tag
    attr = name if value is None else f'{name}="{value}"'
    return tag[:-1] + ' ' + attr + '>'


def tag_with_class(text: str, class_name: str, tag_name: str = 'div') -> re.Match[str] | None:
    pat = re.compile(
        rf'<{tag_name}\b(?=[^>]*class=["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\'])[^>]*>',
        re.I | re.S,
    )
    return pat.search(text)


def ensure_grid_id(text: str, class_name: str, grid_id: str) -> str:
    m = tag_with_class(text, class_name)
    if not m:
        raise SystemExit(f'stage91: missing grid .{class_name}')
    tag = m.group(0)
    if re.search(r'\bid=["\']', tag, re.I):
        return text
    tag = add_attr(tag, 'id', grid_id)
    return text[:m.start()] + tag + text[m.end():]


def add_card_category(text: str, href: str, category: str) -> tuple[str, bool]:
    pat = re.compile(
        rf'<a\b(?=[^>]*href=["\']{re.escape(href)}["\'])[^>]*>',
        re.I | re.S,
    )
    m = pat.search(text)
    if not m:
        return text, False
    tag = m.group(0)
    tag = add_attr(tag, 'data-ux-filter-item')
    tag = add_attr(tag, 'data-ux-category', category)
    return text[:m.start()] + tag + text[m.end():], True


def filterbar(target_id: str, buttons: list[tuple[str, str]]) -> str:
    controls = ''.join(
        f'<button type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}" aria-controls="{target_id}">{label}</button>'
        for key, label in buttons
    )
    return (
        f'<div class="ux-filterbar" data-ux-filterbar data-target-id="{target_id}" role="group" aria-label="Фильтр списка">'
        '<span class="ux-filterbar__label">Фильтр</span>'
        + controls
        + '</div>'
        '<p class="ux-filter-empty" data-ux-filter-empty>В этой категории пока нет элементов.</p>'
    )


def insert_before_grid(text: str, class_name: str, html: str) -> str:
    if 'data-ux-filterbar' in text:
        return text
    m = tag_with_class(text, class_name)
    if not m:
        raise SystemExit(f'stage91: cannot place filter before .{class_name}')
    return text[:m.start()] + html + '\n' + text[m.start():]


configs = [
    {
        'route': '/cases/',
        'grid_class': 's50-case-list',
        'grid_id': 'case-catalog',
        'buttons': [('all', 'Все'), ('web', 'Web / AI'), ('telegram', 'Telegram'), ('crm', 'CRM'), ('mobile', 'Mobile'), ('seo', 'SEO')],
        'cards': {
            '/cases/freelance-os/': 'crm',
            '/cases/siteaudit-studio/': 'seo',
            '/cases/seo-control-center/': 'seo',
            '/cases/sheetpilot-ai/': 'web',
            '/cases/fin-planner/': 'telegram',
            '/cases/swift-calendar/': 'mobile',
            '/cases/auto-crm/': 'crm',
            '/cases/factory-catalog/': 'web',
            '/cases/taxi-app/': 'mobile',
        },
    },
    {
        'route': '/guides/',
        'grid_class': 's50-guide-grid',
        'grid_id': 'guide-catalog',
        'buttons': [('all', 'Все'), ('telegram', 'Telegram'), ('automation', 'Automation'), ('crm', 'CRM'), ('web', 'Web'), ('process', 'Процесс')],
        'cards': {
            '/guides/telegram-bot-cost/': 'telegram',
            '/guides/telegram-bot-brief/': 'telegram',
            '/guides/bot-vs-mini-app-vs-web/': 'telegram',
            '/guides/n8n-vs-make/': 'automation',
            '/guides/n8n-vs-backend/': 'automation',
            '/guides/custom-crm-or-ready/': 'crm',
            '/guides/site-vs-web-app/': 'web',
            '/guides/development-cost/': 'process',
            '/guides/repair-vs-rewrite/': 'process',
        },
    },
    {
        'route': '/tools/',
        'grid_class': 'dt-grid',
        'grid_id': 'tools-list',
        'buttons': [('all', 'Все'), ('dev', 'Dev'), ('seo', 'SEO'), ('marketing', 'Marketing')],
        'cards': {
            '/tools/json-formatter/': 'dev',
            '/tools/cron-builder/': 'dev',
            '/tools/jwt-decoder/': 'dev',
            '/tools/robots-validator/': 'seo',
            '/tools/sitemap-validator/': 'seo',
            '/tools/utm-builder/': 'marketing',
        },
    },
]

changed: list[str] = []
for cfg in configs:
    path = root / cfg['route'].strip('/') / 'index.html'
    if not path.is_file():
        raise SystemExit(f"stage91: missing {cfg['route']}")
    text = path.read_text(encoding='utf-8')
    original = text
    text = add_assets(text)
    text = ensure_grid_id(text, cfg['grid_class'], cfg['grid_id'])

    missing: list[str] = []
    for href, category in cfg['cards'].items():
        text, found = add_card_category(text, href, category)
        if not found:
            missing.append(href)
    if missing:
        raise SystemExit(f"stage91: {cfg['route']} missing mapped cards: {', '.join(missing)}")

    text = insert_before_grid(text, cfg['grid_class'], filterbar(cfg['grid_id'], cfg['buttons']))

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(cfg['route'])

# Final guard: each filtered page has assets, controls and one category per expected card.
problems: list[str] = []
for cfg in configs:
    path = root / cfg['route'].strip('/') / 'index.html'
    text = path.read_text(encoding='utf-8')
    if CSS_MARK not in text or JS_MARK not in text or 'data-ux-filterbar' not in text:
        problems.append(cfg['route'] + ':assets-or-controls')
    if len(re.findall(r'data-ux-filter-item(?:\s|>)', text)) < len(cfg['cards']):
        problems.append(cfg['route'] + ':card-count')
    if f'id="{cfg["grid_id"]}"' not in text:
        problems.append(cfg['route'] + ':grid-id')

if problems:
    raise SystemExit('stage91 catalog filter invariant failed: ' + ', '.join(problems))

print('stage91 catalog filters: ' + ', '.join(changed))
