#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

H1_REPLACEMENTS = {
    "telegram-bots/index.html": (
        '<h1>Разработка Telegram-бота под вашу задачу. <em>От первого сценария до запуска.</em></h1>',
        '<h1>Разработка Telegram-ботов на заказ. <em>От первого сценария до запуска.</em></h1>',
    ),
    "telegram-mini-apps/index.html": (
        '<h1>Мини-приложение внутри Telegram. <em>Когда одного бота уже мало.</em></h1>',
        '<h1>Telegram Mini App на заказ. <em>Когда одного бота уже мало.</em></h1>',
    ),
    "guides/telegram-bot-cost/index.html": (
        '<h1>Сколько стоит сделать Telegram-бот на заказ</h1>',
        '<h1>Сколько стоит сделать Telegram-бот на заказ в 2026 году</h1>',
    ),
    "guides/bot-vs-mini-app-vs-web/index.html": (
        '<h1>Бот, Mini App или web: <em>что выбрать</em></h1>',
        '<h1>Telegram-бот, Mini App или веб-приложение: <em>что выбрать</em></h1>',
    ),
    "cases/sheetpilot-ai/index.html": (
        '<h1>SheetPilot <em>AI.</em></h1>',
        '<h1>ИИ-ассистент для Excel — <em>SheetPilot AI.</em></h1>',
    ),
}

changed = []
for rel, (old, new) in H1_REPLACEMENTS.items():
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"stage164: missing page {rel}")
    text = path.read_text(encoding="utf-8")
    if new in text:
        continue
    if old not in text:
        raise SystemExit(f"stage164: expected H1 not found in {rel}")
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    changed.append(rel)

# The generic XML validator can validate the XML/urlset/loc layer of a Google
# News sitemap, but it does not validate Google-specific news:* requirements.
# State that boundary explicitly instead of pretending to be a full News checker.
sitemap = ROOT / "tools" / "sitemap-validator" / "index.html"
text = sitemap.read_text(encoding="utf-8")
news_block = '''<article data-stage164-news-sitemap="true"><h3>Можно проверить Google News sitemap?</h3><p>Да, для базовой XML-проверки: валидатор увидит структуру urlset, элементы loc, абсолютные URL и дубли. Специальные требования Google News к тегам news:publication, news:publication_date и news:title эта версия не валидирует.</p></article>'''
if 'data-stage164-news-sitemap="true"' not in text:
    anchor = '<article><h3>XML отправляется на сервер?</h3>'
    if anchor not in text:
        raise SystemExit("stage164: sitemap FAQ anchor missing")
    text = text.replace(anchor, news_block + anchor, 1)
    changed.append("tools/sitemap-validator/index.html")

# Tune the snippet without claiming unsupported Google News semantic validation.
old_desc = 'Проверить sitemap.xml онлайн: формат XML, URL, структуру sitemap и типичные ошибки. Бесплатный Sitemap Validator работает прямо в браузере.'
new_desc = 'Проверить sitemap.xml онлайн: XML, URL, дубли и структуру urlset/sitemapindex. Подходит для базовой проверки обычного и Google News sitemap прямо в браузере.'
if old_desc in text:
    text = text.replace(old_desc, new_desc)
# Keep OG/Twitter descriptions in sync when they use the same final copy.
text = text.replace('content="' + old_desc + '"', 'content="' + new_desc + '"')
sitemap.write_text(text, encoding="utf-8")

# Guard final H1s and the honest Google News limitation.
guards = {
    "telegram-bots/index.html": "Разработка Telegram-ботов на заказ.",
    "telegram-mini-apps/index.html": "Telegram Mini App на заказ.",
    "guides/telegram-bot-cost/index.html": "в 2026 году</h1>",
    "guides/bot-vs-mini-app-vs-web/index.html": "Telegram-бот, Mini App или веб-приложение:",
    "cases/sheetpilot-ai/index.html": "ИИ-ассистент для Excel",
    "tools/sitemap-validator/index.html": 'data-stage164-news-sitemap="true"',
}
for rel, needle in guards.items():
    data = (ROOT / rel).read_text(encoding="utf-8")
    if needle not in data:
        raise SystemExit(f"stage164: guard failed {rel}: {needle}")

print(f"stage164 demand tuning: {len(changed)} page changes")
subprocess.run(
    [sys.executable, str(Path(__file__).with_name("stage165_search_conversion_bridge.py")), str(ROOT)],
    check=True,
)
