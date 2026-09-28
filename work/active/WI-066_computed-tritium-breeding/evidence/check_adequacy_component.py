"""Conservation and refusal checks against the native generated input schema."""
import importlib.util
import json
import math
import os
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'exploration/stellarator_e2e/pkg'))
sys.path.insert(0,str(Path(os.environ['STOP_PARSER_TEAX_ROOT'])/'packages/teax-simkit'))
from stellarator_tea.modules.mfe_tritium_breeding.tritium_breeding_adequacy import Tritium_Breeding_AdequacyInput
# Keep the declared seed filename exact.
spec = importlib.util.spec_from_file_location('wi066_adequacy', HERE.parent/'seeds/tritium_breeding_adequacy_impl.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
base = dict(tbr_mean_in=1.2,tbr_lower_in=1.195,defined_in=1.,tbr_floor_in=1.05,
            tbr_required_in=1.19,burn_rate_in=100.,loss_rate_in=19.,eta_extract_in=1.,
            lambda_T_in=0.,I_total_in=0.,G_stock_in=0.,burn_fraction_in=.05,t_recycle_in=.99)
fields = ('design_margin','decay_rate','fuel_margin','extracted_supply_rate','recycle_loss_rate','defined_flag','required_tbr','balance_rate','extraction_loss_rate','stock_growth_rate','numerical_margin','production_rate')
def run(**changes):
    return dict(zip(fields,m.run_tritium_breeding_adequacy(Tritium_Breeding_AdequacyInput(**(base|changes)))))
checks = {}
r=run(); assert r['defined_flag']==1 and r['production_rate']==120 and r['balance_rate']==1 and r['numerical_margin']>0
checks['base_balance']=r
r=run(eta_extract_in=.95,tbr_required_in=119/95); assert r['defined_flag']==1 and r['balance_rate']==-5 and math.isclose(r['extraction_loss_rate'],6)
checks['extraction_separate']=r
r=run(lambda_T_in=.01,I_total_in=100.,G_stock_in=2.,tbr_required_in=1.22); assert r['decay_rate']==1 and r['stock_growth_rate']==2 and r['balance_rate']==-2
checks['inventory_and_growth_separate']=r
for name,value in [('eta_extract_in',0),('burn_fraction_in',0),('t_recycle_in',1.1),('tbr_floor_in',0),('tbr_required_in',0),('loss_rate_in',18),('tbr_mean_in',float('nan')),('tbr_lower_in',1.3),('defined_in',2)]:
    r=run(**{name:value}); assert r['defined_flag']==0,(name,r)
checks['invalid_cases']=9
r=run(defined_in=0);assert r['defined_flag']==0 and r['production_rate']==0 and r['required_tbr']==1.19
checks['undefined_carrier']=r
(HERE/'adequacy-component-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('PASS conservation, independent streams, undefined carrier and 9 malformed inputs')
