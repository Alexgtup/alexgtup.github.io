#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def replace_once(html: str, old: str, new: str, label: str) -> str:
    if new in html:
        return html
    if old not in html:
        raise SystemExit(f"stage22: marker not found for {label}")
    return html.replace(old, new, 1)


def patch_web_development() -> bool:
    path = root / "web-development/index.html"
    if not path.exists():
        raise SystemExit("stage22: missing web-development/index.html")
    html = path.read_text(encoding="utf-8")
    if 'data-stage22-broad-intent="true"' in html:
        return False

    old_title = "Разработка веб-сервисов и MVP на заказ — React, Next.js | Alexuys"
    new_title = "Разработка сайтов и веб-сервисов на заказ | Alexuys"
    old_desc = "Разработка веб-сервисов и MVP на заказ: личные кабинеты, CRM, каталоги, внутренние панели и SaaS-интерфейсы. React, Next.js, backend, API и запуск."
    new_desc = "Разработка сайтов и веб-сервисов на заказ: корпоративные сайты, каталоги, личные кабинеты, CRM, SaaS и MVP. React, Next.js, backend, API и запуск."

    html = replace_once(html, f"<title>{old_title}</title>", f"<title>{new_title}</title>", "title")
    html = html.replace(f'meta content="{old_desc}" name="description"', f'meta content="{new_desc}" name="description"', 1)
    html = html.replace(f'meta content="{old_title}" property="og:title"', f'meta content="{new_title}" property="og:title"', 1)
    html = html.replace(f'meta content="{old_desc}" property="og:description"', f'meta content="{new_desc}" property="og:description"', 1)
    html = html.replace(f'meta content="{old_title}" name="twitter:title"', f'meta content="{new_title}" name="twitter:title"', 1)
    html = html.replace(f'meta content="{old_desc}" name="twitter:description"', f'meta content="{new_desc}" name="twitter:description"', 1)

    html = replace_once(
        html,
        '<h1>Разработка веб-сервисов <em>и MVP</em></h1>',
        '<h1>Разработка сайтов <em>и веб-сервисов</em></h1>',
        "h1",
    )
    html = replace_once(
        html,
        '<p class="lead">Собираю не просто страницу, а рабочий продукт: интерфейс, данные, роли, backend и интеграции. Первый релиз строится вокруг главного пользовательского сценария, чтобы продукт можно было проверить и развивать дальше.</p>',
        '<p class="lead">Разрабатываю сайты и веб-сервисы под задачу: от корпоративного сайта и каталога до личного кабинета, внутренней системы или MVP. Там, где нужны данные и бизнес-логика, подключаются backend, роли, API и интеграции.</p>',
        "lead",
    )

    html = replace_once(
        html,
        '<h2>Коротко: что такое разработка веб-сервиса на заказ</h2>',
        '<h2>Коротко: что входит в разработку сайта и веб-сервиса на заказ</h2>',
        "intent heading",
    )
    html = replace_once(
        html,
        '<p class="intent-summary-lead">Веб-сервис — это не просто информационный сайт, а интерфейс, который работает с данными и процессом: личные кабинеты, внутренние панели, SaaS, каталоги, роли, документы, заявки и API. Заказная разработка оправдана, когда готовый конструктор или CMS уже не закрывают пользовательский сценарий и бизнес-логику.</p>',
        '<p class="intent-summary-lead">Разработка сайта может быть как информационной, так и продуктовой: корпоративный сайт, каталог, личный кабинет, B2B-портал, SaaS или внутренняя система. Для простого контента достаточно лёгкой архитектуры; когда появляются роли, данные, заявки и интеграции, сайт превращается в полноценный веб-сервис с backend и API.</p>',
        "intent lead",
    )

    html = replace_once(
        html,
        '<article class="card"><span class="num" data-nosnippet="">03</span><h3>Каталоги и сервисы</h3><p>Структурированные данные, поиск, карточки и формы заявки.</p></article>',
        '<article class="card"><span class="num" data-nosnippet="">03</span><h3>Сайты и каталоги</h3><p>Корпоративные страницы, структура услуг или продукции, поиск, карточки и формы заявки.</p></article>',
        "website card",
    )

    html = html.replace(
        '"@type":"Service","name":"Разработка веб-сервисов и MVP"',
        '"@type":"Service","@id":"https://alexgtup.github.io/web-development/#service","name":"Разработка сайтов и веб-сервисов на заказ"',
        1,
    )
    html = html.replace('"serviceType":"WEB SERVICE, MVP, PRODUCT"', '"serviceType":"WEBSITE, WEB SERVICE, MVP, PRODUCT"', 1)
    html = html.replace(f'"description":"{old_desc}"', f'"description":"{new_desc}"', 1)

    web_page_schema = '''<script type="application/ld+json" data-stage22-broad-intent="true">{"@context":"https://schema.org","@type":"WebPage","@id":"https://alexgtup.github.io/web-development/#webpage","url":"https://alexgtup.github.io/web-development/","name":"Разработка сайтов и веб-сервисов на заказ","inLanguage":"ru-RU","isPartOf":{"@id":"https://alexgtup.github.io/#website"},"about":{"@id":"https://alexgtup.github.io/#person"},"mainEntity":{"@id":"https://alexgtup.github.io/web-development/#service"},"keywords":["разработка сайтов","разработка сайта на заказ","разработка веб-сервисов","создание сайта","корпоративный сайт","веб-разработка","React","Next.js","MVP"]}</script>'''
    if "</head>" not in html:
        raise SystemExit("stage22: </head> not found")
    html = html.replace("</head>", web_page_schema + "\n</head>", 1)

    path.write_text(html, encoding="utf-8")
    return True


def patch_internal_anchors() -> list[str]:
    changed = []

    # Main page: use an explicit commercial phrase for the web-development hub.
    path = root / "index.html"
    if path.exists():
        html = path.read_text(encoding="utf-8")
        old = "<strong>Веб-продукты</strong>"
        new = "<strong>Сайты и веб-сервисы</strong>"
        if old in html and new not in html:
            html = html.replace(old, new, 1)
            path.write_text(html, encoding="utf-8")
            changed.append("/")

    # Services hub: keep visible anchor, description and ItemList schema aligned
    # with the P0 broad intent owned by /web-development/.
    path = root / "services/index.html"
    if path.exists():
        html = path.read_text(encoding="utf-8")
        touched = False
        replacements = [
            (
                '<a class="service" href="/web-development/"><div class="meta" data-nosnippet=""><span>WEB · MVP</span><span>05</span></div><h2>Веб-сервисы и MVP</h2><p>Личные кабинеты, SaaS-интерфейсы, внутренние панели, каталоги и сервисы с понятной продуктовой логикой.</p>',
                '<a class="service" href="/web-development/"><div class="meta" data-nosnippet=""><span>WEB · SITES · MVP</span><span>05</span></div><h2>Разработка сайтов и веб-сервисов</h2><p>Корпоративные сайты, каталоги, личные кабинеты, SaaS и внутренние системы — от интерфейса до backend и API.</p>',
            ),
            (
                '"url":"https://alexgtup.github.io/web-development/","name":"Веб-сервисы и MVP"',
                '"url":"https://alexgtup.github.io/web-development/","name":"Разработка сайтов и веб-сервисов"',
            ),
        ]
        for old, new in replacements:
            if old in html:
                html = html.replace(old, new, 1)
                touched = True
        if touched:
            path.write_text(html, encoding="utf-8")
            changed.append("/services/")

    return changed


changed = []
if patch_web_development():
    changed.append("/web-development/")
changed.extend(patch_internal_anchors())
print("stage22 patched:", ", ".join(changed) if changed else "already applied")
