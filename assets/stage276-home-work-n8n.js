
(()=>{
  const body=document.body;
  if(!body||body.dataset.page!=="home"||body.dataset.stage276Work!=="true") return;
  const feature=document.querySelector(".p276-feature");
  const shot=document.querySelector(".p276-product-shot");
  if(!feature||!shot||matchMedia("(prefers-reduced-motion: reduce)").matches||!matchMedia("(hover:hover) and (pointer:fine)").matches) return;
  feature.addEventListener("pointermove",e=>{
    const r=feature.getBoundingClientRect();
    const x=((e.clientX-r.left)/r.width-.5)*2;
    const y=((e.clientY-r.top)/r.height-.5)*2;
    shot.style.transform="perspective(1400px) rotateX("+(-y*1.1+1.2).toFixed(2)+"deg) rotateY("+(x*1.5).toFixed(2)+"deg) translateY(-2px)";
  },{passive:true});
  feature.addEventListener("pointerleave",()=>{shot.style.transform=""},{passive:true});
})();
