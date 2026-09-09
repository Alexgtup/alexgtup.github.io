#!/usr/bin/env python3
from pathlib import Path
import html as htmlmod
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')


def main_bounds(text: str):
    start = re.search(r'<main\b[^>]*>', text, re.I)
    if not start:
        return None
    end = re.search(r'</main>', text[start.end():], re.I)
    if not end:
        return None
    return start.start(), start.end(), start.end() + end.start(), start.end() + end.end()


def top_sections(text: str):
    bounds = main_bounds(text)
    if not bounds:
        return []
    _, ms, me, _ = bounds
    frag = text[ms:me]
    tokens = re.compile(r'<section\b[^>]*>|</section\s*>', re.I)
    depth = 0
    start = None
    out = []
    for m in tokens.finditer(frag):
        tok = m.group(0)
        if tok.lower().startswith('<section'):
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0 and start is not None:
                full = frag[start:m.end()]
                hm = re.search(r'<h[12]\b[^>]*>(.*?)</h[12]>', full, re.I | re.S)
                heading = ''
                if hm:
                    heading = re.sub(r'<[^>]+>', ' ', hm.group(1))
                    heading = re.sub(r'\s+', ' ', htmlmod.unescape(heading)).strip()
                out.append({'start': ms + start, 'end': ms + m.end(), 'html': full, 'heading': heading})
                start = None
    return out


def remove_matching(text: str, headings=(), contains=()):
    while True:
        hit = None
        for section in top_sections(text):
            if any(section['heading'].startswith(h) for h in headings) or any(c in section['html'] for c in contains):
                hit = section
                break
        if not hit:
            return text
        text = text[:hit['start']] + text[hit['end']:]


# The three legacy cases should read like portfolio cases, not SEO landing pages.
# Keep context + implemented workflow, remove generic advice/navigation sections.
LEGACY = ('auto-crm', 'factory-catalog', 'taxi-app')
legacy_remove = (
    'Что учесть в похожем проекте.',
    'Какой тип разработки стоит за этим проектом.',
)

rules = {
    'auto-crm': dict(headings=legacy_remove, contains=('Своя CRM или готовое решение →',)),
    'factory-catalog': dict(headings=legacy_remove, contains=()),
    'taxi-app': dict(headings=legacy_remove, contains=()),
    'fin-planner': dict(headings=('Telegram может быть полноценным продуктом.',), contains=()),
    # SheetPilot has distinct task/interface/execution/MVP/stack sections; keep the technical depth.
    'sheetpilot-ai': dict(headings=(), contains=()),
    'swift-calendar': dict(headings=('Мобильная разработка с продуктовой логикой.',), contains=()),
}

changed = 0
report = []
errors = []
for slug, rule in rules.items():
    path = root / 'cases' / slug / 'index.html'
    if not path.exists():
        errors.append(f'missing case {slug}')
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    before = len(top_sections(text))

    if slug in LEGACY:
        text = text.replace('Что в этом кейсе действительно подтверждается.', 'Что реализовано.')
        text = text.replace('Ниже — реализованные функции и их роль в пользовательском сценарии.', 'Ключевые части рабочего сценария и их роль в системе.')

    new = remove_matching(text, rule['headings'], rule['contains'])
    after = len(top_sections(new))
    if new != path.read_text(encoding='utf-8', errors='ignore'):
        path.write_text(new, encoding='utf-8')
        changed += 1
    report.append((slug, before, after))

expected_max = {
    'auto-crm': 4,
    'factory-catalog': 4,
    'taxi-app': 4,
    'fin-planner': 6,
    'sheetpilot-ai': 7,
    'swift-calendar': 4,
}
for slug, _, after in report:
    if after > expected_max[slug]:
        errors.append(f'{slug}: still {after} top-level sections, expected <= {expected_max[slug]}')

for slug in LEGACY:
    path = root / 'cases' / slug / 'index.html'
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    for phrase in ('Что учесть в похожем проекте.', 'Какой тип разработки стоит за этим проектом.', 'Что в этом кейсе действительно подтверждается.'):
        if phrase in text:
            errors.append(f'{slug}: generic legacy section remains: {phrase}')
    if 'Что реализовано.' not in text:
        errors.append(f'{slug}: implemented section was lost')

if errors:
    raise SystemExit('stage98 case polish failed:\n' + '\n'.join(errors))

print('stage98 case polish: ' + ', '.join(f'{s} {b}->{a}' for s, b, a in report) + f'; changed={changed}')
