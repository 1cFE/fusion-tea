"""Actual branch endpoints; mixed source return remains independently controlled."""
AUTO_IMPLEMENTED=False
INPUTS=dict(primary_hot=0.,primary_exchanger_return=0.,secondary_in=0.,secondary_out=0.)
OUTPUTS=['hot_gap','cold_gap']
def calculate(x):return dict(hot_gap=x['primary_hot']-x['secondary_out'],cold_gap=x['primary_exchanger_return']-x['secondary_in'])

from whole_plant_conversion_tea.modules.whole_plant_conversion_accounts.actual_exchanger_approaches import Actual_Exchanger_ApproachesInput

def _native_result(inputs):
    result=calculate({k.removesuffix('_in'):v for k,v in inputs.model_dump().items()})
    return tuple(result[k] for k in ['cold_gap', 'hot_gap'])

def run_actual_exchanger_approaches(inputs: Actual_Exchanger_ApproachesInput) -> tuple[float, float]:
    return _native_result(inputs)
