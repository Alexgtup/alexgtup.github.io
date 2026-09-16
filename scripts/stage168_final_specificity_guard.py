#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage168-final-specificity-guard"

STYLE = r'''<style id="stage168-final-specificity-guard">
/* High-specificity contract: beats legacy !important selectors from old themes. */

body[data-ux-family="hub"] main.p130-hub section.x146-depth,
body[data-ux-family="service"] main section.x146-depth,
body[data-ux-family="guide"] main section.x146-depth,
body[data-ux-family="case"] main section.x146-depth{
  margin:0!important;
  padding:0!important;
  background:
    radial-gradient(44rem 26rem at 88% 0%,rgba(108,132,255,.075),transparent 72%),
    radial-gradient(36rem 26rem at 4% 100%,rgba(201,255,74,.035),transparent 72%),
    #0a0d10!important;
  color:#f3f6f4!important;
  border-top:1px solid rgba(255,255,255,.095)!important;
  border-bottom:1px solid rgba(255,255,255,.095)!important;
}
body[data-ux-family="hub"] main.p130-hub section.x146-depth>.x146-depth__inner,
body[data-ux-family="service"] main section.x146-depth>.x146-depth__inner,
body[data-ux-family="guide"] main section.x146-depth>.x146-depth__inner,
body[data-ux-family="case"] main section.x146-depth>.x146-depth__inner{
  width:min(1320px,calc(100% - 64px))!important;
  max-width:1320px!important;
  margin:0 auto!important;
  padding:clamp(72px,7vw,112px) 0!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__head,
body[data-ux-family="service"] main .x146-depth__head,
body[data-ux-family="guide"] main .x146-depth__head,
body[data-ux-family="case"] main .x146-depth__head{
  display:grid!important;
  grid-template-columns:minmax(120px,.30fr) minmax(0,1.25fr)!important;
  gap:clamp(28px,5vw,78px)!important;
  align-items:start!important;
  margin:0 0 clamp(38px,4.5vw,64px)!important;
  padding:0!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__eyebrow,
body[data-ux-family="service"] main .x146-depth__eyebrow,
body[data-ux-family="guide"] main .x146-depth__eyebrow,
body[data-ux-family="case"] main .x146-depth__eyebrow{
  margin:7px 0 0!important;
  color:rgba(226,233,230,.50)!important;
  font:700 11px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace!important;
  letter-spacing:.17em!important;
  text-transform:uppercase!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__head h2,
body[data-ux-family="service"] main .x146-depth__head h2,
body[data-ux-family="guide"] main .x146-depth__head h2,
body[data-ux-family="case"] main .x146-depth__head h2{
  max-width:18ch!important;
  margin:0!important;
  color:#f3f6f4!important;
  font-size:clamp(40px,4.5vw,70px)!important;
  line-height:.98!important;
  letter-spacing:-.052em!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__intro,
body[data-ux-family="service"] main .x146-depth__intro,
body[data-ux-family="guide"] main .x146-depth__intro,
body[data-ux-family="case"] main .x146-depth__intro{
  max-width:78ch!important;
  margin:22px 0 0!important;
  color:rgba(226,233,230,.70)!important;
  font-size:clamp(16px,1.15vw,19px)!important;
  line-height:1.72!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__grid,
body[data-ux-family="service"] main .x146-depth__grid,
body[data-ux-family="guide"] main .x146-depth__grid,
body[data-ux-family="case"] main .x146-depth__grid{
  display:grid!important;
  grid-template-columns:repeat(2,minmax(0,1fr))!important;
  gap:16px!important;
  margin:0!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__card,
body[data-ux-family="service"] main .x146-depth__card,
body[data-ux-family="guide"] main .x146-depth__card,
body[data-ux-family="case"] main .x146-depth__card{
  min-height:0!important;
  margin:0!important;
  padding:clamp(24px,2.5vw,34px)!important;
  border:1px solid rgba(255,255,255,.095)!important;
  border-radius:24px!important;
  background:linear-gradient(145deg,rgba(255,255,255,.045),rgba(255,255,255,.012)),#0d1115!important;
  color:#f3f6f4!important;
  box-shadow:0 18px 54px rgba(0,0,0,.18)!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__card h3,
body[data-ux-family="service"] main .x146-depth__card h3,
body[data-ux-family="guide"] main .x146-depth__card h3,
body[data-ux-family="case"] main .x146-depth__card h3{
  margin:0!important;color:#f3f6f4!important;font-size:clamp(20px,1.65vw,26px)!important;line-height:1.12!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__card p,
body[data-ux-family="service"] main .x146-depth__card p,
body[data-ux-family="guide"] main .x146-depth__card p,
body[data-ux-family="case"] main .x146-depth__card p{
  margin:14px 0 0!important;color:rgba(226,233,230,.70)!important;font-size:clamp(15px,1vw,17px)!important;line-height:1.68!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__links,
body[data-ux-family="service"] main .x146-depth__links,
body[data-ux-family="guide"] main .x146-depth__links,
body[data-ux-family="case"] main .x146-depth__links{
  display:flex!important;flex-wrap:wrap!important;gap:9px!important;margin:clamp(28px,3vw,42px) 0 0!important;padding:0!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__links a,
body[data-ux-family="service"] main .x146-depth__links a,
body[data-ux-family="guide"] main .x146-depth__links a,
body[data-ux-family="case"] main .x146-depth__links a{
  display:inline-flex!important;align-items:center!important;min-height:40px!important;padding:9px 13px!important;
  border:1px solid rgba(255,255,255,.095)!important;border-radius:999px!important;background:rgba(255,255,255,.025)!important;
  color:rgba(238,243,240,.82)!important;text-decoration:none!important;font-size:13px!important;
}

/* Hub-specific SEO sections were previously forced back to the light paper theme. */
body[data-ux-family="hub"] main.p130-hub section.secondary-demand{
  margin:0!important;padding:0!important;background:#07090b!important;color:#f3f6f4!important;border-top:1px solid rgba(255,255,255,.095)!important;
}
body[data-ux-family="hub"] main.p130-hub section.secondary-demand>.secondary-demand__inner{
  width:min(1320px,calc(100% - 64px))!important;max-width:1320px!important;margin:0 auto!important;padding:clamp(68px,6.5vw,104px) 0!important;
}
body[data-ux-family="hub"] main.p130-hub .secondary-demand__grid{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:14px!important;}
body[data-ux-family="hub"] main.p130-hub .secondary-demand__card{
  min-height:0!important;padding:24px!important;border:1px solid rgba(255,255,255,.095)!important;border-radius:22px!important;background:#0d1115!important;color:#f3f6f4!important;
}
body[data-ux-family="hub"] main.p130-hub .secondary-demand__card h3{color:#f3f6f4!important;}
body[data-ux-family="hub"] main.p130-hub .secondary-demand__card p{color:rgba(226,233,230,.70)!important;}

/* Service end CTA must always be readable. */
body[data-ux-family="service"] main section.p129-contact{
  padding:clamp(70px,7vw,108px) 0!important;background:#07090b!important;color:#f3f6f4!important;
}
body[data-ux-family="service"] main section.p129-contact>.p129-shell{
  width:min(1240px,calc(100% - 64px))!important;max-width:1240px!important;margin:0 auto!important;padding:0!important;
}
body[data-ux-family="service"] main section.p129-contact .p129-contact-card{
  display:grid!important;grid-template-columns:minmax(0,1fr) auto!important;gap:clamp(30px,5vw,74px)!important;align-items:end!important;
  margin:0!important;padding:clamp(34px,4vw,58px)!important;border:1px solid rgba(255,255,255,.14)!important;border-radius:28px!important;
  background:radial-gradient(32rem 20rem at 86% 0%,rgba(108,132,255,.10),transparent 72%),linear-gradient(145deg,rgba(255,255,255,.045),rgba(255,255,255,.012)),#0d1115!important;
  color:#f3f6f4!important;box-shadow:0 28px 80px rgba(0,0,0,.24)!important;
}
body[data-ux-family="service"] main section.p129-contact .p129-contact-card h2{
  max-width:13ch!important;margin:10px 0 16px!important;color:#f3f6f4!important;font-size:clamp(36px,4vw,60px)!important;line-height:.98!important;letter-spacing:-.05em!important;
}
body[data-ux-family="service"] main section.p129-contact .p129-contact-card p{
  max-width:65ch!important;margin:0!important;color:rgba(226,233,230,.70)!important;font-size:16px!important;line-height:1.68!important;
}
body[data-ux-family="service"] main section.p129-contact .p129-contact-card .p129-btn{
  background:#c9ff4a!important;color:#071008!important;border-color:rgba(201,255,74,.42)!important;font-weight:800!important;text-decoration:none!important;
}

/* Case result/demo endcaps must not inherit black typography. */
body[data-ux-family="case"] main section.contact.stage108-endcap,
body[data-ux-family="case"] main section.p132-end{
  color:#f3f6f4!important;
}
body[data-ux-family="case"] main section.contact.stage108-endcap .status-card,
body[data-ux-family="case"] main section.p132-end .status-card{
  color:#f3f6f4!important;background:rgba(5,9,12,.82)!important;border-color:rgba(255,255,255,.11)!important;
}
body[data-ux-family="case"] main section.contact.stage108-endcap .status-card h2,
body[data-ux-family="case"] main section.p132-end .status-card h2{
  color:#f3f6f4!important;
}
body[data-ux-family="case"] main section.contact.stage108-endcap .status-card h2 em,
body[data-ux-family="case"] main section.p132-end .status-card h2 em{
  color:#c9ff4a!important;
}
body[data-ux-family="case"] main section.contact.stage108-endcap .status-card p,
body[data-ux-family="case"] main section.p132-end .status-card p{
  color:rgba(226,233,230,.70)!important;
}

@media(max-width:980px){
  body[data-ux-family="hub"] main.p130-hub section.x146-depth>.x146-depth__inner,
  body[data-ux-family="service"] main section.x146-depth>.x146-depth__inner,
  body[data-ux-family="guide"] main section.x146-depth>.x146-depth__inner,
  body[data-ux-family="case"] main section.x146-depth>.x146-depth__inner,
  body[data-ux-family="hub"] main.p130-hub section.secondary-demand>.secondary-demand__inner,
  body[data-ux-family="service"] main section.p129-contact>.p129-shell{
    width:min(100% - 28px,860px)!important;
  }
  body[data-ux-family="hub"] main.p130-hub .x146-depth__head,
  body[data-ux-family="service"] main .x146-depth__head,
  body[data-ux-family="guide"] main .x146-depth__head,
  body[data-ux-family="case"] main .x146-depth__head{grid-template-columns:1fr!important;gap:16px!important;}
  body[data-ux-family="hub"] main.p130-hub .x146-depth__grid,
  body[data-ux-family="service"] main .x146-depth__grid,
  body[data-ux-family="guide"] main .x146-depth__grid,
  body[data-ux-family="case"] main .x146-depth__grid,
  body[data-ux-family="hub"] main.p130-hub .secondary-demand__grid{grid-template-columns:1fr!important;}
  body[data-ux-family="service"] main section.p129-contact .p129-contact-card{grid-template-columns:1fr!important;align-items:start!important;}
}
@media(max-width:600px){
  body[data-ux-family="hub"] main.p130-hub section.x146-depth>.x146-depth__inner,
  body[data-ux-family="service"] main section.x146-depth>.x146-depth__inner,
  body[data-ux-family="guide"] main section.x146-depth>.x146-depth__inner,
  body[data-ux-family="case"] main section.x146-depth>.x146-depth__inner,
  body[data-ux-family="hub"] main.p130-hub section.secondary-demand>.secondary-demand__inner,
  body[data-ux-family="service"] main section.p129-contact>.p129-shell{
    width:calc(100% - 24px)!important;
  }
}
</style>'''

changed = []
for path in sorted(ROOT.rglob("index.html")):
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("en/"):
        continue
    text = path.read_text(encoding="utf-8")
    if "</head>" not in text:
        continue
    text = re.sub(r'<style\s+id=["\']stage168-final-specificity-guard["\']>.*?</style>', '', text, flags=re.I | re.S)
    text = text.replace("</head>", STYLE + "</head>", 1)
    path.write_text(text, encoding="utf-8")
    changed.append(rel)

for rel in ["cases/index.html","cases/sheetpilot-ai/index.html","python-development/index.html","api-integrations/index.html","services/index.html","guides/index.html"]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    if text.count(MARKER) != 1:
        raise SystemExit(f"stage168: marker guard failed {rel}")

print(f"stage168 specificity guard: {len(changed)} pages")
