#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def patch(path: str, marker: str, block: str) -> bool:
    target = root / path
    if not target.exists():
        raise SystemExit(f"stage20: missing target {path}")
    html = target.read_text(encoding="utf-8")
    if 'data-stage20-telegram-cluster="true"' in html:
        return False
    if marker not in html:
        raise SystemExit(f"stage20: marker not found in {path}: {marker}")
    html = html.replace(marker, block + marker, 1)
    target.write_text(html, encoding="utf-8")
    return True


telegram_proof = r'''
<section class="section" data-stage20-telegram-cluster="true" id="proof"><div class="container"><div class="section-head"><div class="kicker" data-nosnippet="">05 / Подтверждение</div><h2>Не только обещания. <em>Есть что проверить.</em></h2></div><div class="deliver"><article><h3>Реальный Telegram-кейс</h3><p>«Фин Планер» показывает не демо-экран, а проработанный сценарий: бюджет, расходы, регулярные операции, отчёты, цели и прогноз внутри Telegram.</p><p><a href="/cases/fin-planner/">Открыть кейс «Фин Планер» ↗</a></p></article><article><h3>Публичный профиль</h3><p>Профиль Freelance.ru содержит отзывы заказчиков, выполненные проекты и историю работы исполнителя. Это внешний источник, не принадлежащий сайту Alexuys.</p><p><a href="https://freelance.ru/gglalex" rel="noopener noreferrer" target="_blank">Посмотреть профиль Freelance.ru ↗</a></p></article><article><h3>Понятная оценка объёма</h3><p>До старта можно отдельно определить первый рабочий этап: сценарий, интеграции, хранение данных, оплаты и то, что должно быть готово на выходе.</p><p><a href="/guides/telegram-bot-cost/">От чего зависит стоимость разработки ↗</a></p></article><article><h3>Без готового ТЗ</h3><p>Если есть только идея или пример похожего бота, задачу можно сначала разложить на пользовательские действия и технические зависимости.</p><p><a href="/guides/telegram-bot-brief/">Как описать задачу на Telegram-бота ↗</a></p></article></div></div></section>
'''

related_case = r'''
<section data-stage20-telegram-cluster="true" aria-label="Разработка Telegram-ботов" style="padding:3.5rem 0;border-top:1px solid rgba(255,255,255,.1)"><div class="container"><div style="max-width:58rem"><p style="margin:0 0 .65rem;color:#76818b;font:700 .68rem/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase">Telegram development</p><h2 style="margin:0;font-size:clamp(2rem,4vw,3.6rem);line-height:1;letter-spacing:-.04em">Нужен похожий Telegram-бот?</h2><p style="margin:1rem 0 0;color:#98a2ab;max-width:46rem">Основная страница направления собрана отдельно: варианты сценариев, CRM/API-интеграции, оплаты, Mini Apps, процесс оценки и запуск.</p><p style="margin:1.2rem 0 0"><a href="/telegram-bots/" style="font-weight:800">Разработка Telegram-ботов на заказ →</a></p></div></div></section>
'''

related_guide = r'''
<section data-stage20-telegram-cluster="true" aria-label="Разработка Telegram-бота на заказ" style="padding:3rem 0;border-top:1px solid rgba(255,255,255,.1)"><div class="container"><div style="max-width:56rem"><p style="margin:0 0 .55rem;color:#7c858e;font-size:.76rem;text-transform:uppercase;letter-spacing:.08em">Следующий шаг</p><h2 style="margin:0;font-size:clamp(1.9rem,4vw,3.2rem);line-height:1.05;letter-spacing:-.035em">Разработка Telegram-бота под вашу задачу</h2><p style="margin:1rem 0 0;color:#969fa8">Если формат бота уже подходит, на основной странице собраны реальные возможности, кейс, интеграции и способ быстро описать задачу без готового технического задания.</p><p style="margin:1.15rem 0 0"><a href="/telegram-bots/" style="font-weight:800">Перейти к разработке Telegram-ботов →</a></p></div></div></section>
'''

services_link = r'''
<section data-stage20-telegram-cluster="true" aria-label="Основное направление Telegram" style="padding:2.6rem 0;border-top:1px solid rgba(255,255,255,.1)"><div class="container"><p style="margin:0;color:#89929b;max-width:60rem"><strong style="color:#f2f4f2">Основное направление: <a href="/telegram-bots/">разработка Telegram-ботов на заказ</a>.</strong> Заявки, анкеты, оплаты, подписки, уведомления, CRM/API-интеграции и Mini Apps — с отдельным реальным кейсом и практическими разборами.</p></div></section>
'''

changed = []
if patch("telegram-bots/index.html", '<section class="contact">', telegram_proof):
    changed.append("/telegram-bots/")
if patch("cases/fin-planner/index.html", '<section class="contact">', related_case):
    changed.append("/cases/fin-planner/")
for guide in (
    "guides/telegram-bot-cost/index.html",
    "guides/telegram-bot-brief/index.html",
    "guides/bot-vs-mini-app-vs-web/index.html",
):
    if patch(guide, "</main>", related_guide):
        changed.append("/" + guide.removesuffix("index.html"))
if patch("services/index.html", "</main>", services_link):
    changed.append("/services/")

print("stage20 patched:", ", ".join(changed) if changed else "already applied")
