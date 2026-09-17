"""Structure_CostModule Module Wrapper

TEAx module for Structure_Cost calculation.

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

Inputs:
    - residual_fraction: residual_fraction parameter
    - unit_cost: unit_cost parameter
    - p_et_in: p_et_in parameter
    - alpha: alpha parameter
    - structure_vol: structure_vol parameter
    - p_et_ref: p_et_ref parameter

Outputs:
    - cost: cost result
    - legacy_cost: legacy_cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:81

SysML Source: root-0/analyses/mfe_account_costs.sysml:81

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/structure_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.structure_cost_output import Structure_CostOutput


class Structure_CostInput(BaseModel):
    """Input model for Structure_CostModule.

    Attributes:
        residual_fraction: residual_fraction input
        unit_cost: unit_cost input
        p_et_in: p_et_in input
        alpha: alpha input
        structure_vol: structure_vol input
        p_et_ref: p_et_ref input
    """
    residual_fraction: float = Field(..., description="residual_fraction input")
    unit_cost: float = Field(..., description="unit_cost input")
    p_et_in: float = Field(..., description="p_et_in input")
    alpha: float = Field(..., description="alpha input")
    structure_vol: float = Field(..., description="structure_vol input")
    p_et_ref: float = Field(..., description="p_et_ref input")


class Structure_CostModule(ModuleBase[Structure_CostInput, Structure_CostOutput]):
    """TEAx module for Structure_Cost calculation.

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

Inputs:
    - residual_fraction: residual_fraction parameter
    - unit_cost: unit_cost parameter
    - p_et_in: p_et_in parameter
    - alpha: alpha parameter
    - structure_vol: structure_vol parameter
    - p_et_ref: p_et_ref parameter

Outputs:
    - cost: cost result
    - legacy_cost: legacy_cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:81

    SysML Source: root-0/analyses/mfe_account_costs.sysml:81

    Calculation Specification:
        residual_fraction = 1.0
        p_et_ref = 1100.0
        alpha = 0.5
        legacy_cost = unit_cost * structure_vol * (p_et_in / p_et_ref) ** alpha
        cost = residual_fraction * legacy_cost
        
Documentation:
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.structure_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts cost, legacy_cost fields to separate channels.
    """

    name: str = "Structure_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, residual_fraction: float, unit_cost: float, p_et_in: float, alpha: float, structure_vol: float, p_et_ref: float    ) -> Structure_CostInput:
        """Validate inputs and fill defaults.

        Args:
            residual_fraction: residual_fraction input
            unit_cost: unit_cost input
            p_et_in: p_et_in input
            alpha: alpha input
            structure_vol: structure_vol input
            p_et_ref: p_et_ref input

        Returns:
            Validated input model
        """
        return Structure_CostInput(residual_fraction=residual_fraction, unit_cost=unit_cost, p_et_in=p_et_in, alpha=alpha, structure_vol=structure_vol, p_et_ref=p_et_ref)

    def run(
        self, residual_fraction: float, unit_cost: float, p_et_in: float, alpha: float, structure_vol: float, p_et_ref: float    ) -> ModuleResult[Structure_CostOutput]:
        """Execute calculation.

        Args:
            residual_fraction: residual_fraction input
            unit_cost: unit_cost input
            p_et_in: p_et_in input
            alpha: alpha input
            structure_vol: structure_vol input
            p_et_ref: p_et_ref input

        Returns:
            Module result with Structure_CostOutput (cost, legacy_cost)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(residual_fraction, unit_cost, p_et_in, alpha, structure_vol, p_et_ref)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.structure_cost_impl import (
            run_structure_cost,
        )

        # Execute implementation - returns tuple of values
        cost, legacy_cost = run_structure_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Structure_CostOutput(
                cost=cost,
                legacy_cost=legacy_cost,
            )
        )
