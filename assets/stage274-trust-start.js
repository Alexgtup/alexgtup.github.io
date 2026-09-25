
(()=>{
 const body=document.body;
 if(!body||body.dataset.page!=="home"||body.dataset.stage274Trust!=="true") return;
 const zone=document.querySelector(".p128-proof");
 const reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
 if(zone&&!reduce&&matchMedia("(hover:hover) and (pointer:fine)").matches){
   let raf=0,x=0,y=0;
   const paint=()=>{
     raf=0;
     body.style.setProperty("--p274-light-x",(52+x*8).toFixed(1)+"%");
     body.style.setProperty("--p274-light-y",(34+y*6).toFixed(1)+"%");
   };
   zone.addEventListener("pointermove",e=>{
     const r=zone.getBoundingClientRect();
     x=Math.max(-1,Math.min(1,(e.clientX-r.left)/r.width*2-1));
     y=Math.max(-1,Math.min(1,(e.clientY-r.top)/r.height*2-1));
     if(!raf) raf=requestAnimationFrame(paint);
   },{passive:true});
   zone.addEventListener("pointerleave",()=>{x=0;y=0;if(!raf)raf=requestAnimationFrame(paint)},{passive:true});
 }
 const form=document.querySelector("#s44-brief-form");
 if(form){
   form.addEventListener("focusin",()=>form.classList.add("is-active"));
   form.addEventListener("focusout",()=>{if(!form.contains(document.activeElement)) form.classList.remove("is-active")});
 }
})();
