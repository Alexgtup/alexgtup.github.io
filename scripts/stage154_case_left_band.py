#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage154-case-left-band"

STYLE = r'''<style id="stage154-case-left-band">
/* Absolute final hero composition. The existing colour band is the text surface. */
@media (min-width:981px){
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover{
    position:relative!important;
    min-height:calc(88vh - 64px)!important;
    display:flex!important;
    align-items:center!important;
    padding:clamp(54px,5vw,82px) 0!important;
    overflow:hidden!important;
    isolation:isolate!important;
    background:#070a0c!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover::before{
    content:""!important;
    display:block!important;
    position:absolute!important;
    z-index:0!important;
    left:0!important;
    top:19%!important;
    bottom:10%!important;
    width:min(64vw,980px)!important;
    border:0!important;
    border-radius:0 34px 34px 0!important;
    background:
      radial-gradient(48rem 28rem at 12% 30%,rgba(72,126,86,.18),transparent 70%),
      radial-gradient(34rem 22rem at 88% 86%,rgba(190,216,91,.065),transparent 72%),
      linear-gradient(110deg,rgba(18,34,27,.96),rgba(15,23,22,.92) 58%,rgba(14,18,20,.86))!important;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.035),0 28px 90px rgba(0,0,0,.24)!important;
    pointer-events:none!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover::after{
    content:""!important;
    display:block!important;
    position:absolute!important;
    z-index:0!important;
    left:0!important;
    top:19%!important;
    bottom:10%!important;
    width:min(64vw,980px)!important;
    border-radius:0 34px 34px 0!important;
    background-image:linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.014) 1px,transparent 1px)!important;
    background-size:36px 36px!important;
    -webkit-mask-image:linear-gradient(90deg,#000 0%,rgba(0,0,0,.9) 68%,transparent 100%)!important;
    mask-image:linear-gradient(90deg,#000 0%,rgba(0,0,0,.9) 68%,transparent 100%)!important;
    pointer-events:none!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-shell.p132-cover-grid{
    position:relative!important;
    z-index:2!important;
    display:block!important;
    width:min(1380px,calc(100% - 72px))!important;
    max-width:1380px!important;
    min-height:clamp(540px,42vw,660px)!important;
    margin:0 auto!important;
    padding:0!important;
    transform:none!important;
    translate:none!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover-copy{
    position:absolute!important;
    z-index:4!important;
    left:0!important;
    right:auto!important;
    top:50%!important;
    bottom:auto!important;
    transform:translateY(-50%)!important;
    translate:none!important;
    width:min(760px,55vw)!important;
    max-width:760px!important;
    min-width:0!important;
    min-height:0!important;
    margin:0!important;
    padding:clamp(22px,2.6vw,38px) clamp(28px,3vw,46px)!important;
    display:block!important;
    border:0!important;
    border-radius:0!important;
    background:transparent!important;
    box-shadow:none!important;
    backdrop-filter:none!important;
    -webkit-backdrop-filter:none!important;
    overflow:visible!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover-copy::before,
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover-copy::after{
    display:none!important;
    content:none!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-eyebrow{
    color:rgba(230,237,232,.66)!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover h1{
    width:100%!important;
    max-width:11.6ch!important;
    margin:.8rem 0 1.05rem!important;
    font-size:clamp(52px,4.35vw,78px)!important;
    line-height:.92!important;
    letter-spacing:-.055em!important;
    color:#f5f7f4!important;
    text-wrap:balance!important;
    overflow-wrap:normal!important;
    word-break:normal!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover h1 :is(em,span){
    color:#a8e7a8!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover-copy>p:not(.p132-eyebrow){
    width:100%!important;
    max-width:46ch!important;
    margin:0!important;
    color:rgba(236,241,238,.84)!important;
    font-size:clamp(16px,1.05vw,18px)!important;
    line-height:1.66!important;
    text-wrap:pretty!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover-actions{
    margin-top:1.55rem!important;
    gap:.7rem .9rem!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover-visual{
    position:absolute!important;
    z-index:3!important;
    right:0!important;
    left:auto!important;
    top:50%!important;
    bottom:auto!important;
    transform:translateY(-50%)!important;
    translate:none!important;
    width:min(340px,25vw)!important;
    max-width:340px!important;
    min-width:0!important;
    min-height:0!important;
    height:auto!important;
    aspect-ratio:4/3!important;
    margin:0!important;
    border-radius:26px!important;
    overflow:hidden!important;
    box-shadow:0 26px 78px rgba(0,0,0,.34)!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover-visual img{
    width:100%!important;
    height:100%!important;
    min-height:0!important;
    object-fit:cover!important;
    object-position:center!important;
    transform:none!important;
  }

  /* Service/product hero pages such as project-repair use the same left-band logic. */
  html body[data-x135-family="cinematic"] main.p129-service .p129-svc-hero{
    position:relative!important;
    min-height:calc(88vh - 64px)!important;
    display:flex!important;
    align-items:center!important;
    padding:clamp(54px,5vw,82px) 0!important;
    overflow:hidden!important;
    isolation:isolate!important;
  }
  html body[data-x135-family="cinematic"] main.p129-service .p129-shell.p129-svc-grid{
    position:relative!important;
    z-index:2!important;
    display:block!important;
    width:min(1380px,calc(100% - 72px))!important;
    max-width:1380px!important;
    min-height:clamp(540px,42vw,660px)!important;
    margin:0 auto!important;
    padding:0!important;
    transform:none!important;
    translate:none!important;
  }
  html body[data-x135-family="cinematic"] main.p129-service .p129-svc-copy{
    position:absolute!important;
    z-index:4!important;
    left:0!important;
    right:auto!important;
    top:50%!important;
    bottom:auto!important;
    transform:translateY(-50%)!important;
    translate:none!important;
    width:min(780px,56vw)!important;
    max-width:780px!important;
    margin:0!important;
    padding:clamp(22px,2.6vw,38px) clamp(28px,3vw,46px)!important;
    border:0!important;
    background:transparent!important;
    box-shadow:none!important;
  }
  html body[data-x135-family="cinematic"] main.p129-service .p129-svc-copy h1{
    max-width:11.6ch!important;
    font-size:clamp(52px,4.35vw,78px)!important;
    line-height:.92!important;
    letter-spacing:-.055em!important;
    text-wrap:balance!important;
  }
  html body[data-x135-family="cinematic"] main.p129-service .p129-lead{
    max-width:46ch!important;
    font-size:clamp(16px,1.05vw,18px)!important;
    line-height:1.66!important;
  }
  html body[data-x135-family="cinematic"] main.p129-service .p129-svc-board{
    position:absolute!important;
    z-index:3!important;
    right:0!important;
    left:auto!important;
    top:50%!important;
    transform:translateY(-50%)!important;
    translate:none!important;
    width:min(340px,25vw)!important;
    max-width:340px!important;
    margin:0!important;
  }
}

@media(max-width:980px){
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover::before{
    top:0!important;
    bottom:auto!important;
    width:100%!important;
    height:62%!important;
    border-radius:0 0 28px 28px!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover::after{
    display:none!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-shell.p132-cover-grid,
  html body[data-x135-family="cinematic"] main.p129-service .p129-shell.p129-svc-grid{
    display:grid!important;
    grid-template-columns:1fr!important;
    width:min(100% - 32px,800px)!important;
    min-height:0!important;
    gap:26px!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover-copy,
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover-visual,
  html body[data-x135-family="cinematic"] main.p129-service .p129-svc-copy,
  html body[data-x135-family="cinematic"] main.p129-service .p129-svc-board{
    position:relative!important;
    left:auto!important;
    right:auto!important;
    top:auto!important;
    bottom:auto!important;
    transform:none!important;
    width:100%!important;
    max-width:none!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover-copy,
  html body[data-x135-family="cinematic"] main.p129-service .p129-svc-copy{
    padding:28px 20px!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover-visual{
    max-width:520px!important;
    aspect-ratio:16/10!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover h1,
  html body[data-x135-family="cinematic"] main.p129-service .p129-svc-copy h1{
    max-width:100%!important;
    font-size:clamp(48px,10vw,76px)!important;
  }
}

@media(max-width:600px){
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover,
  html body[data-x135-family="cinematic"] main.p129-service .p129-svc-hero{
    min-height:0!important;
    padding:38px 0 56px!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-shell.p132-cover-grid,
  html body[data-x135-family="cinematic"] main.p129-service .p129-shell.p129-svc-grid{
    width:calc(100% - 24px)!important;
  }
  html body[data-x135-family="cinematic"] main.p132-case[data-stage132-case="true"] .p132-cover h1,
  html body[data-x135-family="cinematic"] main.p129-service .p129-svc-copy h1{
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

print(f"stage154 absolute left band: {len(changed)} pages, {len(case_pages)} detailed cases guarded")
