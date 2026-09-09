#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')

REPLACEMENTS = {
    'WORKING FLOW': 'СЦЕНАРИЙ',
    'REAL CASE': 'КЕЙС',
    'BACKEND DEVELOPMENT': 'BACKEND · РАЗРАБОТКА',
    'DATA · WORKFLOW': 'ДАННЫЕ · ПРОЦЕСС',
    'AI AUTOMATION': 'AI · АВТОМАТИЗАЦИЯ',
    'TELEGRAM BOT REPAIR · PYTHON': 'TELEGRAM · ДОРАБОТКА · PYTHON',
    'EXISTING BOT': 'ГОТОВЫЙ БОТ',
    '>REPAIR<': '>ДОРАБОТКА<',
    'TELEGRAM · REAL PROJECT': 'TELEGRAM · КЕЙС',
    'CUSTOM CRM DEVELOPMENT': 'CRM · РАЗРАБОТКА',
    'CRM · INTERNAL PRODUCT': 'CRM · ВНУТРЕННИЙ ПРОДУКТ',
    'LOCAL-FIRST · FREELANCE CRM': 'CRM ДЛЯ ФРИЛАНСЕРА',
    'WHY LOCAL-FIRST': 'ПОЧЕМУ LOCAL-FIRST',
    'NEW LEAD': 'НОВЫЙ ЛИД',
    'TELEGRAM DEVELOPMENT': 'TELEGRAM · РАЗРАБОТКА',
    'TELEGRAM · PRODUCT': 'TELEGRAM · ПРОДУКТ',
    'FREE · LOCAL-FIRST · NO LOGIN': 'БЕЗ ВХОДА · LOCAL-FIRST',
    'WEB DEVELOPMENT': 'WEB · РАЗРАБОТКА',
    'CUSTOM DEVELOPMENT': 'РАЗРАБОТКА',
    'PYTHON DEVELOPMENT': 'PYTHON · РАЗРАБОТКА',
    'MOBILE DEVELOPMENT': 'MOBILE · РАЗРАБОТКА',
    'MVP DEVELOPMENT': 'MVP · РАЗРАБОТКА',
    'PRODUCT · TELEGRAM': 'ПРОДУКТ · TELEGRAM',
    'EXISTING PROJECT REPAIR': 'ДОРАБОТКА ПРОЕКТА',
    'EXISTING PRODUCT · MOBILE': 'MOBILE · ГОТОВЫЙ ПРОДУКТ',
    'N8N / MAKE AUTOMATION': 'N8N / MAKE · АВТОМАТИЗАЦИЯ',
    'WEB · PRODUCT · UX · DECISION GUIDE': 'WEB · PRODUCT · UX · РАЗБОР',
    'N8N · MAKE · BACKEND · DECISION GUIDE': 'N8N · MAKE · BACKEND · РАЗБОР',
    'PROJECT REPAIR · LEGACY · RELEASE · DECISION GUIDE': 'ДОРАБОТКА · LEGACY · RELEASE · РАЗБОР',
    'MOBILE · EXISTING PRODUCT · RELEASE': 'MOBILE · ДОРАБОТКА · RELEASE',
    'LIVE AUDIT': 'LIVE · АУДИТ',
    'TECH SCORE': 'ТЕХНИЧЕСКАЯ ОЦЕНКА',
    'PRODUCT / MVP': 'ПРОДУКТ / MVP',
    'ALEXANDR ALEXANDROV · ALEXUYS · FREELANCE': 'АЛЕКСАНДР · ALEXUYS',
    'ALEXANDR ALEXANDROV · ALEXUYS': 'АЛЕКСАНДР · ALEXUYS',
    'PROJECT LIBRARY · 09 CASES': '9 ПРОЕКТОВ',
    '5 CASES · DIFFERENT FORMATS': '5 КЕЙСОВ · РАЗНЫЕ ФОРМАТЫ',
    'Не листайте всё. <em>Выберите тип задачи.</em>': 'Кейсы по направлениям. <em>Выберите тип задачи.</em>',
    'Полная витрина проектов с коротким описанием, визуальным превью и фильтрацией. Внутри каждого кейса - детали, интерфейс и контекст реализации.': 'Проекты по CRM, Telegram, SEO, web, mobile и автоматизации. Фильтр помогает быстро найти похожую задачу.',
    'Обсудить задачу ↗': 'Обсудить проект ↗',
    'Обсудить в Telegram ↗': 'Обсудить проект ↗',
    'Описать задачу ↗': 'Обсудить проект ↗',
    'Написать напрямую': 'Обсудить проект',
    'Обсудить похожее приложение ↗': 'Обсудить проект ↗',
    'Обсудить похожего бота ↗': 'Обсудить проект ↗',
}

BAD_LABELS = (
    'WORKING FLOW','REAL CASE','CUSTOM DEVELOPMENT','EXISTING PROJECT REPAIR',
    'DECISION GUIDE','ALEXANDR ALEXANDROV · ALEXUYS','PROJECT LIBRARY · 09 CASES'
)

changed = checked = 0
remaining = []
for path in sorted(root.rglob('*.html')):
    rel = str(path.relative_to(root)).replace('\\', '/')
    if rel.startswith('en/'):
        continue
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<main' not in html or '<body' not in html:
        continue
    checked += 1
    m = re.search(r'<body\b[^>]*>', html, re.I)
    if not m:
        continue
    prefix, body = html[:m.end()], html[m.end():]
    original_body = body
    for old, new in REPLACEMENTS.items():
        body = body.replace(old, new)
    if body != original_body:
        path.write_text(prefix + body, encoding='utf-8')
        changed += 1
    for label in BAD_LABELS:
        if label in body:
            remaining.append(f'{rel}: {label}')

if remaining:
    raise SystemExit('stage98 language polish failed:\n' + '\n'.join(remaining[:30]))

print(f'stage98 language polish: changed={changed}; checked={checked}; prototype labels normalized; CTA language unified')
