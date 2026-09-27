"""Render the final verified parameter-study results; no model evaluations.
Run from the repository root: .codex-test/run python docs/write-up/aries-study-assets/render_parameters.py
"""
from pathlib import Path
import hashlib
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'exploration/costed_loop_brayton/studies/20260926-design-study-parameters-b/results/readout.json'
d = json.loads(SOURCE.read_text())
rows = d['rows']
cut = sorted([r for k,r in rows.items() if k.startswith('ir-') and r['flow']==2500 and r['ratio']<=1.45],key=lambda r:r['ratio'])
boundary = [rows[k] for k in d['arrangement_A']['boundary_cases']]
assert len(cut)==7 and len(boundary)==7
limit = rows['ir-boundary-f2500']['ratio']
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
def save(fig,name):
    fig.savefig(OUT/f'{name}.svg',bbox_inches='tight')
    fig.savefig(OUT/f'{name}.png',dpi=170,bbox_inches='tight')
    plt.close(fig)
fig,ax = plt.subplots(2,1,figsize=(9,7),sharex=True,layout='constrained')
for a in ax:
    a.axvspan(1.4245,limit,color='#fce7e5')
    a.axvline(limit,color='#666666',ls='--',lw=1)
    a.grid(alpha=.18)
    a.set_xlim(1.4245,1.4505)
good=[r for r in cut if r['passing']]
bad=[r for r in cut if not r['passing']]
ax[0].plot([r['ratio'] for r in good],[r['net'] for r in good],'-o',color='#147d92',label='Passes implemented checks')
ax[0].scatter([r['ratio'] for r in bad],[r['net'] for r in bad],marker='x',s=90,c='#bd3434',label='Fails heat removal and return condition',zorder=5)
ax[0].annotate('621 MW at the exchanger limit',xy=(limit,620.819),xytext=(1.433,623),arrowprops={'arrowstyle':'->','color':'#444'})
ax[0].set_ylim(570,640)
ax[0].set_ylabel('Net electricity (MW)')
ax[0].legend(loc='lower left',fontsize=9)
ax[0].set_title('Lowering pressure ratio raises output—until heat transfer limits it\nCycle flow fixed at 2,500 kg/s; same selected equipment',loc='left',pad=12)
ax[1].plot([r['ratio'] for r in cut],[r['unmet'] for r in cut],'-o',color='#bd3434')
ax[1].annotate('7.8 MW of heat cannot be removed',xy=(1.425,7.775),xytext=(1.432,6),arrowprops={'arrowstyle':'->','color':'#444'})
ax[1].set_ylabel('Unremoved reactor heat (MW)')
ax[1].set_xlabel('Pressure ratio per compressor stage (lower ratio ←)')
ax[1].set_ylim(-.5,9)
save(fig,'parameter-pressure-ratio')
fig,ax=plt.subplots(1,2,figsize=(11,4.7),layout='constrained')
f=[r['flow'] for r in boundary]
ax[0].plot(f,[r['ratio'] for r in boundary],'-o',color='#147d92')
ax[0].set_ylabel('Stage pressure ratio at exchanger limit')
ax[0].set_title('The limiting ratio depends on cycle flow',loc='left')
ax[1].plot(f,[r['net'] for r in boundary],'-o',color='#147d92')
ax[1].set_ylabel('Net electricity at that limit (MW)')
ax[1].set_title('More flow does not always give more output',loc='left')
for a in ax:
    a.set_xlabel('Cycle helium flow (kg/s)')
    a.grid(alpha=.18)
fig.suptitle('Verified operating points with essentially zero primary bypass',fontsize=13)
save(fig,'parameter-flow-boundary')
(OUT/'parameter-figure-data.json').write_text(json.dumps({'source':str(SOURCE.relative_to(ROOT)),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'study_id':d['study_id'],'pressure_ratio_cases':cut,'boundary_cases':boundary,'note':'Lines join stored evaluations, not additional simulated points. The near-zero-bypass boundary was located at a target fraction of 1e-6.'},indent=2)+'\n')

# Normalize generated SVG whitespace for repository diffs.
for svg in OUT.glob("parameter-*.svg"):
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
