from pydantic import Field
from simkit.config.schema import MultiOutput

class Supplied_Auxiliary_Cooling_CostOutput(MultiOutput):
    """Multi-output container for Supplied_Auxiliary_Cooling_Cost.

WI-079 separate chosen auxiliary allowance and cryogenic package price.
aux_cost = aux_per_mw_in * thermal_class_in * n_mod_in;
cryo_cost = purchase_cost_in; cost = aux_cost + cryo_cost.
The class is thermal MW of the selected procurement scenario, never actual
rejected heat or cold-stage W. The cryo amount is dollars for the selected
package; current one-module scope preserves entering aggregation. Native
completion rejects nonfinite/negative inputs and n_mod_in other than one.
*Source**: modeling_project/REQUIREMENTS.md
*Reference**: MR-7; work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/design.md
*Basis**: reviewed selected amount plus independent budget-class allowance
*Last Updated**: 2026-09-20

SysML Source: root-0/analyses/mfe_account_costs.sysml:33
    """
    cost: float = Field(description="cost output")
    cryo_cost: float = Field(description="cryo_cost output")
    aux_cost: float = Field(description="aux_cost output")
