#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
STYLE_PATH = ROOT / 'assets' / 'stage98-design-system.css'
STYLE_MARK = '/* stage109-content-visual-consistency */'

PROOF_VISUALS = {
    'api-integrations/index.html': ('DATA FLOW', ('WEBHOOK', 'CRM', 'API', 'STATUS')),
    'backend-development/index.html': ('BACKEND', ('CLIENT', 'API', 'LOGIC', 'DATA')),
    'crm-development/index.html': ('CRM FLOW', ('LEAD', 'STATUS', 'MANAGER', 'EVENT')),
    'development/index.html': ('CASES', ('WEB', 'APP', 'BOT', 'CRM')),
    'project-repair/index.html': ('REPAIR', ('BUG', 'TRACE', 'PATCH', 'CHECK')),
    'web-development/index.html': ('WEB B2B', ('UI', 'API', 'DATA', 'DEPLOY')),
}

CSS = r'''
/* stage109-content-visual-consistency */
/* Repeated REAL CASE rings are replaced by small route-specific system maps. */
body[data-ux-family="service"] .stage109-case-diagram{
  position:relative!important;
  min-height:20rem!important;
  overflow:hidden!important;
  background:
    linear-gradient(rgba(255,255,255,.028) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.028) 1px,transparent 1px),
    radial-gradient(circle at 50% 50%,rgba(201,255,74,.08),transparent 12rem),
    #0a0d11!important;
  background-size:36px 36px,36px 36px,auto,auto!important;
}
body[data-ux-family="service"] .stage109-case-diagram>i{display:none!important}
body[data-ux-family="service"] .stage109-case-diagram::before,
body[data-ux-family="service"] .stage109-case-diagram::after{
  content:"";
  position:absolute;
  left:50%;top:50%;
  background:rgba(255,255,255,.1);
  transform:translate(-50%,-50%);
}
body[data-ux-family="service"] .stage109-case-diagram::before{width:min(68%,24rem);height:1px}
body[data-ux-family="service"] .stage109-case-diagram::after{width:1px;height:min(60%,15rem)}
body[data-ux-family="service"] .stage109-case-diagram>b{
  position:absolute!important;
  z-index:3!important;
  left:50%!important;top:50%!important;
  transform:translate(-50%,-50%)!important;
  width:8.1rem!important;height:8.1rem!important;
  display:grid!important;place-items:center!important;
  border:1px solid rgba(201,255,74,.34)!important;
  border-radius:50%!important;
  background:#0d1116!important;
  color:var(--ds-text)!important;
  font:850 .7rem/1.25 ui-monospace,SFMono-Regular,Menlo,monospace!important;
  letter-spacing:.11em!important;
  text-align:center!important;
  box-shadow:0 0 0 1.1rem rgba(201,255,74,.025)!important;
}
body[data-ux-family="service"] .stage109-case-diagram>span{
  position:absolute;
  z-index:2;
  min-width:6.8rem;
  padding:.58rem .7rem;
  border:1px solid var(--ds-line);
  border-radius:.72rem;
  background:rgba(15,19,24,.94);
  color:var(--ds-muted)!important;
  font:800 .63rem/1.2 ui-monospace,SFMono-Regular,Menlo,monospace!important;
  letter-spacing:.08em!important;
  text-align:center;
}
body[data-ux-family="service"] .stage109-case-diagram>span:nth-of-type(1){left:9%;top:18%}
body[data-ux-family="service"] .stage109-case-diagram>span:nth-of-type(2){right:9%;top:18%}
body[data-ux-family="service"] .stage109-case-diagram>span:nth-of-type(3){left:9%;bottom:18%}
body[data-ux-family="service"] .stage109-case-diagram>span:nth-of-type(4){right:9%;bottom:18%}

/* The three decision guides had a plain full-width final section while older guides use a CTA card. */
body[data-ux-family="guide"] main>.stage109-guide-endcap{
  padding-block:clamp(3rem,4.5vw,4rem)!important;
  background:transparent!important;
  border-top:1px solid var(--ds-line)!important;
}
body[data-ux-family="guide"] main>.stage109-guide-endcap>.container{
  width:var(--ds-shell,min(calc(100% - 2.4rem),1280px))!important;
  padding:clamp(1.45rem,3vw,2.35rem)!important;
  border:1px solid var(--ds-line)!important;
  border-radius:var(--ds-radius-lg)!important;
  background:linear-gradient(145deg,var(--ds-surface-2),var(--ds-surface))!important;
}
body[data-ux-family="guide"] .stage109-guide-endcap .section-head{margin-bottom:1.2rem!important}
body[data-ux-family="guide"] .stage109-guide-endcap .related{display:flex!important;flex-wrap:wrap!important;gap:.55rem!important}
body[data-ux-family="guide"] .stage109-guide-endcap .related a{
  min-height:2.35rem!important;
  display:inline-flex!important;
  align-items:center!important;
  padding:.55rem .75rem!important;
  border:1px solid var(--ds-line)!important;
  border-radius:.72rem!important;
  background:transparent!important;
  color:var(--ds-text)!important;
  text-decoration:none!important;
  font-size:.78rem!important;
  font-weight:800!important;
}
body[data-ux-family="guide"] .stage109-guide-endcap .related a[href*="t.me/Alexuys"]{
  margin-left:auto!important;
  border-color:var(--ds-accent)!important;
  background:var(--ds-accent)!important;
  color:#0a0d08!important;
}

/* Product pages get the same deliberate closing surface as service/case pages. */
body[data-ux-family="product"] main>.ux-product-contact.stage109-endcap{
  width:var(--ds-shell,min(calc(100% - 2.4rem),1280px))!important;
  margin:clamp(2.2rem,4vw,3.5rem) auto clamp(3rem,5vw,4.5rem)!important;
  padding:clamp(1.25rem,2.5vw,1.8rem)!important;
  border:1px solid var(--ds-line)!important;
  border-radius:var(--ds-radius-lg)!important;
  background:linear-gradient(145deg,var(--ds-surface-2),var(--ds-surface))!important;
}

@media(max-width:760px){
  body[data-ux-family="service"] .stage109-case-diagram{min-height:16rem!important}
  body[data-ux-family="service"] .stage109-case-diagram>b{width:6.8rem!important;height:6.8rem!important;font-size:.62rem!important}
  body[data-ux-family="service"] .stage109-case-diagram>span{min-width:5.4rem;padding:.48rem .55rem;font-size:.56rem!important}
  body[data-ux-family="service"] .stage109-case-diagram>span:nth-of-type(1),
  body[data-ux-family="service"] .stage109-case-diagram>span:nth-of-type(3){left:4%}
  body[data-ux-family="service"] .stage109-case-diagram>span:nth-of-type(2),
  body[data-ux-family="service"] .stage109-case-diagram>span:nth-of-type(4){right:4%}
  body[data-ux-family="guide"] .stage109-guide-endcap .related a{width:100%!important;justify-content:space-between!important}
  body[data-ux-family="guide"] .stage109-guide-endcap .related a[href*="t.me/Alexuys"]{margin-left:0!important}
}
'''

GENERIC_DIAGRAM_RE = re.compile(
    r'<div\s+aria-hidden=["\']true["\']\s+class=["\']s48-case__diagram["\']>'
    r'<i></i><i></i><i></i><b>REAL<br\s*/?>CASE</b></div>',
    re.I,
)


def proof_visual(center: str, labels: tuple[str, str, str, str]) -> str:
    nodes = ''.join(f'<span>{label}</span>' for label in labels)
    return (
        '<div aria-hidden="true" class="s48-case__diagram stage109-case-diagram">'
        f'{nodes}<b>{center}</b></div>'
    )


def replace_proof_visuals() -> list[str]:
    changed = []
    for rel, (center, labels) in PROOF_VISUALS.items():
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f'stage109: missing proof page {rel}')
        text = path.read_text(encoding='utf-8')
        new, count = GENERIC_DIAGRAM_RE.subn(proof_visual(center, labels), text, count=1)
        if count != 1:
            raise SystemExit(f'stage109: expected one generic proof diagram in {rel}, got {count}')
        if new != text:
            path.write_text(new, encoding='utf-8')
            changed.append(rel)
    return changed


def fix_english_project_repair() -> bool:
    path = ROOT / 'en/project-repair/index.html'
    if not path.is_file():
        raise SystemExit('stage109: en/project-repair missing')
    text = path.read_text(encoding='utf-8')
    old = text
    # Stage108's fallback can mistake the hero Telegram action for the page ending.
    text = re.sub(
        r'(<section\b[^>]*class=["\'][^"\']*\bintl-hero\b[^"\']*)\s+stage108-endcap([^"\']*["\'])',
        r'\1\2', text, count=1, flags=re.I,
    )
    marker = 'data-stage109-project-repair-cta="true"'
    if marker not in text:
        cta = (
            '<section class="intl-container intl-section stage109-endcap" '
            'data-stage109-project-repair-cta="true">'
            '<div class="intl-cta-box"><div><h2>Have an existing project? <em>Send the problem as it is.</em></h2>'
            '<p>A repository link, screenshots, error text or a short description is enough to start with a focused diagnosis.</p></div>'
            '<a class="intl-btn primary" href="https://t.me/Alexuys" rel="noreferrer noopener" target="_blank">Message in Telegram ↗</a>'
            '</div></section>'
        )
        text, count = re.subn(r'</main>', cta + '</main>', text, count=1, flags=re.I)
        if count != 1:
            raise SystemExit('stage109: cannot append en/project-repair CTA')
    if text != old:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def fix_freelance_os() -> bool:
    path = ROOT / 'freelance-os/index.html'
    if not path.is_file():
        raise SystemExit('stage109: freelance-os missing')
    text = path.read_text(encoding='utf-8')
    old = text
    blocks = list(re.finditer(
        r'<details\b(?=[^>]*class=["\'][^"\']*\bux-seo-more\b[^"\']*["\'])[^>]*>.*?</details>',
        text, re.I | re.S,
    ))
    if len(blocks) >= 2:
        replacements = [
            'Когда local-first CRM подходит',
            'Как устроен FreelanceOS',
        ]
        for match, label in reversed(list(zip(blocks[:2], replacements))):
            block = match.group(0)
            block, count = re.subn(r'<summary>.*?</summary>', f'<summary>{label}</summary>', block, count=1, flags=re.I | re.S)
            if count != 1:
                raise SystemExit('stage109: freelance-os detail summary missing')
            text = text[:match.start()] + block + text[match.end():]
    text, _ = re.subn(
        r'<div\b(?=[^>]*class=["\'][^"\']*\bux-product-contact\b)([^>]*)class=["\']([^"\']*)["\']([^>]*)>',
        lambda m: '<div' + m.group(1) + 'class="' + (' '.join((m.group(2) + ' stage109-endcap').split())) + '"' + m.group(3) + '>',
        text, count=1, flags=re.I | re.S,
    )
    if text != old:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def mark_new_guide_endings() -> list[str]:
    changed = []
    for rel in (
        'guides/n8n-vs-backend/index.html',
        'guides/repair-vs-rewrite/index.html',
        'guides/site-vs-web-app/index.html',
    ):
        path = ROOT / rel
        text = path.read_text(encoding='utf-8')
        new, count = re.subn(
            r'<section class="section stage108-endcap">',
            '<section class="section stage108-endcap stage109-guide-endcap">',
            text, count=1,
        )
        if count != 1:
            raise SystemExit(f'stage109: guide endcap missing in {rel}')
        if new != text:
            path.write_text(new, encoding='utf-8')
            changed.append(rel)
    return changed


if not STYLE_PATH.is_file():
    raise SystemExit('stage109: stage98 design source missing')
styles = STYLE_PATH.read_text(encoding='utf-8')
if STYLE_MARK not in styles:
    STYLE_PATH.write_text(styles.rstrip() + '\n\n' + CSS.strip() + '\n', encoding='utf-8')

proof_changed = replace_proof_visuals()
repair_changed = fix_english_project_repair()
product_changed = fix_freelance_os()
guide_changed = mark_new_guide_endings()

# Invariants for the lappies this pass exists to remove.
problems: list[str] = []
for rel in PROOF_VISUALS:
    text = (ROOT / rel).read_text(encoding='utf-8')
    if 'REAL<br/>CASE' in text or 'REAL<br>CASE' in text:
        problems.append(f'{rel}: generic REAL CASE visual remains')
    if text.count('stage109-case-diagram') != 1:
        problems.append(f'{rel}: route-specific proof visual missing/duplicated')

repair = (ROOT / 'en/project-repair/index.html').read_text(encoding='utf-8')
main = re.search(r'<main\b[^>]*>(.*?)</main>', repair, re.I | re.S)
if not main or 'data-stage109-project-repair-cta="true"' not in main.group(1):
    problems.append('en/project-repair: final CTA missing')
else:
    last_section = list(re.finditer(r'<section\b', main.group(1), re.I))[-1]
    if main.group(1).find('data-stage109-project-repair-cta="true"', last_section.start()) < 0:
        problems.append('en/project-repair: CTA is not final section')

fos = (ROOT / 'freelance-os/index.html').read_text(encoding='utf-8')
if fos.count('<summary>Подробнее о реализации и архитектуре</summary>'):
    problems.append('freelance-os: duplicated generic detail summary remains')
if 'ux-product-contact stage109-endcap' not in fos and 'stage109-endcap ux-product-contact' not in fos:
    problems.append('freelance-os: product contact not marked as endcap')

for rel in guide_changed or (
    'guides/n8n-vs-backend/index.html',
    'guides/repair-vs-rewrite/index.html',
    'guides/site-vs-web-app/index.html',
):
    if 'stage109-guide-endcap' not in (ROOT / rel).read_text(encoding='utf-8'):
        problems.append(f'{rel}: guide CTA surface missing')

if STYLE_MARK not in STYLE_PATH.read_text(encoding='utf-8'):
    problems.append('stage109 styles missing')
if problems:
    raise SystemExit('stage109 consistency failed:\n' + '\n'.join(problems))

print(
    'stage109 consistency: '
    f'proof_visuals={len(proof_changed)}; en_project_repair={int(repair_changed)}; '
    f'freelance_os={int(product_changed)}; guide_endings={len(guide_changed)}'
)
