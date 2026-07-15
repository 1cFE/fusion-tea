"""Indirect_CostModule Module Wrapper

TEAx module for Indirect_Cost calculation.

CAS30 indirect service costs, a fraction of total direct cost scaled by
construction time relative to a reference duration:

  cost = indirect_fraction * direct_cost
(construction_time / reference_construction_time)

`indirect_fraction` (0.20 of direct in the source) is a concept input.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:231-236 (cas30_indirect)
*Basis**: Direct-cost fraction scaled by construction-time ratio

Inputs:
    - indirect_fraction: indirect_fraction parameter
    - direct_cost: direct_cost parameter
    - construction_time: construction_time parameter
    - reference_construction_time: reference_construction_time parameter

Outputs:
    - cost: cost result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:276

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:276

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/indirect_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Indirect_CostInput(BaseModel):
    """Input model for Indirect_CostModule.

    Attributes:
        indirect_fraction: indirect_fraction input
        direct_cost: direct_cost input
        construction_time: construction_time input
        reference_construction_time: reference_construction_time input
    """
    indirect_fraction: float = Field(..., description="indirect_fraction input")
    direct_cost: float = Field(..., description="direct_cost input")
    construction_time: float = Field(..., description="construction_time input")
    reference_construction_time: float = Field(..., description="reference_construction_time input")


class Indirect_CostModule(ModuleBase[Indirect_CostInput, Float]):
    """TEAx module for Indirect_Cost calculation.

CAS30 indirect service costs, a fraction of total direct cost scaled by
construction time relative to a reference duration:

  cost = indirect_fraction * direct_cost
(construction_time / reference_construction_time)

`indirect_fraction` (0.20 of direct in the source) is a concept input.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:231-236 (cas30_indirect)
*Basis**: Direct-cost fraction scaled by construction-time ratio

Inputs:
    - indirect_fraction: indirect_fraction parameter
    - direct_cost: direct_cost parameter
    - construction_time: construction_time parameter
    - reference_construction_time: reference_construction_time parameter

Outputs:
    - cost: cost result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:276

    SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:276

    Calculation Specification:
        reference_construction_time = 6.0
        cost = indirect_fraction * direct_cost * (construction_time / reference_construction_time)
        
Documentation:
CAS30 indirect service costs, a fraction of total direct cost scaled by
construction time relative to a reference duration:

  cost = indirect_fraction * direct_cost
(construction_time / reference_construction_time)

`indirect_fraction` (0.20 of direct in the source) is a concept input.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:231-236 (cas30_indirect)
*Basis**: Direct-cost fraction scaled by construction-time ratio

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.indirect_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Indirect_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, indirect_fraction: float, direct_cost: float, construction_time: float, reference_construction_time: float    ) -> Indirect_CostInput:
        """Validate inputs and fill defaults.

        Args:
            indirect_fraction: indirect_fraction input
            direct_cost: direct_cost input
            construction_time: construction_time input
            reference_construction_time: reference_construction_time input

        Returns:
            Validated input model
        """
        return Indirect_CostInput(indirect_fraction=indirect_fraction, direct_cost=direct_cost, construction_time=construction_time, reference_construction_time=reference_construction_time)

    def run(
        self, indirect_fraction: float, direct_cost: float, construction_time: float, reference_construction_time: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            indirect_fraction: indirect_fraction input
            direct_cost: direct_cost input
            construction_time: construction_time input
            reference_construction_time: reference_construction_time input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(indirect_fraction, direct_cost, construction_time, reference_construction_time)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.indirect_cost_impl import (
            run_indirect_cost,
        )

        # Execute implementation - returns single value
        cost = run_indirect_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
