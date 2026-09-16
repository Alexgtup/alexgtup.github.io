#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage154-text-into-existing-band"

STYLE = r'''<style id="stage154-text-into-existing-band">
/* Final composition guard: use the EXISTING coloured hero band as the copy surface.
   Do not create another glass/text card. */
@media (min-width:981px){
  /* Detailed project cases */
  .p132-case .p132-cover{
    min-height:0!important;
    padding:clamp(64px,5.8vw,96px) 0 clamp(64px,6vw,96px)!important;
    overflow:hidden!important;
  }
  .p132-case .p132-shell.p132-cover-grid{
    display:grid!important;
    grid-template-columns:minmax(0,1.22fr) minmax(250px,.40fr)!important;
    width:min(1380px,calc(100% - 72px))!important;
    max-width:1380px!important;
    margin:0 auto!important;
    padding:0!important;
    gap:clamp(28px,3.2vw,46px)!important;
    align-items:center!important;
    direction:ltr!important;
    transform:none!important;
    translate:none!important;
  }
  .p132-case .p132-cover-copy{
    grid-column:1!important;
    grid-row:1!important;
    order:1!important;
    width:100%!important;
    max-width:820px!important;
    min-width:0!important;
    min-height:clamp(450px,37vw,570px)!important;
    margin:0!important;
    padding:clamp(34px,4vw,62px)!important;
    display:flex!important;
    flex-direction:column!important;
    justify-content:center!important;
    align-self:stretch!important;
    justify-self:start!important;
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    border:0!important;
    border-radius:0!important;
    background:transparent!important;
    box-shadow:none!important;
    backdrop-filter:none!important;
    -webkit-backdrop-filter:none!important;
    overflow:visible!important;
    z-index:3!important;
  }
  .p132-case .p132-cover-copy::before,
  .p132-case .p132-cover-copy::after{
    display:none!important;
    content:none!important;
  }
  .p132-case .p132-cover h1{
    width:100%!important;
    max-width:13.5ch!important;
    margin:.85rem 0 1.15rem!important;
    font-size:clamp(58px,5.25vw,98px)!important;
    line-height:.9!important;
    letter-spacing:-.058em!important;
    text-wrap:balance!important;
    overflow-wrap:normal!important;
    word-break:normal!important;
  }
  .p132-case .p132-cover-copy>p:not(.p132-eyebrow){
    width:100%!important;
    max-width:58ch!important;
    margin:0!important;
    font-size:clamp(17px,1.12vw,20px)!important;
    line-height:1.72!important;
    color:rgba(238,242,239,.84)!important;
    text-wrap:pretty!important;
  }
  .p132-case .p132-cover-actions{
    margin-top:1.85rem!important;
    gap:.8rem 1rem!important;
  }
  .p132-case .p132-cover-visual{
    grid-column:2!important;
    grid-row:1!important;
    order:2!important;
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    width:100%!important;
    max-width:320px!important;
    min-width:0!important;
    min-height:0!important;
    height:auto!important;
    aspect-ratio:1.08/1!important;
    margin:0!important;
    align-self:center!important;
    justify-self:end!important;
    border-radius:28px!important;
    overflow:hidden!important;
  }
  .p132-case .p132-cover-visual img{
    width:100%!important;
    height:100%!important;
    min-height:0!important;
    object-fit:cover!important;
    object-position:center!important;
    transform:none!important;
  }

  /* Service/project pages such as /project-repair/: same left-band composition. */
  .p129-service .p129-svc-hero{
    min-height:0!important;
    padding:clamp(64px,5.8vw,96px) 0 clamp(64px,6vw,96px)!important;
    overflow:hidden!important;
  }
  .p129-service .p129-shell.p129-svc-grid{
    display:grid!important;
    grid-template-columns:minmax(0,1.22fr) minmax(280px,.40fr)!important;
    width:min(1380px,calc(100% - 72px))!important;
    max-width:1380px!important;
    margin:0 auto!important;
    padding:0!important;
    gap:clamp(28px,3.2vw,46px)!important;
    align-items:center!important;
    direction:ltr!important;
    transform:none!important;
    translate:none!important;
  }
  .p129-service .p129-svc-copy{
    grid-column:1!important;
    grid-row:1!important;
    order:1!important;
    width:100%!important;
    max-width:850px!important;
    min-width:0!important;
    min-height:clamp(450px,37vw,570px)!important;
    margin:0!important;
    padding:clamp(34px,4vw,62px)!important;
    display:flex!important;
    flex-direction:column!important;
    justify-content:center!important;
    align-self:stretch!important;
    justify-self:start!important;
    position:relative!important;
    inset:auto!important;
    transform:none!important;
    translate:none!important;
    background:transparent!important;
    border:0!important;
    box-shadow:none!important;
  }
  .p129-service .p129-svc-copy h1{
    width:100%!important;
    max-width:13.5ch!important;
    margin:.85rem 0 1.15rem!important;
    font-size:clamp(58px,5.25vw,98px)!important;
    line-height:.9!important;
    letter-spacing:-.058em!important;
    text-wrap:balance!important;
    overflow-wrap:normal!important;
    word-break:normal!important;
  }
  .p129-service .p129-lead{
    width:100%!important;
    max-width:58ch!important;
    margin:0!important;
    font-size:clamp(17px,1.12vw,20px)!important;
    line-height:1.72!important;
    color:rgba(238,242,239,.82)!important;
    text-wrap:pretty!important;
  }
  .p129-service .p129-svc-actions{margin-top:1.85rem!important}
  .p129-service .p129-svc-board{
    grid-column:2!important;
    grid-row:1!important;
    order:2!important;
    width:100%!important;
    max-width:330px!important;
    min-width:0!important;
    margin:0!important;
    align-self:center!important;
    justify-self:end!important;
    transform:none!important;
    translate:none!important;
  }
}

@media(max-width:980px){
  .p132-case .p132-shell.p132-cover-grid,
  .p129-service .p129-shell.p129-svc-grid{
    display:grid!important;
    grid-template-columns:1fr!important;
    width:min(100% - 32px,820px)!important;
    gap:24px!important;
  }
  .p132-case .p132-cover-copy,
  .p129-service .p129-svc-copy{
    grid-column:1!important;
    grid-row:auto!important;
    width:100%!important;
    max-width:none!important;
    min-height:0!important;
    padding:clamp(24px,6vw,38px)!important;
  }
  .p132-case .p132-cover h1,
  .p129-service .p129-svc-copy h1{
    max-width:100%!important;
    font-size:clamp(48px,10vw,76px)!important;
  }
  .p132-case .p132-cover-visual,
  .p129-service .p129-svc-board{
    grid-column:1!important;
    grid-row:auto!important;
    width:100%!important;
    max-width:none!important;
    justify-self:stretch!important;
  }
  .p132-case .p132-cover-visual{aspect-ratio:16/10!important}
}

@media(max-width:600px){
  .p132-case .p132-shell.p132-cover-grid,
  .p129-service .p129-shell.p129-svc-grid{width:calc(100% - 24px)!important}
  .p132-case .p132-cover,
  .p129-service .p129-svc-hero{padding:38px 0 56px!important}
  .p132-case .p132-cover h1,
  .p129-service .p129-svc-copy h1{
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
    raise SystemExit("stage154: no detailed case pages found")
for path in case_pages:
    final = path.read_text(encoding="utf-8")
    if MARKER not in final or "p132-cover-copy" not in final:
        raise SystemExit(f"stage154: case guard failed: {path}")

repair = ROOT / "project-repair" / "index.html"
if not repair.is_file():
    raise SystemExit("stage154: project-repair page missing")
repair_html = repair.read_text(encoding="utf-8")
if MARKER not in repair_html or "p129-svc-copy" not in repair_html:
    raise SystemExit("stage154: project-repair guard failed")

print(f"stage154 text into existing band: {len(changed)} pages, {len(case_pages)} cases guarded")
