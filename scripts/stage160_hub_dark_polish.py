#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage160-hub-dark-polish"

STYLE = r'''<style id="stage160-hub-dark-polish">
/* Final polish for Services / Guides hubs: no legacy paper surfaces. */
main.p130-hub[data-stage130-hub="services"],
main.p130-hub[data-stage130-hub="guides"]{
  background:
    radial-gradient(70rem 34rem at 82% 4%,rgba(112,134,255,.085),transparent 70%),
    radial-gradient(48rem 32rem at 8% 34%,rgba(177,232,164,.035),transparent 72%),
    #070a0c!important;
  color:#f5f7f4!important;
}
main.p130-hub[data-stage130-hub="services"] .p130-hero,
main.p130-hub[data-stage130-hub="guides"] .p130-hero{
  background:transparent!important;color:#f5f7f4!important;padding-bottom:clamp(64px,6vw,96px)!important;
}
main.p130-hub[data-stage130-hub="services"] .p130-hero h1,
main.p130-hub[data-stage130-hub="guides"] .p130-hero h1{color:#f5f7f4!important;max-width:14ch!important;}
main.p130-hub[data-stage130-hub="services"] .p130-lead,
main.p130-hub[data-stage130-hub="guides"] .p130-lead{color:rgba(230,236,234,.72)!important;max-width:64ch!important;}
main.p130-hub[data-stage130-hub="services"] .p130-kicker,
main.p130-hub[data-stage130-hub="guides"] .p130-kicker{color:rgba(211,222,218,.5)!important;}

main.p130-hub[data-stage130-hub="services"] :is(.p130-list-section,.p130-featured,.p130-editorial,.p130-footer-cta,.x146-depth,.secondary-demand,.p131-bridge),
main.p130-hub[data-stage130-hub="guides"] :is(.p130-list-section,.p130-featured,.p130-editorial,.p130-footer-cta,.x146-depth,.secondary-demand,.p131-bridge){background:transparent!important;color:#f5f7f4!important;border:0!important;}
main.p130-hub[data-stage130-hub="services"] :is(.p130-list-section,.p130-featured,.x146-depth,.secondary-demand),
main.p130-hub[data-stage130-hub="guides"] :is(.p130-list-section,.p130-featured,.x146-depth,.secondary-demand){padding:clamp(54px,6vw,88px) 0!important;}
main.p130-hub[data-stage130-hub="services"] :is(.p130-list-section,.p130-featured,.p130-editorial,.p130-footer-cta)>.p130-shell,
main.p130-hub[data-stage130-hub="guides"] :is(.p130-list-section,.p130-featured,.p130-editorial,.p130-footer-cta)>.p130-shell,
main.p130-hub[data-stage130-hub="services"] .x146-depth__inner,
main.p130-hub[data-stage130-hub="guides"] .x146-depth__inner,
main.p130-hub[data-stage130-hub="services"] .secondary-demand__shell,
main.p130-hub[data-stage130-hub="guides"] .secondary-demand__shell{
  width:min(1480px,calc(100% - 64px))!important;max-width:1480px!important;margin:0 auto!important;
}

/* Main routes: compact two-column editorial grid. */
main.p130-hub[data-stage130-hub="services"] .p130-list,
main.p130-hub[data-stage130-hub="guides"] .p130-list{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:14px!important;}
main.p130-hub[data-stage130-hub="services"] .p130-row,
main.p130-hub[data-stage130-hub="guides"] .p130-row{
  display:grid!important;grid-template-columns:auto minmax(0,1fr) auto!important;grid-template-areas:"n title arrow" ". desc arrow"!important;
  gap:8px 16px!important;align-items:start!important;min-height:146px!important;padding:24px 26px!important;
  border:1px solid rgba(255,255,255,.085)!important;border-radius:22px!important;
  background:linear-gradient(145deg,rgba(255,255,255,.045),rgba(255,255,255,.014)),rgba(11,15,19,.76)!important;
  box-shadow:0 18px 52px rgba(0,0,0,.18)!important;text-decoration:none!important;
}
main.p130-hub[data-stage130-hub="services"] .p130-row>span,
main.p130-hub[data-stage130-hub="guides"] .p130-row>span{grid-area:n!important;color:#b8ff5c!important;font:700 11px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace!important;letter-spacing:.08em!important;}
main.p130-hub[data-stage130-hub="services"] .p130-row>strong,
main.p130-hub[data-stage130-hub="guides"] .p130-row>strong{grid-area:title!important;color:#f5f7f4!important;font-size:clamp(19px,1.55vw,24px)!important;line-height:1.1!important;letter-spacing:-.025em!important;}
main.p130-hub[data-stage130-hub="services"] .p130-row>em,
main.p130-hub[data-stage130-hub="guides"] .p130-row>em{grid-area:desc!important;color:rgba(221,229,232,.64)!important;font-style:normal!important;font-size:14px!important;line-height:1.58!important;}
main.p130-hub[data-stage130-hub="services"] .p130-row>b,
main.p130-hub[data-stage130-hub="guides"] .p130-row>b{grid-area:arrow!important;color:rgba(255,255,255,.5)!important;font-size:20px!important;}

/* Remove the giant light SEO block visible in the screenshots. */
main.p130-hub[data-stage130-hub="services"] .x146-depth,
main.p130-hub[data-stage130-hub="guides"] .x146-depth{background:transparent!important;color:#f5f7f4!important;}
main.p130-hub[data-stage130-hub="services"] .x146-depth__head,
main.p130-hub[data-stage130-hub="guides"] .x146-depth__head{
  display:grid!important;grid-template-columns:minmax(140px,.32fr) minmax(0,1fr)!important;gap:clamp(28px,4vw,64px)!important;align-items:start!important;margin-bottom:34px!important;
}
main.p130-hub[data-stage130-hub="services"] .x146-depth__eyebrow,
main.p130-hub[data-stage130-hub="guides"] .x146-depth__eyebrow{color:rgba(209,220,217,.48)!important;font-size:11px!important;letter-spacing:.18em!important;}
main.p130-hub[data-stage130-hub="services"] .x146-depth__head h2,
main.p130-hub[data-stage130-hub="guides"] .x146-depth__head h2{color:#f5f7f4!important;max-width:18ch!important;font-size:clamp(42px,4.5vw,72px)!important;line-height:.94!important;letter-spacing:-.055em!important;margin:0 0 20px!important;}
main.p130-hub[data-stage130-hub="services"] .x146-depth__intro,
main.p130-hub[data-stage130-hub="guides"] .x146-depth__intro{color:rgba(224,232,233,.66)!important;max-width:72ch!important;font-size:16px!important;line-height:1.72!important;}
main.p130-hub[data-stage130-hub="services"] .x146-depth__grid,
main.p130-hub[data-stage130-hub="guides"] .x146-depth__grid{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:16px!important;}
main.p130-hub[data-stage130-hub="services"] .x146-depth__card,
main.p130-hub[data-stage130-hub="guides"] .x146-depth__card{
  min-height:0!important;padding:28px!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:22px!important;
  background:linear-gradient(145deg,rgba(255,255,255,.04),rgba(255,255,255,.012)),#0b0f13!important;box-shadow:none!important;
}
main.p130-hub[data-stage130-hub="services"] .x146-depth__card h3,
main.p130-hub[data-stage130-hub="guides"] .x146-depth__card h3{color:#f5f7f4!important;font-size:22px!important;line-height:1.15!important;margin:0 0 12px!important;}
main.p130-hub[data-stage130-hub="services"] .x146-depth__card p,
main.p130-hub[data-stage130-hub="guides"] .x146-depth__card p{color:rgba(220,228,231,.64)!important;font-size:14px!important;line-height:1.65!important;}
main.p130-hub[data-stage130-hub="services"] .x146-depth__links,
main.p130-hub[data-stage130-hub="guides"] .x146-depth__links{display:flex!important;flex-wrap:wrap!important;gap:10px!important;margin-top:20px!important;}
main.p130-hub[data-stage130-hub="services"] .x146-depth__links a,
main.p130-hub[data-stage130-hub="guides"] .x146-depth__links a{padding:10px 14px!important;border:1px solid rgba(255,255,255,.09)!important;border-radius:999px!important;background:rgba(255,255,255,.025)!important;color:rgba(235,240,238,.78)!important;text-decoration:none!important;}

/* Featured work + task routes. */
main.p130-hub[data-stage130-hub="services"] .p130-featured-card,
main.p130-hub[data-stage130-hub="guides"] .p130-featured-card{
  display:grid!important;grid-template-columns:minmax(0,1.15fr) minmax(320px,.85fr)!important;gap:0!important;overflow:hidden!important;
  border:1px solid rgba(255,255,255,.08)!important;border-radius:28px!important;background:#0b0f13!important;box-shadow:0 24px 70px rgba(0,0,0,.22)!important;text-decoration:none!important;
}
main.p130-hub[data-stage130-hub="services"] .p130-featured-copy,
main.p130-hub[data-stage130-hub="guides"] .p130-featured-copy{padding:clamp(28px,4vw,54px)!important;align-self:center!important;}
main.p130-hub[data-stage130-hub="services"] .p130-featured-copy h2,
main.p130-hub[data-stage130-hub="guides"] .p130-featured-copy h2{color:#f5f7f4!important;font-size:clamp(34px,4vw,60px)!important;}
main.p130-hub[data-stage130-hub="services"] .p130-featured-copy p,
main.p130-hub[data-stage130-hub="guides"] .p130-featured-copy p{color:rgba(222,230,232,.65)!important;}
main.p130-hub[data-stage130-hub="services"] .secondary-demand__head h2,
main.p130-hub[data-stage130-hub="guides"] .secondary-demand__head h2{color:#f5f7f4!important;max-width:18ch!important;}
main.p130-hub[data-stage130-hub="services"] .secondary-demand__intro,
main.p130-hub[data-stage130-hub="guides"] .secondary-demand__intro{color:rgba(221,229,232,.64)!important;}
main.p130-hub[data-stage130-hub="services"] .secondary-demand__grid,
main.p130-hub[data-stage130-hub="guides"] .secondary-demand__grid{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:14px!important;}
main.p130-hub[data-stage130-hub="services"] .secondary-demand__card,
main.p130-hub[data-stage130-hub="guides"] .secondary-demand__card{padding:24px!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:20px!important;background:rgba(255,255,255,.025)!important;color:#f5f7f4!important;text-decoration:none!important;}
main.p130-hub[data-stage130-hub="services"] .secondary-demand__card h3,
main.p130-hub[data-stage130-hub="guides"] .secondary-demand__card h3{color:#f5f7f4!important;}
main.p130-hub[data-stage130-hub="services"] .secondary-demand__card p,
main.p130-hub[data-stage130-hub="guides"] .secondary-demand__card p{color:rgba(220,228,231,.62)!important;}
main.p130-hub[data-stage130-hub="services"] .secondary-demand__card span,
main.p130-hub[data-stage130-hub="guides"] .secondary-demand__card span{color:#b8ff5c!important;}

main.p130-hub[data-stage130-hub="services"] .p131-bridge__inner,
main.p130-hub[data-stage130-hub="guides"] .p131-bridge__inner{width:min(1480px,calc(100% - 64px))!important;max-width:1480px!important;margin:0 auto!important;border-top:1px solid rgba(255,255,255,.075)!important;border-bottom:1px solid rgba(255,255,255,.075)!important;padding:18px 0!important;display:flex!important;flex-wrap:wrap!important;gap:10px 18px!important;}
main.p130-hub[data-stage130-hub="services"] .p131-bridge a,
main.p130-hub[data-stage130-hub="guides"] .p131-bridge a{color:rgba(230,236,238,.68)!important;}
main.p130-hub[data-stage130-hub="services"] .s101-more,
main.p130-hub[data-stage130-hub="guides"] .s101-more{background:#070a0c!important;border:0!important;padding:0 max(32px,calc((100% - 1480px)/2)) 20px!important;}
main.p130-hub[data-stage130-hub="services"] .s101-more a,
main.p130-hub[data-stage130-hub="guides"] .s101-more a{color:rgba(230,236,238,.68)!important;}

@media(max-width:980px){
  main.p130-hub[data-stage130-hub="services"] :is(.p130-list-section,.p130-featured,.p130-editorial,.p130-footer-cta)>.p130-shell,
  main.p130-hub[data-stage130-hub="guides"] :is(.p130-list-section,.p130-featured,.p130-editorial,.p130-footer-cta)>.p130-shell,
  main.p130-hub[data-stage130-hub="services"] .x146-depth__inner,
  main.p130-hub[data-stage130-hub="guides"] .x146-depth__inner,
  main.p130-hub[data-stage130-hub="services"] .secondary-demand__shell,
  main.p130-hub[data-stage130-hub="guides"] .secondary-demand__shell,
  main.p130-hub[data-stage130-hub="services"] .p131-bridge__inner,
  main.p130-hub[data-stage130-hub="guides"] .p131-bridge__inner{width:min(100% - 28px,860px)!important;}
  main.p130-hub[data-stage130-hub="services"] .p130-list,
  main.p130-hub[data-stage130-hub="guides"] .p130-list,
  main.p130-hub[data-stage130-hub="services"] .x146-depth__grid,
  main.p130-hub[data-stage130-hub="guides"] .x146-depth__grid,
  main.p130-hub[data-stage130-hub="services"] .secondary-demand__grid,
  main.p130-hub[data-stage130-hub="guides"] .secondary-demand__grid,
  main.p130-hub[data-stage130-hub="services"] .p130-featured-card,
  main.p130-hub[data-stage130-hub="guides"] .p130-featured-card{grid-template-columns:1fr!important;}
  main.p130-hub[data-stage130-hub="services"] .x146-depth__head,
  main.p130-hub[data-stage130-hub="guides"] .x146-depth__head{grid-template-columns:1fr!important;gap:16px!important;}
}
@media(max-width:600px){
  main.p130-hub[data-stage130-hub="services"] :is(.p130-list-section,.p130-featured,.x146-depth,.secondary-demand),
  main.p130-hub[data-stage130-hub="guides"] :is(.p130-list-section,.p130-featured,.x146-depth,.secondary-demand){padding:42px 0!important;}
  main.p130-hub[data-stage130-hub="services"] .p130-row,
  main.p130-hub[data-stage130-hub="guides"] .p130-row{min-height:0!important;padding:20px!important;grid-template-columns:auto minmax(0,1fr)!important;grid-template-areas:"n title" ". desc"!important;}
  main.p130-hub[data-stage130-hub="services"] .p130-row>b,
  main.p130-hub[data-stage130-hub="guides"] .p130-row>b{display:none!important;}
}
</style>'''

for rel in ("services/index.html", "guides/index.html"):
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"stage160: missing {path}")
    html = path.read_text(encoding="utf-8")
    if MARKER in html:
        continue
    if "</head>" not in html:
        raise SystemExit(f"stage160: head missing {path}")
    html = html.replace("</head>", STYLE + "</head>", 1)
    path.write_text(html, encoding="utf-8")

for rel, hub in (("services/index.html", "services"), ("guides/index.html", "guides")):
    text = (ROOT / rel).read_text(encoding="utf-8")
    if MARKER not in text or f'data-stage130-hub="{hub}"' not in text or "x146-depth" not in text:
        raise SystemExit(f"stage160 guard failed: {rel}")

print("stage160 hub dark polish: services + guides")
