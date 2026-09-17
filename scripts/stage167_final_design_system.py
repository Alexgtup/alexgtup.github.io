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
  display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:0 clamp(34px,5vw,72px)!important;
}
body[data-ux-family="hub"] main.p130-hub .x146-depth__card{
  min-height:0!important;padding:clamp(26px,3vw,40px) 0!important;
  border:0!important;border-top:1px solid var(--ux-line-light)!important;border-radius:0!important;
  background:transparent!important;color:var(--ux-ink)!important;box-shadow:none!important;
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
body[data-ux-family="service"] main .x146-depth__grid{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:0 clamp(34px,5vw,72px)!important;}
body[data-ux-family="service"] main .x146-depth__card{
  padding:clamp(26px,3vw,40px) 0!important;border:0!important;border-top:1px solid var(--ux-line-dark)!important;border-radius:0!important;
  background:transparent!important;color:var(--ux-white)!important;box-shadow:none!important;
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
  background:transparent!important;color:var(--ux-ink)!important;border:0!important;border-top:1px solid var(--ux-line-light)!important;
}
body[data-ux-family="service"] main .secondary-demand{
  background:var(--ux-dark)!important;color:var(--ux-white)!important;border-top:1px solid var(--ux-line-dark)!important;
}
body[data-ux-family="service"] main .secondary-demand :is(h2,h3){color:var(--ux-white)!important;}
body[data-ux-family="service"] main .secondary-demand :is(p,.secondary-demand__intro){color:var(--ux-muted-light)!important;}
body[data-ux-family="service"] main .secondary-demand__card{
  background:transparent!important;color:var(--ux-white)!important;border:0!important;border-top:1px solid var(--ux-line-dark)!important;
}
.secondary-demand__inner,.secondary-demand__shell{
  width:min(1320px,calc(100% - 64px))!important;max-width:1320px!important;margin:0 auto!important;padding:clamp(68px,6.5vw,104px) 0!important;
}
.secondary-demand__grid{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:0 clamp(28px,4vw,56px)!important;}
.secondary-demand__card{min-height:0!important;padding:clamp(24px,2.5vw,34px) 0!important;border-radius:0!important;box-shadow:none!important;}

/* Stage 172: high-intent task map. Keeps SEO links useful for people instead of rendering a keyword wall. */
body[data-ux-family="service"] main .stage172-task-map{
  background:#080b0e!important;color:var(--ux-white)!important;border-top:1px solid var(--ux-line-dark)!important;
}
.stage172-task-map__shell{width:min(1320px,calc(100% - 64px));margin:0 auto;padding:clamp(72px,7vw,112px) 0;}
.stage172-task-map__head{display:grid;grid-template-columns:minmax(120px,.3fr) minmax(0,1.2fr);gap:clamp(28px,5vw,78px);align-items:start;margin-bottom:clamp(34px,4vw,56px);}
.stage172-task-map__eyebrow,.stage172-task-map__group>p{margin:0;color:#7f8b91;font:700 11px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.15em;text-transform:uppercase;}
.stage172-task-map__head h2{margin:0;max-width:15ch;color:var(--ux-white);font-size:clamp(40px,4.5vw,70px);line-height:.96;letter-spacing:-.052em;text-wrap:balance;}
.stage172-task-map__head>div>p{max-width:62ch;margin:18px 0 0;color:var(--ux-muted-light);font-size:clamp(15px,1.05vw,18px);line-height:1.7;}
.stage172-task-map__grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;}
.stage172-task-map__group{position:relative;overflow:hidden;padding:clamp(24px,3vw,38px);border:1px solid var(--ux-line-dark);border-radius:20px;background:linear-gradient(145deg,rgba(255,255,255,.035),rgba(255,255,255,.012));}
.stage172-task-map__group:before{content:"";position:absolute;inset:0 auto 0 0;width:2px;background:var(--ux-lime);opacity:.32;}
.stage172-task-map__group h3{margin:12px 0 24px;color:var(--ux-white);font-size:clamp(24px,2.2vw,34px);line-height:1;letter-spacing:-.04em;}
.stage172-task-map__group nav{display:grid;}
.stage172-task-map__group nav a{display:grid;grid-template-columns:minmax(0,1fr) auto 20px;gap:14px;align-items:center;padding:15px 0;border-top:1px solid var(--ux-line-dark);color:var(--ux-white)!important;text-decoration:none!important;transition:padding-left .18s ease,color .18s ease;}
.stage172-task-map__group nav a:hover{padding-left:8px;color:var(--ux-lime)!important;}
.stage172-task-map__group nav strong{font-size:15px;font-weight:650;letter-spacing:-.015em;}
.stage172-task-map__group nav span{color:#7f8b91;font-size:12px;}
.stage172-task-map__group nav b{font-size:14px;font-weight:500;}

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
  .stage172-task-map__shell{width:min(100% - 28px,860px);}
  .stage172-task-map__head{grid-template-columns:1fr;gap:18px;}
  .stage172-task-map__grid{grid-template-columns:1fr;}
}
@media(max-width:600px){
  body[data-ux-family="hub"] main.p130-hub .x146-depth__inner,
  body[data-ux-family="service"] main .x146-depth__inner,
  .secondary-demand__inner,.secondary-demand__shell{width:calc(100% - 24px)!important;}
  .stage172-task-map__shell{width:calc(100% - 24px);}
  .stage172-task-map__group{padding:22px 18px;}
  .stage172-task-map__group nav a{grid-template-columns:minmax(0,1fr) 18px;}
  .stage172-task-map__group nav a span{display:none;}
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
