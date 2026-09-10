#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BASE = 'https://alexgtup.github.io'
DATE = '2026-09-10'

DEMO_CARDS = '''<article class="growth-card" data-stage106-demo="siteaudit-studio"><span class="growth-label">SEO · CRAWLER · WEB</span><h3>SiteAudit Studio</h3><p>Технический аудит публичного сайта: HTTP, robots.txt, sitemap, canonical, метаданные, ссылки, accessibility и security-сигналы.</p><p><strong>Что проверить:</strong> запустите аудит тестового URL, откройте конкретные найденные сигналы и сравните их с исходной страницей.</p><div class="growth-actions"><a class="growth-link primary" data-demo="siteaudit-studio" href="https://siteaudit-studio.onrender.com/" target="_blank" rel="noopener noreferrer">Открыть сервис</a><a class="growth-link" href="/cases/siteaudit-studio/">Разбор проекта</a></div><p>Сервис использует объяснимые технические проверки и показывает, почему найден конкретный риск.</p></article><article class="growth-card" data-stage106-demo="freelance-os"><span class="growth-label">CRM · LOCAL-FIRST · JAVASCRIPT</span><h3>FreelanceOS</h3><p>Local-first CRM для личной фриланс-практики: лиды, pipeline, follow-up, задачи, источники, бюджет и выручка без регистрации.</p><p><strong>Что проверить:</strong> загрузите demo-данные, проведите лид по воронке, добавьте follow-up и посмотрите, как меняется аналитика.</p><div class="growth-actions"><a class="growth-link primary" data-demo="freelance-os" href="/freelance-os/">Открыть CRM</a><a class="growth-link" href="/cases/freelance-os/">Разбор проекта</a></div><p>В текущем MVP данные остаются в браузере пользователя; резервная копия переносится через JSON export/import.</p></article>'''

VALIDATOR_ACTIONS = '''<div class="actions" data-stage106-seo-tools="true" style="margin-top:1rem"><a class="btn" href="/tools/robots-validator/">Проверить robots.txt →</a><a class="btn" href="/tools/sitemap-validator/">Проверить sitemap.xml →</a></div>'''


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
    # The section has .growth-shell > .growth-grid. Insert before the grid close,
    # preserving the existing two-card markup and making the catalog a balanced 4 cards.
    shell_close = section.rfind('</div>')
    grid_close = section.rfind('</div>', 0, shell_close)
    if grid_close < 0:
        raise SystemExit('stage106: demo grid close not found')
    new_section = section[:grid_close] + DEMO_CARDS + section[grid_close:]
    text = text[:section_match.start()] + new_section + text[section_match.end():]
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
    # Find the final grid closing div by walking from the end of the section: container
    # closes last, grid immediately before it.
    container_close = section.rfind('</div>')
    grid_close = section.rfind('</div>', 0, container_close)
    if grid_close < grid_start.end():
        raise SystemExit('stage106: SiteAudit grid close not found')
    new_section = section[:grid_close + 6] + VALIDATOR_ACTIONS + section[grid_close + 6:]
    text = text[:section_match.start()] + new_section + text[section_match.end():]
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


changed_routes: list[str] = []
if patch_demos():
    changed_routes.append('/demos/')
if patch_crm_related_nav():
    changed_routes.append('/crm-development/')
if patch_siteaudit_tools():
    changed_routes.append('/cases/siteaudit-studio/')

# Only source pages received meaningful visible content, so only their lastmod changes.
lastmod = update_lastmod([BASE + route for route in changed_routes]) if changed_routes else 0

# User-facing guards.
demos = read('demos/index.html')
if len(re.findall(r'<article\b[^>]*class=["\'][^"\']*\bgrowth-card\b', demos, re.I)) != 4:
    raise SystemExit('stage106: demos catalog must contain exactly four product cards')
for required in (
    'data-demo="sheetpilot-ai"', 'data-demo="seo-control-center"',
    'data-demo="siteaudit-studio"', 'data-demo="freelance-os"',
):
    if required not in demos:
        raise SystemExit(f'stage106: demo analytics marker missing: {required}')

siteaudit = read('cases/siteaudit-studio/index.html')
for target in ('/tools/robots-validator/', '/tools/sitemap-validator/'):
    if f'href="{target}"' not in siteaudit:
        raise SystemExit(f'stage106: SiteAudit direct tool link missing: {target}')

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
    f'stage106 proof graph: changed={",".join(changed_routes) or "none"}; lastmod={lastmod}; '
    f'demo_cards=4; nonself_inbound: {summary}'
)
