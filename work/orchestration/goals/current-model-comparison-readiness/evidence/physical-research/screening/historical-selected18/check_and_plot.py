"""Independent quadrature and original-data correspondence checks; research evidence."""
from pathlib import Path
import importlib.util,contextlib,io,csv,json,math,hashlib
p=Path(__file__).parent
spec=importlib.util.spec_from_file_location('screen',p/'calculate.py');m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(m)
checks={}
for key,f in [('1K','nist-original-1K.tsv'),('0.5K','nist-original-halfK.tsv')]:
 raw=list(csv.reader((p/f).read_text().splitlines(),delimiter='\t'))[1:];parser=m.Rows();parser.feed(m.sources[key][0].read_text());assert raw==parser.rows
 checks[key+'_all14columns_exact']=len(raw)
rows=m.sources['0.5K'][1]
checks['cases']=[]
def simpson(fun,n):return (fun(0)+fun(1)+sum((4 if j%2 else 2)*fun(j/n) for j in range(1,n)))/(3*n)
for case in m.results['0.5K']:
 pts=[r for r in rows if r['T']<=case['steam_C']];h0=pts[0]['h'];h3=pts[-1]['h'];k=m.SPAN/(h3-h0);mdot=case['steam_flow_kg_s'];ua=0.;ds=0.;slopes=[]
 for a,b in zip(pts,pts[1:]):
  dh=b['h']-a['h'];dt=b['T']-a['T'];g0=m.T_COLD+k*(a['h']-h0)-a['T'];g1=m.T_COLD+k*(b['h']-h0)-b['T']
  n=2048 if a['phase']!=b['phase'] else 32
  ua+=mdot/1000*dh*simpson(lambda x:1/(g0+x*(g1-g0)),n)
  ds+=dh*simpson(lambda x:1/(a['T']+273.15+x*dt),n)
  if dt:slopes.append(k-dt/dh)
 assert all(s<0 for s in slopes)
 assert case['energy_residual_MW']==0
 assert abs(ua/case['UA_total_MW_K']-1)<1e-8
 assert abs(ds-(pts[-1]['s']-pts[0]['s']))<1e-5
 assert case['conditional_cycle_MW']<case['water_exergy_gain_MW']<case['salt_heat_exergy_MW']
 checks['cases'].append(dict(approach=case['hot_approach_K'],quadrature_UA_relative_error=ua/case['UA_total_MW_K']-1,entropy_integral_error_kJkgK=ds-(pts[-1]['s']-pts[0]['s']),nonboiling_gap_slopes_min_max=[min(slopes),max(slopes)],cycle_to_water_exergy_ratio=case['conditional_cycle_MW']/case['water_exergy_gain_MW']))
assert [c['thermal_20K_screen_satisfied'] for c in m.results['0.5K']]==[False,True,True]
checks['criterion_failures_retained']=['10Khot fails20Kminimum']
try:m.section([{'T':500.,'h':0.,'cp':1.},{'T':510.,'h':1.,'cp':1.}],0,1,1)
except ValueError as e:checks['nonpositive_gap_guard']=str(e)
else:raise AssertionError('negative gap accepted')
(p/'verification.json').write_text(json.dumps(checks,indent=2)+'\n')
# Standalone plots of evidence, not a UI or canonical model output.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axs=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
for case in m.results['0.5K']:
 pts=[r for r in rows if r['T']<=case['steam_C']];h0=pts[0]['h'];h3=pts[-1]['h'];x=[(r['h']-h0)/(h3-h0) for r in pts];water=[r['T'] for r in pts];salt=[m.T_COLD+m.SPAN*q for q in x]
 if case['hot_approach_K']==20:
  axs[0].plot(x,salt,label='HITEC (465°C → 269.665°C)',color='#bd5b1a');axs[0].plot(x,water,label='Water / steam (6.2 MPa)',color='#2166a5')
  for idx in [len([r for r in pts if r['phase']=='liquid'])-1,len([r for r in pts if r['phase']=='liquid'])]:axs[0].axvline(x[idx],color='gray',alpha=.35,ls=':')
  axs[0].set_title('445°C steam: finite heat admission')
 axs[1].plot(x,[s-w for s,w in zip(salt,water)],label=f'{case["hot_approach_K"]} K hot end → {case["steam_C"]:.0f}°C steam')
axs[1].axhline(20,color='black',ls='--',lw=1,label='Proposed 20 K minimum');axs[1].set_title('All local temperature differences')
for ax in axs:ax.set_xlabel('Cumulative fraction of heat added to water');ax.grid(alpha=.2);ax.legend(fontsize=8)
axs[0].set_ylabel('Temperature (°C)');axs[1].set_ylabel('Salt minus water temperature (K)')
fig.suptitle('Screening assumptions: countercurrent, constant salt cp, fixed steam pressure; no installed-capacity claim',fontsize=10)
fig.savefig(p/'admission-profile.png',dpi=180);fig.savefig(p/'admission-profile.svg');plt.close(fig)
paths=[p/'calculate.py',p/'check_and_plot.py',p/'results.json',p/'verification.json',p/'water-properties-halfK.csv',p/'nist-original-1K.tsv',p/'nist-original-halfK.tsv']
(p/'manifest.json').write_text(json.dumps({str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths},indent=2)+'\n')
print(json.dumps(checks,indent=2))
