/* stage145-cases-gallery-interactive */
(() => {
  const main = document.querySelector('[data-stage130-hub="cases"]');
  const section = main?.querySelector('.p130-list-section');
  const shell = section?.querySelector(':scope > .p130-shell');
  if (!main || !section || !shell) return;

  document.querySelectorAll('[data-stage130-hub="cases"] .p130-tile').forEach((tile) => {
    tile.addEventListener('pointermove', (event) => {
      const r = tile.getBoundingClientRect();
      tile.style.setProperty('--x145-card-x', `${event.clientX - r.left}px`);
      tile.style.setProperty('--x145-card-y', `${event.clientY - r.top}px`);
    }, { passive: true });
  });

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const coarse = matchMedia('(pointer: coarse)').matches;
  const saveData = !!(navigator.connection && navigator.connection.saveData);
  if (reduced || coarse || saveData || innerWidth <= 900) return;

  const canvas = document.createElement('canvas');
  canvas.className = 'x145-cases-webgl';
  canvas.setAttribute('aria-hidden', 'true');
  section.prepend(canvas);

  const gl = canvas.getContext('webgl', {
    alpha: true,
    antialias: false,
    depth: false,
    stencil: false,
    powerPreference: 'low-power',
    premultipliedAlpha: false
  });
  if (!gl) { canvas.remove(); return; }

  const vertex = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.0,1.0);}';
  const fragment = `
    precision mediump float;
    uniform vec2 r;
    uniform vec2 m;
    uniform float t;

    float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453123);}
    float noise(vec2 p){
      vec2 i=floor(p),f=fract(p);
      f=f*f*(3.0-2.0*f);
      return mix(mix(hash(i),hash(i+vec2(1.,0.)),f.x),mix(hash(i+vec2(0.,1.)),hash(i+vec2(1.,1.)),f.x),f.y);
    }
    float fbm(vec2 p){
      float v=0.0;
      v+=noise(p)*.54;p=p*2.04+vec2(2.8,1.4);
      v+=noise(p)*.28;p=p*2.01+vec2(1.1,3.3);
      v+=noise(p)*.12;
      return v;
    }
    void main(){
      vec2 uv=(gl_FragCoord.xy-.5*r)/max(r.y,1.0);
      vec2 mm=(m-.5*r)/max(r.y,1.0);
      float tt=t*.075;
      float n=fbm(uv*1.1+vec2(tt,-tt*.58));
      float contour=.5+.5*sin((uv.x*1.8+uv.y*1.15+n*3.7+tt*2.3)*3.14159);
      float contour2=.5+.5*sin((uv.x*1.05-uv.y*1.65-n*2.8-tt*1.7)*3.14159);
      float thread=pow(max(0.0,contour*contour2),4.3);
      float d=length(uv-mm*.58);
      float focus=exp(-d*d*1.85);
      float orbit=exp(-abs(length(uv-mm*.34)-.38)*13.0);

      vec3 coral=vec3(.92,.38,.28);
      vec3 violet=vec3(.39,.42,.96);
      vec3 lime=vec3(.68,.84,.22);
      vec3 col=mix(coral,violet,clamp(n*.72+contour*.34,0.0,1.0));
      col=mix(col,lime,focus*.25+orbit*.08);
      col+=vec3(1.0)*thread*.04;

      float alpha=.03+n*.072+focus*.055+orbit*.032+thread*.048;
      gl_FragColor=vec4(col,alpha);
    }
  `;

  const compile = (type, source) => {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.warn('stage145 shader compile failed', gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  };

  const vs = compile(gl.VERTEX_SHADER, vertex);
  const fs = compile(gl.FRAGMENT_SHADER, fragment);
  if (!vs || !fs) { canvas.remove(); return; }

  const program = gl.createProgram();
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) { canvas.remove(); return; }
  gl.useProgram(program);

  const buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]), gl.STATIC_DRAW);
  const pos = gl.getAttribLocation(program, 'p');
  gl.enableVertexAttribArray(pos);
  gl.vertexAttribPointer(pos, 2, gl.FLOAT, false, 0, 0);

  const ur = gl.getUniformLocation(program, 'r');
  const um = gl.getUniformLocation(program, 'm');
  const ut = gl.getUniformLocation(program, 't');

  let mx=.5,my=.36,tx=mx,ty=my,frame=0,active=true;
  const start=performance.now();

  const resize=()=>{
    const rect=section.getBoundingClientRect();
    const dpr=Math.min(devicePixelRatio||1,1.2);
    const w=Math.max(1,Math.round(rect.width*dpr));
    const h=Math.max(1,Math.round(rect.height*dpr));
    if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;gl.viewport(0,0,w,h)}
  };
  resize();
  const ro='ResizeObserver' in window?new ResizeObserver(resize):null;
  if(ro)ro.observe(section); else addEventListener('resize',resize,{passive:true});

  section.addEventListener('pointermove',(event)=>{
    const rect=section.getBoundingClientRect();
    tx=(event.clientX-rect.left)/Math.max(rect.width,1);
    ty=1-(event.clientY-rect.top)/Math.max(rect.height,1);
  },{passive:true});
  section.addEventListener('pointerleave',()=>{tx=.5;ty=.36},{passive:true});

  const draw=(now)=>{
    if(!active){frame=0;return}
    mx+=(tx-mx)*.03; my+=(ty-my)*.03;
    gl.uniform2f(ur,canvas.width,canvas.height);
    gl.uniform2f(um,mx*canvas.width,my*canvas.height);
    gl.uniform1f(ut,(now-start)/1000);
    gl.drawArrays(gl.TRIANGLES,0,6);
    frame=requestAnimationFrame(draw);
  };

  const io=new IntersectionObserver(([entry])=>{
    active=entry.isIntersecting&&!document.hidden;
    if(active&&!frame)frame=requestAnimationFrame(draw);
    if(!active&&frame){cancelAnimationFrame(frame);frame=0}
  },{threshold:0});
  io.observe(section);

  document.addEventListener('visibilitychange',()=>{
    const rect=section.getBoundingClientRect();
    active=!document.hidden&&rect.bottom>0&&rect.top<innerHeight;
    if(active&&!frame)frame=requestAnimationFrame(draw);
    if(!active&&frame){cancelAnimationFrame(frame);frame=0}
  });

  frame=requestAnimationFrame(draw);
})();
