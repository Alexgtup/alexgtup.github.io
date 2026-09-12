#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
BUNDLE = ROOT / 'assets' / 'stage105-final-ui.css'
MARK = '/* stage117-visual-maturity */'

CSS = r'''
/* stage117-visual-maturity
   Final art-direction layer. The goal is restraint: fewer template-like effects,
   stronger hierarchy, calmer surfaces and more editorial project presentation. */

:root{
  --vm-radius-xs:.7rem;
  --vm-radius-sm:.95rem;
  --vm-radius-md:1.25rem;
  --vm-radius-lg:1.65rem;
  --vm-line:rgba(255,255,255,.10);
  --vm-line-strong:rgba(255,255,255,.18);
  --vm-surface:rgba(255,255,255,.025);
  --vm-surface-hover:rgba(255,255,255,.045);
  --vm-shadow:0 22px 60px rgba(0,0,0,.22);
}

/* Reduce the generic neon/template look site-wide. */
body[data-ux-family] :is(.card,.project,.service-card,.case-card,.case-library-card,.dt-tool-card,.s48-card,.s50-card){
  box-shadow:none!important;
}
body[data-ux-family] :is(.card,.project,.service-card,.case-card,.case-library-card,.dt-tool-card,.s48-card,.s50-card){
  transition:transform .24s cubic-bezier(.2,.7,.2,1),border-color .24s ease,background-color .24s ease!important;
}
body[data-ux-family] :is(.card,.project,.service-card,.case-card,.case-library-card,.dt-tool-card,.s48-card,.s50-card):hover{
  transform:translateY(-2px)!important;
}

/* HOME — treat the page as a developer portfolio, not a SaaS template. */
body[data-page="home"] .site{
  background:
    radial-gradient(circle at 78% 3%,rgba(129,149,255,.055),transparent 27rem),
    linear-gradient(180deg,#090a0c 0%,#08090b 58%,#090a0c 100%)!important;
}
body[data-page="home"] .site::before{
  opacity:.32!important;
  background-size:92px 92px!important;
}
body[data-page="home"] .site::after{
  opacity:.34!important;
  filter:blur(34px)!important;
}
body[data-page="home"] .header{
  backdrop-filter:blur(18px) saturate(112%)!important;
}
body[data-page="home"] .header-inner{
  min-height:4.6rem!important;
}
body[data-page="home"] .nav{gap:1.45rem!important}
body[data-page="home"] .nav a{
  font-size:.82rem!important;
  color:#a9afb6!important;
}
body[data-page="home"] .nav a:hover{color:#f4f5f2!important}

body[data-page="home"] .hero{
  padding-top:clamp(4.6rem,8.5vw,8.5rem)!important;
  padding-bottom:clamp(4.7rem,8vw,7.7rem)!important;
}
body[data-page="home"] .hero-grid{
  grid-template-columns:minmax(0,1.02fr) minmax(25rem,.78fr)!important;
  gap:clamp(3rem,7vw,8rem)!important;
  align-items:center!important;
}
body[data-page="home"] .eyebrow{
  color:#9299a2!important;
  letter-spacing:.095em!important;
  font-size:.66rem!important;
}
body[data-page="home"] .eyebrow-dot{
  width:.38rem!important;height:.38rem!important;
  box-shadow:none!important;
}
body[data-page="home"] .hero h1{
  margin-top:1.35rem!important;
  max-width:11.8ch!important;
  font-size:clamp(4rem,7.7vw,8rem)!important;
  line-height:.895!important;
  letter-spacing:-.072em!important;
  font-weight:690!important;
}
body[data-page="home"] .hero h1 .soft{color:#727982!important}
body[data-page="home"] .hero-copy{
  max-width:34rem!important;
  margin-top:1.8rem!important;
  color:#a0a6ae!important;
  font-size:clamp(1rem,1.35vw,1.12rem)!important;
  line-height:1.72!important;
}
body[data-page="home"] .hero-tags{
  margin-top:1.7rem!important;
  gap:.55rem!important;
  color:#8f969f!important;
  font-size:.67rem!important;
  letter-spacing:.025em!important;
}
body[data-page="home"] .hero-actions{margin-top:2.25rem!important;gap:.65rem!important}
body[data-page="home"] .button{
  min-height:3.05rem!important;
  border-radius:.78rem!important;
  font-size:.86rem!important;
  box-shadow:none!important;
}
body[data-page="home"] .button.primary{
  background:#d0ff5a!important;
  border-color:#d0ff5a!important;
  box-shadow:none!important;
}
body[data-page="home"] .button.primary:hover{background:#dcff7a!important}

/* Hero product visual: flatter, more believable, less decorative. */
body[data-page="home"] .product-stage{
  min-height:32rem!important;
  perspective:none!important;
}
body[data-page="home"] .stage-glow{
  opacity:.34!important;
  inset:15% 7%!important;
  filter:blur(42px)!important;
}
body[data-page="home"] .stage-browser{
  left:2%!important;
  top:4.1rem!important;
  width:91%!important;
  height:24rem!important;
  border-color:rgba(255,255,255,.15)!important;
  border-radius:1.05rem!important;
  background:#101216!important;
  box-shadow:0 28px 70px rgba(0,0,0,.32),inset 0 1px rgba(255,255,255,.035)!important;
  transform:none!important;
}
body[data-page="home"] .browser-top{height:2.75rem!important}
body[data-page="home"] .browser-body{height:calc(100% - 2.75rem)!important}
body[data-page="home"] .kpi{
  border-color:rgba(255,255,255,.075)!important;
  background:#111318!important;
  border-radius:.62rem!important;
}
body[data-page="home"] .dash-chip{
  border-radius:.5rem!important;
  border-color:rgba(255,255,255,.09)!important;
}

/* Sections should read as editorial chapters rather than stacked card bands. */
body[data-page="home"] main>section:not(.hero){
  padding-top:clamp(4.8rem,8vw,8.2rem)!important;
  padding-bottom:clamp(4.8rem,8vw,8.2rem)!important;
}
body[data-page="home"] .section-heading,
body[data-page="home"] .section-head{
  margin-bottom:clamp(2rem,4vw,3.6rem)!important;
}
body[data-page="home"] :is(.section-heading,.section-head) h2{
  font-weight:660!important;
  letter-spacing:-.052em!important;
  line-height:.98!important;
}
body[data-page="home"] :is(.section-heading,.section-head) p{
  color:#8f969f!important;
  line-height:1.7!important;
}

/* Project cards: stronger media hierarchy, quieter chrome. */
body[data-page="home"] :is(.case-card,.project-card,.project){
  border-color:rgba(255,255,255,.095)!important;
  background:rgba(255,255,255,.018)!important;
  border-radius:var(--vm-radius-lg)!important;
  overflow:hidden!important;
}
body[data-page="home"] :is(.case-card,.project-card,.project):hover{
  border-color:rgba(255,255,255,.19)!important;
  background:rgba(255,255,255,.028)!important;
}
body[data-page="home"] :is(.case-card,.project-card,.project) img{
  transition:transform .55s cubic-bezier(.2,.7,.2,1),filter .35s ease!important;
}
body[data-page="home"] :is(.case-card,.project-card,.project):hover img{
  transform:scale(1.012)!important;
}

/* Shared project/case library: premium editorial restraint. */
body[data-page="cases"] .case-library-card{
  border-color:rgba(255,255,255,.10)!important;
  background:rgba(255,255,255,.018)!important;
  border-radius:1.45rem!important;
  box-shadow:none!important;
}
body[data-page="cases"] .case-library-card:hover{
  border-color:rgba(255,255,255,.20)!important;
  background:rgba(255,255,255,.026)!important;
  transform:translateY(-3px)!important;
}
body[data-page="cases"] .case-library-card__media{
  background:#0d0f12!important;
}
body[data-page="cases"] .case-library-card__body{
  padding:clamp(1.2rem,2vw,1.55rem)!important;
}
body[data-page="cases"] .case-library-card__meta,
body[data-page="cases"] .case-library-card__tags{
  color:#858c95!important;
}
body[data-page="cases"] .case-library-card h3{
  letter-spacing:-.035em!important;
  line-height:1.05!important;
}

/* Service pages: remove dashboard/template feel from generic proof cards. */
body[data-ux-family="service"] :is(.s48-card,.s48-proof,.s48-case,.stage109-case-diagram){
  border-radius:1.2rem!important;
  box-shadow:none!important;
}
body[data-ux-family="service"] .stage109-case-diagram{
  background:
    linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.018) 1px,transparent 1px),
    #0d0f12!important;
  background-size:48px 48px,48px 48px,auto!important;
}
body[data-ux-family="service"] .stage109-case-diagram>b{
  box-shadow:none!important;
  border-color:rgba(201,255,74,.22)!important;
  background:#101216!important;
}
body[data-ux-family="service"] .stage109-case-diagram>span{
  border-color:rgba(255,255,255,.09)!important;
  background:#111318!important;
}

/* Calm repeated chips and micro-UI. */
body[data-ux-family] :is(.chip,.tag,.pill,.badge,.case-library-card__badge){
  box-shadow:none!important;
}

/* Light theme receives the same hierarchy without forced dark surfaces. */
html[data-theme="light"] body[data-page="home"] .site{
  background:linear-gradient(180deg,#f8f8f6 0%,#f4f4f1 100%)!important;
}
html[data-theme="light"] body[data-page="home"] .hero h1 .soft{color:#83878c!important}
html[data-theme="light"] body[data-page="home"] .stage-browser{
  background:#fff!important;
  border-color:rgba(16,18,20,.12)!important;
  box-shadow:0 28px 70px rgba(30,34,38,.10)!important;
}
html[data-theme="light"] body[data-page="home"] .kpi{background:#fafafa!important;border-color:rgba(16,18,20,.08)!important}
html[data-theme="light"] body[data-page="home"] :is(.case-card,.project-card,.project),
html[data-theme="light"] body[data-page="cases"] .case-library-card{
  background:rgba(255,255,255,.55)!important;
  border-color:rgba(16,18,20,.10)!important;
}

@media(max-width:980px){
  body[data-page="home"] .hero-grid{
    grid-template-columns:1fr!important;
    gap:3.2rem!important;
  }
  body[data-page="home"] .hero h1{max-width:10.8ch!important}
  body[data-page="home"] .product-stage{min-height:29rem!important;max-width:44rem!important}
  body[data-page="home"] .stage-browser{width:96%!important;left:2%!important}
}

@media(max-width:680px){
  body[data-page="home"] .hero{
    padding-top:3.4rem!important;
    padding-bottom:4.3rem!important;
  }
  body[data-page="home"] .hero h1{
    max-width:100%!important;
    font-size:clamp(3.15rem,15.3vw,4.55rem)!important;
    line-height:.91!important;
    letter-spacing:-.065em!important;
  }
  body[data-page="home"] .hero-copy{
    font-size:.98rem!important;
    line-height:1.64!important;
  }
  body[data-page="home"] .hero-tags{line-height:1.7!important}
  body[data-page="home"] .product-stage{min-height:23.5rem!important}
  body[data-page="home"] .stage-browser{
    top:2rem!important;
    height:20rem!important;
    border-radius:.85rem!important;
  }
  body[data-page="home"] main>section:not(.hero){
    padding-top:4.2rem!important;
    padding-bottom:4.2rem!important;
  }
}

@media(prefers-reduced-motion:reduce){
  body[data-page="home"] :is(.case-card,.project-card,.project) img,
  body[data-ux-family] :is(.card,.project,.service-card,.case-card,.case-library-card,.dt-tool-card,.s48-card,.s50-card){
    transition:none!important;
  }
}
'''

if not BUNDLE.is_file():
    raise SystemExit('stage117: final UI bundle missing')

text = BUNDLE.read_text(encoding='utf-8')
if MARK not in text:
    text = text.rstrip() + '\n\n' + CSS.strip() + '\n'
    BUNDLE.write_text(text, encoding='utf-8')

bundle_text = BUNDLE.read_text(encoding='utf-8')
digest = hashlib.sha256(bundle_text.encode('utf-8')).hexdigest()[:12]
href_re = re.compile(r'(/assets/stage105-final-ui\\.css)\\?v=[^"\\']+', re.I)

pages = 0
refs = 0
home_seen = False
cases_seen = False
service_seen = False
for path in sorted(ROOT.rglob('*.html')):
    html = path.read_text(encoding='utf-8', errors='ignore')
    if '<body' not in html:
        continue
    pages += 1
    home_seen = home_seen or 'data-page="home"' in html
    cases_seen = cases_seen or 'data-page="cases"' in html
    service_seen = service_seen or 'data-ux-family="service"' in html
    new, count = href_re.subn(rf'\\1?v={digest}', html)
    refs += count
    if new != html:
        path.write_text(new, encoding='utf-8')

problems: list[str] = []
if MARK not in BUNDLE.read_text(encoding='utf-8'):
    problems.append('visual maturity CSS marker missing')
if not home_seen:
    problems.append('home page marker not found')
if not cases_seen:
    problems.append('cases page marker not found')
if not service_seen:
    problems.append('service family marker not found')
if refs < 70:
    problems.append(f'only {refs} final UI references rotated')

if problems:
    raise SystemExit('stage117 visual maturity failed:\n' + '\n'.join(problems))

print(f'stage117 visual maturity: pages={pages}; cache_refs={refs}; bundle={digest}; home/cases/services art direction applied')
