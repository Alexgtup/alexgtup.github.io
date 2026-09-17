#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
REVIEWS = 18
PROFESSIONALISM = 10
COMMUNICATION = 9
CLAIMS = 0
REVIEWS_URL = "https://freelance.ru/reviews/gglalex/"
TELEGRAM = "https://t.me/Alexuys"
BASE = "https://alexgtup.github.io"
TODAY = "2026-09-18"

STYLE = r'''<style id="stage177-conversion-trust">
.s177-conversion{background:#f2efe8;color:#171914;border-top:1px solid rgba(27,31,25,.1);border-bottom:1px solid rgba(27,31,25,.12)}
.s177-shell{width:min(1320px,calc(100% - 64px));margin:0 auto;padding:clamp(30px,3.5vw,48px) 0}
.s177-grid{display:grid;grid-template-columns:1.05fr 1.25fr 1fr 1fr;border-top:1px solid rgba(27,31,25,.14)}
.s177-card{min-width:0;padding:clamp(22px,2.3vw,32px) clamp(18px,2.2vw,30px);border-right:1px solid rgba(27,31,25,.14);text-decoration:none!important;color:#171914!important;background:transparent}
.s177-card:first-child{padding-left:0}.s177-card:last-child{padding-right:0;border-right:0}
.s177-kicker{display:block;margin:0 0 12px;color:#6d746a;font:700 10px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.14em;text-transform:uppercase}
.s177-card strong{display:block;color:#171914;font-size:clamp(19px,1.65vw,26px);line-height:1.05;letter-spacing:-.035em}
.s177-card p,.s177-card span{display:block;margin:10px 0 0;color:#555c53;font-size:13px;line-height:1.6}
.s177-card blockquote{margin:0;color:#262a24;font-size:15px;line-height:1.55}
.s177-review-meta{margin-top:10px!important;color:#737a70!important;font-size:11px!important}
.s177-cta{display:flex;flex-direction:column;justify-content:space-between;gap:18px}
.s177-cta b{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:11px 15px;border-radius:999px;background:#171914;color:#fff;font-size:13px;line-height:1.2}
@media(hover:hover) and (pointer:fine){.s177-card[href]:hover strong{color:#496600}.s177-cta:hover b{background:#314207}}
@media(max-width:980px){.s177-shell{width:min(100% - 32px,900px)}.s177-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.s177-card{border-bottom:1px solid rgba(27,31,25,.14)}.s177-card:nth-child(2){border-right:0}.s177-card:nth-last-child(-n+2){border-bottom:0}.s177-card:first-child{padding-left:22px}.s177-card:last-child{padding-right:22px}}
@media(max-width:620px){.s177-shell{width:calc(100% - 24px);padding:24px 0}.s177-grid{grid-template-columns:1fr}.s177-card{padding:20px 4px!important;border-right:0;border-bottom:1px solid rgba(27,31,25,.14)!important}.s177-card:last-child{border-bottom:0!important}}
</style>'''

PAGES = {
    "project-repair": {
        "quote": "Задачу понял сразу, задал нужные вопросы, всё сдал быстро. Рекомендую.",
        "author": "Иван · 15.05.2026",
        "proof_href": "/cases/taxi-app/",
        "proof_kicker": "RELATED CASE",
        "proof_title": "Приложение такси",
        "proof_text": "Пример продолжения уже существующего мобильного продукта.",
        "step": "Пришлите ссылку, ошибку или коротко опишите, что должно заработать.",
        "cta": "Прислать ссылку или ошибку ↗",
    },
    "wordpress-development": {
        "quote": "Отличный специалист, вник в суть, оперативно помог.",
        "author": "Ева Григорова · WordPress · 04.09.2026",
        "proof_href": REVIEWS_URL,
        "proof_kicker": "WORDPRESS PROOF",
        "proof_title": "Свежие отзывы по WordPress",
        "proof_text": "Отзывы за WordPress-задачи опубликованы 04.09 и 16.07.2026.",
        "step": "Достаточно URL сайта и пары предложений о нужной правке.",
        "cta": "Прислать ссылку на WordPress ↗",
    },
    "telegram-bots": {
        "quote": "К задаче приступил моментально, исполнил быстро и без задержек.",
        "author": "Артём · Telegram-бот · 02.10.2025",
        "proof_href": "/cases/fin-planner/",
        "proof_kicker": "REAL TELEGRAM WORK",
        "proof_title": "Fin Planner",
        "proof_text": "Telegram-продукт с данными, отчётами и backend-логикой.",
        "step": "Для старта хватит одного сценария: вход → действие → результат.",
        "cta": "Описать сценарий бота ↗",
    },
    "web-development": {
        "quote": "Получил хороший результат!",
        "author": "Александр Займатов · сайт · 16.07.2026",
        "proof_href": "/cases/factory-catalog/",
        "proof_kicker": "REAL WEB WORK",
        "proof_title": "B2B-каталог производства",
        "proof_text": "Структура каталога, выбор продукции и путь до заявки.",
        "step": "Можно прислать ссылку, Figma или просто описать основной путь пользователя.",
        "cta": "Прислать ссылку или макет ↗",
    },
    "n8n-automation": {
        "quote": "Отличный специалист, вник в суть, оперативно помог.",
        "author": "Ева Григорова · 04.09.2026",
        "proof_href": "/cases/seo-control-center/",
        "proof_kicker": "RELATED WORK",
        "proof_title": "SEO Control Center",
        "proof_text": "Работа с данными, мониторингом и автоматизированными проверками.",
        "step": "Опишите одно ручное действие: откуда приходят данные и куда должны уйти.",
        "cta": "Описать ручной процесс ↗",
    },
}

def sync_reputation(text: str) -> str:
    replacements = [
        (r'<strong>(?:17|18|20)</strong><span>публичных отзывов</span>', f'<strong>{REVIEWS}</strong><span>публичных отзывов</span>'),
        (r'<strong>(?:17|18|20)</strong><span>отзывов в открытом профиле</span>', f'<strong>{REVIEWS}</strong><span>отзывов в открытом профиле</span>'),
        (r'<strong>(?:17|18|20) отзывов</strong><span>в публичном профиле Freelance\.ru</span>', f'<strong>{REVIEWS} отзывов</strong><span>в публичном профиле Freelance.ru</span>'),
        (r'<strong>(?:17|18|20) отзывов · 10/10</strong>', f'<strong>{REVIEWS} отзывов · 10/10</strong>'),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text

def proof_link(cfg: dict) -> str:
    href = cfg["proof_href"]
    external = href.startswith("http")
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ""
    return (
        f'<a class="s177-card" href="{html.escape(href)}"{attrs}>'
        f'<small class="s177-kicker">{html.escape(cfg["proof_kicker"])}</small>'
        f'<strong>{html.escape(cfg["proof_title"])}</strong>'
        f'<span>{html.escape(cfg["proof_text"])}</span></a>'
    )

def block(cfg: dict) -> str:
    return (
        '<section class="s177-conversion" data-stage177-conversion="true" aria-label="Проверяемый опыт и следующий шаг">'
        '<div class="s177-shell"><div class="s177-grid">'
        f'<a class="s177-card" href="{REVIEWS_URL}" target="_blank" rel="noopener noreferrer">'
        '<small class="s177-kicker">FREELANCE.RU</small>'
        f'<strong>{REVIEWS} отзывов · {CLAIMS} претензий</strong>'
        f'<span>{PROFESSIONALISM}/10 профессионализм · {COMMUNICATION}/10 коммуникация</span></a>'
        '<a class="s177-card" href="' + REVIEWS_URL + '" target="_blank" rel="noopener noreferrer">'
        '<small class="s177-kicker">CLIENT REVIEW</small>'
        f'<blockquote>«{html.escape(cfg["quote"])}»</blockquote>'
        f'<span class="s177-review-meta">{html.escape(cfg["author"])}</span></a>'
        + proof_link(cfg) +
        f'<a class="s177-card s177-cta" href="{TELEGRAM}" target="_blank" rel="noopener noreferrer">'
        '<div><small class="s177-kicker">FIRST STEP</small>'
        f'<strong>Без большого ТЗ.</strong><p>{html.escape(cfg["step"])}</p></div>'
        f'<b>{html.escape(cfg["cta"])}</b></a>'
        '</div></div></section>'
    )

# Final source-of-truth pass for reputation facts on the main trust surfaces.
for rel in ("index.html", "about/index.html", "freelance-developer/index.html"):
    fp = ROOT / rel
    if not fp.is_file():
        raise SystemExit(f"stage177: missing reputation page {rel}")
    text = sync_reputation(fp.read_text(encoding="utf-8"))
    fp.write_text(text, encoding="utf-8")

changed = 0
for slug, cfg in PAGES.items():
    fp = ROOT / slug / "index.html"
    if not fp.is_file():
        raise SystemExit(f"stage177: missing service page {slug}")
    text = fp.read_text(encoding="utf-8")
    text = sync_reputation(text)
    text = re.sub(r'<style\s+id=["\']stage177-conversion-trust["\']>.*?</style>', '', text, flags=re.I | re.S)
    text = re.sub(r'\s*<section\b[^>]*data-stage177-conversion="true"[^>]*>.*?</section>\s*', '\n', text, count=1, flags=re.I | re.S)
    if "</head>" not in text:
        raise SystemExit(f"stage177: head missing {slug}")
    text = text.replace("</head>", STYLE + "</head>", 1)
    hero = re.search(r'<section\b[^>]*class=["\'][^"\']*p129-svc-hero[^"\']*["\'][^>]*>.*?</section>', text, flags=re.I | re.S)
    if not hero and slug == "wordpress-development":
        hero = re.search(r'<section\b[^>]*class=["\']container hero["\'][^>]*>.*?</section>', text, flags=re.I | re.S)
    if not hero:
        raise SystemExit(f"stage177: service hero missing {slug}")
    text = text[:hero.end()] + block(cfg) + text[hero.end():]
    fp.write_text(text, encoding="utf-8")
    changed += 1

for slug in PAGES:
    text = (ROOT / slug / "index.html").read_text(encoding="utf-8")
    if text.count('data-stage177-conversion="true"') != 1:
        raise SystemExit(f"stage177: conversion block count invalid {slug}")
    for token in (f"{REVIEWS} отзывов", f"{PROFESSIONALISM}/10", f"{COMMUNICATION}/10", f"{CLAIMS} претензий"):
        if token not in text:
            raise SystemExit(f"stage177: missing {token} on {slug}")

for rel in ("index.html", "about/index.html", "freelance-developer/index.html"):
    text = (ROOT / rel).read_text(encoding="utf-8")
    if "17 отзывов" in text or ">17</strong><span>публичных отзывов" in text:
        raise SystemExit(f"stage177: stale 17-review fact on {rel}")

# Mark the pages changed by this final conversion/reputation pass as fresh for crawlers.
routes = ["/", "/about/", "/freelance-developer/"] + [f"/{slug}/" for slug in PAGES]
for sitemap_name in ("sitemap.xml", "sitemap-google.xml"):
    sitemap = ROOT / sitemap_name
    if not sitemap.is_file():
        continue
    xml = sitemap.read_text(encoding="utf-8")
    touched = 0
    for route in routes:
        url = BASE + route
        pattern = r'(<loc>' + re.escape(url) + r'</loc>\\s*<lastmod>)[^<]+'
        xml, n = re.subn(pattern, r'\\g<1>' + TODAY, xml, count=1)
        touched += n
    if sitemap_name == "sitemap.xml" and touched != len(routes):
        raise SystemExit(f"stage177: sitemap freshness mismatch {touched}/{len(routes)}")
    sitemap.write_text(xml, encoding="utf-8")

print(f"stage177 conversion trust: service_pages={changed}; reviews={REVIEWS}; claims={CLAIMS}")
