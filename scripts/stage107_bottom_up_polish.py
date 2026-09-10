#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from collections import Counter
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')

MAIN_RE = re.compile(r'<main\b[^>]*>.*?</main>', re.I | re.S)
FOOTER_RE = re.compile(r'<footer\b[^>]*>.*?</footer>', re.I | re.S)
DETAIL_RE = re.compile(
    r'\s*<details\b(?=[^>]*class=["\'][^"\']*\bux-seo-more\b[^"\']*["\'])[^>]*>.*?</details>\s*',
    re.I | re.S,
)
SECTION_RE = re.compile(r'<section\b[^>]*>.*?</section>', re.I | re.S)
TELEGRAM_RE = re.compile(r'https://t\.me/Alexuys', re.I)
FOOTER_CLASS_RE = re.compile(r'<footer\b[^>]*class=["\'][^"\']*\bstage107-footer\b[^"\']*["\'][^>]*>', re.I | re.S)

STYLE_MARK = '/* stage107-bottom-up */'
ENDCAP_CSS = r'''
/* stage107-bottom-up */
/* Final rhythm pass: remove the large empty bands that survived earlier layout stages. */
body[data-ux-family="service"] :is(.stage95-service-core,.stage95-service-meta){
  padding-block:clamp(.8rem,1.8vw,1.45rem)!important;
}
body[data-ux-family="service"] :is(.stage95-service-core,.stage95-service-meta)>.s48-section>.container{
  padding:clamp(1.55rem,2.7vw,2.35rem) 0!important;
}
body[data-ux-family="service"] .stage95-service-core+.stage95-service-meta{padding-top:0!important}
body[data-ux-family="service"] :is(.stage95-service-core,.stage95-service-meta) .s48-head{
  margin-bottom:clamp(1rem,1.8vw,1.45rem)!important;
}
body[data-ux-family] main>.stage107-endcap,
body[data-ux-family] main>.stage95-service-meta:last-child .stage107-endcap,
body[data-ux-family] main>.stage95-service-core:last-child .stage107-endcap{
  margin-top:0!important;
  margin-bottom:0!important;
}
body[data-ux-family] .stage107-endcap{
  padding-top:clamp(1.8rem,3.2vw,2.8rem)!important;
  padding-bottom:clamp(2rem,3.4vw,3rem)!important;
}
body[data-ux-family] .stage107-endcap :is(.s48-contact__box,.s51-contact-card,.cta-box,.dt-contact__card,.s64-conversion__inner,.intl-cta-box,.ux-product-contact){
  border:1px solid var(--ds-line)!important;
  border-radius:var(--ds-radius-lg)!important;
  background:linear-gradient(145deg,var(--ds-surface-2),var(--ds-surface))!important;
  box-shadow:none!important;
}
body[data-ux-family] .stage107-endcap :is(.s48-contact__box,.s51-contact-card,.dt-contact__card,.s64-conversion__inner,.intl-cta-box){
  padding:clamp(1.35rem,3vw,2.35rem)!important;
}
body[data-ux-family] .stage107-endcap h2{max-width:18ch}
body[data-ux-family] .stage107-endcap p{max-width:62ch}
body[data-ux-family] .stage107-endcap :is(.related,.s48-contact__actions,.s51-contact-actions,.actions,.growth-actions,.s64-conversion__actions,.ux-product-contact__actions){gap:.65rem!important}
body[data-ux-family] .stage107-endcap :is(h2,p,.actions,.related):last-child{margin-bottom:0!important}

body[data-ux-family] .stage107-footer{
  margin:0!important;
  padding:0!important;
  border:0!important;
  border-top:1px solid var(--ds-line)!important;
  background:var(--ds-bg)!important;
  color:var(--ds-muted)!important;
}
body[data-ux-family] .stage107-footer__inner{
  min-height:0!important;
  padding-block:1.65rem 1.9rem!important;
  display:grid!important;
  grid-template-columns:minmax(13rem,.72fr) minmax(0,1.28fr)!important;
  grid-template-areas:"brand nav" "meta meta";
  gap:1.35rem 2.5rem!important;
  align-items:start!important;
}
body[data-ux-family] .stage107-footer__brand{grid-area:brand;display:grid;gap:.42rem;align-content:start}
body[data-ux-family] .stage107-footer__brand>a{
  width:max-content;
  color:var(--ds-text)!important;
  text-decoration:none!important;
  font-size:1.1rem!important;
  font-weight:850!important;
  letter-spacing:-.04em;
}
body[data-ux-family] .stage107-footer__brand>span{
  color:var(--ds-muted-2)!important;
  font:700 .61rem/1.3 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace!important;
  letter-spacing:.12em!important;
}
body[data-ux-family] .stage107-footer__nav{
  grid-area:nav;
  display:flex!important;
  flex-wrap:wrap!important;
  justify-content:flex-end!important;
  align-items:center!important;
  gap:.55rem 1.15rem!important;
}
body[data-ux-family] .stage107-footer__nav a,
body[data-ux-family] .stage107-footer__meta a{
  color:var(--ds-muted)!important;
  text-decoration:none!important;
  font-size:.82rem!important;
  line-height:1.35!important;
}
body[data-ux-family] .stage107-footer__nav a:hover,
body[data-ux-family] .stage107-footer__meta a:hover{color:var(--ds-text)!important}
body[data-ux-family] .stage107-footer__meta{
  grid-area:meta;
  padding-top:.9rem!important;
  border-top:1px solid var(--ds-line)!important;
  display:flex!important;
  flex-wrap:wrap!important;
  align-items:center!important;
  gap:.55rem 1.15rem!important;
  color:var(--ds-muted-2)!important;
  font-size:.75rem!important;
}
body[data-ux-family] .stage107-footer__meta>span{margin-right:auto}
body[data-ux-family] .stage107-footer .stage95-footer-cookie{
  min-height:auto!important;
  padding:0!important;
  border:0!important;
  background:transparent!important;
  color:var(--ds-muted)!important;
  font-size:.75rem!important;
}
@media(max-width:760px){
  body[data-ux-family="service"] :is(.stage95-service-core,.stage95-service-meta)>.s48-section>.container{padding:1.55rem 0!important}
  body[data-ux-family] .stage107-endcap{padding-block:1.55rem 2rem!important}
  body[data-ux-family] .stage107-footer__inner{
    min-height:0;
    grid-template-columns:1fr!important;
    grid-template-areas:"brand" "nav" "meta";
    gap:1.15rem!important;
    padding-block:1.5rem 1.7rem!important;
  }
  body[data-ux-family] .stage107-footer__nav{justify-content:flex-start!important;gap:.6rem 1rem!important}
  body[data-ux-family] .stage107-footer__meta{align-items:flex-start!important;flex-direction:column!important;gap:.65rem!important}
  body[data-ux-family] .stage107-footer__meta>span{margin-right:0}
}
'''

RU_FOOTER = '''<footer class="footer stage107-footer" data-nosnippet="">
  <div class="container stage107-footer__inner">
    <div class="stage107-footer__brand">
      <a href="/" aria-label="Alexuys - на главную">alexuys</a>
      <span>WEB · APPS · AUTOMATION</span>
    </div>
    <nav class="stage107-footer__nav" aria-label="Ссылки в подвале">
      <a href="/services/">Услуги</a>
      <a href="/cases/">Кейсы</a>
      <a href="/guides/">Разборы</a>
      <a href="/tools/">Инструменты</a>
      <a href="/demos/">Демо</a>
      <a href="/about/">Обо мне</a>
    </nav>
    <div class="stage107-footer__meta">
      <span>© 2026 Alexuys · Александр</span>
      <a href="mailto:alexgtup@gmail.com">alexgtup@gmail.com</a>
      <a href="https://freelance.ru/gglalex" target="_blank" rel="noopener noreferrer">Freelance.ru ↗</a>
      <a href="/privacy/">Конфиденциальность</a>
    </div>
  </div>
</footer>'''

EN_FOOTER = '''<footer class="intl-footer stage107-footer" data-nosnippet="">
  <div class="intl-container stage107-footer__inner">
    <div class="stage107-footer__brand">
      <a href="/en/" aria-label="Alexuys - home">alexuys</a>
      <span>WEB · APPS · AUTOMATION</span>
    </div>
    <nav class="stage107-footer__nav" aria-label="Footer navigation">
      <a href="/en/services/">Services</a>
      <a href="/en/cases/">Cases</a>
      <a href="/en/guides/">Guides</a>
      <a href="/en/about/">About</a>
    </nav>
    <div class="stage107-footer__meta">
      <span>© 2026 Alexuys</span>
      <a href="mailto:alexgtup@gmail.com">alexgtup@gmail.com</a>
      <a href="/en/privacy/">Privacy</a>
      <a href="/" hreflang="ru" lang="ru">Русская версия</a>
    </div>
  </div>
</footer>'''


def relpath(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_en(html: str) -> bool:
    m = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', html, re.I)
    return bool(m and m.group(1).lower().startswith('en'))


def add_endcap_marker(tag: str) -> str:
    if 'stage107-endcap' in tag:
        return tag
    cm = re.search(r'class=(["\'])(.*?)\1', tag, re.I | re.S)
    if cm:
        classes = cm.group(2).split()
        classes.append('stage107-endcap')
        replacement = f'class={cm.group(1)}{" ".join(classes)}{cm.group(1)}'
        tag = tag[:cm.start()] + replacement + tag[cm.end():]
    else:
        tag = tag[:-1] + ' class="stage107-endcap">'
    if 'data-stage107-endcap=' not in tag:
        tag = tag[:-1] + ' data-stage107-endcap="true">'
    return tag


def mark_last_contact(main: str, rel: str) -> tuple[str, bool]:
    if rel in {'index.html', '404.html'}:
        return main, False

    candidates: list[tuple[int, int, str]] = []
    tag_re = re.compile(r'<(?:section|div)\b[^>]*>', re.I | re.S)
    for m in tag_re.finditer(main):
        tag = m.group(0)
        if re.search(
            r'(?:\bid=["\'](?:contact|case-contact|hub-contact|demo-contact)["\'])|'
            r'(?:\bclass=["\'][^"\']*\b(?:s48-contact|s50-cta|s64-conversion|dt-contact|ux-product-contact|cta-box)\b)',
            tag,
            re.I,
        ):
            candidates.append((m.start(), m.end(), tag))

    if candidates:
        start, end, tag = candidates[-1]
        return main[:start] + add_endcap_marker(tag) + main[end:], True

    sections = list(SECTION_RE.finditer(main))
    for sec in reversed(sections):
        block = sec.group(0)
        if not TELEGRAM_RE.search(block):
            continue
        opening = re.match(r'<section\b[^>]*>', block, re.I | re.S)
        if not opening:
            continue
        new_open = add_endcap_marker(opening.group(0))
        new_block = new_open + block[opening.end():]
        return main[:sec.start()] + new_block + main[sec.end():], True
    return main, False


def move_seo_before_contact(main: str, rel: str) -> tuple[str, int]:
    target = rel == 'demos/index.html' or rel == 'tools/index.html' or (
        rel.startswith('tools/') and rel.endswith('/index.html')
    )
    if not target:
        return main, 0

    details = list(DETAIL_RE.finditer(main))
    if not details:
        return main, 0

    contact_openings = list(re.finditer(
        r'<section\b(?=[^>]*(?:\bid=["\'](?:hub-contact|demo-contact)["\']|class=["\'][^"\']*\bdt-contact\b))[^>]*>',
        main,
        re.I | re.S,
    ))
    if not contact_openings:
        return main, 0
    contact_start = contact_openings[-1].start()
    after = [m for m in details if m.start() > contact_start]
    if not after:
        return main, 0

    blocks = [m.group(0).strip() for m in after]
    for m in reversed(after):
        main = main[:m.start()] + '\n' + main[m.end():]

    insert = '\n'.join(blocks) + '\n'
    main = main[:contact_start] + insert + main[contact_start:]
    return main, len(blocks)


style_path = ROOT / 'assets' / 'stage98-design-system.css'
if not style_path.is_file():
    raise SystemExit('stage107: stage98-design-system.css missing')
style_text = style_path.read_text(encoding='utf-8')
if STYLE_MARK not in style_text:
    style_path.write_text(style_text.rstrip() + '\n\n' + ENDCAP_CSS.strip() + '\n', encoding='utf-8')

changed: list[str] = []
footer_changed = 0
moved_details = 0
endcaps = 0

for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    rel = relpath(path)
    if '<main' not in html or rel == '404.html' or path.name.startswith(('google', 'yandex_')):
        continue
    original = html

    mm = MAIN_RE.search(html)
    if mm:
        main = mm.group(0)
        main, moved = move_seo_before_contact(main, rel)
        moved_details += moved
        main, marked = mark_last_contact(main, rel)
        endcaps += int(marked)
        html = html[:mm.start()] + main + html[mm.end():]

    fm = FOOTER_RE.search(html)
    if fm:
        footer = EN_FOOTER if is_en(html) else RU_FOOTER
        html = html[:fm.start()] + footer + html[fm.end():]
        footer_changed += 1

    if html != original:
        path.write_text(html, encoding='utf-8')
        changed.append(rel)

problems: list[str] = []
footer_signatures = Counter()
for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    rel = relpath(path)
    if '<main' not in html or rel == '404.html' or path.name.startswith(('google', 'yandex_')):
        continue
    footer_count = len(FOOTER_CLASS_RE.findall(html))
    if footer_count != 1:
        problems.append(f'{rel}: shared footer count={footer_count}')
    footer = FOOTER_RE.search(html)
    if not footer:
        problems.append(f'{rel}: footer missing')
        continue
    hrefs = tuple(re.findall(r'<a\b[^>]*href=["\']([^"\']+)', footer.group(0), re.I))
    footer_signatures[hrefs] += 1

    if rel == 'demos/index.html' or rel == 'tools/index.html' or (rel.startswith('tools/') and rel.endswith('/index.html')):
        main_m = MAIN_RE.search(html)
        if main_m:
            main = main_m.group(0)
            contact = re.search(
                r'<section\b(?=[^>]*(?:\bid=["\'](?:hub-contact|demo-contact)["\']|class=["\'][^"\']*\bdt-contact\b))[^>]*>',
                main,
                re.I | re.S,
            )
            if contact and any(m.start() > contact.start() for m in DETAIL_RE.finditer(main)):
                problems.append(f'{rel}: SEO disclosure remains after contact')

if len(footer_signatures) > 2:
    problems.append(f'footer signatures={len(footer_signatures)} (expected RU + EN only)')
if STYLE_MARK not in style_path.read_text(encoding='utf-8'):
    problems.append('stage107 styles missing from bundled design source')

if problems:
    raise SystemExit('stage107 bottom-up polish failed:\n' + '\n'.join(problems[:40]))

print(
    f'stage107 bottom-up: pages_changed={len(changed)}; footers={footer_changed}; '
    f'endcaps={endcaps}; seo_details_moved={moved_details}; footer_signatures={len(footer_signatures)}'
)
