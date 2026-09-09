#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

MAIN_RE = re.compile(r"<main\b[^>]*>.*?</main>", re.I | re.S)
SECTION_RE = re.compile(r"<section\b[^>]*>.*?</section>", re.I | re.S)
AUX_CLASS_RE = re.compile(r"\b(?:s68-entry|s66-tool-link)\b", re.I)
TELEGRAM_ANCHOR_RE = re.compile(
    r"\s*<a\b[^>]*href=[\"']https://t\.me/Alexuys[^\"']*[\"'][^>]*>.*?</a>\s*",
    re.I | re.S,
)
DIRECT_RE = re.compile(r"https://t\.me/Alexuys|mailto:alexgtup@gmail\.com", re.I)
UX_MARK = 'data-stage87-ux="true"'
UX_LINK = '<link href="/assets/ux-pass.css?v=20260909-1" rel="stylesheet" data-stage87-ux="true"/>'

changed: list[str] = []
removed = 0

# Existing conversion cleanup: auxiliary recommendation cards must not compete
# with a stronger contact action that follows later on the same page.
for path in sorted(root.rglob("*.html")):
    text = path.read_text(encoding="utf-8")
    mm = MAIN_RE.search(text)
    if not mm:
        continue
    main = mm.group(0)
    original = main
    sections = list(SECTION_RE.finditer(main))

    # Work backwards so offsets of earlier sections stay stable after replacement.
    for index in range(len(sections) - 1, -1, -1):
        sec = sections[index]
        block = sec.group(0)
        opening = block[: block.find(">") + 1]
        if not AUX_CLASS_RE.search(opening) or not TELEGRAM_ANCHOR_RE.search(block):
            continue

        later = main[sec.end():]
        if not DIRECT_RE.search(later):
            continue

        cleaned, count = TELEGRAM_ANCHOR_RE.subn("", block)
        if not count:
            continue
        main = main[:sec.start()] + cleaned + main[sec.end():]
        removed += count
        sections = list(SECTION_RE.finditer(main))

    if main != original:
        text = text[:mm.start()] + main + text[mm.end():]
        path.write_text(text, encoding="utf-8")
        changed.append(path.relative_to(root).as_posix())


def add_class_to_tag(tag: str, class_name: str) -> str:
    class_m = re.search(r'class=(["\'])(.*?)\1', tag, flags=re.I | re.S)
    if class_m:
        classes = class_m.group(2).split()
        if class_name in classes:
            return tag
        classes.append(class_name)
        replacement = f'class={class_m.group(1)}{" ".join(classes)}{class_m.group(1)}'
        return tag[: class_m.start()] + replacement + tag[class_m.end():]
    return tag[:-1] + f' class="{class_name}">'


def add_main_class(text: str, class_name: str) -> str:
    pat = re.compile(r'<main\b[^>]*id=["\']main-content["\'][^>]*>', re.I | re.S)
    return pat.sub(lambda m: add_class_to_tag(m.group(0), class_name), text, count=1)


def add_section_id(text: str, aria_label: str, section_id: str) -> str:
    pat = re.compile(
        rf'<section\b(?=[^>]*aria-labelledby=["\']{re.escape(aria_label)}["\'])[^>]*>',
        re.I | re.S,
    )

    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        if re.search(r'\bid=["\']', tag, re.I):
            return tag
        return tag[:-1] + f' id="{section_id}">'

    return pat.sub(repl, text, count=1)


HOME_NAV = '''\n<nav class="ux-quicknav" aria-label="Быстрый переход по странице" data-stage87-ux-nav="home">
  <div class="container ux-quicknav__inner">
    <a href="#services">Услуги</a>
    <a href="#work">Проекты</a>
    <a href="#budget">Цены</a>
    <a href="#about">Подход</a>
    <a href="#brief" class="ux-quicknav__primary">Написать</a>
  </div>
</nav>\n'''


def build_service_nav(text: str) -> str:
    candidates = (
        ('fit', 'Подходит'),
        ('result', 'Результат'),
        ('case', 'Кейс'),
        ('budget', 'Цена'),
        ('process', 'Процесс'),
    )
    links: list[str] = []
    for section_id, label in candidates:
        if re.search(rf'\bid=["\']{re.escape(section_id)}["\']', text, re.I):
            links.append(f'    <a href="#{section_id}">{label}</a>')

    if re.search(r'\bid=["\']contact["\']', text, re.I):
        links.append('    <a href="#contact" class="ux-quicknav__primary">Написать</a>')
    else:
        links.append('    <a href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer" class="ux-quicknav__primary">Написать</a>')

    return (
        '\n<nav class="ux-quicknav" aria-label="Быстрый переход по странице" data-stage87-ux-nav="service">\n'
        '  <div class="container ux-quicknav__inner">\n'
        + '\n'.join(links)
        + '\n  </div>\n</nav>\n'
    )


def insert_after_first_section_with_class(text: str, class_name: str, html: str, marker: str) -> str:
    if marker in text:
        return text
    pat = re.compile(
        rf'(<section\b(?=[^>]*class=["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\'])[^>]*>.*?</section>)',
        re.I | re.S,
    )
    return pat.sub(lambda m: m.group(1) + html, text, count=1)


def move_home_demo_after_work(text: str) -> str:
    demo_pat = re.compile(
        r'\s*(<section\b(?=[^>]*class=["\'][^"\']*\bgrowth-section\b[^"\']*["\'])(?=[^>]*aria-labelledby=["\']try-projects["\'])[^>]*>.*?</section>)',
        re.I | re.S,
    )
    dm = demo_pat.search(text)
    if not dm:
        return text
    block = dm.group(1)
    text = text[:dm.start()] + text[dm.end():]
    work_pat = re.compile(
        r'(<section\b(?=[^>]*\bid=["\']work["\'])[^>]*>.*?</section>)',
        re.I | re.S,
    )
    return work_pat.sub(lambda m: m.group(1) + "\n" + block, text, count=1)


def collapse_home_optional_brief(text: str) -> str:
    if 'class="ux-brief-more"' in text:
        return text
    pat = re.compile(
        r'(?P<current><label>\s*<span>\s*Что уже есть\s*</span>.*?</label>)\s*'
        r'(?P<limits><label>\s*<span>\s*Срок / бюджет, если есть\s*</span>.*?</label>)',
        re.I | re.S,
    )

    def repl(match: re.Match[str]) -> str:
        return (
            '<details class="ux-brief-more">'
            '<summary>Добавить ссылку, срок или бюджет <span>необязательно</span></summary>'
            '<div class="ux-brief-more__grid">'
            + match.group('current')
            + match.group('limits')
            + '</div></details>'
        )

    return pat.sub(repl, text, count=1)


ux_changed: list[str] = []
for path in sorted(root.rglob("*.html")):
    text = path.read_text(encoding="utf-8")
    is_home = 'class="s44-hero"' in text or "class='s44-hero'" in text
    is_service = 'class="s48-hero"' in text or "class='s48-hero'" in text
    if not (is_home or is_service):
        continue

    original = text
    if UX_MARK not in text:
        text = text.replace('</head>', UX_LINK + '\n</head>', 1)

    if is_home:
        text = add_main_class(text, 'ux-home-main')
        text = add_section_id(text, 'choose-title', 'services')
        text = add_section_id(text, 'budget-title', 'budget')
        text = insert_after_first_section_with_class(text, 's44-hero', HOME_NAV, 'data-stage87-ux-nav="home"')
        text = move_home_demo_after_work(text)
        text = collapse_home_optional_brief(text)
    else:
        text = add_main_class(text, 'ux-service-main')
        text = add_section_id(text, 's48-output-title', 'result')
        text = add_section_id(text, 's48-budget-title', 'budget')
        text = add_section_id(text, 's48-process-title', 'process')
        text = add_section_id(text, 's48-contact-title', 'contact')
        service_nav = build_service_nav(text)
        text = insert_after_first_section_with_class(text, 's48-hero', service_nav, 'data-stage87-ux-nav="service"')

    if text != original:
        path.write_text(text, encoding="utf-8")
        ux_changed.append(path.relative_to(root).as_posix())

# Existing invariant: no auxiliary recommendation may contain Telegram if another
# direct contact action appears later in the same main content.
problems: list[str] = []
for path in sorted(root.rglob("*.html")):
    text = path.read_text(encoding="utf-8")
    mm = MAIN_RE.search(text)
    if not mm:
        continue
    main = mm.group(0)
    for sec in SECTION_RE.finditer(main):
        block = sec.group(0)
        opening = block[: block.find(">") + 1]
        if AUX_CLASS_RE.search(opening) and TELEGRAM_ANCHOR_RE.search(block) and DIRECT_RE.search(main[sec.end():]):
            problems.append(path.relative_to(root).as_posix())
            break

if problems:
    raise SystemExit("stage87 auxiliary action invariant failed: " + ", ".join(problems))

# UX invariants: every homepage/service page that opts into the pass gets the
# stylesheet and an orientation rail. Homepage brief keeps only the core task
# visible by default; optional fields remain available through disclosure.
ux_problems: list[str] = []
for path in sorted(root.rglob("*.html")):
    text = path.read_text(encoding="utf-8")
    is_home = 'class="s44-hero"' in text or "class='s44-hero'" in text
    is_service = 'class="s48-hero"' in text or "class='s48-hero'" in text
    if not (is_home or is_service):
        continue
    if UX_MARK not in text or 'class="ux-quicknav"' not in text:
        ux_problems.append(path.relative_to(root).as_posix())
        continue
    if is_home and 'class="ux-brief-more"' not in text:
        ux_problems.append(path.relative_to(root).as_posix())

if ux_problems:
    raise SystemExit("stage87 UX invariant failed: " + ", ".join(ux_problems))

print(f"stage87 auxiliary actions: removed duplicate Telegram links={removed}; changed pages={len(changed)}")
print(f"stage87 UX pass: pages={len(ux_changed)}")
if ux_changed:
    print("stage87 UX pages: " + ", ".join(ux_changed))
