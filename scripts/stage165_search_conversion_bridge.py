#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = 'data-stage165-intent-bridge="true"'

PAGES = {
    "telegram-bots/index.html": {
        "eyebrow": "ПО ЗАПРОСУ / TELEGRAM",
        "title": "Сначала понять формат, потом считать разработку.",
        "copy": "Если задача уже понятна, ниже можно быстро сравнить стоимость, Mini App и рабочий Telegram-кейс. Если проект уже существует — отдельно есть путь для доработки чужого кода.",
        "links": [
            ("/guides/telegram-bot-cost/", "Сколько стоит Telegram-бот", "оценка по сценарию, интеграциям и объёму логики"),
            ("/telegram-mini-apps/", "Telegram Mini App на заказ", "когда внутри Telegram нужен полноценный интерфейс"),
            ("/cases/fin-planner/", "Кейс: Fin Planner", "Telegram-продукт с данными, отчётами и backend-логикой"),
            ("/telegram-bot-repair/", "Доработка существующего бота", "ошибки, интеграции, новые функции и чужой код"),
        ],
    },
    "telegram-mini-apps/index.html": {
        "eyebrow": "ПО ЗАПРОСУ / MINI APP",
        "title": "Mini App нужен не всегда — сравните соседние форматы.",
        "copy": "Если сценарий укладывается в команды и уведомления, обычный бот может быть проще. Если нужен самостоятельный продукт вне Telegram — полезнее смотреть в сторону веб-приложения.",
        "links": [
            ("/guides/bot-vs-mini-app-vs-web/", "Бот, Mini App или web", "сравнение форматов по интерфейсу и логике"),
            ("/telegram-bots/", "Разработка Telegram-ботов", "для диалоговых сценариев, заявок и автоматизации"),
            ("/web-development/", "Веб-сервис на заказ", "если продукт должен жить независимо от Telegram"),
            ("/mvp-development/", "MVP продукта", "запуск одного законченного пользовательского пути"),
        ],
    },
    "web-development/index.html": {
        "eyebrow": "ПО ЗАПРОСУ / WEB",
        "title": "Проверить уровень лучше по работающим продуктам.",
        "copy": "Вместо абстрактного списка технологий — несколько проектов с разной логикой: B2B-каталог, Excel-сервис и SEO-панель. У каждого есть отдельный разбор реализации.",
        "links": [
            ("/cases/factory-catalog/", "B2B-каталог производства", "структура каталога, выбор продукции и заявка"),
            ("/cases/sheetpilot-ai/", "SheetPilot AI", "веб-сервис обработки Excel с Python-логикой"),
            ("/cases/seo-control-center/", "SEO Control Center", "панель мониторинга поисковых данных"),
            ("/demos/", "Рабочие демо", "продукты, которые можно открыть и проверить"),
        ],
    },
    "backend-development/index.html": {
        "eyebrow": "ПО ЗАПРОСУ / BACKEND",
        "title": "Backend проще оценивать по потоку данных, а не по стеку.",
        "copy": "API, базы, webhooks и фоновые процессы полезнее смотреть в контексте законченного продукта. Ниже — связанные направления и кейсы, где серверная логика является частью пользовательского сценария.",
        "links": [
            ("/api-integrations/", "API-интеграции", "контракты, webhooks, синхронизация и обработка ошибок"),
            ("/cases/fin-planner/", "Fin Planner", "Telegram-интерфейс поверх данных и серверной логики"),
            ("/cases/sheetpilot-ai/", "SheetPilot AI", "обработка файлов, preview и серверный pipeline"),
            ("/project-repair/", "Доработка существующего backend", "если систему нужно продолжить, а не переписывать"),
        ],
    },
    "project-repair/index.html": {
        "eyebrow": "ПО ЗАПРОСУ / REPAIR",
        "title": "Существующий проект — отдельный тип задачи.",
        "copy": "Для доработки важнее быстро локализовать причину, сохранить рабочую часть и менять только нужный участок. Поэтому рядом вынесены отдельные сценарии для Telegram, WordPress и веб-проектов.",
        "links": [
            ("/telegram-bot-repair/", "Доработка Telegram-бота", "Python, aiogram, интеграции и чужой код"),
            ("/wordpress-development/", "Доработка WordPress", "правки темы, логики, форм и существующего сайта"),
            ("/web-development/", "Веб-разработка", "когда доработка перерастает в новый модуль или сервис"),
            ("/guides/repair-vs-rewrite/", "Дорабатывать или переписывать", "как решить это до начала разработки"),
        ],
    },
    "tools/sitemap-validator/index.html": {
        "eyebrow": "SEO / NEXT STEP",
        "title": "Проверка sitemap — только один слой технического SEO.",
        "copy": "Если проблема не в XML, следующий шаг — проверить доступность страниц, robots, canonical, внутренние ссылки и фактическое появление URL в поиске.",
        "links": [
            ("/cases/seo-control-center/", "SEO Control Center", "мониторинг показов, CTR, позиций и состояния URL"),
            ("/cases/siteaudit-studio/", "SiteAudit Studio", "технический crawl и базовая диагностика сайта"),
            ("/tools/robots-validator/", "Robots.txt Validator", "проверка правил для поисковых роботов"),
            ("/web-development/", "Техническая доработка сайта", "если проблема требует изменения самого проекта"),
        ],
    },
    "cases/sheetpilot-ai/index.html": {
        "eyebrow": "CASE / NEXT STEP",
        "title": "От кейса — к рабочему сценарию.",
        "copy": "SheetPilot показывает один вариант продукта вокруг файлов и серверной обработки. Рядом — публичные демо, веб-разработка и Python-направление для похожих задач.",
        "links": [
            ("/demos/", "Открыть рабочие демо", "проверить продуктовые сценарии в браузере"),
            ("/web-development/", "Разработка веб-сервиса", "интерфейс, backend и данные как единый продукт"),
            ("/python-development/", "Python-разработка", "обработка данных, API и прикладная автоматизация"),
        ],
    },
    "cases/seo-control-center/index.html": {
        "eyebrow": "CASE / SEO PRODUCT",
        "title": "SEO Control Center — не отдельный лендинг, а часть SEO-стека.",
        "copy": "Для похожей системы обычно нужны сбор данных, планировщик, хранение истории и интерфейс, который показывает изменения, а не просто сырые цифры.",
        "links": [
            ("/demos/", "Рабочие демо", "посмотреть продуктовые сценарии вживую"),
            ("/n8n-automation/", "n8n и автоматизация", "регулярный сбор данных и workflow между сервисами"),
            ("/tools/sitemap-validator/", "Sitemap Validator", "проверка одного из технических входов SEO"),
            ("/web-development/", "Разработка веб-сервисов", "интерфейс, API и данные для собственного продукта"),
        ],
    },
    "demos/index.html": {
        "eyebrow": "LIVE / ПРОВЕРКА",
        "title": "Демо полезно проверять как продукт, а не как скриншот.",
        "copy": "Откройте сервис, выполните основной сценарий и затем посмотрите связанный кейс. Так видно и интерфейс, и реальную логику за ним. Если нужен похожий продукт, можно сразу перейти к соответствующему направлению разработки.",
        "links": [
            ("/cases/sheetpilot-ai/", "SheetPilot AI — кейс", "Excel, обработка данных и серверная логика"),
            ("/cases/seo-control-center/", "SEO Control Center — кейс", "поисковые данные, мониторинг и автоматизация"),
            ("/cases/siteaudit-studio/", "SiteAudit Studio — кейс", "crawl, HTTP, robots, sitemap и indexability"),
            ("/web-development/", "Заказать похожий веб-сервис", "от одного рабочего сценария до полноценного продукта"),
        ],
    },
}

STYLE = '''<style data-stage165-intent-style="true">
.s165-bridge{width:min(1480px,calc(100% - 64px));margin:0 auto clamp(72px,8vw,124px);padding:clamp(34px,4vw,56px) 0 0;border-top:1px solid rgba(255,255,255,.10);color:inherit}
.s165-bridge__grid{display:grid;grid-template-columns:minmax(0,.82fr) minmax(0,1.18fr);gap:clamp(36px,5vw,86px);align-items:start}
.s165-bridge__eyebrow{margin:0 0 14px;font:700 11px/1.3 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.16em;text-transform:uppercase;opacity:.52}
.s165-bridge h2{max-width:15ch;margin:0;font-size:clamp(34px,3.8vw,60px);line-height:.98;letter-spacing:-.05em;color:inherit}
.s165-bridge__copy{max-width:58ch;margin:20px 0 0;font-size:clamp(16px,1.15vw,19px);line-height:1.65;opacity:.68}
.s165-bridge__links{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid rgba(255,255,255,.08)}
.s165-bridge__link{display:block;min-width:0;padding:20px 18px 22px 0;border-bottom:1px solid rgba(255,255,255,.08);color:inherit;text-decoration:none}
.s165-bridge__link:nth-child(odd){padding-right:28px}.s165-bridge__link:nth-child(even){padding-left:28px;border-left:1px solid rgba(255,255,255,.08)}
.s165-bridge__link strong{display:block;font-size:16px;line-height:1.3;letter-spacing:-.015em}.s165-bridge__link span{display:block;margin-top:7px;font-size:13px;line-height:1.45;opacity:.56}
.s165-bridge__link:hover strong{text-decoration:underline;text-underline-offset:4px}
.s165-bridge__contact{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;gap:20px;padding-top:22px;font-size:14px;opacity:.82}
.s165-bridge__contact a{color:inherit;font-weight:800;text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:3px}
@media(max-width:900px){.s165-bridge{width:min(100% - 28px,860px)}.s165-bridge__grid{grid-template-columns:1fr;gap:30px}.s165-bridge h2{max-width:20ch}.s165-bridge__links{grid-template-columns:1fr}.s165-bridge__link:nth-child(n){padding:18px 0;border-left:0}.s165-bridge__contact{align-items:flex-start;flex-direction:column}}
@media(max-width:600px){.s165-bridge{width:calc(100% - 24px);margin-bottom:72px}.s165-bridge h2{font-size:clamp(32px,10vw,46px)}}
</style>'''


def render_block(cfg: dict) -> str:
    links = []
    for href, title, desc in cfg["links"]:
        links.append(
            f'<a class="s165-bridge__link" href="{html.escape(href, quote=True)}">'
            f'<strong>{html.escape(title)}</strong><span>{html.escape(desc)}</span></a>'
        )
    return (
        f'<section class="s165-bridge" {MARKER} aria-label="Связанные страницы">'
        '<div class="s165-bridge__grid"><div class="s165-bridge__intro">'
        f'<p class="s165-bridge__eyebrow">{html.escape(cfg["eyebrow"])}</p>'
        f'<h2>{html.escape(cfg["title"])}</h2>'
        f'<p class="s165-bridge__copy">{html.escape(cfg["copy"])}</p></div>'
        f'<div class="s165-bridge__links">{"".join(links)}'
        '<div class="s165-bridge__contact"><span>Есть конкретная задача — можно сразу прислать вводные.</span>'
        '<a href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Telegram @Alexuys ↗</a></div>'
        '</div></div></section>'
    )


changed = 0
for rel, cfg in PAGES.items():
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"stage165: missing page {rel}")
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        continue
    if "</main>" not in text or "</head>" not in text:
        raise SystemExit(f"stage165: required shell missing {rel}")
    text = text.replace("</head>", STYLE + "</head>", 1)
    head, tail = text.rsplit("</main>", 1)
    text = head + render_block(cfg) + "</main>" + tail
    path.write_text(text, encoding="utf-8")
    changed += 1

for rel, cfg in PAGES.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    if text.count(MARKER) != 1:
        raise SystemExit(f"stage165: bridge guard failed {rel}")
    for href, _, _ in cfg["links"]:
        if f'href="{href}"' not in text:
            raise SystemExit(f"stage165: link guard failed {rel} -> {href}")
    if 'href="https://t.me/Alexuys"' not in text:
        raise SystemExit(f"stage165: contact guard failed {rel}")

print(f"stage165 search-to-proof bridges: {changed} priority pages")
