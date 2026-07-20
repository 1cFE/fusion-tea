"""Buildings_CostModule Module Wrapper

TEAx module for Buildings_Cost calculation.

CAS21 buildings total, raw (pre-contingency; CAS29 applies contingency
once over the direct sum). Exact 6-term grouped collapse of the
1costingFE 18-building loop (WI-025): every building is linear in
exactly one scaling basis, so the loop groups into base-cost sums per
basis. Grouping is exact linear algebra, not a fit (design-stage proof:
bit-identical to the pinned loop at float64 at the executed powers).
p_the = p_et for a no-DEC plant (costs.py:104) — documented where the
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

Inputs:
    - fixed_base: fixed_base parameter
    - fus_base: fus_base parameter
    - staff_base: staff_base parameter
    - the_base: the_base parameter
    - th_base: th_base parameter
    - et_base: et_base parameter
    - p_fus: p_fus parameter
    - p_the: p_the parameter
    - p_th: p_th parameter
    - p_et: p_et parameter
    - n_mod: n_mod parameter
    - p_fus_ref: p_fus_ref parameter
    - p_the_ref: p_the_ref parameter
    - p_th_ref: p_th_ref parameter
    - p_et_ref: p_et_ref parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:304

SysML Source: root-0/analyses/mfe_account_costs.sysml:304

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/buildings_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Buildings_CostInput(BaseModel):
    """Input model for Buildings_CostModule.

    Attributes:
        fixed_base: fixed_base input
        fus_base: fus_base input
        staff_base: staff_base input
        the_base: the_base input
        th_base: th_base input
        et_base: et_base input
        p_fus: p_fus input
        p_the: p_the input
        p_th: p_th input
        p_et: p_et input
        n_mod: n_mod input
        p_fus_ref: p_fus_ref input
        p_the_ref: p_the_ref input
        p_th_ref: p_th_ref input
        p_et_ref: p_et_ref input
    """
    fixed_base: float = Field(..., description="fixed_base input")
    fus_base: float = Field(..., description="fus_base input")
    staff_base: float = Field(..., description="staff_base input")
    the_base: float = Field(..., description="the_base input")
    th_base: float = Field(..., description="th_base input")
    et_base: float = Field(..., description="et_base input")
    p_fus: float = Field(..., description="p_fus input")
    p_the: float = Field(..., description="p_the input")
    p_th: float = Field(..., description="p_th input")
    p_et: float = Field(..., description="p_et input")
    n_mod: float = Field(..., description="n_mod input")
    p_fus_ref: float = Field(..., description="p_fus_ref input")
    p_the_ref: float = Field(..., description="p_the_ref input")
    p_th_ref: float = Field(..., description="p_th_ref input")
    p_et_ref: float = Field(..., description="p_et_ref input")


class Buildings_CostModule(ModuleBase[Buildings_CostInput, Float]):
    """TEAx module for Buildings_Cost calculation.

CAS21 buildings total, raw (pre-contingency; CAS29 applies contingency
once over the direct sum). Exact 6-term grouped collapse of the
1costingFE 18-building loop (WI-025): every building is linear in
exactly one scaling basis, so the loop groups into base-cost sums per
basis. Grouping is exact linear algebra, not a fit (design-stage proof:
bit-identical to the pinned loop at float64 at the executed powers).
p_the = p_et for a no-DEC plant (costs.py:104) — documented where the
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

Inputs:
    - fixed_base: fixed_base parameter
    - fus_base: fus_base parameter
    - staff_base: staff_base parameter
    - the_base: the_base parameter
    - th_base: th_base parameter
    - et_base: et_base parameter
    - p_fus: p_fus parameter
    - p_the: p_the parameter
    - p_th: p_th parameter
    - p_et: p_et parameter
    - n_mod: n_mod parameter
    - p_fus_ref: p_fus_ref parameter
    - p_the_ref: p_the_ref parameter
    - p_th_ref: p_th_ref parameter
    - p_et_ref: p_et_ref parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:304

    SysML Source: root-0/analyses/mfe_account_costs.sysml:304

    Calculation Specification:
        n_mod = 1.0
        p_fus_ref = 2300.0
        p_the_ref = 1100.0
        p_th_ref = 2500.0
        p_et_ref = 1100.0
        cost = fixed_base + fus_base * (p_fus * n_mod / p_fus_ref) + staff_base * (p_et * n_mod / p_et_ref) ** 0.5 + the_base * (p_the * n_mod / p_the_ref) + th_base * (p_th * n_mod / p_th_ref) + et_base * (p_et * n_mod / p_et_ref)
        
Documentation:
CAS21 buildings total, raw (pre-contingency; CAS29 applies contingency
once over the direct sum). Exact 6-term grouped collapse of the
1costingFE 18-building loop (WI-025): every building is linear in
exactly one scaling basis, so the loop groups into base-cost sums per
basis. Grouping is exact linear algebra, not a fit (design-stage proof:
bit-identical to the pinned loop at float64 at the executed powers).
p_the = p_et for a no-DEC plant (costs.py:104) — documented where the
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.buildings_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Buildings_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, fixed_base: float, fus_base: float, staff_base: float, the_base: float, th_base: float, et_base: float, p_fus: float, p_the: float, p_th: float, p_et: float, n_mod: float, p_fus_ref: float, p_the_ref: float, p_th_ref: float, p_et_ref: float    ) -> Buildings_CostInput:
        """Validate inputs and fill defaults.

        Args:
            fixed_base: fixed_base input
            fus_base: fus_base input
            staff_base: staff_base input
            the_base: the_base input
            th_base: th_base input
            et_base: et_base input
            p_fus: p_fus input
            p_the: p_the input
            p_th: p_th input
            p_et: p_et input
            n_mod: n_mod input
            p_fus_ref: p_fus_ref input
            p_the_ref: p_the_ref input
            p_th_ref: p_th_ref input
            p_et_ref: p_et_ref input

        Returns:
            Validated input model
        """
        return Buildings_CostInput(fixed_base=fixed_base, fus_base=fus_base, staff_base=staff_base, the_base=the_base, th_base=th_base, et_base=et_base, p_fus=p_fus, p_the=p_the, p_th=p_th, p_et=p_et, n_mod=n_mod, p_fus_ref=p_fus_ref, p_the_ref=p_the_ref, p_th_ref=p_th_ref, p_et_ref=p_et_ref)

    def run(
        self, fixed_base: float, fus_base: float, staff_base: float, the_base: float, th_base: float, et_base: float, p_fus: float, p_the: float, p_th: float, p_et: float, n_mod: float, p_fus_ref: float, p_the_ref: float, p_th_ref: float, p_et_ref: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            fixed_base: fixed_base input
            fus_base: fus_base input
            staff_base: staff_base input
            the_base: the_base input
            th_base: th_base input
            et_base: et_base input
            p_fus: p_fus input
            p_the: p_the input
            p_th: p_th input
            p_et: p_et input
            n_mod: n_mod input
            p_fus_ref: p_fus_ref input
            p_the_ref: p_the_ref input
            p_th_ref: p_th_ref input
            p_et_ref: p_et_ref input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(fixed_base, fus_base, staff_base, the_base, th_base, et_base, p_fus, p_the, p_th, p_et, n_mod, p_fus_ref, p_the_ref, p_th_ref, p_et_ref)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.buildings_cost_impl import (
            run_buildings_cost,
        )

        # Execute implementation - returns single value
        cost = run_buildings_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
