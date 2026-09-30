from pydantic import Field
from simkit.config.schema import MultiOutput

class Structure_CostOutput(MultiOutput):
    """Multi-output container for Structure_Cost.

CAS22.1.5 Primary structure (gravity supports, thermal shields,
inter-coil structure, machine base) legacy proxy. WI-059 total-support mode
reallocates residual_fraction of this proxy to an explicitly assumed
nonmagnet allowance, with no sourced allocation; legacy_cost is exposed.
Native completion requires residual_fraction in [0,1].
Volume x gross-electric
scaling:

  cost = unit_cost * structure_vol * (p_et/p_et_ref)^alpha

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:501 (c220105), cas22.py:224 (P_ET_REF=ref_gross_power_mwe)
*Basis**: Volume-based structure cost with gross-electric power law

SysML Source: root-0/analyses/mfe_account_costs.sysml:131
    """
    cost: float = Field(description="cost output")
    legacy_cost: float = Field(description="legacy_cost output")
