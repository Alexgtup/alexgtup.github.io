#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage153-case-left-panel"

STYLE = r'''<style id="stage153-case-left-panel">
/* Final case composition guard. Runs after all cinematic/glass layers. */
@media (min-width:981px){
  body[data-x135-family="cinematic"] .p132-case .p132-cover{
    min-height:0!important;
    padding:clamp(72px,6vw,104px) 0 clamp(70px,6.5vw,104px)!important;
    overflow:hidden!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover::before,
  body[data-x135-family="cinematic"] .p132-case .p132-cover::after{
    display:none!important;
    content:none!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-shell.p132-cover-grid{
    display:grid!important;
    grid-template-columns:minmax(0,1.28fr) minmax(300px,.72fr)!important;
    width:min(1360px,calc(100% - 72px))!important;
    max-width:1360px!important;
    margin:0 auto!important;
    padding:0!important;
    gap:clamp(24px,3vw,44px)!important;
    align-items:stretch!important;
    direction:ltr!important;
    transform:none!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-copy{
    grid-column:1!important;
    order:1!important;
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:none!important;
    min-width:0!important;
    min-height:clamp(470px,39vw,610px)!important;
    margin:0!important;
    padding:clamp(34px,3.7vw,56px)!important;
    display:flex!important;
    flex-direction:column!important;
    justify-content:center!important;
    align-self:stretch!important;
    justify-self:stretch!important;
    border:1px solid rgba(255,255,255,.12)!important;
    border-radius:34px!important;
    background:
      radial-gradient(30rem 22rem at 10% 8%,rgba(129,149,255,.14),transparent 68%),
      radial-gradient(24rem 18rem at 94% 96%,rgba(201,255,74,.07),transparent 70%),
      linear-gradient(145deg,rgba(255,255,255,.082),rgba(255,255,255,.028) 48%,rgba(7,10,13,.64)),
      rgba(12,16,20,.72)!important;
    -webkit-backdrop-filter:blur(24px) saturate(136%)!important;
    backdrop-filter:blur(24px) saturate(136%)!important;
    box-shadow:0 30px 90px rgba(0,0,0,.31),inset 0 1px 0 rgba(255,255,255,.07)!important;
    overflow:hidden!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-copy::before{
    content:""!important;
    position:absolute!important;
    inset:0!important;
    pointer-events:none!important;
    border-radius:inherit!important;
    background:linear-gradient(135deg,rgba(255,255,255,.075),transparent 30%)!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-copy>*{
    position:relative!important;
    z-index:1!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover h1{
    width:100%!important;
    max-width:15ch!important;
    margin:.85rem 0 1.2rem!important;
    font-size:clamp(58px,5.35vw,96px)!important;
    line-height:.9!important;
    letter-spacing:-.058em!important;
    text-wrap:balance!important;
    overflow-wrap:normal!important;
    word-break:normal!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-copy>p:not(.p132-eyebrow){
    width:100%!important;
    max-width:64ch!important;
    margin:0!important;
    color:rgba(232,237,240,.79)!important;
    font-size:clamp(17px,1.16vw,20px)!important;
    line-height:1.72!important;
    text-wrap:pretty!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-actions{
    margin-top:1.9rem!important;
    gap:.8rem 1rem!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-visual{
    grid-column:2!important;
    order:2!important;
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:none!important;
    min-width:0!important;
    min-height:clamp(470px,39vw,610px)!important;
    height:auto!important;
    aspect-ratio:auto!important;
    margin:0!important;
    align-self:stretch!important;
    justify-self:stretch!important;
    border-radius:34px!important;
    overflow:hidden!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-visual img{
    width:100%!important;
    height:100%!important;
    min-height:100%!important;
    object-fit:cover!important;
    object-position:center!important;
    transform:none!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-graphic{
    min-height:100%!important;
  }

  /* Cases hub uses the same left-panel language. */
  main.p130-hub[data-stage130-hub="cases"] .p130-hero{
    min-height:0!important;
    padding:clamp(72px,6vw,104px) 0 clamp(70px,6.5vw,104px)!important;
    overflow:hidden!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero::before,
  main.p130-hub[data-stage130-hub="cases"] .p130-hero::after{
    display:none!important;
    content:none!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-shell.p130-hero-grid{
    display:grid!important;
    grid-template-columns:minmax(0,1.28fr) minmax(280px,.58fr)!important;
    width:min(1360px,calc(100% - 72px))!important;
    max-width:1360px!important;
    margin:0 auto!important;
    gap:clamp(24px,3vw,42px)!important;
    align-items:stretch!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero-grid>div:first-child{
    grid-column:1!important;
    position:relative!important;
    width:100%!important;
    max-width:none!important;
    min-width:0!important;
    min-height:clamp(450px,37vw,570px)!important;
    padding:clamp(34px,3.7vw,56px)!important;
    display:flex!important;
    flex-direction:column!important;
    justify-content:center!important;
    border:1px solid rgba(255,255,255,.12)!important;
    border-radius:34px!important;
    background:
      radial-gradient(30rem 22rem at 10% 8%,rgba(129,149,255,.14),transparent 68%),
      radial-gradient(24rem 18rem at 94% 96%,rgba(201,255,74,.07),transparent 70%),
      linear-gradient(145deg,rgba(255,255,255,.082),rgba(255,255,255,.028) 48%,rgba(7,10,13,.64)),
      rgba(12,16,20,.72)!important;
    -webkit-backdrop-filter:blur(24px) saturate(136%)!important;
    backdrop-filter:blur(24px) saturate(136%)!important;
    box-shadow:0 30px 90px rgba(0,0,0,.31),inset 0 1px 0 rgba(255,255,255,.07)!important;
    overflow:hidden!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero-grid>div:first-child::before{
    content:""!important;
    position:absolute!important;
    inset:0!important;
    pointer-events:none!important;
    border-radius:inherit!important;
    background:linear-gradient(135deg,rgba(255,255,255,.075),transparent 30%)!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero-grid>div:first-child>*{
    position:relative!important;
    z-index:1!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero h1{
    width:100%!important;
    max-width:15ch!important;
    margin:.85rem 0 1.2rem!important;
    font-size:clamp(58px,5.35vw,96px)!important;
    line-height:.9!important;
    letter-spacing:-.058em!important;
    text-wrap:balance!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-lead{
    width:100%!important;
    max-width:62ch!important;
    color:rgba(232,237,240,.79)!important;
    font-size:clamp(17px,1.16vw,20px)!important;
    line-height:1.72!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero-side{
    grid-column:2!important;
    align-self:center!important;
    width:100%!important;
    min-height:220px!important;
    margin:0!important;
    padding:28px!important;
    border:1px solid rgba(255,255,255,.11)!important;
    border-radius:28px!important;
    background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.022)),rgba(12,16,20,.68)!important;
    -webkit-backdrop-filter:blur(20px) saturate(132%)!important;
    backdrop-filter:blur(20px) saturate(132%)!important;
    box-shadow:0 22px 68px rgba(0,0,0,.27),inset 0 1px 0 rgba(255,255,255,.055)!important;
  }
}

@media(max-width:980px){
  body[data-x135-family="cinematic"] .p132-case .p132-shell.p132-cover-grid,
  main.p130-hub[data-stage130-hub="cases"] .p130-shell.p130-hero-grid{
    display:grid!important;
    grid-template-columns:1fr!important;
    width:min(100% - 32px,800px)!important;
    gap:22px!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-copy,
  main.p130-hub[data-stage130-hub="cases"] .p130-hero-grid>div:first-child{
    width:100%!important;
    max-width:none!important;
    min-height:0!important;
    padding:clamp(24px,6vw,38px)!important;
    border-radius:26px!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover-visual{
    grid-column:1!important;
    width:100%!important;
    min-height:0!important;
    aspect-ratio:16/10!important;
    border-radius:26px!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover h1,
  main.p130-hub[data-stage130-hub="cases"] .p130-hero h1{
    max-width:100%!important;
    font-size:clamp(48px,10vw,76px)!important;
  }
  main.p130-hub[data-stage130-hub="cases"] .p130-hero-side{
    grid-column:1!important;
    min-height:0!important;
    border-radius:22px!important;
  }
}

@media(max-width:600px){
  body[data-x135-family="cinematic"] .p132-case .p132-shell.p132-cover-grid,
  main.p130-hub[data-stage130-hub="cases"] .p130-shell.p130-hero-grid{
    width:calc(100% - 24px)!important;
  }
  body[data-x135-family="cinematic"] .p132-case .p132-cover,
  main.p130-hub[data-stage130-hub="cases"] .p130-hero{
    padding:38px 0 56px!important;
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
    raise SystemExit("stage153: no case pages found")
for path in case_pages:
    final = path.read_text(encoding="utf-8")
    if MARKER not in final or "p132-cover-copy" not in final:
        raise SystemExit(f"stage153: detail case guard failed: {path}")

hub = ROOT / "cases" / "index.html"
if not hub.is_file():
    raise SystemExit("stage153: cases hub missing")
hub_html = hub.read_text(encoding="utf-8")
if MARKER not in hub_html or 'data-stage130-hub="cases"' not in hub_html:
    raise SystemExit("stage153: cases hub guard failed")

print(f"stage153 case left panel: {len(changed)} pages, {len(case_pages)} detailed cases guarded")
