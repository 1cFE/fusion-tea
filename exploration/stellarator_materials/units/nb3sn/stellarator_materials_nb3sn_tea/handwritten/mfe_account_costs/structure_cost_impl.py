"""WI-059 primary-structure residual allowance with preserved legacy proxy."""
from stellarator_materials_nb3sn_tea.modules.mfe_account_costs.structure_cost import Structure_CostInput

AUTO_IMPLEMENTED = False


def run_structure_cost(inputs: Structure_CostInput) -> tuple[float, float]:
    if not 0.0 <= inputs.residual_fraction <= 1.0:
        raise ValueError("Structure Cost: residual fraction must be in [0, 1]")
    legacy = inputs.unit_cost * inputs.structure_vol * (inputs.p_et_in/inputs.p_et_ref)**inputs.alpha
    return inputs.residual_fraction * legacy, legacy
