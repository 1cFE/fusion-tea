"""Auto-generated implementation for Structure_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:81

SysML Expressions:
    p_et_ref = 1100.0
    alpha = 0.5
    cost = unit_cost * structure_vol * (p_et / p_et_ref) ** alpha
    
Documentation:
CAS22.1.5 Primary structure (gravity supports, thermal shields,
inter-coil structure, machine base) cost. Volume x gross-electric
scaling:

  cost = unit_cost * structure_vol * (p_et/p_et_ref)^alpha

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:501 (c220105), cas22.py:224 (P_ET_REF=ref_gross_power_mwe)
*Basis**: Volume-based structure cost with gross-electric power law
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.structure_cost import Structure_CostInput


def run_structure_cost(inputs: Structure_CostInput) -> float:
    """Execute Structure_Cost calculation.

CAS22.1.5 Primary structure (gravity supports, thermal shields,
inter-coil structure, machine base) cost. Volume x gross-electric
scaling:

  cost = unit_cost * structure_vol * (p_et/p_et_ref)^alpha

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:501 (c220105), cas22.py:224 (P_ET_REF=ref_gross_power_mwe)
*Basis**: Volume-based structure cost with gross-electric power law

SysML Source: root-0/analyses/mfe_account_costs.sysml:81

SysML Expressions:
    p_et_ref = 1100.0
    alpha = 0.5
    cost = unit_cost * structure_vol * (p_et / p_et_ref) ** alpha
    
Documentation:
CAS22.1.5 Primary structure (gravity supports, thermal shields,
inter-coil structure, machine base) cost. Volume x gross-electric
scaling:

  cost = unit_cost * structure_vol * (p_et/p_et_ref)^alpha

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:501 (c220105), cas22.py:224 (P_ET_REF=ref_gross_power_mwe)
*Basis**: Volume-based structure cost with gross-electric power law

Args:
    inputs: Input parameters validated against Structure_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Structure_CostInput(...)
    >>> result = run_structure_cost(inputs)
    """
    return ((inputs.unit_cost * inputs.structure_vol) * ((inputs.p_et / inputs.p_et_ref) ** inputs.alpha))
