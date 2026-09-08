#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

PROOFS = {
    "/n8n-automation/": {
        "marker": "n8n-seo-control-center",
        "href": "/cases/seo-control-center/",
        "image": "/assets/cases/seo-control-center/seo-control-center-card-01.svg",
        "meta": "N8N · SEO · FULLSTACK",
        "name": "SEO Control Center",
        "body": "В этом проекте n8n не используется как декоративная схема: workflows оркестрируют расписания, синхронизацию данных, запуск crawler, детектор SEO-событий, уведомления, digest и health-monitor. Данные сохраняются в PostgreSQL, а dashboard читает их через backend/API.",
        "alt": "SEO Control Center — проект с n8n workflows для мониторинга SEO и индексации",
        "related": [
            ("/guides/n8n-vs-make/", "n8n или Make"),
            ("/api-integrations/", "API-интеграции"),
            ("/telegram-bots/", "Telegram в автоматизации"),
        ],
    },
    "/python-development/": {
        "marker": "python-sheetpilot",
        "href": "/cases/sheetpilot-ai/",
        "image": "/assets/cases/sheetpilot-ai/sheetpilot-01.svg",
        "meta": "PYTHON · FASTAPI · OPENPYXL",
        "name": "SheetPilot AI",
        "body": "Рабочий Python/FastAPI MVP для обработки XLSX: файл загружается в сервис, команда преобразуется в ограниченный план операций, изменения показываются до сохранения, а новый Excel-файл формируется через openpyxl без перезаписи исходника.",
        "alt": "SheetPilot AI — Python и FastAPI сервис для обработки Excel-файлов",
        "related": [
            ("/backend-development/", "Backend-разработка"),
            ("/api-integrations/", "API-интеграции"),
            ("/n8n-automation/", "Автоматизация процессов"),
        ],
    },
}

GENERIC_PROOF = re.compile(
    r'<section class="s48-section s48-proof" aria-labelledby="s48-proof-title">.*?</section>',
    re.S,
)


def page(route: str) -> Path:
    return root / route.strip("/") / "index.html"


def render(d: dict) -> str:
    related = "".join(
        f'<a href="{href}"><span>Связанный материал</span><b>{label}</b></a>'
        for href, label in d["related"]
    )
    return f'''<section class="s48-section s48-proof" data-stage74-proof="{d['marker']}" aria-labelledby="s74-proof-title-{d['marker']}"><div class="container"><div class="s48-head"><span class="s48-index">03 / ДОКАЗАТЕЛЬСТВО</span><div><h2 id="s74-proof-title-{d['marker']}">Не общий список технологий. <em>Есть проект, где этот стек работает.</em></h2><p>Связанный кейс показывает конкретную архитектуру и рабочий сценарий отдельно от продающего текста этой страницы.</p></div></div><a class="s48-case" href="{d['href']}"><div class="s48-case__image"><img src="{d['image']}" alt="{d['alt']}" loading="lazy" decoding="async"/></div><div class="s48-case__body"><span>{d['meta']}</span><h3>{d['name']}</h3><p>{d['body']}</p><b>Открыть полный кейс ↗</b></div></a><div class="s48-related">{related}</div></div></section>'''


changed = []
for route, data in PROOFS.items():
    p = page(route)
    if not p.is_file():
        raise SystemExit(f"stage74: missing page: {p}")
    text = p.read_text(encoding="utf-8")
    marker = f'data-stage74-proof="{data["marker"]}"'
    if marker not in text:
        text, count = GENERIC_PROOF.subn(render(data), text, count=1)
        if count != 1:
            raise SystemExit(f"stage74: generic proof block not found exactly once: {route}")
        p.write_text(text, encoding="utf-8")
        changed.append(route)

    final = p.read_text(encoding="utf-8")
    for required in (marker, f'href="{data["href"]}"', data["name"], data["meta"]):
        if required not in final:
            raise SystemExit(f"stage74: proof invariant failed for {route}: {required}")
    if "Не выдаю смежный проект" in final:
        raise SystemExit(f"stage74: stale generic proof remains on {route}")

# Content really changed on these two URLs, so keep their lastmod honest without
# regenerating or restructuring the sitemap.
sitemap = root / "sitemap.xml"
if not sitemap.is_file():
    raise SystemExit("stage74: sitemap.xml missing")
sitemap_text = sitemap.read_text(encoding="utf-8")
for route in PROOFS:
    url = f"https://alexgtup.github.io{route}"
    pattern = re.compile(rf'(<loc>{re.escape(url)}</loc>\s*<lastmod>)[^<]+(</lastmod>)')
    sitemap_text, count = pattern.subn(r'\g<1>2026-09-09\g<2>', sitemap_text, count=1)
    if count != 1:
        raise SystemExit(f"stage74: sitemap lastmod marker missing for {url}")
sitemap.write_text(sitemap_text, encoding="utf-8")

print(f"stage74: differentiated real proof on {len(PROOFS)} money pages; changed={changed}")
