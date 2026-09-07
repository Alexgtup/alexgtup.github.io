#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
page = root / 'index.html'
if not page.is_file():
    raise SystemExit(f'stage60: home page missing: {page}')

text = page.read_text(encoding='utf-8')

# Keep the original project grid. Only SheetPilot's visual area becomes a smooth image slider.
STYLE = r'''
<style id="stage60-sheetpilot-slider-style">
.s44-case--sheetpilot .s44-case__image{
  position:relative;
  overflow:hidden;
  isolation:isolate;
  background:#07100b;
}
.s44-case--sheetpilot .sp-image-track{
  display:flex;
  width:500%;
  height:100%;
  will-change:transform;
  animation:sp-image-scroll 22s cubic-bezier(.72,0,.28,1) infinite;
}
.s44-case--sheetpilot .sp-image-track img{
  width:20%!important;
  height:100%!important;
  flex:0 0 20%;
  object-fit:cover!important;
  object-position:center;
  display:block;
}
.s44-case--sheetpilot:hover .sp-image-track,
.s44-case--sheetpilot:focus-visible .sp-image-track{
  animation-play-state:paused;
}
.s44-case--sheetpilot .sp-slider-shade{
  position:absolute;
  inset:0;
  z-index:2;
  pointer-events:none;
  background:linear-gradient(90deg,rgba(5,10,7,.06),transparent 22%,transparent 78%,rgba(5,10,7,.12));
}
.s44-case--sheetpilot .sp-slider-progress{
  position:absolute;
  left:1rem;
  right:1rem;
  bottom:.8rem;
  z-index:3;
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:.35rem;
  pointer-events:none;
}
.s44-case--sheetpilot .sp-slider-progress i{
  height:3px;
  border-radius:999px;
  background:rgba(255,255,255,.22);
  overflow:hidden;
}
.s44-case--sheetpilot .sp-slider-progress i::after{
  content:"";
  display:block;
  width:100%;
  height:100%;
  background:#d4fe6a;
  transform:scaleX(0);
  transform-origin:left;
  animation:sp-dot-1 22s linear infinite;
}
.s44-case--sheetpilot .sp-slider-progress i:nth-child(2)::after{animation-name:sp-dot-2}
.s44-case--sheetpilot .sp-slider-progress i:nth-child(3)::after{animation-name:sp-dot-3}
.s44-case--sheetpilot .sp-slider-progress i:nth-child(4)::after{animation-name:sp-dot-4}
.s44-case--sheetpilot:hover .sp-slider-progress i::after,
.s44-case--sheetpilot:focus-visible .sp-slider-progress i::after{animation-play-state:paused}

@keyframes sp-image-scroll{
  0%,18%{transform:translate3d(0,0,0)}
  23%,41%{transform:translate3d(-20%,0,0)}
  46%,64%{transform:translate3d(-40%,0,0)}
  69%,87%{transform:translate3d(-60%,0,0)}
  92%,100%{transform:translate3d(-80%,0,0)}
}
@keyframes sp-dot-1{
  0%{transform:scaleX(0)} 17%{transform:scaleX(1)} 18%,91%{transform:scaleX(0)} 92%{transform:scaleX(0)} 100%{transform:scaleX(1)}
}
@keyframes sp-dot-2{
  0%,22%{transform:scaleX(0)} 40%{transform:scaleX(1)} 41%,100%{transform:scaleX(0)}
}
@keyframes sp-dot-3{
  0%,45%{transform:scaleX(0)} 63%{transform:scaleX(1)} 64%,100%{transform:scaleX(0)}
}
@keyframes sp-dot-4{
  0%,68%{transform:scaleX(0)} 86%{transform:scaleX(1)} 87%,100%{transform:scaleX(0)}
}
@media(prefers-reduced-motion:reduce){
  .s44-case--sheetpilot .sp-image-track{animation:none;transform:none}
  .s44-case--sheetpilot .sp-slider-progress i::after{animation:none}
  .s44-case--sheetpilot .sp-image-track img:not(:first-child){display:none}
  .s44-case--sheetpilot .sp-image-track{width:100%}
  .s44-case--sheetpilot .sp-image-track img:first-child{width:100%!important;flex-basis:100%}
}
</style>
'''

SLIDER = r'''<div class="s44-case__image sp-image-slider" aria-label="Четыре экрана SheetPilot AI">
  <div class="sp-image-track">
    <img src="/assets/cases/sheetpilot-ai/sheetpilot-01.svg" width="1440" height="1080" loading="lazy" decoding="async" alt="SheetPilot AI — редактирование Excel обычным языком"/>
    <img src="/assets/cases/sheetpilot-ai/sheetpilot-02.svg" width="1440" height="1080" loading="lazy" decoding="async" alt="" aria-hidden="true"/>
    <img src="/assets/cases/sheetpilot-ai/sheetpilot-03.svg" width="1440" height="1080" loading="lazy" decoding="async" alt="" aria-hidden="true"/>
    <img src="/assets/cases/sheetpilot-ai/sheetpilot-04.svg" width="1440" height="1080" loading="lazy" decoding="async" alt="" aria-hidden="true"/>
    <img src="/assets/cases/sheetpilot-ai/sheetpilot-01.svg" width="1440" height="1080" loading="lazy" decoding="async" alt="" aria-hidden="true"/>
  </div>
  <span class="sp-slider-shade" aria-hidden="true"></span>
  <span class="sp-slider-progress" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
</div>'''

if 'id="stage60-sheetpilot-slider-style"' not in text:
    if '</head>' not in text:
        raise SystemExit('stage60: </head> not found')
    text = text.replace('</head>', STYLE + '</head>', 1)

if 'class="s44-case__image sp-image-slider"' not in text:
    card_start = text.find('<a class="s44-case s44-case--visual s44-case--sheetpilot"')
    if card_start < 0:
        raise SystemExit('stage60: SheetPilot card not found')
    body_start = text.find('<div class="s44-case__body">', card_start)
    if body_start < 0:
        raise SystemExit('stage60: SheetPilot body not found')
    segment = text[card_start:body_start]
    image_match = re.search(r'<div class="s44-case__image">\s*<img\b[^>]*>\s*</div>', segment, flags=re.S)
    if not image_match:
        raise SystemExit('stage60: SheetPilot image block not found')
    absolute_start = card_start + image_match.start()
    absolute_end = card_start + image_match.end()
    text = text[:absolute_start] + SLIDER + text[absolute_end:]

# Build-time guards: the global grid must remain untouched, while all four SheetPilot visuals exist.
if 's60-carousel' in text or 'data-stage60-carousel-tools' in text:
    raise SystemExit('stage60: project carousel remnants detected')
for n in range(1, 5):
    if f'/assets/cases/sheetpilot-ai/sheetpilot-0{n}.svg' not in text:
        raise SystemExit(f'stage60: missing SheetPilot visual {n}')
if 'class="s44-case-grid"' not in text:
    raise SystemExit('stage60: original project grid missing')

page.write_text(text, encoding='utf-8')
print('stage60: original project grid restored; SheetPilot visuals slide smoothly inside its card')
