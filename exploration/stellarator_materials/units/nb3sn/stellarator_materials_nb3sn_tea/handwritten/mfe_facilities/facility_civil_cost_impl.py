from __future__ import annotations
"""WI-068 six installed-direct civil products; source2018/CPI2025 basis."""
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_materials_nb3sn_tea.modules.mfe_facilities.facility_civil_cost import Facility_Civil_CostInput
AUTO_IMPLEMENTED = False

def calculate(inputs):
    x=dict(inputs);out=dict(sub_cost_2018=0.,super_cost_2018=0.,cost_2018=0.,cost_2025=0.)
    if not isinstance(x['enabled'],bool):raise ValueError('enabled must be Boolean')
    if not x['enabled']:return out
    if any(isinstance(v,bool) or not math.isfinite(v) or v<0 for k,v in x.items() if k!='enabled'):raise ValueError('civil quantities/rates must be finite nonnegative')
    if x['tonne_interpretation_kg']<=0:raise ValueError('positive tonne conversion required')
    for group in ('sub','super'):
        out[group+'_cost_2018']=sum(x[group+'_'+q]*x[group+'_'+q+'_rate']*(907.18474/x['tonne_interpretation_kg'] if q=='rebar' else 1) for q in ('concrete','formwork','rebar'))*x['civil_rate_multiplier']
    out['cost_2018']=out['sub_cost_2018']+out['super_cost_2018'];out['cost_2025']=out['cost_2018']*x['civil_cpi_ratio']
    if not all(math.isfinite(v) for v in out.values()):raise ValueError('civil cost overflow')
    return out


def run_facility_civil_cost(inputs: Facility_Civil_CostInput) -> tuple[float, float, float, float]:
    x = {name.removesuffix("_in"): getattr(inputs,name) for name in ['sub_formwork_rate_in', 'civil_rate_multiplier_in', 'super_rebar_rate_in', 'sub_formwork_in', 'super_rebar_in', 'super_concrete_rate_in', 'super_concrete_in', 'super_formwork_rate_in', 'sub_concrete_rate_in', 'super_formwork_in', 'enabled_in', 'sub_rebar_rate_in', 'sub_concrete_in', 'civil_cpi_ratio_in', 'tonne_interpretation_kg_in', 'sub_rebar_in']}
    out = calculate(x)
    return tuple(out[name] for name in ['sub_cost_2018', 'super_cost_2018', 'cost_2025', 'cost_2018'])
