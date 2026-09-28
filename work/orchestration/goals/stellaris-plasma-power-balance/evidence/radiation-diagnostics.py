"""Two independently reviewed frozen-state source-law alternatives, not a model patch."""
import hashlib,json,math,sys
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[4];sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e'))
import verify_stellaris as vs
inv=json.loads((D/'model-accounting/inventory.json').read_text());row=next(r for r in inv['cases'] if r['case']=='table5-conditioned-legacy');t=row['terms']
R=12.74;a=1.3;V=425.;B=9.;alphaT=1.2;alphaN=.35;Te0=t['T_e0'];Ti0=14.63
Teavg=Te0/(1+alphaT);neavg=t['n_e_volav']/1e20
# Algebraically regular form of original equation after dividing by V.
def q(te,ne20):return 1.32e-7*B**2.5*math.sqrt(ne20/a)*(te**2.5+(18*a/R)*te**2)
global_power=V*q(Teavg,neavg)
sigpeak=vs._sigv_dt(Ti0)
def local(n):
 acc=0.
 for i in range(n+1):
  rho=i/n;u=1-rho*rho
  te=Te0*u**alphaT;shape=u**(2*alphaN)*vs._sigv_dt(Ti0*u**alphaT)/sigpeak
  ne=2*t['n_D0']*u**alphaN+2*t['n_He0']*shape
  f=q(te,ne/1e20)*2*rho
  acc+=(.5 if i in (0,n) else 1)*f
 return V*acc/n
p200=local(200000);p400=local(400000)
assert math.isclose(p200,p400,rel_tol=1e-8,abs_tol=0)
base=t['p_sync'];aux=t['p_aux_required'];cases=[]
for name,value,scope in [('zohm-global-averages',global_power,'Original volume-average temperature; density mapped to model volume average as explicit assumption; tokamak-to-stellarator transfer.'),('stellaris-local-profile-interpretation',p200,'Sensitivity-only local adaptation of a global correlation; not confirmed source implementation.')]:
 cases.append({'case':name,'synchrotron_MW':value,'delta_aux_MW':value-base,'frozen_aux_MW':aux+value-base,'scope':scope})
out={'scope':'Two frozen-state accounting alternatives; no new native model, coupled solution or downstream plant prediction.','source_review_sha256':hashlib.sha256((D/'synchrotron-math-review.md').read_bytes()).hexdigest(),'geometry':{'R_m':R,'a_m':a,'volume_m3':V,'B_T':B},'temperature_average_keV':Teavg,'density_average_1e20_m3':neavg,'source_reflectivity_implicit':.8,'model_reflectivity':.6,'model_synchrotron_MW':base,'model_aux_MW':aux,'cases':cases,'quadrature':{'intervals':200000,'finer_intervals':400000,'local_200000_MW':p200,'local_400000_MW':p400,'relative_difference':abs(p200-p400)/p400,'relative_check':1e-8},'nonnegative_synchrotron_lower_bound_aux_MW':aux-base,'lower_bound_scope':'Frozen all-other-terms arithmetic bound, not a physical zero-radiation operating point.','interpretation':'Differences combine correlation, reflectivity and averaging assumptions. Neither removes auxiliary demand; production replacement is not established.'}
(D/'radiation-diagnostics.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
