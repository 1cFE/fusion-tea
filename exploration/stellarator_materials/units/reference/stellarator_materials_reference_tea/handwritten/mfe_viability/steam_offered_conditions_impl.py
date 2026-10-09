"""WI080 finite point-state comparison; no implied envelope or machine map."""
from __future__ import annotations
import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_materials_reference_tea.modules.mfe_viability.steam_offered_conditions import Steam_Offered_ConditionsInput
AUTO_IMPLEMENTED = False
FIELDS = ['actual_main_pressure_MPa', 'rated_main_pressure_MPa', 'actual_extraction_pressure_MPa', 'rated_extraction_pressure_MPa', 'actual_steam_C', 'rated_steam_C', 'actual_reheat_C', 'rated_reheat_C', 'actual_condenser_C', 'rated_condenser_C', 'actual_salt_hot_C', 'rated_salt_hot_C', 'actual_salt_return_C', 'rated_salt_return_C', 'actual_salt_cp', 'rated_salt_cp']
PAIRS = ['main_pressure_MPa', 'extraction_pressure_MPa', 'steam_C', 'reheat_C', 'condenser_C', 'salt_hot_C', 'salt_return_C', 'salt_cp']
def same_state(a, b):
    # Reviewed binary representation identity; never a physical operating envelope.
    return math.isfinite(a) and math.isfinite(b) and (
        a == b or abs(a-b) <= 8 * max(math.ulp(a), math.ulp(b)))
def calculate(x):
    if not isinstance(x['enabled'], bool):
        raise ValueError('enabled must be Boolean')
    if not x['enabled']:
        return dict(applicable=False, supported=False, evaluation_defined=0.0)
    for key in FIELDS:
        if isinstance(x[key], bool) or not math.isfinite(x[key]):
            raise ValueError(key + ' must be finite numeric')
    supported = all(same_state(x['actual_'+key], x['rated_'+key]) for key in PAIRS)
    return dict(applicable=True, supported=supported, evaluation_defined=1.0 if supported else 0.0)
def run_steam_offered_conditions(inputs: Steam_Offered_ConditionsInput) -> tuple[float, float, float]:
    result = calculate({'enabled': inputs.enabled_in, **{key: getattr(inputs, key+'_in') for key in FIELDS}})
    from stellarator_materials_reference_tea.schemas.steam_offered_conditions_output import Steam_Offered_ConditionsOutput
    return tuple(result[name] for name in Steam_Offered_ConditionsOutput.model_fields)
