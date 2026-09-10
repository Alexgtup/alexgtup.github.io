#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from collections import Counter
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
MAIN_RE = re.compile(r'<main\b[^>]*>.*?</main>', re.I | re.S)
FOOTER_RE = re.compile(r'<footer\b[^>]*>.*?</footer>', re.I | re.S)
SECTION_RE = re.compile(r'<section\b[^>]*>.*?</section>', re.I | re.S)
DETAIL_RE = re.compile(
    r'\s*<details\b(?=[^>]*class=["\'][^"\']*\bux-seo-more\b[^"\']*["\'])[^>]*>.*?</details>\s*',
    re.I | re.S,
)
TELEGRAM_RE = re.compile(r'https://t\.me/Alexuys', re.I)
STYLE_MARK = '/* stage108-sitewide-visual-cleanup */'

CSS = r'''
/* stage108-sitewide-visual-cleanup */
/* Earlier visual passes accumulated vertical padding on the same service sections. */
body[data-ux-family="service"] .stage95-service-core,
body[data-ux-family="service"] .stage95-service-meta{
  padding-block:clamp(2.25rem,3.4vw,3.25rem)!important;
}
body[data-ux-family="service"] .stage95-service-core>.s48-section>.container,
body[data-ux-family="service"] .stage95-service-meta>.s48-section>.container{
  padding:clamp(1.85rem,2.9vw,2.7rem) 0!important;
}
body[data-ux-family="service"] main.ux-service-main>.s48-section,
body[data-ux-family="service"] main.ux-service-main>.stage95-review-strip.s48-section{
  padding-block:clamp(3rem,4.7vw,4.15rem)!important;
}
body[data-ux-family="service"] main.ux-service-main>.s101-related{
  padding:clamp(3rem,4.5vw,4rem) 0!important;
}
body[data-ux-family="service"] main.ux-service-main>.s101-related .s101-card{
  min-height:11.5rem!important;
}
body[data-ux-family="service"] .s48-proof .s48-case{
  min-height:21rem!important;
}
body[data-ux-family="service"] .s48-proof :is(.s48-case__image,.s48-case__diagram){
  min-height:20rem!important;
}
body[data-ux-family="service"] .s48-proof .s48-case__body{
  padding:clamp(1.35rem,3vw,2.5rem)!important;
}
body[data-ux-family="service"] .s48-proof .s48-case__body h3{
  font-size:clamp(1.65rem,2.8vw,2.8rem)!important;
}
body[data-ux-family="service"] .s48-proof .s48-case__body b{margin-top:1.25rem!important}

/* Generic case art now reads like a system surface instead of an empty placeholder. */
body[data-ux-family="service"] .s48-case__diagram{
  background:
    linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px),
    radial-gradient(circle at 50% 48%,rgba(129,149,255,.13),transparent 12rem),#0a0d11!important;
  background-size:34px 34px,34px 34px,auto,auto!important;
}
body[data-ux-family="service"] .s48-case__diagram i{border-color:rgba(255,255,255,.1)!important}
body[data-ux-family="service"] .s48-case__diagram i:nth-child(1){border-color:rgba(201,255,74,.28)!important}
body[data-ux-family="service"] .s48-case__diagram b{
  display:grid!important;
  place-items:center!important;
  width:6.5rem;
  height:6.5rem;
  border:1px solid rgba(201,255,74,.24);
  border-radius:50%;
  background:rgba(9,12,15,.86);
  color:var(--ds-text)!important;
  font-size:.72rem!important;
  line-height:1.35!important;
  letter-spacing:.13em!important;
  box-shadow:0 0 0 1rem rgba(201,255,74,.015)!important;
}

/* Discovery links remain crawlable, but no longer appear as raw SEO text. */
body[data-ux-family] main>.s103-discovery{
  width:var(--ds-shell,min(calc(100% - 2.4rem),1280px))!important;
  max-width:1280px!important;
  margin:clamp(1.2rem,2.4vw,2rem) auto!important;
  padding:.7rem!important;
  display:flex!important;
  flex-wrap:wrap!important;
  gap:.45rem!important;
  border:1px solid var(--ds-line)!important;
  border-radius:1rem!important;
  background:var(--ds-surface)!important;
}
body[data-ux-family] main>.s103-discovery a{
  min-height:2.25rem!important;
  display:inline-flex!important;
  align-items:center!important;
  padding:.48rem .7rem!important;
  border:1px solid var(--ds-line)!important;
  border-radius:999px!important;
  background:transparent!important;
  color:var(--ds-muted)!important;
  text-decoration:none!important;
  font-size:.75rem!important;
  font-weight:750!important;
}
body[data-ux-family] main>.s103-discovery a:hover{
  color:var(--ds-text)!important;
  border-color:var(--ds-line-strong)!important;
  background:var(--ds-surface-2)!important;
}

/* The final action should end the page without a large empty tail. */
body[data-ux-family] main>.stage108-endcap{
  padding-block:clamp(3rem,4.8vw,4.25rem)!important;
}
body[data-ux-family] .stage108-endcap :is(
  .s48-contact__box,.s51-contact-card,.cta-box,.dt-contact__card,
  .s64-conversion__inner,.intl-cta-box,.ux-product-contact
){
  border:1px solid var(--ds-line)!important;
  border-radius:var(--ds-radius-lg)!important;
  background:linear-gradient(145deg,var(--ds-surface-2),var(--ds-surface))!important;
  box-shadow:none!important;
}
body[data-ux-family] .stage108-endcap :is(
  .s48-contact__box,.s51-contact-card,.dt-contact__card,.s64-conversion__inner,.intl-cta-box
){
  padding:clamp(1.35rem,2.6vw,2.2rem)!important;
}
body[data-ux-family] .stage108-endcap h2{max-width:18ch!important}
body[data-ux-family] .stage108-endcap p{max-width:62ch!important}

/* One footer component replaces the legacy footer variants. */
body[data-ux-family] .stage108-footer{
  margin:0!important;
  padding:0!important;
  border:0!important;
  border-top:1px solid var(--ds-line)!important;
  background:var(--ds-bg)!important;
  color:var(--ds-muted)!important;
}
body[data-ux-family] .stage108-footer__inner{
  padding-block:2.15rem 2.35rem!important;
  display:grid!important;
  grid-template-columns:minmax(13rem,.7fr) minmax(0,1.3fr)!important;
  grid-template-areas:"brand nav" "meta meta";
  gap:1.8rem 2.5rem!important;
  align-items:start!important;
}
body[data-ux-family] .stage108-footer__brand{
  grid-area:brand;
  display:grid;
  gap:.4rem;
  align-content:start;
}
body[data-ux-family] .stage108-footer__brand>a{
  width:max-content;
  color:var(--ds-text)!important;
  text-decoration:none!important;
  font-size:1.08rem!important;
  font-weight:850!important;
  letter-spacing:-.04em;
}
body[data-ux-family] .stage108-footer__brand>span{
  color:var(--ds-muted-2)!important;
  font:700 .6rem/1.3 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace!important;
  letter-spacing:.12em!important;
}
body[data-ux-family] .stage108-footer__nav{
  grid-area:nav;
  display:flex!important;
  flex-wrap:wrap!important;
  justify-content:flex-end!important;
  gap:.55rem 1.05rem!important;
}
body[data-ux-family] .stage108-footer__nav a,
body[data-ux-family] .stage108-footer__meta a{
  color:var(--ds-muted)!important;
  text-decoration:none!important;
  font-size:.8rem!important;
  line-height:1.35!important;
}
body[data-ux-family] .stage108-footer__nav a:hover,
body[data-ux-family] .stage108-footer__meta a:hover{color:var(--ds-text)!important}
body[data-ux-family] .stage108-footer__meta{
  grid-area:meta;
  padding-top:1rem!important;
  border-top:1px solid var(--ds-line)!important;
  display:flex!important;
  flex-wrap:wrap!important;
  align-items:center!important;
  gap:.55rem 1.05rem!important;
  color:var(--ds-muted-2)!important;
  font-size:.74rem!important;
}
body[data-ux-family] .stage108-footer__meta>span{margin-right:auto}
body[data-ux-family] .stage108-footer .stage95-footer-cookie{
  min-height:auto!important;
  padding:0!important;
  border:0!important;
  background:transparent!important;
  color:var(--ds-muted)!important;
  font-size:.74rem!important;
}

/* Services hub: discovery belongs to the shell and the final action stays close. */
body[data-page="services"] #service-options{
  padding-bottom:clamp(2.8rem,4vw,3.8rem)!important;
}
body[data-page="services"] main>.s103-discovery{
  margin-top:0!important;
  margin-bottom:clamp(2rem,3.4vw,3rem)!important;
}
body[data-page="services"] main>.s64-conversion.stage108-endcap{padding-top:0!important}

@media(max-width:820px){
  body[data-ux-family="service"] .stage95-service-core,
  body[data-ux-family="service"] .stage95-service-meta{padding-block:1.8rem!important}
  body[data-ux-family="service"] .stage95-service-core>.s48-section>.container,
  body[data-ux-family="service"] .stage95-service-meta>.s48-section>.container{padding:1.65rem 0!important}
  body[data-ux-family="service"] main.ux-service-main>.s48-section,
  body[data-ux-family="service"] main.ux-service-main>.stage95-review-strip.s48-section{padding-block:2.7rem!important}
  body[data-ux-family="service"] main.ux-service-main>.s101-related{padding:2.7rem 0!important}
  body[data-ux-family="service"] .s48-proof .s48-case{min-height:0!important}
  body[data-ux-family="service"] .s48-proof :is(.s48-case__image,.s48-case__diagram){min-height:17rem!important}
  body[data-ux-family] main>.s103-discovery{
    width:min(calc(100% - 2rem),1280px)!important;
    margin:1rem auto!important;
    padding:.55rem!important;
    flex-wrap:nowrap!important;
    overflow-x:auto!important;
    scrollbar-width:none;
  }
  body[data-ux-family] main>.s103-discovery::-webkit-scrollbar{display:none}
  body[data-ux-family] main>.s103-discovery a{
    flex:0 0 auto!important;
    min-height:2.15rem!important;
  }
  body[data-ux-family] main>.stage108-endcap{padding-block:2.7rem!important}
  body[data-ux-family] .stage108-footer__inner{
    grid-template-columns:1fr!important;
    grid-template-areas:"brand" "nav" "meta";
    gap:1.25rem!important;
    padding-block:1.75rem 2rem!important;
  }
  body[data-ux-family] .stage108-footer__nav{justify-content:flex-start!important}
  body[data-ux-family] .stage108-footer__meta{
    align-items:flex-start!important;
    flex-direction:column!important;
    gap:.6rem!important;
  }
  body[data-ux-family] .stage108-footer__meta>span{margin-right:0}
}
'''

RU_FOOTER = '''<footer class="footer stage108-footer" data-nosnippet=""><div class="container stage108-footer__inner"><div class="stage108-footer__brand"><a href="/" aria-label="Alexuys - на главную">alexuys</a><span>WEB · APPS · AUTOMATION</span></div><nav class="stage108-footer__nav" aria-label="Ссылки в подвале"><a href="/services/">Услуги</a><a href="/cases/">Кейсы</a><a href="/guides/">Разборы</a><a href="/tools/">Инструменты</a><a href="/demos/">Демо</a><a href="/about/">Обо мне</a></nav><div class="stage108-footer__meta"><span>© 2026 Alexuys · Александр</span><a href="mailto:alexgtup@gmail.com">alexgtup@gmail.com</a><a href="https://freelance.ru/gglalex" target="_blank" rel="noopener noreferrer">Freelance.ru ↗</a><a href="/privacy/">Конфиденциальность</a></div></div></footer>'''
EN_FOOTER = '''<footer class="intl-footer stage108-footer" data-nosnippet=""><div class="intl-container stage108-footer__inner"><div class="stage108-footer__brand"><a href="/en/" aria-label="Alexuys - home">alexuys</a><span>WEB · APPS · AUTOMATION</span></div><nav class="stage108-footer__nav" aria-label="Footer navigation"><a href="/en/services/">Services</a><a href="/en/cases/">Cases</a><a href="/en/guides/">Guides</a><a href="/en/about/">About</a></nav><div class="stage108-footer__meta"><span>© 2026 Alexuys</span><a href="mailto:alexgtup@gmail.com">alexgtup@gmail.com</a><a href="/en/privacy/">Privacy</a><a href="/" hreflang="ru" lang="ru">Русская версия</a></div></div></footer>'''


def is_en(html: str) -> bool:
    match = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', html, re.I)
    return bool(match and match.group(1).lower().startswith('en'))


def add_class(tag: str, name: str) -> str:
    if re.search(rf'\b{re.escape(name)}\b', tag):
        return tag
    match = re.search(r'class=(["\'])(.*?)\1', tag, re.I | re.S)
    if match:
        classes = match.group(2).split() + [name]
        replacement = f'class={match.group(1)}{" ".join(classes)}{match.group(1)}'
        return tag[:match.start()] + replacement + tag[match.end():]
    return tag[:-1] + f' class="{name}">'


def mark_last_contact(main: str, rel: str) -> tuple[str, bool]:
    if rel == 'index.html':
        return main, False
    pattern = (
        r'(?:\bid=["\'](?:contact|case-contact|hub-contact|demo-contact)["\'])|'
        r'(?:\bclass=["\'][^"\']*\b(?:s48-contact|s50-cta|s64-conversion|dt-contact|ux-product-contact|cta-box)\b)'
    )
    candidates: list[re.Match[str]] = []
    for match in re.finditer(r'<section\b[^>]*>', main, re.I | re.S):
        if re.search(pattern, match.group(0), re.I):
            candidates.append(match)
    if candidates:
        match = candidates[-1]
        return main[:match.start()] + add_class(match.group(0), 'stage108-endcap') + main[match.end():], True

    for section in reversed(list(SECTION_RE.finditer(main))):
        if not TELEGRAM_RE.search(section.group(0)):
            continue
        opening = re.match(r'<section\b[^>]*>', section.group(0), re.I | re.S)
        if not opening:
            continue
        block = add_class(opening.group(0), 'stage108-endcap') + section.group(0)[opening.end():]
        return main[:section.start()] + block + main[section.end():], True
    return main, False


def move_seo_before_contact(main: str, rel: str) -> tuple[str, int]:
    target = (
        rel == 'demos/index.html'
        or rel == 'tools/index.html'
        or (rel.startswith('tools/') and rel.endswith('/index.html'))
    )
    if not target:
        return main, 0
    details = list(DETAIL_RE.finditer(main))
    if not details:
        return main, 0
    contacts = list(re.finditer(
        r'<section\b(?=[^>]*(?:\bid=["\'](?:hub-contact|demo-contact)["\']|class=["\'][^"\']*\bdt-contact\b))[^>]*>',
        main,
        re.I | re.S,
    ))
    if not contacts:
        return main, 0
    contact_start = contacts[-1].start()
    after = [match for match in details if match.start() > contact_start]
    if not after:
        return main, 0
    blocks = [match.group(0).strip() for match in after]
    for match in reversed(after):
        main = main[:match.start()] + '\n' + main[match.end():]
    return main[:contact_start] + '\n'.join(blocks) + '\n' + main[contact_start:], len(blocks)


style_path = ROOT / 'assets' / 'stage98-design-system.css'
if not style_path.is_file():
    raise SystemExit('stage108: design-system source missing')
style = style_path.read_text(encoding='utf-8')
if STYLE_MARK not in style:
    style_path.write_text(style.rstrip() + '\n\n' + CSS.strip() + '\n', encoding='utf-8')

changed: list[str] = []
footer_changed = 0
moved_details = 0
endcaps = 0

for path in sorted(ROOT.rglob('*.html')):
    rel = path.relative_to(ROOT).as_posix()
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<main' not in html or rel == '404.html' or path.name.startswith(('google', 'yandex_')):
        continue
    original = html
    main_match = MAIN_RE.search(html)
    if main_match:
        main = main_match.group(0)
        main, moved = move_seo_before_contact(main, rel)
        moved_details += moved
        main, marked = mark_last_contact(main, rel)
        endcaps += int(marked)
        html = html[:main_match.start()] + main + html[main_match.end():]
    footer_match = FOOTER_RE.search(html)
    if footer_match:
        replacement = EN_FOOTER if is_en(html) else RU_FOOTER
        html = html[:footer_match.start()] + replacement + html[footer_match.end():]
        footer_changed += 1
    if html != original:
        path.write_text(html, encoding='utf-8')
        changed.append(rel)

problems: list[str] = []
footer_signatures = Counter()
user_pages = 0
for path in sorted(ROOT.rglob('*.html')):
    rel = path.relative_to(ROOT).as_posix()
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<main' not in html or rel == '404.html' or path.name.startswith(('google', 'yandex_')):
        continue
    user_pages += 1
    footer_count = len(re.findall(
        r'<footer\b[^>]*class=["\'][^"\']*\bstage108-footer\b', html, re.I
    ))
    if footer_count != 1:
        problems.append(f'{rel}: shared footer count={footer_count}')
    footer = FOOTER_RE.search(html)
    if not footer:
        problems.append(f'{rel}: footer missing')
        continue
    hrefs = tuple(re.findall(r'<a\b[^>]*href=["\']([^"\']+)', footer.group(0), re.I))
    footer_signatures[hrefs] += 1

    target = (
        rel == 'demos/index.html'
        or rel == 'tools/index.html'
        or (rel.startswith('tools/') and rel.endswith('/index.html'))
    )
    if target:
        main_match = MAIN_RE.search(html)
        if main_match:
            main = main_match.group(0)
            contacts = list(re.finditer(
                r'<section\b(?=[^>]*(?:\bid=["\'](?:hub-contact|demo-contact)["\']|class=["\'][^"\']*\bdt-contact\b))[^>]*>',
                main,
                re.I | re.S,
            ))
            if contacts and any(match.start() > contacts[-1].start() for match in DETAIL_RE.finditer(main)):
                problems.append(f'{rel}: SEO disclosure remains after contact')

if len(footer_signatures) > 2:
    problems.append(f'footer signatures={len(footer_signatures)} (expected RU + EN only)')
if STYLE_MARK not in style_path.read_text(encoding='utf-8'):
    problems.append('stage108 visual styles missing')

if problems:
    raise SystemExit('stage108 sitewide visual cleanup failed:\n' + '\n'.join(problems[:40]))

print(
    f'stage108 visual cleanup: pages={user_pages}; changed={len(changed)}; '
    f'footers={footer_changed}; endcaps={endcaps}; moved_seo={moved_details}; '
    f'footer_signatures={len(footer_signatures)}'
)
