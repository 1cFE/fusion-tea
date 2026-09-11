"""Reactor_Source_HeatModule Module Wrapper

TEAx module for Reactor_Source_Heat calculation.

The reactor's heat with no pump credit (WI-045, goal plant-closure):
  q_source = mn * p_neutron + p_alpha + p_input
the first three terms of 'MFE Power Balance Calc''s thermal sum in the
same order, published as its own producer so the primary loop can size
its flow from it without a dependency cycle (the power balance consumes
the loop's recovered heat). The alpha/neutron split is the inlined D-T
ratio 3.52/17.58 exactly as the power balance forms it, so q_source
equals the power balance's own partial sum to the bit.
*Source**: models/library/analyses/mfe_power_balance.sysml ('MFE Power Balance Calc', p_th)
*Ref**: WI-019 collapse p_th = mn*p_neutron + p_alpha + p_input + (recovered pump heat)
*Basis**: reactor source heat before the loop's own recovered work; the heat ledger's one source (packet § 5)

Inputs:
    - p_input_in: p_input_in parameter
    - p_nrl: p_nrl parameter
    - mn_in: mn_in parameter

Outputs:
    - q_source: q_source result

SysML Source: root-0/analyses/mfe_power_balance.sysml:171

SysML Source: root-0/analyses/mfe_power_balance.sysml:171

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_power_balance/reactor_source_heat_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Reactor_Source_HeatInput(BaseModel):
    """Input model for Reactor_Source_HeatModule.

    Attributes:
        p_input_in: p_input_in input
        p_nrl: p_nrl input
        mn_in: mn_in input
    """
    p_input_in: float = Field(..., description="p_input_in input")
    p_nrl: float = Field(..., description="p_nrl input")
    mn_in: float = Field(..., description="mn_in input")


class Reactor_Source_HeatModule(ModuleBase[Reactor_Source_HeatInput, Float]):
    """TEAx module for Reactor_Source_Heat calculation.

The reactor's heat with no pump credit (WI-045, goal plant-closure):
  q_source = mn * p_neutron + p_alpha + p_input
the first three terms of 'MFE Power Balance Calc''s thermal sum in the
same order, published as its own producer so the primary loop can size
its flow from it without a dependency cycle (the power balance consumes
the loop's recovered heat). The alpha/neutron split is the inlined D-T
ratio 3.52/17.58 exactly as the power balance forms it, so q_source
equals the power balance's own partial sum to the bit.
*Source**: models/library/analyses/mfe_power_balance.sysml ('MFE Power Balance Calc', p_th)
*Ref**: WI-019 collapse p_th = mn*p_neutron + p_alpha + p_input + (recovered pump heat)
*Basis**: reactor source heat before the loop's own recovered work; the heat ledger's one source (packet § 5)

Inputs:
    - p_input_in: p_input_in parameter
    - p_nrl: p_nrl parameter
    - mn_in: mn_in parameter

Outputs:
    - q_source: q_source result

SysML Source: root-0/analyses/mfe_power_balance.sysml:171

    SysML Source: root-0/analyses/mfe_power_balance.sysml:171

    Calculation Specification:
        p_alpha = 3.52 / 17.58 * p_nrl
        p_neutron = p_nrl - p_alpha
        q_source = mn_in * p_neutron + p_alpha + p_input_in
        
Documentation:
The reactor's heat with no pump credit (WI-045, goal plant-closure):
  q_source = mn * p_neutron + p_alpha + p_input
the first three terms of 'MFE Power Balance Calc''s thermal sum in the
same order, published as its own producer so the primary loop can size
its flow from it without a dependency cycle (the power balance consumes
the loop's recovered heat). The alpha/neutron split is the inlined D-T
ratio 3.52/17.58 exactly as the power balance forms it, so q_source
equals the power balance's own partial sum to the bit.
*Source**: models/library/analyses/mfe_power_balance.sysml ('MFE Power Balance Calc', p_th)
*Ref**: WI-019 collapse p_th = mn*p_neutron + p_alpha + p_input + (recovered pump heat)
*Basis**: reactor source heat before the loop's own recovered work; the heat ledger's one source (packet § 5)

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_power_balance.reactor_source_heat_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Reactor_Source_HeatModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_input_in: float, p_nrl: float, mn_in: float    ) -> Reactor_Source_HeatInput:
        """Validate inputs and fill defaults.

        Args:
            p_input_in: p_input_in input
            p_nrl: p_nrl input
            mn_in: mn_in input

        Returns:
            Validated input model
        """
        return Reactor_Source_HeatInput(p_input_in=p_input_in, p_nrl=p_nrl, mn_in=mn_in)

    def run(
        self, p_input_in: float, p_nrl: float, mn_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            p_input_in: p_input_in input
            p_nrl: p_nrl input
            mn_in: mn_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_input_in, p_nrl, mn_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_power_balance.reactor_source_heat_impl import (
            run_reactor_source_heat,
        )

        # Execute implementation - returns single value
        q_source = run_reactor_source_heat(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(q_source))
