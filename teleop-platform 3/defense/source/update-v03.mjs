import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
const work='/workspace/scratch/4a2d12871e46/audit-v03/deck';
const source='/workspace/scratch/4a2d12871e46/audit-v03/work/teleop-platform/defense/robot-teleop-defense.pptx';
const skill='/root/.codex/skills/builtins/presentations';
process.env.RUNTIME_NODE=process.env.CODEX_PRIMARY_RUNTIME_NODE;
process.env.RUNTIME_NODE_MODULES=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
process.env.RUNTIME_PYTHON=process.env.CODEX_PRIMARY_RUNTIME_PYTHON;
process.env.RUNTIME_BIN_DIR=process.env.CODEX_PRIMARY_RUNTIME+'/dependencies/bin/override';
const {finalizePresentation}=await import(pathToFileURL(skill+'/container_tools/artifact_tool_utils.mjs'));
const p=await PresentationFile.importPptx(await FileBlob.load(source));
const records=(await p.inspect({kind:'textbox,table,notes',maxChars:250000})).ndjson.split('\n').filter(Boolean).map(x=>JSON.parse(x));
for(const row of records){
  if(row.kind==='textbox' && row.text==='机器人遥操作框架 · Panda 仿真验证'){
    const text=row.slideIndex>=4&&row.slideIndex<=8
      ? '软件 v0.3 · 图像、轨迹与频率来自 v0.2 演示'
      : '机器人遥操作框架 · 软件 v0.3 · Panda 仿真验证';
    p.resolve(row.id).text.replace(row.text,text);
  }
  if(row.kind==='textbox'&&row.slideIndex===8&&row.text==='仿真控制平均频率'){
    p.resolve(row.id).text.replace(row.text,'v0.2 演示平均频率');
  }
  if(row.kind==='table'&&row.slideIndex===8){
    const table=p.resolve(row.id);
    table.cells.set(0,1,'v0.3 软件验收');
    table.cells.set(1,1,'41 项通过，0 跳过');
    table.cells.set(2,1,'正常操作及导出失败提示通过');
    table.cells.set(3,1,'配置校验与 NPZ 一致性通过');
  }
  if(row.kind==='notes'){
    let text=row.text;
    if(row.slideIndex===8){
      text='v0.3 在 Linux 环境严格执行 41 项测试，全部通过且无跳过。新增检查覆盖旧使能标记、网页重放、多页面控制、配置修改、NPZ 不一致和导出失败。真实浏览器正常流程、保存失败提示、独立 wheel 加载和一键启动自动报告均通过。右侧 99.26 Hz、11.76 ms 和 35.43 s 来自 v0.2 历史演示，不是这次新软件的性能对照，也不是硬实时或跨地域结果。\n\n来源：reports/AUDIT_V03.md；reports/v03/tests/tests.json；reports/v03/browser-check.json；reports/v03/wheel-check.json；reports/manual-demo.json。';
    }else if(row.slideIndex>=4&&row.slideIndex<=7){
      text='版本说明：本页截图、视频和数值保留自 v0.2 演示；软件在 v0.3 已增加错误处理和自动验收，没有把历史数据重新标为新实验。\n\n'+text;
    }
    p.resolve(row.id).setText(text);
  }
}
await fs.writeFile(work+'/build/updated-inspect.ndjson',(await p.inspect({kind:'slide,textbox,table,notes',maxChars:250000})).ndjson);
const candidate=work+'/build/candidate-v03.pptx';
await(await PresentationFile.exportPptx(p)).save(candidate);
// Preserve original chart OOXML/workbook verbatim: this import/export version
// drops its embedded workbook relationship. No chart data are regenerated.
const repaired=work+'/build/candidate-v03-preserved.pptx';
execFileSync(process.env.CODEX_PRIMARY_RUNTIME_PYTHON,[work+'/build/restore_chart.py',source,candidate,repaired],{stdio:'inherit'});
const result=await finalizePresentation({workspaceDir:work,candidatePath:repaired,finalPath:work+'/output/robot-teleop-defense-v03.pptx',
  pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON,
  integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',
  layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...[2,4,7,8,9].flatMap(x=>['--require-native-table-slide',String(x)])],
  requiredNativeTableOwnerSlides:[2,4,7,8,9],requiredNativeChartOwnerSlides:[6],
  requiredEmbeddedWorkbookChartOwnerSlides:[6],
  fontPolicy:{basis:'reference',families:['Noto Sans CJK SC'],referencePath:source,referenceSha256:crypto.createHash('sha256').update(await fs.readFile(source)).digest('hex')},
  verifyArtifactToolImport:true,receiptPath:work+'/build/validation-v03.json'});
console.log(JSON.stringify({finalPath:result.finalPath,sha256:result.finalSha256}));
const final=await PresentationFile.importPptx(await FileBlob.load(result.finalPath));
for(let i=0;i<final.slides.items.length;i++){
  const im=await final.export({slide:final.slides.items[i],format:'png',scale:1});
  await fs.writeFile(work+`/build/final-${i+1}.png`,new Uint8Array(await im.arrayBuffer()));
}
