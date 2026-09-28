"""Preconstruction_CostModule Module Wrapper

TEAx module for Preconstruction_Cost calculation.

CAS10 preconstruction PRE-CONTINGENCY subtotal: land (sqrt of
plant-total net electric, anchored at ref_net_power) plus the fixed
adders (permits + licensing + studies + reports + other -- fuel- and
FOAK/NOAK-keyed, so a concept input). costs.py:79 adds CAS10's own
contingency; deliberately NOT carried here -- the plant's CAS29 applies
contingency once over the direct sum (convention preserved, MR-WI025-3).
WI-029 doc correction: the old note "1cfe full CAS10 = this subtotal
x 1.10 exactly" was a stale FOAK reading. At NOAK -- the regime both the
design and handshake points run -- contingency_rate_noak = 0.0, so 1cfe's
full CAS10 equals this subtotal exactly. No number changes; the model
applies no CAS10 contingency and that was already NOAK-correct.
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:52-80 (cas10_preconstruction);
costing_constants.yaml:8, :15-23
*Basis**: CAS10 subtotal, contingency deliberately omitted (CAS29)

Inputs:
    - land_cost: land_cost parameter
    - n_mod_in: n_mod_in parameter
    - fixed_precon: fixed_precon parameter
    - ref_net_power: ref_net_power parameter
    - land_intensity: land_intensity parameter
    - p_net: p_net parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:366

SysML Source: root-0/analyses/mfe_account_costs.sysml:366

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/preconstruction_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Preconstruction_CostInput(BaseModel):
    """Input model for Preconstruction_CostModule.

    Attributes:
        land_cost: land_cost input
        n_mod_in: n_mod_in input
        fixed_precon: fixed_precon input
        ref_net_power: ref_net_power input
        land_intensity: land_intensity input
        p_net: p_net input
    """
    land_cost: float = Field(..., description="land_cost input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    fixed_precon: float = Field(..., description="fixed_precon input")
    ref_net_power: float = Field(..., description="ref_net_power input")
    land_intensity: float = Field(..., description="land_intensity input")
    p_net: float = Field(..., description="p_net input")


class Preconstruction_CostModule(ModuleBase[Preconstruction_CostInput, Float]):
    """TEAx module for Preconstruction_Cost calculation.

CAS10 preconstruction PRE-CONTINGENCY subtotal: land (sqrt of
plant-total net electric, anchored at ref_net_power) plus the fixed
adders (permits + licensing + studies + reports + other -- fuel- and
FOAK/NOAK-keyed, so a concept input). costs.py:79 adds CAS10's own
contingency; deliberately NOT carried here -- the plant's CAS29 applies
contingency once over the direct sum (convention preserved, MR-WI025-3).
WI-029 doc correction: the old note "1cfe full CAS10 = this subtotal
x 1.10 exactly" was a stale FOAK reading. At NOAK -- the regime both the
design and handshake points run -- contingency_rate_noak = 0.0, so 1cfe's
full CAS10 equals this subtotal exactly. No number changes; the model
applies no CAS10 contingency and that was already NOAK-correct.
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:52-80 (cas10_preconstruction);
costing_constants.yaml:8, :15-23
*Basis**: CAS10 subtotal, contingency deliberately omitted (CAS29)

Inputs:
    - land_cost: land_cost parameter
    - n_mod_in: n_mod_in parameter
    - fixed_precon: fixed_precon parameter
    - ref_net_power: ref_net_power parameter
    - land_intensity: land_intensity parameter
    - p_net: p_net parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:366

    SysML Source: root-0/analyses/mfe_account_costs.sysml:366

    Calculation Specification:
        n_mod_in = 1.0
        land_intensity = 0.25
        land_cost = 10000.0
        ref_net_power = 1000.0
        cost = land_intensity * (p_net * n_mod_in * ref_net_power) ** 0.5 * land_cost + fixed_precon
        
Documentation:
CAS10 preconstruction PRE-CONTINGENCY subtotal: land (sqrt of
plant-total net electric, anchored at ref_net_power) plus the fixed
adders (permits + licensing + studies + reports + other -- fuel- and
FOAK/NOAK-keyed, so a concept input). costs.py:79 adds CAS10's own
contingency; deliberately NOT carried here -- the plant's CAS29 applies
contingency once over the direct sum (convention preserved, MR-WI025-3).
WI-029 doc correction: the old note "1cfe full CAS10 = this subtotal
x 1.10 exactly" was a stale FOAK reading. At NOAK -- the regime both the
design and handshake points run -- contingency_rate_noak = 0.0, so 1cfe's
full CAS10 equals this subtotal exactly. No number changes; the model
applies no CAS10 contingency and that was already NOAK-correct.
*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py
*Ref**: costs.py:52-80 (cas10_preconstruction);
costing_constants.yaml:8, :15-23
*Basis**: CAS10 subtotal, contingency deliberately omitted (CAS29)

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.preconstruction_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Preconstruction_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, land_cost: float, n_mod_in: float, fixed_precon: float, ref_net_power: float, land_intensity: float, p_net: float    ) -> Preconstruction_CostInput:
        """Validate inputs and fill defaults.

        Args:
            land_cost: land_cost input
            n_mod_in: n_mod_in input
            fixed_precon: fixed_precon input
            ref_net_power: ref_net_power input
            land_intensity: land_intensity input
            p_net: p_net input

        Returns:
            Validated input model
        """
        return Preconstruction_CostInput(land_cost=land_cost, n_mod_in=n_mod_in, fixed_precon=fixed_precon, ref_net_power=ref_net_power, land_intensity=land_intensity, p_net=p_net)

    def run(
        self, land_cost: float, n_mod_in: float, fixed_precon: float, ref_net_power: float, land_intensity: float, p_net: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            land_cost: land_cost input
            n_mod_in: n_mod_in input
            fixed_precon: fixed_precon input
            ref_net_power: ref_net_power input
            land_intensity: land_intensity input
            p_net: p_net input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(land_cost, n_mod_in, fixed_precon, ref_net_power, land_intensity, p_net)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.preconstruction_cost_impl import (
            run_preconstruction_cost,
        )

        # Execute implementation - returns single value
        cost = run_preconstruction_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
