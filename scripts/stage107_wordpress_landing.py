#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
BASE = "https://alexgtup.github.io"
ROUTE = "/wordpress-development/"
TODAY = "2026-09-16"


def page_path(route: str) -> Path:
    return ROOT / ("index.html" if route == "/" else route.strip("/") + "/index.html")


def write_wordpress_page() -> None:
    path = page_path(ROUTE)
    path.parent.mkdir(parents=True, exist_ok=True)
    html = r'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<meta name="theme-color" content="#08090b"/>
<meta name="color-scheme" content="dark"/>
<title>Доработка WordPress сайта - разработка и исправления | Alexuys</title>
<meta name="description" content="Доработка WordPress сайтов: ошибки, формы, адаптив, скорость, темы и плагины, API-интеграции, техническое SEO и микроразметка. Работа с существующим сайтом без лишней пересборки."/>
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
<link rel="canonical" href="https://alexgtup.github.io/wordpress-development/"/>
<meta property="og:type" content="website"/>
<meta property="og:locale" content="ru_RU"/>
<meta property="og:site_name" content="Alexuys"/>
<meta property="og:title" content="Доработка WordPress сайта - разработка и исправления | Alexuys"/>
<meta property="og:description" content="Исправления и развитие существующих WordPress сайтов: формы, адаптив, производительность, интеграции, SEO и микроразметка."/>
<meta property="og:url" content="https://alexgtup.github.io/wordpress-development/"/>
<meta property="og:image" content="https://alexgtup.github.io/assets/og/alexuys-default.jpg"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="Доработка WordPress сайта - разработка и исправления | Alexuys"/>
<meta name="twitter:description" content="WordPress разработчик для доработки действующего сайта: ошибки, формы, скорость, интеграции и техническое SEO."/>
<meta name="twitter:image" content="https://alexgtup.github.io/assets/og/alexuys-default.jpg"/>
<meta name="author" content="Alexuys"/>
<link rel="author" href="https://alexgtup.github.io/about/"/>
<link rel="icon" href="/favicon.ico" sizes="any"/>
<link rel="icon" href="/favicon.svg" type="image/svg+xml"/>
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180"/>
<link rel="manifest" href="/site.webmanifest"/>
<link rel="stylesheet" href="/assets/universal-media.css"/>
<link rel="stylesheet" href="/assets/site-enhancements.css"/>
<link rel="stylesheet" href="/assets/layout-system.css"/>
<style>
:root{--bg:#08090b;--surface:#10141a;--surface2:#0d1116;--text:#f3f5f2;--muted:#98a0aa;--line:rgba(255,255,255,.1);--line2:rgba(255,255,255,.18);--lime:#c9ff4a;--blue:#8195ff;--page:clamp(1.1rem,4vw,4rem);--max:88rem}
*{box-sizing:border-box}html{background:var(--bg);scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 85% 4%,rgba(129,149,255,.12),transparent 29rem),radial-gradient(circle at 5% 42%,rgba(201,255,74,.035),transparent 22rem),var(--bg);color:var(--text);font-family:ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;line-height:1.58;-webkit-font-smoothing:antialiased}.container{width:min(100%,var(--max));margin:auto;padding-inline:var(--page)}a{color:inherit}.header{position:sticky;top:0;z-index:30;background:rgba(8,9,11,.82);backdrop-filter:blur(18px);border-bottom:1px solid var(--line)}.head{min-height:4.8rem;display:flex;align-items:center;justify-content:space-between;gap:1rem}.brand{display:flex;align-items:center;gap:.7rem;text-decoration:none;font-weight:850}.brand-mark{width:42px;height:42px;display:grid;place-items:center;border-radius:14px;background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.1)}.brand-mark svg{width:24px;height:24px}.nav{display:flex;align-items:center;gap:1rem}.nav a{font-size:.79rem;color:#abb2ba;text-decoration:none}.nav .cta{background:var(--lime);color:#090a0b;padding:.64rem .88rem;border-radius:.8rem;font-weight:850}.crumbs{padding-top:2rem;color:#737c86;font-size:.72rem}.crumbs a{text-decoration:none}.hero{display:grid;grid-template-columns:1.18fr .82fr;gap:clamp(2rem,5vw,5rem);align-items:end;padding:3rem 0 5.5rem}.eyebrow{font:750 .66rem/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.09em;text-transform:uppercase;color:#858e98}.hero h1{margin:1rem 0 0;max-width:11ch;font-size:clamp(3.35rem,7vw,7rem);line-height:.91;letter-spacing:-.067em}.hero h1 em{font-style:normal;color:#929aa3}.lead{max-width:47rem;margin:1.35rem 0 0;color:#9da5ae;font-size:clamp(1rem,1.45vw,1.14rem);line-height:1.75}.actions{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:1.6rem}.btn{display:inline-flex;min-height:3rem;align-items:center;justify-content:center;padding:.76rem 1rem;border:1px solid var(--line);border-radius:.9rem;text-decoration:none;font-size:.82rem;font-weight:850}.btn.primary{background:var(--lime);border-color:var(--lime);color:#090a0b}.hero-side{border:1px solid var(--line);border-radius:1.5rem;padding:1rem;background:linear-gradient(145deg,#121720,#0c1015)}.signal{display:grid;gap:.6rem}.signal article{padding:1rem;border:1px solid var(--line);border-radius:1rem;background:rgba(255,255,255,.018)}.signal small{display:block;color:#75808a;font:750 .61rem/1 ui-monospace,monospace;text-transform:uppercase}.signal strong{display:block;margin:.45rem 0 .25rem}.signal span{color:#8f98a2;font-size:.78rem}.section{padding:5.4rem 0}.section-head{display:grid;grid-template-columns:.28fr 1.72fr;gap:2rem;margin-bottom:2rem}.index{color:#747e88;font:750 .62rem/1 ui-monospace,monospace}.section h2{margin:0;max-width:15ch;font-size:clamp(2.45rem,4.8vw,4.8rem);line-height:.97;letter-spacing:-.055em}.section h2 em{font-style:normal;color:#929aa3}.intro{max-width:48rem;color:#929ba4}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:.72rem}.card{padding:1.25rem;border:1px solid var(--line);border-radius:1.12rem;background:linear-gradient(145deg,#11161c,#0d1015)}.card small{color:#77818b;font:750 .61rem/1 ui-monospace,monospace}.card h3{margin:.8rem 0 .5rem;font-size:1.08rem}.card p{margin:0;color:#929ba4;font-size:.86rem}.process{border-top:1px solid var(--line)}.step{display:grid;grid-template-columns:4rem .68fr 1.32fr;gap:1rem;padding:1.35rem 0;border-bottom:1px solid var(--line)}.step span{color:#727c86;font:750 .61rem/1 ui-monospace,monospace}.step p{margin:0;color:#919aa4}.related{display:grid;grid-template-columns:repeat(4,1fr);gap:.65rem}.related a{padding:1rem;border:1px solid var(--line);border-radius:1rem;background:#0d1116;text-decoration:none}.related strong{display:block}.related span{display:block;margin-top:.35rem;color:#808a94;font-size:.72rem}.faq{border-top:1px solid var(--line)}details{padding:1.1rem 0;border-bottom:1px solid var(--line)}summary{cursor:pointer;font-weight:850}details p{max-width:60rem;color:#949ca6}.contact{padding:5.8rem 0 4rem}.contact-card{padding:clamp(1.5rem,4vw,3.2rem);border:1px solid var(--line);border-radius:1.55rem;background:linear-gradient(145deg,#12161d,#0c0f13)}.contact-card h2{margin:0;max-width:13ch;font-size:clamp(2.6rem,5vw,5rem);line-height:.95;letter-spacing:-.06em}.contact-card p{max-width:44rem;color:#98a0a9}.footer{border-top:1px solid var(--line);padding:2rem 0 3rem;color:#707984;font-size:.72rem}.footer .container{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap}@media(max-width:850px){.hero,.section-head{grid-template-columns:1fr}.cards{grid-template-columns:1fr 1fr}.related{grid-template-columns:1fr 1fr}.step{grid-template-columns:2.5rem 1fr}.step p{grid-column:2}.nav a:not(.cta){display:none}}@media(max-width:560px){.hero{padding-top:1.5rem}.hero h1{font-size:clamp(3rem,15vw,4.7rem)}.cards,.related{grid-template-columns:1fr}.section{padding:4.2rem 0}}
</style>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","@id":"https://alexgtup.github.io/wordpress-development/#service","name":"Доработка WordPress сайтов","serviceType":"WordPress development and website maintenance","url":"https://alexgtup.github.io/wordpress-development/","description":"Доработка существующих WordPress сайтов: ошибки, формы, адаптив, производительность, темы и плагины, API-интеграции, техническое SEO и микроразметка.","provider":{"@type":"Person","@id":"https://alexgtup.github.io/#person","name":"Александр","url":"https://alexgtup.github.io/about/"},"areaServed":"Worldwide"}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Можно доработать существующий WordPress сайт без пересборки?","acceptedAnswer":{"@type":"Answer","text":"Да. Сначала проверяется текущая тема, плагины, шаблоны и конфликтующие изменения. Если существующую основу разумно сохранить, работа идёт поверх неё без ненужной пересборки сайта."}},{"@type":"Question","name":"Можно исправить формы, мобильную версию и плагины?","acceptedAnswer":{"@type":"Answer","text":"Да. Можно разбирать конкретные ошибки формы, адаптива, JavaScript, PHP, темы или плагинов и исправлять их по отдельности."}},{"@type":"Question","name":"Работаете с техническим SEO WordPress?","acceptedAnswer":{"@type":"Answer","text":"Да. В доработку могут входить индексация, sitemap, robots, canonical, метаданные, микроразметка, скорость и внутренняя перелинковка."}},{"@type":"Question","name":"Нужно ли готовое техническое задание?","acceptedAnswer":{"@type":"Answer","text":"Нет. Для начала достаточно ссылки на сайт и короткого описания проблемы или желаемого результата."}}]}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Главная","item":"https://alexgtup.github.io/"},{"@type":"ListItem","position":2,"name":"Услуги","item":"https://alexgtup.github.io/services/"},{"@type":"ListItem","position":3,"name":"Доработка WordPress","item":"https://alexgtup.github.io/wordpress-development/"}]}</script>
</head>
<body data-page="wordpress-development">
<a class="skip-link" href="#main-content">Перейти к содержанию</a>
<header class="header" data-nosnippet><div class="container head"><a class="brand" href="/" aria-label="Alexuys - на главную"><span class="brand-mark" aria-hidden="true"><svg fill="none" viewBox="0 0 36 36"><path d="M8 10h4.5c5.3 0 5.3 8 10.3 8H28" stroke="#f3f4f1" stroke-linecap="round" stroke-width="2"/><path d="M8 26h4.5c5.3 0 5.3-8 10.3-8H28" stroke="#8195ff" stroke-linecap="round" stroke-width="2"/><circle cx="8" cy="10" fill="#f3f4f1" r="2.2"/><circle cx="8" cy="26" fill="#8195ff" r="2.2"/><circle cx="28" cy="18" fill="#c9ff4a" r="2.75"/></svg></span><strong>alexuys</strong></a><nav class="nav" aria-label="Навигация"><a href="/cases/">Кейсы</a><a href="/services/">Услуги</a><a href="/guides/">Разборы</a><a class="cta" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer">Обсудить задачу ↗</a></nav></div></header>
<main id="main-content">
<div class="container crumbs"><a href="/">Главная</a> / <a href="/services/">Услуги</a> / Доработка WordPress</div>
<section class="container hero"><div><div class="eyebrow">WORDPRESS · ДОРАБОТКА · ПОДДЕРЖКА</div><h1>Доработка WordPress <em>без пересборки с нуля.</em></h1><p class="lead">Если сайт уже работает, но мешают ошибки, старый код, формы, мобильная версия, скорость, плагины или SEO - сначала разбираю текущую систему и сохраняю то, что не требует замены.</p><div class="actions"><a class="btn primary" href="https://t.me/Alexuys?text=Здравствуйте.%20Нужна%20доработка%20WordPress%20сайта.%20Ссылка%3A%20" target="_blank" rel="noopener noreferrer">Прислать сайт ↗</a><a class="btn" href="/project-repair/">Как проходит доработка</a></div></div><aside class="hero-side"><div class="signal"><article><small>СТАРТ</small><strong>Можно с одной проблемы</strong><span>Ссылка на сайт + что сейчас не работает.</span></article><article><small>КОД</small><strong>Тема, плагины, PHP, JS</strong><span>Сначала причина, потом точечное изменение.</span></article><article><small>ПОИСК</small><strong>SEO и микроразметка</strong><span>Индексация, sitemap, metadata, schema и скорость.</span></article><article><small>ФОРМАТ</small><strong>Новый блок или развитие сайта</strong><span>Не только исправления - можно добавлять функционал.</span></article></div></aside></section>
<section class="section container"><div class="section-head"><div class="index">01 / ЗАДАЧИ</div><div><h2>Что обычно нужно <em>исправить или добавить.</em></h2><p class="intro">Страница рассчитана именно на действующие WordPress проекты, где ценнее аккуратно продолжить систему, чем заново собирать сайт.</p></div></div><div class="cards"><article class="card"><small>01</small><h3>Формы и заявки</h3><p>Валидация, согласия, отправка писем, AJAX, ошибки полей, интеграция с CRM или внешним API.</p></article><article class="card"><small>02</small><h3>Мобильная версия</h3><p>Меню, sticky-шапка, переполнение, сетки, таблицы, кнопки и проблемные экраны 320-430 px.</p></article><article class="card"><small>03</small><h3>Тема и плагины</h3><p>Доработка шаблонов, PHP и JavaScript, конфликты плагинов, шорткоды и логика вывода блоков.</p></article><article class="card"><small>04</small><h3>Новые страницы и блоки</h3><p>Посадочные страницы, калькуляторы, FAQ, табы, формы, каталоги и переиспользуемые компоненты.</p></article><article class="card"><small>05</small><h3>Скорость</h3><p>Лишние скрипты и стили, изображения, lazy load, кеширование и тяжёлые элементы интерфейса.</p></article><article class="card"><small>06</small><h3>Техническое SEO</h3><p>Canonical, robots, sitemap, метаданные, JSON-LD, внутренняя перелинковка и проблемы индексации.</p></article></div></section>
<section class="section container"><div class="section-head"><div class="index">02 / ПРОЦЕСС</div><div><h2>Сначала причина. <em>Потом изменение.</em></h2><p class="intro">На существующем WordPress сайте опасно исправлять симптом отдельным CSS или ещё одним плагином, если проблема находится уровнем ниже.</p></div></div><div class="process"><div class="step"><span>01</span><strong>Проверка текущего состояния</strong><p>Смотрю страницу, тему, активные плагины, код и место, где появляется ошибка.</p></div><div class="step"><span>02</span><strong>Минимальный безопасный объём</strong><p>Определяю, что нужно изменить, а что лучше оставить без вмешательства.</p></div><div class="step"><span>03</span><strong>Правка и проверка сценария</strong><p>Проверяю desktop/mobile, пользовательский путь и связанные формы или интеграции.</p></div><div class="step"><span>04</span><strong>Следующий этап при необходимости</strong><p>Если задача раскрывает более системную проблему, её можно вынести в отдельный понятный этап.</p></div></div></section>
<section class="section container"><div class="section-head"><div class="index">03 / СВЯЗАНО</div><div><h2>Когда WordPress - только <em>часть задачи.</em></h2></div></div><div class="related"><a href="/project-repair/"><strong>Доработка проекта</strong><span>Чужой код, ошибки и незавершённые релизы</span></a><a href="/api-integrations/"><strong>API-интеграции</strong><span>CRM, формы, webhooks и внешние сервисы</span></a><a href="/web-development/"><strong>Веб-разработка</strong><span>Когда WordPress уже ограничивает продукт</span></a><a href="/guides/development-cost/"><strong>Оценка разработки</strong><span>Как определить объём первого этапа</span></a></div></section>
<section class="section container"><div class="section-head"><div class="index">04 / FAQ</div><div><h2>До начала работы</h2></div></div><div class="faq"><details><summary>Можно начать с одной небольшой правки?</summary><p>Да. Для первого обращения достаточно ссылки и описания конкретной проблемы. Не требуется заранее собирать большое ТЗ.</p></details><details><summary>Нужно ли менять тему или ставить новый конструктор?</summary><p>Не обязательно. Если текущая основа позволяет решить задачу без пересборки, её разумнее сохранить.</p></details><details><summary>Можно работать с уже изменённой темой?</summary><p>Да. Перед правкой важно определить, где находятся кастомные изменения и что может быть перезаписано обновлением.</p></details><details><summary>Можно одновременно поправить SEO и интерфейс?</summary><p>Да, если задачи связаны. Например, новая посадочная страница может одновременно требовать адаптива, формы, метаданных, schema и корректной перелинковки.</p></details></div></section>
<section class="contact container"><div class="contact-card"><h2>Пришлите ссылку <em>и проблему.</em></h2><p>Можно коротко: что сейчас происходит, как должно работать и на какой странице это видно. Этого достаточно, чтобы начать разбор.</p><div class="actions"><a class="btn primary" href="https://t.me/Alexuys?text=Здравствуйте.%20Нужна%20доработка%20WordPress%20сайта.%20Ссылка%3A%20" target="_blank" rel="noopener noreferrer">Написать в Telegram ↗</a><a class="btn" href="/cases/">Посмотреть кейсы</a></div></div></section>
</main>
<footer class="footer"><div class="container"><span>Alexuys · разработка и доработка цифровых продуктов</span><a href="/privacy/">Конфиденциальность</a></div></footer>
<script src="/assets/analytics.js" defer></script><script src="/assets/site-enhancements.js" defer></script>
</body></html>'''
    path.write_text(html, encoding="utf-8")


def add_sitemap_entry() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    loc = BASE + ROUTE
    if f"<loc>{loc}</loc>" in text:
        return
    entry = f'<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>0.90</priority></url>'
    if "</urlset>" not in text:
        raise SystemExit("stage107: sitemap closing tag missing")
    text = text.replace("</urlset>", entry + "</urlset>", 1)
    path.write_text(text, encoding="utf-8")


def patch_services() -> None:
    path = page_path("/services/")
    text = path.read_text(encoding="utf-8")
    if 'href="/wordpress-development/"' in text:
        return
    marker = '<div class="semantic-links-grid">'
    card = '<a href="/wordpress-development/"><strong>Доработка WordPress</strong><span>Ошибки, формы, адаптив, скорость, SEO и интеграции</span></a>'
    if marker in text:
        text = text.replace(marker, marker + card, 1)
    else:
        block = '<nav class="s101-more" aria-label="Дополнительные услуги"><a href="/wordpress-development/">Доработка WordPress сайта</a></nav>'
        if "</main>" not in text:
            raise SystemExit("stage107: services insertion point missing")
        text = text.replace("</main>", block + "</main>", 1)
    path.write_text(text, encoding="utf-8")


def add_related(route: str, label: str) -> None:
    path = page_path(route)
    if not path.is_file():
        raise SystemExit(f"stage107: related source missing: {route}")
    text = path.read_text(encoding="utf-8")
    marker = f'data-stage107-wordpress="{route.strip("/") or "home"}"'
    if marker in text:
        return
    block = (
        f'<nav class="s101-more s107-related" {marker} aria-label="Связанная услуга">'
        f'<a href="/wordpress-development/">{label}</a></nav>'
    )
    patterns = [
        r'<section\b[^>]*class="[^"]*\bs48-contact\b[^"]*"[^>]*>',
        r'<section\b[^>]*class="[^"]*\bcontact\b[^"]*"[^>]*>',
        r'<section\b[^>]*id="contact"[^>]*>',
        r'</main>',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            text = text[:match.start()] + block + "\n" + text[match.start():]
            path.write_text(text, encoding="utf-8")
            return
    raise SystemExit(f"stage107: no related insertion point for {route}")


write_wordpress_page()
add_sitemap_entry()
patch_services()
add_related("/project-repair/", "Отдельно: доработка WordPress сайта")
add_related("/web-development/", "Есть действующий WordPress? Доработка без пересборки")
add_related("/api-integrations/", "WordPress + API: формы, CRM и внешние сервисы")
add_related("/freelance-developer/", "Доработка WordPress как отдельная задача")

# Guards for the new commercial entry.
html = page_path(ROUTE).read_text(encoding="utf-8")
for required in (
    '<link rel="canonical" href="https://alexgtup.github.io/wordpress-development/"/>',
    'Доработка WordPress',
    'application/ld+json',
    'href="https://t.me/Alexuys',
):
    if required not in html:
        raise SystemExit("stage107: WordPress page invariant missing: " + required)

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
if sitemap.count("https://alexgtup.github.io/wordpress-development/") != 1:
    raise SystemExit("stage107: WordPress sitemap invariant failed")

inbound = 0
for path in ROOT.rglob("*.html"):
    if path == page_path(ROUTE):
        continue
    try:
        body = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    if 'href="/wordpress-development/"' in body:
        inbound += 1
if inbound < 5:
    raise SystemExit(f"stage107: weak WordPress inbound graph: {inbound}")

print(f"stage107 WordPress landing: route={ROUTE}; inbound_sources={inbound}; sitemap=ok")
