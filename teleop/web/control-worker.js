// The browser input heartbeat runs independently of WebGL and UI painting.
// A held target is intentional while the operator holds a slider position.
let token='', target=null, running=false, inputSeq=0;
const clientId=crypto.randomUUID();
onmessage=({data})=>{
  if(data.type==='init'){token=data.token;if(!running){running=true;tick()}}
  if(data.type==='target')target=data;
};
async function tick(){
  try{
    const state=await(await fetch('/api/control-state')).json();
    if(target?.enabled && !state.finished){
      if(['ESTOP','FAULT'].includes(state.mode)||(state.mode==='HOLD'&&target.epoch!==state.epoch)){
        target.enabled=false;postMessage({type:'disarmed',reason:state.reason});
      }else{
        const body={session:state.session,lease:state.lease,epoch:target.epoch,
          q:target.q,gripper:target.gripper,deadman:true,client_id:clientId,input_seq:inputSeq++};
        const response=await fetch('/api/command',{method:'POST',
          headers:{'Content-Type':'application/json','X-Control-Token':token},body:JSON.stringify(body)});
        const result=await response.json();
        if(!response.ok||!result.accepted){target.enabled=false;
          postMessage({type:'disarmed',reason:result.error||result.reason||'command_rejected'})}
      }
    }
    if(state.finished){running=false;return}
  }catch(error){
    if(target)target.enabled=false;
    postMessage({type:'disarmed',reason:'connection_error: '+error.message});
  }
  if(running)setTimeout(tick,30);
}
