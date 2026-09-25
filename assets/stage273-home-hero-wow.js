
(() => {
  const body=document.body;
  if(!body || body.dataset.page!=="home" || body.dataset.stage273Hero!=="true") return;
  const hero=document.querySelector(".p128-hero");
  if(!hero) return;
  const reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine=matchMedia("(hover:hover) and (pointer:fine) and (min-width:901px)").matches;
  if(reduce || !fine) return;
  let raf=0, tx=0, ty=0;
  const paint=()=>{
    raf=0;
    body.style.setProperty("--p273-x",tx.toFixed(3));
    body.style.setProperty("--p273-y",ty.toFixed(3));
    body.style.setProperty("--p273-glow-x",(70+tx*8).toFixed(1)+"%");
    body.style.setProperty("--p273-glow-y",(36+ty*7).toFixed(1)+"%");
    body.style.setProperty("--p273-copy-x",(-tx*3).toFixed(2)+"px");
    body.style.setProperty("--p273-copy-y",(-ty*2).toFixed(2)+"px");
    body.style.setProperty("--p273-bg-x",(-tx*8).toFixed(2)+"px");
    body.style.setProperty("--p273-bg-y",(-ty*6).toFixed(2)+"px");
    body.style.setProperty("--p273-orbit-x",(tx*13).toFixed(2)+"px");
    body.style.setProperty("--p273-orbit-y",(ty*9).toFixed(2)+"px");
    body.style.setProperty("--p273-orbit-rev-x",(-tx*9).toFixed(2)+"px");
    body.style.setProperty("--p273-orbit-rev-y",(-ty*7).toFixed(2)+"px");
    body.style.setProperty("--p273-live-x",(-tx*12).toFixed(2)+"px");
    body.style.setProperty("--p273-live-y",(-ty*9).toFixed(2)+"px");
    body.style.setProperty("--p273-window-x",(tx*11).toFixed(2)+"px");
    body.style.setProperty("--p273-window-y",(ty*8).toFixed(2)+"px");
    body.style.setProperty("--p273-window-ry",(tx*1.8).toFixed(2)+"deg");
    body.style.setProperty("--p273-window-rx",(-ty*1.2).toFixed(2)+"deg");
    body.style.setProperty("--p273-mobile-x",(-tx*15).toFixed(2)+"px");
    body.style.setProperty("--p273-mobile-y",(-ty*10).toFixed(2)+"px");
    body.style.setProperty("--p273-mobile-ry",(-tx*1.4).toFixed(2)+"deg");
    body.style.setProperty("--p273-flow-x",(tx*8).toFixed(2)+"px");
    body.style.setProperty("--p273-flow-y",(-ty*8).toFixed(2)+"px");
  };
  hero.addEventListener("pointermove",(e)=>{
    const r=hero.getBoundingClientRect();
    tx=Math.max(-1,Math.min(1,(e.clientX-r.left)/r.width*2-1));
    ty=Math.max(-1,Math.min(1,(e.clientY-r.top)/r.height*2-1));
    if(!raf) raf=requestAnimationFrame(paint);
  },{passive:true});
  hero.addEventListener("pointerleave",()=>{
    tx=0;ty=0;
    if(!raf) raf=requestAnimationFrame(paint);
  },{passive:true});
})();
