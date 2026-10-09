"""WI-067 finite binary scenario guard; prevents selecting a disabled zero ledger."""
import math
from stellarator_materials_nb3sn_tea.modules.mfe_cooling_accounts.cooling_scenario_guard import Cooling_Scenario_GuardInput

AUTO_IMPLEMENTED = False


def run_cooling_scenario_guard(inputs: Cooling_Scenario_GuardInput) -> tuple[float, float]:
    for value in (inputs.cost_mode_in, inputs.energy_mode_in):
        if not math.isfinite(value) or value not in (0., 1.):
            raise ValueError('Cooling Scenario Guard: modes must be finite and binary')
    if (inputs.cost_mode_in or inputs.energy_mode_in) and not inputs.equipment_enabled_in:
        raise ValueError('Cooling Scenario Guard: selected effects require enabled equipment')
    return inputs.energy_mode_in, inputs.cost_mode_in
