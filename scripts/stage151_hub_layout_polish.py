#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage151-hub-layout-polish"

STYLE = r'''<style id="stage151-hub-layout-polish">
/* Final hub pass: readable composition first, decorative art second. */
body[data-x135-family="cinematic"] .p130-hub .p130-hero{
  min-height:0!important;
  padding:clamp(64px,6.5vw,98px) 0 clamp(70px,7vw,108px)!important;
  background:
    radial-gradient(38rem 28rem at 86% 22%,rgba(201,255,74,.07),transparent 68%),
    radial-gradient(32rem 24rem at 12% 108%,rgba(102,228,255,.055),transparent 68%),
    #080b0d!important;
  overflow:hidden!important;
}

/* Retire the giant pseudo-art panels that consumed half of the first viewport. */
body[data-x135-family="cinematic"] .p130-hub .p130-hero::before,
body[data-x135-family="cinematic"] .p130-hub .p130-hero::after{
  display:none!important;
  content:none!important;
  animation:none!important;
}

body[data-x135-family="cinematic"] .p130-hub .p130-shell.p130-hero-grid{
  width:min(1260px,calc(100% - 64px))!important;
  max-width:1260px!important;
  margin-inline:auto!important;
  display:grid!important;
  grid-template-columns:minmax(0,1.38fr) minmax(300px,.62fr)!important;
  gap:clamp(38px,5vw,72px)!important;
  align-items:center!important;
  transform:none!important;
}

body[data-x135-family="cinematic"] .p130-hub .p130-hero-grid>div:first-child{
  width:100%!important;
  max-width:820px!important;
  min-width:0!important;
}

body[data-x135-family="cinematic"] .p130-hub .p130-hero h1{
  width:100%!important;
  max-width:13.5ch!important;
  margin:.8rem 0 1.3rem!important;
  font-size:clamp(62px,6.1vw,100px)!important;
  line-height:.91!important;
  letter-spacing:-.058em!important;
  text-wrap:balance!important;
  overflow-wrap:normal!important;
  word-break:normal!important;
}

body[data-x135-family="cinematic"] .p130-hub .p130-lead{
  width:100%!important;
  max-width:60ch!important;
  margin:1.15rem 0 0!important;
  color:rgba(226,233,236,.76)!important;
  font-size:clamp(17px,1.25vw,20px)!important;
  line-height:1.72!important;
  text-wrap:pretty!important;
}

body[data-x135-family="cinematic"] .p130-hub .p130-hero-side{
  width:100%!important;
  min-width:0!important;
  align-self:center!important;
  padding:clamp(22px,2.5vw,30px)!important;
  border:1px solid rgba(255,255,255,.115)!important;
  border-radius:26px!important;
  background:
    linear-gradient(145deg,rgba(255,255,255,.075),rgba(255,255,255,.026) 48%,rgba(8,11,14,.58)),
    rgba(14,18,22,.66)!important;
  -webkit-backdrop-filter:blur(22px) saturate(132%)!important;
  backdrop-filter:blur(22px) saturate(132%)!important;
  box-shadow:0 24px 72px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.06)!important;
  color:rgba(224,231,235,.72)!important;
  font-size:15px!important;
  line-height:1.7!important;
}
body[data-x135-family="cinematic"] .p130-hub .p130-hero-side strong{
  color:#f5f7f4!important;
  font-size:clamp(18px,1.5vw,22px)!important;
  line-height:1.2!important;
  margin-bottom:.75rem!important;
}

/* Hub headings should open the section instead of floating in a narrow column. */
body[data-x135-family="cinematic"] .p130-hub .p129-section-head{
  display:grid!important;
  grid-template-columns:minmax(120px,.24fr) minmax(0,1.76fr)!important;
  gap:clamp(24px,4vw,56px)!important;
  align-items:end!important;
  margin-bottom:clamp(28px,4vw,48px)!important;
}
body[data-x135-family="cinematic"] .p130-hub .p129-section-head h2{
  max-width:18ch!important;
  margin:0!important;
  font-size:clamp(40px,4.2vw,66px)!important;
  line-height:.96!important;
  text-wrap:balance!important;
}

/* Services/guides/freelance: turn long scan-lines into premium task cards. */
body[data-x135-family="cinematic"] .p130-hub .p130-list{
  display:grid!important;
  grid-template-columns:repeat(2,minmax(0,1fr))!important;
  gap:14px!important;
  border-top:0!important;
}
body[data-x135-family="cinematic"] .p130-hub .p130-row{
  min-width:0!important;
  min-height:168px!important;
  display:grid!important;
  grid-template-columns:42px minmax(0,1fr) 28px!important;
  grid-template-rows:auto 1fr!important;
  gap:10px 14px!important;
  align-content:start!important;
  align-items:start!important;
  padding:24px!important;
  border:1px solid rgba(255,255,255,.105)!important;
  border-radius:24px!important;
  background:
    linear-gradient(145deg,rgba(255,255,255,.068),rgba(255,255,255,.022) 48%,rgba(8,11,14,.52)),
    rgba(13,17,21,.66)!important;
  -webkit-backdrop-filter:blur(20px) saturate(130%)!important;
  backdrop-filter:blur(20px) saturate(130%)!important;
  box-shadow:0 20px 58px rgba(0,0,0,.24),inset 0 1px 0 rgba(255,255,255,.05)!important;
  text-decoration:none!important;
  transform:none!important;
}
body[data-x135-family="cinematic"] .p130-hub .p130-row>span:first-child{
  grid-column:1!important;
  grid-row:1 / span 2!important;
  color:rgba(201,255,74,.76)!important;
  padding-top:.25rem!important;
}
body[data-x135-family="cinematic"] .p130-hub .p130-row strong{
  grid-column:2!important;
  grid-row:1!important;
  min-width:0!important;
  font-size:clamp(22px,2vw,31px)!important;
  line-height:1.02!important;
  letter-spacing:-.04em!important;
  text-wrap:balance!important;
}
body[data-x135-family="cinematic"] .p130-hub .p130-row em{
  grid-column:2!important;
  grid-row:2!important;
  min-width:0!important;
  color:rgba(218,226,230,.68)!important;
  font-size:15px!important;
  line-height:1.6!important;
  text-wrap:pretty!important;
}
body[data-x135-family="cinematic"] .p130-hub .p130-row b{
  grid-column:3!important;
  grid-row:1!important;
  justify-self:end!important;
  color:#c9ff4a!important;
}

/* Supporting blocks get the same matte-glass system. */
body[data-x135-family="cinematic"] .p130-hub :is(
  .p130-featured-card,
  .x146-depth__card,
  .secondary-demand__card,
  .p131-bridge__inner,
  .p130-proof-stack>div,
  .p130-proof-stack>a
){
  border-color:rgba(255,255,255,.11)!important;
  background:
    linear-gradient(145deg,rgba(255,255,255,.07),rgba(255,255,255,.024) 45%,rgba(8,11,14,.54)),
    rgba(13,17,21,.66)!important;
  -webkit-backdrop-filter:blur(20px) saturate(130%)!important;
  backdrop-filter:blur(20px) saturate(130%)!important;
  box-shadow:0 22px 68px rgba(0,0,0,.26),inset 0 1px 0 rgba(255,255,255,.055)!important;
}

body[data-x135-family="cinematic"] .p130-hub .p130-featured-card{
  border-radius:28px!important;
  grid-template-columns:minmax(0,1.18fr) minmax(320px,.82fr)!important;
  min-height:440px!important;
}
body[data-x135-family="cinematic"] .p130-hub .p130-featured-media{min-height:440px!important}
body[data-x135-family="cinematic"] .p130-hub .p130-featured-copy{
  padding:clamp(30px,4vw,54px)!important;
  justify-content:center!important;
  background:transparent!important;
}
body[data-x135-family="cinematic"] .p130-hub .p130-featured-copy p{
  max-width:54ch!important;
  line-height:1.68!important;
  text-wrap:pretty!important;
}

body[data-x135-family="cinematic"] [data-stage130-hub]:not([data-stage130-hub="about"]) .p130-footer-cta>div{
  color:#f5f7f4!important;
  border:1px solid rgba(255,255,255,.12)!important;
  background:
    radial-gradient(28rem 18rem at 100% 0,rgba(201,255,74,.08),transparent 70%),
    linear-gradient(145deg,rgba(255,255,255,.075),rgba(255,255,255,.025)),
    rgba(12,16,20,.72)!important;
  -webkit-backdrop-filter:blur(22px) saturate(132%)!important;
  backdrop-filter:blur(22px) saturate(132%)!important;
  box-shadow:0 28px 82px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.06)!important;
}
body[data-x135-family="cinematic"] [data-stage130-hub]:not([data-stage130-hub="about"]) .p130-footer-cta p{
  color:rgba(225,232,235,.7)!important;
  line-height:1.7!important;
}
body[data-x135-family="cinematic"] [data-stage130-hub]:not([data-stage130-hub="about"]) .p130-footer-cta .p129-btn{
  background:#c9ff4a!important;
  color:#080b0d!important;
}

@media (hover:hover) and (pointer:fine){
  body[data-x135-family="cinematic"] .p130-hub .p130-row{
    transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease!important;
  }
  body[data-x135-family="cinematic"] .p130-hub .p130-row:hover{
    padding:24px!important;
    transform:translateY(-3px)!important;
    border-color:rgba(201,255,74,.24)!important;
    box-shadow:0 28px 78px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.07)!important;
  }
}

@media(max-width:1080px){
  body[data-x135-family="cinematic"] .p130-hub .p130-shell.p130-hero-grid{
    width:min(100% - 42px,1040px)!important;
    grid-template-columns:minmax(0,1.12fr) minmax(280px,.88fr)!important;
    gap:32px!important;
  }
  body[data-x135-family="cinematic"] .p130-hub .p130-hero h1{
    max-width:14ch!important;
    font-size:clamp(54px,6.8vw,78px)!important;
  }
}

@media(max-width:900px){
  body[data-x135-family="cinematic"] .p130-hub .p130-shell.p130-hero-grid{
    width:min(100% - 32px,760px)!important;
    grid-template-columns:1fr!important;
    gap:26px!important;
  }
  body[data-x135-family="cinematic"] .p130-hub .p130-hero-grid>div:first-child{max-width:none!important}
  body[data-x135-family="cinematic"] .p130-hub .p130-hero h1{max-width:12ch!important}
  body[data-x135-family="cinematic"] .p130-hub .p129-section-head{grid-template-columns:1fr!important;gap:10px!important}
  body[data-x135-family="cinematic"] .p130-hub .p130-list{grid-template-columns:1fr!important}
  body[data-x135-family="cinematic"] .p130-hub .p130-featured-card{grid-template-columns:1fr!important;min-height:0!important}
  body[data-x135-family="cinematic"] .p130-hub .p130-featured-media{min-height:0!important;aspect-ratio:16/10!important}
}

@media(max-width:600px){
  body[data-x135-family="cinematic"] .p130-hub .p130-hero{padding:42px 0 58px!important}
  body[data-x135-family="cinematic"] .p130-hub .p130-shell.p130-hero-grid{width:calc(100% - 24px)!important}
  body[data-x135-family="cinematic"] .p130-hub .p130-hero h1{
    max-width:100%!important;
    font-size:clamp(44px,12.8vw,62px)!important;
    line-height:.92!important;
  }
  body[data-x135-family="cinematic"] .p130-hub .p130-lead{font-size:16px!important;line-height:1.65!important}
  body[data-x135-family="cinematic"] .p130-hub .p130-hero-side{border-radius:20px!important;padding:20px!important}
  body[data-x135-family="cinematic"] .p130-hub .p130-row{min-height:0!important;padding:20px!important;border-radius:20px!important;grid-template-columns:34px minmax(0,1fr) 24px!important}
  body[data-x135-family="cinematic"] .p130-hub .p130-row:hover{padding:20px!important}
}

@media(prefers-reduced-motion:reduce){
  body[data-x135-family="cinematic"] .p130-hub .p130-row{transition:none!important;transform:none!important}
}
</style>'''

changed = []
for path in sorted(ROOT.rglob("index.html")):
    text = path.read_text(encoding="utf-8")
    if MARKER in text or "</head>" not in text:
        continue
    text = text.replace("</head>", STYLE + "</head>", 1)
    path.write_text(text, encoding="utf-8")
    changed.append(path)

services = ROOT / "services" / "index.html"
if not services.is_file():
    raise SystemExit("stage151: services page missing")
final = services.read_text(encoding="utf-8")
for token in (MARKER, "p130-hero-grid", "p130-row", "secondary-demand"):
    if token not in final:
        raise SystemExit(f"stage151: services guard failed: {token}")

print(f"stage151 hub layout polish: {len(changed)} pages")
