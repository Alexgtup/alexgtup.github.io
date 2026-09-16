#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage157-designer-case-hero"

STYLE = r'''<style id="stage157-designer-case-hero">
/* Final case/service hero: editorial split, no card-on-card composition. */
@media (min-width:981px){
  body[data-x135-family="cinematic"] .p132-cover.p155-cover,
  body[data-x135-family="cinematic"] .p155-service-hero{
    position:relative!important;
    display:grid!important;
    grid-template-columns:minmax(0,.88fr) minmax(460px,1.12fr)!important;
    align-items:center!important;
    gap:clamp(56px,6vw,96px)!important;
    width:min(1320px,calc(100% - 80px))!important;
    max-width:1320px!important;
    min-height:clamp(580px,48vw,720px)!important;
    margin:clamp(70px,7vw,110px) auto clamp(84px,8vw,128px)!important;
    padding:clamp(18px,2vw,30px) 0!important;
    overflow:visible!important;
    isolation:isolate!important;
    border:0!important;
    border-radius:0!important;
    background:transparent!important;
    box-shadow:none!important;
    backdrop-filter:none!important;
    -webkit-backdrop-filter:none!important;
  }

  body[data-x135-family="cinematic"] .p132-cover.p155-cover::before,
  body[data-x135-family="cinematic"] .p155-service-hero::before{
    content:""!important;
    display:block!important;
    position:absolute!important;
    z-index:-1!important;
    width:min(620px,46vw)!important;
    aspect-ratio:1!important;
    right:-6%!important;
    top:50%!important;
    transform:translateY(-50%)!important;
    border-radius:50%!important;
    background:radial-gradient(circle,rgba(105,133,255,.105) 0%,rgba(70,110,90,.055) 38%,transparent 72%)!important;
    filter:blur(8px)!important;
    pointer-events:none!important;
  }

  body[data-x135-family="cinematic"] .p132-cover.p155-cover::after,
  body[data-x135-family="cinematic"] .p155-service-hero::after{
    content:""!important;
    display:block!important;
    position:absolute!important;
    left:0!important;
    right:0!important;
    bottom:-36px!important;
    height:1px!important;
    background:linear-gradient(90deg,transparent,rgba(255,255,255,.10) 18%,rgba(255,255,255,.10) 82%,transparent)!important;
    pointer-events:none!important;
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
    max-width:620px!important;
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
    margin:0 0 22px!important;
    color:rgba(225,233,228,.58)!important;
    font-size:12px!important;
    line-height:1.35!important;
    letter-spacing:.19em!important;
    text-transform:uppercase!important;
  }

  body[data-x135-family="cinematic"] .p155-band h1,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy h1{
    width:100%!important;
    max-width:11.8ch!important;
    margin:0 0 28px!important;
    font-size:clamp(64px,5.25vw,96px)!important;
    line-height:.90!important;
    letter-spacing:-.065em!important;
    color:#f5f7f4!important;
    text-wrap:balance!important;
    overflow-wrap:normal!important;
    word-break:normal!important;
  }

  body[data-x135-family="cinematic"] .p155-band h1 :is(em,span){
    color:#a8e0a4!important;
  }

  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy>p:not(.p132-eyebrow),
  body[data-x135-family="cinematic"] .p155-service-band .p129-lead{
    width:100%!important;
    max-width:46ch!important;
    margin:0!important;
    color:rgba(232,238,234,.72)!important;
    font-size:clamp(17px,1.16vw,20px)!important;
    line-height:1.72!important;
    text-wrap:pretty!important;
  }

  body[data-x135-family="cinematic"] .p155-band .p132-cover-actions,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-actions{
    margin-top:34px!important;
    display:flex!important;
    flex-wrap:wrap!important;
    align-items:center!important;
    gap:12px 20px!important;
  }

  body[data-x135-family="cinematic"] .p155-preview,
  body[data-x135-family="cinematic"] .p155-service-preview{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:620px!important;
    min-width:0!important;
    margin:0!important;
    align-self:center!important;
    justify-self:end!important;
  }

  body[data-x135-family="cinematic"] .p155-preview::before,
  body[data-x135-family="cinematic"] .p155-service-preview::before{
    content:""!important;
    position:absolute!important;
    z-index:-1!important;
    inset:10% 8% -6% 8%!important;
    border-radius:34px!important;
    background:linear-gradient(135deg,rgba(120,149,255,.15),rgba(94,150,111,.08))!important;
    filter:blur(44px)!important;
    opacity:.8!important;
    pointer-events:none!important;
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
    border:1px solid rgba(255,255,255,.095)!important;
    border-radius:28px!important;
    overflow:hidden!important;
    background:rgba(255,255,255,.025)!important;
    box-shadow:0 34px 90px rgba(0,0,0,.38),inset 0 1px 0 rgba(255,255,255,.04)!important;
  }

  body[data-x135-family="cinematic"] .p155-preview .p132-cover-visual{
    aspect-ratio:16/10!important;
  }

  body[data-x135-family="cinematic"] .p155-preview .p132-cover-visual img{
    width:100%!important;
    height:100%!important;
    min-height:0!important;
    object-fit:cover!important;
    object-position:center!important;
  }
}

@media (max-width:1180px) and (min-width:981px){
  body[data-x135-family="cinematic"] .p132-cover.p155-cover,
  body[data-x135-family="cinematic"] .p155-service-hero{
    grid-template-columns:minmax(0,.95fr) minmax(390px,1.05fr)!important;
    gap:42px!important;
    width:min(1120px,calc(100% - 56px))!important;
  }
  body[data-x135-family="cinematic"] .p155-band h1,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy h1{
    font-size:clamp(56px,5.4vw,78px)!important;
  }
}

@media (max-width:980px){
  body[data-x135-family="cinematic"] .p132-cover.p155-cover,
  body[data-x135-family="cinematic"] .p155-service-hero{
    position:relative!important;
    display:grid!important;
    grid-template-columns:1fr!important;
    gap:42px!important;
    width:min(100% - 28px,820px)!important;
    min-height:0!important;
    margin:44px auto 68px!important;
    padding:0!important;
    border:0!important;
    border-radius:0!important;
    overflow:visible!important;
    background:transparent!important;
    box-shadow:none!important;
  }

  body[data-x135-family="cinematic"] .p132-cover.p155-cover::before,
  body[data-x135-family="cinematic"] .p132-cover.p155-cover::after,
  body[data-x135-family="cinematic"] .p155-service-hero::before,
  body[data-x135-family="cinematic"] .p155-service-hero::after{
    content:none!important;
    display:none!important;
  }

  body[data-x135-family="cinematic"] .p155-band,
  body[data-x135-family="cinematic"] .p155-service-band,
  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:none!important;
    min-height:0!important;
    margin:0!important;
    padding:0!important;
    background:transparent!important;
    box-shadow:none!important;
    border:0!important;
  }

  body[data-x135-family="cinematic"] .p155-band h1,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy h1{
    max-width:12ch!important;
    margin-bottom:22px!important;
    font-size:clamp(48px,10.5vw,72px)!important;
    line-height:.92!important;
  }

  body[data-x135-family="cinematic"] .p155-preview,
  body[data-x135-family="cinematic"] .p155-service-preview{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:640px!important;
    margin:0!important;
    justify-self:start!important;
  }
}

@media (max-width:600px){
  body[data-x135-family="cinematic"] .p132-cover.p155-cover,
  body[data-x135-family="cinematic"] .p155-service-hero{
    width:calc(100% - 24px)!important;
    gap:30px!important;
    margin-top:34px!important;
  }
  body[data-x135-family="cinematic"] .p155-band h1,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy h1{
    max-width:100%!important;
    font-size:clamp(44px,13vw,64px)!important;
  }
  body[data-x135-family="cinematic"] .p155-preview .p132-cover-visual,
  body[data-x135-family="cinematic"] .p155-service-preview .p129-svc-board{
    border-radius:22px!important;
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
    raise SystemExit("stage157: no p155 heroes found")

for path in sorted((ROOT / "cases").glob("*/index.html")):
    html = path.read_text(encoding="utf-8")
    if "p155-cover" in html and MARKER not in html:
        raise SystemExit(f"stage157: case guard failed: {path}")

print(f"stage157 designer case hero: {changed} pages")
