#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import json
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BASE = 'https://alexgtup.github.io'
DATE = '2026-09-10'

DEMO_CARDS = '''<article class="growth-card" data-stage106-demo="siteaudit-studio"><span class="growth-label">SEO · CRAWLER · WEB</span><h3>SiteAudit Studio</h3><p>Технический аудит публичного сайта: HTTP, robots.txt, sitemap, canonical, метаданные, ссылки, accessibility и security-сигналы.</p><p><strong>Что проверить:</strong> запустите аудит тестового URL, откройте конкретные найденные сигналы и сравните их с исходной страницей.</p><div class="growth-actions"><a class="growth-link primary" data-demo="siteaudit-studio" href="https://siteaudit-studio.onrender.com/" target="_blank" rel="noopener noreferrer">Открыть сервис</a><a class="growth-link" href="/cases/siteaudit-studio/">Разбор проекта</a></div><p>Сервис использует объяснимые технические проверки и показывает, почему найден конкретный риск.</p></article><article class="growth-card" data-stage106-demo="freelance-os"><span class="growth-label">CRM · LOCAL-FIRST · JAVASCRIPT</span><h3>FreelanceOS</h3><p>Local-first CRM для личной фриланс-практики: лиды, pipeline, follow-up, задачи, источники, бюджет и выручка без регистрации.</p><p><strong>Что проверить:</strong> загрузите demo-данные, проведите лид по воронке, добавьте follow-up и посмотрите, как меняется аналитика.</p><div class="growth-actions"><a class="growth-link primary" data-demo="freelance-os" href="/freelance-os/">Открыть CRM</a><a class="growth-link" href="/cases/freelance-os/">Разбор проекта</a></div><p>В текущем MVP данные остаются в браузере пользователя; резервная копия переносится через JSON export/import.</p></article>'''

VALIDATOR_ACTIONS = '''<div class="actions" data-stage106-seo-tools="true" style="margin-top:1rem"><a class="btn" href="/tools/robots-validator/">Проверить robots.txt →</a><a class="btn" href="/tools/sitemap-validator/">Проверить sitemap.xml →</a></div>'''

SITEAUDIT_DESCRIPTION = (
    'SiteAudit Studio - кейс web-сервиса для технического SEO-аудита: HTTP, robots.txt, '
    'sitemap, canonical, метаданные, ссылки и безопасный crawler.'
)

DEMOS_SCHEMA = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    '@id': BASE + '/demos/#page',
    'url': BASE + '/demos/',
    'name': 'Демо веб-сервисов и примеры разработки',
    'inLanguage': 'ru-RU',
    'mainEntity': {
        '@type': 'ItemList',
        'itemListElement': [
            {
                '@type': 'ListItem',
                'position': 1,
                'item': {
                    '@type': 'SoftwareApplication',
                    'name': 'SheetPilot AI',
                    'applicationCategory': 'BusinessApplication',
                    'url': BASE + '/cases/sheetpilot-ai/',
                },
            },
            {
                '@type': 'ListItem',
                'position': 2,
                'item': {
                    '@type': 'SoftwareApplication',
                    'name': 'SEO Control Center',
                    'applicationCategory': 'DeveloperApplication',
                    'url': BASE + '/cases/seo-control-center/',
                },
            },
            {
                '@type': 'ListItem',
                'position': 3,
                'item': {
                    '@type': 'SoftwareApplication',
                    'name': 'SiteAudit Studio',
                    'applicationCategory': 'DeveloperApplication',
                    'url': BASE + '/cases/siteaudit-studio/',
                },
            },
            {
                '@type': 'ListItem',
                'position': 4,
                'item': {
                    '@type': 'SoftwareApplication',
                    'name': 'FreelanceOS',
                    'applicationCategory': 'BusinessApplication',
                    'url': BASE + '/freelance-os/',
                },
            },
        ],
    },
}


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f'stage106: missing {rel}')
    return path.read_text(encoding='utf-8')


def write(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding='utf-8')


def patch_demos() -> bool:
    rel = 'demos/index.html'
    text = read(rel)
    if 'data-stage106-demo="siteaudit-studio"' in text and 'data-stage106-demo="freelance-os"' in text:
        return False
    section_match = re.search(r'<section\b[^>]*id=["\']demo-products["\'][^>]*>.*?</section>', text, re.I | re.S)
    if not section_match:
        raise SystemExit('stage106: #demo-products section missing')
    section = section_match.group(0)
    shell_close = section.rfind('</div>')
    grid_close = section.rfind('</div>', 0, shell_close)
    if grid_close < 0:
        raise SystemExit('stage106: demo grid close not found')
    new_section = section[:grid_close] + DEMO_CARDS + section[grid_close:]
    text = text[:section_match.start()] + new_section + text[section_match.end():]
    write(rel, text)
    return True


def patch_demos_schema() -> bool:
    rel = 'demos/index.html'
    text = read(rel)
    marker = 'data-stage106-demos-schema="true"'
    if marker in text:
        return False
    if '</head>' not in text:
        raise SystemExit('stage106: demos head missing')
    payload = json.dumps(DEMOS_SCHEMA, ensure_ascii=False, separators=(',', ':'))
    script = f'<script type="application/ld+json" {marker}>{payload}</script>'
    text = text.replace('</head>', script + '</head>', 1)
    write(rel, text)
    return True


def patch_crm_related_nav() -> bool:
    rel = 'crm-development/index.html'
    text = read(rel)
    marker = 'data-stage106-freelanceos="true"'
    if marker in text:
        return False
    section_match = re.search(r'<section\b[^>]*data-stage101-related=["\']true["\'][^>]*>.*?</section>', text, re.I | re.S)
    if not section_match:
        raise SystemExit('stage106: CRM Stage101 related section missing')
    section = section_match.group(0)
    nav_match = re.search(r'<nav\b[^>]*class=["\'][^"\']*\bs101-more\b[^"\']*["\'][^>]*>.*?</nav>', section, re.I | re.S)
    if not nav_match:
        raise SystemExit('stage106: CRM related nav missing')
    nav = nav_match.group(0)
    link = '<a data-stage106-freelanceos="true" href="/freelance-os/">Живой CRM-продукт</a>'
    new_nav = nav.replace('</nav>', link + '</nav>', 1)
    new_section = section[:nav_match.start()] + new_nav + section[nav_match.end():]
    text = text[:section_match.start()] + new_section + text[section_match.end():]
    write(rel, text)
    return True


def patch_siteaudit_tools() -> bool:
    rel = 'cases/siteaudit-studio/index.html'
    text = read(rel)
    if 'data-stage106-seo-tools="true"' in text:
        return False
    section_match = re.search(r'<section\b[^>]*id=["\']case-overview["\'][^>]*>.*?</section>', text, re.I | re.S)
    if not section_match:
        raise SystemExit('stage106: SiteAudit overview missing')
    section = section_match.group(0)
    grid_start = re.search(r'<div\b[^>]*class=["\'][^"\']*\bgrid\b[^"\']*["\'][^>]*>', section, re.I)
    if not grid_start:
        raise SystemExit('stage106: SiteAudit overview grid missing')
    container_close = section.rfind('</div>')
    grid_close = section.rfind('</div>', 0, container_close)
    if grid_close < grid_start.end():
        raise SystemExit('stage106: SiteAudit grid close not found')
    new_section = section[:grid_close + 6] + VALIDATOR_ACTIONS + section[grid_close + 6:]
    text = text[:section_match.start()] + new_section + text[section_match.end():]
    write(rel, text)
    return True


def patch_siteaudit_description() -> bool:
    rel = 'cases/siteaudit-studio/index.html'
    text = read(rel)
    pattern = re.compile(r'<meta\b(?=[^>]*\bname=["\']description["\'])[^>]*>', re.I)
    match = pattern.search(text)
    if not match:
        raise SystemExit('stage106: SiteAudit meta description missing')
    replacement = f'<meta name="description" content="{SITEAUDIT_DESCRIPTION}"/>'
    if match.group(0) == replacement:
        return False
    text = text[:match.start()] + replacement + text[match.end():]
    write(rel, text)
    return True


def update_lastmod(urls: list[str]) -> int:
    path = ROOT / 'sitemap.xml'
    if not path.is_file():
        raise SystemExit('stage106: sitemap.xml missing')
    text = path.read_text(encoding='utf-8')
    changed = 0
    for url in urls:
        pattern = re.compile(rf'(<loc>{re.escape(url)}</loc>\s*<lastmod>)[^<]+(</lastmod>)')
        text, count = pattern.subn(rf'\g<1>{DATE}\g<2>', text, count=1)
        if count != 1:
            raise SystemExit(f'stage106: sitemap URL missing: {url}')
        changed += 1
    path.write_text(text, encoding='utf-8')
    return changed


def route_for_file(path: Path) -> str | None:
    rel = path.relative_to(ROOT).as_posix()
    if not rel.endswith('index.html'):
        return None
    parent = rel[:-len('index.html')].strip('/')
    return '/' if not parent else '/' + parent + '/'


def normalize_internal(href: str) -> str | None:
    if href.startswith('/'):
        path = urlparse(href).path
    elif href.startswith(BASE):
        path = urlparse(href).path
    else:
        return None
    if not path:
        return '/'
    if path.endswith('/'):
        return path
    if '.' not in path.rsplit('/', 1)[-1]:
        return path + '/'
    return None


def inbound_nonself(target: str) -> set[str]:
    sources: set[str] = set()
    href_re = re.compile(r'<a\b[^>]*href=["\']([^"\']+)["\']', re.I)
    for path in ROOT.rglob('index.html'):
        source = route_for_file(path)
        if not source or source == target:
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        if any(normalize_internal(href) == target for href in href_re.findall(text)):
            sources.add(source)
    return sources


changed_routes: set[str] = set()
if patch_demos():
    changed_routes.add('/demos/')
if patch_demos_schema():
    changed_routes.add('/demos/')
if patch_crm_related_nav():
    changed_routes.add('/crm-development/')
if patch_siteaudit_tools():
    changed_routes.add('/cases/siteaudit-studio/')
if patch_siteaudit_description():
    changed_routes.add('/cases/siteaudit-studio/')

lastmod = update_lastmod([BASE + route for route in sorted(changed_routes)]) if changed_routes else 0

# User-facing and search-quality guards.
demos = read('demos/index.html')
if len(re.findall(r'<article\b[^>]*class=["\'][^"\']*\bgrowth-card\b', demos, re.I)) != 4:
    raise SystemExit('stage106: demos catalog must contain exactly four product cards')
for required in (
    'data-demo="sheetpilot-ai"', 'data-demo="seo-control-center"',
    'data-demo="siteaudit-studio"', 'data-demo="freelance-os"',
    'data-stage106-demos-schema="true"', '"@type":"CollectionPage"', '"@type":"ItemList"',
):
    if required not in demos:
        raise SystemExit(f'stage106: demos marker/schema missing: {required}')

siteaudit = read('cases/siteaudit-studio/index.html')
for target in ('/tools/robots-validator/', '/tools/sitemap-validator/'):
    if f'href="{target}"' not in siteaudit:
        raise SystemExit(f'stage106: SiteAudit direct tool link missing: {target}')
if SITEAUDIT_DESCRIPTION not in siteaudit or len(SITEAUDIT_DESCRIPTION) > 155:
    raise SystemExit('stage106: SiteAudit description guard failed')

minimums = {
    '/freelance-os/': 3,
    '/tools/robots-validator/': 3,
    '/tools/sitemap-validator/': 3,
}
counts: dict[str, int] = {}
for target, minimum in minimums.items():
    sources = inbound_nonself(target)
    counts[target] = len(sources)
    if len(sources) < minimum:
        raise SystemExit(
            f'stage106: weak inbound graph remains for {target}: {len(sources)} < {minimum}; '
            + ', '.join(sorted(sources))
        )

summary = ', '.join(f'{target}={count}' for target, count in counts.items())
print(
    f'stage106 proof graph: changed={",".join(sorted(changed_routes)) or "none"}; lastmod={lastmod}; '
    f'demo_cards=4; demos_schema=CollectionPage+ItemList; siteaudit_desc={len(SITEAUDIT_DESCRIPTION)}; '
    f'nonself_inbound: {summary}'
)
