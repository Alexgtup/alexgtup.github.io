#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
CSS_MARK = 'data-stage92-ux-css="true"'
JS_MARK = 'data-stage92-ux-js="true"'
CSS_LINK = '<link href="/assets/ux-interactions.css?v=20260909-2" rel="stylesheet" data-stage92-ux-css="true"/>'
JS_LINK = '<script defer src="/assets/ux-interactions.js?v=20260909-1" data-stage92-ux-js="true"></script>'
MAIN_OPEN_RE = re.compile(r'<main\b[^>]*>', re.I | re.S)
SECTION_RE = re.compile(r'<section\b[^>]*>.*?</section>', re.I | re.S)


def add_assets(text: str) -> str:
    if CSS_MARK not in text:
        text = text.replace('</head>', CSS_LINK + '\n</head>', 1)
    if JS_MARK not in text:
        text = text.replace('</body>', JS_LINK + '\n</body>', 1)
    return text


def add_main_class(text: str, class_name: str) -> str:
    def repl(m: re.Match[str]) -> str:
        tag = m.group(0)
        cm = re.search(r'class=(["\'])(.*?)\1', tag, re.I | re.S)
        if cm:
            classes = cm.group(2).split()
            if class_name in classes:
                return tag
            classes.append(class_name)
            new_class = f'class={cm.group(1)}{" ".join(classes)}{cm.group(1)}'
            return tag[:cm.start()] + new_class + tag[cm.end():]
        return tag[:-1] + f' class="{class_name}">'
    return MAIN_OPEN_RE.sub(repl, text, count=1)


def add_id_to_opening(tag: str, element_id: str) -> str:
    if re.search(r'\bid=["\']', tag, re.I):
        return tag
    return tag[:-1] + f' id="{element_id}">'


def add_id_first_section_class(text: str, class_name: str, element_id: str, nth: int = 1) -> str:
    pat = re.compile(
        rf'<section\b(?=[^>]*class=["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\'])[^>]*>',
        re.I | re.S,
    )
    matches = list(pat.finditer(text))
    if len(matches) < nth:
        return text
    m = matches[nth - 1]
    tag = add_id_to_opening(m.group(0), element_id)
    return text[:m.start()] + tag + text[m.end():]


def add_progress(text: str) -> str:
    if 'class="ux-reading-progress"' in text:
        return text
    m = MAIN_OPEN_RE.search(text)
    if not m:
        return text
    progress = '<div class="ux-reading-progress" aria-hidden="true"><span></span></div>\n'
    return text[:m.start()] + progress + text[m.start():]


def insert_tool_helpers(text: str) -> str:
    if 'class="ux-tool-helperbar"' in text:
        return text
    pat = re.compile(r'<div\b(?=[^>]*class=["\'][^"\']*\bdt-workspace\b[^"\']*["\'])[^>]*>', re.I | re.S)
    m = pat.search(text)
    if not m:
        return text
    helper = '''<div class="ux-tool-helperbar" aria-label="Быстрые действия инструмента">
  <span class="ux-tool-helperbar__label">Быстрые действия</span>
  <button type="button" data-ux-paste>Вставить из буфера</button>
  <button type="button" data-ux-clear>Очистить</button>
  <kbd title="Запустить основное действие">Ctrl/⌘ + Enter</kbd>
</div>\n'''
    return text[:m.start()] + helper + text[m.start():]


def plain_heading(block: str) -> tuple[re.Match[str] | None, str]:
    hm = re.search(r'<h([23])\b[^>]*>(.*?)</h\1>', block, re.I | re.S)
    if not hm:
        return None, ''
    label = re.sub(r'<[^>]+>', ' ', hm.group(2))
    label = html.unescape(re.sub(r'\s+', ' ', label)).strip()
    return hm, label


def collapse_section_by_heading(text: str, phrase: str, element_id: str) -> str:
    if f'id="{element_id}"' in text:
        return text
    for m in SECTION_RE.finditer(text):
        block = m.group(0)
        hm, label = plain_heading(block)
        if not hm or phrase.lower() not in label.lower():
            continue
        opening_end = block.find('>') + 1
        inner = block[opening_end:-len('</section>')]
        # Remove the visible heading from its original location; retain semantic H2 as sr-only.
        inner_hm = re.search(r'<h([23])\b[^>]*>.*?</h\1>', inner, re.I | re.S)
        if inner_hm:
            inner = inner[:inner_hm.start()] + inner[inner_hm.end():]
        replacement = (
            f'<details class="ux-guide-more" id="{element_id}">'
            f'<summary>{html.escape(label)}</summary>'
            '<div class="ux-guide-more__content">'
            f'<h2 class="ux-sr-only">{html.escape(label)}</h2>'
            + inner
            + '</div></details>'
        )
        return text[:m.start()] + replacement + text[m.end():]
    return text


def ensure_section_id_by_heading(text: str, phrase: str, element_id: str) -> str:
    if f'id="{element_id}"' in text:
        return text
    for m in SECTION_RE.finditer(text):
        block = m.group(0)
        _, label = plain_heading(block)
        if phrase.lower() not in label.lower():
            continue
        opening_end = block.find('>') + 1
        opening = add_id_to_opening(block[:opening_end], element_id)
        block = opening + block[opening_end:]
        return text[:m.start()] + block + text[m.end():]
    return text


def insert_decision_jumps(text: str) -> str:
    if 'class="ux-guide-jumps"' in text:
        return text
    links = [
        ('compare', 'Сравнение'),
        ('guide-differences', 'Различия'),
        ('guide-estimate', 'Оценка'),
        ('guide-faq', 'FAQ'),
    ]
    available = [(i, label) for i, label in links if re.search(rf'\bid=["\']{re.escape(i)}["\']', text, re.I)]
    if len(available) < 2:
        return text
    nav = '<nav class="ux-guide-jumps" aria-label="Навигация по разбору"><div class="container ux-guide-jumps__inner">' + ''.join(
        f'<a href="#{i}">{label}</a>' for i, label in available
    ) + '</div></nav>'
    hero_pat = re.compile(r'(<section\b(?=[^>]*class=["\'][^"\']*\bhero\b[^"\']*["\'])[^>]*>.*?</section>)', re.I | re.S)
    return hero_pat.sub(lambda m: m.group(1) + '\n' + nav, text, count=1)


changed_tools: list[str] = []
for path in sorted((root / 'tools').glob('*/index.html')):
    text = path.read_text(encoding='utf-8')
    original = text
    text = add_assets(text)
    text = add_main_class(text, 'ux-tool-main')
    text = insert_tool_helpers(text)
    if text != original:
        path.write_text(text, encoding='utf-8')
        changed_tools.append('/' + path.relative_to(root).parent.as_posix() + '/')

changed_guides: list[str] = []
for path in sorted((root / 'guides').glob('*/index.html')):
    text = path.read_text(encoding='utf-8')
    original = text
    text = add_assets(text)
    text = add_main_class(text, 'ux-guide-main')
    text = add_progress(text)

    # Three decision-guide templates do not have the article TOC used by the regular guides.
    is_decision = 'class="layout"' not in text and "class='layout'" not in text
    if is_decision:
        text = ensure_section_id_by_heading(text, 'Выбирайте по ограничениям задачи', 'compare')
        text = collapse_section_by_heading(text, 'Где решение начинает отличаться', 'guide-differences')
        text = collapse_section_by_heading(text, 'Ориентир до технического задания', 'guide-estimate')
        text = ensure_section_id_by_heading(text, 'Два частых пограничных случая', 'guide-faq')
        text = insert_decision_jumps(text)

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed_guides.append('/' + path.relative_to(root).parent.as_posix() + '/')

# Guards.
problems: list[str] = []
for path in sorted((root / 'tools').glob('*/index.html')):
    text = path.read_text(encoding='utf-8')
    rel = '/' + path.relative_to(root).parent.as_posix() + '/'
    if CSS_MARK not in text or JS_MARK not in text or 'class="ux-tool-helperbar"' not in text:
        problems.append(rel + ':tool-helper')

for path in sorted((root / 'guides').glob('*/index.html')):
    text = path.read_text(encoding='utf-8')
    rel = '/' + path.relative_to(root).parent.as_posix() + '/'
    if CSS_MARK not in text or JS_MARK not in text or 'class="ux-reading-progress"' not in text:
        problems.append(rel + ':reading-assets')
    if 'class="layout"' not in text and "class='layout'" not in text:
        required = ('compare', 'guide-differences', 'guide-estimate', 'guide-faq')
        ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', text, re.I))
        if not set(required).issubset(ids):
            problems.append(rel + ':decision-sections')
        for href in re.findall(r'class=["\']ux-guide-jumps[^>]*>.*?href=["\']#([^"\']+)', text, re.I | re.S):
            if href not in ids:
                problems.append(rel + ':#' + href)

if problems:
    raise SystemExit('stage92 UX invariant failed: ' + ', '.join(problems[:30]))

print(f'stage92 tools={len(changed_tools)} guides={len(changed_guides)}')
print('stage92 tool pages: ' + ', '.join(changed_tools))
print('stage92 guide pages: ' + ', '.join(changed_guides))
