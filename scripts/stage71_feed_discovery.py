#!/usr/bin/env python3
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
feed_path = root / 'feed.xml'
sitemap_path = root / 'sitemap.xml'
if not feed_path.is_file() or not sitemap_path.is_file():
    raise SystemExit('stage71: feed.xml or sitemap.xml missing')

ATOM = 'http://www.w3.org/2005/Atom'
SM = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', ATOM)

base = 'https://alexgtup.github.io'
updated = '2026-09-08T00:00:00Z'
entries = [
    ('/python-development/', 'Python-разработка: API, автоматизация и Telegram', 'Python-разработка для API, Telegram-ботов, автоматизации, обработки данных и backend-задач.'),
    ('/backend-development/', 'Backend-разработка: API, данные и серверная логика', 'Backend-разработка: REST API, базы данных, авторизация, интеграции, фоновые процессы и production-логика.'),
    ('/freelance-os/', 'FreelanceOS — local-first CRM фрилансера', 'Рабочая CRM без регистрации: лиды, pipeline, follow-up, задачи, источники и финансовая аналитика в браузере.'),
    ('/cases/freelance-os/', 'FreelanceOS — кейс CRM от лида до оплаты', 'Кейс разработки local-first CRM для фриланс-практики: workflow, канбан, задачи, аналитика и JSON backup.'),
    ('/tools/', 'DevTools Hub — бесплатные инструменты разработчика', 'Браузерные инструменты без регистрации: JSON, UTM, Cron, JWT, robots.txt и sitemap XML.'),
    ('/tools/robots-validator/', 'robots.txt Validator — проверка robots.txt в браузере', 'Локальная проверка robots.txt: директивы, группы user-agent, sitemap и базовые риски индексации.'),
    ('/tools/sitemap-validator/', 'Sitemap XML Validator — проверка sitemap.xml', 'Локальная проверка sitemap XML: структура, URL, дубли и базовые ошибки без отправки содержимого на сервер.'),
    ('/cases/siteaudit-studio/', 'SiteAudit Studio — кейс технического аудита сайта', 'Кейс web-сервиса для технического SEO-аудита с ограниченным crawler, explainable score и SSRF-защитой.'),
    ('/cases/seo-control-center/', 'SEO Control Center — мониторинг индексации и поисковых метрик', 'Кейс панели для контроля индексации, показов, CTR, позиций и технического состояния страниц.'),
    ('/cases/sheetpilot-ai/', 'SheetPilot AI — обработка Excel с предпросмотром', 'Кейс ассистента для обработки Excel-файлов с предпросмотром изменений и выгрузкой результата.'),
]

# Every discovery target must already belong to the canonical sitemap.
sm_root = ET.parse(sitemap_path).getroot()
locs = {(node.text or '').strip() for node in sm_root.findall(f'.//{{{SM}}}loc') if (node.text or '').strip()}
missing_sitemap = [base + route for route, _, _ in entries if base + route not in locs]
if missing_sitemap:
    raise SystemExit('stage71: discovery target missing from sitemap: ' + ', '.join(missing_sitemap))

feed_tree = ET.parse(feed_path)
feed = feed_tree.getroot()
if feed.tag != f'{{{ATOM}}}feed':
    raise SystemExit('stage71: feed.xml is not Atom')

# Refresh the feed-level updated timestamp.
updated_node = feed.find(f'{{{ATOM}}}updated')
if updated_node is None:
    updated_node = ET.SubElement(feed, f'{{{ATOM}}}updated')
updated_node.text = updated

existing = {}
for entry in feed.findall(f'{{{ATOM}}}entry'):
    ident = entry.find(f'{{{ATOM}}}id')
    if ident is not None and ident.text:
        existing[ident.text.strip()] = entry

added = 0
for route, title, summary in entries:
    url = base + route
    entry = existing.get(url)
    if entry is None:
        entry = ET.SubElement(feed, f'{{{ATOM}}}entry')
        ET.SubElement(entry, f'{{{ATOM}}}title').text = title
        link = ET.SubElement(entry, f'{{{ATOM}}}link')
        link.set('href', url)
        ET.SubElement(entry, f'{{{ATOM}}}id').text = url
        ET.SubElement(entry, f'{{{ATOM}}}updated').text = updated
        ET.SubElement(entry, f'{{{ATOM}}}summary').text = summary
        added += 1
    else:
        title_node = entry.find(f'{{{ATOM}}}title')
        summary_node = entry.find(f'{{{ATOM}}}summary')
        entry_updated = entry.find(f'{{{ATOM}}}updated')
        if title_node is not None: title_node.text = title
        if summary_node is not None: summary_node.text = summary
        if entry_updated is not None: entry_updated.text = updated

feed_tree.write(feed_path, encoding='utf-8', xml_declaration=True)

# Reparse and guard exact discovery coverage + unique ids.
final = ET.parse(feed_path).getroot()
ids = [(node.text or '').strip() for node in final.findall(f'.//{{{ATOM}}}entry/{{{ATOM}}}id')]
if len(ids) != len(set(ids)):
    raise SystemExit('stage71: duplicate Atom entry ids')
missing_feed = [base + route for route, _, _ in entries if base + route not in ids]
if missing_feed:
    raise SystemExit('stage71: target missing from Atom feed: ' + ', '.join(missing_feed))

print(f'stage71: Atom discovery refreshed; {len(entries)} guarded targets, {added} new entries, feed updated={updated}')