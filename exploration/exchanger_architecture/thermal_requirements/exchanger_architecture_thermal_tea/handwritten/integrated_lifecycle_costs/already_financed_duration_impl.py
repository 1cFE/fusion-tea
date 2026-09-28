"""Guard the supplied already-financed capital boundary; no second IDC."""
from exchanger_architecture_thermal_tea.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def _reviewed_run_already_financed_duration(inputs):
    v=values(inputs)
    require(v['years']==0., 'already-financed capital requires exactly zero additional construction years')
    return finish('already_financed_duration',dict(years=0.))


from exchanger_architecture_thermal_tea.modules.integrated_lifecycle_costs.already_financed_duration import Already_Financed_DurationInput


def run_already_financed_duration(inputs: Already_Financed_DurationInput) -> float:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_already_financed_duration(inputs)
