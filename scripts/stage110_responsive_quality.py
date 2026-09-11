#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
STYLE_PATH = ROOT / 'assets' / 'stage98-design-system.css'
STYLE_MARK = '/* stage110-responsive-quality */'

CSS = r'''
/* stage110-responsive-quality */
/*
  Final cross-family QA layer after the DOM/content passes.
  Goals: no hidden mobile navigation content, denser service reading rhythm,
  safer case media, larger secondary tap targets, and a shorter mobile footer.
*/

/* Case media should never escape the reading column when a legacy case uses
   intrinsic image widths larger than its current card/hero container. */
body[data-ux-family="case"] :is(.visual,.hero-visual,.s51-map){
  width:100%!important;
  max-width:100%!important;
  min-width:0!important;
}
body[data-ux-family="case"] :is(.visual,.hero-visual) :is(picture,img){
  display:block!important;
  max-width:100%!important;
}
body[data-ux-family="case"] :is(.visual,.hero-visual) img{
  width:100%!important;
  height:auto!important;
}

/* The three newer comparison guides had a larger closing rhythm than the rest
   of the editorial family. Keep the CTA prominent without creating a visual gap. */
body[data-ux-family="guide"] main>.stage109-guide-endcap{
  padding-block:clamp(2.25rem,3.4vw,3.1rem)!important;
}

/* Secondary actions should still feel clickable. This deliberately targets
   navigation/action surfaces only, never links inside article prose. */
body[data-ux-family] main :is(
  .portfolio-card__footer,
  .case-library-card__action,
  .s101-related,
  .s103-discovery,
  .related,
  .s48-related,
  .s50-related
) a{
  min-height:2.25rem;
  display:inline-flex;
  align-items:center;
}

@media(max-width:820px){
  /* Service pages were still noticeably taller than adjacent families after
     stacking to one column. Reduce only whitespace, not content. */
  body[data-ux-family="service"] :is(.stage95-service-core,.stage95-service-meta){
    padding-block:1.35rem!important;
  }
  body[data-ux-family="service"] :is(.stage95-service-core,.stage95-service-meta)>.s48-section>.container{
    padding:1.35rem 0!important;
  }
  body[data-ux-family="service"] main.ux-service-main>.s48-section,
  body[data-ux-family="service"] main.ux-service-main>.stage95-review-strip.s48-section{
    padding-block:2.15rem!important;
  }
  body[data-ux-family="service"] main.ux-service-main>.s101-related{
    padding:2.1rem 0!important;
  }
  body[data-ux-family="service"] .s48-proof :is(.s48-case__image,.s48-case__diagram,.stage109-case-diagram){
    min-height:14.5rem!important;
  }
  body[data-ux-family] main>.stage108-endcap{
    padding-block:2.15rem!important;
  }

  /* Legacy article TOCs used a horizontally clipped one-line rail. Showing all
     chapters is more predictable on phone and removes the hidden-content edge. */
  body[data-page^="guides--"] .toc{
    display:flex!important;
    flex-wrap:wrap!important;
    align-items:center!important;
    width:100%!important;
    max-width:100%!important;
    overflow:visible!important;
    white-space:normal!important;
    gap:.38rem!important;
    padding:.5rem!important;
  }
  body[data-page^="guides--"] .toc a{
    flex:0 1 auto!important;
    min-height:2.35rem!important;
    white-space:normal!important;
  }
  body[data-page^="guides--"] :is(.crumbs,.breadcrumbs){
    max-width:100%!important;
    overflow:visible!important;
    white-space:normal!important;
    overflow-wrap:anywhere!important;
  }

  /* Shared footer: two compact navigation columns instead of one long vertical
     list. Metadata remains fully visible and keeps comfortable tap height. */
  body[data-ux-family] .stage108-footer__inner{
    gap:.9rem!important;
    padding-block:1.35rem 1.55rem!important;
  }
  body[data-ux-family] .stage108-footer__nav{
    display:grid!important;
    grid-template-columns:repeat(2,minmax(0,1fr))!important;
    justify-content:stretch!important;
    gap:.12rem .8rem!important;
  }
  body[data-ux-family] .stage108-footer__nav a,
  body[data-ux-family] .stage108-footer__meta a{
    min-height:2.25rem!important;
    display:flex!important;
    align-items:center!important;
  }
  body[data-ux-family] .stage108-footer__meta{
    display:grid!important;
    grid-template-columns:repeat(2,minmax(0,1fr))!important;
    align-items:start!important;
    gap:.1rem .8rem!important;
    padding-top:.7rem!important;
  }
  body[data-ux-family] .stage108-footer__meta>span{
    grid-column:1/-1!important;
    margin-right:0!important;
    min-height:2rem;
    display:flex;
    align-items:center;
  }

  /* Common card and catalog actions previously rendered as 14-20px text rows. */
  body[data-ux-family] main :is(
    .portfolio-card__footer,
    .case-library-card__action,
    .s101-card,
    .s50-card,
    .s44-route,
    .s48-proof,
    .s48-related,
    .s101-related
  ) a{
    min-height:2.4rem!important;
    display:inline-flex!important;
    align-items:center!important;
  }
}

@media(max-width:520px){
  /* Very narrow phones: preserve readable footer labels without horizontal
     overflow while keeping the two-column information density. */
  body[data-ux-family] .stage108-footer__nav,
  body[data-ux-family] .stage108-footer__meta{
    grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;
  }
  body[data-ux-family] .stage108-footer__nav a,
  body[data-ux-family] .stage108-footer__meta a{
    min-width:0!important;
    overflow-wrap:anywhere!important;
  }
}
'''


def full_pages() -> list[Path]:
    pages: list[Path] = []
    for path in sorted(ROOT.rglob('*.html')):
        text = path.read_text(encoding='utf-8', errors='ignore')
        if '<main' not in text or '<body' not in text:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if path.name.startswith(('google', 'yandex_')):
            continue
        pages.append(path)
    return pages


if not STYLE_PATH.is_file():
    raise SystemExit('stage110: stage98 design source missing')
styles = STYLE_PATH.read_text(encoding='utf-8')
if STYLE_MARK not in styles:
    STYLE_PATH.write_text(styles.rstrip() + '\n\n' + CSS.strip() + '\n', encoding='utf-8')

pages = full_pages()
problems: list[str] = []
family_counts: dict[str, int] = {}

for path in pages:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding='utf-8', errors='ignore')
    body = re.search(r'<body\b([^>]*)>', text, re.I | re.S)
    family = ''
    if body:
        match = re.search(r'data-ux-family=["\']([^"\']+)', body.group(1), re.I)
        family = match.group(1) if match else ''
    family_counts[family or 'unclassified'] = family_counts.get(family or 'unclassified', 0) + 1

    # Every real page needs a viewport declaration and exactly one visible content H1.
    if not re.search(r'<meta\b[^>]*name=["\']viewport["\']', text, re.I):
        problems.append(f'{rel}: viewport meta missing')
    h1_count = len(re.findall(r'<h1\b', text, re.I))
    if rel != '404.html' and h1_count != 1:
        problems.append(f'{rel}: h1 count={h1_count}')

    # The unified shell should be present once on all non-404 content pages.
    if rel != '404.html':
        if len(re.findall(r'<header\b[^>]*class=["\'][^"\']*\bstage98-header\b', text, re.I | re.S)) != 1:
            problems.append(f'{rel}: shared header missing/duplicated')
        if len(re.findall(r'<footer\b[^>]*class=["\'][^"\']*\bstage108-footer\b', text, re.I | re.S)) != 1:
            problems.append(f'{rel}: shared footer missing/duplicated')

    # Images that reserve no intrinsic space are a common mobile layout-shift source.
    for tag in re.findall(r'<img\b[^>]*>', text, re.I | re.S):
        if not re.search(r'\bwidth=["\']\d+', tag, re.I) or not re.search(r'\bheight=["\']\d+', tag, re.I):
            problems.append(f'{rel}: image without width/height')
            break

    # No empty anchors or javascript pseudo-links in the final static output.
    if re.search(r'<a\b[^>]*href=["\']\s*(?:#|javascript:[^"\']*)?["\']', text, re.I):
        problems.append(f'{rel}: empty/pseudo anchor remains')

# Responsive-family regression guards. These are intentionally marker-based so
# later refactors can change exact values without silently dropping the fixes.
final_styles = STYLE_PATH.read_text(encoding='utf-8')
for marker in (
    'body[data-page^="guides--"] .toc',
    'body[data-ux-family] .stage108-footer__nav',
    'body[data-ux-family="service"] :is(.stage95-service-core,.stage95-service-meta)',
    'body[data-ux-family="case"] :is(.visual,.hero-visual,.s51-map)',
):
    if marker not in final_styles:
        problems.append(f'responsive CSS guard missing: {marker}')

if len(pages) < 70:
    problems.append(f'only {len(pages)} user-facing pages audited')

if problems:
    raise SystemExit('stage110 responsive quality failed:\n' + '\n'.join(problems[:60]))

families = ', '.join(f'{key}={value}' for key, value in sorted(family_counts.items()))
print(f'stage110 responsive quality: audited={len(pages)} pages; {families}; viewport/header/footer/media/tap guards OK')
