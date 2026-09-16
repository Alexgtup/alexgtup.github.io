#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage156-stable-hero-layout"

STYLE = r'''<style id="stage156-stable-hero-layout">
/* Final stable layout: no absolute positioning, no viewport-anchored offsets. */
@media (min-width:981px){
  body[data-x135-family="cinematic"] .p155-cover,
  body[data-x135-family="cinematic"] .p155-service-hero{
    position:relative!important;
    display:grid!important;
    grid-template-columns:minmax(0,1fr) minmax(260px,340px)!important;
    align-items:center!important;
    gap:clamp(28px,3.2vw,52px)!important;
    width:min(1380px,calc(100% - 72px))!important;
    max-width:1380px!important;
    min-height:auto!important;
    margin:clamp(54px,6vw,88px) auto!important;
    padding:0!important;
    overflow:visible!important;
    background:transparent!important;
  }

  body[data-x135-family="cinematic"] .p155-band,
  body[data-x135-family="cinematic"] .p155-service-band{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    min-width:0!important;
    min-height:clamp(480px,38vw,590px)!important;
    height:auto!important;
    margin:0!important;
    padding:clamp(42px,4.2vw,64px)!important;
    display:flex!important;
    align-items:center!important;
    justify-content:flex-start!important;
    border-radius:32px!important;
    overflow:hidden!important;
    box-shadow:0 26px 84px rgba(0,0,0,.26)!important;
  }

  body[data-x135-family="cinematic"] .p155-band{
    background:
      radial-gradient(44rem 26rem at 12% 28%,rgba(72,126,86,.21),transparent 70%),
      radial-gradient(32rem 20rem at 88% 86%,rgba(190,216,91,.07),transparent 72%),
      linear-gradient(110deg,rgba(18,34,27,.97),rgba(15,23,22,.94) 58%,rgba(14,18,20,.88))!important;
  }

  body[data-x135-family="cinematic"] .p155-service-band{
    background:
      radial-gradient(42rem 25rem at 10% 28%,rgba(124,70,73,.16),transparent 70%),
      linear-gradient(110deg,rgba(42,24,25,.96),rgba(30,22,23,.93) 58%,rgba(18,18,20,.88))!important;
  }

  body[data-x135-family="cinematic"] .p155-band::after,
  body[data-x135-family="cinematic"] .p155-service-band::after{
    content:""!important;
    position:absolute!important;
    inset:0!important;
    background-image:
      linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),
      linear-gradient(90deg,rgba(255,255,255,.014) 1px,transparent 1px)!important;
    background-size:36px 36px!important;
    pointer-events:none!important;
    opacity:.8!important;
  }

  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:760px!important;
    min-width:0!important;
    min-height:0!important;
    margin:0!important;
    padding:0!important;
    display:block!important;
    border:0!important;
    background:transparent!important;
    box-shadow:none!important;
    backdrop-filter:none!important;
    -webkit-backdrop-filter:none!important;
    overflow:visible!important;
    z-index:2!important;
  }

  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy::before,
  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy::after,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy::before,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy::after{
    display:none!important;
    content:none!important;
  }

  body[data-x135-family="cinematic"] .p155-band h1,
  body[data-x135-family="cinematic"] .p155-service-band .p129-svc-copy h1{
    width:100%!important;
    max-width:13ch!important;
    margin:.85rem 0 1.05rem!important;
    font-size:clamp(50px,4.25vw,80px)!important;
    line-height:.92!important;
    letter-spacing:-.052em!important;
    text-wrap:balance!important;
    overflow-wrap:normal!important;
    word-break:normal!important;
  }

  body[data-x135-family="cinematic"] .p155-band .p132-cover-copy>p:not(.p132-eyebrow),
  body[data-x135-family="cinematic"] .p155-service-band .p129-lead{
    width:100%!important;
    max-width:52ch!important;
    margin:0!important;
    font-size:clamp(16px,1.03vw,18px)!important;
    line-height:1.68!important;
    text-wrap:pretty!important;
  }

  body[data-x135-family="cinematic"] .p155-preview,
  body[data-x135-family="cinematic"] .p155-service-preview{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:340px!important;
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
  }

  body[data-x135-family="cinematic"] .p155-preview .p132-cover-visual{
    aspect-ratio:4/3!important;
    border-radius:26px!important;
    overflow:hidden!important;
    box-shadow:0 24px 72px rgba(0,0,0,.32)!important;
  }

  body[data-x135-family="cinematic"] .p155-preview .p132-cover-visual img{
    width:100%!important;
    height:100%!important;
    min-height:0!important;
    object-fit:cover!important;
    object-position:center!important;
  }
}

@media (max-width:980px){
  body[data-x135-family="cinematic"] .p155-cover,
  body[data-x135-family="cinematic"] .p155-service-hero{
    position:relative!important;
    display:grid!important;
    grid-template-columns:1fr!important;
    gap:22px!important;
    width:min(100% - 24px,800px)!important;
    margin:34px auto 56px!important;
    padding:0!important;
    min-height:0!important;
    overflow:visible!important;
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
    padding:30px 24px!important;
    border-radius:26px!important;
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
    font-size:clamp(44px,10vw,72px)!important;
  }

  body[data-x135-family="cinematic"] .p155-preview,
  body[data-x135-family="cinematic"] .p155-service-preview{
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:520px!important;
    margin:0!important;
    justify-self:start!important;
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

print(f"stage156 stable hero layout: {changed} pages")
