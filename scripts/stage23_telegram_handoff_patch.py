#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
path = root / "telegram-bots/index.html"
if not path.exists():
    raise SystemExit("stage23: missing telegram-bots/index.html")

html = path.read_text(encoding="utf-8")
if 'data-stage23-handoff="true"' in html:
    print("stage23 patched: already applied")
    raise SystemExit(0)

marker = '<section class="section" data-stage20-telegram-cluster="true" id="proof">'
if marker not in html:
    raise SystemExit("stage23: Stage 20 proof marker not found")

block = r'''
<section class="section" data-stage23-handoff="true" id="handoff"><div class="container"><div class="section-head"><div class="kicker" data-nosnippet="">05 / На выходе</div><h2>Проект остаётся <em>у заказчика.</em></h2></div><div class="deliver"><article><h3>Исходный код</h3><p>Передаю исходники проекта, чтобы бот не был привязан к закрытому конструктору или одному исполнителю и его можно было развивать дальше.</p></article><article><h3>Рабочий запуск</h3><p>Бот разворачивается в согласованном окружении. Для серверного проекта отдельно проверяются запуск, переменные окружения и базовая работа после перезапуска.</p></article><article><h3>Доступы и интеграции</h3><p>Фиксируется, какие внешние сервисы использует проект: Telegram, CRM, база данных, платежи, API и другие зависимости конкретной задачи.</p></article><article><h3>Короткая инструкция</h3><p>Передаю необходимую информацию для эксплуатации: где находятся настройки, как устроен запуск и что потребуется для дальнейшей доработки.</p></article></div><p class="real-note" data-nosnippet="">Точный состав передачи зависит от проекта и согласуется до разработки: простой бот и продукт с backend, платежами и Mini App требуют разного набора инфраструктуры.</p></div></section>
'''

html = html.replace(marker, block + marker, 1)
path.write_text(html, encoding="utf-8")
print("stage23 patched: /telegram-bots/")
