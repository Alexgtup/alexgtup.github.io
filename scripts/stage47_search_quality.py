#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import html as html_lib
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def page(route: str) -> Path:
    return root / ("index.html" if route == "/" else route.strip("/") + "/index.html")


def update_head(route: str, title: str, desc: str) -> None:
    p = page(route)
    if not p.is_file():
        raise SystemExit(f"stage47: missing route {route}")
    text = p.read_text(encoding="utf-8")
    et = html_lib.escape(title, quote=True)
    ed = html_lib.escape(desc, quote=True)
    text, n = re.subn(r"<title>.*?</title>", f"<title>{et}</title>", text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"stage47: title not found {route}")
    for attr, key, value in (
        ("name", "description", ed),
        ("property", "og:title", et),
        ("property", "og:description", ed),
        ("name", "twitter:title", et),
        ("name", "twitter:description", ed),
    ):
        pat = re.compile(rf'(<meta\s+content=")[^"]*("\s+{attr}="{re.escape(key)}"\s*/?>)', re.I)
        text = pat.sub(lambda m: m.group(1) + value + m.group(2), text, count=1)
    p.write_text(text, encoding="utf-8")


HEADS = {
    "/": (
        "Разработка сайтов, приложений, Telegram-ботов и автоматизации | Alexuys",
        "Разработка сайтов, веб-сервисов, приложений, Telegram-ботов, CRM, API-интеграций и автоматизации. Реальные кейсы, ориентиры стоимости и прямой контакт с разработчиком.",
    ),
    "/telegram-bots/": (
        "Разработка Telegram-ботов на заказ — CRM, API, оплаты | Alexuys",
        "Разработка Telegram-ботов на заказ: заявки, анкеты, CRM/API, оплаты, подписки, базы данных и Mini Apps. Реальный кейс, стоимость и передача исходников.",
    ),
    "/web-development/": (
        "Разработка сайтов и веб-сервисов на заказ | Alexuys",
        "Разработка сайтов, каталогов, личных кабинетов, веб-сервисов и MVP. Реальные кейсы, ориентиры стоимости, адаптив, интеграции и запуск проекта.",
    ),
    "/n8n-automation/": (
        "Автоматизация n8n и Make на заказ — CRM, API, Telegram | Alexuys",
        "Автоматизация процессов в n8n и Make: webhooks, CRM, API, Telegram, таблицы, уведомления и обработка ошибок. Стоимость первого workflow и варианты реализации.",
    ),
    "/project-repair/": (
        "Доработка сайта, Telegram-бота и чужого кода | Alexuys",
        "Доработка существующих сайтов, Telegram-ботов и веб-сервисов: ошибки, чужой код, формы, адаптив, API и интеграции. Можно начать с небольшой задачи.",
    ),
    "/api-integrations/": (
        "API-интеграции на заказ — CRM, платежи, Telegram и сервисы | Alexuys",
        "Разработка API-интеграций между CRM, Telegram, платежами, сайтами и внешними сервисами. Обмен данными, webhooks, авторизация и обработка ошибок.",
    ),
    "/app-development/": (
        "Разработка мобильных приложений на заказ | Alexuys",
        "Разработка мобильных приложений под реальный пользовательский сценарий: iOS/Swift и кроссплатформенные проекты. Кейсы интерфейсов, логики и доработки приложений.",
    ),
    "/services/": (
        "Услуги разработки — сайты, приложения, Telegram, CRM и автоматизация | Alexuys",
        "Выберите задачу: сайт или веб-сервис, приложение, Telegram-бот, CRM, API-интеграция, n8n/Make автоматизация или доработка существующего проекта.",
    ),
}
for route, (title, desc) in HEADS.items():
    update_head(route, title, desc)


RELATED = {
    "/telegram-bots/": (
        "Связанные материалы и доказательства",
        "Перед заказом можно посмотреть реальный Telegram-продукт, ориентиры стоимости и короткий бриф.",
        [
            ("/cases/fin-planner/", "Реальный кейс: Фин Планер", "Telegram-бот с полноценным пользовательским сценарием, регулярными операциями, целями и отчётами."),
            ("/guides/telegram-bot-cost/", "Сколько стоит Telegram-бот", "От чего зависит оценка и почему считать только количество кнопок недостаточно."),
            ("/guides/telegram-bot-brief/", "Что прислать для оценки", "Короткий бриф без большого технического задания."),
        ],
    ),
    "/web-development/": (
        "Связанные кейсы и ориентиры",
        "Не обязательно оценивать веб-разработку по списку технологий — ниже реальные примеры и разбор стоимости.",
        [
            ("/cases/factory-catalog/", "B2B-каталог завода", "Корпоративный каталог продукции, структура данных и заявки."),
            ("/guides/development-cost/", "Из чего складывается стоимость", "Объём логики, интеграции, состояние исходников и требования к запуску."),
            ("/mvp-development/", "Если нужен MVP", "Отдельный путь для продукта, который надо быстро довести до рабочего первого релиза."),
        ],
    ),
    "/n8n-automation/": (
        "Что посмотреть перед автоматизацией",
        "Полезно сначала понять границы workflow и место API — так проще не собрать хрупкую цепочку из случайных шагов.",
        [
            ("/guides/n8n-vs-make/", "n8n или Make", "Когда удобнее low-code сценарий и чем отличаются подходы к автоматизации."),
            ("/api-integrations/", "API-интеграции", "Когда workflow должен надёжно обмениваться данными с CRM и внешними сервисами."),
            ("/telegram-bots/", "Telegram как часть процесса", "Бот может быть интерфейсом для заявок, уведомлений и действий сотрудников."),
        ],
    ),
    "/project-repair/": (
        "Не всегда нужен новый проект",
        "Если рабочая база уже есть, сначала выгоднее понять, можно ли восстановить критичный сценарий без полного переписывания.",
        [
            ("/cases/taxi-app/", "Кейс мобильного проекта", "Пример работы с существующим продуктом и критичным пользовательским сценарием."),
            ("/guides/development-cost/", "Как оценивать доработку", "Почему состояние исходников и неизвестные интеграции влияют на цену сильнее количества экранов."),
            ("/web-development/", "Веб-разработка", "Если после аудита становится понятно, что нужен отдельный новый модуль или сервис."),
        ],
    ),
    "/api-integrations/": (
        "Интеграция должна быть частью процесса",
        "API само по себе не является результатом: важен путь данных от исходного события до конечного действия и обработка сбоев.",
        [
            ("/cases/auto-crm/", "Кейс CRM автосалона", "Рабочий процесс заявок, статусов и данных сотрудников."),
            ("/n8n-automation/", "n8n / Make", "Когда интеграцию разумно оформить как управляемый workflow."),
            ("/backend-development/", "Backend-разработка", "Если между системами нужна отдельная серверная логика, хранение или очереди."),
        ],
    ),
    "/app-development/": (
        "Приложение — это сценарий, а не набор экранов",
        "До оценки полезнее посмотреть похожую продуктовую логику и выбрать платформу, чем начинать с длинного списка функций.",
        [
            ("/cases/swift-calendar/", "iOS-календарь на Swift", "Нативный интерфейс, события, календарная логика и подписка."),
            ("/cases/taxi-app/", "Приложение такси", "Мобильный пользовательский сценарий сервиса поездок."),
            ("/ios-development/", "Нативная iOS-разработка", "Отдельное направление для задач, где нужен Swift и системные возможности iOS."),
        ],
    ),
}


def related_block(title: str, intro: str, cards: list[tuple[str, str, str]]) -> str:
    card_html = "".join(
        f'<a class="s47-link" href="{href}"><strong>{html_lib.escape(name)}</strong><span>{html_lib.escape(desc)}</span><b>Открыть →</b></a>'
        for href, name, desc in cards
    )
    return (
        '<section class="s47-related" data-stage47-related="true" aria-label="Связанные материалы">'
        '<div class="container"><div class="s47-related__head">'
        f'<div><span class="s47-label">ПРОВЕРИТЬ ДО ОБРАЩЕНИЯ</span><h2>{html_lib.escape(title)}</h2></div>'
        f'<p>{html_lib.escape(intro)}</p></div><div class="s47-related__grid">{card_html}</div></div></section>'
    )

for route, (title, intro, cards) in RELATED.items():
    p = page(route)
    if not p.is_file():
        continue
    text = p.read_text(encoding="utf-8")
    if 'data-stage47-related="true"' in text:
        continue
    block = related_block(title, intro, cards)
    markers = (
        '<section class="verified-trust verified-trust--compact"',
        '<section class="contact"',
        '<section class="contact">',
        '</main>',
    )
    marker = next((m for m in markers if m in text), None)
    if marker:
        text = text.replace(marker, block + "\n" + marker, 1)
        p.write_text(text, encoding="utf-8")

css = root / "assets" / "site-enhancements.css"
if not css.is_file():
    raise SystemExit("stage47: site-enhancements.css missing")
ct = css.read_text(encoding="utf-8")
if "/* stage47 search quality */" not in ct:
    ct += r'''

/* stage47 search quality */
.s47-related{padding:clamp(3.8rem,7vw,6rem) 0;border-top:1px solid rgba(255,255,255,.075)}
.s47-related__head{display:grid;grid-template-columns:1fr .72fr;gap:2rem;align-items:end;margin-bottom:1.35rem}.s47-related__head h2{margin:.55rem 0 0;font-size:clamp(2rem,4vw,3.7rem);line-height:.98;letter-spacing:-.045em;max-width:17ch}.s47-related__head p{margin:0;color:#929ba4;max-width:42rem}.s47-label{color:#7f8993;font:800 .62rem/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.085em}.s47-related__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem}.s47-link{display:flex;min-height:12.5rem;flex-direction:column;padding:1.2rem;border:1px solid rgba(255,255,255,.1);border-radius:1.05rem;background:linear-gradient(145deg,#11151b,#0d1015);text-decoration:none;transition:transform .2s ease,border-color .2s ease}.s47-link:hover{transform:translateY(-3px);border-color:rgba(255,255,255,.2)}.s47-link strong{font-size:1.04rem;letter-spacing:-.02em}.s47-link span{margin:.6rem 0 1rem;color:#89939d;font-size:.78rem;line-height:1.55}.s47-link b{margin-top:auto;font-size:.73rem}
@media(max-width:820px){.s47-related__head{grid-template-columns:1fr;gap:.8rem}.s47-related__grid{grid-template-columns:1fr}.s47-link{min-height:0}}
'''
    css.write_text(ct, encoding="utf-8")

print("stage47 search quality: metadata + related proof/crawl links applied")
