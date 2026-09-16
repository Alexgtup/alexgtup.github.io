#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage150-premium-glass-polish"

STYLE = r'''<style id="stage150-premium-glass-polish">
:root{
  --x150-glass:rgba(14,18,22,.64);
  --x150-glass-soft:rgba(255,255,255,.045);
  --x150-glass-strong:rgba(16,20,25,.78);
  --x150-border:rgba(255,255,255,.115);
  --x150-border-hi:rgba(255,255,255,.18);
  --x150-shadow:0 26px 80px rgba(0,0,0,.30),inset 0 1px 0 rgba(255,255,255,.055);
  --x150-radius:28px;
}

/* One restrained glass language across the portfolio. */
.stage98-header,
.header.stage98-header{
  background:rgba(7,9,12,.68)!important;
  border-bottom:1px solid rgba(255,255,255,.08)!important;
  -webkit-backdrop-filter:blur(24px) saturate(138%)!important;
  backdrop-filter:blur(24px) saturate(138%)!important;
  box-shadow:0 12px 42px rgba(0,0,0,.16)!important;
}

:is(
  .p128-feature,.p128-proof,.p128-form,
  .p129-svc-board,.p129-case-card,.p129-contact-card,
  .p130-featured-card,.p130-tile,.p130-footer-cta>div,
  .p132-cover-visual,.p132-panel .card,.p132-panel .feature,.p132-panel .shot,
  .p132-panel .note,.p132-panel .demo,.p132-panel .related a,.p132-end .cta-box,
  .s75-author__inner,.search-demand__card,
  .case-card,.project-card,.service-card,.guide-card,.review-card,.process-card,.metrics-card
){
  border-color:var(--x150-border)!important;
  background:
    linear-gradient(145deg,rgba(255,255,255,.072),rgba(255,255,255,.025) 42%,rgba(9,12,16,.56)),
    var(--x150-glass)!important;
  -webkit-backdrop-filter:blur(22px) saturate(132%)!important;
  backdrop-filter:blur(22px) saturate(132%)!important;
  box-shadow:var(--x150-shadow)!important;
}

:is(.p128-feature,.p129-case-card,.p130-featured-card,.p130-tile,.p132-cover-visual,.case-card,.project-card,.service-card,.guide-card){
  overflow:hidden;
}

/* Case covers: give copy room first; visual supports the story instead of squeezing it. */
body[data-x135-family="cinematic"] .p132-case .p132-cover{
  min-height:0!important;
  padding:clamp(62px,6.2vw,94px) 0 clamp(68px,7vw,108px)!important;
}
body[data-x135-family="cinematic"] .p132-case .p132-shell.p132-cover-grid{
  display:grid!important;
  grid-template-columns:minmax(0,1.22fr) minmax(380px,.78fr)!important;
  width:min(1320px,calc(100% - 64px))!important;
  max-width:1320px!important;
  margin:0 auto!important;
  padding:0!important;
  gap:clamp(36px,4.6vw,68px)!important;
  align-items:center!important;
  justify-content:normal!important;
  transform:none!important;
}
body[data-x135-family="cinematic"] .p132-case .p132-cover-copy{
  width:100%!important;
  max-width:760px!important;
  min-width:0!important;
  margin:0!important;
  padding:0!important;
  flex:none!important;
  order:1!important;
  justify-self:start!important;
}
body[data-x135-family="cinematic"] .p132-case .p132-cover h1{
  max-width:10.8ch!important;
  margin:.8rem 0 1.25rem!important;
  font-size:clamp(62px,6vw,104px)!important;
  line-height:.88!important;
  letter-spacing:-.062em!important;
  text-wrap:balance!important;
  overflow-wrap:normal!important;
  word-break:normal!important;
}
body[data-x135-family="cinematic"] .p132-case .p132-cover-copy>p:not(.p132-eyebrow){
  width:100%!important;
  max-width:62ch!important;
  margin-top:1.35rem!important;
  color:rgba(230,236,239,.78)!important;
  font-size:clamp(17px,1.28vw,20px)!important;
  line-height:1.72!important;
  text-wrap:pretty!important;
}
body[data-x135-family="cinematic"] .p132-case .p132-cover-actions{
  margin-top:1.9rem!important;
  gap:.8rem 1rem!important;
}
body[data-x135-family="cinematic"] .p132-case .p132-cover-visual{
  width:100%!important;
  max-width:520px!important;
  min-width:0!important;
  min-height:0!important;
  aspect-ratio:16/11!important;
  order:2!important;
  justify-self:end!important;
  align-self:center!important;
  flex:none!important;
  margin:0!important;
  border-radius:var(--x150-radius)!important;
  transform:none!important;
  animation:none!important;
}
body[data-x135-family="cinematic"] .p132-case .p132-cover-visual img{
  width:100%!important;
  height:100%!important;
  object-fit:cover!important;
  transform:none!important;
}

/* Readable case story: labels stay compact, content gets real line length. */
body[data-x135-family="cinematic"] .p132-case>.p132-panel .section-head{
  display:grid!important;
  grid-template-columns:minmax(96px,.22fr) minmax(0,1.78fr)!important;
  gap:clamp(24px,4vw,58px)!important;
  align-items:start!important;
}
body[data-x135-family="cinematic"] .p132-case>.p132-panel .section-head>div:last-child{
  width:100%!important;
  max-width:940px!important;
}
body[data-x135-family="cinematic"] .p132-case>.p132-panel .section-head h2{
  max-width:17ch!important;
  text-wrap:balance!important;
}
body[data-x135-family="cinematic"] .p132-case>.p132-panel :is(.copy,.lead,.note,p){
  text-wrap:pretty;
}
body[data-x135-family="cinematic"] .p132-case>.p132-panel .copy{
  max-width:68ch!important;
  font-size:clamp(16px,1.1vw,18px)!important;
  line-height:1.75!important;
}
body[data-x135-family="cinematic"] .p132-case>.p132-panel :is(.card,.feature,.shot,.note,.demo,.related a){
  border-radius:clamp(18px,2vw,26px)!important;
}
body[data-x135-family="cinematic"] .p132-case>.p132-panel :is(.card,.feature){
  padding:clamp(18px,2vw,26px)!important;
}

/* Legacy case layouts that do not yet use p132 receive the same width correction. */
body[data-ux-family="case"] .hero-grid{
  grid-template-columns:minmax(0,1.16fr) minmax(340px,.84fr)!important;
  gap:clamp(32px,5vw,72px)!important;
}
body[data-ux-family="case"] .hero-grid>div:first-child{
  min-width:0!important;
  max-width:760px!important;
}
body[data-ux-family="case"] .hero-grid :is(.lead,p){max-width:62ch!important;text-wrap:pretty}
body[data-ux-family="case"] :is(.visual,.demo,.shot,.cta-box,.contact-card,.card,.feature,.related a){
  border-color:var(--x150-border)!important;
  background:
    linear-gradient(145deg,rgba(255,255,255,.07),rgba(255,255,255,.022)),
    rgba(12,16,20,.68)!important;
  -webkit-backdrop-filter:blur(20px) saturate(130%)!important;
  backdrop-filter:blur(20px) saturate(130%)!important;
  box-shadow:var(--x150-shadow)!important;
}

/* Subtle depth, never a flashy gimmick. */
@media (hover:hover) and (pointer:fine){
  :is(.p128-feature,.p129-case-card,.p130-tile,.p132-panel .card,.p132-panel .feature,.case-card,.project-card,.service-card,.guide-card){
    transition:transform .28s ease,border-color .28s ease,box-shadow .28s ease!important;
  }
  :is(.p128-feature,.p129-case-card,.p130-tile,.p132-panel .card,.p132-panel .feature,.case-card,.project-card,.service-card,.guide-card):hover{
    transform:translateY(-3px)!important;
    border-color:var(--x150-border-hi)!important;
    box-shadow:0 30px 90px rgba(0,0,0,.34),inset 0 1px 0 rgba(255,255,255,.08)!important;
  }
}

@media(max-width:1100px){
  body[data-x135-family="cinematic"] .p132-case .p132-shell.p132-cover-grid{
    grid-template-columns:minmax(0,1.08fr) minmax(340px,.92fr)!important;
    width:min(100% - 42px,1100px)!important;
    gap:34px!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover h1{font-size:clamp(58px,7vw,86px)!important}
  body[data-x135-family="cinematic"] .p132-case .p132-cover-visual{max-width:470px!important}
}

@media(max-width:900px){
  body[data-x135-family="cinematic"] .p132-case .p132-shell.p132-cover-grid,
  body[data-ux-family="case"] .hero-grid{
    display:grid!important;
    grid-template-columns:1fr!important;
    width:min(100% - 32px,780px)!important;
    gap:32px!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-copy,
  body[data-x135-family="cinematic"] .p132-case .p132-cover-visual{
    width:100%!important;
    max-width:none!important;
    justify-self:stretch!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover h1{
    max-width:12ch!important;
    font-size:clamp(54px,10vw,82px)!important;
  }
  body[data-x135-family="cinematic"] .p132-case>.p132-panel .section-head{
    grid-template-columns:1fr!important;
    gap:12px!important;
  }
}

@media(max-width:600px){
  body[data-x135-family="cinematic"] .p132-case .p132-shell.p132-cover-grid,
  body[data-ux-family="case"] .hero-grid{width:calc(100% - 24px)!important}
  body[data-x135-family="cinematic"] .p132-case .p132-cover{padding:38px 0 58px!important}
  body[data-x135-family="cinematic"] .p132-case .p132-cover h1{
    max-width:100%!important;
    font-size:clamp(46px,13vw,66px)!important;
    line-height:.9!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-copy>p:not(.p132-eyebrow){
    max-width:100%!important;
    font-size:16px!important;
    line-height:1.68!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-visual{border-radius:20px!important;aspect-ratio:16/10!important}
  :is(.p128-feature,.p129-svc-board,.p129-case-card,.p130-featured-card,.p130-tile,.p132-cover-visual,.p132-panel .card,.p132-panel .feature,.p132-panel .shot,.p132-panel .note,.p132-panel .demo,.case-card,.project-card,.service-card,.guide-card){
    -webkit-backdrop-filter:blur(16px) saturate(125%)!important;
    backdrop-filter:blur(16px) saturate(125%)!important;
  }
}

@media(prefers-reduced-motion:reduce){
  :is(.p128-feature,.p129-case-card,.p130-tile,.p132-panel .card,.p132-panel .feature,.case-card,.project-card,.service-card,.guide-card){transition:none!important;transform:none!important}
}
</style>'''

changed = []
for path in sorted(ROOT.rglob("index.html")):
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        continue
    if "</head>" not in text:
        continue
    text = text.replace("</head>", STYLE + "</head>", 1)
    path.write_text(text, encoding="utf-8")
    changed.append(path)

case_pages = sorted((ROOT / "cases").glob("*/index.html")) if (ROOT / "cases").is_dir() else []
if not case_pages:
    raise SystemExit("stage150: no case pages found")
for path in case_pages:
    final = path.read_text(encoding="utf-8")
    if MARKER not in final:
        raise SystemExit(f"stage150: premium layer missing: {path}")

print(f"stage150 premium glass polish: {len(changed)} pages, {len(case_pages)} case pages guarded")
