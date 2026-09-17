#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage167-component-theme-pairs"

STYLE = r'''<style id="stage167-component-theme-pairs">
:root{
  --ux-dark:#07090b;--ux-dark-2:#0b1015;--ux-card:#0d1115;
  --ux-light:#f2efe8;--ux-light-2:#ebe7de;--ux-paper:#fbfaf7;
  --ux-white:#f3f6f4;--ux-ink:#171914;
  --ux-muted-dark:#596058;--ux-muted-light:rgba(226,233,230,.72);
  --ux-line-dark:rgba(255,255,255,.10);--ux-line-light:rgba(27,31,25,.12);
  --ux-lime:#c9ff4a;--ux-coral:#ff765e;
}

/* HUB discovery/editorial sections: LIGHT surface + DARK type. */
body[data-ux-family="hub"] main.p130-hub .x146-depth{
  margin:0!important;padding:0!important;overflow:hidden!important;
  background:
    radial-gradient(48rem 28rem at 92% 0%,rgba(126,112,211,.09),transparent 70%),
    radial-gradient(38rem 26rem at 4% 100%,rgba(201,255,74,.08),transparent 72%),
    linear-gradient(135deg,var(--ux-light),var(--ux-light-2))!important;
  color:var(--ux-ink)!important;
  border-top:1px solid var(--ux-line-light)!important;
  border-bottom:1px solid var(--ux-line-light)!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__inner{
  width:min(1320px,calc(100% - 64px))!important;max-width:1320px!important;
  margin:0 auto!important;padding:clamp(72px,7vw,112px) 0!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__head{
  display:grid!important;grid-template-columns:minmax(120px,.30fr) minmax(0,1.25fr)!important;
  gap:clamp(28px,5vw,78px)!important;align-items:start!important;margin:0 0 clamp(38px,4.5vw,64px)!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth :is(h2,h3){color:var(--ux-ink)!important;}
body[data-ux-family="hub"] main.p130-hub .x146-depth__head h2{
  max-width:18ch!important;margin:0!important;font-size:clamp(40px,4.5vw,70px)!important;
  line-height:.98!important;letter-spacing:-.052em!important;text-wrap:balance!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__eyebrow{
  color:#6b7167!important;font:700 11px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace!important;
  letter-spacing:.17em!important;text-transform:uppercase!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__intro{
  max-width:78ch!important;margin:22px 0 0!important;color:#4f554d!important;
  font-size:clamp(16px,1.15vw,19px)!important;line-height:1.72!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__grid{
  display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:16px!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__card{
  min-height:0!important;padding:clamp(24px,2.5vw,34px)!important;
  border:1px solid var(--ux-line-light)!important;border-radius:24px!important;
  background:rgba(255,255,255,.70)!important;color:var(--ux-ink)!important;
  box-shadow:0 18px 50px rgba(40,37,31,.06)!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__card p{
  margin:14px 0 0!important;color:#555c53!important;font-size:clamp(15px,1vw,17px)!important;line-height:1.68!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__links{
  display:flex!important;flex-wrap:wrap!important;gap:9px!important;margin:clamp(28px,3vw,42px) 0 0!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__links a{
  padding:9px 13px!important;border:1px solid rgba(27,31,25,.15)!important;border-radius:999px!important;
  background:rgba(255,255,255,.74)!important;color:#252922!important;text-decoration:none!important;font-size:13px!important;
}

/* Service SEO sections: DARK surface + LIGHT type. */
body[data-ux-family="service"] main .x146-depth{
  margin:0!important;padding:0!important;background:#0a0d10!important;color:var(--ux-white)!important;
  border-top:1px solid var(--ux-line-dark)!important;border-bottom:1px solid var(--ux-line-dark)!important;
}
body[data-ux-family="service"] main .x146-depth__inner{
  width:min(1320px,calc(100% - 64px))!important;max-width:1320px!important;margin:0 auto!important;
  padding:clamp(72px,7vw,112px) 0!important;
}
body[data-ux-family="service"] main .x146-depth__head{
  display:grid!important;grid-template-columns:minmax(120px,.30fr) minmax(0,1.25fr)!important;
  gap:clamp(28px,5vw,78px)!important;margin:0 0 clamp(38px,4.5vw,64px)!important;
}
body[data-ux-family="service"] main .x146-depth :is(h2,h3){color:var(--ux-white)!important;}
body[data-ux-family="service"] main .x146-depth__head h2{
  max-width:18ch!important;margin:0!important;font-size:clamp(40px,4.5vw,70px)!important;line-height:.98!important;letter-spacing:-.052em!important;
}
body[data-ux-family="service"] main .x146-depth__eyebrow{color:rgba(226,233,230,.50)!important;}
body[data-ux-family="service"] main .x146-depth__intro{color:var(--ux-muted-light)!important;max-width:78ch!important;line-height:1.72!important;}
body[data-ux-family="service"] main .x146-depth__grid{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:16px!important;}
body[data-ux-family="service"] main .x146-depth__card{
  padding:clamp(24px,2.5vw,34px)!important;border:1px solid var(--ux-line-dark)!important;border-radius:24px!important;
  background:linear-gradient(145deg,rgba(255,255,255,.045),rgba(255,255,255,.012)),var(--ux-card)!important;color:var(--ux-white)!important;
}
body[data-ux-family="service"] main .x146-depth__card p{color:var(--ux-muted-light)!important;line-height:1.68!important;}
body[data-ux-family="service"] main .x146-depth__links a{
  color:rgba(238,243,240,.84)!important;border:1px solid var(--ux-line-dark)!important;background:rgba(255,255,255,.025)!important;
}

/* Secondary demand alternates by page family instead of inheriting blindly. */
body[data-ux-family="hub"] main.p130-hub .secondary-demand{
  background:var(--ux-paper)!important;color:var(--ux-ink)!important;border-top:1px solid var(--ux-line-light)!important;
}
body[data-ux-family="hub"] main.p130-hub .secondary-demand :is(h2,h3){color:var(--ux-ink)!important;}
body[data-ux-family="hub"] main.p130-hub .secondary-demand :is(p,.secondary-demand__intro){color:#555c53!important;}
body[data-ux-family="hub"] main.p130-hub .secondary-demand__card{
  background:#fff!important;color:var(--ux-ink)!important;border:1px solid var(--ux-line-light)!important;
}
body[data-ux-family="service"] main .secondary-demand{
  background:var(--ux-dark)!important;color:var(--ux-white)!important;border-top:1px solid var(--ux-line-dark)!important;
}
body[data-ux-family="service"] main .secondary-demand :is(h2,h3){color:var(--ux-white)!important;}
body[data-ux-family="service"] main .secondary-demand :is(p,.secondary-demand__intro){color:var(--ux-muted-light)!important;}
body[data-ux-family="service"] main .secondary-demand__card{
  background:var(--ux-card)!important;color:var(--ux-white)!important;border:1px solid var(--ux-line-dark)!important;
}
.secondary-demand__inner,.secondary-demand__shell{
  width:min(1320px,calc(100% - 64px))!important;max-width:1320px!important;margin:0 auto!important;padding:clamp(68px,6.5vw,104px) 0!important;
}
.secondary-demand__grid{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:14px!important;}
.secondary-demand__card{min-height:0!important;padding:24px!important;border-radius:22px!important;}

/* Explicit DARK conversion components always carry LIGHT type. */
body[data-ux-family="service"] .p129-contact-card,
body[data-ux-family="case"] .status-card{
  color:var(--ux-white)!important;background:var(--ux-card)!important;border-color:var(--ux-line-dark)!important;
}
body[data-ux-family="service"] .p129-contact-card :is(h2,h3,strong),
body[data-ux-family="case"] .status-card :is(h2,h3,strong){color:var(--ux-white)!important;}
body[data-ux-family="service"] .p129-contact-card p,
body[data-ux-family="case"] .status-card p{color:var(--ux-muted-light)!important;}
body[data-ux-family="service"] .p129-contact-card .p129-btn,
body[data-ux-family="case"] .status-card .btn.primary{
  background:var(--ux-lime)!important;color:#071008!important;border-color:var(--ux-lime)!important;
}

/* Search conversion bridge: only force case routes, which are dark. */
body[data-ux-family="case"] .s165-bridge{color:var(--ux-white)!important;border-top-color:var(--ux-line-dark)!important;}
body[data-ux-family="case"] .s165-bridge h2{color:var(--ux-white)!important;}
body[data-ux-family="case"] .s165-bridge__copy,
body[data-ux-family="case"] .s165-bridge__link span{color:var(--ux-muted-light)!important;opacity:1!important;}
body[data-ux-family="case"] .s165-bridge__link strong,
body[data-ux-family="case"] .s165-bridge__contact{color:var(--ux-white)!important;}

@media(max-width:900px){
  body[data-ux-family="hub"] main.p130-hub .x146-depth__inner,
  body[data-ux-family="service"] main .x146-depth__inner,
  .secondary-demand__inner,.secondary-demand__shell{width:min(100% - 28px,860px)!important;}
  body[data-ux-family="hub"] main.p130-hub .x146-depth__head,
  body[data-ux-family="service"] main .x146-depth__head{grid-template-columns:1fr!important;gap:18px!important;}
  body[data-ux-family="hub"] main.p130-hub .x146-depth__grid,
  body[data-ux-family="service"] main .x146-depth__grid,
  .secondary-demand__grid{grid-template-columns:1fr!important;}
}
@media(max-width:600px){
  body[data-ux-family="hub"] main.p130-hub .x146-depth__inner,
  body[data-ux-family="service"] main .x146-depth__inner,
  .secondary-demand__inner,.secondary-demand__shell{width:calc(100% - 24px)!important;}
}
</style>'''

changed=[]
for path in sorted(ROOT.rglob("index.html")):
    rel=path.relative_to(ROOT).as_posix()
    if rel.startswith("en/"):
        continue
    text=path.read_text(encoding="utf-8")
    if "</head>" not in text:
        continue
    text=re.sub(r'<style\s+id=["\']stage167-(?:final-design-system|component-theme-pairs)["\']>.*?</style>','',text,flags=re.I|re.S)
    text=text.replace("</head>",STYLE+"</head>",1)
    path.write_text(text,encoding="utf-8")
    changed.append(rel)

for rel in ["cases/index.html","services/index.html","guides/index.html","api-integrations/index.html","python-development/index.html"]:
    text=(ROOT/rel).read_text(encoding="utf-8")
    if text.count(MARKER)!=1:
        raise SystemExit(f"stage167: marker guard failed {rel}")

print(f"stage167 component theme pairs: {len(changed)} pages")
