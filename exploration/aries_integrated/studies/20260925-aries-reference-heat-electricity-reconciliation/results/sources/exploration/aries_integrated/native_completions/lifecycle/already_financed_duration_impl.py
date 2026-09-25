"""Guard the supplied already-financed capital boundary; no second IDC."""
from aries_integrated.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def run_already_financed_duration(inputs):
    v=values(inputs)
    require(v['years']==0., 'already-financed capital requires exactly zero additional construction years')
    return finish('already_financed_duration',dict(years=0.))
