#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage170-case-contrast"

STYLE = r'''<style id="stage170-case-contrast">
/* Final component-level contrast fixes. Never recolor page/body globally. */
body[data-ux-family="case"] main .p132-cover-graphic strong{
  color:rgba(243,246,244,.18)!important;
  -webkit-text-stroke:1px rgba(243,246,244,.10)!important;
}
body[data-ux-family="case"] main .p132-cover-graphic span{
  color:rgba(243,246,244,.70)!important;
}

/* Hub footer CTA: the surface is dark, so every readable descendant must be light. */
main.p130-hub .p130-footer-cta{
  color:#f3f6f4!important;
}
main.p130-hub .p130-footer-cta>div{
  color:#f3f6f4!important;
}
main.p130-hub .p130-footer-cta :is(h2,h3,strong){
  color:#f3f6f4!important;
}
main.p130-hub .p130-footer-cta :is(p,li){
  color:rgba(226,233,230,.74)!important;
}
main.p130-hub .p130-footer-cta :is(.p130-kicker,.eyebrow,small){
  color:rgba(226,233,230,.56)!important;
}
main.p130-hub .p130-footer-cta a:not(.p130-btn):not(.btn){
  color:#f3f6f4!important;
}
main.p130-hub .p130-footer-cta :is(.p130-btn,.btn){
  color:#071008!important;
}

body[data-ux-family="case"] main section.p132-end :is(.s51-contact-card,.cta-box),
body[data-ux-family="case"] main section.stage108-endcap :is(.s51-contact-card,.cta-box){
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
  background:linear-gradient(145deg,rgba(255,255,255,.035),rgba(255,255,255,.01)),#0b1015!important;
  color:#f3f6f4!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.035)!important;
}
body[data-ux-family="case"] main section.p132-end :is(.s51-contact-card,.cta-box) :is(h2,h3,strong),
body[data-ux-family="case"] main section.stage108-endcap :is(.s51-contact-card,.cta-box) :is(h2,h3,strong){
  color:#f3f6f4!important;
}
body[data-ux-family="case"] main section.p132-end :is(.s51-contact-card,.cta-box) h2,
body[data-ux-family="case"] main section.stage108-endcap :is(.s51-contact-card,.cta-box) h2{
  max-width:18ch!important;
  margin:0!important;
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
  color:rgba(226,233,230,.72)!important;
  font-size:clamp(15px,1.08vw,18px)!important;
  line-height:1.68!important;
}
body[data-ux-family="case"] main section.p132-end :is(.s51-kicker,.eyebrow),
body[data-ux-family="case"] main section.stage108-endcap :is(.s51-kicker,.eyebrow){
  display:block!important;
  margin:0 0 12px!important;
  color:rgba(201,255,74,.72)!important;
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
    if rel.startswith("en/"):
        continue
    text = path.read_text(encoding="utf-8")
    if "</head>" not in text:
        continue
    text = re.sub(r'<style\s+id=["\']stage170-(?:case-about-contrast|case-contrast)["\']>.*?</style>', '', text, flags=re.I | re.S)
    text = text.replace("</head>", STYLE + "</head>", 1)
    path.write_text(text, encoding="utf-8")
    changed.append(rel)

for rel in [
    "cases/index.html",
    "services/index.html",
    "guides/index.html",
    "about/index.html",
    "freelance-developer/index.html",
    "cases/auto-crm/index.html",
    "cases/taxi-app/index.html",
    "cases/factory-catalog/index.html",
    "cases/seo-control-center/index.html",
    "cases/siteaudit-studio/index.html",
    "cases/freelance-os/index.html",
]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    if text.count(MARKER) != 1:
        raise SystemExit(f"stage170: marker guard failed {rel}")

print(f"stage170 component contrast: {len(changed)} pages")
