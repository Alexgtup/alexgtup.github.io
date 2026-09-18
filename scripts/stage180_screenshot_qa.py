#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re, sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
MARKER = 'stage180-screenshot-qa'
STYLE = r'''<style id="stage180-screenshot-qa">
/* Final screenshot-driven QA. Runs after all visual systems. */

/* Search-depth links must read as separate controls, never one glued text line. */
body[data-ux-family="service"] main .x146-depth__links,
body[data-ux-family="guide"] main .x146-depth__links,
body[data-ux-family="case"] main .x146-depth__links{
  display:flex!important;flex-wrap:wrap!important;gap:9px!important;
  margin:clamp(26px,3vw,40px) 0 0!important;padding:0!important;
}
body[data-ux-family="service"] main .x146-depth__links a,
body[data-ux-family="guide"] main .x146-depth__links a,
body[data-ux-family="case"] main .x146-depth__links a{
  display:inline-flex!important;align-items:center!important;min-height:40px!important;
  padding:9px 13px!important;border:1px solid rgba(255,255,255,.095)!important;
  border-radius:999px!important;background:rgba(255,255,255,.025)!important;
  color:rgba(238,243,240,.84)!important;text-decoration:none!important;font-size:13px!important;
}

/* Legacy search-entry navs should sit inside the content width instead of becoming detached black strips. */
body[data-page="services"] main.p130-hub > .s101-more,
body[data-ux-family="service"] main > .s101-more.s107-related{
  width:min(1320px,calc(100% - 64px))!important;max-width:1320px!important;
  margin:22px auto!important;padding:0!important;min-height:0!important;
  display:flex!important;flex-wrap:wrap!important;gap:9px!important;
  background:transparent!important;border:0!important;color:inherit!important;
}
body[data-page="services"] main.p130-hub > .s101-more a,
body[data-ux-family="service"] main > .s101-more.s107-related a{
  display:inline-flex!important;align-items:center!important;min-height:38px!important;
  padding:8px 13px!important;border:1px solid rgba(255,255,255,.10)!important;
  border-radius:999px!important;background:rgba(255,255,255,.025)!important;
  color:rgba(238,243,240,.82)!important;text-decoration:none!important;font-size:13px!important;
}
body[data-page="services"] main.p130-hub > .s101-more a{
  border-color:rgba(20,23,18,.14)!important;background:rgba(255,255,255,.62)!important;color:#252922!important;
}

/* Primary actions on dark guide cards need dark text on the lime surface. */
body[data-ux-family="guide"] .ux-guide-main .button.primary,
body[data-ux-family="guide"] .ux-guide-main a.button.primary{
  color:#071008!important;background:#c9ff4a!important;border-color:#c9ff4a!important;font-weight:800!important;
}

/* Warm About world: old dark-theme muted colors were unreadable on the yellow background. */
main.p130-hub[data-stage130-hub="about"] .p130-editorial-statement p{color:rgba(20,19,15,.72)!important}
main.p130-hub[data-stage130-hub="about"] .p130-editorial-statement .p129-textlink{
  color:#17140f!important;border-bottom-color:rgba(23,20,15,.38)!important;
}
main.p130-hub[data-stage130-hub="about"] .p130-proof-stack span{color:rgba(20,19,15,.62)!important}
main.p130-hub[data-stage130-hub="about"] .p131-bridge{border-color:rgba(20,19,15,.14)!important}
main.p130-hub[data-stage130-hub="about"] .p131-bridge :is(span,a){color:rgba(20,19,15,.70)!important}
main.p130-hub[data-stage130-hub="about"] .p131-bridge a{
  background:rgba(255,255,255,.18)!important;border-color:rgba(20,19,15,.12)!important;
}

/* Real project previews: never collapse or hide the screenshot area. */
main.p129-service .p129-case-media>img{
  display:block!important;width:100%!important;height:100%!important;min-height:100%!important;
  object-fit:cover!important;object-position:center!important;opacity:1!important;
}

@media(max-width:980px){
  body[data-page="services"] main.p130-hub > .s101-more,
  body[data-ux-family="service"] main > .s101-more.s107-related{width:min(100% - 28px,860px)!important}
}
@media(max-width:600px){
  body[data-page="services"] main.p130-hub > .s101-more,
  body[data-ux-family="service"] main > .s101-more.s107-related{width:calc(100% - 24px)!important;margin:16px auto!important}
  body[data-page="project-repair"] main.p129-service h1{font-size:clamp(38px,10.5vw,44px)!important;line-height:.94!important}
}
</style>'''

changed=0
for path in sorted(ROOT.rglob('index.html')):
    text=path.read_text(encoding='utf-8',errors='ignore')
    if '</head>' not in text:
        continue
    # Defensive replacement: these four raster placeholders decode to pure black.
    for n in range(1,5):
        text=text.replace(f'/assets/cases/sheetpilot-ai/sheetpilot-0{n}-720w.webp','/assets/cases/sheetpilot-ai/sheetpilot-live-01.webp')
    text=re.sub(r'<style\s+id=["\']stage180-screenshot-qa["\']>.*?</style>','',text,flags=re.I|re.S)
    text=text.replace('</head>',STYLE+'</head>',1)
    path.write_text(text,encoding='utf-8')
    changed+=1

for rel in ['services/index.html','api-integrations/index.html','web-development/index.html','guides/api-integration-checklist/index.html','about/index.html']:
    p=ROOT/rel
    if not p.is_file(): raise SystemExit(f'stage180: missing {rel}')
    s=p.read_text(encoding='utf-8')
    if MARKER not in s: raise SystemExit(f'stage180: marker missing {rel}')
if 'sheetpilot-01-720w.webp' in (ROOT/'web-development/index.html').read_text(encoding='utf-8'):
    raise SystemExit('stage180: black SheetPilot asset still referenced on web-development')
print(f'stage180 screenshot QA: {changed} pages')
