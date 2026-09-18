#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BASE = 'https://alexgtup.github.io'
TODAY = '2026-09-18'


def page(rel: str) -> tuple[Path, str]:
    p = ROOT / rel / 'index.html'
    if not p.is_file():
        raise SystemExit(f'stage182: missing {rel}')
    return p, p.read_text(encoding='utf-8')


def set_meta(doc: str, title: str, desc: str) -> str:
    doc, n = re.subn(r'<title>.*?</title>', '<title>'+html.escape(title)+'</title>', doc, count=1, flags=re.I|re.S)
    if n != 1:
        raise SystemExit('stage182: title not found')
    replacements = [
        ('name', 'description', desc),
        ('property', 'og:title', title),
        ('property', 'og:description', desc),
        ('name', 'twitter:title', title),
        ('name', 'twitter:description', desc),
    ]
    for attr, key, value in replacements:
        pat = rf'<meta\b(?=[^>]*\b{attr}=["\']{re.escape(key)}["\'])[^>]*>'
        repl = f'<meta {attr}="{key}" content="{html.escape(value, quote=True)}"/>'
        if re.search(pat, doc, re.I):
            doc = re.sub(pat, repl, doc, count=1, flags=re.I)
        else:
            doc = doc.replace('</head>', repl + '</head>', 1)
    return doc


def replace_once(doc: str, old: str, new: str, label: str) -> str:
    if new in doc:
        return doc
    if old not in doc:
        raise SystemExit(f'stage182: marker missing: {label}')
    return doc.replace(old, new, 1)

# 1) Telegram bots: query already averages position ~7 but had no clicks.
p, s = page('telegram-bots')
title = 'Разработчик Telegram-ботов на заказ - кейсы и цена | Alexuys'
desc = 'Разработчик Telegram-ботов на заказ: заявки, CRM/API, оплаты и автоматизация. Реальный кейс, исходники у заказчика; первый рабочий этап от 15 000 ₽.'
s = set_meta(s, title, desc)
s = replace_once(
    s,
    '<p class="p129-lead">Бот для заявок, оплат, уведомлений или внутренних задач. Сначала запускаем один понятный сценарий, затем при необходимости подключаем CRM, платежи и другие сервисы. Первый этап — от 15 000 ₽.</p>',
    '<p class="p129-lead">Бот для заявок, оплат, уведомлений или внутренних задач. Работа напрямую с разработчиком: сначала запускается один понятный сценарий, затем при необходимости подключаются CRM, платежи и другие сервисы. Первый рабочий этап — от 15 000 ₽, исходники остаются у заказчика.</p>',
    'telegram lead',
)
# Keep Service schema wording aligned with the visible offer without changing the price semantics.
s = s.replace(
    '"description":"Разработка Telegram-ботов на заказ от 15 000 ₽: заявки, CRM/API, оплаты, подписки и Mini Apps. Исходники и доступы; отзывы и история работ доступны в публичном профиле Freelance.ru."',
    '"description":"Разработка Telegram-ботов на заказ: заявки, CRM/API, оплаты, подписки и Mini Apps. Первый рабочий этап от 15 000 ₽; исходники и доступы остаются у заказчика."',
    1,
)
p.write_text(s, encoding='utf-8')

# 2) Cost guide: match the strongest price query and give a concrete but non-misleading answer.
p, s = page('guides/telegram-bot-cost')
title = 'Сколько стоит сделать Telegram-бота на заказ в 2026 | Alexuys'
desc = 'Сколько стоит сделать Telegram-бота на заказ в 2026: первый рабочий этап от 15 000 ₽. Итоговая цена зависит от сценариев, CRM/API, оплат, базы и Mini App.'
s = set_meta(s, title, desc)
price_answer = '''<div class="callout" data-stage182-price-answer="true"><b>Практический ориентир:</b> первый рабочий этап Telegram-бота — от 15 000 ₽. Это не фиксированная цена любого бота: итоговая оценка зависит от числа сценариев, хранения данных, CRM/API, оплат, Mini App и требований к запуску.</div>'''
if 'data-stage182-price-answer="true"' not in s:
    anchor = '<section id="factors"><h2>Что сильнее всего влияет на стоимость</h2>'
    if anchor not in s:
        raise SystemExit('stage182: cost factors anchor missing')
    s = s.replace(anchor, price_answer + anchor, 1)
p.write_text(s, encoding='utf-8')

# 3) Telegram Mini App: already averages ~4.75, so improve the commercial snippet rather than create a duplicate page.
p, s = page('telegram-mini-apps')
title = 'Telegram Mini App на заказ - разработка под ключ | Alexuys'
desc = 'Telegram Mini App на заказ: каталог, кабинет, формы, оплаты, backend и Bot API. Полный пользовательский сценарий внутри Telegram без отдельной установки приложения.'
s = set_meta(s, title, desc)
s = replace_once(
    s,
    '<p class="p129-lead">Если в Telegram нужны каталог, кабинет, сложная форма или несколько экранов, удобнее открыть полноценный интерфейс прямо внутри мессенджера — без отдельной установки приложения.</p>',
    '<p class="p129-lead">Telegram Mini App на заказ как цельный сценарий: интерфейс, авторизация, backend, Bot API, данные и интеграции. Подходит для каталога, кабинета, сложной формы или оплаты внутри Telegram — без отдельной установки приложения.</p>',
    'mini app lead',
)
p.write_text(s, encoding='utf-8')

# 4) Fin Planner: Yandex already shows the case for control-of-income/expenses variants at positions 6–12.
p, s = page('cases/fin-planner')
title = 'Telegram-бот для контроля доходов и расходов | кейс Fin Planner'
desc = 'Fin Planner — Telegram-бот для учета и контроля доходов и расходов, бюджета, регулярных трат, баланса и финансовой статистики. Реальный интерфейс и сценарии.'
s = set_meta(s, title, desc)
s = replace_once(
    s,
    '<h1>Telegram-бот для учета доходов и расходов — Fin Planner.</h1>',
    '<h1>Telegram-бот для контроля доходов и расходов — Fin Planner.</h1>',
    'fin planner h1',
)
p.write_text(s, encoding='utf-8')

# Freshness only for materially changed URLs.
targets = {
    f'{BASE}/telegram-bots/',
    f'{BASE}/guides/telegram-bot-cost/',
    f'{BASE}/telegram-mini-apps/',
    f'{BASE}/cases/fin-planner/',
}
for name in ('sitemap.xml', 'sitemap-google.xml'):
    sm = ROOT / name
    if not sm.exists():
        continue
    text = sm.read_text(encoding='utf-8')
    for url in targets:
        text = re.sub(r'(<loc>'+re.escape(url)+r'</loc><lastmod>)[^<]+', rf'\g<1>{TODAY}', text, count=1)
    sm.write_text(text, encoding='utf-8')

# Hard guards prevent future stages from silently reverting this data-led pass.
guards = {
    'telegram-bots': ['Разработчик Telegram-ботов на заказ - кейсы и цена', 'Первый рабочий этап — от 15 000 ₽'],
    'guides/telegram-bot-cost': ['Сколько стоит сделать Telegram-бота на заказ в 2026', 'data-stage182-price-answer="true"'],
    'telegram-mini-apps': ['Telegram Mini App на заказ - разработка под ключ', 'Telegram Mini App на заказ как цельный сценарий'],
    'cases/fin-planner': ['Telegram-бот для контроля доходов и расходов', 'учета и контроля доходов и расходов'],
}
for rel, needles in guards.items():
    data = (ROOT / rel / 'index.html').read_text(encoding='utf-8')
    for needle in needles:
        if needle not in data:
            raise SystemExit(f'stage182: guard failed {rel}: {needle}')

print(f'stage182 yandex ctr clusters: pages={len(guards)}')
