import os,sys,math,json
from pathlib import Path
sys.path.insert(0,'/tmp/wi054-independent-audit/link')
sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from stellarator_tea.modules.mfe_plasma_sustainment.plasma_sustainment import Plasma_SustainmentInput
from stellarator_tea.handwritten.mfe_plasma_sustainment.plasma_sustainment_impl import run_plasma_sustainment
base=dict(iota_23_in=.9,Z_eff_in=1,ash_frac_in=.2002,alpha_T_in=0,kappa_sync_in=1,V=100,n_e0_in=1e20,T_i0_in=4,f_suppr_in=.5,R_in=12.7,tau_ratio_in=0,f_ren_in=1,f_W_in=1e-5,E_fus_in=2.816e-12,alpha_n_in=0,B_in=9,f_alpha_in=.95,r_TiTe_in=1,R_w_sync_in=.6,a_in=1.3)
rows=[]
# Uniform Te allows analytic integral of n0²(1-rho²)^(2a) 2rho drho = n0²/(2a+1).
for a in (0,1,2):
 em=base['n_e0_in']**2*base['V']/(2*a+1)
 expected=[5.35e-37*math.sqrt(4)*em/1e6,1e-5*5e-31*em/1e6]
 r=run_plasma_sustainment(Plasma_SustainmentInput(**{**base,'alpha_n_in':a}))
 actual=[r[4],r[13]]
 assert all(math.isclose(x,y,rel_tol=1e-8) for x,y in zip(expected,actual))
 rows.append({'alpha_n':a,'expected_MW':expected,'actual_MW':actual})
print(json.dumps(rows,indent=2))
