"""Auto-generated implementation for Buildings_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:304

SysML Expressions:
    n_mod_in = 1.0
    p_fus_ref = 2300.0
    p_the_ref = 1100.0
    p_th_ref = 2500.0
    p_et_ref = 1100.0
    cost = fixed_base + fus_base * (p_fus * n_mod_in / p_fus_ref) + staff_base * (p_et_in * n_mod_in / p_et_ref) ** 0.5 + the_base * (p_the_in * n_mod_in / p_the_ref) + th_base * (p_th_in * n_mod_in / p_th_ref) + et_base * (p_et_in * n_mod_in / p_et_ref)
    
Documentation:
CAS21 buildings total, raw (pre-contingency; CAS29 applies contingency
once over the direct sum). Exact 6-term grouped collapse of the
1costingFE 18-building loop (WI-025): every building is linear in
exactly one scaling basis, so the loop groups into base-cost sums per
basis. Grouping is exact linear algebra, not a fit (design-stage proof:
bit-identical to the pinned loop at float64 at the executed powers).
p_the = p_et for a no-DEC plant (costs.py:104) -- documented where the
instance binds. Base sums are concept inputs (fuel-keyed, MR-3);
reference powers are 1cfe calibration constants.
  cost = fixed_base + fus_base*(p_fus*n_mod/p_fus_ref)
       + staff_base*(p_et*n_mod/p_et_ref)**0.5
       + the_base*(p_the*n_mod/p_the_ref)
       + th_base*(p_th*n_mod/p_th_ref) + et_base*(p_et*n_mod/p_et_ref)
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:83-144 (cas21_buildings; scale_map :121-130, refs
:102-106, SC cryogenics gate :137); costing_constants.yaml:175-197
*Basis**: exact linear grouping of the per-building loop (WI-025 D1)
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.buildings_cost import Buildings_CostInput


def run_buildings_cost(inputs: Buildings_CostInput) -> float:
    """Execute Buildings_Cost calculation.

CAS21 buildings total, raw (pre-contingency; CAS29 applies contingency
once over the direct sum). Exact 6-term grouped collapse of the
1costingFE 18-building loop (WI-025): every building is linear in
exactly one scaling basis, so the loop groups into base-cost sums per
basis. Grouping is exact linear algebra, not a fit (design-stage proof:
bit-identical to the pinned loop at float64 at the executed powers).
p_the = p_et for a no-DEC plant (costs.py:104) -- documented where the
instance binds. Base sums are concept inputs (fuel-keyed, MR-3);
reference powers are 1cfe calibration constants.
  cost = fixed_base + fus_base*(p_fus*n_mod/p_fus_ref)
       + staff_base*(p_et*n_mod/p_et_ref)**0.5
       + the_base*(p_the*n_mod/p_the_ref)
       + th_base*(p_th*n_mod/p_th_ref) + et_base*(p_et*n_mod/p_et_ref)
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:83-144 (cas21_buildings; scale_map :121-130, refs
:102-106, SC cryogenics gate :137); costing_constants.yaml:175-197
*Basis**: exact linear grouping of the per-building loop (WI-025 D1)

SysML Source: root-0/analyses/mfe_account_costs.sysml:304

SysML Expressions:
    n_mod_in = 1.0
    p_fus_ref = 2300.0
    p_the_ref = 1100.0
    p_th_ref = 2500.0
    p_et_ref = 1100.0
    cost = fixed_base + fus_base * (p_fus * n_mod_in / p_fus_ref) + staff_base * (p_et_in * n_mod_in / p_et_ref) ** 0.5 + the_base * (p_the_in * n_mod_in / p_the_ref) + th_base * (p_th_in * n_mod_in / p_th_ref) + et_base * (p_et_in * n_mod_in / p_et_ref)
    
Documentation:
CAS21 buildings total, raw (pre-contingency; CAS29 applies contingency
once over the direct sum). Exact 6-term grouped collapse of the
1costingFE 18-building loop (WI-025): every building is linear in
exactly one scaling basis, so the loop groups into base-cost sums per
basis. Grouping is exact linear algebra, not a fit (design-stage proof:
bit-identical to the pinned loop at float64 at the executed powers).
p_the = p_et for a no-DEC plant (costs.py:104) -- documented where the
instance binds. Base sums are concept inputs (fuel-keyed, MR-3);
reference powers are 1cfe calibration constants.
  cost = fixed_base + fus_base*(p_fus*n_mod/p_fus_ref)
       + staff_base*(p_et*n_mod/p_et_ref)**0.5
       + the_base*(p_the*n_mod/p_the_ref)
       + th_base*(p_th*n_mod/p_th_ref) + et_base*(p_et*n_mod/p_et_ref)
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:83-144 (cas21_buildings; scale_map :121-130, refs
:102-106, SC cryogenics gate :137); costing_constants.yaml:175-197
*Basis**: exact linear grouping of the per-building loop (WI-025 D1)

Args:
    inputs: Input parameters validated against Buildings_CostInput schema

Returns:
    float: cost

Example:
    >>> inputs = Buildings_CostInput(...)
    >>> result = run_buildings_cost(inputs)
    """
    return (((((inputs.fixed_base + (inputs.fus_base * ((inputs.p_fus * inputs.n_mod_in) / inputs.p_fus_ref))) + (inputs.staff_base * (((inputs.p_et_in * inputs.n_mod_in) / inputs.p_et_ref) ** 0.5))) + (inputs.the_base * ((inputs.p_the_in * inputs.n_mod_in) / inputs.p_the_ref))) + (inputs.th_base * ((inputs.p_th_in * inputs.n_mod_in) / inputs.p_th_ref))) + (inputs.et_base * ((inputs.p_et_in * inputs.n_mod_in) / inputs.p_et_ref)))
