#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def route_file(route: str) -> Path:
    return ROOT / route.strip("/") / "index.html"


def replace_all(route: str, replacements: dict[str, str]) -> int:
    path = route_file(route)
    if not path.is_file():
        raise SystemExit(f"stage126: missing {route}")
    text = path.read_text(encoding="utf-8")
    changed = 0
    for old, new in replacements.items():
        if old not in text:
            raise SystemExit(f"stage126: fragment missing on {route}: {old[:80]}")
        text = text.replace(old, new, 1)
        changed += 1
    path.write_text(text, encoding="utf-8")
    return changed

changed = 0
changed += replace_all('/freelance-developer/', {
    'Можно начать <em>с конкретного законченного результата.</em>': 'Можно начать <em>с одной понятной задачи.</em>',
    'Это не фиксированная цена на любой проект, а понятная граница первого этапа. Если задача шире, объём согласуется до расширения работ.': 'Ниже — ориентиры первого этапа. Если задача шире, сначала согласуем, что именно должно заработать и сколько это будет стоить.',
    'Одна ограниченная задача или связанный блок правок в существующем сайте, backend или приложении.': 'Исправить конкретную проблему в существующем сайте, боте или приложении.',
    'Первый рабочий сценарий: заявки, данные, CRM/API, уведомления или оплаты.': 'Бот для заявок, уведомлений, оплат или другой одной понятной задачи.',
    'n8n / Make →': 'Автоматизация рутины →',
    'Один законченный workflow с webhook, CRM, Telegram, таблицами или внешним API.': 'Один повторяющийся процесс, который сейчас приходится выполнять вручную.',
    'API / CRM интеграция →': 'Связать сервисы →',
    'Связка существующих систем через REST API и webhooks с проверкой данных и результата.': 'Например, связать сайт, CRM, платежи, Telegram или таблицы между собой.',
    'Технический SEO-аудит →': 'Проверить сайт →',
    'Индексация, robots/sitemap, canonical, технические дубли, внутренние ссылки и план исправлений.': 'Найти технические проблемы, которые мешают поиску видеть страницы, и получить план исправлений.',
})

changed += replace_all('/backend-development/', {
    'Связанные сценарии для backend-задачи': 'Что ещё может пригодиться для проекта',
    'n8n или backend': 'Автоматизация или отдельный сервис',
})

changed += replace_all('/n8n-automation/', {
    'Полезно проверить перед сборкой workflow': 'Что полезно проверить перед автоматизацией',
    'n8n или backend': 'Автоматизация или отдельный сервис',
})

changed += replace_all('/telegram-bot-repair/', {
    'Telegram — не отдельная кнопка. <em>Есть backend, данные и интеграции.</em>': 'Бот может быть связан <em>с данными, оплатами и другими сервисами.</em>',
    'CRM, API и оплаты': 'Данные, оплаты и другие сервисы',
})

print(f"stage126 microcopy cleanup: changes={changed}; pages=4")
