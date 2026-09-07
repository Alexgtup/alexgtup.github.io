#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
page = root / 'index.html'
if not page.is_file():
    raise SystemExit(f'stage60: home page missing: {page}')

text = page.read_text(encoding='utf-8')

STYLE = r'''
<style id="stage60-project-carousel-style">
.s44-projects .s44-case-grid.s60-carousel{
  display:grid!important;
  grid-template-columns:none!important;
  grid-auto-flow:column!important;
  grid-auto-columns:clamp(24rem,47vw,43rem)!important;
  gap:1rem!important;
  overflow-x:auto!important;
  overflow-y:hidden!important;
  scroll-snap-type:x mandatory;
  scroll-behavior:smooth;
  overscroll-behavior-inline:contain;
  scrollbar-width:none;
  -ms-overflow-style:none;
  padding:.2rem 0 1rem!important;
  margin-top:1rem;
  touch-action:pan-x pan-y;
  -webkit-overflow-scrolling:touch;
}
.s44-projects .s44-case-grid.s60-carousel::-webkit-scrollbar{display:none}
.s44-projects .s44-case-grid.s60-carousel>*{
  grid-column:auto!important;
  min-width:0!important;
  scroll-snap-align:start;
  scroll-snap-stop:always;
  opacity:.68;
  transform:scale(.978);
  transform-origin:center;
  transition:opacity .45s ease,transform .55s cubic-bezier(.2,.7,.2,1),border-color .35s ease,box-shadow .45s ease;
}
.s44-projects .s44-case-grid.s60-carousel>*.is-active{
  opacity:1;
  transform:scale(1);
  box-shadow:0 24px 70px rgba(0,0,0,.28);
}
.s44-projects .s44-case--sheetpilot{grid-template-columns:minmax(0,.56fr) minmax(0,.44fr)!important;min-height:22rem!important}
.s60-carousel-tools{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin:.3rem 0 .35rem}
.s60-carousel-hint{display:flex;align-items:center;gap:.65rem;color:#7f8993;font-size:.72rem}
.s60-carousel-hint i{width:.42rem;height:.42rem;border-radius:50%;background:#d4fe6a;box-shadow:0 0 18px rgba(212,254,106,.45)}
.s60-carousel-ui{display:flex;align-items:center;gap:.55rem}
.s60-carousel-progress{width:clamp(5.5rem,10vw,9rem);height:3px;border-radius:999px;background:rgba(255,255,255,.09);overflow:hidden}
.s60-carousel-progress>i{display:block;width:100%;height:100%;transform:scaleX(0);transform-origin:left center;background:#d4fe6a;transition:transform .18s ease}
.s60-carousel-btn{width:2.55rem;height:2.55rem;border-radius:999px;border:1px solid rgba(255,255,255,.12);background:#10151a;color:#f4f6f4;display:grid;place-items:center;cursor:pointer;font-size:1rem;transition:transform .22s ease,border-color .22s ease,background .22s ease,color .22s ease,opacity .22s ease}
.s60-carousel-btn:hover{transform:translateY(-2px);border-color:rgba(212,254,106,.38);background:#151c18;color:#d4fe6a}
.s60-carousel-btn:active{transform:translateY(0) scale(.96)}
.s60-carousel-btn[disabled]{opacity:.35;cursor:default;transform:none}
.s60-carousel-btn:focus-visible{outline:2px solid #d4fe6a;outline-offset:3px}
.s60-carousel-edge{position:relative}
.s60-carousel-edge:after{content:"";position:absolute;right:0;top:3.3rem;bottom:1rem;width:clamp(2rem,6vw,5rem);pointer-events:none;background:linear-gradient(90deg,transparent,rgba(8,11,15,.88));opacity:.85}
@media(max-width:900px){
  .s44-projects .s44-case-grid.s60-carousel{grid-auto-columns:min(86vw,38rem)!important;gap:.75rem!important}
  .s44-projects .s44-case--sheetpilot{grid-template-columns:1fr!important;min-height:0!important}
  .s60-carousel-progress{width:5.5rem}
}
@media(max-width:620px){
  .s44-projects .s44-case-grid.s60-carousel{grid-auto-columns:88vw!important;padding-bottom:.55rem!important}
  .s60-carousel-hint span{display:none}
  .s60-carousel-btn{width:2.35rem;height:2.35rem}
  .s60-carousel-edge:after{width:1.5rem;top:3rem}
}
@media(prefers-reduced-motion:reduce){
  .s44-projects .s44-case-grid.s60-carousel{scroll-behavior:auto}
  .s44-projects .s44-case-grid.s60-carousel>*{transition:none;transform:none;opacity:1}
}
</style>
'''

TOOLS = r'''
<div class="s60-carousel-tools" data-stage60-carousel-tools="true">
  <div class="s60-carousel-hint"><i aria-hidden="true"></i><span>Листайте проекты — стрелками, трекпадом или свайпом</span></div>
  <div class="s60-carousel-ui">
    <div class="s60-carousel-progress" aria-hidden="true"><i></i></div>
    <button class="s60-carousel-btn" type="button" data-s60-prev aria-label="Предыдущий проект">←</button>
    <button class="s60-carousel-btn" type="button" data-s60-next aria-label="Следующий проект">→</button>
  </div>
</div>
'''

SCRIPT = r'''
<script id="stage60-project-carousel-script">
(()=>{
  const init=()=>{
    const track=document.querySelector('.s44-projects .s44-case-grid.s60-carousel');
    if(!track || track.dataset.s60Ready==='1') return;
    track.dataset.s60Ready='1';
    const prev=document.querySelector('[data-s60-prev]');
    const next=document.querySelector('[data-s60-next]');
    const bar=document.querySelector('.s60-carousel-progress>i');
    const items=[...track.children];
    if(!items.length) return;

    const gap=()=>parseFloat(getComputedStyle(track).columnGap||getComputedStyle(track).gap||'16')||16;
    const step=()=>Math.max(1,items[0].getBoundingClientRect().width+gap());
    const maxScroll=()=>Math.max(0,track.scrollWidth-track.clientWidth);

    let raf=0;
    const update=()=>{
      raf=0;
      const max=maxScroll();
      const ratio=max>0?Math.min(1,Math.max(0,track.scrollLeft/max)):0;
      if(bar) bar.style.transform=`scaleX(${Math.max(.045,ratio)})`;
      if(prev) prev.disabled=track.scrollLeft<=3;
      if(next) next.disabled=track.scrollLeft>=max-3;
    };
    const schedule=()=>{if(!raf) raf=requestAnimationFrame(update)};
    const move=(dir)=>track.scrollBy({left:dir*step(),behavior:'smooth'});

    prev?.addEventListener('click',()=>{move(-1);pauseAuto()});
    next?.addEventListener('click',()=>{move(1);pauseAuto()});
    track.addEventListener('scroll',schedule,{passive:true});
    track.addEventListener('keydown',(e)=>{
      if(e.key==='ArrowRight'){e.preventDefault();move(1);pauseAuto()}
      if(e.key==='ArrowLeft'){e.preventDefault();move(-1);pauseAuto()}
    });

    const observer=new IntersectionObserver(entries=>{
      entries.forEach(entry=>entry.target.classList.toggle('is-active',entry.intersectionRatio>=.58));
    },{root:track,threshold:[.2,.58,.85]});
    items.forEach(item=>observer.observe(item));

    let timer=null;
    let resumeTimer=null;
    const fine=matchMedia('(pointer:fine) and (prefers-reduced-motion:no-preference)');
    const startAuto=()=>{
      if(!fine.matches || document.hidden || timer) return;
      timer=setInterval(()=>{
        const max=maxScroll();
        if(max<8) return;
        const atEnd=track.scrollLeft>=max-6;
        track.scrollTo({left:atEnd?0:Math.min(max,track.scrollLeft+step()),behavior:'smooth'});
      },5200);
    };
    const stopAuto=()=>{if(timer){clearInterval(timer);timer=null}};
    function pauseAuto(){
      stopAuto();
      if(resumeTimer) clearTimeout(resumeTimer);
      resumeTimer=setTimeout(startAuto,9000);
    }
    track.addEventListener('mouseenter',stopAuto);
    track.addEventListener('mouseleave',startAuto);
    track.addEventListener('pointerdown',pauseAuto,{passive:true});
    track.addEventListener('touchstart',pauseAuto,{passive:true});
    track.addEventListener('focusin',stopAuto);
    track.addEventListener('focusout',startAuto);
    document.addEventListener('visibilitychange',()=>document.hidden?stopAuto():startAuto());
    fine.addEventListener?.('change',()=>{stopAuto();startAuto()});
    window.addEventListener('resize',schedule,{passive:true});

    update();
    startAuto();
  };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init,{once:true});
  else init();
})();
</script>
'''

if 'id="stage60-project-carousel-style"' not in text:
    if '</head>' not in text:
        raise SystemExit('stage60: </head> not found')
    text = text.replace('</head>', STYLE + '</head>', 1)

if 'data-stage60-carousel-tools="true"' not in text:
    marker = '<div class="s44-case-grid">'
    if marker not in text:
        marker = '<div class="s44-case-grid s60-carousel" id="project-carousel" tabindex="0" aria-label="Карусель проектов">'
    if marker.startswith('<div class="s44-case-grid">'):
        replacement = TOOLS + '<div class="s44-case-grid s60-carousel" id="project-carousel" tabindex="0" aria-label="Карусель проектов">'
        text = text.replace(marker, replacement, 1)
    else:
        text = text.replace(marker, TOOLS + marker, 1)
else:
    text = text.replace('<div class="s44-case-grid">','<div class="s44-case-grid s60-carousel" id="project-carousel" tabindex="0" aria-label="Карусель проектов">',1)

if 'id="stage60-project-carousel-script"' not in text:
    if '</body>' not in text:
        raise SystemExit('stage60: </body> not found')
    text = text.replace('</body>', SCRIPT + '</body>', 1)

if 's60-carousel' not in text or 'data-s60-next' not in text or 'stage60-project-carousel-script' not in text:
    raise SystemExit('stage60: carousel injection failed')

page.write_text(text, encoding='utf-8')
print('stage60: smooth project carousel enabled on homepage')
