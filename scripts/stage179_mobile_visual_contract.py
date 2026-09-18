#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
MARKER = 'stage179-mobile-visual-contract'
STYLE = r'''<style id="stage179-mobile-visual-contract">
/* Final mobile visual contract. Must run after all cinematic/editorial stages. */
html,body{max-width:100%;overflow-x:clip!important}

/* Decorative home layers must never visibly spill out of the hero. */
body[data-page="home"] .p128-hero{overflow:clip!important}
body[data-page="home"] .p128-hero__visual{overflow:clip!important}
body[data-page="home"] .x138-ghostword{right:0!important;max-width:100%!important;overflow:hidden!important}
body[data-page="home"] .p128-orbit{right:0!important}

@media(max-width:600px){
  /* Typography: preserve the editorial character without turning headings into walls of text. */
  body[data-wow="true"] .p129-service h1,
  main.p129-service h1,
  main.p130-hub h1{
    width:100%!important;max-width:none!important;
    font-size:clamp(40px,11vw,50px)!important;
    line-height:.92!important;letter-spacing:-.055em!important;
    text-wrap:balance!important;overflow-wrap:normal!important;word-break:normal!important;
  }
  main.p129-service h2,
  main.p130-hub h2{
    overflow-wrap:normal!important;word-break:normal!important;text-wrap:pretty!important;
  }

  /* Late cinematic rules used absolute overlays here and squeezed copy to 13–39px columns. */
  main.p129-service .p129-no-case{
    display:grid!important;grid-template-columns:minmax(0,1fr)!important;
    gap:24px!important;min-height:0!important;padding:24px!important;
  }
  main.p129-service .p129-no-case>div{width:100%!important;min-width:0!important;max-width:none!important}
  main.p129-service .p129-no-case h2{
    width:100%!important;max-width:18ch!important;
    font-size:clamp(32px,9vw,40px)!important;line-height:1!important;margin:.6rem 0 0!important;
  }
  main.p129-service .p129-no-case .p129-btn{justify-self:start!important}

  main.p129-service .p129-case-card{
    display:grid!important;grid-template-columns:minmax(0,1fr)!important;
    min-height:0!important;height:auto!important;border-radius:20px!important;
  }
  main.p129-service .p129-case-media{
    position:relative!important;inset:auto!important;width:100%!important;
    min-height:0!important;aspect-ratio:16/11!important;
  }
  main.p129-service .p129-case-media:after{background:linear-gradient(180deg,rgba(5,7,8,.03),rgba(5,7,8,.18))!important}
  main.p129-service .p129-case-copy{
    position:relative!important;inset:auto!important;width:100%!important;max-width:none!important;
    padding:24px!important;display:block!important;
  }
  main.p129-service .p129-case-copy h2{
    width:100%!important;max-width:none!important;
    font-size:clamp(34px,10vw,44px)!important;line-height:.98!important;margin:.7rem 0 1rem!important;
  }
  main.p129-service .p129-case-copy p{font-size:16px!important;line-height:1.55!important;max-width:38rem!important}

  /* Related cards were 220px high on phones despite containing only 2–3 short lines. */
  main.p129-service .p129-related-grid{gap:10px!important}
  main.p129-service .p129-related-grid a{
    min-height:138px!important;padding:18px!important;border-radius:18px!important;
  }
  main.p129-service .p129-related-grid strong{font-size:clamp(21px,6.5vw,27px)!important;line-height:1.03!important}

  /* Contact block: remove the billboard effect on narrow screens. */
  main.p129-service .p129-contact{padding:64px 0 34px!important}
  main.p129-service .p129-contact-card{padding:24px!important;gap:24px!important}
  main.p129-service .p129-contact-card h2{font-size:clamp(38px,11vw,48px)!important;line-height:.94!important;max-width:11ch!important}

  /* Proof/trust cards need content-driven height, not equal desktop slabs. */
  body[data-ux-family="service"] :is(.x177-trust-card,.x178-path-card){min-height:0!important;height:auto!important}

  /* Home decorations: keep them inside the composition at 320–430px. */
  body[data-page="home"] .x138-ghostword{font-size:min(34vw,138px)!important;right:0!important;bottom:-.08em!important}
  body[data-page="home"] .p128-orbit{width:260px!important;height:260px!important;right:-12px!important}
}

@media(max-width:380px){
  body[data-wow="true"] .p129-service h1,
  main.p129-service h1,
  main.p130-hub h1{font-size:40px!important}
  main.p129-service .p129-section-head h2{font-size:clamp(30px,9vw,36px)!important;line-height:1.02!important}
  main.p129-service .p129-case-copy h2{font-size:36px!important}
  main.p129-service .p129-related-grid a{min-height:126px!important}
}
</style>'''

changed = 0
for path in sorted(ROOT.rglob('index.html')):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '</head>' not in text:
        continue
    text = re.sub(r'<style\s+id=["\']stage179-mobile-visual-contract["\']>.*?</style>', '', text, flags=re.I | re.S)
    text = text.replace('</head>', STYLE + '</head>', 1)
    path.write_text(text, encoding='utf-8')
    changed += 1

# Guards for the pages where the regression was measurable.
for rel in ['n8n-automation/index.html','project-repair/index.html','api-integrations/index.html','index.html']:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f'stage179: missing required page {rel}')
    text = path.read_text(encoding='utf-8', errors='ignore')
    if MARKER not in text:
        raise SystemExit(f'stage179: marker missing in {rel}')
print(f'stage179 mobile visual contract: {changed} pages')
