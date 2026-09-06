#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote
import html as H
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def route_file(route: str) -> Path:
    return root / route.strip("/") / "index.html"


def set_head(route: str, title: str, desc: str) -> None:
    p = route_file(route)
    text = p.read_text(encoding="utf-8")
    et, ed = H.escape(title, quote=True), H.escape(desc, quote=True)
    text = re.sub(r"<title>.*?</title>", f"<title>{et}</title>", text, count=1, flags=re.S | re.I)
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


def replace_main(route: str, main_html: str) -> None:
    p = route_file(route)
    if not p.is_file():
        raise SystemExit(f"stage51: missing {route}")
    text = p.read_text(encoding="utf-8")
    text, n = re.subn(
        r'<main\b[^>]*id="main-content"[^>]*>.*?</main>',
        lambda _m: main_html,
        text,
        count=1,
        flags=re.S | re.I,
    )
    if n != 1:
        raise SystemExit(f"stage51: main replace failed {route}")
    p.write_text(text, encoding="utf-8")


CASES = {
    "/cases/auto-crm/": {
        "kind": "crm",
        "kicker": "CRM · WORKFLOW · WEBHOOKS",
        "title": "CRM автосалона: <em>заявка не теряется между статусами.</em>",
        "lead": "Кейс внутренней CRM, где важен не отдельный экран, а связный рабочий контур: входящая заявка, текущий статус, работа менеджера, webhooks и дальнейшие автоматические действия.",
        "meta_title": "CRM для автосалона — заявки, статусы и автоматизация | Кейс Alexuys",
        "meta_desc": "Кейс CRM для автосалона: единый учёт заявок, статусы менеджеров, webhooks и автоматизация рабочего процесса. Схема решения и реализованный контур.",
        "proof": [("CRM", "единый рабочий контур"), ("Webhooks", "связь событий и действий"), ("Statuses", "видимое состояние заявки")],
        "problem_title": "Не ещё одна таблица заявок. <em>Нужен был управляемый процесс.</em>",
        "problem": "Когда заявка проходит через несколько действий и сотрудников, простого списка недостаточно. Система должна хранить текущее состояние и давать понятный следующий шаг, а события — уходить дальше без ручного копирования.",
        "steps": [
            ("01", "Входящая заявка", "Заявка попадает в единый рабочий контур вместо разрозненных каналов."),
            ("02", "Статус работы", "Текущее состояние видно в CRM и используется как часть дальнейшей логики."),
            ("03", "Действие менеджера", "Работа сотрудника меняет состояние заявки, а не остаётся отдельной заметкой."),
            ("04", "Webhook / автоматизация", "Событие можно передать во внешний сценарий и продолжить процесс автоматически."),
        ],
        "implemented": [
            ("Единый учёт заявок", "Один рабочий контур вместо нескольких независимых списков."),
            ("Статусы", "Состояние заявки становится частью процесса и понятно следующему участнику."),
            ("Webhooks", "События CRM можно передавать во внешние интеграции и автоматизацию."),
            ("Рабочая логика", "Интерфейс связан с действиями менеджеров, а не существует отдельно от процесса."),
        ],
        "scope": "На странице не придумываются проценты роста продаж, скорость обработки или экономия времени: таких публично подтверждённых цифр по проекту нет. Кейс показывает именно тип реализованной системы и рабочую логику.",
        "related": [("/crm-development/", "Разработка CRM"), ("/api-integrations/", "API-интеграции"), ("/n8n-automation/", "Автоматизация n8n / Make")],
        "cta": "Нужен похожий внутренний процесс?",
        "cta_text": "Можно прислать текущую схему заявок, таблицу, CRM или просто описать, где именно теряется следующий шаг.",
    },
    "/cases/factory-catalog/": {
        "kind": "catalog",
        "kicker": "B2B · CATALOG · 1C · REQUESTS",
        "title": "Каталог завода: <em>от структуры продукции до заявки.</em>",
        "lead": "B2B-кейс, где сайт должен не просто показать ассортимент. Продукция получает понятную структуру, пользователь доходит до нужной позиции и формирует заявку, а данные передаются во внутренний учёт и 1С.",
        "meta_title": "B2B-каталог завода с заявками и интеграцией 1С | Кейс Alexuys",
        "meta_desc": "Кейс B2B-каталога завода: структура продукции, путь до заявки и интеграция с внутренним учётом и 1С. Схема решения без выдуманных результатов.",
        "proof": [("B2B", "каталог технической продукции"), ("1C", "интеграция с внутренним учётом"), ("Request", "путь пользователя до заявки")],
        "problem_title": "Каталог должен помогать выбрать. <em>Не быть складом карточек.</em>",
        "problem": "Для производственного сайта важна структура: пользователь должен понять, где находится нужная продукция и что делать дальше. Отдельная задача — передать сформированную заявку во внутренний рабочий контур, а не оставить её изолированной в форме сайта.",
        "steps": [
            ("01", "Структура продукции", "Ассортимент организован как каталог, а не как длинный несвязанный список."),
            ("02", "Выбор позиции", "Пользователь доходит до нужного продукта через понятную информационную структуру."),
            ("03", "Заявка", "Выбранный контекст превращается в запрос клиента, который можно дальше обрабатывать."),
            ("04", "Внутренний учёт / 1С", "Данные не заканчиваются на сайте и передаются в связанный внутренний процесс."),
        ],
        "implemented": [
            ("Каталог продукции", "Структурированное представление ассортимента вместо набора разрозненных страниц."),
            ("Путь до заявки", "Коммерческое действие связано с выбранной продукцией и контекстом пользователя."),
            ("Интеграционный слой", "Сайт связан с внутренним учётом и 1С как частью общего процесса."),
            ("B2B-логика", "Приоритет — техническая структура, выбор и заявка, а не декоративная витрина."),
        ],
        "scope": "В репозитории нет публичных скриншотов этого проекта, поэтому визуал ниже — не выдаваемый за оригинальный интерфейс скриншот, а схема структуры кейса. Не добавляются неподтверждённые цифры по конверсии или объёму заявок.",
        "related": [("/web-development/", "Разработка сайтов и веб-сервисов"), ("/api-integrations/", "API-интеграции"), ("/crm-development/", "CRM и внутренние системы")],
        "cta": "Нужен каталог, который заканчивается заявкой, а не карточкой?",
        "cta_text": "Можно прислать текущий каталог, Excel/1С-структуру или пример продукции — сначала разберём путь пользователя и данных.",
    },
    "/cases/taxi-app/": {
        "kind": "taxi",
        "kicker": "MOBILE · EXISTING PRODUCT · RELEASE",
        "title": "Приложение такси: <em>доработать критичный путь без переписывания продукта.</em>",
        "lead": "Кейс работы с существующим мобильным приложением: авторизация, поездки, уведомления, взаимодействие с API и подготовка стабильной релизной сборки. Здесь ценность — сохранить уже работающий продукт и довести критичный сценарий до релиза.",
        "meta_title": "Доработка приложения такси и подготовка релиза | Кейс Alexuys",
        "meta_desc": "Кейс доработки приложения такси: авторизация, поездки, уведомления, API и подготовка релизной сборки. Работа с существующим мобильным продуктом.",
        "proof": [("Existing app", "работа с готовым продуктом"), ("API", "состояния поездки и данные"), ("Release", "подготовка сборки к выпуску")],
        "problem_title": "Существующий продукт — это ограничение. <em>И одновременно актив.</em>",
        "problem": "При доработке мобильного приложения нельзя рассматривать нужную функцию отдельно от уже работающего пути пользователя. Изменения в авторизации, поездке, API или уведомлениях должны сохранять связанные состояния и не ломать релизный контур.",
        "steps": [
            ("01", "Авторизация", "Пользователь должен стабильно войти в приложение до перехода к основному сценарию."),
            ("02", "Поездка", "Ключевой пользовательский путь связан с текущим состоянием заказа и действиями клиента."),
            ("03", "API и уведомления", "Интерфейс зависит от серверных данных и изменений состояния, которые приходят извне."),
            ("04", "Релизная сборка", "Изменения доводятся до состояния, пригодного для выпуска, а не остаются локальной правкой."),
        ],
        "implemented": [
            ("Авторизация", "Работа с входом пользователя как обязательной частью основного мобильного сценария."),
            ("Сценарий поездки", "Связанные состояния и действия внутри существующего приложения."),
            ("API / уведомления", "Взаимодействие клиентского интерфейса с внешними данными и событиями."),
            ("Подготовка релиза", "Фокус не только на коде функции, но и на доведении сборки до выпуска."),
        ],
        "scope": "Кейс не приписывает проекту метрики роста, количество поездок или финансовые результаты. Он показывает опыт доработки существующего мобильного продукта, где важны совместимость изменений и целостность пользовательского пути.",
        "related": [("/project-repair/", "Доработка существующего проекта"), ("/app-development/", "Разработка приложений"), ("/api-integrations/", "API-интеграции")],
        "cta": "Есть приложение, которое нужно довести до рабочего релиза?",
        "cta_text": "Пришлите исходники, текущую сборку или список проблем. Первый этап можно ограничить одним критичным пользовательским сценарием.",
    },
}


def visual(kind: str) -> str:
    if kind == "crm":
        return '''<div class="s51-visual s51-crm" aria-label="Схема рабочего контура CRM"><div class="s51-visual-label">СХЕМА РАБОЧЕГО КОНТУРА · НЕ СКРИНШОТ</div><div class="s51-window"><div class="s51-windowbar"><b>Auto CRM</b><span>requests / workflow</span><i>live state</i></div><div class="s51-kpis"><div><small>Вход</small><strong>Заявка</strong></div><div><small>Состояние</small><strong>Статус</strong></div><div><small>Ответственный</small><strong>Менеджер</strong></div></div><div class="s51-flow"><span>Новая заявка</span><b>→</b><span>В работе</span><b>→</b><span>Следующее действие</span></div><div class="s51-event"><small>EVENT</small><strong>status.changed</strong><span>Webhook → внешний сценарий / автоматизация</span></div></div></div>'''
    if kind == "catalog":
        return '''<div class="s51-visual s51-catalog" aria-label="Схема структуры B2B-каталога"><div class="s51-visual-label">СХЕМА СТРУКТУРЫ · НЕ СКРИНШОТ</div><div class="s51-catalog-shell"><aside><b>Продукция</b><span>Категория A</span><span>Категория B</span><span>Категория C</span><span>Технические данные</span></aside><div class="s51-catalog-main"><small>B2B CATALOG</small><h3>Выбор продукции</h3><div class="s51-products"><div><i>01</i><strong>Позиция</strong><small>характеристики</small></div><div><i>02</i><strong>Позиция</strong><small>характеристики</small></div><div><i>03</i><strong>Позиция</strong><small>характеристики</small></div></div><div class="s51-request"><small>REQUEST FLOW</small><strong>Выбранная продукция → заявка</strong><span>→ внутренний учёт / 1С</span></div></div></div></div>'''
    return '''<div class="s51-visual s51-taxi" aria-label="Схема пользовательского пути приложения такси"><div class="s51-visual-label">СХЕМА ПОЛЬЗОВАТЕЛЬСКОГО ПУТИ · НЕ СКРИНШОТ</div><div class="s51-phone"><div class="s51-phonebar"><span>09:41</span><i>API online</i></div><div class="s51-map"><span class="s51-road a"></span><span class="s51-road b"></span><span class="s51-road c"></span><i class="s51-pin start"></i><i class="s51-pin finish"></i><b class="s51-route-line"></b></div><div class="s51-ride"><small>ТЕКУЩИЙ СЦЕНАРИЙ</small><strong>Поездка в процессе</strong><span>API status → UI → notification</span></div></div><div class="s51-mobile-steps"><span>01 Авторизация</span><b>↓</b><span>02 Поездка</span><b>↓</b><span>03 API / уведомления</span><b>↓</b><span>04 Release build</span></div></div>'''


def cards(items: list[tuple[str, str]]) -> str:
    return "".join(f'<article><h3>{H.escape(t)}</h3><p>{H.escape(d)}</p></article>' for t, d in items)


def step_cards(items: list[tuple[str, str, str]]) -> str:
    return "".join(f'<article><span>{n}</span><h3>{H.escape(t)}</h3><p>{H.escape(d)}</p></article>' for n, t, d in items)


def related(items: list[tuple[str, str]]) -> str:
    return "".join(f'<a href="{href}"><strong>{H.escape(title)}</strong><span>Перейти →</span></a>' for href, title in items)


for route, data in CASES.items():
    set_head(route, data["meta_title"], data["meta_desc"])
    tg_text = "Здравствуйте. Посмотрел кейс " + data["cta"].replace("?", "") + "\n\nЗадача: "
    telegram = "https://t.me/Alexuys?text=" + quote(tg_text)
    proof = "".join(f'<div><strong>{H.escape(a)}</strong><span>{H.escape(b)}</span></div>' for a, b in data["proof"])
    main = f'''<main id="main-content" data-stage51-case="{data['kind']}">
<section class="s51-hero"><div class="container"><nav class="s51-crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>→</span><a href="/cases/">Кейсы</a></nav><div class="s51-hero-grid"><div><span class="s51-kicker">{data['kicker']}</span><h1>{data['title']}</h1><p class="s51-lead">{data['lead']}</p><div class="s51-actions"><a class="s51-btn s51-btn--primary" href="{telegram}" target="_blank" rel="noopener noreferrer">Обсудить похожую задачу ↗</a><a class="s51-btn" href="/cases/">Все кейсы</a></div><div class="s51-proof">{proof}</div></div>{visual(data['kind'])}</div></div></section>
<section class="s51-section"><div class="container"><div class="s51-head"><span>01 / КОНТЕКСТ</span><div><h2>{data['problem_title']}</h2><p>{data['problem']}</p></div></div><div class="s51-steps">{step_cards(data['steps'])}</div></div></section>
<section class="s51-section s51-section--surface"><div class="container"><div class="s51-head"><span>02 / РЕАЛИЗОВАНО</span><div><h2>Что в этом кейсе <em>действительно подтверждается.</em></h2><p>Без универсальных обещаний и результатов, которых нельзя проверить по материалам проекта.</p></div></div><div class="s51-implemented">{cards(data['implemented'])}</div></div></section>
<section class="s51-section"><div class="container"><div class="s51-head"><span>03 / ГРАНИЦЫ</span><div><h2>Не превращаю кейс <em>в рекламную легенду.</em></h2><p>{data['scope']}</p></div></div><div class="s51-proof-note"><strong>Почему это важно</strong><p>Кейс полезен как подтверждение опыта с конкретным типом продукта и логики. Для новой задачи всё равно сначала проверяется её собственный контекст, ограничения и текущая реализация.</p></div></div></section>
<section class="s51-section"><div class="container"><div class="s51-head"><span>04 / СВЯЗАНО</span><div><h2>Какой тип разработки <em>стоит за этим проектом.</em></h2><p>Если задача похожа только частично, проще перейти сразу к нужному направлению.</p></div></div><div class="s51-related">{related(data['related'])}</div></div></section>
<section class="contact s51-contact"><div class="container"><div class="s51-contact-card"><div><span class="s51-kicker">ПОХОЖИЙ ПРОЕКТ</span><h2>{data['cta']}</h2><p>{data['cta_text']}</p></div><div class="s51-contact-actions"><a class="s51-btn s51-btn--primary" href="{telegram}" target="_blank" rel="noopener noreferrer">Написать @Alexuys ↗</a><a class="s51-btn" href="/services/">Выбрать направление</a></div></div></div></section>
</main>'''
    replace_main(route, main)

css_path = root / "assets/site-enhancements.css"
css = css_path.read_text(encoding="utf-8") if css_path.is_file() else ""
marker = "/* stage51 proof-driven case experience */"
if marker not in css:
    css += r'''

/* stage51 proof-driven case experience */
.s51-hero{padding:clamp(2.5rem,6vw,6rem) 0 clamp(5rem,9vw,8rem);background:radial-gradient(circle at 82% 8%,rgba(129,149,255,.12),transparent 28rem)}
.s51-crumbs{display:flex;gap:.55rem;align-items:center;margin-bottom:clamp(2rem,4vw,4rem);color:#727c86;font-size:.72rem}.s51-crumbs a{text-decoration:none}.s51-hero-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(25rem,.82fr);gap:clamp(2rem,5vw,5rem);align-items:center}.s51-kicker{display:block;color:#7e8791;font:750 .65rem/1.3 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.09em;text-transform:uppercase}.s51-hero h1{margin:1rem 0 0;max-width:11ch;font-size:clamp(3.2rem,6.7vw,6.8rem);line-height:.91;letter-spacing:-.065em}.s51-hero h1 em,.s51-head h2 em{font-style:normal;color:#9299a3}.s51-lead{max-width:46rem;margin:1.35rem 0 0;color:#9ba3ac;font-size:clamp(1rem,1.4vw,1.14rem);line-height:1.75}.s51-actions{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:1.65rem}.s51-btn{display:inline-flex;min-height:3rem;align-items:center;justify-content:center;padding:.75rem 1rem;border:1px solid rgba(255,255,255,.11);border-radius:.9rem;text-decoration:none;font-size:.8rem;font-weight:850}.s51-btn--primary{background:#c9ff4a;border-color:#c9ff4a;color:#090a0b}.s51-proof{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.55rem;margin-top:2rem}.s51-proof div{border-top:1px solid rgba(255,255,255,.11);padding-top:.8rem}.s51-proof strong,.s51-proof span{display:block}.s51-proof strong{font-size:.82rem}.s51-proof span{margin-top:.22rem;color:#7f8993;font-size:.69rem;line-height:1.45}
.s51-visual{position:relative;min-width:0;border:1px solid rgba(255,255,255,.11);border-radius:1.7rem;padding:2.9rem .85rem .85rem;background:linear-gradient(145deg,#141820,#0c0f13);box-shadow:0 38px 90px rgba(0,0,0,.38);overflow:hidden}.s51-visual-label{position:absolute;top:1rem;right:1rem;color:#6e7882;font:750 .56rem/1.2 ui-monospace,monospace;letter-spacing:.07em}.s51-window{border:1px solid rgba(255,255,255,.08);border-radius:1rem;overflow:hidden;background:#0d1116}.s51-windowbar{display:grid;grid-template-columns:1fr auto auto;gap:.7rem;padding:.8rem;border-bottom:1px solid rgba(255,255,255,.08);align-items:center}.s51-windowbar span{color:#737d87;font-size:.67rem}.s51-windowbar i{font-style:normal;color:#9ff1df;font-size:.66rem}.s51-kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:.55rem;padding:.7rem}.s51-kpis div,.s51-event{border:1px solid rgba(255,255,255,.07);border-radius:.8rem;padding:.75rem;background:rgba(255,255,255,.018)}.s51-kpis small,.s51-event small,.s51-event span{display:block;color:#737d87;font-size:.62rem}.s51-kpis strong{display:block;margin-top:.22rem}.s51-flow{display:flex;gap:.45rem;align-items:center;padding:0 .7rem .7rem}.s51-flow span{flex:1;border:1px solid rgba(129,149,255,.16);border-radius:.75rem;padding:.65rem;text-align:center;color:#b7bfca;font-size:.68rem}.s51-flow b{color:#66717d}.s51-event{margin:0 .7rem .7rem}.s51-event strong{display:block;margin:.25rem 0}.s51-catalog-shell{display:grid;grid-template-columns:.32fr .68fr;min-height:25rem;border:1px solid rgba(255,255,255,.08);border-radius:1rem;overflow:hidden}.s51-catalog-shell aside{padding:1rem;background:#0b0e12;border-right:1px solid rgba(255,255,255,.08)}.s51-catalog-shell aside b,.s51-catalog-shell aside span{display:block}.s51-catalog-shell aside span{padding:.66rem 0;border-bottom:1px solid rgba(255,255,255,.05);color:#78828c;font-size:.7rem}.s51-catalog-main{padding:1rem}.s51-catalog-main>small{color:#707a84;font-size:.62rem}.s51-catalog-main h3{margin:.25rem 0 0;font-size:1.45rem}.s51-products{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.5rem;margin-top:1rem}.s51-products div{border:1px solid rgba(255,255,255,.07);border-radius:.8rem;padding:.75rem}.s51-products i,.s51-products strong,.s51-products small{display:block}.s51-products i{color:#8195ff;font-style:normal;font-size:.6rem}.s51-products small{margin-top:.3rem;color:#737d87;font-size:.62rem}.s51-request{margin-top:.65rem;border:1px solid rgba(201,255,74,.14);border-radius:.85rem;padding:.8rem;background:rgba(201,255,74,.035)}.s51-request small,.s51-request strong,.s51-request span{display:block}.s51-request small,.s51-request span{color:#7c8791;font-size:.64rem}.s51-request strong{margin:.22rem 0}.s51-taxi{display:grid;grid-template-columns:minmax(14rem,.7fr) minmax(10rem,.3fr);gap:.75rem;align-items:center}.s51-phone{max-width:18rem;margin:auto;border:1px solid rgba(255,255,255,.1);border-radius:2rem;padding:.65rem;background:#0d1116;box-shadow:0 25px 55px rgba(0,0,0,.35)}.s51-phonebar{display:flex;justify-content:space-between;padding:.2rem .25rem .55rem;color:#707a84;font-size:.58rem}.s51-phonebar i{font-style:normal;color:#9ff1df}.s51-map{position:relative;height:12rem;border-radius:1.35rem;background:linear-gradient(145deg,#111722,#10131b);overflow:hidden}.s51-road{position:absolute;height:1px;background:#263247;transform-origin:left}.s51-road.a{left:8%;top:24%;width:96%;transform:rotate(27deg)}.s51-road.b{left:0;top:70%;width:112%;transform:rotate(-18deg)}.s51-road.c{left:47%;top:0;width:92%;transform:rotate(72deg)}.s51-pin{position:absolute;width:.48rem;height:.48rem;border-radius:50%;background:#8195ff;box-shadow:0 0 0 .24rem rgba(129,149,255,.13)}.s51-pin.start{left:25%;top:31%}.s51-pin.finish{right:21%;bottom:23%}.s51-route-line{position:absolute;left:27%;top:33%;width:50%;height:42%;border-left:2px solid #8195ff;border-bottom:2px solid #8195ff;border-radius:0 0 0 1.2rem;transform:skewX(-17deg)}.s51-ride{padding:.8rem .35rem .25rem}.s51-ride small,.s51-ride strong,.s51-ride span{display:block}.s51-ride small,.s51-ride span{color:#737d87;font-size:.62rem}.s51-ride strong{margin:.25rem 0}.s51-mobile-steps{display:grid;gap:.48rem}.s51-mobile-steps span{border:1px solid rgba(255,255,255,.08);border-radius:.75rem;padding:.68rem;color:#a4adb6;font-size:.68rem}.s51-mobile-steps b{text-align:center;color:#596471}
.s51-section{padding:clamp(5rem,8vw,8rem) 0}.s51-section--surface{border-block:1px solid rgba(255,255,255,.07);background:rgba(255,255,255,.012)}.s51-head{display:grid;grid-template-columns:minmax(8rem,.28fr) minmax(0,1fr);gap:2rem;margin-bottom:2rem}.s51-head>span{color:#707a84;font:750 .62rem/1.3 ui-monospace,monospace;letter-spacing:.08em}.s51-head h2{margin:0;max-width:15ch;font-size:clamp(2.4rem,4.9vw,4.9rem);line-height:.97;letter-spacing:-.055em}.s51-head p{max-width:48rem;margin:1rem 0 0;color:#919aa4;line-height:1.72}.s51-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid rgba(255,255,255,.1)}.s51-steps article{padding:1.35rem 1.15rem 1.35rem 0;border-bottom:1px solid rgba(255,255,255,.1)}.s51-steps article+article{padding-left:1.15rem;border-left:1px solid rgba(255,255,255,.08)}.s51-steps span{color:#6f7983;font:750 .62rem/1 ui-monospace,monospace}.s51-steps h3{margin:.75rem 0 0;font-size:1rem}.s51-steps p{margin:.55rem 0 0;color:#89939d;font-size:.82rem;line-height:1.62}.s51-implemented{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.65rem}.s51-implemented article{border:1px solid rgba(255,255,255,.09);border-radius:1rem;padding:1.1rem;background:#0e1217}.s51-implemented h3{margin:0;font-size:1rem}.s51-implemented p{margin:.48rem 0 0;color:#8b949e;font-size:.83rem;line-height:1.62}.s51-proof-note{max-width:58rem;border-left:2px solid #8195ff;padding:1rem 1.1rem;background:rgba(129,149,255,.035)}.s51-proof-note strong{display:block}.s51-proof-note p{margin:.45rem 0 0;color:#8f98a2;font-size:.86rem;line-height:1.68}.s51-related{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.65rem}.s51-related a{border:1px solid rgba(255,255,255,.09);border-radius:1rem;padding:1.05rem;text-decoration:none;background:#0e1217;transition:.2s ease}.s51-related a:hover{transform:translateY(-2px);border-color:rgba(255,255,255,.18)}.s51-related strong,.s51-related span{display:block}.s51-related span{margin-top:.4rem;color:#77828d;font-size:.72rem}.s51-contact{padding:0 0 clamp(5rem,8vw,8rem)!important}.s51-contact-card{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2rem;align-items:end;border:1px solid rgba(255,255,255,.1);border-radius:1.5rem;padding:clamp(1.5rem,4vw,3rem);background:linear-gradient(145deg,#13171c,#0c0f13)}.s51-contact-card h2{margin:.65rem 0 0;max-width:14ch;font-size:clamp(2.3rem,4.6vw,4.8rem);line-height:.97;letter-spacing:-.055em}.s51-contact-card p{max-width:42rem;color:#919aa4}.s51-contact-actions{display:grid;gap:.55rem;min-width:14rem}
@media(max-width:920px){.s51-hero-grid,.s51-head,.s51-contact-card{grid-template-columns:1fr}.s51-proof{grid-template-columns:1fr 1fr 1fr}.s51-steps{grid-template-columns:1fr 1fr}.s51-steps article:nth-child(3){padding-left:0;border-left:0}.s51-taxi{grid-template-columns:1fr}.s51-mobile-steps{grid-template-columns:repeat(4,1fr);align-items:center}.s51-mobile-steps b{transform:rotate(-90deg)}.s51-contact-actions{min-width:0}}
@media(max-width:640px){.s51-hero{padding-top:2rem}.s51-hero h1{max-width:100%;font-size:clamp(2.7rem,13vw,4rem)}.s51-actions{display:grid}.s51-btn{width:100%;white-space:normal;text-align:center}.s51-proof{grid-template-columns:1fr}.s51-visual{border-radius:1.2rem}.s51-windowbar{grid-template-columns:1fr}.s51-windowbar span,.s51-windowbar i{display:none}.s51-kpis,.s51-products{grid-template-columns:1fr}.s51-flow{display:grid}.s51-flow b{transform:rotate(90deg);text-align:center}.s51-catalog-shell{grid-template-columns:1fr}.s51-catalog-shell aside{display:none}.s51-steps,.s51-implemented,.s51-related{grid-template-columns:1fr}.s51-steps article,.s51-steps article+article,.s51-steps article:nth-child(3){padding:1rem 0;border-left:0}.s51-mobile-steps{grid-template-columns:1fr}.s51-mobile-steps b{transform:none}.s51-head h2{max-width:100%;font-size:clamp(2.1rem,11vw,3.2rem)}.s51-contact-card{border-radius:1.15rem}.s51-contact-card h2{max-width:100%}}
'''
    css_path.write_text(css, encoding="utf-8")

print("stage51 case experience: auto-crm + factory-catalog + taxi-app rebuilt")
