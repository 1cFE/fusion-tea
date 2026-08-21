"""Vessel_CostModule Module Wrapper

TEAx module for Vessel_Cost calculation.

CAS22.1.6 Vacuum-vessel SHELL cost (double-walled SS chamber, port
extensions, gauges, leak detection). Volume x gross-electric scaling:

  cost = unit_cost * vessel_vol * (p_et/p_et_ref)^alpha

Reproduces only the volume-based vessel-shell sub-term (c220106_vessel).
The gas-load pumping sub-term (c220106_pump) is a within-envelope but
input-heavy expression (Boltzmann/charge constants, fuel-keyed E_fus,
NBI/fueling throughput); it is omitted here and left for Stage-3
deepening. See the plant doc's initial-model-limitations note.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:515 (c220106_vessel), cas22.py:224 (P_ET_REF)
*Basis**: Volume-based vessel-shell cost with gross-electric power law

Inputs:
    - p_et_in: p_et_in parameter
    - alpha: alpha parameter
    - vessel_vol: vessel_vol parameter
    - p_et_ref: p_et_ref parameter
    - unit_cost: unit_cost parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:108

SysML Source: root-0/analyses/mfe_account_costs.sysml:108

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/vessel_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Vessel_CostInput(BaseModel):
    """Input model for Vessel_CostModule.

    Attributes:
        p_et_in: p_et_in input
        alpha: alpha input
        vessel_vol: vessel_vol input
        p_et_ref: p_et_ref input
        unit_cost: unit_cost input
    """
    p_et_in: float = Field(..., description="p_et_in input")
    alpha: float = Field(..., description="alpha input")
    vessel_vol: float = Field(..., description="vessel_vol input")
    p_et_ref: float = Field(..., description="p_et_ref input")
    unit_cost: float = Field(..., description="unit_cost input")


class Vessel_CostModule(ModuleBase[Vessel_CostInput, Float]):
    """TEAx module for Vessel_Cost calculation.

CAS22.1.6 Vacuum-vessel SHELL cost (double-walled SS chamber, port
extensions, gauges, leak detection). Volume x gross-electric scaling:

  cost = unit_cost * vessel_vol * (p_et/p_et_ref)^alpha

Reproduces only the volume-based vessel-shell sub-term (c220106_vessel).
The gas-load pumping sub-term (c220106_pump) is a within-envelope but
input-heavy expression (Boltzmann/charge constants, fuel-keyed E_fus,
NBI/fueling throughput); it is omitted here and left for Stage-3
deepening. See the plant doc's initial-model-limitations note.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:515 (c220106_vessel), cas22.py:224 (P_ET_REF)
*Basis**: Volume-based vessel-shell cost with gross-electric power law

Inputs:
    - p_et_in: p_et_in parameter
    - alpha: alpha parameter
    - vessel_vol: vessel_vol parameter
    - p_et_ref: p_et_ref parameter
    - unit_cost: unit_cost parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:108

    SysML Source: root-0/analyses/mfe_account_costs.sysml:108

    Calculation Specification:
        p_et_ref = 1100.0
        alpha = 0.6
        cost = unit_cost * vessel_vol * (p_et_in / p_et_ref) ** alpha
        
Documentation:
CAS22.1.6 Vacuum-vessel SHELL cost (double-walled SS chamber, port
extensions, gauges, leak detection). Volume x gross-electric scaling:

  cost = unit_cost * vessel_vol * (p_et/p_et_ref)^alpha

Reproduces only the volume-based vessel-shell sub-term (c220106_vessel).
The gas-load pumping sub-term (c220106_pump) is a within-envelope but
input-heavy expression (Boltzmann/charge constants, fuel-keyed E_fus,
NBI/fueling throughput); it is omitted here and left for Stage-3
deepening. See the plant doc's initial-model-limitations note.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:515 (c220106_vessel), cas22.py:224 (P_ET_REF)
*Basis**: Volume-based vessel-shell cost with gross-electric power law

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.vessel_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Vessel_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_et_in: float, alpha: float, vessel_vol: float, p_et_ref: float, unit_cost: float    ) -> Vessel_CostInput:
        """Validate inputs and fill defaults.

        Args:
            p_et_in: p_et_in input
            alpha: alpha input
            vessel_vol: vessel_vol input
            p_et_ref: p_et_ref input
            unit_cost: unit_cost input

        Returns:
            Validated input model
        """
        return Vessel_CostInput(p_et_in=p_et_in, alpha=alpha, vessel_vol=vessel_vol, p_et_ref=p_et_ref, unit_cost=unit_cost)

    def run(
        self, p_et_in: float, alpha: float, vessel_vol: float, p_et_ref: float, unit_cost: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            p_et_in: p_et_in input
            alpha: alpha input
            vessel_vol: vessel_vol input
            p_et_ref: p_et_ref input
            unit_cost: unit_cost input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_et_in, alpha, vessel_vol, p_et_ref, unit_cost)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.vessel_cost_impl import (
            run_vessel_cost,
        )

        # Execute implementation - returns single value
        cost = run_vessel_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
