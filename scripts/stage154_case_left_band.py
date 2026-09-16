#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage154-case-left-band"

STYLE = r'''<style id="stage154-case-left-band">
/* Final case hero: copy lives inside the large left band, preview stays right. */
@media (min-width:981px){
  body[data-x135-family="cinematic"] .p132-case .p132-cover{
    position:relative!important;
    min-height:calc(88vh - 64px)!important;
    display:flex!important;
    align-items:center!important;
    padding:clamp(64px,6vw,96px) 0!important;
    overflow:hidden!important;
    isolation:isolate!important;
    background:#070a0c!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover::before{
    content:""!important;
    display:block!important;
    position:absolute!important;
    z-index:0!important;
    left:0!important;
    top:24%!important;
    bottom:14%!important;
    width:min(64vw,980px)!important;
    border:0!important;
    border-radius:0 34px 34px 0!important;
    background:
      radial-gradient(48rem 28rem at 12% 30%,rgba(72,126,86,.16),transparent 70%),
      radial-gradient(34rem 22rem at 88% 86%,rgba(190,216,91,.06),transparent 72%),
      linear-gradient(110deg,rgba(18,34,27,.94),rgba(15,23,22,.90) 58%,rgba(14,18,20,.83))!important;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.035),0 28px 90px rgba(0,0,0,.24)!important;
    pointer-events:none!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover::after{
    content:""!important;
    display:block!important;
    position:absolute!important;
    z-index:0!important;
    left:0!important;
    top:24%!important;
    bottom:14%!important;
    width:min(64vw,980px)!important;
    border-radius:0 34px 34px 0!important;
    background-image:linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.014) 1px,transparent 1px)!important;
    background-size:36px 36px!important;
    -webkit-mask-image:linear-gradient(90deg,#000 0%,rgba(0,0,0,.9) 68%,transparent 100%)!important;
    mask-image:linear-gradient(90deg,#000 0%,rgba(0,0,0,.9) 68%,transparent 100%)!important;
    pointer-events:none!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-shell.p132-cover-grid{
    position:relative!important;
    z-index:2!important;
    display:grid!important;
    grid-template-columns:minmax(0,1.42fr) minmax(300px,.58fr)!important;
    width:min(1380px,calc(100% - 72px))!important;
    max-width:1380px!important;
    margin:0 auto!important;
    padding:0!important;
    gap:clamp(34px,4.2vw,68px)!important;
    align-items:center!important;
    direction:ltr!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-copy{
    grid-column:1!important;
    order:1!important;
    width:100%!important;
    max-width:790px!important;
    min-width:0!important;
    min-height:0!important;
    margin:0!important;
    padding:clamp(18px,2vw,28px) clamp(24px,3.2vw,46px)!important;
    align-self:center!important;
    justify-self:start!important;
    display:block!important;
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    border:0!important;
    border-radius:0!important;
    background:transparent!important;
    -webkit-backdrop-filter:none!important;
    backdrop-filter:none!important;
    box-shadow:none!important;
    overflow:visible!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-copy::before,
  body[data-x135-family="cinematic"] .p132-case .p132-cover-copy::after{
    display:none!important;
    content:none!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-eyebrow{
    color:rgba(230,237,232,.66)!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover h1{
    width:100%!important;
    max-width:13.5ch!important;
    margin:.8rem 0 1.15rem!important;
    font-size:clamp(58px,5.2vw,94px)!important;
    line-height:.9!important;
    letter-spacing:-.058em!important;
    color:#f5f7f4!important;
    text-wrap:balance!important;
    overflow-wrap:normal!important;
    word-break:normal!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover h1 :is(em,span){
    color:#a8e7a8!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-copy>p:not(.p132-eyebrow){
    width:100%!important;
    max-width:58ch!important;
    margin:0!important;
    color:rgba(232,237,235,.78)!important;
    font-size:clamp(17px,1.12vw,19px)!important;
    line-height:1.72!important;
    text-wrap:pretty!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-actions{
    margin-top:1.75rem!important;
    gap:.8rem 1rem!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-visual{
    grid-column:2!important;
    order:2!important;
    width:100%!important;
    max-width:360px!important;
    min-width:0!important;
    min-height:0!important;
    height:auto!important;
    aspect-ratio:4/3!important;
    margin:0!important;
    align-self:center!important;
    justify-self:end!important;
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    border-radius:26px!important;
    overflow:hidden!important;
    box-shadow:0 26px 78px rgba(0,0,0,.34)!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-visual img{
    width:100%!important;
    height:100%!important;
    min-height:0!important;
    object-fit:cover!important;
    object-position:center!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-graphic{
    min-height:100%!important;
  }

  /* Cases hub mirrors the same composition. */
  main.p130-hub[data-stage130-hub="cases"] .p130-hero{
    position:relative!important;
    min-height:calc(82vh - 64px)!important;
    display:flex!important;
    align-items:center!important;
    padding:clamp(64px,6vw,96px) 0!important;
    overflow:hidden!important;
    isolation:isolate!important;
    background:#070a0c!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero::before{
    content:""!important;
    display:block!important;
    position:absolute!important;
    z-index:0!important;
    left:0!important;
    top:22%!important;
    bottom:14%!important;
    width:min(65vw,990px)!important;
    border-radius:0 34px 34px 0!important;
    background:
      radial-gradient(48rem 28rem at 12% 30%,rgba(72,126,86,.16),transparent 70%),
      linear-gradient(110deg,rgba(18,34,27,.94),rgba(15,23,22,.90) 58%,rgba(14,18,20,.83))!important;
    pointer-events:none!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero::after{
    display:none!important;
    content:none!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-shell.p130-hero-grid{
    position:relative!important;
    z-index:2!important;
    display:grid!important;
    grid-template-columns:minmax(0,1.42fr) minmax(280px,.58fr)!important;
    width:min(1380px,calc(100% - 72px))!important;
    max-width:1380px!important;
    margin:0 auto!important;
    gap:clamp(34px,4.2vw,68px)!important;
    align-items:center!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero-grid>div:first-child{
    width:100%!important;
    max-width:790px!important;
    min-width:0!important;
    min-height:0!important;
    margin:0!important;
    padding:clamp(18px,2vw,28px) clamp(24px,3.2vw,46px)!important;
    border:0!important;
    border-radius:0!important;
    background:transparent!important;
    -webkit-backdrop-filter:none!important;
    backdrop-filter:none!important;
    box-shadow:none!important;
    overflow:visible!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero-grid>div:first-child::before,
  main.p130-hub[data-stage130-hub="cases"] .p130-hero-grid>div:first-child::after{
    display:none!important;
    content:none!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero h1{
    max-width:13.5ch!important;
    font-size:clamp(58px,5.2vw,94px)!important;
    line-height:.9!important;
    color:#f5f7f4!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-lead{
    max-width:58ch!important;
    color:rgba(232,237,235,.78)!important;
    line-height:1.72!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero-side{
    width:100%!important;
    max-width:320px!important;
    min-height:0!important;
    justify-self:end!important;
    align-self:center!important;
  }
}

@media(max-width:980px){
  body[data-x135-family="cinematic"] .p132-case .p132-cover::before,
  main.p130-hub[data-stage130-hub="cases"] .p130-hero::before{
    top:0!important;
    bottom:auto!important;
    width:100%!important;
    height:62%!important;
    border-radius:0 0 28px 28px!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-shell.p132-cover-grid,
  main.p130-hub[data-stage130-hub="cases"] .p130-shell.p130-hero-grid{
    display:grid!important;
    grid-template-columns:1fr!important;
    width:min(100% - 32px,800px)!important;
    gap:26px!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-copy,
  main.p130-hub[data-stage130-hub="cases"] .p130-hero-grid>div:first-child{
    width:100%!important;
    max-width:none!important;
    padding:28px 20px!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-visual{
    grid-column:1!important;
    width:100%!important;
    max-width:520px!important;
    justify-self:start!important;
    aspect-ratio:16/10!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover h1,
  main.p130-hub[data-stage130-hub="cases"] .p130-hero h1{
    max-width:100%!important;
    font-size:clamp(48px,10vw,76px)!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero-side{
    grid-column:1!important;
    justify-self:start!important;
    max-width:520px!important;
  }
}

@media(max-width:600px){
  body[data-x135-family="cinematic"] .p132-case .p132-cover,
  main.p130-hub[data-stage130-hub="cases"] .p130-hero{
    min-height:0!important;
    padding:38px 0 56px!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-shell.p132-cover-grid,
  main.p130-hub[data-stage130-hub="cases"] .p130-shell.p130-hero-grid{
    width:calc(100% - 24px)!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover h1,
  main.p130-hub[data-stage130-hub="cases"] .p130-hero h1{
    font-size:clamp(42px,12.5vw,60px)!important;
    line-height:.92!important;
  }
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

case_pages = sorted((ROOT / "cases").glob("*/index.html")) if (ROOT / "cases").is_dir() else []
if not case_pages:
    raise SystemExit("stage154: no case pages found")
for path in case_pages:
    final = path.read_text(encoding="utf-8")
    if MARKER not in final or "p132-cover-copy" not in final:
        raise SystemExit(f"stage154: detail case guard failed: {path}")

hub = ROOT / "cases" / "index.html"
if not hub.is_file():
    raise SystemExit("stage154: cases hub missing")
hub_html = hub.read_text(encoding="utf-8")
if MARKER not in hub_html or 'data-stage130-hub="cases"' not in hub_html:
    raise SystemExit("stage154: cases hub guard failed")

print(f"stage154 case left band: {len(changed)} pages, {len(case_pages)} detailed cases guarded")
