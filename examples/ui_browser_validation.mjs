// Optional developer check; beginners do not need Node/Playwright.
import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES
  ? process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright' : 'playwright');
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output=process.env.TELEOP_UI_OUTPUT || path.join(root,'runs','ui-check-'+Date.now());
await fs.mkdir(output,{recursive:true});
const python=process.env.TELEOP_PYTHON || 'python';
let browser;
const checks={scope:'Automated real browser interactions; no human study or physical hardware',scenarios:[]};

async function scenario(name,injectFailure=false){
  const dir=path.join(output,name);await fs.mkdir(dir);
  const server=spawn(python,['-u','-m','teleop','ui','--output',path.join(dir,'episode'),'--port','0'],
    {cwd:root,stdio:['ignore','pipe','pipe']});
  let logs='',page;
  server.stderr.on('data',d=>logs+=d.toString());
  try{
    const url=await new Promise((resolve,reject)=>{
      const timer=setTimeout(()=>reject(Error('server start timeout: '+logs)),30000);
      server.stdout.on('data',d=>{logs+=d.toString();const match=logs.match(/http:\/\/127\.0\.0\.1:\d+/);
        if(match){clearTimeout(timer);resolve(match[0])}});
      server.on('error',e=>{clearTimeout(timer);reject(e)});
      server.on('exit',c=>{clearTimeout(timer);reject(Error('server exited '+c+': '+logs))});
    });
    page=await browser.newPage({viewport:{width:1500,height:1000}});
    const errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto(url);
    await page.waitForFunction(()=>window.teleopView?.isModelReady(),{timeout:30000});
    const result={name,modelLoaded:true,pageErrors:errors};
    if(injectFailure){
      // Exclusive export must refuse this file; UI must show failure, not success.
      await fs.writeFile(path.join(dir,'episode','episode.npz'),'sentinel-do-not-overwrite');
    }else{
      const unauthorized=await page.request.post(url+'/api/action',{data:{action:'estop'}});
      if(unauthorized.status()!==400)throw Error('Missing control token was accepted');
      result.unauthorizedRejected=true;
      await page.locator('#enable').click();
      await page.waitForFunction(()=>window.teleopView.getState().mode==='ACTIVE');
      await page.locator('#joint-0').focus();
      for(let i=0;i<60;i++)await page.keyboard.press('ArrowRight');
      await page.waitForFunction(()=>{const s=window.teleopView.getState();return s.mode==='ACTIVE'&&s.q[0]>.24});
      await page.locator('#gripper').focus();
      for(let i=0;i<85;i++)await page.keyboard.press('ArrowRight');
      await page.waitForFunction(()=>window.teleopView.getState().gripper>.72);
      await page.screenshot({path:path.join(dir,'active.png')});
      result.motionAndGripper=true;
      await page.locator('#pause').click();
      await page.waitForFunction(()=>window.teleopView.getState().mode==='HOLD');
      await page.locator('#pause').click();
      await page.locator('#enable').click();
      await page.waitForFunction(()=>window.teleopView.getState().mode==='ACTIVE');
      result.holdAndExplicitRearm=true;
      await page.locator('#estop').click();
      await page.waitForFunction(()=>window.teleopView.getState().mode==='ESTOP');
      await page.locator('#reset').click();
      await page.waitForFunction(()=>window.teleopView.getState().mode==='DISARMED');
      result.estopAndReset=true;
    }
    await page.locator('#finish').click();
    await page.waitForFunction(()=>window.teleopView.getState().finalized);
    const state=await page.evaluate(()=>window.teleopView.getState());
    const banner=await page.locator('#saved').innerText();
    if(injectFailure){
      if(state.summary?.complete!==false || !banner.includes('未全部完成'))throw Error('Failure was presented as success');
      if(await fs.readFile(path.join(dir,'episode','episode.npz'),'utf8')!=='sentinel-do-not-overwrite')throw Error('Existing file overwritten');
      result.exportFailureShown=true;
    }else if(state.summary?.complete!==true || !banner.includes('完整保存')){
      throw Error('Recording not complete: '+JSON.stringify(state.summary));
    }else result.completeExport=true;
    await page.screenshot({path:path.join(dir,'saved.png')});
    if(errors.length)throw Error('Browser errors: '+errors.join('; '));
    result.passed=true;checks.scenarios.push(result);
  }finally{
    if(page)await page.close();
    if(server.exitCode===null){
      const exited=new Promise(resolve=>server.once('exit',resolve));
      server.kill('SIGINT');
      const timer=setTimeout(()=>server.kill('SIGKILL'),12000);
      await exited;clearTimeout(timer);
    }
    await fs.writeFile(path.join(dir,'server.log'),logs);
  }
}
try{
  browser=await chromium.launch({executablePath:process.env.TELEOP_CHROME||undefined,headless:true,
    args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage']});
  await scenario('normal');
  await scenario('export-failure',true);
  checks.passed=checks.scenarios.length===2;
}catch(error){checks.passed=false;checks.error=String(error);process.exitCode=1}
finally{
  if(browser)await browser.close();
  await fs.writeFile(path.join(output,'browser-check.json'),JSON.stringify(checks,null,2));
  console.log(JSON.stringify({output,...checks},null,2));
}
