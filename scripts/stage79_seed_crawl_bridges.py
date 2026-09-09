#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
TODAY = "2026-09-09"

# These five pages are confirmed by fresh Google URL Inspection as
# Submitted and indexed. The targets below are already SEARCHABLE in Yandex,
# but Google still reports them as "URL is unknown to Google".
BRIDGES = {
    "telegram-bots": {
        "label": "СВЯЗАННЫЕ СЦЕНАРИИ",
        "title": "Что выбрать дальше для Telegram-проекта",
        "cards": [
            (
                "Telegram Mini App",
                "Когда внутри Telegram нужен полноценный интерфейс: каталог, кабинет, формы и сложные пользовательские сценарии.",
                "/telegram-mini-apps/",
                "Посмотреть Mini Apps →",
            ),
            (
                "MVP продукта",
                "Подходит, если бот — только часть первого релиза и нужно быстро проверить всю ключевую механику продукта.",
                "/mvp-development/",
                "Разработка MVP →",
            ),
            (
                "Доработка существующего бота",
                "Если проект уже запущен, но нужно исправить ошибки, восстановить интеграции или продолжить чужой код.",
                "/telegram-bot-repair/",
                "Доработка Telegram-бота →",
            ),
        ],
    },
    "crm-development": {
        "label": "СВЯЗАННЫЕ СЦЕНАРИИ",
        "title": "Что посмотреть перед разработкой CRM",
        "cards": [
            (
                "Реальный CRM-кейс",
                "CRM для автосалона: заявки, статусы, рабочие роли и автоматизация процесса в одном интерфейсе.",
                "/cases/auto-crm/",
                "Открыть кейс CRM →",
            ),
            (
                "Своя CRM или готовая",
                "Разбор границы между коробочным решением и собственной системой до начала разработки.",
                "/guides/custom-crm-or-ready/",
                "Сравнить варианты →",
            ),
            (
                "API-интеграции",
                "Связка CRM с сайтом, Telegram, платежами, таблицами и внешними сервисами.",
                "/api-integrations/",
                "Интеграции API →",
            ),
        ],
    },
    "n8n-automation": {
        "label": "СВЯЗАННЫЕ СЦЕНАРИИ",
        "title": "Где заканчивается workflow и начинается код",
        "cards": [
            (
                "n8n или backend",
                "Когда workflow уже становится слишком сложным и часть логики лучше вынести в отдельный сервис.",
                "/guides/n8n-vs-backend/",
                "n8n vs backend →",
            ),
            (
                "n8n или Make",
                "Сравнение двух подходов к no-code/low-code автоматизации с учётом поддержки и self-hosted сценариев.",
                "/guides/n8n-vs-make/",
                "n8n vs Make →",
            ),
            (
                "API-интеграции",
                "Если главная задача — надёжно связать несколько систем, webhooks, CRM и внешние API.",
                "/api-integrations/",
                "Интеграции API →",
            ),
        ],
    },
    "python-development": {
        "label": "СВЯЗАННЫЕ СЦЕНАРИИ",
        "title": "Где Python используется в реальном продукте",
        "cards": [
            (
                "Доработка Telegram-бота",
                "Python/aiogram-проект, который нужно продолжить, исправить или восстановить после чужой разработки.",
                "/telegram-bot-repair/",
                "Доработка бота →",
            ),
            (
                "MVP-разработка",
                "Первый законченный релиз сервиса, бота или веб-продукта с минимально необходимой backend-логикой.",
                "/mvp-development/",
                "Разработка MVP →",
            ),
            (
                "Фин Планер",
                "Кейс Telegram-продукта для учёта расходов, регулярных операций, целей и отчётов.",
                "/cases/fin-planner/",
                "Открыть кейс →",
            ),
        ],
    },
    "backend-development": {
        "label": "СВЯЗАННЫЕ СЦЕНАРИИ",
        "title": "Следующие шаги для backend-задачи",
        "cards": [
            (
                "API-интеграции",
                "Когда серверная часть должна связать CRM, Telegram, платежи, таблицы и внешние системы.",
                "/api-integrations/",
                "Интеграции API →",
            ),
            (
                "MVP-разработка",
                "Если backend нужен как часть первого рабочего релиза, который можно проверить на реальном сценарии.",
                "/mvp-development/",
                "Разработка MVP →",
            ),
            (
                "Доработка проекта",
                "Подходит для существующего backend: ошибки, незавершённые API, интеграции, миграции и чужой код.",
                "/project-repair/",
                "Доработка проекта →",
            ),
        ],
    },
}


def card_html(card: tuple[str, str, str, str]) -> str:
    title, body, href, anchor = card
    return (
        '<article class="growth-card">'
        f"<h3>{escape(title)}</h3>"
        f"<p>{escape(body)}</p>"
        f'<a class="growth-link" href="{escape(href, quote=True)}">{escape(anchor)}</a>'
        "</article>"
    )


def build_section(route: str, cfg: dict) -> str:
    sid = f"stage79-{route.replace('/', '-')}"
    cards = "".join(card_html(card) for card in cfg["cards"])
    return (
        f'<section class="growth-section" data-stage79="true" aria-labelledby="{sid}">'
        '<div class="growth-shell">'
        f'<span class="growth-label">{escape(cfg["label"])}</span>'
        f'<h2 id="{sid}">{escape(cfg["title"])}</h2>'
        f'<div class="growth-grid">{cards}</div>'
        "</div></section>"
    )


changed = []
for route, cfg in BRIDGES.items():
    page = ROOT / route / "index.html"
    if not page.is_file():
        raise SystemExit(f"stage79: missing page {page}")

    text = page.read_text(encoding="utf-8")
    marker = 'data-stage79="true"'
    if marker not in text:
        # Keep existing FAQ/contact ending intact. Insert the crawl bridge just
        # before the final FAQ block used across commercial service pages.
        anchor = '<section class="growth-section growth-faq"'
        pos = text.find(anchor)
        if pos < 0:
            raise SystemExit(f"stage79: FAQ insertion anchor not found on /{route}/")
        text = text[:pos] + build_section(route, cfg) + text[pos:]
        page.write_text(text, encoding="utf-8")
        changed.append(route)

    # Hard guard: every intended target must exist in the final page HTML.
    final_text = page.read_text(encoding="utf-8")
    for _, _, href, _ in cfg["cards"]:
        if f'href="{href}"' not in final_text:
            raise SystemExit(f"stage79: missing crawl bridge {href} on /{route}/")

# Update lastmod only for the five seed pages whose HTML changed. Avoid
# reparsing/reformatting the sitemap; patch only the matching <url> blocks.
sitemap = ROOT / "sitemap.xml"
if not sitemap.is_file():
    raise SystemExit("stage79: missing sitemap.xml")
xml = sitemap.read_text(encoding="utf-8")
for route in BRIDGES:
    loc = f"https://alexgtup.github.io/{route}/"
    block_re = re.compile(
        rf"(<url>\s*.*?<loc>{re.escape(loc)}</loc>.*?</url>)",
        flags=re.DOTALL,
    )
    match = block_re.search(xml)
    if not match:
        raise SystemExit(f"stage79: sitemap entry not found for {loc}")
    block = match.group(1)
    if "<lastmod>" in block:
        patched = re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{TODAY}</lastmod>", block, count=1)
    else:
        patched = block.replace(f"<loc>{loc}</loc>", f"<loc>{loc}</loc><lastmod>{TODAY}</lastmod>", 1)
    xml = xml[: match.start(1)] + patched + xml[match.end(1) :]
sitemap.write_text(xml, encoding="utf-8")

print(f"stage79: crawl bridges verified on {len(BRIDGES)} indexed seed pages; changed={len(changed)}")
for route in BRIDGES:
    targets = ", ".join(card[2] for card in BRIDGES[route]["cards"])
    print(f"  /{route}/ -> {targets}")
