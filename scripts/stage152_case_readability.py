#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
MARKER = "stage152-case-readability"

STYLE = r'''<style id="stage152-case-readability">
/* Final case-page readability pass. It deliberately runs after every cinematic layer. */
body[data-ux-family="case"] .p132-case .p132-cover{
  min-height:0!important;
  padding:clamp(56px,5.5vw,84px) 0 clamp(64px,6.2vw,96px)!important;
}
body[data-ux-family="case"] .p132-case .p132-shell.p132-cover-grid{
  width:min(1380px,calc(100% - 56px))!important;
  max-width:1380px!important;
  margin-inline:auto!important;
  padding:0!important;
  display:grid!important;
  grid-template-columns:minmax(0,1.52fr) minmax(320px,.68fr)!important;
  gap:clamp(34px,4.4vw,66px)!important;
  align-items:center!important;
  justify-content:normal!important;
  position:relative!important;
  inset:auto!important;
  transform:none!important;
}
body[data-ux-family="case"] .p132-case .p132-cover-copy{
  width:100%!important;
  max-width:860px!important;
  min-width:0!important;
  margin:0!important;
  padding:0!important;
  position:relative!important;
  inset:auto!important;
  transform:none!important;
  justify-self:start!important;
  order:1!important;
}
body[data-ux-family="case"] .p132-case .p132-cover h1{
  width:100%!important;
  max-width:16ch!important;
  margin:.75rem 0 1.2rem!important;
  font-size:clamp(52px,5.15vw,86px)!important;
  line-height:.94!important;
  letter-spacing:-.052em!important;
  text-wrap:balance!important;
  overflow-wrap:normal!important;
  word-break:normal!important;
  hyphens:none!important;
}
body[data-ux-family="case"] .p132-case .p132-cover-copy>p:not(.p132-eyebrow){
  width:100%!important;
  max-width:70ch!important;
  margin:1.15rem 0 0!important;
  font-size:clamp(17px,1.18vw,20px)!important;
  line-height:1.72!important;
  color:rgba(226,233,236,.78)!important;
  text-wrap:pretty!important;
}
body[data-ux-family="case"] .p132-case .p132-cover-actions{
  margin-top:1.8rem!important;
  gap:.75rem 1rem!important;
}
body[data-ux-family="case"] .p132-case .p132-cover-visual{
  width:100%!important;
  max-width:460px!important;
  min-width:0!important;
  min-height:0!important;
  aspect-ratio:4/3!important;
  margin:0!important;
  padding:0!important;
  position:relative!important;
  inset:auto!important;
  transform:none!important;
  animation:none!important;
  justify-self:end!important;
  align-self:center!important;
  order:2!important;
  border-radius:28px!important;
  border:1px solid rgba(255,255,255,.12)!important;
  background:linear-gradient(145deg,rgba(255,255,255,.07),rgba(255,255,255,.02)),rgba(10,14,18,.72)!important;
  -webkit-backdrop-filter:blur(22px) saturate(132%)!important;
  backdrop-filter:blur(22px) saturate(132%)!important;
  box-shadow:0 28px 82px rgba(0,0,0,.34),inset 0 1px 0 rgba(255,255,255,.06)!important;
  overflow:hidden!important;
}
body[data-ux-family="case"] .p132-case .p132-cover-visual img{
  width:100%!important;
  height:100%!important;
  object-fit:cover!important;
  object-position:center!important;
  transform:none!important;
}
body[data-ux-family="case"] .p132-case .p132-cover-graphic{
  min-height:0!important;
  height:100%!important;
  padding:clamp(22px,2.4vw,32px)!important;
}
body[data-ux-family="case"] .p132-case .p132-cover-graphic strong{
  font-size:clamp(78px,9vw,132px)!important;
}
body[data-ux-family="case"] .p132-case .p132-cover-graphic span{
  max-width:11ch!important;
  font-size:clamp(28px,3vw,46px)!important;
}

/* Story sections: compact label column, wide readable content column. */
body[data-ux-family="case"] .p132-case>.p132-panel,
body[data-ux-family="case"] .p132-case>.p132-end{
  width:min(1260px,calc(100% - 56px))!important;
  max-width:1260px!important;
  margin-inline:auto!important;
}
body[data-ux-family="case"] .p132-case>.p132-panel .section-head{
  display:grid!important;
  grid-template-columns:minmax(110px,.2fr) minmax(0,1.8fr)!important;
  gap:clamp(26px,4vw,58px)!important;
  align-items:start!important;
}
body[data-ux-family="case"] .p132-case>.p132-panel .section-head>div:last-child{
  width:100%!important;
  max-width:980px!important;
  min-width:0!important;
}
body[data-ux-family="case"] .p132-case>.p132-panel .section-head h2{
  width:100%!important;
  max-width:20ch!important;
  font-size:clamp(38px,4.1vw,66px)!important;
  line-height:.98!important;
  letter-spacing:-.045em!important;
  text-wrap:balance!important;
}
body[data-ux-family="case"] .p132-case>.p132-panel :is(.copy,.lead){
  width:100%!important;
  max-width:72ch!important;
  font-size:clamp(16px,1.05vw,18px)!important;
  line-height:1.76!important;
  text-wrap:pretty!important;
}

/* Keep internal project cards visually consistent without shrinking their copy. */
body[data-ux-family="case"] .p132-case>.p132-panel :is(.card,.feature,.note,.demo,.shot,.related a),
body[data-ux-family="case"] .p132-case>.p132-end :is(.cta-box,.contact-card){
  border-radius:clamp(18px,2vw,26px)!important;
  border-color:rgba(255,255,255,.11)!important;
  background:linear-gradient(145deg,rgba(255,255,255,.07),rgba(255,255,255,.022) 46%,rgba(7,10,13,.56)),rgba(12,16,20,.7)!important;
  -webkit-backdrop-filter:blur(20px) saturate(128%)!important;
  backdrop-filter:blur(20px) saturate(128%)!important;
  box-shadow:0 22px 66px rgba(0,0,0,.27),inset 0 1px 0 rgba(255,255,255,.05)!important;
}
body[data-ux-family="case"] .p132-case>.p132-panel :is(.card,.feature) p{
  max-width:42ch!important;
  line-height:1.65!important;
}

@media(max-width:1120px){
  body[data-ux-family="case"] .p132-case .p132-shell.p132-cover-grid{
    width:min(100% - 42px,1120px)!important;
    grid-template-columns:minmax(0,1.28fr) minmax(320px,.72fr)!important;
    gap:34px!important;
  }
  body[data-ux-family="case"] .p132-case .p132-cover h1{
    max-width:15ch!important;
    font-size:clamp(50px,6vw,76px)!important;
  }
  body[data-ux-family="case"] .p132-case .p132-cover-visual{max-width:420px!important}
}

@media(max-width:900px){
  body[data-ux-family="case"] .p132-case .p132-shell.p132-cover-grid{
    width:min(100% - 32px,780px)!important;
    grid-template-columns:1fr!important;
    gap:30px!important;
  }
  body[data-ux-family="case"] .p132-case .p132-cover-copy,
  body[data-ux-family="case"] .p132-case .p132-cover-visual{
    width:100%!important;
    max-width:none!important;
    justify-self:stretch!important;
  }
  body[data-ux-family="case"] .p132-case .p132-cover h1{
    max-width:100%!important;
    font-size:clamp(48px,9.5vw,72px)!important;
  }
  body[data-ux-family="case"] .p132-case .p132-cover-visual{
    aspect-ratio:16/10!important;
  }
  body[data-ux-family="case"] .p132-case>.p132-panel,
  body[data-ux-family="case"] .p132-case>.p132-end{
    width:min(100% - 32px,780px)!important;
  }
  body[data-ux-family="case"] .p132-case>.p132-panel .section-head{
    grid-template-columns:1fr!important;
    gap:12px!important;
  }
  body[data-ux-family="case"] .p132-case>.p132-panel .section-head h2{max-width:100%!important}
}

@media(max-width:600px){
  body[data-ux-family="case"] .p132-case .p132-cover{padding:34px 0 54px!important}
  body[data-ux-family="case"] .p132-case .p132-shell.p132-cover-grid,
  body[data-ux-family="case"] .p132-case>.p132-panel,
  body[data-ux-family="case"] .p132-case>.p132-end{width:calc(100% - 24px)!important}
  body[data-ux-family="case"] .p132-case .p132-cover h1{
    max-width:100%!important;
    font-size:clamp(42px,12.2vw,58px)!important;
    line-height:.94!important;
  }
  body[data-ux-family="case"] .p132-case .p132-cover-copy>p:not(.p132-eyebrow){
    max-width:100%!important;
    font-size:16px!important;
    line-height:1.68!important;
  }
  body[data-ux-family="case"] .p132-case .p132-cover-actions{
    display:grid!important;
    grid-template-columns:1fr!important;
  }
  body[data-ux-family="case"] .p132-case .p132-cover-actions a{
    width:100%!important;
    justify-content:center!important;
    text-align:center!important;
  }
}
</style>'''

case_dir = ROOT / "cases"
case_pages = sorted(p for p in case_dir.glob("*/index.html") if p.is_file()) if case_dir.exists() else []
if not case_pages:
    raise SystemExit("stage152: no case pages found")

changed = []
for path in case_pages:
    text = path.read_text(encoding="utf-8")
    if 'data-stage132-case="true"' not in text:
        continue
    if MARKER in text:
        continue
    if "</head>" not in text:
        raise SystemExit(f"stage152: head closing tag missing: {path}")
    text = text.replace("</head>", STYLE + "</head>", 1)
    path.write_text(text, encoding="utf-8")
    changed.append(path)

if len(changed) < 9:
    raise SystemExit(f"stage152: expected 9 case pages, updated {len(changed)}")

for path in changed:
    final = path.read_text(encoding="utf-8")
    for guard in (MARKER, 'max-width:16ch!important', 'grid-template-columns:minmax(0,1.52fr) minmax(320px,.68fr)!important'):
        if guard not in final:
            raise SystemExit(f"stage152: guard failed {guard}: {path}")

print(f"stage152 case readability: {len(changed)} case pages widened and rebalanced")
