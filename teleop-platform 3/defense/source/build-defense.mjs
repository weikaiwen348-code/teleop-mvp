import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
process.env.RUNTIME_NODE=process.env.CODEX_PRIMARY_RUNTIME_NODE;
process.env.RUNTIME_NODE_MODULES=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
process.env.RUNTIME_PYTHON=process.env.CODEX_PRIMARY_RUNTIME_PYTHON;
process.env.RUNTIME_BIN_DIR=process.env.CODEX_PRIMARY_RUNTIME+'/dependencies/bin/override';
const ROOT=process.env.TELEOP_WORK_ROOT||'/workspace/scratch/4a2d12871e46';
const workspaceDir=path.join(ROOT,'presentation-work');
const build=path.join(workspaceDir,'build'), output=path.join(workspaceDir,'output');
const SKILL_DIR='/root/.codex/skills/builtins/presentations';
const {finalizePresentation,applyPresentationChartFont,resolvePresentationFont}=await import(pathToFileURL(path.join(SKILL_DIR,'container_tools/artifact_tool_utils.mjs')).href);
const family=resolvePresentationFont({fontFamily:'Noto Sans CJK SC',availableFonts:['Noto Sans CJK SC']});
const C={ink:'#153543',teal:'#087F8C',muted:'#627A84',line:'#D9E4E7',pale:'#EAF4F5',paper:'#FAFCFD',red:'#B53D48',gray:'#9AB0B8'};
const p=Presentation.create({slideSize:{width:1280,height:720}});
const data=JSON.parse(await fs.readFile(path.join(ROOT,'defense-media/evidence.json'),'utf8'));
await fs.mkdir(output,{recursive:true});await fs.mkdir(path.join(build,'preview'),{recursive:true});
const notes=[];
function text(s,str,x,y,w,h,size=25,color=C.ink,bold=false){const z=s.shapes.add({name:'text-'+str.slice(0,24),geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});z.text=str;z.text.style={typeface:family,fontSize:size,color,bold,autoFit:'none',wrap:'square',insets:{top:0,left:0,right:0,bottom:0},verticalAlignment:'top'};return z}
function rule(s,x,y,w,col=C.line){return s.shapes.add({geometry:'line',position:{left:x,top:y,width:w,height:0},fill:'none',line:{fill:col,width:1}})}
function base(title,kicker){const s=p.slides.add();s.background.fill=C.paper;text(s,kicker.toUpperCase(),64,30,1100,28,16,C.teal,true);text(s,title,64,77,1152,67,43,C.ink,true);rule(s,64,658,1152);text(s,'机器人遥操作框架 · Panda 仿真验证',64,677,1000,24,15,C.muted);text(s,String(p.slides.items.length).padStart(2,'0'),1160,674,56,24,18,C.teal,true);return s}
function note(s,str,sources=[]){str=str.replace('三千四百九十五行，其中二千三百二十六行',`${data.rows} 行，其中 ${data.active_rows} 行`).replace('约一百一十九点三毫秒',`约 ${data.last_accepted_to_hold_ms.toFixed(1)} 毫秒`).replace('这次约三十五点三五秒的本机演示，仿真控制平均九十八点八七赫兹，周期间隔百分之九十五分位约十一点七五毫秒。',`这次约 ${data.elapsed_wall_s.toFixed(2)} 秒的本机演示，仿真控制平均 ${data.actual_hz.toFixed(2)} 赫兹，周期间隔第 95 百分位约 ${data.period_p95_ms.toFixed(2)} 毫秒。`);const n=str+'\n\n证据与来源：\n'+sources.join('\n');s.speakerNotes.textFrame.setText(n);notes.push({slide:p.slides.items.length,script:str,sources})}
function table(s,values,x,y,w,h,widths){const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,columnWidths:widths,values});t.borders.assign({fill:C.line,width:1,style:'solid'});for(let r=0;r<values.length;r++){t.rows[r].height=h/values.length;for(let c=0;c<values[0].length;c++){const cell=t.getCell(r,c);cell.fill=r===0?C.ink:(r%2? '#FFFFFF':C.pale);cell.text.style={typeface:family,fontSize:r===0?22:23,color:r===0?'#FFFFFF':C.ink,bold:r===0,verticalAlignment:'middle',insets:{left:16,right:14,top:8,bottom:8}}}}return t}
async function photo(s,file,x,y,w,h,crop){return s.images.add({blob:new Uint8Array(await fs.readFile(path.join(ROOT,'defense-media',file))),contentType:'image/png',alt:'本次 Panda 仿真实际运行截图',fit:'contain',position:{left:x,top:y,width:w,height:h},...(crop?{crop}:{})})}
const modelURL='https://github.com/google-deepmind/mujoco_menagerie/tree/4d038b3feae26ec82b46a4d586379114012a8ac7/franka_emika_panda';
const gelloURL='https://arxiv.org/abs/2309.13037';
// 01
{
 const s=p.slides.add();s.background.fill=C.paper;
 text(s,'结题答辩 / 软件原型',64,51,500,40,20,C.teal,true);
 text(s,'机器人遥操作框架\n设计与仿真验证',64,181,620,175,59,C.ink,true);
 text(s,'Franka Panda · 交互控制 · 示教数据采集',64,398,610,65,25,C.muted);
 await photo(s,'demo-active.png',686,159,530,420,{left:250/1500,right:657/1500,top:180/1000,bottom:350/1000});
 rule(s,64,591,1152);text(s,'阶段成果：可运行的软件闭环与可复现的演示',64,614,1120,46,24,C.teal,true);
 text(s,'本次验证范围为仿真；未连接实体 GELLO 或机械臂。',64,673,1100,24,16,C.muted);
 note(s,'各位老师好。本项目围绕机器人遥操作和示教数据采集，完成了一套可运行的软件原型。下面主要介绍七关节映射、交互控制、断流保护和数据保存，并用 Panda 仿真的实际运行结果展示。本次验证范围是仿真，没有把实体硬件或跨地域性能作为已完成结果。',['工程 README.md、reports/RESULTS_V02.md','实际截图 defense-media/demo-active.png',modelURL]);
}
// 02
{
 const s=base('软件闭环已经跑通','01 / 完成范围');
 table(s,[['研究任务','当前成果','验证范围'],['机械臂与操作端集成','公开 Panda 模型 + 七关节滑块','仿真'],['同构映射与交互','零位/方向/比例映射 + 运动约束','软件测试'],['示教轨迹采集','状态、动作、事件与 NPZ 导出','完整性检查']],64,183,1152,344,[315,560,277]);
 text(s,'实体 GELLO、Franka/UR 驱动与动力学标定仍需实机验证。',64,564,1140,57,26,C.muted);
 note(s,'原项目包含硬件集成、控制映射和示教采集三部分。本次已完成软件侧的控制与记录闭环：操作端采用七关节滑块，机器人端采用公开 Panda 模型，保存状态、动作和事件。硬件相关目标还没有完成实机验证。因此我将成果表述为遥操作框架设计与仿真验证，而不是完整的实机平台验收。',['README.md；teleop/panda.py；teleop/manual.py；teleop/recording.py',modelURL]);
}
// 03
{
 const s=base('控制与记录在机器人端闭环','02 / 系统架构');
 function node(label,x,y,w,accent=false){const n=s.shapes.add({geometry:'rect',name:label,position:{left:x,top:y,width:w,height:112},fill:accent?C.ink:C.pale,line:{fill:C.line,width:1}});n.text=label;n.text.style={typeface:family,fontSize:25,bold:true,color:accent?'#FFFFFF':C.ink,alignment:'center',verticalAlignment:'middle',insets:{top:12,bottom:12,left:10,right:10},autoFit:'none'};return n}
 const input=node('操作输入\n滑块 / 可选 GELLO',64,186,302);
 const mapping=node('同构映射\n零位、符号、比例',444,186,302);
 const ctrl=node('机器人端控制\n约束 + 状态机',824,186,368,true);
 const robot=node('Panda / MuJoCo\n关节、夹爪与观测',824,435,368);
 const log=node('异步记录\nJSONL → NPZ',444,435,302);
 const arr=(a,b,from,to,dashed=false)=>s.shapes.connect(a,b,{kind:'straight',fromSide:from,toSide:to,line:{fill:C.teal,width:2,style:dashed?'dashed':'solid'},tail:{type:'triangle',width:'med',length:'med'}});
 arr(input,mapping,'right','left');arr(mapping,ctrl,'right','left');arr(ctrl,robot,'bottom','top');arr(robot,log,'left','right');
 s.shapes.connect(robot,ctrl,{kind:'elbow',fromSide:'right',toSide:'right',line:{fill:C.gray,width:2,style:'dashed'},tail:{type:'triangle',width:'med',length:'med'}});
 text(s,'动作',1018,337,110,35,20,C.teal);text(s,'状态反馈',1115,361,101,31,17,C.muted);
 text(s,'本地界面：HTTP 心跳；双进程远程入口：UDP + HMAC。',64,591,1120,45,23,C.muted);
 note(s,'系统将输入、映射和机器人后端分开。映射目标先进入机器人端控制器，经过范围、速度和加速度约束，再下发给 Panda 仿真。机器人状态反馈给控制器并进入记录模块。记录在独立写盘线程中完成。浏览器心跳使用 Web Worker，避免三维绘图阻塞指令。当前界面是本机 HTTP 入口；另外保留了双进程 UDP 和 HMAC 校验链路。',['teleop/manual.py；teleop/web/control-worker.js；teleop/network.py；teleop/control.py']);
}
// 04
{
 const s=base('同构映射与运动约束分开处理','03 / 控制方法');
 text(s,'q_target = q_ref + s · g · (q_leader − o)',64,183,1138,75,36,C.teal,true);
 table(s,[['映射量','用途'],['零位 o','对齐操作端与机器人参考位置'],['方向 s','统一关节旋转方向'],['比例 g','调整关节输入的幅度']],64,287,646,270,[175,471]);
 text(s,'各项逐关节运算；当前滑块演示采用恒等映射。',64,258,1138,26,19,C.muted);
 text(s,'机器人端运动约束',770,291,420,42,27,C.ink,true);
 text(s,'关节范围检查\n速度上限 0.4 rad/s\n加速度上限 1.0 rad/s²\n目标位置减速\n使能前对齐当前位置',770,354,422,192,25,C.ink);
 text(s,'适用条件：同关节数、同拓扑、明确关节顺序；六关节与七关节直接映射会被拒绝。',64,595,1140,45,21,C.muted);
 note(s,'同构映射采用每个关节的零位、方向和比例参数。可以通过多姿态最小二乘拟合这些参数，并用独立姿态验证。浏览器输入与 Panda 使用相同七关节坐标，因此本次演示是恒等映射。映射结果并不直接执行，而是进入机器人端约束。固定目标附近另加入制动距离约束，降低参考轨迹过冲。示例速度上限为每秒零点四弧度，加速度上限为每秒平方一点零弧度。这是仿真配置，不是机械臂厂家伺服指标。',['teleop/mapping.py；teleop/control.py；configs/panda_model.json；tests/test_core.py',gelloURL]);
}
// 05
{
 const s=base('交互界面可以直接演示','04 / 操作流程');
 await photo(s,'demo-active.png',64,158,796,475);
 text(s,'01  对齐并开启跟随',899,207,316,72,27,C.teal,true);
 text(s,'02  关节与夹爪输入',899,303,316,72,27,C.ink,true);
 text(s,'03  结束并保存轨迹',899,399,316,72,27,C.ink,true);
 text(s,'演示视频约 40 秒\n包含保持、恢复与急停',899,525,315,78,22,C.muted);
 note(s,'这一页是本次实际运行的界面。先对齐当前状态并开启跟随，再拖动关节或夹爪滑块，最后结束并保存。演示视频还包含暂停发送、超时保持、重新使能和软件急停复位。视频通过脚本操作真实浏览器界面录制，用于可复现地检查流程，不是实体 GELLO 示教或人类操作效果实验。现场也可以直接手动拖动同一界面。',['defense-media/demo-active.png；panda-teleop-demo.mp4','reports/ui-checks.json；docs/MANUAL_UI.md']);
}
// 06
{
 const s=base('轨迹保留目标、下发动作与观测','05 / 运行数据');
 const d=data.native_chart;
 const chart=s.charts.add('scatter',{position:{left:64,top:182,width:801,height:402},
  series:[{name:'映射目标',xValues:d.time_s,values:d.target.map(v=>Number(v.toFixed(6))),line:{fill:C.gray,width:2,style:'dashed'},marker:{symbol:'none'}},{name:'下发动作',xValues:d.time_s,values:d.action.map(v=>Number(v.toFixed(6))),line:{fill:C.teal,width:3},marker:{symbol:'none'}},{name:'仿真观测',xValues:d.time_s,values:d.observation.map(v=>Number(v.toFixed(6))),line:{fill:'#D28B43',width:2},marker:{symbol:'none'}}],
  scatterOptions:{style:'line'},hasLegend:true,legend:{position:'bottom',overlay:false,textStyle:{fontSize:19}},
  chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF',chartLine:{fill:'none',width:0},
  xAxis:{title:'首次使能后的时间 / s',min:0,max:7,majorUnit:1,numberFormatCode:'0',majorGridlines:null,textStyle:{fontSize:18,fill:C.muted}},
  yAxis:{title:'第 1 关节 / rad',min:0,max:.65,majorUnit:.1,numberFormatCode:'0.0',majorGridlines:{fill:C.line,width:1},textStyle:{fontSize:18,fill:C.muted}}});
 applyPresentationChartFont(chart,{fontFamily:family});
 text(s,'三条轨迹各有用途',908,225,308,45,27,C.ink,true);
 text(s,'target：操作目标\naction：约束后指令\nobservation：仿真反馈',908,294,308,143,24,C.ink);
 text(s,'训练时需使用执行动作，\n保留中断区间与有效掩码。',908,483,308,91,23,C.muted);
 text(s,'本次 Panda 第 1 关节运动片段；图表数据来自保存日志，非实体机械臂精度测量。',64,608,1152,38,20,C.muted);
 note(s,'图中展示首次使能之后七秒的第一关节片段。灰色是映射目标，绿色是控制器下发动作，橙色是仿真观测。目标和执行动作分开，是因为机器人端约束会改变输入轨迹。训练数据不能把未经执行的原始目标误当成实际动作。这里的图用的是保存日志，不是实机精度证明；也没有用这些曲线宣称毫米级精度。',['manual_demo_episode/steps.jsonl；reports/manual-demo.json','图中约每 12 行抽样一次；横轴减去首次 ACTIVE 时间；图表角度显示值保留 6 位小数，原始日志不变。']);
}
// 07
{
 const s=base('超时保持需要再次人工使能','06 / 异常处理');
 const e=data.events;
 table(s,[['时刻 / s','状态','触发原因'],...e.slice(1).map(x=>[x.time_s.toFixed(3),x.mode,({armed:'人工使能',input_timeout:'发送暂停，输入超时',local_ui_estop:'本地软件急停',local_reset:'本地复位'})[x.reason]])],64,188,715,376,[160,180,375]);
 text(s,data.last_accepted_to_hold_ms.toFixed(1)+' ms',848,214,360,79,57,C.teal,true);
 text(s,'最后接受指令到 HOLD',848,306,356,70,25,C.ink);
 text(s,'旧 epoch 不会自动恢复\n复位后仍需重新使能',848,442,356,96,24,C.muted);
 text(s,'HOLD 为仿真数值冻结；上述时间不是实体机械臂的制动时间或停止距离。',64,607,1152,39,21,C.muted);
 note(s,'这次运行暂停发送后进入 HOLD。日志显示，最后接受的指令到 HOLD 约一百一十九点三毫秒。保护触发后使能 epoch 更新，旧命令不能自动恢复运动。恢复要重新对齐并使能；软件急停则锁定，必须本地复位。需要说明，这里的停止是仿真数值冻结，不代表实体机械臂真实制动时间。',['reports/manual-demo.json；manual_demo_episode/steps.jsonl','teleop/control.py；teleop/protocol.py；tests/test_core.py']);
}
// 08
{
 const s=base('示教轨迹可检验、可导出','07 / 数据结构');
 table(s,[['NPZ 字段','含义'],['observation / action','执行前状态 / 随后下发动作'],['target','原始映射目标，单独保存'],['timestamp','机器人端单调时钟相对时间'],['valid','ACTIVE 为真，其余区间保留'],['gripper_observation / action','夹爪观测与目标，归一化 0–1']],64,183,788,396,[344,444]);
 text(s,String(data.rows),913,207,298,78,63,C.teal,true);
 text(s,'行轨迹已完整保存',913,302,298,73,25,C.ink);
 text(s,String(data.active_rows)+' 行 ACTIVE\n位置矩阵 '+data.rows+' × 7\nsuccess = null',913,422,298,137,24,C.muted);
 text(s,'JSONL + 元数据 + SHA-256 + NPZ；当前是项目 schema，尚未转换为 LeRobot / RLDS。',64,605,1152,40,20,C.muted);
 note(s,'这段演示完整保存了三千四百九十五行，其中二千三百二十六行处于 ACTIVE。记录先保存观测，再保存随后执行的动作，保留原始目标和时间戳。非 ACTIVE 行不删除，而是使用 valid 掩码标记，以免中断被拼成连续轨迹。元数据记录配置和校验和。任务成功字段保留为空，因为没有实现任务成功判定。目前是项目自身的 NPZ 格式，还没有完成 LeRobot 或 RLDS 转换。',['teleop/recording.py；manual_demo_episode/metadata.json；manual_demo_episode/episode.npz']);
}
// 09
{
 const s=base('验证结果有日志和测试支撑','08 / 验证证据');
 table(s,[['检查项目','本次结果'],['单元与集成测试','29 项通过'],['浏览器交互','关节、夹爪、保持、复位与保存通过'],['记录完整性','行数、单调时间与 SHA-256 通过'],['安装包资源','独立加载 Panda 模型与心跳脚本通过']],64,183,762,365,[289,473]);
 text(s,data.actual_hz.toFixed(2)+' Hz',879,213,334,82,56,C.teal,true);
 text(s,'仿真控制平均频率',879,307,334,46,24,C.ink);
 text(s,'周期 P95  '+data.period_p95_ms.toFixed(2)+' ms\n墙钟运行  '+data.elapsed_wall_s.toFixed(2)+' s',879,411,334,107,24,C.muted);
 text(s,'频率来自本机 Python 仿真线程；不能外推为硬实时伺服、远程单向延迟或长期稳定性。',64,604,1152,46,20,C.muted);
 note(s,'验证包括二十九项单元和集成测试，覆盖映射、非法输入、有效期、状态机、数据校验和网络链路。新增的 Panda 测试检查了模型资源、关节跟随和原生夹爪。浏览器还通过真实按钮和滑块操作验证了整个采集流程。这次约三十五点三五秒的本机演示，仿真控制平均九十八点八七赫兹，周期间隔百分之九十五分位约十一点七五毫秒。这些是软件运行观测，不代表硬实时或跨地域性能。',['reports/tests-v02.txt；reports/ui-checks.json；reports/manual-demo.json；reports/RESULTS_V02.md']);
}
// 10
{
 const s=base('完成仿真阶段，保留实机接入口','09 / 结论与后续');
 text(s,'当前成果',64,193,542,50,30,C.teal,true);
 text(s,'七关节交互与 Panda 仿真闭环\n映射、运动约束与异常状态处理\n轨迹完整保存与可复现演示',64,268,550,205,28,C.ink);
 text(s,'后续验证',697,193,510,50,30,C.teal,true);
 text(s,'实体 GELLO 与厂家机器人驱动\n实机零位、工具与动力学标定\n局域网 / 跨地域网络与相机同步',697,268,515,205,28,C.ink);
 rule(s,64,523,1152);text(s,'已形成可演示、可记录、可复现的软件原型。',64,565,1148,58,31,C.ink,true);
 note(s,'本项目已经形成可演示、可记录、可复现的软件原型。主要成果是把七关节输入、同构映射、机器人端约束、仿真和数据流整合到一起。GELLO 与 Franka、UR 的适配已有公开工作，因此本项目不宣称首次适配或提出新的重定向算法。下一步需要接入真实手柄和厂家驱动，完成实机标定，再测量局域网、跨地域和相机同步性能。以上是本次实际完成的范围。',['README.md；docs/HARDWARE.md；docs/SOURCES.md',gelloURL,modelURL]);
}
await fs.writeFile(path.join(build,'speaker-notes.json'),JSON.stringify(notes,null,2));
const candidate=path.join(build,'candidate.pptx');
await(await PresentationFile.exportPptx(p)).save(candidate);
for(let i=0;i<p.slides.items.length;i++){
 const slide=p.slides.items[i];const preview=await p.export({slide,format:'png',scale:1.25});
 await fs.writeFile(path.join(build,'preview',`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await preview.arrayBuffer()));
 const layout=await slide.export({format:'layout'});await fs.writeFile(path.join(build,'preview',`slide-${i+1}.json`),await layout.text());
}
const finalPath=path.join(output,'robot-teleop-defense-ready.pptx');
const result=await finalizePresentation({workspaceDir,candidatePath:candidate,finalPath,
 pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON,
 integrityValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...([2,4,7,8,9].flatMap(n=>['--require-native-table-slide',String(n)]))],
 requiredNativeTableOwnerSlides:[2,4,7,8,9],requiredNativeChartOwnerSlides:[6],
 materializeLiteralChartWorkbooks:true,
 fontPolicy:{basis:'design',families:[family]},verifyArtifactToolImport:true,
 receiptPath:path.join(build,'validation-ready.json')});
console.log(JSON.stringify({finalPath,result}));
