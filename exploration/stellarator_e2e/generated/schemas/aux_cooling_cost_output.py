from pydantic import Field
from simkit.config.schema import MultiOutput

class Aux_Cooling_CostOutput(MultiOutput):
    """Multi-output container for Aux_Cooling_Cost.

Auxiliary cooling + cryoplant account:

  cost = aux_per_mw * (n_mod * p_th) + cryo_base * (p_cryo / p_cryo_ref) ** alpha

aux term linear in plant-total thermal; cryoplant power-law in
per-module cryo electric power (NOT scaled by n_mod -- each module has
its own cryoplant).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py (pin 0254385)
*Ref**: cas22.py:693-695 (c220300); p_cryo_ref 30 (:694), alpha 0.7 (:694)
*Basis**: Plant-total aux + per-module cryoplant power law

SysML Source: root-0/analyses/mfe_account_costs.sysml:559
    """
    aux_cost: float = Field(description="aux_cost output")
    cryo_cost: float = Field(description="cryo_cost output")
    cost: float = Field(description="cost output")
