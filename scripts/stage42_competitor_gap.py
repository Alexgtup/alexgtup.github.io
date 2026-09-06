#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html as html_lib
import json
import re
import subprocess
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
PROFILE = "https://freelance.ru/gglalex"
TELEGRAM = "https://t.me/Alexuys"


def page_path(route: str) -> Path:
    return root / ("index.html" if route == "/" else route.strip("/") + "/index.html")


def load(route: str) -> tuple[Path, str]:
    path = page_path(route)
    if not path.is_file():
        raise SystemExit(f"stage42: missing route {route}: {path}")
    return path, path.read_text(encoding="utf-8")


def save(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def insert_after_hero(text: str, block: str, route: str) -> str:
    if 'data-stage42-market="true"' in text:
        return text
    start = text.find('<section class="hero"')
    if start < 0:
        raise SystemExit(f"stage42: hero not found: {route}")
    end = text.find('</section>', start)
    if end < 0:
        raise SystemExit(f"stage42: hero end not found: {route}")
    end += len('</section>')
    return text[:end] + "\n" + block + text[end:]


def insert_before_trust(text: str, block: str, route: str) -> str:
    marker = '<section class="verified-trust'
    if block and 'data-stage42-packages="true"' not in text:
        pos = text.find(marker)
        if pos < 0:
            raise SystemExit(f"stage42: trust marker not found: {route}")
        text = text[:pos] + block + "\n" + text[pos:]
    return text


def set_description(text: str, description: str) -> str:
    escaped = html_lib.escape(description, quote=True)
    patterns = (
        (r'(<meta\s+content=")[^"]*("\s+name="description"\s*/?>)', r'\1' + escaped + r'\2'),
        (r'(<meta\s+content=")[^"]*("\s+property="og:description"\s*/?>)', r'\1' + escaped + r'\2'),
        (r'(<meta\s+content=")[^"]*("\s+name="twitter:description"\s*/?>)', r'\1' + escaped + r'\2'),
    )
    for pattern, repl in patterns:
        text, _ = re.subn(pattern, repl, text, count=1)
    return text


def update_service_schema(text: str, route: str, low_price: int, description: str) -> str:
    script_re = re.compile(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.S | re.I)
    target_url = "https://alexgtup.github.io" + route
    changed = False

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        raw = match.group(2).strip()
        try:
            data = json.loads(raw)
        except Exception:
            return match.group(0)

        objects = data if isinstance(data, list) else [data]
        touched = False
        for obj in objects:
            if not isinstance(obj, dict):
                continue
            if obj.get("@type") == "Service" and obj.get("url") == target_url:
                obj["description"] = description
                obj["offers"] = {
                    "@type": "Offer",
                    "priceCurrency": "RUB",
                    "price": str(low_price),
                    "url": target_url,
                    "availability": "https://schema.org/InStock",
                    "description": "Стартовая стоимость первого рабочего этапа; точная оценка после согласования объёма."
                }
                touched = True
        if not touched:
            return match.group(0)
        changed = True
        payload = objects if isinstance(data, list) else objects[0]
        return match.group(1) + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + match.group(3)

    text = script_re.sub(repl, text)
    if not changed:
        raise SystemExit(f"stage42: Service schema not found for {route}")
    return text


def decision_block(price: str, result: str, handoff: str, extra: str) -> str:
    return f'''
<section class="market-proof" data-stage42-market="true" aria-label="Условия старта и результат">
  <div class="container market-proof__grid">
    <div class="market-proof__item market-proof__item--price"><span>СТАРТ</span><strong>{price}</strong><p>Ориентир до детальной оценки. Финальная сумма фиксируется после просмотра сценария и интеграций.</p></div>
    <div class="market-proof__item"><span>ПЕРВЫЙ РЕЗУЛЬТАТ</span><strong>{result}</strong><p>Сначала определяется один проверяемый результат, а не бесконечный список абстрактных работ.</p></div>
    <div class="market-proof__item"><span>ПЕРЕДАЧА</span><strong>{handoff}</strong><p>Рабочая реализация и необходимые доступы остаются у заказчика, без искусственной привязки к исполнителю.</p></div>
    <div class="market-proof__item"><span>ПРОВЕРКА</span><strong>20+ отзывов на Freelance.ru</strong><p>{extra} <a href="{PROFILE}" rel="me noopener noreferrer" target="_blank">Проверить профиль ↗</a></p></div>
  </div>
</section>
'''


def packages_block(title: str, intro: str, packages: list[tuple[str, str, str, str]]) -> str:
    cards = []
    for label, price, name, body in packages:
        cards.append(f'''<article class="market-package"><span>{label}</span><strong>{price}</strong><h3>{name}</h3><p>{body}</p></article>''')
    return f'''
<section class="section market-packages" data-stage42-packages="true" aria-label="Ориентиры стоимости">
  <div class="container">
    <div class="section-head"><div class="kicker" data-nosnippet="">Стоимость · ориентиры</div><div><h2>{title}</h2><p class="market-packages__lead">{intro}</p></div></div>
    <div class="market-packages__grid">{''.join(cards)}</div>
    <div class="handoff-grid" aria-label="Что фиксируется перед началом">
      <article><span>01</span><strong>Граница задачи</strong><p>До старта фиксируем, какой сценарий считается готовым и что не входит в первый этап.</p></article>
      <article><span>02</span><strong>Проверка результата</strong><p>После публикации проверяется согласованный пользовательский сценарий, интеграция или workflow.</p></article>
      <article><span>03</span><strong>Передача проекта</strong><p>Исходники, workflow, настройки и нужные доступы передаются в согласованном объёме.</p></article>
      <article><span>04</span><strong>Без большого ТЗ</strong><p>Для первичной оценки достаточно описания задачи, ссылки, скриншота или примера похожей реализации.</p></article>
    </div>
    <div class="market-packages__actions"><a class="button primary" href="{TELEGRAM}" rel="noopener noreferrer" target="_blank">Описать задачу в Telegram ↗</a><a class="button" href="{PROFILE}" rel="me noopener noreferrer" target="_blank">Сначала проверить Freelance.ru ↗</a></div>
  </div>
</section>
'''


configs = {
    "/telegram-bots/": {
        "price": "от 15 000 ₽",
        "result": "Один рабочий сценарий",
        "handoff": "Исходники + доступы",
        "extra": "Отзывы находятся на внешней площадке, а не нарисованы внутри портфолио.",
        "description": "Разработка Telegram-ботов на заказ от 15 000 ₽: заявки, CRM/API, оплаты, подписки и Mini Apps. Исходники и доступы, 20+ отзывов на Freelance.ru.",
        "low": 15000,
        "packages": packages_block(
            "Понятно, <em>за что платите.</em>",
            "Это не фиксированные тарифы на любой проект, а нижние ориентиры для первого законченного этапа. Сложность платежей, ролей, Mini App и внешних API оценивается отдельно.",
            [
                ("START", "от 15 000 ₽", "Первый сценарий", "Заявка, анкета, уведомление, хранение данных или другой один законченный пользовательский путь + запуск."),
                ("INTEGRATION", "от 30 000 ₽", "Бот + CRM / API", "Передача данных, webhooks, статусы, база данных, внешняя система и обработка ошибок в связанном сценарии."),
                ("PRODUCT", "от 60 000 ₽", "Бот как продукт", "Несколько сценариев, платежи или подписки, роли, служебная логика, админ-функции или Telegram Mini App."),
            ],
        ),
    },
    "/n8n-automation/": {
        "price": "от 15 000 ₽",
        "result": "Один работающий workflow",
        "handoff": "Workflow + доступы",
        "extra": "Публичная история работ позволяет проверить исполнителя до обсуждения автоматизации.",
        "description": "Автоматизация n8n/Make от 15 000 ₽: CRM, Telegram, API, таблицы и webhooks. Self-hosted, обработка ошибок, передача workflow и доступов.",
        "low": 15000,
        "packages": packages_block(
            "Автоматизация <em>без тумана в смете.</em>",
            "Первый этап строится вокруг одного измеримого потока данных. Если нужны несколько систем, AI-шаги, очереди или мониторинг, объём расширяется после схемы процесса.",
            [
                ("WORKFLOW", "от 15 000 ₽", "Один процесс", "Webhook или триггер, преобразование данных, действие в целевом сервисе и понятная ветка ошибки."),
                ("CONNECTED", "от 30 000 ₽", "Несколько систем", "CRM, Telegram, таблицы, API или почта в одном связанном процессе с проверками и уведомлениями."),
                ("PRODUCTION", "от 60 000 ₽", "Рабочий контур", "Несколько workflow, self-hosted при необходимости, повторные попытки, журналирование и контроль критичных сбоев."),
            ],
        ),
    },
    "/project-repair/": {
        "price": "от 5 000 ₽",
        "result": "Исправленный сценарий",
        "handoff": "Правки в вашем проекте",
        "extra": "Можно прийти с одной ошибкой, а не заказывать полную переделку сайта или бота.",
        "description": "Доработка сайтов и Telegram-ботов от 5 000 ₽: ошибки, адаптив, формы, API и чужой код. Оценка до старта, 20+ отзывов на Freelance.ru.",
        "low": 5000,
        "packages": "",
    },
    "/web-development/": {
        "price": "от 15 000 ₽",
        "result": "Законченный первый релиз",
        "handoff": "Исходники + деплой",
        "extra": "Вместо обещаний можно открыть реальные кейсы и независимый профиль исполнителя.",
        "description": "Разработка сайтов и веб-сервисов от 15 000 ₽: страницы, каталоги, кабинеты и MVP на React/Next.js. Исходники, API, запуск и передача доступов.",
        "low": 15000,
        "packages": packages_block(
            "Начинаем <em>с законченного этапа.</em>",
            "Не каждый проект требует сразу большого веб-сервиса. Первый релиз можно ограничить одной страницей, каталогом или главным пользовательским сценарием и расширять после проверки.",
            [
                ("PAGE", "от 15 000 ₽", "Страница / небольшой сайт", "Адаптивная реализация, формы и базовые интерактивные элементы; подключение готового API при необходимости."),
                ("SITE", "от 30 000 ₽", "Сайт или каталог", "Несколько страниц, структура контента или продукции, формы, данные и интеграции по согласованному сценарию."),
                ("PRODUCT", "от 60 000 ₽", "Веб-сервис / MVP", "Авторизация, роли, backend, база данных, API и один законченный продуктовый сценарий для первого релиза."),
            ],
        ),
    },
}

changed_routes: list[str] = []
for route, cfg in configs.items():
    path, text = load(route)
    before = text
    text = insert_after_hero(text, decision_block(cfg["price"], cfg["result"], cfg["handoff"], cfg["extra"]), route)
    if cfg["packages"]:
        text = insert_before_trust(text, cfg["packages"], route)
    text = set_description(text, cfg["description"])
    text = update_service_schema(text, route, cfg["low"], cfg["description"])
    if text != before:
        save(path, text)
        changed_routes.append(route)

# Make the same commercial facts explicit for crawlers/AI systems without review markup.
llms = root / "llms.txt"
if not llms.is_file():
    raise SystemExit("stage42: llms.txt missing")
llms_text = llms.read_text(encoding="utf-8")
llms_marker = "## Коммерческие ориентиры и передача результата"
if llms_marker not in llms_text:
    llms_text += f'''\n\n{llms_marker}\n- Доработка существующего сайта или Telegram-бота: ориентир от 5 000 ₽ после просмотра задачи.\n- Разработка Telegram-бота: первый рабочий этап от 15 000 ₽.\n- Автоматизация n8n / Make: первый рабочий workflow от 15 000 ₽.\n- Разработка сайта / первого веб-релиза: ориентир от 15 000 ₽.\n- Итоговые исходники, workflow и необходимые доступы передаются заказчику в согласованном объёме.\n- Для первичной оценки не требуется большое техническое задание: достаточно описания процесса, ссылки, скриншота или примера.\n- Внешняя репутация исполнителя проверяется отдельно: {PROFILE}\n'''
    llms.write_text(llms_text, encoding="utf-8")

# Shared styles for the decision layer and package cards.
css = root / "assets" / "site-enhancements.css"
if not css.is_file():
    raise SystemExit("stage42: site-enhancements.css missing")
css_text = css.read_text(encoding="utf-8")
if "/* stage42 competitor decision layer */" not in css_text:
    css_text += r'''

/* stage42 competitor decision layer */
.market-proof{border-block:1px solid rgba(255,255,255,.085);background:linear-gradient(180deg,rgba(255,255,255,.018),rgba(255,255,255,.006))}.market-proof .container{width:min(100%,86rem);margin-inline:auto;padding-inline:clamp(1.1rem,4vw,4.4rem)}.market-proof__grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));padding-block:.78rem}.market-proof__item{min-width:0;padding:1.05rem 1.15rem;border-left:1px solid rgba(255,255,255,.085)}.market-proof__item:first-child{border-left:0}.market-proof__item>span{display:block;color:#717b85;font:750 .59rem/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em}.market-proof__item>strong{display:block;margin-top:.48rem;color:#f2f4f1;font-size:clamp(1.02rem,1.55vw,1.3rem);letter-spacing:-.028em}.market-proof__item--price>strong{color:#c9ff4a;font-size:clamp(1.35rem,2vw,1.75rem)}.market-proof__item p{margin:.48rem 0 0;color:#7e8791;font-size:.7rem;line-height:1.5}.market-proof__item a{color:#bfc6cd;text-underline-offset:3px}.market-packages__lead{max-width:52rem;color:#929ba4;line-height:1.7}.market-packages__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.72rem}.market-package{display:flex;flex-direction:column;min-height:17rem;padding:1.3rem;border:1px solid rgba(255,255,255,.1);border-radius:1.15rem;background:radial-gradient(circle at 90% 0,rgba(129,149,255,.075),transparent 14rem),linear-gradient(145deg,#11151b,#0c0f13)}.market-package>span{color:#737d87;font:750 .61rem/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em}.market-package>strong{margin-top:.7rem;color:#c9ff4a;font-size:clamp(1.45rem,2.7vw,2.15rem);letter-spacing:-.04em}.market-package h3{margin:auto 0 .5rem;font-size:1.14rem;letter-spacing:-.025em}.market-package p{margin:0;color:#8f98a2;font-size:.8rem;line-height:1.62}.handoff-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.6rem;margin-top:.75rem}.handoff-grid article{padding:1rem;border:1px solid rgba(255,255,255,.075);border-radius:.9rem;background:rgba(255,255,255,.014)}.handoff-grid span{color:#6f7882;font:750 .58rem/1 ui-monospace,SFMono-Regular,Menlo,monospace}.handoff-grid strong{display:block;margin:.65rem 0 .35rem;font-size:.85rem}.handoff-grid p{margin:0;color:#7f8992;font-size:.7rem;line-height:1.52}.market-packages__actions{display:flex;flex-wrap:wrap;gap:.62rem;margin-top:1rem}
@media(max-width:900px){.market-proof__grid{grid-template-columns:repeat(2,minmax(0,1fr))}.market-proof__item:nth-child(3){border-left:0;border-top:1px solid rgba(255,255,255,.085)}.market-proof__item:nth-child(4){border-top:1px solid rgba(255,255,255,.085)}.market-packages__grid{grid-template-columns:1fr}.market-package{min-height:13rem}.handoff-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){.market-proof__grid{grid-template-columns:1fr;padding-block:.4rem}.market-proof__item,.market-proof__item:nth-child(3),.market-proof__item:nth-child(4){border-left:0;border-top:1px solid rgba(255,255,255,.085);padding-inline:0}.market-proof__item:first-child{border-top:0}.handoff-grid{grid-template-columns:1fr}.market-packages__actions{display:grid}.market-packages__actions .button{width:100%}}
'''
    css.write_text(css_text, encoding="utf-8")

# Stage 42 mutates the shared stylesheet after Stage 40, so fingerprint again using
# the final bytes that will actually be published.
fingerprint = Path(__file__).with_name("stage41_asset_fingerprints.py")
if not fingerprint.is_file():
    raise SystemExit("stage42: stage41_asset_fingerprints.py missing")
subprocess.check_call([sys.executable, str(fingerprint), str(root)])

print("stage42 competitor gap patched:", ", ".join(changed_routes) if changed_routes else "already applied")
