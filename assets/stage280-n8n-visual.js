
(()=>{
  const body=document.body;
  if(!body||body.dataset.stage280Visual!=="true") return;
  const canvas=document.querySelector(".stage280-canvas");
  const screen=canvas?.querySelector(".stage280-screen");
  if(!canvas||!screen||matchMedia("(prefers-reduced-motion: reduce)").matches||!matchMedia("(hover:hover) and (pointer:fine)").matches) return;
  canvas.addEventListener("pointermove",e=>{
    const r=canvas.getBoundingClientRect();
    const x=((e.clientX-r.left)/r.width-.5)*2;
    const y=((e.clientY-r.top)/r.height-.5)*2;
    screen.style.transform="translate(-50%,-43%) perspective(1400px) rotateX("+(-y*1.0+1.2).toFixed(2)+"deg) rotateY("+(x*1.35).toFixed(2)+"deg)";
  },{passive:true});
  canvas.addEventListener("pointerleave",()=>{screen.style.transform=""},{passive:true});
})();
