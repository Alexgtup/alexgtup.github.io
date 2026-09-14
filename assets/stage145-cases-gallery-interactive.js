/* stage145-cases-gallery-interactive */
(() => {
  const main = document.querySelector('[data-stage130-hub="cases"]');
  const section = main?.querySelector('.p130-list-section');
  const shell = section?.querySelector(':scope > .p130-shell');
  const tiles = [...(main?.querySelectorAll('.p130-tile') || [])];
  if (!main || !section || !shell || !tiles.length) return;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const coarse = matchMedia('(pointer: coarse)').matches;
  const saveData = !!(navigator.connection && navigator.connection.saveData);
  const desktopFx = !reduced && !coarse && !saveData && innerWidth > 900;

  /* Card surfaces behave like physical exhibits and feed the background with focus. */
  let activeIndex = -1;
  const setActive = (index) => {
    activeIndex = index;
    section.querySelectorAll('.x145-network path').forEach((path) => {
      const a = Number(path.dataset.a);
      const b = Number(path.dataset.b);
      path.classList.toggle('is-hot', index >= 0 && (a === index || b === index));
    });
  };

  tiles.forEach((tile, index) => {
    tile.addEventListener('pointermove', (event) => {
      const r = tile.getBoundingClientRect();
      const x = event.clientX - r.left;
      const y = event.clientY - r.top;
      tile.style.setProperty('--x145-card-x', `${x}px`);
      tile.style.setProperty('--x145-card-y', `${y}px`);
      tile.style.setProperty('--x145-angle', `${Math.atan2(y - r.height / 2, x - r.width / 2) * 180 / Math.PI + 90}deg`);
      if (desktopFx) {
        const nx = x / Math.max(r.width, 1) - .5;
        const ny = y / Math.max(r.height, 1) - .5;
        tile.style.setProperty('--x145-rx', `${(-ny * 2.8).toFixed(2)}deg`);
        tile.style.setProperty('--x145-ry', `${(nx * 3.2).toFixed(2)}deg`);
      }
    }, { passive: true });
    tile.addEventListener('pointerenter', () => setActive(index), { passive: true });
    tile.addEventListener('pointerleave', () => {
      tile.style.setProperty('--x145-rx', '0deg');
      tile.style.setProperty('--x145-ry', '0deg');
      setActive(-1);
    }, { passive: true });
  });

  if (!desktopFx) return;

  /* A live constellation connects the cases through the negative space between cards. */
  const ns = 'http://www.w3.org/2000/svg';
  const network = document.createElementNS(ns, 'svg');
  network.classList.add('x145-network');
  network.setAttribute('aria-hidden', 'true');
  network.setAttribute('preserveAspectRatio', 'none');
  section.prepend(network);

  const leftLabel = document.createElement('span');
  leftLabel.className = 'x145-field-label x145-field-label--left';
  leftLabel.textContent = 'CASE FIELD / 01—09';
  leftLabel.setAttribute('aria-hidden', 'true');
  section.append(leftLabel);

  const rightLabel = document.createElement('span');
  rightLabel.className = 'x145-field-label x145-field-label--right';
  rightLabel.textContent = 'REAL WORK / LIVE INDEX';
  rightLabel.setAttribute('aria-hidden', 'true');
  section.append(rightLabel);

  const edges = [];
  for (let i = 0; i < tiles.length - 1; i += 1) edges.push([i, i + 1]);
  for (let i = 0; i < tiles.length - 3; i += 3) edges.push([i, i + 3]);
  if (tiles.length > 5) edges.push([1, 5]);
  if (tiles.length > 8) edges.push([4, 8]);

  const buildNetwork = () => {
    const sr = section.getBoundingClientRect();
    const width = Math.max(1, sr.width);
    const height = Math.max(1, sr.height);
    network.setAttribute('viewBox', `0 0 ${width} ${height}`);
    network.textContent = '';

    const points = tiles.map((tile) => {
      const r = tile.getBoundingClientRect();
      return {
        x: r.left - sr.left + r.width / 2,
        y: r.top - sr.top + r.height / 2
      };
    });

    edges.forEach(([a, b], edgeIndex) => {
      const p1 = points[a];
      const p2 = points[b];
      if (!p1 || !p2) return;
      const path = document.createElementNS(ns, 'path');
      const dx = p2.x - p1.x;
      const dy = p2.y - p1.y;
      const bend = ((edgeIndex % 2 ? -1 : 1) * Math.min(90, Math.hypot(dx, dy) * .12));
      const c1x = p1.x + dx * .34 - dy / Math.max(Math.hypot(dx, dy), 1) * bend;
      const c1y = p1.y + dy * .34 + dx / Math.max(Math.hypot(dx, dy), 1) * bend;
      const c2x = p1.x + dx * .66 - dy / Math.max(Math.hypot(dx, dy), 1) * bend;
      const c2y = p1.y + dy * .66 + dx / Math.max(Math.hypot(dx, dy), 1) * bend;
      path.setAttribute('d', `M ${p1.x.toFixed(1)} ${p1.y.toFixed(1)} C ${c1x.toFixed(1)} ${c1y.toFixed(1)} ${c2x.toFixed(1)} ${c2y.toFixed(1)} ${p2.x.toFixed(1)} ${p2.y.toFixed(1)}`);
      path.dataset.a = String(a);
      path.dataset.b = String(b);
      if (activeIndex >= 0 && (a === activeIndex || b === activeIndex)) path.classList.add('is-hot');
      network.append(path);
    });

    points.forEach((point, index) => {
      const dot = document.createElementNS(ns, 'circle');
      dot.setAttribute('cx', point.x.toFixed(1));
      dot.setAttribute('cy', point.y.toFixed(1));
      dot.setAttribute('r', index % 3 === 0 ? '3.4' : '2.4');
      network.append(dot);
    });
  };

  requestAnimationFrame(buildNetwork);
  const networkRO = 'ResizeObserver' in window ? new ResizeObserver(() => requestAnimationFrame(buildNetwork)) : null;
  if (networkRO) networkRO.observe(section);
  addEventListener('resize', () => requestAnimationFrame(buildNetwork), { passive: true });

  /* WebGL: topographic flow + moving attractors + cursor lens + click shockwave. */
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
    uniform vec2 c;
    uniform float t;
    uniform float pulse;

    float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453123);}
    float noise(vec2 p){
      vec2 i=floor(p),f=fract(p);
      f=f*f*(3.0-2.0*f);
      return mix(mix(hash(i),hash(i+vec2(1.,0.)),f.x),mix(hash(i+vec2(0.,1.)),hash(i+vec2(1.,1.)),f.x),f.y);
    }
    float fbm(vec2 p){
      float v=0.0;
      v+=noise(p)*.54;p=p*2.03+vec2(2.7,1.3);
      v+=noise(p)*.27;p=p*2.01+vec2(1.2,3.2);
      v+=noise(p)*.13;p=p*2.02+vec2(4.1,.7);
      v+=noise(p)*.06;
      return v;
    }
    float softRing(float d,float rad,float width){return exp(-pow((d-rad)/max(width,.001),2.0));}

    void main(){
      vec2 uv=(gl_FragCoord.xy-.5*r)/max(r.y,1.0);
      vec2 mm=(m-.5*r)/max(r.y,1.0);
      vec2 cc=(c-.5*r)/max(r.y,1.0);
      float tt=t*.075;

      float n1=fbm(uv*1.02+vec2(tt,-tt*.52));
      float n2=fbm(uv*1.72+vec2(-tt*.42,tt*.28));
      vec2 warped=uv+vec2(n2-.5,n1-.5)*.075;

      vec2 a=vec2(sin(t*.17)*.72,cos(t*.13)*.38);
      vec2 b=vec2(cos(t*.11)*.62,-.28+sin(t*.09)*.32);
      vec2 d=vec2(-.48+sin(t*.07)*.22,.46+cos(t*.12)*.24);
      float fa=exp(-dot(warped-a,warped-a)*2.5);
      float fb=exp(-dot(warped-b,warped-b)*3.0);
      float fd=exp(-dot(warped-d,warped-d)*3.3);
      float field=fa+fb*.88+fd*.74+n1*.34;

      float topo=abs(fract((field+warped.x*.22-warped.y*.12)*7.0)-.5);
      float contour=1.0-smoothstep(.455,.495,topo);
      float ribbon=pow(.5+.5*sin((warped.x*2.1-warped.y*1.7+n1*4.4-tt*2.0)*3.14159),7.0);

      float md=length(warped-mm*.62);
      float focus=exp(-md*md*2.25);
      float orbit1=softRing(md,.25,.024);
      float orbit2=softRing(md,.46,.018)*.62;
      float angle=atan(warped.y-mm.y*.62,warped.x-mm.x*.62);
      float spokes=pow(max(0.0,.5+.5*cos(angle*6.0+t*.7)),12.0)*focus;

      float pd=length(warped-cc*.62);
      float shock=softRing(pd,max(0.0,pulse)*1.15,.026)*(1.0-clamp(pulse,0.0,1.0));
      shock*=step(0.0,pulse);

      vec2 grid=(warped+vec2(2.4))*8.0;
      vec2 gid=floor(grid);
      vec2 gf=fract(grid)-.5;
      float star=step(.958,hash(gid))*exp(-dot(gf,gf)*125.0);

      vec3 coral=vec3(.96,.34,.24);
      vec3 violet=vec3(.35,.35,.98);
      vec3 lime=vec3(.67,.86,.18);
      vec3 cyan=vec3(.18,.73,.88);
      vec3 ink=vec3(.18,.17,.22);

      vec3 col=mix(coral,violet,clamp(n1*.76+fa*.24,0.0,1.0));
      col=mix(col,cyan,fb*.16+ribbon*.07);
      col=mix(col,lime,focus*.30+fd*.13+shock*.72);
      col=mix(col,ink,contour*.12);
      col+=vec3(1.0)*star*.28;

      float alpha=.025+n1*.045+contour*.052+ribbon*.045+focus*.055+orbit1*.06+orbit2*.035+spokes*.035+shock*.16+star*.09;
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
  const uc = gl.getUniformLocation(program, 'c');
  const ut = gl.getUniformLocation(program, 't');
  const up = gl.getUniformLocation(program, 'pulse');

  let mx=.5,my=.36,tx=mx,ty=my,frame=0,active=true;
  let clickX=.5,clickY=.5,pulseStart=-1;
  const start=performance.now();

  const resize=()=>{
    const rect=section.getBoundingClientRect();
    const dpr=Math.min(devicePixelRatio||1,1.25);
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
  section.addEventListener('pointerdown',(event)=>{
    const rect=section.getBoundingClientRect();
    clickX=(event.clientX-rect.left)/Math.max(rect.width,1);
    clickY=1-(event.clientY-rect.top)/Math.max(rect.height,1);
    pulseStart=performance.now();
  },{passive:true});

  const draw=(now)=>{
    if(!active){frame=0;return}
    mx+=(tx-mx)*.035; my+=(ty-my)*.035;
    const pulse=pulseStart<0?-1:Math.min(1,(now-pulseStart)/1200);
    if(pulse>=1)pulseStart=-1;
    gl.uniform2f(ur,canvas.width,canvas.height);
    gl.uniform2f(um,mx*canvas.width,my*canvas.height);
    gl.uniform2f(uc,clickX*canvas.width,clickY*canvas.height);
    gl.uniform1f(ut,(now-start)/1000);
    gl.uniform1f(up,pulse);
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
