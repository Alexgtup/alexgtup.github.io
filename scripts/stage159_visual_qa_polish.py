#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import subprocess
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage159-visual-qa"

STYLE = r'''<style id="stage159-visual-qa">
/* stage159 visual QA polish */
html,body{max-width:100%;overflow-x:clip}
main,main>*,section,article,[class*="shell"],[class*="grid"]{min-width:0}
img,video,canvas,svg{max-width:100%}

/* Runtime-independent visibility after retiring old cinematic/reveal layers. */
body[data-ux-family="hub"] .wow-reveal,
body[data-ux-family="service"] .wow-reveal,
body[data-ux-family="guide"] .wow-reveal{
  opacity:1!important;visibility:visible!important;transform:none!important;translate:none!important;filter:none!important;
}

/* Cases hub: remove the legacy paper world that survived the runtime cleanup. */
main.p130-hub[data-stage130-hub="cases"]{
  background:
    radial-gradient(58rem 34rem at 82% 8%,rgba(109,137,255,.09),transparent 68%),
    radial-gradient(44rem 30rem at 8% 38%,rgba(168,224,164,.045),transparent 72%),
    #070a0c!important;
  color:#f5f7f4!important;
}
main.p130-hub[data-stage130-hub="cases"] .p130-hero{color:#f5f7f4!important;}
main.p130-hub[data-stage130-hub="cases"] .p130-hero h1{color:#f5f7f4!important;}
main.p130-hub[data-stage130-hub="cases"] .p130-lead{color:rgba(232,238,235,.72)!important;}
main.p130-hub[data-stage130-hub="cases"] .p130-list-section,
main.p130-hub[data-stage130-hub="cases"] .p130-footer-cta,
main.p130-hub[data-stage130-hub="cases"] .x146-depth{background:transparent!important;color:#f5f7f4!important;}
main.p130-hub[data-stage130-hub="cases"] .p130-list-section{padding:0 0 clamp(90px,9vw,138px)!important;}
main.p130-hub[data-stage130-hub="cases"] .p130-mosaic{gap:clamp(14px,1.5vw,22px)!important;}
main.p130-hub[data-stage130-hub="cases"] .p130-tile{
  border:1px solid rgba(255,255,255,.085)!important;border-radius:26px!important;
  background:linear-gradient(145deg,rgba(255,255,255,.045),rgba(255,255,255,.015)),#0b0f13!important;
  box-shadow:0 20px 64px rgba(0,0,0,.20)!important;overflow:hidden!important;
}
main.p130-hub[data-stage130-hub="cases"] .p130-tile__body,
main.p130-hub[data-stage130-hub="cases"] .p130-text-tile{color:#f5f7f4!important;}
main.p130-hub[data-stage130-hub="cases"] .p130-tile :is(strong,h2,h3){color:#f5f7f4!important;}
main.p130-hub[data-stage130-hub="cases"] .p130-tile :is(span,p){color:rgba(224,231,235,.68)!important;}
main.p130-hub[data-stage130-hub="cases"] .p130-tile__media{background:#0a0e12!important;}
main.p130-hub[data-stage130-hub="cases"] .p130-tile__media img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important;}

/* Service hero boards: the old light-world typography was surviving on a dark card. */
body[data-ux-family="service"] .p155-service-preview .p129-svc-board{color:#eef2f1!important;}
body[data-ux-family="service"] .p155-service-preview .p129-svc-board .p129-svc-no{
  color:rgba(255,255,255,.08)!important;-webkit-text-stroke:1px rgba(255,255,255,.07)!important;
}
body[data-ux-family="service"] .p155-service-preview .p129-svc-board h2{
  color:#f5f7f4!important;font-size:clamp(30px,3vw,48px)!important;line-height:.96!important;letter-spacing:-.045em!important;
}
body[data-ux-family="service"] .p155-service-preview .p129-svc-board li{
  color:rgba(226,233,236,.72)!important;border-top-color:rgba(255,255,255,.08)!important;
}
body[data-ux-family="service"] .p155-service-preview .p129-svc-board li::marker{color:#b7ff55!important;}
body[data-ux-family="service"] :is(.p129-outcomes,.p129-process,.p129-cases,.p129-faq,.p129-final){overflow:clip!important;}

/* About keeps its warm identity, but restores readable contrast. */
main.p130-hub[data-stage130-hub="about"] .p130-hero h1{color:#17140f!important;}
main.p130-hub[data-stage130-hub="about"] .p130-hero h1 span{color:#d34d43!important;}
main.p130-hub[data-stage130-hub="about"] .p130-lead{color:rgba(23,20,15,.70)!important;}
main.p130-hub[data-stage130-hub="about"] .p130-kicker{color:rgba(23,20,15,.52)!important;}

/* Legacy WordPress landing was the only RU service page still using the pre-p129 hero. */
body[data-page="wordpress-development"] .container.hero{
  width:min(1480px,calc(100% - 64px))!important;max-width:1480px!important;margin:0 auto!important;
  padding:clamp(70px,7vw,112px) 0 clamp(86px,8vw,128px)!important;
  display:grid!important;grid-template-columns:minmax(0,1.14fr) minmax(360px,.66fr)!important;
  gap:clamp(54px,6vw,96px)!important;align-items:center!important;
}
body[data-page="wordpress-development"] .container.hero>div:first-child{min-width:0!important;}
body[data-page="wordpress-development"] .container.hero h1{
  width:100%!important;max-width:none!important;margin:18px 0 28px!important;
  font-size:clamp(68px,6.1vw,108px)!important;line-height:.89!important;letter-spacing:-.068em!important;text-wrap:pretty!important;
}
body[data-page="wordpress-development"] .container.hero h1 em{color:#ff765e!important;}
body[data-page="wordpress-development"] .container.hero .lead{max-width:68ch!important;}
body[data-page="wordpress-development"] .container.hero .hero-side{width:100%!important;max-width:470px!important;justify-self:end!important;}

/* A final rhythm pass for wide editorial pages. */
@media(min-width:981px){
  body[data-ux-family="hub"] .p130-hero-side{margin-top:0!important;}
  body[data-ux-family="service"] .p155-service-preview{margin-top:0!important;}
}
@media(max-width:980px){
  main.p130-hub[data-stage130-hub="cases"] .p130-hero{padding-top:48px!important;}
  body[data-page="wordpress-development"] .container.hero{
    width:min(100% - 28px,860px)!important;grid-template-columns:1fr!important;gap:36px!important;padding:48px 0 72px!important;
  }
  body[data-page="wordpress-development"] .container.hero h1{font-size:clamp(50px,11vw,78px)!important;}
  body[data-page="wordpress-development"] .container.hero .hero-side{justify-self:start!important;max-width:680px!important;}
}
@media(max-width:600px){
  main.p130-hub[data-stage130-hub="cases"] .p130-shell.p130-hero-grid,
  body[data-page="wordpress-development"] .container.hero{width:calc(100% - 24px)!important;}
  body[data-ux-family="service"] .p155-service-preview .p129-svc-board{padding:24px!important;border-radius:22px!important;}
}
</style>'''

changed = 0
for path in sorted(ROOT.rglob("index.html")):
    html = path.read_text(encoding="utf-8")
    if MARKER in html:
        continue
    if "</head>" not in html:
        raise SystemExit(f"stage159: head missing: {path}")
    html = html.replace("</head>", STYLE + "</head>", 1)
    path.write_text(html, encoding="utf-8")
    changed += 1

checks = {
    ROOT / "cases" / "index.html": [MARKER, 'data-stage130-hub="cases"'],
    ROOT / "development" / "index.html": [MARKER, "p129-svc-board"],
    ROOT / "wordpress-development" / "index.html": [MARKER, 'data-page="wordpress-development"'],
    ROOT / "about" / "index.html": [MARKER, 'data-stage130-hub="about"'],
}
for path, needles in checks.items():
    if not path.is_file():
        raise SystemExit(f"stage159: required page missing: {path}")
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"stage159: guard failed {needle}: {path}")

print(f"stage159 visual QA polish: {changed} pages")
subprocess.run([sys.executable, str(Path(__file__).with_name("stage160_hub_dark_polish.py")), str(ROOT)], check=True)
subprocess.run([sys.executable, str(Path(__file__).with_name("stage162_copy_quality_cleanup.py")), str(ROOT)], check=True)
