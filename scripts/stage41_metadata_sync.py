#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def page(route: str):
    p = root / ("index.html" if route == "/" else route.strip("/") + "/index.html")
    if not p.is_file():
        raise SystemExit(f"stage41: missing {route}")
    return p, p.read_text(encoding="utf-8")


def sync(text: str, old_title: str, new_title: str, old_desc: str, new_desc: str):
    text = text.replace(old_title, new_title)
    text = text.replace(old_desc, new_desc)
    return text

# Homepage metadata follows the new commercial focus established in Stage 39.
p, html = page("/")
html = sync(
    html,
    "Разработка Telegram-ботов, CRM и автоматизации | Alexuys",
    "Telegram-боты, автоматизация и доработка проектов | Alexuys",
    "Разработка Telegram-ботов, CRM, автоматизации, API-интеграций и веб-сервисов под реальные рабочие процессы. Кейсы, услуги и прямой контакт.",
    "Разработка и доработка Telegram-ботов, автоматизации и интеграций. Существующие проекты, n8n/Make, API, исправление ошибок, реальные кейсы и прямой контакт."
)
p.write_text(html, encoding="utf-8")

# Project repair social/snippet metadata must match the strengthened landing page too.
p, html = page("/project-repair/")
html = sync(
    html,
    "Доработка сайта и чужого проекта — исправление ошибок | Alexuys",
    "Доработка сайтов и Telegram-ботов — исправление ошибок | Alexuys",
    "Доработка сайта, Telegram-бота или веб-сервиса: аудит кода, исправление ошибок, интеграций и логики, завершение проекта и подготовка к релизу.",
    "Доработка сайтов, Telegram-ботов и существующих проектов: исправление ошибок, API и интеграций, чужой код, адаптив, завершение и подготовка к релизу."
)
p.write_text(html, encoding="utf-8")

print("stage41 metadata: homepage and project-repair snippets synchronized with commercial positioning")
