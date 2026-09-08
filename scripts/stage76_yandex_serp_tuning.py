#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from html import escape
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
DATE = "2026-09-09"

PAGES = {
    "/": {
        "title": "Разработчик Telegram-ботов, сайтов и автоматизации | Alexuys",
        "description": "Частный разработчик Telegram-ботов, сайтов, CRM и автоматизации на заказ. Python, n8n/Make, API-интеграции, реальные кейсы и прямой контакт.",
        "old_h1_html": "Сайты, приложения, Telegram-боты <em>и автоматизация.</em>",
        "h1_html": "Разработчик <em>Telegram-ботов</em>, сайтов и автоматизации.",
        "h1_text": "Разработчик Telegram-ботов, сайтов и автоматизации.",
        "old_lead": "Разрабатываю цифровые продукты с нуля и подключаюсь к уже существующим проектам. Веб-сервисы, мобильные приложения, боты, CRM, API-интеграции и автоматизация — напрямую с разработчиком, без передачи задачи между менеджерами.",
        "lead": "Разрабатываю Telegram-ботов, сайты и веб-сервисы, CRM, API-интеграции и автоматизацию. Можно прийти с новой задачей или существующим проектом — общение напрямую с разработчиком, без передачи между менеджерами.",
        "must": ["Telegram-ботов", "CRM", "n8n/Make"],
    },
    "/telegram-bots/": {
        "title": "Telegram-бот на заказ — стоимость от 15 000 ₽ | Alexuys",
        "description": "Сколько стоит Telegram-бот на заказ: первый рабочий сценарий от 15 000 ₽. Python и aiogram 3, CRM/API, оплаты, базы данных, исходники и запуск.",
        "old_h1_html": "Разработка Telegram-ботов на заказ. <em>Python, aiogram 3, CRM и API.</em>",
        "h1_html": "Telegram-бот на заказ: <em>разработка от 15 000 ₽.</em>",
        "h1_text": "Telegram-бот на заказ: разработка от 15 000 ₽.",
        "old_lead": "Новый Telegram-бот под рабочий сценарий: заявки, анкеты, база данных, оплаты, CRM/API и уведомления. Код и окружение передаются, а сложность определяется логикой, а не числом кнопок.",
        "lead": "Стоимость первого рабочего сценария — от 15 000 ₽. Разработка на Python и aiogram 3: заявки, анкеты, база данных, оплаты, CRM/API и уведомления. Код и окружение передаются заказчику.",
        "must": ["от 15 000 ₽", "Python", "aiogram 3", "CRM/API"],
    },
    "/telegram-mini-apps/": {
        "title": "Telegram Mini App на заказ — разработка под ключ | Alexuys",
        "description": "Заказать Telegram Mini App: интерфейс внутри Telegram для каталога, кабинета, форм и оплат. Web App API, backend, Bot API, адаптив и запуск.",
        "old_h1_html": "Mini App, когда боту <em>уже тесно внутри сообщений и кнопок.</em>",
        "h1_html": "Telegram Mini App на заказ — <em>интерфейс внутри Telegram.</em>",
        "h1_text": "Telegram Mini App на заказ — интерфейс внутри Telegram.",
        "old_lead": "Веб-интерфейс внутри Telegram для каталогов, кабинетов, сложных форм, выбора и интерактивных сценариев. Bot API остаётся точкой входа, а Mini App даёт полноценный интерфейс там, где он действительно нужен.",
        "lead": "Разработка Telegram Mini App для каталогов, кабинетов, сложных форм, заказов и интерактивных сценариев. Пользователь остаётся внутри Telegram, а Web App связывается с Bot API, backend и рабочими данными.",
        "must": ["Telegram Mini App на заказ", "Bot API", "backend"],
    },
    "/n8n-automation/": {
        "title": "n8n Automation Workflow на заказ — настройка и API | Alexuys",
        "description": "Разработка n8n automation workflow на заказ: webhooks, API, Telegram, CRM, Google Sheets, error handling и self-hosted запуск. От 15 000 ₽ за первый workflow.",
        "old_h1_html": "Настройка n8n и автоматизация на заказ. <em>Workflow, API, Telegram и CRM.</em>",
        "h1_html": "n8n Automation Workflow на заказ. <em>API, Telegram и CRM.</em>",
        "h1_text": "n8n Automation Workflow на заказ. API, Telegram и CRM.",
        "old_lead": "Собираю и дорабатываю workflows в n8n: формы и Telegram, CRM и таблицы, HTTP/API, webhooks, ветки ошибок и уведомления. Можно начать с одного рабочего сценария.",
        "lead": "Разрабатываю и дорабатываю n8n automation workflows: Telegram, CRM, Google Sheets, HTTP/API, webhooks, ветки ошибок и уведомления. Первый законченный workflow — от 15 000 ₽.",
        "must": ["n8n Automation Workflow", "webhooks", "от 15 000 ₽"],
    },
}


def html_path(route: str) -> Path:
    return root / "index.html" if route == "/" else root / route.strip("/") / "index.html"


def replace_once(text: str, old: str, new: str, route: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"stage76: {route} {label} expected once, found {count}")
    return text.replace(old, new, 1)


def set_meta(text: str, *, title: str, description: str, route: str) -> str:
    et = escape(title, quote=False)
    ed = escape(description, quote=True)
    text, n = re.subn(r"<title>.*?</title>", f"<title>{et}</title>", text, count=1, flags=re.I | re.S)
    if n != 1:
        raise SystemExit(f"stage76: title missing: {route}")

    def replace_meta(attr: str, key: str, value: str, src: str) -> str:
        pattern = rf'(<meta\b[^>]*\b{attr}=["\']{re.escape(key)}["\'][^>]*\bcontent=["\'])[^"\']*(["\'][^>]*>)'
        out, count = re.subn(pattern, lambda m: m.group(1) + value + m.group(2), src, count=1, flags=re.I)
        if count == 0:
            pattern2 = rf'(<meta\b[^>]*\bcontent=["\'])[^"\']*(["\'][^>]*\b{attr}=["\']{re.escape(key)}["\'][^>]*>)'
            out, count = re.subn(pattern2, lambda m: m.group(1) + value + m.group(2), src, count=1, flags=re.I)
        return out

    text = replace_meta("name", "description", ed, text)
    text = replace_meta("property", "og:title", escape(title, quote=True), text)
    text = replace_meta("property", "og:description", ed, text)
    text = replace_meta("name", "twitter:title", escape(title, quote=True), text)
    text = replace_meta("name", "twitter:description", ed, text)
    return text


changed = []
for route, cfg in PAGES.items():
    p = html_path(route)
    if not p.is_file():
        raise SystemExit(f"stage76: missing {route}: {p}")
    text = p.read_text(encoding="utf-8")
    text = set_meta(text, title=cfg["title"], description=cfg["description"], route=route)
    text = replace_once(text, cfg["old_h1_html"], cfg["h1_html"], route, "final hero h1")
    text = replace_once(text, cfg["old_lead"], cfg["lead"], route, "final hero lead")
    p.write_text(text, encoding="utf-8")

    final = p.read_text(encoding="utf-8")
    if f"<title>{escape(cfg['title'], quote=False)}</title>" not in final:
        raise SystemExit(f"stage76: title invariant failed: {route}")
    if cfg["h1_html"] not in final or cfg["lead"] not in final:
        raise SystemExit(f"stage76: visible intent invariant failed: {route}")
    for token in cfg["must"]:
        if token not in final:
            raise SystemExit(f"stage76: required token missing {route}: {token}")
    changed.append(route)

# Update lastmod only for the pages whose visible search entry was changed.
sitemap = root / "sitemap.xml"
if not sitemap.is_file():
    raise SystemExit("stage76: sitemap.xml missing")
s = sitemap.read_text(encoding="utf-8")
for route in PAGES:
    url = "https://alexgtup.github.io/" if route == "/" else f"https://alexgtup.github.io{route}"
    pattern = re.compile(rf'(<loc>{re.escape(url)}</loc>\s*<lastmod>)[^<]+(</lastmod>)')
    s, n = pattern.subn(rf'\g<1>{DATE}\g<2>', s, count=1)
    if n != 1:
        raise SystemExit(f"stage76: sitemap lastmod missing: {url}")
sitemap.write_text(s, encoding="utf-8")

print("stage76: Yandex SERP tuning applied to " + ", ".join(changed))
