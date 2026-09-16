#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage156-stable-hero-layout-v2"

STYLE = r'''<style id="stage156-stable-hero-layout-v2">
/* Final visual system for case/service heroes: one coherent premium surface. */
@media (min-width:981px){
  body[data-x135-family="cinematic"] .p132-cover.p155-cover,
  body[data-x135-family="cinematic"] .p155-service-hero{
    position:relative!important;
    display:grid!important;
    grid-template-columns:minmax(0,1.25fr) minmax(320px,.75fr)!important;
    align-items:center!important;
    gap:clamp(40px,4.6vw,72px)!important;
    width:min(1320px,calc(100% - 72px))!important;
    max-width:1320px!important;
    min-height:clamp(560px,46vw,680px)!important;
    margin:clamp(72px,7vw,110px) auto!important;
    padding:clamp(46px,5vw,76px)!important;
    overflow:hidden!important;
    isolation:isolate!important;
    border:1px solid rgba(255,255,255,.085)!important;
    border-radius:38px!important;
    background:
      radial-gradient(42rem 30rem at 7% 18%,rgba(72,126,86,.15),transparent 72%),
      radial-gradient(30rem 24rem at 92% 14%,rgba(103,128,255,.10),transparent 72%),
      linear-gradient(145deg,rgba(14,20,19,.98),rgba(8,11,14,.985) 64%,rgba(7,9,12,.99))!important;
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,.045),
      0 36px 110px rgba(0,0,0,.38)!important;
    backdrop-filter:blur(18px) saturate(125%)!important;
    -webkit-backdrop-filter:blur(18px) saturate(125%)!important;
  }

  body[data-x135-family="cinematic"] .p132-cover.p155-cover::before,
  body[data-x135-family="cinematic"] .p132-cover.p155-cover::after,
  body[data-x135-family="cinematic"] .p155-service-hero::before,
  body[data-x135-family="cinematic"] .p155-service-hero::after{
    content:none!important;
    display:none!important;
  }

  body[data-x135-family="cinematic"] .p155-band,
  body[data-x135-family="cinematic"] .p155-service-band{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    min-width:0!important;
    min-height:0!important;
    height:auto!important;
    margin:0!important;
    padding:0!important;
    display:block!important;
    border:0!important;
    border-radius:0!important;
    background:transparent!important;
    box-shadow:none!important;
    overflow:visible!important;
  }

  body[data-x135-family="cinematic"] .p155-band::before,
  body[data-x135-family="cinematic"] .p155-band::after,
  body[data-x135-family="cinematic"] .p155-service-band::before,
  body[data-x135-family="cinematic"] .p155-service-band::after{
    content:none!important;
    display:none!important;
  }

  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:720px!important;
    min-width:0!important;
    min-height:0!important;
    margin:0!important;
    padding:0!important;
    display:block!important;
    border:0!important;
    border-radius:0!important;
    background:transparent!important;
    box-shadow:none!important;
    backdrop-filter:none!important;
    -webkit-backdrop-filter:none!important;
    overflow:visible!important;
  }

  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy::before,
  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy::after,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy::before,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy::after{
    content:none!important;
    display:none!important;
  }

  body[data-x135-family="cinematic"] .p155-band .p132-eyebrow,
  body[data-x135-family="cinematic"] .p155-service-band .p129-kicker{
    margin:0 0 18px!important;
    color:rgba(222,232,225,.62)!important;
    font-size:12px!important;
    line-height:1.35!important;
    letter-spacing:.18em!important;
    text-transform:uppercase!important;
  }

  body[data-x135-family="cinematic"] .p155-band h1,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy h1{
    width:100%!important;
    max-width:12.5ch!important;
    margin:0 0 24px!important;
    font-size:clamp(58px,4.8vw,90px)!important;
    line-height:.91!important;
    letter-spacing:-.06em!important;
    color:#f6f8f5!important;
    text-wrap:balance!important;
    overflow-wrap:normal!important;
    word-break:normal!important;
  }

  body[data-x135-family="cinematic"] .p155-band h1 :is(em,span){
    color:#a9e5a7!important;
  }

  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy>p:not(.p132-eyebrow),
  body[data-x135-family="cinematic"] .p155-service-band .p129-lead{
    width:100%!important;
    max-width:52ch!important;
    margin:0!important;
    color:rgba(235,240,237,.78)!important;
    font-size:clamp(17px,1.12vw,20px)!important;
    line-height:1.68!important;
    text-wrap:pretty!important;
  }

  body[data-x135-family="cinematic"] .p155-band .p132-cover-actions,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-actions{
    margin-top:30px!important;
    display:flex!important;
    flex-wrap:wrap!important;
    align-items:center!important;
    gap:12px 18px!important;
  }

  body[data-x135-family="cinematic"] .p155-preview,
  body[data-x135-family="cinematic"] .p155-service-preview{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:430px!important;
    min-width:0!important;
    margin:0!important;
    align-self:center!important;
    justify-self:end!important;
  }

  body[data-x135-family="cinematic"] .p155-preview .p132-cover-visual,
  body[data-x135-family="cinematic"] .p155-service-preview .p129-svc-board{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:none!important;
    min-width:0!important;
    min-height:0!important;
    margin:0!important;
    border:1px solid rgba(255,255,255,.10)!important;
    border-radius:30px!important;
    overflow:hidden!important;
    background:rgba(255,255,255,.035)!important;
    box-shadow:
      0 30px 80px rgba(0,0,0,.36),
      inset 0 1px 0 rgba(255,255,255,.05)!important;
  }

  body[data-x135-family="cinematic"] .p155-preview .p132-cover-visual{
    aspect-ratio:4/3!important;
  }

  body[data-x135-family="cinematic"] .p155-preview .p132-cover-visual img{
    width:100%!important;
    height:100%!important;
    min-height:0!important;
    object-fit:cover!important;
    object-position:center!important;
  }
}

@media (max-width:1100px) and (min-width:981px){
  body[data-x135-family="cinematic"] .p132-cover.p155-cover,
  body[data-x135-family="cinematic"] .p155-service-hero{
    grid-template-columns:minmax(0,1.15fr) minmax(280px,.85fr)!important;
    gap:32px!important;
    padding:44px!important;
  }
  body[data-x135-family="cinematic"] .p155-band h1,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy h1{
    font-size:clamp(52px,5vw,72px)!important;
  }
}

@media (max-width:980px){
  body[data-x135-family="cinematic"] .p132-cover.p155-cover,
  body[data-x135-family="cinematic"] .p155-service-hero{
    position:relative!important;
    display:grid!important;
    grid-template-columns:1fr!important;
    gap:28px!important;
    width:min(100% - 24px,820px)!important;
    min-height:0!important;
    margin:32px auto 56px!important;
    padding:28px!important;
    border:1px solid rgba(255,255,255,.08)!important;
    border-radius:28px!important;
    overflow:hidden!important;
    background:
      radial-gradient(34rem 24rem at 8% 10%,rgba(72,126,86,.14),transparent 72%),
      linear-gradient(145deg,rgba(14,20,19,.985),rgba(8,11,14,.99))!important;
    box-shadow:0 24px 70px rgba(0,0,0,.30)!important;
  }

  body[data-x135-family="cinematic"] .p155-band,
  body[data-x135-family="cinematic"] .p155-service-band{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    min-height:0!important;
    margin:0!important;
    padding:0!important;
    background:transparent!important;
    box-shadow:none!important;
    border:0!important;
  }

  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy{
    width:100%!important;
    max-width:none!important;
    margin:0!important;
    padding:0!important;
  }

  body[data-x135-family="cinematic"] .p155-band h1,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy h1{
    max-width:100%!important;
    margin-bottom:20px!important;
    font-size:clamp(44px,10.5vw,70px)!important;
    line-height:.93!important;
  }

  body[data-x135-family="cinematic"] .p155-preview,
  body[data-x135-family="cinematic"] .p155-service-preview{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:560px!important;
    margin:0!important;
    justify-self:start!important;
  }
}

@media (max-width:600px){
  body[data-x135-family="cinematic"] .p132-cover.p155-cover,
  body[data-x135-family="cinematic"] .p155-service-hero{
    width:calc(100% - 20px)!important;
    padding:22px!important;
    border-radius:24px!important;
    gap:24px!important;
  }
}
</style>'''

changed = 0
for path in sorted(ROOT.rglob("index.html")):
    html = path.read_text(encoding="utf-8")
    if MARKER in html or "</head>" not in html:
        continue
    if "p155-cover" not in html and "p155-service-hero" not in html:
        continue
    html = html.replace("</head>", STYLE + "</head>", 1)
    path.write_text(html, encoding="utf-8")
    changed += 1

if changed == 0:
    raise SystemExit("stage156: no p155 heroes found")

for path in sorted((ROOT / "cases").glob("*/index.html")):
    html = path.read_text(encoding="utf-8")
    if "p155-cover" in html and MARKER not in html:
        raise SystemExit(f"stage156: case guard failed: {path}")

print(f"stage156 designer hero v2: {changed} pages")
