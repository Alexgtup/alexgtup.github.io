#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')

HOME_CARD = '''\n<a class="s44-case s44-case--visual s44-case--sheetpilot" href="/cases/sheetpilot-ai/">\n  <div class="s44-case__image"><img src="/assets/cases/sheetpilot-ai/sheetpilot-01.svg" width="1440" height="1080" loading="lazy" decoding="async" alt="SheetPilot AI — ИИ-ассистент для обработки Excel-файлов"/></div>\n  <div class="s44-case__body"><span>AI · EXCEL · FULLSTACK</span><h3>SheetPilot AI</h3><p>Рабочий MVP для обработки Excel обычным языком: загрузка XLSX, ограниченный план изменений, предпросмотр результата и экспорт нового файла.</p><b>Открыть полный кейс ↗</b></div>\n</a>\n'''

CASES_CARD = '''\n<a class="visual sp-sheetpilot-case" href="/cases/sheetpilot-ai/"><img src="/assets/cases/sheetpilot-ai/sheetpilot-01.svg" width="1440" height="1080" loading="lazy" decoding="async" alt="Интерфейс SheetPilot AI для обработки Excel"/><div><span>AI · EXCEL · FULLSTACK</span><h3>SheetPilot AI</h3><p>Excel-ассистент: команда обычным языком, безопасный preview изменений и экспорт нового файла.</p><b>Открыть кейс ↗</b></div></a>\n'''


def patch(path: Path, marker: str, unique: str, card: str, count_old: str, count_new: str) -> None:
    if not path.is_file():
        raise SystemExit(f'stage59: page missing: {path}')
    text = path.read_text(encoding='utf-8')
    if unique not in text:
        if marker not in text:
            raise SystemExit(f'stage59: grid marker missing: {path}')
        text = text.replace(marker, marker + card, 1)
    text = text.replace(count_old, count_new, 1)
    if unique not in text:
        raise SystemExit(f'stage59: SheetPilot card insertion failed: {path}')
    path.write_text(text, encoding='utf-8')


patch(
    root / 'index.html',
    '<div class="s44-case-grid">',
    '<a class="s44-case s44-case--visual s44-case--sheetpilot" href="/cases/sheetpilot-ai/">',
    HOME_CARD,
    '<strong>5</strong><span>подробных кейсов на сайте</span>',
    '<strong>6</strong><span>подробных кейсов на сайте</span>',
)
patch(
    root / 'cases' / 'index.html',
    '<div class="s50-case-list">',
    '<a class="visual sp-sheetpilot-case" href="/cases/sheetpilot-ai/">',
    CASES_CARD,
    '<strong>5</strong><span>подробных кейсов</span>',
    '<strong>6</strong><span>подробных кейсов</span>',
)

print('stage59: SheetPilot AI is present inside both existing project grids')
