"""Independent analytic radiation examples, then supported manual-stage comparison."""
import json
import math
import os
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'link'))
sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from stellarator_tea.modules.mfe_plasma_sustainment.plasma_sustainment import Plasma_SustainmentInput
from stellarator_tea.handwritten.mfe_plasma_sustainment.plasma_sustainment_impl import run_plasma_sustainment
base=dict(iota_23_in=.9,Z_eff_in=1,ash_frac_in=.2002,alpha_T_in=0,kappa_sync_in=1,V=100,n_e0_in=1e20,T_i0_in=4,f_suppr_in=.5,R_in=12.7,tau_ratio_in=0,f_ren_in=1,f_W_in=1e-5,E_fus_in=2.816e-12,alpha_n_in=0,B_in=9,f_alpha_in=.95,r_TiTe_in=1,R_w_sync_in=.6,a_in=1.3)
rows=[]
# Analytic emission measure for n=n0*(1-rho^2)^a:
# Substitute u=1-rho^2, du=-2rho drho, so integral n^2 dV/V = n0^2/(2a+1).
# At constant Te=4keV the adopted tungsten curve is exactly its 5e-31 W m^3 plateau.
for exponent in (0.,1.):
    expected_brems=1.07/(2*exponent+1)
    expected_line=5./(2*exponent+1)
    out=run_plasma_sustainment(Plasma_SustainmentInput(**{**base,'alpha_n_in':exponent}))
    actual={'brems_MW':out[4],'line_MW':out[13]}
    for found,expected in [(out[4],expected_brems),(out[13],expected_line)]:assert math.isclose(found,expected,rel_tol=1e-8), (found,expected)
    rows.append({'alpha_n':exponent,'analytic_MW':{'brems':expected_brems,'line':expected_line},'native':actual})
(HERE/'dimensional-example.json').write_text(json.dumps({'basis':'analytic volume integral; coefficient dimensions independent of native code; 1e-8 relative allows N=200000 trapezoid rounding','cases':rows},indent=2)+'\n')
print(rows)
