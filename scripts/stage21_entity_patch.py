#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def read(path: str) -> tuple[Path, str]:
    target = root / path
    if not target.exists():
        raise SystemExit(f"stage21: missing target {path}")
    return target, target.read_text(encoding="utf-8")


def write(target: Path, html: str) -> None:
    target.write_text(html, encoding="utf-8")


changed = []

# 1) Give the primary Telegram service a stable entity ID and connect the page,
#    service and developer explicitly in JSON-LD.
target, html = read("telegram-bots/index.html")
service_old = '"@type":"Service","name":"Разработка Telegram-ботов на заказ"'
service_new = '"@type":"Service","@id":"https://alexgtup.github.io/telegram-bots/#service","name":"Разработка Telegram-ботов на заказ"'
if service_new not in html:
    if service_old not in html:
        raise SystemExit("stage21: Telegram Service schema marker not found")
    html = html.replace(service_old, service_new, 1)

webpage_schema = r'''<script type="application/ld+json" data-stage21-entity="true">{"@context":"https://schema.org","@type":"WebPage","@id":"https://alexgtup.github.io/telegram-bots/#webpage","url":"https://alexgtup.github.io/telegram-bots/","name":"Разработка Telegram-ботов на заказ — API, CRM, оплаты | Alexuys","inLanguage":"ru-RU","isPartOf":{"@id":"https://alexgtup.github.io/#website"},"about":{"@id":"https://alexgtup.github.io/#person"},"mainEntity":{"@id":"https://alexgtup.github.io/telegram-bots/#service"},"significantLink":["https://alexgtup.github.io/cases/fin-planner/","https://alexgtup.github.io/guides/telegram-bot-cost/","https://alexgtup.github.io/guides/telegram-bot-brief/","https://alexgtup.github.io/guides/bot-vs-mini-app-vs-web/"]}</script>'''
if 'data-stage21-entity="true"' not in html:
    if "</head>" not in html:
        raise SystemExit("stage21: </head> not found in telegram-bots/index.html")
    html = html.replace("</head>", webpage_schema + "\n</head>", 1)

write(target, html)
changed.append("/telegram-bots/")

# 2) Add a visible trust block to the developer profile. It uses only verifiable
#    destinations and avoids invented testimonials or unverifiable metrics.
target, html = read("about/index.html")
if 'data-stage21-public-proof="true"' not in html:
    marker = '<section class="container cta-box">'
    if marker not in html:
        raise SystemExit("stage21: about CTA marker not found")

    proof_block = r'''
<section class="container section" data-stage21-public-proof="true" aria-labelledby="public-proof-title"><div class="section-head"><div class="kicker" data-nosnippet="">ПУБЛИЧНАЯ ПРОВЕРКА</div><div><h2 id="public-proof-title">Можно проверить <em>вне этого сайта.</em></h2><p>Не опираюсь только на описание на собственной странице: профиль исполнителя, GitHub и рабочий Telegram-кейс открываются отдельно.</p></div></div><div class="stage21-proof-grid"><a class="stage21-proof-card" href="https://freelance.ru/gglalex" rel="me noopener noreferrer" target="_blank"><small>FREELANCE.RU</small><strong>Публичный профиль исполнителя</strong><span>Отзывы, выполненные задания, портфолио и история профиля на независимой площадке.</span><b>Открыть профиль ↗</b></a><a class="stage21-proof-card" href="https://github.com/Alexgtup/alexgtup.github.io" rel="me noopener noreferrer" target="_blank"><small>GITHUB</small><strong>Репозиторий портфолио</strong><span>Публичная история разработки сайта, кейсов, SEO-изменений и технических проверок.</span><b>Открыть GitHub ↗</b></a><a class="stage21-proof-card" href="/cases/fin-planner/"><small>TELEGRAM CASE</small><strong>Фин Планер</strong><span>Отдельный кейс Telegram-продукта с реальным интерфейсом, сценарием и описанием функций.</span><b>Посмотреть кейс ↗</b></a></div></section>
'''
    html = html.replace(marker, proof_block + marker, 1)

    style = r'''<style data-stage21-public-proof-style="true">.stage21-proof-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.75rem}.stage21-proof-card{min-width:0;display:flex;flex-direction:column;min-height:13.5rem;padding:1.15rem;border:1px solid var(--line);border-radius:1.1rem;background:linear-gradient(145deg,#11161c,#0c1015);text-decoration:none;transition:transform .18s ease,border-color .18s ease,background .18s ease}.stage21-proof-card:hover{transform:translateY(-2px);border-color:var(--line2);background:linear-gradient(145deg,#131920,#0d1116)}.stage21-proof-card small{color:#747e88;font:750 .6rem/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.05em}.stage21-proof-card strong{display:block;margin:1.7rem 0 .55rem;font-size:1.08rem;letter-spacing:-.02em}.stage21-proof-card span{color:#8f98a2;font-size:.8rem;line-height:1.6}.stage21-proof-card b{margin-top:auto;padding-top:1rem;color:#c7cdd3;font-size:.76rem}@media(max-width:820px){.stage21-proof-grid{grid-template-columns:1fr}}@media(max-width:560px){body[data-page="about"] .cta-box{grid-template-columns:1fr}.actions{min-width:0}}</style>'''
    if "</head>" not in html:
        raise SystemExit("stage21: </head> not found in about/index.html")
    html = html.replace("</head>", style + "\n</head>", 1)
    write(target, html)
    changed.append("/about/")

print("stage21 patched:", ", ".join(changed) if changed else "already applied")
