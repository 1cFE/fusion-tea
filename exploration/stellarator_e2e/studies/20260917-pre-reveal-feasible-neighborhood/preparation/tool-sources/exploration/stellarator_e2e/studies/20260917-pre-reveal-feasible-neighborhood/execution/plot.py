"""Standalone fixed-configuration map from retained native data; no model calls."""
import csv,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
H=Path(__file__).resolve().parents[1];R=H/'results';P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
selection=read(H/'preparation/refinement-selection.json');anchor=selection['anchor'];point=anchor['point'];a=read(R/'analysis.json');native={r['proposal_id']:r for r in a['cases']};aliases={r['id']:r['canonical_proposal_id'] for r in read(H/'preparation/proposals.json')};scan=read(R/'refine-oracle-scan.json')['rows'];plotrows=[r for r in scan if r['family']=='map'];data=[]
for r in plotrows:
 n=native.get(aliases.get(r['id'],r['id']));pt=r['point'];d={'proposal_id':r['id'],'R_m':pt[P+'plasma__R'],'current_MAturn':pt[P+'magnet__coil__I_coil']/1e6,'classification':'oracle-refused','native_candidate_id':'','divertor_margin_MW_m2':None,'field_margin_T':None,'auxiliary_window_margin_MW':None,'violated':';'.join(r.get('violated',[]))}
 if n:
  q=n['quantities'];m=n['signed_margins'];d.update(native_candidate_id=n['candidate_id'],classification='pass' if n['all20_satisfied'] and q['power_account_valid'] else ('invalid-account' if not q['power_account_valid'] else 'fail'),divertor_margin_MW_m2=m['divertor_heat_ok'],field_margin_T=m['peak_field_ok'],auxiliary_window_margin_MW=min(m['sustainment_ok'],m['burn_hold_ok']),violated=';'.join(n['violated']))
 else:assert r['outcome']=='refused',r['id']
 data.append(d)
with (R/'map-data.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
fig,axs=plt.subplots(2,2,figsize=(13,10));axs=axs.ravel()
styles={'pass':('#198754','o','All20 + valid account (native)'),'fail':('#c74343','o','Fails ≥1 screen (native)'),'invalid-account':('#d68b00','s','Invalid power account (native)'),'oracle-refused':('#555555','x','Oracle domain refusal (not native)')}
for c,(color,marker,label) in styles.items():
 rows=[r for r in data if r['classification']==c]
 axs[0].scatter([r['R_m'] for r in rows],[r['current_MAturn'] for r in rows],c=color,marker=marker,s=25,label=f'{label}: {len(rows)}')
axs[0].legend(loc='best',fontsize=8);axs[0].set_title('Evaluated classifications; white space is unsampled')
for ax,key,title in zip(axs[1:],['divertor_margin_MW_m2','field_margin_T','auxiliary_window_margin_MW'],['Divertor margin [MW/m²]','Peak-field margin [T]','Heating-window margin [MW]']):
 rows=[r for r in data if r[key] is not None];vals=[r[key] for r in rows];lim=max(abs(v) for v in vals) or 1
 sc=ax.scatter([r['R_m'] for r in rows],[r['current_MAturn'] for r in rows],c=vals,cmap='RdBu',norm=TwoSlopeNorm(vmin=-lim,vcenter=0,vmax=lim),s=27)
 bad=[r for r in data if r[key] is None];ax.scatter([r['R_m'] for r in bad],[r['current_MAturn'] for r in bad],c='#555',marker='x',s=25)
 fig.colorbar(sc,ax=ax,pad=.02,label='Positive = inside this limit');ax.set_title(title+'; zero is the screen')
for ax in axs:
 ax.set(xlabel='Major radius R [m]',ylabel='Coil ampere-turns [MA-turn]');ax.grid(alpha=.15)
 ax.scatter(point[P+'plasma__R'],point[P+'magnet__coil__I_coil']/1e6,marker='*',s=150,facecolors='none',edgecolors='black',linewidths=1.4,zorder=5)
 ax.scatter(12.7,15.4,marker='P',s=75,facecolors='none',edgecolors='black',zorder=5)
# Keep three margin panels focused on the sampled slice; the overview retains the projected r2 marker.
for ax in axs[1:]:
 xs=[r['R_m'] for r in data];ys=[r['current_MAturn'] for r in data];dx=(max(xs)-min(xs))*.04;dy=(max(ys)-min(ys))*.04
 ax.set_xlim(min(xs)-dx,max(xs)+dx);ax.set_ylim(min(ys)-dy,max(ys)+dy)
fig.suptitle('Stellaris-based model: fixed-configuration engineering screens',fontsize=15)
fixed=f"Fixed: a={point[P+'plasma__a']:.5g} m; peak ne={point[P+'plasma__n_e0']/1e20:.5g}×10²⁰ m⁻³; peak Ti={point[P+'plasma__T_i0']:.5g} keV; radial/cavity={point[P+'magnet__coil__coil_t']:.3g}/{point[P+'magnet__casing__interior_y']:.3g} m; loops={point[P+'heat_transport__n_loops']:g}."
fig.text(.5,.075,fixed,ha='center',fontsize=9)
fig.text(.5,.054,'Profiles0.35/1.2; current-sized inventory ×1.01; live helium loop/cycle/calendar; all material, transport and limits held.',ha='center',fontsize=9)
fig.text(.5,.033,'Star: selected anchor. Cross-box: r2 projection in overview; other inputs differ. No interpolated feasible area or hidden optimization.',ha='center',fontsize=9)
fig.text(.5,.012,'Conditional model screens only: achieved breeding, hardware qualification and full accommodation/manufacturing/cooling costs remain unresolved.',ha='center',fontsize=9)
fig.tight_layout(rect=(0,.095,1,.95));fig.savefig(R/'feasibility-map.png',dpi=180);fig.savefig(R/'feasibility-map.svg');plt.close(fig)
(R/'plot-metadata.json').write_text(json.dumps({'fixed_inputs':{k:v for k,v in point.items() if k not in [P+'plasma__R',P+'magnet__coil__I_coil']},'anchor':anchor['id'],'plot_rows':len(data),'counts':{c:sum(r['classification']==c for r in data) for c in styles},'data':'map-data.csv','no_interpolation':True,'r2_marker':'Projection only, differs from fixed slice.'},indent=2)+'\n')
print('Plot retained',len(data),'evaluated locations')
