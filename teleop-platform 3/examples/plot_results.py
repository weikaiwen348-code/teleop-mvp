"""Optional publication-style evidence plot; requires matplotlib."""
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    p=argparse.ArgumentParser(); p.add_argument('--run-dir',required=True); p.add_argument('--output',required=True)
    a=p.parse_args(); root=Path(a.run_dir)
    report=json.loads((root/'validation.json').read_text())
    rows=[json.loads(s) for s in (root/'blackout'/'steps.jsonl').read_text().splitlines()]
    t=np.array([r['t_robot_s'] for r in rows]); active=np.array([r['mode']=='ACTIVE' for r in rows])
    fig,axes=plt.subplots(3,1,figsize=(10,8),gridspec_kw={'height_ratios':[2,1,1.5]},layout='constrained')
    fig.patch.set_facecolor('#f8fafc')
    for ax in axes:
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y',alpha=.18)
    for key,label,color in [('target.q','Latest target','#64748b'),('action.q','Limited action','#2563eb'),('observation.q','Observation before action','#059669')]:
        axes[0].plot(t,[r[key][0] for r in rows],label=label,color=color,lw=1.8)
    axes[0].axvline(3,color='#dc2626',ls='--',label='Input cut at 3.0 s')
    axes[0].set(ylabel='Joint 1 (rad)',title='Synthetic blackout experiment | toy joint plant, 100 Hz')
    axes[0].legend(fontsize=9,loc='lower center',ncols=2)
    axes[1].step(t,active,where='post',color='#2563eb')
    axes[1].set(yticks=[0,1],yticklabels=['HOLD / disarmed','ACTIVE'],ylim=(-.1,1.2),xlabel='Simulation time (s)')
    axes[1].axvline(3,color='#dc2626',ls='--')
    axes[1].annotate('HOLD at 3.10 s\n100 ms after input cut',xy=(3.1,0),xytext=(3.5,.55),arrowprops={'arrowstyle':'->','color':'#334155'})
    names=['baseline','delay_loss','mujoco']
    values=[report['results'][n]['previous_action_vs_observation_rmse_rad']*1000 for n in names]
    axes[2].barh(['Toy / no delay','Toy / 20 ms + jitter + loss','Generic MuJoCo chain'],values,color=['#94a3b8','#2563eb','#059669'])
    for i,v in enumerate(values): axes[2].text(v+.15,i,f'{v:.2f}',va='center')
    axes[2].set(xlabel='Observation vs previous action RMSE (mrad)',xlim=(0,max(values)*1.25))
    fig.suptitle('Software validation only — not Franka/UR hardware performance',fontsize=14,fontweight='bold')
    fig.savefig(a.output,dpi=160)


if __name__=='__main__': main()
