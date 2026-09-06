#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
page = root / "cases" / "fin-planner" / "index.html"
if not page.is_file():
    raise SystemExit("stage40: Fin Planner case not found")
html = page.read_text(encoding="utf-8")

marker = '<section class="section"><div class="container"><div class="section-head"><div class="kicker" data-nosnippet="">04 / Что показывает кейс</div>'
proof = '''<section class="section"><div class="container"><div class="section-head"><div class="kicker" data-nosnippet="">04 / Что можно проверить</div><h2>Не обещания. <em>То, что видно в кейсе.</em></h2></div><div class="deliver"><article><h3>Оригинальный интерфейс</h3><p>В галерее опубликован отдельный экран Telegram-бота без презентационной обработки, поэтому можно посмотреть реальную структуру меню и финансовых сценариев.</p></article><article><h3>6 групп функций</h3><p>Доходы и расходы, регулярные траты, баланс и отчёты, финансовый анализ, цели и прогноз — все эти сценарии перечислены и показаны как части одного продукта.</p></article><article><h3>Telegram — основной интерфейс</h3><p>Учёт, аналитика и планирование доступны в одном чате без отдельного приложения для базового пользовательского пути.</p></article><article><h3>Проверяемая связь с услугой</h3><p>Кейс связан с основной страницей разработки Telegram-ботов и показывает, какой уровень продуктовой логики может находиться за обычным интерфейсом мессенджера.</p></article></div></div></section>'''
if '04 / Что можно проверить' not in html:
    if marker not in html:
        raise SystemExit("stage40: insertion marker not found")
    html = html.replace(marker, proof + marker.replace('04 / Что показывает кейс','05 / Что показывает кейс'), 1)
else:
    html = html.replace('04 / Что показывает кейс', '05 / Что показывает кейс', 1)

page.write_text(html, encoding="utf-8")
print("stage40 proof: Fin Planner now separates verifiable evidence from presentation")
