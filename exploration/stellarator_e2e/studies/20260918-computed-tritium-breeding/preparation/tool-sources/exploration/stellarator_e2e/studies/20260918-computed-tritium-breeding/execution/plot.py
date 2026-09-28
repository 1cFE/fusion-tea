"""Plot retained generated-package results without model evaluation."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H=Path(__file__).resolve().parents[1]
r=[x for x in json.loads((H/'results/interpreted-cases.json').read_text()) if x['breeding_defined']]
x=[a['thickness_m'] for a in r]
fig,axes=plt.subplots(2,1,figsize=(8,7),sharex=True,layout='constrained')
fig.set_layout_engine('constrained',rect=(0,.045,1,.955))
axes[0].plot(x,[a['tbr_mean'] for a in r],'o-',label='Mean TBR')
axes[0].plot(x,[a['tbr_lower'] for a in r],'s-',label='Numerical lower estimate')
axes[0].axhline(r[0]['required_tbr'],color='black',ls='--',label='Conditional requirement 1.190')
axes[0].set(ylabel='Tritium per source neutron',title='Conditional breeding response and represented cost')
axes[0].legend(loc='lower right',fontsize=9)
axes[1].plot(x,[a['blanket_cost_dollars']/1e6 for a in r],'o-',color='tab:purple',label='CAS22 blanket aggregate')
axes[1].set(xlabel='Breeder thickness (m)',ylabel='Blanket cost ($ million)')
axes[1].axvspan(.825,1,color='tab:red',alpha=.08,label='Sampled peak-field violations')
axes[1].legend(fontsize=9)
for a in axes:a.grid(alpha=.25)
fig.text(.5,.008,'Fixed 70% Li-6, declared 3% toroidal window; all sampled cases fail other plant screens.',ha='center',fontsize=8)
fig.savefig(H/'results/response-and-cost.png',dpi=170)
fig.savefig(H/'results/response-and-cost.pdf')
