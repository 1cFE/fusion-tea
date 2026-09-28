"""Plot the fixed-scenario response and its numerical allowance, not physical confidence."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

h=Path(__file__).resolve().parent
v=json.loads((h/'table-validation.json').read_text())
x=np.array([r['thickness_m'] for r in v['nodes']]); y=np.array([r['mean'] for r in v['nodes']]);se=np.array([r['std_error'] for r in v['nodes']])
grid=np.linspace(x[0],x[-1],401);mean=np.interp(grid,x,y)
i=np.clip(np.searchsorted(x,grid,side='right')-1,0,len(x)-2);f=(grid-x[i])/(x[i+1]-x[i]);spread=.01+2*np.sqrt((1-f)**2*se[i]**2+f*f*se[i+1]**2)
fig,ax=plt.subplots(figsize=(8,5))
ax.fill_between(grid,mean-spread,mean+spread,color='#cbdced',label='± (2 MC SE + 0.01 numerical allowance)')
ax.plot(x,y,'o-',color='#1b5886',label='Transport nodes / linear response')
w=v['withheld'];ax.errorbar([r['thickness_m'] for r in w],[r['mean'] for r in w],yerr=[2*r['std_error'] for r in w],fmt='x',color='#222222',capsize=3,label='Independent withheld transport, ±2 MC SE')
ax.axhline(1.190,color='#a44236',linestyle='--',label='Reference conditional fuel requirement 1.190')
ax.set(xlabel='Breeder thickness (m)',ylabel='Recoverable tritons per emitted DT neutron',title='Computed breeding: fixed toroidal single-window scenario')
ax.text(.02,.03,'70% Li-6 • uniform volume source • fixed material cards\nNumerical allowance excludes physical scenario and shape uncertainty',transform=ax.transAxes,fontsize=9)
ax.legend(loc='upper left',fontsize=8);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(h/'thickness-response.png',dpi=180)
