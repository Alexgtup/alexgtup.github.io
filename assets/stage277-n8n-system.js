
(()=>{
  const body=document.body;
  if(!body||body.dataset.stage277System!=="true") return;
  if(matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const hero=document.querySelector(".stage277-hero-surface");
  const art=hero?.querySelector(".stage277-canvas-art");
  if(!hero||!art||!matchMedia("(hover:hover) and (pointer:fine)").matches) return;
  let raf=0,x=0,y=0;
  const paint=()=>{
    raf=0;
    art.style.transform="translate3d("+(x*5).toFixed(2)+"px,"+(y*4).toFixed(2)+"px,0)";
  };
  hero.addEventListener("pointermove",e=>{
    const r=hero.getBoundingClientRect();
    x=((e.clientX-r.left)/r.width-.5)*2;
    y=((e.clientY-r.top)/r.height-.5)*2;
    if(!raf) raf=requestAnimationFrame(paint);
  },{passive:true});
  hero.addEventListener("pointerleave",()=>{x=0;y=0;if(!raf)raf=requestAnimationFrame(paint)},{passive:true});
})();
