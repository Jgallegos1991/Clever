// WebGL2 nanobot swarm — 3D, soft neon, offline-only
// - 20k+ points, perspective depth, shape morphs (sphere, ring, torus, panel, text),
// - free-hand attractor, idle self-evolution, brightness kept soft (alpha <= 0.25)
// Exports: startParticles(canvas, {count}), triggerPulse(), updateFieldMode(mode), morphForIntent(meta)

let gl, program, buffer, uPointSize, uColorA, uColorB, uProj, uTime;
let positions, targets, velocities, count = 20000, width, height;
let modeHue = 200; // default hue
let pulseEnergy = 0;
let proj = new Float32Array(16);
let startTime = performance.now();
let pointer = { x: 0, y: 0, down: false };
let idleTimer = 0;

const VS = `#version 300 es
precision mediump float;
layout(location=0) in vec3 a_position;
uniform mat4 u_proj;
uniform float u_pointSize;
uniform float u_time;
void main(){
  // Gentle auto-rotation around Y for a sense of depth
  float ang = u_time * 0.15;
  float ca = cos(ang), sa = sin(ang);
  vec3 p = vec3(
    a_position.x * ca + a_position.z * sa,
    a_position.y,
    -a_position.x * sa + a_position.z * ca
  );
  vec4 clip = u_proj * vec4(p, 1.0);
  gl_Position = clip;
  // Perspective-scaled point size
  float w = max(0.0001, clip.w);
  float perspective = 1.0 / w;
  gl_PointSize = u_pointSize * clamp(perspective * 1.8, 0.6, 3.5);
}
`;

const FS = `#version 300 es
precision mediump float;
out vec4 outColor;
uniform vec4 u_colorA; // inner
uniform vec4 u_colorB; // outer
void main(){
  // soft round point
  vec2 p = gl_PointCoord.xy * 2.0 - 1.0;
  float r = clamp(1.0 - dot(p,p), 0.0, 1.0);
  vec4 c = mix(u_colorB, u_colorA, pow(r, 1.5));
  c.a *= r;
  outColor = c;
}
`;

function mkShader(type, src){
  const s = gl.createShader(type);
  gl.shaderSource(s, src);
  gl.compileShader(s);
  if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)){
    throw new Error(gl.getShaderInfoLog(s)||'shader compile failed');
  }
  return s;
}

function mkProgram(){
  const vs = mkShader(gl.VERTEX_SHADER, VS);
  const fs = mkShader(gl.FRAGMENT_SHADER, FS);
  const p = gl.createProgram();
  gl.attachShader(p, vs); gl.attachShader(p, fs);
  gl.bindAttribLocation(p, 0, 'a_position');
  gl.linkProgram(p);
  if (!gl.getProgramParameter(p, gl.LINK_STATUS)){
    throw new Error(gl.getProgramInfoLog(p)||'link failed');
  }
  return p;
}

function hsv(h, s, v, a=1){
  let f = (n, k=(n+h/60)%6) => v - v*s*Math.max(Math.min(k,4-k,1),0);
  return [f(5), f(3), f(1), a];
}

function setColors(){
  // Keep alpha soft per spec (<= 0.25)
  const inner = hsv(modeHue, 1, 0.9, 0.22);
  const outer = hsv((modeHue+30)%360, 0.8, 0.8, 0.06);
  gl.uniform4fv(uColorA, inner);
  gl.uniform4fv(uColorB, outer);
}

function perspective(out, fovy, aspect, near, far){
  const f = 1.0 / Math.tan(fovy/2);
  out[0]=f/aspect; out[1]=0; out[2]=0; out[3]=0;
  out[4]=0; out[5]=f; out[6]=0; out[7]=0;
  out[8]=0; out[9]=0; out[10]=(far+near)/(near-far); out[11]=-1;
  out[12]=0; out[13]=0; out[14]=(2*far*near)/(near-far); out[15]=0;
  return out;
}

function resize(canvas){
  width = canvas.width = window.innerWidth;
  height = canvas.height = window.innerHeight;
  gl.viewport(0,0,width,height);
  perspective(proj, Math.PI/3, width/height, 0.1, 2000.0);
  gl.uniformMatrix4fv(uProj, false, proj);
}

function initParticles(){
  positions = new Float32Array(count*3);
  targets = new Float32Array(count*3);
  velocities = new Float32Array(count*3);
  const R = Math.min(width, height) * 0.35;
  for (let i=0;i<count;i++){
    // start in a loose sphere
    const a = Math.random()*Math.PI*2;
    const b = Math.acos(2*Math.random()-1);
    const r = R * Math.cbrt(Math.random());
    const x = r*Math.sin(b)*Math.cos(a);
    const y = r*Math.cos(b);
    const z = r*Math.sin(b)*Math.sin(a) - 500; // shift back a bit
    const ix = i*3;
    positions[ix]=x; positions[ix+1]=y; positions[ix+2]=z;
    targets[ix]=x; targets[ix+1]=y; targets[ix+2]=z;
    velocities[ix]=0; velocities[ix+1]=0; velocities[ix+2]=0;
  }
  buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, positions, gl.DYNAMIC_DRAW);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);
}

function morphTo(shape){
  const n = count;
  if (shape === 'sphere'){
    const R = Math.min(width, height)*0.35;
    for(let i=0;i<n;i++){
      const phi = Math.acos(1 - 2 * (i + 0.5) / n);
      const theta = Math.PI * (1 + Math.sqrt(5)) * i;
      const x = R * Math.sin(phi) * Math.cos(theta);
      const y = R * Math.cos(phi);
      const z = R * Math.sin(phi) * Math.sin(theta) - 500;
      const ix=i*3; targets[ix]=x; targets[ix+1]=y; targets[ix+2]=z;
    }
  } else if (shape === 'ring'){
    const R = Math.min(width, height)*0.42;
    for(let i=0;i<n;i++){
      const a = (i/n) * Math.PI*2;
      const r = R + Math.sin(i*0.07)*6.0;
      const ix=i*3; targets[ix] = Math.cos(a)*r; targets[ix+1] = 0; targets[ix+2] = Math.sin(a)*r - 500;
    }
  } else if (shape === 'torus'){
    const R = Math.min(width, height)*0.36; // major
    const r = Math.min(width, height)*0.12; // minor
    for(let i=0;i<n;i++){
      const u = (i % Math.floor(Math.sqrt(n))) / Math.floor(Math.sqrt(n)) * Math.PI*2.0;
      const v = Math.floor(i / Math.floor(Math.sqrt(n))) / Math.floor(Math.sqrt(n)) * Math.PI*2.0;
      const x = (R + r*Math.cos(v)) * Math.cos(u);
      const y = r * Math.sin(v);
      const z = (R + r*Math.cos(v)) * Math.sin(u) - 600;
      const ix=i*3; targets[ix]=x; targets[ix+1]=y; targets[ix+2]=z;
    }
  } else if (shape === 'panel'){
    const cols = Math.floor(Math.sqrt(n));
    const spacing = Math.min(10, (Math.min(width,height)*0.55)/cols);
    const half = (cols*spacing)/2;
    for(let i=0;i<n;i++){
      const col = i % cols; const row = Math.floor(i/cols);
      const ix=i*3;
      targets[ix] = -half + col*spacing;
      targets[ix+1] = -half + row*spacing;
      targets[ix+2] = -520 + (Math.random()-0.5)*6.0; // slight thickness
    }
  } else if (shape === 'wave'){
    const cols = Math.floor(Math.sqrt(n));
    const spacing = Math.min(12, (Math.min(width,height)*0.5)/cols);
    const half = (cols*spacing)/2;
    for(let i=0;i<n;i++){
      const col = i % cols; const row = Math.floor(i/cols);
      const ix=i*3;
      const x = -half + col*spacing;
      const y = -half + row*spacing + Math.sin(col*0.3)*9.0;
      const z = -520 + Math.cos(row*0.3)*9.0;
      targets[ix]=x; targets[ix+1]=y; targets[ix+2]=z;
    }
  } else {
    // swarm random near center
    const R = Math.min(width,height)*0.4;
    for(let i=0;i<n;i++){
      const a = Math.random()*Math.PI*2; const b = Math.acos(2*Math.random()-1);
      const r = R * Math.cbrt(Math.random());
      const ix=i*3;
      targets[ix]= r*Math.sin(b)*Math.cos(a);
      targets[ix+1]= r*Math.cos(b);
      targets[ix+2]= r*Math.sin(b)*Math.sin(a) - 520;
    }
  }
  pulseEnergy += 0.5;
}

function tick(){
  // physics update
  const n=count; const follow=0.06; const jitter=0.5;
  const boost = pulseEnergy; pulseEnergy *= 0.96;
  const now = performance.now();
  for(let i=0;i<n;i++){
    const ix=i*3;
    let dx = targets[ix]-positions[ix];
    let dy = targets[ix+1]-positions[ix+1];
    let dz = targets[ix+2]-positions[ix+2];
    // Free-hand pointer attractor (project pointer into world plane z ~= -520)
    if (pointer.down){
      const px = (pointer.x - width/2);
      const py = (height/2 - pointer.y);
      dx += (px - positions[ix]) * 0.015;
      dy += (py - positions[ix+1]) * 0.015;
    }
    velocities[ix] += dx*follow + (Math.sin(i*0.13 + now*0.0017))*jitter;
    velocities[ix+1] += dy*follow + (Math.cos(i*0.11 + now*0.0014))*jitter;
    velocities[ix+2] += dz*follow + (Math.sin(i*0.07 + now*0.0011))*jitter*0.6;
    velocities[ix] *= 0.90; velocities[ix+1] *= 0.90; velocities[ix+2] *= 0.90;
    positions[ix] += velocities[ix] * (1.0 + boost*0.2);
    positions[ix+1] += velocities[ix+1] * (1.0 + boost*0.2);
    positions[ix+2] += velocities[ix+2] * (1.0 + boost*0.18);
  }
}

function render(){
  tick();
  const now = performance.now();
  const t = (now - startTime) / 1000.0;
  idleTimer += 1;
  if (idleTimer > 600) { // ~10s at 60fps
    // self-evolve morphs subtly
    const S = ['sphere','ring','torus','panel','wave','swarm'];
    morphTo(S[(Math.random()*S.length)|0]);
    idleTimer = 0;
  }
  gl.uniform1f(uTime, t);
  gl.clearColor(0,0,0,0.08);
  gl.clear(gl.COLOR_BUFFER_BIT);
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferSubData(gl.ARRAY_BUFFER, 0, positions);
  gl.drawArrays(gl.POINTS, 0, count);
  requestAnimationFrame(render);
}

export function startParticles(canvas, opts={}){
  const desired = Number(new URLSearchParams(location.search).get('particles')) || opts.count || count;
  count = Math.max(20000, Math.min(60000, desired));
  gl = canvas.getContext('webgl2', { antialias:false, premultipliedAlpha:true });
  if (!gl) throw new Error('WebGL2 not available');
  program = mkProgram();
  gl.useProgram(program);
  uPointSize = gl.getUniformLocation(program, 'u_pointSize');
  uColorA = gl.getUniformLocation(program, 'u_colorA');
  uColorB = gl.getUniformLocation(program, 'u_colorB');
  uProj = gl.getUniformLocation(program, 'u_proj');
  uTime = gl.getUniformLocation(program, 'u_time');
  gl.uniform1f(uPointSize, 2.4);
  setColors();
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
  window.addEventListener('resize', () => resize(canvas));
  resize(canvas);
  initParticles();
  morphTo('swarm');
  // pointer attractor
  const onMove = (e)=>{ const rect = canvas.getBoundingClientRect(); pointer.x = e.clientX - rect.left; pointer.y = e.clientY - rect.top; };
  canvas.addEventListener('pointerdown', (e)=>{ pointer.down = true; onMove(e); });
  canvas.addEventListener('pointermove', onMove);
  window.addEventListener('pointerup', ()=>{ pointer.down = false; });
  render();
}

export function triggerPulse(){ pulseEnergy += 0.8; }

export function updateFieldMode(mode='Base'){
  const map = { Base:200, Calm:210, Curious:270, Analytical:50, Excited:30, Positive:150, Negative:0 };
  modeHue = map[mode] ?? 200;
  setColors();
}

export function morphForIntent(meta){
  const raw = (typeof meta === 'string' ? meta : (meta?.shape || meta?.shape_to_form || '')).toLowerCase();
  if (raw.includes('write ')) {
    const txt = raw.split('write ')[1]?.trim()?.slice(0, 24) || 'CLEVER';
    morphToText(txt.toUpperCase());
  } else if (raw.includes('sphere')||raw.includes('ball')||raw.includes('circle')) morphTo('sphere');
  else if (raw.includes('torus')) morphTo('torus');
  else if (raw.includes('ring')||raw.includes('donut')) morphTo('ring');
  else if (raw.includes('panel')||raw.includes('grid')) morphTo('panel');
  else if (raw.includes('wave')||raw.includes('ocean')||raw.includes('flow')) morphTo('wave');
  else morphTo('sphere');
}

// Text morph using an offscreen canvas sampler (offline & local)
function morphToText(text){
  try {
    const size = Math.min(width, height) * 0.6;
    const cw = Math.floor(size), ch = Math.floor(size*0.35+80);
    const cvs = new OffscreenCanvas(cw, ch);
    const ctx = cvs.getContext('2d');
    ctx.clearRect(0,0,cw,ch);
    ctx.fillStyle = '#fff';
    ctx.font = `bold ${Math.floor(size*0.22)}px Inter, Arial, sans-serif`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(text, cw/2, ch/2);
    const img = ctx.getImageData(0,0,cw,ch);
    const pts = [];
    for(let y=0;y<ch;y+=2){
      for(let x=0;x<cw;x+=2){
        const a = img.data[(y*cw + x)*4 + 3];
        if (a>128 && Math.random()<0.55) pts.push([x, y]);
      }
    }
    const n = count; const cx = cw/2; const cy = ch/2; const scale = 1.5;
    for(let i=0;i<n;i++){
      const p = pts[(i%pts.length)];
      const ix=i*3;
      if (p){
        targets[ix]   = (p[0]-cx)*scale;
        targets[ix+1] = (cy-p[1])*scale;
        targets[ix+2] = -520 + (Math.random()-0.5)*4.0;
      } else {
        targets[ix]   = (Math.random()-0.5)*cw*0.6;
        targets[ix+1] = (Math.random()-0.5)*ch*0.6;
        targets[ix+2] = -520;
      }
    }
    pulseEnergy += 0.6;
  } catch (_) {
    morphTo('panel');
  }
}
