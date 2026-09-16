#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage170-case-about-contrast"

STYLE = r'''<style id="stage170-case-about-contrast">
/* Remaining legacy case CTAs and About typography. */
body[data-ux-family="case"] main .p132-cover-graphic strong{
  color:rgba(243,246,244,.16)!important;
  -webkit-text-stroke:1px rgba(243,246,244,.08)!important;
}
body[data-ux-family="case"] main .p132-cover-graphic span{
  color:rgba(243,246,244,.68)!important;
}

body[data-ux-family="case"] main section.p132-end .s51-contact-card,
body[data-ux-family="case"] main section.stage108-endcap .s51-contact-card,
body[data-ux-family="case"] main section.p132-end .cta-box,
body[data-ux-family="case"] main section.stage108-endcap .cta-box{
  display:grid!important;
  grid-template-columns:minmax(0,1fr) auto!important;
  gap:clamp(28px,4vw,58px)!important;
  align-items:end!important;
  width:100%!important;
  max-width:none!important;
  margin:0!important;
  padding:clamp(30px,3.5vw,48px)!important;
  border:1px solid rgba(255,255,255,.10)!important;
  border-radius:24px!important;
  background:linear-gradient(145deg,rgba(255,255,255,.035),rgba(255,255,255,.01)),rgba(5,9,12,.84)!important;
  color:#f3f6f4!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.035)!important;
}
body[data-ux-family="case"] main section.p132-end :is(.s51-contact-card,.cta-box) h2,
body[data-ux-family="case"] main section.stage108-endcap :is(.s51-contact-card,.cta-box) h2{
  max-width:18ch!important;
  margin:0!important;
  color:#f3f6f4!important;
  font-size:clamp(34px,3.7vw,58px)!important;
  line-height:.99!important;
  letter-spacing:-.048em!important;
  text-wrap:balance!important;
}
body[data-ux-family="case"] main section.p132-end :is(.s51-contact-card,.cta-box) h2 em,
body[data-ux-family="case"] main section.stage108-endcap :is(.s51-contact-card,.cta-box) h2 em{
  color:#c9ff4a!important;
  font-style:normal!important;
}
body[data-ux-family="case"] main section.p132-end :is(.s51-contact-card,.cta-box) p,
body[data-ux-family="case"] main section.stage108-endcap :is(.s51-contact-card,.cta-box) p{
  max-width:68ch!important;
  margin:16px 0 0!important;
  color:rgba(226,233,230,.70)!important;
  font-size:clamp(15px,1.08vw,18px)!important;
  line-height:1.68!important;
}
body[data-ux-family="case"] main section.p132-end :is(.s51-kicker,.eyebrow),
body[data-ux-family="case"] main section.stage108-endcap :is(.s51-kicker,.eyebrow){
  display:block!important;
  margin:0 0 12px!important;
  color:rgba(201,255,74,.68)!important;
  font:700 11px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace!important;
  letter-spacing:.16em!important;
  text-transform:uppercase!important;
}
body[data-ux-family="case"] main section.p132-end :is(.s51-contact-card,.cta-box) :is(.actions,.cta-actions),
body[data-ux-family="case"] main section.stage108-endcap :is(.s51-contact-card,.cta-box) :is(.actions,.cta-actions){
  display:flex!important;
  flex-wrap:wrap!important;
  gap:10px!important;
  justify-content:flex-end!important;
}
body[data-ux-family="case"] main section.p132-end :is(.s51-contact-card,.cta-box) a,
body[data-ux-family="case"] main section.stage108-endcap :is(.s51-contact-card,.cta-box) a{
  color:inherit;
}

/* About used to be a light-paper route. It now belongs to the same dark system. */
body[data-ux-family="hub"] main.p130-hub[data-stage130-hub="about"]{
  background:#07090b!important;
  color:#f3f6f4!important;
}
body[data-ux-family="hub"] main.p130-hub[data-stage130-hub="about"] .p130-hero{
  background:transparent!important;
  color:#f3f6f4!important;
}
body[data-ux-family="hub"] main.p130-hub[data-stage130-hub="about"] .p130-hero h1{
  color:#f3f6f4!important;
}
body[data-ux-family="hub"] main.p130-hub[data-stage130-hub="about"] .p130-hero h1 span{
  color:#ff765e!important;
}
body[data-ux-family="hub"] main.p130-hub[data-stage130-hub="about"] .p130-lead{
  color:rgba(226,233,230,.72)!important;
}
body[data-ux-family="hub"] main.p130-hub[data-stage130-hub="about"] .p130-kicker{
  color:rgba(226,233,230,.50)!important;
}
body[data-ux-family="hub"] main.p130-hub[data-stage130-hub="about"] .p130-editorial,
body[data-ux-family="hub"] main.p130-hub[data-stage130-hub="about"] .p130-footer-cta{
  background:#07090b!important;
  color:#f3f6f4!important;
}
body[data-ux-family="hub"] main.p130-hub[data-stage130-hub="about"] :is(.p130-editorial,.p130-footer-cta) :is(h2,h3,strong){
  color:#f3f6f4!important;
}
body[data-ux-family="hub"] main.p130-hub[data-stage130-hub="about"] :is(.p130-editorial,.p130-footer-cta) p{
  color:rgba(226,233,230,.70)!important;
}

@media(max-width:900px){
  body[data-ux-family="case"] main section.p132-end :is(.s51-contact-card,.cta-box),
  body[data-ux-family="case"] main section.stage108-endcap :is(.s51-contact-card,.cta-box){
    grid-template-columns:1fr!important;
    align-items:start!important;
  }
  body[data-ux-family="case"] main section.p132-end :is(.s51-contact-card,.cta-box) :is(.actions,.cta-actions),
  body[data-ux-family="case"] main section.stage108-endcap :is(.s51-contact-card,.cta-box) :is(.actions,.cta-actions){
    justify-content:flex-start!important;
  }
}
@media(max-width:600px){
  body[data-ux-family="case"] main section.p132-end :is(.s51-contact-card,.cta-box),
  body[data-ux-family="case"] main section.stage108-endcap :is(.s51-contact-card,.cta-box){
    padding:24px!important;
    border-radius:20px!important;
  }
}
</style>'''

changed = []
for path in sorted(ROOT.rglob("index.html")):
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("en/") or "</head>" not in path.read_text(encoding="utf-8"):
        continue
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'<style\s+id=["\']stage170-case-about-contrast["\']>.*?</style>', '', text, flags=re.I | re.S)
    text = text.replace("</head>", STYLE + "</head>", 1)
    path.write_text(text, encoding="utf-8")
    changed.append(rel)

for rel in ["about/index.html","cases/auto-crm/index.html","cases/taxi-app/index.html","cases/factory-catalog/index.html","cases/seo-control-center/index.html","cases/siteaudit-studio/index.html","cases/freelance-os/index.html"]:
    text=(ROOT/rel).read_text(encoding="utf-8")
    if text.count(MARKER)!=1:
        raise SystemExit(f"stage170: marker guard failed {rel}")

print(f"stage170 case/about contrast: {len(changed)} pages")
