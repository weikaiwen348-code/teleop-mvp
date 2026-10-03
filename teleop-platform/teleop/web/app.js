import * as THREE from 'three';
import {OrbitControls} from '/web/OrbitControls.js';
const $=s=>document.querySelector(s), canvas=$('#canvas');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.2));
renderer.outputColorSpace=THREE.SRGBColorSpace;
const scene=new THREE.Scene();scene.background=new THREE.Color('#e8eeef');
const camera=new THREE.PerspectiveCamera(40,1,.01,20);camera.up.set(0,0,1);camera.position.set(1.25,-1.65,1.35);
const orbit=new OrbitControls(camera,canvas);orbit.target.set(.28,0,.48);orbit.enableDamping=true;
scene.add(new THREE.HemisphereLight(0xffffff,0x8ba0ac,2.1));
const light=new THREE.DirectionalLight(0xffffff,2.5);light.position.set(2,-3,4);scene.add(light);
const ground=new THREE.Mesh(new THREE.PlaneGeometry(3.4,3.4),new THREE.MeshStandardMaterial({color:'#d2dee2',roughness:1}));ground.position.z=-.002;scene.add(ground);
const grid=new THREE.GridHelper(3.4,17,0xa6bbc4,0xc4d3d9);grid.rotation.x=Math.PI/2;grid.position.z=.001;scene.add(grid);
const axis=new THREE.AxesHelper(.13);axis.position.set(-.13,-.16,.004);scene.add(axis);
const objects=new Map(), ranges=[], matrix=new THREE.Matrix4();
let state=null,armed=false,paused=false,epoch='',finished=false,initialized=false,modelReady=false;
const worker=new Worker('/web/control-worker.js');
function syncTarget(){worker.postMessage({type:'target',enabled:armed&&!paused,epoch,q:ranges.map(r=>Number(r.value)),gripper:Number($('#gripper').value)})}
worker.onmessage=({data})=>{if(data.type==='disarmed'){armed=false;$('#message').textContent='跟随已停止：'+data.reason+'。请对齐并重新使能。'}};
worker.postMessage({type:'init',token:window.CONTROL_TOKEN});
let lastPaint=0;
function render(t){requestAnimationFrame(render);if(t-lastPaint<33)return;lastPaint=t;const w=canvas.clientWidth,h=canvas.clientHeight;if(canvas.width!==Math.floor(w*renderer.getPixelRatio())||canvas.height!==Math.floor(h*renderer.getPixelRatio())){renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix()}orbit.update();renderer.render(scene,camera)}requestAnimationFrame(render);
async function post(path,data){const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-Control-Token':window.CONTROL_TOKEN},body:JSON.stringify(data)});const j=await r.json();if(!r.ok)throw Error(j.error||'请求失败');return j}
function align(){if(!state)return;ranges.forEach((r,i)=>{r.value=state.q[i];r.dispatchEvent(new Event('input'))});$('#gripper').value=state.gripper;$('#gripper').dispatchEvent(new Event('input'))}
async function loadModel(){const model=await (await fetch('/api/model')).json();const geometries=new Map();for(const [id,m] of Object.entries(model.meshes)){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(m.vertices,3));g.setIndex(m.faces);g.computeVertexNormals();geometries.set(Number(id),g)}for(const item of model.geoms){const c=new THREE.Color().setRGB(...item.color.slice(0,3));const mesh=new THREE.Mesh(geometries.get(item.mesh),new THREE.MeshStandardMaterial({color:c,roughness:.53,metalness:.08}));scene.add(mesh);objects.set(item.id,mesh)}modelReady=true;$('#message').textContent='Panda 模型已加载。点击开启跟随后可以手动控制。'}
function updateUI(s){$('#mode').textContent=({DISARMED:'未使能',ACTIVE:'跟随中',HOLD:'保持',ESTOP:'急停锁定',FAULT:'故障'})[s.mode]||s.mode;$('#mode').style.color=s.mode==='ESTOP'||s.mode==='FAULT'?'#c34148':'#087f8c';$('#time').textContent=s.time.toFixed(1)+' s';$('#rows').textContent=s.recorded_rows;$('#error').textContent=Math.max(...s.q.map((x,i)=>Math.abs(x-s.target[i]))).toFixed(3)+' rad';const events={startup:'系统等待人工使能。',armed:'正在接收人工输入，关节目标经过速度和加速度限制。',input_timeout:'输入已中断，系统进入保持。恢复后请重新开启跟随。',local_ui_estop:'软件急停已锁定，需要本地复位。',local_reset:'已复位，请重新开启跟随。',tracking_error:'跟踪差超过阈值，请复位并减小运动幅度。',deadman_released:'操作端取消使能，系统保持当前位置。'};$('#event').textContent=events[s.reason]||s.reason;if(s.mode==='ESTOP'||s.mode==='FAULT'||(s.mode==='HOLD'&&epoch!==s.epoch))armed=false;for(const pose of s.poses||[]){const obj=objects.get(pose.id);if(!obj)continue;const a=pose.mat;matrix.set(a[0],a[1],a[2],0,a[3],a[4],a[5],0,a[6],a[7],a[8],0,0,0,0,1);obj.position.fromArray(pose.pos);obj.quaternion.setFromRotationMatrix(matrix)}if(s.finished&&s.summary){finished=true;$('#saved').style.display='block';$('#message').textContent=`完整保存 ${s.summary.steps} 行，已同时导出 episode.npz。`;document.querySelectorAll('button,input').forEach(x=>x.disabled=true)}}
function setupSliders(s){for(let i=0;i<7;i++){const row=document.createElement('div');row.className='row';row.innerHTML=`<label for="joint-${i}">关节 ${i+1}<output id="joint-value-${i}"></output></label><input id="joint-${i}" type="range" min="${s.lower[i]}" max="${s.upper[i]}" step="0.005" value="${s.q[i]}">`;$('#sliders').appendChild(row);const r=row.querySelector('input');r.addEventListener('input',()=>{row.querySelector('output').textContent=Number(r.value).toFixed(3)+' rad';syncTarget()});r.dispatchEvent(new Event('input'));ranges.push(r)}initialized=true}
$('#gripper').addEventListener('input',()=>{$('#gripper-value').textContent=Math.round(Number($('#gripper').value)*100)+'%';syncTarget()});
$('#enable').onclick=()=>{if(!state||!modelReady)return;armed=false;align();epoch=state.epoch;armed=true;paused=false;$('#pause').classList.remove('paused');$('#pause').textContent='暂停指令发送';$('#message').textContent='已对齐当前位置。现在可以拖动关节滑块。';syncTarget()};
$('#align').onclick=align;
$('#pause').onclick=()=>{paused=!paused;$('#pause').classList.toggle('paused',paused);$('#pause').textContent=paused?'恢复指令发送':'暂停指令发送';$('#message').textContent=paused?'指令发送暂停，机器人端会独立检测输入超时。':'发送已恢复，请点击开启跟随。';if(!paused)armed=false;syncTarget()};
$('#estop').onclick=async()=>{armed=false;syncTarget();await post('/api/action',{action:'estop'})};
$('#reset').onclick=async()=>{armed=false;syncTarget();await post('/api/action',{action:'reset'});$('#message').textContent='已本地复位，请重新开启跟随。'};
$('#finish').onclick=async()=>{armed=false;syncTarget();await post('/api/action',{action:'finish'});$('#message').textContent='正在关闭轨迹并计算校验和。'};
async function tick(){try{state=await(await fetch('/api/state')).json();if(!initialized)setupSliders(state);updateUI(state)}catch(e){$('#message').textContent='连接异常：'+e.message}if(!finished)setTimeout(tick,100)}
loadModel().catch(e=>$('#message').textContent='模型加载失败：'+e.message);tick();
// A read-only state hook for reproducible UI checks, not an automatic motion generator.
window.teleopView={getState:()=>state,isModelReady:()=>modelReady};
