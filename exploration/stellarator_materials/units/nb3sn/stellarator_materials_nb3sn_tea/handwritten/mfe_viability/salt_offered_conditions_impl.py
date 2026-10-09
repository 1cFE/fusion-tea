"""WI080 finite point-state comparison; no implied envelope or machine map."""
from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_materials_nb3sn_tea.modules.mfe_viability.salt_offered_conditions import Salt_Offered_ConditionsInput
AUTO_IMPLEMENTED = False
FIELDS = ['actual_hot_C', 'rated_hot_C', 'actual_return_C', 'rated_return_C', 'actual_cp', 'rated_cp']
PAIRS = ['hot_C', 'return_C', 'cp']
def same_state(a, b):
    # Reviewed binary representation identity; never a physical operating envelope.
    return math.isfinite(a) and math.isfinite(b) and (
        a == b or abs(a-b) <= 8 * max(math.ulp(a), math.ulp(b)))
def calculate(x):
    if not isinstance(x['enabled'], bool):
        raise ValueError('enabled must be Boolean')
    if isinstance(x['mode'],bool) or x['mode'] not in (0.0,1.0):
        raise ValueError('mode must be exactly zero or one')
    if not x['enabled'] or x['mode'] == 0.0:
        return dict(applicable=False, supported=False, evaluation_defined=0.0)
    for key in FIELDS:
        if isinstance(x[key], bool) or not math.isfinite(x[key]):
            raise ValueError(key + ' must be finite numeric')
    supported = all(same_state(x['actual_'+key], x['rated_'+key]) for key in PAIRS)
    return dict(applicable=True, supported=supported, evaluation_defined=1.0 if supported else 0.0)
def run_salt_offered_conditions(inputs: Salt_Offered_ConditionsInput) -> tuple[float, float, float]:
    result = calculate({'enabled': inputs.enabled_in, 'mode': inputs.mode_in, **{key: getattr(inputs, key+'_in') for key in FIELDS}})
    from stellarator_materials_nb3sn_tea.schemas.salt_offered_conditions_output import Salt_Offered_ConditionsOutput
    return tuple(result[name] for name in Salt_Offered_ConditionsOutput.model_fields)
