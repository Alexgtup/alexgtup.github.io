#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

PROFILE = "https://freelance.ru/gglalex"
REVIEWS = "https://freelance.ru/reviews/gglalex/"


def path_for(route: str) -> Path:
    return root / ("index.html" if route == "/" else route.strip("/") + "/index.html")


def insert_before_conversion(route: str, block: str) -> bool:
    path = path_for(route)
    if not path.is_file():
        raise SystemExit(f"stage40: missing route {route}: {path}")
    html = path.read_text(encoding="utf-8")
    if 'data-stage40-trust="true"' in html:
        return False

    markers = (
        '<section class="contact">',
        '<section class="contact"',
        '<section aria-labelledby="brief-title"',
        '</main>',
    )
    marker = next((m for m in markers if m in html), None)
    if not marker:
        raise SystemExit(f"stage40: conversion marker not found: {route}")
    html = html.replace(marker, block + "\n" + marker, 1)
    path.write_text(html, encoding="utf-8")
    return True


full_trust = f'''
<section class="verified-trust verified-trust--full" data-stage40-trust="true" aria-labelledby="verified-trust-title">
  <div class="container">
    <div class="verified-trust__head">
      <div class="verified-trust__label" data-nosnippet="">Проверяемая репутация</div>
      <div>
        <h2 id="verified-trust-title">Не нужно верить портфолио <em>на слово.</em></h2>
        <p>Отзывы и история выполненных заданий находятся на независимой площадке Freelance.ru. Сайт не скрывает внешний профиль: его можно открыть до обращения и самостоятельно посмотреть проекты, оценки и отзывы заказчиков.</p>
      </div>
    </div>
    <div class="verified-trust__stats" aria-label="Публичная история Freelance.ru">
      <a href="{PROFILE}" rel="me noopener noreferrer" target="_blank"><strong>20+</strong><span>отзывов в публичном профиле</span></a>
      <a href="{PROFILE}" rel="me noopener noreferrer" target="_blank"><strong>20+</strong><span>выполненных заданий на площадке</span></a>
      <a href="{REVIEWS}" rel="noopener noreferrer" target="_blank"><strong>2023–2026</strong><span>публичная история отзывов по разным задачам</span></a>
    </div>
    <div class="verified-trust__reviews">
      <article><blockquote>«Работа выполнена на 100%.»</blockquote><p>Проверка кода сайта и запуск · апрель 2026</p></article>
      <article><blockquote>«Есть поддержка проекта после релиза.»</blockquote><p>Разработка приложения · апрель 2026</p></article>
      <article><blockquote>«Правки вносит оперативно.»</blockquote><p>Telegram-бот · октябрь 2025</p></article>
    </div>
    <div class="verified-trust__actions">
      <a class="button primary" href="{REVIEWS}" rel="noopener noreferrer" target="_blank">Проверить отзывы на Freelance.ru ↗</a>
      <a class="button" href="/cases/">Посмотреть реальные кейсы</a>
    </div>
    <p class="verified-trust__note">Если удобнее сначала проверить исполнителя на внешней площадке — начните с профиля, а уже потом переходите к обсуждению задачи.</p>
  </div>
</section>
'''

compact_trust = f'''
<section class="verified-trust verified-trust--compact" data-stage40-trust="true" aria-label="Проверяемая репутация на Freelance.ru">
  <div class="container">
    <div class="verified-trust__compact-card">
      <div><span class="verified-trust__label" data-nosnippet="">Внешнее подтверждение</span><h2>Отзывы и история работ — <em>на Freelance.ru.</em></h2><p>20+ отзывов и 20+ выполненных заданий доступны на независимой площадке. Можно проверить профиль до того, как писать или заказывать разработку.</p></div>
      <div class="verified-trust__compact-actions"><a class="button primary" href="{PROFILE}" rel="me noopener noreferrer" target="_blank">Открыть профиль ↗</a><a class="button" href="{REVIEWS}" rel="noopener noreferrer" target="_blank">Отзывы ↗</a></div>
    </div>
  </div>
</section>
'''

changed = []
if insert_before_conversion("/", full_trust):
    changed.append("/")

for route in (
    "/telegram-bots/",
    "/project-repair/",
    "/n8n-automation/",
    "/ai-automation/",
    "/api-integrations/",
    "/web-development/",
    "/services/",
):
    if insert_before_conversion(route, compact_trust):
        changed.append(route)

css = root / "assets" / "site-enhancements.css"
if not css.is_file():
    raise SystemExit("stage40: site-enhancements.css missing")
css_text = css.read_text(encoding="utf-8")
if "/* stage40 verified trust */" not in css_text:
    css_text += r'''

/* stage40 verified trust */
.verified-trust{padding:clamp(4.2rem,8vw,7.2rem) 0;border-top:1px solid rgba(255,255,255,.09)}
.verified-trust .container{width:min(100%,86rem);margin-inline:auto;padding-inline:clamp(1.1rem,4vw,4.4rem)}
.verified-trust__head{display:grid;grid-template-columns:.34fr 1.66fr;gap:2rem;margin-bottom:1.8rem}.verified-trust__label{font:750 .65rem/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:#7f8993}.verified-trust h2{margin:0;font-size:clamp(2.35rem,4.7vw,4.7rem);line-height:.98;letter-spacing:-.052em;max-width:15ch}.verified-trust h2 em{font-style:normal;color:#969ea7}.verified-trust__head p{max-width:52rem;margin:1rem 0 0;color:#969fa8;line-height:1.72}.verified-trust__stats{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem}.verified-trust__stats a{display:grid;gap:.4rem;padding:1.3rem;border:1px solid rgba(255,255,255,.11);border-radius:1.1rem;background:linear-gradient(145deg,#11151b,#0c0f13);text-decoration:none}.verified-trust__stats strong{font-size:clamp(1.8rem,4vw,3rem);letter-spacing:-.05em}.verified-trust__stats span{color:#8e97a0;font-size:.78rem;line-height:1.45}.verified-trust__reviews{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem;margin-top:.7rem}.verified-trust__reviews article{padding:1.25rem;border:1px solid rgba(255,255,255,.09);border-radius:1.05rem;background:rgba(255,255,255,.018)}.verified-trust__reviews blockquote{margin:0;font-size:1rem;font-weight:800;letter-spacing:-.02em}.verified-trust__reviews p{margin:.7rem 0 0;color:#77818b;font-size:.7rem}.verified-trust__actions{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:1.15rem}.verified-trust__note{margin:.85rem 0 0;color:#747d87;font-size:.72rem;max-width:58rem}.verified-trust__compact-card{display:grid;grid-template-columns:1fr auto;gap:2rem;align-items:center;padding:clamp(1.35rem,3vw,2rem);border:1px solid rgba(255,255,255,.11);border-radius:1.3rem;background:linear-gradient(145deg,#11151b,#0c0f13)}.verified-trust--compact h2{margin:.55rem 0 0;font-size:clamp(1.8rem,3.4vw,3rem);line-height:1;letter-spacing:-.045em;max-width:18ch}.verified-trust--compact p{margin:.8rem 0 0;color:#929aa4;max-width:48rem}.verified-trust__compact-actions{display:flex;gap:.55rem;flex-wrap:wrap;justify-content:flex-end}
@media(max-width:820px){.verified-trust__head,.verified-trust__compact-card{grid-template-columns:1fr}.verified-trust__stats,.verified-trust__reviews{grid-template-columns:1fr}.verified-trust__compact-actions{justify-content:flex-start}}
@media(max-width:560px){.verified-trust{padding:4rem 0}.verified-trust__actions,.verified-trust__compact-actions{display:grid}.verified-trust .button{width:100%}}
'''
    css.write_text(css_text, encoding="utf-8")

print("stage40 trust patched:", ", ".join(changed) if changed else "already applied")
