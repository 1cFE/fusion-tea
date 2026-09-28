"""Retain numerical residuals from the shipped sealed package, without regeneration."""
from pathlib import Path
import json
from decimal import Decimal, localcontext
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
from tests.models.test_ife_zero_discount_repair import CASES, POINTS, BOUNDARIES, PREFIX, assert_finance, assert_eligibility
from tests.ife_oracle import decimal_present_value_reference
root=Path(__file__).resolve().parent
package=Path('exploration/ife_e2e/generated').resolve()
ev=PreparedEvaluator(ProvisionalPackageLoader(package,'ife_tea',root/'measurement-link'),package/'pipelines/pipeline.yaml',expects_constraint_report=True)
bridge=CandidateBridge(ev.entry_models)
cases=[(name, POINTS[name]|dict(construction_duration=yc,operational_duration=no,discount_rate=rate)) for name,yc,no,rate in CASES]
cases += [('positive_neighbor',BOUNDARIES['positive_neighbor']|dict(discount_rate=rate)) for rate in (0.,1e-12,-1e-12,.08)]
rows=[]
for name,overrides in cases:
 result=ev.evaluate(bridge.build({PREFIX+k:v for k,v in overrides.items()}))
 assert_finance(result,overrides);assert_eligibility(result,name in ('baseline','positive_neighbor'))
 reference,kind=decimal_present_value_reference(overrides)
 values={key:result.outputs[PREFIX+'lcoe_calc__'+key] for key in ('discounted_cost','discounted_energy')}
 values.update({key:result.outputs[PREFIX+'pv_factors__'+key] for key in ('construction_factor','operation_factor')})
 values['price']=result.outputs[PREFIX+'hawker_price__price']
 with localcontext() as context:
  context.prec=80
  errors={key:float(abs(Decimal.from_float(value)-reference[key])/(abs(reference[key]) if reference[key] else 1)) for key,value in values.items()}
 rows.append(dict(scenario=name,inputs=overrides,actual=values,reference={k:str(v) for k,v in reference.items()},reference_kind=kind,relative_or_zero_absolute_errors=errors,responses=dict(result.responses)))
(root/'channel-results.json').write_text(json.dumps(rows,indent=2)+'\n')
print(len(rows),'cases; max strict residual',max(max(row['relative_or_zero_absolute_errors'].values()) for row in rows))
