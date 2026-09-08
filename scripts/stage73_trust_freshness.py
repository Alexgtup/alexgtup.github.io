#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")


def read(rel):
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"missing {path}")
    return path, path.read_text(encoding="utf-8")


def save(path, text):
    path.write_text(text, encoding="utf-8")

# Homepage: keep independently verifiable trust links, not marketplace counters that become stale.
p, home = read("index.html")
home_pairs = [
    ('<strong>20</strong><span>публичных отзывов на Freelance.ru</span>', '<strong>Отзывы</strong><span>публично на Freelance.ru</span>'),
    ('<strong>9 / 10</strong><span>профессионализм и коммуникация</span>', '<strong>Задания</strong><span>история выполненных работ</span>'),
    ('<strong>6 лет</strong><span>опыта в публичном профиле</span>', '<strong>2023</strong><span>профиль на площадке</span>'),
    ('<strong>9</strong><span>подробных кейсов на сайте</span>', '<strong>Кейсы</strong><span>проекты и рабочие продукты</span>'),
]
for old, new in home_pairs:
    if old in home:
        home = home.replace(old, new)
    elif new not in home:
        raise SystemExit(f"Stage73 homepage fact marker changed: {old}")
old_trust = 'Публичный профиль Freelance.ru можно открыть до обращения: 20 отзывов, оценки 9/10 по профессионализму и коммуникации, 6 лет опыта в профиле. В профиле доступны отзывы заказчиков и история работы на площадке.'
new_trust = 'Публичный профиль Freelance.ru можно открыть до обращения. В профиле доступны отзывы заказчиков, оценки и история выполненных работ на независимой площадке.'
if old_trust in home:
    home = home.replace(old_trust, new_trust)
elif new_trust not in home:
    raise SystemExit("Stage73 homepage trust copy marker changed")
home = home.replace('<strong>от 5 000 ₽</strong><h3>Доработка / исправление</h3>', '<strong>от 10 000 ₽</strong><h3>Доработка / исправление</h3>')
save(p, home)

# Services hub: remove stale counters and keep packaged project-repair entry consistent.
p, services = read("services/index.html")
old_services_proof = '<div class="s44-proofline s44-proofline--services"><a href="https://freelance.ru/gglalex" rel="me noopener noreferrer" target="_blank"><strong>20</strong><span>публичных отзывов</span></a><div><strong>6 лет</strong><span>опыта в профиле</span></div><a href="/cases/"><strong>5</strong><span>подробных кейсов</span></a><a href="/project-repair/"><strong>от 5 000 ₽</strong><span>небольшая доработка</span></a></div>'
new_services_proof = '<div class="s44-proofline s44-proofline--services"><a href="https://freelance.ru/gglalex" rel="me noopener noreferrer" target="_blank"><strong>Отзывы</strong><span>публично на Freelance.ru</span></a><div><strong>2023</strong><span>профиль на площадке</span></div><a href="/cases/"><strong>Кейсы</strong><span>проекты и рабочие продукты</span></a><a href="/project-repair/"><strong>от 10 000 ₽</strong><span>доработка проекта</span></a></div>'
if old_services_proof in services:
    services = services.replace(old_services_proof, new_services_proof)
elif new_services_proof not in services:
    raise SystemExit("Stage73 services proofline marker changed")
services = services.replace('<a class="s44-service-map__item s44-service-map__item--repair" href="/project-repair/"><span>06 · EXISTING PROJECT</span><h2>Доработка чужого или незавершённого проекта</h2><p>Ошибка, форма, адаптив, интеграция, новый функционал, старый код или проект, который нужно довести до релиза.</p><div><b>от 5 000 ₽</b>', '<a class="s44-service-map__item s44-service-map__item--repair" href="/project-repair/"><span>06 · EXISTING PROJECT</span><h2>Доработка чужого или незавершённого проекта</h2><p>Ошибка, форма, адаптив, интеграция, новый функционал, старый код или проект, который нужно довести до релиза.</p><div><b>от 10 000 ₽</b>')
save(p, services)

# Packaged minimum for repair is now 10k; synchronize the canonical repair landing.
p, repair = read("project-repair/index.html")
repair = repair.replace('от 5 000 ₽', 'от 10 000 ₽')
repair = repair.replace('от 5 000 руб.', 'от 10 000 руб.')
repair = repair.replace('"price":"5000"', '"price":"10000"')
repair = repair.replace('Оценка до старта, 20 отзывов · оценки 9/9.', 'Оценка до старта; отзывы и история работ доступны в публичном профиле Freelance.ru.')
save(p, repair)

# General small-task entry pages must not contradict the packaged repair minimum.
for rel in ["development/index.html", "web-development/index.html"]:
    p, text = read(rel)
    text = text.replace('от 5 000 ₽', 'от 10 000 ₽')
    text = text.replace('от 5 000 руб.', 'от 10 000 руб.')
    save(p, text)

# Telegram Service schema: keep reputation verifiable through links, not embedded counters.
p, telegram = read("telegram-bots/index.html")
telegram = telegram.replace('Исходники и доступы, 20 отзывов · оценки 9/9.', 'Исходники и доступы; отзывы и история работ доступны в публичном профиле Freelance.ru.')
save(p, telegram)

# Final generated-output invariant. Scope numeric marketplace claims to pages that previously leaked them.
forbidden = {
    "index.html": ["6 лет", "9 / 10", "оценки 9/10", "20 отзывов", "20</strong><span>публичных отзывов", "<strong>9</strong><span>подробных кейсов"],
    "services/index.html": ["6 лет", "<strong>20</strong><span>публичных отзывов", "<strong>5</strong><span>подробных кейсов", "от 5 000 ₽"],
    "telegram-bots/index.html": ["20 отзывов · оценки 9/9", "оценки 9/9"],
    "project-repair/index.html": ["20 отзывов · оценки 9/9", "оценки 9/9", "от 5 000 ₽", "от 5 000 руб.", '"price":"5000"'],
    "development/index.html": ["от 5 000 ₽"],
    "web-development/index.html": ["от 5 000 ₽", "от 5 000 руб."],
}
errors = []
for rel, phrases in forbidden.items():
    _, text = read(rel)
    for phrase in phrases:
        if phrase in text:
            errors.append(f"{rel}: stale claim remains: {phrase}")

# Positive invariants prove the final public facts/offers are still present.
positive = {
    "index.html": ["<strong>Отзывы</strong>", "<strong>Задания</strong>", "<strong>2023</strong>", "<strong>Кейсы</strong>"],
    "freelance-developer/index.html": ['data-freelance-offers="v2"', 'data-offer="project_repair"', 'data-offer="telegram_bot"', 'data-offer="n8n"', 'data-offer="api_integration"', 'data-offer="seo_audit"'],
    "project-repair/index.html": ["от 10 000 ₽", '"price":"10000"'],
}
for rel, phrases in positive.items():
    _, text = read(rel)
    for phrase in phrases:
        if phrase not in text:
            errors.append(f"{rel}: required freshness invariant missing: {phrase}")

if errors:
    raise SystemExit("Stage73 trust freshness failed:\n- " + "\n- ".join(errors))

print("Stage73 trust freshness: OK; stale marketplace counters removed, repair minimum synchronized")
