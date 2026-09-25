
(()=>{
  const body=document.body;
  if(!body||body.dataset.stage281Cinema!=="true") return;
  const reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.querySelectorAll("[data-s281-player]").forEach((player,pi)=>{
    const frames=[...player.querySelectorAll(".s281-frame")];
    const counter=player.querySelector("[data-s281-count]");
    const duration=Number(player.dataset.duration||3600);
    let index=0,timer=null,visible=true,hover=false;

    const paint=()=>{
      frames.forEach((f,i)=>f.classList.toggle("is-active",i===index));
      if(counter) counter.textContent=String(index+1).padStart(2,"0")+" / "+String(frames.length).padStart(2,"0");
      player.style.setProperty("--duration",(hover?Math.max(1500,duration*.55):duration)+"ms");
      player.classList.remove("is-playing");
      void player.offsetWidth;
      player.classList.add("is-playing");
    };
    const stop=()=>{if(timer){clearTimeout(timer);timer=null}};
    const schedule=()=>{
      stop();
      if(reduce||!visible||frames.length<2) return;
      const wait=hover?Math.max(1500,duration*.55):duration;
      timer=setTimeout(()=>{index=(index+1)%frames.length;paint();schedule()},wait);
    };
    paint();

    const io=new IntersectionObserver(es=>{
      const e=es[0]; visible=!!e?.isIntersecting;
      if(visible) schedule(); else stop();
    },{threshold:.18});
    io.observe(player);

    player.addEventListener("pointerenter",()=>{hover=true;player.classList.add("is-hovering");paint();schedule()},{passive:true});
    player.addEventListener("pointerleave",()=>{hover=false;player.classList.remove("is-hovering");paint();schedule()},{passive:true});
  });

  if(!reduce&&matchMedia("(hover:hover) and (pointer:fine)").matches){
    document.querySelectorAll(".s281-media").forEach(media=>{
      media.addEventListener("pointermove",e=>{
        const r=media.getBoundingClientRect();
        const x=((e.clientX-r.left)/r.width-.5)*2;
        const y=((e.clientY-r.top)/r.height-.5)*2;
        media.style.setProperty("--mx",(x*8).toFixed(2)+"px");
        media.style.setProperty("--my",(y*6).toFixed(2)+"px");
        media.style.setProperty("--ry",(x*1.6).toFixed(2)+"deg");
        media.style.setProperty("--rx",(-y*1.1).toFixed(2)+"deg");
      },{passive:true});
      media.addEventListener("pointerleave",()=>{
        media.style.setProperty("--mx","0px");
        media.style.setProperty("--my","0px");
        media.style.setProperty("--ry","0deg");
        media.style.setProperty("--rx","0deg");
      },{passive:true});
    });
  }
})();
